"""Concealed drawer slides (Blum Movento, Grass Dynapro) as hardware.

A slide dictates the drawer box: its sides' inner faces sit 21 mm from the
carcass sides (inner width LW - 42, both catalogs), its length is the
nominal length less 10 (SKL = NL - 10), its bottom panel's underside lies
28.5 mm (Blum) or 28 mm (Grass) above the slide's bottom (the bay's
bottom), and its sides hang below the panel by the recess. The carcass
needs NL + 3 of depth behind the runner's front. `drawer_box()` returns
that box; `recess` the bottom panel's height above the sides' lower edge.
`machine_box()` cuts the front and back boards out for the couplings and
rear hooks and drills the back board for the hooks: into its rear face,
or through it from its inner face when the hook hole's depth is
`through`, so the back needs no machining from its rear face.

Mounted on a drawer scope, a slide pre-drills the carcass sides: a row 38
mm above the bay's bottom, at the hole positions of `lib.drawer_slides`
measured from the runner's front (the drawer face's back for inset
fronts, the carcass front edge for overlay fronts). The runners' own
fronts are 4 mm (Grass) or 2 mm (Blum) behind that. It also places the
runner pair as boxes (`RunnerShape`), one body per runner.

Sources: Grass "Dynapro Planungshinweise" 113378 12/2021 (installation
dimensions and assembly steps; read 2026-10-11), Blum TD-132/1 DE/06.22
p.5 and the Blum catalogue 2024/2025 p.413 (Movento planning and drawer
assembly); hole patterns from `lib.drawer_slides`; drawer-box machining
as Florian read it from the Grass and Blum sheets (2026-10-11/12); runner
shapes measured from Häfele's CAD models (2026-10-12).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, cast

from shapely.geometry import Point, Polygon
from shapely.geometry import box as shapely_box
from shapely.geometry.base import BaseGeometry
from shapely.ops import unary_union

from lib import drawer_slides as data

from ..core import directions
from ..core.box import Box
from ..core.directions import Axis, Direction, Frame
from ..core.errors import LangError
from ..core.layout_types import BoxDict, HardwareBodyLayout
from ..core.ops import Pocket
from ..core.refs import Pos, PosLike, Through, as_pos
from ..core.geometry import parts_of

if TYPE_CHECKING:
    from ..core.part import Board, Face
    from ..core.scope import Scope

#: Far enough to stand for "beyond the board", mm.
_FAR = 1e9
#: The drawer sides' inner faces from the carcass sides (LW - 42), mm.
INNER_FACE_OFFSET = 21.0
#: Thickest drawer side the runner takes, mm (both catalogs: max. 16).
MAX_SIDE_THICKNESS = 16.0
#: Drawer box length below the nominal length (SKL = NL - 10), mm.
BOX_SHORTER_THAN_NL = 10.0
#: The bottom panel's underside above the slide's bottom (the bay's
#: bottom), where the drawer member's top carries it, per model family,
#: mm: Blum "min. 28.5" with the screw row at 38; Grass 10 below the screw
#: row. (Häfele's Dynapro models put the member's top at 28.5 as well.)
BOTTOM_HEIGHT: dict[str, float] = {"Blum": 28.5, "Grass": 28.0}
#: Allowed height of the bottom panel's underside above the sides' lower
#: edge, per model family, mm.
BOTTOM_RECESS: dict[str, tuple[float, float]] = {
    "Blum": (12.0, 15.0),
    "Grass": (10.0, 13.0),
}


@dataclass(frozen=True)
class BoxMachining:
    """What the drawer box needs cut and drilled for a slide family, mm.
    The cut-outs run from the board's lower edge up to the bottom panel's
    underside; widths are measured from the drawer sides' inner faces.
    Hook holes are drilled into the back board's rear face (or through it
    from its inner face), given as (from the side's inner face, above the
    bottom panel's underside)."""
    #: Width of the cut-out at each end of the front board, for the couplings.
    front_cutout: float
    #: Width of the cut-out at each end of the back board, for the rear hooks.
    back_cutout: float
    #: Hole positions for each rear hook.
    hook_holes: tuple[tuple[float, float], ...]
    #: (diameter, depth) of the hook holes unless the slide says otherwise.
    hook_hole: tuple[float, float]


#: Per model family. Grass: pre-drill holes for the screws of the rear
#: hook. Blum: one hole for the rear hook's pin; with TIP-ON BLUMOTION
#: (not modelled) the back board's cut-out is 125 wide.
BOX_MACHINING: dict[str, BoxMachining] = {
    "Blum": BoxMachining(front_cutout=75.0, back_cutout=75.0, hook_holes=((7.0, 11.0),), hook_hole=(6.0, 10.0)),
    "Grass": BoxMachining(front_cutout=69.0, back_cutout=35.0,
                          hook_holes=((42.0, 15.0), (42.0, 15.0 + 32.0), (10.0, 15.0 + 32.0)),
                          hook_hole=(2.0, 8.0)),
}


#: The rear hooks' holes as a slide takes them: (diameter, depth) in mm,
#: the depth a number (into the back board's rear face) or `through` (from
#: its inner face).
HookHole = tuple[float, float | Through]


def _family(model: data.SlideModel) -> str:
    return model.name.split()[0]


#: Two ends of a box along one axis, mm.
Extent = tuple[float, float]
#: A box in a runner's frame: its x, y and z extents. x runs from the
#: carcass side's inner face toward the drawer, y back from the runner
#: front of the hole positions, z up from the bay's bottom.
RunnerBox = tuple[Extent, Extent, Extent]


@dataclass(frozen=True)
class RunnerShape:
    """A closed runner of a slide family as five boxes: the cabinet rail
    (a flange against the carcass side and a base with the carriage), the
    drawer member, whose top carries the bottom panel, the coupling under
    the panel's front end and the rear hook behind the drawer box. Each
    family keeps one cross-section across all its lengths and load
    classes; the lengths follow from NL. The real cabinet rail ends 2/3 to
    9/10 of the way back, depending on model and length; here it runs the
    whole length. The coupling takes the width of the front board's
    cut-out, the space reserved for it."""
    #: The cabinet rail's front behind the runner front, mm.
    front: float
    #: The runner's rear end beyond NL, mm.
    rear: float
    #: The runner's lowest point above the bay's bottom, mm.
    bottom: float
    #: The flange: thickness and top.
    flange: Extent
    #: The base with the carriage on it: width and top.
    base: Extent
    #: How far the drawer member, beside the base, reaches from the side.
    member: float
    #: The coupling: length behind the drawer box's front, height below the bottom panel.
    coupling: Extent
    #: The rear hook above the bottom panel's underside: from and to across, and its top.
    hook: tuple[float, float, float]

    def boxes(self, nl: float, floor: float, box_length: float, coupling_width: float) -> dict[str, RunnerBox]:
        """The boxes at nominal length `nl`, the bottom panel's underside
        at `floor`, the drawer box `box_length` long (from the runner front)."""
        end = nl + self.rear
        x0, x1, top = self.hook
        return {
            "flange": ((0.0, self.flange[0]), (self.front, end), (self.bottom, self.flange[1])),
            "base": ((0.0, self.base[0]), (self.front, end), (self.bottom, self.base[1])),
            "member": ((self.base[0], self.member), (self.front, end), (self.bottom, floor)),
            "coupling": ((INNER_FACE_OFFSET, INNER_FACE_OFFSET + coupling_width), (0.0, self.coupling[0]),
                         (floor - self.coupling[1], floor)),
            "hook": ((x0, x1), (box_length, end), (floor, top)),
        }


#: Per model family, measured from Häfele's models (2026-10-12): Dynapro
#: 40 kg NL 300, 450 and 600 and 70 kg NL 500 (433.19.602/608/613,
#: 433.20.630), Movento 760H NL 250, 450 and 600, 766H NL 450 and the
#: Movento coupling (433.24.010/018/024/218, 433.24.980). The Dynapro
#: models include the coupling. Rounded to 0.1 mm.
RUNNER_SHAPES: dict[str, RunnerShape] = {
    "Blum": RunnerShape(front=2.0, rear=2.5, bottom=0.0, flange=(2.9, 48.9), base=(23.1, 4.9), member=62.3,
                        coupling=(88.6, 13.3), hook=(16.6, 47.5, 51.1)),
    "Grass": RunnerShape(front=4.0, rear=1.5, bottom=1.1, flange=(2.5, 49.0), base=(22.9, 12.9), member=53.9,
                         coupling=(61.5, 23.6), hook=(24.5, 39.5, 34.9)),
}


class DrawerSlide:
    """One slide model at a nominal length, with the pre-drill settings:
    `holes` per side from the odd or even set (see `lib.drawer_slides`),
    `predrill` as (diameter, depth) in mm; `hook_hole` the rear hooks'
    holes in the back board, (diameter, depth) or (diameter, `through`)."""

    def __init__(self, model: data.SlideModel, nl: int, holes: int = 4, odd: bool = True,
                 predrill: tuple[float, float] = (2.0, 4.0), bottom_recess: float | None = None,
                 hook_hole: HookHole | None = None):
        if nl not in model.nominal_lengths:
            raise LangError(f"{model.name} is not made in NL {nl}; lengths: {model.nominal_lengths}.")
        self.model = model
        self.nl = nl
        self.holes = holes
        self.odd = odd
        self.predrill = predrill
        if hook_hole is not None:
            diameter, depth = hook_hole
            if diameter <= 0 or (not isinstance(depth, Through) and depth <= 0):
                raise LangError(f"{self.name}: hook_hole= needs a diameter and a depth greater than zero, or "
                                f"through, not {hook_hole!r}.")
        #: (diameter, depth) of the rear hooks' holes in the back board, or
        #: None for the family's: Grass pre-drills 2 x 8 for the hook's
        #: screws, Blum drills 6 x 10 for its pin. A depth of `through`
        #: drills them through from the back board's inner face.
        self.hook_hole: HookHole | None = hook_hole
        lo, hi = BOTTOM_RECESS[_family(model)]
        if bottom_recess is None:
            bottom_recess = (lo + hi) / 2
        elif not lo <= bottom_recess <= hi:
            raise LangError(f"{model.name}: the bottom recess must be {lo:g} to {hi:g} mm, not {bottom_recess:g}.")
        #: The bottom panel's underside above the drawer sides' lower edge.
        self.recess: float = bottom_recess

    @property
    def name(self) -> str:
        return f"{self.model.name} NL {self.nl}"

    @property
    def box_length(self) -> float:
        return self.nl - BOX_SHORTER_THAN_NL

    @property
    def depth_needed(self) -> float:
        """Carcass depth behind the runner's front (MET = NL + 3)."""
        return self.nl + data.DEPTH_ALLOWANCE

    @property
    def bottom_height(self) -> float:
        """The bottom panel's underside above the bay's bottom."""
        return BOTTOM_HEIGHT[_family(self.model)]

    @property
    def side_lift(self) -> float:
        """The drawer sides' lower edge above the bay's bottom: the bottom
        panel's underside (`bottom_height`) less the recess the sides hang
        below it."""
        return self.bottom_height - self.recess

    def drawer_box(self, bay: Box, front: PosLike, side_thickness: float, height: float) -> Box:
        """The drawer box's outer envelope in `bay`: the runner's front at
        `front`, the sides' inner faces 21 mm from the carcass sides, the
        box NL - 10 long and `height` high, its sides' lower edge
        `side_lift` above the bay's bottom so that the bottom panel's
        underside lies `bottom_height` above it."""
        if side_thickness > MAX_SIDE_THICKNESS:
            raise LangError(f"{self.name}: drawer sides may be at most {MAX_SIDE_THICKNESS:g} mm thick.")
        clearance = INNER_FACE_OFFSET - side_thickness
        front_pos = as_pos(front, "drawer_box(front=)")
        back = bay.frame.direction("back")
        if front_pos.axis != back.axis:
            raise LangError(f"{self.name}: the front position {front_pos} is not on the bay's depth axis.")
        available = (bay.back.value - front_pos.value) * back.sign
        if available < self.depth_needed:
            raise LangError(f"{self.name}: needs {self.depth_needed:g} mm behind the runner's front, "
                            f"the bay has {available:g}.")
        box = bay.shrunk(left=clearance, right=clearance)
        box = box.with_sides(front=front_pos, back=Pos(back.axis, front_pos.value + back.sign * self.box_length))
        bottom = bay.bottom.into(self.side_lift)
        return box.with_sides(bottom=bottom, top=bay.bottom.into(self.side_lift + height))

    def machine_box(self, sides: tuple[Board, Board], front: Board, back: Board, floor: Board) -> None:
        """`slide.machine_box(sides=(l, r), front=f, back=k, floor=floor)`:
        the drawer box's cut-outs and holes. At each end of the front board
        a cut-out for the coupling and at each end of the back board one
        for the rear hook, from the side's inner face (Grass 69 and 35
        wide, Blum 75 and 75) and from the board's lower edge up to the
        floor's underside. Into the back board's rear face the holes for
        each hook (`hook_hole` diameter and depth): Grass three pre-drill
        holes, 42 from the side's inner face at 15 and 47 above the floor's
        underside and 10 from the inner face at 47; Blum one hole, 7 from
        the inner face at 11. With a depth of `through` they go through
        the back board from its inner face, where a box joint's reliefs
        are too, so the back needs no machining from its rear face.

        A hook hole that would run into the floor, where it goes into the
        back board, or into the groove it sits in there, is an error, and
        nothing is cut: with Blum (11 above the floor's underside) a floor
        of 8 mm or more cannot go into the back, so its groove join names
        the sides and the front only."""
        try:
            data = BOX_MACHINING[_family(self.model)]
        except KeyError:
            raise LangError(f"{self.name}: no drawer-box machining data for {_family(self.model)}.") from None
        frame = floor.box().frame
        width_axis = frame.direction("left").axis
        floor_bottom = floor.bottom.position
        diameter, depth = self.hook_hole or data.hook_hole
        # through holes from the inner face, fixed-depth ones from the rear
        hook_face = back.inner if isinstance(depth, Through) else back.outer
        for side in sides:
            if side.inner.direction.axis != width_axis:
                raise LangError(f"{self.name}: {side.path} is not a side of the drawer box.", side.path)
        for board in (front, back):
            if board.box().frame.direction("back").axis == width_axis:
                raise LangError(f"{self.name}: {board.path} is not the drawer's front or back.", board.path)
        holes = [(side, Pos(width_axis, side.inner.value + side.inner.direction.sign * across), up)
                 for side in sides for across, up in data.hook_holes]
        for side, at, up in holes:
            self._check_hook_hole(back, floor, hook_face, at, floor_bottom + up, diameter, depth, side)
        for side in sides:
            inward = side.inner.direction            # from this side into the drawer
            inner = side.inner.value
            which = (-inward).name                   # the side's own name in the frame: left or right
            for board, width, what in ((front, data.front_cutout, "coupling"), (back, data.back_cutout, "hook")):
                box = board.box()
                region = (box.with_side(-inward, inner)
                             .with_side(inward, inner + inward.sign * width)
                             .with_side(frame.direction("top"), floor_bottom.value))
                board.cut(region, name=f"{what}_{which}")
            for hole_side, at, up in holes:
                if hole_side is side:
                    back.hole(d=diameter, depth=depth, at=hook_face.bottom(floor_bottom + up).left(at))

    def _check_hook_hole(self, back: Board, floor: Board, face: Face, at: Pos, height: Pos, diameter: float,
                         depth: float | Through, side: Board) -> None:
        """An error when the hook hole at `at` and `height` on the back
        board's face `face` would run into the floor where it goes into the
        back board, or into a pocket of the back board the floor lies in
        there (its groove, with the groove's clearance)."""
        t, ft = back.t_axis, floor.t_axis
        if ft not in (back.u_axis, back.v_axis) or t not in (floor.u_axis, floor.v_axis):
            return                                   # not a floor across the back board
        bb = back.box()
        floor_t = _span(floor, t, (bb.lo[t], bb.hi[t]))
        if floor_t is None:
            return                                   # the floor does not go into the back board
        reach = back.thickness if isinstance(depth, Through) else depth
        hole_t = _sorted(face.value, face.value - face.direction.sign * reach)
        coords = {at.axis: at.value, height.axis: height.value}
        hole = Point(coords[back.u_axis], coords[back.v_axis]).buffer(diameter / 2, quad_segs=16)
        what: str | None = None
        if hole.intersection(_section(floor, back, hole_t)).area > 1e-6:
            what = floor.path
        else:
            held = _section(floor, back, floor_t)
            for op in back.ops:
                if not isinstance(op, Pocket) or op.shape.geometry.intersection(held).area <= 1e-6:
                    continue
                pocket_face = back.face(directions.frame.direction(op.face))
                pocket_t = _sorted(pocket_face.value, pocket_face.value - pocket_face.direction.sign * op.depth)
                if not (_overlap(pocket_t, floor_t) and _overlap(pocket_t, hole_t)):
                    continue
                if hole.intersection(op.shape.geometry).area > 1e-6:
                    what = f"{op.name or 'the pocket'}, where {floor.path} goes into it"
                    break
        if what is not None:
            raise LangError(
                f"{self.name}: the rear hook's {diameter:g} mm hole {abs(at.value - side.inner.value):g} from "
                f"{side.path}'s inner face and {height.value - floor.bottom.value:g} above the floor's underside "
                f"would run into {what}: leave the back board out of the floor's groove join (name the sides and "
                "the front only, as with Blum), or make the floor thinner.", back.path)

    def hole_positions(self) -> list[float]:
        """Pre-drill positions behind the runner's front, mm."""
        candidates = data.candidate_holes(self.model, self.nl, self.odd)
        return data.choose_holes(candidates, self.holes)

    def mount(self, scope: Scope, /, **options: object) -> None:
        """`drawer.mount(slide, sides=(left, right), front=face.back)`:
        pre-drills the carcass sides for this drawer, a row 38 mm above
        the drawer's bay bottom, from the runner's front at `front`."""
        unknown = set(options) - {"sides", "front"}
        if unknown or "sides" not in options or "front" not in options:
            raise LangError(f"{self.name}: mount() takes sides=(left, right) and front=, got {sorted(options)}.")
        sides = cast(tuple["Board", "Board"], options["sides"])
        self.predrill_sides(scope, sides, cast(PosLike, options["front"]))

    def predrill_sides(self, scope: Scope, sides: tuple[Board, Board], front: PosLike) -> None:
        bay = scope.require_box("mount")
        front_pos = as_pos(front, "mount(front=)")
        back = bay.frame.direction("back")
        if front_pos.axis != back.axis:
            raise LangError(f"{self.name}: the front position {front_pos} is not on the bay's depth axis.")
        row = bay.bottom.into(data.HOLE_ROW_HEIGHT)
        diameter, depth = self.predrill
        for side in sides:
            face = side.inner
            if face.axis != bay.frame.direction("left").axis:
                raise LangError(f"{self.name}: {side.path} is not a side of the drawer's bay.", side.path)
            for position in self.hole_positions():
                along = Pos(back.axis, front_pos.value + back.sign * position)
                side.hole(d=diameter, depth=depth, at=face.bottom(row).front(along))
        self._place_runners(scope, sides, front_pos)

    def runner_boxes(self) -> dict[str, RunnerBox]:
        """One runner's boxes in its own frame (see `RunnerBox`)."""
        family = _family(self.model)
        return RUNNER_SHAPES[family].boxes(self.nl, self.bottom_height, self.box_length,
                                           BOX_MACHINING[family].front_cutout)

    def _place_runners(self, scope: Scope, sides: tuple[Board, Board], front_pos: Pos) -> None:
        """Records the runner pair, a body per runner named by the
        drawer's own left and right, seen standing in front of it: each
        runner's boxes from its side's inner face, the runner front at
        `front_pos` and the bay's bottom. A module written without front=
        (in the van's terms) or mirrored calls the drawer's right its
        left, so the drawer's right is worked out from its back and up."""
        bay = scope.require_box("mount")
        frame = bay.frame
        back, up = frame.direction("back"), frame.direction("top")
        right = _cross(frame, back, up)
        bodies: list[HardwareBodyLayout] = []
        for which, inward in (("left", right), ("right", -right)):
            side = next((s for s in sides if s.inner.direction == inward), None)
            if side is None:
                raise LangError(f"{self.name}: sides must be one left and one right carcass side.")
            starts = ((inward, side.inner.value), (back, front_pos.value), (up, bay.bottom.value))
            boxes = [_world_box(starts, box) for box in self.runner_boxes().values()]
            bodies.append(HardwareBodyLayout(name=which, boxes=boxes))
        scope.place_hardware("runners", bodies)


def _sorted(a: float, b: float) -> tuple[float, float]:
    return (a, b) if a <= b else (b, a)


def _overlap(a: tuple[float, float], b: tuple[float, float]) -> bool:
    return min(a[1], b[1]) - max(a[0], b[0]) > 1e-6


def _span(floor: Board, axis: Axis, within: tuple[float, float]) -> tuple[float, float] | None:
    """The stretch along `axis` (one of the floor's in-plane axes) that the
    floor's outline covers within `within`, or None."""
    i = 0 if floor.u_axis == axis else 1
    b = floor.outline.bounds
    lo, hi = max(b[i], within[0]), min(b[i + 2], within[1])
    return (lo, hi) if hi - lo > 1e-6 else None


def _section(floor: Board, back: Board, band: tuple[float, float]) -> BaseGeometry:
    """The floor's material within `band` along the back board's thickness,
    seen on the back board's face, in its outline frame: where along the
    back the floor's outline reaches into the band, through the floor's
    thickness."""
    t, ft = back.t_axis, floor.t_axis
    u, v = floor.u_axis, floor.v_axis
    along: Axis = u if v == t else v
    lo: dict[Axis, float] = {u: -_FAR, v: -_FAR}
    hi: dict[Axis, float] = {u: _FAR, v: _FAR}
    lo[t], hi[t] = band
    inside = floor.outline.geometry.intersection(shapely_box(lo[u], lo[v], hi[u], hi[v]))
    i = 0 if along == u else 1
    fb = floor.box()
    pieces: list[BaseGeometry] = []
    for g in parts_of(inside):
        if g.area <= 1e-9:
            continue
        corners: dict[Axis, tuple[float, float]] = {along: (float(g.bounds[i]), float(g.bounds[i + 2])),
                                                    ft: (fb.lo[ft], fb.hi[ft])}
        bu, bv = corners[back.u_axis], corners[back.v_axis]
        pieces.append(shapely_box(bu[0], bv[0], bu[1], bv[1]))
    return unary_union(pieces) if pieces else Polygon()


def _world_box(starts: tuple[tuple[Direction, float], ...], box: RunnerBox) -> BoxDict:
    """A runner box in world coordinates: each of its extents measured
    along a direction from a world position."""
    lo, hi = [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]
    for (direction, start), (a, b) in zip(starts, box):
        ends = sorted((start + direction.sign * a, start + direction.sign * b))
        i = "xyz".index(direction.axis)
        lo[i], hi[i] = ends
    return {"min": lo, "max": hi}


def _cross(frame: Frame, a: Direction, b: Direction) -> Direction:
    """The direction of a x b, for two perpendicular directions."""
    (ax, ay, az), (bx, by, bz) = a.vector, b.vector
    v = (ay * bz - az * by, az * bx - ax * bz, ax * by - ay * bx)
    i = next(k for k in range(3) if v[k])
    return frame.direction_of(("x", "y", "z")[i], v[i])
