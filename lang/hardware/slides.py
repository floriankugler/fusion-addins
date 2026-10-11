"""Concealed drawer slides (Blum Movento, Grass Dynapro) as hardware.

A slide dictates the drawer box: its sides' inner faces sit 21 mm from the
carcass sides (inner width LW - 42, both catalogs), its length is the
nominal length less 10 (SKL = NL - 10), its bottom panel's underside lies
28 mm above the slide's bottom (the bay's bottom), and its sides hang below
the panel by the recess. The carcass needs NL + 3 of depth behind the
runner's front. `drawer_box()` returns that box; `recess` the bottom
panel's height above the sides' lower edge. `machine_box()` cuts the
front and back boards out for the couplings and rear hooks and pre-drills
the back board for the hooks.

Mounted on a drawer scope, a slide pre-drills the carcass sides: a row 38
mm above the bay's bottom, at the hole positions of `lib.drawer_slides`
measured from the runner's front (the drawer face's back for inset
fronts, the carcass front edge for overlay fronts). The runner's own front
is 4 mm behind that.

Sources: Grass "Dynapro Planungshinweise" 113378 12/2021 (installation
dimensions and assembly steps; read 2026-10-11), Blum TD-132/1 DE/06.22
p.5; hole patterns from `lib.drawer_slides`; drawer-box machining as
Florian read it from the Grass sheet (2026-10-11).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, cast

from lib import drawer_slides as data

from ..core.box import Box
from ..core.errors import LangError
from ..core.layout_types import BoxDict, HardwareBodyLayout
from ..core.refs import Pos, PosLike, as_pos

if TYPE_CHECKING:
    from ..core.part import Board
    from ..core.scope import Scope

#: The drawer sides' inner faces from the carcass sides (LW - 42), mm.
INNER_FACE_OFFSET = 21.0
#: Thickest drawer side the runner takes, mm (both catalogs: max. 16).
MAX_SIDE_THICKNESS = 16.0
#: Drawer box length below the nominal length (SKL = NL - 10), mm.
BOX_SHORTER_THAN_NL = 10.0
#: The bottom panel's underside above the slide's bottom (the bay's
#: bottom), mm: 10 below the screw row at 38 (Grass; Blum assumed).
BOTTOM_HEIGHT = 28.0
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
    Hook holes are drilled into the back board's rear face, given as
    (from the side's inner face, above the bottom panel's underside)."""
    #: Width of the cut-out at each end of the front board, for the couplings.
    front_cutout: float
    #: Width of the cut-out at each end of the back board, for the rear hooks.
    back_cutout: float
    #: Pre-drill positions for each rear hook.
    hook_holes: tuple[tuple[float, float], ...]


#: Per model family (Grass per Florian's reading of the Dynapro sheet).
BOX_MACHINING: dict[str, BoxMachining] = {
    "Grass": BoxMachining(front_cutout=69.0, back_cutout=35.0,
                          hook_holes=((42.0, 15.0), (42.0, 15.0 + 32.0), (10.0, 15.0 + 32.0))),
}


def _family(model: data.SlideModel) -> str:
    return model.name.split()[0]


@dataclass(frozen=True)
class RunnerModel:
    """A STEP file of a runner pair from Häfele's CAD box, with the facts
    needed to place it: in the file, x = 0 is the left runner's mounting
    face, y = 0 its front (`front_offset` behind the carcass edge), z is
    up with the screw row at `row_z`; the right runner is the mirrored
    second body, `pair_distance` away."""
    file: str
    #: The same model as a mesh for the preview, or None for envelope boxes.
    mesh: str | None
    bodies: tuple[str, str]
    front_offset: float
    row_z: float
    pair_distance: float
    #: Each body's bounding box in the file's frame, mm.
    envelopes: tuple[Envelope, Envelope]


Envelope = tuple[tuple[float, float, float], tuple[float, float, float]]

#: Model files by (slide model name, nominal length). Measured in Fusion
#: after import (2026-10-11): holes at y = 6..257 (catalog 10..261, so
#: KV = y + 4), row at z = 35.9, bodies x 0..57.1 and 342.9..400.
RUNNER_MODELS: dict[tuple[str, int], RunnerModel] = {
    (data.DYNAPRO_40.name, 450): RunnerModel(
        file="catalog/hardware/grass_dynapro_40_nl450_433.19.608.stp",
        mesh="catalog/hardware/grass_dynapro_40_nl450_433.19.608.gltf",
        bodies=("Body1", "Body2"), front_offset=4.0, row_z=35.9, pair_distance=400.0,
        envelopes=(((0.0, -2.6, -1.0), (57.1, 447.5, 46.9)),
                   ((342.9, -2.6, -1.0), (400.0, 447.5, 46.9)))),
}


