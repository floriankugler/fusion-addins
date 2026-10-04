"""Festool DOMINO slots for the native joinery add-ins.

connectors_native offers Dominos as a connector type, tenons_native as a
tenon type. Both cut the slots into the face of the board the selected
edge's board butts against, and can engrave V-grooves next to the selected
edge that mark where the Domino machine cuts the matching mortises into the
selected board. Everything Domino about that lives here: the published
Domino sizes and machine stops, the dialog inputs (DominoInputs) and the
sketches and cuts (DominoBuilder).
"""
from dataclasses import dataclass
from enum import Enum, unique
from typing import Callable

import adsk.core
import adsk.fusion

from . import edge_sketch, inputs, utils


@unique
class EndStop(Enum):
    """Distance from the board end to the center of the first and last
    Domino. The value is the distance in mm set by the Domino machine's own
    stops: 37 mm for the built-in stop latches (stop pins on older machines),
    20 mm with the additional stop ZA-DF 500/700 fitted. CUSTOM uses an End
    Offset input of the add-in instead."""

    STOP_LATCH = 37
    ADDITIONAL_STOP = 20
    CUSTOM = 0


@unique
class DepthMode(Enum):
    HALF_LENGTH = 1
    MATERIAL_REMAINING = 2


@unique
class LooseSlots(Enum):
    """Extra length of every slot but one per board, in mm. The two fixed
    steps match the wider mortise settings of the Domino DF 500, which cuts
    13, 19 or 23 mm plus the cutter diameter."""

    NONE = 0
    PLUS_6 = 6
    PLUS_10 = 10
    CUSTOM = 1


@unique
class Marks(Enum):
    NONE = 0
    ALL = 1
    SKIP_FIRST_AND_LAST = 2


@dataclass(frozen=True)
class FenceStop:
    """A height stop of the Domino machine's fence. Stops are labelled with
    the board thickness they center the mortise on, so the mortise ends up
    half that far from the face the fence rests on."""

    value: int
    thickness: float
    label: str

    @property
    def name(self) -> str:
        return f"{self.thickness:g} mm ({self.label})"


FENCE_CENTERED = 0
FENCE_CUSTOM = 1
FENCE_STOPS = [
    FenceStop(1000 + thickness, thickness, "Festool")
    for thickness in (16, 20, 22, 25, 28, 36, 40)
] + [
    # Aftermarket (e.g. 3D-printed) stop gauges add further thicknesses.
    FenceStop(2000 + thickness, thickness, "Alternative")
    for thickness in (9, 11, 12, 13, 16, 18)
]


@dataclass(frozen=True)
class Size:
    """Festool DOMINO tenon dimensions in mm, as published in Festool's
    technical data ("thickness x length x width")."""

    value: int
    thickness: float
    width: float
    length: float

    @property
    def name(self) -> str:
        return f"{self.thickness:g} x {self.length:g}"


SIZES = [
    Size(420, 4, 16.6, 20),
    Size(530, 5, 18.8, 30),
    Size(640, 6, 19.8, 40),
    Size(836, 8, 21.9, 36),
    Size(840, 8, 21.9, 40),
    Size(850, 8, 21.9, 50),
    Size(880, 8, 21.9, 80),
    Size(8100, 8, 21.9, 100),
    Size(1050, 10, 23.9, 50),
    Size(1080, 10, 23.9, 80),
    Size(10100, 10, 23.9, 100),
    Size(12100, 12, 25.9, 100),
    Size(12140, 12, 25.9, 140),
    Size(1475, 14, 27.9, 75),
    Size(14100, 14, 27.9, 100),
    Size(14140, 14, 27.9, 140),
]


