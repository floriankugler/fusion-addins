"""Face cutouts: openings cut into a board from one of its big faces, as the
cutouts_native add-in (Face Cutout) makes them, to make a board lighter or
to vent through it.

`side.cutout()` cuts out the face inside a border (`border=`), keeping
material around everything the board has so far (`around=`): its holes and
through cuts, pockets and holes on either big face, holes into its narrow
faces, V-grooves. `keep=` keeps material where other boards meet it, such
as a shelf in the middle of a side. A pattern leaves more material:
`cross(width)` two bands along the diagonals, `triangles(columns, rows,
spacing)` a lattice of triangles. The openings' corners are rounded
(`radius=`), the outside ones as a router leaves them and the inside ones
alike, and the rims can be chamfered on the face they are cut from.

The geometry is plain 2D in the board's outline frame (shapely), drawn the
way the add-in builds its tool bodies: the region is the inset outline,
less the material kept; a pattern is laid out in the region's bounding
rectangle and clipped to the region; then every corner is filleted. The
fillets are worked out on the lines and arcs the polygons stand for
(`lang.emit.arcs.fit`), so arcs stay exact and the emitter draws them as
arcs, tangent to their neighbours. Offsets of curved shapes (a ring
around a slot) are put back onto their exact circles for the same reason.

The sizes of the patterns come from `lib/cutout_patterns.py`, shared with
the add-in.
"""
from __future__ import annotations

import math
from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal

from shapely.geometry import LineString, Point, Polygon
from shapely.geometry.base import BaseGeometry
from shapely.geometry.polygon import orient
from shapely.ops import nearest_points, unary_union

from lib import cutout_patterns as data

from ..emit.arcs import Arc2, Circle2, Curve2, Line2, fit
from .directions import ExtentName
from .errors import LangError, one_of
from .geometry import polygons_of

if TYPE_CHECKING:
    from .part import Anchor

Point2 = tuple[float, float]

#: Arcs are drawn with a vertex at least every this many degrees, so that
#: short pieces of them are still recognised as arcs.
_ARC_STEP = math.radians(1.0)
#: Corners turning less than this are left as they are: they are the joints
#: of a polygon standing for a curve, not corners.
_MIN_CORNER = math.radians(2.0)
#: How far (mm) a vertex of an offset may lie off the circle it stands for,
#: at least: an offset's mitred joins on a polygon standing for an arc lie
#: up to half a percent of the radius outside it (`_snap_tolerance`).
_SNAP = 0.05
_EPS = 1e-9
#: How near (mm) a vertex of a piece rounded as a cutter would must lie to an
#: arc of the piece, and that arc's point nearest it to the arc's circle, to
#: be put back onto the circle: the two offsets blur the arc by less.
_ON_ARC = 0.01
#: Pieces of an offset with less area (mm2) than this are slivers, not pieces.
_SLIVER = 1e-6
#: How close (mm) a corner must lie to a point that names it.
_AT = 1e-6


# -- patterns -------------------------------------------------------------------------

@dataclass(frozen=True)
class Triangles:
    """A lattice of triangles, rows alternately pointing up and down; see
    `triangles()`."""
    columns: int
    rows: int
    spacing: float
    aligned: bool
    along: ExtentName | None
    start: Anchor | None


@dataclass(frozen=True)
class Cross:
    """Two bands of material along the diagonals; see `cross()`."""
    width: float


Pattern = Triangles | Cross


def triangles(columns: int = data.COLUMNS, rows: int = data.ROWS, spacing: float = data.SPACING, *,
              aligned: bool = False, along: ExtentName | None = None, start: Anchor | None = None) -> Triangles:
    """Triangles in `rows` rows, alternately pointing up and down, with
    `columns` pitches between the first column and the last, which sit on
    the ends of the region and are halved. `spacing` is the true gap
    between neighbours, square to their sides. `aligned=True` makes them
    taller, so that each rounded tip just reaches the next row's base line.
    `along=` is the extent the columns run along (the region's longer side
    by default); `start=` the corner the first triangle sits on, as a
    corner of the face (`side.inner.bottom.back`); by default the corner
    at the bottom, front and left."""
    if columns < 1 or rows < 1:
        raise LangError(f"triangles: columns and rows must be at least 1, got {columns} and {rows}.")
    if spacing <= 0:
        raise LangError(f"triangles: spacing must be positive, got {spacing:g}.")
    if along is not None:
        one_of(along, ExtentName, "triangles(along=)")
    return Triangles(columns, rows, float(spacing), aligned, along, start)


def cross(width: float = data.CROSS_WIDTH) -> Cross:
    """Leaves two bands of material `width` wide along the diagonals of the
    region and cuts out the four wedges between them."""
    if width <= 0:
        raise LangError(f"cross: the width must be positive, got {width:g}.")
    return Cross(float(width))


@dataclass(frozen=True)
class PatternFrame:
    """Where a pattern is laid out: the rectangle `bounds` (u0, v0, u1, v1)
    in the outline's frame, which of its axes the columns run along (0 for
    u, 1 for v), and the corner it starts at: per axis -1 for the low end,
    +1 for the high end."""
    bounds: tuple[float, float, float, float]
    columns_axis: Literal[0, 1]
    start: tuple[int, int]


# -- the cutout ----------------------------------------------------------------------------

@dataclass
class Openings:
    """What a cutout removes, piece by piece, and how many pieces were too
    small for the corner radius and left out."""
    pieces: list[Polygon]
    dropped: int

    @property
    def geometry(self) -> BaseGeometry:
        return unary_union(self.pieces)