class DrawerSlide:
    """One slide model at a nominal length, with the pre-drill settings:
    `holes` per side from the odd or even set (see `lib.drawer_slides`),
    `predrill` as (diameter, depth) in mm."""

    def __init__(self, model: data.SlideModel, nl: int, holes: int = 4, odd: bool = True,
                 predrill: tuple[float, float] = (2.0, 4.0), bottom_recess: float | None = None,
                 hook_predrill: tuple[float, float] = (2.0, 8.0)):
        if nl not in model.nominal_lengths:
            raise LangError(f"{model.name} is not made in NL {nl}; lengths: {model.nominal_lengths}.")
        self.model = model
        self.nl = nl
        self.holes = holes
        self.odd = odd
        self.predrill = predrill
        #: (diameter, depth) of the rear hooks' pre-drill holes in the back board.
        self.hook_predrill = hook_predrill
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
    def side_lift(self) -> float:
        """The drawer sides' lower edge above the bay's bottom: the bottom
        panel's underside at 28 less the recess the sides hang below it."""
        return BOTTOM_HEIGHT - self.recess

    def drawer_box(self, bay: Box, front: PosLike, side_thickness: float, height: float) -> Box:
        """The drawer box's outer envelope in `bay`: the runner's front at
        `front`, the sides' inner faces 21 mm from the carcass sides, the
        box NL - 10 long and `height` high, its sides' lower edge
        `side_lift` above the bay's bottom so that the bottom panel's
        underside lies 28 above it."""
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
        a cut-out for the coupling, 69 wide from the side's inner face, and
        at each end of the back board one for the rear hook, 35 wide; both
        from the board's lower edge up to the floor's underside. Into the
        back board's rear face, three pre-drill holes per hook (`hook_predrill`
        diameter and depth): 42 from the side's inner face at 15 and 47
        above the floor's underside, and 10 from the inner face at 47."""
        try:
            data = BOX_MACHINING[_family(self.model)]
        except KeyError:
            raise LangError(f"{self.name}: no drawer-box machining data for {_family(self.model)}.") from None
        frame = floor.box().frame
        width_axis = frame.direction("left").axis
        floor_bottom = floor.bottom.position
        diameter, depth = self.hook_predrill
        for side in sides:
            inward = side.inner.direction            # from this side into the drawer
            if inward.axis != width_axis:
                raise LangError(f"{self.name}: {side.path} is not a side of the drawer box.", side.path)
            inner = side.inner.value
            which = (-inward).name                   # the side's own name in the frame: left or right
            for board, width, what in ((front, data.front_cutout, "coupling"), (back, data.back_cutout, "hook")):
                box = board.box()
                if box.frame.direction("back").axis == width_axis:
                    raise LangError(f"{self.name}: {board.path} is not the drawer's front or back.", board.path)
                region = (box.with_side(-inward, inner)
                             .with_side(inward, inner + inward.sign * width)
                             .with_side(frame.direction("top"), floor_bottom.value))
                board.cut(region, name=f"{what}_{which}")
            for across, up in data.hook_holes:
                at = Pos(width_axis, inner + inward.sign * across)
                back.hole(d=diameter, depth=depth, at=back.outer.bottom(floor_bottom + up).left(at))

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
        bay = scope._need_box("mount")  # type: ignore[reportPrivateUsage]
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

    def _place_runners(self, scope: Scope, sides: tuple[Board, Board], front_pos: Pos) -> None:
        """Records the runner pair's model, when there is a file for this
        slide and length: the left runner's mounting face on the left side's
        inner face, its front 4 mm behind the runner front, its screw row
        38 mm above the bay bottom; the right runner moved to the right side."""
        model = RUNNER_MODELS.get((self.model.name, self.nl))
        if model is None:
            return
        bay = scope._need_box("mount")  # type: ignore[reportPrivateUsage]
        frame = bay.frame
        left_dir, right_dir = frame.direction("left"), frame.direction("right")
        left_side = next((s for s in sides if s.inner.direction == right_dir), None)
        right_side = next((s for s in sides if s.inner.direction == left_dir), None)
        if left_side is None or right_side is None:
            raise LangError(f"{self.name}: sides must be one left and one right carcass side.")
        back, up = frame.direction("back"), frame.direction("top")
        inner_width = abs(right_side.inner.value - left_side.inner.value)
        origin = [0.0, 0.0, 0.0]
        origin[_index(left_dir.axis)] = left_side.inner.value
        origin[_index(back.axis)] = front_pos.value + back.sign * model.front_offset
        origin[_index(up.axis)] = bay.bottom.value + (data.HOLE_ROW_HEIGHT - model.row_z)
        def envelope(index: int) -> BoxDict:
            lo, hi = model.envelopes[index]
            return {"min": list(lo), "max": list(hi)}
        bodies = [
            HardwareBodyLayout(name=model.bodies[0], offset=[0.0, 0.0, 0.0], envelope=envelope(0)),
            HardwareBodyLayout(name=model.bodies[1], offset=[inner_width - model.pair_distance, 0.0, 0.0],
                               envelope=envelope(1)),
        ]
        scope.place_hardware("runners", model.file, (origin[0], origin[1], origin[2]),
                             {"x": right_dir, "y": back, "z": up}, bodies, mesh=model.mesh)


def _index(axis: str) -> int:
    return "xyz".index(axis)
