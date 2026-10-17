"""The parts as they lie on their blank, and what a cutter reaches.

A part on a blank (`Placed`) maps its (u, v) frame, the frame of its
outline and its big faces' operations, into the setup's: the nest's
`transform` with the part flat and its machining face up, a quarter turn
and a move, mirrored where the part is seen from its other side, so every
ring is oriented again after the move (counter-clockwise around what it
encloses). Its faces are the machining face (`machine`, the stock's top),
the other big face, and the narrow faces.

**The opening test** (`unreached`) [`proposals/cam.md`, Where Auto Setup
goes wrong]: a cutter of radius r reaches the region opened by r (shrunk
by r, grown again), so what it leaves is the region less its opening. The
cutter must leave `TOOL_CLEARANCE` (Auto Setup's 0.1 mm) in the narrowest
passage it goes through, so the test opens by r plus half of that (less
`SLACK`): a slot the language made 0.1 wider than its cutter takes that
cutter. Of what is
left, slivers narrower than `CLEAN` are noise, the dog bones the region
holds are another operation's (`excused`), and the fillet a round cutter
always leaves in a sharp inside corner is what any cutter leaves: a piece
at a corner between two curves that meet at an angle (`sharp_corners`),
within the tangent points of the cutter's circle there. Anything else (a
passage too narrow, a rounded corner tighter than the cutter) is
unreached: a narrower cutter's.

**The hold** (`hold`): a part's footprint on the vacuum bed shrunk by a
margin, where air leaks in at every free edge, in cm².
"""
from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass

from shapely import affinity, make_valid, normalize
from shapely.geometry import LineString, MultiLineString, MultiPolygon, Point, Polygon
from shapely.geometry.base import BaseGeometry
from shapely.geometry.polygon import orient
from shapely.ops import nearest_points, unary_union

from ..core.geometry import polygons_of
from ..core.layout_types import PartLayout, Rings
from ..emit.arcs import Arc2, Circle2, Curve2, Line2, fit

Point2 = tuple[float, float]
AXES = ("x", "y", "z")

#: How much narrower (mm) a cutter must be than the narrowest passage it
#: machines (Auto Setup's `TOOL_CLEARANCE`, 0.01 cm).
TOOL_CLEARANCE = 0.1
#: Pieces of what a cutter leaves narrower than twice this (mm) are noise.
CLEAN = 0.005
#: How much less (mm) than half of `TOOL_CLEARANCE` the opening test
#: allows: the layout's circles are polygons with their corners on the
#: circle a degree apart, a hair inside it (1e-4 mm at 3 mm radius).
SLACK = 1e-3
#: How much narrower (mm) a lenient test takes the cutter (`unreached`).
LENIENT = 0.01
#: Beyond a corner's fillet, a tail of what a cutter leaves narrower than
#: this (mm) is the buffers' noise along a wall it touches [found by
#: fuzzing, 2026-10-17: 0.0103 mm, along 7 mm of a wall].
THIN = 0.05
#: A turn within this (radians) of half a turn is the boundary turning
#: back, whose side its sign does not tell (`sharp_corners`).
REVERSAL = 1e-3
#: Less than half a turn by this (radians) between a cutter's contacts is
#: as good as walls parallel: a passage, no corner (`_is_fillet`).
PASSAGE = 0.01
#: A piece of what a cutter leaves smaller than this (mm²) is none.
LEFT = 1e-2
#: Vertices of a ring closer than this (mm) are one: a union leaves some
#: next to each other, and `arcs.fit` read a corner of any angle into a
#: line between them [found 2026-10-17: a dog bone tangent to a wall at a
#: ring's start, 3e-18 mm].
REPEATED = 1e-9
#: Segments per quarter circle of the buffers.
QUAD = 32
#: A junction turning less than this (radians) is tangent: no corner.
TANGENT = 1e-4


def polygons(rings: Rings) -> list[Polygon]:
    """Rings as the layout writes them: an exterior (counter-clockwise),
    then its holes (clockwise), then the next polygon's."""
    out: list[Polygon] = []
    shell: list[list[float]] | None = None
    holes: list[list[list[float]]] = []
    for ring in rings:
        if _ring_area(ring) > 0:
            if shell is not None:
                out.append(Polygon(shell, holes))
            shell, holes = ring, []
        else:
            holes.append(ring)
    if shell is not None:
        out.append(Polygon(shell, holes))
    return out


