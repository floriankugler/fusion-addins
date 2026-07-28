from typing import cast

import adsk.core
import adsk.fusion

from lib import addin, inputs, ui_placement, utils
from lib.fusionbootstrap.runtime import RuntimeInfo


_addin: addin.Addin | None = None


def run(context, runtime_info: RuntimeInfo):
    global _addin
    _addin = ConcealedHingeNative(runtime_info)


def stop(context):
    global _addin
    if _addin:
        _addin.shutdown()
    _addin = None


class ConcealedHingeNativeInputs(inputs.Inputs):
    class Types:
        BLUM_CLIP_TOP_THIN_0 = inputs.DropDownInput.Item(
            "Blum CLIP top 110 Thin +0",
            0,
        )
        BLUM_CLIP_TOP_THIN_3 = inputs.DropDownInput.Item(
            "Blum CLIP top 110 Thin +3",
            1,
        )

    def __init__(self, units_manager: adsk.core.UnitsManager):
        units = units_manager.defaultLengthUnits
        self.door_edge = inputs.SelectionByEntityTokenInput(
            id="door_edge",
            name="Door Edge",
            filter=["LinearEdges"],
            lower_bound=1,
            upper_bound=1,
            tool_tip="Select the hinged edge of one door body.",
        )
        self.carcass_edge = inputs.SelectionByEntityTokenInput(
            id="carcass_edge",
            name="Carcass Board Edge",
            filter=["LinearEdges"],
            lower_bound=1,
            upper_bound=1,
            tool_tip="Select the corresponding edge of the carcass board.",
        )
        self.type = inputs.DropDownInput(
            id="type",
            name="Hinge Type",
            options=utils.misc.class_property_values(
                ConcealedHingeNativeInputs.Types,
                inputs.DropDownInput.Item,
            ),
            default_value=(
                ConcealedHingeNativeInputs.Types.BLUM_CLIP_TOP_THIN_0.value
            ),
            tool_tip="The hinge drilling pattern to use.",
        )
        self.offset = inputs.FloatInput(
            id="offset",
            name="End Margin",
            default_value=6,
            tool_tip=(
                "Distance from each end of the selected door edge to the "
                "corresponding hinge center."
            ),
            units=units,
        )
        self.offset.minimum_value = 2.7
        self.predrill_diameter = inputs.FloatInput(
            id="predrill_diameter",
            name="Predrill Diameter",
            default_value=2.54 / 8,
            tool_tip="Diameter of the carcass screw pilot holes.",
            units=units,
        )
        self.predrill_diameter.minimum_value = 0.01
        self.predrill_depth = inputs.FloatInput(
            id="predrill_depth",
            name="Predrill Depth",
            default_value=0.3,
            tool_tip="Depth of the carcass screw pilot holes.",
            units=units,
        )
        self.predrill_depth.minimum_value = 0.01
        super().__init__()


