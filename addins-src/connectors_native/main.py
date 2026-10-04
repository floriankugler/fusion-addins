from dataclasses import dataclass
from enum import Enum, unique
import os
from typing import cast

import adsk.core
import adsk.fusion

from lib import addin, inputs, ui_placement, utils
from lib.fusionbootstrap.runtime import RuntimeInfo


_addin: addin.Addin | None = None


@unique
class ConnectorType(Enum):
    CLAMEX_P10 = 10
    CLAMEX_P14 = 14
    CABINEO_8 = 8
    CABINEO_12 = 12
    CABINEO_8_M6 = 9
    DOMINO = 50

    @property
    def is_clamex(self) -> bool:
        return self in (ConnectorType.CLAMEX_P10, ConnectorType.CLAMEX_P14)

    @property
    def is_cabineo(self) -> bool:
        return self in (
            ConnectorType.CABINEO_8,
            ConnectorType.CABINEO_12,
            ConnectorType.CABINEO_8_M6,
        )

    @property
    def is_domino(self) -> bool:
        return self == ConnectorType.DOMINO


@unique
class CabineoSurface(Enum):
    NONE = 0
    FLUSH = 1
    ANTI_BREAK = 2


@unique
class CabineoInsert(Enum):
    M6X123 = 1
    M6X153 = 2
    THREADED_INSERT = 3


@unique
class PositioningMode(Enum):
    NUMBER = 1
    CUSTOM_POINTS = 2


@unique
class DominoEndStop(Enum):
    """Distance from the board end to the center of the first and last
    Domino. The value is the distance in mm set by the Domino machine's own
    stops: 37 mm for the built-in stop latches (stop pins on older machines),
    20 mm with the additional stop ZA-DF 500/700 fitted. CUSTOM uses the
    End Offset input instead."""

    STOP_LATCH = 37
    ADDITIONAL_STOP = 20
    CUSTOM = 0


@unique
class DominoDepthMode(Enum):
    HALF_LENGTH = 1
    MATERIAL_REMAINING = 2


@unique
class DominoLooseSlots(Enum):
    """Extra length of every slot but one per board, in mm. The two fixed
    steps match the wider mortise settings of the Domino DF 500, which cuts
    13, 19 or 23 mm plus the cutter diameter."""

    NONE = 0
    PLUS_6 = 6
    PLUS_10 = 10
    CUSTOM = 1


@unique
class DominoMarks(Enum):
    NONE = 0
    ALL = 1
    SKIP_FIRST_AND_LAST = 2


@dataclass(frozen=True)
class _DominoFenceStop:
    """A height stop of the Domino machine's fence. Stops are labelled with
    the board thickness they center the mortise on, so the mortise ends up
    half that far from the face the fence rests on."""

    value: int
    thickness: float
    label: str

    @property
    def name(self) -> str:
        return f"{self.thickness:g} mm ({self.label})"


_DOMINO_FENCE_CENTERED = 0
_DOMINO_FENCE_CUSTOM = 1
_DOMINO_FENCE_STOPS = [
    _DominoFenceStop(1000 + thickness, thickness, "Festool")
    for thickness in (16, 20, 22, 25, 28, 36, 40)
] + [
    # Aftermarket (e.g. 3D-printed) stop gauges add further thicknesses.
    _DominoFenceStop(2000 + thickness, thickness, "Alternative")
    for thickness in (12, 15, 18, 22, 24, 30, 36)
]


@dataclass(frozen=True)
class _DominoSize:
    """Festool DOMINO tenon dimensions in mm, as published in Festool's
    technical data ("thickness x length x width")."""

    value: int
    thickness: float
    width: float
    length: float

    @property
    def name(self) -> str:
        return f"{self.thickness:g} x {self.length:g}"


_DOMINO_SIZES = [
    _DominoSize(420, 4, 16.6, 20),
    _DominoSize(530, 5, 18.8, 30),
    _DominoSize(640, 6, 19.8, 40),
    _DominoSize(836, 8, 21.9, 36),
    _DominoSize(840, 8, 21.9, 40),
    _DominoSize(850, 8, 21.9, 50),
    _DominoSize(880, 8, 21.9, 80),
    _DominoSize(8100, 8, 21.9, 100),
    _DominoSize(1050, 10, 23.9, 50),
    _DominoSize(1080, 10, 23.9, 80),
    _DominoSize(10100, 10, 23.9, 100),
    _DominoSize(12100, 12, 25.9, 100),
    _DominoSize(12140, 12, 25.9, 140),
    _DominoSize(1475, 14, 27.9, 75),
    _DominoSize(14100, 14, 27.9, 100),
    _DominoSize(14140, 14, 27.9, 140),
]


@dataclass(frozen=True)
class _ResolvedGeometry:
    edge: adsk.fusion.BRepEdge
    access_face: adsk.fusion.BRepFace
    small_face: adsk.fusion.BRepFace
    guide_face: adsk.fusion.BRepFace
    access_thickness: float
    guide_thickness: float


@dataclass(frozen=True)
class _AdditionalBoard:
    """A board selected via an additional edge. It receives the same
    connector pattern as the first board: the shared access-sketch profiles
    are extruded into it, and its guide holes are added to the shared
    small-face sketch."""

    edge: adsk.fusion.BRepEdge
    access_face: adsk.fusion.BRepFace
    small_face: adsk.fusion.BRepFace
    access_thickness: float


@dataclass(frozen=True)
class _GuideHole:
    diameter: float
    diameter_expression: str
    depth: float | str
    collar_diameter: float | None = None
    collar_diameter_expression: str | None = None
    collar_depth: float | str | None = None


@dataclass(frozen=True)
class _SketchContext:
    sketch: adsk.fusion.Sketch
    edge_line: adsk.fusion.SketchLine
    edge_start: adsk.fusion.SketchPoint
    edge_end: adsk.fusion.SketchPoint
    parameter_role: str


@dataclass(frozen=True)
class _AccessLayout:
    station_points: list[adsk.fusion.SketchPoint]
    alignment_points: list[adsk.fusion.SketchPoint]


class _OptionalFloatInput(inputs.Input):
    input: adsk.core.StringValueCommandInput
    value: float | None
    expression: str | None
    validation_error: str | None

    def __init__(
        self,
        id: str,
        name: str,
        tool_tip: str,
        units_manager: adsk.core.UnitsManager,
        units: str,
        update_visibility=lambda: True,
    ):
        super().__init__(id, name, tool_tip, update_visibility)
        self.units_manager = units_manager
        self.units = units
        self.value = None
        self.expression = None
        self.validation_error = None

    def create_input(
        self,
        command_inputs: adsk.core.CommandInputs,
        params: adsk.fusion.CustomFeatureParameters | None,
    ):
        self.input = command_inputs.addStringValueInput(
            self.id,
            self.name,
            "",
        )
        self.input.tooltip = self.tool_tip

    def update_from_input(self):
        expression = self.input.value.strip()
        self.expression = expression or None
        self.validation_error = None
        if not expression:
            self.value = None
            self.input.isValueError = False
            return
        if not self.units_manager.isValidExpression(expression, self.units):
            self.value = None
            self.validation_error = f"{self.name} is not a valid length."
            self.input.isValueError = True
            return
        self.value = self.units_manager.evaluateExpression(
            expression,
            self.units,
        )
        self.input.isValueError = False

    def create_in_feature_input(
        self,
        feature_input: adsk.fusion.CustomFeatureInput,
    ):
        raise RuntimeError("Optional inputs are not used by custom features.")

    def update_in_feature(self, feature: adsk.fusion.CustomFeature):
        raise RuntimeError("Optional inputs are not used by custom features.")

    def update_from_feature(self, feature: adsk.fusion.CustomFeature):
        raise RuntimeError("Optional inputs are not used by custom features.")


def run(context, runtime_info: RuntimeInfo):
    global _addin
    _addin = ConnectorsNative(runtime_info)
    # Dev support: allow external tooling to restart this add-in by firing the
    # custom event '<id>_reload' (see lib/fusionbootstrap/reloader.py).
    from lib.fusionbootstrap import reloader
    entry = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "connectors_native.py",
    )
    reloader.ensure(runtime_info.id + "_reload", entry)


def stop(context):
    global _addin
    if _addin:
        _addin.shutdown()
    _addin = None


