"""Dog bones: round reliefs in the inside corners a router leaves rounded.

A router bit leaves its radius in every inside corner of a cut or pocket,
so a part with square corners does not go in. A dog bone takes the corner
out: a circle a little wider than the bit, on the corner's bisector, far
enough out that it reaches just past the corner. The geometry is the
dog_bones_native add-in's (`corner_relief`): the centre `(tool / 2) /
sin(angle)` from the corner, `angle` being the angle between the corner's
two edges (90 degrees: half a tool), the radius that plus `relief / 2`, so
the circle reaches `relief / 2` past the corner. Joints that cut inside
corners put such reliefs into their own cuts (tenons, half laps);
`hidden_relief` is their other kind, along one edge where the joint's
other board covers it.

`board.dogbones()` puts one into every inside corner the board has where
the call is written, or into those of the operations `at=` names; corners
made later get none, so the call goes after the cuts and joins whose
corners it should relieve. `corners` finds them: where two straight edges
of the material meet and the material goes around the corner by more than
half a turn, seen from either big face, at any angle. Straight means a
line of the outline or a shape as the emitter draws it: runs that stand
for an arc (`lang.emit.arcs.fit`), such as circles, round slot ends,
rounded corners and other reliefs, have no corners, nor does a junction
between a line and an arc, as the add-in only takes corners between
straight edges. A vertex that turns no more than an arc's segments do
(`arcs.MAX_STEP`) is not a corner either, nor one with an edge shorter
than `geometry.NARROWEST`. The regions are cleaned first
(`geometry.clean`), as every shape is: the spikes and slivers booleans
leave where two drawings of one edge or arc meet are not corners. So a
corner relieved before, by a joint or by a hole over it, is not relieved
again.

A corner's wall runs from the face it is seen on, the board's own or a
pocket's floor, down to the floor of what lies next to it, or through the
board: the relief goes as deep, a through cut where the corner is a corner
of the outline, else a pocket from that face. Like the add-in, it removes
only the material at its own corner: where the circle reaches other
material (across a narrow opening, into a neighbouring feature), that is
left alone; where it reaches into a cut, nothing changes there.
"""
from __future__ import annotations

import math
from collections.abc import Iterator
from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal

from shapely.geometry import Point, Polygon
from shapely.geometry.base import BaseGeometry
from shapely.geometry.polygon import orient
from shapely.ops import unary_union

from ..emit.arcs import MAX_STEP, Line2, fit
from .cutouts import circle_geometry
from .errors import LangError
from .ops import Cut, Hole, Pocket
from .shapes import Shape, circle
from .geometry import NARROWEST, opened, polygons_of

if TYPE_CHECKING:
    from .part import Board

#: The joints' kinds of dog bones: on the corner's bisector (`corner_relief`),
#: or along one edge, under the other board (`hidden_relief`).
DogBones = Literal["corner", "hidden"]
Point2 = tuple[float, float]

#: How far (mm) from a corner the probes into the space next to it lie.
_PROBE = 0.01
#: How close (mm) a point must be to count as on a line or at a corner.
_ON = 1e-6
#: Depths closer than this (mm) are one.
_EPS = 1e-9
#: Material (mm²) a relief may take beyond its corner and still be a circle.
_SLIVER = 1e-6


# -- the reliefs' geometry -------------------------------------------------------------------

def corner_relief(corner: Point2, a: Point2, b: Point2, tool: float, relief: float) -> Shape:
    """The dog bone at `corner`, whose edges run along the unit vectors `a`
    and `b` from it, as dog_bones_native draws it: centred on the bisector,
    `(tool / 2) / sin(angle)` from the corner, and that plus `relief / 2` in
    radius, so it reaches `relief / 2` past the corner. At 90 degrees it is
    `tool + relief` across, centred half a tool from the corner."""
    sin = abs(a[0] * b[1] - a[1] * b[0])
    if sin < 1e-9:
        raise LangError("a dog bone needs a corner, not two edges in one line.")
    reach = tool / 2 / sin
    bx, by = a[0] + b[0], a[1] + b[1]
    k = reach / math.hypot(bx, by)
    return circle(2 * reach + relief, (corner[0] + bx * k, corner[1] + by * k))