def openings(region: BaseGeometry, frame: PatternFrame, pattern: Pattern | None, radius: float,
             path: str) -> Openings:
    """The openings of a cutout: `region` (the inset outline less the
    material kept) cut out whole, or with `pattern` laid out in `frame`;
    every corner rounded with `radius`."""
    if pattern is None:
        raw = region
    elif isinstance(pattern, Cross):
        raw = region.difference(_cross_bands(frame, pattern, path))
    else:
        raw = region.intersection(_triangles(frame, pattern, radius, path))
    pieces = [p for p in polygons_of(raw) if p.area > 1e-6]
    if radius <= 0:
        return Openings(pieces, 0)
    rounded: list[Polygon] = []
    dropped = 0
    for piece in pieces:
        out = fillet(piece, radius)
        if not out:
            dropped += 1
        rounded.extend(out)
    return Openings(rounded, dropped)


def _to_frame(frame: PatternFrame, a: float, b: float) -> Point2:
    """A point given in the pattern's own coordinates, `a` along the
    columns and `b` across them, both from the start corner, in the
    outline's frame."""
    u0, v0, u1, v1 = frame.bounds
    su, sv = frame.start
    du = a if frame.columns_axis == 0 else b
    dv = b if frame.columns_axis == 0 else a
    return (u0 + du if su < 0 else u1 - du, v0 + dv if sv < 0 else v1 - dv)


def _extents(frame: PatternFrame) -> tuple[float, float]:
    """The rectangle's extent along the columns and across them."""
    u0, v0, u1, v1 = frame.bounds
    return (u1 - u0, v1 - v0) if frame.columns_axis == 0 else (v1 - v0, u1 - u0)


def _cross_bands(frame: PatternFrame, pattern: Cross, path: str) -> BaseGeometry:
    u0, v0, u1, v1 = frame.bounds
    limit = data.cross_max_width(u1 - u0, v1 - v0)
    if pattern.width >= limit - 1e-6:
        raise LangError(f"cutout: the cross is too wide for its region; it must be narrower than {limit:.1f}.",
                        path)
    reach = max(u1 - u0, v1 - v0)
    bands: list[BaseGeometry] = []
    for (a, b) in (((u0, v0), (u1, v1)), ((u1, v0), (u0, v1))):
        dx, dy = b[0] - a[0], b[1] - a[1]
        n = math.hypot(dx, dy)
        ex, ey = dx / n * reach, dy / n * reach
        line = LineString([(a[0] - ex, a[1] - ey), (b[0] + ex, b[1] + ey)])
        bands.append(line.buffer(pattern.width / 2, cap_style="flat"))
    return unary_union(bands)


def _triangles(frame: PatternFrame, pattern: Triangles, radius: float, path: str) -> BaseGeometry:
    extent_a, extent_b = _extents(frame)
    if pattern.aligned and radius <= 0:
        raise LangError("cutout: aligned triangles need a corner radius above 0.", path)
    try:
        sizes = data.triangles(extent_a, extent_b, pattern.columns, pattern.rows, pattern.spacing,
                               aligned_radius=radius if pattern.aligned else None)
    except ValueError as e:
        raise LangError(f"cutout: {e}", path) from None
    shapes: list[Polygon] = []
    for j in range(pattern.rows):
        bottom = j * sizes.pitch_v
        for k in range(pattern.columns + 1):
            up = (j + k) % 2 == 0
            local = _triangle(k * sizes.pitch_u, bottom if up else bottom + sizes.height, up, sizes.width,
                              sizes.apex_height, radius if pattern.aligned else None)
            shapes.append(Polygon([_to_frame(frame, a, b) for a, b in local]))
    return unary_union(shapes)


def _triangle(centre: float, base: float, up: bool, width: float, apex: float,
              tip_radius: float | None) -> list[Point2]:
    """A triangle in the pattern's coordinates, its base on `base`, pointing
    up (toward larger b) or down, its tip rounded with `tip_radius` when
    given (the aligned triangles' tips are part of the seed in the add-in,
    before the pattern is clipped)."""
    s = 1.0 if up else -1.0
    half = width / 2
    left, right, top = (centre - half, base), (centre + half, base), (centre, base + s * apex)
    if tip_radius is None:
        points = [left, right, top]
    else:
        side = math.hypot(half, apex)
        # The tip's circle touches both sides; its centre lies on the
        # altitude, `tip_radius / sin(half angle)` from the apex.
        c = (centre, top[1] - s * tip_radius * side / half)
        # Where the circle touches the right side (the foot of its centre
        # on that side), and its mirror image on the left side.
        ux, uy = -half / side, s * apex / side           # along the right side, from the base toward the tip
        along = (c[0] - right[0]) * ux + (c[1] - right[1]) * uy
        foot_r = (right[0] + ux * along, right[1] + uy * along)
        foot_l = (2 * centre - foot_r[0], foot_r[1])
        points = [left, right] + _arc_points(c, tip_radius, foot_r, foot_l, ccw=up)
    return points


# -- arcs and fillets ---------------------------------------------------------------------
#
# Shared beyond the cutouts: `Shape.rounded()` rounds every corner of a
# shape with `filleted`, and `lang.core.corners` rounds or cuts off chosen
# corners of a board's outline (`filleted(at=)`, `chamfered`).

def _angle(c: Point2, p: Point2) -> float:
    return math.atan2(p[1] - c[1], p[0] - c[0])