class DominoInputs:
    """The Domino options of an add-in dialog, mixed into the add-in's
    Inputs class.

    The add-in calls the add_domino_* methods from its own __init__, before
    Inputs.__init__ collects the inputs, at the points where they belong in
    its dialog. The input ids end up in stored edit states and saved
    defaults, so they must not change.
    """

    domino_size: inputs.DropDownInput
    domino_end_stop: inputs.DropDownInput
    domino_length_offset: inputs.FloatInput
    domino_loose_slots: inputs.DropDownInput
    domino_loose_slot_extra: inputs.FloatInput
    domino_exact_slot_last: inputs.CheckboxInput
    domino_height_offset: inputs.FloatInput
    domino_fence_height: inputs.DropDownInput
    domino_fence_distance: inputs.FloatInput
    domino_depth_mode: inputs.DropDownInput
    domino_depth_offset: inputs.FloatInput
    domino_material_remaining: inputs.FloatInput
    domino_marks: inputs.DropDownInput
    domino_mark_depth: inputs.FloatInput
    domino_mark_length: inputs.FloatInput
    #: How validation messages and tooltips name the board that receives
    #: the slots.
    domino_slot_board: str

    def add_domino_size_input(
        self,
        update_visibility: Callable[[], bool],
    ) -> None:
        self.domino_size = inputs.DropDownInput(
            id="dominoSize",
            name="Domino Size",
            options=[
                inputs.DropDownInput.Item(size.name, size.value)
                for size in SIZES
            ],
            default_value=530,
            tool_tip="Festool DOMINO tenon size (thickness x length in mm).",
            update_visibility=update_visibility,
        )

    def add_domino_end_stop_input(
        self,
        update_visibility: Callable[[], bool],
    ) -> None:
        Item = inputs.DropDownInput.Item
        self.domino_end_stop = inputs.DropDownInput(
            id="dominoEndStop",
            name="End Stop",
            options=[
                Item("37 mm (Stop Latch)", EndStop.STOP_LATCH.value),
                Item("20 mm (Additional Stop)", EndStop.ADDITIONAL_STOP.value),
                Item("Custom", EndStop.CUSTOM.value),
            ],
            default_value=EndStop.STOP_LATCH.value,
            tool_tip=(
                "Distance from each end of the selected edge to the center of "
                "the first and last Domino. 37 mm matches the Domino "
                "machine's stop latches, 20 mm the additional stop; Custom "
                "uses the End Offset value."
            ),
            update_visibility=update_visibility,
        )

    def add_domino_slot_inputs(
        self,
        units: str,
        is_domino: Callable[[], bool],
        slot_board: str,
    ) -> None:
        """The inputs that shape the slots and the reference marks.
        `slot_board` names the board that receives the slots, e.g.
        "adjacent board"."""
        Item = inputs.DropDownInput.Item
        self.domino_slot_board = slot_board
        self.domino_length_offset = inputs.FloatInput(
            id="dominoLengthOffset",
            name="Slot Length Offset",
            default_value=0,
            tool_tip=(
                "Added to the Domino's width to get the slot length along "
                "the edge. Negative values make the slot tighter."
            ),
            units=units,
            update_visibility=is_domino,
        )
        # A value input created from the number 0 cannot report its
        # expression until the dialog is on screen; the slot dimensions are
        # built from these expressions, so give both an explicit one.
        self.domino_length_offset.default_expression = "0 mm"
        self.domino_loose_slots = inputs.DropDownInput(
            id="dominoLooseSlots",
            name="Loose Slots",
            options=[
                Item("None", LooseSlots.NONE.value),
                Item("+6 mm", LooseSlots.PLUS_6.value),
                Item("+10 mm", LooseSlots.PLUS_10.value),
                Item("Custom", LooseSlots.CUSTOM.value),
            ],
            default_value=LooseSlots.NONE.value,
            tool_tip=(
                "Makes every slot but one per board longer, like the wider "
                "mortise settings of the Domino machine (+6 mm and +10 mm). "
                "The one exact slot keeps the boards aligned, the loose "
                "ones forgive small position errors."
            ),
            update_visibility=is_domino,
        )
        has_loose_slots = lambda: (
            is_domino()
            and self.domino_loose_slots.value != LooseSlots.NONE.value
        )
        self.domino_loose_slot_extra = inputs.FloatInput(
            id="dominoLooseSlotExtra",
            name="Loose Slot Extra Length",
            default_value=0.6,
            tool_tip="Extra length of the loose slots.",
            units=units,
            update_visibility=lambda: (
                is_domino()
                and self.domino_loose_slots.value == LooseSlots.CUSTOM.value
            ),
        )
        self.domino_loose_slot_extra.minimum_value = 0
        self.domino_loose_slot_extra.minimum_inclusive = False
        self.domino_exact_slot_last = inputs.CheckboxInput(
            id="dominoExactSlotLast",
            name="Exact Slot at Other End",
            default_value=False,
            tool_tip=(
                "The exact slot is the first one along the edge. Tick this "
                "to make it the one at the other end instead."
            ),
            update_visibility=has_loose_slots,
        )
        self.domino_height_offset = inputs.FloatInput(
            id="dominoHeightOffset",
            name="Slot Height Offset",
            default_value=0,
            tool_tip=(
                "Added to the Domino's thickness to get the slot height. "
                "Negative values make the slot tighter."
            ),
            units=units,
            update_visibility=is_domino,
        )
        self.domino_height_offset.default_expression = "0 mm"
        self.domino_fence_height = inputs.DropDownInput(
            id="dominoFenceHeight",
            name="Fence Height",
            options=(
                [Item("Centered", FENCE_CENTERED)]
                + [Item(stop.name, stop.value) for stop in FENCE_STOPS]
                + [Item("Custom", FENCE_CUSTOM)]
            ),
            default_value=FENCE_CENTERED,
            tool_tip=(
                "Position of the slots across the board's thickness. "
                "Centered follows the board. A fence stop is named after the "
                "board thickness it is made for and puts the slot half that "
                "far from the large face next to the selected edge - the "
                "face the Domino machine's fence rests on. Custom takes that "
                "distance directly."
            ),
            update_visibility=is_domino,
        )
        self.domino_fence_distance = inputs.FloatInput(
            id="dominoFenceDistance",
            name="Slot Center from Face",
            default_value=1,
            tool_tip=(
                "Distance from the large face next to the selected edge to "
                "the center of the slots."
            ),
            units=units,
            update_visibility=lambda: (
                is_domino()
                and self.domino_fence_height.value == FENCE_CUSTOM
            ),
        )
        self.domino_fence_distance.minimum_value = 0
        self.domino_fence_distance.minimum_inclusive = False
        self.domino_depth_mode = inputs.DropDownInput(
            id="dominoDepthMode",
            name="Slot Depth",
            options=[
                Item("Half Domino Length", DepthMode.HALF_LENGTH.value),
                Item("Material Remaining", DepthMode.MATERIAL_REMAINING.value),
            ],
            default_value=DepthMode.HALF_LENGTH.value,
            tool_tip=(
                "Half Domino Length cuts the slot half the Domino's length "
                "plus the Depth Offset deep. Material Remaining cuts as deep "
                "as possible while leaving the given thickness of the "
                f"{slot_board}."
            ),
            update_visibility=is_domino,
        )
        is_half_length = lambda: (
            self.domino_depth_mode.value == DepthMode.HALF_LENGTH.value
        )
        self.domino_depth_offset = inputs.FloatInput(
            id="dominoDepthOffset",
            name="Depth Offset",
            default_value=0.05,
            tool_tip="Added to half the Domino's length to get the slot depth.",
            units=units,
            update_visibility=lambda: is_domino() and is_half_length(),
        )
        self.domino_material_remaining = inputs.FloatInput(
            id="dominoMaterialRemaining",
            name="Material Remaining",
            default_value=0.3,
            tool_tip=(
                f"Thickness of the {slot_board} left below the slot. The "
                "slot depth follows the board's thickness."
            ),
            units=units,
            update_visibility=lambda: is_domino() and not is_half_length(),
        )
        self.domino_material_remaining.minimum_value = 0
        self.domino_marks = inputs.DropDownInput(
            id="dominoMarks",
            name="Reference Marks",
            options=[
                Item("None", Marks.NONE.value),
                Item("All Dominos", Marks.ALL.value),
                Item("Skip First and Last", Marks.SKIP_FIRST_AND_LAST.value),
            ],
            default_value=Marks.NONE.value,
            tool_tip=(
                "Engraves V-grooves (for a 90 degree chamfer cutter) at the "
                "Domino positions into the large face next to the selected "
                "edge, as alignment marks for the Domino machine. Skip First "
                "and Last leaves out the two end positions, which the "
                "machine's stops locate."
            ),
            update_visibility=is_domino,
        )
        has_marks = lambda: (
            is_domino() and self.domino_marks.value != Marks.NONE.value
        )
        self.domino_mark_depth = inputs.FloatInput(
            id="dominoMarkDepth",
            name="Mark Depth",
            default_value=0.03,
            tool_tip=(
                "Depth of the V-grooves. Cut with a 90 degree cutter, a "
                "groove is twice as wide as it is deep."
            ),
            units=units,
            update_visibility=has_marks,
        )
        self.domino_mark_depth.minimum_value = 0
        self.domino_mark_depth.minimum_inclusive = False
        self.domino_mark_length = inputs.FloatInput(
            id="dominoMarkLength",
            name="Mark Length",
            default_value=0.4,
            tool_tip="Length of the V-grooves, measured from the edge.",
            units=units,
            update_visibility=has_marks,
        )
        self.domino_mark_length.minimum_value = 0
        self.domino_mark_length.minimum_inclusive = False

    # Values derived from the inputs. Lengths are in cm, expressions are
    # written into the sketch dimensions and feature extents.

    def domino_size_spec(self) -> Size:
        value = self.domino_size.value
        size = next((size for size in SIZES if size.value == value), None)
        if not size:
            raise ValueError("Select a Domino size.")
        return size

    def domino_slot_height(self, size: Size) -> float:
        return size.thickness / 10 + self.domino_height_offset.value

    def domino_slot_length(self, size: Size) -> float:
        """Length of an exact slot along the edge."""
        return size.width / 10 + self.domino_length_offset.value

    def domino_slot_length_expression(self, size: Size) -> str:
        return f"{size.width:g} mm + ({self.domino_length_offset.expression})"

    def domino_loose_extra(self) -> tuple[float, str] | None:
        """Extra length of the loose slots as value and expression, or None
        when every slot is cut to the exact size."""
        mode = LooseSlots(self.domino_loose_slots.value)
        if mode == LooseSlots.NONE:
            return None
        if mode == LooseSlots.CUSTOM:
            return (
                self.domino_loose_slot_extra.value,
                self.domino_loose_slot_extra.expression,
            )
        return mode.value / 10, f"{mode.value} mm"

    def domino_slot_center_distance(self) -> tuple[float, str] | None:
        """Distance from the selected edge's large face to the slot centers,
        as value and expression. None centers the slots on each board."""
        value = self.domino_fence_height.value
        if value == FENCE_CENTERED:
            return None
        if value == FENCE_CUSTOM:
            return (
                self.domino_fence_distance.value,
                self.domino_fence_distance.expression,
            )
        stop = next((stop for stop in FENCE_STOPS if stop.value == value), None)
        if not stop:
            raise ValueError("Select a Fence Height.")
        return stop.thickness / 20, f"{stop.thickness / 2:g} mm"

    def domino_end_offset(
        self,
        custom: inputs.FloatInput,
    ) -> tuple[float, str]:
        """Distance from the edge ends to the centers of the first and last
        Domino, as value and expression: the End Stop's, or the add-in's
        `custom` input for a Custom stop."""
        stop = EndStop(self.domino_end_stop.value)
        if stop != EndStop.CUSTOM:
            return stop.value / 10, f"{stop.value} mm"
        return custom.value, custom.expression

    def domino_marked_stations(
        self,
        stations: list[adsk.fusion.SketchPoint],
    ) -> list[adsk.fusion.SketchPoint]:
        marks = Marks(self.domino_marks.value)
        if marks == Marks.NONE:
            return []
        # A single Domino is centered on the edge, out of reach of the
        # machine's end stops, so it always keeps its mark.
        if marks == Marks.SKIP_FIRST_AND_LAST and len(stations) > 1:
            return stations[1:-1]
        return list(stations)

    def domino_validation_error(
        self,
        board_thickness: float,
        slot_board_thickness: float,
        tolerance: float,
    ) -> str | None:
        """Checks the Domino options against the thinnest selected board
        and the board that receives the slots."""
        try:
            size = self.domino_size_spec()
        except Exception as exc:
            return str(exc)
        height = self.domino_slot_height(size)
        if height <= tolerance:
            return "Slot Height Offset must leave a positive slot height."
        if self.domino_slot_length(size) - height <= tolerance:
            return (
                "Slot Length Offset must leave the slot longer than it is "
                "high."
            )
        if height >= board_thickness - tolerance:
            return "The Domino slot is higher than the selected board is thick."
        try:
            center_distance = self.domino_slot_center_distance()
        except Exception as exc:
            return str(exc)
        if center_distance is not None and (
            center_distance[0] - height / 2 < -tolerance
            or center_distance[0] + height / 2 > board_thickness + tolerance
        ):
            return (
                "At this Fence Height the Domino slot does not fit within "
                "the selected board's thickness."
            )

        slot_board = self.domino_slot_board
        if (
            DepthMode(self.domino_depth_mode.value)
            == DepthMode.MATERIAL_REMAINING
        ):
            remaining = self.domino_material_remaining.value
            if remaining < 0:
                return "Material Remaining cannot be negative."
            if remaining >= slot_board_thickness - tolerance:
                return (
                    f"Material Remaining must be less than the {slot_board}'s "
                    "thickness."
                )
        else:
            depth = size.length / 20 + self.domino_depth_offset.value
            if depth <= tolerance:
                return "Depth Offset must leave a positive slot depth."
            if depth >= slot_board_thickness - tolerance:
                return (
                    f"The Domino slot is deeper than the {slot_board} is "
                    "thick. Pick a shorter Domino or set Slot Depth to "
                    "Material Remaining."
                )

        loose_extra = self.domino_loose_extra()
        if loose_extra is not None and loose_extra[0] <= 0:
            return "Loose Slot Extra Length must be greater than zero."

        if Marks(self.domino_marks.value) != Marks.NONE:
            if self.domino_mark_depth.value <= 0:
                return "Mark Depth must be greater than zero."
            if self.domino_mark_length.value <= 0:
                return "Mark Length must be greater than zero."
            if self.domino_mark_depth.value >= board_thickness - tolerance:
                return "Mark Depth must be less than the board's thickness."
        return None


