"""Door latches (Everlock, the Pull Lock 44 and the Sugatsune LL-66
one-touch latch) as hardware, as the door_latch_native add-in places them.

A latch holds a door or a drawer face shut against a carcass board beside
one of its edges: `cab.mount(latch("Pull Lock 44"), door=door,
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

and the carcass face a pilot pair for the strike: 14 mm to either side at
25 mm behind the door's inner face (Everlock), 10 at 24 (LL-66), and the
Pull Lock's keeper 9.5 to either side at 29 behind the door's front face,
where the lock sits (its drawing measures the keeper from the bezel).
"Below" is on the door, square to its edge, from the plane of the carcass
face away from the carcass board, "behind" on the carcass face from the
plane of the door's inner or front face, so an inset and an overlay door
get the same latch relative to the carcass. Pilot holes are `pilot`
(diameter, depth), by default 1/8" x 3 mm. One latch sits in the middle
of the door's edge (the door's extent along it), more run from `end=`
from its ends, evenly spaced; they are numbered from the door's own left,
seen standing in front of it, or from the bottom on an upright edge.

Refused as the add-in refuses: a pilot not smaller than the pattern's
narrowest pilot spacing (Everlock 16, Pull Lock 19, LL-66 20), several
latches on an edge no longer than twice `end=`, a carcass board parallel
to the door, and holes that do not fit on their face (`Board.hole_fits`:
each hole's centre and the four points its radius away along and across
the edge must lie on the door's or the carcass board's face, outside the
holes and pockets made before; the add-in probes its faces the same way,
including a pilot-sized circle at each LL-66 station's centre); and pilot
holes as deep as a board is thick. Beyond the add-in: latches so close
that a hole of one meets a hole of another, and a Pull Lock 44 on a door
thicker than 20.4 mm, where its pawl, behind the housing, would lie in
the door (`LatchShape.max_door`).

Mounted, a latch also places itself, closed, as boxes: the part on the
door and its strike on the carcass board, which interlock when closed, as
one body per latch (`latch_1`, ...) in an item `<door>_latches`. Their
sizes are one table, `LATCH_SHAPES`, separate from the drilling data,
measured from the latches' drawings and Sugatsune's CAD model. `reach` is
how far the part behind the door's front reaches from the carcass face,
which a drawer box behind a latched face keeps clear of.

Operations are named by latch, the other board and the latch's number:
`pull_lock_top_1` and `pull_lock_top_1_counterbore` in the door,
`everlock_top_1a` to `_1d` for its pilot holes (a and b nearer the carcass
face), `pull_lock_door_1a` and `_1b` in the carcass board.
"""
from __future__ import annotations

import math

from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal

from lib import door_latches as data

from ..core.directions import AXES, Axis
from ..core.errors import LangError, one_of
from ..core.faces import Face
from ..core.layout_types import BoxDict, HardwareBodyLayout
from ..core.part import Board
from ..core.refs import through, to
from ..core.shapes import circle
from ..joints.common import make_spacing
from .common import (TOLERANCE, LocalBox, Point2, along, check_hole, check_hole_size, check_pilot_depth, middle,
                     mm, numbering, uv, world_box)

if TYPE_CHECKING:
    from ..core.scope import Scope

#: The latches of `lib.door_latches`, by the names a build file uses.
LatchModel = Literal["Everlock", "Pull Lock 44", "LL-66"]
#: The latch in operation names.
_OP_NAMES: dict[str, str] = {"Everlock": "everlock", "Pull Lock 44": "pull_lock", "LL-66": "ll66"}
#: Two ends of a box along one direction, mm.
Extent = tuple[float, float]
#: A box relative to a latch: along the door's edge from the station,
#: below the carcass face (toward the door's middle) and behind the door's
#: inner face (negative: into the door and past its front).
LatchBox = LocalBox


