"""Fully constrained sketches laid out along a selected board edge, and the
cuts made from them.

The native joinery add-ins build their sketches the same way: on a face of
a board, with the selected edge projected in as a construction line, and
every other entity positioned against that line through constraints and as
few dimensions as possible. EdgeSketcher holds the helpers for that. They
started out in connectors_native and are shared with lib/domino.py.
"""
from dataclasses import dataclass
from typing import Callable, cast

import adsk.core
import adsk.fusion

from . import utils


@dataclass(frozen=True)
class SketchContext:
    sketch: adsk.fusion.Sketch
    edge_line: adsk.fusion.SketchLine
    edge_start: adsk.fusion.SketchPoint
    edge_end: adsk.fusion.SketchPoint
    parameter_role: str


def translated(
    point: adsk.core.Point3D,
    direction: adsk.core.Vector3D,
    distance: float,
) -> adsk.core.Point3D:
    result = point.copy()
    translation = direction.copy()
    translation.scaleBy(distance)
    result.translateBy(translation)
    return result


def opposite(direction: adsk.core.Vector3D) -> adsk.core.Vector3D:
    result = direction.copy()
    result.scaleBy(-1)
    return result


def edge_midpoint(edge: adsk.fusion.BRepEdge) -> adsk.core.Point3D:
    start = edge.startVertex.geometry
    end = edge.endVertex.geometry
    return adsk.core.Point3D.create(
        (start.x + end.x) / 2,
        (start.y + end.y) / 2,
        (start.z + end.z) / 2,
    )


def extent_direction(
    sketch: adsk.fusion.Sketch,
    direction: adsk.core.Vector3D,
):
    sketch_normal = sketch.xDirection.crossProduct(sketch.yDirection)
    return (
        adsk.fusion.ExtentDirections.PositiveExtentDirection
        if sketch_normal.dotProduct(direction) >= 0
        else adsk.fusion.ExtentDirections.NegativeExtentDirection
    )


def evenly_spaced_positions(
    edge: adsk.fusion.BRepEdge,
    count: int,
    end_offset: float,
) -> list[adsk.core.Point3D]:
    """`count` points along the edge, the first and last `end_offset` from
    its ends and the rest evenly spaced between them. A single point is
    centered on the edge."""
    direction = utils.brep.normal_along_edge(edge)
    if count == 1:
        distances = [edge.length / 2]
    else:
        spacing = (edge.length - 2 * end_offset) / (count - 1)
        distances = [end_offset + index * spacing for index in range(count)]
    return [
        translated(edge.startVertex.geometry, direction, distance)
        for distance in distances
    ]


def find_by_token(
    design: adsk.fusion.Design,
    token: str,
    entity_type,
    description: str,
):
    """Re-resolves an entity of `entity_type` (e.g. adsk.fusion.BRepBody)
    from its entity token. Features created in between can invalidate a
    direct reference to a body or face, the token still finds it."""
    entity = next(
        (
            candidate
            for found in design.findEntityByToken(token)
            if (candidate := entity_type.cast(found))
        ),
        None,
    )
    if not entity:
        raise RuntimeError(f"Fusion could not re-resolve the {description}.")
    return entity


