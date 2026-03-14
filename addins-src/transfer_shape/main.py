from lib import custom_compute_feature, inputs, combine, errors, utils, ui_placement
from lib.fusionbootstrap.runtime import RuntimeInfo
import adsk.core, adsk.fusion
from typing import cast

_feature: custom_compute_feature.CustomComputeFeature | None = None
DEBUG_KEEP_RESULT_SKETCH = True


def run(context, runtime_info: RuntimeInfo):
    global _feature
    _feature = TransferShape(runtime_info)


def stop(context):
    global _feature
    if _feature:
        _feature.shutdown()
    _feature = None


class TransferShapeInputs(inputs.Inputs):
    class Operations:
        JOIN = inputs.DropDownInput.Item("Join", 0)
        CUT = inputs.DropDownInput.Item("Cut", 1)
        INTERSECT = inputs.DropDownInput.Item("Intersect", 2)

    def __init__(self, units_manager: adsk.core.UnitsManager):
        units = units_manager.defaultLengthUnits
        self.target_face = inputs.SelectionByEntityTokenInput(
            id="targetFace",
            name="Target face",
            filter=["PlanarFaces"],
            lower_bound=1,
            upper_bound=1,
            tool_tip="Select the planar face of the body to modify.",
        )
        self.base_sketch = inputs.SelectionByEntityTokenInput(
            id="baseSketch",
            name="Sketch",
            filter=["Sketches"],
            lower_bound=0,
            upper_bound=1,
            tool_tip="Optional: select a sketch to project into the transfer sketch.",
        )
        self.intersect_faces = inputs.SelectionByEntityTokenInput(
            id="intersectFaces",
            name="Intersect faces",
            filter=["Faces"],
            lower_bound=0,
            upper_bound=0,
            tool_tip="Select faces to intersect with the temporary sketch plane.",
        )
        self.project_entities = inputs.SelectionByEntityTokenInput(
            id="projectGeometry",
            name="Project edges",
            filter=["Edges"],
            lower_bound=0,
            upper_bound=0,
            tool_tip="Select edges to project into the temporary sketch.",
        )
        self.heal_tolerance = inputs.FloatInput(
            id="healTolerance",
            name="Heal tolerance",
            default_value=3,
            tool_tip="Maximum endpoint distance for healing projected/intersected curves.",
            units=units,
        )
        self.close_loop = inputs.CheckboxInput(
            id="closeLoop",
            name="Close loop",
            default_value=False,
            tool_tip="Automatically close the transfer curve if start and end points are within the heal tolerance.",
        )
        self.offset = inputs.FloatInput(
            id="offset",
            name="Offset",
            default_value=0,
            tool_tip="Offset applied to the healed transfer curves.",
            units=units,
        )
        self.operation = inputs.DropDownInput(
            id="operation",
            name="Operation",
            options=[
                TransferShapeInputs.Operations.JOIN,
                TransferShapeInputs.Operations.CUT,
                TransferShapeInputs.Operations.INTERSECT,
            ],
            default_value=TransferShapeInputs.Operations.CUT.value,
            tool_tip="Boolean operation to apply with the generated transfer body.",
        )
        super().__init__()


