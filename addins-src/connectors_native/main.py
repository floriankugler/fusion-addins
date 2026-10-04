from dataclasses import dataclass
from enum import Enum, unique
import os
from typing import cast

import adsk.core
import adsk.fusion

from lib import addin, domino, edge_sketch, inputs, ui_placement, utils
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

    def save_state(self) -> str:
        return self.expression or ""

    def restore_state(self, state, design: adsk.fusion.Design) -> bool:
        if not isinstance(state, str):
            return False
        self.expression = state or None
        if self.input:
            self.input.value = state
        return True

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


class ConnectorsNativeInputs(domino.DominoInputs, inputs.Inputs):
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
        self.add_domino_size_input(is_domino)
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
        self.add_domino_end_stop_input(
            lambda: is_domino() and has_end_offset()
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
                    == domino.EndStop.CUSTOM.value
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

        self.add_domino_slot_inputs(units, is_domino, "adjacent board")

        super().__init__()


class ConnectorsNative(addin.Addin):
    inputs: ConnectorsNativeInputs
    _parameter_prefix: str
    _target_body_tokens: dict[str, str]
    _start_face_tokens: dict[str, str]
    _sketcher: edge_sketch.EdgeSketcher

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

    @property
    def group_edit_enabled(self) -> bool:
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

        self._sketcher = edge_sketch.EdgeSketcher(
            self._set_parameter_expression,
            self._name_parameter,
        )
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
        access_cut_direction = edge_sketch.opposite(
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
            )
            return

        access_context = self._sketcher.create_sketch(
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
        self._sketcher.require_fully_constrained(access_context.sketch)

        relief_context: edge_sketch.SketchContext | None = None
        if connector_type.is_cabineo and surface != CabineoSurface.NONE:
            relief_context = self._sketcher.create_sketch(
                component,
                geometry.access_face,
                geometry.edge,
                "Connector (Native) - Access Relief",
                "accessRelief",
            )
            relief_station_points = self._sketcher.project_points(
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
            self._sketcher.require_fully_constrained(relief_context.sketch)

        guide_hole = self._guide_hole(connector_type, geometry.guide_thickness)
        guide_context = self._sketcher.create_sketch(
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
        self._sketcher.require_fully_constrained(guide_context.sketch)

        collar_context: edge_sketch.SketchContext | None = None
        if (
            guide_hole.collar_diameter is not None
            and guide_hole.collar_diameter_expression is not None
        ):
            collar_context = self._sketcher.create_sketch(
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
            self._sketcher.require_fully_constrained(collar_context.sketch)

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
            last_feature = self._sketcher.create_cut_extrude(
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
                last_feature = self._sketcher.create_cut_extrude(
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

        last_feature = self._sketcher.create_cut_extrude(
            component=component,
            sketch=guide_context.sketch,
            target_body=self._target_body(component, "guide"),
            direction=opposite_cut_direction,
            distance=guide_hole.depth,
            name="Connector (Native) - Opposite Cut",
            parameter_role="oppositeDepth",
        )

        if collar_context and guide_hole.collar_depth is not None:
            last_feature = self._sketcher.create_cut_extrude(
                component=component,
                sketch=collar_context.sketch,
                target_body=self._target_body(component, "guide"),
                direction=opposite_cut_direction,
                distance=guide_hole.collar_depth,
                name="Connector (Native) - Insert Collar Cut",
                parameter_role="collarDepth",
            )

        self.group_features(
            access_context.sketch,
            last_feature,
            "Connector (Native)",
        )

    def _execute_domino(
        self,
        component: adsk.fusion.Component,
        geometry: _ResolvedGeometry,
        additional_boards: list[_AdditionalBoard],
        positions: list[adsk.core.Point3D],
    ) -> None:
        """Domino slots are cut into the adjacent board's face only. The
        mortises in the selected boards' small faces are left to the Domino
        machine; optional V-grooves on the large faces mark their positions.
        """
        builder = domino.DominoBuilder(
            self._sketcher,
            self.inputs,
            "Connector (Native)",
        )
        sketches = builder.create_sketches(
            component,
            [
                domino.Board(
                    geometry.edge,
                    geometry.small_face,
                    geometry.access_thickness,
                )
            ]
            + [
                domino.Board(board.edge, board.small_face, board.access_thickness)
                for board in additional_boards
            ],
            positions,
            self._custom_points(geometry.edge),
            self._end_offset(),
        )
        last_feature = builder.cut(
            component,
            sketches,
            self._target_body_tokens["guide"],
            utils.brep.get_opposite_face(geometry.guide_face).entityToken,
            [
                self._target_body_tokens[f"access{board_index}"]
                for board_index in range(len(additional_boards) + 1)
            ],
        )
        self.group_features(
            sketches.positions,
            last_feature,
            "Connector (Native)",
        )

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
            return self.inputs.domino_validation_error(
                min(
                    [geometry.access_thickness]
                    + [board.access_thickness for board in additional_boards]
                ),
                geometry.guide_thickness,
                self.app.pointTolerance * 10,
            )
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

        return edge_sketch.evenly_spaced_positions(
            edge,
            self.inputs.number_of_connectors.value,
            self._end_offset()[0],
        )

    def _end_offset(self) -> tuple[float, str]:
        """Distance from the edge ends to the first and last connector, as
        value and expression. Dominos can take it from the machine's stops
        instead of the End Offset input."""
        if ConnectorType(self.inputs.size.value).is_domino:
            return self.inputs.domino_end_offset(self.inputs.offset)
        return self.inputs.offset.value, self.inputs.offset.expression

    def _custom_points(
        self,
        edge: adsk.fusion.BRepEdge,
    ) -> list[adsk.core.Base] | None:
        """The Custom Points sorted along the edge, or None when the
        connectors are positioned by number."""
        if (
            PositioningMode(self.inputs.positioning.value)
            == PositioningMode.CUSTOM_POINTS
        ):
            return self._sorted_custom_points(edge)
        return None

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

    def _add_access_geometry(
        self,
        context: edge_sketch.SketchContext,
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
                width_dimension, centerline = self._sketcher.add_center_to_center_slot(
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
        context: edge_sketch.SketchContext,
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
            width_dimension, _ = self._sketcher.add_center_to_center_slot(
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
        context: edge_sketch.SketchContext,
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
                    self._sketcher.centered_points_for_board(
                        context,
                        board.edge,
                        board.small_face,
                        board.access_thickness,
                        reference_cross_lines,
                    )
                )
            centers: list[adsk.fusion.SketchPoint] = []
            lines = context.sketch.sketchCurves.sketchLines
            constraints = context.sketch.geometricConstraints
            reference_centerline: adsk.fusion.SketchLine | None = None
            for center in centerline_points:
                center_model = center.worldGeometry
                first_model = edge_sketch.translated(
                    center_model,
                    edge_direction,
                    -10.1 / 2,
                )
                second_model = edge_sketch.translated(
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
                    self._sketcher.add_distance_dimension(
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
                self._sketcher.offset_points_for_board(
                    context,
                    board.edge,
                    board.small_face,
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
        context: edge_sketch.SketchContext,
        source_points: list[adsk.fusion.SketchPoint],
        diameter: float,
        diameter_expression: str,
        parameter_role: str,
    ) -> list[adsk.fusion.SketchPoint]:
        centers = self._sketcher.project_points(
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
        context: edge_sketch.SketchContext,
        alignment_points: list[adsk.fusion.SketchPoint],
        small_face: adsk.fusion.BRepFace,
        edge: adsk.fusion.BRepEdge,
        inward: adsk.core.Vector3D,
    ) -> tuple[
        list[adsk.fusion.SketchPoint],
        list[adsk.fusion.SketchLine],
    ]:
        projected_points = self._sketcher.project_points(
            context.sketch,
            alignment_points,
            "access-hole midpoints",
        )
        return self._sketcher.board_center_points(
            context,
            projected_points,
            small_face,
            edge,
            inward,
        )

    def _cabineo_guide_center_points(
        self,
        context: edge_sketch.SketchContext,
        alignment_points: list[adsk.fusion.SketchPoint],
        inward: adsk.core.Vector3D,
        surface: CabineoSurface,
    ) -> tuple[
        list[adsk.fusion.SketchPoint],
        list[adsk.fusion.SketchLine],
    ]:
        projected_points = self._sketcher.project_points(
            context.sketch,
            alignment_points,
            "access-hole midpoints",
        )
        return self._sketcher.edge_offset_points(
            context,
            projected_points,
            inward,
            0.58 if surface == CabineoSurface.FLUSH else 0.5,
            "0.58 cm" if surface == CabineoSurface.FLUSH else "0.5 cm",
            "oppositeEdgeOffset",
        )

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
        context: edge_sketch.SketchContext,
        edge: adsk.fusion.BRepEdge,
        positions: list[adsk.core.Point3D],
    ) -> list[adsk.fusion.SketchPoint]:
        return self._sketcher.add_station_points(
            context,
            positions,
            self._custom_points(edge),
            self._end_offset(),
        )

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
        context: edge_sketch.SketchContext,
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
            farthest_model = edge_sketch.translated(
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
                self._sketcher.add_distance_dimension(
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
                    model_point = edge_sketch.translated(
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
                        self._sketcher.add_distance_dimension(
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

    def _target_body(
        self,
        component: adsk.fusion.Component,
        role: str,
    ) -> adsk.fusion.BRepBody:
        # Re-resolve via entity token: features created in between can
        # invalidate direct body references.
        return edge_sketch.find_by_token(
            component.parentDesign,
            self._target_body_tokens[role],
            adsk.fusion.BRepBody,
            f"connector {role} body",
        )

    def _start_face(
        self,
        component: adsk.fusion.Component,
        role: str,
    ) -> adsk.fusion.BRepFace:
        # Re-resolve via entity token: every cut that starts from this face
        # also modifies it, which invalidates a direct face reference.
        return edge_sketch.find_by_token(
            component.parentDesign,
            self._start_face_tokens[role],
            adsk.fusion.BRepFace,
            f"connector {role} face",
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