def _sweep(c: Point2, p: Point2, q: Point2, ccw: bool) -> float:
    """The angle from `p` to `q` about `c`, going counter-clockwise or not,
    in [0, 2 pi)."""
    d = _angle(c, q) - _angle(c, p)
    if not ccw:
        d = -d
    return d % (2 * math.pi)


def _arc_points(c: Point2, r: float, p: Point2, q: Point2, ccw: bool, sweep: float | None = None) -> list[Point2]:
    """Points on the circle from `p` to `q` (both included), at most
    `_ARC_STEP` apart and at least four segments when the arc allows; the
    end points are taken as given."""
    total = _sweep(c, p, q, ccw) if sweep is None else sweep
    n = max(1, math.ceil(total / _ARC_STEP - 1e-9))
    if total >= math.radians(2.0):
        n = max(n, 4)
    a0 = _angle(c, p)
    sign = 1.0 if ccw else -1.0
    out = [p]
    for i in range(1, n):
        a = a0 + sign * total * i / n
        out.append((c[0] + r * math.cos(a), c[1] + r * math.sin(a)))
    out.append(q)
    return out


@dataclass
class _Seg:
    """A line, or an arc about `c` with radius `r`, from `a` to `b`."""
    a: Point2
    b: Point2
    c: Point2 | None = None
    r: float = 0.0
    ccw: bool = True

    def tangent(self, p: Point2) -> Point2:
        if self.c is None:
            dx, dy = self.b[0] - self.a[0], self.b[1] - self.a[1]
            n = math.hypot(dx, dy)
            return (dx / n, dy / n)
        rx, ry = (p[0] - self.c[0]) / self.r, (p[1] - self.c[1]) / self.r
        return (-ry, rx) if self.ccw else (ry, -rx)

    def length(self) -> float:
        if self.c is None:
            return math.dist(self.a, self.b)
        return _sweep(self.c, self.a, self.b, self.ccw) * self.r

    def param(self, p: Point2) -> float:
        """How far along the segment `p` lies, as a length from `a`."""
        if self.c is None:
            t = self.tangent(p)
            return (p[0] - self.a[0]) * t[0] + (p[1] - self.a[1]) * t[1]
        s = _sweep(self.c, self.a, p, self.ccw)
        if s > math.pi + _sweep(self.c, self.a, self.b, self.ccw) / 2:
            s -= 2 * math.pi      # a hair before the start
        return s * self.r

    def foot(self, p: Point2) -> Point2:
        """The point of the segment's line or circle nearest `p`."""
        if self.c is None:
            t = self.tangent(p)
            along = (p[0] - self.a[0]) * t[0] + (p[1] - self.a[1]) * t[1]
            return (self.a[0] + t[0] * along, self.a[1] + t[1] * along)
        dx, dy = p[0] - self.c[0], p[1] - self.c[1]
        n = math.hypot(dx, dy)
        return (self.c[0] + dx / n * self.r, self.c[1] + dy / n * self.r)

    def step(self, p: Point2, d: float) -> Point2:
        """The point `d` along the segment from `p` (back for negative `d`)."""
        if self.c is None:
            t = self.tangent(p)
            return (p[0] + t[0] * d, p[1] + t[1] * d)
        a = _angle(self.c, p) + (d / self.r) * (1 if self.ccw else -1)
        return (self.c[0] + self.r * math.cos(a), self.c[1] + self.r * math.sin(a))

    def points(self, p: Point2, q: Point2) -> list[Point2]:
        """The segment from `p` to `q` (on it) as points, `q` excluded."""
        if self.c is None:
            return [p]
        return _arc_points(self.c, self.r, p, q, self.ccw)[:-1]


def _segments(ring: Sequence[Point2]) -> list[_Seg] | None:
    """The ring as lines and arcs; None for a full circle."""
    segs: list[_Seg] = []
    for curve in fit(ring):
        if isinstance(curve, Circle2):
            return None
        if isinstance(curve, Line2):
            if math.dist(curve.a, curve.b) > 1e-9:
                segs.append(_Seg(curve.a, curve.b))
        else:
            arc: Arc2 = curve
            ccw = _sweep(arc.center, arc.a, arc.mid, True) < math.pi
            segs.append(_Seg(arc.a, arc.b, arc.center, arc.radius, ccw))
    return segs