def _ring_area(ring: Sequence[Sequence[float]]) -> float:
    a = 0.0
    for p, q in zip(ring, [*ring[1:], ring[0]]):
        a += p[0] * q[1] - q[0] * p[1]
    return a / 2


def rings_of(g: BaseGeometry) -> list[list[list[float]]]:
    """A region's rings for the plan file: each polygon's exterior
    (counter-clockwise), then its holes (clockwise)."""
    out: list[list[list[float]]] = []
    for poly in polygons_of(g):
        poly = orient(poly, 1.0)
        for ring in [poly.exterior, *poly.interiors]:
            out.append([[float(x), float(y)] for x, y in list(ring.coords)[:-1]])
    return out


def ring_points(ring: object) -> list[list[float]]:
    coords = list(getattr(ring, "coords"))
    return [[float(c[0]), float(c[1])] for c in coords[:-1]]


# -- a part on its blank ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Placed:
    """A part as it lies on its blank: x = a u + b v + x0, y = c u + d v +
    y0, from its (u, v) frame into the setup's."""
    part: PartLayout
    a: float
    b: float
    c: float
    d: float
    x0: float
    y0: float
    #: The world axis and sign of each face name (`front`: ("x", -1)).
    frame: dict[str, tuple[str, int]]

    @staticmethod
    def of(part: PartLayout, transform: list[list[float]], frame: dict[str, str]) -> Placed:
        axes = part["axes"]
        iu, iv, it = AXES.index(axes["u"]), AXES.index(axes["v"]), AXES.index(axes["t"])
        decoded = {name: (code[1], 1 if code[0] == "+" else -1) for name, code in frame.items()}
        machine_axis, sign = decoded[part["machine"]]
        assert machine_axis == axes["t"]
        t = part["box"]["max"][it] if sign > 0 else part["box"]["min"][it]
        rx, ry = transform[0], transform[1]
        return Placed(part, rx[iu], rx[iv], ry[iu], ry[iv], rx[3] + rx[it] * t, ry[3] + ry[it] * t, decoded)

    @property
    def path(self) -> str:
        return self.part["path"]

    @property
    def thickness(self) -> float:
        return self.part["thickness"]

    @property
    def mirrored(self) -> bool:
        return self.a * self.d - self.b * self.c < 0

    def point(self, u: float, v: float) -> Point2:
        return (self.a * u + self.b * v + self.x0, self.c * u + self.d * v + self.y0)

    def geometry(self, g: BaseGeometry) -> BaseGeometry:
        """A geometry in the part's (u, v) frame, in the setup's."""
        return affinity.affine_transform(g, [self.a, self.b, self.c, self.d, self.x0, self.y0])

    def region(self, rings: Rings) -> BaseGeometry:
        """Layout rings as a region in the setup's frame."""
        return self.geometry(unary_union(polygons(rings)))

    def face(self, name: str) -> str:
        """`machine`, `other` (the other big face) or `narrow`."""
        axis, sign = self.frame[name]
        if axis != self.part["axes"]["t"]:
            return "narrow"
        return "machine" if self.frame[self.part["machine"]] == (axis, sign) else "other"

    def is_through(self, depth: float) -> bool:
        return depth >= self.thickness - 1e-6

    # -- the outline -------------------------------------------------------------------------------

    def outline(self) -> Polygon:
        """The layout's outline (through cuts are in it)."""
        return _one(self.region(self.part["outline"]))

    def openings(self, big_hole: float, uv: bool = False) -> list[tuple[int, BaseGeometry]]:
        """The through pockets and the through holes wider than `big_hole`
        (either big face), by their index in the part's ops; in the part's
        frame with `uv`."""
        out: list[tuple[int, BaseGeometry]] = []
        for k, op in enumerate(self.part["ops"]):
            if op["kind"] == "pocket" and self.face(op["face"]) != "narrow" and self.is_through(op["depth"]):
                g = unary_union(polygons(op["shape"]))
            elif op["kind"] == "hole" and self.face(op["face"]) != "narrow" and \
                    (op["through"] or self.is_through(op["depth"])) and op["d"] > big_hole:
                g = Point(op["u"], op["v"]).buffer(op["d"] / 2, quad_segs=90)
            else:
                continue
            out.append((k, g if uv else self.geometry(g)))
        return out

    def machine_outline(self, big_hole: float, uv: bool = False) -> Polygon:
        """The outline less its openings (`openings`): what its contours cut,
        the outer loop of its faces; in the part's frame with `uv`."""
        shape: BaseGeometry = unary_union(polygons(self.part["outline"]))
        holes = [g for _k, g in self.openings(big_hole, uv=True)]
        if holes:
            shape = shape.difference(unary_union(holes))
        return _one(shape if uv else self.geometry(shape))

    def footprint(self) -> Polygon:
        """What lies on the bed: the outline less every through pocket and hole."""
        return self.machine_outline(0.0)


