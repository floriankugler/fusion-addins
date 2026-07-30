import math
import os
from dataclasses import dataclass, replace
from typing import cast

import adsk.core
import adsk.fusion

from lib import addin, inputs, ui_placement, utils
from lib.fusionbootstrap.runtime import RuntimeInfo


_addin: addin.Addin | None = None


@dataclass(frozen=True)
class _Corner:
    vertex: adsk.fusion.BRepVertex
    edge_one: adsk.fusion.BRepEdge
    edge_two: adsk.fusion.BRepEdge
    bisector: adsk.core.Vector3D
    outside_angle: float
    perpendicular_edge: adsk.fusion.BRepEdge | None = None


def run(context, runtime_info: RuntimeInfo):
    global _addin
    _addin = DogBonesNative(runtime_info)


def stop(context):
    global _addin
    if _addin:
        _addin.shutdown()
    _addin = None


class DogBonesNativeInputs(inputs.Inputs):
    def __init__(self, units_manager: adsk.core.UnitsManager):
        units = units_manager.defaultLengthUnits
        self.entities = inputs.SelectionByEntityTokenInput(
            id="entities",
            name="Face or Edges",
            filter=["LinearEdges", "PlanarFaces"],
            lower_bound=1,
            upper_bound=0,
            tool_tip=(
                "Select one planar face, or one or more parallel linear edges "
                "on the same body."
            ),
        )
        self.diameter = inputs.FloatInput(
            id="diameter",
            name="Tool Diameter",
            default_value=0.6,
            tool_tip="Diameter of the tool used to machine the contour.",
            units=units,
        )
        self.diameter.minimum_value = 0.0001
        self.offset = inputs.FloatInput(
            id="offset",
            name="Offset",
            default_value=0.01,
            tool_tip="Additional clearance added to the dog-bone diameter.",
            units=units,
        )
        # A zero offset degenerates the in-face region into two lens
        # profiles that touch only at the corner vertex, so it is excluded.
        self.offset.minimum_value = 0
        self.offset.minimum_inclusive = False
        super().__init__()