def _offset_crossings(s1: _Seg, s2: _Seg, side: float, r: float, near: Point2) -> list[Point2]:
    """Where the two segments' lines or circles, each moved `r` to `side`
    (+1 left of its direction, -1 right), cross: the centres of the
    fillets touching both."""
    def moved(s: _Seg, at: Point2) -> tuple[Point2, Point2] | tuple[Point2, float]:
        if s.c is None:
            t = s.tangent(at)
            n = (-t[1] * side * r, t[0] * side * r)
            return ((s.a[0] + n[0], s.a[1] + n[1]), t)
        # the left of a counter-clockwise arc is toward its centre
        return (s.c, s.r - side * r * (1.0 if s.ccw else -1.0))

    m1, m2 = moved(s1, near), moved(s2, near)
    candidates: list[Point2] = []
    if s1.c is None and s2.c is None:
        (p, t), (q, u) = m1, m2
        assert isinstance(t, tuple) and isinstance(u, tuple)
        den = t[0] * u[1] - t[1] * u[0]
        if abs(den) < 1e-12:
            return []
        k = ((q[0] - p[0]) * u[1] - (q[1] - p[1]) * u[0]) / den
        candidates.append((p[0] + t[0] * k, p[1] + t[1] * k))
    elif s1.c is None or s2.c is None:
        (p, t), (c, rr) = (m1, m2) if s1.c is None else (m2, m1)
        assert isinstance(t, tuple) and isinstance(rr, float)
        if rr <= 0:
            return []
        fx, fy = p[0] - c[0], p[1] - c[1]
        b = fx * t[0] + fy * t[1]
        disc = b * b - (fx * fx + fy * fy - rr * rr)
        if disc < 0:
            return []
        for k in (-b - math.sqrt(disc), -b + math.sqrt(disc)):
            candidates.append((p[0] + t[0] * k, p[1] + t[1] * k))
    else:
        (c1, r1), (c2, r2) = m1, m2
        assert isinstance(r1, float) and isinstance(r2, float)
        d = math.dist(c1, c2)
        if r1 <= 0 or r2 <= 0 or d < 1e-12 or d > r1 + r2 or d < abs(r1 - r2):
            return []
        along = (d * d + r1 * r1 - r2 * r2) / (2 * d)
        h = math.sqrt(max(r1 * r1 - along * along, 0.0))
        ux, uy = (c2[0] - c1[0]) / d, (c2[1] - c1[1]) / d
        mx, my = c1[0] + along * ux, c1[1] + along * uy
        candidates += [(mx - h * uy, my + h * ux), (mx + h * uy, my - h * ux)]
    return candidates


def _turn(s1: _Seg, s2: _Seg, p: Point2) -> float:
    """How far the ring turns at `p`, where `s1` ends and `s2` begins
    (positive to the left). At a cusp, where the two run back along each
    other (a ring touching the border), the tangents alone cannot tell the
    way; the side `s2` leaves to, seen from `s1`, does."""
    t1, t2 = s1.tangent(p), s2.tangent(p)
    cross = t1[0] * t2[1] - t1[1] * t2[0]
    dot = t1[0] * t2[0] + t1[1] * t2[1]
    turn = math.atan2(cross, dot)
    if abs(turn) > math.pi - 1e-3:
        d = 1e-3 * min(s1.length(), s2.length(), 1.0)
        q1, q2 = s1.step(p, -d), s2.step(p, d)
        left = -t1[1] * (q2[0] - q1[0]) + t1[0] * (q2[1] - q1[1])
        turn = math.copysign(math.pi, left)
    return turn


def _fillet_ring(ring: Sequence[Point2], r: float, at: Sequence[Point2] | None = None,
                 areas: list[float] | None = None) -> list[Point2] | None:
    """The ring with every corner filleted with radius `r`, convex and
    concave alike (the material lies to the left), or only the corners at
    the points `at`; None when a fillet does not fit between its
    neighbours. Each fillet's area, as between two lines, is added to
    `areas`."""
    segs = _segments(ring)
    if segs is None:
        return list(ring)
    n = len(segs)
    if n < 2:
        return list(ring)
    # per corner k (the end of segment k): the fillet's centre, its ends on
    # segment k and k + 1, and which way it turns
    fillets: list[tuple[Point2, Point2, Point2, bool] | None] = []
    for k in range(n):
        s1, s2 = segs[k], segs[(k + 1) % n]
        p = s1.b
        turn = _turn(s1, s2, p)
        if abs(turn) < _MIN_CORNER or (at is not None and not _named(p, at)):
            fillets.append(None)
            continue
        side = 1.0 if turn > 0 else -1.0
        # the fillet touches both segments, not their extensions
        centres = [c for c in _offset_crossings(s1, s2, side, r, p)
                   if s1.param(s1.foot(c)) <= s1.length() + 1e-7 and s2.param(s2.foot(c)) >= -1e-7]
        if not centres:
            return None
        centre = min(centres, key=lambda c: math.dist(c, p))
        # Between two lines the centre lies r / cos(turn / 2) from the
        # corner; one much farther off is a wrong crossing of arcs.
        if math.dist(centre, p) > 4 * r / max(math.cos(abs(turn) / 2), 1e-3):
            return None
        fillets.append((centre, s1.foot(centre), s2.foot(centre), turn > 0))
        if areas is not None:
            areas.append(r * r * (math.tan(abs(turn) / 2) - abs(turn) / 2))
    if at is not None and all(f is None for f in fillets):
        return list(ring)            # no corner of this ring is named: as it was
    # each segment must keep a part between the fillets at its ends
    for k, s in enumerate(segs):
        before, after = fillets[k - 1], fillets[k]
        start = s.param(before[2]) if before else 0.0
        end = s.param(after[1]) if after else s.length()
        if start < -1e-7 or end > s.length() + 1e-7 or end < start - 1e-7:
            return None
    out: list[Point2] = []
    for k, s in enumerate(segs):
        before, after = fillets[k - 1], fillets[k]
        p = before[2] if before else s.a
        q = after[1] if after else s.b
        if s.param(q) < s.param(p):
            # the fillets at both ends use the segment up, give or take
            # rounding (a slot's end): they meet halfway
            p = q = ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)
        out += s.points(p, q)
        if after is not None:
            centre, _, b, ccw = after
            out += _arc_points(centre, r, q, b, ccw)[:-1]
    return _deduplicated(out)


def _deduplicated(points: list[Point2]) -> list[Point2]:
    out: list[Point2] = []
    for p in points:
        if not out or math.dist(p, out[-1]) > 1e-9:
            out.append(p)
    if len(out) > 1 and math.dist(out[0], out[-1]) <= 1e-9:
        out.pop()
    return out


