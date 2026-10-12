"""Concealed hinges (Blum CLIP top 110 for thin doors) as hardware.

`cab.mount(hinge, door=door, carcass=left)` hinges a door on a carcass
board standing square to it: a side for a door that opens sideways, a
partition between two doors, the top or bottom for a flap. It drills what
the concealed_hinge_native add-in drills from the two edges it is given:
the door's hinged edge, the edge of its inner face (the big face toward
the carcass board) next to that board, and the carcass board's edge, the
front edge of its face toward the door's middle, where the mounting
plates go.

- `count=` hinges (2; the add-in always makes two), the outer ones'
  centres `margin=` from the ends of the door's hinged edge (60), the rest
  evenly between.
- Per hinge two holes in the door's inner face, 10 mm wide and 5 deep and
  32 apart along the edge, in a row 27 mm (+0 model) or 30 mm (+3) from
  the carcass board's face toward the door's middle, whatever the door's
  overlay or gap.
- Per hinge two pre-drill holes for the mounting plate's screws in the
  carcass board's face, 32 apart, 38.5 mm behind the door's inner face,
  `predrill=` wide and deep (1/8 inch by 3).
- The hinges are placed as `<door>_hinges`, a body per hinge made of
  four boxes, cup, arm, clip and mounting plate (`HINGE_SHAPES`, measured
  from Häfele's CAD models). Hinges are numbered by their place
  along the edge, from the bottom, or for a flap from the door's own
  left, seen standing in front of it, so a cabinet and a module in the
  van's terms number them alike: bodies `hinge1`, `hinge2`, ...

Refused as the add-in refuses: an end margin under 27 mm (its dialog's
smallest), hinges 42 mm apart or closer (their hole pairs would meet), a
door and carcass board that are one board, and holes whose centres miss
their face. The add-in's edges are boards here, so the door and the
carcass board must stand square to each other: the hinged edge then runs
along the carcass board's face. The hinge dictates nothing about the
door's overlay or gap that the add-in knows (its plausibility check of
the overlay is switched off), so there is no door-sizing method.

Drilling dimensions from `lib/concealed_hinges.py`, the add-in's, which
it reads too. Operations are named by the other board and the hinge,
`hinge_left_1a` and `_1b` in the door, `hinge_door_1a` in the side (with a
suffix where two doors of one name share a partition).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal

from shapely.geometry import Point

from lib import concealed_hinges as data

from ..core import directions
from ..core.box import Box
from ..core.directions import AXES, Axis
from ..core.errors import LangError, one_of
from ..core.layout_types import BoxDict, HardwareBodyLayout
from ..core.part import Board, Face
from ..core.refs import Pos

if TYPE_CHECKING:
    from ..core.scope import Scope

HingeModel = Literal["Blum CLIP top 110 Thin +0", "Blum CLIP top 110 Thin +3"]
EPS = 1e-6

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
HINGE_SHAPES: dict[str, HingeShape] = {
    "Blum CLIP top 110 Thin +0": _CLIP_TOP_THIN,
    "Blum CLIP top 110 Thin +3": _CLIP_TOP_THIN.raised(3.0),
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


class ConcealedHinge:
    """A concealed hinge model with the add-in's settings: `margin` from each
    end of the door's hinged edge to the nearest hinge's centre, `count`
    hinges per door, `predrill` as (diameter, depth) of the carcass holes,
    mm."""

    def __init__(self, model: HingeModel = "Blum CLIP top 110 Thin +0", *, margin: float = data.DEFAULT_END_MARGIN,
                 count: int = 2,
                 predrill: tuple[float, float] = (data.DEFAULT_PREDRILL_DIAMETER, data.DEFAULT_PREDRILL_DEPTH)):
        self.model = data.HINGE_MODELS[one_of(model, HingeModel, "ConcealedHinge()")]
        if margin < data.MIN_END_MARGIN:
            raise LangError(f"{self.name}: the end margin must be at least {data.MIN_END_MARGIN:g} mm, "
                            f"not {margin:g}.")
        if count < 2:
            raise LangError(f"{self.name}: a door takes at least two hinges, not {count}.")
        for what, value in zip(("diameter", "depth"), predrill):
            if value < data.MIN_PREDRILL:
                raise LangError(f"{self.name}: the pre-drill {what} must be at least {data.MIN_PREDRILL:g} mm, "
                                f"not {value:g}.")
        self.margin = float(margin)
        self.count = count
        self.predrill = predrill

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

    def stations(self, door: Board, carcass: Board) -> list[Pos]:
        """The hinges' centres along the door's hinged edge, in the order
        they are numbered."""
        return self._stations(self._meeting(door, carcass), door)

    def mount(self, scope: Scope, /, **options: object) -> None:
        """`cab.mount(hinge, door=door, carcass=left)`: drills the door and
        the carcass board for the hinges and places them in `scope`."""
        unknown = set(options) - {"door", "carcass"}
        if unknown or "door" not in options or "carcass" not in options:
            raise LangError(f"{self.name}: mount() takes door= and carcass=, got {sorted(options)}.", scope.path)
        door, carcass = options["door"], options["carcass"]
        if not isinstance(door, Board) or not isinstance(carcass, Board):
            raise LangError(f"{self.name}: door= and carcass= take boards.", scope.path)
        self._hinge(scope, door, carcass)

    # -- geometry ------------------------------------------------------------------------------

    def _meeting(self, door: Board, carcass: Board) -> _Meeting:
        if door is carcass:
            raise LangError(f"{self.name}: the door and the carcass board must be two different boards.", door.path)
        across, back = carcass.t_axis, door.t_axis
        if across == back:
            raise LangError(f"{self.name}: {door.path} and {carcass.path} lie in parallel planes; a door is hinged "
                            "on a carcass board standing square to it.", door.path)
        along: Axis = next(a for a in AXES if a != across and a != back)
        db, cb = door.box(), carcass.box()
        toward_door = _sign(_middle(db, across) - _middle(cb, across))
        toward_carcass = _sign(_middle(cb, back) - _middle(db, back))
        if toward_door == 0:
            raise LangError(f"{self.name}: {door.path} is centred on {carcass.path}'s thickness, so neither of "
                            f"its faces is the one toward the door.", door.path)
        if toward_carcass == 0:
            raise LangError(f"{self.name}: {door.path} is centred on {carcass.path}'s depth; a door stands in "
                            "front of the board it is hinged on.", door.path)
        door_face = door.face(door.scope.frame.direction_of(back, toward_carcass))
        carcass_face = carcass.face(carcass.scope.frame.direction_of(across, toward_door))
        return _Meeting(door_face, carcass_face, along, (db.lo[along], db.hi[along]),
                        _order(along, back, toward_carcass))

    def _stations(self, m: _Meeting, door: Board) -> list[Pos]:
        """The add-in measures the margin along the door's edge (its sketch
        dimensions run from the door edge's ends), so the carcass board's
        extent does not matter."""
        lo, hi = m.ends
        length = hi - lo
        if length <= 2 * self.margin + EPS:
            raise LangError(f"{self.name}: the door's hinged edge ({length:g} mm) is too short for an end margin "
                            f"of {self.margin:g}.", door.path)
        pitch = (length - 2 * self.margin) / (self.count - 1)
        if pitch <= 2 * data.HINGE_HALF_EXTENT + EPS:
            raise LangError(f"{self.name}: the door's hinged edge ({length:g} mm) is too short for {self.count} "
                            f"hinges more than {2 * data.HINGE_HALF_EXTENT:g} mm apart at an end margin of "
                            f"{self.margin:g}.", door.path)
        values = [lo + self.margin + i * pitch for i in range(self.count)]
        return [Pos(m.along, v) for v in (values if m.order > 0 else values[::-1])]

    # -- mounting ------------------------------------------------------------------------------

    def _hinge(self, scope: Scope, door: Board, carcass: Board) -> None:
        """Works out every hole and checks them all before it drills one,
        so a refused mount changes nothing."""
        m = self._meeting(door, carcass)
        stations = self._stations(m, door)
        c, d = m.carcass_face, m.door_face
        door_row = c.value + c.direction.sign * self.door_row          # across, toward the door's middle
        carcass_row = d.value + d.direction.sign * self.carcass_row    # back, into the carcass
        half = data.HOLE_PAIR_SPACING / 2
        door_holes: list[tuple[str, tuple[float, float]]] = []
        carcass_holes: list[tuple[str, tuple[float, float]]] = []
        for i, station in enumerate(stations, 1):
            for letter, offset in (("a", -half * m.order), ("b", half * m.order)):
                along = station.value + offset
                in_door = {c.axis: door_row, m.along: along}
                in_carcass = {d.axis: carcass_row, m.along: along}
                door_holes.append((f"hinge_{carcass.name}_{i}{letter}", (in_door[door.u_axis], in_door[door.v_axis])))
                carcass_holes.append((f"hinge_{door.name}_{i}{letter}",
                                      (in_carcass[carcass.u_axis], in_carcass[carcass.v_axis])))
        for board, face, holes, what in ((door, d, door_holes, "door"), (carcass, c, carcass_holes, "carcass")):
            outline = board.outline.geometry
            if any(outline.distance(Point(point)) > EPS for _, point in holes):
                raise LangError(f"{self.name}: the {what} holes do not fit on {board.path}'s {face.name} face.",
                                board.path)
        taken = [hole for hole, _ in door_holes if door.has_operation(hole)]
        if taken:
            raise LangError(f"{self.name}: {door.path} is hinged on {carcass.path} already ({taken[0]}).", door.path)
        diameter, depth = self.predrill
        for hole, point in door_holes:
            door.add_hole(d, point, data.DOOR_CUP_DIAMETER, data.DOOR_CUP_DEPTH, name=hole)
        for hole, point in carcass_holes:       # doors of one name in different scopes may share a partition
            carcass.add_hole(c, point, diameter, depth, name=carcass.unique_op_name(hole))
        self._place(scope, door, m, stations)

    def _place(self, scope: Scope, door: Board, m: _Meeting, stations: list[Pos]) -> None:
        """Records the hinges as `<door>_hinges`, a body per hinge
        (`hinge1`, `hinge2`, ... in the order they are numbered), each made
        of the model's `HINGE_SHAPES` boxes, measured from the carcass
        board's face, the door's inner face and the hinge's centre."""
        name, n = f"{door.name}_hinges", 2
        while any(item["name"] == name for item in scope.hardware):     # doors of one name in child scopes
            name, n = f"{door.name}_hinges_{n}", n + 1
        c, d = m.carcass_face, m.door_face
        bodies: list[HardwareBodyLayout] = []
        for i, station in enumerate(stations, 1):
            starts: tuple[tuple[Axis, int, float], ...] = (
                (c.axis, c.direction.sign, c.value), (d.axis, d.direction.sign, d.value), (m.along, 1, station.value))
            boxes = [_world_box(starts, box) for box in HINGE_SHAPES[self.name].boxes().values()]
            bodies.append(HardwareBodyLayout(name=f"hinge{i}", boxes=boxes))
        scope.place_hardware(name, bodies)


