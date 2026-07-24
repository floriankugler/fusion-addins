import math
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
    FULL_CUTOUT = inputs.DropDownInput.Item("Full Cutout", 0)
    TRIANGLES = inputs.DropDownInput.Item("Triangles", 1)

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
        self.pattern_type = inputs.DropDownInput(
            id="pattern_type",
            name="Pattern",
            options=[self.FULL_CUTOUT, self.TRIANGLES],
            default_value=self.FULL_CUTOUT.value,
            tool_tip="Create one full cutout or restrict it to a triangle pattern.",
        )
        triangle_input_visible = lambda: (
            self.pattern_type.value == self.TRIANGLES.value
        )
        self.triangle_columns = inputs.IntegerInput(
            id="triangle_columns",
            name="Columns",
            default_value=8,
            minimum=1,
            maximum=100,
            tool_tip="Number of triangles along the longest pattern direction.",
            update_visibility=triangle_input_visible,
        )
        self.triangle_rows = inputs.IntegerInput(
            id="triangle_rows",
            name="Rows",
            default_value=6,
            minimum=1,
            maximum=100,
            tool_tip="Number of triangle rows.",
            update_visibility=triangle_input_visible,
        )
        self.triangle_spacing = inputs.FloatInput(
            id="triangle_spacing",
            name="Triangle Spacing",
            default_value=2,
            tool_tip="True edge-to-edge clearance between adjacent triangles.",
            units=units,
            update_visibility=triangle_input_visible,
        )
        self.triangle_spacing.minimum_value = 0

        super().__init__()


