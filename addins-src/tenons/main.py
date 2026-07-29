from dataclasses import dataclass
from enum import Enum, unique
import math
import os
from typing import cast

import adsk.core
import adsk.fusion

from lib import addin, inputs, ui_placement, utils
from lib.fusionbootstrap.runtime import RuntimeInfo


_addin: addin.Addin | None = None


@unique
class ConnectorType(Enum):
    NONE = 0
    SCREW = 1
    CLAMEX_P10 = 10
    CLAMEX_P14 = 14
    CABINEO_8 = 8
    CABINEO_12 = 12
    CABINEO_8_M6 = 9

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


@unique
class ScrewType(Enum):
    NONE = 0
    CENTERED = 1
    TWO_SIDES = 2


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


@dataclass(frozen=True)
class _ResolvedGeometry:
    edge: adsk.fusion.BRepEdge
    tenon_face: adsk.fusion.BRepFace
    small_face: adsk.fusion.BRepFace
    mortise_face: adsk.fusion.BRepFace
    tenon_opposite_face: adsk.fusion.BRepFace
    mortise_opposite_face: adsk.fusion.BRepFace
    tenon_thickness: float
    mortise_thickness: float


@dataclass(frozen=True)
class _SketchContext:
    sketch: adsk.fusion.Sketch
    edge_line: adsk.fusion.SketchLine
    edge_start: adsk.fusion.SketchPoint
    edge_end: adsk.fusion.SketchPoint
    parameter_role: str


@dataclass(frozen=True)
class _TenonLayout:
    context: _SketchContext
    centers: list[adsk.fusion.SketchPoint]
    center_model_points: list[adsk.core.Point3D]
    bases: list[adsk.fusion.SketchLine]
    base_starts: list[adsk.fusion.SketchPoint]
    base_ends: list[adsk.fusion.SketchPoint]
    outers: list[adsk.fusion.SketchLine]
    outer_starts: list[adsk.fusion.SketchPoint]
    outer_ends: list[adsk.fusion.SketchPoint]


@dataclass(frozen=True)
class _GuideHole:
    diameter: float
    diameter_expression: str
    depth: str
    edge_distance: float
    collar_diameter: float | None = None
    collar_diameter_expression: str | None = None
    collar_depth: str | None = None


@dataclass(frozen=True)
class _CutSpec:
    sketch: adsk.fusion.Sketch
    body_role: str
    direction: adsk.core.Vector3D
    distance: float | str | None
    name: str
    parameter_role: str


@dataclass(frozen=True)
class _HoleSpec:
    sketch: adsk.fusion.Sketch
    body_role: str
    direction: adsk.core.Vector3D
    center_points: list[adsk.fusion.SketchPoint]
    diameter_expression: str
    depth: str | None  # None cuts through the whole target body.
    name: str
    parameter_role: str


def run(context, runtime_info: RuntimeInfo):
    global _addin
    _addin = Tenons(runtime_info)


def stop(context):
    global _addin
    if _addin:
        _addin.shutdown()
    _addin = None


