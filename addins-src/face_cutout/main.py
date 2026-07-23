from typing import cast

import adsk.core
import adsk.fusion

from lib import addin, inputs, ui_placement, utils
from lib.fusionbootstrap.runtime import RuntimeInfo


_addin: addin.Addin | None = None


def run(context, runtime_info: RuntimeInfo):
    global _addin
    _addin = FaceCutout(runtime_info)


def stop(context):
    global _addin
    if _addin:
        _addin.shutdown()
    _addin = None


class FaceCutoutInputs(inputs.Inputs):
    def __init__(self, units_manager: adsk.core.UnitsManager):
        units = units_manager.defaultLengthUnits

        self.face = inputs.SelectionByEntityTokenInput(
            id="face",
            name="Face",
            filter=["PlanarFaces"],
            lower_bound=1,
            upper_bound=1,
            tool_tip="Select one planar face on the body to cut.",
        )
        self.outer_inset = inputs.FloatInput(
            id="outer_inset",
            name="Outer Inset",
            default_value=2,
            tool_tip="Material to retain inside the outer boundary of the selected face.",
            units=units,
        )
        self.outer_inset.minimum_value = 0
        self.inner_feature_inset = inputs.FloatInput(
            id="inner_feature_inset",
            name="Inner Feature Inset",
            default_value=2,
            tool_tip="Material to retain around each inner boundary of the selected face.",
            units=units,
        )
        self.inner_feature_inset.minimum_value = 0
        self.remaining_material = inputs.FloatInput(
            id="remaining_material",
            name="Remaining Material",
            default_value=0,
            tool_tip="Material thickness to leave at the opposite face.",
            units=units,
        )
        self.remaining_material.minimum_value = 0
        self.fillet_radius = inputs.FloatInput(
            id="fillet_radius",
            name="Fillet Radius",
            default_value=0.8,
            tool_tip="Radius for the vertical edges of the cutout tool body. Use zero for no fillet.",
            units=units,
        )
        self.fillet_radius.minimum_value = 0
        self.tabs = inputs.CheckboxInput(
            id="tabs",
            name="Create Tabs",
            default_value=True,
            tool_tip="Connect isolated inner loops to the outer perimeter with material tabs.",
        )

        super().__init__()