class FaceCutout(addin.Addin):
    inputs: FaceCutoutInputs
    _parameter_prefix: str

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
        self._parameter_prefix = self._unique_parameter_prefix(
            component.parentDesign
        )
        opposite_face = utils.brep.get_opposite_face(face)
        cut_direction = utils.brep.normal_towards_face(face, opposite_face)
        existing_body_tokens = {
            body.entityToken
            for body in component.bRepBodies
        }

        sketch, profile, outer_curves = self._create_cutout_sketch(component, face)
        extrude = self._create_tool_extrude(
            component,
            sketch,
            profile,
            opposite_face,
            cut_direction,
        )

        tool_bodies = cast(
            list[adsk.fusion.BRepBody],
            utils.fusion.as_list(extrude.bodies),
        )
        if self.inputs.pattern_type.value == FaceCutoutInputs.TRIANGLES.value:
            (
                pattern_sketch,
                u_direction,
                v_direction,
                pitch_u_expression,
                pitch_v_expression,
            ) = self._create_triangle_pattern_sketch(
                component,
                face,
                outer_curves,
            )
            pattern_extrude = self._create_pattern_extrude(
                component,
                pattern_sketch,
                opposite_face,
                cut_direction,
            )
            self._create_solid_triangle_pattern(
                component,
                cast(
                    list[adsk.fusion.BRepBody],
                    utils.fusion.as_list(pattern_extrude.bodies),
                ),
                u_direction,
                v_direction,
                pitch_u_expression,
                pitch_v_expression,
            )
            pattern_bodies = [
                body
                for body in component.bRepBodies
                if body.entityToken not in existing_body_tokens
                and body != tool_bodies[0]
            ]
            if not pattern_bodies:
                raise RuntimeError(
                    "The solid triangle pattern did not create any tool bodies."
                )
            intersection = self._create_intersect_combine(
                component,
                tool_bodies[0],
                pattern_bodies,
            )
            tool_bodies = cast(
                list[adsk.fusion.BRepBody],
                utils.fusion.as_list(intersection.bodies),
            )

        tool_bodies = self._create_tool_fillets(
            component,
            tool_bodies,
            cut_direction,
        )

        combine = self._create_cut_combine(component, face.body, tool_bodies)
        self._group_features(component, sketch, combine)

    def _unique_parameter_prefix(
        self,
        design: adsk.fusion.Design,
    ) -> str:
        parameter_names = {
            parameter.name
            for parameter in design.allParameters
        }
        base = "faceCutout"
        index = 1
        while True:
            candidate = base if index == 1 else f"{base}{index}"
            if not any(
                name.startswith(f"{candidate}_")
                for name in parameter_names
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
            (self.inputs.triangle_spacing.value, "Triangle Spacing"),
        ]:
            if input_value < 0:
                return f"{name} cannot be negative."

        try:
            thickness = utils.brep.get_board_thickness(face)
        except Exception as exc:
            return f"Could not find a parallel opposite face: {exc}"
        if self.inputs.remaining_material.value >= thickness - 1e-6:
            return "Remaining Material must be smaller than the body thickness."
        if (
            self.inputs.pattern_type.value == FaceCutoutInputs.TRIANGLES.value
            and self.inputs.triangle_spacing.value <= 1e-6
        ):
            return "Triangle Spacing must be greater than zero."
        return None

    def _create_cutout_sketch(
        self,
        component: adsk.fusion.Component,
        face: adsk.fusion.BRepFace,
    ) -> tuple[
        adsk.fusion.Sketch,
        adsk.fusion.Profile,
        list[adsk.fusion.SketchCurve],
    ]:
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
        inner_loop_index = 0

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
            if loop.isOuter:
                input_value = self.inputs.outer_inset
                parameter_role = "outerInset"
            else:
                inner_loop_index += 1
                input_value = self.inputs.inner_feature_inset
                parameter_role = f"innerInset{inner_loop_index}"
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
                    parameter_role=parameter_role,
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
        return sketch, profile, outer_curves

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
        parameter_role: str,
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
        dimension = constraint.dimension
        if not dimension or not dimension.parameter:
            raise RuntimeError(
                "Fusion did not create a parameter for the loop offset."
            )
        self._name_parameter(dimension.parameter, parameter_role)
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

    def _create_triangle_pattern_sketch(
        self,
        component: adsk.fusion.Component,
        face: adsk.fusion.BRepFace,
        outer_curves: list[adsk.fusion.SketchCurve],
    ) -> tuple[
        adsk.fusion.Sketch,
        adsk.fusion.SketchLine,
        adsk.fusion.SketchLine,
        str,
        str,
    ]:
        sketch = component.sketches.addWithoutEdges(face)
        if not sketch:
            raise RuntimeError("Fusion failed to create the triangle pattern sketch.")
        sketch.name = "Face Cutout - Triangle Seeds"

        (
            origin,
            u_direction,
            v_direction,
            extent_u,
            extent_v,
            extent_u_parameter,
            extent_v_parameter,
            u_vector,
            v_vector,
        ) = self._create_rectangular_pattern_boundary(
            sketch,
            outer_curves,
        )

        columns = self.inputs.triangle_columns.value
        rows = self.inputs.triangle_rows.value
        spacing = self.inputs.triangle_spacing.value
        triangle_width, triangle_height = self._triangle_dimensions(
            extent_u,
            extent_v,
            columns,
            rows,
            spacing,
        )

        sketch.isComputeDeferred = True
        spacing_dimension = self._create_seed_spacing_dimension(
            sketch,
            origin,
            u_direction,
            u_vector,
            spacing,
        )
        spacing_parameter = spacing_dimension.parameter
        if not spacing_parameter:
            raise RuntimeError("Fusion did not create the triangle spacing parameter.")

        height_expression = (
            f"(({extent_v_parameter.name}) - "
            f"{rows - 1} * ({spacing_parameter.name})) / {rows}"
        )
        width_expression = self._triangle_width_expression(
            extent_u_parameter.name,
            height_expression,
            spacing_parameter.name,
            columns,
        )

        seeds: list[
            tuple[adsk.fusion.SketchLine, adsk.fusion.SketchLine]
        ] = []
        width_parameter: adsk.fusion.ModelParameter | None = None
        height_parameter: adsk.fusion.ModelParameter | None = None
        pitch_u_expression = ""
        pitch_v_expression = ""
        pitch_u = (
            triangle_width / 2
            + spacing
            * math.sqrt(
                triangle_height * triangle_height
                + (triangle_width / 2) * (triangle_width / 2)
            )
            / triangle_height
        )
        pitch_v = triangle_height + spacing

        for row in range(2):
            for column in range(2):
                points_up = (row + column) % 2 == 0
                seed_index = row * 2 + column + 1
                base_u = column * pitch_u - triangle_width / 2
                base_v = row * pitch_v + (
                    0 if points_up else triangle_height
                )
                if column == 0:
                    u_position_expression = (
                        f"({width_parameter.name}) / 2"
                        if width_parameter
                        else f"({width_expression}) / 2"
                    )
                else:
                    u_position_expression = (
                        f"({pitch_u_expression}) - "
                        f"({width_parameter.name}) / 2"
                    )
                v_position_expression = (
                    (
                        f"{row} * ({pitch_v_expression})"
                        if points_up
                        else (
                            f"{row} * ({pitch_v_expression}) + "
                            f"({height_parameter.name})"
                        )
                    )
                    if height_parameter
                    else "0 cm"
                )

                base, altitude, width_dimension, height_dimension = (
                    self._add_seed_triangle(
                        sketch,
                        origin,
                        u_direction,
                        v_direction,
                        u_vector,
                        v_vector,
                        base_u,
                        base_v,
                        base_u,
                        base_v,
                        u_position_expression,
                        v_position_expression,
                        triangle_width,
                        triangle_height,
                        points_up,
                        width_expression,
                        height_expression,
                        seed_index,
                        seeds[0] if seeds else None,
                    )
                )
                seeds.append((base, altitude))
                if not width_parameter:
                    width_parameter = (
                        width_dimension.parameter
                        if width_dimension
                        else None
                    )
                    height_parameter = (
                        height_dimension.parameter
                        if height_dimension
                        else None
                    )
                    if not width_parameter or not height_parameter:
                        raise RuntimeError(
                            "Fusion did not create the triangle seed parameters."
                        )
                    pitch_u_expression = (
                        f"(({width_parameter.name}) / 2 + "
                        f"({spacing_parameter.name}) * "
                        f"sqrt(({height_parameter.name}) * "
                        f"({height_parameter.name}) + "
                        f"(({width_parameter.name}) / 2) * "
                        f"(({width_parameter.name}) / 2)) / "
                        f"({height_parameter.name}))"
                    )
                    pitch_v_expression = (
                        f"(({height_parameter.name}) + "
                        f"({spacing_parameter.name}))"
                    )

        sketch.isComputeDeferred = False
        self._require_fully_constrained(sketch)
        if sketch.profiles.count != 4:
            raise RuntimeError(
                "The triangle seed sketch did not create four profiles "
                f"({sketch.profiles.count} found)."
            )
        return (
            sketch,
            u_direction,
            v_direction,
            pitch_u_expression,
            pitch_v_expression,
        )

    def _create_rectangular_pattern_boundary(
        self,
        sketch: adsk.fusion.Sketch,
        outer_curves: list[adsk.fusion.SketchCurve],
    ) -> tuple[
        adsk.fusion.SketchPoint,
        adsk.fusion.SketchLine,
        adsk.fusion.SketchLine,
        float,
        float,
        adsk.fusion.ModelParameter,
        adsk.fusion.ModelParameter,
        adsk.core.Vector3D,
        adsk.core.Vector3D,
    ]:
        boundary = [
            line
            for entity in sketch.project2(
                cast(list[adsk.core.Base], outer_curves),
                True,
            )
            if (line := adsk.fusion.SketchLine.cast(entity))
        ]
        if len(boundary) != 4:
            raise ValueError(
                "Triangle patterns currently require a rectangular selected "
                "face whose offset outer loop contains exactly four lines."
            )
        self._set_construction(
            sketch,
            cast(list[adsk.fusion.SketchCurve], boundary),
            True,
        )

        u_source = max(boundary, key=lambda line: line.length)
        origin = u_source.startSketchPoint
        connected = [
            line
            for line in boundary
            if line != u_source
            and (
                line.startSketchPoint.geometry.distanceTo(origin.geometry) <= 1e-5
                or line.endSketchPoint.geometry.distanceTo(origin.geometry) <= 1e-5
            )
        ]
        if len(connected) != 1:
            raise ValueError(
                "The offset outer loop is not a single closed rectangle."
            )
        v_source = connected[0]
        u_end = u_source.endSketchPoint
        v_end = (
            v_source.endSketchPoint
            if v_source.startSketchPoint.geometry.distanceTo(origin.geometry)
            <= 1e-5
            else v_source.startSketchPoint
        )
        u_vector = origin.geometry.vectorTo(u_end.geometry)
        v_vector = origin.geometry.vectorTo(v_end.geometry)
        extent_u = u_vector.length
        extent_v = v_vector.length
        if (
            extent_u <= 1e-6
            or extent_v <= 1e-6
            or not u_vector.normalize()
            or not v_vector.normalize()
            or abs(u_vector.dotProduct(v_vector)) > 1e-5
        ):
            raise ValueError(
                "The offset outer loop must contain four perpendicular lines."
            )

        directions = [
            self._normalized_line_vector(line)
            for line in boundary
        ]
        u_parallel = sum(
            1
            for direction in directions
            if abs(abs(direction.dotProduct(u_vector)) - 1) <= 1e-5
        )
        v_parallel = sum(
            1
            for direction in directions
            if abs(abs(direction.dotProduct(v_vector)) - 1) <= 1e-5
        )
        if u_parallel != 2 or v_parallel != 2:
            raise ValueError(
                "The offset outer loop must contain two pairs of parallel lines."
            )

        lines = sketch.sketchCurves.sketchLines
        u_direction = lines.addByTwoPoints(
            origin.geometry,
            u_end.geometry,
        )
        v_direction = lines.addByTwoPoints(
            origin.geometry,
            v_end.geometry,
        )
        for direction, end in (
            (u_direction, u_end),
            (v_direction, v_end),
        ):
            direction.isConstruction = True
            sketch.geometricConstraints.addCoincident(
                direction.startSketchPoint,
                origin,
            )
            sketch.geometricConstraints.addCoincident(
                direction.endSketchPoint,
                end,
            )

        u_dimension = self._dimension_line_length(
            sketch,
            u_direction,
            "",
            is_driving=False,
            parameter_role="patternLength",
        )
        v_dimension = self._dimension_line_length(
            sketch,
            v_direction,
            "",
            is_driving=False,
            parameter_role="patternWidth",
        )
        if not u_dimension.parameter or not v_dimension.parameter:
            raise RuntimeError(
                "Fusion failed to measure the rectangular pattern boundary."
            )
        return (
            origin,
            u_direction,
            v_direction,
            extent_u,
            extent_v,
            u_dimension.parameter,
            v_dimension.parameter,
            u_vector,
            v_vector,
        )

    def _normalized_line_vector(
        self,
        line: adsk.fusion.SketchLine,
    ) -> adsk.core.Vector3D:
        vector = line.startSketchPoint.geometry.vectorTo(
            line.endSketchPoint.geometry
        )
        if not vector.normalize():
            raise ValueError("The rectangular boundary contains a zero-length line.")
        return vector

    def _create_seed_spacing_dimension(
        self,
        sketch: adsk.fusion.Sketch,
        origin: adsk.fusion.SketchPoint,
        u_direction: adsk.fusion.SketchLine,
        u_vector: adsk.core.Vector3D,
        spacing: float,
    ) -> adsk.fusion.SketchLinearDimension:
        end = origin.geometry.copy()
        offset = u_vector.copy()
        offset.scaleBy(-spacing)
        end.translateBy(offset)
        line = sketch.sketchCurves.sketchLines.addByTwoPoints(
            origin.geometry,
            end,
        )
        line.isConstruction = True
        constraints = sketch.geometricConstraints
        constraints.addCoincident(line.startSketchPoint, origin)
        constraints.addParallel(line, u_direction)
        return self._dimension_line_length(
            sketch,
            line,
            self.inputs.triangle_spacing.expression,
            parameter_role="triangleSpacing",
        )

    def _add_seed_triangle(
        self,
        sketch: adsk.fusion.Sketch,
        origin: adsk.fusion.SketchPoint,
        u_direction: adsk.fusion.SketchLine,
        v_direction: adsk.fusion.SketchLine,
        u_vector: adsk.core.Vector3D,
        v_vector: adsk.core.Vector3D,
        base_u: float,
        base_v: float,
        u_position: float,
        v_position: float,
        u_position_expression: str,
        v_position_expression: str,
        width: float,
        height: float,
        points_up: bool,
        width_expression: str,
        height_expression: str,
        seed_index: int,
        size_seed: tuple[
            adsk.fusion.SketchLine,
            adsk.fusion.SketchLine,
        ]
        | None,
    ) -> tuple[
        adsk.fusion.SketchLine,
        adsk.fusion.SketchLine,
        adsk.fusion.SketchLinearDimension | None,
        adsk.fusion.SketchLinearDimension | None,
    ]:
        base_start_geometry = self._seed_point(
            origin.geometry,
            u_vector,
            v_vector,
            base_u,
            base_v,
        )
        base_end_geometry = self._seed_point(
            origin.geometry,
            u_vector,
            v_vector,
            base_u + width,
            base_v,
        )
        apex_geometry = self._seed_point(
            origin.geometry,
            u_vector,
            v_vector,
            base_u + width / 2,
            base_v + (height if points_up else -height),
        )
        lines = sketch.sketchCurves.sketchLines
        base = lines.addByTwoPoints(
            base_start_geometry,
            base_end_geometry,
        )
        constraints = sketch.geometricConstraints
        constraints.addParallel(base, u_direction)
        self._constrain_seed_position(
            sketch,
            origin,
            base.startSketchPoint,
            u_direction,
            v_direction,
            u_vector,
            v_vector,
            u_position,
            v_position,
            u_position_expression,
            v_position_expression,
            seed_index,
        )

        midpoint = sketch.sketchPoints.add(
            self._seed_point(
                origin.geometry,
                u_vector,
                v_vector,
                base_u + width / 2,
                base_v,
            )
        )
        constraints.addMidPoint(midpoint, base)
        apex = sketch.sketchPoints.add(apex_geometry)
        altitude = lines.addByTwoPoints(midpoint, apex)
        altitude.isConstruction = True
        constraints.addParallel(altitude, v_direction)
        lines.addByTwoPoints(base.endSketchPoint, apex)
        lines.addByTwoPoints(apex, base.startSketchPoint)

        width_dimension = None
        height_dimension = None
        if size_seed:
            constraints.addEqual(size_seed[0], base)
            constraints.addEqual(size_seed[1], altitude)
        else:
            width_dimension = self._dimension_line_length(
                sketch,
                base,
                width_expression,
                parameter_role="triangleWidth",
            )
            height_dimension = self._dimension_line_length(
                sketch,
                altitude,
                height_expression,
                parameter_role="triangleHeight",
            )
        return base, altitude, width_dimension, height_dimension

    def _constrain_seed_position(
        self,
        sketch: adsk.fusion.Sketch,
        origin: adsk.fusion.SketchPoint,
        point: adsk.fusion.SketchPoint,
        u_direction: adsk.fusion.SketchLine,
        v_direction: adsk.fusion.SketchLine,
        u_vector: adsk.core.Vector3D,
        v_vector: adsk.core.Vector3D,
        u_value: float,
        v_value: float,
        u_expression: str,
        v_expression: str,
        seed_index: int,
    ) -> None:
        constraints = sketch.geometricConstraints
        anchor = origin
        if abs(u_value) > 1e-9:
            u_line = sketch.sketchCurves.sketchLines.addByTwoPoints(
                origin.geometry,
                self._seed_point(
                    origin.geometry,
                    u_vector,
                    v_vector,
                    u_value,
                    0,
                ),
            )
            u_line.isConstruction = True
            constraints.addCoincident(u_line.startSketchPoint, origin)
            constraints.addParallel(u_line, u_direction)
            self._dimension_line_length(
                sketch,
                u_line,
                u_expression,
                parameter_role=f"triangleSeed{seed_index}UOffset",
            )
            anchor = u_line.endSketchPoint
        if v_value > 1e-9:
            v_line = sketch.sketchCurves.sketchLines.addByTwoPoints(
                anchor.geometry,
                point.geometry,
            )
            v_line.isConstruction = True
            constraints.addCoincident(v_line.startSketchPoint, anchor)
            constraints.addCoincident(v_line.endSketchPoint, point)
            constraints.addParallel(v_line, v_direction)
            self._dimension_line_length(
                sketch,
                v_line,
                v_expression,
                parameter_role=f"triangleSeed{seed_index}VOffset",
            )
        else:
            constraints.addCoincident(point, anchor)

    def _seed_point(
        self,
        origin: adsk.core.Point3D,
        u_vector: adsk.core.Vector3D,
        v_vector: adsk.core.Vector3D,
        u: float,
        v: float,
    ) -> adsk.core.Point3D:
        point = origin.copy()
        u_offset = u_vector.copy()
        u_offset.scaleBy(u)
        point.translateBy(u_offset)
        v_offset = v_vector.copy()
        v_offset.scaleBy(v)
        point.translateBy(v_offset)
        return point

    def _dimension_line_length(
        self,
        sketch: adsk.fusion.Sketch,
        line: adsk.fusion.SketchLine,
        expression: str,
        is_driving: bool = True,
        parameter_role: str | None = None,
    ) -> adsk.fusion.SketchLinearDimension:
        start = line.startSketchPoint.geometry
        end = line.endSketchPoint.geometry
        text_point = adsk.core.Point3D.create(
            (start.x + end.x) / 2 + 0.2,
            (start.y + end.y) / 2 + 0.2,
            0,
        )
        dimension = sketch.sketchDimensions.addDistanceDimension(
            line.startSketchPoint,
            line.endSketchPoint,
            adsk.fusion.DimensionOrientations.AlignedDimensionOrientation,
            text_point,
            is_driving,
        )
        if not dimension or not dimension.parameter:
            raise RuntimeError(
                "Fusion failed to create a triangle seed dimension."
            )
        if is_driving:
            dimension.parameter.expression = expression
        if parameter_role:
            self._name_parameter(dimension.parameter, parameter_role)
        return dimension

    def _create_solid_triangle_pattern(
        self,
        component: adsk.fusion.Component,
        seed_bodies: list[adsk.fusion.BRepBody],
        u_direction: adsk.fusion.SketchLine,
        v_direction: adsk.fusion.SketchLine,
        pitch_u_expression: str,
        pitch_v_expression: str,
    ) -> adsk.fusion.RectangularPatternFeature | None:
        quantity_u = max(
            1,
            math.ceil((self.inputs.triangle_columns.value + 1) / 2),
        )
        quantity_v = max(
            1,
            math.ceil(self.inputs.triangle_rows.value / 2),
        )
        if quantity_u == 1 and quantity_v == 1:
            return None
        entities = adsk.core.ObjectCollection.createWithArray(
            cast(list[adsk.core.Base], seed_bodies)
        )
        pattern_input = (
            component.features.rectangularPatternFeatures.createInput(
                entities,
                u_direction,
                adsk.core.ValueInput.createByReal(quantity_u),
                adsk.core.ValueInput.createByString(
                    f"2 * ({pitch_u_expression})"
                ),
                adsk.fusion.PatternDistanceType.SpacingPatternDistanceType,
            )
        )
        if not pattern_input:
            raise RuntimeError(
                "Fusion failed to initialize the solid triangle pattern."
            )
        if not pattern_input.setDirectionTwo(
            v_direction,
            adsk.core.ValueInput.createByReal(quantity_v),
            adsk.core.ValueInput.createByString(
                f"2 * ({pitch_v_expression})"
            ),
        ):
            raise RuntimeError(
                "Fusion rejected the solid triangle pattern row definition."
            )
        pattern = component.features.rectangularPatternFeatures.add(
            pattern_input
        )
        if not pattern:
            raise RuntimeError(
                "Fusion failed to create the solid triangle pattern."
            )
        pattern.name = "Face Cutout - Solid Triangle Pattern"
        return pattern

    def _triangle_dimensions(
        self,
        extent_u: float,
        extent_v: float,
        columns: int,
        rows: int,
        spacing: float,
    ) -> tuple[float, float]:
        height = (extent_v - (rows - 1) * spacing) / rows
        if height <= 1e-6:
            raise ValueError(
                "Triangle spacing and row count leave no room for triangle height."
            )
        # The first triangle is centered on the start boundary and the final
        # triangle is centered on the opposite boundary. The requested column
        # count therefore describes the number of center-to-center pitches
        # across the rectangle:
        #
        #   extent_u = columns * (width / 2 + projected_edge_spacing)
        #
        # Solving that equation for width keeps both clipped end triangles
        # exactly one half wide.
        a = columns / 2
        b = columns * spacing
        coefficient = a * a - b * b / (4 * height * height)
        if abs(coefficient) <= 1e-9:
            raise ValueError("Triangle spacing is too large for the requested columns.")
        discriminant = (
            a * a * extent_u * extent_u
            - coefficient * (extent_u * extent_u - b * b)
        )
        if discriminant < -1e-8:
            raise ValueError("Triangle spacing is too large for the pattern boundary.")
        width = (
            a * extent_u - math.sqrt(max(0, discriminant))
        ) / coefficient
        if width <= 1e-6 or extent_u - a * width < -1e-6:
            raise ValueError("The requested triangle pattern does not fit the boundary.")
        return width, height

    def _triangle_width_expression(
        self,
        extent_parameter: str,
        height_expression: str,
        spacing_parameter: str,
        columns: int,
    ) -> str:
        a = columns / 2
        b = f"({columns} * ({spacing_parameter}))"
        height = f"({height_expression})"
        coefficient = (
            f"(({a}) * ({a}) - ({b}) * ({b}) / "
            f"(4 * ({height}) * ({height})))"
        )
        discriminant = (
            f"(({a}) * ({a}) * ({extent_parameter}) * ({extent_parameter}) - "
            f"({coefficient}) * "
            f"(({extent_parameter}) * ({extent_parameter}) - ({b}) * ({b})))"
        )
        return (
            f"(({a}) * ({extent_parameter}) - sqrt({discriminant})) / "
            f"({coefficient})"
        )

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

    def _create_pattern_extrude(
        self,
        component: adsk.fusion.Component,
        sketch: adsk.fusion.Sketch,
        opposite_face: adsk.fusion.BRepFace,
        cut_direction: adsk.core.Vector3D,
    ) -> adsk.fusion.ExtrudeFeature:
        profiles = adsk.core.ObjectCollection.create()
        for profile in sketch.profiles:
            profiles.add(profile)
        if profiles.count == 0:
            raise RuntimeError("The triangle sketch does not contain any profiles.")

        extrude_input = component.features.extrudeFeatures.createInput(
            profiles,
            adsk.fusion.FeatureOperations.NewBodyFeatureOperation,  # type: ignore
        )
        if not extrude_input:
            raise RuntimeError("Fusion failed to initialize the triangle extrude.")

        signed_remainder = f"-({self.inputs.remaining_material.expression})"
        extent = adsk.fusion.ToEntityExtentDefinition.create(
            opposite_face,
            False,
            adsk.core.ValueInput.createByString(signed_remainder),
        )
        if not extent:
            raise RuntimeError("Fusion failed to define the triangle extrude extent.")
        extent.directionHint = cut_direction

        sketch_normal = sketch.xDirection.crossProduct(sketch.yDirection)
        direction = (
            adsk.fusion.ExtentDirections.PositiveExtentDirection
            if sketch_normal.dotProduct(cut_direction) >= 0
            else adsk.fusion.ExtentDirections.NegativeExtentDirection
        )
        if not extrude_input.setOneSideExtent(extent, direction):
            raise RuntimeError("Fusion rejected the triangle extrude extent.")

        extrude = component.features.extrudeFeatures.add(extrude_input)
        if not extrude or extrude.bodies.count == 0:
            raise RuntimeError("The triangle profiles did not produce tool bodies.")
        extrude.name = "Face Cutout - Triangle Pattern"
        return extrude

    def _create_intersect_combine(
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
            raise RuntimeError("Fusion failed to initialize the triangle intersection.")
        combine_input.operation = (
            adsk.fusion.FeatureOperations.IntersectFeatureOperation  # type: ignore
        )
        combine_input.isKeepToolBodies = False
        combine = component.features.combineFeatures.add(combine_input)
        if not combine or combine.bodies.count == 0:
            raise RuntimeError("The triangles did not intersect the full cutout tool.")
        combine.name = "Face Cutout - Pattern Intersection"
        return combine

    def _create_tool_fillets(
        self,
        component: adsk.fusion.Component,
        tool_bodies: list[adsk.fusion.BRepBody],
        cut_direction: adsk.core.Vector3D,
    ) -> list[adsk.fusion.BRepBody]:
        if self.inputs.fillet_radius.value <= 1e-9:
            return tool_bodies

        radius = self.inputs.fillet_radius.value
        eligible = [
            body
            for body in tool_bodies
            if self._body_can_accept_fillet(body, cut_direction, radius)
        ]
        result = [body for body in tool_bodies if body not in eligible]
        fillets: list[adsk.fusion.FilletFeature] = []
        result.extend(
            self._fillet_body_group(
                component,
                eligible,
                cut_direction,
                fillets,
            )
        )
        for index, fillet in enumerate(fillets, start=1):
            fillet.name = (
                "Face Cutout - Fillet"
                if len(fillets) == 1
                else f"Face Cutout - Fillet {index}"
            )
        return result

    def _body_can_accept_fillet(
        self,
        body: adsk.fusion.BRepBody,
        cut_direction: adsk.core.Vector3D,
        radius: float,
    ) -> bool:
        normal = cut_direction.copy()
        if not normal.normalize():
            return False
        reference = (
            adsk.core.Vector3D.create(1, 0, 0)
            if abs(normal.x) < 0.9
            else adsk.core.Vector3D.create(0, 1, 0)
        )
        first_axis = normal.crossProduct(reference)
        if not first_axis.normalize():
            return False
        second_axis = normal.crossProduct(first_axis)
        if not second_axis.normalize():
            return False

        first_projections = [
            vertex.geometry.asVector().dotProduct(first_axis)
            for vertex in body.vertices
        ]
        second_projections = [
            vertex.geometry.asVector().dotProduct(second_axis)
            for vertex in body.vertices
        ]
        if not first_projections or not second_projections:
            return False
        minimum_span = min(
            max(first_projections) - min(first_projections),
            max(second_projections) - min(second_projections),
        )
        return minimum_span > 2 * radius + 1e-6

    def _fillet_body_group(
        self,
        component: adsk.fusion.Component,
        bodies: list[adsk.fusion.BRepBody],
        cut_direction: adsk.core.Vector3D,
        fillets: list[adsk.fusion.FilletFeature],
    ) -> list[adsk.fusion.BRepBody]:
        if not bodies:
            return []
        edges = [
            edge
            for body in bodies
            for edge in body.edges
            if utils.brep.is_parallel(edge, cut_direction)
            and not utils.brep.is_smooth_edge(edge)
        ]
        if not edges:
            return bodies

        fillet_input = component.features.filletFeatures.createInput()
        edge_collection = adsk.core.ObjectCollection.createWithArray(
            cast(list[adsk.core.Base], edges)
        )
        fillet_input.edgeSetInputs.addConstantRadiusEdgeSet(
            edge_collection,
            adsk.core.ValueInput.createByString(
                self.inputs.fillet_radius.expression
            ),
            False,
        )
        try:
            fillet = component.features.filletFeatures.add(fillet_input)
        except RuntimeError:
            if len(bodies) == 1:
                # An irregular boundary fragment can be locally too small even
                # when its overall span is large enough. Leave only that body
                # unfilleted and continue with the rest of the cutout.
                return bodies
            midpoint = len(bodies) // 2
            return self._fillet_body_group(
                component,
                bodies[:midpoint],
                cut_direction,
                fillets,
            ) + self._fillet_body_group(
                component,
                bodies[midpoint:],
                cut_direction,
                fillets,
            )

        if not fillet or fillet.bodies.count == 0:
            return bodies
        fillets.append(fillet)
        return cast(
            list[adsk.fusion.BRepBody],
            utils.fusion.as_list(fillet.bodies),
        )

    def _create_cut_combine(
        self,
        component: adsk.fusion.Component,
        target_body: adsk.fusion.BRepBody,
        tool_bodies: list[adsk.fusion.BRepBody],
    ) -> adsk.fusion.CombineFeature:
        tools = adsk.core.ObjectCollection.createWithArray(
            cast(list[adsk.core.Base], tool_bodies)
        )
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
