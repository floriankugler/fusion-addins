"""Door latches (Everlock, the Pull Lock 44 and the Sugatsune LL-66
one-touch latch) as hardware, as the door_latch_native add-in places them.

A latch holds a door or a drawer face shut against a carcass board beside
one of its edges: `cab.mount(DoorLatch("Pull Lock 44"), door=door,
carcass=top)`. Its body sits on the door's inner face, the big face toward
the carcass board, its strike (the LL-66's counter plate) on the carcass
face, the carcass board's big face toward the door's middle, or the face
given (`carcass=shelf.top` for a latch above a shelf). The latch sits
beside the door's edge on that side: under a carcass top, the door's upper
edge. The add-in has the same selected as two edges: the door's edge on
its inner face and the carcass face's edge next to it.

Per latch the door gets (positions and sizes from `lib.door_latches`):

- Everlock: a 25 mm finger hole through the door, 30 mm below the carcass
  face, and four pilot holes for the body, 26 mm to either side, 26 and 42
  mm below it;
- Pull Lock 44: a 38.1 mm hole through the door, 34 mm below the carcass
  face, and from its inner face a 48 mm counterbore that leaves 10 mm at
  the front, on a door thicker than that;
- LL-66: two pilot holes for the body, 28 mm to either side, 10 mm below;

and the carcass face a pilot pair for the strike, behind the door's inner
face: 14 mm to either side at 25 mm (Everlock), 9.5 at 29 (Pull Lock), 10
at 24 (LL-66). "Below" is on the door, square to its edge, from the plane
of the carcass face away from the carcass board, "behind" on the carcass
face from the plane of the door's inner face, so an inset and an overlay
door get the same latch relative to the carcass. Pilot holes are
`predrill` (diameter, depth), by default 1/8" x 3 mm. One latch sits in the
middle of the door's edge (the door's extent along it), more run from
`end=` from its ends, evenly spaced; they are numbered from the door's own
left, seen standing in front of it, or from the bottom on an upright edge.

Refused as the add-in refuses: a pre-drill not smaller than the pattern's
narrowest pilot spacing (Everlock 16, Pull Lock 19, LL-66 20), several
latches on an edge no longer than twice `end=`, a carcass board parallel
to the door, and holes that do not lie on their face: each hole's centre
and the four points its radius away along and across the edge must be on
the door's or the carcass board's outline (the add-in probes its faces
the same way, including a pilot-sized circle at each LL-66 station's
centre). Pockets and holes made before are not taken into account.

Mounted, a latch also places itself, closed, as boxes: the part on the
door (`latch_1`, ...) and its strike on the carcass board (`strike_1`,
...), one body each. Their sizes are one table, `LATCH_SHAPES`, separate
from the drilling data; with no drawings of the latches in the repo most
of its numbers are rough, marked as such. `reach` is how far the part on
the door reaches from the carcass face, which a drawer box behind a
latched face keeps clear of.

Operations are named by latch, the other board and the latch's number:
`pull_lock_top_1` and `pull_lock_top_1_counterbore` in the door,
`everlock_top_1a` to `_1d` for its pilot holes (a and b nearer the carcass
face), `pull_lock_door_1a` and `_1b` in the carcass board.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal

from shapely.geometry import Point

from lib import door_latches as data

from ..core import directions
from ..core.directions import AXES, Axis, Direction
from ..core.errors import LangError, one_of
from ..core.layout_types import BoxDict, HardwareBodyLayout
from ..core.part import Board, Face
from ..core.refs import through, to
from ..core.shapes import circle

if TYPE_CHECKING:
    from ..core.scope import Scope

#: The latches of `lib.door_latches`, by the names a build file uses.
LatchModel = Literal["Everlock", "Pull Lock 44", "LL-66"]
#: The latch in operation names.
_OP_NAMES: dict[str, str] = {"Everlock": "everlock", "Pull Lock 44": "pull_lock", "LL-66": "ll66"}
EPS = 1e-6
Point2 = tuple[float, float]
#: Two ends of a box along one direction, mm.
Extent = tuple[float, float]
#: A box relative to a latch: along the door's edge from the station,
#: below the carcass face (toward the door's middle) and behind the door's
#: inner face (negative: into the door and past its front).
LatchBox = tuple[Extent, Extent, Extent]


@dataclass(frozen=True)
class LatchShape:
    """A latch, closed, as boxes around one station (mm; `LatchBox`): the
    part on the door, `body` on its inner face, `core` (along, below)
    through its thickness and `knob` (along, below, how far it stands
    proud) on its front, and its counterpart on the carcass board,
    `strike` (the LL-66's counter plate) under the carcass face. Only these
    numbers decide the boxes and `reach`."""
    body: LatchBox
    strike: LatchBox
    core: tuple[Extent, Extent] | None = None
    knob: tuple[Extent, Extent, float] | None = None

    def latch_boxes(self, door_thickness: float) -> list[LatchBox]:
        """The part on the door as boxes, on a door `door_thickness` thick."""
        boxes = [self.body]
        if self.core is not None:
            boxes.append((self.core[0], self.core[1], (-door_thickness, 0.0)))
        if self.knob is not None:
            along, below, proud = self.knob
            boxes.append((along, below, (-door_thickness - proud, -door_thickness)))
        return boxes

    @property
    def reach(self) -> float:
        """How far below the carcass face the part on the door reaches."""
        return max(below[1] for _, below, _ in self.latch_boxes(0.0))


#: Per latch, closed. There are no drawings of the latches in the repo
#: (2026-10-12), so most numbers are rough: boxes around the drilling
#: pattern of `lib.door_latches`, a body about 4 around its screws' centres
#: (heads some 8 across), a strike plate 6 around its screws and 3 thick,
#: and the body reaching up to the strike and back to its front edge. To be
#: replaced by measured numbers when drawings or CAD files come.
LATCH_SHAPES: dict[str, LatchShape] = {
    "Everlock": LatchShape(
        body=((-30.0, 30.0),      # rough: the screws 26 to either side, + 4
              (3.0, 46.0),        # rough: from the strike down to 4 beyond the far screw row (42)
              (0.0, 19.0)),       # rough: back to the strike's front edge
        strike=((-20.0, 20.0),    # rough: its screws 14 to either side, + 6
                (0.0, 3.0),       # rough: a 3 mm plate
                (19.0, 31.0)),    # rough: its screws 25 behind the door, +- 6
    ),
    "Pull Lock 44": LatchShape(
        body=((-24.0, 24.0),      # rough: the rear housing, as wide as the 48 mm counterbore
              (3.0, 58.0),        # rough: from the strike down to the counterbore's far edge (34 + 24)
              (0.0, 23.0)),       # rough: back to the strike's front edge
        strike=((-15.5, 15.5),    # rough: its screws 9.5 to either side, + 6
                (0.0, 3.0),       # rough: a 3 mm plate
                (23.0, 35.0)),    # rough: its screws 29 behind the door, +- 6
        core=((-13.4, 13.4),      # a square inside the 38.1 mm hole, 34 below (drilling data)
              (20.6, 47.4)),
        knob=((-22.0, 22.0),      # rough: the "44" read as the knob's diameter, centred on the hole
              (12.0, 56.0),
              8.0),               # rough: how far it stands proud of the door's front
    ),
    "LL-66": LatchShape(
        body=((-33.0, 33.0),      # rough: 66 long, read from the name (the holes 56 apart leave 5 each end)
              (3.5, 23.5),        # its top 3.5 below the carcass face (datasheet, as the add-in has it), 20 high rough
              (0.0, 18.0)),       # rough: back to the counter plate's front edge
        strike=((-16.0, 16.0),    # rough: its screws 10 to either side, + 6
                (0.0, 3.0),       # rough: a 3 mm plate
                (18.0, 30.0)),    # rough: its screws 24 behind the door, +- 6
    ),
}


@dataclass(frozen=True)
class _Where:
    """Where a latch goes, in world terms: the door's inner face, the
    carcass face, the axis of the door's edge and the stations on it in
    their order."""
    door: Board
    inner: Face
    carcass: Board
    face: Face
    along: Axis
    stations: tuple[float, ...]

    def on_door(self, s: float, along: float, below: float) -> Point2:
        """A point on the door's inner face, in its (u, v)."""
        down = self.face.direction
        return _uv(self.door, {self.along: s + along, down.axis: self.face.value + down.sign * below})

    def on_carcass(self, s: float, along: float, behind: float) -> Point2:
        """A point on the carcass face, in its (u, v)."""
        back = self.inner.direction
        return _uv(self.carcass, {self.along: s + along, back.axis: self.inner.value + back.sign * behind})

    def world_box(self, s: float, box: LatchBox) -> BoxDict:
        """A latch box in world coordinates."""
        def span(start: float, direction: Direction, extent: Extent) -> Extent:
            a, b = start + direction.sign * extent[0], start + direction.sign * extent[1]
            return (min(a, b), max(a, b))

        along, below, behind = box
        ranges: dict[Axis, Extent] = {
            self.along: (s + along[0], s + along[1]),
            self.face.axis: span(self.face.value, self.face.direction, below),
            self.inner.axis: span(self.inner.value, self.inner.direction, behind),
        }
        return {"min": [ranges[a][0] for a in AXES], "max": [ranges[a][1] for a in AXES]}


@dataclass(frozen=True)
class _Hole:
    """A hole to make, found before anything is machined."""
    board: Board
    face: Face
    point: Point2
    d: float
    name: str
    #: "pilot" (`depth` deep), "through", or "counterbore" (leaving `depth`
    #: of material at the door's front).
    kind: data.HoleKind
    depth: float = 0.0


class DoorLatch:
    """A latch model with the add-in's settings: `count` latches along the
    door's edge, one in the middle or the outer ones `end` from its ends
    (100 mm by default), and `predrill`, the (diameter, depth) of the pilot
    holes for the screws of the body and the strike (1/8" x 3 mm)."""

    def __init__(self, model: LatchModel, count: int = 1, end: float = data.END_OFFSET,
                 predrill: tuple[float, float] = (data.PREDRILL_DIAMETER, data.PREDRILL_DEPTH)):
        self.model: LatchModel = one_of(model, LatchModel, "DoorLatch()")
        self.pattern = data.LATCHES[model]
        if count < 1:
            raise LangError(f"{model}: there must be at least one latch, not count={count}.")
        if count > 1 and end <= 0:
            raise LangError(f"{model}: end= must be greater than zero, not {end:g}.")
        diameter, depth = predrill
        if diameter <= 0 or depth <= 0:
            raise LangError(f"{model}: the pre-drill's diameter and depth must be greater than zero, "
                            f"not {diameter:g} x {depth:g}.")
        if diameter >= self.pattern.max_predrill:
            raise LangError(f"{model}: a {diameter:g} mm pre-drill is too large for the latch's drilling pattern; "
                            f"it must be smaller than {self.pattern.max_predrill:g}.")
        self.count = count
        self.end = end
        self.predrill = (float(diameter), float(depth))

    @property
    def name(self) -> str:
        return self.model

    @property
    def shape(self) -> LatchShape:
        return LATCH_SHAPES[self.model]

    @property
    def reach(self) -> float:
        """How far from the carcass face the latch takes room on the door,
        mm (its boxes' far end, `LATCH_SHAPES`: Everlock 46, Pull Lock 58,
        LL-66 23.5): a drawer box behind a latched face stays that far
        from the board the latch catches on, e.g. its top at
        `shelf.bottom.gap(latch.reach)`."""
        return self.shape.reach

    def mount(self, scope: Scope, /, **options: object) -> None:
        """`cab.mount(latch, door=door, carcass=top)`: drills the door and
        the carcass board for the latches and places them as boxes in the
        scope. `carcass=` is a board, the latch going against its big face
        toward the door's middle, or that face itself (`shelf.top`)."""
        unknown = set(options) - {"door", "carcass"}
        if unknown or "door" not in options or "carcass" not in options:
            raise LangError(f"{self.name}: mount() takes door= and carcass=, got {sorted(options)}.", scope.path)
        door, carcass = options["door"], options["carcass"]
        if not isinstance(door, Board):
            raise LangError(f"{self.name}: door= must be a board, not {door!r}.", scope.path)
        if not isinstance(carcass, (Board, Face)):
            raise LangError(f"{self.name}: carcass= must be a board or one of its faces, not {carcass!r}.",
                            scope.path)
        where = self._where(door, carcass)
        holes = self._holes(where)
        for hole in holes:                       # check everything before machining anything
            if not _fits(hole.board, hole.point, hole.d):
                raise LangError(f"{self.name}: the hole {hole.name!r} ({hole.d:g} mm) does not lie on "
                                f"{hole.board.path}'s {hole.face.name} face.", hole.board.path)
        for anchor in self._anchors(where):
            if not _fits(door, anchor, self.predrill[0]):
                raise LangError(f"{self.name}: the latch does not fit on {door.path}'s {where.inner.name} face.",
                                door.path)
        for hole in holes:
            if hole.kind == "counterbore":
                outer = Face(hole.board, -hole.face.direction)
                hole.board.add_pocket(hole.face, circle(hole.d, center=hole.point), to(outer, -hole.depth),
                                      hole.board.unique_op_name(hole.name))
            else:
                depth = through if hole.kind == "through" else hole.depth
                hole.board.add_hole(hole.face, hole.point, hole.d, depth, hole.board.unique_op_name(hole.name))
        self._place(scope, where)

    # -- where ---------------------------------------------------------------------------------------

    def _where(self, door: Board, carcass: Board | Face) -> _Where:
        board = carcass.part if isinstance(carcass, Face) else carcass
        if board is door:
            raise LangError(f"{self.name}: the door and the carcass board must be two boards.", door.path)
        db, cb = door.box(), board.box()
        t, c = door.t_axis, board.t_axis
        if c == t:
            raise LangError(f"{self.name}: {board.path} lies parallel to the door; the latch needs a carcass board "
                            "square to it, beside one of its edges.", door.path)
        along: Axis = next(a for a in AXES if a not in (t, c))
        if isinstance(carcass, Face):
            if not carcass.is_big:
                raise LangError(f"{self.name}: {carcass!r} is a narrow face; name a big face of the carcass board.",
                                door.path)
            face = carcass
        else:
            middle = (db.lo[c] + db.hi[c]) / 2
            if cb.lo[c] < middle < cb.hi[c]:
                raise LangError(f"{self.name}: {board.path} lies across the middle of the door; name the face the "
                                f"latch goes against, e.g. carcass={board.name}.bottom.", door.path)
            face = Face(board, board.scope.frame.direction_of(c, 1 if middle > cb.hi[c] else -1))
        # the door's inner face: toward the carcass board
        mine, theirs = (db.lo[t] + db.hi[t]) / 2, (cb.lo[t] + cb.hi[t]) / 2
        if abs(theirs - mine) < EPS:
            raise LangError(f"{self.name}: {board.path} is centred on the door's thickness; which face is the "
                            "door's inner face?", door.path)
        inner = Face(door, door.scope.frame.direction_of(t, 1 if theirs > mine else -1))
        length = db.hi[along] - db.lo[along]
        try:
            stations = [db.lo[along] + s for s in data.stations(length, self.count, self.end)]
        except ValueError:
            raise LangError(f"{self.name}: the door's edge ({length:g} mm) is too short for {self.count} latches "
                            f"{self.end:g} from its ends.", door.path) from None
        if _order(inner.direction, along) < 0:
            stations.reverse()
        return _Where(door, inner, board, face, along, tuple(stations))

    def _holes(self, where: _Where) -> list[_Hole]:
        """Every hole the latches need, in the add-in's order: the door's
        pilot holes, its main holes, the counterbores, the carcass pilots."""
        pattern, (pd, pdepth) = self.pattern, self.predrill
        kind = _OP_NAMES[self.model]
        sign = _order(where.inner.direction, where.along)
        door, carcass = where.door, where.carcass
        pilots: list[_Hole] = []
        mains: list[_Hole] = []
        counterbores: list[_Hole] = []
        strikes: list[_Hole] = []
        door_pilots = sorted((h for h in pattern.door if h.kind == "pilot"), key=lambda h: (h.below, h.along * sign))
        for i, s in enumerate(where.stations, 1):
            base = f"{kind}_{carcass.name}_{i}"
            for letter, h in zip("abcd", door_pilots):
                pilots.append(_Hole(door, where.inner, where.on_door(s, h.along, h.below), pd, base + letter,
                                    "pilot", pdepth))
            for h in pattern.door:
                if h.diameter is None:
                    continue
                point = where.on_door(s, h.along, h.below)
                if h.kind == "through":
                    mains.append(_Hole(door, where.inner, point, h.diameter, base, "through"))
                elif h.remaining is not None and door.thickness > h.remaining:
                    counterbores.append(_Hole(door, where.inner, point, h.diameter, base + "_counterbore",
                                              "counterbore", h.remaining))
            pair = sorted(pattern.carcass_holes(), key=lambda p: p[0] * sign)
            for letter, (a, behind) in zip("ab", pair):
                strikes.append(_Hole(carcass, where.face, where.on_carcass(s, a, behind), pd,
                                     f"{kind}_{door.name}_{i}{letter}", "pilot", pdepth))
        return pilots + mains + counterbores + strikes

    def _anchors(self, where: _Where) -> list[Point2]:
        """Each station's centre on the door, where the add-in's layout
        anchors it."""
        return [where.on_door(s, 0.0, self.pattern.station_inset) for s in where.stations]

    def _place(self, scope: Scope, where: _Where) -> None:
        """The latches, closed, and their strikes as boxes, one body each."""
        latch, strike = self.shape.latch_boxes(where.door.thickness), self.shape.strike
        bodies: list[HardwareBodyLayout] = []
        for i, s in enumerate(where.stations, 1):
            bodies.append(HardwareBodyLayout(name=f"latch_{i}", boxes=[where.world_box(s, b) for b in latch]))
            bodies.append(HardwareBodyLayout(name=f"strike_{i}", boxes=[where.world_box(s, strike)]))
        name, n = "latches", 2
        while (name in scope.parts or name in scope.children
               or any(item["name"] == name for item in scope.hardware)):
            name, n = f"latches_{n}", n + 1
        scope.place_hardware(name, bodies)


def _uv(board: Board, coords: dict[Axis, float]) -> Point2:
    return (coords[board.u_axis], coords[board.v_axis])


def _fits(board: Board, point: Point2, d: float) -> bool:
    """Whether a hole's centre and the points its radius away along both
    of the face's axes lie on the board's outline."""
    r = d / 2
    u, v = point
    outline = board.outline.geometry
    return all(outline.distance(Point(p)) <= EPS for p in ((u, v), (u - r, v), (u + r, v), (u, v - r), (u, v + r)))


def _order(back: Direction, along: Axis) -> int:
    """Which way the latches are numbered along the edge's axis: from the
    door's own left to its right, seen standing in front of it (its right
    is back x up, `back` pointing from the door to the carcass), from the
    bottom up on an upright edge, else along the world axis."""
    up = directions.frame.direction("top")
    if up.axis == along:
        return up.sign
    if back.axis == up.axis:                  # a door lying flat
        return 1
    (bx, by, bz), (ux, uy, uz) = back.vector, up.vector
    right = (by * uz - bz * uy, bz * ux - bx * uz, bx * uy - by * ux)
    return 1 if right[AXES.index(along)] > 0 else -1