def hidden_relief(corner: Point2, along: Point2, tool: float, relief: float) -> Shape:
    """A dog bone that stays out of sight: centred on the edge that runs
    from `corner` along the unit vector `along`, half the tool plus half
    the relief from the corner, so it touches the corner's other edge and
    bulges past `along`'s edge instead, where a joint's other board covers
    it (a tenon's root under the mortise, a mortise's end under the
    shoulder, a lap's floor in the other board's notch)."""
    r = (tool + relief) / 2
    return circle(2 * r, (corner[0] + along[0] * r, corner[1] + along[1] * r))


# -- inside corners of a board ---------------------------------------------------------------

@dataclass(frozen=True)
class Corner:
    """An inside corner of a board's material, in the outline's frame:
    where two straight edges meet at `point`, running along the unit
    vectors `a` and `b` from it, the material around it on the far side
    of both."""
    point: Point2
    a: Point2
    b: Point2
    #: The big face (world name) it is seen from: where its relief is cut from.
    face: str
    #: Where its wall starts, as a depth from `face`: 0 on the face itself,
    #: a pocket's depth on that pocket's floor.
    top: float
    #: Where its wall ends, as a depth from `face`; None through the board.
    bottom: float | None
    #: Whether its relief is a through cut, part of the outline: what lies
    #: next to the corner is outside the outline, not a through pocket or hole.
    outline_cut: bool
    #: Every big face it is seen from: both for a corner through the board.
    faces: tuple[str, ...]
    #: The named operations whose contour runs through it and that cut the
    #: space next to it, in the board's order.
    ops: tuple[str, ...]
    #: Whether it lies on the outer boundary of the outline.
    on_outline: bool
    #: The material on the level it is seen on (the face, or a pocket's
    #: floor), for what its relief may take.
    level: BaseGeometry
    #: The material that its relief must leave alone below that level:
    #: everything shallower than `bottom`, or all of it for a through corner.
    keep: BaseGeometry

    @property
    def angle(self) -> float:
        """The angle between its edges, in radians: 90 degrees for a
        square corner, less for an acute one."""
        return math.acos(max(-1.0, min(1.0, self.a[0] * self.b[0] + self.a[1] * self.b[1])))


def corners(board: Board) -> list[Corner]:
    """Every inside corner of the board's material, seen from both big
    faces: those of its outline (through cuts included), of pockets and
    through pockets from either face, and of pockets on a pocket's floor.
    A corner through the board is listed once, from the face on which it
    starts deepest (where the add-in, run on that face, would relieve it
    most exactly). Holes count as round; V-grooves, chamfers and the
    operations on narrow faces do not count."""
    t = board.thickness
    outline = board.outline.geometry
    faces = [f.world_name for f in board.big_faces()]
    removed: dict[str, list[tuple[BaseGeometry, float]]] = {f: [] for f in faces}
    voids: list[BaseGeometry] = []
    for op in board.ops:
        if isinstance(op, Pocket):
            region, face, depth = op.shape.geometry, op.face, op.depth
        elif isinstance(op, Hole):
            region, face, depth = _disc((op.u, op.v), op.d / 2), op.face, (t if op.through else op.depth)
        else:
            continue
        if face not in removed:
            continue
        if depth >= t - _EPS:
            voids.append(region)
        else:
            removed[face].append((region, depth))
    # Pockets from both faces that meet go through where they overlap.
    first, second = faces
    for g0, d0 in removed[first]:
        for g1, d1 in removed[second]:
            if d0 + d1 >= t - _EPS:
                voids.append(g0.intersection(g1))
    void = unary_union(voids) if voids else Polygon()
    # (cleaned as every shape is, and opened, as the levels below: the spikes,
    # slivers and walls of no width of two drawings of one edge made corners
    # that came and went with the board's place [found by fuzzing, 2026-10-13
    # and 14])
    material = opened(outline.difference(void)) if voids else outline
    exteriors = [p.exterior for p in polygons_of(outline)]

    through: dict[tuple[float, float], Corner] = {}
    found: list[Corner] = []
    for face in faces:
        cuts = removed[face]
        levels = sorted({0.0} | {d for _, d in cuts})
        for top in levels:
            deeper = unary_union([g for g, d in cuts if d > top + _EPS])
            if top == 0.0:
                level = material
            else:
                level = unary_union([g for g, d in cuts if d >= top - _EPS]).intersection(material)
            # (opened: where pockets from either face meet along an edge of one of them, a level's
            # ring can run along itself, a wall of no width, kept or parted as the rounding fell, and
            # its ends made corners at one place of the board only [found by fuzzing, 2026-10-14])
            level = opened(level.difference(deeper))
            for point, a, b in _concave(level):
                probe = _toward(point, a, b, _PROBE)
                outside = not outline.contains(probe)
                if outside or void.contains(probe):
                    bottom = None
                else:
                    bottom = max((d for g, d in cuts if g.contains(probe)), default=0.0)
                    if bottom <= top + _EPS:
                        continue        # a wall going up: an island's corner, not an inside one
                if bottom is None:
                    keep = material
                else:
                    keep = material.difference(unary_union([g for g, d in cuts if d >= bottom - _EPS]))
                corner = Corner(point, a, b, face, top, bottom, outside, (face,),
                                _made_by(board, point, probe, face),
                                any(r.distance(Point(point)) < _ON for r in exteriors), level, keep)
                if bottom is not None:
                    found.append(corner)
                    continue
                key = (round(point[0], 6), round(point[1], 6))
                seen = through.get(key)
                if seen is None:
                    through[key] = corner
                else:
                    deepest = corner if corner.top > seen.top + _EPS else seen
                    through[key] = _with_faces(deepest, seen.faces + (face,))
    return list(through.values()) + found


