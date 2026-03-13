from lib import custom_compute_feature, inputs, combine, errors, utils, ui_placement
from lib.fusionbootstrap.runtime import RuntimeInfo
import adsk.core, adsk.fusion
from typing import cast
from dataclasses import dataclass

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
            utils.fusion.log(len(source_curves))
            rebuilt = self.rebuild_curves_as_spline(temp_sketch, source_curves)
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
                temp_sketch.project2(cast(list[adsk.core.Base], utils.fusion.as_list(base_sketch.sketchCurves)), False)

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
            transfer_body = self.create_transfer_body_by_extrude(largest_profile, temp_base, opposite_face)
            return [combine.Combine(target_face.body, transfer_body, self.selected_operation())]
        
        finally:
            temp_base.finishEdit()
            if not DEBUG_KEEP_RESULT_SKETCH:
                temp_base.deleteMe()

    def sequenced_curves(self, curves: list[adsk.fusion.SketchCurve]) -> list[tuple[adsk.fusion.SketchCurve, bool]]:
        if not curves:
            return []
        tolerance = self.inputs.heal_tolerance.value
        remaining_curves = list(curves)
        ordered: list[tuple[adsk.fusion.SketchCurve, bool]] = []
        ordered.append((remaining_curves.pop(), False))
        while remaining_curves:
            first_curve = ordered[0]
            last_curve = ordered[-1]
            start_point = first_curve[0].startSketchPoint if not first_curve[1] else first_curve[0].endSketchPoint # type: ignore
            end_point = last_curve[0].endSketchPoint if not last_curve[1] else last_curve[0].startSketchPoint # type: ignore

            def find_next_curve(point: adsk.fusion.SketchPoint, curves: list[adsk.fusion.SketchCurve]) -> tuple[adsk.fusion.SketchCurve, adsk.fusion.SketchPoint, float] | None:
                candidates: list[tuple[float, adsk.fusion.SketchCurve, adsk.fusion.SketchPoint]] = []
                for curve in curves:
                    start = curve.startSketchPoint  # type: ignore
                    end = curve.endSketchPoint # type: ignore
                    dist = point.geometry.distanceTo(start.geometry)
                    if dist < tolerance:
                        candidates.append((dist, curve, start))
                    dist = point.geometry.distanceTo(end.geometry)
                    if dist < tolerance:
                        candidates.append((dist, curve, end))
                candidates.sort(key=lambda x: x[0])
                if not candidates:
                    return None
                return candidates[0][1], candidates[0][2], candidates[0][0]
            
            next = find_next_curve(end_point, remaining_curves)
            previous = find_next_curve(start_point, remaining_curves)

            if next and (not previous or next[2] <= previous[2]):
                flipped = next[1] == next[0].endSketchPoint # type: ignore
                ordered.append((next[0], flipped))
                remaining_curves.remove(next[0])
            elif previous:
                flipped = previous[1] == previous[0].startSketchPoint # type: ignore
                ordered.insert(0, (previous[0], flipped))
                remaining_curves.remove(previous[0])

            if not next and not previous:
                break
                    
        if remaining_curves:
            raise errors.InvalidInputError("Failed to sequence transfer curves into a continuous path.")
        return ordered

    def selected_base_sketch(self) -> adsk.fusion.Sketch | None:
        selection = cast(list[adsk.fusion.Sketch], self.inputs.base_sketch.value)
        if selection:
            return selection[0]

    def create_transfer_body_by_extrude(
        self,
        profile: adsk.fusion.Profile,
        temp_base: adsk.fusion.BaseFeature,
        to_entity: adsk.core.Base,
    ) -> adsk.fusion.BRepBody:
        extrude_input = self.component.features.extrudeFeatures.createInput(profile, adsk.fusion.FeatureOperations.NewBodyFeatureOperation) # type: ignore
        extrude_input.targetBaseFeature = temp_base
        extrude_input.setOneSideExtent(
            adsk.fusion.ToEntityExtentDefinition.create(to_entity, False), 
            adsk.fusion.ExtentDirections.PositiveExtentDirection  # type: ignore
        )
        extrude_feature = self.component.features.extrudeFeatures.add(extrude_input)
        if extrude_feature.bodies.count < 1:
            raise errors.InvalidInputError("Failed to create transfer body from profile extrusion.")
        mgr = adsk.fusion.TemporaryBRepManager.get()
        return mgr.copy(extrude_feature.bodies[0])

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

    def rebuild_curves_as_spline(
        self, sketch: adsk.fusion.Sketch, curves: list[adsk.fusion.SketchCurve]
    ) -> adsk.fusion.SketchCurve | None:
        if not curves:
            return None
        sequenced = self.sequenced_curves(curves)
        sample_spacing = 0.35
        fit_point_spacing = 0.3

        sampled_points: list[adsk.core.Point3D] = []
        for curve, reverse in sequenced:
            points = self.sample_curve_points(curve, sample_spacing, reverse)
            for point in points:
                if sampled_points and sampled_points[-1].distanceTo(point) < fit_point_spacing:
                    continue
                sampled_points.append(point)

        if len(sampled_points) < 2:
            return None
        
        if self.inputs.close_loop.value and sampled_points[0].distanceTo(sampled_points[-1]) < self.inputs.heal_tolerance.value:
            sampled_points.append(sampled_points[0])

        spline: adsk.fusion.SketchCurve | None = None
        try:
            # Degree-5 control-point spline provides C2 continuity.
            if len(sampled_points) >= 6:
                spline = sketch.sketchCurves.sketchControlPointSplines.add(
                    cast(list[adsk.core.Base], sampled_points),
                    adsk.fusion.SplineDegrees.SplineDegreeFive,  # type: ignore
                )
                
            elif len(sampled_points) >= 4:
                spline = sketch.sketchCurves.sketchControlPointSplines.add(
                    cast(list[adsk.core.Base], sampled_points),
                    adsk.fusion.SplineDegrees.SplineDegreeThree, # type: ignore
                )
        except:
            spline = None

        if not spline:
            fit_points = adsk.core.ObjectCollection.create()
            for point in sampled_points:
                fit_points.add(point)
            spline = sketch.sketchCurves.sketchFittedSplines.add(fit_points)

        return spline

    def sample_curve_points(
        self, curve: adsk.fusion.SketchCurve, spacing: float, reverse: bool
    ) -> list[adsk.core.Point3D]:
        geometry = curve.geometry # type: ignore
        nurbs = geometry if isinstance(geometry, adsk.core.NurbsCurve3D) else geometry.asNurbsCurve  # type: ignore
        evaluator = nurbs.evaluator
        _, start_param, end_param = evaluator.getParameterExtents()
        _, total_length = evaluator.getLengthAtParameter(start_param, end_param)

        points: list[adsk.core.Point3D] = []
        _, start_point = evaluator.getPointAtParameter(start_param)
        points.append(start_point)
        offset = spacing
        while offset < total_length:
            _, param = evaluator.getParameterAtLength(start_param, offset)
            _, point = evaluator.getPointAtParameter(param)
            points.append(point)
            offset += spacing

        _, end_point = evaluator.getPointAtParameter(end_param)
        points.append(end_point) 

        if reverse:
            points.reverse()
        return points

    def apply_offset(self, sketch: adsk.fusion.Sketch, curve: adsk.fusion.SketchCurve) -> adsk.fusion.SketchCurve:
        offset = self.inputs.offset.value
        offset_input = sketch.geometricConstraints.createOffsetInput([curve], adsk.core.ValueInput.createByReal(offset))
        offset_input.isTopologyMatched = False
        constraint = sketch.geometricConstraints.addOffset2(offset_input)
        if not constraint:
            raise errors.InvalidInputError("Offset did not produce any curves.")
        offset_curves = constraint.childCurves
        rebuilt = self.rebuild_curves_as_spline(sketch, offset_curves)
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