def _one(g: BaseGeometry) -> Polygon:
    pieces = [p for p in polygons_of(g) if p.area > 1e-6]
    if not pieces:
        return Polygon()
    return orient(max(pieces, key=lambda p: p.area), 1.0)


# -- corners and the opening test ---------------------------------------------------------------------

def _start_dir(c: Curve2) -> Point2:
    if isinstance(c, Line2):
        return _unit(c.b[0] - c.a[0], c.b[1] - c.a[1])
    assert isinstance(c, Arc2)
    return _arc_tangent(c, c.a)


def _end_dir(c: Curve2) -> Point2:
    if isinstance(c, Line2):
        return _unit(c.b[0] - c.a[0], c.b[1] - c.a[1])
    assert isinstance(c, Arc2)
    return _arc_tangent(c, c.b)


def _arc_tangent(c: Arc2, p: Point2) -> Point2:
    """The direction an arc runs at its point `p`."""
    ccw = (c.a[0] - c.center[0]) * (c.mid[1] - c.center[1]) - (c.a[1] - c.center[1]) * (c.mid[0] - c.center[0]) > 0
    rx, ry = p[0] - c.center[0], p[1] - c.center[1]
    return _unit(-ry, rx) if ccw else _unit(ry, -rx)


def _unit(x: float, y: float) -> Point2:
    n = math.hypot(x, y)
    return (x / n, y / n) if n > 0 else (0.0, 0.0)


def sharp_corners(region: BaseGeometry) -> list[tuple[Point2, float]]:
    """The region's corners that a round cutter cannot get into: where its
    boundary, as lines and arcs (`arcs.fit`), turns toward the region
    between two curves that do not meet tangent; each with its angle inside
    the region (radians, less than half a turn)."""
    out: list[tuple[Point2, float]] = []
    for whole in polygons_of(region):
        poly = _unrepeated_polygon(whole)
        if poly is None:
            continue
        poly = orient(poly, 1.0)                 # the region on the left of every ring
        for ring in [poly.exterior, *poly.interiors]:
            coords = list(ring.coords)
            curves = fit(coords)
            if len(curves) < 2 or any(isinstance(c, Circle2) for c in curves):
                continue
            for before, after in zip([curves[-1], *curves[:-1]], curves):
                t1, t2 = _end_dir(before), _start_dir(after)
                assert not isinstance(after, Circle2)
                start = after.a
                turn = math.atan2(t1[0] * t2[1] - t1[1] * t2[0], t1[0] * t2[0] + t1[1] * t2[1])
                if abs(turn) > math.pi - REVERSAL:
                    # (the boundary turns back: whether a needle of the region or a cusp of what is
                    # outside it, the sign of the turn does not tell [found 2026-10-17: two dog bones
                    # that touch, read as a corner of no angle, which took any piece for its fillet])
                    k = min(range(len(coords) - 1), key=lambda i: math.dist(coords[i], start))
                    (x0, y0), (x1, y1) = coords[k - 1 if k else -2][:2], coords[k + 1][:2]
                    turn = math.pi if poly.contains(Point((x0 + x1) / 2, (y0 + y1) / 2)) else -math.pi
                if turn > TANGENT:
                    out.append(((after.a[0], after.a[1]), math.pi - turn))
    return out


