"""Corners of a board's outline, rounded or cut off: `board.fillet()` and
`board.chamfer()` on an edge through the board.

A corner of the outline is an edge of the board through its thickness,
where two narrow faces meet. Rounding it or cutting it off changes the
board's shape, so it is done to the outline, in 2D, as a cut is: everything
after it sees the new shape (contacts, crossings, the interference check,
dog bones, cutouts), the preview extrudes it, and the emitter draws it as
part of the outline, the arcs as arcs (`lang.emit.arcs.fit`), so Fusion
makes one cylindrical face per rounded corner and no fillet or chamfer
feature.

A corner is where two of the lines and arcs the outline stands for meet at
an angle (`cutouts.corner_points`), convex or concave: a fillet takes
material off a convex corner and adds it to a concave one, as
`Shape.rounded()` does to every corner of a shape. The arcs are worked out
on those lines and arcs, so they are exact and tangent to their
neighbours. A chamfer cuts a corner off by a straight line from `size`
before it to `size` after it along the outline.
"""
from __future__ import annotations

import math
from collections.abc import Callable, Sequence
from dataclasses import dataclass

from shapely.geometry import MultiPolygon, Point, Polygon

from .cutouts import chamfered, corner_points, filleted
from .errors import LangError
from .shapes import Shape

Point2 = tuple[float, float]
#: How close (mm) a corner must lie to a contour to be one of its corners.
#: Where a circle meets a line, the corner lies on the true circle, up to
#: the sagitta of the circle's polygon (half a percent of its radius) off it.
ON_CONTOUR = 0.05
#: How close (mm) a point must lie to a corner to name it.
_AT = 1e-6

#: Rounds or cuts off the polygon's corners at the given points; None when
#: they do not fit.
Change = Callable[[Polygon, Sequence[Point2]], Polygon | None]


@dataclass(frozen=True)
class Named:
    """A corner of the outline, as a build file named it (`label`, for
    messages)."""
    point: Point2
    label: str


def find(outline: Shape) -> list[tuple[Point2, bool]]:
    """Every corner of the outline, each with whether it lies on the outer
    boundary of its polygon (else on a hole, a through cut's contour)."""
    return [c for poly in outline.polygons() for c in corner_points(poly)]


def round_corners(outline: Shape, corners: Sequence[Named], r: float, path: str) -> Shape:
    """The outline with the corners named rounded with radius `r`."""
    return _changed(outline, corners, lambda poly, at: filleted(poly, r, at), f"fillet({r:g})", "arc", path)


def clip_corners(outline: Shape, corners: Sequence[Named], size: float, path: str) -> Shape:
    """The outline with the corners named cut off `size` along both their
    edges."""
    return _changed(outline, corners, lambda poly, at: chamfered(poly, size, at), f"chamfer({size:g})",
                    "chamfer", path)


def _changed(outline: Shape, corners: Sequence[Named], change: Change, what: str, kind: str,
             path: str) -> Shape:
    pieces: list[Polygon] = []
    for poly in outline.polygons():
        mine = [c for c in corners if poly.boundary.distance(Point(c.point)) <= _AT]
        if not mine:
            pieces.append(poly)
            continue
        out = change(poly, [c.point for c in mine])
        if out is None:
            raise LangError(f"{what}: {_why(poly, mine, change, kind)}.", path)
        pieces.append(out)
    geometry = pieces[0] if len(pieces) == 1 else MultiPolygon(pieces)
    return Shape(geometry, outline.axes)


def _why(poly: Polygon, corners: Sequence[Named], change: Change, kind: str) -> str:
    """Why the corners do not fit: a corner whose edges are too short for
    it, one whose arc runs into another contour of the outline, or two
    neighbours that need more than the edge between them."""
    rings = [Polygon(r) for r in [poly.exterior, *poly.interiors]]
    for c in corners:
        if change(poly, [c.point]) is not None:
            continue
        ring = next(r for r in rings if r.exterior.distance(Point(c.point)) <= _AT)
        if change(ring, [c.point]) is None:
            done = "rounded" if kind == "arc" else "chamfered"
            return f"an edge at {c.label} is too short for the {kind}, so the corner cannot be {done} with it"
        return f"the {kind} at {c.label} runs into another contour of the outline (a through cut near it)"
    for ring in rings:
        # neighbours around the ring, each pair alone
        order = [p for p, _ in corner_points(ring)]
        mine = sorted(((min(range(len(order)), key=lambda i: math.dist(order[i], c.point)), c)
                       for c in corners if ring.exterior.distance(Point(c.point)) <= _AT), key=lambda x: x[0])
        for (i, a), (j, b) in zip(mine, mine[1:] + mine[:1]):
            if a is not b and (j - i) % len(order) == 1 and change(poly, [a.point, b.point]) is None:
                return f"the {kind}s at {a.label} and {b.label} need more than the edge between them"
    labels = ", ".join(c.label for c in corners)
    return f"the {kind}s at {labels} do not fit together"
