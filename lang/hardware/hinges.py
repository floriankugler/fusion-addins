"""Concealed hinges (Blum CLIP top 110 for thin doors) as hardware.

`cab.mount(hinge, door=door, carcass=left)` hinges a door on a carcass
board standing square to it: a side for a door that opens sideways, a
partition between two doors, the top or bottom for a flap. It drills what
the concealed_hinge_native add-in drills from the two edges it is given:
the door's hinged edge, the edge of its inner face (the big face toward
the carcass board) next to that board, and the carcass board's edge, the
front edge of its face toward the door's middle, where the mounting
plates go, or of the face given (`carcass=wall.left`, for a partition
the door's middle lies within).

- `count=` hinges (2; the add-in always makes two), the outer ones'
  centres `end=` from the ends of the door's hinged edge (60), the rest
  evenly between (`lib.stations`).
- Per hinge two holes in the door's inner face, 10 mm wide and 5 deep and
  32 apart along the edge, in a row 27 mm (+0 model) or 30 mm (+3) from
  the carcass board's face toward the door's middle, whatever the door's
  overlay or gap.
- Per hinge two pre-drill holes for the mounting plate's screws in the
  carcass board's face, 32 apart, 38.5 mm behind the door's inner face,
  `pilot=` wide and deep (1/8 inch by 3).
- The hinges are placed as `<door>_hinges`, a body per hinge made of
  four boxes, cup, arm, clip and mounting plate (`HINGE_SHAPES`, measured
  from Häfele's CAD models). Hinges are numbered by their place
  along the edge, from the bottom, or for a flap from the door's own
  left, seen standing in front of it, so a cabinet and a module in the
  van's terms number them alike: bodies `hinge_1`, `hinge_2`, ...

Refused as the add-in refuses: an end distance under 27 mm (its dialog's
smallest), hinges closer than their mounting plates are long, 56.2 mm (the
add-in refuses 42 or closer, where their hole pairs meet; the plates meet
before, Florian 2026-10-13), a door and carcass board that are one board, and holes that do not fit on
their face (`Board.hole_fits`: off the board, over its edge, or in a hole
or pocket made before), or as deep as the board is thick. The add-in's
edges are boards here, so the door and the carcass board must stand
square to each other: the hinged edge then runs along the carcass board's
face. The hinge dictates nothing about the door's overlay or gap that the
add-in knows (its plausibility check of the overlay is switched off), so
there is no door-sizing method.

Drilling dimensions from `lib/concealed_hinges.py`, the add-in's, which
it reads too. Operations are named by the other board and the hinge,
`hinge_left_1a` and `_1b` in the door, `hinge_door_1a` in the side (with a
suffix where two doors of one name share a partition).
"""
from __future__ import annotations

import string
from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal

from lib import concealed_hinges as data
from lib.stations import stations as spread

from ..core.directions import AXES, Axis, world_frame
from ..core.errors import LangError, one_of
from ..core.faces import Face
from ..core.layout_types import HardwareBodyLayout
from ..core.part import Board
from ..core.refs import Pos
from .common import TOLERANCE, Point2, along, check_hole, check_pilot_depth, middle, mm, numbering, uv, world_box

if TYPE_CHECKING:
    from ..core.scope import Scope

HingeModel = Literal["Blum CLIP top 110 Thin +0", "Blum CLIP top 110 Thin +3"]

#: Two ends of a box along one axis, mm.
Extent = tuple[float, float]
#: A box in a hinge's frame, mm: its extents across (from the carcass
#: board's face toward the door's middle), back (from the door's inner face
#: into the carcass) and along the hinged edge (from the hinge's centre).
HingeBox = tuple[Extent, Extent, Extent]