class EdgeSketcher:
    """Builds the sketch entities and cuts of a native joinery add-in.

    Every dimension's expression goes through `set_expression` and every
    created parameter through `name_parameter`, so the add-in keeps control
    over the cost of those writes (see e.g.
    ConnectorsNative._set_parameter_expression).
    """

    def __init__(
        self,
        set_expression: Callable[[adsk.fusion.ModelParameter, str], None],
        name_parameter: Callable[[adsk.fusion.ModelParameter, str], None],
    ):
        self.app = adsk.core.Application.get()
        self._set_expression = set_expression
        self._name_parameter = name_parameter

    def create_sketch(
        self,
        component: adsk.fusion.Component,
        face: adsk.fusion.BRepFace,
        edge: adsk.fusion.BRepEdge,
        name: str,
        parameter_role: str,
    ) -> SketchContext:
        sketch = component.sketches.addWithoutEdges(face)
        if not sketch:
            raise RuntimeError(f"Fusion failed to create '{name}'.")
        sketch.name = name
        edge_line = self.project_single_line(
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
        # Defer the sketch solve while the geometry is added: in large
        # documents every individual sketch mutation otherwise pays a full
        # document-transaction cost (~80-560 ms each measured). Deferring
        # must start only after project2 (it throws InternalValidationError
        # on a deferred sketch). The sketch is re-solved in
        # require_fully_constrained, which every build path calls before the
        # sketch is read again; a fully constrained sketch solves to the same
        # geometry either way.
        sketch.isComputeDeferred = True
        return SketchContext(
            sketch=sketch,
            edge_line=edge_line,
            edge_start=edge_start,
            edge_end=edge_end,
            parameter_role=parameter_role,
        )

    def require_fully_constrained(
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

    # Projection

    def project_entities(
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

    def project_single_line(
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
        would split the profiles the joint geometry is built from.

        Lines that already existed before the call are never deleted: a
        repeated projection can return the line an earlier call created,
        and that one still belongs to its caller.
        """
        before = list(sketch.sketchCurves.sketchLines)
        projected = [
            line
            for candidate in self.project_entities(
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

    def project_reference_line(
        self,
        sketch: adsk.fusion.Sketch,
        edge: adsk.fusion.BRepEdge,
        description: str,
    ) -> adsk.fusion.SketchLine:
        projected = self.project_single_line(sketch, edge, description)
        projected.isConstruction = True
        return projected

    def project_opposite_edge(
        self,
        sketch: adsk.fusion.Sketch,
        small_face: adsk.fusion.BRepFace,
        selected_edge: adsk.fusion.BRepEdge,
    ) -> adsk.fusion.SketchLine:
        selected_midpoint = edge_midpoint(selected_edge)
        candidates = [
            edge
            for edge in small_face.edges
            if (
                utils.brep.is_linear(edge)
                and utils.brep.is_parallel(edge, selected_edge)
                and edge_midpoint(edge).distanceTo(selected_midpoint) > 1e-6
            )
        ]
        if not candidates:
            raise RuntimeError(
                "Could not find the opposite long edge of the small face."
            )
        opposite_edge = max(
            candidates,
            key=lambda edge: edge_midpoint(edge).distanceTo(selected_midpoint),
        )
        return self.project_reference_line(
            sketch,
            opposite_edge,
            "opposite edge of the small face",
        )

    def project_points(
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
            for entity in self.project_entities(
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

    def project_point(
        self,
        sketch: adsk.fusion.Sketch,
        source_point: adsk.core.Base,
        description: str,
    ) -> adsk.fusion.SketchPoint:
        projected = [
            point
            for entity in self.project_entities(
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

    # Stations along the selected edge

    def add_station_points(
        self,
        context: SketchContext,
        positions: list[adsk.core.Point3D],
        custom_points: list[adsk.core.Base] | None,
        end_offset: tuple[float, str] | None,
    ) -> list[adsk.fusion.SketchPoint]:
        """Points on the projected edge at `positions` (sorted along the
        edge). With `custom_points` (sorted the same way), each station
        follows the projection of its point. Otherwise the stations are
        spaced equally, the first and last `end_offset` (value and
        expression) from the edge's ends; a single station is centered."""
        if custom_points is not None:
            return self._add_custom_station_points(
                context,
                custom_points,
                positions,
            )
        return self._add_position_points(context, positions, end_offset)

    def _add_custom_station_points(
        self,
        context: SketchContext,
        source_points: list[adsk.core.Base],
        positions: list[adsk.core.Point3D],
    ) -> list[adsk.fusion.SketchPoint]:
        if len(source_points) != len(positions):
            raise RuntimeError(
                "The Custom Point projections are incomplete."
            )

        sketch = context.sketch
        constraints = sketch.geometricConstraints
        stations: list[adsk.fusion.SketchPoint] = []
        for source_point, position in zip(source_points, positions):
            projected = self.project_point(
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
        context: SketchContext,
        positions: list[adsk.core.Point3D],
        end_offset: tuple[float, str] | None,
    ) -> list[adsk.fusion.SketchPoint]:
        sketch = context.sketch
        constraints = sketch.geometricConstraints
        count = len(positions)
        points: list[adsk.fusion.SketchPoint] = []
        for position in positions:
            point = sketch.sketchPoints.add(
                sketch.modelToSketchSpace(position)
            )
            if not point:
                raise RuntimeError(
                    "Fusion failed to create a position point."
                )
            constraints.addCoincident(point, context.edge_line)
            points.append(point)

        if count == 1:
            constraints.addMidPoint(points[0], context.edge_line)
            return points

        if end_offset is None:
            raise ValueError("Equally spaced positions need an end offset.")
        end_offset_value, end_offset_expression = end_offset
        if end_offset_value == 0:
            constraints.addCoincident(points[0], context.edge_start)
            constraints.addCoincident(points[-1], context.edge_end)
        else:
            first_margin = self.add_distance_dimension(
                sketch,
                context.edge_start,
                points[0],
                end_offset_expression,
                f"{context.parameter_role}FirstMargin",
            )
            self.add_distance_dimension(
                sketch,
                points[-1],
                context.edge_end,
                first_margin.parameter.name,
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
                    "Fusion failed to create spacing geometry."
                )
            spacing_line.isConstruction = True
            spacing_lines.append(spacing_line)
        for spacing_line in spacing_lines[1:]:
            constraints.addEqual(spacing_lines[0], spacing_line)
        return points

    def board_center_points(
        self,
        context: SketchContext,
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
        opposite_edge = self.project_opposite_edge(
            context.sketch,
            small_face,
            edge,
        )
        lines = context.sketch.sketchCurves.sketchLines
        constraints = context.sketch.geometricConstraints
        centers: list[adsk.fusion.SketchPoint] = []
        cross_lines: list[adsk.fusion.SketchLine] = []
        for base_point in base_points:
            initial_end = translated(base_point.worldGeometry, inward, 1)
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
            centers.append(self._add_midpoint(context.sketch, cross_line))
            cross_lines.append(cross_line)
        return centers, cross_lines

    def centered_points_for_board(
        self,
        context: SketchContext,
        edge: adsk.fusion.BRepEdge,
        small_face: adsk.fusion.BRepFace,
        thickness: float,
        reference_cross_lines: list[adsk.fusion.SketchLine],
        stations: list[adsk.fusion.SketchPoint] | None = None,
    ) -> list[adsk.fusion.SketchPoint]:
        """The board_center_points of a further board along `edge`, at the
        stations of `reference_cross_lines` (the first board's). When
        `stations` is given, the points where each station meets the
        board's edge are appended to it."""
        sketch = context.sketch
        lines = sketch.sketchCurves.sketchLines
        constraints = sketch.geometricConstraints
        board_edge_line = self.project_reference_line(
            sketch,
            edge,
            "additional board edge",
        )
        opposite_edge = self.project_opposite_edge(sketch, small_face, edge)
        inward = utils.brep.normal_into_face(edge, small_face)
        centers: list[adsk.fusion.SketchPoint] = []
        for reference in reference_cross_lines:
            # Same station as the first board's cross line, spanning this
            # board's own small face so the points stay centered on its
            # thickness. Collinearity with the reference line carries the
            # along-edge position without a fixed dimension.
            start_model = utils.brep.project_point_onto_edge(
                reference.startSketchPoint.worldGeometry,
                edge,
            )
            end_model = translated(start_model, inward, thickness)
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
            centers.append(self._add_midpoint(sketch, cross_line))
            if stations is not None:
                stations.append(cross_line.startSketchPoint)
        return centers

    def edge_offset_points(
        self,
        context: SketchContext,
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
            initial_end = translated(
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

        self.add_distance_dimension(
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

    def offset_points_for_board(
        self,
        context: SketchContext,
        edge: adsk.fusion.BRepEdge,
        small_face: adsk.fusion.BRepFace,
        reference_offset_lines: list[adsk.fusion.SketchLine],
        stations: list[adsk.fusion.SketchPoint] | None = None,
    ) -> list[adsk.fusion.SketchPoint]:
        """The edge_offset_points of a further board along `edge`, at the
        stations and offset of `reference_offset_lines` (the first
        board's). When `stations` is given, the points where each station
        meets the board's edge are appended to it."""
        sketch = context.sketch
        lines = sketch.sketchCurves.sketchLines
        constraints = sketch.geometricConstraints
        board_edge_line = self.project_reference_line(
            sketch,
            edge,
            "additional board edge",
        )
        inward = utils.brep.normal_into_face(edge, small_face)
        points: list[adsk.fusion.SketchPoint] = []
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
                edge,
            )
            end_model = translated(start_model, inward, reference_length)
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
            points.append(offset_line.endSketchPoint)
            if stations is not None:
                stations.append(offset_line.startSketchPoint)
        return points

    def _add_midpoint(
        self,
        sketch: adsk.fusion.Sketch,
        line: adsk.fusion.SketchLine,
    ) -> adsk.fusion.SketchPoint:
        start = line.startSketchPoint.geometry
        end = line.endSketchPoint.geometry
        midpoint = sketch.sketchPoints.add(
            adsk.core.Point3D.create(
                (start.x + end.x) / 2,
                (start.y + end.y) / 2,
                0,
            )
        )
        if not midpoint:
            raise RuntimeError("Fusion failed to create a midpoint.")
        sketch.geometricConstraints.addMidPoint(midpoint, line)
        return midpoint

    # Dimensioned geometry

    def add_center_to_center_slot(
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
        self._set_expression(dimensions[0].parameter, width_expression)
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

    def add_distance_dimension(
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
                "Fusion failed to create a distance dimension."
            )
        if is_driving:
            if expression is None:
                raise ValueError("A driving dimension requires an expression.")
            self._set_expression(dimension.parameter, expression)
        self._name_parameter(dimension.parameter, parameter_role)
        return dimension

    # Cuts

    def create_cut_extrude(
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
        """Cuts every profile of `sketch` `distance` deep, into
        `target_body` only. With `start_face` the cut starts at that face
        instead of the sketch plane."""
        extrude_input = component.features.extrudeFeatures.createInput(
            self._all_profiles(sketch),
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
        if not extrude_input.setOneSideExtent(
            extent,
            extent_direction(sketch, direction),
        ):
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

    def create_cut_extrude_to_face(
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
        extrude_input = component.features.extrudeFeatures.createInput(
            self._all_profiles(sketch),
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
            extent_direction(sketch, direction),
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
