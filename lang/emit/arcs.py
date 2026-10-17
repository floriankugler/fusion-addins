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


def _keeps_its_way(piece: _Piece, points: Sequence[Point2], at: Callable[[int], Point2]) -> bool:
    """Whether the arc drawn through its ends and middle turns its circle's
    way, no farther than the vertices it stands for and a step at each end.

    A vertex moves only where every arc it ends or starts keeps its way:
    where a small circle touches a large one from inside, the bump its
    coarser polygon pokes out of the large one has its ends on the point
    they touch at, or past it, and the arc would vanish or run the long
    way round."""
    assert piece.circle is not None
    n = len(points)
    center = piece.circle[0]
    span = sum(abs(_turn(center, points[k % n], points[(k + 1) % n])) for k in range(piece.i, piece.j))
    a, mid, b = at(piece.i), at((piece.i + piece.j) // 2), at(piece.j)
    sweep = 0.0
    for p, q in ((a, mid), (mid, b)):
        t = _turn(center, p, q)
        sweep += (t if piece.ccw else -t) % (2 * math.pi)
    return 0 < sweep <= span + 2 * MAX_STEP


def _sagitta(piece: _Piece, at: Callable[[int], Point2]) -> float:
    """How far the chords of an arc's polygon lie inside its circle: the
    sagitta of its longest step."""
    assert piece.circle is not None
    center, r = piece.circle
    step = max(abs(_turn(center, at(k), at(k + 1))) for k in range(piece.i, piece.j))
    return r * (1 - math.cos(step / 2))


#: The widest gap (mm) between two curves that touch: the arcs a boolean or
#: an offset leaves touching meet within a thousandth of a millimetre.
_TOUCHING = 0.002


def _touching_circles(a: tuple[Point2, float], b: tuple[Point2, float], on_a: bool) -> Point2 | None:
    """Where two circles touch, outside or inside each other, give or take
    `_TOUCHING`: on the line through their centres, on circle `a` when
    `on_a` (the finer arc's: the other one then reaches it), else on `b`;
    None when they do not touch."""
    (ca, ra), (cb, rb) = a, b
    d = math.dist(ca, cb)
    if d < 1e-12:
        return None
    ux, uy = (cb[0] - ca[0]) / d, (cb[1] - ca[1]) / d
    if abs(d - (ra + rb)) <= _TOUCHING:                 # outside each other
        sa, sb = ra, d - rb
    elif d < 10 * _TOUCHING:
        return None                                     # (nearly) one circle: they share an arc, not a point
    elif ra >= rb and abs(ra - rb - d) <= _TOUCHING:    # b inside a: beyond b, seen from a's centre
        sa, sb = ra, d + rb
    elif rb > ra and abs(rb - ra - d) <= _TOUCHING:     # a inside b: beyond a, seen from b's centre
        sa, sb = -ra, d - rb
    else:
        return None
    s = sa if on_a else sb
    return (ca[0] + ux * s, ca[1] + uy * s)


def _touching_line(circle: tuple[Point2, float], p: Point2, q: Point2) -> Point2 | None:
    """Where the line through `p` and `q` touches the circle, give or take
    `_TOUCHING`: the circle's point nearest the line, so the arc stays on
    its circle and the line takes up what gap there is; None when it does
    not touch."""
    (cx, cy), r = circle
    dx, dy = q[0] - p[0], q[1] - p[1]
    length = math.hypot(dx, dy)
    if length == 0:
        return None
    dx, dy = dx / length, dy / length
    t = (cx - p[0]) * dx + (cy - p[1]) * dy
    foot = (p[0] + dx * t, p[1] + dy * t)
    h = math.dist(foot, (cx, cy))
    if abs(h - r) > _TOUCHING or h < 1e-12:
        return None
    return (cx + (foot[0] - cx) * r / h, cy + (foot[1] - cy) * r / h)


def _short_of(target: Point2 | None, x: Point2, other: Point2) -> Point2 | None:
    """`target`, a point on the line from the vertex `x` to `other`, when it
    lies short of `other`: a vertex moved past the line's other end would
    turn the line back on itself, and one moved onto it, where `other`
    lies on the circle too, would leave a line of no length (within
    `TOLERANCE`: the crossing is found to about 1e-11 mm, and whether it
    fell short or past was the rounding's choice [found by fuzzing,
    2026-10-13])."""
    if target is None:
        return None
    dx, dy = other[0] - x[0], other[1] - x[1]
    length2 = dx * dx + dy * dy
    if length2 == 0 or ((target[0] - x[0]) * dx + (target[1] - x[1]) * dy) / length2 >= 1 - 1e-9 \
            or math.dist(target, other) <= TOLERANCE:
        return None
    return target


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


#: Curves meeting at less than this angle meet at a glancing angle.
_GLANCING = math.radians(10.0)


def _glancing(p: Point2, a: tuple[Point2, float], b: tuple[Point2, float] | None,
              toward: Point2 | None = None) -> bool:
    """Whether the circle `a` meets the circle `b`, or the line from `p`
    toward `toward`, at `p` at a glancing angle."""
    (ca, ra) = a
    na = ((p[0] - ca[0]) / ra, (p[1] - ca[1]) / ra)        # the normal of circle a at p
    if b is not None:
        (cb, rb) = b
        nb = ((p[0] - cb[0]) / rb, (p[1] - cb[1]) / rb)
        return abs(na[0] * nb[1] - na[1] * nb[0]) < math.sin(_GLANCING)
    assert toward is not None
    dx, dy = toward[0] - p[0], toward[1] - p[1]
    length = math.hypot(dx, dy)
    if length == 0:
        return True
    return abs(na[0] * dx + na[1] * dy) / length < math.sin(_GLANCING)


def _chord_of(piece: _Piece, on_arc: Point2, x: Point2, outward: int) -> bool:
    """Whether the segment from the arc's end `on_arc` to `x` is a piece of
    one of its chords: a boolean with another shape cut the circle's
    polygon there, so `x` lies on the polygon, not on the circle.
    `outward` is +1 past the arc's end, -1 before its start. A chord lies
    inside its circle; a line the arc runs into tangentially lies outside,
    as near as a chord close to the arc's end."""
    assert piece.circle is not None
    center, radius = piece.circle
    sagitta = radius * (1 - math.cos(MAX_STEP / 2))
    if not radius - sagitta - TOLERANCE <= math.dist(x, center) <= radius + TOLERANCE:
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
    # A single chord between two arcs is claimed by both, the one before
    # it reaching for its far end and the one after it for its near end:
    # the two arcs meet where their circles cross, at its near end.
    for m in sorted(ends):
        before_arc, chord = ends[m]
        near = chord.i % n
        if near not in starts or starts[near][1] is not chord:
            continue
        after_arc = starts.pop(near)[0]
        del ends[m]
        assert before_arc.circle is not None and after_arc.circle is not None
        a, b = at(chord.i), at(chord.j)
        target = _onto_circles(before_arc.circle, after_arc.circle, ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2))
        if target is None or _glancing(target, before_arc.circle, after_arc.circle):
            target = _touching_circles(before_arc.circle, after_arc.circle,
                                       _sagitta(before_arc, at) <= _sagitta(after_arc, at))
        reach = 2 * min(before_arc.circle[1], after_arc.circle[1]) * math.sin(MAX_STEP / 2)
        if target is None or max(math.dist(target, a), math.dist(target, b)) > reach:
            continue
        moved[near] = target
        after_arc.i -= 1
        if not (_keeps_its_way(before_arc, points, at) and _keeps_its_way(after_arc, points, at)):
            del moved[near]
            after_arc.i += 1
            continue
        absorbed.append(chord)
    # The arc a vertex begins or ends without a chord between: a vertex an
    # arc reaches for that begins another arc goes where the two circles
    # cross, not along that arc's first chord.
    starting = {p.i % n: p for p in pieces if p.circle is not None}
    ending = {p.j % n: p for p in pieces if p.circle is not None}
    for m in sorted(set(ends) | set(starts)):
        x = at(m)
        end, start = ends.get(m), starts.get(m)
        circles: tuple[tuple[Point2, float], tuple[Point2, float]] | None = None
        pair: tuple[_Piece, _Piece] | None = None
        if end is not None and start is not None:
            assert end[0].circle is not None and start[0].circle is not None
            circles = (end[0].circle, start[0].circle)
            pair = (end[0], start[0])
        elif end is not None and m in starting:
            beyond = starting[m].circle
            assert end[0].circle is not None and beyond is not None
            circles = (end[0].circle, beyond)
            pair = (end[0], starting[m])
        elif start is not None and m in ending:
            beyond = ending[m].circle
            assert start[0].circle is not None and beyond is not None
            circles = (beyond, start[0].circle)
            pair = (ending[m], start[0])
        arc = (end or start)
        assert arc is not None and arc[0].circle is not None
        following = at(m + 1) if end is not None else at(m - 1)
        # Where the arc meets the line or the other arc at a glancing angle
        # (a fillet touching them), the crossing found is ill-conditioned
        # and may lie far along the curves: where they touch, the junction
        # goes to the point they touch at; else the vertex stays.
        if circles is not None:
            assert pair is not None
            target = _onto_circles(circles[0], circles[1], x)
            if target is None or _glancing(target, circles[0], circles[1]):
                target = _touching_circles(circles[0], circles[1], _sagitta(pair[0], at) <= _sagitta(pair[1], at))
        else:
            line = (x, following) if end is not None else (following, x)
            target = _short_of(_onto_line(arc[0].circle, line[0], line[1], x), x, following)
            if target is None or _glancing(target, arc[0].circle, None, following):
                target = _short_of(_touching_line(arc[0].circle, x, following), x, following)
        reach = 2 * arc[0].circle[1] * math.sin(MAX_STEP / 2)
        if target is None or math.dist(target, x) > reach:
            continue
        moved[m] = target
        if end is not None:
            end[0].j += 1
        if start is not None:
            start[0].i -= 1
        if not all(_keeps_its_way(piece, points, at) for piece in (pair or (arc[0],))):
            del moved[m]
            if end is not None:
                end[0].j -= 1
            if start is not None:
                start[0].i += 1
            continue
        if end is not None:
            absorbed.append(end[1])
        if start is not None:
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
    # The circle through the arc's ends and middle is the best estimate;
    # an arc that ends where it starts (a ring touching itself there) has
    # two points for it, and keeps the circle it was grown on.
    better = _circumcircle(a, mid, b) if math.dist(a, b) > TOLERANCE else None
    if better is not None:
        center, radius = better
    return Arc2(a, mid, b, center, radius)