@dataclass(frozen=True)
class HingeShape:
    """A closed hinge as four boxes in its own frame (see `HingeBox`), the
    space it takes rather than its form. The boxes overlap where the pieces
    join, so each hinge is one body. Nothing but `_place` reads them."""
    #: The cup: the hinge's door part, on the door's inner face over the
    #: door holes (its bosses in the holes are left out).
    cup: HingeBox
    #: The arm's front part, from the cup back to the mounting plate.
    arm: HingeBox
    #: The arm's rear part with the clip, over the mounting plate.
    clip: HingeBox
    #: The mounting plate on the carcass board's face, around its screws.
    plate: HingeBox

    def boxes(self) -> dict[str, HingeBox]:
        return {"cup": self.cup, "arm": self.arm, "clip": self.clip, "plate": self.plate}

    @property
    def length(self) -> float:
        """How long the hinge is along the edge, centred on its centre: the
        mounting plate's 56.2 for the CLIP top. Two hinges closer than this
        meet."""
        return 2 * max(max(abs(a), abs(b)) for _, _, (a, b) in self.boxes().values())

    def raised(self, height: float) -> HingeShape:
        """The hinge on a plate `height` higher: the plate that much taller,
        the rest that much further from the carcass board."""
        def up(box: HingeBox) -> HingeBox:
            (a0, a1), back, along = box
            return (a0 + height, a1 + height), back, along
        (p0, p1), back, along = self.plate
        return HingeShape(up(self.cup), up(self.arm), up(self.clip), ((p0, p1 + height), back, along))


#: Measured 2026-10-12 on Häfele's CAD models (glTF, closed) of the hinge
#: 342.46.681 (Blum CLIP top 110 for thin doors) and the cruciform mounting
#: plates 342.20.800 (0 mm) and 342.20.830 (3 mm): the hinge's door bosses
#: sit 27 from the carcass face and 16 to either side of its centre, as the
#: drilling data has them; the plate's screws on its centre line, 38.5
#: behind the door. The 3 mm plate is the 0 mm one 3 mm taller, and the +3
#: model is the hinge on it. The arm starts 2 mm inside the cup and the clip
#: 2 mm inside the arm, where they join, so the boxes overlap.
_CLIP_TOP_THIN = HingeShape(
    cup=((0.0, 39.1), (0.0, 8.0), (-22.0, 22.0)),
    arm=((1.9, 48.1), (6.0, 40.0), (-15.3, 15.3)),
    clip=((3.2, 34.2), (38.0, 77.0), (-12.9, 12.9)),
    plate=((0.0, 8.5), (17.5, 59.0), (-28.1, 28.1)),   # 41.5 deep, 56.2 long, centred on its screws
)
#: Per model: the hinge on the plate as much higher as the model's door
#: row lies further from the carcass board (`lib.concealed_hinges`: 3 mm
#: for the +3).
HINGE_SHAPES: dict[str, HingeShape] = {
    model.name: _CLIP_TOP_THIN.raised(model.door_row - data.CLIP_TOP_THIN_0.door_row)
    for model in data.HINGE_MODELS.values()
}


@dataclass(frozen=True)
class _Meeting:
    """Where a door meets the carcass board it is hinged on, in world terms."""
    #: The door's inner face, toward the carcass board; its outward normal
    #: points into the carcass.
    door_face: Face
    #: The carcass board's face toward the door's middle, for the plates;
    #: its outward normal points toward the door's middle.
    carcass_face: Face
    #: The axis the hinged edge runs along.
    along: Axis
    #: The hinged edge's ends.
    ends: Extent
    #: +1 or -1: the order in which hinges and holes are numbered along it.
    order: int


@dataclass(frozen=True)
class _Hole:
    board: Board
    face: Face
    point: Point2
    name: str