@dataclass(frozen=True)
class LatchShape:
    """A latch, closed, as boxes around one station (mm; `LatchBox`): `door`
    boxes behind the door's inner face, `front` boxes measured from the
    door's front face instead (behind it; negative: proud of it), for the
    parts that rest on the front or are dimensioned from it, and `strike`
    boxes, the counterpart on the carcass face, behind the door's inner
    face or (`strike_front`) its front face. Only these numbers decide the
    boxes and `reach`."""
    door: tuple[LatchBox, ...]
    strike: tuple[LatchBox, ...] = ()
    front: tuple[LatchBox, ...] = ()
    #: Strike boxes measured from the door's front face, as `front`.
    strike_front: tuple[LatchBox, ...] = ()
    #: The thickest door it fits, mm, when a part behind the front reaches
    #: past the door's holes: on a thicker door it would lie in the door.
    max_door: float | None = None

    def latch_boxes(self, door_thickness: float) -> list[LatchBox]:
        """The part on the door as boxes, on a door `door_thickness` thick."""
        return list(self.door) + _from_front(self.front, door_thickness)

    def strike_boxes(self, door_thickness: float) -> list[LatchBox]:
        """The strike as boxes, on a door `door_thickness` thick."""
        return list(self.strike) + _from_front(self.strike_front, door_thickness)

    @property
    def reach(self) -> float:
        """How far below the carcass face the part on the door reaches,
        leaving out what stands proud of the door's front."""
        inside = list(self.door) + [box for box in self.front if box[2][1] > 0]
        return max(below[1] for _, below, _ in inside)


def _from_front(boxes: tuple[LatchBox, ...], door_thickness: float) -> list[LatchBox]:
    """Boxes measured from the door's front face, behind its inner face."""
    return [(along, below, (d0 - door_thickness, d1 - door_thickness)) for along, below, (d0, d1) in boxes]


