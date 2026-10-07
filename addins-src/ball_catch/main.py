import os
from dataclasses import dataclass, field
from typing import cast

import adsk.core
import adsk.fusion

from lib import addin, edge_sketch, hole_features, inputs, ui_placement, utils
from lib.fusionbootstrap.runtime import RuntimeInfo


_addin: addin.Addin | None = None

NAME = "Ball Catch"
#: Geometric tolerance for the placement checks, in cm.
TOLERANCE = 1e-4
#: How far inside a face the fit probes along its border sit, in cm.
PROBE_INSET = 0.01


def _mm(value_cm: float) -> str:
    """Derive a millimeter expression string from a centimeter value so the
    sketch dimensions can never drift from the analytic placement math."""
    return f"{value_cm * 10:.6g} mm"


def _format_mm(value_cm: float) -> str:
    return f"{value_cm * 10:.1f}".rstrip("0").rstrip(".") + " mm"


@dataclass(frozen=True)
class CatchSpec:
    """Mounting data of a ball catch that holds an inspection hatch in its
    opening, in cm.

    The catch bridges the slot milled around the hatch: the holder is
    screwed to the frame with its stop webs against the opening's edge
    (the contour), the ball to the hatch. Both screws sit on the
    perpendicular to the contour through the catch's position.
    """

    name: str
    #: From the contour into the frame.
    holder_hole_outward: float
    #: From the contour into the hatch.
    ball_hole_inward: float
    #: Along the contour. The stop webs at its ends must bear on a straight
    #: edge.
    holder_width: float
    #: Width of the ball along the contour.
    ball_width: float
    #: Diameter of the ball's base around its screw.
    ball_base_diameter: float
    #: Width range of the slot between frame and hatch.
    min_gap: float
    max_gap: float
    #: Mounting surface each part needs beside the slot.
    mounting_depth: float


# Ganter GN 450-28-14, from the catalog drawing: the holder's screw sits
# 8.4 mm from its stop webs, and the two screws are s1 = 17.8-19.3 mm apart,
# so the ball's screw goes 9.4 mm (s1 min) into the hatch. The slot must be
# 2.5-3.5 mm wide, and each part needs 15 mm of mounting surface beside it.
GN_450 = CatchSpec(
    name="GN 450",
    holder_hole_outward=0.84,
    ball_hole_inward=0.94,
    holder_width=2.8,
    ball_width=1.4,
    ball_base_diameter=1.0,
    min_gap=0.25,
    max_gap=0.35,
    mounting_depth=1.5,
)


def run(context, runtime_info: RuntimeInfo):
    global _addin
    _addin = BallCatch(runtime_info)
    # Dev support: allow external tooling to restart this add-in by firing the
    # custom event '<id>_reload' (see lib/fusionbootstrap/reloader.py).
    from lib.fusionbootstrap import reloader
    entry = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "ball_catch.py",
    )
    reloader.ensure(runtime_info.id + "_reload", entry)


def stop(context):
    global _addin
    if _addin:
        _addin.shutdown()
    _addin = None


class BallCatchInputs(inputs.Inputs):
    class Positioning:
        NUMBER = inputs.DropDownInput.Item("Number of Catches", 0)
        CUSTOM_POINTS = inputs.DropDownInput.Item("Custom Points", 1)

    def __init__(self, units_manager: adsk.core.UnitsManager):
        units = units_manager.defaultLengthUnits
        self.opening_edge = inputs.SelectionByEntityTokenInput(
            id="opening_edge",
            name="Opening Edge",
            filter=["LinearEdges"],
            lower_bound=1,
            upper_bound=1,
            tool_tip=(
                "Select a straight edge of the opening in the frame, on the "
                "face the catches are screwed to. The catches go on this edge "
                "and the opposite one."
            ),
        )
        self.positioning = inputs.DropDownInput(
            id="positioning",
            name="Positioning",
            options=utils.misc.class_property_values(
                BallCatchInputs.Positioning,
                inputs.DropDownInput.Item,
            ),
            default_value=BallCatchInputs.Positioning.NUMBER.value,
            tool_tip=(
                "Space a number of catches along the Opening Edge and the "
                "opposite edge, or place a catch at each selected point."
            ),
        )
        is_number_positioning = lambda: (
            self.positioning.value == BallCatchInputs.Positioning.NUMBER.value
        )
        self.number_of_catches = inputs.IntegerInput(
            id="number_of_catches",
            name="Number of Catches",
            default_value=4,
            minimum=1,
            maximum=20,
            tool_tip=(
                "The catches are shared between the Opening Edge and the "
                "opposite edge. With an odd number, the Opening Edge gets one "
                "more."
            ),
            update_visibility=is_number_positioning,
        )
        self.end_offset = inputs.FloatInput(
            id="end_offset",
            name="End Offset",
            default_value=4.0,
            tool_tip=(
                "Distance of the first and last catch on an edge from the ends "
                "of its straight part. A single catch on an edge is centered."
            ),
            units=units,
            update_visibility=lambda: (
                is_number_positioning() and self.number_of_catches.value > 2
            ),
        )
        self.end_offset.minimum_value = 0
        self.points = inputs.SelectionByEntityTokenInput(
            id="points",
            name="Custom Points",
            filter=["Vertices", "SketchPoints", "ConstructionPoints"],
            lower_bound=0,
            upper_bound=0,
            tool_tip=(
                "Select a point on the opening's contour for each catch. Each "
                "point is projected perpendicularly onto the nearest straight "
                "edge of the opening."
            ),
            update_visibility=lambda: not is_number_positioning(),
        )
        self.pilot_diameter = inputs.FloatInput(
            id="pilot_diameter",
            name="Pilot Diameter",
            default_value=0.2,
            tool_tip="Diameter of the pilot holes for the holder and ball screws.",
            units=units,
        )
        self.pilot_diameter.minimum_value = 0.0001
        self.pilot_depth = inputs.FloatInput(
            id="pilot_depth",
            name="Pilot Depth",
            default_value=0.4,
            tool_tip="Depth of the flat-bottomed pilot holes.",
            units=units,
        )
        self.pilot_depth.minimum_value = 0.0001
        super().__init__()