class TransferShape(custom_compute_feature.CustomComputeFeature):
    inputs: TransferShapeInputs

    @property
    def plugin_name(self) -> str:
        return "Transfer Shape"

    @property
    def plugin_desc(self) -> str:
        return "Transfer intersected/projected shape onto a target body with heal and offset support."

    @property
    def plugin_tooltip(self) -> str:
        return "Transfer intersected/projected shape onto a target body with heal and offset support."

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

    def create_inputs(self) -> TransferShapeInputs:
        return TransferShapeInputs(self.app.activeProduct.unitsManager)

    def execute(self) -> list[combine.Combine]:
        selection = cast(list[adsk.fusion.BRepFace], self.inputs.target_face.value)
        if not selection:
            return []
        target_face = selection[0]

        if len(self.inputs.intersect_faces.value) == 0 and len(self.inputs.project_entities.value) == 0:
            return []

        temp_base: adsk.fusion.BaseFeature
        try:
            temp_base = self.component.features.baseFeatures.add()
            temp_base.startEdit()
            temp_sketch = self.component.sketches.addToBaseOrFormFeature(target_face, temp_base, includeFaceEdges=False)

            source_curves = self.intersect_transfer_faces(temp_sketch) + self.project_transfer_geometry(temp_sketch)
            rebuilt = utils.sketch.rebuild_curves_as_spline(
                curves=source_curves,
                sketch=temp_sketch,
                sample_spacing=0.35,
                min_fit_point_spacing=0.3,
                tolerance=self.inputs.heal_tolerance.value,
                close_loop=self.inputs.close_loop.value,
            )
            if not rebuilt:
                raise errors.InvalidInputError("Failed to resolve intersected/projected curves into a continuous spline.")

            for curve in source_curves:
                curve.deleteMe()

            if self.inputs.offset.value != 0:
                offset_curve = self.apply_offset(temp_sketch, rebuilt)
                if not offset_curve:
                    raise errors.InvalidInputError("Failed to apply offset to transfer curves.")
                rebuilt.deleteMe()
                rebuilt = offset_curve

            if base_sketch := self.selected_base_sketch():
                temp_sketch.project2(cast(list[adsk.core.Base], utils.fusion.as_list(base_sketch.sketchCurves)), isLinked=False)

            if DEBUG_KEEP_RESULT_SKETCH:
                temp_sketch.name = "Transfer Shape Debug Result"
                temp_base.finishEdit()
                return []

            if temp_sketch.profiles.count < 1:
                raise errors.InvalidInputError(
                    "No closed profile found after transfer. Ensure source geometry can form a closed loop."
                )

            profiles = utils.fusion.as_list(temp_sketch.profiles)
            profiles.sort(key=lambda p: p.areaProperties().area, reverse=True)
            largest_profile = profiles[0]
            opposite_face = utils.brep.get_opposite_face(target_face)
            transfer_body = utils.brep.create_body_from_profile_by_extrude(
                profile=largest_profile,
                base=temp_base,
                to_entity=opposite_face,
            )
            return [combine.Combine(target_face.body, transfer_body, self.selected_operation())]

        finally:
            temp_base.finishEdit()
            if not DEBUG_KEEP_RESULT_SKETCH:
                temp_base.deleteMe()

    def selected_base_sketch(self) -> adsk.fusion.Sketch | None:
        if self.inputs.base_sketch.value:
            return cast(adsk.fusion.Sketch, self.inputs.base_sketch.value[0])

    def intersect_transfer_faces(self, sketch: adsk.fusion.Sketch) -> list[adsk.fusion.SketchCurve]:
        selected_faces = cast(list[adsk.fusion.BRepFace], self.inputs.intersect_faces.value)
        if not selected_faces:
            return []
        created = sketch.intersectWithSketchPlane(cast(list[adsk.core.Base], selected_faces))
        intersected_curves = self.extract_sketch_curves(created)
        return intersected_curves

    def project_transfer_geometry(self, sketch: adsk.fusion.Sketch) -> list[adsk.fusion.SketchCurve]:
        entities = cast(list[adsk.fusion.BRepEdge], self.inputs.project_entities.value)
        if not entities:
            return []
        created = sketch.project2(cast(list[adsk.core.Base], entities), False)
        return self.extract_sketch_curves(created)

    def extract_sketch_curves(self, entities: list[adsk.fusion.SketchEntity]) -> list[adsk.fusion.SketchCurve]:
        return [e for e in entities if isinstance(e, adsk.fusion.SketchCurve)]

    def apply_offset(self, sketch: adsk.fusion.Sketch, curve: adsk.fusion.SketchCurve) -> adsk.fusion.SketchCurve:
        offset = self.inputs.offset.value
        offset_input = sketch.geometricConstraints.createOffsetInput([curve], adsk.core.ValueInput.createByReal(offset))
        offset_input.isTopologyMatched = False
        constraint = sketch.geometricConstraints.addOffset2(offset_input)
        if not constraint:
            raise errors.InvalidInputError("Offset did not produce any curves.")
        offset_curves = constraint.childCurves
        rebuilt = utils.sketch.rebuild_curves_as_spline(
            curves=offset_curves,
            sketch=sketch,
            sample_spacing=0.35,
            min_fit_point_spacing=0.3,
            tolerance=self.inputs.heal_tolerance.value,
            close_loop=self.inputs.close_loop.value,
        )
        if not rebuilt:
            raise errors.InvalidInputError("Failed to resolve offset curves into a continuous spline.")
        for curve in offset_curves:
            curve.deleteMe()
        return rebuilt

    def selected_operation(self) -> combine.Operation:
        value = self.inputs.operation.value
        if value == TransferShapeInputs.Operations.JOIN.value:
            return combine.Operation.JOIN
        if value == TransferShapeInputs.Operations.CUT.value:
            return combine.Operation.CUT
        if value == TransferShapeInputs.Operations.INTERSECT.value:
            return combine.Operation.INTERSECT
        raise errors.InvalidInputError("Unsupported combine operation selected.")