def _with_faces(c: Corner, faces: tuple[str, ...]) -> Corner:
    return Corner(c.point, c.a, c.b, c.face, c.top, c.bottom, c.outline_cut, faces, c.ops, c.on_outline,
                  c.level, c.keep)


def _made_by(board: Board, point: Point2, probe: Point, face: str) -> tuple[str, ...]:
    """The named cuts and pockets whose contour runs through the corner
    and that cut the space next to it, seen from `face`."""
    names: list[str] = []
    p = Point(point)
    for op in board.ops:
        if not isinstance(op, (Cut, Pocket)) or not op.name:
            continue
        if isinstance(op, Pocket) and op.face != face and op.depth < board.thickness - _EPS:
            continue
        g = op.shape.geometry
        if g.boundary.distance(p) < _ON and g.contains(probe):
            names.append(op.name)
    return tuple(names)


def _concave(region: BaseGeometry) -> Iterator[tuple[Point2, Point2, Point2]]:
    """The region's inside corners: vertices between two straight edges
    (as `arcs.fit` reads the rings) where the boundary turns away from the
    material by more than an arc's segment does. Each with the unit
    vectors along its two edges, away from it."""
    for poly in polygons_of(region):
        poly = orient(poly, 1.0)              # the material on the left of every ring
        for ring in [poly.exterior, *poly.interiors]:
            curves = fit(list(ring.coords))
            for before, after in zip([curves[-1], *curves[:-1]], curves):
                if not (isinstance(before, Line2) and isinstance(after, Line2)):
                    continue
                v = after.a
                ix, iy = v[0] - before.a[0], v[1] - before.a[1]
                ox, oy = after.b[0] - v[0], after.b[1] - v[1]
                li, lo = math.hypot(ix, iy), math.hypot(ox, oy)
                if li < NARROWEST or lo < NARROWEST:
                    # (no corner is meant with an edge that short: what a relief with no
                    # relief= leaves where its circle's polygon passes a hair inside the
                    # corner [found by fuzzing, 2026-10-13])
                    continue
                if math.atan2(ix * oy - iy * ox, ix * ox + iy * oy) >= -MAX_STEP:
                    continue                  # a turn toward the material, or too slight
                yield v, (-ix / li, -iy / li), (ox / lo, oy / lo)


def _toward(point: Point2, a: Point2, b: Point2, distance: float) -> Point:
    """The point `distance` from `point` along the bisector of `a` and `b`:
    into the space next to a corner."""
    bx, by = a[0] + b[0], a[1] + b[1]
    k = distance / math.hypot(bx, by)
    return Point(point[0] + bx * k, point[1] + by * k)


def _disc(c: Point2, r: float) -> Polygon:
    """A hole as a polygon, drawn as every circle is (`circle_geometry`)."""
    return circle_geometry(c, r)


# -- what board.dogbones() asks for --------------------------------------------------------------

@dataclass(frozen=True)
class Target:
    """What `dogbones(at=)` names: a named operation (given as the
    operation, kept by its name), a big face by its world name, or the
    outline's outer boundary."""
    kind: Literal["operation", "face", "outline"]
    name: str = ""