class _InputError(Exception):
    """A selection or value the catches cannot be placed with; the message is
    shown in the dialog."""


@dataclass
class _Catch:
    #: Counts from 1, in the order the dialog's messages refer to.
    number: int
    #: Where the catch sits on the contour.
    station: adsk.core.Point3D
    holder: adsk.core.Point3D
    ball: adsk.core.Point3D
    #: The Custom Point the catch follows, None when spaced by number.
    source: adsk.core.Base | None


@dataclass
class _Side:
    """A straight edge of the opening and the catches on it."""

    edge: adsk.fusion.BRepEdge
    label: str
    #: From the edge's start to its end.
    along: adsk.core.Vector3D
    #: In the frame face, away from the opening.
    outward: adsk.core.Vector3D
    #: Sorted along the edge.
    catches: list[_Catch] = field(default_factory=list)

    def distance_along(self, point: adsk.core.Point3D) -> float:
        return self.edge.startVertex.geometry.vectorTo(point).dotProduct(self.along)

    def point_at(self, distance: float, outward: float = 0.0) -> adsk.core.Point3D:
        point = edge_sketch.translated(
            self.edge.startVertex.geometry,
            self.along,
            distance,
        )
        return edge_sketch.translated(point, self.outward, outward)


@dataclass
class _Layout:
    frame_face: adsk.fusion.BRepFace
    hatch_face: adsk.fusion.BRepFace
    sides: list[_Side]
    #: The End Offset (value, expression) when spaced by number and some
    #: edge carries more than one catch.
    end_offset: tuple[float, str] | None


def _opening_face(
    edge: adsk.fusion.BRepEdge,
) -> tuple[adsk.fusion.BRepFace, adsk.fusion.BRepLoop] | None:
    """The planar face in which the edge borders a hole, and that hole's
    loop."""
    for face in edge.faces:
        if not utils.brep.is_planar(face):
            continue
        for loop in face.loops:
            if not loop.isOuter and any(candidate == edge for candidate in loop.edges):
                return face, loop
    return None