class ConcealedHinge:
    """A concealed hinge model with the add-in's settings: `count` hinges
    per door, the outer ones' centres `end` from the ends of the door's
    hinged edge, `pilot` as (diameter, depth) of the carcass holes, mm."""

    def __init__(self, model: HingeModel = "Blum CLIP top 110 Thin +0", *, count: int = 2,
                 end: float = data.DEFAULT_END_MARGIN,
                 pilot: tuple[float, float] = (data.DEFAULT_PREDRILL_DIAMETER, data.DEFAULT_PREDRILL_DEPTH)):
        self.model = data.HINGE_MODELS[one_of(model, HingeModel, "hinge()")]
        if end < data.MIN_END_MARGIN:
            raise LangError(f"{self.name}: end= must be at least {mm(data.MIN_END_MARGIN)}, not {mm(end)}.")
        if count < 2:
            raise LangError(f"{self.name}: a door takes at least two hinges, not {count}.")
        for what, value in zip(("diameter", "depth"), pilot):
            if value < data.MIN_PREDRILL:
                raise LangError(f"{self.name}: the pilot {what} must be at least {mm(data.MIN_PREDRILL)}, "
                                f"not {mm(value)}.")
        self.count = count
        #: From each end of the door's hinged edge to the nearest hinge's centre.
        self.end = float(end)
        self.pilot = (float(pilot[0]), float(pilot[1]))

    @property
    def name(self) -> str:
        return self.model.name

    @property
    def door_row(self) -> float:
        """The door holes' row from the carcass board's face, mm."""
        return self.model.door_row

    @property
    def carcass_row(self) -> float:
        """The carcass holes' row behind the door's inner face, mm."""
        return data.CARCASS_ROW_INSET

    def stations(self, door: Board, carcass: Board | Face) -> list[Pos]:
        """The hinges' centres along the door's hinged edge, in the order
        they are numbered."""
        return self._stations(self._meeting(door, carcass), door)

    def mount(self, scope: Scope, /, *, door: Board, carcass: Board | Face) -> None:
        """`cab.mount(hinge, door=door, carcass=left)`: drills the door and
        the carcass board for the hinges and places them in `scope`.
        `carcass=` is the board, the plates going on its big face toward
        the door's middle, or that face itself (`wall.left`). Nothing is
        drilled unless every hole fits."""
        m = self._meeting(door, carcass)
        stations = self._stations(m, door)
        door_holes, carcass_holes = self._holes(m, stations)
        taken = [hole.name for hole in door_holes if door.has_operation(hole.name)]
        if taken:
            raise LangError(f"{self.name}: {door.path} is hinged on {m.carcass_face.part.path} already ({taken[0]}).",
                            door.path)
        diameter, depth = self.pilot
        check_pilot_depth(self.name, door, data.DOOR_CUP_DEPTH, "door hole")
        check_pilot_depth(self.name, m.carcass_face.part, depth, "pilot")
        for holes, d, what in ((door_holes, data.DOOR_CUP_DIAMETER, "door hole"),
                               (carcass_holes, diameter, "pilot hole")):
            for hole in holes:
                check_hole(self.name, hole.board, hole.face, hole.point, d, what)
        for hole in door_holes:
            door.add_hole(hole.face, hole.point, data.DOOR_CUP_DIAMETER, data.DOOR_CUP_DEPTH, name=hole.name)
        for hole in carcass_holes:       # doors of one name in different scopes may share a partition
            hole.board.add_hole(hole.face, hole.point, diameter, depth, name=hole.board.unique_op_name(hole.name))
        self._place(scope, door, m, stations)

    # -- geometry ------------------------------------------------------------------------------

    def _meeting(self, door: Board, carcass: Board | Face) -> _Meeting:
        board = carcass.part if isinstance(carcass, Face) else carcass
        if door is board:
            raise LangError(f"{self.name}: the door and the carcass board must be two different boards.", door.path)
        across, back = board.t_axis, door.t_axis
        if across == back:
            raise LangError(f"{self.name}: {door.path} and {board.path} lie in parallel planes; a door is hinged "
                            "on a carcass board standing square to it.", door.path)
        edge: Axis = next(a for a in AXES if a != across and a != back)
        db, cb = door.box(), board.box()
        door_middle = middle(db, across)
        if isinstance(carcass, Face):
            if not carcass.is_big:
                raise LangError(f"{self.name}: {carcass!r} is a narrow face; name the big face of the carcass "
                                "board the mounting plates go on.", door.path)
            if (door_middle - carcass.value) * carcass.direction.sign < -board.thickness - TOLERANCE:
                raise LangError(f"{self.name}: {door.path} lies behind {board.path}'s {carcass.name} face, on the "
                                "far side of the board; the mounting plates go on the face toward the door.",
                                door.path)
            carcass_face = carcass
        else:
            if cb.lo[across] - TOLERANCE <= door_middle <= cb.hi[across] + TOLERANCE:
                a, b = (board.face(board.scope.frame.direction_of(across, sign)).name for sign in (-1, 1))
                raise LangError(f"{self.name}: the middle of {door.path} lies within {board.path}'s thickness; "
                                f"name the face the mounting plates go on, carcass={board.name}.{a} or "
                                f"{board.name}.{b}.", door.path)
            carcass_face = board.face(board.scope.frame.direction_of(across, 1 if door_middle > cb.hi[across] else -1))
        toward_carcass = middle(cb, back) - middle(db, back)
        if abs(toward_carcass) < TOLERANCE:
            raise LangError(f"{self.name}: {door.path} is centred on {board.path}'s depth; a door stands in "
                            "front of the board it is hinged on.", door.path)
        sign = 1 if toward_carcass > 0 else -1
        door_face = door.face(door.scope.frame.direction_of(back, sign))
        return _Meeting(door_face, carcass_face, edge, (db.lo[edge], db.hi[edge]),
                        numbering(world_frame().direction_of(back, sign), edge))

    def _stations(self, m: _Meeting, door: Board) -> list[Pos]:
        """The add-in measures `end` along the door's edge (its sketch
        dimensions run from the door edge's ends), so the carcass board's
        extent does not matter."""
        lo, hi = m.ends
        length = hi - lo
        if length <= 2 * self.end + TOLERANCE:
            raise LangError(f"{self.name}: the door's hinged edge ({mm(length)}) is too short for hinges "
                            f"{mm(self.end)} from its ends.", door.path)
        values = [lo + s for s in spread(length, self.count, self.end)]
        # (the add-in's rule is the hole pairs', 42; their mounting plates meet up to 56.2 [found by
        # fuzzing, refused by Florian 2026-10-13])
        apart = max(2 * data.HINGE_HALF_EXTENT, HINGE_SHAPES[self.name].length)
        if values[1] - values[0] < apart - TOLERANCE:
            raise LangError(f"{self.name}: the door's hinged edge ({mm(length)}) is too short for {self.count} "
                            f"hinges at least {mm(apart)} apart, {mm(self.end)} from its ends: their mounting "
                            "plates would meet.", door.path)
        return [Pos(m.along, v) for v in (values if m.order > 0 else values[::-1])]

    def _holes(self, m: _Meeting, stations: list[Pos]) -> tuple[list[_Hole], list[_Hole]]:
        """The door holes and the carcass holes, numbered by hinge and
        lettered a, b in the order the hinges are numbered."""
        c, d = m.carcass_face, m.door_face
        door, carcass = d.part, c.part
        door_row = c.value + c.direction.sign * self.door_row          # across, toward the door's middle
        carcass_row = d.value + d.direction.sign * self.carcass_row    # back, into the carcass
        half = data.HOLE_PAIR_SPACING / 2
        door_holes: list[_Hole] = []
        carcass_holes: list[_Hole] = []
        for i, station in enumerate(stations, 1):
            for letter, offset in zip(string.ascii_lowercase, (-half * m.order, half * m.order)):
                at = station.value + offset
                door_holes.append(_Hole(door, d, uv(door, {c.axis: door_row, m.along: at}),
                                        f"hinge_{carcass.name}_{i}{letter}"))
                carcass_holes.append(_Hole(carcass, c, uv(carcass, {d.axis: carcass_row, m.along: at}),
                                           f"hinge_{door.name}_{i}{letter}"))
        return door_holes, carcass_holes

    def _place(self, scope: Scope, door: Board, m: _Meeting, stations: list[Pos]) -> None:
        """Records the hinges as `<door>_hinges`, a body per hinge
        (`hinge_1`, `hinge_2`, ... in the order they are numbered), each
        made of the model's `HINGE_SHAPES` boxes, measured from the carcass
        board's face, the door's inner face and the hinge's centre."""
        c, d = m.carcass_face, m.door_face
        bodies: list[HardwareBodyLayout] = []
        for i, station in enumerate(stations, 1):
            starts = ((c.direction, c.value), (d.direction, d.value), (along(m.along), station.value))
            boxes = [world_box(starts, box) for box in HINGE_SHAPES[self.name].boxes().values()]
            bodies.append(HardwareBodyLayout(name=f"hinge_{i}", boxes=boxes))
        scope.place_hardware(scope.unique_hardware_name(f"{door.name}_hinges"), bodies)


def hinge(model: HingeModel = "Blum CLIP top 110 Thin +0", *, count: int = 2,
          end: float = data.DEFAULT_END_MARGIN,
          pilot: tuple[float, float] = (data.DEFAULT_PREDRILL_DIAMETER, data.DEFAULT_PREDRILL_DEPTH)
          ) -> ConcealedHinge:
    """A concealed hinge, `hinge("Blum CLIP top 110 Thin +3", count=3)`:
    see `ConcealedHinge`, the type it returns."""
    return ConcealedHinge(model, count=count, end=end, pilot=pilot)
