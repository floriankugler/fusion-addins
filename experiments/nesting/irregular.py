"""Irregular parts, less like rectangles than the examples' boards, as a
parts file (the format of export_parts.py, with arcs):

- `ring`: a round frame, 900 across with a 700 opening, and discs that fit
  in the opening (600) and next to it (300, 180);
- `rail`: curved rails, ring sectors 820 to 900 radius over 70 degrees;
- `wave`: shelves 1200 long with a wavy front (two periods, 250 +- 60 deep);
- `rocker`: rocker runners, a crescent between two arcs, 900 long;
- `bracket`: shelf brackets with a coved hypotenuse (an arc, concave);
- `lbracket`: L brackets with rounded corners;
- `oval`: oval trays, 500 x 320;
- `blob`: random star-shaped polygons, concave;
- `side`: chair sides, a concave polygon with a raked back.

Each part has its outline three ways: `arcs` (lines and true circular arcs,
for PackingSolver: points `[x, y]`, an arc's centre `[cx, cy, 1]`
counter-clockwise or `[cx, cy, -1]` clockwise between the points it
joins, or `{"circle": [cx, cy, r]}`), `true_rings` (finely sampled, chord
error 0.01 mm, for the checks) and `rings` (sampled, then grown and
simplified like export_parts.py, so that it contains the part, for solvers
that take polygons).

    .venv/bin/python experiments/nesting/irregular.py --out experiments/nesting/out/parts/cases
"""
from __future__ import annotations

import argparse
import json
import math
import random
from pathlib import Path

from shapely import Polygon
from shapely.geometry.polygon import orient

from export_parts import rings_of, simplified

FINE = 0.01


class Path2:
    """A closed outline of lines and arcs, starting at `start`; the last
    element runs back to the start (a line)."""

    def __init__(self, x: float, y: float):
        self.elements: list[list[float]] = [[x, y]]

    def line(self, x: float, y: float) -> Path2:
        self.elements.append([x, y])
        return self

    def arc(self, x: float, y: float, cx: float, cy: float, ccw: bool) -> Path2:
        self.elements.append([cx, cy, 1 if ccw else -1])
        self.elements.append([x, y])
        return self

    def sampled(self, tol: float = FINE) -> list[tuple[float, float]]:
        pts: list[tuple[float, float]] = [(self.elements[0][0], self.elements[0][1])]
        i = 1
        while i < len(self.elements):
            e = self.elements[i]
            if len(e) == 3:
                end = self.elements[i + 1]
                pts.extend(arc_points(pts[-1], (end[0], end[1]), (e[0], e[1]), e[2] > 0, tol)[1:])
                i += 2
            else:
                pts.append((e[0], e[1]))
                i += 1
        return pts


def arc_points(a, b, c, ccw: bool, tol: float) -> list[tuple[float, float]]:
    r = math.dist(a, c)
    t0 = math.atan2(a[1] - c[1], a[0] - c[0])
    t1 = math.atan2(b[1] - c[1], b[0] - c[0])
    sweep = t1 - t0
    if ccw and sweep <= 0:
        sweep += 2 * math.pi
    if not ccw and sweep >= 0:
        sweep -= 2 * math.pi
    step = 2 * math.acos(max(-1.0, 1 - tol / r))
    n = max(2, math.ceil(abs(sweep) / step))
    return [(c[0] + r * math.cos(t0 + sweep * k / n), c[1] + r * math.sin(t0 + sweep * k / n)) for k in range(n + 1)]


def circle_points(cx: float, cy: float, r: float, tol: float = FINE) -> list[tuple[float, float]]:
    n = max(8, math.ceil(2 * math.pi / (2 * math.acos(1 - tol / r))))
    return [(cx + r * math.cos(2 * math.pi * k / n), cy + r * math.sin(2 * math.pi * k / n)) for k in range(n)]


def entry(pid: str, poly: Polygon, arcs: list | None, tolerance: float) -> dict:
    poly = orient(poly)
    assert poly.is_valid, pid
    simple = simplified(poly, tolerance)
    x0, y0, x1, y1 = poly.bounds
    return {"id": pid, "source": "irregular", "thickness": 15, "grained": True, "grain": None,
            "area": poly.area, "size": [x1 - x0, y1 - y0],
            "vertices_true": len(poly.exterior.coords) - 1, "vertices": len(simple.exterior.coords) - 1,
            "rings": rings_of(simple), "true_rings": rings_of(poly), "arcs": arcs}


