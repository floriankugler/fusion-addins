"""Check a nesting result against its job, independently of the solver, and
draw it.

    .venv/bin/python experiments/nesting/check.py job.json result.json --svg nest.svg

Each placed part is rebuilt from the job's true rings (`check_rings`, the
exported outline, which contains the part's outline) with the result's rotation and translation, then measured with
shapely: overlaps between parts, the smallest gap between two parts and to
the edge of the sheet, the sheet each part lies on (a part on a bridge or
across two sheets of a bridged bin is reported), the turns used, and how
much of the sheets used the parts cover. The checks print one line each and
`--json` writes them for the summaries.
"""
from __future__ import annotations

import argparse
import json
import math
from collections import Counter
from pathlib import Path

from shapely import Polygon, STRtree, box
from shapely import affinity


def placed_shape(part: dict, rotation: float, translation: list[float]) -> Polygon:
    rings = part.get("check_rings", part["rings"])
    poly = Polygon(rings[0], rings[1:])
    poly = affinity.rotate(poly, rotation, origin=(0, 0))
    return affinity.translate(poly, translation[0], translation[1])


def check(job: dict, result: dict) -> tuple[dict, list[tuple[int, int, dict, Polygon]]]:
    parts = job["parts"]
    bin_poly = Polygon(job["bin"]["rings"][0])
    rects = [box(*r) for r in job["sheet_rects"]]
    if job.get("offcut"):
        rects = [Polygon(job["offcut"])]
    spacing = job.get("spacing", job["config"]["spacing"])
    rotations = job["config"]["rotations"]
    allowed = {round(i * 360 / rotations, 6) % 360 for i in range(rotations)}

    placed: list[tuple[int, int, dict, Polygon]] = []  # (bin, sheet, part, shape)
    problems: list[str] = []
    for b, entry in enumerate(result["bins"]):
        # SVGnest: a bin is a copy of the job's bin polygon, a list of items.
        # PackingSolver: a bin is one sheet of the job, in its own coordinates.
        items = entry["items"] if isinstance(entry, dict) else entry
        own_sheet = entry["sheet"] if isinstance(entry, dict) else None
        for item in items:
            part = parts[item["index"]]
            shape = placed_shape(part, item["rotation"], item["translation"])
            if round(item["rotation"], 6) % 360 not in allowed:
                problems.append(f"{part['id']}: turned {item['rotation']} (allowed {sorted(allowed)})")
            if own_sheet is not None:
                w, h = job["sheets"][own_sheet]
                if not shape.within(box(0, 0, w, h).buffer(1e-6)):
                    problems.append(f"{part['id']}: off its {w:g} x {h:g} sheet")
                placed.append((b, own_sheet, part, shape))
                continue
            if not shape.within(bin_poly.buffer(1e-6)):
                problems.append(f"{part['id']}: outside the bin by {shape.difference(bin_poly).area:.3f} mm2")
            sheet = next((i for i, r in enumerate(rects) if shape.within(r.buffer(1e-6))), -1)
            if sheet < 0:
                problems.append(f"{part['id']}: on no single sheet (bridge or across sheets)")
            placed.append((b, sheet, part, shape))

    # Gaps: between parts on one bin, and from each part to its sheet's edge.
    min_gap, min_edge, overlaps = math.inf, math.inf, 0
    by_bin: dict[int, list[Polygon]] = {}
    for b, _s, _p, shape in placed:
        by_bin.setdefault(b, []).append(shape)
    for shapes in by_bin.values():
        tree = STRtree(shapes)
        for i, s in enumerate(shapes):
            for j in tree.query(s, predicate="dwithin", distance=max(4 * spacing, 50)):
                if j <= i:
                    continue
                inter = s.intersection(shapes[j]).area
                if inter > 1e-3:
                    overlaps += 1
                min_gap = min(min_gap, s.distance(shapes[j]))
    own = isinstance(result["bins"][0], dict) if result["bins"] else False

    def sheet_rect(sheet: int) -> Polygon:
        if own:
            w, h = job["sheets"][sheet]
            return box(0, 0, w, h)
        return rects[sheet]

    for _b, sheet, _p, shape in placed:
        if sheet >= 0:
            min_edge = min(min_edge, sheet_rect(sheet).exterior.distance(shape))
    if overlaps:
        problems.append(f"{overlaps} overlapping pairs")

    # Sheets used, cover, and how far along x the parts reach on each.
    used = Counter((b, s) for b, s, _p, _sh in placed if s >= 0)
    sheet_area = sum(sheet_rect(s).area for _b, s in used)
    part_area = sum(p["area"] for _b, _s, p, _sh in placed)
    reach = {}
    for (b, s) in used:
        xs = [sh.bounds[2] for bb, ss, _p, sh in placed if (bb, ss) == (b, s)]
        reach[f"{b}.{s}"] = round(max(xs) - sheet_rect(s).bounds[0], 1)
    turns = Counter(round(item["rotation"]) for entry in result["bins"]
                    for item in (entry["items"] if isinstance(entry, dict) else entry))
    summary = {
        "parts": len(parts), "placed": len(placed), "unplaced": len(result["unplaced"]),
        "bins": len(result["bins"]), "sheets_used": len(used),
        "sheet_sizes": [f"{job['sheets'][s][0]:g}x{job['sheets'][s][1]:g}" for _b, s in sorted(used)] if own else None,
        "cover": round(part_area / sheet_area, 4) if sheet_area else 0,
        "min_gap": round(min_gap, 3) if min_gap < math.inf else None,
        "min_edge": round(min_edge, 3) if min_edge < math.inf else None,
        "reach_x": reach, "turns": dict(turns),
        "evaluations": result.get("evaluations"), "seconds": round(result.get("seconds", 0), 2),
        "best_at": result.get("bestAt"),
        "problems": problems,
    }
    return summary, placed


