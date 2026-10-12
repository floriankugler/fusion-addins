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
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal

from shapely.geometry import LineString, MultiPolygon, Polygon
from shapely.geometry.base import BaseGeometry
from shapely.geometry.polygon import orient
from shapely.ops import unary_union

from lib import cutout_patterns as data

from ..emit.arcs import Arc2, Circle2, Line2, fit
from .directions import ExtentName
from .errors import LangError, one_of

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
    pieces = [p for p in _polygons(raw) if p.area > 1e-6]
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


def _polygons(g: BaseGeometry) -> list[Polygon]:
    if isinstance(g, Polygon):
        return [] if g.is_empty else [g]
    if isinstance(g, MultiPolygon):
        return [p for p in g.geoms if not p.is_empty]
    return [p for sub in getattr(g, "geoms", []) for p in _polygons(sub)]


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


def _fillet_ring(ring: Sequence[Point2], r: float) -> list[Point2] | None:
    """The ring with every corner filleted with radius `r`, convex and
    concave alike (the material lies to the left); None when a fillet does
    not fit between its neighbours."""
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
        if abs(turn) < _MIN_CORNER:
            fillets.append(None)
            continue
        side = 1.0 if turn > 0 else -1.0
        # the fillet touches both segments, not their extensions
        centres = [c for c in _offset_crossings(s1, s2, side, r, p)
                   if s1.param(s1.foot(c)) <= s1.length() + 1e-7 and s2.param(s2.foot(c)) >= -1e-7]
        if not centres:
            return None
        centre = min(centres, key=lambda c: math.dist(c, p))
        if math.dist(centre, p) > 4 * r / max(math.sin(abs(turn) / 2), 1e-3):
            return None
        fillets.append((centre, s1.foot(centre), s2.foot(centre), turn > 0))
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
        out += s.points(p, q)
        if after is not None:
            centre, a, b, ccw = after
            out += _arc_points(centre, r, a, b, ccw)[:-1]
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
    exterior = _fillet_ring(_ring_points(piece.exterior.coords), r)
    holes = [_fillet_ring(_ring_points(h.coords), r) for h in piece.interiors]
    if exterior is not None and all(h is not None for h in holes):
        out = Polygon(exterior, [h for h in holes if h is not None])
        if out.is_valid and abs(out.area - piece.area) < 0.5 * piece.area + 1:
            return [out]
    # A fillet does not fit between its neighbours (a short piece of edge
    # between two corners): round the outside corners as a cutter would,
    # leave the inside ones, and put the arcs the piece had back onto their
    # circles, which the two offsets blur.
    targets = _arc_targets(piece, 0.0)
    opened = piece.buffer(-r, join_style="round", quad_segs=16).buffer(r, join_style="round", quad_segs=16)
    return [_onto_circles(p, targets) for p in _polygons(opened) if p.area > 1e-6]


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
    for poly in _polygons(g):
        if len(poly.interiors) == 0:
            curves = fit(_ring_points(poly.exterior.coords))
            if len(curves) == 1 and isinstance(curves[0], Circle2):
                c, radius = curves[0].center, curves[0].radius
                if radius + d > _EPS:
                    out.append(_circle(c, radius + d))
                continue
        buffered = poly.buffer(d, join_style="mitre", mitre_limit=100.0)
        targets = _arc_targets(poly, d)
        out += [_onto_circles(p, targets) for p in _polygons(buffered)]
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


def _onto_circles(poly: Polygon, targets: list[_Target]) -> Polygon:
    if not targets:
        return poly
    rings = [_snap_ring(_ring_points(r.coords), targets) for r in [poly.exterior] + list(poly.interiors)]
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


def _snap_ring(points: list[Point2], targets: list[_Target]) -> list[Point2]:
    """Moves the vertices lying on (near) a target circle onto it, and
    redraws each run of them as an arc with evenly spaced vertices."""
    n = len(points)
    owner = [_target_of(p, targets) for p in points]
    if all(o is None for o in owner):
        return points
    if all(o is not None and o == owner[0] for o in owner):
        c, r = targets[owner[0]][0], targets[owner[0]][1]    # type: ignore[index]
        return _circle(c, r).exterior.coords[:-1]           # type: ignore[return-value]
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