class ConnectorsNativeInputs(inputs.Inputs):
    class Positioning:
        NUMBER = inputs.DropDownInput.Item(
            "Number of Connectors",
            PositioningMode.NUMBER.value,
        )
        CUSTOM_POINTS = inputs.DropDownInput.Item(
            "Custom Points",
            PositioningMode.CUSTOM_POINTS.value,
        )

    class Types:
        CLAMEX_P10 = inputs.DropDownInput.Item(
            "Clamex P10",
            ConnectorType.CLAMEX_P10.value,
        )
        CLAMEX_P14 = inputs.DropDownInput.Item(
            "Clamex P14",
            ConnectorType.CLAMEX_P14.value,
        )
        CABINEO_8 = inputs.DropDownInput.Item(
            "Cabineo 8",
            ConnectorType.CABINEO_8.value,
        )
        CABINEO_12 = inputs.DropDownInput.Item(
            "Cabineo 12",
            ConnectorType.CABINEO_12.value,
        )
        CABINEO_8_M6 = inputs.DropDownInput.Item(
            "Cabineo 8 M6",
            ConnectorType.CABINEO_8_M6.value,
        )
        DOMINO = inputs.DropDownInput.Item(
            "Domino",
            ConnectorType.DOMINO.value,
        )

    class DominoEndStops:
        STOP_LATCH = inputs.DropDownInput.Item(
            "37 mm (Stop Latch)",
            DominoEndStop.STOP_LATCH.value,
        )
        ADDITIONAL_STOP = inputs.DropDownInput.Item(
            "20 mm (Additional Stop)",
            DominoEndStop.ADDITIONAL_STOP.value,
        )
        CUSTOM = inputs.DropDownInput.Item(
            "Custom",
            DominoEndStop.CUSTOM.value,
        )

    class DominoDepthModes:
        HALF_LENGTH = inputs.DropDownInput.Item(
            "Half Domino Length",
            DominoDepthMode.HALF_LENGTH.value,
        )
        MATERIAL_REMAINING = inputs.DropDownInput.Item(
            "Material Remaining",
            DominoDepthMode.MATERIAL_REMAINING.value,
        )

    class DominoLooseSlotModes:
        NONE = inputs.DropDownInput.Item(
            "None",
            DominoLooseSlots.NONE.value,
        )
        PLUS_6 = inputs.DropDownInput.Item(
            "+6 mm",
            DominoLooseSlots.PLUS_6.value,
        )
        PLUS_10 = inputs.DropDownInput.Item(
            "+10 mm",
            DominoLooseSlots.PLUS_10.value,
        )
        CUSTOM = inputs.DropDownInput.Item(
            "Custom",
            DominoLooseSlots.CUSTOM.value,
        )

    class DominoMarkModes:
        NONE = inputs.DropDownInput.Item("None", DominoMarks.NONE.value)
        ALL = inputs.DropDownInput.Item("All Dominos", DominoMarks.ALL.value)
        SKIP_FIRST_AND_LAST = inputs.DropDownInput.Item(
            "Skip First and Last",
            DominoMarks.SKIP_FIRST_AND_LAST.value,
        )

    class SurfaceTypes:
        NONE = inputs.DropDownInput.Item("None", CabineoSurface.NONE.value)
        FLUSH = inputs.DropDownInput.Item("Flush", CabineoSurface.FLUSH.value)
        ANTI_BREAK = inputs.DropDownInput.Item(
            "Anti-Break",
            CabineoSurface.ANTI_BREAK.value,
        )

    class InsertTypes:
        M6X123 = inputs.DropDownInput.Item(
            "M6x12.3",
            CabineoInsert.M6X123.value,
        )
        M6X153 = inputs.DropDownInput.Item(
            "M6x15.3",
            CabineoInsert.M6X153.value,
        )
        THREADED_INSERT = inputs.DropDownInput.Item(
            "Threaded Insert",
            CabineoInsert.THREADED_INSERT.value,
        )

    def __init__(self, units_manager: adsk.core.UnitsManager):
        units = units_manager.defaultLengthUnits

        self.edge = inputs.SelectionByEntityTokenInput(
            id="edge",
            name="Edges",
            filter=["LinearEdges"],
            # No lower bound: the preview's cuts can consume the selected
            # edges, which silently clears the selection input, and a
            # required selection would then disable OK and stop preview
            # updates. The "at least one edge" rule lives in
            # _validation_error, checked against the cached selection.
            lower_bound=0,
            upper_bound=0,
            tool_tip=(
                "Select one or more parallel edges lying in one plane. The "
                "first edge's large face receives the access holes and "
                "defines the connector positions; every edge's board gets "
                "the same pattern. The common plane must be perpendicular "
                "to the first edge's large face."
            ),
        )
        self.size = inputs.DropDownInput(
            id="size",
            name="Variant",
            options=utils.misc.class_property_values(
                ConnectorsNativeInputs.Types,
                inputs.DropDownInput.Item,
            ),
            default_value=ConnectorsNativeInputs.Types.CLAMEX_P10.value,
            tool_tip="Variant of the Clamex, Cabineo or Domino connector.",
        )
        is_domino = lambda: self.size.value == ConnectorType.DOMINO.value
        self.domino_size = inputs.DropDownInput(
            id="dominoSize",
            name="Domino Size",
            options=[
                inputs.DropDownInput.Item(size.name, size.value)
                for size in _DOMINO_SIZES
            ],
            default_value=530,
            tool_tip="Festool DOMINO tenon size (thickness x length in mm).",
            update_visibility=is_domino,
        )
        self.positioning = inputs.DropDownInput(
            id="positioning",
            name="Positioning",
            options=utils.misc.class_property_values(
                ConnectorsNativeInputs.Positioning,
                inputs.DropDownInput.Item,
            ),
            default_value=ConnectorsNativeInputs.Positioning.NUMBER.value,
            tool_tip=(
                "Place an exact number of connectors or align connectors "
                "with selected points."
            ),
        )
        is_number_positioning = lambda: (
            self.positioning.value == PositioningMode.NUMBER.value
        )
        self.points = inputs.SelectionByEntityTokenInput(
            id="points",
            name="Custom Points",
            filter=["Vertices", "SketchPoints", "ConstructionPoints"],
            lower_bound=0,
            upper_bound=0,
            tool_tip=(
                "Select one or more points. Each point is projected into the "
                "access sketch and perpendicularly onto the selected edge."
            ),
            update_visibility=lambda: (
                self.positioning.value
                == PositioningMode.CUSTOM_POINTS.value
            ),
        )
        self.number_of_connectors = inputs.IntegerInput(
            id="numberOfConnectors",
            name="Number of Connectors",
            default_value=3,
            minimum=1,
            maximum=100,
            tool_tip="Number of equally spaced connectors along the selected edge.",
            update_visibility=is_number_positioning,
        )
        has_end_offset = lambda: (
            is_number_positioning() and self.number_of_connectors.value > 1
        )
        self.domino_end_stop = inputs.DropDownInput(
            id="dominoEndStop",
            name="End Stop",
            options=utils.misc.class_property_values(
                ConnectorsNativeInputs.DominoEndStops,
                inputs.DropDownInput.Item,
            ),
            default_value=(
                ConnectorsNativeInputs.DominoEndStops.STOP_LATCH.value
            ),
            tool_tip=(
                "Distance from each end of the selected edge to the center of "
                "the first and last Domino. 37 mm matches the Domino "
                "machine's stop latches, 20 mm the additional stop; Custom "
                "uses the End Offset value."
            ),
            update_visibility=lambda: is_domino() and has_end_offset(),
        )
        self.offset = inputs.FloatInput(
            id="offset",
            name="End Offset",
            default_value=6,
            tool_tip=(
                "Distance from each end of the selected edge to the first and "
                "last connector. A single connector is always centered."
            ),
            units=units,
            update_visibility=lambda: (
                has_end_offset()
                and (
                    not is_domino()
                    or self.domino_end_stop.value
                    == DominoEndStop.CUSTOM.value
                )
            ),
        )
        self.offset.minimum_value = 0

        is_clamex = lambda: self.size.value in (
            ConnectorType.CLAMEX_P10.value,
            ConnectorType.CLAMEX_P14.value,
        )
        is_cabineo = lambda: self.size.value in (
            ConnectorType.CABINEO_8.value,
            ConnectorType.CABINEO_12.value,
            ConnectorType.CABINEO_8_M6.value,
        )
        self.clamex_guide_hole_diameter = inputs.FloatInput(
            id="clamexGuideHoleDiameter",
            name="Guide Hole Diameter",
            default_value=0.77,
            tool_tip="Diameter of the paired Clamex holes in the adjacent board.",
            units=units,
            update_visibility=is_clamex,
        )
        self.clamex_guide_hole_diameter.minimum_value = 0
        self.clamex_board_thickness = _OptionalFloatInput(
            id="clamexBoardThickness",
            name="Board Thickness (Optional)",
            tool_tip=(
                "Optional access-board thickness. When blank, Connector (Native) "
                "measures the selected board. The access cut is half this value."
            ),
            units_manager=units_manager,
            units=units,
            update_visibility=is_clamex,
        )
        self.through_guide_holes = inputs.CheckboxInput(
            id="throughGuideHoles",
            name="Through Opposite Holes",
            default_value=False,
            tool_tip="Cut the holes in the adjacent board through its full thickness.",
            update_visibility=lambda: not is_domino(),
        )
        self.cabineo_surface = inputs.DropDownInput(
            id="cabineoSurface",
            name="Surface",
            options=utils.misc.class_property_values(
                ConnectorsNativeInputs.SurfaceTypes,
                inputs.DropDownInput.Item,
            ),
            default_value=ConnectorsNativeInputs.SurfaceTypes.NONE.value,
            tool_tip="Surface treatment around the Cabineo connector pocket.",
            update_visibility=is_cabineo,
        )
        self.cabineo_anti_break_depth = inputs.FloatInput(
            id="cabineoAntiBreakDepth",
            name="Anti-Break Depth",
            default_value=0.08,
            tool_tip="Depth of the shallow Cabineo anti-break relief.",
            units=units,
            update_visibility=lambda: (
                is_cabineo()
                and self.cabineo_surface.value
                == CabineoSurface.ANTI_BREAK.value
            ),
        )
        self.cabineo_anti_break_depth.minimum_value = 0
        self.cabineo_anti_break_distance = inputs.FloatInput(
            id="cabineoAntiBreakDistance",
            name="Anti-Break Distance",
            default_value=0.06,
            tool_tip="Additional radius of the Cabineo anti-break relief.",
            units=units,
            update_visibility=lambda: (
                is_cabineo()
                and self.cabineo_surface.value
                == CabineoSurface.ANTI_BREAK.value
            ),
        )
        self.cabineo_anti_break_distance.minimum_value = 0

        is_m6 = lambda: self.size.value == ConnectorType.CABINEO_8_M6.value
        self.cabineo_insert_type = inputs.DropDownInput(
            id="insertType",
            name="Insert Type",
            options=utils.misc.class_property_values(
                ConnectorsNativeInputs.InsertTypes,
                inputs.DropDownInput.Item,
            ),
            default_value=ConnectorsNativeInputs.InsertTypes.THREADED_INSERT.value,
            tool_tip="Opposite-hole variant for the Cabineo 8 M6.",
            update_visibility=is_m6,
        )
        is_threaded_insert = lambda: (
            is_m6()
            and self.cabineo_insert_type.value
            == CabineoInsert.THREADED_INSERT.value
        )
        self.threaded_insert_core_diameter = inputs.FloatInput(
            id="threadedInsertCoreDiameter",
            name="Core Diameter",
            default_value=0.79,
            tool_tip="Core diameter of the threaded insert hole.",
            units=units,
            update_visibility=is_threaded_insert,
        )
        self.threaded_insert_core_diameter.minimum_value = 0
        self.threaded_insert_core_depth = inputs.FloatInput(
            id="threadedInsertCoreDepth",
            name="Core Depth",
            default_value=1.27 + 0.08,
            tool_tip="Core depth of the threaded insert hole.",
            units=units,
            update_visibility=is_threaded_insert,
        )
        self.threaded_insert_core_depth.minimum_value = 0
        self.threaded_insert_collar_diameter = inputs.FloatInput(
            id="threadedInsertCollarDiameter",
            name="Collar Diameter",
            default_value=1.27,
            tool_tip="Diameter of the threaded insert collar relief.",
            units=units,
            update_visibility=is_threaded_insert,
        )
        self.threaded_insert_collar_diameter.minimum_value = 0
        self.threaded_insert_collar_depth = inputs.FloatInput(
            id="threadedInsertCollarDepth",
            name="Collar Depth",
            default_value=0.08,
            tool_tip="Depth of the threaded insert collar relief.",
            units=units,
            update_visibility=is_threaded_insert,
        )
        self.threaded_insert_collar_depth.minimum_value = 0

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
            options=utils.misc.class_property_values(
                ConnectorsNativeInputs.DominoLooseSlotModes,
                inputs.DropDownInput.Item,
            ),
            default_value=(
                ConnectorsNativeInputs.DominoLooseSlotModes.NONE.value
            ),
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
            and self.domino_loose_slots.value != DominoLooseSlots.NONE.value
        )
        self.domino_loose_slot_extra = inputs.FloatInput(
            id="dominoLooseSlotExtra",
            name="Loose Slot Extra Length",
            default_value=0.6,
            tool_tip="Extra length of the loose slots.",
            units=units,
            update_visibility=lambda: (
                is_domino()
                and self.domino_loose_slots.value
                == DominoLooseSlots.CUSTOM.value
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
                [inputs.DropDownInput.Item("Centered", _DOMINO_FENCE_CENTERED)]
                + [
                    inputs.DropDownInput.Item(stop.name, stop.value)
                    for stop in _DOMINO_FENCE_STOPS
                ]
                + [inputs.DropDownInput.Item("Custom", _DOMINO_FENCE_CUSTOM)]
            ),
            default_value=_DOMINO_FENCE_CENTERED,
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
                and self.domino_fence_height.value == _DOMINO_FENCE_CUSTOM
            ),
        )
        self.domino_fence_distance.minimum_value = 0
        self.domino_fence_distance.minimum_inclusive = False
        self.domino_depth_mode = inputs.DropDownInput(
            id="dominoDepthMode",
            name="Slot Depth",
            options=utils.misc.class_property_values(
                ConnectorsNativeInputs.DominoDepthModes,
                inputs.DropDownInput.Item,
            ),
            default_value=(
                ConnectorsNativeInputs.DominoDepthModes.HALF_LENGTH.value
            ),
            tool_tip=(
                "Half Domino Length cuts the slot half the Domino's length "
                "plus the Depth Offset deep. Material Remaining cuts as deep "
                "as possible while leaving the given thickness of the "
                "adjacent board."
            ),
            update_visibility=is_domino,
        )
        is_domino_half_length = lambda: (
            self.domino_depth_mode.value == DominoDepthMode.HALF_LENGTH.value
        )
        self.domino_depth_offset = inputs.FloatInput(
            id="dominoDepthOffset",
            name="Depth Offset",
            default_value=0.05,
            tool_tip="Added to half the Domino's length to get the slot depth.",
            units=units,
            update_visibility=lambda: is_domino() and is_domino_half_length(),
        )
        self.domino_material_remaining = inputs.FloatInput(
            id="dominoMaterialRemaining",
            name="Material Remaining",
            default_value=0.3,
            tool_tip=(
                "Thickness of the adjacent board left below the slot. The "
                "slot depth follows the board's thickness."
            ),
            units=units,
            update_visibility=lambda: (
                is_domino() and not is_domino_half_length()
            ),
        )
        self.domino_material_remaining.minimum_value = 0
        self.domino_marks = inputs.DropDownInput(
            id="dominoMarks",
            name="Reference Marks",
            options=utils.misc.class_property_values(
                ConnectorsNativeInputs.DominoMarkModes,
                inputs.DropDownInput.Item,
            ),
            default_value=ConnectorsNativeInputs.DominoMarkModes.NONE.value,
            tool_tip=(
                "Engraves V-grooves (for a 90 degree chamfer cutter) at the "
                "Domino positions into the large face next to the selected "
                "edge, as alignment marks for the Domino machine. Skip First "
                "and Last leaves out the two end positions, which the "
                "machine's stops locate."
            ),
            update_visibility=is_domino,
        )
        has_domino_marks = lambda: (
            is_domino() and self.domino_marks.value != DominoMarks.NONE.value
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
            update_visibility=has_domino_marks,
        )
        self.domino_mark_depth.minimum_value = 0
        self.domino_mark_depth.minimum_inclusive = False
        self.domino_mark_length = inputs.FloatInput(
            id="dominoMarkLength",
            name="Mark Length",
            default_value=0.4,
            tool_tip="Length of the V-grooves, measured from the edge.",
            units=units,
            update_visibility=has_domino_marks,
        )
        self.domino_mark_length.minimum_value = 0
        self.domino_mark_length.minimum_inclusive = False

        super().__init__()


