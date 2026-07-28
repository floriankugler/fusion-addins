from dataclasses import dataclass
from typing import cast

import adsk.core
import adsk.fusion

from lib import addin, inputs, ui_placement, utils
from lib.fusionbootstrap.runtime import RuntimeInfo


_addin: addin.Addin | None = None


@dataclass(frozen=True)
class _Hole:
    center: adsk.core.Point3D
    diameter: float


def run(context, runtime_info: RuntimeInfo):
    global _addin
    _addin = DoorLatchNative(runtime_info)


def stop(context):
    global _addin
    if _addin:
        _addin.shutdown()
    _addin = None


class DoorLatchNativeInputs(inputs.Inputs):
    class Types:
        EVERLOCK = inputs.DropDownInput.Item("Everlock", 0)
        PULL_LOCK_44 = inputs.DropDownInput.Item("Pull Lock 44mm", 1)

    def __init__(self, units_manager: adsk.core.UnitsManager):
        units = units_manager.defaultLengthUnits
        self.door_edge = inputs.SelectionByEntityTokenInput(
            id="door_edge",
            name="Door Edge",
            filter=["LinearEdges"],
            lower_bound=1,
            upper_bound=1,
            tool_tip=(
                "Select the door or drawer edge beside which the latch is "
                "installed."
            ),
        )
        self.carcass_edge = inputs.SelectionByEntityTokenInput(
            id="carcass_edge",
            name="Carcass Face Edge",
            filter=["LinearEdges"],
            lower_bound=1,
            upper_bound=1,
            tool_tip=(
                "Select the corresponding edge of the carcass face. The edge "
                "must run parallel to the selected Door Edge."
            ),
        )
        self.type = inputs.DropDownInput(
            id="type",
            name="Latch Type",
            options=utils.misc.class_property_values(
                DoorLatchNativeInputs.Types,
                inputs.DropDownInput.Item,
            ),
            default_value=DoorLatchNativeInputs.Types.EVERLOCK.value,
            tool_tip="The latch drilling pattern to create.",
        )
        self.number = inputs.IntegerInput(
            id="number",
            name="Number of Latches",
            default_value=1,
            minimum=1,
            maximum=10,
            tool_tip="The number of latch stations along the door edge.",
        )
        self.offset = inputs.FloatInput(
            id="offset",
            name="End Offset",
            default_value=10,
            tool_tip=(
                "Distance from each end of the Door Edge to the first and "
                "last latch station."
            ),
            units=units,
            update_visibility=lambda: self.number.value > 1,
        )
        self.offset.minimum_value = 0.0001
        self.predrill_diameter = inputs.FloatInput(
            id="predrill_diameter",
            name="Predrill Diameter",
            default_value=2.54 / 8,
            tool_tip="Diameter of the latch screw pilot holes.",
            units=units,
        )
        self.predrill_diameter.minimum_value = 0.0001
        self.predrill_depth = inputs.FloatInput(
            id="predrill_depth",
            name="Predrill Depth",
            default_value=0.3,
            tool_tip="Depth of the latch screw pilot holes.",
            units=units,
        )
        self.predrill_depth.minimum_value = 0.0001
        super().__init__()


