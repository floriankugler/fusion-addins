"""Write a nesting job from an exported parts file (export_parts.py).

    .venv/bin/python experiments/nesting/jobs.py out/parts/all/birch_15.json \
        --sheets 2500x1250 --out out/jobs/b15.json --rotations 2 --spacing 10

One sheet size: the job's bin is that rectangle, and SVGnest opens as many
of them as it needs. Several sheets (`--sheets 1000x800 2500x1250 ...`): the
bin is one polygon made of them, Multi Arrange's trick: the sheets stand
side by side, `--gap` apart, bottom-aligned, joined along their bottom edge
by bridges `--bridge` mm high, too thin for a part to cross. SVGnest
still opens more copies of that whole polygon when the parts do not fit.

Grain (`--grain long`): every part is first turned so that its longer side
lies along x, the sheet's length, as the grain of birch plywood runs; with
`--rotations 2` SVGnest may then only turn it by 180 degrees. `--grain free`
leaves the parts as they are.

Spacing (`--offset own`, the default): the parts are grown here by half
the spacing, mitred, and simplified by `--simplify` (the grown outline still
contains the part grown by half the spacing), each sheet is shrunk by the
margin less half the spacing, and SVGnest gets a spacing of 0. SVGnest's
own spacing (`--offset svgnest`) rounds every convex corner, which makes a
rectangle 20 vertices and its no-fit polygons far slower, and its inward
offset of the bin is skipped when it does not give one polygon (a bridged
bin); its margin is the spacing. The job keeps each part's true rings for
check.py.

Parts that fit none of the sheets either way round are left out and
listed (they would be `.nest(False)`).
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from shapely import Polygon, box, union_all
from shapely import affinity
from shapely.geometry.polygon import orient


def parse_sheet(s: str) -> tuple[float, float, int]:
    """`2500x1250` (as many as needed) or `2500x1250*2` (two of them)."""
    size, _, count = s.lower().partition("*")
    w, h = size.split("x")
    return float(w), float(h), int(count) if count else -1


def bridged(sheets: list[tuple[float, float]], gap: float, bridge: float,
            inset: float) -> tuple[Polygon, list[list[float]]]:
    """The sheets side by side, bottom-aligned, each shrunk by `inset`,
    joined by thin bridges along the bottom; and each sheet's rectangle
    [x0, y0, x1, y1]."""
    rects, pieces, x = [], [], 0.0
    for i, (w, h) in enumerate(sheets):
        rects.append([x, 0.0, x + w, h])
        pieces.append(box(x + inset, inset, x + w - inset, h - inset))
        if i < len(sheets) - 1:
            pieces.append(box(x + w - inset - 1, inset, x + w + gap + inset + 1, inset + bridge))
        x += w + gap
    shape = union_all(pieces)
    assert isinstance(shape, Polygon)
    return orient(shape), rects


def rings_of(p: Polygon) -> list[list[list[float]]]:
    def r(c) -> list[list[float]]:
        return [[round(x, 4), round(y, 4)] for x, y in list(c.coords)[:-1]]
    return [r(p.exterior)] + [r(i) for i in p.interiors]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("parts", type=Path, nargs="+", help="parts files; their parts are pooled")
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--sheets", nargs="+", default=["2500x1250"])
    ap.add_argument("--bin-polygon", default=None,
                    help='the bin as "x,y x,y ..." (an offcut), instead of --sheets')
    ap.add_argument("--gap", type=float, default=100.0)
    ap.add_argument("--bridge", type=float, default=1.0)
    ap.add_argument("--grain", choices=["long", "free"], default="long")
    ap.add_argument("--copies", type=int, default=1, help="each part this many times")
    ap.add_argument("--only", nargs="*", default=None, help="keep parts whose id starts with one of these")
    ap.add_argument("--spacing", type=float, default=10.0, help="between parts, mm")
    ap.add_argument("--margin", type=float, default=None, help="to the sheet's edge, mm (default: the spacing)")
    ap.add_argument("--offset", choices=["own", "svgnest"], default="own")
    ap.add_argument("--simplify", type=float, default=0.5, help="mm, with --offset own")
    ap.add_argument("--rotations", type=int, default=2)
    ap.add_argument("--population", type=int, default=10)
    ap.add_argument("--mutation", type=int, default=10)
    ap.add_argument("--holes", action="store_true", help="SVGnest useHoles: parts into other parts' holes")
    ap.add_argument("--concave", action="store_true", help="SVGnest exploreConcave")
    ap.add_argument("--curve-tolerance", type=float, default=0.05)
    ap.add_argument("--patch", nargs="*", default=[], help="fixes nest.mjs applies to SVGnest (holes)")
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--evaluations", type=int, default=100)
    ap.add_argument("--seconds", type=float, default=60.0)
    a = ap.parse_args()

    sheet_types = [parse_sheet(s) for s in a.sheets]
    sheets = [(w, h) for w, h, _n in sheet_types]
    margin = a.spacing if a.margin is None else a.margin
    own = a.offset == "own"
    if own:
        inset, grow, solver_spacing = margin - a.spacing / 2, a.spacing / 2, 0.0
    else:
        if margin != a.spacing:
            ap.error("with --offset svgnest the margin is the spacing")
        inset, grow, solver_spacing = 0.0, 0.0, a.spacing
    if a.bin_polygon:
        outline = Polygon([tuple(float(v) for v in xy.split(",")) for xy in a.bin_polygon.split()])
        inner = outline.buffer(-inset, join_style="mitre") if inset else outline
        assert isinstance(inner, Polygon)
        bin_shape, rects = orient(inner), [list(outline.bounds)]
        sheets = [(outline.bounds[2] - outline.bounds[0], outline.bounds[3] - outline.bounds[1])]
    elif len(sheets) == 1:
        w, h = sheets[0]
        bin_shape, rects = orient(box(inset, inset, w - inset, h - inset)), [[0.0, 0.0, w, h]]
    else:
        bin_shape, rects = bridged(sheets, a.gap, a.bridge, inset)

    parts, left_out = [], []
    material = None
    docs = [json.loads(f.read_text()) for f in a.parts]
    # Examples share part paths (floor.batten0): prefix ids with their example
    # when the parts come from several.
    sources = {p.get("source") for doc in docs for p in doc["parts"]}
    for doc in docs:
        material = material or doc["material"]
        for p in doc["parts"]:
            if a.only is not None and not any(p["id"].startswith(o) for o in a.only):
                continue
            poly = Polygon(p["rings"][0], p["rings"][1:])
            x0, y0, x1, y1 = poly.bounds
            turned = 0
            if a.grain == "long" and (y1 - y0) > (x1 - x0):
                poly, turned = affinity.rotate(poly, 90, origin=(0, 0)), 90
            x0, y0, x1, y1 = poly.bounds
            w, h = x1 - x0, y1 - y0
            w, h = w + 2 * margin, h + 2 * margin
            fits = any((w <= sw and h <= sh) if a.grain == "long" or a.rotations < 4
                       else (w <= sw and h <= sh) or (w <= sh and h <= sw) for sw, sh in sheets)
            if not fits:
                left_out.append(f"{p['id']} {w:.0f} x {h:.0f}")
                continue
            solver_poly = poly
            if own:
                solver_poly = poly.buffer(grow + 1.5 * a.simplify, join_style="mitre", mitre_limit=10)
                solver_poly = solver_poly.simplify(a.simplify, preserve_topology=True)
                assert solver_poly.buffer(1e-6).contains(poly.buffer(grow, join_style="mitre", mitre_limit=10))
            for c in range(a.copies):
                prefix = f"{p['source']}:" if len(sources) > 1 else ""
                parts.append({
                    "id": prefix + p["id"] + (f"@{c + 1}" if a.copies > 1 else ""),
                    "source": p.get("source"),
                    "area": p["area"],
                    "turned": turned,
                    "rings": rings_of(orient(solver_poly)),
                    "check_rings": rings_of(orient(poly)),
                })

    job = {
        "material": material,
        "sheets": [list(s) for s in sheets],
        # For solvers that take sheet types (ps_nest.py); copies -1: as many as needed.
        "sheet_types": [{"width": w, "height": h, "copies": n} for w, h, n in sheet_types],
        "sheet_rects": rects,
        "offcut": [list(c) for c in list(Polygon([tuple(float(v) for v in xy.split(",")) for xy in a.bin_polygon.split()]).exterior.coords)[:-1]] if a.bin_polygon else None,
        "grain": a.grain,
        "spacing": a.spacing, "margin": margin, "offset": a.offset,
        "left_out": left_out,
        "parts": parts,
        "bin": {"rings": rings_of(bin_shape)},
        "config": {
            "spacing": solver_spacing, "rotations": a.rotations,
            "populationSize": a.population, "mutationRate": a.mutation,
            "useHoles": a.holes, "exploreConcave": a.concave,
            "curveTolerance": a.curve_tolerance,
        },
        "patches": a.patch,
        "seed": a.seed, "evaluations": a.evaluations, "seconds": a.seconds,
    }
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps(job, indent=1))
    area = sum(p["area"] for p in parts) / 1e6
    verts = sum(len(p["rings"][0]) for p in parts)
    print(f"{a.out}: {len(parts)} parts ({verts} vertices), {area:.2f} m2 on {' + '.join(a.sheets)}"
          + (f"; left out {len(left_out)}: {', '.join(left_out)}" if left_out else ""))


if __name__ == "__main__":
    main()