class DogBonesNative(addin.Addin):
    inputs: DogBonesNativeInputs
    _parameter_prefix: str
    _first_center_distance_name: str | None = None
    _first_diameter_name: str | None = None

    @property
    def resource_dir(self) -> str:
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), "Resources")

    @property
    def plugin_name(self) -> str:
        return "Dog Bones (Native)"

    @property
    def plugin_desc(self) -> str:
        return "Create dog-bone cutouts with native Fusion features."

    @property
    def plugin_tooltip(self) -> str:
        return (
            "Creates a fully constrained dog-bone sketch and a native cut "
            "extrude without using the custom feature API."
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

    def create_inputs(self) -> DogBonesNativeInputs:
        design = adsk.fusion.Design.cast(self.app.activeProduct)
        if not design:
            raise RuntimeError("Dog Bones (Native) requires an active Fusion design.")
        return DogBonesNativeInputs(design.unitsManager)

    def pre_select(self, input, selection) -> bool:
        if not self.inputs or not input or input.id != self.inputs.entities.id:
            return True

        existing = self.inputs.entities.value
        face = adsk.fusion.BRepFace.cast(selection)
        if face:
            return bool(
                not existing
                and face.body.isSolid
                and utils.brep.is_planar(face)
            )

        edge = adsk.fusion.BRepEdge.cast(selection)
        if not edge or not self._is_eligible_linear_edge(edge):
            return False
        if not existing:
            return edge.body.isSolid
        if any(adsk.fusion.BRepFace.cast(entity) for entity in existing):
            return False

        first = adsk.fusion.BRepEdge.cast(existing[0])
        return bool(
            first
            and self._same_body(first.body, edge.body)
            and utils.brep.is_parallel(first, edge)
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

        entities = self.inputs.entities.value
        selected_face = adsk.fusion.BRepFace.cast(entities[0])
        selected_edges: list[adsk.fusion.BRepEdge] = []
        if selected_face:
            face = cast(
                adsk.fusion.BRepFace,
                selected_face.nativeObject or selected_face,
            )
            corners = self._corners_for_face(face)
        else:
            selected_edges = [
                cast(adsk.fusion.BRepEdge, edge.nativeObject or edge)
                for entity in entities
                if (edge := adsk.fusion.BRepEdge.cast(entity))
            ]
            face, corners = self._face_and_corners_for_edges(selected_edges)

        component = face.body.parentComponent
        sketch, circles = self._create_dogbone_sketch(
            component,
            face,
            selected_edges,
            corners,
        )
        corner_profiles = self._dogbone_profiles(sketch, face, corners, circles)

        # Cut each corner to the face at the far end of its perpendicular
        # edge. Corners of different depths (e.g. pocket vs. through window)
        # get separate extrudes instead of all cutting to the largest
        # parallel face of the body.
        groups: list[
            tuple[adsk.fusion.BRepFace, list[adsk.fusion.Profile]]
        ] = []
        for corner, profile in corner_profiles:
            extent_face = self._extent_face_for_corner(face, corner)
            group = next(
                (item for item in groups if item[0] == extent_face),
                None,
            )
            if group is None:
                groups.append((extent_face, [profile]))
            elif all(profile != existing for existing in group[1]):
                group[1].append(profile)

        last_extrude: adsk.fusion.ExtrudeFeature | None = None
        for group_index, (extent_face, group_profiles) in enumerate(
            groups,
            start=1,
        ):
            last_extrude = self._create_cut_extrude(
                component,
                face,
                extent_face,
                sketch,
                adsk.core.ObjectCollection.createWithArray(
                    cast(list[adsk.core.Base], group_profiles)
                ),
                group_index,
                len(groups),
            )
        if not last_extrude:
            raise RuntimeError("Dog Bones (Native) did not create any cut.")
        self._group_features(component, sketch, last_extrude)

    def _extent_face_for_corner(
        self,
        face: adsk.fusion.BRepFace,
        corner: _Corner,
    ) -> adsk.fusion.BRepFace:
        edge = corner.perpendicular_edge
        plane = adsk.core.Plane.cast(face.geometry)
        if edge and plane:
            far_vertex = (
                edge.endVertex
                if self._same_vertex(edge.startVertex, corner.vertex)
                else edge.startVertex
            )
            candidates = [
                candidate
                for candidate in far_vertex.faces
                if candidate != face
                and (
                    candidate_plane := adsk.core.Plane.cast(
                        candidate.geometry
                    )
                )
                and candidate_plane.normal.isParallelTo(plane.normal)
            ]
            if candidates:
                candidates.sort(key=lambda item: item.area, reverse=True)
                return candidates[0]
        return utils.brep.get_opposite_face(face)

    def _validation_error(self) -> str | None:
        design = adsk.fusion.Design.cast(self.app.activeProduct)
        if not design:
            return "An active Fusion design is required."
        if design.designType != adsk.fusion.DesignTypes.ParametricDesignType:  # type: ignore
            return "Dog Bones (Native) requires Design History."
        if not self.inputs or not self.inputs.entities.value:
            return "Select one planar face, or one or more parallel edges."
        if self.inputs.diameter.value <= 0:
            return "Tool Diameter must be greater than zero."
        if self.inputs.offset.value <= 0:
            return "Offset must be greater than zero."

        entities = self.inputs.entities.value
        faces = [
            face
            for entity in entities
            if (face := adsk.fusion.BRepFace.cast(entity))
        ]
        edges = [
            edge
            for entity in entities
            if (edge := adsk.fusion.BRepEdge.cast(entity))
        ]
        if len(faces) == 1 and not edges:
            selected = faces[0]
            if not selected.body.isSolid or not utils.brep.is_planar(selected):
                return "The selected face must be a planar face on a solid body."
            face = cast(
                adsk.fusion.BRepFace,
                selected.nativeObject or selected,
            )
            if face.body.parentComponent != design.activeComponent:
                return (
                    "Activate the component that owns the selected face, then "
                    "run Dog Bones (Native) again."
                )
            if not self._corners_for_face(face):
                return (
                    "The selected face has no eligible concave corners "
                    "with perpendicular linear body edges."
                )
            try:
                utils.brep.get_opposite_face(face)
            except Exception as exc:
                return f"Could not find a parallel opposite face: {exc}"
            return None

        if faces:
            return "Select either one face or edges; do not mix selection types."
        if not edges:
            return "Select one planar face, or one or more parallel edges."
        if any(not self._is_eligible_linear_edge(edge) for edge in edges):
            return "Every selected edge must be linear and have two adjacent faces."

        native_edges = [
            cast(adsk.fusion.BRepEdge, edge.nativeObject or edge)
            for edge in edges
        ]
        body = native_edges[0].body
        if any(not self._same_body(body, edge.body) for edge in native_edges[1:]):
            return "All selected edges must belong to the same body."
        if body.parentComponent != design.activeComponent:
            return (
                "Activate the component that owns the selected edges, then "
                "run Dog Bones (Native) again."
            )
        if any(
            not utils.brep.is_parallel(native_edges[0], edge)
            for edge in native_edges[1:]
        ):
            return "All selected edges must be parallel."
        try:
            face, corners = self._face_and_corners_for_edges(native_edges)
            if len(corners) != len(native_edges):
                return "Each selected edge must terminate at a concave corner."
            utils.brep.get_opposite_face(face)
        except Exception as exc:
            return str(exc)
        return None

    def _is_eligible_linear_edge(self, edge: adsk.fusion.BRepEdge) -> bool:
        return bool(
            edge.body
            and edge.body.isSolid
            and edge.faces.count == 2
            and utils.brep.is_linear(edge)
        )

    def _same_body(
        self,
        first: adsk.fusion.BRepBody,
        second: adsk.fusion.BRepBody,
    ) -> bool:
        first_native = first.nativeObject or first
        second_native = second.nativeObject or second
        return first_native == second_native

    def _corners_for_face(
        self,
        face: adsk.fusion.BRepFace,
    ) -> list[_Corner]:
        vertices: list[adsk.fusion.BRepVertex] = []
        for loop in face.loops:
            for edge in loop.edges:
                for vertex in (edge.startVertex, edge.endVertex):
                    if not any(
                        self._same_vertex(vertex, item) for item in vertices
                    ):
                        vertices.append(vertex)

        corners: list[_Corner] = []
        for vertex in vertices:
            corner = self._corner_at_vertex(face, vertex)
            if not corner:
                continue
            perpendicular_edges = [
                edge
                for edge in vertex.edges
                if edge != corner.edge_one
                and edge != corner.edge_two
                and self._is_eligible_linear_edge(edge)
                and utils.brep.is_perpendicular(edge, face)
            ]
            if perpendicular_edges:
                corners.append(
                    replace(
                        corner,
                        perpendicular_edge=perpendicular_edges[0],
                    )
                )
        return corners

    def _face_and_corners_for_edges(
        self,
        edges: list[adsk.fusion.BRepEdge],
    ) -> tuple[adsk.fusion.BRepFace, list[_Corner]]:
        if not edges:
            raise ValueError("Select at least one edge.")

        direction = utils.brep.normal_along_edge(edges[0])
        candidates: list[tuple[adsk.fusion.BRepFace, list[_Corner]]] = []
        for face in edges[0].body.faces:
            plane = adsk.core.Plane.cast(face.geometry)
            if not plane or not plane.normal.isParallelTo(direction):
                continue

            corners: list[_Corner] = []
            for edge in edges:
                corner = self._corner_for_selected_edge(face, edge)
                if not corner:
                    break
                corners.append(corner)
            if len(corners) == len(edges):
                candidates.append((face, corners))

        if not candidates:
            raise ValueError(
                "The selected edges do not share a perpendicular face where "
                "each edge ends at a concave corner."
            )
        candidates.sort(key=lambda candidate: candidate[0].area, reverse=True)
        return candidates[0]

    def _corner_for_selected_edge(
        self,
        face: adsk.fusion.BRepFace,
        edge: adsk.fusion.BRepEdge,
    ) -> _Corner | None:
        for endpoint in (edge.startVertex, edge.endVertex):
            face_vertex = next(
                (
                    vertex
                    for loop in face.loops
                    for boundary in loop.edges
                    for vertex in (boundary.startVertex, boundary.endVertex)
                    if self._same_vertex(vertex, endpoint)
                ),
                None,
            )
            if face_vertex:
                corner = self._corner_at_vertex(face, face_vertex)
                if corner:
                    return replace(corner, perpendicular_edge=edge)
        return None

    def _corner_at_vertex(
        self,
        face: adsk.fusion.BRepFace,
        vertex: adsk.fusion.BRepVertex,
    ) -> _Corner | None:
        # Consider every loop: notches sit on the outer loop, while window
        # and pocket corners sit on inner loops. The off-face probe below
        # works identically for both.
        for loop in face.loops:
            incident = [
                edge
                for edge in loop.edges
                if self._edge_has_vertex(edge, vertex)
            ]
            if len(incident) != 2 or any(
                not utils.brep.is_linear(edge)
                for edge in incident
            ):
                continue

            direction_one = self._edge_direction_from_vertex(
                incident[0],
                vertex,
            )
            direction_two = self._edge_direction_from_vertex(
                incident[1],
                vertex,
            )
            dot = max(-1.0, min(1.0, direction_one.dotProduct(direction_two)))
            outside_angle = math.acos(dot)
            if outside_angle <= 1e-6 or outside_angle >= math.pi - 1e-6:
                continue

            bisector = direction_one.copy()
            bisector.add(direction_two)
            if not bisector.normalize():
                continue

            probe_distance = min(
                min(incident[0].length, incident[1].length) * 0.05,
                max(self.app.pointTolerance * 100, 0.01),
            )
            probe = vertex.geometry.copy()
            probe_vector = bisector.copy()
            probe_vector.scaleBy(probe_distance)
            probe.translateBy(probe_vector)
            if face.isPointOnFace(probe, self.app.pointTolerance * 10):
                continue

            return _Corner(
                vertex=vertex,
                edge_one=incident[0],
                edge_two=incident[1],
                bisector=bisector,
                outside_angle=outside_angle,
            )
        return None

    def _same_vertex(
        self,
        first: adsk.fusion.BRepVertex,
        second: adsk.fusion.BRepVertex,
    ) -> bool:
        first_native = first.nativeObject or first
        second_native = second.nativeObject or second
        return (
            first_native == second_native
            or first.geometry.distanceTo(second.geometry)
            <= self.app.pointTolerance * 10
        )

    def _edge_has_vertex(
        self,
        edge: adsk.fusion.BRepEdge,
        vertex: adsk.fusion.BRepVertex,
    ) -> bool:
        return self._same_vertex(edge.startVertex, vertex) or self._same_vertex(
            edge.endVertex,
            vertex,
        )

    def _edge_direction_from_vertex(
        self,
        edge: adsk.fusion.BRepEdge,
        vertex: adsk.fusion.BRepVertex,
    ) -> adsk.core.Vector3D:
        other = (
            edge.endVertex
            if self._same_vertex(edge.startVertex, vertex)
            else edge.startVertex
        )
        direction = vertex.geometry.vectorTo(other.geometry)
        if not direction.normalize():
            raise ValueError("A zero-length boundary edge cannot define a dog bone.")
        return direction

    def _create_dogbone_sketch(
        self,
        component: adsk.fusion.Component,
        face: adsk.fusion.BRepFace,
        selected_edges: list[adsk.fusion.BRepEdge],
        corners: list[_Corner],
    ) -> tuple[adsk.fusion.Sketch, list[adsk.fusion.SketchCircle]]:
        self._parameter_prefix = self._unique_parameter_prefix(
            component.parentDesign
        )
        sketch = component.sketches.addWithoutEdges(face)
        if not sketch:
            raise RuntimeError("Fusion failed to create the dog-bone sketch.")
        sketch.name = "Dog Bones (Native) - Layout"

        projected_lines: dict[int, adsk.fusion.SketchLine] = {}
        for loop in face.loops:
            edges = cast(list[adsk.core.Base], utils.fusion.as_list(loop.edges))
            projected = sketch.project2(edges, True)
            if not projected:
                raise RuntimeError("Fusion failed to project a face loop.")
            for entity in projected:
                line = adsk.fusion.SketchLine.cast(entity)
                referenced = (
                    adsk.fusion.BRepEdge.cast(line.referencedEntity)
                    if line
                    else None
                )
                if line and referenced:
                    native = referenced.nativeObject or referenced
                    projected_lines[native.tempId] = line

        if selected_edges:
            projected_edges = sketch.project2(
                cast(list[adsk.core.Base], selected_edges),
                True,
            )
            if len(projected_edges) < len(selected_edges):
                raise RuntimeError("Fusion failed to project every selected edge.")

        sketch.isComputeDeferred = True
        self._first_center_distance_name = None
        self._first_diameter_name = None
        circles: list[adsk.fusion.SketchCircle] = []
        for corner_index, corner in enumerate(corners, start=1):
            line_one = self._projected_line(
                sketch,
                projected_lines,
                corner.edge_one,
            )
            line_two = self._projected_line(
                sketch,
                projected_lines,
                corner.edge_two,
            )
            circles.append(
                self._add_dogbone_geometry(
                    sketch,
                    corner,
                    line_one,
                    line_two,
                    corner_index,
                )
            )

        sketch.isComputeDeferred = False
        self._require_fully_constrained(sketch)
        return sketch, circles

    def _projected_line(
        self,
        sketch: adsk.fusion.Sketch,
        projected_lines: dict[int, adsk.fusion.SketchLine],
        edge: adsk.fusion.BRepEdge,
    ) -> adsk.fusion.SketchLine:
        native = edge.nativeObject or edge
        result = projected_lines.get(native.tempId)
        if result:
            return result

        start = sketch.modelToSketchSpace(edge.startVertex.geometry)
        end = sketch.modelToSketchSpace(edge.endVertex.geometry)
        for curve in sketch.sketchCurves:
            line = adsk.fusion.SketchLine.cast(curve)
            if not line:
                continue
            first = line.startSketchPoint.geometry
            second = line.endSketchPoint.geometry
            same_direction = (
                first.distanceTo(start) <= self.app.pointTolerance * 10
                and second.distanceTo(end) <= self.app.pointTolerance * 10
            )
            opposite_direction = (
                first.distanceTo(end) <= self.app.pointTolerance * 10
                and second.distanceTo(start) <= self.app.pointTolerance * 10
            )
            if same_direction or opposite_direction:
                return line
        raise RuntimeError("Could not match a projected boundary edge.")

    def _center_distance_for_corner(self, corner: _Corner) -> float:
        # For non-perpendicular corners the tool cannot reach the corner
        # along the bisector unless the center moves out by 1/sin(angle)
        # (same compensation as the old custom-feature version).
        radius = self.inputs.diameter.value / 2
        return max(radius, radius / math.sin(corner.outside_angle))

    def _add_dogbone_geometry(
        self,
        sketch: adsk.fusion.Sketch,
        corner: _Corner,
        line_one: adsk.fusion.SketchLine,
        line_two: adsk.fusion.SketchLine,
        corner_index: int,
    ) -> adsk.fusion.SketchCircle:
        vertex_point = sketch.modelToSketchSpace(corner.vertex.geometry)
        center_distance = self._center_distance_for_corner(corner)
        center_model = corner.vertex.geometry.copy()
        center_offset = corner.bisector.copy()
        center_offset.scaleBy(center_distance)
        center_model.translateBy(center_offset)
        center_point = sketch.modelToSketchSpace(center_model)

        meeting_point = self._line_endpoint_at(line_one, vertex_point)
        center_line = sketch.sketchCurves.sketchLines.addByTwoPoints(
            meeting_point,
            center_point,
        )
        if not center_line:
            raise RuntimeError("Fusion failed to create a dog-bone bisector.")
        center_line.isConstruction = True

        circle = sketch.sketchCurves.sketchCircles.addByCenterRadius(
            center_line.endSketchPoint,
            center_distance + self.inputs.offset.value / 2,
        )
        if not circle:
            raise RuntimeError("Fusion failed to create a dog-bone circle.")

        bisector_2d = vertex_point.vectorTo(center_point)
        if not bisector_2d.normalize():
            raise RuntimeError("The dog-bone bisector has zero length.")
        edge_one_direction = self._line_direction_from_point(
            line_one,
            vertex_point,
        )
        placement_distance = max(self.inputs.diameter.value, 0.5)

        outside_text = self._translated_sketch_point(
            vertex_point,
            bisector_2d,
            placement_distance,
        )
        outside_dimension = sketch.sketchDimensions.addAngularDimension(
            line_one,
            line_two,
            outside_text,
            False,
        )
        if not outside_dimension or not outside_dimension.parameter:
            raise RuntimeError("Fusion failed to measure the outside corner angle.")
        self._name_parameter(
            outside_dimension.parameter,
            f"corner{corner_index}_outsideAngle",
        )

        # The length dimension must precede the bisector angular dimension:
        # the reverse order makes the sketch solver flag some corners as
        # over-constrained.
        length_text = center_line.endSketchPoint.geometry.copy()
        perpendicular = adsk.core.Vector3D.create(
            -bisector_2d.y,
            bisector_2d.x,
            0,
        )
        length_text.translateBy(perpendicular)
        length_dimension = sketch.sketchDimensions.addDistanceDimension(
            center_line.startSketchPoint,
            center_line.endSketchPoint,
            adsk.fusion.DimensionOrientations.AlignedDimensionOrientation,  # type: ignore
            length_text,
        )
        if not length_dimension or not length_dimension.parameter:
            raise RuntimeError("Fusion failed to dimension the dog-bone center line.")
        # The 1/sin(angle) reach compensation is baked as a numeric factor:
        # the corner angle is measured from fixed projected geometry and can
        # never change parametrically, and a max()/sin() expression that
        # references the driven angle breaks the sketch solver.
        compensation = max(1.0, 1.0 / math.sin(corner.outside_angle))
        length_dimension.parameter.expression = (
            f"({self.inputs.diameter.expression}) / 2 * {compensation:.9g}"
        )
        self._name_parameter(
            length_dimension.parameter,
            f"corner{corner_index}_centerDistance",
        )
        center_distance_name = length_dimension.parameter.name

        half_direction = edge_one_direction.copy()
        half_direction.add(bisector_2d)
        if not half_direction.normalize():
            raise RuntimeError("Fusion failed to locate the bisector angle dimension.")
        half_text = self._translated_sketch_point(
            vertex_point,
            half_direction,
            placement_distance * 0.75,
        )
        half_dimension = sketch.sketchDimensions.addAngularDimension(
            line_one,
            center_line,
            half_text,
        )
        if not half_dimension or not half_dimension.parameter:
            raise RuntimeError("Fusion failed to dimension the dog-bone bisector.")
        half_dimension.parameter.expression = (
            f"({outside_dimension.parameter.name}) / 2"
        )
        self._name_parameter(
            half_dimension.parameter,
            f"corner{corner_index}_bisectorAngle",
        )

        diameter_text = circle.centerSketchPoint.geometry.copy()
        diameter_text.x += max(
            self.inputs.diameter.value + self.inputs.offset.value,
            0.5,
        )
        diameter_dimension = sketch.sketchDimensions.addDiameterDimension(
            circle,
            diameter_text,
        )
        if not diameter_dimension or not diameter_dimension.parameter:
            raise RuntimeError("Fusion failed to dimension the dog-bone circle.")
        if self._first_center_distance_name is None:
            # The first corner carries the user's offset expression; later
            # corners reference it instead of duplicating the expression.
            diameter_dimension.parameter.expression = (
                f"2 * {center_distance_name} + "
                f"({self.inputs.offset.expression})"
            )
        else:
            diameter_dimension.parameter.expression = (
                f"2 * {center_distance_name} + "
                f"({self._first_diameter_name} - "
                f"2 * {self._first_center_distance_name})"
            )
        self._name_parameter(
            diameter_dimension.parameter,
            f"corner{corner_index}_diameter",
        )
        if self._first_center_distance_name is None:
            self._first_center_distance_name = center_distance_name
            self._first_diameter_name = diameter_dimension.parameter.name
        return circle

    def _unique_parameter_prefix(
        self,
        design: adsk.fusion.Design,
    ) -> str:
        parameter_names = {
            parameter.name
            for parameter in design.allParameters
        }
        base = "dogBones"
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

    def _line_endpoint_at(
        self,
        line: adsk.fusion.SketchLine,
        point: adsk.core.Point3D,
    ) -> adsk.fusion.SketchPoint:
        if (
            line.startSketchPoint.geometry.distanceTo(point)
            <= line.endSketchPoint.geometry.distanceTo(point)
        ):
            return line.startSketchPoint
        return line.endSketchPoint

    def _line_direction_from_point(
        self,
        line: adsk.fusion.SketchLine,
        point: adsk.core.Point3D,
    ) -> adsk.core.Vector3D:
        endpoint = self._line_endpoint_at(line, point)
        other = (
            line.endSketchPoint
            if endpoint == line.startSketchPoint
            else line.startSketchPoint
        )
        direction = point.vectorTo(other.geometry)
        if not direction.normalize():
            raise RuntimeError("A projected boundary line has zero length.")
        return direction

    def _translated_sketch_point(
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

    def _dogbone_profiles(
        self,
        sketch: adsk.fusion.Sketch,
        face: adsk.fusion.BRepFace,
        corners: list[_Corner],
        circles: list[adsk.fusion.SketchCircle],
    ) -> list[tuple[_Corner, adsk.fusion.Profile]]:
        if len(corners) != len(circles):
            raise RuntimeError("Each dog-bone corner must have one sketch circle.")

        selected: list[tuple[_Corner, adsk.fusion.Profile]] = []
        for corner, circle in zip(corners, circles):
            probe = self._dogbone_profile_probe(sketch, face, corner, circle)
            matches = [
                profile
                for profile in sketch.profiles
                if self._profile_uses_circle(profile, circle)
                and profile.face.isPointOnFace(
                    probe,
                    self.app.pointTolerance * 10,
                )
            ]
            if len(matches) != 1:
                raise RuntimeError(
                    "Fusion could not identify exactly one in-face profile "
                    "for a dog-bone circle."
                )
            selected.append((corner, matches[0]))

        if not selected:
            raise RuntimeError("No in-face dog-bone profiles were found.")
        return selected

    def _profile_uses_circle(
        self,
        profile: adsk.fusion.Profile,
        circle: adsk.fusion.SketchCircle,
    ) -> bool:
        return any(
            profile_curve.sketchEntity == circle
            for loop in profile.profileLoops
            for profile_curve in loop.profileCurves
        )

    def _dogbone_profile_probe(
        self,
        sketch: adsk.fusion.Sketch,
        face: adsk.fusion.BRepFace,
        corner: _Corner,
        circle: adsk.fusion.SketchCircle,
    ) -> adsk.core.Point3D:
        direction_one = self._edge_direction_from_vertex(
            corner.edge_one,
            corner.vertex,
        )
        direction_two = self._edge_direction_from_vertex(
            corner.edge_two,
            corner.vertex,
        )
        probe_direction = direction_one.copy()
        away_from_outside = direction_two.copy()
        away_from_outside.scaleBy(-0.05)
        probe_direction.add(away_from_outside)
        if not probe_direction.normalize():
            raise RuntimeError("Could not determine an in-face profile probe.")

        center_distance = self._center_distance_for_corner(corner)
        progress_towards_center = probe_direction.dotProduct(corner.bisector)
        if progress_towards_center <= 0:
            raise RuntimeError("The dog-bone profile probe points away from its circle.")
        probe_distance = min(
            circle.radius * 0.05,
            center_distance * progress_towards_center * 0.25,
        )
        probe_model = corner.vertex.geometry.copy()
        probe_offset = probe_direction.copy()
        probe_offset.scaleBy(probe_distance)
        probe_model.translateBy(probe_offset)

        if not face.isPointOnFace(
            probe_model,
            self.app.pointTolerance * 10,
        ):
            raise RuntimeError("Could not place a dog-bone profile probe inside the face.")
        probe = sketch.modelToSketchSpace(probe_model)
        center = circle.centerSketchPoint.geometry
        if probe.distanceTo(center) >= circle.radius:
            raise RuntimeError("The dog-bone profile probe lies outside its circle.")
        return probe

    def _create_cut_extrude(
        self,
        component: adsk.fusion.Component,
        face: adsk.fusion.BRepFace,
        opposite_face: adsk.fusion.BRepFace,
        sketch: adsk.fusion.Sketch,
        profiles: adsk.core.ObjectCollection,
        group_index: int = 1,
        group_count: int = 1,
    ) -> adsk.fusion.ExtrudeFeature:
        extrude_input = component.features.extrudeFeatures.createInput(
            profiles,
            adsk.fusion.FeatureOperations.CutFeatureOperation,  # type: ignore
        )
        if not extrude_input:
            raise RuntimeError("Fusion failed to initialize the dog-bone cut.")

        cut_direction = utils.brep.normal_towards_face(face, opposite_face)
        extent = adsk.fusion.ToEntityExtentDefinition.create(
            opposite_face,
            False,
        )
        if not extent:
            raise RuntimeError("Fusion failed to define the opposite-face extent.")
        extent.directionHint = cut_direction

        sketch_normal = sketch.xDirection.crossProduct(sketch.yDirection)
        direction = (
            adsk.fusion.ExtentDirections.PositiveExtentDirection
            if sketch_normal.dotProduct(cut_direction) >= 0
            else adsk.fusion.ExtentDirections.NegativeExtentDirection
        )
        if not extrude_input.setOneSideExtent(extent, direction):
            raise RuntimeError("Fusion rejected the dog-bone cut extent.")
        extrude_input.participantBodies = [face.body]

        extrude = component.features.extrudeFeatures.add(extrude_input)
        if not extrude:
            raise RuntimeError("Fusion failed to create the dog-bone cut.")
        extrude.name = (
            "Dog Bones (Native) - Cut"
            if group_count == 1
            else f"Dog Bones (Native) - Cut (Depth {group_index})"
        )
        sketch.isVisible = False
        return extrude

    def _group_features(
        self,
        component: adsk.fusion.Component,
        sketch: adsk.fusion.Sketch,
        extrude: adsk.fusion.ExtrudeFeature,
    ) -> None:
        group = component.parentDesign.timeline.timelineGroups.add(
            sketch.timelineObject.index,
            extrude.timelineObject.index,
        )
        if group:
            group.name = "Dog Bones (Native)"
            group.isCollapsed = True

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
            "Dog Bones (Native) generated an under-constrained sketch "
            f"({len(unconstrained)} unconstrained curves: {details})."
        )