@dataclass(frozen=True)
class Board:
    """A board that gets Dominos along its selected edge: the edge, the
    board's end face along it (which butts against the board receiving the
    slots), and the board's thickness."""

    edge: adsk.fusion.BRepEdge
    small_face: adsk.fusion.BRepFace
    thickness: float


@dataclass(frozen=True)
class Sketches:
    positions: adsk.fusion.Sketch
    slots: adsk.fusion.Sketch
    marks: adsk.fusion.Sketch | None
    #: Per station of the first board, a construction line on its selected
    #: edge, centered on the station and as long as an exact slot. Only
    #: built on request (see DominoBuilder.create_sketches).
    footprints: list[adsk.fusion.SketchLine]
    #: From the sketch plane into the board receiving the slots.
    slot_direction: adsk.core.Vector3D


class DominoBuilder:
    """Builds the Domino sketches and cuts of one joint.

    All sketches lie in the plane of the first board's small face. Every
    further board shares the first board's stations: its slots are cut at
    the same positions along the edge, and its marks are engraved there.
    """

    def __init__(
        self,
        sketcher: edge_sketch.EdgeSketcher,
        settings: DominoInputs,
        name: str,
    ):
        """`name` prefixes the names of the created sketches and features,
        e.g. "Connector (Native)"."""
        self.sketcher = sketcher
        self.settings = settings
        self.name = name

    def create_sketches(
        self,
        component: adsk.fusion.Component,
        boards: list[Board],
        positions: list[adsk.core.Point3D],
        custom_points: list[adsk.core.Base] | None,
        end_offset: tuple[float, str] | None,
        footprints: bool = False,
    ) -> Sketches:
        """`positions`, `custom_points` and `end_offset` place the stations
        along the first board's edge, see EdgeSketcher.add_station_points.
        With `footprints`, the positions sketch also gets a footprint line
        per station (see Sketches.footprints)."""
        sketcher = self.sketcher
        settings = self.settings
        first = boards[0]
        size = settings.domino_size_spec()
        edge_direction = utils.brep.normal_along_edge(first.edge)
        inwards = [
            utils.brep.normal_into_face(board.edge, board.small_face)
            for board in boards
        ]

        # The positions get a sketch of their own: the slot and mark
        # sketches then only hold geometry hanging off projected points.
        # Drawn into one sketch, the positions and around twenty slots are
        # more than Fusion's sketch solver resolves.
        position_context = sketcher.create_sketch(
            component,
            first.small_face,
            first.edge,
            f"{self.name} - Domino Positions",
            "domino",
        )
        station_points = sketcher.add_station_points(
            position_context,
            positions,
            custom_points,
            end_offset,
        )
        # Per board, first board first: the stations on the board's own
        # selected edge (the marks are built on these) and the slot centers.
        board_stations: list[list[adsk.fusion.SketchPoint]] = [
            station_points
        ] + [[] for _ in boards[1:]]
        board_centers: list[list[adsk.fusion.SketchPoint]]
        center_distance = settings.domino_slot_center_distance()
        if center_distance is None:
            centers, cross_lines = sketcher.board_center_points(
                position_context,
                station_points,
                first.small_face,
                first.edge,
                inwards[0],
            )
            board_centers = [centers] + [
                sketcher.centered_points_for_board(
                    position_context,
                    board.edge,
                    board.small_face,
                    board.thickness,
                    cross_lines,
                    board_stations[board_index],
                )
                for board_index, board in enumerate(boards[1:], start=1)
            ]
        else:
            centers, offset_lines = sketcher.edge_offset_points(
                position_context,
                station_points,
                inwards[0],
                center_distance[0],
                center_distance[1],
                "dominoFenceDistance",
            )
            board_centers = [centers] + [
                sketcher.offset_points_for_board(
                    position_context,
                    board.edge,
                    board.small_face,
                    offset_lines,
                    board_stations[board_index],
                )
                for board_index, board in enumerate(boards[1:], start=1)
            ]
        footprint_lines = (
            self._add_footprints(
                position_context,
                station_points,
                edge_direction,
                size,
            )
            if footprints
            else []
        )
        sketcher.require_fully_constrained(position_context.sketch)

        slot_context = sketcher.create_sketch(
            component,
            first.small_face,
            first.edge,
            f"{self.name} - Domino Slots",
            "dominoSlot",
        )
        self._add_slots(
            slot_context,
            sketcher.project_points(
                slot_context.sketch,
                [center for centers in board_centers for center in centers],
                "Domino slot centers",
            ),
            len(station_points),
            edge_direction,
            size,
        )
        sketcher.require_fully_constrained(slot_context.sketch)

        mark_context: edge_sketch.SketchContext | None = None
        marked_stations = [
            settings.domino_marked_stations(stations)
            for stations in board_stations
        ]
        if marked_stations[0]:
            mark_context = sketcher.create_sketch(
                component,
                first.small_face,
                first.edge,
                f"{self.name} - Domino Marks",
                "dominoMark",
            )
            self._add_marks(
                mark_context,
                marked_stations,
                edge_direction,
                [board.edge for board in boards],
                inwards,
            )
            sketcher.require_fully_constrained(mark_context.sketch)

        return Sketches(
            positions=position_context.sketch,
            slots=slot_context.sketch,
            marks=mark_context.sketch if mark_context else None,
            footprints=footprint_lines,
            slot_direction=utils.brep.normal_away_from_body(first.small_face),
        )

    def cut(
        self,
        component: adsk.fusion.Component,
        sketches: Sketches,
        slot_body_token: str,
        slot_far_face_token: str,
        mark_body_tokens: list[str],
    ) -> adsk.fusion.Feature:
        """Cuts the slots into the slot body and the marks into the mark
        bodies (the selected boards). The far face is the slot body's face
        opposite the sketch plane, which Material Remaining measures from.
        Returns the last feature created."""
        sketcher = self.sketcher
        settings = self.settings
        design = component.parentDesign
        slot_body = edge_sketch.find_by_token(
            design,
            slot_body_token,
            adsk.fusion.BRepBody,
            "Domino slot body",
        )
        last_feature: adsk.fusion.Feature
        if (
            DepthMode(settings.domino_depth_mode.value)
            == DepthMode.MATERIAL_REMAINING
        ):
            # Cut up to the slot board's far face, so the remaining
            # material survives a change of that board's thickness.
            last_feature = sketcher.create_cut_extrude_to_face(
                component=component,
                sketch=sketches.slots,
                target_body=slot_body,
                target_face=edge_sketch.find_by_token(
                    design,
                    slot_far_face_token,
                    adsk.fusion.BRepFace,
                    "far face of the Domino slot body",
                ),
                direction=sketches.slot_direction,
                offset=settings.domino_material_remaining.expression,
                name=f"{self.name} - Domino Slot Cut",
                parameter_role="dominoSlotRemaining",
            )
        else:
            size = settings.domino_size_spec()
            last_feature = sketcher.create_cut_extrude(
                component=component,
                sketch=sketches.slots,
                target_body=slot_body,
                direction=sketches.slot_direction,
                distance=(
                    f"{size.length / 2:g} mm + "
                    f"({settings.domino_depth_offset.expression})"
                ),
                name=f"{self.name} - Domino Slot Cut",
                parameter_role="dominoSlotDepth",
            )

        if sketches.marks:
            last_feature = sketcher.create_cut_extrude(
                component=component,
                sketch=sketches.marks,
                target_body=[
                    edge_sketch.find_by_token(
                        design,
                        token,
                        adsk.fusion.BRepBody,
                        "Domino mark body",
                    )
                    for token in mark_body_tokens
                ],
                direction=edge_sketch.opposite(sketches.slot_direction),
                distance=settings.domino_mark_length.expression,
                name=f"{self.name} - Domino Mark Cut",
                parameter_role="dominoMarkLength",
            )

        # No cut is made from the positions sketch, so nothing has hidden it.
        sketches.positions.isVisible = False
        return last_feature

    def _add_footprints(
        self,
        context: edge_sketch.SketchContext,
        stations: list[adsk.fusion.SketchPoint],
        edge_direction: adsk.core.Vector3D,
        size: Size,
    ) -> list[adsk.fusion.SketchLine]:
        sketch = context.sketch
        lines = sketch.sketchCurves.sketchLines
        constraints = sketch.geometricConstraints
        half_length = self.settings.domino_slot_length(size) / 2
        footprints: list[adsk.fusion.SketchLine] = []
        for station in stations:
            station_model = station.worldGeometry
            footprint = lines.addByTwoPoints(
                sketch.modelToSketchSpace(
                    edge_sketch.translated(
                        station_model,
                        edge_direction,
                        -half_length,
                    )
                ),
                sketch.modelToSketchSpace(
                    edge_sketch.translated(
                        station_model,
                        edge_direction,
                        half_length,
                    )
                ),
            )
            if not footprint:
                raise RuntimeError(
                    "Fusion failed to create a Domino footprint."
                )
            footprint.isConstruction = True
            # Parallel through the station, which lies on the edge: the
            # footprint runs along the edge without a second constraint
            # tying it to the edge line.
            constraints.addParallel(footprint, context.edge_line)
            constraints.addMidPoint(station, footprint)
            if not footprints:
                self.sketcher.add_distance_dimension(
                    sketch,
                    footprint.startSketchPoint,
                    footprint.endSketchPoint,
                    self.settings.domino_slot_length_expression(size),
                    "dominoFootprint",
                )
            else:
                constraints.addEqual(footprints[0], footprint)
            footprints.append(footprint)
        return footprints

    def _add_slots(
        self,
        context: edge_sketch.SketchContext,
        centers: list[adsk.fusion.SketchPoint],
        station_count: int,
        edge_direction: adsk.core.Vector3D,
        size: Size,
    ) -> None:
        """`centers` holds `station_count` slot centers per board, each
        board's in the same order along the edge."""
        sketch = context.sketch
        constraints = sketch.geometricConstraints
        settings = self.settings
        height = settings.domino_slot_height(size)
        exact_span = settings.domino_slot_length(size) - height
        loose_extra = settings.domino_loose_extra()
        exact_station = (
            station_count - 1
            if settings.domino_exact_slot_last.value
            else 0
        )
        height_expression = (
            f"{size.thickness:g} mm + "
            f"({settings.domino_height_offset.expression})"
        )
        first_width_parameter: adsk.fusion.ModelParameter | None = None
        exact_reference: adsk.fusion.SketchLine | None = None
        exact_span_parameter: adsk.fusion.ModelParameter | None = None
        loose_reference: adsk.fusion.SketchLine | None = None
        # Each board's exact slot comes first, so the loose slots can be
        # dimensioned relative to it.
        order = sorted(
            range(len(centers)),
            key=lambda index: index % station_count != exact_station,
        )
        for index in order:
            center = centers[index]
            is_loose = (
                loose_extra is not None
                and index % station_count != exact_station
            )
            span = exact_span
            if loose_extra and is_loose:
                span += loose_extra[0]
            center_model = center.worldGeometry
            width_dimension, centerline = (
                self.sketcher.add_center_to_center_slot(
                    sketch,
                    sketch.modelToSketchSpace(
                        edge_sketch.translated(
                            center_model,
                            edge_direction,
                            -span / 2,
                        )
                    ),
                    sketch.modelToSketchSpace(
                        edge_sketch.translated(
                            center_model,
                            edge_direction,
                            span / 2,
                        )
                    ),
                    (
                        height_expression
                        if first_width_parameter is None
                        else first_width_parameter.name
                    ),
                    f"dominoSlot{index + 1}Height",
                )
            )
            constraints.addParallel(centerline, context.edge_line)
            constraints.addMidPoint(center, centerline)
            if first_width_parameter is None:
                first_width_parameter = width_dimension.parameter
            if not is_loose and exact_reference is None:
                # The slot's overall length is the Domino's width: the
                # center-to-center span is that minus the slot's own height.
                exact_span_parameter = self.sketcher.add_distance_dimension(
                    sketch,
                    centerline.startSketchPoint,
                    centerline.endSketchPoint,
                    (
                        f"{settings.domino_slot_length_expression(size)}"
                        f" - {first_width_parameter.name}"
                    ),
                    "dominoSlotSpan",
                ).parameter
                exact_reference = centerline
            elif loose_extra and is_loose and loose_reference is None:
                if exact_span_parameter is None:
                    raise RuntimeError(
                        "The exact Domino slot must precede the loose slots."
                    )
                self.sketcher.add_distance_dimension(
                    sketch,
                    centerline.startSketchPoint,
                    centerline.endSketchPoint,
                    f"{exact_span_parameter.name} + ({loose_extra[1]})",
                    "dominoLooseSlotSpan",
                )
                loose_reference = centerline
            else:
                constraints.addEqual(
                    loose_reference if is_loose else exact_reference,
                    centerline,
                )

    def _add_marks(
        self,
        context: edge_sketch.SketchContext,
        marked_stations: list[list[adsk.fusion.SketchPoint]],
        edge_direction: adsk.core.Vector3D,
        edges: list[adsk.fusion.BRepEdge],
        inwards: list[adsk.core.Vector3D],
    ) -> None:
        """Draws one V-groove cross-section per marked station and board.

        The sketch lies in the plane of the small faces, so each triangle is
        the cross-section of a groove that the mark cut then runs into the
        board, away from the selected edge.

        `marked_stations` holds, per board, the stations to mark as points
        of the positions sketch on that board's selected edge; `edges` and
        `inwards` are the boards' selected edges and the directions from
        them into the boards.
        """
        sketch = context.sketch
        lines = sketch.sketchCurves.sketchLines
        constraints = sketch.geometricConstraints
        depth = self.settings.domino_mark_depth.value
        # Every board's stations are projected from the positions sketch, so
        # all grooves are built the same way on points that follow that
        # sketch.
        projected = self.sketcher.project_points(
            sketch,
            [station for stations in marked_stations for station in stations],
            "Domino stations",
        )
        reference_depth_line: adsk.fusion.SketchLine | None = None
        reference_flanks: list[adsk.fusion.SketchLine] | None = None
        for board_index, (edge, inward) in enumerate(zip(edges, inwards)):
            count = len(marked_stations[board_index])
            stations, projected = projected[:count], projected[count:]
            edge_line = (
                context.edge_line
                if board_index == 0
                else self.sketcher.project_reference_line(
                    sketch,
                    edge,
                    "additional board edge",
                )
            )
            for station in stations:
                depth_line = lines.addByTwoPoints(
                    station,
                    sketch.modelToSketchSpace(
                        edge_sketch.translated(
                            station.worldGeometry,
                            inward,
                            depth,
                        )
                    ),
                )
                if not depth_line:
                    raise RuntimeError(
                        "Fusion failed to create a Domino mark depth line."
                    )
                depth_line.isConstruction = True
                constraints.addPerpendicular(depth_line, edge_line)
                if reference_depth_line is None:
                    self.sketcher.add_distance_dimension(
                        sketch,
                        depth_line.startSketchPoint,
                        depth_line.endSketchPoint,
                        self.settings.domino_mark_depth.expression,
                        "dominoMarkDepth",
                    )
                    reference_depth_line = depth_line
                else:
                    constraints.addEqual(reference_depth_line, depth_line)
                flanks = self._add_mark_groove(
                    sketch,
                    depth_line,
                    edge_line,
                    edge_direction,
                    depth,
                    reference_flanks,
                )
                if reference_flanks is None:
                    reference_flanks = flanks

    def _add_mark_groove(
        self,
        sketch: adsk.fusion.Sketch,
        depth_line: adsk.fusion.SketchLine,
        edge_line: adsk.fusion.SketchLine,
        edge_direction: adsk.core.Vector3D,
        depth: float,
        reference_flanks: list[adsk.fusion.SketchLine] | None,
    ) -> list[adsk.fusion.SketchLine]:
        """Closes a 90 degree V around `depth_line`, which runs from the
        board's edge down to the bottom of the groove. Returns the two
        flanks; later grooves pass the first groove's as `reference_flanks`
        and copy its angle."""
        lines = sketch.sketchCurves.sketchLines
        constraints = sketch.geometricConstraints
        top_model = depth_line.startSketchPoint.worldGeometry
        # The groove's opening is created first and put on the edge while it
        # is still free; the flanks then pin its two ends. Closing the V
        # between two already positioned flank ends instead leaves a line
        # that Fusion reports as unconstrained.
        opening = lines.addByTwoPoints(
            sketch.modelToSketchSpace(
                edge_sketch.translated(top_model, edge_direction, -depth)
            ),
            sketch.modelToSketchSpace(
                edge_sketch.translated(top_model, edge_direction, depth)
            ),
        )
        if not opening:
            raise RuntimeError("Fusion failed to create a Domino mark.")
        constraints.addCollinear(opening, edge_line)
        flanks = [
            lines.addByTwoPoints(end, depth_line.endSketchPoint)
            for end in (opening.startSketchPoint, opening.endSketchPoint)
        ]
        if not all(flanks):
            raise RuntimeError("Fusion failed to create a Domino mark flank.")
        if reference_flanks is None:
            # Perpendicular flanks of equal length: a symmetric 90 degree V,
            # whose width follows from the depth alone.
            constraints.addPerpendicular(flanks[0], flanks[1])
            constraints.addEqual(flanks[0], flanks[1])
        else:
            for flank, reference in zip(flanks, reference_flanks):
                constraints.addParallel(flank, reference)
        return flanks