def _ring_points(coords: Iterable[Sequence[float]]) -> list[Point2]:
    return _deduplicated([(float(c[0]), float(c[1])) for c in list(coords)[:-1]])


def fillet(piece: Polygon, r: float) -> list[Polygon]:
    """The piece with every corner rounded with radius `r`, as the add-in's
    fillets round the tool bodies: none when it is too small for the
    radius (a circle of it does not fit), several when the rounding parts
    it at a narrow neck."""
    if piece.buffer(-r, join_style="round").is_empty:
        return []
    piece = orient(piece, 1.0)
    out = filleted(piece, r)
    if out is not None and _cut_by(out, r):
        return [out]
    # A fillet does not fit between its neighbours (a short piece of edge
    # between two corners), or the piece has a part narrower than the
    # cutter, which the fillets of its corners leave: round the outside
    # corners as a cutter would, part it at narrow necks,
    # leave the inside ones, and put the arcs the piece had back onto their
    # circles, which the two offsets blur. The new arcs are the cutter's
    # path around the corners of the inset, r from them; their vertices
    # stay as they are, also where they run close to an arc of the piece.
    targets = _arc_targets(piece, 0.0)
    inner = piece.buffer(-r, join_style="round", quad_segs=16)
    opened = inner.buffer(r, join_style="round", quad_segs=16)
    # (an arc of the piece as round as the cutter shrinks to a point of
    # the inset: the cutter's path there is that arc, which goes back)
    centres = [c for c in _sharp_vertices(inner, 2 * math.pi / 64 + _MIN_CORNER)
               if not any(abs(t[1] - r) <= _SNAP and math.dist(t[0], c) <= _SNAP for t in targets)]

    boundary = piece.boundary

    def not_on_an_arc(q: Point2) -> bool:
        """Whether a vertex stays as it is: on a new arc, or not on an arc
        of the piece (a line's vertex near the end of an arc, say)."""
        if any(abs(math.dist(q, c) - r) <= 1e-6 for c in centres):
            return True
        if boundary.distance(Point(q)) > _ON_ARC:
            return True
        near = nearest_points(boundary, Point(q))[0]
        return not any(abs(math.dist((near.x, near.y), t[0]) - t[1]) <= _ON_ARC for t in targets)
    return [_onto_circles(p, targets, keep=not_on_an_arc) for p in polygons_of(opened) if p.area > 1e-6]


def _sharp_vertices(g: BaseGeometry, turn: float) -> list[Point2]:
    """The vertices of every ring of `g` that turn by more than `turn`
    (radians), either way: the corners of an inset made with round joins
    of 16 segments a quarter (5.6 degrees a step), not its round joins."""
    out: list[Point2] = []
    for poly in polygons_of(g):
        for ring in [poly.exterior, *poly.interiors]:
            pts = _ring_points(ring.coords)
            n = len(pts)
            for k in range(n):
                a, p, b = pts[k - 1], pts[k], pts[(k + 1) % n]
                ax, ay, bx, by = p[0] - a[0], p[1] - a[1], b[0] - p[0], b[1] - p[1]
                if abs(math.atan2(ax * by - ay * bx, ax * bx + ay * by)) > turn:
                    out.append(p)
    return out


def _cut_by(piece: Polygon, r: float) -> bool:
    """Whether a cutter of radius `r` reaches all of the piece: nothing is
    left of it but slivers where the cutter's polygon and the arcs' differ
    (a hundredth of r^2), not a part narrower than the cutter."""
    reached = piece.buffer(-0.99 * r, quad_segs=64).buffer(0.99 * r, quad_segs=64)
    return len(polygons_of(reached)) <= 1 and all(g.area <= 0.01 * r * r + 1e-3
                                                   for g in polygons_of(piece.difference(reached)))


def filleted(piece: Polygon, r: float, at: Sequence[Point2] | None = None) -> Polygon | None:
    """The piece with every corner rounded with radius `r`, convex and
    concave alike, exactly: worked out on the lines and arcs it stands for.
    `at` limits it to the corners at those points (see `corner_points`).
    None when a fillet does not fit between its neighbours. Two fillets
    may use up the edge between them, so a 12 wide rectangle rounded with
    6 gets round ends."""
    piece = orient(piece, 1.0)
    areas: list[float] = []
    exterior = _fillet_ring(_ring_points(piece.exterior.coords), r, at, areas)
    holes = [_fillet_ring(_ring_points(h.coords), r, at, areas) for h in piece.interiors]
    if not _rings_left(exterior, holes):
        return None
    out = Polygon(exterior, [h for h in holes if h is not None])
    # A sanity check against fillets gone wrong: the area changes by what
    # the fillets take or add, which for the sharp tips of a sliver can be
    # more than half of it.
    if out.is_valid and abs(out.area - piece.area) < max(0.5 * piece.area, 2 * sum(areas)) + 1:
        return out
    return None


def _rings_left(exterior: list[Point2] | None, holes: Sequence[list[Point2] | None]) -> bool:
    """Whether every ring was rounded or cut off and kept three vertices: a
    spike running out and back along one line can lose all but two."""
    return exterior is not None and len(exterior) >= 3 and all(h is not None and len(h) >= 3 for h in holes)


def _named(p: Point2, at: Sequence[Point2]) -> bool:
    return any(math.dist(p, q) <= _AT for q in at)


