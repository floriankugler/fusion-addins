"""The plan's loops in space: their winding, and whether a point lies on
one of their curves.

The Fusion emitter builds temporary faces from loops wound so that the
face has the normal it wants, and finds a chamfer's edges by their
midpoints on the contour's curves. This is the part of that work that
needs no Fusion, in world millimetres, so it is unit tested; `fusion.py`
converts Fusion's centimetres before it asks.
"""
from __future__ import annotations

import math

from .plan import Arc, Circle, Curve, Line, Loop, Point3, Vec, loop_points


def dot(a: Vec, b: Vec) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def cross(a: Vec, b: Vec) -> Vec:
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def newell_normal(ring: list[Point3]) -> Vec:
    """The normal of a planar polygon by Newell's method: it points the way
    the ring winds counter-clockwise about, and its length is twice the
    polygon's area."""
    nx = ny = nz = 0.0
    for i, a in enumerate(ring):
        b = ring[(i + 1) % len(ring)]
        nx += (a[1] - b[1]) * (a[2] + b[2])
        ny += (a[2] - b[2]) * (a[0] + b[0])
        nz += (a[0] - b[0]) * (a[1] + b[1])
    return (nx, ny, nz)


def reversed_curve(curve: Curve) -> Curve:
    """The curve run the other way; a full circle as it is."""
    if isinstance(curve, Line):
        return Line(curve.b, curve.a)
    if isinstance(curve, Arc):
        return Arc(curve.b, curve.mid, curve.a, curve.center, curve.radius)
    return curve


def oriented(loop: Loop, normal: Vec) -> Loop:
    """The loop wound so that the face made from it has `normal`
    (right-hand rule). A full circle is drawn about `normal` anyway."""
    points = loop_points(loop)
    if not points or dot(newell_normal(points), normal) >= 0:
        return loop
    return [reversed_curve(c) for c in reversed(loop)]


def polygon_loop(points: list[Point3]) -> Loop:
    """A closed polygon as a loop of lines."""
    return [Line(a, points[(i + 1) % len(points)]) for i, a in enumerate(points)]


def on_arc(p: Point3, arc: Arc, normal: Vec, slack: float = 1e-6) -> bool:
    """Whether `p`, a point on the arc's circle, lies between its ends,
    going the way its middle point does; `normal` is the plane's normal,
    `slack` the angle (radians) a point may lie past an end."""
    c = arc.center

    def angle(q: Point3) -> float:
        u = (arc.a[0] - c[0], arc.a[1] - c[1], arc.a[2] - c[2])
        v = (q[0] - c[0], q[1] - c[1], q[2] - c[2])
        return math.atan2(dot(normal, cross(u, v)), dot(u, v)) % (2 * math.pi)

    mid, end, at = angle(arc.mid), angle(arc.b), angle(p)
    if mid < end:                         # counter-clockwise about the normal
        return at <= end + slack or at >= 2 * math.pi - slack
    return at >= end - slack or at <= slack


def on_curve(p: Point3, curve: Curve, normal: Vec, tolerance: float) -> bool:
    """Whether `p`, a point in the curve's plane, lies on the curve, within
    `tolerance` (mm)."""
    if isinstance(curve, Line):
        return dist_to_segment(p, curve.a, curve.b) < tolerance
    if abs(math.dist(p, curve.center) - curve.radius) >= tolerance:
        return False
    return isinstance(curve, Circle) or on_arc(p, curve, normal)


def dist_to_segment(p: Point3, a: Point3, b: Point3) -> float:
    ab = (b[0] - a[0], b[1] - a[1], b[2] - a[2])
    ap = (p[0] - a[0], p[1] - a[1], p[2] - a[2])
    length2 = dot(ab, ab)
    t = 0.0 if length2 == 0 else max(0.0, min(1.0, dot(ap, ab) / length2))
    c = (a[0] + t * ab[0], a[1] + t * ab[1], a[2] + t * ab[2])
    return math.dist(p, c)