class DoorLatchNative(addin.Addin):
    inputs: DoorLatchNativeInputs
    _parameter_prefix: str

    @property
    def plugin_name(self) -> str:
        return "Door Latch (Native)"

    @property
    def plugin_desc(self) -> str:
        return "Create door-latch holes with native Fusion features."

    @property
    def plugin_tooltip(self) -> str:
        return (
            "Creates fully constrained sketches and native cut extrudes from "
            "one explicitly selected door edge and carcass-face edge."
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

    def create_inputs(self) -> DoorLatchNativeInputs:
        design = adsk.fusion.Design.cast(self.app.activeProduct)
        if not design:
            raise RuntimeError(
                "Door Latch (Native) requires an active Fusion design."
            )
        return DoorLatchNativeInputs(design.unitsManager)

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

        door_edge = cast(
            adsk.fusion.BRepEdge,
            self.inputs.door_edge.value[0],
        )
        carcass_edge = cast(
            adsk.fusion.BRepEdge,
            self.inputs.carcass_edge.value[0],
        )
        door_face = cast(
            adsk.fusion.BRepFace,
            utils.brep.largest_face_of_edge(door_edge),
        )
        carcass_face = cast(
            adsk.fusion.BRepFace,
            utils.brep.largest_face_of_edge(carcass_edge),
        )
        door_occurrence = door_face.assemblyContext
        carcass_occurrence = carcass_face.assemblyContext
        latch_positions = self._latch_positions(door_edge)
        door_groups = self._door_hole_groups(
            carcass_edge,
            door_edge,
            door_face,
            latch_positions,
        )
        carcass_holes = self._carcass_holes(
            carcass_edge,
            carcass_face,
            latch_positions,
        )

        design = cast(adsk.fusion.Design, self.app.activeProduct)
        self._parameter_prefix = self._unique_parameter_prefix(design)

        native_door_face, native_door_edge, native_door_groups = (
            self._native_face_edge_and_hole_groups(
                door_face,
                door_edge,
                door_groups,
            )
        )
        native_carcass_face, native_carcass_edge, native_carcass_groups = (
            self._native_face_edge_and_hole_groups(
                carcass_face,
                carcass_edge,
                [carcass_holes],
            )
        )

        first_sketch: adsk.fusion.Sketch
        if (
            self.inputs.type.value
            == DoorLatchNativeInputs.Types.EVERLOCK.value
        ):
            (
                door_layout_sketch,
                door_pilot_circles,
                door_main_circles,
            ) = self._create_everlock_door_sketch(
                native_door_face,
                native_door_edge,
                native_carcass_edge,
                door_occurrence,
                carcass_occurrence,
                native_door_groups[0],
                native_door_groups[1],
            )
            first_sketch = door_layout_sketch
            self._create_distance_cut(
                native_door_face,
                door_layout_sketch,
                depth_value=self.inputs.predrill_depth.value,
                depth_expression=self.inputs.predrill_depth.expression,
                name="Door Latch (Native) - Door Pilot Holes",
                parameter_role="doorPilotDepth",
                profiles=self._profiles_for_circles(
                    door_layout_sketch,
                    door_pilot_circles,
                ),
            )
            self._create_through_cut(
                native_door_face,
                door_layout_sketch,
                name="Door Latch (Native) - Finger Holes",
                parameter_role="fingerHoleCut",
                profiles=self._profiles_for_circles(
                    door_layout_sketch,
                    door_main_circles,
                ),
            )
            door_main_points = [
                circle.centerSketchPoint
                for circle in door_main_circles
            ]
        elif (
            self.inputs.type.value
            == DoorLatchNativeInputs.Types.PULL_LOCK_44.value
        ):
            lock_sketch, lock_circles = self._create_pull_lock_door_sketch(
                native_door_face,
                native_door_edge,
                native_carcass_edge,
                door_occurrence,
                carcass_occurrence,
                native_door_groups[0],
            )
            first_sketch = lock_sketch
            self._create_through_cut(
                native_door_face,
                lock_sketch,
                name="Door Latch (Native) - Pull Lock Through Holes",
                parameter_role="pullLockThroughCut",
            )
            door_main_points = [
                circle.centerSketchPoint
                for circle in lock_circles
            ]
            if len(native_door_groups) > 1:
                counterbore_sketch = self._create_projected_circle_sketch(
                    native_door_face,
                    door_occurrence,
                    door_main_points,
                    diameter_expression="48 mm",
                    name="Door Latch (Native) - Pull Lock Counterbore Layout",
                    parameter_role="pullLockCounterboreDiameter",
                )
                counterbore_depth = (
                    utils.brep.get_board_thickness(native_door_face) - 1.0
                )
                self._create_distance_cut(
                    native_door_face,
                    counterbore_sketch,
                    depth_value=counterbore_depth,
                    depth_expression=None,
                    name="Door Latch (Native) - Pull Lock Counterbores",
                    parameter_role="pullLockCounterboreDepth",
                )
        else:
            raise ValueError("Unsupported latch type.")

        carcass_sketch = self._create_carcass_sketch_from_door(
            native_carcass_face,
            native_door_edge,
            carcass_occurrence,
            door_occurrence,
            door_main_points,
            native_carcass_groups[0],
        )
        carcass_cut = self._create_distance_cut(
            native_carcass_face,
            carcass_sketch,
            depth_value=self.inputs.predrill_depth.value,
            depth_expression=self.inputs.predrill_depth.expression,
            name="Door Latch (Native) - Carcass Pilot Holes",
            parameter_role="carcassPilotDepth",
        )
        self._group_features(design, first_sketch, carcass_cut)

    def _validation_error(self) -> str | None:
        design = adsk.fusion.Design.cast(self.app.activeProduct)
        if not design:
            return "An active Fusion design is required."
        if design.designType != adsk.fusion.DesignTypes.ParametricDesignType:  # type: ignore
            return (
                "Door Latch (Native) requires Design History "
                "(a parametric design)."
            )
        if not self.inputs or len(self.inputs.door_edge.value) != 1:
            return "Select one Door Edge."
        if len(self.inputs.carcass_edge.value) != 1:
            return "Select one Carcass Face Edge."

        door_edge = adsk.fusion.BRepEdge.cast(
            self.inputs.door_edge.value[0]
        )
        carcass_edge = adsk.fusion.BRepEdge.cast(
            self.inputs.carcass_edge.value[0]
        )
        if not door_edge or not utils.brep.is_linear(door_edge):
            return "The Door Edge must be a straight body edge."
        if not carcass_edge or not utils.brep.is_linear(carcass_edge):
            return "The Carcass Face Edge must be a straight body edge."
        if not door_edge.body.isSolid or not carcass_edge.body.isSolid:
            return "Both selected edges must belong to solid bodies."
        native_door_body = door_edge.body.nativeObject or door_edge.body
        native_carcass_body = carcass_edge.body.nativeObject or carcass_edge.body
        if native_door_body == native_carcass_body:
            return "Select edges on two different bodies."
        if not utils.brep.is_parallel(door_edge, carcass_edge):
            return "The Door Edge and Carcass Face Edge must be parallel."

        door_face = utils.brep.largest_face_of_edge(door_edge)
        carcass_face = utils.brep.largest_face_of_edge(carcass_edge)
        if not door_face or not carcass_face:
            return "Each selected edge must border a planar board face."
        try:
            utils.brep.get_opposite_face(door_face)
            carcass_opposite = utils.brep.get_opposite_face(carcass_face)
        except ValueError:
            return "Each selected board face must have an opposite planar face."
        if (
            door_face.body.parentComponent.parentDesign != design
            or carcass_face.body.parentComponent.parentDesign != design
        ):
            return "Both selected bodies must belong to the active design."

        door_inset_direction = utils.brep.normal_into_face(
            door_edge,
            door_face,
        )
        carcass_body_direction = utils.brep.normal_towards_face(
            carcass_face,
            carcass_opposite,
        )
        if not utils.vector.is_opposite_direction(
            door_inset_direction,
            carcass_body_direction,
        ):
            return (
                "The selected edges do not describe a door edge facing the "
                "selected carcass board."
            )
        if self.inputs.number.value > 1:
            if self.inputs.offset.value <= 0:
                return "End Offset must be greater than zero."
            if door_edge.length <= 2 * self.inputs.offset.value:
                return (
                    "The Door Edge is too short for the requested End Offset."
                )
        if self.inputs.predrill_diameter.value <= 0:
            return "Predrill Diameter must be greater than zero."
        if self.inputs.predrill_depth.value <= 0:
            return "Predrill Depth must be greater than zero."

        latch_positions = self._latch_positions(door_edge)
        if len(latch_positions) != self.inputs.number.value:
            return "Could not place every latch station on the Door Edge."
        door_groups = self._door_hole_groups(
            carcass_edge,
            door_edge,
            door_face,
            latch_positions,
        )
        carcass_holes = self._carcass_holes(
            carcass_edge,
            carcass_face,
            latch_positions,
        )
        for group in door_groups:
            if not self._holes_fit_face(
                door_face,
                door_edge,
                group,
            ):
                return (
                    "The resulting door holes do not fit on the selected "
                    "door face."
                )
        if not self._holes_fit_face(
            carcass_face,
            carcass_edge,
            carcass_holes,
        ):
            return (
                "The resulting carcass holes do not fit on the selected "
                "carcass face."
            )
        return None

    def _latch_positions(
        self,
        door_edge: adsk.fusion.BRepEdge,
    ) -> list[adsk.core.Vector3D]:
        count = self.inputs.number.value
        if count == 1:
            distances = [door_edge.length / 2]
        else:
            available = door_edge.length - 2 * self.inputs.offset.value
            if available <= 0:
                return []
            spacing = available / (count - 1)
            distances = [
                self.inputs.offset.value + spacing * index
                for index in range(count)
            ]
        direction = utils.vector.subtract(
            door_edge.endVertex.geometry.asVector(),
            door_edge.startVertex.geometry.asVector(),
        )
        return utils.vector.compute_points_along_vector(
            door_edge.startVertex.geometry,
            direction,
            distances,
        )

    def _door_hole_groups(
        self,
        carcass_edge: adsk.fusion.BRepEdge,
        door_edge: adsk.fusion.BRepEdge,
        door_face: adsk.fusion.BRepFace,
        positions: list[adsk.core.Vector3D],
    ) -> list[list[_Hole]]:
        normal_into_door_face = utils.brep.normal_into_face(
            door_edge,
            door_face,
        )
        edge_delta = utils.vector.subtract(
            door_edge.startVertex.geometry.asVector(),
            carcass_edge.startVertex.geometry.asVector(),
        )
        distance = -normal_into_door_face.dotProduct(edge_delta)
        predrill_diameter = self.inputs.predrill_diameter.value

        if (
            self.inputs.type.value
            == DoorLatchNativeInputs.Types.EVERLOCK.value
        ):
            pilot_offsets = [
                (-2.6, distance + 2.6),
                (2.6, distance + 2.6),
                (-2.6, distance + 4.2),
                (2.6, distance + 4.2),
            ]
            return [
                self._holes_on_face(
                    door_face,
                    door_edge,
                    positions,
                    pilot_offsets,
                    predrill_diameter,
                ),
                self._holes_on_face(
                    door_face,
                    door_edge,
                    positions,
                    [(0, distance + 3.0)],
                    2.5,
                ),
            ]

        if (
            self.inputs.type.value
            == DoorLatchNativeInputs.Types.PULL_LOCK_44.value
        ):
            through_holes = self._holes_on_face(
                door_face,
                door_edge,
                positions,
                [(0, distance + 3.4)],
                3.81,
            )
            if utils.brep.get_board_thickness(door_face) > 1.0:
                counterbores = self._holes_on_face(
                    door_face,
                    door_edge,
                    positions,
                    [(0, distance + 3.4)],
                    4.8,
                )
                return [through_holes, counterbores]
            return [through_holes]

        raise ValueError("Unsupported latch type.")

    def _carcass_holes(
        self,
        carcass_edge: adsk.fusion.BRepEdge,
        carcass_face: adsk.fusion.BRepFace,
        positions: list[adsk.core.Vector3D],
    ) -> list[_Hole]:
        normal_into_carcass_face = utils.brep.normal_into_face(
            carcass_edge,
            carcass_face,
        )
        gap_vector = utils.vector.subtract(
            carcass_edge.startVertex.geometry.asVector(),
            positions[0],
        )
        gap = normal_into_carcass_face.dotProduct(gap_vector)

        if (
            self.inputs.type.value
            == DoorLatchNativeInputs.Types.EVERLOCK.value
        ):
            offsets = [(-1.4, 2.5 - gap), (1.4, 2.5 - gap)]
        elif (
            self.inputs.type.value
            == DoorLatchNativeInputs.Types.PULL_LOCK_44.value
        ):
            offsets = [(-0.95, 2.9 - gap), (0.95, 2.9 - gap)]
        else:
            raise ValueError("Unsupported latch type.")
        return self._holes_on_face(
            carcass_face,
            carcass_edge,
            positions,
            offsets,
            self.inputs.predrill_diameter.value,
        )

    def _holes_on_face(
        self,
        face: adsk.fusion.BRepFace,
        edge: adsk.fusion.BRepEdge,
        positions: list[adsk.core.Vector3D],
        offsets: list[tuple[float, float]],
        diameter: float,
    ) -> list[_Hole]:
        origin, x_axis, y_axis, _ = utils.brep.coordinate_system_on_face(
            face,
            edge,
        )
        holes: list[_Hole] = []
        for position in positions:
            along_edge = utils.vector.subtract(
                position,
                origin.asVector(),
            ).dotProduct(x_axis)
            for along_offset, inset in offsets:
                center = origin.asVector()
                center.add(
                    utils.vector.scaled_by(
                        x_axis,
                        along_edge + along_offset,
                    )
                )
                center.add(utils.vector.scaled_by(y_axis, inset))
                holes.append(_Hole(center.asPoint(), diameter))
        return holes

    def _holes_fit_face(
        self,
        face: adsk.fusion.BRepFace,
        edge: adsk.fusion.BRepEdge,
        holes: list[_Hole],
    ) -> bool:
        _, x_axis, y_axis, _ = utils.brep.coordinate_system_on_face(
            face,
            edge,
        )
        tolerance = self.app.pointTolerance * 10
        for hole in holes:
            radius = hole.diameter / 2
            probes = [hole.center]
            for axis in (x_axis, y_axis):
                for sign in (-1, 1):
                    probe = hole.center.copy()
                    offset = utils.vector.scaled_by(axis, radius * sign)
                    probe.translateBy(offset)
                    probes.append(probe)
            if not all(
                face.isPointOnFace(probe, tolerance)
                for probe in probes
            ):
                return False
        return True

    def _native_face_edge_and_hole_groups(
        self,
        face: adsk.fusion.BRepFace,
        edge: adsk.fusion.BRepEdge,
        groups: list[list[_Hole]],
    ) -> tuple[
        adsk.fusion.BRepFace,
        adsk.fusion.BRepEdge,
        list[list[_Hole]],
    ]:
        native_face = adsk.fusion.BRepFace.cast(face.nativeObject) or face
        native_edge = adsk.fusion.BRepEdge.cast(edge.nativeObject) or edge
        occurrence = face.assemblyContext
        if not occurrence:
            copied_groups = [
                [_Hole(hole.center.copy(), hole.diameter) for hole in group]
                for group in groups
            ]
            return native_face, native_edge, copied_groups

        inverse = utils.matrix.inverted_matrix(occurrence.transform2)
        native_groups: list[list[_Hole]] = []
        for group in groups:
            native_group: list[_Hole] = []
            for hole in group:
                center = hole.center.copy()
                center.transformBy(inverse)
                native_group.append(_Hole(center, hole.diameter))
            native_groups.append(native_group)
        return native_face, native_edge, native_groups

    def _create_everlock_door_sketch(
        self,
        face: adsk.fusion.BRepFace,
        door_edge: adsk.fusion.BRepEdge,
        carcass_edge: adsk.fusion.BRepEdge,
        door_occurrence: adsk.fusion.Occurrence | None,
        carcass_occurrence: adsk.fusion.Occurrence | None,
        pilot_holes: list[_Hole],
        main_holes: list[_Hole],
    ) -> tuple[
        adsk.fusion.Sketch,
        list[adsk.fusion.SketchCircle],
        list[adsk.fusion.SketchCircle],
    ]:
        if len(pilot_holes) != len(main_holes) * 4:
            raise RuntimeError(
                "Each Everlock main hole requires four door pilot holes."
            )
        face = self._current_face(face)
        door_edge = self._current_edge(door_edge)
        carcass_edge = self._current_edge(carcass_edge)
        sketch = face.body.parentComponent.sketches.addWithoutEdges(face)
        if not sketch:
            raise RuntimeError(
                "Fusion failed to create the Everlock door layout."
            )
        sketch.name = "Door Latch (Native) - Everlock Door Layout"

        projected_door_edge = self._project_line(
            sketch,
            door_edge,
            "Door Edge",
        )
        projected_carcass_edge = self._project_line(
            sketch,
            carcass_edge,
            "Carcass Edge",
            sketch_occurrence=door_occurrence,
            entity_occurrence=carcass_occurrence,
        )

        sketch.isComputeDeferred = True
        main_circles, placement_lines = self._add_door_main_hole_layout(
            sketch,
            face,
            door_edge,
            projected_door_edge,
            projected_carcass_edge,
            main_holes,
            offset_value=3.0,
            offset_expression="30 mm",
            offset_parameter_role="everlockCarcassOffset",
            diameter_expression="25 mm",
            diameter_parameter_role="everlockMainDiameter",
        )
        pilot_circles: list[adsk.fusion.SketchCircle] = []
        first_column_line: adsk.fusion.SketchLine | None = None
        first_lower_row_line: adsk.fusion.SketchLine | None = None
        first_upper_row_line: adsk.fusion.SketchLine | None = None
        first_pilot_circle: adsk.fusion.SketchCircle | None = None

        for station_index, placement_line in enumerate(
            placement_lines,
            start=1,
        ):
            station_pilots = pilot_holes[
                (station_index - 1) * 4:station_index * 4
            ]
            (
                station_circles,
                column_line,
                lower_row_line,
                upper_row_line,
            ) = self._add_everlock_pilot_pattern(
                sketch,
                projected_door_edge,
                placement_line,
                placement_line.endSketchPoint,
                station_pilots,
                first_column_line,
                first_lower_row_line,
                first_upper_row_line,
                first_pilot_circle,
            )
            if not first_column_line:
                first_column_line = column_line
                first_lower_row_line = lower_row_line
                first_upper_row_line = upper_row_line
            if not first_pilot_circle:
                first_pilot_circle = station_circles[0]
            pilot_circles.extend(station_circles)

        sketch.isComputeDeferred = False
        self._require_fully_constrained(sketch)
        return sketch, pilot_circles, main_circles

    def _create_pull_lock_door_sketch(
        self,
        face: adsk.fusion.BRepFace,
        door_edge: adsk.fusion.BRepEdge,
        carcass_edge: adsk.fusion.BRepEdge,
        door_occurrence: adsk.fusion.Occurrence | None,
        carcass_occurrence: adsk.fusion.Occurrence | None,
        main_holes: list[_Hole],
    ) -> tuple[
        adsk.fusion.Sketch,
        list[adsk.fusion.SketchCircle],
    ]:
        face = self._current_face(face)
        door_edge = self._current_edge(door_edge)
        carcass_edge = self._current_edge(carcass_edge)
        sketch = face.body.parentComponent.sketches.addWithoutEdges(face)
        if not sketch:
            raise RuntimeError(
                "Fusion failed to create the Pull Lock layout."
            )
        sketch.name = "Door Latch (Native) - Pull Lock Layout"
        projected_door_edge = self._project_line(
            sketch,
            door_edge,
            "Door Edge",
        )
        projected_carcass_edge = self._project_line(
            sketch,
            carcass_edge,
            "Carcass Edge",
            sketch_occurrence=door_occurrence,
            entity_occurrence=carcass_occurrence,
        )

        sketch.isComputeDeferred = True
        circles, _ = self._add_door_main_hole_layout(
            sketch,
            face,
            door_edge,
            projected_door_edge,
            projected_carcass_edge,
            main_holes,
            offset_value=3.4,
            offset_expression="34 mm",
            offset_parameter_role="pullLockCarcassOffset",
            diameter_expression="38.1 mm",
            diameter_parameter_role="pullLockDiameter",
        )
        sketch.isComputeDeferred = False
        self._require_fully_constrained(sketch)
        return sketch, circles

    def _add_door_main_hole_layout(
        self,
        sketch: adsk.fusion.Sketch,
        face: adsk.fusion.BRepFace,
        door_edge: adsk.fusion.BRepEdge,
        projected_door_edge: adsk.fusion.SketchLine,
        projected_carcass_edge: adsk.fusion.SketchLine,
        main_holes: list[_Hole],
        offset_value: float,
        offset_expression: str,
        offset_parameter_role: str,
        diameter_expression: str,
        diameter_parameter_role: str,
    ) -> tuple[
        list[adsk.fusion.SketchCircle],
        list[adsk.fusion.SketchLine],
    ]:
        station_points = self._door_station_points(
            sketch,
            face,
            door_edge,
            projected_door_edge,
            main_holes,
        )
        first_alignment_line: adsk.fusion.SketchLine | None = None
        first_placement_line: adsk.fusion.SketchLine | None = None
        first_circle: adsk.fusion.SketchCircle | None = None
        placement_lines: list[adsk.fusion.SketchLine] = []
        circles: list[adsk.fusion.SketchCircle] = []

        for station_point, main_hole in zip(station_points, main_holes):
            main_center = sketch.modelToSketchSpace(main_hole.center)
            main_center.z = 0
            carcass_foot_in_sketch = self._project_point_onto_sketch_line(
                main_center,
                projected_carcass_edge,
            )
            if (
                station_point.geometry.distanceTo(carcass_foot_in_sketch)
                <= self.app.pointTolerance * 10
            ):
                carcass_reference_point = station_point
            else:
                carcass_reference_point = sketch.sketchPoints.add(
                    carcass_foot_in_sketch
                )
                if not carcass_reference_point:
                    raise RuntimeError(
                        "Fusion failed to create the carcass-edge anchor."
                    )
                if not sketch.geometricConstraints.addCoincident(
                    carcass_reference_point,
                    projected_carcass_edge,
                ):
                    raise RuntimeError(
                        "Fusion failed to anchor the door layout to the "
                        "projected carcass edge."
                    )
                alignment_line = (
                    sketch.sketchCurves.sketchLines.addByTwoPoints(
                        station_point,
                        carcass_reference_point,
                    )
                )
                if not alignment_line:
                    raise RuntimeError(
                        "Fusion failed to align the door and carcass anchors."
                    )
                alignment_line.isConstruction = True
                if first_alignment_line:
                    if not sketch.geometricConstraints.addParallel(
                        first_alignment_line,
                        alignment_line,
                    ):
                        raise RuntimeError(
                            "Fusion failed to align the latch stations."
                        )
                else:
                    if not sketch.geometricConstraints.addPerpendicular(
                        projected_door_edge,
                        alignment_line,
                    ):
                        raise RuntimeError(
                            "Fusion failed to align the carcass anchor with "
                            "the selected Door Edge."
                        )
                    first_alignment_line = alignment_line

            placement_line = sketch.sketchCurves.sketchLines.addByTwoPoints(
                carcass_reference_point,
                main_center,
            )
            if not placement_line:
                raise RuntimeError(
                    "Fusion failed to create the latch placement anchor."
                )
            placement_line.isConstruction = True
            if first_placement_line:
                if not sketch.geometricConstraints.addParallel(
                    first_placement_line,
                    placement_line,
                ):
                    raise RuntimeError(
                        "Fusion failed to align the latch carcass offsets."
                    )
                if not sketch.geometricConstraints.addEqual(
                    first_placement_line,
                    placement_line,
                ):
                    raise RuntimeError(
                        "Fusion failed to equalize the latch carcass offsets."
                    )
            else:
                if not sketch.geometricConstraints.addPerpendicular(
                    projected_carcass_edge,
                    placement_line,
                ):
                    raise RuntimeError(
                        "Fusion failed to orient the latch placement anchor."
                    )
                placement_dimension = self._add_length_dimension(
                    sketch,
                    placement_line,
                    offset_value,
                )
                placement_dimension.parameter.expression = offset_expression
                self._name_parameter(
                    placement_dimension.parameter,
                    offset_parameter_role,
                )
                first_placement_line = placement_line
            placement_lines.append(placement_line)

            circle = sketch.sketchCurves.sketchCircles.addByCenterRadius(
                placement_line.endSketchPoint,
                main_hole.diameter / 2,
            )
            if not circle:
                raise RuntimeError(
                    "Fusion failed to create a latch main hole."
                )
            if first_circle:
                if not sketch.geometricConstraints.addEqual(
                    first_circle,
                    circle,
                ):
                    raise RuntimeError(
                        "Fusion failed to equalize the latch main holes."
                    )
            else:
                self._dimension_circle(
                    sketch,
                    circle,
                    diameter_expression,
                    diameter_parameter_role,
                )
                first_circle = circle
            circles.append(circle)
        return circles, placement_lines

    def _door_station_points(
        self,
        sketch: adsk.fusion.Sketch,
        face: adsk.fusion.BRepFace,
        door_edge: adsk.fusion.BRepEdge,
        projected_door_edge: adsk.fusion.SketchLine,
        main_holes: list[_Hole],
    ) -> list[adsk.fusion.SketchPoint]:
        door_origin, door_axis, _, _ = (
            utils.brep.coordinate_system_on_face(face, door_edge)
        )
        door_reference_point = self._line_endpoint_near(
            sketch,
            projected_door_edge,
            door_origin,
        )
        door_end_point = (
            projected_door_edge.endSketchPoint
            if door_reference_point
            == projected_door_edge.startSketchPoint
            else projected_door_edge.startSketchPoint
        )
        station_points: list[adsk.fusion.SketchPoint] = []
        for main_hole in main_holes:
            center_delta = utils.vector.subtract(
                main_hole.center.asVector(),
                door_origin.asVector(),
            )
            along_distance = center_delta.dotProduct(door_axis)
            station_model = door_origin.copy()
            station_model.translateBy(
                utils.vector.scaled_by(door_axis, along_distance)
            )
            station_in_sketch = sketch.modelToSketchSpace(station_model)
            station_in_sketch.z = 0
            station_point = sketch.sketchPoints.add(station_in_sketch)
            if not station_point:
                raise RuntimeError(
                    "Fusion failed to create a latch station."
                )
            station_points.append(station_point)

        if len(station_points) == 1:
            if not sketch.geometricConstraints.addMidPoint(
                station_points[0],
                projected_door_edge,
            ):
                raise RuntimeError(
                    "Fusion failed to center the latch on the Door Edge."
                )
            return station_points

        for station_point in station_points:
            if not sketch.geometricConstraints.addCoincident(
                station_point,
                projected_door_edge,
            ):
                raise RuntimeError(
                    "Fusion failed to place a latch station on the Door Edge."
                )

        station_segments: list[adsk.fusion.SketchLine] = []
        segment_points = [
            door_reference_point,
            *station_points,
            door_end_point,
        ]
        for start_point, end_point in zip(
            segment_points,
            segment_points[1:],
        ):
            segment = sketch.sketchCurves.sketchLines.addByTwoPoints(
                start_point,
                end_point,
            )
            if not segment:
                raise RuntimeError(
                    "Fusion failed to create latch station spacing."
                )
            segment.isConstruction = True
            station_segments.append(segment)

        leading_segment = station_segments[0]
        trailing_segment = station_segments[-1]
        end_offset_dimension = self._add_length_dimension(
            sketch,
            leading_segment,
            self.inputs.offset.value,
        )
        end_offset_dimension.parameter.expression = (
            self.inputs.offset.expression
        )
        self._name_parameter(
            end_offset_dimension.parameter,
            "latchEndOffset",
        )
        if not sketch.geometricConstraints.addEqual(
            leading_segment,
            trailing_segment,
        ):
            raise RuntimeError(
                "Fusion failed to equalize the latch end offsets."
            )

        spacing_segments = station_segments[1:-1]
        if spacing_segments:
            first_spacing = spacing_segments[0]
            for spacing_segment in spacing_segments[1:]:
                if not sketch.geometricConstraints.addEqual(
                    first_spacing,
                    spacing_segment,
                ):
                    raise RuntimeError(
                        "Fusion failed to equalize the latch spacing."
                    )
        return station_points

    def _create_projected_circle_sketch(
        self,
        face: adsk.fusion.BRepFace,
        occurrence: adsk.fusion.Occurrence | None,
        source_points: list[adsk.fusion.SketchPoint],
        diameter_expression: str,
        name: str,
        parameter_role: str,
    ) -> adsk.fusion.Sketch:
        face = self._current_face(face)
        sketch = face.body.parentComponent.sketches.addWithoutEdges(face)
        if not sketch:
            raise RuntimeError(f"Fusion failed to create '{name}'.")
        sketch.name = name
        projected_points: list[adsk.fusion.SketchPoint] = []
        for source_point in source_points:
            projected = self._project_entities(
                sketch,
                [source_point],
                sketch_occurrence=occurrence,
                entity_occurrence=occurrence,
            )
            projected_point = next(
                (
                    adsk.fusion.SketchPoint.cast(
                        candidate.nativeObject or candidate
                    )
                    for entity in projected
                    if (
                        candidate
                        := adsk.fusion.SketchPoint.cast(entity)
                    )
                ),
                None,
            )
            if not projected_point:
                raise RuntimeError(
                    f"Fusion failed to project a hole center into '{name}'."
                )
            projected_points.append(projected_point)

        sketch.isComputeDeferred = True
        first_circle: adsk.fusion.SketchCircle | None = None
        for projected_point in projected_points:
            circle = sketch.sketchCurves.sketchCircles.addByCenterRadius(
                projected_point,
                1.0,
            )
            if not circle:
                raise RuntimeError(
                    f"Fusion failed to create a projected circle in '{name}'."
                )
            if first_circle:
                if not sketch.geometricConstraints.addEqual(
                    first_circle,
                    circle,
                ):
                    raise RuntimeError(
                        f"Fusion failed to equalize circles in '{name}'."
                    )
            else:
                self._dimension_circle(
                    sketch,
                    circle,
                    diameter_expression,
                    parameter_role,
                )
                first_circle = circle
        sketch.isComputeDeferred = False
        self._require_fully_constrained(sketch)
        return sketch

    def _add_everlock_pilot_pattern(
        self,
        sketch: adsk.fusion.Sketch,
        projected_door_edge: adsk.fusion.SketchLine,
        placement_line: adsk.fusion.SketchLine,
        main_center: adsk.fusion.SketchPoint,
        pilot_holes: list[_Hole],
        first_column_line: adsk.fusion.SketchLine | None,
        first_lower_row_line: adsk.fusion.SketchLine | None,
        first_upper_row_line: adsk.fusion.SketchLine | None,
        first_pilot_circle: adsk.fusion.SketchCircle | None,
    ) -> tuple[
        list[adsk.fusion.SketchCircle],
        adsk.fusion.SketchLine,
        adsk.fusion.SketchLine,
        adsk.fusion.SketchLine,
    ]:
        if len(pilot_holes) != 4:
            raise RuntimeError(
                "An Everlock station must contain four pilot holes."
            )
        pilot_centers = [
            sketch.modelToSketchSpace(hole.center)
            for hole in pilot_holes
        ]
        for center in pilot_centers:
            center.z = 0

        lower_left, lower_right, upper_left, upper_right = pilot_centers
        main_geometry = main_center.geometry
        door_axis = projected_door_edge.startSketchPoint.geometry.vectorTo(
            projected_door_edge.endSketchPoint.geometry
        )
        if not door_axis.normalize():
            raise RuntimeError("The projected Door Edge has zero length.")
        left_distance = main_geometry.vectorTo(lower_left).dotProduct(
            door_axis
        )
        right_distance = main_geometry.vectorTo(lower_right).dotProduct(
            door_axis
        )
        left_column_point = main_geometry.copy()
        left_column_point.translateBy(
            utils.vector.scaled_by(door_axis, left_distance)
        )
        right_column_point = main_geometry.copy()
        right_column_point.translateBy(
            utils.vector.scaled_by(door_axis, right_distance)
        )

        left_column_line = sketch.sketchCurves.sketchLines.addByTwoPoints(
            main_center,
            left_column_point,
        )
        right_column_line = sketch.sketchCurves.sketchLines.addByTwoPoints(
            main_center,
            right_column_point,
        )
        if not left_column_line or not right_column_line:
            raise RuntimeError(
                "Fusion failed to create the Everlock column references."
            )
        left_column_line.isConstruction = True
        right_column_line.isConstruction = True
        if not sketch.geometricConstraints.addPerpendicular(
            placement_line,
            left_column_line,
        ):
            raise RuntimeError(
                "Fusion failed to align the Everlock pilot columns."
            )
        if not sketch.geometricConstraints.addCollinear(
            left_column_line,
            right_column_line,
        ):
            raise RuntimeError(
                "Fusion failed to align the Everlock pilot columns."
            )
        if not sketch.geometricConstraints.addEqual(
            left_column_line,
            right_column_line,
        ):
            raise RuntimeError(
                "Fusion failed to make the Everlock columns symmetric."
            )
        if first_column_line:
            if not sketch.geometricConstraints.addEqual(
                first_column_line,
                left_column_line,
            ):
                raise RuntimeError(
                    "Fusion failed to equalize the Everlock column spacing."
                )
        else:
            column_dimension = self._add_length_dimension(
                sketch,
                left_column_line,
                2.6,
            )
            column_dimension.parameter.expression = "26 mm"
            self._name_parameter(
                column_dimension.parameter,
                "everlockPilotColumnOffset",
            )

        lower_left_line = sketch.sketchCurves.sketchLines.addByTwoPoints(
            left_column_line.endSketchPoint,
            lower_left,
        )
        lower_right_line = sketch.sketchCurves.sketchLines.addByTwoPoints(
            right_column_line.endSketchPoint,
            lower_right,
        )
        upper_left_line = sketch.sketchCurves.sketchLines.addByTwoPoints(
            left_column_line.endSketchPoint,
            upper_left,
        )
        upper_right_line = sketch.sketchCurves.sketchLines.addByTwoPoints(
            right_column_line.endSketchPoint,
            upper_right,
        )
        row_lines = (
            lower_left_line,
            lower_right_line,
            upper_left_line,
            upper_right_line,
        )
        if any(not line for line in row_lines):
            raise RuntimeError(
                "Fusion failed to create the Everlock row references."
            )
        for line in row_lines:
            line.isConstruction = True
        if not sketch.geometricConstraints.addParallel(
            placement_line,
            lower_left_line,
        ):
            raise RuntimeError(
                "Fusion failed to orient the lower Everlock pilot row."
            )
        if not sketch.geometricConstraints.addParallel(
            lower_left_line,
            lower_right_line,
        ):
            raise RuntimeError(
                "Fusion failed to align the lower Everlock pilot row."
            )
        if not sketch.geometricConstraints.addParallel(
            lower_left_line,
            upper_left_line,
        ):
            raise RuntimeError(
                "Fusion failed to orient the upper Everlock pilot row."
            )
        if not sketch.geometricConstraints.addParallel(
            upper_left_line,
            upper_right_line,
        ):
            raise RuntimeError(
                "Fusion failed to align the upper Everlock pilot row."
            )
        if not sketch.geometricConstraints.addEqual(
            lower_left_line,
            lower_right_line,
        ):
            raise RuntimeError(
                "Fusion failed to equalize the lower Everlock row."
            )
        if not sketch.geometricConstraints.addEqual(
            upper_left_line,
            upper_right_line,
        ):
            raise RuntimeError(
                "Fusion failed to equalize the upper Everlock row."
            )

        if first_lower_row_line:
            if not sketch.geometricConstraints.addEqual(
                first_lower_row_line,
                lower_left_line,
            ):
                raise RuntimeError(
                    "Fusion failed to equalize the lower row offsets."
                )
        else:
            lower_dimension = self._add_length_dimension(
                sketch,
                lower_left_line,
                0.4,
            )
            lower_dimension.parameter.expression = "4 mm"
            self._name_parameter(
                lower_dimension.parameter,
                "everlockLowerPilotRowOffset",
            )
        if first_upper_row_line:
            if not sketch.geometricConstraints.addEqual(
                first_upper_row_line,
                upper_left_line,
            ):
                raise RuntimeError(
                    "Fusion failed to equalize the upper row offsets."
                )
        else:
            upper_dimension = self._add_length_dimension(
                sketch,
                upper_left_line,
                1.2,
            )
            upper_dimension.parameter.expression = "12 mm"
            self._name_parameter(
                upper_dimension.parameter,
                "everlockUpperPilotRowOffset",
            )

        circles: list[adsk.fusion.SketchCircle] = []
        for center_line, hole in zip(row_lines, pilot_holes):
            circle = sketch.sketchCurves.sketchCircles.addByCenterRadius(
                center_line.endSketchPoint,
                hole.diameter / 2,
            )
            if not circle:
                raise RuntimeError(
                    "Fusion failed to create an Everlock pilot circle."
                )
            if first_pilot_circle:
                if not sketch.geometricConstraints.addEqual(
                    first_pilot_circle,
                    circle,
                ):
                    raise RuntimeError(
                        "Fusion failed to equalize the Everlock pilot holes."
                    )
            elif circles:
                if not sketch.geometricConstraints.addEqual(
                    circles[0],
                    circle,
                ):
                    raise RuntimeError(
                        "Fusion failed to equalize the Everlock pilot holes."
                    )
            else:
                self._dimension_circle(
                    sketch,
                    circle,
                    self.inputs.predrill_diameter.expression,
                    "everlockPilotDiameter",
                )
            circles.append(circle)
        return (
            circles,
            left_column_line,
            lower_left_line,
            upper_left_line,
        )

    def _create_carcass_sketch_from_door(
        self,
        face: adsk.fusion.BRepFace,
        door_edge: adsk.fusion.BRepEdge,
        carcass_occurrence: adsk.fusion.Occurrence | None,
        door_occurrence: adsk.fusion.Occurrence | None,
        door_main_points: list[adsk.fusion.SketchPoint],
        holes: list[_Hole],
    ) -> adsk.fusion.Sketch:
        if len(holes) != len(door_main_points) * 2:
            raise RuntimeError(
                "Each latch station requires two carcass pilot holes."
            )
        face = self._current_face(face)
        door_edge = self._current_edge(door_edge)
        sketch = face.body.parentComponent.sketches.addWithoutEdges(face)
        if not sketch:
            raise RuntimeError(
                "Fusion failed to create the carcass pilot layout."
            )
        sketch.name = "Door Latch (Native) - Carcass Pilot Layout"
        projected_door_edge = self._project_line(
            sketch,
            door_edge,
            "Door Edge",
            sketch_occurrence=carcass_occurrence,
            entity_occurrence=door_occurrence,
        )

        projected_main_points: list[adsk.fusion.SketchPoint] = []
        for point in door_main_points:
            projected = self._project_entities(
                sketch,
                [point],
                sketch_occurrence=carcass_occurrence,
                entity_occurrence=door_occurrence,
            )
            projected_point = next(
                (
                    adsk.fusion.SketchPoint.cast(
                        candidate.nativeObject or candidate
                    )
                    for entity in projected
                    if (
                        candidate
                        := adsk.fusion.SketchPoint.cast(entity)
                    )
                ),
                None,
            )
            if not projected_point:
                raise RuntimeError(
                    "Fusion failed to project a door latch center into the "
                    "carcass sketch."
                )
            projected_main_points.append(projected_point)

        sketch.isComputeDeferred = True
        first_inset_line: adsk.fusion.SketchLine | None = None
        first_pair_line: adsk.fusion.SketchLine | None = None
        first_circle: adsk.fusion.SketchCircle | None = None
        for station_index, projected_main_point in enumerate(
            projected_main_points,
            start=1,
        ):
            station_holes = holes[
                (station_index - 1) * 2:station_index * 2
            ]
            left_hole, right_hole = station_holes
            pair_center_model = utils.vector.center(
                [left_hole.center, right_hole.center]
            )
            pair_center = sketch.modelToSketchSpace(pair_center_model)
            pair_center.z = 0
            inset_line = sketch.sketchCurves.sketchLines.addByTwoPoints(
                projected_main_point,
                pair_center,
            )
            if not inset_line:
                raise RuntimeError(
                    "Fusion failed to create the carcass inset reference."
                )
            inset_line.isConstruction = True
            if first_inset_line:
                if not sketch.geometricConstraints.addParallel(
                    first_inset_line,
                    inset_line,
                ):
                    raise RuntimeError(
                        "Fusion failed to align the carcass insets."
                    )
                if not sketch.geometricConstraints.addEqual(
                    first_inset_line,
                    inset_line,
                ):
                    raise RuntimeError(
                        "Fusion failed to equalize the carcass insets."
                    )
            else:
                if not sketch.geometricConstraints.addPerpendicular(
                    projected_door_edge,
                    inset_line,
                ):
                    raise RuntimeError(
                        "Fusion failed to orient the carcass inset from the "
                        "projected Door Edge."
                    )
                inset_value = (
                    2.5
                    if self.inputs.type.value
                    == DoorLatchNativeInputs.Types.EVERLOCK.value
                    else 2.9
                )
                inset_dimension = self._add_length_dimension(
                    sketch,
                    inset_line,
                    inset_value,
                )
                inset_dimension.parameter.expression = (
                    "25 mm"
                    if self.inputs.type.value
                    == DoorLatchNativeInputs.Types.EVERLOCK.value
                    else "29 mm"
                )
                self._name_parameter(
                    inset_dimension.parameter,
                    "carcassPilotInsetFromDoorEdge",
                )
                first_inset_line = inset_line

            left_center = sketch.modelToSketchSpace(left_hole.center)
            right_center = sketch.modelToSketchSpace(right_hole.center)
            left_center.z = 0
            right_center.z = 0
            left_line = sketch.sketchCurves.sketchLines.addByTwoPoints(
                inset_line.endSketchPoint,
                left_center,
            )
            right_line = sketch.sketchCurves.sketchLines.addByTwoPoints(
                inset_line.endSketchPoint,
                right_center,
            )
            if not left_line or not right_line:
                raise RuntimeError(
                    "Fusion failed to create the carcass pair references."
            )
            left_line.isConstruction = True
            right_line.isConstruction = True
            if not sketch.geometricConstraints.addPerpendicular(
                inset_line,
                left_line,
            ):
                raise RuntimeError(
                    "Fusion failed to align the carcass pilot pair with "
                    "the projected Door Edge."
                )
            if not sketch.geometricConstraints.addCollinear(
                left_line,
                right_line,
            ):
                raise RuntimeError(
                    "Fusion failed to align the carcass pilot pair."
                )
            if not sketch.geometricConstraints.addEqual(
                left_line,
                right_line,
            ):
                raise RuntimeError(
                    "Fusion failed to make the carcass pilot pair symmetric."
                )
            if first_pair_line:
                if not sketch.geometricConstraints.addEqual(
                    first_pair_line,
                    left_line,
                ):
                    raise RuntimeError(
                        "Fusion failed to equalize the carcass pilot spacing."
                    )
            else:
                pair_offset = (
                    1.4
                    if self.inputs.type.value
                    == DoorLatchNativeInputs.Types.EVERLOCK.value
                    else 0.95
                )
                pair_dimension = self._add_length_dimension(
                    sketch,
                    left_line,
                    pair_offset,
                )
                pair_dimension.parameter.expression = (
                    "14 mm"
                    if self.inputs.type.value
                    == DoorLatchNativeInputs.Types.EVERLOCK.value
                    else "9.5 mm"
                )
                self._name_parameter(
                    pair_dimension.parameter,
                    "carcassPilotPairOffset",
                )
                first_pair_line = left_line

            for line in (left_line, right_line):
                circle = sketch.sketchCurves.sketchCircles.addByCenterRadius(
                    line.endSketchPoint,
                    left_hole.diameter / 2,
                )
                if not circle:
                    raise RuntimeError(
                        "Fusion failed to create a carcass pilot circle."
                    )
                if first_circle:
                    if not sketch.geometricConstraints.addEqual(
                        first_circle,
                        circle,
                    ):
                        raise RuntimeError(
                            "Fusion failed to equalize the carcass pilots."
                        )
                else:
                    self._dimension_circle(
                        sketch,
                        circle,
                        self.inputs.predrill_diameter.expression,
                        "carcassPilotDiameter",
                    )
                    first_circle = circle

        sketch.isComputeDeferred = False
        self._require_fully_constrained(sketch)
        return sketch

    def _project_line(
        self,
        sketch: adsk.fusion.Sketch,
        edge: adsk.fusion.BRepEdge,
        label: str,
        sketch_occurrence: adsk.fusion.Occurrence | None = None,
        entity_occurrence: adsk.fusion.Occurrence | None = None,
    ) -> adsk.fusion.SketchLine:
        projected = self._project_entities(
            sketch,
            [edge],
            sketch_occurrence=sketch_occurrence,
            entity_occurrence=entity_occurrence,
        )
        line = next(
            (
                adsk.fusion.SketchLine.cast(
                    candidate.nativeObject or candidate
                )
                for entity in projected
                if (candidate := adsk.fusion.SketchLine.cast(entity))
            ),
            None,
        )
        if not line:
            raise RuntimeError(
                f"Fusion failed to project the {label} into '{sketch.name}'."
            )
        line.isConstruction = True
        return line

    def _project_entities(
        self,
        sketch: adsk.fusion.Sketch,
        entities: list[adsk.core.Base],
        sketch_occurrence: adsk.fusion.Occurrence | None = None,
        entity_occurrence: adsk.fusion.Occurrence | None = None,
    ) -> list[adsk.fusion.SketchEntity]:
        projection_sketch = (
            sketch.createForAssemblyContext(sketch_occurrence)
            if sketch_occurrence
            else sketch
        )
        if not projection_sketch:
            raise RuntimeError(
                f"Fusion failed to create an assembly-context proxy for "
                f"'{sketch.name}'."
            )
        projection_entities: list[adsk.core.Base] = []
        for entity in entities:
            projection_entity = (
                entity.createForAssemblyContext(entity_occurrence)
                if entity_occurrence
                else entity
            )
            if not projection_entity:
                raise RuntimeError(
                    "Fusion failed to create an assembly-context projection "
                    "reference."
                )
            projection_entities.append(projection_entity)
        return projection_sketch.project2(
            projection_entities,
            True,
        )

    def _line_endpoint_near(
        self,
        sketch: adsk.fusion.Sketch,
        line: adsk.fusion.SketchLine,
        model_point: adsk.core.Point3D,
    ) -> adsk.fusion.SketchPoint:
        point = sketch.modelToSketchSpace(model_point)
        return min(
            (line.startSketchPoint, line.endSketchPoint),
            key=lambda endpoint: endpoint.geometry.distanceTo(point),
        )

    def _project_point_onto_sketch_line(
        self,
        point: adsk.core.Point3D,
        line: adsk.fusion.SketchLine,
    ) -> adsk.core.Point3D:
        start = line.startSketchPoint.geometry
        direction = start.vectorTo(line.endSketchPoint.geometry)
        if not direction.normalize():
            raise RuntimeError("A projected reference edge has zero length.")
        distance = start.vectorTo(point).dotProduct(direction)
        result = start.copy()
        result.translateBy(
            utils.vector.scaled_by(direction, distance)
        )
        return result

    def _dimension_circle(
        self,
        sketch: adsk.fusion.Sketch,
        circle: adsk.fusion.SketchCircle,
        expression: str,
        parameter_role: str,
    ) -> None:
        text_point = circle.centerSketchPoint.geometry.copy()
        text_point.x += max(circle.radius * 2, 0.5)
        text_point.y += max(circle.radius * 2, 0.5)
        dimension = sketch.sketchDimensions.addDiameterDimension(
            circle,
            text_point,
        )
        if not dimension or not dimension.parameter:
            raise RuntimeError(
                "Fusion failed to dimension a latch-hole circle."
            )
        dimension.parameter.expression = expression
        self._name_parameter(dimension.parameter, parameter_role)

    def _profiles_for_circles(
        self,
        sketch: adsk.fusion.Sketch,
        circles: list[adsk.fusion.SketchCircle],
    ) -> adsk.core.ObjectCollection:
        selected: list[adsk.fusion.Profile] = []
        for circle in circles:
            matches = [
                profile
                for profile in sketch.profiles
                if any(
                    profile_curve.sketchEntity == circle
                    for loop in profile.profileLoops
                    for profile_curve in loop.profileCurves
                )
            ]
            if len(matches) != 1:
                raise RuntimeError(
                    f"Fusion could not identify the profile for a circle in "
                    f"'{sketch.name}'."
                )
            if all(matches[0] != profile for profile in selected):
                selected.append(matches[0])
        profiles = adsk.core.ObjectCollection.createWithArray(
            cast(list[adsk.core.Base], selected)
        )
        if profiles.count != len(circles):
            raise RuntimeError(
                f"'{sketch.name}' did not produce one profile per hole."
            )
        return profiles

    def _add_length_dimension(
        self,
        sketch: adsk.fusion.Sketch,
        line: adsk.fusion.SketchLine,
        value: float,
    ) -> adsk.fusion.SketchLinearDimension:
        midpoint = line.startSketchPoint.geometry.copy()
        midpoint.x = (
            line.startSketchPoint.geometry.x
            + line.endSketchPoint.geometry.x
        ) / 2
        midpoint.y = (
            line.startSketchPoint.geometry.y
            + line.endSketchPoint.geometry.y
        ) / 2
        dimension = sketch.sketchDimensions.addDistanceDimension(
            line.startSketchPoint,
            line.endSketchPoint,
            adsk.fusion.DimensionOrientations.AlignedDimensionOrientation,  # type: ignore
            midpoint,
        )
        if not dimension or not dimension.parameter:
            raise RuntimeError("Fusion failed to create a sketch distance.")
        dimension.parameter.value = value
        return dimension

    def _create_distance_cut(
        self,
        face: adsk.fusion.BRepFace,
        sketch: adsk.fusion.Sketch,
        depth_value: float,
        depth_expression: str | None,
        name: str,
        parameter_role: str,
        profiles: adsk.core.ObjectCollection | None = None,
    ) -> adsk.fusion.ExtrudeFeature:
        if depth_value <= 0:
            raise RuntimeError(f"'{name}' requires a positive depth.")
        face = self._current_face(face)
        profile_input = (
            profiles
            if profiles is not None
            else self._all_profiles(sketch)
        )
        component = face.body.parentComponent
        extrude_input = component.features.extrudeFeatures.createInput(
            profile_input,
            adsk.fusion.FeatureOperations.CutFeatureOperation,  # type: ignore
        )
        if not extrude_input:
            raise RuntimeError(f"Fusion failed to initialize '{name}'.")
        value_input = (
            adsk.core.ValueInput.createByString(depth_expression)
            if depth_expression
            else adsk.core.ValueInput.createByReal(depth_value)
        )
        extent = adsk.fusion.DistanceExtentDefinition.create(value_input)
        if not extent:
            raise RuntimeError(f"Fusion failed to define the depth of '{name}'.")
        self._set_cut_extent(face, sketch, extrude_input, extent, name)
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

    def _create_through_cut(
        self,
        face: adsk.fusion.BRepFace,
        sketch: adsk.fusion.Sketch,
        name: str,
        parameter_role: str,
        profiles: adsk.core.ObjectCollection | None = None,
    ) -> adsk.fusion.ExtrudeFeature:
        face = self._current_face(face)
        profile_input = (
            profiles
            if profiles is not None
            else self._all_profiles(sketch)
        )
        component = face.body.parentComponent
        extrude_input = component.features.extrudeFeatures.createInput(
            profile_input,
            adsk.fusion.FeatureOperations.CutFeatureOperation,  # type: ignore
        )
        if not extrude_input:
            raise RuntimeError(f"Fusion failed to initialize '{name}'.")
        opposite_face = utils.brep.get_opposite_face(face)
        extent = adsk.fusion.ToEntityExtentDefinition.create(
            opposite_face,
            False,
        )
        if not extent:
            raise RuntimeError(
                f"Fusion failed to define the opposite-face extent of '{name}'."
            )
        extent.directionHint = utils.brep.normal_towards_face(
            face,
            opposite_face,
        )
        self._set_cut_extent(face, sketch, extrude_input, extent, name)
        extrude = component.features.extrudeFeatures.add(extrude_input)
        if not extrude:
            raise RuntimeError(f"Fusion failed to create '{name}'.")
        extrude.name = name
        sketch.isVisible = False
        self._name_feature_parameters(extrude, parameter_role)
        return extrude

    def _set_cut_extent(
        self,
        face: adsk.fusion.BRepFace,
        sketch: adsk.fusion.Sketch,
        extrude_input: adsk.fusion.ExtrudeFeatureInput,
        extent: adsk.fusion.ExtentDefinition,
        name: str,
    ) -> None:
        normal_into_body = utils.brep.normal_towards_face(
            face,
            utils.brep.get_opposite_face(face),
        )
        sketch_normal = sketch.xDirection.crossProduct(sketch.yDirection)
        direction = (
            adsk.fusion.ExtentDirections.PositiveExtentDirection
            if sketch_normal.dotProduct(normal_into_body) >= 0
            else adsk.fusion.ExtentDirections.NegativeExtentDirection
        )
        if not extrude_input.setOneSideExtent(extent, direction):
            raise RuntimeError(f"Fusion rejected the cut extent of '{name}'.")
        extrude_input.participantBodies = [self._current_body(face.body)]

    def _current_face(
        self,
        face: adsk.fusion.BRepFace,
    ) -> adsk.fusion.BRepFace:
        entities = face.body.parentComponent.parentDesign.findEntityByToken(
            face.entityToken
        )
        current = next(
            (
                candidate
                for entity in entities
                if (candidate := adsk.fusion.BRepFace.cast(entity))
            ),
            None,
        )
        if not current:
            raise RuntimeError(
                "The selected board face is no longer available in the "
                "current timeline state."
            )
        return current

    def _current_edge(
        self,
        edge: adsk.fusion.BRepEdge,
    ) -> adsk.fusion.BRepEdge:
        entities = edge.body.parentComponent.parentDesign.findEntityByToken(
            edge.entityToken
        )
        current = next(
            (
                candidate
                for entity in entities
                if (candidate := adsk.fusion.BRepEdge.cast(entity))
            ),
            None,
        )
        if not current:
            raise RuntimeError(
                "The selected board edge is no longer available in the "
                "current timeline state."
            )
        return current

    def _current_body(
        self,
        body: adsk.fusion.BRepBody,
    ) -> adsk.fusion.BRepBody:
        entities = body.parentComponent.parentDesign.findEntityByToken(
            body.entityToken
        )
        current = next(
            (
                candidate
                for entity in entities
                if (candidate := adsk.fusion.BRepBody.cast(entity))
            ),
            None,
        )
        if not current:
            raise RuntimeError(
                "The selected board body is no longer available in the "
                "current timeline state."
            )
        return current

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

    def _unique_parameter_prefix(
        self,
        design: adsk.fusion.Design,
    ) -> str:
        parameter_names = {
            parameter.name
            for parameter in design.allParameters
        }
        base = "doorLatchNative"
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
        if sketch.isFullyConstrained:
            return
        unconstrained = [
            curve
            for curve in sketch.sketchCurves
            if not curve.isFullyConstrained
        ]
        details = ", ".join(
            (
                f"{curve.objectType.split('::')[-1]}"
                f"(construction={curve.isConstruction})"
            )
            for curve in unconstrained
        )
        raise RuntimeError(
            f"'{sketch.name}' is under-constrained "
            f"({len(unconstrained)} unconstrained curves: {details})."
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
                "Fusion created the latch features but could not group them."
            )
        group.name = "Door Latch (Native)"
        group.isCollapsed = False