def corner_points(piece: Polygon) -> list[tuple[Point2, bool]]:
    """The piece's corners, ring by ring in order around each, each with
    whether it lies on the exterior: where two of the lines and arcs the
    piece stands for (`lang.emit.arcs.fit`) meet at an angle, convex or
    concave. Arcs have none, nor have lines and arcs meeting tangentially,
    such as a rounded corner's."""
    piece = orient(piece, 1.0)
    out: list[tuple[Point2, bool]] = []
    for k, ring in enumerate([piece.exterior, *piece.interiors]):
        segs = _segments(_ring_points(ring.coords))
        if segs is None or len(segs) < 2:
            continue
        for i, s1 in enumerate(segs):
            s2 = segs[(i + 1) % len(segs)]
            if abs(_turn(s1, s2, s1.b)) >= _MIN_CORNER:
                out.append((s1.b, k == 0))
    return out


def _chamfer_ring(ring: Sequence[Point2], d: float, at: Sequence[Point2]) -> list[Point2] | None:
    """The ring with its corners at the points `at` cut off by a straight
    line from `d` before each to `d` after it, measured along its lines and
    arcs; None when an edge is too short for that."""
    segs = _segments(ring)
    if segs is None or len(segs) < 2:
        return list(ring)
    n = len(segs)
    # per corner k (the end of segment k): the cut's ends on segment k and k + 1
    cuts: list[tuple[Point2, Point2] | None] = []
    for k in range(n):
        s1, s2 = segs[k], segs[(k + 1) % n]
        p = s1.b
        if abs(_turn(s1, s2, p)) < _MIN_CORNER or not _named(p, at):
            cuts.append(None)
            continue
        if d > s1.length() + 1e-7 or d > s2.length() + 1e-7:
            return None
        cuts.append((s1.step(p, -d), s2.step(p, d)))
    if all(c is None for c in cuts):
        return list(ring)
    # each segment must keep a part between the cuts at its ends
    for k, s in enumerate(segs):
        before, after = cuts[k - 1], cuts[k]
        start = s.param(before[1]) if before else 0.0
        end = s.param(after[0]) if after else s.length()
        if end < start - 1e-7:
            return None
    out: list[Point2] = []
    for k, s in enumerate(segs):
        before, after = cuts[k - 1], cuts[k]
        p = before[1] if before else s.a
        q = after[0] if after else s.b
        if s.param(q) < s.param(p):
            p = q = ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)     # two cuts use the edge up
        out += s.points(p, q)
        if after is not None:
            out.append(q)            # the cut runs from here to the next segment's start
    return _deduplicated(out)


def chamfered(piece: Polygon, d: float, at: Sequence[Point2]) -> Polygon | None:
    """The piece with its corners at the points `at` (see `corner_points`)
    cut off `d` along both their edges, as a router cuts a chamfered
    corner of an outline; None when an edge is too short for that."""
    piece = orient(piece, 1.0)
    exterior = _chamfer_ring(_ring_points(piece.exterior.coords), d, at)
    holes = [_chamfer_ring(_ring_points(h.coords), d, at) for h in piece.interiors]
    if not _rings_left(exterior, holes):
        return None
    out = Polygon(exterior, [h for h in holes if h is not None])
    return out if out.is_valid and out.area > 0 else None


# -- offsets ---------------------------------------------------------------------------------

def grown(g: BaseGeometry, d: float) -> BaseGeometry:
    """`g` grown by `d` (shrunk for a negative `d`) as Fusion offsets a
    sketch loop: lines move out and meet where they did, so corners stay
    sharp (the cutout's fillets round them), and arcs of `g` become arcs of
    the offset on their exact circles: a circle stays a circle, a slot's
    round ends stay round."""
    if abs(d) < _EPS:
        return g
    out: list[BaseGeometry] = []
    for poly in polygons_of(g):
        if len(poly.interiors) == 0:
            curves = fit(_ring_points(poly.exterior.coords))
            if len(curves) == 1 and isinstance(curves[0], Circle2):
                c, radius = curves[0].center, curves[0].radius
                if radius + d > _EPS:
                    out.append(_circle(c, radius + d))
                continue
        buffered = poly.buffer(d, join_style="mitre", mitre_limit=100.0)
        targets = _arc_targets(poly, d)
        # An inward offset that all but closes a shape (a slot by half its
        # width) leaves slivers without area; snapped, they would have too
        # few vertices for a ring.
        out += [_onto_circles(p, targets) for p in polygons_of(buffered) if p.area > _SLIVER]
    return unary_union(out) if out else Polygon()


#: A circle an offset's vertices are put back onto: centre, radius, and the
#: arc's start angle, sweep and direction (a whole circle sweeps 2 pi).
_Target = tuple[Point2, float, float, float, bool]


def _arc_targets(poly: Polygon, d: float) -> list[_Target]:
    """The circles the arcs of `poly` lie on, moved out and in by `d`:
    where the arcs of its offset by `d` lie."""
    targets: list[_Target] = []
    for ring in [poly.exterior] + list(poly.interiors):
        for curve in fit(_ring_points(ring.coords)):
            if isinstance(curve, Circle2):
                arc: _Target = (curve.center, curve.radius, 0.0, 2 * math.pi, True)
            elif isinstance(curve, Arc2):
                ccw = _sweep(curve.center, curve.a, curve.mid, True) < math.pi
                arc = (curve.center, curve.radius, _angle(curve.center, curve.a),
                       _sweep(curve.center, curve.a, curve.b, ccw), ccw)
            else:
                continue
            c, rr, a0, sweep, ccw = arc
            for radius in {rr + d, rr - d}:
                if radius > _EPS:
                    targets.append((c, radius, a0, sweep, ccw))
    return targets