def unreached(region: BaseGeometry, radius: float, excused: BaseGeometry | None = None,
              clearance: float = TOOL_CLEARANCE, lenient: bool = False) -> list[Polygon]:
    """What a cutter of `radius` leaves of `region` (see the module's doc):
    the pieces neither its opening covers, nor the corners' fillets, nor
    `excused` (the dog bones other operations cut). `clearance` is what it
    must leave in the narrowest passage: none for a contour, which follows
    a fillet of its own radius (a box joint's). `lenient` (the plan's
    check) takes the cutter `LENIENT` narrower, a fillet's zone that much
    wider and slivers that much wider as noise: what is on the edge for the
    plan, which noise may tip either way, is no fault for the check [found
    by fuzzing, 2026-10-17]."""
    if region.is_empty:
        return []
    if not region.is_valid:
        region = make_valid(region)
    # (normalized: the buffers and the arcs read off the rings answered otherwise for one polygon
    # written from another start or the other way round [found by fuzzing, 2026-10-17])
    region = normalize(_unrepeated(region))
    r = radius + clearance / 2 - SLACK - (LENIENT if lenient else 0.0)
    wider = 2 * LENIENT if lenient else 0.0
    inner = shrunk(region, r)
    opening = inner.buffer(r, quad_segs=QUAD) if not inner.is_empty else Polygon()
    residue = region.difference(opening) if not opening.is_empty else region
    clean = CLEAN + (2 * LENIENT if lenient else 0.0)
    residue = _cleaned(residue, clean)
    if residue.is_empty:
        return []
    corners = sharp_corners(region) if not opening.is_empty else []
    rings = _boundary(region)

    def fillet(piece: Polygon) -> bool:
        return any(_is_fillet(piece, corner, angle, rings, inner, r, wider, excused) for corner, angle in corners)

    # (the fillets first, then the dog bones: a dog bone over a corner cuts
    # its fillet into pieces that are no fillet each [found by fuzzing,
    # 2026-10-17])
    out: list[Polygon] = []
    for piece in polygons_of(residue):
        if piece.area < LEFT or fillet(piece):
            continue
        rest = _cleaned(piece.difference(excused), clean) if excused is not None and not excused.is_empty else piece
        out += [q for q in polygons_of(rest) if q.area >= LEFT and not fillet(q)]
    return out


def _unrepeated(region: BaseGeometry) -> BaseGeometry:
    """The region without vertices closer than `REPEATED` to the one before,
    and without the rings that leaves no area."""
    out = [q for q in (_unrepeated_polygon(p) for p in polygons_of(region)) if q is not None]
    return out[0] if len(out) == 1 else MultiPolygon(out)


def _unrepeated_polygon(poly: Polygon) -> Polygon | None:
    def ring(coords: list[tuple[float, ...]]) -> list[tuple[float, float]]:
        out: list[tuple[float, float]] = []
        for x, y, *_z in coords:
            if not out or math.dist(out[-1], (x, y)) > REPEATED:
                out.append((x, y))
        while len(out) > 1 and math.dist(out[0], out[-1]) <= REPEATED:
            out.pop()
        return out if len(out) >= 3 else []

    shell = ring(list(poly.exterior.coords))
    if not shell:
        return None
    return Polygon(shell, [h for h in (ring(list(i.coords)) for i in poly.interiors) if h])


def _cleaned(g: BaseGeometry, clean: float = CLEAN) -> BaseGeometry:
    """Without slivers narrower than twice `clean`."""
    return g.buffer(-clean, join_style="mitre").buffer(clean, join_style="mitre")


def _boundary(region: BaseGeometry) -> list[LineString]:
    """The region's rings as closed lines, the region on their left."""
    out: list[LineString] = []
    for poly in polygons_of(region):
        poly = orient(poly, 1.0)
        out += [LineString(ring.coords) for ring in [poly.exterior, *poly.interiors]]
    return out