class ConnectorsNative(addin.Addin):
    inputs: ConnectorsNativeInputs
    _parameter_prefix: str
    _target_body_tokens: dict[str, str]
    _start_face_tokens: dict[str, str]

    @property
    def plugin_name(self) -> str:
        return "Connector (Native)"

    @property
    def plugin_desc(self) -> str:
        return (
            "Clamex, Cabineo and Domino connectors using native Fusion "
            "features."
        )

    @property
    def plugin_tooltip(self) -> str:
        return (
            "Creates fully constrained sketches and standard cut extrudes for "
            "Clamex, Cabineo and Domino connectors."
        )

    @property
    def resource_dir(self) -> str:
        return os.path.join(os.path.dirname(__file__), "Resources")

    @property
    def preview_enabled(self) -> bool:
        # All of execute() is native features (sketches + cut extrudes), so
        # the shared executePreview support can run it as a live preview.
        return True

    def get_ui_placement(self) -> ui_placement.UIPlacement:
        section = ui_placement.PlacementSpec(
            id="SeparatorBeforeCustomAddins",
            anchor_id="FusionMoveCommand",
            insert_before=True,
        )
        command = ui_placement.PlacementSpec(
            id=self.create_command_id,
            anchor_id=section.id,
            insert_before=True,
        )
        return ui_placement.UIPlacement(
            panel_id="SolidModifyPanel",
            command=command,
            section=section,
        )

    def create_inputs(self) -> ConnectorsNativeInputs:
        design = adsk.fusion.Design.cast(self.app.activeProduct)
        if not design:
            raise RuntimeError("Connector (Native) requires an active Fusion design.")
        return ConnectorsNativeInputs(design.unitsManager)

    def pre_select(self, input, selection) -> bool:
        if not self.inputs or not input:
            return True
        if input.id == self.inputs.edge.id:
            edge = adsk.fusion.BRepEdge.cast(selection)
            if not (
                edge
                and edge.body.isSolid
                and utils.brep.is_linear(edge)
                and edge.faces.count == 2
                and all(utils.brep.is_planar(face) for face in edge.faces)
            ):
                return False
            first = next(
                (
                    candidate
                    for entity in self.inputs.edge.value
                    if (candidate := adsk.fusion.BRepEdge.cast(entity))
                ),
                None,
            )
            return first is None or utils.brep.is_parallel(first, edge)
        if input.id == self.inputs.points.id:
            return bool(
                adsk.fusion.BRepVertex.cast(selection)
                or adsk.fusion.SketchPoint.cast(selection)
                or adsk.fusion.ConstructionPoint.cast(selection)
            )
        return True

    def _validate(self, args: adsk.core.ValidateInputsEventArgs):
        self._apply_validation(args, self._validation_error)

    def execute(self):
        error = self._validation_error()
        if error:
            raise ValueError(error)

        geometry = self._resolve_geometry()
        additional_boards = self._resolve_additional_boards(geometry)
        component = geometry.access_face.body.parentComponent
        design = component.parentDesign
        self._parameter_prefix = self._unique_parameter_prefix(design)
        self._target_body_tokens = {
            "access0": geometry.access_face.body.entityToken,
            "guide": geometry.guide_face.body.entityToken,
        }
        self._start_face_tokens = {
            "access0": geometry.access_face.entityToken,
        }
        for board_index, board in enumerate(additional_boards, start=1):
            self._target_body_tokens[f"access{board_index}"] = (
                board.edge.body.entityToken
            )
            self._start_face_tokens[f"access{board_index}"] = (
                board.access_face.entityToken
            )
        connector_type = ConnectorType(self.inputs.size.value)
        surface = CabineoSurface(self.inputs.cabineo_surface.value)
        positions = self._connector_positions(geometry.edge)
        edge_direction = utils.brep.normal_along_edge(geometry.edge)
        access_inward = utils.brep.normal_into_face(
            geometry.edge,
            geometry.access_face,
        )
        small_face_inward = utils.brep.normal_into_face(
            geometry.edge,
            geometry.small_face,
        )
        access_cut_direction = self._opposite(
            utils.brep.normal_away_from_body(geometry.access_face)
        )
        opposite_cut_direction = utils.brep.normal_away_from_body(
            geometry.small_face
        )
        if connector_type.is_domino:
            self._execute_domino(
                component,
                geometry,
                additional_boards,
                positions,
                edge_direction,
                small_face_inward,
                opposite_cut_direction,
            )
            return

        access_context = self._create_sketch(
            component,
            geometry.access_face,
            geometry.edge,
            "Connector (Native) - Access Holes",
            "access",
        )
        access_layout = self._add_access_geometry(
            access_context,
            positions,
            access_inward,
            connector_type,
            geometry.edge,
        )
        self._require_fully_constrained(access_context.sketch)

        relief_context: _SketchContext | None = None
        if connector_type.is_cabineo and surface != CabineoSurface.NONE:
            relief_context = self._create_sketch(
                component,
                geometry.access_face,
                geometry.edge,
                "Connector (Native) - Access Relief",
                "accessRelief",
            )
            relief_station_points = self._project_points(
                relief_context.sketch,
                access_layout.station_points,
                "access relief stations",
            )
            self._add_access_relief_geometry(
                relief_context,
                relief_station_points,
                access_inward,
                surface,
            )
            self._require_fully_constrained(relief_context.sketch)

        guide_hole = self._guide_hole(connector_type, geometry.guide_thickness)
        guide_context = self._create_sketch(
            component,
            geometry.small_face,
            geometry.edge,
            "Connector (Native) - Opposite Holes",
            "opposite",
        )
        guide_centers = self._add_guide_geometry(
            guide_context,
            access_layout.alignment_points,
            geometry.small_face,
            geometry.edge,
            edge_direction,
            small_face_inward,
            connector_type,
            surface,
            guide_hole,
            additional_boards,
        )
        self._require_fully_constrained(guide_context.sketch)

        collar_context: _SketchContext | None = None
        if (
            guide_hole.collar_diameter is not None
            and guide_hole.collar_diameter_expression is not None
        ):
            collar_context = self._create_sketch(
                component,
                geometry.small_face,
                geometry.edge,
                "Connector (Native) - Insert Collars",
                "collar",
            )
            self._add_projected_circles(
                collar_context,
                guide_centers,
                guide_hole.collar_diameter,
                guide_hole.collar_diameter_expression,
                "collarDiameter",
            )
            self._require_fully_constrained(collar_context.sketch)

        access_thicknesses = [geometry.access_thickness] + [
            board.access_thickness for board in additional_boards
        ]
        board_count = len(access_thicknesses)

        def board_suffix(index: int) -> str:
            return "" if index == 0 else str(index + 1)

        def board_name(base: str, index: int) -> str:
            return (
                base
                if board_count == 1
                else f"{base} (Board {index + 1})"
            )

        last_feature: adsk.fusion.Feature | None = None
        for board_index, access_thickness in enumerate(access_thicknesses):
            access_depth: float | str = (
                (
                    f"({self.inputs.clamex_board_thickness.expression}) / 2"
                    if self.inputs.clamex_board_thickness.expression
                    else access_thickness / 2
                )
                if connector_type.is_clamex
                else 1.1
                if surface == CabineoSurface.FLUSH
                else 1.05
            )
            last_feature = self._create_cut_extrude(
                component=component,
                sketch=access_context.sketch,
                target_body=self._target_body(
                    component,
                    f"access{board_index}",
                ),
                direction=access_cut_direction,
                distance=access_depth,
                name=board_name("Connector (Native) - Access Cut", board_index),
                parameter_role=f"accessDepth{board_suffix(board_index)}",
                start_face=self._start_face(
                    component,
                    f"access{board_index}",
                ),
            )

        if relief_context:
            relief_depth: float | str = (
                0.08
                if surface == CabineoSurface.FLUSH
                else self.inputs.cabineo_anti_break_depth.expression
            )
            for board_index in range(board_count):
                last_feature = self._create_cut_extrude(
                    component=component,
                    sketch=relief_context.sketch,
                    target_body=self._target_body(
                        component,
                        f"access{board_index}",
                    ),
                    direction=access_cut_direction,
                    distance=relief_depth,
                    name=board_name(
                        "Connector (Native) - Access Relief Cut",
                        board_index,
                    ),
                    parameter_role=(
                        f"accessReliefDepth{board_suffix(board_index)}"
                    ),
                    start_face=self._start_face(
                        component,
                        f"access{board_index}",
                    ),
                )

        last_feature = self._create_cut_extrude(
            component=component,
            sketch=guide_context.sketch,
            target_body=self._target_body(component, "guide"),
            direction=opposite_cut_direction,
            distance=guide_hole.depth,
            name="Connector (Native) - Opposite Cut",
            parameter_role="oppositeDepth",
        )

        if collar_context and guide_hole.collar_depth is not None:
            last_feature = self._create_cut_extrude(
                component=component,
                sketch=collar_context.sketch,
                target_body=self._target_body(component, "guide"),
                direction=opposite_cut_direction,
                distance=guide_hole.collar_depth,
                name="Connector (Native) - Insert Collar Cut",
                parameter_role="collarDepth",
            )

        self._group_features(component, access_context.sketch, last_feature)

    def _execute_domino(
        self,
        component: adsk.fusion.Component,
        geometry: _ResolvedGeometry,
        additional_boards: list[_AdditionalBoard],
        positions: list[adsk.core.Point3D],
        edge_direction: adsk.core.Vector3D,
        small_face_inward: adsk.core.Vector3D,
        opposite_cut_direction: adsk.core.Vector3D,
    ) -> None:
        """Domino slots are cut into the adjacent board's face only. The
        mortises in the selected boards' small faces are left to the Domino
        machine; optional V-grooves on the large faces mark their positions.
        """
        size = self._domino_size()
        self._start_face_tokens["guideOpposite"] = (
            utils.brep.get_opposite_face(geometry.guide_face).entityToken
        )

        # The positions get a sketch of their own: the slot and mark
        # sketches then only hold geometry hanging off projected points.
        # Drawn into one sketch, the positions and around twenty slots are
        # more than Fusion's sketch solver resolves.
        position_context = self._create_sketch(
            component,
            geometry.small_face,
            geometry.edge,
            "Connector (Native) - Domino Positions",
            "domino",
        )
        station_points = self._add_station_points(
            position_context,
            geometry.edge,
            positions,
        )
        # Per board, first board first: the stations on the board's own
        # selected edge (the marks are built on these) and the slot centers.
        board_stations: list[list[adsk.fusion.SketchPoint]] = [
            station_points
        ] + [[] for _ in additional_boards]
        board_centers: list[list[adsk.fusion.SketchPoint]]
        fence_distance = self._domino_fence_distance()
        if fence_distance is None:
            centers, cross_lines = self._board_center_points(
                position_context,
                station_points,
                geometry.small_face,
                geometry.edge,
                small_face_inward,
            )
            board_centers = [centers] + [
                self._clamex_guide_centers_for_board(
                    position_context,
                    board,
                    cross_lines,
                    board_stations[board_index],
                )
                for board_index, board in enumerate(additional_boards, start=1)
            ]
        else:
            centers, offset_lines = self._edge_offset_points(
                position_context,
                station_points,
                small_face_inward,
                fence_distance[0],
                fence_distance[1],
                "dominoFenceDistance",
            )
            board_centers = [centers] + [
                self._cabineo_guide_centers_for_board(
                    position_context,
                    board,
                    offset_lines,
                    board_stations[board_index],
                )
                for board_index, board in enumerate(additional_boards, start=1)
            ]
        self._require_fully_constrained(position_context.sketch)

        slot_context = self._create_sketch(
            component,
            geometry.small_face,
            geometry.edge,
            "Connector (Native) - Domino Slots",
            "dominoSlot",
        )
        self._add_domino_slots(
            slot_context,
            self._project_points(
                slot_context.sketch,
                [center for centers in board_centers for center in centers],
                "Domino slot centers",
            ),
            len(station_points),
            edge_direction,
            size,
        )
        self._require_fully_constrained(slot_context.sketch)

        mark_context: _SketchContext | None = None
        marked_stations = [
            self._domino_marked_stations(stations)
            for stations in board_stations
        ]
        if marked_stations[0]:
            mark_context = self._create_sketch(
                component,
                geometry.small_face,
                geometry.edge,
                "Connector (Native) - Domino Marks",
                "dominoMark",
            )
            self._add_domino_marks(
                mark_context,
                marked_stations,
                edge_direction,
                [geometry.edge] + [board.edge for board in additional_boards],
                [small_face_inward]
                + [
                    utils.brep.normal_into_face(board.edge, board.small_face)
                    for board in additional_boards
                ],
            )
            self._require_fully_constrained(mark_context.sketch)

        last_feature: adsk.fusion.Feature
        if (
            DominoDepthMode(self.inputs.domino_depth_mode.value)
            == DominoDepthMode.MATERIAL_REMAINING
        ):
            # Cut up to the adjacent board's far face, so the remaining
            # material survives a change of that board's thickness.
            last_feature = self._create_cut_extrude_to_face(
                component=component,
                sketch=slot_context.sketch,
                target_body=self._target_body(component, "guide"),
                target_face=self._start_face(component, "guideOpposite"),
                direction=opposite_cut_direction,
                offset=self.inputs.domino_material_remaining.expression,
                name="Connector (Native) - Domino Slot Cut",
                parameter_role="dominoSlotRemaining",
            )
        else:
            last_feature = self._create_cut_extrude(
                component=component,
                sketch=slot_context.sketch,
                target_body=self._target_body(component, "guide"),
                direction=opposite_cut_direction,
                distance=(
                    f"{size.length / 2:g} mm + "
                    f"({self.inputs.domino_depth_offset.expression})"
                ),
                name="Connector (Native) - Domino Slot Cut",
                parameter_role="dominoSlotDepth",
            )

        if mark_context:
            last_feature = self._create_cut_extrude(
                component=component,
                sketch=mark_context.sketch,
                target_body=[
                    self._target_body(component, f"access{board_index}")
                    for board_index in range(len(additional_boards) + 1)
                ],
                direction=self._opposite(opposite_cut_direction),
                distance=self.inputs.domino_mark_length.expression,
                name="Connector (Native) - Domino Mark Cut",
                parameter_role="dominoMarkLength",
            )

        # No cut is made from the positions sketch, so nothing has hidden it.
        position_context.sketch.isVisible = False
        self._group_features(component, position_context.sketch, last_feature)

    def _domino_size(self) -> _DominoSize:
        value = self.inputs.domino_size.value
        size = next(
            (size for size in _DOMINO_SIZES if size.value == value),
            None,
        )
        if not size:
            raise ValueError("Select a Domino size.")
        return size

    def _domino_slot_height(self, size: _DominoSize) -> float:
        return size.thickness / 10 + self.inputs.domino_height_offset.value

    def _domino_slot_length(self, size: _DominoSize) -> float:
        return size.width / 10 + self.inputs.domino_length_offset.value

    def _domino_loose_slot_extra(self) -> tuple[float, str] | None:
        """Extra length of the loose slots as value and expression, or None
        when every slot is cut to the exact size."""
        mode = DominoLooseSlots(self.inputs.domino_loose_slots.value)
        if mode == DominoLooseSlots.NONE:
            return None
        if mode == DominoLooseSlots.CUSTOM:
            return (
                self.inputs.domino_loose_slot_extra.value,
                self.inputs.domino_loose_slot_extra.expression,
            )
        return mode.value / 10, f"{mode.value} mm"

    def _domino_fence_distance(self) -> tuple[float, str] | None:
        """Distance from the selected edge's large face to the slot centers,
        as value and expression. None centers the slots on each board."""
        value = self.inputs.domino_fence_height.value
        if value == _DOMINO_FENCE_CENTERED:
            return None
        if value == _DOMINO_FENCE_CUSTOM:
            return (
                self.inputs.domino_fence_distance.value,
                self.inputs.domino_fence_distance.expression,
            )
        stop = next(
            (stop for stop in _DOMINO_FENCE_STOPS if stop.value == value),
            None,
        )
        if not stop:
            raise ValueError("Select a Fence Height.")
        return stop.thickness / 20, f"{stop.thickness / 2:g} mm"

    def _domino_marked_stations(
        self,
        station_points: list[adsk.fusion.SketchPoint],
    ) -> list[adsk.fusion.SketchPoint]:
        marks = DominoMarks(self.inputs.domino_marks.value)
        if marks == DominoMarks.NONE:
            return []
        # A single connector is centered on the edge, out of reach of the
        # machine's end stops, so it always keeps its mark.
        if marks == DominoMarks.SKIP_FIRST_AND_LAST and len(station_points) > 1:
            return station_points[1:-1]
        return list(station_points)

    def _add_domino_slots(
        self,
        context: _SketchContext,
        centers: list[adsk.fusion.SketchPoint],
        station_count: int,
        edge_direction: adsk.core.Vector3D,
        size: _DominoSize,
    ) -> None:
        """`centers` holds `station_count` slot centers per board, each
        board's in the same order along the edge."""
        sketch = context.sketch
        constraints = sketch.geometricConstraints
        height = self._domino_slot_height(size)
        exact_span = self._domino_slot_length(size) - height
        loose_extra = self._domino_loose_slot_extra()
        exact_station = (
            station_count - 1
            if self.inputs.domino_exact_slot_last.value
            else 0
        )
        height_expression = (
            f"{size.thickness:g} mm + "
            f"({self.inputs.domino_height_offset.expression})"
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
            width_dimension, centerline = self._add_center_to_center_slot(
                sketch,
                sketch.modelToSketchSpace(
                    self._translated(center_model, edge_direction, -span / 2)
                ),
                sketch.modelToSketchSpace(
                    self._translated(center_model, edge_direction, span / 2)
                ),
                (
                    height_expression
                    if first_width_parameter is None
                    else first_width_parameter.name
                ),
                f"dominoSlot{index + 1}Height",
            )
            constraints.addParallel(centerline, context.edge_line)
            constraints.addMidPoint(center, centerline)
            if first_width_parameter is None:
                first_width_parameter = width_dimension.parameter
            if not is_loose and exact_reference is None:
                # The slot's overall length is the Domino's width: the
                # center-to-center span is that minus the slot's own height.
                exact_span_parameter = self._add_distance_dimension(
                    sketch,
                    centerline.startSketchPoint,
                    centerline.endSketchPoint,
                    (
                        f"{size.width:g} mm + "
                        f"({self.inputs.domino_length_offset.expression})"
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
                self._add_distance_dimension(
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

    def _add_domino_marks(
        self,
        context: _SketchContext,
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
        depth = self.inputs.domino_mark_depth.value
        # Every board's stations are projected from the positions sketch, so
        # all grooves are built the same way on points that follow that
        # sketch.
        projected = self._project_points(
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
                else self._project_reference_line(
                    sketch,
                    edge,
                    "additional board edge",
                )
            )
            for station in stations:
                depth_line = lines.addByTwoPoints(
                    station,
                    sketch.modelToSketchSpace(
                        self._translated(station.worldGeometry, inward, depth)
                    ),
                )
                if not depth_line:
                    raise RuntimeError(
                        "Fusion failed to create a Domino mark depth line."
                    )
                depth_line.isConstruction = True
                constraints.addPerpendicular(depth_line, edge_line)
                if reference_depth_line is None:
                    self._add_distance_dimension(
                        sketch,
                        depth_line.startSketchPoint,
                        depth_line.endSketchPoint,
                        self.inputs.domino_mark_depth.expression,
                        "dominoMarkDepth",
                    )
                    reference_depth_line = depth_line
                else:
                    constraints.addEqual(reference_depth_line, depth_line)
                flanks = self._add_domino_mark_groove(
                    sketch,
                    depth_line,
                    edge_line,
                    edge_direction,
                    depth,
                    reference_flanks,
                )
                if reference_flanks is None:
                    reference_flanks = flanks

    def _add_domino_mark_groove(
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
                self._translated(top_model, edge_direction, -depth)
            ),
            sketch.modelToSketchSpace(
                self._translated(top_model, edge_direction, depth)
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

    def _validation_error(self) -> str | None:
        design = adsk.fusion.Design.cast(self.app.activeProduct)
        if not design:
            return "An active Fusion design is required."
        if design.designType != adsk.fusion.DesignTypes.ParametricDesignType:  # type: ignore
            return "Connector (Native) requires Design History (a parametric design)."
        if not self.inputs or len(self.inputs.edge.value) < 1:
            return "Select at least one straight edge."

        for edge_index, selected in enumerate(
            self.inputs.edge.value,
            start=1,
        ):
            selected_edge = adsk.fusion.BRepEdge.cast(selected)
            if not selected_edge or not utils.brep.is_linear(selected_edge):
                return (
                    f"Selected edge {edge_index} must be a straight BRep "
                    "edge."
                )
            if not selected_edge.body.isSolid:
                return (
                    f"Selected edge {edge_index} must belong to a solid "
                    "body."
                )
            if selected_edge.faces.count != 2 or not all(
                utils.brep.is_planar(face) for face in selected_edge.faces
            ):
                return (
                    f"Selected edge {edge_index} must join two planar faces."
                )

        try:
            geometry = self._resolve_geometry()
        except Exception as exc:
            return str(exc)

        if geometry.edge.body.parentComponent != design.activeComponent:
            return (
                "Activate the component that owns the selected edge, then run "
                "Connector (Native) again."
            )
        if geometry.guide_face.body.parentComponent != design.activeComponent:
            return (
                "This first Connector (Native) version requires both board bodies in "
                "the active component."
            )
        if geometry.access_face.body == geometry.guide_face.body:
            return "The adjacent holes must be cut into a second solid body."

        positioning = PositioningMode(self.inputs.positioning.value)
        if positioning == PositioningMode.CUSTOM_POINTS:
            if not self.inputs.points.value:
                return "Select at least one Custom Point."
            try:
                positions = self._custom_point_positions(geometry.edge)
            except Exception as exc:
                return str(exc)
            direction = utils.brep.normal_along_edge(geometry.edge)
            start = geometry.edge.startVertex.geometry
            distances = [
                start.vectorTo(position).dotProduct(direction)
                for position in positions
            ]
            tolerance = self.app.pointTolerance * 10
            if any(
                distance < -tolerance
                or distance > geometry.edge.length + tolerance
                for distance in distances
            ):
                return (
                    "Every Custom Point must project within the selected edge."
                )
            if any(
                second - first <= tolerance
                for first, second in zip(distances, distances[1:])
            ):
                return (
                    "Custom Points must project to distinct positions along "
                    "the selected edge."
                )
        else:
            end_offset, _ = self._end_offset()
            if end_offset < 0:
                return "End Offset cannot be negative."
            if (
                self.inputs.number_of_connectors.value > 1
                and 2 * end_offset >= geometry.edge.length - 1e-6
            ):
                return (
                    "End Offset must leave positive spacing between the first "
                    "and last connector."
                )

        try:
            additional_boards = self._resolve_additional_boards(geometry)
        except Exception as exc:
            return str(exc)
        if additional_boards:
            small_plane = adsk.core.Plane.cast(geometry.small_face.geometry)
            if not small_plane:
                return "The first edge's small face must be planar."
            seen_bodies = [geometry.access_face.body]
            for board in additional_boards:
                if not utils.brep.is_parallel(board.edge, geometry.edge):
                    return "All selected edges must be parallel."
                if any(board.edge.body == body for body in seen_bodies):
                    return "Each selected edge must lie on a different body."
                seen_bodies.append(board.edge.body)
                if board.edge.body == geometry.guide_face.body:
                    return (
                        "The adjacent holes must be cut into a second solid "
                        "body."
                    )
                if (
                    board.edge.body.parentComponent
                    != design.activeComponent
                ):
                    return (
                        "Activate the component that owns all selected "
                        "edges, then run Connector (Native) again."
                    )
                for vertex in (
                    board.edge.startVertex,
                    board.edge.endVertex,
                ):
                    delta = small_plane.origin.vectorTo(vertex.geometry)
                    if (
                        abs(delta.dotProduct(small_plane.normal))
                        > self.app.pointTolerance * 100
                    ):
                        return (
                            "Every selected edge must lie in the plane of "
                            "the first edge's small face."
                        )
            try:
                positions = self._connector_positions(geometry.edge)
            except Exception as exc:
                return str(exc)
            span_tolerance = self.app.pointTolerance * 10
            for board in additional_boards:
                board_direction = utils.brep.normal_along_edge(board.edge)
                board_start = board.edge.startVertex.geometry
                for position in positions:
                    projected = utils.brep.project_point_onto_edge(
                        position,
                        board.edge,
                    )
                    distance = board_start.vectorTo(projected).dotProduct(
                        board_direction
                    )
                    if (
                        distance < -span_tolerance
                        or distance > board.edge.length + span_tolerance
                    ):
                        return (
                            "Every connector position must lie within every "
                            "selected edge."
                        )

        connector_type = ConnectorType(self.inputs.size.value)
        surface = CabineoSurface(self.inputs.cabineo_surface.value)
        if connector_type.is_domino:
            return self._domino_validation_error(geometry, additional_boards)
        if connector_type.is_clamex:
            if self.inputs.clamex_guide_hole_diameter.value <= 0:
                return "Guide Hole Diameter must be greater than zero."
            if self.inputs.clamex_board_thickness.validation_error:
                return self.inputs.clamex_board_thickness.validation_error
            if (
                self.inputs.clamex_board_thickness.value is not None
                and self.inputs.clamex_board_thickness.value <= 0
            ):
                return "Board Thickness must be greater than zero."
        if (
            connector_type.is_cabineo
            and surface == CabineoSurface.ANTI_BREAK
            and self.inputs.cabineo_anti_break_depth.value <= 0
        ):
            return "Anti-Break Depth must be greater than zero."
        if self.inputs.cabineo_anti_break_distance.value < 0:
            return "Anti-Break Distance cannot be negative."

        if (
            connector_type == ConnectorType.CABINEO_8_M6
            and self.inputs.cabineo_insert_type.value
            == CabineoInsert.THREADED_INSERT.value
        ):
            values = [
                (
                    self.inputs.threaded_insert_core_diameter.value,
                    "Core Diameter",
                ),
                (self.inputs.threaded_insert_core_depth.value, "Core Depth"),
                (
                    self.inputs.threaded_insert_collar_diameter.value,
                    "Collar Diameter",
                ),
                (
                    self.inputs.threaded_insert_collar_depth.value,
                    "Collar Depth",
                ),
            ]
            for value, name in values:
                if value <= 0:
                    return f"{name} must be greater than zero."
            if (
                self.inputs.threaded_insert_collar_diameter.value
                < self.inputs.threaded_insert_core_diameter.value
            ):
                return "Collar Diameter cannot be smaller than Core Diameter."
        return None

    def _domino_validation_error(
        self,
        geometry: _ResolvedGeometry,
        additional_boards: list[_AdditionalBoard],
    ) -> str | None:
        try:
            size = self._domino_size()
        except Exception as exc:
            return str(exc)
        tolerance = self.app.pointTolerance * 10
        access_thickness = min(
            [geometry.access_thickness]
            + [board.access_thickness for board in additional_boards]
        )
        height = self._domino_slot_height(size)
        if height <= tolerance:
            return "Slot Height Offset must leave a positive slot height."
        if self._domino_slot_length(size) - height <= tolerance:
            return (
                "Slot Length Offset must leave the slot longer than it is "
                "high."
            )
        if height >= access_thickness - tolerance:
            return "The Domino slot is higher than the selected board is thick."
        try:
            fence_distance = self._domino_fence_distance()
        except Exception as exc:
            return str(exc)
        if fence_distance is not None and (
            fence_distance[0] - height / 2 < -tolerance
            or fence_distance[0] + height / 2 > access_thickness + tolerance
        ):
            return (
                "At this Fence Height the Domino slot does not fit within "
                "the selected board's thickness."
            )

        if (
            DominoDepthMode(self.inputs.domino_depth_mode.value)
            == DominoDepthMode.MATERIAL_REMAINING
        ):
            remaining = self.inputs.domino_material_remaining.value
            if remaining < 0:
                return "Material Remaining cannot be negative."
            if remaining >= geometry.guide_thickness - tolerance:
                return (
                    "Material Remaining must be less than the adjacent "
                    "board's thickness."
                )
        else:
            depth = size.length / 20 + self.inputs.domino_depth_offset.value
            if depth <= tolerance:
                return "Depth Offset must leave a positive slot depth."
            if depth >= geometry.guide_thickness - tolerance:
                return (
                    "The Domino slot is deeper than the adjacent board is "
                    "thick. Pick a shorter Domino or set Slot Depth to "
                    "Material Remaining."
                )

        loose_extra = self._domino_loose_slot_extra()
        if loose_extra is not None and loose_extra[0] <= 0:
            return "Loose Slot Extra Length must be greater than zero."

        if DominoMarks(self.inputs.domino_marks.value) != DominoMarks.NONE:
            if self.inputs.domino_mark_depth.value <= 0:
                return "Mark Depth must be greater than zero."
            if self.inputs.domino_mark_length.value <= 0:
                return "Mark Length must be greater than zero."
            if (
                self.inputs.domino_mark_depth.value
                >= access_thickness - tolerance
            ):
                return "Mark Depth must be less than the board's thickness."
        return None

    def _resolve_additional_boards(
        self,
        first: _ResolvedGeometry,
    ) -> list[_AdditionalBoard]:
        boards: list[_AdditionalBoard] = []
        first_normal = utils.brep.normal_away_from_body(first.access_face)
        for selected in self.inputs.edge.value[1:]:
            proxy = adsk.fusion.BRepEdge.cast(selected)
            if not proxy:
                raise ValueError("Every selection must be a straight edge.")
            edge = cast(adsk.fusion.BRepEdge, proxy.nativeObject or proxy)
            access_face: adsk.fusion.BRepFace | None = None
            small_face: adsk.fusion.BRepFace | None = None
            for face in edge.faces:
                if not utils.brep.is_planar(face):
                    raise ValueError(
                        "Every selected edge must join two planar faces."
                    )
                normal = utils.brep.normal_away_from_body(face)
                if normal.dotProduct(first_normal) > 1 - 1e-6:
                    access_face = face
                else:
                    small_face = face
            if not access_face or not small_face:
                raise ValueError(
                    "Each additional edge must border a face oriented like "
                    "the first edge's large face."
                )
            boards.append(
                _AdditionalBoard(
                    edge=edge,
                    access_face=access_face,
                    small_face=small_face,
                    access_thickness=utils.brep.get_board_thickness(
                        access_face
                    ),
                )
            )
        return boards

    def _resolve_geometry(self) -> _ResolvedGeometry:
        selected = cast(adsk.fusion.BRepEdge, self.inputs.edge.value[0])
        edge = cast(adsk.fusion.BRepEdge, selected.nativeObject or selected)
        faces = utils.brep.find_mating_faces_at_edge(edge)
        if not faces:
            raise ValueError(
                "Could not find a second board face mating with the selected edge."
            )
        access_face, small_face, _ = faces
        access_face = cast(
            adsk.fusion.BRepFace,
            access_face.nativeObject or access_face,
        )
        small_face = cast(
            adsk.fusion.BRepFace,
            small_face.nativeObject or small_face,
        )
        guide_face = self._adjacent_guide_face(
            edge,
            access_face,
            small_face,
        )
        return _ResolvedGeometry(
            edge=edge,
            access_face=access_face,
            small_face=small_face,
            guide_face=guide_face,
            access_thickness=utils.brep.get_board_thickness(access_face),
            guide_thickness=utils.brep.get_board_thickness(guide_face),
        )

    def _adjacent_guide_face(
        self,
        edge: adsk.fusion.BRepEdge,
        access_face: adsk.fusion.BRepFace,
        small_face: adsk.fusion.BRepFace,
    ) -> adsk.fusion.BRepFace:
        # Probe along the whole edge rather than at its midpoint alone. The
        # guide board can meet just part of the edge, and a single probe
        # misses it whenever that part does not cover the middle.
        test_points = utils.brep.sample_points_along_edge(
            edge,
            offset=utils.vector.scaled_by(
                utils.brep.normal_into_face(edge, small_face),
                0.1,
            ),
        )
        # Exclude every selected edge's body: the guide board is the one
        # the selected boards are mounted against.
        excluded_bodies = [access_face.body]
        for selected in self.inputs.edge.value:
            proxy = adsk.fusion.BRepEdge.cast(selected)
            if proxy:
                native = cast(
                    adsk.fusion.BRepEdge,
                    proxy.nativeObject or proxy,
                )
                excluded_bodies.append(native.body)
        candidates: list[tuple[int, float, adsk.fusion.BRepFace]] = []
        component = access_face.body.parentComponent
        for body in component.bRepBodies:
            if any(body == excluded for excluded in excluded_bodies):
                continue
            # A body whose bounding box misses the edge cannot hold a face
            # running along it, and rejecting it here avoids reading the
            # geometry of every one of its faces.
            if not utils.brep.bounding_boxes_overlap(
                body.boundingBox,
                edge.boundingBox,
                utils.brep.PROBE_PROXIMITY,
            ):
                continue
            for face in body.faces:
                # face_contains_edge is bounding-box gated, so it throws out
                # nearly every face before anything probes the points.
                if not (
                    utils.brep.is_planar(face)
                    and utils.brep.is_perpendicular(face, access_face)
                    and utils.brep.face_contains_edge(face, edge)
                ):
                    continue
                contact = sum(
                    1
                    for point in test_points
                    if face.isPointOnFace(point, 1e-6)
                )
                if contact:
                    candidates.append((contact, face.area, face))
        if not candidates:
            raise ValueError(
                "Could not find an adjacent board face along the selected edge."
            )
        # Whichever face runs along the most of the edge is the board the
        # selection is mounted against; area only breaks ties.
        candidates.sort(key=lambda c: (c[0], c[1]), reverse=True)
        return candidates[0][2]

    def _connector_positions(
        self,
        edge: adsk.fusion.BRepEdge,
    ) -> list[adsk.core.Point3D]:
        if (
            PositioningMode(self.inputs.positioning.value)
            == PositioningMode.CUSTOM_POINTS
        ):
            return self._custom_point_positions(edge)

        count = self.inputs.number_of_connectors.value
        direction = utils.brep.normal_along_edge(edge)
        if count == 1:
            distances = [edge.length / 2]
        else:
            end_offset, _ = self._end_offset()
            available = edge.length - 2 * end_offset
            spacing = available / (count - 1)
            distances = [
                end_offset + index * spacing
                for index in range(count)
            ]
        return [
            self._translated(edge.startVertex.geometry, direction, distance)
            for distance in distances
        ]

    def _end_offset(self) -> tuple[float, str]:
        """Distance from the edge ends to the first and last connector, as
        value and expression. Dominos can take it from the machine's stops
        instead of the End Offset input."""
        if ConnectorType(self.inputs.size.value).is_domino:
            stop = DominoEndStop(self.inputs.domino_end_stop.value)
            if stop != DominoEndStop.CUSTOM:
                return stop.value / 10, f"{stop.value} mm"
        return self.inputs.offset.value, self.inputs.offset.expression

    def _custom_point_positions(
        self,
        edge: adsk.fusion.BRepEdge,
    ) -> list[adsk.core.Point3D]:
        positions = [
            utils.brep.project_point_onto_edge(
                self._point_geometry(point),
                edge,
            )
            for point in self.inputs.points.value
        ]
        direction = utils.brep.normal_along_edge(edge)
        start = edge.startVertex.geometry
        positions.sort(
            key=lambda point: start.vectorTo(point).dotProduct(direction)
        )
        return positions

    def _sorted_custom_points(
        self,
        edge: adsk.fusion.BRepEdge,
    ) -> list[adsk.core.Base]:
        direction = utils.brep.normal_along_edge(edge)
        start = edge.startVertex.geometry
        points = [
            cast(adsk.core.Base, point)
            for point in self.inputs.points.value
        ]
        points.sort(
            key=lambda point: start.vectorTo(
                utils.brep.project_point_onto_edge(
                    self._point_geometry(point),
                    edge,
                )
            ).dotProduct(direction)
        )
        return points

    def _create_sketch(
        self,
        component: adsk.fusion.Component,
        face: adsk.fusion.BRepFace,
        edge: adsk.fusion.BRepEdge,
        name: str,
        parameter_role: str,
    ) -> _SketchContext:
        sketch = component.sketches.addWithoutEdges(face)
        if not sketch:
            raise RuntimeError(f"Fusion failed to create '{name}'.")
        sketch.name = name
        edge_line = self._project_single_line(
            sketch,
            edge,
            f"selected edge into '{name}'",
        )
        edge_line.isConstruction = True
        start_vertex = edge.startVertex.geometry
        edge_start = min(
            (edge_line.startSketchPoint, edge_line.endSketchPoint),
            key=lambda point: point.worldGeometry.distanceTo(start_vertex),
        )
        edge_end = (
            edge_line.endSketchPoint
            if edge_start == edge_line.startSketchPoint
            else edge_line.startSketchPoint
        )
        # Defer the sketch solve while the connector geometry is added: in
        # large documents every individual sketch mutation otherwise pays a
        # full document-transaction cost (~80-560 ms each measured). Deferring
        # must start only after project2 (it throws InternalValidationError on
        # a deferred sketch). The sketch is re-solved in
        # _require_fully_constrained, which every build path calls before the
        # sketch is read again; a fully constrained sketch solves to the same
        # geometry either way.
        sketch.isComputeDeferred = True
        return _SketchContext(
            sketch=sketch,
            edge_line=edge_line,
            edge_start=edge_start,
            edge_end=edge_end,
            parameter_role=parameter_role,
        )

    def _add_access_geometry(
        self,
        context: _SketchContext,
        positions: list[adsk.core.Point3D],
        inward: adsk.core.Vector3D,
        connector_type: ConnectorType,
        edge: adsk.fusion.BRepEdge,
    ) -> _AccessLayout:
        position_points = self._add_station_points(
            context,
            edge,
            positions,
        )
        if connector_type == ConnectorType.CLAMEX_P14:
            centers = self._add_normal_points(
                context,
                position_points,
                inward,
                [0.75],
                ["0.75 cm"],
                "HoleInset",
            )
            circles = self._add_equal_circles(
                context.sketch,
                centers,
                0.6 / 2,
                "0.6 cm",
                "accessHoleDiameter",
            )
            return _AccessLayout(
                station_points=position_points,
                alignment_points=[
                    circle.centerSketchPoint for circle in circles
                ],
            )

        if connector_type == ConnectorType.CLAMEX_P10:
            centers = self._add_normal_points(
                context,
                position_points,
                inward,
                [0.5, 0.75],
                ["0.5 cm", "0.75 cm"],
                "SlotCenter",
            )
            alignment_points: list[adsk.fusion.SketchPoint] = []
            first_width_parameter: adsk.fusion.ModelParameter | None = None
            for index in range(0, len(centers), 2):
                width_expression = (
                    "0.6 cm"
                    if first_width_parameter is None
                    else first_width_parameter.name
                )
                width_dimension, centerline = self._add_center_to_center_slot(
                    context.sketch,
                    centers[index],
                    centers[index + 1],
                    width_expression,
                    f"accessSlot{index // 2 + 1}Width",
                )
                if first_width_parameter is None:
                    first_width_parameter = width_dimension.parameter
                start = centerline.startSketchPoint.geometry
                end = centerline.endSketchPoint.geometry
                midpoint = context.sketch.sketchPoints.add(
                    adsk.core.Point3D.create(
                        (start.x + end.x) / 2,
                        (start.y + end.y) / 2,
                        0,
                    )
                )
                if not midpoint:
                    raise RuntimeError(
                        "Fusion failed to create a P10 slot midpoint."
                    )
                context.sketch.geometricConstraints.addMidPoint(
                    midpoint,
                    centerline,
                )
                alignment_points.append(midpoint)
            return _AccessLayout(
                station_points=position_points,
                alignment_points=alignment_points,
            )

        centers = self._add_normal_points(
            context,
            position_points,
            inward,
            [0.36, 1.48, 2.6],
            ["0.36 cm", "1.48 cm", "2.6 cm"],
            "HoleInset",
        )
        circles = self._add_equal_circles(
            context.sketch,
            centers,
            1.5 / 2,
            "1.5 cm",
            "accessHoleDiameter",
        )
        return _AccessLayout(
            station_points=position_points,
            alignment_points=[
                circles[index].centerSketchPoint
                for index in range(1, len(circles), 3)
            ],
        )

    def _add_access_relief_geometry(
        self,
        context: _SketchContext,
        position_points: list[adsk.fusion.SketchPoint],
        inward: adsk.core.Vector3D,
        surface: CabineoSurface,
    ) -> None:
        if surface == CabineoSurface.ANTI_BREAK:
            centers = self._add_normal_points(
                context,
                position_points,
                inward,
                [0.36, 1.48, 2.6],
                ["0.36 cm", "1.48 cm", "2.6 cm"],
                "HoleInset",
            )
            self._add_equal_circles(
                context.sketch,
                centers,
                1.5 / 2 + self.inputs.cabineo_anti_break_distance.value,
                (
                    "1.5 cm + 2 * "
                    f"({self.inputs.cabineo_anti_break_distance.expression})"
                ),
                "accessReliefDiameter",
            )
            return

        top_centers = self._add_normal_points(
            context,
            position_points,
            inward,
            [2.6],
            ["2.6 cm"],
            "SlotCenter",
        )
        first_width_parameter: adsk.fusion.ModelParameter | None = None
        for index, (bottom, top) in enumerate(
            zip(position_points, top_centers)
        ):
            width_expression = (
                "1.67 cm"
                if first_width_parameter is None
                else first_width_parameter.name
            )
            width_dimension, _ = self._add_center_to_center_slot(
                context.sketch,
                bottom,
                top,
                width_expression,
                f"accessReliefSlot{index + 1}Width",
            )
            if first_width_parameter is None:
                first_width_parameter = width_dimension.parameter

    def _add_guide_geometry(
        self,
        context: _SketchContext,
        alignment_points: list[adsk.fusion.SketchPoint],
        small_face: adsk.fusion.BRepFace,
        edge: adsk.fusion.BRepEdge,
        edge_direction: adsk.core.Vector3D,
        inward: adsk.core.Vector3D,
        connector_type: ConnectorType,
        surface: CabineoSurface,
        guide_hole: _GuideHole,
        additional_boards: list[_AdditionalBoard],
    ) -> list[adsk.fusion.SketchPoint]:
        if connector_type.is_clamex:
            centerline_points, reference_cross_lines = (
                self._clamex_guide_center_points(
                    context,
                    alignment_points,
                    small_face,
                    edge,
                    inward,
                )
            )
            for board in additional_boards:
                centerline_points.extend(
                    self._clamex_guide_centers_for_board(
                        context,
                        board,
                        reference_cross_lines,
                    )
                )
            centers: list[adsk.fusion.SketchPoint] = []
            lines = context.sketch.sketchCurves.sketchLines
            constraints = context.sketch.geometricConstraints
            reference_centerline: adsk.fusion.SketchLine | None = None
            for center in centerline_points:
                center_model = center.worldGeometry
                first_model = self._translated(
                    center_model,
                    edge_direction,
                    -10.1 / 2,
                )
                second_model = self._translated(
                    center_model,
                    edge_direction,
                    10.1 / 2,
                )
                centerline = lines.addByTwoPoints(
                    context.sketch.modelToSketchSpace(first_model),
                    context.sketch.modelToSketchSpace(second_model),
                )
                if not centerline:
                    raise RuntimeError(
                        "Fusion failed to create a Clamex guide centerline."
                    )
                centerline.isConstruction = True
                constraints.addParallel(centerline, context.edge_line)
                constraints.addMidPoint(center, centerline)
                if reference_centerline is None:
                    self._add_distance_dimension(
                        context.sketch,
                        centerline.startSketchPoint,
                        centerline.endSketchPoint,
                        "10.1 cm",
                        "guidePairSpacing",
                    )
                    reference_centerline = centerline
                else:
                    constraints.addEqual(reference_centerline, centerline)
                centers.extend(
                    [
                        centerline.startSketchPoint,
                        centerline.endSketchPoint,
                    ]
                )
            self._add_equal_circles(
                context.sketch,
                centers,
                guide_hole.diameter / 2,
                guide_hole.diameter_expression,
                "guideHoleDiameter",
            )
            return centers

        centerline_points, reference_offset_lines = (
            self._cabineo_guide_center_points(
                context,
                alignment_points,
                inward,
                surface,
            )
        )
        for board in additional_boards:
            centerline_points.extend(
                self._cabineo_guide_centers_for_board(
                    context,
                    board,
                    reference_offset_lines,
                )
            )
        self._add_equal_circles(
            context.sketch,
            centerline_points,
            guide_hole.diameter / 2,
            guide_hole.diameter_expression,
            "guideHoleDiameter",
        )
        return centerline_points

    def _add_projected_circles(
        self,
        context: _SketchContext,
        source_points: list[adsk.fusion.SketchPoint],
        diameter: float,
        diameter_expression: str,
        parameter_role: str,
    ) -> list[adsk.fusion.SketchPoint]:
        centers = self._project_points(
            context.sketch,
            source_points,
            "guide-hole centers",
        )
        self._add_equal_circles(
            context.sketch,
            centers,
            diameter / 2,
            diameter_expression,
            parameter_role,
        )
        return centers

    def _clamex_guide_center_points(
        self,
        context: _SketchContext,
        alignment_points: list[adsk.fusion.SketchPoint],
        small_face: adsk.fusion.BRepFace,
        edge: adsk.fusion.BRepEdge,
        inward: adsk.core.Vector3D,
    ) -> tuple[
        list[adsk.fusion.SketchPoint],
        list[adsk.fusion.SketchLine],
    ]:
        projected_points = self._project_points(
            context.sketch,
            alignment_points,
            "access-hole midpoints",
        )
        return self._board_center_points(
            context,
            projected_points,
            small_face,
            edge,
            inward,
        )

    def _board_center_points(
        self,
        context: _SketchContext,
        base_points: list[adsk.fusion.SketchPoint],
        small_face: adsk.fusion.BRepFace,
        edge: adsk.fusion.BRepEdge,
        inward: adsk.core.Vector3D,
    ) -> tuple[
        list[adsk.fusion.SketchPoint],
        list[adsk.fusion.SketchLine],
    ]:
        """Centers `base_points` (points of this sketch on the selected
        edge) on the board's thickness. Returns the centers and the
        construction lines that span the small face at each station."""
        opposite_edge = self._project_opposite_edge(
            context.sketch,
            small_face,
            edge,
        )
        lines = context.sketch.sketchCurves.sketchLines
        constraints = context.sketch.geometricConstraints
        centers: list[adsk.fusion.SketchPoint] = []
        cross_lines: list[adsk.fusion.SketchLine] = []
        for base_point in base_points:
            initial_end = self._translated(
                base_point.worldGeometry,
                inward,
                1,
            )
            cross_line = lines.addByTwoPoints(
                base_point,
                context.sketch.modelToSketchSpace(initial_end),
            )
            if not cross_line:
                raise RuntimeError(
                    "Fusion failed to create a board-center construction line."
                )
            cross_line.isConstruction = True
            constraints.addPerpendicular(cross_line, context.edge_line)
            constraints.addCoincident(
                cross_line.endSketchPoint,
                opposite_edge,
            )
            start = cross_line.startSketchPoint.geometry
            end = cross_line.endSketchPoint.geometry
            midpoint = context.sketch.sketchPoints.add(
                adsk.core.Point3D.create(
                    (start.x + end.x) / 2,
                    (start.y + end.y) / 2,
                    0,
                )
            )
            if not midpoint:
                raise RuntimeError(
                    "Fusion failed to create a board-center midpoint."
                )
            constraints.addMidPoint(midpoint, cross_line)
            centers.append(midpoint)
            cross_lines.append(cross_line)
        return centers, cross_lines

    def _clamex_guide_centers_for_board(
        self,
        context: _SketchContext,
        board: _AdditionalBoard,
        reference_cross_lines: list[adsk.fusion.SketchLine],
        stations: list[adsk.fusion.SketchPoint] | None = None,
    ) -> list[adsk.fusion.SketchPoint]:
        """Returns the board's hole centers. When `stations` is given, the
        points where each station meets the board's edge are appended to
        it."""
        sketch = context.sketch
        lines = sketch.sketchCurves.sketchLines
        constraints = sketch.geometricConstraints
        board_edge_line = self._project_reference_line(
            sketch,
            board.edge,
            "additional board edge",
        )
        opposite_edge = self._project_opposite_edge(
            sketch,
            board.small_face,
            board.edge,
        )
        inward = utils.brep.normal_into_face(board.edge, board.small_face)
        centers: list[adsk.fusion.SketchPoint] = []
        for reference in reference_cross_lines:
            # Same station as the first board's cross line, spanning this
            # board's own small face so the holes stay centered on its
            # thickness. Collinearity with the reference line carries the
            # along-edge position without a fixed dimension.
            start_model = utils.brep.project_point_onto_edge(
                reference.startSketchPoint.worldGeometry,
                board.edge,
            )
            end_model = self._translated(
                start_model,
                inward,
                board.access_thickness,
            )
            cross_line = lines.addByTwoPoints(
                sketch.modelToSketchSpace(start_model),
                sketch.modelToSketchSpace(end_model),
            )
            if not cross_line:
                raise RuntimeError(
                    "Fusion failed to create a board-center construction line."
                )
            cross_line.isConstruction = True
            constraints.addCoincident(
                cross_line.startSketchPoint,
                board_edge_line,
            )
            constraints.addCoincident(
                cross_line.endSketchPoint,
                opposite_edge,
            )
            constraints.addCollinear(cross_line, reference)
            start = cross_line.startSketchPoint.geometry
            end = cross_line.endSketchPoint.geometry
            midpoint = sketch.sketchPoints.add(
                adsk.core.Point3D.create(
                    (start.x + end.x) / 2,
                    (start.y + end.y) / 2,
                    0,
                )
            )
            if not midpoint:
                raise RuntimeError(
                    "Fusion failed to create a board-center midpoint."
                )
            constraints.addMidPoint(midpoint, cross_line)
            centers.append(midpoint)
            if stations is not None:
                stations.append(cross_line.startSketchPoint)
        return centers

    def _cabineo_guide_center_points(
        self,
        context: _SketchContext,
        alignment_points: list[adsk.fusion.SketchPoint],
        inward: adsk.core.Vector3D,
        surface: CabineoSurface,
    ) -> tuple[
        list[adsk.fusion.SketchPoint],
        list[adsk.fusion.SketchLine],
    ]:
        projected_points = self._project_points(
            context.sketch,
            alignment_points,
            "access-hole midpoints",
        )
        return self._edge_offset_points(
            context,
            projected_points,
            inward,
            0.58 if surface == CabineoSurface.FLUSH else 0.5,
            "0.58 cm" if surface == CabineoSurface.FLUSH else "0.5 cm",
            "oppositeEdgeOffset",
        )

    def _edge_offset_points(
        self,
        context: _SketchContext,
        base_points: list[adsk.fusion.SketchPoint],
        inward: adsk.core.Vector3D,
        edge_offset: float,
        edge_offset_expression: str,
        parameter_role: str,
    ) -> tuple[
        list[adsk.fusion.SketchPoint],
        list[adsk.fusion.SketchLine],
    ]:
        """Offsets `base_points` (points of this sketch on the selected
        edge) into the small face by one shared distance. Returns the offset
        points and the construction lines leading to them."""
        lines = context.sketch.sketchCurves.sketchLines
        constraints = context.sketch.geometricConstraints
        offset_lines: list[adsk.fusion.SketchLine] = []
        for base_point in base_points:
            initial_end = self._translated(
                base_point.worldGeometry,
                inward,
                edge_offset,
            )
            offset_line = lines.addByTwoPoints(
                base_point,
                context.sketch.modelToSketchSpace(initial_end),
            )
            if not offset_line:
                raise RuntimeError(
                    "Fusion failed to create an edge-offset line."
                )
            offset_line.isConstruction = True
            constraints.addPerpendicular(offset_line, context.edge_line)
            offset_lines.append(offset_line)

        self._add_distance_dimension(
            context.sketch,
            offset_lines[0].startSketchPoint,
            offset_lines[0].endSketchPoint,
            edge_offset_expression,
            parameter_role,
        )
        for offset_line in offset_lines[1:]:
            constraints.addEqual(offset_lines[0], offset_line)
        return (
            [line.endSketchPoint for line in offset_lines],
            offset_lines,
        )

    def _cabineo_guide_centers_for_board(
        self,
        context: _SketchContext,
        board: _AdditionalBoard,
        reference_offset_lines: list[adsk.fusion.SketchLine],
        stations: list[adsk.fusion.SketchPoint] | None = None,
    ) -> list[adsk.fusion.SketchPoint]:
        """Returns the board's hole centers. When `stations` is given, the
        points where each station meets the board's edge are appended to
        it."""
        sketch = context.sketch
        lines = sketch.sketchCurves.sketchLines
        constraints = sketch.geometricConstraints
        board_edge_line = self._project_reference_line(
            sketch,
            board.edge,
            "additional board edge",
        )
        inward = utils.brep.normal_into_face(board.edge, board.small_face)
        centers: list[adsk.fusion.SketchPoint] = []
        for reference in reference_offset_lines:
            # Same station and edge offset as the first board's line.
            # Collinearity with the reference line carries the along-edge
            # position without a fixed dimension; the equal constraint
            # carries the edge offset.
            reference_length = (
                reference.startSketchPoint.geometry.distanceTo(
                    reference.endSketchPoint.geometry
                )
            )
            start_model = utils.brep.project_point_onto_edge(
                reference.startSketchPoint.worldGeometry,
                board.edge,
            )
            end_model = self._translated(
                start_model,
                inward,
                reference_length,
            )
            offset_line = lines.addByTwoPoints(
                sketch.modelToSketchSpace(start_model),
                sketch.modelToSketchSpace(end_model),
            )
            if not offset_line:
                raise RuntimeError(
                    "Fusion failed to create an edge-offset line."
                )
            offset_line.isConstruction = True
            constraints.addCoincident(
                offset_line.startSketchPoint,
                board_edge_line,
            )
            constraints.addCollinear(offset_line, reference)
            constraints.addEqual(reference, offset_line)
            centers.append(offset_line.endSketchPoint)
            if stations is not None:
                stations.append(offset_line.startSketchPoint)
        return centers

    def _project_entities(
        self,
        sketch: adsk.fusion.Sketch,
        entities: list[adsk.core.Base],
    ) -> list[adsk.core.Base]:
        # project2 throws InternalValidationError on a compute-deferred
        # sketch; briefly re-enable solving around it.
        was_deferred = sketch.isComputeDeferred
        if was_deferred:
            sketch.isComputeDeferred = False
        try:
            return sketch.project2(entities, True)
        finally:
            if was_deferred:
                sketch.isComputeDeferred = True

    def _project_single_line(
        self,
        sketch: adsk.fusion.Sketch,
        entity: adsk.core.Base,
        description: str,
    ) -> adsk.fusion.SketchLine:
        """Projects one straight entity and keeps only its own projection.

        project2 hands back more than what was asked for on some geometry:
        for an edge of a board's narrow end face it also projects that
        face's parallel edge, so a sketch on the end face gets two lines
        1 thickness apart, and a sketch on the broad face - where both
        edges project onto the same place - gets the same line twice.
        Fusion offers no way to ask for less, so the result is matched
        back to the source and the surplus lines are deleted; leaving them
        would split the profiles the connector geometry is built from.

        Lines that already existed before the call are never deleted: a
        repeated projection can return the line an earlier call created,
        and that one still belongs to its caller.
        """
        before = list(sketch.sketchCurves.sketchLines)
        projected = [
            line
            for candidate in self._project_entities(
                sketch,
                cast(list[adsk.core.Base], [entity]),
            )
            if (line := adsk.fusion.SketchLine.cast(candidate))
        ]
        start, end = self._flattened_endpoints(sketch, entity)
        tolerance = self.app.pointTolerance * 100

        def matches_source(line: adsk.fusion.SketchLine) -> bool:
            first = line.startSketchPoint.geometry
            second = line.endSketchPoint.geometry
            return (
                max(first.distanceTo(start), second.distanceTo(end))
                <= tolerance
                or max(first.distanceTo(end), second.distanceTo(start))
                <= tolerance
            )

        keeper = next(
            (line for line in projected if matches_source(line)),
            None,
        )
        if not keeper:
            raise RuntimeError(
                f"Fusion failed to project the {description}."
            )
        # Deleting while the sketch is compute-deferred is fine: only
        # project2 itself rejects a deferred sketch.
        for line in projected:
            if line == keeper or any(line == earlier for earlier in before):
                continue
            line.deleteMe()
        return keeper

    def _flattened_endpoints(
        self,
        sketch: adsk.fusion.Sketch,
        entity: adsk.core.Base,
    ) -> tuple[adsk.core.Point3D, adsk.core.Point3D]:
        """The entity's endpoints where they land in the sketch plane."""
        edge = adsk.fusion.BRepEdge.cast(entity)
        if edge:
            ends = (edge.startVertex.geometry, edge.endVertex.geometry)
        else:
            line = adsk.fusion.SketchLine.cast(entity)
            if not line:
                raise RuntimeError(
                    "Only straight entities can be projected as a line."
                )
            ends = (
                line.startSketchPoint.worldGeometry,
                line.endSketchPoint.worldGeometry,
            )
        flattened = []
        for point in ends:
            local = sketch.modelToSketchSpace(point)
            local.z = 0
            flattened.append(local)
        return flattened[0], flattened[1]

    def _project_reference_line(
        self,
        sketch: adsk.fusion.Sketch,
        edge: adsk.fusion.BRepEdge,
        description: str,
    ) -> adsk.fusion.SketchLine:
        projected = self._project_single_line(sketch, edge, description)
        projected.isConstruction = True
        return projected

    def _project_opposite_edge(
        self,
        sketch: adsk.fusion.Sketch,
        small_face: adsk.fusion.BRepFace,
        selected_edge: adsk.fusion.BRepEdge,
    ) -> adsk.fusion.SketchLine:
        selected_midpoint = self._edge_midpoint(selected_edge)
        candidates = [
            edge
            for edge in small_face.edges
            if (
                utils.brep.is_linear(edge)
                and utils.brep.is_parallel(edge, selected_edge)
                and self._edge_midpoint(edge).distanceTo(selected_midpoint)
                > 1e-6
            )
        ]
        if not candidates:
            raise RuntimeError(
                "Could not find the opposite long edge of the small face."
            )
        opposite_edge = max(
            candidates,
            key=lambda edge: self._edge_midpoint(edge).distanceTo(
                selected_midpoint
            ),
        )
        projected = self._project_single_line(
            sketch,
            opposite_edge,
            "opposite edge of the small face",
        )
        projected.isConstruction = True
        return projected

    def _project_points(
        self,
        sketch: adsk.fusion.Sketch,
        source_points: list[adsk.fusion.SketchPoint],
        description: str,
    ) -> list[adsk.fusion.SketchPoint]:
        # One batched project2 call: each call pays a full document
        # transaction (plus the deferral toggle), so per-point calls are
        # several times slower in large documents.
        if not source_points:
            return []
        projected = [
            point
            for entity in self._project_entities(
                sketch,
                cast(list[adsk.core.Base], list(source_points)),
            )
            if (point := adsk.fusion.SketchPoint.cast(entity))
        ]
        if len(projected) != len(source_points):
            raise RuntimeError(
                f"Fusion failed to project the {description}."
            )
        # project2 does not hand the projections back in the order of its
        # input, so pair each source with the projection that landed on it.
        ordered: list[adsk.fusion.SketchPoint] = []
        for source in source_points:
            target = sketch.modelToSketchSpace(source.worldGeometry)
            target.z = 0
            nearest = min(
                projected,
                key=lambda point: point.geometry.distanceTo(target),
            )
            projected.remove(nearest)
            ordered.append(nearest)
        return ordered

    def _guide_hole(
        self,
        connector_type: ConnectorType,
        guide_thickness: float,
    ) -> _GuideHole:
        if connector_type.is_clamex:
            return _GuideHole(
                diameter=self.inputs.clamex_guide_hole_diameter.value,
                diameter_expression=(
                    self.inputs.clamex_guide_hole_diameter.expression
                ),
                depth=(
                    guide_thickness
                    if self.inputs.through_guide_holes.value
                    else 0.8
                ),
            )

        if connector_type == ConnectorType.CABINEO_8:
            diameter = 0.5
            diameter_expression = "0.5 cm"
            depth: float | str = 0.8
            collar_diameter = None
            collar_diameter_expression = None
            collar_depth = None
        elif connector_type == ConnectorType.CABINEO_12:
            diameter = 0.5
            diameter_expression = "0.5 cm"
            depth = 1.2
            collar_diameter = None
            collar_diameter_expression = None
            collar_depth = None
        else:
            insert = CabineoInsert(self.inputs.cabineo_insert_type.value)
            if insert == CabineoInsert.M6X123:
                diameter = 0.8
                diameter_expression = "0.8 cm"
                depth = 1.35
                collar_diameter = None
                collar_diameter_expression = None
                collar_depth = None
            elif insert == CabineoInsert.M6X153:
                diameter = 0.8
                diameter_expression = "0.8 cm"
                depth = 1.65
                collar_diameter = None
                collar_diameter_expression = None
                collar_depth = None
            else:
                diameter = self.inputs.threaded_insert_core_diameter.value
                diameter_expression = (
                    self.inputs.threaded_insert_core_diameter.expression
                )
                depth = self.inputs.threaded_insert_core_depth.expression
                collar_diameter = (
                    self.inputs.threaded_insert_collar_diameter.value
                )
                collar_diameter_expression = (
                    self.inputs.threaded_insert_collar_diameter.expression
                )
                collar_depth = self.inputs.threaded_insert_collar_depth.expression

        if self.inputs.through_guide_holes.value:
            depth = guide_thickness
        return _GuideHole(
            diameter=diameter,
            diameter_expression=diameter_expression,
            depth=depth,
            collar_diameter=collar_diameter,
            collar_diameter_expression=collar_diameter_expression,
            collar_depth=collar_depth,
        )

    def _add_station_points(
        self,
        context: _SketchContext,
        edge: adsk.fusion.BRepEdge,
        positions: list[adsk.core.Point3D],
    ) -> list[adsk.fusion.SketchPoint]:
        if (
            PositioningMode(self.inputs.positioning.value)
            == PositioningMode.CUSTOM_POINTS
        ):
            return self._add_custom_station_points(
                context,
                edge,
                positions,
            )
        return self._add_position_points(context, positions)

    def _add_custom_station_points(
        self,
        context: _SketchContext,
        edge: adsk.fusion.BRepEdge,
        positions: list[adsk.core.Point3D],
    ) -> list[adsk.fusion.SketchPoint]:
        source_points = self._sorted_custom_points(edge)
        if len(source_points) != len(positions):
            raise RuntimeError(
                "The Custom Point projections are incomplete."
            )

        sketch = context.sketch
        constraints = sketch.geometricConstraints
        stations: list[adsk.fusion.SketchPoint] = []
        for source_point, position in zip(source_points, positions):
            projected = self._project_point(
                sketch,
                source_point,
                "Custom Point",
            )
            projected_on_edge = sketch.modelToSketchSpace(position)
            if (
                projected.geometry.distanceTo(projected_on_edge)
                <= self.app.pointTolerance * 10
            ):
                stations.append(projected)
                continue

            drop = sketch.sketchCurves.sketchLines.addByTwoPoints(
                projected,
                projected_on_edge,
            )
            if not drop:
                raise RuntimeError(
                    "Fusion failed to align a Custom Point with the edge."
                )
            drop.isConstruction = True
            constraints.addPerpendicular(drop, context.edge_line)
            constraints.addCoincident(
                drop.endSketchPoint,
                context.edge_line,
            )
            stations.append(drop.endSketchPoint)
        return stations

    def _add_position_points(
        self,
        context: _SketchContext,
        positions: list[adsk.core.Point3D],
    ) -> list[adsk.fusion.SketchPoint]:
        sketch = context.sketch
        constraints = sketch.geometricConstraints
        count = len(positions)
        points: list[adsk.fusion.SketchPoint] = []
        for index, position in enumerate(positions):
            point = sketch.sketchPoints.add(
                sketch.modelToSketchSpace(position)
            )
            if not point:
                raise RuntimeError(
                    "Fusion failed to create a connector position point."
                )
            constraints.addCoincident(point, context.edge_line)
            points.append(point)

        if count == 1:
            constraints.addMidPoint(points[0], context.edge_line)
            return points

        first_margin_parameter: adsk.fusion.ModelParameter | None = None
        end_offset, end_offset_expression = self._end_offset()
        if end_offset == 0:
            constraints.addCoincident(points[0], context.edge_start)
            constraints.addCoincident(points[-1], context.edge_end)
        else:
            first_margin = self._add_distance_dimension(
                sketch,
                context.edge_start,
                points[0],
                end_offset_expression,
                f"{context.parameter_role}FirstMargin",
            )
            first_margin_parameter = first_margin.parameter
            self._add_distance_dimension(
                sketch,
                points[-1],
                context.edge_end,
                first_margin_parameter.name,
                f"{context.parameter_role}LastMargin",
            )

        spacing_lines: list[adsk.fusion.SketchLine] = []
        for first, second in zip(points, points[1:]):
            spacing_line = sketch.sketchCurves.sketchLines.addByTwoPoints(
                first,
                second,
            )
            if not spacing_line:
                raise RuntimeError(
                    "Fusion failed to create connector spacing geometry."
                )
            spacing_line.isConstruction = True
            spacing_lines.append(spacing_line)
        for spacing_line in spacing_lines[1:]:
            constraints.addEqual(spacing_lines[0], spacing_line)
        return points

    def _project_point(
        self,
        sketch: adsk.fusion.Sketch,
        source_point: adsk.core.Base,
        description: str,
    ) -> adsk.fusion.SketchPoint:
        projected = [
            point
            for entity in self._project_entities(
                sketch,
                cast(list[adsk.core.Base], [source_point]),
            )
            if (point := adsk.fusion.SketchPoint.cast(entity))
        ]
        if len(projected) != 1:
            raise RuntimeError(
                f"Fusion failed to project the {description}."
            )
        return projected[0]

    def _point_geometry(
        self,
        point: adsk.core.Base,
    ) -> adsk.core.Point3D:
        sketch_point = adsk.fusion.SketchPoint.cast(point)
        if sketch_point:
            return sketch_point.worldGeometry
        vertex = adsk.fusion.BRepVertex.cast(point)
        if vertex:
            return vertex.geometry
        construction_point = adsk.fusion.ConstructionPoint.cast(point)
        if construction_point:
            return construction_point.geometry
        raise ValueError(
            "Custom Points must be sketch points, vertices, or construction "
            "points."
        )

    def _add_normal_points(
        self,
        context: _SketchContext,
        base_points: list[adsk.fusion.SketchPoint],
        inward: adsk.core.Vector3D,
        offsets: list[float],
        expressions: list[str],
        parameter_role: str,
    ) -> list[adsk.fusion.SketchPoint]:
        if not offsets or len(offsets) != len(expressions):
            raise ValueError("Each normal point requires a distance expression.")

        sketch = context.sketch
        constraints = sketch.geometricConstraints
        points: list[adsk.fusion.SketchPoint] = []
        farthest_index = max(range(len(offsets)), key=offsets.__getitem__)
        reference_lines: dict[int, adsk.fusion.SketchLine] = {}
        for connector_index, base in enumerate(base_points):
            base_model = base.worldGeometry
            farthest_model = self._translated(
                base_model,
                inward,
                offsets[farthest_index],
            )
            normal_line = sketch.sketchCurves.sketchLines.addByTwoPoints(
                base,
                sketch.modelToSketchSpace(farthest_model),
            )
            if not normal_line:
                raise RuntimeError(
                    "Fusion failed to create a connector construction line."
                )
            normal_line.isConstruction = True
            constraints.addPerpendicular(normal_line, context.edge_line)
            if connector_index == 0:
                self._add_distance_dimension(
                    sketch,
                    normal_line.startSketchPoint,
                    normal_line.endSketchPoint,
                    expressions[farthest_index],
                    (
                        f"{context.parameter_role}{parameter_role}"
                        f"1_{farthest_index + 1}"
                    ),
                )
                reference_lines[farthest_index] = normal_line
            else:
                constraints.addEqual(
                    reference_lines[farthest_index],
                    normal_line,
                )

            connector_points: list[adsk.fusion.SketchPoint] = []
            for offset_index, (offset, expression) in enumerate(
                zip(offsets, expressions)
            ):
                if offset_index == farthest_index:
                    point = normal_line.endSketchPoint
                else:
                    model_point = self._translated(
                        base_model,
                        inward,
                        offset,
                    )
                    offset_line = (
                        sketch.sketchCurves.sketchLines.addByTwoPoints(
                            base,
                            sketch.modelToSketchSpace(model_point),
                        )
                    )
                    if not offset_line:
                        raise RuntimeError(
                            "Fusion failed to create a connector inset line."
                        )
                    offset_line.isConstruction = True
                    constraints.addPerpendicular(
                        offset_line,
                        context.edge_line,
                    )
                    if connector_index == 0:
                        self._add_distance_dimension(
                            sketch,
                            offset_line.startSketchPoint,
                            offset_line.endSketchPoint,
                            expression,
                            (
                                f"{context.parameter_role}{parameter_role}"
                                f"1_{offset_index + 1}"
                            ),
                        )
                        reference_lines[offset_index] = offset_line
                    else:
                        constraints.addEqual(
                            reference_lines[offset_index],
                            offset_line,
                        )
                    point = offset_line.endSketchPoint
                connector_points.append(point)
            points.extend(connector_points)
        return points

    def _add_equal_circles(
        self,
        sketch: adsk.fusion.Sketch,
        centers: list[adsk.fusion.SketchPoint],
        radius: float,
        diameter_expression: str,
        parameter_role: str,
    ) -> list[adsk.fusion.SketchCircle]:
        if not centers:
            raise ValueError("At least one circle center is required.")
        constraints = sketch.geometricConstraints
        circles: list[adsk.fusion.SketchCircle] = []
        for center in centers:
            circle = sketch.sketchCurves.sketchCircles.addByCenterRadius(
                center.geometry,
                radius,
            )
            if not circle:
                raise RuntimeError("Fusion failed to create a connector circle.")
            constraints.addCoincident(circle.centerSketchPoint, center)
            circles.append(circle)

        diameter_text = circles[0].centerSketchPoint.geometry.copy()
        diameter_text.x += max(radius * 2, 0.5)
        diameter_text.y += max(radius * 2, 0.5)
        diameter = sketch.sketchDimensions.addDiameterDimension(
            circles[0],
            diameter_text,
        )
        if not diameter or not diameter.parameter:
            raise RuntimeError(
                "Fusion failed to dimension the connector circles."
            )
        self._set_parameter_expression(diameter.parameter, diameter_expression)
        self._name_parameter(diameter.parameter, parameter_role)
        for circle in circles[1:]:
            constraints.addEqual(circles[0], circle)
        return circles

    def _add_center_to_center_slot(
        self,
        sketch: adsk.fusion.Sketch,
        start: adsk.fusion.SketchPoint | adsk.core.Point3D,
        end: adsk.fusion.SketchPoint | adsk.core.Point3D,
        width_expression: str,
        parameter_role: str,
    ) -> tuple[
        adsk.fusion.SketchDimension,
        adsk.fusion.SketchLine,
    ]:
        entities = sketch.addCenterToCenterSlot(
            start,
            end,
            adsk.core.ValueInput.createByString(width_expression),
            True,
        )
        dimensions = [
            dimension
            for entity in entities
            if (dimension := adsk.fusion.SketchDimension.cast(entity))
        ]
        if len(dimensions) != 1 or not dimensions[0].parameter:
            raise RuntimeError(
                "Fusion failed to create the slot width dimension."
            )
        self._set_parameter_expression(dimensions[0].parameter, width_expression)
        self._name_parameter(dimensions[0].parameter, parameter_role)
        centerlines = [
            line
            for entity in entities
            if (
                (line := adsk.fusion.SketchLine.cast(entity))
                and line.isConstruction
            )
        ]
        if len(centerlines) != 1:
            raise RuntimeError(
                "Fusion failed to return the slot centerline."
            )
        return dimensions[0], centerlines[0]

    def _add_distance_dimension(
        self,
        sketch: adsk.fusion.Sketch,
        start: adsk.fusion.SketchPoint,
        end: adsk.fusion.SketchPoint,
        expression: str | None,
        parameter_role: str,
        is_driving: bool = True,
    ) -> adsk.fusion.SketchLinearDimension:
        start_geometry = start.geometry
        end_geometry = end.geometry
        text_point = adsk.core.Point3D.create(
            (start_geometry.x + end_geometry.x) / 2 + 0.2,
            (start_geometry.y + end_geometry.y) / 2 + 0.2,
            0,
        )
        dimension = sketch.sketchDimensions.addDistanceDimension(
            start,
            end,
            adsk.fusion.DimensionOrientations.AlignedDimensionOrientation,  # type: ignore
            text_point,
            is_driving,
        )
        if not dimension or not dimension.parameter:
            raise RuntimeError(
                "Fusion failed to create a connector distance dimension."
            )
        if is_driving:
            if expression is None:
                raise ValueError("A driving dimension requires an expression.")
            self._set_parameter_expression(dimension.parameter, expression)
        self._name_parameter(dimension.parameter, parameter_role)
        return dimension

    def _target_body(
        self,
        component: adsk.fusion.Component,
        role: str,
    ) -> adsk.fusion.BRepBody:
        # Re-resolve via entity token: features created in between can
        # invalidate direct body references.
        entities = component.parentDesign.findEntityByToken(
            self._target_body_tokens[role]
        )
        body = next(
            (
                candidate
                for entity in entities
                if (candidate := adsk.fusion.BRepBody.cast(entity))
            ),
            None,
        )
        if not body:
            raise RuntimeError(
                f"Fusion could not re-resolve the connector {role} body."
            )
        return body

    def _start_face(
        self,
        component: adsk.fusion.Component,
        role: str,
    ) -> adsk.fusion.BRepFace:
        # Re-resolve via entity token: every cut that starts from this face
        # also modifies it, which invalidates a direct face reference.
        entities = component.parentDesign.findEntityByToken(
            self._start_face_tokens[role]
        )
        face = next(
            (
                candidate
                for entity in entities
                if (candidate := adsk.fusion.BRepFace.cast(entity))
            ),
            None,
        )
        if not face:
            raise RuntimeError(
                f"Fusion could not re-resolve the connector {role} face."
            )
        return face

    def _create_cut_extrude(
        self,
        component: adsk.fusion.Component,
        sketch: adsk.fusion.Sketch,
        target_body: adsk.fusion.BRepBody | list[adsk.fusion.BRepBody],
        direction: adsk.core.Vector3D,
        distance: float | str,
        name: str,
        parameter_role: str,
        start_face: adsk.fusion.BRepFace | None = None,
    ) -> adsk.fusion.ExtrudeFeature:
        profiles = adsk.core.ObjectCollection.create()
        for profile in sketch.profiles:
            profiles.add(profile)
        if profiles.count == 0:
            raise RuntimeError(f"'{sketch.name}' did not create any profiles.")

        extrude_input = component.features.extrudeFeatures.createInput(
            profiles,
            adsk.fusion.FeatureOperations.CutFeatureOperation,  # type: ignore
        )
        if not extrude_input:
            raise RuntimeError(f"Fusion failed to initialize '{name}'.")
        if start_face is not None:
            # Start the cut at the target board's own face: additional
            # boards can sit at a different depth than the sketch plane.
            start = adsk.fusion.FromEntityStartDefinition.create(
                start_face,
                adsk.core.ValueInput.createByReal(0),
            )
            if not start:
                raise RuntimeError(
                    f"Fusion failed to define the start face of '{name}'."
                )
            extrude_input.startExtent = start
        value_input = (
            adsk.core.ValueInput.createByString(distance)
            if isinstance(distance, str)
            else adsk.core.ValueInput.createByReal(distance)
        )
        extent = adsk.fusion.DistanceExtentDefinition.create(value_input)
        if not extent:
            raise RuntimeError(f"Fusion failed to define the depth of '{name}'.")
        extent_direction = self._extent_direction(sketch, direction)
        if not extrude_input.setOneSideExtent(extent, extent_direction):
            raise RuntimeError(f"Fusion rejected the extent of '{name}'.")
        extrude_input.participantBodies = (
            target_body if isinstance(target_body, list) else [target_body]
        )

        extrude = component.features.extrudeFeatures.add(extrude_input)
        if not extrude:
            raise RuntimeError(f"Fusion failed to create '{name}'.")
        extrude.name = name
        sketch.isVisible = False

        final_extent = adsk.fusion.DistanceExtentDefinition.cast(
            extrude.extentOne
        )
        if final_extent and final_extent.distance:
            self._name_parameter(final_extent.distance, parameter_role)
        final_start = adsk.fusion.FromEntityStartDefinition.cast(
            extrude.startExtent
        )
        if final_start:
            start_offset = adsk.fusion.ModelParameter.cast(final_start.offset)
            if start_offset:
                self._name_parameter(
                    start_offset,
                    f"{parameter_role}StartOffset",
                )
        if extrude.taperAngleOne:
            self._name_parameter(
                extrude.taperAngleOne,
                f"{parameter_role}TaperAngle",
            )
        return extrude

    def _create_cut_extrude_to_face(
        self,
        component: adsk.fusion.Component,
        sketch: adsk.fusion.Sketch,
        target_body: adsk.fusion.BRepBody,
        target_face: adsk.fusion.BRepFace,
        direction: adsk.core.Vector3D,
        offset: str,
        name: str,
        parameter_role: str,
    ) -> adsk.fusion.ExtrudeFeature:
        """Cuts from the sketch plane towards `target_face`, stopping
        `offset` short of it."""
        profiles = adsk.core.ObjectCollection.create()
        for profile in sketch.profiles:
            profiles.add(profile)
        if profiles.count == 0:
            raise RuntimeError(f"'{sketch.name}' did not create any profiles.")

        extrude_input = component.features.extrudeFeatures.createInput(
            profiles,
            adsk.fusion.FeatureOperations.CutFeatureOperation,  # type: ignore
        )
        if not extrude_input:
            raise RuntimeError(f"Fusion failed to initialize '{name}'.")
        extent = adsk.fusion.ToEntityExtentDefinition.create(
            target_face,
            False,
            adsk.core.ValueInput.createByString(f"-({offset})"),
        )
        if not extent:
            raise RuntimeError(f"Fusion failed to define the depth of '{name}'.")
        extent.directionHint = direction
        if not extrude_input.setOneSideExtent(
            extent,
            self._extent_direction(sketch, direction),
        ):
            raise RuntimeError(f"Fusion rejected the extent of '{name}'.")
        extrude_input.participantBodies = [target_body]

        extrude = component.features.extrudeFeatures.add(extrude_input)
        if not extrude:
            raise RuntimeError(f"Fusion failed to create '{name}'.")
        extrude.name = name
        sketch.isVisible = False

        final_extent = adsk.fusion.ToEntityExtentDefinition.cast(
            extrude.extentOne
        )
        if final_extent:
            final_offset = adsk.fusion.ModelParameter.cast(final_extent.offset)
            if final_offset:
                self._name_parameter(final_offset, parameter_role)
        return extrude

    def _extent_direction(
        self,
        sketch: adsk.fusion.Sketch,
        direction: adsk.core.Vector3D,
    ):
        sketch_normal = sketch.xDirection.crossProduct(sketch.yDirection)
        return (
            adsk.fusion.ExtentDirections.PositiveExtentDirection
            if sketch_normal.dotProduct(direction) >= 0
            else adsk.fusion.ExtentDirections.NegativeExtentDirection
        )

    def _unique_parameter_prefix(
        self,
        design: adsk.fusion.Design,
    ) -> str:
        parameter_names = {parameter.name for parameter in design.allParameters}
        base = "connectorsNative"
        index = 1
        while True:
            candidate = base if index == 1 else f"{base}{index}"
            if not any(
                name.startswith(f"{candidate}_")
                for name in parameter_names
            ):
                return candidate
            index += 1

    def _set_parameter_expression(
        self,
        parameter: adsk.fusion.ModelParameter,
        expression: str,
    ) -> None:
        """Overrides the shared helper: writes only expressions that carry a
        parametric link.

        Every dimension here is created on geometry already placed at the
        intended value (audited per call site - see door_latch_native's
        counterbore for the failure mode when that invariant is violated),
        so writing a pure literal changes nothing but the displayed text.
        An expression that names a parameter is different - that link cannot
        be recovered from the geometry - so those are always written (e.g.
        later slots referencing the first slot's width parameter).

        See Addin._expression_references_parameter for why this is worth
        doing: a parameter write costs ~0.5 s on a large assembly.
        """
        if self._expression_references_parameter(expression):
            parameter.expression = expression

    def _name_parameter(
        self,
        parameter: adsk.fusion.ModelParameter,
        role: str,
    ) -> None:
        """Renaming is disabled: it is pure cosmetics and it dominates the
        runtime on large assemblies.

        Nothing depends on the names. Every cross-reference here reads
        `parameter.name` live, so Fusion's auto-generated names (d123) carry
        the parametric links just as well.

        The cost is set by the size of the document, not by the number of
        parameters: a rename measures 0.2 ms in an empty design but ~460 ms
        in a 1750-feature assembly, because each write triggers a document
        update that scales with the model.

        To restore human-readable names, delete this early return.
        """
        return

    def _group_features(
        self,
        component: adsk.fusion.Component,
        first_sketch: adsk.fusion.Sketch,
        last_feature: adsk.fusion.Feature,
    ) -> None:
        group = component.parentDesign.timeline.timelineGroups.add(
            first_sketch.timelineObject.index,
            last_feature.timelineObject.index,
        )
        if group:
            group.name = "Connector (Native)"
            group.isCollapsed = True

    def _require_fully_constrained(
        self,
        sketch: adsk.fusion.Sketch,
    ) -> None:
        if sketch.isComputeDeferred:
            sketch.isComputeDeferred = False
        fixed_curves = [
            curve
            for curve in sketch.sketchCurves
            if curve.isFixed and not curve.isReference
        ]
        if fixed_curves:
            raise RuntimeError(
                f"'{sketch.name}' contains fixed sketch geometry."
            )
        if sketch.isFullyConstrained:
            return
        unconstrained_count = sum(
            1 for curve in sketch.sketchCurves if not curve.isFullyConstrained
        )
        raise RuntimeError(
            f"'{sketch.name}' is under-constrained "
            f"({unconstrained_count} unconstrained curves)."
        )

    def _translated(
        self,
        point: adsk.core.Point3D,
        direction: adsk.core.Vector3D,
        distance: float,
    ) -> adsk.core.Point3D:
        result = point.copy()
        translation = direction.copy()
        translation.scaleBy(distance)
        result.translateBy(translation)
        return result

    def _edge_midpoint(
        self,
        edge: adsk.fusion.BRepEdge,
    ) -> adsk.core.Point3D:
        start = edge.startVertex.geometry
        end = edge.endVertex.geometry
        return adsk.core.Point3D.create(
            (start.x + end.x) / 2,
            (start.y + end.y) / 2,
            (start.z + end.z) / 2,
        )

    def _opposite(
        self,
        direction: adsk.core.Vector3D,
    ) -> adsk.core.Vector3D:
        result = direction.copy()
        result.scaleBy(-1)
        return result
