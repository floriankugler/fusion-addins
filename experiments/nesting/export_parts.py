"""Turn layout files into nesting input: one JSON file per material with
each part's machine outline (its outline less its through cuts), simplified
so that it never cuts into the part.

    .venv/bin/python experiments/nesting/export_parts.py out/van/layout.json \
        --out experiments/nesting/out/parts --tolerance 0.25

A part's outline is in its own (u, v) plane, mm. Simplifying is
conservative: the outline is grown by 1.5 x `tolerance` (mitred, so
rectangles stay rectangles), then simplified by `tolerance`. The result
contains the true outline (checked) and lies at most about 2.5 x `tolerance`
outside it.

Each file also gets an SVG with the parts in a row and a 2500 x 1250 sheet,
to drop into SVGnest's own page.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from shapely import Polygon, MultiPolygon, union_all
from shapely.geometry.polygon import orient


def ring_area(ring: list[list[float]]) -> float:
    a = 0.0
    for (x0, y0), (x1, y1) in zip(ring, ring[1:] + ring[:1]):
        a += x0 * y1 - x1 * y0
    return a / 2


def polygons(rings: list[list[list[float]]]) -> list[Polygon]:
    """Rings as the layout writes them: an exterior (counter-clockwise),
    then its holes (clockwise), then the next polygon."""
    out: list[Polygon] = []
    shell: list[list[float]] | None = None
    holes: list[list[list[float]]] = []
    for ring in rings:
        if ring_area(ring) > 0:
            if shell is not None:
                out.append(Polygon(shell, holes))
            shell, holes = ring, []
        else:
            holes.append(ring)
    if shell is not None:
        out.append(Polygon(shell, holes))
    return out


def machine_outline(part: dict) -> Polygon | MultiPolygon:
    shape = union_all(polygons(part["outline"]))
    cuts = [p for op in part["ops"] if op["kind"] == "cut" for p in polygons(op["shape"])]
    if cuts:
        shape = shape.difference(union_all(cuts))
    return shape


def simplified(shape: Polygon, tolerance: float) -> Polygon:
    # Grown by more than the simplification is asked to move a point: the
    # topology preserving simplifier moved a cutout's hole 0.286 mm at
    # tolerance 0.25.
    grown = shape.buffer(1.5 * tolerance, join_style="mitre", mitre_limit=10)
    out = grown.simplify(tolerance, preserve_topology=True)
    assert isinstance(out, Polygon), type(out)
    assert out.buffer(1e-6).contains(shape), "simplified outline cuts into the part"
    return orient(out)


def rings_of(p: Polygon) -> list[list[list[float]]]:
    def r(c) -> list[list[float]]:
        return [[round(x, 4), round(y, 4)] for x, y in list(c.coords)[:-1]]
    return [r(p.exterior)] + [r(i) for i in p.interiors]


def svg_path(p: Polygon, dx: float, dy: float) -> str:
    d = []
    for ring in [p.exterior, *p.interiors]:
        pts = list(ring.coords)[:-1]
        d.append("M " + " L ".join(f"{x + dx:.3f} {y + dy:.3f}" for x, y in pts) + " Z")
    return " ".join(d)


def export(layouts: list[Path], out: Path, tolerance: float, sheet: tuple[float, float]) -> None:
    by_material: dict[str, list[dict]] = {}
    for path in layouts:
        layout = json.loads(path.read_text())
        for module in layout["modules"]:
            for part in module["parts"]:
                shape = machine_outline(part)
                pieces = list(shape.geoms) if isinstance(shape, MultiPolygon) else [shape]
                for k, piece in enumerate(pieces):
                    simple = simplified(piece, tolerance)
                    x0, y0, x1, y1 = simple.bounds
                    by_material.setdefault(part["material"], []).append({
                        "id": part["path"] + (f"#{k}" if len(pieces) > 1 else ""),
                        "source": path.parent.name,
                        "thickness": part["thickness"],
                        "grained": part["grained"],
                        "grain": part["grain"],
                        "area": piece.area,
                        "size": [x1 - x0, y1 - y0],
                        "vertices_true": len(piece.exterior.coords) - 1,
                        "vertices": len(simple.exterior.coords) - 1,
                        "rings": rings_of(simple),
                    })
    out.mkdir(parents=True, exist_ok=True)
    for material, parts in sorted(by_material.items()):
        name = material.replace(" ", "_")
        doc = {"material": material, "tolerance": tolerance, "parts": parts}
        (out / f"{name}.json").write_text(json.dumps(doc, indent=1))
        write_svg(out / f"{name}.svg", parts, sheet)
        total = sum(p["area"] for p in parts) / 1e6
        print(f"{material}: {len(parts)} parts, {total:.2f} m2 "
              f"({total / (sheet[0] * sheet[1] / 1e6):.2f} sheets), "
              f"vertices {sum(p['vertices_true'] for p in parts)} -> {sum(p['vertices'] for p in parts)}")
        for p in parts:
            w, h = p["size"]
            if not ((w <= sheet[0] and h <= sheet[1]) or (w <= sheet[1] and h <= sheet[0])):
                print(f"  too large for the sheet: {p['id']} {w:.0f} x {h:.0f}", file=sys.stderr)


def write_svg(path: Path, parts: list[dict], sheet: tuple[float, float]) -> None:
    """The sheet first (SVGnest's page asks which shape is the bin), then the
    parts in a row below it."""
    items = [f'<rect id="sheet" x="0" y="0" width="{sheet[0]}" height="{sheet[1]}" fill="none" stroke="black"/>']
    x, y, row = 0.0, sheet[1] + 50, 0.0
    for p in parts:
        poly = Polygon(p["rings"][0], p["rings"][1:])
        x0, y0, x1, y1 = poly.bounds
        if x + (x1 - x0) > 4 * sheet[0]:
            x, y, row = 0.0, y + row + 20, 0.0
        items.append(f'<path id="{p["id"]}" d="{svg_path(poly, x - x0, y - y0)}" fill="none" stroke="blue"/>')
        x += (x1 - x0) + 20
        row = max(row, y1 - y0)
    width, height = 4 * sheet[0], y + row
    path.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width / 5:.0f}" height="{height / 5:.0f}" '
                    f'viewBox="0 0 {width:.0f} {height:.0f}">\n' + "\n".join(items) + "\n</svg>\n")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("layouts", nargs="+", type=Path)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--tolerance", type=float, default=0.25)
    ap.add_argument("--sheet", type=float, nargs=2, default=(2500.0, 1250.0))
    a = ap.parse_args()
    export(a.layouts, a.out, a.tolerance, tuple(a.sheet))


if __name__ == "__main__":
    main()