@dataclass(frozen=True)
class Request:
    """One `board.dogbones()` call: the cutter and the relief, and which
    corners (None: all of them)."""
    tool: float
    relief: float
    at: tuple[Target, ...] | None


@dataclass(frozen=True)
class Relief:
    """The reliefs of one operation's corners at one depth, to add to the
    board as an operation named `name` (made unique by the board): a
    through cut when `face` is None, else a pocket from `face`, `depth`
    deep or through when `depth` is None."""
    name: str
    face: str | None
    depth: float | None
    shape: Shape


def reliefs(board: Board, request: Request) -> list[Relief]:
    """The reliefs a request puts into the board's corners as it is now,
    one per operation the corners belong to (the last that runs through
    each) and depth."""
    groups: dict[tuple[str, str | None, float | None], list[Shape]] = {}
    for c in corners(board):
        if request.at is not None and not any(_names(c, target) for target in request.at):
            continue
        base = f"{c.ops[-1]}_dogbones" if c.ops else "dogbones"
        face = None if c.bottom is None and c.outline_cut else c.face
        groups.setdefault((base, face, c.bottom), []).append(_relief_shape(c, request))
    # In the order of the operations they belong to, the outline's own corners
    # first, then by face and depth: the order the corners are found in
    # follows where each ring starts, which follows the board's place in the
    # world [found by fuzzing, 2026-10-13].
    order = {getattr(op, "name", None): k for k, op in enumerate(board.ops)}

    def key(item: tuple[tuple[str, str | None, float | None], list[Shape]]) -> tuple[int, str, float]:
        (base, face, depth), _ = item
        owner = base.removesuffix("_dogbones")
        return (order.get(owner, -1), face or "", math.inf if depth is None else depth)

    out: list[Relief] = []
    for (base, face, depth), shapes in sorted(groups.items(), key=key):
        shape = shapes[0]
        for s in shapes[1:]:
            shape = shape.union(s)
        out.append(Relief(base, face, depth, shape))
    return out


def _names(c: Corner, target: Target) -> bool:
    if target.kind == "operation":
        return target.name in c.ops
    if target.kind == "face":
        return target.name in c.faces
    return c.on_outline


def _near_part(g: BaseGeometry, p: Point, near: float) -> BaseGeometry:
    """What of `g` is held on to the part near `p` by more than a point:
    a piece that touches it at a point only is apart, whether shapely
    made the two one polygon or two [found by fuzzing, 2026-10-14: a
    piece of 7.4 mm2 touching the corner's material at a point was its
    own at one place of the board and another's at the next]."""
    opened = g.buffer(-_ON, join_style="mitre", mitre_limit=1e6)
    parts = [h for h in polygons_of(opened) if h.distance(p) < near + _ON]
    if not parts or len(parts) == len(polygons_of(opened)):
        return g
    return g.intersection(unary_union(parts).buffer(2 * _ON, join_style="mitre", mitre_limit=1e6))


def _relief_shape(c: Corner, request: Request) -> Shape:
    """The corner's relief: the add-in's circle, less any material it
    reaches that is not the corner's own (the piece of the circle on the
    corner's level that touches the corner)."""
    disc = corner_relief(c.point, c.a, c.b, request.tool, request.relief)
    p = Point(c.point)
    # (with relief=0 the circle runs through the corner, its polygon a hair
    # inside, and touched nothing of the corner's own: the whole relief went
    # as another's material [found by fuzzing, 2026-10-13]. The polygon's
    # chord crosses the corner's edges up to its sagitta over the sine of
    # the angle between edge and circle from the corner; twice that.)
    radius = (request.tool / 2) / math.sin(c.angle) + request.relief / 2
    sagitta = radius * (1 - math.cos(math.pi / 360))           # the whole degrees' (`circle_geometry`)
    near = 2 * sagitta / math.sin(max((math.pi - c.angle) / 2, MAX_STEP / 2)) + _ON
    own = _near_part(unary_union([g for g in polygons_of(disc.geometry.intersection(c.level)) if g.distance(p) < near]),
                     p, near)
    excess = disc.geometry.intersection(c.keep).difference(own)
    if excess.area <= _SLIVER:
        return disc
    return Shape(disc.geometry.difference(excess))