#: Per latch, closed (measured 2026-10-12). Everlock: from the maker's
#: installation drawing (everlock.de, "Einbausituation"; body 40 wide, 32
#: deep, 60 above the carcass face; mounting wings 52 between their screw
#: columns; strike under the body, its screws 25 behind the door); without
#: the aluminium inset, which needs a 30 mm hole, so nothing on the front.
#: Pull Lock 44: from the lock's drawing (Florian, 2026-10-12; bezel 44
#: across and 2.5 proud, for panels 1 to 10 thick, which the counterbore
#: leaves; housing 38 across and 20.4 deep behind the front, clamp plate
#: 46.8 across behind the 10 mm panel, pawl to 33 behind the front; keeper
#: an L of 1.5 mm steel, 32.5 wide, its screw slots 19 apart, the plate from
#: 8.6 in front of the slots to 7.5 behind them, the lip 12.5 long); the
#: parts in the door's holes are squares inside them, so that no box reaches
#: into the door. LL-66: Sugatsune's CAD model LL-66_0.step (base 66 x 18.5
#: x 8.5, mechanism, counter plate 30 x 10.6 x 17), measured in its frame of
#: a door and a carcass board.
LATCH_SHAPES: dict[str, LatchShape] = {
    "Everlock": LatchShape(
        door=(((-20.0, 20.0), (10.0, 60.0), (0.0, 32.0)),       # body
              ((-32.0, 32.0), (16.6, 50.7), (0.0, 3.0)),        # mounting wings
              ((-6.0, 6.0), (0.0, 10.0), (17.0, 27.0))),        # bolt, rough width
        strike=(((-20.0, 20.0), (0.0, 9.0), (9.0, 34.0)),),
    ),
    "Pull Lock 44": LatchShape(
        door=(),
        # The keeper, from the door's front as the drawing has it (its slots
        # 29 behind the front, the drilled pair): its plate on the carcass
        # face, its lip toward the latch, where the pawl catches behind it.
        strike_front=(((-16.25, 16.25), (0.0, 1.5), (20.4, 36.5)),    # plate
                      ((-16.25, 16.25), (0.0, 12.5), (20.4, 21.9))),  # lip
        front=(((-22.0, 22.0), (12.0, 56.0), (-2.5, 0.0)),      # bezel, 34 below the carcass face
               ((-13.4, 13.4), (20.6, 47.4), (0.0, 20.4)),      # housing, a square in the 38.1 hole
               ((-16.9, 16.9), (17.1, 50.9), (10.0, 11.5)),     # clamp plate, a square in the 48 counterbore
               ((-8.0, 8.0), (7.5, 24.0), (20.4, 33.0))),       # pawl, rough width
        # The pawl swings from the housing's end, 20.4 behind the front, 2.5 mm
        # past the counterbore toward the carcass face [refused on thicker doors,
        # Florian 2026-10-13, after fuzzing found it reaching into a 22 mm door].
        max_door=20.4,
    ),
    "LL-66": LatchShape(
        door=(((-33.0, 33.0), (2.6, 21.1), (0.0, 8.5)),         # base
              ((-24.5, 24.5), (3.0, 24.6), (1.5, 24.4))),       # mechanism
        strike=(((-15.0, 15.0), (0.0, 10.6), (13.8, 30.7)),),   # counter plate
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
        return uv(self.door, {self.along: s + along, down.axis: self.face.value + down.sign * below})

    def on_carcass(self, s: float, along: float, behind: float) -> Point2:
        """A point on the carcass face, in its (u, v)."""
        back = self.inner.direction
        return uv(self.carcass, {self.along: s + along, back.axis: self.inner.value + back.sign * behind})

    def world_box(self, s: float, box: LatchBox) -> BoxDict:
        """A latch box in world coordinates: along the edge from the
        station, below the carcass face, behind the door's inner face."""
        return world_box(((along(self.along), s), (self.face.direction, self.face.value),
                          (self.inner.direction, self.inner.value)), box)


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
    #: The latch it is for, numbered as the latches are.
    latch: int = 1


class DoorLatch:
    """A latch model with the add-in's settings: `count` latches along the
    door's edge, one in the middle or the outer ones `end` from its ends
    (100 mm by default), and `pilot`, the (diameter, depth) of the pilot
    holes for the screws of the body and the strike (1/8" x 3 mm)."""

    def __init__(self, model: LatchModel, *, count: int = 1, end: float = data.END_OFFSET,
                 pilot: tuple[float, float] = (data.PREDRILL_DIAMETER, data.PREDRILL_DEPTH)):
        self.model: LatchModel = one_of(model, LatchModel, "latch()")
        self.pattern = data.LATCHES[model]
        make_spacing(model, count, None)
        if count > 1 and end <= 0:
            raise LangError(f"{model}: end= must be greater than zero, not {end:g}.")
        diameter, depth = check_hole_size(model, "pilot", pilot)
        if diameter >= self.pattern.max_predrill:
            raise LangError(f"{model}: a {mm(diameter)} pilot is too large for the latch's drilling pattern; "
                            f"it must be smaller than {mm(self.pattern.max_predrill)}.")
        self.count = count
        self.end = float(end)
        self.pilot = (diameter, depth)

    @property
    def name(self) -> str:
        return self.model

    @property
    def shape(self) -> LatchShape:
        return LATCH_SHAPES[self.model]

    @property
    def reach(self) -> float:
        """How far below the carcass face the latch takes room on the door,
        mm: the farthest its boxes behind the door's front reach, leaving
        out what stands proud of the front (`LatchShape.reach`; Everlock 60,
        Pull Lock 50.9, LL-66 24.6). A drawer box behind a latched face
        stays that far from the board the latch catches on, e.g. its top at
        `shelf.bottom.gap(latch.reach)`."""
        return self.shape.reach

    def mount(self, scope: Scope, /, *, door: Board, carcass: Board | Face) -> None:
        """`cab.mount(latch, door=door, carcass=top)`: drills the door and
        the carcass board for the latches and places them as boxes in the
        scope. `carcass=` is a board, the latch going against its big face
        toward the door's middle, or that face itself (`shelf.top`).
        Nothing is drilled unless every hole fits."""
        where = self._where(door, carcass)
        limit = self.shape.max_door
        if limit is not None and door.thickness > limit + TOLERANCE:
            raise LangError(f"{self.name}: {door.path} is {mm(door.thickness)} thick; the latch fits doors up to "
                            f"{mm(limit)}, behind which its pawl swings.", door.path)
        holes = self._holes(where)
        check_pilot_depth(self.name, door, self.pilot[1], "pilot")
        check_pilot_depth(self.name, where.carcass, self.pilot[1], "pilot")
        for hole in holes:                       # check everything before machining anything
            check_hole(self.name, hole.board, hole.face, hole.point, hole.d, f"hole {hole.name!r}")
        self._check_apart(holes)
        for anchor in self._anchors(where):
            if not door.hole_fits(where.inner, anchor, self.pilot[0]):
                raise LangError(f"{self.name}: the latch does not fit on {door.path}'s {where.inner.name} face.",
                                door.path)
        for hole in holes:
            if hole.kind == "counterbore":
                outer = Face(hole.board, -hole.face.direction)
                hole.board.add_pocket(hole.face, circle(hole.d, center=hole.point), to(outer, leave=hole.depth),
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
        edge: Axis = next(a for a in AXES if a not in (t, c))
        if isinstance(carcass, Face):
            if not carcass.is_big:
                raise LangError(f"{self.name}: {carcass!r} is a narrow face; name a big face of the carcass board.",
                                door.path)
            face = carcass
        else:
            door_middle = middle(db, c)
            if cb.lo[c] - TOLERANCE <= door_middle <= cb.hi[c] + TOLERANCE:
                raise LangError(f"{self.name}: {board.path} lies across the middle of the door; name the face the "
                                f"latch goes against, e.g. carcass={board.name}.bottom.", door.path)
            face = board.face(board.scope.frame.direction_of(c, 1 if door_middle > cb.hi[c] else -1))
        # the door's inner face: toward the carcass board
        mine, theirs = middle(db, t), middle(cb, t)
        if abs(theirs - mine) < TOLERANCE:
            raise LangError(f"{self.name}: {board.path} is centred on the door's thickness; which face is the "
                            "door's inner face?", door.path)
        inner = door.face(door.scope.frame.direction_of(t, 1 if theirs > mine else -1))
        length = db.hi[edge] - db.lo[edge]
        try:
            stations = [db.lo[edge] + s for s in data.stations(length, self.count, self.end)]
        except ValueError:
            raise LangError(f"{self.name}: the door's edge ({mm(length)}) is too short for {self.count} latches "
                            f"{mm(self.end)} from its ends.", door.path) from None
        if numbering(inner.direction, edge) < 0:
            stations.reverse()
        return _Where(door, inner, board, face, edge, tuple(stations))

    def _holes(self, where: _Where) -> list[_Hole]:
        """Every hole the latches need, in the add-in's order: the door's
        pilot holes, its main holes, the counterbores, the carcass pilots."""
        pattern, (pd, pdepth) = self.pattern, self.pilot
        kind = _OP_NAMES[self.model]
        sign = numbering(where.inner.direction, where.along)
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
                                    "pilot", pdepth, i))
            for h in pattern.door:
                if h.diameter is None:
                    continue
                point = where.on_door(s, h.along, h.below)
                if h.kind == "through":
                    mains.append(_Hole(door, where.inner, point, h.diameter, base, "through", latch=i))
                elif h.remaining is not None and door.thickness > h.remaining + TOLERANCE:
                    counterbores.append(_Hole(door, where.inner, point, h.diameter, base + "_counterbore",
                                              "counterbore", h.remaining, i))
            pair = sorted(pattern.carcass_holes(door.thickness), key=lambda p: p[0] * sign)
            for letter, (a, behind) in zip("ab", pair):
                strikes.append(_Hole(carcass, where.face, where.on_carcass(s, a, behind), pd,
                                     f"{kind}_{door.name}_{i}{letter}", "pilot", pdepth, i))
        return pilots + mains + counterbores + strikes

    def _check_apart(self, holes: list[_Hole]) -> None:
        """No hole of one latch meets a hole of another in the same board:
        each is checked against what was there before, not against the
        others [found by fuzzing, 2026-10-13: two Everlocks 34 mm apart,
        and three Pull Locks 9 apart, whose second hole the core refused
        once the first lock was drilled]. A latch's own holes may meet, as
        the Pull Lock's hole and its counterbore do."""
        for i, a in enumerate(holes):
            for b in holes[i + 1:]:
                if a.board is b.board and a.latch != b.latch and \
                        math.dist(a.point, b.point) < (a.d + b.d) / 2 - TOLERANCE:
                    raise LangError(f"{self.name}: latches {a.latch} and {b.latch} are too close: their holes "
                                    f"{a.name!r} and {b.name!r} in {a.board.path} meet.", a.board.path)

    def _anchors(self, where: _Where) -> list[Point2]:
        """Each station's centre on the door, where the add-in's layout
        anchors it."""
        return [where.on_door(s, 0.0, self.pattern.station_inset) for s in where.stations]

    def _place(self, scope: Scope, where: _Where) -> None:
        """The latches, closed, as boxes in `<door>_latches`: each latch and
        its strike one body, `latch_1`, `latch_2`, ..."""
        t = where.door.thickness
        boxes = self.shape.latch_boxes(t) + self.shape.strike_boxes(t)
        bodies = [HardwareBodyLayout(name=f"latch_{i}", boxes=[where.world_box(s, b) for b in boxes])
                  for i, s in enumerate(where.stations, 1)]
        scope.place_hardware(scope.unique_hardware_name(f"{where.door.name}_latches"), bodies)


def latch(model: LatchModel, *, count: int = 1, end: float = data.END_OFFSET,
          pilot: tuple[float, float] = (data.PREDRILL_DIAMETER, data.PREDRILL_DEPTH)) -> DoorLatch:
    """A door latch, `latch("Pull Lock 44", count=2)`: see `DoorLatch`, the
    type it returns."""
    return DoorLatch(model, count=count, end=end, pilot=pilot)