def parts(tolerance: float, seed: int = 7) -> list[dict]:
    out = []
    # A round frame and discs.
    ring = Polygon(circle_points(0, 0, 450), [circle_points(0, 0, 350)])
    out.append(entry("ring", ring, [{"circle": [0, 0, 450]}, {"circle": [0, 0, 350]}], tolerance))
    for i, r in enumerate([300, 150, 150, 150, 90, 90, 90, 90]):
        out.append(entry(f"disc{2 * r}_{i}", Polygon(circle_points(0, 0, r)), [{"circle": [0, 0, r]}], tolerance))
    # Curved rails: ring sectors.
    ro, ri, sweep = 900.0, 820.0, math.radians(70)
    for i in range(6):
        p = (Path2(ro, 0).arc(ro * math.cos(sweep), ro * math.sin(sweep), 0, 0, True)
             .line(ri * math.cos(sweep), ri * math.sin(sweep)).arc(ri, 0, 0, 0, False))
        out.append(entry(f"rail{i}", Polygon(p.sampled()), [p.elements], tolerance))
    # Wavy shelves (no arcs: sampled sine).
    for i in range(4):
        front = [(x, 250 + 60 * math.sin(2 * math.pi * x / 600)) for x in [1200 * k / 240 for k in range(241)]]
        poly = Polygon([(0, 0), (1200, 0)] + front[::-1])
        out.append(entry(f"wave{i}", poly, None, tolerance))
    # Rocker runners: a crescent between two arcs bulging down.
    c, s1, s2 = 900.0, 60.0, 20.0
    r1, r2 = (c * c / 4 + s1 * s1) / (2 * s1), (c * c / 4 + s2 * s2) / (2 * s2)
    for i in range(4):
        p = (Path2(0, 0).arc(c, 0, c / 2, r1 - s1, True).line(c, 40)
             .arc(0, 40, c / 2, 40 - s2 + r2, False))
        out.append(entry(f"rocker{i}", Polygon(p.sampled()), [p.elements], tolerance))
    # Shelf brackets with a coved hypotenuse.
    for i in range(6):
        p = Path2(0, 0).line(300, 0).line(300, 40).arc(40, 300, 300, 300, False).line(0, 300)
        out.append(entry(f"bracket{i}", Polygon(p.sampled()), [p.elements], tolerance))
    # L brackets, rounded (polygons from shapely).
    lshape = Polygon([(0, 0), (400, 0), (400, 80), (80, 80), (80, 300), (0, 300)])
    lround = lshape.buffer(-30, quad_segs=64).buffer(30, quad_segs=64).buffer(25, quad_segs=64).buffer(-25, quad_segs=64)
    for i in range(4):
        out.append(entry(f"lbracket{i}", lround, None, tolerance))
    # Ovals.
    oval = Polygon([(250 * math.cos(t), 160 * math.sin(t)) for t in [2 * math.pi * k / 720 for k in range(720)]])
    for i in range(2):
        out.append(entry(f"oval{i}", oval, None, tolerance))
    # Random star-shaped polygons.
    rnd = random.Random(seed)
    for i in range(8):
        n = rnd.randint(7, 12)
        rmax = rnd.uniform(150, 320)
        angles = sorted(rnd.uniform(0, 2 * math.pi) for _ in range(n))
        pts = [(math.cos(a) * rnd.uniform(0.45, 1) * rmax, math.sin(a) * rnd.uniform(0.45, 1) * rmax) for a in angles]
        poly = Polygon(pts)
        if not poly.is_valid:
            poly = poly.buffer(0)
        out.append(entry(f"blob{i}", poly, None, tolerance))
    # Chair sides: a concave polygon with a raked back.
    side = Polygon([(0, 0), (60, 0), (80, 330), (380, 330), (400, 0), (460, 0), (450, 420),
                    (170, 440), (230, 820), (150, 830), (60, 440), (0, 420)])
    for i in range(2):
        out.append(entry(f"side{i}", side, None, tolerance))
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--tolerance", type=float, default=0.25)
    a = ap.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)
    ps = parts(a.tolerance)
    (a.out / "irregular.json").write_text(json.dumps({"material": "irregular", "tolerance": a.tolerance, "parts": ps}, indent=1))
    area = sum(p["area"] for p in ps) / 1e6
    print(f"irregular: {len(ps)} parts, {area:.2f} m2, vertices {sum(p['vertices_true'] for p in ps)} "
          f"-> {sum(p['vertices'] for p in ps)}")


if __name__ == "__main__":
    main()
