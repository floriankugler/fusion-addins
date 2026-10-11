"""Arcs recovered from the layout's polygons.

The layout's shapes are polygons (shapely), but many of them stand for
curves: circles, the round ends of slots, rounded corners, offsets with
round joins. Each of those puts its vertices exactly on a circle, a few
degrees apart. `fit` finds such runs in a closed ring and returns the ring
as lines, arcs and full circles, so that the emitter draws true arcs, one
cylindrical face where the polygon would give a fan of small flat ones.
Where a boolean cut such a polygon, the cut point lies on one of its chords,
a hair off the circle; it is moved onto the circle (along the line it
continues in, or where two circles cross), so arcs meet lines and each
other exactly.

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
from collections.abc import Callable, Sequence
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


@dataclass
class _Piece:
    """Vertices `i` to `j` of the ring (indices modulo its length, j > i)
    as one line segment, or as an arc of `circle` when it has one."""
    i: int
    j: int
    circle: tuple[Point2, float] | None = None
    ccw: bool = True


def _same_circle(a: _Piece, b: _Piece) -> bool:
    if a.circle is None or b.circle is None:
        return False
    (ca, ra), (cb, rb) = a.circle, b.circle
    return math.dist(ca, cb) <= 10 * TOLERANCE and abs(ra - rb) <= 10 * TOLERANCE and a.ccw == b.ccw


def _onto_line(circle: tuple[Point2, float], p: Point2, q: Point2, near: Point2) -> Point2 | None:
    """Where the line through `p` and `q` crosses the circle, nearest `near`."""
    (cx, cy), r = circle
    dx, dy = q[0] - p[0], q[1] - p[1]
    length = math.hypot(dx, dy)
    if length == 0:
        return None
    dx, dy = dx / length, dy / length
    fx, fy = p[0] - cx, p[1] - cy
    b = fx * dx + fy * dy
    disc = b * b - (fx * fx + fy * fy - r * r)
    if disc < 0:
        return None
    roots = (-b - math.sqrt(disc), -b + math.sqrt(disc))
    points = [(p[0] + t * dx, p[1] + t * dy) for t in roots]
    return min(points, key=lambda x: math.dist(x, near))


def _onto_circles(a: tuple[Point2, float], b: tuple[Point2, float], near: Point2) -> Point2 | None:
    """Where two circles cross, nearest `near`."""
    (ac, ar), (bc, br) = a, b
    d = math.dist(ac, bc)
    if d == 0 or d > ar + br or d < abs(ar - br):
        return None
    along = (d * d + ar * ar - br * br) / (2 * d)
    h = math.sqrt(max(ar * ar - along * along, 0.0))
    ux, uy = (bc[0] - ac[0]) / d, (bc[1] - ac[1]) / d
    mx, my = ac[0] + along * ux, ac[1] + along * uy
    points = [(mx - h * uy, my + h * ux), (mx + h * uy, my - h * ux)]
    return min(points, key=lambda x: math.dist(x, near))


def _chord_of(piece: _Piece, on_arc: Point2, x: Point2, outward: int) -> bool:
    """Whether the segment from the arc's end `on_arc` to `x` is a piece of
    one of its chords: a boolean with another shape cut the circle's
    polygon there, so `x` lies on the polygon, not on the circle.
    `outward` is +1 past the arc's end, -1 before its start."""
    assert piece.circle is not None
    center, radius = piece.circle
    sagitta = radius * (1 - math.cos(MAX_STEP / 2))
    if abs(math.dist(x, center) - radius) > sagitta + TOLERANCE:
        return False
    step = _turn(center, on_arc, x) * outward
    return 0 < (step if piece.ccw else -step) <= MAX_STEP


def _snap(pieces: list[_Piece], points: Sequence[Point2], moved: dict[int, Point2]) -> list[_Piece]:
    """Moves the vertices where an arc meets a line or another arc onto
    the true circle, and lets the arcs reach them.

    A boolean (a relief circle added to a rectangle, a circle cut from an
    outline) crosses the circle's polygon on one of its chords, up to the
    chord's sagitta off the circle, so the arc found by `_grow` stops one
    vertex short and a short piece of chord remains. That vertex goes onto
    the circle along the line it continues in, or onto both circles where
    two arcs meet, and the chord piece becomes part of the arc."""
    n = len(points)

    def at(k: int) -> Point2:
        return moved.get(k % n, points[k % n])

    count = len(pieces)
    if count < 3:
        return pieces
    ends: dict[int, tuple[_Piece, _Piece]] = {}      # vertex -> (arc, chord piece leading to it)
    starts: dict[int, tuple[_Piece, _Piece]] = {}    # vertex -> (arc, chord piece leading from it)
    for k, piece in enumerate(pieces):
        if piece.circle is None:
            continue
        after, before = pieces[(k + 1) % count], pieces[k - 1]
        if after.circle is None and after.j - after.i == 1 and _chord_of(piece, at(piece.j), at(after.j), 1):
            ends[after.j % n] = (piece, after)
        if before.circle is None and before.j - before.i == 1 and _chord_of(piece, at(piece.i), at(before.i), -1):
            starts[before.i % n] = (piece, before)
    absorbed: list[_Piece] = []
    for m in sorted(set(ends) | set(starts)):
        x = at(m)
        end, start = ends.get(m), starts.get(m)
        if end is not None and start is not None:
            assert end[0].circle is not None and start[0].circle is not None
            target = _onto_circles(end[0].circle, start[0].circle, x)
        elif end is not None:
            assert end[0].circle is not None
            target = _onto_line(end[0].circle, x, at(m + 1), x)
        else:
            assert start is not None and start[0].circle is not None
            target = _onto_line(start[0].circle, at(m - 1), x, x)
        arc = (end or start)
        assert arc is not None and arc[0].circle is not None
        reach = 2 * arc[0].circle[1] * math.sin(MAX_STEP / 2)
        if target is None or math.dist(target, x) > reach:
            continue
        moved[m] = target
        if end is not None:
            end[0].j += 1
            absorbed.append(end[1])
        if start is not None:
            start[0].i -= 1
            absorbed.append(start[1])
    return [p for p in pieces if not any(p is a for a in absorbed)]


def _curve(piece: _Piece, at: Callable[[int], Point2], n: int) -> Curve2:
    a, b = at(piece.i), at(piece.j)
    if piece.circle is None:
        return Line2(a, b)
    center, radius = piece.circle
    if piece.j - piece.i >= n:
        return Circle2(center, radius)
    mid = at((piece.i + piece.j) // 2)
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
    pieces: list[_Piece] = []
    i = 0
    while i < n:
        grown = _grow(points, i) if n >= MIN_SEGMENTS + 1 else None
        if grown is None:
            pieces.append(_Piece(i, i + 1))
            i += 1
            continue
        j, center, radius = grown
        pieces.append(_Piece(i, j, (center, radius), _turn(center, points[i], points[(i + 1) % n]) > 0))
        i = j
    # A ring that starts inside an arc has it split into its last and first
    # piece; join them.
    first, last = pieces[0], pieces[-1]
    if len(pieces) > 1 and _same_circle(first, last):
        pieces = [_Piece(last.i, first.j + n, first.circle, first.ccw)] + pieces[1:-1]
    moved: dict[int, Point2] = {}
    pieces = _snap(pieces, points, moved)

    def at(k: int) -> Point2:
        return moved.get(k % n, points[k % n])

    return [_curve(piece, at, n) for piece in pieces]