class ConcealedHingeNative(addin.Addin):
    inputs: ConcealedHingeNativeInputs
    _parameter_prefix: str

    @property
    def plugin_name(self) -> str:
        return "Concealed Hinge (Native)"

    @property
    def plugin_desc(self) -> str:
        return "Create concealed-hinge holes with native Fusion features."

    @property
    def plugin_tooltip(self) -> str:
        return (
            "Creates fully constrained sketches and native cut extrudes for "
            "one explicitly selected door and carcass board."
        )

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

    def create_inputs(self) -> ConcealedHingeNativeInputs:
        design = adsk.fusion.Design.cast(self.app.activeProduct)
        if not design:
            raise RuntimeError(
                "Concealed Hinge (Native) requires an active Fusion design."
            )
        return ConcealedHingeNativeInputs(design.unitsManager)

    def pre_select(self, input, selection) -> bool:
        if not self.inputs or not input:
            return True
        if input.id not in {
            self.inputs.door_edge.id,
            self.inputs.carcass_edge.id,
        }:
            return True
        edge = adsk.fusion.BRepEdge.cast(selection)
        return bool(
            edge
            and edge.body
            and edge.body.isSolid
            and utils.brep.is_linear(edge)
            and utils.brep.largest_face_of_edge(edge)
        )

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

        door_edge = cast(adsk.fusion.BRepEdge, self.inputs.door_edge.value[0])
        carcass_edge = cast(
            adsk.fusion.BRepEdge,
            self.inputs.carcass_edge.value[0],
        )
        door_edge = cast(
            adsk.fusion.BRepEdge,
            door_edge.nativeObject or door_edge,
        )
        carcass_edge = cast(
            adsk.fusion.BRepEdge,
            carcass_edge.nativeObject or carcass_edge,
        )
        door_face = cast(
            adsk.fusion.BRepFace,
            utils.brep.largest_face_of_edge(door_edge),
        )
        carcass_face = cast(
            adsk.fusion.BRepFace,
            utils.brep.largest_face_of_edge(carcass_edge),
        )

        hinge_positions = self._hinge_positions(carcass_edge, door_edge)
        expected_door_centers = self._door_hole_centers(
            carcass_edge,
            door_edge,
            door_face,
            hinge_positions,
        )
        expected_carcass_centers = self._carcass_hole_centers(
            carcass_edge,
            carcass_face,
            door_face,
            hinge_positions,
        )

        design = cast(adsk.fusion.Design, self.app.activeProduct)
        self._parameter_prefix = self._unique_parameter_prefix(design)

        door_sketch, door_pair_lines = self._create_door_sketch(
            door_face,
            door_edge,
            carcass_edge,
            expected_door_centers,
        )
        carcass_sketch = self._create_carcass_sketch(
            carcass_face,
            door_edge,
            door_pair_lines,
            expected_carcass_centers,
        )
        self._verify_hole_centers(
            door_sketch,
            expected_door_centers,
            "door",
        )
        self._verify_hole_centers(
            carcass_sketch,
            expected_carcass_centers,
            "carcass",
        )

        self._create_cut_extrude(
            door_face,
            door_sketch,
            depth_expression="5 mm",
            name="Concealed Hinge - Door Holes",
            parameter_role="doorDepth",
        )
        carcass_cut = self._create_cut_extrude(
            carcass_face,
            carcass_sketch,
            depth_expression=self.inputs.predrill_depth.expression,
            name="Concealed Hinge - Carcass Holes",
            parameter_role="carcassDepth",
        )
        self._group_features(design, door_sketch, carcass_cut)

    def _validation_error(self) -> str | None:
        design = adsk.fusion.Design.cast(self.app.activeProduct)
        if not design:
            return "An active Fusion design is required."
        if design.designType != adsk.fusion.DesignTypes.ParametricDesignType:  # type: ignore
            return (
                "Concealed Hinge (Native) requires Design History "
                "(a parametric design)."
            )
        if not self.inputs or len(self.inputs.door_edge.value) != 1:
            return "Select one Door Edge."
        if len(self.inputs.carcass_edge.value) != 1:
            return "Select one Carcass Board Edge."

        door_edge = adsk.fusion.BRepEdge.cast(self.inputs.door_edge.value[0])
        carcass_edge = adsk.fusion.BRepEdge.cast(
            self.inputs.carcass_edge.value[0]
        )
        if not door_edge or not utils.brep.is_linear(door_edge):
            return "The Door Edge must be a straight body edge."
        if not carcass_edge or not utils.brep.is_linear(carcass_edge):
            return "The Carcass Board Edge must be a straight body edge."
        if not door_edge.body.isSolid or not carcass_edge.body.isSolid:
            return "Both selected edges must belong to solid bodies."
        native_door_body = door_edge.body.nativeObject or door_edge.body
        native_carcass_body = (
            carcass_edge.body.nativeObject or carcass_edge.body
        )
        if native_door_body == native_carcass_body:
            return "Select edges on two different bodies."
        if not utils.brep.is_parallel(door_edge, carcass_edge):
            return "The Door Edge and Carcass Board Edge must be parallel."

        door_face = utils.brep.largest_face_of_edge(door_edge)
        carcass_face = utils.brep.largest_face_of_edge(carcass_edge)
        if not door_face or not carcass_face:
            return "Each selected edge must border a planar board face."
        try:
            utils.brep.get_opposite_face(door_face)
            utils.brep.get_opposite_face(carcass_face)
        except ValueError:
            return "Each selected board face must have an opposite planar face."
        if (
            door_face.body.parentComponent.parentDesign != design
            or carcass_face.body.parentComponent.parentDesign != design
        ):
            return "Both selected bodies must belong to the active design."
        native_door_component = (
            (door_edge.nativeObject or door_edge).body.parentComponent
        )
        native_carcass_component = (
            (carcass_edge.nativeObject or carcass_edge).body.parentComponent
        )
        if native_door_component != native_carcass_component:
            return (
                "The two selected bodies must belong to the same component "
                "so their edges can be linked between the native sketches."
            )
        if native_door_component != design.activeComponent:
            return (
                "Activate the component that owns both selected bodies, then "
                "run Concealed Hinge (Native) again."
            )
        if self.inputs.offset.value <= 0:
            return "End Margin must be greater than zero."
        if self.inputs.predrill_diameter.value <= 0:
            return "Predrill Diameter must be greater than zero."
        if self.inputs.predrill_depth.value <= 0:
            return "Predrill Depth must be greater than zero."

        positions = self._hinge_positions(carcass_edge, door_edge)
        if len(positions) != 2:
            return "The Door Edge is too short for this End Margin."
        door_centers = self._door_hole_centers(
            carcass_edge,
            door_edge,
            door_face,
            positions,
        )
        carcass_centers = self._carcass_hole_centers(
            carcass_edge,
            carcass_face,
            door_face,
            positions,
        )
        if not all(door_face.isPointOnFace(point, 1e-5) for point in door_centers):
            return "The resulting door holes do not fit on the selected door face."
        if not all(
            carcass_face.isPointOnFace(point, 1e-5)
            for point in carcass_centers
        ):
            return (
                "The resulting carcass holes do not fit on the selected "
                "carcass face."
            )
        return None

    def _hinge_positions(
        self,
        carcass_edge: adsk.fusion.BRepEdge,
        door_edge: adsk.fusion.BRepEdge,
    ) -> list[adsk.core.Vector3D]:
        start_point = utils.brep.project_point_onto_edge(
            door_edge.startVertex.geometry,
            carcass_edge,
        )
        end_point = utils.brep.project_point_onto_edge(
            door_edge.endVertex.geometry,
            carcass_edge,
        )
        direction = utils.vector.subtract(
            end_point.asVector(),
            start_point.asVector(),
        )
        offset = self.inputs.offset.value
        if direction.length <= 2 * offset + 1e-6:
            return []
        return utils.vector.compute_points_along_vector(
            start_point,
            direction,
            [offset, direction.length - offset],
        )

    def _door_hole_centers(
        self,
        carcass_edge: adsk.fusion.BRepEdge,
        door_edge: adsk.fusion.BRepEdge,
        door_face: adsk.fusion.BRepFace,
        hinge_positions: list[adsk.core.Vector3D],
    ) -> list[adsk.core.Point3D]:
        normal_into_door_face = utils.brep.normal_into_face(
            door_edge,
            door_face,
        )
        edge_delta = utils.vector.subtract(
            door_edge.startVertex.geometry.asVector(),
            carcass_edge.startVertex.geometry.asVector(),
        )
        inset = -normal_into_door_face.dotProduct(edge_delta)
        if (
            self.inputs.type.value
            == ConcealedHingeNativeInputs.Types.BLUM_CLIP_TOP_THIN_0.value
        ):
            inset += 2.7
        elif (
            self.inputs.type.value
            == ConcealedHingeNativeInputs.Types.BLUM_CLIP_TOP_THIN_3.value
        ):
            inset += 3.0
        else:
            raise ValueError("Unsupported hinge type.")
        return self._paired_hole_centers(
            door_face,
            door_edge,
            hinge_positions,
            inset,
        )

    def _carcass_hole_centers(
        self,
        carcass_edge: adsk.fusion.BRepEdge,
        carcass_face: adsk.fusion.BRepFace,
        door_face: adsk.fusion.BRepFace,
        hinge_positions: list[adsk.core.Vector3D],
    ) -> list[adsk.core.Point3D]:
        point_on_door_face = utils.brep.project_point_onto_face(
            hinge_positions[0].asPoint(),
            door_face,
        )
        normal_into_carcass_face = utils.brep.normal_into_face(
            carcass_edge,
            carcass_face,
        )
        gap_vector = utils.vector.subtract(
            point_on_door_face.asVector(),
            hinge_positions[0],
        )
        gap = -normal_into_carcass_face.dotProduct(gap_vector)
        inset = 3.7 - (gap - 0.15)
        return self._paired_hole_centers(
            carcass_face,
            carcass_edge,
            hinge_positions,
            inset,
        )

    def _paired_hole_centers(
        self,
        face: adsk.fusion.BRepFace,
        edge: adsk.fusion.BRepEdge,
        hinge_positions: list[adsk.core.Vector3D],
        inset: float,
    ) -> list[adsk.core.Point3D]:
        origin, x_axis, y_axis, _ = utils.brep.coordinate_system_on_face(
            face,
            edge,
        )
        centers: list[adsk.core.Point3D] = []
        for position in hinge_positions:
            along_edge = utils.vector.subtract(
                position,
                origin.asVector(),
            ).dotProduct(x_axis)
            for pair_offset in (-1.6, 1.6):
                center = origin.asVector()
                center.add(
                    utils.vector.scaled_by(
                        x_axis,
                        along_edge + pair_offset,
                    )
                )
                center.add(utils.vector.scaled_by(y_axis, inset))
                centers.append(center.asPoint())
        return centers

    def _create_door_sketch(
        self,
        face: adsk.fusion.BRepFace,
        door_edge: adsk.fusion.BRepEdge,
        carcass_edge: adsk.fusion.BRepEdge,
        expected_centers: list[adsk.core.Point3D],
    ) -> tuple[adsk.fusion.Sketch, list[adsk.fusion.SketchLine]]:
        if len(expected_centers) != 4:
            raise ValueError("The door sketch requires four hole centers.")
        component = face.body.parentComponent
        sketch = component.sketches.addWithoutEdges(face)
        if not sketch:
            raise RuntimeError(
                "Fusion failed to create the door hinge sketch."
            )
        sketch.name = "Concealed Hinge - Door Positions"

        projected_door_edge = self._project_line(
            sketch,
            door_edge,
            "door edge",
        )
        projected_carcass_edge = self._project_line(
            sketch,
            carcass_edge,
            "carcass edge",
        )
        door_pattern_offset, door_pattern_expression = (
            self._door_pattern_offset()
        )
        hole_row = self._add_linked_offset_line(
            sketch,
            projected_carcass_edge,
            expected_centers[0],
            door_pattern_offset,
            door_pattern_expression,
            "doorPatternOffset",
        )

        door_start = self._nearest_line_endpoint(
            projected_door_edge,
            sketch.modelToSketchSpace(door_edge.startVertex.geometry),
        )
        door_end = self._nearest_line_endpoint(
            projected_door_edge,
            sketch.modelToSketchSpace(door_edge.endVertex.geometry),
        )
        constraints = sketch.geometricConstraints
        lines = sketch.sketchCurves.sketchLines
        pair_lines: list[adsk.fusion.SketchLine] = []
        circle_centers: list[adsk.fusion.SketchPoint] = []
        spacing_expression = "32 mm"
        margin_expression = self.inputs.offset.expression

        for hinge_index in range(2):
            first_center = expected_centers[hinge_index * 2]
            second_center = expected_centers[hinge_index * 2 + 1]
            first_in_sketch = sketch.modelToSketchSpace(first_center)
            second_in_sketch = sketch.modelToSketchSpace(second_center)
            pair_line = lines.addByTwoPoints(
                first_in_sketch,
                second_in_sketch,
            )
            if not pair_line:
                raise RuntimeError(
                    "Fusion failed to create a door hinge-pair reference."
                )
            pair_line.isConstruction = True
            if not constraints.addCollinear(hole_row, pair_line):
                raise RuntimeError(
                    "Fusion failed to align a door hinge-pair reference."
                )
            spacing_dimension = self._add_distance_dimension(
                sketch,
                pair_line.startSketchPoint,
                pair_line.endSketchPoint,
                spacing_expression,
                f"doorHinge{hinge_index + 1}HoleSpacing",
            )
            spacing_expression = spacing_dimension.parameter.name

            midpoint_model = adsk.core.Point3D.create(
                (first_center.x + second_center.x) / 2,
                (first_center.y + second_center.y) / 2,
                (first_center.z + second_center.z) / 2,
            )
            station_model = utils.brep.project_point_onto_edge(
                midpoint_model,
                door_edge,
            )
            normal_line = lines.addByTwoPoints(
                sketch.modelToSketchSpace(station_model),
                sketch.modelToSketchSpace(midpoint_model),
            )
            if not normal_line:
                raise RuntimeError(
                    "Fusion failed to create a door hinge margin reference."
                )
            normal_line.isConstruction = True
            if not constraints.addCoincident(
                normal_line.startSketchPoint,
                projected_door_edge,
            ):
                raise RuntimeError(
                    "Fusion failed to attach a hinge margin to the door edge."
                )
            if not constraints.addPerpendicular(
                projected_door_edge,
                normal_line,
            ):
                raise RuntimeError(
                    "Fusion failed to orient a hinge margin reference."
                )
            if not constraints.addMidPoint(
                normal_line.endSketchPoint,
                pair_line,
            ):
                raise RuntimeError(
                    "Fusion failed to center a door hinge hole pair."
                )

            margin_endpoint = door_start if hinge_index == 0 else door_end
            margin_dimension = self._add_distance_dimension(
                sketch,
                margin_endpoint,
                normal_line.startSketchPoint,
                margin_expression,
                (
                    "doorStartMargin"
                    if hinge_index == 0
                    else "doorEndMargin"
                ),
            )
            margin_expression = margin_dimension.parameter.name
            pair_lines.append(pair_line)
            circle_centers.extend(
                [
                    pair_line.startSketchPoint,
                    pair_line.endSketchPoint,
                ]
            )

        self._add_equal_circles(
            sketch,
            circle_centers,
            radius=0.5,
            diameter_expression="10 mm",
            parameter_role="doorDiameter",
        )
        self._require_fully_constrained(sketch)
        return sketch, pair_lines

    def _create_carcass_sketch(
        self,
        face: adsk.fusion.BRepFace,
        door_edge: adsk.fusion.BRepEdge,
        door_pair_lines: list[adsk.fusion.SketchLine],
        expected_centers: list[adsk.core.Point3D],
    ) -> adsk.fusion.Sketch:
        if len(door_pair_lines) != 2 or len(expected_centers) != 4:
            raise ValueError(
                "The carcass sketch requires two door alignment references "
                "and four hole centers."
            )
        component = face.body.parentComponent
        sketch = component.sketches.addWithoutEdges(face)
        if not sketch:
            raise RuntimeError(
                "Fusion failed to create the carcass hinge sketch."
            )
        sketch.name = "Concealed Hinge - Carcass Positions"

        projected_door_edge = self._project_line(
            sketch,
            door_edge,
            "door edge",
        )
        hole_row = self._add_linked_offset_line(
            sketch,
            projected_door_edge,
            expected_centers[0],
            3.85,
            "38.5 mm",
            "carcassPatternOffset",
        )

        constraints = sketch.geometricConstraints
        lines = sketch.sketchCurves.sketchLines
        remaining_centers = [point.copy() for point in expected_centers]
        circle_centers: list[adsk.fusion.SketchPoint] = []
        for hinge_index, door_pair_line in enumerate(door_pair_lines, start=1):
            projected_pair = self._project_line(
                sketch,
                door_pair_line,
                f"door hinge {hinge_index} hole pair",
            )
            for endpoint in (
                projected_pair.startSketchPoint,
                projected_pair.endSketchPoint,
            ):
                endpoint_model = sketch.sketchToModelSpace(
                    endpoint.geometry
                )
                expected_center = min(
                    remaining_centers,
                    key=lambda point: point.distanceTo(endpoint_model),
                )
                remaining_centers.remove(expected_center)
                transfer_line = lines.addByTwoPoints(
                    endpoint,
                    sketch.modelToSketchSpace(expected_center),
                )
                if not transfer_line:
                    raise RuntimeError(
                        "Fusion failed to transfer a door hinge position "
                        "into the carcass sketch."
                    )
                transfer_line.isConstruction = True
                if not constraints.addPerpendicular(
                    projected_door_edge,
                    transfer_line,
                ):
                    raise RuntimeError(
                        "Fusion failed to align a carcass hinge position."
                    )
                if not constraints.addCoincident(
                    transfer_line.endSketchPoint,
                    hole_row,
                ):
                    raise RuntimeError(
                        "Fusion failed to attach a carcass hole to its row."
                    )
                circle_centers.append(transfer_line.endSketchPoint)

        self._add_equal_circles(
            sketch,
            circle_centers,
            radius=self.inputs.predrill_diameter.value / 2,
            diameter_expression=self.inputs.predrill_diameter.expression,
            parameter_role="carcassDiameter",
        )
        self._require_fully_constrained(sketch)
        return sketch

    def _project_line(
        self,
        sketch: adsk.fusion.Sketch,
        source: adsk.core.Base,
        description: str,
    ) -> adsk.fusion.SketchLine:
        projected = sketch.project2(
            cast(list[adsk.core.Base], [source]),
            True,
        )
        line = next(
            (
                candidate
                for entity in projected
                if (candidate := adsk.fusion.SketchLine.cast(entity))
            ),
            None,
        )
        if not line:
            raise RuntimeError(
                f"Fusion failed to project the {description} into "
                f"'{sketch.name}'."
            )
        line.isConstruction = True
        return line

    def _door_pattern_offset(self) -> tuple[float, str]:
        if (
            self.inputs.type.value
            == ConcealedHingeNativeInputs.Types.BLUM_CLIP_TOP_THIN_0.value
        ):
            return 2.7, "27 mm"
        if (
            self.inputs.type.value
            == ConcealedHingeNativeInputs.Types.BLUM_CLIP_TOP_THIN_3.value
        ):
            return 3.0, "30 mm"
        raise ValueError("Unsupported hinge type.")

    def _add_linked_offset_line(
        self,
        sketch: adsk.fusion.Sketch,
        source_line: adsk.fusion.SketchLine,
        expected_model_point: adsk.core.Point3D,
        distance: float,
        expression: str,
        parameter_role: str,
    ) -> adsk.fusion.SketchLine:
        expected_point = sketch.modelToSketchSpace(expected_model_point)
        expected_point.z = 0
        source_start = source_line.startSketchPoint.geometry
        source_end = source_line.endSketchPoint.geometry
        source_direction = source_start.vectorTo(source_end)
        if not source_direction.normalize():
            raise RuntimeError("A projected reference has zero length.")
        normal = adsk.core.Vector3D.create(
            -source_direction.y,
            source_direction.x,
            0,
        )
        opposite_normal = normal.copy()
        opposite_normal.scaleBy(-1)
        expected_delta = source_start.vectorTo(expected_point)
        if opposite_normal.dotProduct(expected_delta) > normal.dotProduct(
            expected_delta
        ):
            normal = opposite_normal
        offset_vector = normal.copy()
        offset_vector.scaleBy(distance)
        row_start = source_start.copy()
        row_start.translateBy(offset_vector)
        row_end = source_end.copy()
        row_end.translateBy(offset_vector)

        lines = sketch.sketchCurves.sketchLines
        constraints = sketch.geometricConstraints
        row_line = lines.addByTwoPoints(row_start, row_end)
        if not row_line:
            raise RuntimeError(
                f"Fusion failed to create a linked row in '{sketch.name}'."
            )
        row_line.isConstruction = True
        if not constraints.addParallel(source_line, row_line):
            raise RuntimeError(
                f"Fusion failed to orient a row in '{sketch.name}'."
            )
        if not constraints.addEqual(source_line, row_line):
            raise RuntimeError(
                f"Fusion failed to match a row in '{sketch.name}'."
            )

        offset_line = lines.addByTwoPoints(
            source_line.startSketchPoint,
            row_line.startSketchPoint,
        )
        if not offset_line:
            raise RuntimeError(
                f"Fusion failed to locate a row in '{sketch.name}'."
            )
        offset_line.isConstruction = True
        if not constraints.addPerpendicular(source_line, offset_line):
            raise RuntimeError(
                f"Fusion failed to constrain a row offset in '{sketch.name}'."
            )
        self._add_distance_dimension(
            sketch,
            offset_line.startSketchPoint,
            offset_line.endSketchPoint,
            expression,
            parameter_role,
        )
        if self._point_to_line_distance(expected_point, row_line) > max(
            self.app.pointTolerance * 100,
            1e-5,
        ):
            raise RuntimeError(
                f"The linked row in '{sketch.name}' is on the wrong side."
            )
        return row_line

    def _point_to_line_distance(
        self,
        point: adsk.core.Point3D,
        line: adsk.fusion.SketchLine,
    ) -> float:
        start = line.startSketchPoint.geometry
        end = line.endSketchPoint.geometry
        direction = start.vectorTo(end)
        length = direction.length
        if length <= 1e-9:
            raise RuntimeError("A projected reference has zero length.")
        offset = start.vectorTo(point)
        return abs(direction.x * offset.y - direction.y * offset.x) / length

    def _nearest_line_endpoint(
        self,
        line: adsk.fusion.SketchLine,
        point: adsk.core.Point3D,
    ) -> adsk.fusion.SketchPoint:
        return min(
            (line.startSketchPoint, line.endSketchPoint),
            key=lambda endpoint: endpoint.geometry.distanceTo(point),
        )

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
                raise RuntimeError(
                    f"Fusion failed to create a circle in '{sketch.name}'."
                )
            if not constraints.addCoincident(
                circle.centerSketchPoint,
                center,
            ):
                raise RuntimeError(
                    f"Fusion failed to constrain a circle in '{sketch.name}'."
                )
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
                f"Fusion failed to dimension circles in '{sketch.name}'."
            )
        diameter.parameter.expression = diameter_expression
        self._name_parameter(diameter.parameter, parameter_role)
        for circle in circles[1:]:
            if not constraints.addEqual(circles[0], circle):
                raise RuntimeError(
                    f"Fusion failed to equalize circles in '{sketch.name}'."
                )
        return circles

    def _add_distance_dimension(
        self,
        sketch: adsk.fusion.Sketch,
        start: adsk.fusion.SketchPoint,
        end: adsk.fusion.SketchPoint,
        expression: str,
        parameter_role: str,
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
        )
        if not dimension or not dimension.parameter:
            raise RuntimeError(
                f"Fusion failed to create a distance in '{sketch.name}'."
            )
        dimension.parameter.expression = expression
        self._name_parameter(dimension.parameter, parameter_role)
        return dimension

    def _verify_hole_centers(
        self,
        sketch: adsk.fusion.Sketch,
        expected_centers: list[adsk.core.Point3D],
        role: str,
    ) -> None:
        actual_centers = [
            sketch.sketchToModelSpace(circle.centerSketchPoint.geometry)
            for circle in sketch.sketchCurves.sketchCircles
        ]
        if len(actual_centers) != len(expected_centers):
            raise RuntimeError(
                f"The {role} sketch created the wrong number of holes."
            )
        tolerance = max(self.app.pointTolerance * 100, 1e-5)
        remaining = list(actual_centers)
        for expected in expected_centers:
            actual = min(
                remaining,
                key=lambda point: point.distanceTo(expected),
            )
            error = actual.distanceTo(expected)
            if error > tolerance:
                raise RuntimeError(
                    f"The {role} sketch differs from the original concealed "
                    f"hinge position by {error:.6g} cm."
                )
            remaining.remove(actual)

    def _create_cut_extrude(
        self,
        face: adsk.fusion.BRepFace,
        sketch: adsk.fusion.Sketch,
        depth_expression: str,
        name: str,
        parameter_role: str,
    ) -> adsk.fusion.ExtrudeFeature:
        component = face.body.parentComponent
        profiles = adsk.core.ObjectCollection.create()
        for profile in sketch.profiles:
            profiles.add(profile)
        if profiles.count != 4:
            raise RuntimeError(
                f"'{sketch.name}' must create exactly four hole profiles."
            )

        extrude_input = component.features.extrudeFeatures.createInput(
            profiles,
            adsk.fusion.FeatureOperations.CutFeatureOperation,  # type: ignore
        )
        if not extrude_input:
            raise RuntimeError(f"Fusion failed to initialize '{name}'.")
        extent = adsk.fusion.DistanceExtentDefinition.create(
            adsk.core.ValueInput.createByString(depth_expression)
        )
        if not extent:
            raise RuntimeError(f"Fusion failed to define the depth of '{name}'.")

        normal_into_body = utils.brep.normal_towards_face(
            face,
            utils.brep.get_opposite_face(face),
        )
        sketch_normal = sketch.xDirection.crossProduct(sketch.yDirection)
        extent_direction = (
            adsk.fusion.ExtentDirections.PositiveExtentDirection
            if sketch_normal.dotProduct(normal_into_body) >= 0
            else adsk.fusion.ExtentDirections.NegativeExtentDirection
        )
        if not extrude_input.setOneSideExtent(extent, extent_direction):
            raise RuntimeError(f"Fusion rejected the depth of '{name}'.")
        extrude_input.participantBodies = [face.body]

        extrude = component.features.extrudeFeatures.add(extrude_input)
        if not extrude:
            raise RuntimeError(f"Fusion failed to create '{name}'.")
        extrude.name = name
        sketch.isVisible = False
        final_extent = adsk.fusion.DistanceExtentDefinition.cast(
            extrude.extentOne
        )
        if not final_extent or not final_extent.distance:
            raise RuntimeError(
                f"Fusion did not create a distance parameter for '{name}'."
            )
        self._name_parameter(final_extent.distance, parameter_role)
        self._name_feature_parameters(
            extrude,
            parameter_role,
            excluded=final_extent.distance,
        )
        return extrude

    def _unique_parameter_prefix(
        self,
        design: adsk.fusion.Design,
    ) -> str:
        parameter_names = {parameter.name for parameter in design.allParameters}
        base = "concealedHingeNative"
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

    def _name_feature_parameters(
        self,
        feature: adsk.fusion.Feature,
        base_role: str,
        excluded: adsk.fusion.ModelParameter | None = None,
    ) -> None:
        suffixes = {
            "AlongDistance": "distance",
            "Side1Offset": "endOffset",
            "TaperAngle": "taperAngle",
        }
        fallback_index = 1
        for parameter in feature.parentComponent.modelParameters:
            if parameter.createdBy != feature or parameter == excluded:
                continue
            suffix = suffixes.get(parameter.role)
            if not suffix:
                suffix = f"parameter{fallback_index}"
                fallback_index += 1
            self._name_parameter(parameter, f"{base_role}_{suffix}")

    def _require_fully_constrained(
        self,
        sketch: adsk.fusion.Sketch,
    ) -> None:
        fixed_geometry = [
            entity
            for entity in [
                *list(sketch.sketchCurves),
                *list(sketch.sketchPoints),
            ]
            if entity != sketch.originPoint
            if entity.isFixed and not entity.isReference
        ]
        if fixed_geometry:
            raise RuntimeError(
                f"'{sketch.name}' contains fixed sketch geometry."
            )
        if sketch.isFullyConstrained:
            return
        unconstrained_curves = sum(
            1
            for curve in sketch.sketchCurves
            if not curve.isFullyConstrained
        )
        raise RuntimeError(
            f"'{sketch.name}' is under-constrained "
            f"({unconstrained_curves} unconstrained curves)."
        )

    def _group_features(
        self,
        design: adsk.fusion.Design,
        first_sketch: adsk.fusion.Sketch,
        last_feature: adsk.fusion.Feature,
    ) -> None:
        group = design.timeline.timelineGroups.add(
            first_sketch.timelineObject.index,
            last_feature.timelineObject.index,
        )
        if not group:
            raise RuntimeError(
                "Fusion created the hinge features but could not group them."
            )
        group.name = "Concealed Hinge (Native)"
        group.isCollapsed = False