class TenonsInputs(inputs.Inputs):
    class Positioning:
        NUMBER = inputs.DropDownInput.Item("Number of Tenons", 1)
        POINTS = inputs.DropDownInput.Item("Custom Points", 2)

    class Connectors:
        NONE = inputs.DropDownInput.Item("None", ConnectorType.NONE.value)
        SCREW = inputs.DropDownInput.Item("Screw", ConnectorType.SCREW.value)
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

    class Screws:
        NONE = inputs.DropDownInput.Item("None", ScrewType.NONE.value)
        CENTERED = inputs.DropDownInput.Item(
            "Centered",
            ScrewType.CENTERED.value,
        )
        TWO_SIDES = inputs.DropDownInput.Item(
            "Two Sides",
            ScrewType.TWO_SIDES.value,
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
            name="Edge",
            filter=["LinearEdges"],
            lower_bound=1,
            upper_bound=1,
            tool_tip="Select one straight edge along which to create tenons.",
        )
        self.positioning = inputs.DropDownInput(
            id="positioning",
            name="Positioning",
            options=utils.misc.class_property_values(
                TenonsInputs.Positioning,
                inputs.DropDownInput.Item,
            ),
            default_value=TenonsInputs.Positioning.NUMBER.value,
            tool_tip="Position an exact number of tenons or use selected sketch points.",
        )
        self.points = inputs.SelectionByEntityTokenInput(
            id="points",
            name="Custom Points",
            filter=["SketchPoints"],
            lower_bound=0,
            upper_bound=0,
            tool_tip=(
                "Select sketch points. Each point is projected perpendicularly "
                "onto the selected edge to locate one tenon."
            ),
            update_visibility=lambda: (
                self.positioning.value
                == TenonsInputs.Positioning.POINTS.value
            ),
        )
        self.number_of_tenons = inputs.IntegerInput(
            id="numberOfTenons",
            name="Number of Tenons",
            default_value=3,
            minimum=1,
            maximum=100,
            tool_tip=(
                "Number of equally spaced tenons. A single tenon is centered."
            ),
            update_visibility=lambda: (
                self.positioning.value
                == TenonsInputs.Positioning.NUMBER.value
            ),
        )
        self.distance_from_edge = inputs.FloatInput(
            id="distanceFromEdge",
            name="End Margin",
            default_value=3.0,
            tool_tip=(
                "Distance from each edge endpoint to the nearest tenon edge."
            ),
            units=units,
            update_visibility=lambda: (
                self.positioning.value
                == TenonsInputs.Positioning.NUMBER.value
                and self.number_of_tenons.value > 1
            ),
        )
        self.distance_from_edge.minimum_value = 0
        self.width = inputs.FloatInput(
            id="width",
            name="Tenon Width",
            default_value=5.0,
            tool_tip="Width of every tenon along the selected edge.",
            units=units,
        )
        self.width.minimum_value = 0
        self.remaining_material = inputs.FloatInput(
            id="remainingMaterial",
            name="Remaining Material",
            default_value=0,
            tool_tip="Material to leave at the back of the mortise board.",
            units=units,
        )
        self.remaining_material.minimum_value = 0
        self.mortise_length_offset = inputs.FloatInput(
            id="mortiseLengthOffset",
            name="Mortise Length Offset",
            default_value=0.01,
            tool_tip="Clearance added to the mortise along the selected edge.",
            units=units,
        )
        # The offset dimensions between the projected tenon profile and the
        # mortise rectangle require a positive value.
        self.mortise_length_offset.minimum_value = 0
        self.mortise_length_offset.minimum_inclusive = False
        self.mortise_width_offset = inputs.FloatInput(
            id="mortiseWidthOffset",
            name="Mortise Width Offset",
            default_value=0.01,
            tool_tip="Clearance added across the tenon-board thickness.",
            units=units,
        )
        self.mortise_width_offset.minimum_value = 0
        self.mortise_width_offset.minimum_inclusive = False
        self.mortise_depth_offset = inputs.FloatInput(
            id="mortiseDepthOffset",
            name="Mortise Depth Offset",
            default_value=0.05,
            tool_tip="Extra depth added beyond the tenon length.",
            units=units,
        )
        self.tool_diameter = inputs.FloatInput(
            id="toolDiameter",
            name="Tool Diameter",
            default_value=0.6,
            tool_tip="Router diameter used for the tenon and mortise dog bones.",
            units=units,
        )
        self.tool_diameter.minimum_value = 0
        self.dog_bone_offset = inputs.FloatInput(
            id="dogBoneOffset",
            name="Dog Bone Offset",
            default_value=0.01,
            tool_tip="Extra diameter added to every dog-bone relief.",
            units=units,
        )

        self.connector = inputs.DropDownInput(
            id="connector",
            name="Connector",
            options=utils.misc.class_property_values(
                TenonsInputs.Connectors,
                inputs.DropDownInput.Item,
            ),
            default_value=TenonsInputs.Connectors.NONE.value,
            tool_tip="Optional screw, Clamex, or Cabineo connector holes.",
        )

        is_screw = lambda: self.connector.value == ConnectorType.SCREW.value
        self.screw_diameter = inputs.FloatInput(
            id="screwDiameter",
            name="Screw Diameter",
            default_value=0.4,
            tool_tip="Diameter of the connector screw holes.",
            units=units,
            update_visibility=is_screw,
        )
        self.screw_diameter.minimum_value = 0
        self.mortise_screw = inputs.DropDownInput(
            id="mortiseScrew",
            name="Mortise Screw",
            options=utils.misc.class_property_values(
                TenonsInputs.Screws,
                inputs.DropDownInput.Item,
            ),
            default_value=TenonsInputs.Screws.CENTERED.value,
            tool_tip="Screw-hole placement in the mortise board.",
            update_visibility=is_screw,
        )
        self.tenon_screw = inputs.DropDownInput(
            id="tenonScrew",
            name="Tenon Screw",
            options=utils.misc.class_property_values(
                TenonsInputs.Screws,
                inputs.DropDownInput.Item,
            ),
            default_value=TenonsInputs.Screws.NONE.value,
            tool_tip="Screw-hole placement through the tenons.",
            update_visibility=is_screw,
        )
        self.screw_offset = inputs.FloatInput(
            id="screwOffset",
            name="Screw Offset",
            default_value=1.2,
            tool_tip="Distance from a tenon edge to a two-sided screw hole.",
            units=units,
            update_visibility=lambda: (
                is_screw()
                and (
                    self.mortise_screw.value == ScrewType.TWO_SIDES.value
                    or self.tenon_screw.value == ScrewType.TWO_SIDES.value
                )
            ),
        )
        self.screw_offset.minimum_value = 0

        is_lamello = lambda: ConnectorType(self.connector.value).is_clamex or (
            ConnectorType(self.connector.value).is_cabineo
        )
        is_clamex = lambda: ConnectorType(self.connector.value).is_clamex
        is_cabineo = lambda: ConnectorType(self.connector.value).is_cabineo
        self.clamex_guide_hole_diameter = inputs.FloatInput(
            id="clamexGuideHoleDiameter",
            name="Guide Hole Diameter",
            default_value=0.77,
            tool_tip="Diameter of the paired Clamex holes in the mortise board.",
            units=units,
            update_visibility=is_clamex,
        )
        self.clamex_guide_hole_diameter.minimum_value = 0
        self.through_guide_holes = inputs.CheckboxInput(
            id="throughGuideHoles",
            name="Through Opposite Holes",
            default_value=False,
            tool_tip="Cut the mortise-board guide holes through its full thickness.",
            update_visibility=is_lamello,
        )
        self.cabineo_surface = inputs.DropDownInput(
            id="cabineoSurface",
            name="Surface",
            options=utils.misc.class_property_values(
                TenonsInputs.SurfaceTypes,
                inputs.DropDownInput.Item,
            ),
            default_value=TenonsInputs.SurfaceTypes.NONE.value,
            tool_tip="Surface treatment around the Cabineo pocket.",
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

        is_m6 = lambda: (
            self.connector.value == ConnectorType.CABINEO_8_M6.value
        )
        self.cabineo_insert_type = inputs.DropDownInput(
            id="insertType",
            name="Insert Type",
            options=utils.misc.class_property_values(
                TenonsInputs.InsertTypes,
                inputs.DropDownInput.Item,
            ),
            default_value=TenonsInputs.InsertTypes.THREADED_INSERT.value,
            tool_tip="Opposite-hole variant for Cabineo 8 M6.",
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
            default_value=1.35,
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

        super().__init__()


class Tenons(addin.Addin):
    inputs: TenonsInputs
    _parameter_prefix: str
    _body_tokens: dict[str, str]

    @property
    def plugin_name(self) -> str:
        return "Tenons"

    @property
    def plugin_desc(self) -> str:
        return "Create sheet-good tenons and mortises with native Fusion features."

    @property
    def plugin_tooltip(self) -> str:
        return (
            "Creates fully constrained sketches, join and cut extrudes, dog "
            "bones, and optional connector holes in the standard timeline."
        )

    @property
    def resource_dir(self) -> str:
        return os.path.join(os.path.dirname(__file__), "Resources")

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

    def create_inputs(self) -> TenonsInputs:
        design = adsk.fusion.Design.cast(self.app.activeProduct)
        if not design:
            raise RuntimeError("Tenons requires an active Fusion design.")
        return TenonsInputs(design.unitsManager)

    def pre_select(self, input, selection) -> bool:
        if not self.inputs or not input:
            return True
        if input.id == self.inputs.edge.id:
            edge = adsk.fusion.BRepEdge.cast(selection)
            return bool(
                edge
                and edge.body.isSolid
                and utils.brep.is_linear(edge)
                and edge.faces.count == 2
                and all(utils.brep.is_planar(face) for face in edge.faces)
            )
        if input.id == self.inputs.points.id:
            return bool(adsk.fusion.SketchPoint.cast(selection))
        return True

    def _validate(self, args: adsk.core.ValidateInputsEventArgs):
        try:
            self.update_inputs_from_ui()
            error = self._validation_error()
        except Exception as exc:
            error = str(exc)
        args.areInputsValid = error is None
        self.showError(error)

    def execute(self):
        error = self._validation_error()
        if error:
            raise ValueError(error)

        geometry = self._resolve_geometry()
        component = geometry.tenon_face.body.parentComponent
        self._parameter_prefix = self._unique_parameter_prefix(
            component.parentDesign
        )
        self._body_tokens = {
            "tenon": geometry.tenon_face.body.entityToken,
            "mortise": geometry.mortise_face.body.entityToken,
        }

        positions = self._tenon_positions(geometry.edge)
        tenon_through_direction = utils.brep.normal_towards_face(
            geometry.tenon_face,
            geometry.tenon_opposite_face,
        )
        mortise_cut_direction = utils.brep.normal_away_from_body(
            geometry.small_face
        )

        layout = self._create_tenon_layout(
            component,
            geometry,
            positions,
        )
        self._require_fully_constrained(layout.context.sketch)

        tenon_tool_feature = self._create_to_entity_extrude(
            component=component,
            sketch=layout.context.sketch,
            target_body=geometry.tenon_face.body,
            target_entity=geometry.tenon_opposite_face,
            direction=tenon_through_direction,
            offset_expression=None,
            operation=adsk.fusion.FeatureOperations.NewBodyFeatureOperation,  # type: ignore
            name="Tenons - Tool Bodies",
            parameter_role="tenonThickness",
        )
        tenon_tools = cast(
            list[adsk.fusion.BRepBody],
            utils.fusion.as_list(tenon_tool_feature.bodies),
        )
        if len(tenon_tools) != len(layout.centers):
            raise RuntimeError(
                "Fusion did not create one tool body for every tenon."
            )

        mortise_sketch = self._create_mortise_sketch(
            component,
            geometry,
            tenon_tools,
        )
        self._require_fully_constrained(mortise_sketch)

        root_dogbone_sketch = self._create_root_dogbone_sketch(
            component,
            geometry,
            layout,
        )
        self._require_fully_constrained(root_dogbone_sketch)

        connector_type = ConnectorType(self.inputs.connector.value)
        connector_sketches: list[adsk.fusion.Sketch] = []
        connector_specs: list[_CutSpec] = []
        connector_holes: list[_HoleSpec] = []
        if connector_type == ConnectorType.SCREW:
            (
                connector_sketches,
                connector_specs,
                connector_holes,
            ) = self._create_screw_sketches(
                component,
                geometry,
                layout,
            )
        elif connector_type.is_clamex or connector_type.is_cabineo:
            (
                connector_sketches,
                connector_specs,
                connector_holes,
            ) = self._create_lamello_sketches(
                component,
                geometry,
                layout,
                connector_type,
            )
        for sketch in connector_sketches:
            self._require_fully_constrained(sketch)

        last_feature = self._create_join_combine(
            component,
            self._target_body(component, "tenon"),
            tenon_tools,
        )
        tenon_body = self._target_body(component, "tenon")
        last_feature = self._create_to_entity_extrude(
            component=component,
            sketch=root_dogbone_sketch,
            target_body=tenon_body,
            target_entity=tenon_body,
            direction=tenon_through_direction,
            offset_expression=None,
            operation=adsk.fusion.FeatureOperations.CutFeatureOperation,  # type: ignore
            name="Tenons - Root Dog Bone Cut",
            parameter_role="rootDogBoneDepth",
        )
        last_feature = self._create_to_entity_extrude(
            component=component,
            sketch=mortise_sketch,
            target_body=self._target_body(component, "mortise"),
            target_entity=geometry.mortise_opposite_face,
            direction=mortise_cut_direction,
            offset_expression=(
                f"({self.inputs.mortise_depth_offset.expression}) - "
                f"({self.inputs.remaining_material.expression})"
            ),
            operation=adsk.fusion.FeatureOperations.CutFeatureOperation,  # type: ignore
            name="Tenons - Mortise Cut",
            parameter_role="mortiseDepth",
        )
        for spec in connector_specs:
            target_body = self._target_body(component, spec.body_role)
            if spec.distance is None:
                last_feature = self._create_to_entity_extrude(
                    component=component,
                    sketch=spec.sketch,
                    target_body=target_body,
                    target_entity=target_body,
                    direction=spec.direction,
                    offset_expression=None,
                    operation=adsk.fusion.FeatureOperations.CutFeatureOperation,  # type: ignore
                    name=spec.name,
                    parameter_role=spec.parameter_role,
                )
            else:
                last_feature = self._create_distance_extrude(
                    component=component,
                    sketch=spec.sketch,
                    target_body=target_body,
                    direction=spec.direction,
                    distance=spec.distance,
                    operation=adsk.fusion.FeatureOperations.CutFeatureOperation,  # type: ignore
                    name=spec.name,
                    parameter_role=spec.parameter_role,
                )
        for hole_spec in connector_holes:
            last_feature = self._create_hole_feature(
                component,
                hole_spec,
                self._target_body(component, hole_spec.body_role),
            )

        self._group_features(
            component,
            layout.context.sketch,
            last_feature,
        )

    def _validation_error(self) -> str | None:
        design = adsk.fusion.Design.cast(self.app.activeProduct)
        if not design:
            return "An active Fusion design is required."
        if design.designType != adsk.fusion.DesignTypes.ParametricDesignType:  # type: ignore
            return "Tenons requires Design History (a parametric design)."
        if not self.inputs or len(self.inputs.edge.value) != 1:
            return "Select one straight edge."

        selected = adsk.fusion.BRepEdge.cast(self.inputs.edge.value[0])
        if not selected or not utils.brep.is_linear(selected):
            return "The selected entity must be a straight BRep edge."
        if not selected.body.isSolid:
            return "The selected edge must belong to a solid body."
        if selected.faces.count != 2 or not all(
            utils.brep.is_planar(face) for face in selected.faces
        ):
            return "The selected edge must join two planar faces."

        try:
            geometry = self._resolve_geometry()
            positions = self._tenon_positions(geometry.edge)
        except Exception as exc:
            return str(exc)
        if geometry.tenon_face.body.parentComponent != design.activeComponent:
            return (
                "Activate the component that owns the selected edge, then run "
                "Tenons again."
            )
        if geometry.mortise_face.body.parentComponent != design.activeComponent:
            return "Both board bodies must be in the active component."
        if geometry.tenon_face.body == geometry.mortise_face.body:
            return "The mortises must be cut into a second solid body."

        if self.inputs.width.value <= 0:
            return "Tenon Width must be greater than zero."
        if self.inputs.tool_diameter.value <= 0:
            return "Tool Diameter must be greater than zero."
        if self.inputs.dog_bone_offset.value < 0:
            return "Dog Bone Offset cannot be negative."
        if self.inputs.distance_from_edge.value < 0:
            return "End Margin cannot be negative."
        if self.inputs.remaining_material.value < 0:
            return "Remaining Material cannot be negative."
        if (
            self.inputs.remaining_material.value
            >= geometry.mortise_thickness - 1e-6
        ):
            return (
                "Remaining Material must be smaller than the mortise-board "
                "thickness."
            )
        if self.inputs.mortise_length_offset.value <= 0:
            return "Mortise Length Offset must be greater than zero."
        if self.inputs.mortise_width_offset.value <= 0:
            return "Mortise Width Offset must be greater than zero."

        intervals = sorted(
            self._distance_from_edge_start(geometry.edge, point)
            for point in positions
        )
        half_width = self.inputs.width.value / 2
        if intervals[0] < half_width - 1e-6:
            return "The first tenon extends beyond the selected edge."
        if intervals[-1] > geometry.edge.length - half_width + 1e-6:
            return "The last tenon extends beyond the selected edge."
        if any(
            right - left < self.inputs.width.value - 1e-6
            for left, right in zip(intervals, intervals[1:])
        ):
            return "The selected tenon positions overlap."

        connector = ConnectorType(self.inputs.connector.value)
        if connector.is_clamex or connector.is_cabineo:
            minimum_gap = 12.0 if connector.is_clamex else 4.0
            gaps = [
                intervals[0] - half_width,
                *[
                    right - left - self.inputs.width.value
                    for left, right in zip(intervals, intervals[1:])
                ],
                geometry.edge.length - intervals[-1] - half_width,
            ]
            if min(gaps) < minimum_gap - 1e-6:
                return (
                    f"Every connector gap must be at least "
                    f"{minimum_gap * 10:g} mm."
                )
            if connector.is_clamex and (
                self.inputs.clamex_guide_hole_diameter.value <= 0
            ):
                return "Guide Hole Diameter must be greater than zero."
            if (
                connector.is_cabineo
                and self.inputs.cabineo_surface.value
                == CabineoSurface.ANTI_BREAK.value
                and self.inputs.cabineo_anti_break_depth.value <= 0
            ):
                return "Anti-Break Depth must be greater than zero."
        if connector == ConnectorType.SCREW:
            if self.inputs.screw_diameter.value <= 0:
                return "Screw Diameter must be greater than zero."
            if (
                self.inputs.mortise_screw.value == ScrewType.TWO_SIDES.value
                or self.inputs.tenon_screw.value == ScrewType.TWO_SIDES.value
            ) and self.inputs.screw_offset.value <= 0:
                return (
                    "Screw Offset must be greater than zero for two-sided "
                    "screws."
                )
            if (
                self.inputs.tenon_screw.value == ScrewType.TWO_SIDES.value
                and 2 * self.inputs.screw_offset.value
                >= self.inputs.width.value - 1e-6
            ):
                return (
                    "Screw Offset must be smaller than half the Tenon Width "
                    "for two-sided tenon screws."
                )
        if (
            connector == ConnectorType.CABINEO_8_M6
            and self.inputs.cabineo_insert_type.value
            == CabineoInsert.THREADED_INSERT.value
        ):
            values = [
                (self.inputs.threaded_insert_core_diameter.value, "Core Diameter"),
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

    def _resolve_geometry(self) -> _ResolvedGeometry:
        selected = cast(adsk.fusion.BRepEdge, self.inputs.edge.value[0])
        edge = cast(adsk.fusion.BRepEdge, selected.nativeObject or selected)
        faces = utils.brep.find_mating_faces_at_edge(edge)
        if not faces:
            raise ValueError(
                "Could not find a perpendicular mating board along this edge."
            )
        tenon_face, small_face, mortise_face = faces
        tenon_face = cast(
            adsk.fusion.BRepFace,
            tenon_face.nativeObject or tenon_face,
        )
        small_face = cast(
            adsk.fusion.BRepFace,
            small_face.nativeObject or small_face,
        )
        mortise_face = cast(
            adsk.fusion.BRepFace,
            mortise_face.nativeObject or mortise_face,
        )
        return _ResolvedGeometry(
            edge=edge,
            tenon_face=tenon_face,
            small_face=small_face,
            mortise_face=mortise_face,
            tenon_opposite_face=utils.brep.get_opposite_face(tenon_face),
            mortise_opposite_face=utils.brep.get_opposite_face(mortise_face),
            tenon_thickness=utils.brep.get_board_thickness(tenon_face),
            mortise_thickness=utils.brep.get_board_thickness(mortise_face),
        )

    def _tenon_positions(
        self,
        edge: adsk.fusion.BRepEdge,
    ) -> list[adsk.core.Point3D]:
        direction = utils.brep.normal_along_edge(edge)
        if (
            self.inputs.positioning.value
            == TenonsInputs.Positioning.POINTS.value
        ):
            if not self.inputs.points.value:
                raise ValueError("Select at least one Custom Point.")
            result = [
                utils.brep.project_point_onto_edge(
                    cast(adsk.fusion.SketchPoint, point).worldGeometry,
                    edge,
                )
                for point in self.inputs.points.value
            ]
            result.sort(
                key=lambda point: self._distance_from_edge_start(edge, point)
            )
            return result

        count = self.inputs.number_of_tenons.value
        if count == 1:
            distances = [edge.length / 2]
        else:
            available = (
                edge.length
                - 2 * self.inputs.distance_from_edge.value
                - self.inputs.width.value
            )
            if available <= 0:
                raise ValueError(
                    "End Margin and Tenon Width leave no room for placement."
                )
            pitch = available / (count - 1)
            distances = [
                self.inputs.distance_from_edge.value
                + self.inputs.width.value / 2
                + index * pitch
                for index in range(count)
            ]
        return [
            self._translated(edge.startVertex.geometry, direction, distance)
            for distance in distances
        ]

    def _sorted_custom_points(
        self,
        edge: adsk.fusion.BRepEdge,
    ) -> list[adsk.fusion.SketchPoint]:
        points = [
            cast(adsk.fusion.SketchPoint, point)
            for point in self.inputs.points.value
        ]
        points.sort(
            key=lambda point: self._distance_from_edge_start(
                edge,
                utils.brep.project_point_onto_edge(
                    point.worldGeometry,
                    edge,
                ),
            )
        )
        return points

    def _create_tenon_layout(
        self,
        component: adsk.fusion.Component,
        geometry: _ResolvedGeometry,
        positions: list[adsk.core.Point3D],
    ) -> _TenonLayout:
        edge = geometry.edge
        face = geometry.tenon_face
        rear_edge = utils.brep.closest_parallel_edge_of_face(
            edge,
            geometry.mortise_opposite_face,
        )
        if not rear_edge:
            raise RuntimeError(
                "Fusion could not find the rear edge of the mortise board."
            )
        sketch = component.sketches.addWithoutEdges(face)
        if not sketch:
            raise RuntimeError("Fusion failed to create 'Tenons - Layout'.")
        sketch.name = "Tenons - Layout"

        preprojected_points: list[adsk.fusion.SketchPoint] | None = None
        if (
            self.inputs.positioning.value
            == TenonsInputs.Positioning.POINTS.value
        ):
            preprojected_points = [
                self._project_point(sketch, point)
                for point in self._sorted_custom_points(edge)
            ]
        rear_line = self._project_line(sketch, rear_edge)
        rear_line.isConstruction = True
        context = self._finish_edge_context(
            sketch,
            edge,
            "tenon",
        )
        sketch.isComputeDeferred = True
        constraints = sketch.geometricConstraints
        centers = self._add_tenon_center_points(
            context,
            edge,
            positions,
            preprojected_points,
        )
        direction = utils.brep.normal_along_edge(edge)
        outward = self._opposite(
            utils.brep.normal_into_face(edge, face)
        )
        tenon_length = (
            geometry.mortise_thickness - self.inputs.remaining_material.value
        )
        bases: list[adsk.fusion.SketchLine] = []
        base_starts: list[adsk.fusion.SketchPoint] = []
        base_ends: list[adsk.fusion.SketchPoint] = []
        outers: list[adsk.fusion.SketchLine] = []
        outer_starts: list[adsk.fusion.SketchPoint] = []
        outer_ends: list[adsk.fusion.SketchPoint] = []
        first_base: adsk.fusion.SketchLine | None = None
        first_outer: adsk.fusion.SketchLine | None = None
        for index, (center, center_model) in enumerate(
            zip(centers, positions),
            start=1,
        ):
            half_width = self.inputs.width.value / 2
            start_model = self._translated(center_model, direction, -half_width)
            end_model = self._translated(center_model, direction, half_width)
            outer_start = self._translated(start_model, outward, tenon_length)
            outer_end = self._translated(end_model, outward, tenon_length)
            lines = sketch.sketchCurves.sketchLines
            base = lines.addByTwoPoints(
                sketch.modelToSketchSpace(start_model),
                sketch.modelToSketchSpace(end_model),
            )
            right = lines.addByTwoPoints(
                base.endSketchPoint,
                sketch.modelToSketchSpace(outer_end),
            )
            outer = lines.addByTwoPoints(
                right.endSketchPoint,
                sketch.modelToSketchSpace(outer_start),
            )
            left = lines.addByTwoPoints(
                outer.endSketchPoint,
                base.startSketchPoint,
            )
            if not all((base, right, outer, left)):
                raise RuntimeError("Fusion failed to create a tenon rectangle.")
            constraints.addCoincident(base.startSketchPoint, context.edge_line)
            constraints.addCoincident(base.endSketchPoint, context.edge_line)
            constraints.addMidPoint(center, base)
            constraints.addPerpendicular(right, base)
            constraints.addParallel(outer, base)
            constraints.addPerpendicular(left, base)
            if first_base is None:
                first_base = base
                self._add_line_length_dimension(
                    sketch,
                    base,
                    self.inputs.width.expression,
                    "tenonWidth",
                )
            else:
                constraints.addEqual(first_base, base)
            if first_outer is None:
                first_outer = outer
                if (
                    self.inputs.remaining_material.value
                    <= self.app.pointTolerance * 10
                ):
                    constraints.addCoincident(
                        outer.startSketchPoint,
                        rear_line,
                    )
                else:
                    self._add_offset_dimension(
                        sketch,
                        rear_line,
                        outer,
                        self.inputs.remaining_material.expression,
                        "tenonRemainingMaterial",
                    )
            else:
                constraints.addCollinear(first_outer, outer)
            bases.append(base)
            base_starts.append(base.startSketchPoint)
            base_ends.append(base.endSketchPoint)
            outers.append(outer)
            outer_starts.append(outer.startSketchPoint)
            outer_ends.append(outer.endSketchPoint)

        if (
            self.inputs.positioning.value
            == TenonsInputs.Positioning.NUMBER.value
            and len(bases) > 1
        ):
            if (
                self.inputs.distance_from_edge.value
                <= self.app.pointTolerance * 10
            ):
                # A zero End Margin cannot be expressed as a distance
                # dimension between coincident points.
                constraints.addCoincident(
                    bases[0].startSketchPoint,
                    context.edge_start,
                )
                constraints.addCoincident(
                    bases[-1].endSketchPoint,
                    context.edge_end,
                )
            else:
                start_margin = self._add_distance_dimension(
                    sketch,
                    context.edge_start,
                    bases[0].startSketchPoint,
                    self.inputs.distance_from_edge.expression,
                    "startMargin",
                )
                self._add_distance_dimension(
                    sketch,
                    bases[-1].endSketchPoint,
                    context.edge_end,
                    start_margin.parameter.name,
                    "endMargin",
                )
            if len(centers) > 2:
                # With two tenons the spacing is already determined by the
                # margins; a single span would stay unconstrained.
                spans: list[adsk.fusion.SketchLine] = []
                for left_center, right_center in zip(centers, centers[1:]):
                    span = sketch.sketchCurves.sketchLines.addByTwoPoints(
                        left_center,
                        right_center,
                    )
                    if not span:
                        raise RuntimeError(
                            "Fusion failed to create a tenon spacing line."
                        )
                    span.isConstruction = True
                    spans.append(span)
                for span in spans[1:]:
                    constraints.addEqual(spans[0], span)
        sketch.isComputeDeferred = False
        return _TenonLayout(
            context=context,
            centers=centers,
            center_model_points=positions,
            bases=bases,
            base_starts=base_starts,
            base_ends=base_ends,
            outers=outers,
            outer_starts=outer_starts,
            outer_ends=outer_ends,
        )

    def _add_tenon_center_points(
        self,
        context: _SketchContext,
        edge: adsk.fusion.BRepEdge,
        positions: list[adsk.core.Point3D],
        preprojected_points: list[adsk.fusion.SketchPoint] | None = None,
    ) -> list[adsk.fusion.SketchPoint]:
        sketch = context.sketch
        constraints = sketch.geometricConstraints
        if (
            self.inputs.positioning.value
            == TenonsInputs.Positioning.POINTS.value
        ):
            source_points = self._sorted_custom_points(edge)
            if (
                preprojected_points is None
                or len(preprojected_points) != len(source_points)
            ):
                raise RuntimeError(
                    "The Custom Point projections are incomplete."
                )
            result: list[adsk.fusion.SketchPoint] = []
            for projected, position in zip(
                preprojected_points,
                positions,
            ):
                projected_on_edge = sketch.modelToSketchSpace(position)
                if (
                    projected.geometry.distanceTo(projected_on_edge)
                    <= self.app.pointTolerance * 10
                ):
                    result.append(projected)
                    continue
                drop = sketch.sketchCurves.sketchLines.addByTwoPoints(
                    projected,
                    projected_on_edge,
                )
                if not drop:
                    raise RuntimeError(
                        "Fusion failed to project a Custom Point onto the edge."
                    )
                drop.isConstruction = True
                constraints.addPerpendicular(drop, context.edge_line)
                constraints.addCoincident(
                    drop.endSketchPoint,
                    context.edge_line,
                )
                result.append(drop.endSketchPoint)
            return result

        result = []
        for position in positions:
            point = sketch.sketchPoints.add(
                sketch.modelToSketchSpace(position)
            )
            if not point:
                raise RuntimeError(
                    "Fusion failed to create a tenon center point."
                )
            constraints.addCoincident(point, context.edge_line)
            result.append(point)
        if len(result) == 1:
            constraints.addMidPoint(result[0], context.edge_line)
        return result

    def _create_mortise_sketch(
        self,
        component: adsk.fusion.Component,
        geometry: _ResolvedGeometry,
        tenon_tools: list[adsk.fusion.BRepBody],
    ) -> adsk.fusion.Sketch:
        sketch = component.sketches.addWithoutEdges(geometry.small_face)
        if not sketch:
            raise RuntimeError("Fusion failed to create 'Tenons - Mortises'.")
        sketch.name = "Tenons - Mortises"
        projected_profiles = [
            self._project_tenon_profile(sketch, tool)
            for tool in tenon_tools
        ]
        context = self._finish_edge_context(
            sketch,
            geometry.edge,
            "mortise",
        )
        sketch = context.sketch
        sketch.isComputeDeferred = True
        rectangles = self._add_offset_mortise_rectangles(
            context,
            projected_profiles,
        )
        self._add_rectangle_dogbones(
            sketch,
            rectangles,
            context.edge_line,
            "mortiseDogBone",
            geometry.mortise_face.body,
            utils.brep.normal_away_from_body(geometry.small_face),
        )
        sketch.isComputeDeferred = False
        return sketch

    def _create_root_dogbone_sketch(
        self,
        component: adsk.fusion.Component,
        geometry: _ResolvedGeometry,
        layout: _TenonLayout,
    ) -> adsk.fusion.Sketch:
        context, projected_bases, _ = self._create_layout_reference_sketch(
            component,
            geometry.tenon_face,
            geometry.edge,
            layout,
            "Tenons - Root Dog Bones",
            "rootDogBone",
        )
        sketch = context.sketch
        sketch.isComputeDeferred = True
        outward = self._opposite(
            utils.brep.normal_into_face(
                geometry.edge,
                geometry.tenon_face,
            )
        )
        edge_direction = utils.brep.normal_along_edge(geometry.edge)
        corners: list[
            tuple[
                adsk.fusion.SketchPoint,
                adsk.core.Point3D,
                adsk.core.Vector3D,
            ]
        ] = []
        for center, (_, projected_start, projected_end) in zip(
            layout.center_model_points,
            projected_bases,
        ):
            corners.extend(
                [
                    (
                        projected_start,
                        self._translated(
                            center,
                            edge_direction,
                            -self.inputs.width.value / 2,
                        ),
                        self._opposite(edge_direction),
                    ),
                    (
                        projected_end,
                        self._translated(
                            center,
                            edge_direction,
                            self.inputs.width.value / 2,
                        ),
                        edge_direction,
                    ),
                ]
            )
        self._add_dogbone_circles_from_model_points(
            sketch,
            context.edge_line,
            corners,
            outward,
            "rootDogBone",
        )
        sketch.isComputeDeferred = False
        return sketch

    def _create_screw_sketches(
        self,
        component: adsk.fusion.Component,
        geometry: _ResolvedGeometry,
        layout: _TenonLayout,
    ) -> tuple[
        list[adsk.fusion.Sketch],
        list[_CutSpec],
        list[_HoleSpec],
    ]:
        sketches: list[adsk.fusion.Sketch] = []
        holes: list[_HoleSpec] = []
        mortise_type = ScrewType(self.inputs.mortise_screw.value)
        if mortise_type != ScrewType.NONE:
            context, projected_bases, _ = self._create_layout_reference_sketch(
                component,
                geometry.small_face,
                geometry.edge,
                layout,
                "Tenons - Mortise Screws",
                "mortiseScrew",
            )
            sketch = context.sketch
            sketch.isComputeDeferred = True
            if mortise_type == ScrewType.CENTERED:
                edge_points = self._gap_points_from_bases(
                    context,
                    projected_bases,
                )
            else:
                edge_points = self._two_sided_points(
                    context,
                    outside=True,
                    projected_bases=projected_bases,
                )
            centers = self._midpoints_across_small_face(
                context,
                edge_points,
                geometry.small_face,
                geometry.edge,
            )
            sketch.isComputeDeferred = False
            sketches.append(sketch)
            holes.append(
                _HoleSpec(
                    sketch=sketch,
                    body_role="mortise",
                    direction=utils.brep.normal_away_from_body(
                        geometry.small_face
                    ),
                    center_points=centers,
                    diameter_expression=self.inputs.screw_diameter.expression,
                    depth=None,
                    name="Tenons - Mortise Screw Holes",
                    parameter_role="mortiseScrew",
                )
            )

        tenon_type = ScrewType(self.inputs.tenon_screw.value)
        if tenon_type != ScrewType.NONE:
            (
                context,
                parameter_bases,
                parameter_outers,
            ) = self._create_layout_reference_sketch(
                component,
                geometry.tenon_face,
                geometry.edge,
                layout,
                "Tenons - Tenon Screws",
                "tenonScrew",
            )
            sketch = context.sketch
            sketch.isComputeDeferred = True
            if tenon_type == ScrewType.CENTERED:
                base_points = self._base_midpoints(context, parameter_bases)
            else:
                base_points = self._two_sided_points(
                    context,
                    outside=False,
                    projected_bases=parameter_bases,
                )
            centers = self._midpoints_to_projected_lines(
                context,
                base_points,
                parameter_outers,
                1 if tenon_type == ScrewType.CENTERED else 2,
            )
            sketch.isComputeDeferred = False
            sketches.append(sketch)
            holes.append(
                _HoleSpec(
                    sketch=sketch,
                    body_role="tenon",
                    direction=utils.brep.normal_towards_face(
                        geometry.tenon_face,
                        geometry.tenon_opposite_face,
                    ),
                    center_points=centers,
                    diameter_expression=self.inputs.screw_diameter.expression,
                    depth=None,
                    name="Tenons - Tenon Screw Holes",
                    parameter_role="tenonScrew",
                )
            )
        return sketches, [], holes

    def _create_lamello_sketches(
        self,
        component: adsk.fusion.Component,
        geometry: _ResolvedGeometry,
        layout: _TenonLayout,
        connector_type: ConnectorType,
    ) -> tuple[
        list[adsk.fusion.Sketch],
        list[_CutSpec],
        list[_HoleSpec],
    ]:
        sketches: list[adsk.fusion.Sketch] = []
        specs: list[_CutSpec] = []
        holes: list[_HoleSpec] = []
        (
            access_context,
            access_bases,
            _,
        ) = self._create_layout_reference_sketch(
            component,
            geometry.tenon_face,
            geometry.edge,
            layout,
            "Tenons - Connector Access",
            "connectorAccess",
        )
        access_context.sketch.isComputeDeferred = True
        access_points = self._gap_points_from_bases(
            access_context,
            access_bases,
        )
        (
            alignment_points,
            access_hole_centers,
            access_hole_diameter,
        ) = self._add_access_geometry(
            access_context,
            access_points,
            utils.brep.normal_into_face(
                geometry.edge,
                geometry.tenon_face,
            ),
            connector_type,
        )
        access_context.sketch.isComputeDeferred = False
        sketches.append(access_context.sketch)
        access_depth: str
        if connector_type.is_clamex:
            access_depth = self._real_length_expression(
                geometry.tenon_thickness / 2
            )
        else:
            access_depth = (
                "1.15 cm"
                if self.inputs.cabineo_surface.value
                == CabineoSurface.FLUSH.value
                else "1.1 cm"
            )
        access_direction = self._opposite(
            utils.brep.normal_away_from_body(geometry.tenon_face)
        )
        if access_hole_centers is None or access_hole_diameter is None:
            # Clamex P10 slots are not round; they stay a cut extrude.
            specs.append(
                _CutSpec(
                    sketch=access_context.sketch,
                    body_role="tenon",
                    direction=access_direction,
                    distance=access_depth,
                    name="Tenons - Connector Access Cut",
                    parameter_role="connectorAccessDepth",
                )
            )
        else:
            holes.append(
                _HoleSpec(
                    sketch=access_context.sketch,
                    body_role="tenon",
                    direction=access_direction,
                    center_points=access_hole_centers,
                    diameter_expression=access_hole_diameter,
                    depth=access_depth,
                    name="Tenons - Connector Access Holes",
                    parameter_role="connectorAccess",
                )
            )

        surface = CabineoSurface(self.inputs.cabineo_surface.value)
        if connector_type.is_cabineo and surface != CabineoSurface.NONE:
            relief_context, relief_bases, _ = (
                self._create_layout_reference_sketch(
                    component,
                    geometry.tenon_face,
                    geometry.edge,
                    layout,
                    "Tenons - Connector Relief",
                    "connectorRelief",
                )
            )
            relief_context.sketch.isComputeDeferred = True
            relief_points = self._gap_points_from_bases(
                relief_context,
                relief_bases,
            )
            (
                relief_hole_centers,
                relief_hole_diameter,
            ) = self._add_access_relief_geometry(
                relief_context,
                relief_points,
                utils.brep.normal_into_face(
                    geometry.edge,
                    geometry.tenon_face,
                ),
                surface,
            )
            relief_context.sketch.isComputeDeferred = False
            sketches.append(relief_context.sketch)
            relief_depth = (
                self.inputs.cabineo_anti_break_depth.expression
                if surface == CabineoSurface.ANTI_BREAK
                else "0.08 cm"
            )
            if relief_hole_centers is None or relief_hole_diameter is None:
                # Flush relief slots are not round; they stay a cut extrude.
                specs.append(
                    _CutSpec(
                        sketch=relief_context.sketch,
                        body_role="tenon",
                        direction=access_direction,
                        distance=relief_depth,
                        name="Tenons - Connector Relief Cut",
                        parameter_role="connectorReliefDepth",
                    )
                )
            else:
                holes.append(
                    _HoleSpec(
                        sketch=relief_context.sketch,
                        body_role="tenon",
                        direction=access_direction,
                        center_points=relief_hole_centers,
                        diameter_expression=relief_hole_diameter,
                        depth=relief_depth,
                        name="Tenons - Connector Relief Holes",
                        parameter_role="connectorRelief",
                    )
                )

        guide_hole = self._guide_hole(connector_type)
        guide_context, projected_alignment = (
            self._create_projected_points_edge_sketch(
                component,
                geometry.small_face,
                geometry.edge,
                alignment_points,
                "Tenons - Connector Opposite Holes",
                "connectorGuide",
            )
        )
        guide_context.sketch.isComputeDeferred = True
        guide_centers = self._add_guide_geometry(
            guide_context,
            projected_alignment,
            geometry.small_face,
            geometry.edge,
            utils.brep.normal_along_edge(geometry.edge),
            utils.brep.normal_into_face(
                geometry.edge,
                geometry.small_face,
            ),
            connector_type,
            guide_hole,
        )
        guide_context.sketch.isComputeDeferred = False
        sketches.append(guide_context.sketch)
        guide_direction = utils.brep.normal_away_from_body(
            geometry.small_face
        )
        holes.append(
            _HoleSpec(
                sketch=guide_context.sketch,
                body_role="mortise",
                direction=guide_direction,
                center_points=guide_centers,
                diameter_expression=guide_hole.diameter_expression,
                depth=(
                    None
                    if self.inputs.through_guide_holes.value
                    else guide_hole.depth
                ),
                name="Tenons - Connector Opposite Holes",
                parameter_role="connectorGuide",
            )
        )

        if (
            guide_hole.collar_depth is not None
            and guide_hole.collar_diameter_expression is not None
        ):
            collar_context, collar_centers = (
                self._create_projected_points_edge_sketch(
                    component,
                    geometry.small_face,
                    geometry.edge,
                    guide_centers,
                    "Tenons - Connector Insert Collars",
                    "connectorCollar",
                )
            )
            sketches.append(collar_context.sketch)
            holes.append(
                _HoleSpec(
                    sketch=collar_context.sketch,
                    body_role="mortise",
                    direction=guide_direction,
                    center_points=collar_centers,
                    diameter_expression=(
                        guide_hole.collar_diameter_expression
                    ),
                    depth=guide_hole.collar_depth,
                    name="Tenons - Connector Insert Collar Holes",
                    parameter_role="connectorCollar",
                )
            )
        return sketches, specs, holes

    def _add_access_geometry(
        self,
        context: _SketchContext,
        position_points: list[adsk.fusion.SketchPoint],
        inward: adsk.core.Vector3D,
        connector_type: ConnectorType,
    ) -> tuple[
        list[adsk.fusion.SketchPoint],
        list[adsk.fusion.SketchPoint] | None,
        str | None,
    ]:
        if connector_type == ConnectorType.CLAMEX_P14:
            centers = self._add_normal_points(
                context,
                position_points,
                inward,
                [0.75],
                ["0.75 cm"],
                "HoleInset",
            )
            # The round access holes are created as Hole features from
            # these constrained points.
            return centers, centers, "0.6 cm"
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
            slot_width_parameter: adsk.fusion.ModelParameter | None = None
            for index in range(0, len(centers), 2):
                width_expression = (
                    "0.6 cm"
                    if slot_width_parameter is None
                    else slot_width_parameter.name
                )
                dimension, centerline = self._add_center_to_center_slot(
                    context.sketch,
                    centers[index],
                    centers[index + 1],
                    width_expression,
                    f"connectorAccessSlot{index // 2 + 1}Width",
                )
                if slot_width_parameter is None:
                    slot_width_parameter = dimension.parameter
                midpoint = context.sketch.sketchPoints.add(
                    self._sketch_line_midpoint(centerline)
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
            return alignment_points, None, None
        centers = self._add_normal_points(
            context,
            position_points,
            inward,
            [0.36, 1.48, 2.6],
            ["0.36 cm", "1.48 cm", "2.6 cm"],
            "HoleInset",
        )
        alignment_points = [
            centers[index]
            for index in range(1, len(centers), 3)
        ]
        return alignment_points, centers, "1.5 cm"

    def _add_access_relief_geometry(
        self,
        context: _SketchContext,
        position_points: list[adsk.fusion.SketchPoint],
        inward: adsk.core.Vector3D,
        surface: CabineoSurface,
    ) -> tuple[list[adsk.fusion.SketchPoint] | None, str | None]:
        if surface == CabineoSurface.ANTI_BREAK:
            centers = self._add_normal_points(
                context,
                position_points,
                inward,
                [0.36, 1.48, 2.6],
                ["0.36 cm", "1.48 cm", "2.6 cm"],
                "HoleInset",
            )
            return centers, (
                "1.5 cm + 2 * "
                f"({self.inputs.cabineo_anti_break_distance.expression})"
            )
        top_centers = self._add_normal_points(
            context,
            position_points,
            inward,
            [2.6],
            ["2.6 cm"],
            "SlotCenter",
        )
        slot_width_parameter: adsk.fusion.ModelParameter | None = None
        for index, (bottom, top) in enumerate(
            zip(position_points, top_centers),
            start=1,
        ):
            width_expression = (
                "1.67 cm"
                if slot_width_parameter is None
                else slot_width_parameter.name
            )
            dimension, _ = self._add_center_to_center_slot(
                context.sketch,
                bottom,
                top,
                width_expression,
                f"connectorReliefSlot{index}Width",
            )
            if slot_width_parameter is None:
                slot_width_parameter = dimension.parameter
        return None, None

    def _add_guide_geometry(
        self,
        context: _SketchContext,
        alignment_points: list[adsk.fusion.SketchPoint],
        small_face: adsk.fusion.BRepFace,
        selected_edge: adsk.fusion.BRepEdge,
        edge_direction: adsk.core.Vector3D,
        inward: adsk.core.Vector3D,
        connector_type: ConnectorType,
        guide_hole: _GuideHole,
    ) -> list[adsk.fusion.SketchPoint]:
        if connector_type.is_clamex:
            centerline_points = self._midpoints_across_small_face(
                context,
                alignment_points,
                small_face,
                selected_edge,
            )
            centers: list[adsk.fusion.SketchPoint] = []
            first_centerline: adsk.fusion.SketchLine | None = None
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
                centerline = context.sketch.sketchCurves.sketchLines.addByTwoPoints(
                    context.sketch.modelToSketchSpace(first_model),
                    context.sketch.modelToSketchSpace(second_model),
                )
                if not centerline:
                    raise RuntimeError(
                        "Fusion failed to create a Clamex guide centerline."
                    )
                centerline.isConstruction = True
                context.sketch.geometricConstraints.addParallel(
                    centerline,
                    context.edge_line,
                )
                context.sketch.geometricConstraints.addMidPoint(
                    center,
                    centerline,
                )
                if first_centerline is None:
                    first_centerline = centerline
                    self._add_line_length_dimension(
                        context.sketch,
                        centerline,
                        "10.1 cm",
                        "connectorGuidePairSpacing",
                    )
                else:
                    context.sketch.geometricConstraints.addEqual(
                        first_centerline,
                        centerline,
                    )
                centers.extend(
                    [
                        centerline.startSketchPoint,
                        centerline.endSketchPoint,
                    ]
                )
            # The guide holes themselves are created as Hole features from
            # these constrained points.
            return centers

        return self._add_normal_points(
            context,
            alignment_points,
            inward,
            [guide_hole.edge_distance],
            [self._real_length_expression(guide_hole.edge_distance)],
            "HoleInset",
        )

    def _guide_hole(
        self,
        connector_type: ConnectorType,
    ) -> _GuideHole:
        if connector_type.is_clamex:
            # Through holes are handled by the caller with a to-body extent,
            # so the fixed depth here only applies to non-through holes.
            return _GuideHole(
                diameter=self.inputs.clamex_guide_hole_diameter.value,
                diameter_expression=(
                    self.inputs.clamex_guide_hole_diameter.expression
                ),
                depth="0.8 cm",
                edge_distance=0,
            )

        surface = CabineoSurface(self.inputs.cabineo_surface.value)
        edge_distance = 0.58 if surface == CabineoSurface.FLUSH else 0.5
        collar_diameter = None
        collar_expression = None
        collar_depth = None
        if connector_type == ConnectorType.CABINEO_8:
            diameter = 0.5
            diameter_expression = "0.5 cm"
            depth = "0.8 cm"
        elif connector_type == ConnectorType.CABINEO_12:
            diameter = 0.5
            diameter_expression = "0.5 cm"
            depth = "1.2 cm"
        else:
            insert = CabineoInsert(self.inputs.cabineo_insert_type.value)
            if insert == CabineoInsert.M6X123:
                diameter = 0.8
                diameter_expression = "0.8 cm"
                depth = "1.35 cm"
            elif insert == CabineoInsert.M6X153:
                diameter = 0.8
                diameter_expression = "0.8 cm"
                depth = "1.65 cm"
            else:
                diameter = self.inputs.threaded_insert_core_diameter.value
                diameter_expression = (
                    self.inputs.threaded_insert_core_diameter.expression
                )
                depth = self.inputs.threaded_insert_core_depth.expression
                collar_diameter = (
                    self.inputs.threaded_insert_collar_diameter.value
                )
                collar_expression = (
                    self.inputs.threaded_insert_collar_diameter.expression
                )
                collar_depth = self.inputs.threaded_insert_collar_depth.expression
        return _GuideHole(
            diameter=diameter,
            diameter_expression=diameter_expression,
            depth=depth,
            edge_distance=edge_distance,
            collar_diameter=collar_diameter,
            collar_diameter_expression=collar_expression,
            collar_depth=collar_depth,
        )

    def _finish_edge_context(
        self,
        sketch: adsk.fusion.Sketch,
        edge: adsk.fusion.BRepEdge,
        parameter_role: str,
        orientation_point: adsk.core.Point3D | None = None,
    ) -> _SketchContext:
        edge_line = self._project_line(sketch, edge)
        edge_line.isConstruction = True
        start_vertex = orientation_point or edge.startVertex.geometry
        edge_start = min(
            (edge_line.startSketchPoint, edge_line.endSketchPoint),
            key=lambda point: point.worldGeometry.distanceTo(start_vertex),
        )
        edge_end = (
            edge_line.endSketchPoint
            if edge_start == edge_line.startSketchPoint
            else edge_line.startSketchPoint
        )
        return _SketchContext(
            sketch=sketch,
            edge_line=edge_line,
            edge_start=edge_start,
            edge_end=edge_end,
            parameter_role=parameter_role,
        )

    def _create_layout_reference_sketch(
        self,
        component: adsk.fusion.Component,
        face: adsk.fusion.BRepFace,
        edge: adsk.fusion.BRepEdge,
        layout: _TenonLayout,
        name: str,
        parameter_role: str,
    ) -> tuple[
        _SketchContext,
        list[
            tuple[
                adsk.fusion.SketchLine,
                adsk.fusion.SketchPoint,
                adsk.fusion.SketchPoint,
            ]
        ],
        list[
            tuple[
                adsk.fusion.SketchLine,
                adsk.fusion.SketchPoint,
                adsk.fusion.SketchPoint,
            ]
        ],
    ]:
        sketch = component.sketches.addWithoutEdges(face)
        if not sketch:
            raise RuntimeError(f"Fusion failed to create '{name}'.")
        sketch.name = name

        projected_base_lines = [
            self._project_line(sketch, line)
            for line in layout.bases
        ]
        projected_outer_lines = [
            self._project_line(sketch, line)
            for line in layout.outers
        ]
        for line in [*projected_base_lines, *projected_outer_lines]:
            line.isConstruction = True
        context = self._finish_edge_context(
            sketch,
            edge,
            parameter_role,
        )
        bases = [
            self._oriented_projected_base(context, line)
            for line in projected_base_lines
        ]
        bases.sort(
            key=lambda item: self._distance_along_sketch_edge(
                context,
                item[1].geometry,
            )
        )
        outers = [
            self._oriented_projected_base(context, line)
            for line in projected_outer_lines
        ]
        outers.sort(
            key=lambda item: self._distance_along_sketch_edge(
                context,
                item[1].geometry,
            )
        )
        return context, bases, outers

    def _create_projected_points_edge_sketch(
        self,
        component: adsk.fusion.Component,
        face: adsk.fusion.BRepFace,
        edge: adsk.fusion.BRepEdge,
        source_points: list[adsk.fusion.SketchPoint],
        name: str,
        parameter_role: str,
    ) -> tuple[_SketchContext, list[adsk.fusion.SketchPoint]]:
        sketch = component.sketches.addWithoutEdges(face)
        if not sketch:
            raise RuntimeError(f"Fusion failed to create '{name}'.")
        sketch.name = name
        projected_points = [
            self._project_point(sketch, point)
            for point in source_points
        ]
        context = self._finish_edge_context(
            sketch,
            edge,
            parameter_role,
        )
        return context, projected_points

    def _project_tenon_profile(
        self,
        sketch: adsk.fusion.Sketch,
        tool_body: adsk.fusion.BRepBody,
    ) -> list[adsk.fusion.SketchLine]:
        projected = sketch.projectCutEdges(tool_body)
        lines = [
            line
            for entity in projected
            if (line := adsk.fusion.SketchLine.cast(entity))
        ]
        if len(lines) != 4:
            raise RuntimeError(
                "A native tenon did not project as a four-sided profile."
            )
        for line in lines:
            line.isConstruction = True
        return lines

    def _add_offset_mortise_rectangles(
        self,
        context: _SketchContext,
        projected_profiles: list[list[adsk.fusion.SketchLine]],
    ) -> list[
        tuple[
            adsk.fusion.SketchLine,
            adsk.fusion.SketchLine,
            adsk.fusion.SketchLine,
            adsk.fusion.SketchLine,
            adsk.fusion.SketchPoint,
        ]
    ]:
        sketch = context.sketch
        constraints = sketch.geometricConstraints
        edge_vector = context.edge_line.startSketchPoint.geometry.vectorTo(
            context.edge_line.endSketchPoint.geometry
        )
        if not edge_vector.normalize():
            raise RuntimeError("The projected edge has zero length.")
        normal = adsk.core.Vector3D.create(
            -edge_vector.y,
            edge_vector.x,
            0,
        )

        def coordinate(point: adsk.core.Point3D, axis) -> float:
            return point.x * axis.x + point.y * axis.y

        length_reference: str | None = None
        width_reference: str | None = None
        rectangles = []
        for index, projected in enumerate(projected_profiles, start=1):
            parallel: list[adsk.fusion.SketchLine] = []
            perpendicular: list[adsk.fusion.SketchLine] = []
            points: list[adsk.fusion.SketchPoint] = []
            for line in projected:
                line_vector = line.startSketchPoint.geometry.vectorTo(
                    line.endSketchPoint.geometry
                )
                if not line_vector.normalize():
                    raise RuntimeError(
                        "A projected tenon profile contains a zero-length line."
                    )
                if abs(line_vector.dotProduct(edge_vector)) > 0.9:
                    parallel.append(line)
                else:
                    perpendicular.append(line)
                points.extend(
                    [line.startSketchPoint, line.endSketchPoint]
                )
            if len(parallel) != 2 or len(perpendicular) != 2:
                raise RuntimeError(
                    "Fusion could not orient a projected tenon profile."
                )
            parallel.sort(
                key=lambda line: coordinate(
                    self._sketch_line_midpoint(line),
                    normal,
                )
            )
            perpendicular.sort(
                key=lambda line: coordinate(
                    self._sketch_line_midpoint(line),
                    edge_vector,
                )
            )
            min_u = min(coordinate(point.geometry, edge_vector) for point in points)
            max_u = max(coordinate(point.geometry, edge_vector) for point in points)
            min_v = min(coordinate(point.geometry, normal) for point in points)
            max_v = max(coordinate(point.geometry, normal) for point in points)
            origin = adsk.core.Point3D.create(0, 0, 0)

            def at(u: float, v: float) -> adsk.core.Point3D:
                point = self._translated(origin, edge_vector, u)
                return self._translated(point, normal, v)

            length_offset = self.inputs.mortise_length_offset.value / 2
            width_offset = self.inputs.mortise_width_offset.value / 2
            lower_left = at(min_u - length_offset, min_v - width_offset)
            lower_right = at(max_u + length_offset, min_v - width_offset)
            upper_right = at(max_u + length_offset, max_v + width_offset)
            upper_left = at(min_u - length_offset, max_v + width_offset)
            lines = sketch.sketchCurves.sketchLines
            lower = lines.addByTwoPoints(lower_left, lower_right)
            right = lines.addByTwoPoints(lower.endSketchPoint, upper_right)
            upper = lines.addByTwoPoints(right.endSketchPoint, upper_left)
            left = lines.addByTwoPoints(
                upper.endSketchPoint,
                lower.startSketchPoint,
            )
            diagonal = lines.addByTwoPoints(
                lower.startSketchPoint,
                right.endSketchPoint,
            )
            if not all((lower, right, upper, left, diagonal)):
                raise RuntimeError(
                    "Fusion failed to create an offset mortise rectangle."
                )
            diagonal.isConstruction = True
            constraints.addParallel(lower, context.edge_line)
            constraints.addPerpendicular(right, lower)
            constraints.addParallel(upper, lower)
            constraints.addPerpendicular(left, lower)
            length_expression = (
                f"({self.inputs.mortise_length_offset.expression}) / 2"
                if length_reference is None
                else length_reference
            )
            left_dimension = self._add_offset_dimension(
                sketch,
                perpendicular[0],
                left,
                length_expression,
                f"mortise{index}LeftOffset",
            )
            if length_reference is None:
                length_reference = left_dimension.parameter.name
            self._add_offset_dimension(
                sketch,
                perpendicular[1],
                right,
                length_reference,
                f"mortise{index}RightOffset",
            )
            width_expression = (
                f"({self.inputs.mortise_width_offset.expression}) / 2"
                if width_reference is None
                else width_reference
            )
            lower_dimension = self._add_offset_dimension(
                sketch,
                parallel[0],
                lower,
                width_expression,
                f"mortise{index}LowerOffset",
            )
            if width_reference is None:
                width_reference = lower_dimension.parameter.name
            self._add_offset_dimension(
                sketch,
                parallel[1],
                upper,
                width_reference,
                f"mortise{index}UpperOffset",
            )
            center = sketch.sketchPoints.add(
                self._sketch_line_midpoint(diagonal)
            )
            if not center:
                raise RuntimeError(
                    "Fusion failed to create a mortise center point."
                )
            constraints.addMidPoint(center, diagonal)
            rectangles.append((lower, right, upper, left, center))
        return rectangles

    def _oriented_projected_base(
        self,
        context: _SketchContext,
        base: adsk.fusion.SketchLine,
    ) -> tuple[
        adsk.fusion.SketchLine,
        adsk.fusion.SketchPoint,
        adsk.fusion.SketchPoint,
    ]:
        start = min(
            (base.startSketchPoint, base.endSketchPoint),
            key=lambda point: self._distance_along_sketch_edge(
                context,
                point.geometry,
            ),
        )
        end = (
            base.endSketchPoint
            if start == base.startSketchPoint
            else base.startSketchPoint
        )
        return base, start, end

    def _add_rectangle_dogbones(
        self,
        sketch: adsk.fusion.Sketch,
        rectangles: list[
            tuple[
                adsk.fusion.SketchLine,
                adsk.fusion.SketchLine,
                adsk.fusion.SketchLine,
                adsk.fusion.SketchLine,
                adsk.fusion.SketchPoint,
            ]
        ],
        edge_line: adsk.fusion.SketchLine,
        parameter_role: str,
        target_body: adsk.fusion.BRepBody,
        into_body: adsk.core.Vector3D,
    ) -> None:
        constraints = sketch.geometricConstraints
        offset = self.inputs.tool_diameter.value / (2 * math.sqrt(2))
        first_circle: adsk.fusion.SketchCircle | None = None
        first_offset: adsk.fusion.SketchLine | None = None
        for rectangle_index, (lower, right, upper, left, _) in enumerate(
            rectangles,
            start=1,
        ):
            corners = [
                (
                    lower.startSketchPoint,
                    lower.endSketchPoint,
                    left.startSketchPoint,
                ),
                (
                    lower.endSketchPoint,
                    lower.startSketchPoint,
                    right.endSketchPoint,
                ),
                (
                    right.endSketchPoint,
                    upper.endSketchPoint,
                    right.startSketchPoint,
                ),
                (
                    upper.endSketchPoint,
                    right.endSketchPoint,
                    left.endSketchPoint,
                ),
            ]
            for corner_index, (corner, x_inside, y_inside) in enumerate(
                corners,
                start=1,
            ):
                x_in = corner.geometry.vectorTo(x_inside.geometry)
                y_in = corner.geometry.vectorTo(y_inside.geometry)
                x_in.normalize()
                y_in.normalize()
                if not self._corner_needs_dogbone(
                    sketch,
                    corner.geometry,
                    x_in,
                    y_in,
                    target_body,
                    into_body,
                ):
                    # The mortise breaks out of the board here, so the tool
                    # can enter from the open side and no relief is needed.
                    # Cutting one anyway would notch the mating surface.
                    continue
                step_point = self._translated(
                    corner.geometry,
                    x_in,
                    offset,
                )
                center_point = self._translated(
                    step_point,
                    y_in,
                    offset,
                )
                x_step = sketch.sketchCurves.sketchLines.addByTwoPoints(
                    corner,
                    step_point,
                )
                y_step = sketch.sketchCurves.sketchLines.addByTwoPoints(
                    x_step.endSketchPoint,
                    center_point,
                )
                if not x_step or not y_step:
                    raise RuntimeError(
                        "Fusion failed to create a mortise dog-bone center."
                    )
                x_step.isConstruction = True
                y_step.isConstruction = True
                constraints.addParallel(x_step, edge_line)
                constraints.addPerpendicular(y_step, edge_line)
                if first_offset is None:
                    first_offset = x_step
                    self._add_line_length_dimension(
                        sketch,
                        x_step,
                        (
                            f"({self.inputs.tool_diameter.expression}) / "
                            f"(2 * sqrt(2))"
                        ),
                        f"{parameter_role}CenterOffset",
                    )
                else:
                    constraints.addEqual(first_offset, x_step)
                constraints.addEqual(first_offset, y_step)
                circle = sketch.sketchCurves.sketchCircles.addByCenterRadius(
                    y_step.endSketchPoint.geometry,
                    (
                        self.inputs.tool_diameter.value
                        + self.inputs.dog_bone_offset.value
                    )
                    / 2,
                )
                if not circle:
                    raise RuntimeError(
                        "Fusion failed to create a mortise dog-bone circle."
                    )
                constraints.addCoincident(
                    circle.centerSketchPoint,
                    y_step.endSketchPoint,
                )
                if first_circle is None:
                    first_circle = circle
                    self._add_circle_diameter_dimension(
                        sketch,
                        circle,
                        (
                            f"({self.inputs.tool_diameter.expression}) + "
                            f"({self.inputs.dog_bone_offset.expression})"
                        ),
                        f"{parameter_role}Diameter",
                    )
                else:
                    constraints.addEqual(first_circle, circle)

    def _corner_needs_dogbone(
        self,
        sketch: adsk.fusion.Sketch,
        corner: adsk.core.Point3D,
        x_in: adsk.core.Vector3D,
        y_in: adsk.core.Vector3D,
        target_body: adsk.fusion.BRepBody,
        into_body: adsk.core.Vector3D,
    ) -> bool:
        # Probe slightly outside the rectangle corner (along the outward
        # diagonal) and slightly into the board (the sketch plane lies on
        # the board surface): only corners embedded in material need a
        # relief.
        outward = adsk.core.Vector3D.create(
            -(x_in.x + y_in.x),
            -(x_in.y + y_in.y),
            0,
        )
        if not outward.normalize():
            return True
        epsilon = max(self.app.pointTolerance * 100, 0.01)
        probe = corner.copy()
        translation = outward.copy()
        translation.scaleBy(epsilon)
        probe.translateBy(translation)
        probe_model = sketch.sketchToModelSpace(probe)
        depth_offset = into_body.copy()
        depth_offset.scaleBy(epsilon)
        probe_model.translateBy(depth_offset)
        return (
            target_body.pointContainment(probe_model)
            == adsk.fusion.PointContainment.PointInsidePointContainment
        )

    def _add_dogbone_circles_from_model_points(
        self,
        sketch: adsk.fusion.Sketch,
        edge_line: adsk.fusion.SketchLine,
        corners: list[
            tuple[
                adsk.fusion.SketchPoint,
                adsk.core.Point3D,
                adsk.core.Vector3D,
            ]
        ],
        inward: adsk.core.Vector3D,
        parameter_role: str,
    ) -> None:
        constraints = sketch.geometricConstraints
        offset = self.inputs.tool_diameter.value / (2 * math.sqrt(2))
        first_circle: adsk.fusion.SketchCircle | None = None
        first_offset: adsk.fusion.SketchLine | None = None
        for index, (corner, model_point, along) in enumerate(corners, start=1):
            step_model = self._translated(model_point, along, offset)
            center_model = self._translated(step_model, inward, offset)
            along_step = sketch.sketchCurves.sketchLines.addByTwoPoints(
                corner.geometry,
                sketch.modelToSketchSpace(step_model),
            )
            if not along_step:
                raise RuntimeError(
                    "Fusion failed to create a root dog-bone edge offset."
                )
            inward_step = sketch.sketchCurves.sketchLines.addByTwoPoints(
                along_step.endSketchPoint.geometry,
                sketch.modelToSketchSpace(center_model),
            )
            if not inward_step:
                raise RuntimeError(
                    "Fusion failed to create a root dog-bone center."
                )
            along_step.isConstruction = True
            inward_step.isConstruction = True
            constraints.addCoincident(
                along_step.startSketchPoint,
                corner,
            )
            constraints.addCoincident(
                inward_step.startSketchPoint,
                along_step.endSketchPoint,
            )
            constraints.addParallel(along_step, edge_line)
            constraints.addPerpendicular(inward_step, edge_line)
            if first_offset is None:
                first_offset = along_step
                self._add_line_length_dimension(
                    sketch,
                    along_step,
                    (
                        f"({self.inputs.tool_diameter.expression}) / "
                        f"(2 * sqrt(2))"
                    ),
                    f"{parameter_role}CenterOffset",
                )
            else:
                constraints.addEqual(first_offset, along_step)
            constraints.addEqual(first_offset, inward_step)
            circle = sketch.sketchCurves.sketchCircles.addByCenterRadius(
                inward_step.endSketchPoint.geometry,
                (
                    self.inputs.tool_diameter.value
                    + self.inputs.dog_bone_offset.value
                )
                / 2,
            )
            if not circle:
                raise RuntimeError(
                    "Fusion failed to create a root dog-bone circle."
                )
            constraints.addCoincident(
                circle.centerSketchPoint,
                inward_step.endSketchPoint,
            )
            if first_circle is None:
                first_circle = circle
                self._add_circle_diameter_dimension(
                    sketch,
                    circle,
                    (
                        f"({self.inputs.tool_diameter.expression}) + "
                        f"({self.inputs.dog_bone_offset.expression})"
                    ),
                    f"{parameter_role}Diameter",
                )
            else:
                constraints.addEqual(first_circle, circle)

    def _gap_points_from_bases(
        self,
        context: _SketchContext,
        projected_bases: list[
            tuple[
                adsk.fusion.SketchLine,
                adsk.fusion.SketchPoint,
                adsk.fusion.SketchPoint,
            ]
        ],
    ) -> list[adsk.fusion.SketchPoint]:
        starts = [start for _, start, _ in projected_bases]
        ends = [end for _, _, end in projected_bases]
        boundaries = [
            (context.edge_start, starts[0]),
            *list(zip(ends[:-1], starts[1:])),
            (ends[-1], context.edge_end),
        ]
        result = []
        constraints = context.sketch.geometricConstraints
        for first, second in boundaries:
            gap = context.sketch.sketchCurves.sketchLines.addByTwoPoints(
                first.geometry,
                second.geometry,
            )
            if not gap:
                raise RuntimeError(
                    "Fusion failed to create a connector gap reference."
                )
            gap.isConstruction = True
            constraints.addCoincident(gap.startSketchPoint, first)
            constraints.addCoincident(gap.endSketchPoint, second)
            midpoint = context.sketch.sketchPoints.add(
                adsk.core.Point3D.create(
                    (first.geometry.x + second.geometry.x) / 2,
                    (first.geometry.y + second.geometry.y) / 2,
                    0,
                )
            )
            if not midpoint:
                raise RuntimeError(
                    "Fusion failed to create a connector position."
                )
            constraints.addMidPoint(midpoint, gap)
            result.append(midpoint)
        return result

    def _base_midpoints(
        self,
        context: _SketchContext,
        projected_bases: list[
            tuple[
                adsk.fusion.SketchLine,
                adsk.fusion.SketchPoint,
                adsk.fusion.SketchPoint,
            ]
        ],
    ) -> list[adsk.fusion.SketchPoint]:
        result = []
        for projected, start, end in projected_bases:
            midpoint = context.sketch.sketchPoints.add(
                adsk.core.Point3D.create(
                    (start.geometry.x + end.geometry.x) / 2,
                    (start.geometry.y + end.geometry.y) / 2,
                    0,
                )
            )
            if not midpoint:
                raise RuntimeError(
                    "Fusion failed to create a projected tenon midpoint."
                )
            context.sketch.geometricConstraints.addMidPoint(
                midpoint,
                projected,
            )
            result.append(midpoint)
        return result

    def _project_opposite_edge(
        self,
        sketch: adsk.fusion.Sketch,
        small_face: adsk.fusion.BRepFace,
        selected_edge: adsk.fusion.BRepEdge,
    ) -> adsk.fusion.SketchLine:
        design = selected_edge.body.parentComponent.parentDesign
        resolved_edges = [
            edge
            for entity in design.findEntityByToken(selected_edge.entityToken)
            if (edge := adsk.fusion.BRepEdge.cast(entity))
        ]
        if resolved_edges:
            selected_edge = resolved_edges[0]
            small_face = min(
                (
                    face
                    for face in selected_edge.faces
                    if utils.brep.is_planar(face)
                ),
                key=lambda face: face.area,
            )
        selected_midpoint = utils.brep.edge_middle_point(selected_edge)
        candidates = [
            edge
            for edge in small_face.edges
            if (
                utils.brep.is_linear(edge)
                and utils.brep.is_parallel(edge, selected_edge)
                and utils.brep.edge_middle_point(edge).distanceTo(
                    selected_midpoint
                )
                > self.app.pointTolerance * 10
            )
        ]
        if not candidates:
            raise RuntimeError(
                "Could not find the opposite long edge of the small face."
            )
        opposite = max(
            candidates,
            key=lambda edge: utils.brep.edge_middle_point(edge).distanceTo(
                selected_midpoint
            ),
        )
        first = self._project_point(sketch, opposite.startVertex)
        second = self._project_point(sketch, opposite.endVertex)
        line = sketch.sketchCurves.sketchLines.addByTwoPoints(
            first.geometry,
            second.geometry,
        )
        if not line:
            raise RuntimeError(
                "Fusion failed to create the opposite-edge reference."
            )
        constraints = sketch.geometricConstraints
        constraints.addCoincident(line.startSketchPoint, first)
        constraints.addCoincident(line.endSketchPoint, second)
        line.isConstruction = True
        return line

    def _midpoints_across_small_face(
        self,
        context: _SketchContext,
        edge_points: list[adsk.fusion.SketchPoint],
        small_face: adsk.fusion.BRepFace,
        selected_edge: adsk.fusion.BRepEdge,
    ) -> list[adsk.fusion.SketchPoint]:
        was_deferred = context.sketch.isComputeDeferred
        if was_deferred:
            context.sketch.isComputeDeferred = False
        opposite = self._project_opposite_edge(
            context.sketch,
            small_face,
            selected_edge,
        )
        if was_deferred:
            context.sketch.isComputeDeferred = True
        constraints = context.sketch.geometricConstraints
        result = []
        for edge_point in edge_points:
            span = context.sketch.sketchCurves.sketchLines.addByTwoPoints(
                edge_point,
                self._sketch_line_midpoint(opposite),
            )
            if not span:
                raise RuntimeError(
                    "Fusion failed to create a small-face cross-line."
                )
            span.isConstruction = True
            constraints.addPerpendicular(span, context.edge_line)
            constraints.addCoincident(span.endSketchPoint, opposite)
            midpoint = context.sketch.sketchPoints.add(
                self._sketch_line_midpoint(span)
            )
            if not midpoint:
                raise RuntimeError(
                    "Fusion failed to create a small-face midpoint."
                )
            constraints.addMidPoint(midpoint, span)
            result.append(midpoint)
        return result

    def _midpoints_to_projected_lines(
        self,
        context: _SketchContext,
        base_points: list[adsk.fusion.SketchPoint],
        projected_lines: list[
            tuple[
                adsk.fusion.SketchLine,
                adsk.fusion.SketchPoint,
                adsk.fusion.SketchPoint,
            ]
        ],
        points_per_line: int,
    ) -> list[adsk.fusion.SketchPoint]:
        if len(base_points) != len(projected_lines) * points_per_line:
            raise RuntimeError(
                "Tenon screw points do not match the projected tenon tips."
            )
        constraints = context.sketch.geometricConstraints
        result = []
        for index, base_point in enumerate(base_points):
            target_line = projected_lines[index // points_per_line][0]
            span = context.sketch.sketchCurves.sketchLines.addByTwoPoints(
                base_point,
                self._sketch_line_midpoint(target_line),
            )
            if not span:
                raise RuntimeError(
                    "Fusion failed to create a tenon-center cross-line."
                )
            span.isConstruction = True
            constraints.addPerpendicular(span, context.edge_line)
            constraints.addCoincident(span.endSketchPoint, target_line)
            midpoint = context.sketch.sketchPoints.add(
                self._sketch_line_midpoint(span)
            )
            if not midpoint:
                raise RuntimeError(
                    "Fusion failed to create a tenon screw midpoint."
                )
            constraints.addMidPoint(midpoint, span)
            result.append(midpoint)
        return result

    def _two_sided_points(
        self,
        context: _SketchContext,
        outside: bool,
        projected_bases: list[
            tuple[
                adsk.fusion.SketchLine,
                adsk.fusion.SketchPoint,
                adsk.fusion.SketchPoint,
            ]
        ],
    ) -> list[adsk.fusion.SketchPoint]:
        edge_direction = context.edge_start.worldGeometry.vectorTo(
            context.edge_end.worldGeometry
        )
        if not edge_direction.normalize():
            raise RuntimeError("The referenced joint edge has zero length.")
        constraints = context.sketch.geometricConstraints
        points: list[adsk.fusion.SketchPoint] = []
        first_offset: adsk.fusion.SketchLine | None = None
        for _, start_ref, end_ref in projected_bases:
            directions = (
                (self._opposite(edge_direction), edge_direction)
                if outside
                else (edge_direction, self._opposite(edge_direction))
            )
            for reference, model, direction in (
                (start_ref, start_ref.worldGeometry, directions[0]),
                (end_ref, end_ref.worldGeometry, directions[1]),
            ):
                target_model = self._translated(
                    model,
                    direction,
                    self.inputs.screw_offset.value,
                )
                line = context.sketch.sketchCurves.sketchLines.addByTwoPoints(
                    reference,
                    context.sketch.modelToSketchSpace(target_model),
                )
                if not line:
                    raise RuntimeError(
                        "Fusion failed to create a screw offset reference."
                    )
                line.isConstruction = True
                constraints.addParallel(line, context.edge_line)
                if first_offset is None:
                    first_offset = line
                    self._add_line_length_dimension(
                        context.sketch,
                        line,
                        self.inputs.screw_offset.expression,
                        f"{context.parameter_role}Offset",
                    )
                else:
                    constraints.addEqual(first_offset, line)
                points.append(line.endSketchPoint)
        return points

    def _add_normal_points(
        self,
        context: _SketchContext,
        base_points: list[adsk.fusion.SketchPoint],
        normal: adsk.core.Vector3D,
        offsets: list[float],
        expressions: list[str],
        parameter_role: str,
    ) -> list[adsk.fusion.SketchPoint]:
        if not offsets or len(offsets) != len(expressions):
            raise ValueError("Each normal point needs a distance expression.")
        sketch = context.sketch
        constraints = sketch.geometricConstraints
        result: list[adsk.fusion.SketchPoint] = []
        farthest = max(range(len(offsets)), key=offsets.__getitem__)
        reference_lines: dict[int, adsk.fusion.SketchLine] = {}
        for item_index, base in enumerate(base_points, start=1):
            base_model = base.worldGeometry
            farthest_model = self._translated(
                base_model,
                normal,
                offsets[farthest],
            )
            normal_line = sketch.sketchCurves.sketchLines.addByTwoPoints(
                base,
                sketch.modelToSketchSpace(farthest_model),
            )
            if not normal_line:
                raise RuntimeError(
                    "Fusion failed to create a normal construction line."
            )
            normal_line.isConstruction = True
            constraints.addPerpendicular(normal_line, context.edge_line)
            if item_index == 1:
                self._add_line_length_dimension(
                    sketch,
                    normal_line,
                    expressions[farthest],
                    (
                        f"{context.parameter_role}{parameter_role}"
                        f"{farthest + 1}"
                    ),
                )
                reference_lines[farthest] = normal_line
            else:
                constraints.addEqual(reference_lines[farthest], normal_line)
            item_points: list[adsk.fusion.SketchPoint] = []
            for offset_index, (offset, expression) in enumerate(
                zip(offsets, expressions)
            ):
                if offset_index == farthest:
                    point = normal_line.endSketchPoint
                else:
                    offset_line = sketch.sketchCurves.sketchLines.addByTwoPoints(
                        base,
                        sketch.modelToSketchSpace(
                            self._translated(base_model, normal, offset)
                        ),
                    )
                    if not offset_line:
                        raise RuntimeError(
                            "Fusion failed to create a normal inset line."
                        )
                    offset_line.isConstruction = True
                    constraints.addPerpendicular(
                        offset_line,
                        context.edge_line,
                    )
                    if item_index == 1:
                        self._add_line_length_dimension(
                            sketch,
                            offset_line,
                            expression,
                            f"{context.parameter_role}{parameter_role}"
                            f"1_{offset_index + 1}",
                        )
                        reference_lines[offset_index] = offset_line
                    else:
                        constraints.addEqual(
                            reference_lines[offset_index],
                            offset_line,
                        )
                    point = offset_line.endSketchPoint
                item_points.append(point)
            result.extend(item_points)
        return result

    def _create_hole_feature(
        self,
        component: adsk.fusion.Component,
        spec: _HoleSpec,
        target_body: adsk.fusion.BRepBody,
    ) -> adsk.fusion.HoleFeature:
        if not spec.center_points:
            raise RuntimeError(
                f"'{spec.name}' requires at least one hole center."
            )
        hole_features = component.features.holeFeatures
        hole_input = hole_features.createSimpleInput(
            adsk.core.ValueInput.createByString(spec.diameter_expression)
        )
        if not hole_input:
            raise RuntimeError(f"Fusion failed to initialize '{spec.name}'.")
        if not hole_input.setPositionBySketchPoints(
            adsk.core.ObjectCollection.createWithArray(
                cast(list[adsk.core.Base], spec.center_points)
            )
        ):
            raise RuntimeError(
                f"Fusion rejected the positions of '{spec.name}'."
            )
        # The natural hole direction is opposite the sketch normal.
        sketch_normal = spec.sketch.xDirection.crossProduct(
            spec.sketch.yDirection
        )
        natural_direction = sketch_normal.copy()
        natural_direction.scaleBy(-1)
        hole_input.isDefaultDirection = (
            natural_direction.dotProduct(spec.direction) > 0
        )
        if spec.depth is None:
            # Through hole: cut to the far side of the target body instead
            # of a fixed depth.
            if not hole_input.setOneSideToExtent(
                target_body,
                False,
                spec.direction,
            ):
                raise RuntimeError(
                    f"Fusion rejected the to-body extent of '{spec.name}'."
                )
        else:
            if not hole_input.setDistanceExtent(
                adsk.core.ValueInput.createByString(spec.depth)
            ):
                raise RuntimeError(
                    f"Fusion rejected the depth of '{spec.name}'."
                )
            # Fixed-depth holes are always flat-bottomed to match the
            # geometry a router or Forstner bit produces.
            hole_input.tipAngle = adsk.core.ValueInput.createByString(
                "180 deg"
            )
        hole_input.participantBodies = [target_body]

        hole = hole_features.add(hole_input)
        if not hole:
            raise RuntimeError(f"Fusion failed to create '{spec.name}'.")
        hole.name = spec.name
        spec.sketch.isVisible = False

        if hole.holeDiameter:
            self._name_parameter(
                hole.holeDiameter,
                f"{spec.parameter_role}Diameter",
            )
        depth_extent = adsk.fusion.DistanceExtentDefinition.cast(
            hole.extentDefinition
        )
        if depth_extent and depth_extent.distance:
            self._name_parameter(
                depth_extent.distance,
                f"{spec.parameter_role}Depth",
            )
        if hole.tipAngle:
            self._name_parameter(
                hole.tipAngle,
                f"{spec.parameter_role}TipAngle",
            )
        return hole

    def _add_center_to_center_slot(
        self,
        sketch: adsk.fusion.Sketch,
        start: adsk.fusion.SketchPoint,
        end: adsk.fusion.SketchPoint,
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
            raise RuntimeError("Fusion failed to dimension a connector slot.")
        dimensions[0].parameter.expression = width_expression
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
                "Fusion failed to return the connector slot centerline."
            )
        return dimensions[0], centerlines[0]

    def _add_line_length_dimension(
        self,
        sketch: adsk.fusion.Sketch,
        line: adsk.fusion.SketchLine,
        expression: str,
        parameter_role: str,
    ) -> adsk.fusion.SketchLinearDimension:
        return self._add_distance_dimension(
            sketch,
            line.startSketchPoint,
            line.endSketchPoint,
            expression,
            parameter_role,
        )

    def _add_offset_dimension(
        self,
        sketch: adsk.fusion.Sketch,
        reference: adsk.fusion.SketchLine,
        line: adsk.fusion.SketchLine,
        expression: str,
        parameter_role: str,
    ) -> adsk.fusion.SketchOffsetDimension:
        text = self._sketch_line_midpoint(line)
        text.x += 0.2
        text.y += 0.2
        dimension = sketch.sketchDimensions.addOffsetDimension(
            reference,
            line,
            text,
        )
        if not dimension or not dimension.parameter:
            raise RuntimeError("Fusion failed to create an offset dimension.")
        dimension.parameter.expression = expression
        self._name_parameter(dimension.parameter, parameter_role)
        return dimension

    def _add_distance_dimension(
        self,
        sketch: adsk.fusion.Sketch,
        start: adsk.fusion.SketchPoint,
        end: adsk.fusion.SketchPoint,
        expression: str,
        parameter_role: str,
    ) -> adsk.fusion.SketchLinearDimension:
        text = adsk.core.Point3D.create(
            (start.geometry.x + end.geometry.x) / 2 + 0.2,
            (start.geometry.y + end.geometry.y) / 2 + 0.2,
            0,
        )
        dimension = sketch.sketchDimensions.addDistanceDimension(
            start,
            end,
            adsk.fusion.DimensionOrientations.AlignedDimensionOrientation,  # type: ignore
            text,
        )
        if not dimension or not dimension.parameter:
            raise RuntimeError("Fusion failed to create a distance dimension.")
        dimension.parameter.expression = expression
        self._name_parameter(dimension.parameter, parameter_role)
        return dimension

    def _add_circle_diameter_dimension(
        self,
        sketch: adsk.fusion.Sketch,
        circle: adsk.fusion.SketchCircle,
        expression: str,
        parameter_role: str,
    ) -> None:
        text = circle.centerSketchPoint.geometry.copy()
        text.x += max(circle.radius * 2, 0.5)
        text.y += max(circle.radius * 2, 0.5)
        dimension = sketch.sketchDimensions.addDiameterDimension(
            circle,
            text,
        )
        if not dimension or not dimension.parameter:
            raise RuntimeError("Fusion failed to dimension a circle.")
        dimension.parameter.expression = expression
        self._name_parameter(dimension.parameter, parameter_role)

    def _create_join_combine(
        self,
        component: adsk.fusion.Component,
        target_body: adsk.fusion.BRepBody,
        tool_bodies: list[adsk.fusion.BRepBody],
    ) -> adsk.fusion.CombineFeature:
        tools = adsk.core.ObjectCollection.createWithArray(
            cast(list[adsk.core.Base], tool_bodies)
        )
        combine_input = component.features.combineFeatures.createInput(
            target_body,
            tools,
        )
        if not combine_input:
            raise RuntimeError("Fusion failed to initialize the tenon join.")
        combine_input.operation = (
            adsk.fusion.FeatureOperations.JoinFeatureOperation  # type: ignore
        )
        combine_input.isKeepToolBodies = False
        combine = component.features.combineFeatures.add(combine_input)
        if not combine:
            raise RuntimeError("Fusion failed to join the tenons.")
        combine.name = "Tenons - Join"
        return combine

    def _create_to_entity_extrude(
        self,
        component: adsk.fusion.Component,
        sketch: adsk.fusion.Sketch,
        target_body: adsk.fusion.BRepBody,
        target_entity: adsk.core.Base,
        direction: adsk.core.Vector3D,
        offset_expression: str | None,
        operation,
        name: str,
        parameter_role: str,
    ) -> adsk.fusion.ExtrudeFeature:
        profiles = self._all_profiles(sketch)
        extrude_input = component.features.extrudeFeatures.createInput(
            profiles,
            operation,
        )
        if not extrude_input:
            raise RuntimeError(f"Fusion failed to initialize '{name}'.")
        if offset_expression is None:
            extent = adsk.fusion.ToEntityExtentDefinition.create(
                target_entity,
                False,
            )
        else:
            extent = adsk.fusion.ToEntityExtentDefinition.create(
                target_entity,
                False,
                adsk.core.ValueInput.createByString(offset_expression),
            )
        if not extent:
            raise RuntimeError(f"Fusion failed to define '{name}' extent.")
        extent.directionHint = direction
        if adsk.fusion.BRepBody.cast(target_entity):
            extent.isMinimumSolution = False
        if not extrude_input.setOneSideExtent(
            extent,
            self._extent_direction(sketch, direction),
        ):
            raise RuntimeError(f"Fusion rejected the extent of '{name}'.")
        if operation == adsk.fusion.FeatureOperations.CutFeatureOperation:  # type: ignore
            extrude_input.participantBodies = [target_body]
        extrude = component.features.extrudeFeatures.add(extrude_input)
        if (
            not extrude
            or (
                operation
                == adsk.fusion.FeatureOperations.NewBodyFeatureOperation  # type: ignore
                and extrude.bodies.count == 0
            )
        ):
            raise RuntimeError(f"Fusion failed to create '{name}'.")
        extrude.name = name
        sketch.isVisible = False
        final_extent = adsk.fusion.ToEntityExtentDefinition.cast(
            extrude.extentOne
        )
        if final_extent:
            offset = adsk.fusion.ModelParameter.cast(final_extent.offset)
            if offset:
                self._name_parameter(offset, f"{parameter_role}Offset")
        self._name_extrude_parameters(extrude, parameter_role)
        return extrude

    def _create_distance_extrude(
        self,
        component: adsk.fusion.Component,
        sketch: adsk.fusion.Sketch,
        target_body: adsk.fusion.BRepBody,
        direction: adsk.core.Vector3D,
        distance: float | str,
        operation,
        name: str,
        parameter_role: str,
    ) -> adsk.fusion.ExtrudeFeature:
        extrude_input = component.features.extrudeFeatures.createInput(
            self._all_profiles(sketch),
            operation,
        )
        if not extrude_input:
            raise RuntimeError(f"Fusion failed to initialize '{name}'.")
        value = (
            adsk.core.ValueInput.createByString(distance)
            if isinstance(distance, str)
            else adsk.core.ValueInput.createByReal(distance)
        )
        extent = adsk.fusion.DistanceExtentDefinition.create(value)
        if not extent:
            raise RuntimeError(f"Fusion failed to define '{name}' depth.")
        if not extrude_input.setOneSideExtent(
            extent,
            self._extent_direction(sketch, direction),
        ):
            raise RuntimeError(f"Fusion rejected the extent of '{name}'.")
        if operation == adsk.fusion.FeatureOperations.CutFeatureOperation:  # type: ignore
            extrude_input.participantBodies = [target_body]
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
        if extrude.taperAngleOne:
            self._name_parameter(
                extrude.taperAngleOne,
                f"{parameter_role}TaperAngle",
            )
        return extrude

    def _all_profiles(
        self,
        sketch: adsk.fusion.Sketch,
    ) -> adsk.core.ObjectCollection:
        profiles = adsk.core.ObjectCollection.create()
        for profile in sketch.profiles:
            profiles.add(profile)
        if profiles.count == 0:
            raise RuntimeError(f"'{sketch.name}' did not create any profiles.")
        return profiles

    def _name_extrude_parameters(
        self,
        extrude: adsk.fusion.ExtrudeFeature,
        role: str,
    ) -> None:
        if extrude.taperAngleOne:
            self._name_parameter(
                extrude.taperAngleOne,
                f"{role}TaperAngle",
            )

    def _project_line(
        self,
        sketch: adsk.fusion.Sketch,
        line: adsk.core.Base,
    ) -> adsk.fusion.SketchLine:
        projected = sketch.project2(
            cast(list[adsk.core.Base], [line]),
            True,
        )
        if len(projected) != 1:
            raise RuntimeError("Fusion failed to project a reference line.")
        result = adsk.fusion.SketchLine.cast(projected[0])
        if not result:
            raise RuntimeError("A projected reference is not a straight line.")
        return result

    def _project_point(
        self,
        sketch: adsk.fusion.Sketch,
        point: adsk.core.Base,
    ) -> adsk.fusion.SketchPoint:
        projected = sketch.project2(
            cast(list[adsk.core.Base], [point]),
            True,
        )
        if len(projected) != 1:
            raise RuntimeError("Fusion failed to project a reference point.")
        result = adsk.fusion.SketchPoint.cast(projected[0])
        if not result:
            raise RuntimeError("A projected reference is not a point.")
        return result

    def _sketch_line_midpoint(
        self,
        line: adsk.fusion.SketchLine,
    ) -> adsk.core.Point3D:
        return adsk.core.Point3D.create(
            (
                line.startSketchPoint.geometry.x
                + line.endSketchPoint.geometry.x
            )
            / 2,
            (
                line.startSketchPoint.geometry.y
                + line.endSketchPoint.geometry.y
            )
            / 2,
            0,
        )

    def _distance_along_sketch_edge(
        self,
        context: _SketchContext,
        point: adsk.core.Point3D,
    ) -> float:
        start = context.edge_start.geometry
        direction = start.vectorTo(context.edge_end.geometry)
        if not direction.normalize():
            raise RuntimeError("The projected selected edge has zero length.")
        return direction.dotProduct(start.vectorTo(point))

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

    def _target_body(
        self,
        component: adsk.fusion.Component,
        role: str,
    ) -> adsk.fusion.BRepBody:
        # Re-resolve via entity token: features created in between can
        # invalidate direct body references.
        entities = component.parentDesign.findEntityByToken(
            self._body_tokens[role]
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
            raise RuntimeError(f"Fusion could not re-resolve the {role} body.")
        return body

    def _unique_parameter_prefix(
        self,
        design: adsk.fusion.Design,
    ) -> str:
        names = {parameter.name for parameter in design.allParameters}
        base = "tenons"
        index = 1
        while True:
            candidate = base if index == 1 else f"{base}{index}"
            if not any(
                name.startswith(f"{candidate}_")
                for name in names
            ):
                return candidate
            index += 1

    def _name_parameter(
        self,
        parameter: adsk.fusion.ModelParameter,
        role: str,
    ) -> None:
        name = f"{self._parameter_prefix}_{role}"
        parameter.name = name
        if parameter.name != name:
            raise RuntimeError(
                f"Fusion did not accept the parameter name '{name}'."
            )

    def _require_fully_constrained(
        self,
        sketch: adsk.fusion.Sketch,
    ) -> None:
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
        unconstrained_curves = [
            curve
            for curve in sketch.sketchCurves
            if not curve.isFullyConstrained
        ]
        unconstrained_points = [
            point
            for point in sketch.sketchPoints
            if not point.isFullyConstrained
        ]
        raise RuntimeError(
            f"'{sketch.name}' is under-constrained "
            f"({len(unconstrained_curves)} curves and "
            f"{len(unconstrained_points)} points)."
        )

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
            group.name = "Tenons"
            group.isCollapsed = False

    def _distance_from_edge_start(
        self,
        edge: adsk.fusion.BRepEdge,
        point: adsk.core.Point3D,
    ) -> float:
        direction = utils.brep.normal_along_edge(edge)
        delta = edge.startVertex.geometry.vectorTo(point)
        return direction.dotProduct(delta)

    def _real_length_expression(self, value: float) -> str:
        return f"{value:.12g} cm"

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

    def _opposite(
        self,
        direction: adsk.core.Vector3D,
    ) -> adsk.core.Vector3D:
        result = direction.copy()
        result.scaleBy(-1)
        return result
