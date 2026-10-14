"""Synthetic parts files for the quirks (same format as export_parts.py):

- `squares`: twelve 400 x 400 squares, more than one 1000 x 500 sheet holds.
- `frame`: a 1200 x 800 frame with a 1000 x 600 opening, and small parts
  that fit in the opening.
- `mixed`: rectangles, L shapes and triangles of assorted sizes.
- `faceframe`: a cabinet's face frame, 1400 x 720 with a 1300 x 620
  opening (inner corners rounded 6 for the cutter), to nest with the van.

    .venv/bin/python experiments/nesting/cases.py --out experiments/nesting/out/parts/cases
"""
from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

from shapely import Polygon, box
from shapely.geometry.polygon import orient


def part(pid: str, poly: Polygon) -> dict:
    poly = orient(poly)
    rings = [[[round(x, 4), round(y, 4)] for x, y in list(r.coords)[:-1]] for r in [poly.exterior, *poly.interiors]]
    x0, y0, x1, y1 = poly.bounds
    return {"id": pid, "source": "cases", "thickness": 15, "grained": True, "grain": None, "area": poly.area,
            "size": [x1 - x0, y1 - y0], "vertices_true": len(rings[0]), "vertices": len(rings[0]), "rings": rings}


def squares() -> list[dict]:
    return [part(f"sq{i}", box(0, 0, 400, 400)) for i in range(12)]


def frame() -> list[dict]:
    out = [part("frame", Polygon([(0, 0), (1200, 0), (1200, 800), (0, 800)],
                                 [[(100, 100), (100, 700), (1100, 700), (1100, 100)]]))]
    out += [part(f"small{i}", box(0, 0, 300, 200)) for i in range(6)]
    return out


def mixed(seed: int = 3) -> list[dict]:
    rnd = random.Random(seed)
    out = []
    for i in range(10):
        out.append(part(f"rect{i}", box(0, 0, rnd.randint(200, 900), rnd.randint(100, 500))))
    for i in range(6):
        w, h, t = rnd.randint(300, 700), rnd.randint(300, 600), rnd.randint(80, 150)
        out.append(part(f"L{i}", Polygon([(0, 0), (w, 0), (w, t), (t, t), (t, h), (0, h)])))
    for i in range(6):
        w, h = rnd.randint(200, 600), rnd.randint(200, 500)
        out.append(part(f"tri{i}", Polygon([(0, 0), (w, 0), (0, h)])))
    return out


def faceframe() -> list[dict]:
    opening = box(50, 50, 1350, 670).buffer(-6, join_style="mitre").buffer(6, quad_segs=16)
    return [part("faceframe", Polygon(box(0, 0, 1400, 720).exterior.coords, [opening.exterior.coords]))]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)
    for name, parts in [("squares", squares()), ("frame", frame()), ("mixed", mixed()), ("faceframe", faceframe())]:
        (a.out / f"{name}.json").write_text(json.dumps({"material": name, "tolerance": 0, "parts": parts}, indent=1))
        print(name, len(parts), "parts")


if __name__ == "__main__":
    main()