def svg(job: dict, result: dict, placed: list[tuple[int, int, dict, Polygon]], path: Path) -> None:
    """One row per bin: SVGnest's copies of the job's bin polygon (with the
    sheets in it), or PackingSolver's sheets, each its own size."""
    bin_poly = Polygon(job["bin"]["rings"][0])
    rows: list[tuple[list[Polygon], Polygon | None]] = []  # (outlines, background)
    for entry in result["bins"] or [[]]:
        if isinstance(entry, dict):
            w, h = job["sheets"][entry["sheet"]]
            rows.append(([box(0, 0, w, h)], box(0, 0, w, h)))
        else:
            rows.append(([box(*r) for r in job["sheet_rects"]], bin_poly))
    pad = 60
    x0 = min(min(o.bounds[0] for o in outs) for outs, _bg in rows)
    x1 = max(max(o.bounds[2] for o in outs) for outs, _bg in rows)
    heights = [max(o.bounds[3] for o in outs) for outs, _bg in rows]
    total_h = sum(h + pad for h in heights) + pad
    w = x1 - x0
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0 - pad} 0 {w + 2 * pad} {total_h}" '
           f'width="{(w + 2 * pad) / 4:.0f}" height="{total_h / 4:.0f}" font-family="sans-serif">',
           '<rect x="-1e5" y="-1e5" width="2e5" height="2e5" fill="#fff"/>']

    def path_d(p: Polygon, dy: float) -> str:
        d = []
        for ring in [p.exterior, *p.interiors]:
            pts = list(ring.coords)[:-1]
            d.append("M " + " L ".join(f"{x:.2f} {dy - y:.2f}" for x, y in pts) + " Z")
        return " ".join(d)

    top = pad
    for b, ((outlines, background), h) in enumerate(zip(rows, heights)):
        dy = top + h  # y up: a point (x, y) is drawn at dy - y
        top += h + pad
        if background is not None:
            out.append(f'<path d="{path_d(background, dy)}" fill="#f3efe6" stroke="#888" stroke-width="2"/>')
        for o in outlines:
            out.append(f'<path d="{path_d(o, dy)}" fill="none" stroke="#444" stroke-width="3"/>')
        for bb, _s, part, shape in placed:
            if bb != b:
                continue
            out.append(f'<path d="{path_d(shape, dy)}" fill="#7aa6d8" fill-opacity="0.75" '
                       f'fill-rule="evenodd" stroke="#1d4f8a" stroke-width="1.5"/>')
            c = shape.representative_point()
            size = max(10, min(40, math.sqrt(shape.area) / 6))
            out.append(f'<text x="{c.x:.1f}" y="{dy - c.y:.1f}" font-size="{size:.0f}" text-anchor="middle" '
                       f'dominant-baseline="middle" fill="#102a4a">{part["id"]}</text>')
    out.append("</svg>")
    path.write_text("\n".join(out))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("job", type=Path)
    ap.add_argument("result", type=Path)
    ap.add_argument("--svg", type=Path)
    ap.add_argument("--json", type=Path)
    a = ap.parse_args()
    job = json.loads(a.job.read_text())
    result = json.loads(a.result.read_text())
    summary, placed = check(job, result)
    for k, v in summary.items():
        if k != "problems":
            print(f"{k}: {v}")
    for p in summary["problems"]:
        print("PROBLEM", p)
    if a.svg:
        svg(job, result, placed, a.svg)
    if a.json:
        a.json.write_text(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