class FaceCutout(addin.Addin):
    inputs: FaceCutoutInputs

    @property
    def plugin_name(self) -> str:
        return "Face Cutout"

    @property
    def plugin_desc(self) -> str:
        return "Create an inset face cutout with native Fusion features."

    @property
    def plugin_tooltip(self) -> str:
        return "Creates a sketch, extrude, optional fillet, and cut combine in the timeline."

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

    def create_inputs(self) -> FaceCutoutInputs:
        design = adsk.fusion.Design.cast(self.app.activeProduct)
        if not design:
            raise RuntimeError("Face Cutout requires an active Fusion design.")
        return FaceCutoutInputs(design.unitsManager)

    def pre_select(self, input, selection) -> bool:
        if not self.inputs or not input or input.id != self.inputs.face.id:
            return True
        face = adsk.fusion.BRepFace.cast(selection)
        return bool(face and face.body.isSolid and utils.brep.is_planar(face))

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

        selected_face = cast(adsk.fusion.BRepFace, self.inputs.face.value[0])
        face = selected_face.nativeObject or selected_face
        component = face.body.parentComponent
        opposite_face = utils.brep.get_opposite_face(face)
        cut_direction = utils.brep.normal_towards_face(face, opposite_face)

        sketch, profile = self._create_cutout_sketch(component, face)
        extrude = self._create_tool_extrude(
            component,
            sketch,
            profile,
            opposite_face,
            cut_direction,
        )

        tool_body = extrude.bodies.item(0)
        fillet = self._create_tool_fillet(component, tool_body, cut_direction)
        if fillet:
            tool_body = fillet.bodies.item(0)

        combine = self._create_cut_combine(component, face.body, tool_body)
        self._group_features(component, sketch, combine)

    def _validation_error(self) -> str | None:
        design = adsk.fusion.Design.cast(self.app.activeProduct)
        if not design:
            return "An active Fusion design is required."
        if design.designType != adsk.fusion.DesignTypes.ParametricDesignType:  # type: ignore
            return "Face Cutout requires Design History (a parametric design)."
        if not self.inputs or len(self.inputs.face.value) != 1:
            return "Select one planar face."

        selected_face = adsk.fusion.BRepFace.cast(self.inputs.face.value[0])
        if not selected_face or not utils.brep.is_planar(selected_face):
            return "The selected entity must be a planar face."
        if not selected_face.body.isSolid:
            return "The selected face must belong to a solid body."

        face = selected_face.nativeObject or selected_face
        if face.body.parentComponent != design.activeComponent:
            return "Activate the component that owns the selected face, then run Face Cutout again."

        for input_value, name in [
            (self.inputs.outer_inset.value, "Outer Inset"),
            (self.inputs.inner_feature_inset.value, "Inner Feature Inset"),
            (self.inputs.remaining_material.value, "Remaining Material"),
            (self.inputs.fillet_radius.value, "Fillet Radius"),
        ]:
            if input_value < 0:
                return f"{name} cannot be negative."

        try:
            thickness = utils.brep.get_board_thickness(face)
        except Exception as exc:
            return f"Could not find a parallel opposite face: {exc}"
        if self.inputs.remaining_material.value >= thickness - 1e-6:
            return "Remaining Material must be smaller than the body thickness."
        return None

    def _create_cutout_sketch(
        self,
        component: adsk.fusion.Component,
        face: adsk.fusion.BRepFace,
    ) -> tuple[adsk.fusion.Sketch, adsk.fusion.Profile]:
        # Sketches.add projects every edge of a BRep face automatically. That
        # would mix all face loops into each per-loop area probe below and can
        # make a valid inner offset look like it has the wrong direction.
        sketch = component.sketches.addWithoutEdges(face)
        if not sketch:
            raise RuntimeError("Fusion failed to create a sketch on the selected face.")
        sketch.name = "Face Cutout - Insets"

        final_curves: list[adsk.fusion.SketchCurve] = []
        outer_curves: list[adsk.fusion.SketchCurve] = []
        inner_loop_curves: list[list[adsk.fusion.SketchCurve]] = []

        for loop in face.loops:
            edges = cast(list[adsk.core.Base], utils.fusion.as_list(loop.edges))
            projected = [
                curve
                for entity in sketch.project2(edges, True)
                if (curve := adsk.fusion.SketchCurve.cast(entity))
            ]
            if not projected:
                raise RuntimeError("Fusion failed to project one of the face loops.")

            original_profile = self._largest_profile(sketch)
            if not original_profile:
                raise RuntimeError("A projected face loop did not create a closed profile.")
            original_area = original_profile.areaProperties().area

            self._set_construction(sketch, projected, True)
            input_value = self.inputs.outer_inset if loop.isOuter else self.inputs.inner_feature_inset
            if input_value.value <= 1e-9:
                loop_curves = projected
            else:
                loop_curves = self._offset_loop(
                    sketch=sketch,
                    source_curves=projected,
                    distance=input_value.value,
                    expression=input_value.expression,
                    original_area=original_area,
                    should_be_smaller=loop.isOuter,
                )

            final_curves.extend(loop_curves)
            if loop.isOuter:
                outer_curves.extend(loop_curves)
            else:
                inner_loop_curves.append(loop_curves)
            self._set_construction(sketch, loop_curves, True)

        self._set_construction(sketch, final_curves, False)
        if self.inputs.tabs.value:
            self._create_tabs(sketch, face, outer_curves, inner_loop_curves)
        profile = self._profile_bounded_by(sketch, outer_curves) or self._largest_profile(sketch)
        if not profile:
            raise RuntimeError("The inset curves did not create a usable cutout profile.")
        self._require_fully_constrained(sketch)
        return sketch, profile

    def _create_tabs(
        self,
        sketch: adsk.fusion.Sketch,
        face: adsk.fusion.BRepFace,
        outer_curves: list[adsk.fusion.SketchCurve],
        inner_loop_curves: list[list[adsk.fusion.SketchCurve]],
    ) -> None:
        if not outer_curves:
            return

        face_normal = utils.brep.normal_away_from_body(face)
        overlap = 0.1

        for inner_curves in inner_loop_curves:
            if self._curve_sets_intersect(inner_curves, outer_curves):
                continue

            inner_center = self._curve_set_center(sketch, inner_curves)
            connection = self._closest_point_on_curves(inner_center, outer_curves)
            if not connection:
                raise RuntimeError("Could not find a tab connection to the outer loop.")
            outer_point, distance = connection
            if distance <= 1e-6:
                continue

            connection_direction = inner_center.vectorTo(outer_point)
            if not connection_direction.normalize():
                continue
            lateral_direction = face_normal.crossProduct(connection_direction)
            if not lateral_direction.normalize():
                raise RuntimeError("Could not determine the tab width direction.")

            (
                min_width_point,
                max_width_point,
                min_width_projection,
                max_width_projection,
            ) = self._curve_set_extents(inner_curves, lateral_direction)
            tab_width = max_width_projection - min_width_projection
            if tab_width <= 1e-6:
                raise RuntimeError("Could not determine a valid tab width.")

            first_corner = self._translated_point(
                min_width_point,
                connection_direction,
                -overlap,
            )
            second_corner = self._translated_point(
                max_width_point,
                connection_direction,
                -overlap,
            )

            width_center_projection = (
                min_width_projection + max_width_projection
            ) / 2
            outer_width_projection = outer_point.asVector().dotProduct(
                lateral_direction
            )
            end_center = self._translated_point(
                outer_point,
                lateral_direction,
                width_center_projection - outer_width_projection,
            )
            end_center = self._translated_point(
                end_center,
                connection_direction,
                overlap,
            )
            fourth_corner = self._translated_point(
                end_center,
                lateral_direction,
                -tab_width / 2,
            )
            third_point = self._translated_point(
                end_center,
                lateral_direction,
                tab_width / 2,
            )

            tab_lines = sketch.sketchCurves.sketchLines
            first_line = tab_lines.addByTwoPoints(
                sketch.modelToSketchSpace(first_corner),
                sketch.modelToSketchSpace(second_corner),
            )
            second_line = tab_lines.addByTwoPoints(
                first_line.endSketchPoint,
                sketch.modelToSketchSpace(third_point),
            )
            third_line = tab_lines.addByTwoPoints(
                second_line.endSketchPoint,
                sketch.modelToSketchSpace(fourth_corner),
            )
            fourth_line = tab_lines.addByTwoPoints(
                third_line.endSketchPoint,
                first_line.startSketchPoint,
            )
            for line in (first_line, second_line, third_line, fourth_line):
                line.isFixed = True

    def _curve_sets_intersect(
        self,
        first: list[adsk.fusion.SketchCurve],
        second: list[adsk.fusion.SketchCurve],
    ) -> bool:
        second_collection = adsk.core.ObjectCollection.createWithArray(
            cast(list[adsk.core.Base], second)
        )
        for curve in first:
            success, _, intersection_points = curve.intersections(second_collection)
            if success and intersection_points.count > 0:
                return True
        return False

    def _curve_set_center(
        self,
        sketch: adsk.fusion.Sketch,
        curves: list[adsk.fusion.SketchCurve],
    ) -> adsk.core.Point3D:
        if not curves:
            raise RuntimeError("Could not determine the center of an inner loop.")
        boxes = [curve.boundingBox for curve in curves]
        min_x = min(box.minPoint.x for box in boxes)
        max_x = max(box.maxPoint.x for box in boxes)
        min_y = min(box.minPoint.y for box in boxes)
        max_y = max(box.maxPoint.y for box in boxes)
        center = adsk.core.Point3D.create(
            (min_x + max_x) / 2,
            (min_y + max_y) / 2,
            0,
        )
        return sketch.sketchToModelSpace(center)

    def _curve_set_extents(
        self,
        curves: list[adsk.fusion.SketchCurve],
        direction: adsk.core.Vector3D,
    ) -> tuple[adsk.core.Point3D, adsk.core.Point3D, float, float]:
        normalized_direction = direction.copy()
        if not normalized_direction.normalize():
            raise RuntimeError("Could not normalize the tab width direction.")

        projected_points: list[tuple[float, adsk.core.Point3D]] = []
        for curve in curves:
            evaluator = curve.worldGeometry.evaluator  # type: ignore
            success, start_parameter, end_parameter = evaluator.getParameterExtents()
            if not success:
                continue
            success, points = evaluator.getStrokes(
                start_parameter,
                end_parameter,
                1e-5,
            )
            if not success:
                continue
            projected_points.extend(
                (
                    point.asVector().dotProduct(normalized_direction),
                    point,
                )
                for point in points
            )

        if not projected_points:
            raise RuntimeError("Could not measure the offset inner loop.")
        min_projection, min_point = min(projected_points, key=lambda item: item[0])
        max_projection, max_point = max(projected_points, key=lambda item: item[0])
        return min_point, max_point, min_projection, max_projection

    def _closest_point_on_curves(
        self,
        point: adsk.core.Point3D,
        curves: list[adsk.fusion.SketchCurve],
    ) -> tuple[adsk.core.Point3D, float] | None:
        closest: tuple[adsk.core.Point3D, float] | None = None
        for curve in curves:
            projected = self._project_point_to_curve(
                point,
                curve.worldGeometry.evaluator,  # type: ignore
            )
            if not projected:
                continue
            distance = point.distanceTo(projected)
            if closest is None or distance < closest[1]:
                closest = (projected, distance)
        return closest

    def _project_point_to_curve(
        self,
        point: adsk.core.Point3D,
        evaluator,
    ) -> adsk.core.Point3D | None:
        success, parameter = evaluator.getParameterAtPoint(point)
        if not success:
            return None
        success, start_parameter, end_parameter = evaluator.getParameterExtents()
        if not success:
            return None
        parameter = max(
            min(start_parameter, end_parameter),
            min(max(start_parameter, end_parameter), parameter),
        )
        success, projected = evaluator.getPointAtParameter(parameter)
        return projected if success else None

    def _translated_point(
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

    def _offset_loop(
        self,
        sketch: adsk.fusion.Sketch,
        source_curves: list[adsk.fusion.SketchCurve],
        distance: float,
        expression: str,
        original_area: float,
        should_be_smaller: bool,
    ) -> list[adsk.fusion.SketchCurve]:
        direction_sign: int | None = None

        for sign in (1, -1):
            probe = self._add_offset_constraint(
                sketch,
                source_curves,
                adsk.core.ValueInput.createByReal(sign * distance),
            )
            if not probe:
                continue
            probe_curves = cast(list[adsk.fusion.SketchCurve], list(probe.childCurves))
            candidate = self._largest_profile(sketch)
            candidate_area = candidate.areaProperties().area if candidate else None
            is_smaller = candidate_area is not None and candidate_area < original_area
            is_correct = candidate_area is not None and is_smaller == should_be_smaller
            self._delete_probe(probe, probe_curves)
            if is_correct:
                direction_sign = sign
                break

        if direction_sign is None:
            boundary = "outer" if should_be_smaller else "inner"
            raise RuntimeError(f"Could not determine a valid offset direction for an {boundary} loop.")

        signed_expression = expression if direction_sign > 0 else f"-({expression})"
        constraint = self._add_offset_constraint(
            sketch,
            source_curves,
            adsk.core.ValueInput.createByString(signed_expression),
        )
        if not constraint:
            raise RuntimeError("Fusion failed to create the final parametric loop offset.")
        return cast(list[adsk.fusion.SketchCurve], list(constraint.childCurves))

    def _add_offset_constraint(
        self,
        sketch: adsk.fusion.Sketch,
        curves: list[adsk.fusion.SketchCurve],
        value: adsk.core.ValueInput,
    ) -> adsk.fusion.OffsetConstraint | None:
        try:
            offset_input = sketch.geometricConstraints.createOffsetInput(curves, value)
            if not offset_input:
                return None
            offset_input.isTopologyMatched = False
            return sketch.geometricConstraints.addOffset2(offset_input)
        except Exception:
            return None

    def _delete_probe(
        self,
        constraint: adsk.fusion.OffsetConstraint,
        curves: list[adsk.fusion.SketchCurve],
    ) -> None:
        for curve in curves:
            if curve and curve.isValid:
                curve.deleteMe()
        if constraint.isValid and constraint.isDeletable:
            constraint.deleteMe()

    def _create_tool_extrude(
        self,
        component: adsk.fusion.Component,
        sketch: adsk.fusion.Sketch,
        profile: adsk.fusion.Profile,
        opposite_face: adsk.fusion.BRepFace,
        cut_direction: adsk.core.Vector3D,
    ) -> adsk.fusion.ExtrudeFeature:
        extrude_input = component.features.extrudeFeatures.createInput(
            profile,
            adsk.fusion.FeatureOperations.NewBodyFeatureOperation,  # type: ignore
        )
        if not extrude_input:
            raise RuntimeError("Fusion failed to initialize the cutout tool extrude.")

        remainder_expression = self.inputs.remaining_material.expression
        # A negative to-entity offset stops before the entity in the extrude
        # direction, leaving material at the opposite face.
        signed_remainder = f"-({remainder_expression})"
        extent = adsk.fusion.ToEntityExtentDefinition.create(
            opposite_face,
            False,
            adsk.core.ValueInput.createByString(signed_remainder),
        )
        if not extent:
            raise RuntimeError("Fusion failed to define the opposite-face extrude extent.")
        extent.directionHint = cut_direction

        sketch_normal = sketch.xDirection.crossProduct(sketch.yDirection)
        direction = (
            adsk.fusion.ExtentDirections.PositiveExtentDirection
            if sketch_normal.dotProduct(cut_direction) >= 0
            else adsk.fusion.ExtentDirections.NegativeExtentDirection
        )
        if not extrude_input.setOneSideExtent(extent, direction):
            raise RuntimeError("Fusion rejected the cutout tool extrude extent.")

        extrude = component.features.extrudeFeatures.add(extrude_input)
        if not extrude or extrude.bodies.count != 1:
            raise RuntimeError("The cutout profile did not produce one solid tool body.")
        extrude.name = "Face Cutout - Tool"
        return extrude

    def _create_tool_fillet(
        self,
        component: adsk.fusion.Component,
        tool_body: adsk.fusion.BRepBody,
        cut_direction: adsk.core.Vector3D,
    ) -> adsk.fusion.FilletFeature | None:
        if self.inputs.fillet_radius.value <= 1e-9:
            return None

        edges = [
            edge
            for edge in tool_body.edges
            if utils.brep.is_parallel(edge, cut_direction) and not utils.brep.is_smooth_edge(edge)
        ]
        if not edges:
            return None

        fillet_input = component.features.filletFeatures.createInput()
        edge_collection = adsk.core.ObjectCollection.createWithArray(
            cast(list[adsk.core.Base], edges)
        )
        fillet_input.edgeSetInputs.addConstantRadiusEdgeSet(
            edge_collection,
            adsk.core.ValueInput.createByString(self.inputs.fillet_radius.expression),
            False,
        )
        fillet = component.features.filletFeatures.add(fillet_input)
        if not fillet or fillet.bodies.count != 1:
            raise RuntimeError("Fusion failed to fillet the cutout tool body.")
        fillet.name = "Face Cutout - Fillet"
        return fillet

    def _create_cut_combine(
        self,
        component: adsk.fusion.Component,
        target_body: adsk.fusion.BRepBody,
        tool_body: adsk.fusion.BRepBody,
    ) -> adsk.fusion.CombineFeature:
        tools = adsk.core.ObjectCollection.create()
        tools.add(tool_body)
        combine_input = component.features.combineFeatures.createInput(target_body, tools)
        if not combine_input:
            raise RuntimeError("Fusion failed to initialize the cut combine.")
        combine_input.operation = adsk.fusion.FeatureOperations.CutFeatureOperation  # type: ignore
        combine_input.isKeepToolBodies = False
        combine = component.features.combineFeatures.add(combine_input)
        if not combine:
            raise RuntimeError("Fusion failed to cut the target body.")
        combine.name = "Face Cutout - Cut"
        return combine

    def _group_features(
        self,
        component: adsk.fusion.Component,
        sketch: adsk.fusion.Sketch,
        combine: adsk.fusion.CombineFeature,
    ) -> None:
        start_index = sketch.timelineObject.index
        end_index = combine.timelineObject.index
        group = component.parentDesign.timeline.timelineGroups.add(start_index, end_index)
        if group:
            group.name = "Face Cutout"
            group.isCollapsed = False

    def _largest_profile(self, sketch: adsk.fusion.Sketch) -> adsk.fusion.Profile | None:
        profiles = utils.fusion.as_list(sketch.profiles)
        if not profiles:
            return None
        return max(profiles, key=lambda profile: profile.areaProperties().area)

    def _profile_bounded_by(
        self,
        sketch: adsk.fusion.Sketch,
        outer_curves: list[adsk.fusion.SketchCurve],
    ) -> adsk.fusion.Profile | None:
        outer_tokens = {curve.entityToken for curve in outer_curves}
        candidates: list[adsk.fusion.Profile] = []
        for profile in sketch.profiles:
            outer_loop = next((loop for loop in profile.profileLoops if loop.isOuter), None)
            if not outer_loop:
                continue
            loop_tokens = {
                curve.sketchEntity.entityToken
                for curve in outer_loop.profileCurves
                if curve.sketchEntity
            }
            if loop_tokens & outer_tokens:
                candidates.append(profile)
        if not candidates:
            return None
        return max(candidates, key=lambda profile: profile.areaProperties().area)

    def _set_construction(
        self,
        sketch: adsk.fusion.Sketch,
        curves: list[adsk.fusion.SketchCurve],
        is_construction: bool,
    ) -> None:
        state = (
            adsk.fusion.SketchCurveConstructionStates.ConstructionSketchCurveConstructionState
            if is_construction
            else adsk.fusion.SketchCurveConstructionStates.NormalSketchCurveConstructionState
        )
        sketch.setConstructionState(curves, state)  # type: ignore

    def _require_fully_constrained(self, sketch: adsk.fusion.Sketch) -> None:
        if sketch.isFullyConstrained:
            return
        unconstrained_count = sum(
            1 for curve in sketch.sketchCurves if not curve.isFullyConstrained
        )
        raise RuntimeError(
            "Face Cutout generated an under-constrained sketch "
            f"({unconstrained_count} unconstrained curves)."
        )