def _is_fillet(piece: Polygon, corner: Point2, angle: float, rings: Sequence[LineString], inner: BaseGeometry,
               r: float, wider: float = 0.0, excused: BaseGeometry | None = None) -> bool:
    """Whether a piece a cutter left is its fillet in the sharp corner: it
    touches the corner and lies within the tangent points of the cutter's
    circle between two straight sides of the corner's angle,
    `r / tan(angle / 2)` from it (a step lower than the cutter's radius
    too); or within the cutter's reach of it, from where the cutter that
    comes nearest the corner touches the boundary on either side of it, the
    boundary turning only toward the region between those two contacts (a
    line or an arc bulging away, a corner cut off by short edges), so that
    a passage too narrow for the cutter, whose mouth turns away from the
    region, is no fillet. An arc side puts the contact farther out than two
    lines do [found 2026-10-17: a Cabineo's access hole over the board's
    edge, a line meeting an arc, left a fillet 3.06 out where two lines
    leave one 1.81 out, and the plan sent the 2 mm cutter for it]. Along a
    dog bone (`excused`), which its own cutter mills, the boundary may turn
    away; what reaches past the corner's zone narrower than `THIN` is the
    buffers' noise along a wall the cutter touches. `wider` for the check."""
    v = Point(corner)
    # (cleaning the slivers, `unreached` takes a piece's tip back from an acute corner, the
    # farther the sharper the corner and the wider the cleaning [found by fuzzing, 2026-10-17: a
    # cap 0.36 mm high between an arc and a line at 11°, 0.03 mm back for the plan and 0.14 for
    # its check, which saw no fillet])
    back = min((CLEAN + wider) / math.sin(max(angle, 1e-9) / 2), r)
    if piece.distance(v) > 10 * CLEAN + wider + back or inner.is_empty:
        return False
    # (a corner of next to no angle reaches far: capped [found by fuzzing, 2026-10-17])
    lines = min(r / math.tan(max(angle, 1e-9) / 2), 1e4) * (1.1 if wider else 1.0) + 2 * CLEAN + wider
    if _within(piece, v, lines):
        return True
    ring = min(rings, key=lambda line: line.distance(v))
    if ring.distance(v) > 1e-3:
        return False
    v = ring.interpolate(ring.project(v))      # (`arcs.fit` puts a corner on its circle, a hair off the polygon)
    c = nearest_points(inner, v)[0]
    touch = c.buffer(r + 10 * CLEAN + wider, quad_segs=QUAD)
    length = ring.length
    s_v = ring.project(v)
    hits: list[tuple[float, float, Point]] = []        # forward and backward distance from the corner, contact
    met = ring.intersection(touch)
    for g in getattr(met, "geoms", [met]):
        if g.is_empty:
            continue
        if g.distance(v) < 1e-9:
            # the corner lies within the cutter's reach: the contacts are that stretch's ends
            ends = [Point(q) for q in (g.coords[0], g.coords[-1])] if hasattr(g, "coords") and len(g.coords) else [v]
            far = max(v.distance(q) for q in ends)
            return _within(piece, v, far + 2 * CLEAN + wider)
        at = g.interpolate(g.project(c)) if isinstance(g, LineString) else Point(g.coords[0])
        pos = ring.project(at)
        hits.append(((pos - s_v) % length, (s_v - pos) % length, at))
    if not hits:
        return False
    fwd = min(hits, key=lambda h: h[0])
    back = min(hits, key=lambda h: h[1])
    if fwd[0] + back[1] >= length - 1e-9:
        return False
    # the boundary from one contact through the corner to the other turns only toward the region, at
    # the contacts too (a passage's mouth corner)
    step = min(1.0, r / 2)
    path = [ring.interpolate((s_v - back[1] - step) % length)] + \
        _between(ring, s_v - back[1] - step, s_v + fwd[0] + step) + [ring.interpolate((s_v + fwd[0] + step) % length)]
    bones = excused.buffer(10 * CLEAN) if excused is not None and not excused.is_empty else None
    sides = _sides(ring, v)
    for a, b, d in zip(path, path[1:], path[2:]):
        ux, uy, wx, wy = b.x - a.x, b.y - a.y, d.x - b.x, d.y - b.y
        n = math.hypot(ux, uy) * math.hypot(wx, wy)
        if n > 1e-18 and (ux * wy - uy * wx) < -1e-6 * n and (bones is None or not bones.contains(b)) and \
                not any(line.distance(b) < 1e-6 and b.distance(end) > 1e-6 for line, end in sides):
            return False
    # and from one contact to the other less than half a turn: walls that run apart no more than
    # parallel are a passage the cutter does not get into [found 2026-10-17: a slot as wide as the
    # cutter, round its end beyond a dog bone, passed for the fillet of the corner there]
    if _turning([back[2], *_between(ring, s_v - back[1], s_v + fwd[0]), fwd[2]]) >= math.pi - PASSAGE:
        return False
    reach = max(v.distance(back[2]), v.distance(fwd[2])) * (1.1 if wider else 1.0) + 2 * CLEAN + wider
    return _within(piece, v, reach)


def _turning(path: Sequence[Point]) -> float:
    """How far a path turns left in all (radians, right turns negative)."""
    total = 0.0
    dirs = [(b.x - a.x, b.y - a.y) for a, b in zip(path, path[1:]) if a.distance(b) > 1e-12]
    for (ux, uy), (wx, wy) in zip(dirs, dirs[1:]):
        total += math.atan2(ux * wy - uy * wx, ux * wx + uy * wy)
    return total