def _from_corner(points: list[Point2]) -> list[Point2]:
    """The ring started where no arc runs through: at its sharpest corner,
    a vertex turning more than an arc's segments do, or, when every corner
    is rounded, where the segments' length changes most (a line meeting an
    arc, or arcs of different radii meeting). An arc wrapping around the
    start would be split, and its part before the start would not be found
    when it has fewer than MIN_SEGMENTS segments."""
    n = len(points)
    if n < 3:
        return points
    best, best_key = 0, (0, 0.0)
    for i in range(n):
        p, q, r = points[i - 1], points[i], points[(i + 1) % n]
        ax, ay = q[0] - p[0], q[1] - p[1]
        bx, by = r[0] - q[0], r[1] - q[1]
        turn = abs(math.atan2(ax * by - ay * bx, ax * bx + ay * by))
        if turn > MAX_STEP:
            key = (2, turn)
        else:
            a, b = math.hypot(ax, ay), math.hypot(bx, by)
            key = (1, max(a, b) / max(min(a, b), 1e-12))
        if key > best_key:
            best, best_key = i, key
    return points if best == 0 else points[best:] + points[:best]


def fit(ring: Sequence[Sequence[float]]) -> list[Curve2]:
    """The closed ring (no repeated closing point needed) as lines, arcs
    and full circles, in the ring's order."""
    points: list[Point2] = [(float(p[0]), float(p[1])) for p in ring]
    if len(points) > 1 and points[0] == points[-1]:
        points.pop()
    if not points:      # (a ring without points has no curves [found by fuzzing, 2026-10-17])
        return []
    points = _from_corner(points)
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