class BallCatch(addin.Addin):
    inputs: BallCatchInputs
    _sketcher: edge_sketch.EdgeSketcher

    @property
    def resource_dir(self) -> str:
        # Absolute path so the command can also be (re)registered from outside
        # Fusion's add-in launcher (e.g. a scripted restart during development).
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), "Resources")

    @property
    def preview_enabled(self) -> bool:
        # execute() builds native features only, so Fusion's executePreview
        # transaction can run it as a live preview and roll it back again.
        return True

    @property
    def group_edit_enabled(self) -> bool:
        return True

    @property
    def plugin_name(self) -> str:
        return NAME

    @property
    def plugin_desc(self) -> str:
        return "Pilot holes for the ball catches that hold an inspection hatch in its opening."

    @property
    def plugin_tooltip(self) -> str:
        return (
            "Creates a fully constrained layout and flat-bottomed pilot holes "
            "for Ganter GN 450 ball catches: the holders on the frame beside "
            "the opening, the balls on the hatch."
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

    def create_inputs(self) -> BallCatchInputs:
        design = adsk.fusion.Design.cast(self.app.activeProduct)
        if not design:
            raise RuntimeError(f"{NAME} requires an active Fusion design.")
        return BallCatchInputs(design.unitsManager)

    # Selection

    def pre_select(self, input, selection) -> bool:
        if not self.inputs or not input:
            return True
        if input.id == self.inputs.opening_edge.id:
            edge = adsk.fusion.BRepEdge.cast(selection)
            return bool(
                edge
                and edge.body
                and edge.body.isSolid
                and utils.brep.is_linear(edge)
                and _opening_face(edge)
            )
        if input.id == self.inputs.points.id:
            return bool(
                adsk.fusion.BRepVertex.cast(selection)
                or adsk.fusion.SketchPoint.cast(selection)
                or adsk.fusion.ConstructionPoint.cast(selection)
            )
        return True

    # Validation

    def _validate(self, args: adsk.core.ValidateInputsEventArgs):
        self._apply_validation(args, self._validation_error)

    def _validation_error(self) -> str | None:
        try:
            self._layout()
        except _InputError as error:
            return str(error)
        return None

    def _is_number_positioning(self) -> bool:
        return (
            self.inputs.positioning.value
            == BallCatchInputs.Positioning.NUMBER.value
        )

    def _layout(self) -> _Layout:
        """Resolves the selections and computes every hole position.
        Raises _InputError when the catches cannot be placed."""
        design = adsk.fusion.Design.cast(self.app.activeProduct)
        if not design:
            raise _InputError("An active Fusion design is required.")
        if design.designType != adsk.fusion.DesignTypes.ParametricDesignType:  # type: ignore
            raise _InputError(f"{NAME} requires Design History (a parametric design).")
        if not self.inputs or len(self.inputs.opening_edge.value) != 1:
            raise _InputError("Select the Opening Edge.")
        spec = GN_450
        if self.inputs.pilot_diameter.value <= 0:
            raise _InputError("Pilot Diameter must be greater than zero.")
        if self.inputs.pilot_depth.value <= 0:
            raise _InputError("Pilot Depth must be greater than zero.")

        edge = self._native_edge(self.inputs.opening_edge.value[0])
        if edge.body.parentComponent != design.activeComponent:
            raise _InputError(
                "The frame must belong to the active component. Activate the "
                f"component that owns it, then run {NAME} again."
            )
        opening = _opening_face(edge)
        if not opening:
            raise _InputError(
                "The Opening Edge must border the opening in a flat face of "
                "the frame. Select an edge of the opening's contour on the "
                "face the catches go on."
            )
        frame_face, loop = opening
        try:
            frame_thickness = utils.brep.get_board_thickness(frame_face)
        except (ValueError, RuntimeError):
            raise _InputError("The frame must be a board with two parallel faces.")

        selected = self._side(edge, frame_face, "Opening Edge")
        if self._is_number_positioning():
            sides, end_offset = self._spaced_sides(spec, selected, frame_face, loop)
        else:
            sides = self._custom_point_sides(spec, design, frame_face, loop)
            end_offset = None
        catches = sorted(
            (catch for side in sides for catch in side.catches),
            key=lambda catch: catch.number,
        )

        hatch_face = self._hatch_face(frame_face, catches)
        try:
            hatch_thickness = utils.brep.get_board_thickness(hatch_face)
        except (ValueError, RuntimeError):
            raise _InputError("The hatch must be a board with two parallel faces.")
        depth = self.inputs.pilot_depth.value
        if depth >= frame_thickness - TOLERANCE:
            raise _InputError(
                "Pilot Depth must be less than the frame thickness "
                f"({_format_mm(frame_thickness)})."
            )
        if depth >= hatch_thickness - TOLERANCE:
            raise _InputError(
                "Pilot Depth must be less than the hatch thickness "
                f"({_format_mm(hatch_thickness)})."
            )
        for side in sides:
            gap = self._gap(side, hatch_face)
            if not spec.min_gap - TOLERANCE <= gap <= spec.max_gap + TOLERANCE:
                raise _InputError(
                    f"The slot between frame and hatch is {_format_mm(gap)} "
                    f"wide at the {side.label}. The {spec.name} needs "
                    f"{_format_mm(spec.min_gap)} to {_format_mm(spec.max_gap)}."
                )
            self._check_fit(spec, side, gap, frame_face, hatch_face)
        return _Layout(
            frame_face=frame_face,
            hatch_face=hatch_face,
            sides=sides,
            end_offset=end_offset,
        )

    def _side(
        self,
        edge: adsk.fusion.BRepEdge,
        frame_face: adsk.fusion.BRepFace,
        label: str,
    ) -> _Side:
        along = utils.brep.normal_along_edge(edge)
        _, normal = frame_face.evaluator.getNormalAtPoint(edge.startVertex.geometry)
        outward = along.crossProduct(normal)
        outward.normalize()
        probe = edge_sketch.translated(
            edge_sketch.edge_midpoint(edge),
            outward,
            PROBE_INSET,
        )
        if not frame_face.isPointOnFace(probe, TOLERANCE):
            outward.scaleBy(-1)
        return _Side(edge=edge, label=label, along=along, outward=outward)

    def _catch(
        self,
        spec: CatchSpec,
        side: _Side,
        distance: float,
        number: int,
        source: adsk.core.Base | None,
    ) -> _Catch:
        return _Catch(
            number=number,
            station=side.point_at(distance),
            holder=side.point_at(distance, spec.holder_hole_outward),
            ball=side.point_at(distance, -spec.ball_hole_inward),
            source=source,
        )

    def _spaced_sides(
        self,
        spec: CatchSpec,
        selected: _Side,
        frame_face: adsk.fusion.BRepFace,
        loop: adsk.fusion.BRepLoop,
    ) -> tuple[list[_Side], tuple[float, str] | None]:
        """The selected edge takes the larger half of the catches, the
        opposite edge the rest. One catch on an edge is centered; more run
        from End Offset to End Offset, evenly spaced."""
        count = self.inputs.number_of_catches.value
        counts = [(count + 1) // 2, count // 2]
        sides = [selected]
        if counts[1]:
            sides.append(self._opposite_side(selected, frame_face, loop))
        offset = self.inputs.end_offset.value
        half_width = spec.holder_width / 2
        number = 1
        for side, side_count in zip(sides, counts):
            length = side.edge.length
            if side_count == 1:
                if length < spec.holder_width - TOLERANCE:
                    raise _InputError(
                        f"The {side.label} is {_format_mm(length)} long, "
                        f"shorter than the {_format_mm(spec.holder_width)} "
                        "wide holder."
                    )
                distances = [length / 2]
            else:
                if offset < half_width - TOLERANCE:
                    raise _InputError(
                        f"End Offset must be at least {_format_mm(half_width)}: "
                        f"the {_format_mm(spec.holder_width)} wide holder must "
                        "sit on the straight part of the edge."
                    )
                spacing = (length - 2 * offset) / (side_count - 1)
                if spacing < spec.holder_width - TOLERANCE:
                    needed = 2 * offset + (side_count - 1) * spec.holder_width
                    raise _InputError(
                        f"The {side.label} is {_format_mm(length)} long. "
                        f"{side_count} catches {_format_mm(offset)} from its "
                        f"ends need {_format_mm(needed)}."
                    )
                distances = [offset + index * spacing for index in range(side_count)]
            side.catches = [
                self._catch(spec, side, distance, number + index, None)
                for index, distance in enumerate(distances)
            ]
            number += side_count
        end_offset = None
        if any(len(side.catches) > 1 for side in sides):
            end_offset = (offset, self.inputs.end_offset.expression or _mm(offset))
        return sides, end_offset

    def _opposite_side(
        self,
        selected: _Side,
        frame_face: adsk.fusion.BRepFace,
        loop: adsk.fusion.BRepLoop,
    ) -> _Side:
        """The straight edge across the opening from the selected one: it
        runs parallel, faces it, and overlaps it the most (the nearest one
        on a tie)."""
        length = selected.edge.length
        candidates: list[tuple[float, float, _Side]] = []
        for edge in loop.edges:
            if (
                edge == selected.edge
                or not utils.brep.is_linear(edge)
                or not utils.brep.is_parallel(edge, selected.edge)
            ):
                continue
            across = -selected.outward.dotProduct(
                selected.edge.startVertex.geometry.vectorTo(edge.startVertex.geometry)
            )
            if across <= TOLERANCE:
                continue
            ends = sorted(
                selected.distance_along(vertex.geometry)
                for vertex in (edge.startVertex, edge.endVertex)
            )
            overlap = min(ends[1], length) - max(ends[0], 0.0)
            if overlap <= TOLERANCE:
                continue
            side = self._side(edge, frame_face, "opposite edge")
            if side.outward.dotProduct(selected.outward) >= 0:
                continue
            candidates.append((round(overlap / TOLERANCE), -across, side))
        if not candidates:
            raise _InputError(
                "The opening has no straight edge opposite the Opening Edge. "
                "Use Custom Points to place the catches."
            )
        return max(candidates, key=lambda candidate: candidate[:2])[2]

    def _custom_point_sides(
        self,
        spec: CatchSpec,
        design: adsk.fusion.Design,
        frame_face: adsk.fusion.BRepFace,
        loop: adsk.fusion.BRepLoop,
    ) -> list[_Side]:
        """Each Custom Point goes onto the nearest straight edge of the
        opening, perpendicularly."""
        if not self.inputs.points.value:
            raise _InputError("Select at least one Custom Point.")
        edges = [edge for edge in loop.edges if utils.brep.is_linear(edge)]
        if not edges:
            raise _InputError("The opening has no straight edges.")
        plane_origin = loop.edges.item(0).startVertex.geometry
        _, normal = frame_face.evaluator.getNormalAtPoint(plane_origin)
        half_width = spec.holder_width / 2
        sides: list[_Side] = []
        for number, entity in enumerate(self.inputs.points.value, 1):
            source, point, component = self._native_point(entity)
            if component != design.activeComponent:
                raise _InputError("Custom Points must belong to the active component.")
            # Into the frame face's plane.
            point = edge_sketch.translated(
                point,
                normal,
                -plane_origin.vectorTo(point).dotProduct(normal),
            )
            nearest: tuple[float, adsk.fusion.BRepEdge, float] | None = None
            for edge in edges:
                start = edge.startVertex.geometry
                along = utils.brep.normal_along_edge(edge)
                distance = start.vectorTo(point).dotProduct(along)
                foot = edge_sketch.translated(
                    start,
                    along,
                    min(max(distance, 0.0), edge.length),
                )
                offset = foot.distanceTo(point)
                if nearest is None or offset < nearest[0]:
                    nearest = (offset, edge, distance)
            assert nearest is not None
            _, edge, distance = nearest
            side = next((side for side in sides if side.edge == edge), None)
            if side is None:
                side = self._side(edge, frame_face, f"edge of Custom Point {number}")
                sides.append(side)
            if not (
                half_width - TOLERANCE
                <= distance
                <= edge.length - half_width + TOLERANCE
            ):
                raise _InputError(
                    f"Custom Point {number} is too close to the end of its "
                    f"edge's straight part. The {_format_mm(spec.holder_width)} "
                    f"wide holder needs {_format_mm(half_width)} on both sides."
                )
            side.catches.append(self._catch(spec, side, distance, number, source))

        for side in sides:
            side.catches.sort(key=lambda catch: side.distance_along(catch.station))
            for first, second in zip(side.catches, side.catches[1:]):
                spacing = side.distance_along(second.station) - side.distance_along(
                    first.station
                )
                if spacing < spec.holder_width - TOLERANCE:
                    raise _InputError(
                        f"Custom Points {min(first.number, second.number)} and "
                        f"{max(first.number, second.number)} are "
                        f"{_format_mm(spacing)} apart. The holders are "
                        f"{_format_mm(spec.holder_width)} wide."
                    )
        return sides

    def _hatch_face(
        self,
        frame_face: adsk.fusion.BRepFace,
        catches: list[_Catch],
    ) -> adsk.fusion.BRepFace:
        """The hatch's face the balls are screwed to: the face of another
        body that lies in the frame face's plane under every ball."""
        component = frame_face.body.parentComponent
        hatch_face: adsk.fusion.BRepFace | None = None
        for catch in catches:
            face = self._face_at(component, frame_face, catch.ball)
            if not face:
                raise _InputError(
                    f"There is no hatch under the ball of catch {catch.number}. "
                    "Model the hatch as a separate body in the opening, flush "
                    "with the frame on this face."
                )
            if hatch_face is None:
                hatch_face = face
            elif face != hatch_face:
                raise _InputError("All balls must go on the same hatch.")
        assert hatch_face is not None
        return hatch_face

    def _face_at(
        self,
        component: adsk.fusion.Component,
        frame_face: adsk.fusion.BRepFace,
        point: adsk.core.Point3D,
    ) -> adsk.fusion.BRepFace | None:
        # A point search instead of a scan over all faces: that stays cheap
        # in large designs.
        found = component.findBRepUsingPoint(
            point,
            adsk.fusion.BRepEntityTypes.BRepFaceEntityType,  # type: ignore
            TOLERANCE,
            True,
        )
        for entity in found:
            face = adsk.fusion.BRepFace.cast(entity)
            if (
                face
                and face.body != frame_face.body
                and face.body.isSolid
                and utils.brep.is_planar(face)
                and utils.brep.is_parallel(face, frame_face)
                and face.isPointOnFace(point, TOLERANCE)
            ):
                return face
        return None

    def _gap(self, side: _Side, hatch_face: adsk.fusion.BRepFace) -> float:
        """Width of the slot between the side's edge and the hatch."""
        result = self.app.measureManager.measureMinimumDistance(side.edge, hatch_face)
        return result.value

    def _check_fit(
        self,
        spec: CatchSpec,
        side: _Side,
        gap: float,
        frame_face: adsk.fusion.BRepFace,
        hatch_face: adsk.fusion.BRepFace,
    ) -> None:
        """Each part needs its mounting surface beside the slot, and the
        pilot holes must land on their faces."""
        pilot_radius = self.inputs.pilot_diameter.value / 2
        base_radius = max(spec.ball_base_diameter / 2, pilot_radius)
        for catch in side.catches:
            distance = side.distance_along(catch.station)
            holder_probes = [
                side.point_at(distance + sign * spec.holder_width / 2, outward)
                for sign in (-1, 1)
                for outward in (PROBE_INSET, spec.mounting_depth)
            ] + self._rim(side, catch.holder, pilot_radius)
            if not all(frame_face.isPointOnFace(probe, TOLERANCE) for probe in holder_probes):
                raise _InputError(
                    f"The holder of catch {catch.number} does not fit on the "
                    f"frame. It needs {_format_mm(spec.holder_width)} × "
                    f"{_format_mm(spec.mounting_depth)} beside the opening."
                )
            ball_probes = [
                side.point_at(distance + sign * spec.ball_width / 2, -(gap + inward))
                for sign in (-1, 1)
                for inward in (PROBE_INSET, spec.mounting_depth)
            ] + self._rim(side, catch.ball, base_radius)
            if not all(hatch_face.isPointOnFace(probe, TOLERANCE) for probe in ball_probes):
                raise _InputError(
                    f"The ball of catch {catch.number} does not fit on the "
                    f"hatch. It needs {_format_mm(spec.ball_width)} × "
                    f"{_format_mm(spec.mounting_depth)} beside the slot."
                )

    def _rim(
        self,
        side: _Side,
        center: adsk.core.Point3D,
        radius: float,
    ) -> list[adsk.core.Point3D]:
        return [
            edge_sketch.translated(center, direction, sign * radius)
            for direction in (side.along, side.outward)
            for sign in (-1, 1)
        ]

    def _native_edge(self, entity: adsk.core.Base) -> adsk.fusion.BRepEdge:
        edge = adsk.fusion.BRepEdge.cast(entity)
        if not edge:
            raise _InputError("The Opening Edge must be a body edge.")
        edge = cast(adsk.fusion.BRepEdge, edge.nativeObject or edge)
        if not utils.brep.is_linear(edge):
            raise _InputError("The Opening Edge must be a straight edge.")
        if not edge.body.isSolid:
            raise _InputError("The Opening Edge must belong to a solid body.")
        return edge

    def _native_point(
        self,
        entity: adsk.core.Base,
    ) -> tuple[adsk.core.Base, adsk.core.Point3D, adsk.fusion.Component]:
        """The point entity without assembly context, its position in its
        component's space, and that component."""
        vertex = adsk.fusion.BRepVertex.cast(entity)
        if vertex:
            vertex = cast(adsk.fusion.BRepVertex, vertex.nativeObject or vertex)
            return vertex, vertex.geometry, vertex.body.parentComponent
        sketch_point = adsk.fusion.SketchPoint.cast(entity)
        if sketch_point:
            sketch_point = cast(
                adsk.fusion.SketchPoint,
                sketch_point.nativeObject or sketch_point,
            )
            sketch = sketch_point.parentSketch
            return (
                sketch_point,
                sketch.sketchToModelSpace(sketch_point.geometry),
                sketch.parentComponent,
            )
        construction_point = adsk.fusion.ConstructionPoint.cast(entity)
        if construction_point:
            construction_point = cast(
                adsk.fusion.ConstructionPoint,
                construction_point.nativeObject or construction_point,
            )
            return (
                construction_point,
                construction_point.geometry,
                construction_point.component,
            )
        raise _InputError(
            "Custom Points must be vertices, sketch points or construction points."
        )

    # Features

    def execute(self):
        try:
            layout = self._layout()
        except _InputError as error:
            raise ValueError(str(error))
        spec = GN_450
        self._sketcher = edge_sketch.EdgeSketcher(
            self._set_parameter_expression,
            self._name_parameter,
        )
        design = cast(adsk.fusion.Design, self.app.activeProduct)
        hatch_token = layout.hatch_face.entityToken

        sketch, holder_points, ball_points = self._create_sketch(spec, layout)
        holder_holes = hole_features.create_simple_hole(
            layout.frame_face,
            sketch,
            holder_points,
            self._expression(self.inputs.pilot_diameter),
            self._expression(self.inputs.pilot_depth),
            f"{NAME} - Holder Pilot Holes",
        )
        # The balls drill like the holders: they follow the first hole
        # feature's parameters.
        depth = hole_features.depth_parameter(holder_holes)
        hatch_face = edge_sketch.find_by_token(
            design,
            hatch_token,
            adsk.fusion.BRepFace,
            "hatch face",
        )
        ball_holes = hole_features.create_simple_hole(
            hatch_face,
            sketch,
            ball_points,
            holder_holes.holeDiameter.name,
            depth.name if depth else self._expression(self.inputs.pilot_depth),
            f"{NAME} - Ball Pilot Holes",
        )
        if not self.group_features(sketch, ball_holes, NAME):
            raise RuntimeError(
                "Fusion created the catch holes but could not group them."
            )

    def _expression(self, value_input: inputs.FloatInput) -> str:
        return value_input.expression or _mm(value_input.value)

    def _create_sketch(
        self,
        spec: CatchSpec,
        layout: _Layout,
    ) -> tuple[
        adsk.fusion.Sketch,
        list[adsk.fusion.SketchPoint],
        list[adsk.fusion.SketchPoint],
    ]:
        """One sketch on the frame face holds every catch: its position on a
        projected contour edge and two construction lines perpendicular to
        that edge, out to the holder hole and in to the ball hole. Only the
        first catch is dimensioned; the others take its line lengths through
        equal constraints. The positions are spaced by the End Offset, or
        each follows its projected Custom Point."""
        component = layout.frame_face.body.parentComponent
        sketch = component.sketches.addWithoutEdges(layout.frame_face)
        if not sketch:
            raise RuntimeError(f"Fusion failed to create the {NAME} sketch.")
        sketch.name = f"{NAME} - Positions"
        contexts = [self._edge_context(sketch, side) for side in layout.sides]
        custom_points = [
            self._sketcher.project_point(
                sketch,
                cast(adsk.core.Base, catch.source),
                f"Custom Point {catch.number}",
            )
            if catch.source
            else None
            for side in layout.sides
            for catch in side.catches
        ]
        # Defer the sketch solve while the geometry is added; see
        # EdgeSketcher.create_sketch.
        sketch.isComputeDeferred = True
        lines = sketch.sketchCurves.sketchLines
        constraints = sketch.geometricConstraints

        def local(point: adsk.core.Point3D) -> adsk.core.Point3D:
            result = sketch.modelToSketchSpace(point)
            result.z = 0
            return result

        def construction_line(
            start: adsk.fusion.SketchPoint,
            end: adsk.core.Point3D,
        ) -> adsk.fusion.SketchLine:
            line = lines.addByTwoPoints(start, local(end))
            if not line:
                raise RuntimeError(f"Fusion failed to draw '{sketch.name}'.")
            line.isConstruction = True
            return line

        first_margin: adsk.fusion.SketchLinearDimension | None = None
        first_lines: tuple[adsk.fusion.SketchLine, adsk.fusion.SketchLine] | None = None
        holder_points: list[adsk.fusion.SketchPoint] = []
        ball_points: list[adsk.fusion.SketchPoint] = []
        expected: list[adsk.core.Point3D] = []
        custom_point_iterator = iter(custom_points)
        for side, context in zip(layout.sides, contexts):
            if self._is_number_positioning():
                stations, first_margin = self._add_spaced_stations(
                    context,
                    side,
                    layout.end_offset,
                    first_margin,
                )
            else:
                stations = self._add_stations(context, side)
            for catch, station in zip(side.catches, stations):
                holder_line = construction_line(station, catch.holder)
                constraints.addPerpendicular(holder_line, context.edge_line)
                ball_line = construction_line(station, catch.ball)
                constraints.addPerpendicular(ball_line, context.edge_line)
                custom_point = next(custom_point_iterator)
                if custom_point:
                    # The catch's perpendicular runs through its Custom Point
                    # (a point-on-line constraint includes the extension), so
                    # the catch follows the point along the contour and the
                    # contour across it.
                    constraints.addCoincident(custom_point, holder_line)
                if first_lines is None:
                    self._sketcher.add_distance_dimension(
                        sketch,
                        holder_line.startSketchPoint,
                        holder_line.endSketchPoint,
                        _mm(spec.holder_hole_outward),
                        "ballCatchHolderHole",
                    )
                    self._sketcher.add_distance_dimension(
                        sketch,
                        ball_line.startSketchPoint,
                        ball_line.endSketchPoint,
                        _mm(spec.ball_hole_inward),
                        "ballCatchBallHole",
                    )
                    first_lines = (holder_line, ball_line)
                else:
                    constraints.addEqual(first_lines[0], holder_line)
                    constraints.addEqual(first_lines[1], ball_line)
                holder_points.append(holder_line.endSketchPoint)
                ball_points.append(ball_line.endSketchPoint)
                expected.append(catch.holder)
                expected.append(catch.ball)

        self._sketcher.require_fully_constrained(sketch)
        self._verify_points(
            sketch,
            [point for pair in zip(holder_points, ball_points) for point in pair],
            expected,
        )
        return sketch, holder_points, ball_points

    def _edge_context(
        self,
        sketch: adsk.fusion.Sketch,
        side: _Side,
    ) -> edge_sketch.SketchContext:
        edge_line = self._sketcher.project_reference_line(
            sketch,
            side.edge,
            side.label,
        )
        start_vertex = side.edge.startVertex.geometry
        edge_start = min(
            (edge_line.startSketchPoint, edge_line.endSketchPoint),
            key=lambda point: sketch.sketchToModelSpace(point.geometry).distanceTo(
                start_vertex
            ),
        )
        edge_end = (
            edge_line.endSketchPoint
            if edge_start == edge_line.startSketchPoint
            else edge_line.startSketchPoint
        )
        return edge_sketch.SketchContext(
            sketch=sketch,
            edge_line=edge_line,
            edge_start=edge_start,
            edge_end=edge_end,
            parameter_role="ballCatch",
        )

    def _add_spaced_stations(
        self,
        context: edge_sketch.SketchContext,
        side: _Side,
        end_offset: tuple[float, str] | None,
        first_margin: adsk.fusion.SketchLinearDimension | None,
    ) -> tuple[list[adsk.fusion.SketchPoint], adsk.fusion.SketchLinearDimension | None]:
        """The catch positions on one projected edge: a single one at its
        midpoint, more from End Offset to End Offset with equal spacing.
        Every End Offset dimension follows the first one.

        Only the first position is put on the edge; the others follow it
        along spacing lines parallel to the edge. Putting every position on
        the edge solves the same, but with equal spacing chains on two edges
        the constraint analyzer reports the middle positions of the second
        edge as free (2026-10-07)."""
        sketch = context.sketch
        constraints = sketch.geometricConstraints
        if len(side.catches) == 1:
            stations = self._add_stations(context, side)
            constraints.addMidPoint(stations[0], context.edge_line)
            return stations, first_margin

        if end_offset is None:
            raise RuntimeError("Spaced catches need an End Offset.")
        stations: list[adsk.fusion.SketchPoint] = []
        for catch in side.catches:
            local = sketch.modelToSketchSpace(catch.station)
            local.z = 0
            station = sketch.sketchPoints.add(local)
            if not station:
                raise RuntimeError(f"Fusion failed to draw '{sketch.name}'.")
            stations.append(station)
        constraints.addCoincident(stations[0], context.edge_line)
        first = self._sketcher.add_distance_dimension(
            sketch,
            context.edge_start,
            stations[0],
            first_margin.parameter.name if first_margin else end_offset[1],
            "ballCatchEndOffset",
        )
        first_margin = first_margin or first
        self._sketcher.add_distance_dimension(
            sketch,
            stations[-1],
            context.edge_end,
            first_margin.parameter.name,
            "ballCatchEndOffset",
        )
        spacing_lines: list[adsk.fusion.SketchLine] = []
        for start, end in zip(stations, stations[1:]):
            spacing_line = sketch.sketchCurves.sketchLines.addByTwoPoints(start, end)
            if not spacing_line:
                raise RuntimeError(f"Fusion failed to draw '{sketch.name}'.")
            spacing_line.isConstruction = True
            constraints.addParallel(spacing_line, context.edge_line)
            spacing_lines.append(spacing_line)
        for spacing_line in spacing_lines[1:]:
            constraints.addEqual(spacing_lines[0], spacing_line)
        return stations, first_margin

    def _add_stations(
        self,
        context: edge_sketch.SketchContext,
        side: _Side,
    ) -> list[adsk.fusion.SketchPoint]:
        """A point on the projected edge for each catch of the side, free to
        slide along it."""
        sketch = context.sketch
        stations: list[adsk.fusion.SketchPoint] = []
        for catch in side.catches:
            local = sketch.modelToSketchSpace(catch.station)
            local.z = 0
            station = sketch.sketchPoints.add(local)
            if not station:
                raise RuntimeError(f"Fusion failed to draw '{sketch.name}'.")
            sketch.geometricConstraints.addCoincident(station, context.edge_line)
            stations.append(station)
        return stations

    def _verify_points(
        self,
        sketch: adsk.fusion.Sketch,
        points: list[adsk.fusion.SketchPoint],
        expected: list[adsk.core.Point3D],
    ) -> None:
        """Guards the constraint setup: the solved sketch must reproduce
        the analytic hole positions."""
        tolerance = max(self.app.pointTolerance * 100, 1e-5)
        for point, target in zip(points, expected):
            error = sketch.sketchToModelSpace(point.geometry).distanceTo(target)
            if error > tolerance:
                raise RuntimeError(
                    f"'{sketch.name}' differs from the computed catch "
                    f"position by {error:.6g} cm."
                )

    # Parameters

    def _set_parameter_expression(
        self,
        parameter: adsk.fusion.ModelParameter,
        expression: str,
    ) -> None:
        """Writes only expressions that carry a parametric link (the later
        End Offsets, or an End Offset given as a user parameter). Every
        dimension is created on geometry already at its value, so writing a
        literal would only change the displayed text, at the cost of a
        document update (see Addin._expression_references_parameter)."""
        if self._expression_references_parameter(expression):
            parameter.expression = expression

    def _name_parameter(
        self,
        parameter: adsk.fusion.ModelParameter,
        role: str,
    ) -> None:
        """Parameters keep Fusion's names (see AGENTS.md): every value here
        is edited through the dialog (group edit), and every cross-reference
        reads `parameter.name` live."""
        return