def _sides(ring: LineString, v: Point) -> list[tuple[LineString, Point]]:
    """The two curves that meet at a corner (`arcs.fit`), each as the
    stretch of the ring it covers and with its other end: along an arc of
    them bulging into the region the boundary turns away from it, which a
    passage's mouth beyond them does too."""
    curves = [c for c in fit(list(ring.coords)) if not isinstance(c, Circle2)]
    if len(curves) < 2:
        return []
    k = min(range(len(curves)), key=lambda i: math.dist(curves[i].a, (v.x, v.y)))
    out: list[tuple[LineString, Point]] = []
    length = ring.length
    for c, other in ((curves[k - 1], curves[k - 1].a), (curves[k], curves[k].b)):
        a, b = Point(c.a), Point(c.b)
        s_a, s_b = ring.project(a), ring.project(b)
        if s_b <= s_a:
            s_b += length
        out.append((LineString([a, *_between(ring, s_a, s_b), b]), Point(other)))
    return out


def _within(piece: Polygon, v: Point, reach: float) -> bool:
    """Whether the piece lies within `reach` of the corner, but for what is
    narrower than `THIN` beyond it."""
    beyond = piece.difference(v.buffer(reach, quad_segs=QUAD))
    return beyond.area < CLEAN * CLEAN or _cleaned(beyond, THIN / 2).area < CLEAN * CLEAN


def _between(ring: LineString, start: float, end: float) -> list[Point]:
    """The ring's vertices strictly between two distances along it (`start`
    may be negative, `end` past its length: it wraps)."""
    coords = list(ring.coords)[:-1]
    length = ring.length
    positions: list[tuple[float, Point]] = []
    s = 0.0
    for k, q in enumerate(coords):
        positions.append((s, Point(q)))
        nxt = coords[(k + 1) % len(coords)]
        s += math.dist(q, nxt)
    out: list[tuple[float, Point]] = []
    for shift in (-length, 0.0, length):
        out += [(pos + shift, q) for pos, q in positions if start + 1e-12 < pos + shift < end - 1e-12]
    return [q for _pos, q in sorted(out, key=lambda e: e[0])]


def gets_in(region: BaseGeometry, radius: float, clearance: float = TOOL_CLEARANCE) -> bool:
    """Whether a cutter of `radius` gets into the region at all."""
    return not shrunk(region, radius + clearance / 2 - SLACK).is_empty


def shrunk(region: BaseGeometry, r: float) -> BaseGeometry:
    """The region shrunk by `r`: where a cutter of that radius can be
    centred. Without the pieces GEOS leaves where none can be, nearer the
    boundary than `r` [found 2026-10-17: 6e-8 mm² 0.08 mm from a wall that a
    dog bone met tangent where the ring started, which grown back took that
    corner's cusp for reached, and not the other three corners' cusps].
    Normalized first, as `unreached` says."""
    region = normalize(_unrepeated(region))
    inner = region.buffer(-r, quad_segs=QUAD)
    pieces = polygons_of(inner)
    edge = region.boundary
    keep = [q for q in pieces if edge.distance(q.representative_point()) >= r - 10 * CLEAN]
    return inner if len(keep) == len(pieces) else unary_union(keep) if keep else Polygon()


# -- holding --------------------------------------------------------------------------------------

def eroded(footprint: BaseGeometry, margin: float) -> BaseGeometry:
    """The footprint shrunk by `margin`: where the vacuum holds. Normalized
    first: where a narrow neck pinches off, shapely's result depends on
    where the rings start and which way they run (1% of the area, found
    by fuzzing, 2026-10-17)."""
    return normalize(footprint).buffer(-margin, quad_segs=QUAD) if margin > 0 else footprint


def hold(footprint: BaseGeometry, margin: float) -> float:
    """The footprint's area shrunk by `margin`, in cm²."""
    return float(eroded(footprint, margin).area) / 100.0


def lines_of(g: BaseGeometry) -> list[LineString]:
    """The lines of a geometry (a section of boundaries)."""
    if isinstance(g, LineString):
        return [g] if not g.is_empty else []
    if isinstance(g, MultiLineString) or hasattr(g, "geoms"):
        return [line for sub in getattr(g, "geoms", []) for line in lines_of(sub)]
    return []