def _circle(c: Point2, r: float) -> Polygon:
    n = max(8, math.ceil(2 * math.pi / _ARC_STEP))
    return Polygon([(c[0] + r * math.cos(2 * math.pi * i / n), c[1] + r * math.sin(2 * math.pi * i / n))
                    for i in range(n)])


def _onto_circles(poly: Polygon, targets: list[_Target], keep: Callable[[Point2], bool] | None = None) -> Polygon:
    if not targets:
        return poly
    rings = [_snap_ring(_ring_points(r.coords), targets, keep) for r in [poly.exterior] + list(poly.interiors)]
    if any(len(r) < 3 for r in rings):
        return poly
    out = Polygon(rings[0], rings[1:])
    # The snapped shape must be the same shape, only truer to its circles.
    limit = 2 * max(_snap_tolerance(t[1]) for t in targets)
    return out if out.is_valid and out.hausdorff_distance(poly) <= limit else poly


def _snap_tolerance(r: float) -> float:
    return max(_SNAP, 0.006 * r)


def _target_of(p: Point2, targets: list[_Target]) -> int | None:
    best: tuple[float, int] | None = None
    for i, (c, r, a0, sweep, ccw) in enumerate(targets):
        off = abs(math.dist(p, c) - r)
        if off > _snap_tolerance(r):
            continue
        if sweep < 2 * math.pi - 1e-9:
            # within the arc's angles, give or take a little
            s = (_angle(c, p) - a0) * (1 if ccw else -1) % (2 * math.pi)
            margin = math.radians(3)
            if not (s <= sweep + margin or s >= 2 * math.pi - margin):
                continue
        if best is None or off < best[0]:
            best = (off, i)
    return None if best is None else best[1]


def _snap_ring(points: list[Point2], targets: list[_Target],
               keep: Callable[[Point2], bool] | None = None) -> list[Point2]:
    """Moves the vertices lying on (near) a target circle onto it, and
    redraws each run of them as an arc with evenly spaced vertices; not
    those `keep` names."""
    n = len(points)
    owner = [None if keep is not None and keep(p) else _target_of(p, targets) for p in points]
    if all(o is None for o in owner):
        return points
    first = owner[0]
    if first is not None and all(o == first for o in owner):
        c, r = targets[first][0], targets[first][1]
        return [(float(x), float(y)) for x, y in list(_circle(c, r).exterior.coords)[:-1]]
    # start at a vertex that begins a run, so no run wraps around the end
    start = next(i for i in range(n) if owner[i] != owner[i - 1])
    order = points[start:] + points[:start]
    owners = owner[start:] + owner[:start]
    out: list[Point2] = []
    i = 0
    while i < n:
        o = owners[i]
        j = i
        while j + 1 < n and owners[j + 1] == o:
            j += 1
        if o is None or j == i:
            out += order[i:j + 1]
        else:
            c, r = targets[o][0], targets[o][1]
            first, last = _on(c, r, order[i]), _on(c, r, order[j])
            # the run's direction: the way its vertices turn about the centre
            turn = sum(math.remainder(_angle(c, order[k + 1]) - _angle(c, order[k]), 2 * math.pi)
                       for k in range(i, j))
            out += _arc_points(c, r, first, last, turn > 0, abs(turn))
        i = j + 1
    return _deduplicated(out)


def _on(c: Point2, r: float, p: Point2) -> Point2:
    dx, dy = p[0] - c[0], p[1] - c[1]
    n = math.hypot(dx, dy)
    return (c[0] + dx / n * r, c[1] + dy / n * r)


def circle_geometry(c: Point2, r: float) -> Polygon:
    """A circle as a polygon with its vertices exactly on it, close enough
    together to be drawn as a circle again."""
    return _circle(c, r)


# -- an exact inset of one polygon ---------------------------------------------------------------

def inset(polygon: Polygon, d: float) -> BaseGeometry:
    """The polygon's outline moved `d` inward, as Fusion offsets a sketch
    loop: lines move square to themselves and meet where they met, so a
    sharp corner stays sharp, and arcs keep their centres, so a corner
    rounded with r becomes one rounded with r - d. Exact: worked out on the
    lines and arcs the polygon stands for (`lang.emit.arcs.fit`), with the
    arcs' vertices on their circles and the lines where they belong.
    Outlines it cannot offset that way (an arc or a line vanishing) are
    left to `grown`, which is exact up to a few ten-thousandths of a
    millimetre where a line meets an arc. A ball catch's hatch is its
    opening inset by the slot."""
    ring = [(float(x), float(y)) for x, y in list(orient(polygon, 1.0).exterior.coords)[:-1]]
    curves = fit(ring)
    if len(curves) == 1 and isinstance(curves[0], Circle2):
        whole = curves[0]
        return _circle(whole.center, whole.radius - d) if whole.radius > d else Polygon()
    moved = [_inset_curve(c, d) for c in curves]
    n = len(moved)
    joints: list[Point2 | None] = [_inset_joint(moved[k], moved[(k + 1) % n]) for k in range(n)]
    points: list[Point2] = []
    for k, curve in enumerate(moved):
        start, end = joints[k - 1], joints[k]
        if start is None or end is None:
            return grown(polygon, -d)
        points.append(start)
        if isinstance(curve, Arc2):
            points += _arc_between(curve, start, end)
    out = Polygon(points)
    reference = grown(polygon, -d)
    if not out.is_valid or out.is_empty or out.hausdorff_distance(reference) > 0.01:
        return reference
    return out