def _middle(box: Box, axis: Axis) -> float:
    return (box.lo[axis] + box.hi[axis]) / 2


def _sign(value: float) -> int:
    return 0 if abs(value) < EPS else (1 if value > 0 else -1)


def _order(along: Axis, back: Axis, toward_carcass: int) -> int:
    """Which way hinges are numbered along the edge: from the bottom; along
    a level edge from the door's own left, seen standing in front of it
    (its right is back x up, as for a drawer's runners); for a lid, whose
    front faces up, toward the world's positive axis."""
    up = directions.frame.direction("top")
    if along == up.axis:
        return up.sign
    if back == up.axis:
        return 1
    b = [0, 0, 0]
    b[AXES.index(back)] = toward_carcass
    u = up.vector
    right = (b[1] * u[2] - b[2] * u[1], b[2] * u[0] - b[0] * u[2], b[0] * u[1] - b[1] * u[0])
    return right[AXES.index(along)]


def _world_box(starts: tuple[tuple[Axis, int, float], ...], box: HingeBox) -> BoxDict:
    """A hinge box in world coordinates: each of its extents measured along
    an axis, in a direction, from a world position."""
    lo, hi = [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]
    for (axis, sign, start), (a, b) in zip(starts, box):
        i = AXES.index(axis)
        lo[i], hi[i] = sorted((start + sign * a, start + sign * b))
    return {"min": lo, "max": hi}
