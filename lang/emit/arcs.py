"""Arcs recovered from the layout's polygons.

The layout's shapes are polygons (shapely), but many of them stand for
curves: circles, the round ends of slots, rounded corners, offsets with
round joins. Each of those puts its vertices exactly on a circle, a few
degrees apart. `fit` finds such runs in a closed ring and returns the ring
as lines, arcs and full circles, so that the emitter draws true arcs, one
cylindrical face where the polygon would give a fan of small flat ones.

A run is an arc when at least `MIN_SEGMENTS` consecutive segments, each
turning by `MIN_STEP` to `MAX_STEP` about one centre, all have their ends
on one circle within `TOLERANCE`. The layout step's arcs pass easily: their
vertices lie on the circle to about 1e-12 mm. A coarse regular polygon (an
octagon turns 45 degrees a step) stays a polygon, and so does a curve
sampled finely with rounding noise, such as the master's contours (every
0.1 mm, rounded to 0.1 micrometre): too little turn per step, too much
noise. Plain Python, no Fusion.
"""
from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass

Point2 = tuple[float, float]

#: The largest turn per segment that still counts as part of an arc:
#: shapely's default of 8 segments per quarter circle turns 11.25 degrees.
MAX_STEP = math.radians(11.5)
#: The smallest turn per segment of an arc: finer polygons are samples of
#: curves, not arcs the layout made.
MIN_STEP = math.radians(0.5)
#: The fewest segments that make an arc. With three, rounding noise in a
#: finely sampled small curve now and then lines up by chance.
MIN_SEGMENTS = 4
#: How far (mm) a vertex may lie off the circle.
TOLERANCE = 1e-7


@dataclass(frozen=True)
class Line2:
    a: Point2
    b: Point2


@dataclass(frozen=True)
class Arc2:
    """From `a` through `mid` to `b` about `center`; `mid` is one of the
    polygon's vertices between the two."""
    a: Point2
    mid: Point2
    b: Point2
    center: Point2
    radius: float


@dataclass(frozen=True)
class Circle2:
    center: Point2
    radius: float


Curve2 = Line2 | Arc2 | Circle2


def _circumcircle(p: Point2, q: Point2, r: Point2) -> tuple[Point2, float] | None:
    """The circle through three points, or None when they are collinear.
    Worked out relative to `p`, which keeps the precision for points close
    together far from the origin."""
    bx, by = q[0] - p[0], q[1] - p[1]
    cx, cy = r[0] - p[0], r[1] - p[1]
    d = 2 * (bx * cy - by * cx)
    if abs(d) < 1e-15:
        return None
    b2, c2 = bx * bx + by * by, cx * cx + cy * cy
    ux = (cy * b2 - by * c2) / d
    uy = (bx * c2 - cx * b2) / d
    return (p[0] + ux, p[1] + uy), math.hypot(ux, uy)


def _turn(center: Point2, p: Point2, q: Point2) -> float:
    """The signed angle from `p` to `q` about `center`."""
    ax, ay = p[0] - center[0], p[1] - center[1]
    bx, by = q[0] - center[0], q[1] - center[1]
    return math.atan2(ax * by - ay * bx, ax * bx + ay * by)


def _grow(points: Sequence[Point2], i: int) -> tuple[int, Point2, float] | None:
    """The longest arc starting at vertex `i`, as the index of its last
    vertex (at most len(points), which stands for vertex 0 again) and its
    circle; None when fewer than MIN_SEGMENTS segments fit one."""
    n = len(points)
    if n - i < MIN_SEGMENTS:
        return None

    def at(k: int) -> Point2:
        return points[k % n]

    circle = _circumcircle(at(i), at(i + 1), at(i + 2))
    if circle is None:
        return None
    center, radius = circle
    first = _turn(center, at(i), at(i + 1))
    j = i
    while j < n:
        q = at(j + 1)
        if abs(math.dist(q, center) - radius) > TOLERANCE:
            break
        step = _turn(center, at(j), q)
        if (step > 0) != (first > 0) or not MIN_STEP <= abs(step) <= MAX_STEP:
            break
        j += 1
    if j - i < MIN_SEGMENTS:
        return None
    return j, center, radius


def _same_circle(a: Arc2, b: Arc2) -> bool:
    return math.dist(a.center, b.center) <= 10 * TOLERANCE and abs(a.radius - b.radius) <= 10 * TOLERANCE


def _arc(points: Sequence[Point2], i: int, j: int, center: Point2, radius: float) -> Arc2 | Circle2:
    n = len(points)
    a, b = points[i % n], points[j % n]
    if j - i >= n:
        return Circle2(center, radius)
    mid = points[((i + j) // 2) % n]
    # The circle through the arc's ends and middle is the best estimate.
    better = _circumcircle(a, mid, b)
    if better is not None:
        center, radius = better
    return Arc2(a, mid, b, center, radius)


def fit(ring: Sequence[Sequence[float]]) -> list[Curve2]:
    """The closed ring (no repeated closing point needed) as lines, arcs
    and full circles, in the ring's order."""
    points: list[Point2] = [(float(p[0]), float(p[1])) for p in ring]
    if len(points) > 1 and points[0] == points[-1]:
        points.pop()
    n = len(points)
    curves: list[Curve2] = []
    i = 0
    while i < n:
        grown = _grow(points, i) if n >= MIN_SEGMENTS + 1 else None
        if grown is None:
            curves.append(Line2(points[i], points[(i + 1) % n]))
            i += 1
            continue
        j, center, radius = grown
        curves.append(_arc(points, i, j, center, radius))
        i = j
    # A ring that starts inside an arc has it split into its last and first
    # curve; join them.
    first, last = curves[0], curves[-1]
    if (len(curves) > 1 and isinstance(first, Arc2) and isinstance(last, Arc2) and _same_circle(first, last)
            and (_turn(first.center, first.a, first.mid) > 0) == (_turn(last.center, last.a, last.mid) > 0)):
        joined: Curve2 = (Circle2(first.center, first.radius) if len(curves) == 2 and first.b == last.a
                          else Arc2(last.a, last.b, first.b, first.center, first.radius))
        curves = [joined] + curves[1:-1]
    return curves