def _inset_curve(curve: Curve2, d: float) -> Curve2:
    """A line or arc of a counter-clockwise ring moved `d` to its left,
    into the ring."""
    if isinstance(curve, Line2):
        (ax, ay), (bx, by) = curve.a, curve.b
        length = math.hypot(bx - ax, by - ay)
        nx, ny = -(by - ay) / length, (bx - ax) / length
        return Line2((ax + nx * d, ay + ny * d), (bx + nx * d, by + ny * d))
    assert isinstance(curve, Arc2)
    (ax, ay), (mx, my), (bx, by) = curve.a, curve.mid, curve.b
    left = (mx - ax) * (by - my) - (my - ay) * (bx - mx) > 0     # turning left: the centre is inside
    radius = curve.radius - d if left else curve.radius + d
    c = curve.center

    def on(p: Point2) -> Point2:
        dx, dy = p[0] - c[0], p[1] - c[1]
        k = radius / math.hypot(dx, dy)
        return (c[0] + dx * k, c[1] + dy * k)
    return Arc2(on(curve.a), on(curve.mid), on(curve.b), c, radius) if radius > 1e-9 else Line2(c, c)


def _inset_joint(p: Curve2, q: Curve2) -> Point2 | None:
    """Where the moved curve `p` ends and `q` begins: their common end
    where they met tangentially, else where they cross (nearest the ends);
    None when they do not."""
    end, start = _curve_ends(p)[1], _curve_ends(q)[0]
    if math.dist(end, start) <= 1e-6:
        return ((end[0] + start[0]) / 2, (end[1] + start[1]) / 2)
    near = ((end[0] + start[0]) / 2, (end[1] + start[1]) / 2)
    if isinstance(p, Line2) and isinstance(q, Line2):
        return _lines_cross(p, q)
    if isinstance(p, Arc2) and isinstance(q, Arc2):
        return _circles_cross(p, q, near)
    line, arc = (p, q) if isinstance(p, Line2) else (q, p)
    assert isinstance(line, Line2) and isinstance(arc, Arc2)
    return _line_circle_cross(line, arc, near)


def _curve_ends(curve: Curve2) -> tuple[Point2, Point2]:
    assert not isinstance(curve, Circle2)
    return curve.a, curve.b


def _lines_cross(p: Line2, q: Line2) -> Point2 | None:
    (ax, ay), (bx, by) = p.a, p.b
    (cx, cy), (dx, dy) = q.a, q.b
    ux, uy, wx, wy = bx - ax, by - ay, dx - cx, dy - cy
    den = ux * wy - uy * wx
    if abs(den) < 1e-12:
        return None
    t = ((cx - ax) * wy - (cy - ay) * wx) / den
    return (ax + t * ux, ay + t * uy)


def _line_circle_cross(line: Line2, arc: Arc2, near: Point2) -> Point2 | None:
    (ax, ay), (bx, by) = line.a, line.b
    (cx, cy), r = arc.center, arc.radius
    length = math.hypot(bx - ax, by - ay)
    if length == 0:
        return None
    ux, uy = (bx - ax) / length, (by - ay) / length
    fx, fy = ax - cx, ay - cy
    b = fx * ux + fy * uy
    disc = b * b - (fx * fx + fy * fy - r * r)
    if disc < 0:
        return None
    points = [(ax + t * ux, ay + t * uy) for t in (-b - math.sqrt(disc), -b + math.sqrt(disc))]
    return min(points, key=lambda x: math.dist(x, near))


def _circles_cross(p: Arc2, q: Arc2, near: Point2) -> Point2 | None:
    (pc, pr), (qc, qr) = (p.center, p.radius), (q.center, q.radius)
    dist = math.dist(pc, qc)
    if dist == 0 or dist > pr + qr or dist < abs(pr - qr):
        return None
    along = (dist * dist + pr * pr - qr * qr) / (2 * dist)
    h = math.sqrt(max(pr * pr - along * along, 0.0))
    ux, uy = (qc[0] - pc[0]) / dist, (qc[1] - pc[1]) / dist
    mx, my = pc[0] + along * ux, pc[1] + along * uy
    return min([(mx - h * uy, my + h * ux), (mx + h * uy, my - h * ux)], key=lambda x: math.dist(x, near))


def _arc_between(arc: Arc2, start: Point2, end: Point2) -> list[Point2]:
    """The vertices strictly between `start` and `end` on the arc's circle,
    the way the arc turns, at most `_ARC_STEP` apart."""
    c, r = arc.center, arc.radius
    (ax, ay), (mx, my), (bx, by) = arc.a, arc.mid, arc.b
    ccw = (mx - ax) * (by - my) - (my - ay) * (bx - mx) > 0
    a0 = math.atan2(start[1] - c[1], start[0] - c[0])
    a1 = math.atan2(end[1] - c[1], end[0] - c[0])
    sweep = (a1 - a0) % (2 * math.pi) if ccw else -((a0 - a1) % (2 * math.pi))
    steps = max(4, math.ceil(abs(sweep) / _ARC_STEP))
    return [(c[0] + r * math.cos(a0 + sweep * i / steps), c[1] + r * math.sin(a0 + sweep * i / steps))
            for i in range(1, steps)]
