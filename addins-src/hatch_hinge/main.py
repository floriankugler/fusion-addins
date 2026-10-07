import os
from dataclasses import dataclass
from typing import cast

import adsk.core
import adsk.fusion

from lib import addin, edge_sketch, hole_features, inputs, ui_placement, utils
from lib.fusionbootstrap.runtime import RuntimeInfo


_addin: addin.Addin | None = None

# Geometric tolerance for the placement checks, in cm.
TOLERANCE = 1e-4
# How far in front of the carcass the closed hatch may be modelled, in cm.
# The hinges' depth adjustment takes up a small gap.
MAX_HATCH_GAP = 0.2


def _mm(value_cm: float) -> str:
    """Derive a millimeter expression string from a centimeter value so the
    sketch dimensions can never drift from the analytic placement math."""
    return f"{value_cm * 10:g} mm"


def _format_mm(value_cm: float) -> str:
    return f"{value_cm * 10:.1f}".rstrip("0").rstrip(".") + " mm"


@dataclass(frozen=True)
class HingeSpec:
    """Drilling data of a lift-up hatch hinge, in cm.

    Everything is measured from the hinge reference: the level of the
    underside of the carcass top, where it meets the inner front edge of
    the side panel (the manufacturer's drilling template is pushed up
    against the underside of the top). "Below" runs down from that level,
    "back" into the carcass from its front edge, and "inward" into the
    cabinet from the side panel's inner face.
    """

    name: str
    carcass_hole_diameter: float
    carcass_hole_back: float
    carcass_first_hole_below: float
    carcass_hole_pitch: float
    carcass_hole_count: int
    hatch_hole_inward: float
    hatch_first_hole_below: float
    hatch_hole_pitch: float
    hatch_hole_count: int
    #: (hatch thickness, overlap) pairs, ascending: how far the hatch top
    #: may reach above the hinge reference before the hatch hits the
    #: carcass while opening fully. Interpolated linearly in between; the
    #: thickness range is the supported one.
    max_overlap: tuple[tuple[float, float], ...]
    #: The same limit with the opening limited to 90 degrees.
    limited_max_overlap: float
    #: Footprint of the mounting plate on the hatch (inward range, below
    #: range). It must lie on the hatch.
    plate_inward: tuple[float, float]
    plate_below: tuple[float, float]
    #: Points inside the closed hinge (inward, back, below). No other body
    #: may contain them.
    probe_points: tuple[tuple[float, float, float], ...]

    @property
    def min_hatch_thickness(self) -> float:
        return self.max_overlap[0][0]

    @property
    def max_hatch_thickness(self) -> float:
        return self.max_overlap[-1][0]

    def overlap_limit(self, hatch_thickness: float, limited: bool) -> float:
        if limited:
            return self.limited_max_overlap
        table = self.max_overlap
        if hatch_thickness <= table[0][0]:
            return table[0][1]
        for (thickness0, overlap0), (thickness1, overlap1) in zip(
            table,
            table[1:],
        ):
            if hatch_thickness <= thickness1:
                fraction = (hatch_thickness - thickness0) / (
                    thickness1 - thickness0
                )
                return overlap0 + (overlap1 - overlap0) * fraction
        return table[-1][1]


# Häfele Free space 1.11 (372.27.xxx, every spring strength drills the
# same), from the installation manual, checked against Häfele's STEP model
# (372.27.300): closed, the hinge stops 1.8 mm below the carcass top, its
# plate slots sit 90 and 26 mm above the top carcass hole, and at 90 degrees
# the hatch clears the carcass front up to a 38 mm overlap. The STEP centres
# the plate 24.15 mm from the side panel; the manual's 25 mm is used, the
# hinge's +-1.5 mm side adjustment covers the difference. Plate footprint
# and probe points come from the STEP model.
FREE_SPACE_1_11 = HingeSpec(
    name="Häfele Free space 1.11",
    carcass_hole_diameter=0.5,
    carcass_hole_back=3.7,
    carcass_first_hole_below=10.2,
    carcass_hole_pitch=3.2,
    carcass_hole_count=3,
    hatch_hole_inward=2.5,
    hatch_first_hole_below=1.2,
    hatch_hole_pitch=6.4,
    hatch_hole_count=2,
    max_overlap=(
        (1.6, 2.45),
        (1.8, 2.4),
        (1.9, 2.35),
        (2.2, 2.25),
        (2.4, 2.2),
        (2.6, 2.15),
        (2.8, 2.1),
    ),
    limited_max_overlap=3.7,
    plate_inward=(1.55, 3.45),
    plate_below=(0.5, 8.3),
    probe_points=(
        (1.6, 3.7, 0.3),
        (2.5, 0.1, 0.3),
        (1.3, 2.5, 0.6),
        (1.2, 2.5, 4.2),
        (1.2, 2.5, 8.2),
        (1.2, 2.5, 15.2),
        (3.0, 0.3, 6.2),
    ),
)


def run(context, runtime_info: RuntimeInfo):
    global _addin
    _addin = HatchHinge(runtime_info)
    # Dev support: allow external tooling to restart this add-in by firing the
    # custom event '<id>_reload' (see lib/fusionbootstrap/reloader.py).
    from lib.fusionbootstrap import reloader
    entry = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "hatch_hinge.py",
    )
    reloader.ensure(runtime_info.id + "_reload", entry)


def stop(context):
    global _addin
    if _addin:
        _addin.shutdown()
    _addin = None


class HatchHingeInputs(inputs.Inputs):
    class Types:
        FREE_SPACE_1_11 = inputs.DropDownInput.Item(FREE_SPACE_1_11.name, 0)

    class Openings:
        FULL = inputs.DropDownInput.Item("107° (full)", 0)
        LIMITED = inputs.DropDownInput.Item("90° (limiter)", 1)

    def __init__(self, units_manager: adsk.core.UnitsManager):
        units = units_manager.defaultLengthUnits
        self.hatch_edge = inputs.SelectionByEntityTokenInput(
            id="hatch_edge",
            name="Hatch Top Edge",
            filter=["LinearEdges"],
            lower_bound=1,
            upper_bound=1,
            tool_tip=(
                "Select the top edge of the hatch's inner face. The hatch "
                "must be modelled in its closed position."
            ),
        )
        self.carcass_edges = inputs.SelectionByEntityTokenInput(
            id="carcass_edges",
            name="Carcass Front Edges",
            filter=["LinearEdges"],
            lower_bound=1,
            upper_bound=2,
            tool_tip=(
                "Select the inner front edge of the side panel that carries "
                "a hinge, or of both side panels."
            ),
        )
        self.top_reference = inputs.SelectionByEntityTokenInput(
            id="top_reference",
            name="Top Reference",
            filter=["Vertices", "SketchPoints", "ConstructionPoints"],
            lower_bound=0,
            upper_bound=1,
            tool_tip=(
                "Optional point at the level of the underside of the carcass "
                "top, which the hinges are positioned from. Without it the "
                "top end of each Carcass Front Edge is used, which is right "
                "when the top sits on the side panels."
            ),
        )
        self.type = inputs.DropDownInput(
            id="type",
            name="Hinge Type",
            options=utils.misc.class_property_values(
                HatchHingeInputs.Types,
                inputs.DropDownInput.Item,
            ),
            default_value=HatchHingeInputs.Types.FREE_SPACE_1_11.value,
            tool_tip="The hinge whose drilling pattern is created.",
        )
        self.opening = inputs.DropDownInput(
            id="opening",
            name="Opening Angle",
            options=utils.misc.class_property_values(
                HatchHingeInputs.Openings,
                inputs.DropDownInput.Item,
            ),
            default_value=HatchHingeInputs.Openings.FULL.value,
            tool_tip=(
                "The opening angle the hinges are set to. It only decides "
                "how far the hatch may reach above the underside of the "
                "carcass top."
            ),
        )
        self.carcass_depth = inputs.FloatInput(
            id="carcass_depth",
            name="Carcass Hole Depth",
            default_value=1.2,
            tool_tip="Depth of the 5 mm holes in the side panels.",
            units=units,
        )
        self.carcass_depth.minimum_value = 0.01
        self.pilot_diameter = inputs.FloatInput(
            id="pilot_diameter",
            name="Hatch Pilot Diameter",
            default_value=0.2,
            tool_tip="Diameter of the pilot holes for the mounting plate screws.",
            units=units,
        )
        self.pilot_diameter.minimum_value = 0.01
        self.pilot_depth = inputs.FloatInput(
            id="pilot_depth",
            name="Hatch Pilot Depth",
            default_value=0.4,
            tool_tip="Depth of the pilot holes in the hatch.",
            units=units,
        )
        self.pilot_depth.minimum_value = 0.01
        super().__init__()


class _InputError(Exception):
    """A selection or value the hinge cannot be placed with; the message is
    shown in the dialog."""


@dataclass
class _HingeSide:
    """One hinge: the side panel it mounts on and its hole positions."""

    edge: adsk.fusion.BRepEdge
    face: adsk.fusion.BRepFace
    #: Projected into the sketches as the level of the hinge reference.
    reference: adsk.core.Base
    is_left: bool
    inward: adsk.core.Vector3D
    back: adsk.core.Vector3D
    #: The inner front edge at the reference level.
    front_point: adsk.core.Point3D
    #: The reference level on the carcass hole column.
    corner: adsk.core.Point3D
    carcass_holes: list[adsk.core.Point3D]
    #: The reference level on the hatch hole column.
    hatch_column: adsk.core.Point3D
    hatch_holes: list[adsk.core.Point3D]
    #: How far the hatch top reaches above the reference.
    overlap: float


@dataclass
class _Layout:
    hatch_face: adsk.fusion.BRepFace
    up: adsk.core.Vector3D
    #: The carcass sketch lies on the first side's panel.
    sides: list[_HingeSide]


class HatchHinge(addin.Addin):
    inputs: HatchHingeInputs

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
        return "Hatch Hinge"

    @property
    def plugin_desc(self) -> str:
        return "Create the drilling for lift-up hatch hinges with native Fusion features."

    @property
    def plugin_tooltip(self) -> str:
        return (
            "Creates the holes for the hinges of a lift-up hatch in the hatch "
            "and the carcass side panels, from fully constrained sketches."
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

    def create_inputs(self) -> HatchHingeInputs:
        design = adsk.fusion.Design.cast(self.app.activeProduct)
        if not design:
            raise RuntimeError("Hatch Hinge requires an active Fusion design.")
        return HatchHingeInputs(design.unitsManager)

    def pre_select(self, input, selection) -> bool:
        if not self.inputs or not input:
            return True
        if input.id in {
            self.inputs.hatch_edge.id,
            self.inputs.carcass_edges.id,
        }:
            edge = adsk.fusion.BRepEdge.cast(selection)
            return bool(
                edge
                and edge.body
                and edge.body.isSolid
                and utils.brep.is_linear(edge)
                and utils.brep.largest_face_of_edge(edge)
            )
        if input.id == self.inputs.top_reference.id:
            return bool(
                adsk.fusion.BRepVertex.cast(selection)
                or adsk.fusion.SketchPoint.cast(selection)
                or adsk.fusion.ConstructionPoint.cast(selection)
            )
        return True

    def _validate(self, args: adsk.core.ValidateInputsEventArgs):
        self._apply_validation(args, self._validation_error)

    def _validation_error(self) -> str | None:
        try:
            self._layout()
        except _InputError as error:
            return str(error)
        return None

    def _spec(self) -> HingeSpec:
        if self.inputs.type.value != HatchHingeInputs.Types.FREE_SPACE_1_11.value:
            raise _InputError("Unsupported hinge type.")
        return FREE_SPACE_1_11

    # Placement

    def _layout(self) -> _Layout:
        """Resolves the selections and computes every hole position.
        Raises _InputError when the hinges cannot be placed."""
        design = adsk.fusion.Design.cast(self.app.activeProduct)
        if not design:
            raise _InputError("An active Fusion design is required.")
        if design.designType != adsk.fusion.DesignTypes.ParametricDesignType:  # type: ignore
            raise _InputError(
                "Hatch Hinge requires Design History (a parametric design)."
            )
        if not self.inputs or len(self.inputs.hatch_edge.value) != 1:
            raise _InputError("Select the Hatch Top Edge.")
        if not 1 <= len(self.inputs.carcass_edges.value) <= 2:
            raise _InputError("Select one or two Carcass Front Edges.")
        if len(self.inputs.top_reference.value) > 1:
            raise _InputError("Select at most one Top Reference point.")
        spec = self._spec()
        self._check_values()

        hatch_edge = self._native_edge(
            self.inputs.hatch_edge.value[0],
            "Hatch Top Edge",
        )
        carcass_edges = [
            self._native_edge(edge, "Carcass Front Edge")
            for edge in self.inputs.carcass_edges.value
        ]
        reference = (
            self._native_point(self.inputs.top_reference.value[0])
            if self.inputs.top_reference.value
            else None
        )

        component = design.activeComponent
        owners = [hatch_edge.body.parentComponent] + [
            edge.body.parentComponent for edge in carcass_edges
        ]
        if reference:
            owners.append(reference[2])
        if any(owner != component for owner in owners):
            raise _InputError(
                "The hatch, the side panels and the Top Reference must "
                "belong to the active component. Activate the component "
                "that owns them, then run Hatch Hinge again."
            )
        carcass_bodies = [edge.body for edge in carcass_edges]
        if hatch_edge.body in carcass_bodies:
            raise _InputError(
                "The Hatch Top Edge and the Carcass Front Edges must belong "
                "to different bodies."
            )
        if len(carcass_bodies) == 2 and carcass_bodies[0] == carcass_bodies[1]:
            raise _InputError(
                "Select the two Carcass Front Edges on different side panels."
            )

        hatch_face = self._board_face(hatch_edge, "Hatch Top Edge")
        hatch_thickness = utils.brep.get_board_thickness(hatch_face)
        if not (
            spec.min_hatch_thickness - TOLERANCE
            <= hatch_thickness
            <= spec.max_hatch_thickness + TOLERANCE
        ):
            raise _InputError(
                f"The hatch is {_format_mm(hatch_thickness)} thick; the "
                f"{spec.name} fits hatches from "
                f"{_format_mm(spec.min_hatch_thickness)} to "
                f"{_format_mm(spec.max_hatch_thickness)}."
            )
        up = utils.vector.scaled_by(
            utils.brep.normal_into_face(hatch_edge, hatch_face),
            -1,
        )
        hatch_point = hatch_edge.startVertex.geometry
        towards_carcass = utils.brep.normal_away_from_body(hatch_face)
        hatch_center = hatch_face.centroid

        sides = [
            self._hinge_side(
                spec,
                edge,
                reference,
                up,
                hatch_point,
                towards_carcass,
                hatch_center,
                hatch_thickness,
            )
            for edge in carcass_edges
        ]
        if len(sides) == 2:
            first, second = sides
            facing = utils.vector.subtract(
                second.front_point.asVector(),
                first.front_point.asVector(),
            )
            if not (
                utils.vector.is_parallel_direction(first.inward, second.inward)
                and first.inward.dotProduct(second.inward) < 0
                and first.inward.dotProduct(facing) > 0
            ):
                raise _InputError(
                    "The two Carcass Front Edges must be on opposite side "
                    "panels of the cabinet."
                )
            # One sketch drills both panels, so their hinge references must
            # line up across the cabinet.
            height = abs(up.dotProduct(facing))
            if height > TOLERANCE:
                raise _InputError(
                    "The hinge references of the two side panels differ by "
                    f"{_format_mm(height)} in height. Select a Top Reference "
                    "point at the underside of the carcass top."
                )
            depth = abs(first.back.dotProduct(facing))
            if depth > TOLERANCE:
                raise _InputError(
                    "The front edges of the two side panels are "
                    f"{_format_mm(depth)} apart in depth; both panels are "
                    "drilled from one sketch and need flush front edges."
                )

        limited = self.inputs.opening.value == HatchHingeInputs.Openings.LIMITED.value
        limit = spec.overlap_limit(hatch_thickness, limited)
        overlap = max(side.overlap for side in sides)
        if overlap > limit + TOLERANCE:
            hint = (
                ""
                if limited
                else (
                    f" ({_format_mm(spec.limited_max_overlap)} with the "
                    "opening limited to 90°)"
                )
            )
            raise _InputError(
                f"The hatch top reaches {_format_mm(overlap)} above the "
                f"underside of the carcass top. The {spec.name} allows at "
                f"most {_format_mm(limit)} for a "
                f"{_format_mm(hatch_thickness)} hatch{hint}."
            )

        carcass_radius = spec.carcass_hole_diameter / 2
        pilot_radius = self.inputs.pilot_diameter.value / 2
        for side in sides:
            if not self._points_on_face(
                side.face,
                side.carcass_holes,
                carcass_radius,
                up,
                side.back,
            ):
                raise _InputError(
                    "The carcass holes do not fit on the side panel's inner "
                    "face."
                )
            plate = [
                self._hatch_point(side, up, inward - spec.hatch_hole_inward, below)
                for inward in spec.plate_inward
                for below in spec.plate_below
            ]
            if not self._points_on_face(hatch_face, plate, 0, up, side.inward):
                raise _InputError(
                    "The hinge's mounting plate does not fit on the hatch. "
                    "It covers "
                    f"{_format_mm(spec.plate_below[0])} to "
                    f"{_format_mm(spec.plate_below[1])} below the underside "
                    "of the carcass top."
                )
            if not self._points_on_face(
                hatch_face,
                side.hatch_holes,
                pilot_radius,
                up,
                side.inward,
            ):
                raise _InputError("The pilot holes do not fit on the hatch.")
            side_thickness = utils.brep.get_board_thickness(side.face)
            if self.inputs.carcass_depth.value >= side_thickness - TOLERANCE:
                raise _InputError(
                    "Carcass Hole Depth must be less than the side panel "
                    f"thickness ({_format_mm(side_thickness)})."
                )
            obstacle = self._hinge_space_obstacle(component, side, up, spec)
            if obstacle:
                raise _InputError(
                    f"The hinge would collide with '{obstacle}'. The hinges "
                    "are positioned from the underside of the carcass top: "
                    "when the side panels run up past the top, select a "
                    "point on the top's underside as Top Reference."
                )
        if self.inputs.pilot_depth.value >= hatch_thickness - TOLERANCE:
            raise _InputError(
                "Hatch Pilot Depth must be less than the hatch thickness "
                f"({_format_mm(hatch_thickness)})."
            )
        return _Layout(hatch_face=hatch_face, up=up, sides=sides)

    def _check_values(self) -> None:
        if self.inputs.carcass_depth.value <= 0:
            raise _InputError("Carcass Hole Depth must be greater than zero.")
        if self.inputs.pilot_diameter.value <= 0:
            raise _InputError("Hatch Pilot Diameter must be greater than zero.")
        if self.inputs.pilot_depth.value <= 0:
            raise _InputError("Hatch Pilot Depth must be greater than zero.")

    def _hinge_side(
        self,
        spec: HingeSpec,
        edge: adsk.fusion.BRepEdge,
        reference: tuple[adsk.core.Base, adsk.core.Point3D, adsk.fusion.Component] | None,
        up: adsk.core.Vector3D,
        hatch_point: adsk.core.Point3D,
        towards_carcass: adsk.core.Vector3D,
        hatch_center: adsk.core.Point3D,
        hatch_thickness: float,
    ) -> _HingeSide:
        face = self._board_face(edge, "Carcass Front Edge")
        if not utils.brep.is_parallel(edge, up):
            raise _InputError(
                "Each Carcass Front Edge must run vertically: parallel to "
                "the hatch and perpendicular to the Hatch Top Edge."
            )
        edge_point = edge.startVertex.geometry
        # From the hatch's inner face back to the carcass front.
        gap = towards_carcass.dotProduct(
            utils.vector.subtract(edge_point.asVector(), hatch_point.asVector())
        )
        if gap < -hatch_thickness / 2:
            raise _InputError(
                "Select the top edge of the hatch's inner face, the face "
                "towards the carcass."
            )
        back = utils.brep.normal_into_face(edge, face)
        if not utils.vector.is_parallel_direction(back, towards_carcass):
            raise _InputError("The side panels must be perpendicular to the hatch.")
        if back.dotProduct(towards_carcass) < 0:
            raise _InputError(
                "Select the front edge of the side panel, the one behind "
                "the hatch."
            )
        if gap < -TOLERANCE:
            raise _InputError(
                f"The hatch reaches {_format_mm(-gap)} into the carcass. "
                "Model the closed hatch in front of the carcass."
            )
        if gap > MAX_HATCH_GAP + TOLERANCE:
            raise _InputError(
                "The hatch must be modelled in its closed position, against "
                f"the carcass front (it is {_format_mm(gap)} in front of it)."
            )
        inward = utils.brep.normal_away_from_body(face)
        if inward.dotProduct(
            utils.vector.subtract(hatch_center.asVector(), edge_point.asVector())
        ) <= 0:
            raise _InputError(
                "Select the inner front edge of the side panel, on the face "
                "towards the inside of the cabinet."
            )

        if reference:
            reference_entity, reference_point, _ = reference
        else:
            top_vertex = max(
                (edge.startVertex, edge.endVertex),
                key=lambda vertex: up.dotProduct(vertex.geometry.asVector()),
            )
            reference_entity = top_vertex
            reference_point = top_vertex.geometry
        level = up.dotProduct(
            utils.vector.subtract(
                reference_point.asVector(),
                edge_point.asVector(),
            )
        )
        front_point = utils.vector.add(
            edge_point.asVector(),
            utils.vector.scaled_by(up, level),
        ).asPoint()
        corner = utils.vector.add(
            front_point.asVector(),
            utils.vector.scaled_by(back, spec.carcass_hole_back),
        ).asPoint()
        carcass_holes = [
            utils.vector.subtract(
                corner.asVector(),
                utils.vector.scaled_by(
                    up,
                    spec.carcass_first_hole_below
                    + index * spec.carcass_hole_pitch,
                ),
            ).asPoint()
            for index in range(spec.carcass_hole_count)
        ]
        hatch_column = utils.vector.add(
            utils.vector.subtract(
                front_point.asVector(),
                utils.vector.scaled_by(back, gap),
            ),
            utils.vector.scaled_by(inward, spec.hatch_hole_inward),
        ).asPoint()
        # Seen from the front (looking along `back`), the left side panel's
        # inner face points to the right.
        right = back.crossProduct(up)
        overlap = up.dotProduct(
            utils.vector.subtract(
                hatch_point.asVector(),
                reference_point.asVector(),
            )
        )
        side = _HingeSide(
            edge=edge,
            face=face,
            reference=reference_entity,
            is_left=inward.dotProduct(right) > 0,
            inward=inward,
            back=back,
            front_point=front_point,
            corner=corner,
            carcass_holes=carcass_holes,
            hatch_column=hatch_column,
            hatch_holes=[],
            overlap=overlap,
        )
        side.hatch_holes = [
            self._hatch_point(
                side,
                up,
                0,
                spec.hatch_first_hole_below + index * spec.hatch_hole_pitch,
            )
            for index in range(spec.hatch_hole_count)
        ]
        return side

    def _hatch_point(
        self,
        side: _HingeSide,
        up: adsk.core.Vector3D,
        inward: float,
        below: float,
    ) -> adsk.core.Point3D:
        """A point on the hatch's inner face, relative to the hatch hole
        column at the reference level."""
        point = side.hatch_column.asVector()
        point.add(utils.vector.scaled_by(side.inward, inward))
        point.subtract(utils.vector.scaled_by(up, below))
        return point.asPoint()

    def _hinge_point(
        self,
        side: _HingeSide,
        up: adsk.core.Vector3D,
        inward: float,
        back: float,
        below: float,
    ) -> adsk.core.Point3D:
        point = side.front_point.asVector()
        point.add(utils.vector.scaled_by(side.inward, inward))
        point.add(utils.vector.scaled_by(side.back, back))
        point.subtract(utils.vector.scaled_by(up, below))
        return point.asPoint()

    def _hinge_space_obstacle(
        self,
        component: adsk.fusion.Component,
        side: _HingeSide,
        up: adsk.core.Vector3D,
        spec: HingeSpec,
    ) -> str | None:
        """Name of a visible body of the component that occupies the closed
        hinge's space. Catches a hinge reference set too high, e.g. the top
        of side panels that run up past the carcass top. Bodies of child
        occurrences are not checked."""
        points = [
            self._hinge_point(side, up, inward, back, below)
            for inward, back, below in spec.probe_points
        ]
        inside = adsk.fusion.PointContainment.PointInsidePointContainment
        for body in component.bRepBodies:
            if not body.isSolid or not body.isVisible:
                continue
            box = body.boundingBox
            for point in points:
                if box.contains(point) and body.pointContainment(point) == inside:
                    return body.name
        return None

    def _points_on_face(
        self,
        face: adsk.fusion.BRepFace,
        centers: list[adsk.core.Point3D],
        radius: float,
        first_direction: adsk.core.Vector3D,
        second_direction: adsk.core.Vector3D,
    ) -> bool:
        """True when every center, and its rim in both directions when
        `radius` is set, lies on the face."""
        offsets = [(0.0, 0.0)]
        if radius > 0:
            offsets += [
                (radius, 0.0),
                (-radius, 0.0),
                (0.0, radius),
                (0.0, -radius),
            ]
        for center in centers:
            for first, second in offsets:
                point = center.asVector()
                point.add(utils.vector.scaled_by(first_direction, first))
                point.add(utils.vector.scaled_by(second_direction, second))
                if not face.isPointOnFace(point.asPoint(), TOLERANCE):
                    return False
        return True

    def _native_edge(
        self,
        entity: adsk.core.Base,
        description: str,
    ) -> adsk.fusion.BRepEdge:
        edge = adsk.fusion.BRepEdge.cast(entity)
        if not edge:
            raise _InputError(f"The {description} must be a body edge.")
        edge = cast(adsk.fusion.BRepEdge, edge.nativeObject or edge)
        if not utils.brep.is_linear(edge):
            raise _InputError(f"The {description} must be a straight edge.")
        if not edge.body.isSolid:
            raise _InputError(f"The {description} must belong to a solid body.")
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
            "The Top Reference must be a vertex, sketch point or "
            "construction point."
        )

    def _board_face(
        self,
        edge: adsk.fusion.BRepEdge,
        description: str,
    ) -> adsk.fusion.BRepFace:
        face = utils.brep.largest_face_of_edge(edge)
        if not face:
            raise _InputError(
                f"The {description} must border a planar board face."
            )
        try:
            utils.brep.get_opposite_face(face)
        except ValueError:
            raise _InputError(
                f"The board of the {description} must have two parallel "
                "faces."
            )
        return face

    # Features

    def execute(self):
        try:
            layout = self._layout()
        except _InputError as error:
            raise ValueError(str(error))
        spec = self._spec()
        self._sketcher = edge_sketch.EdgeSketcher(
            self._set_parameter_expression,
            self._name_parameter,
        )

        carcass_sketch, corner = self._create_carcass_sketch(spec, layout)
        # One sketch drills both side panels: the first cut starts at the
        # sketch's own face, the other one at the opposite panel's inner
        # face, as deep as the first.
        depth = self.inputs.carcass_depth.expression
        for index, side in enumerate(layout.sides):
            cut = self._sketcher.create_cut_extrude(
                side.face.body.parentComponent,
                carcass_sketch,
                side.face.body,
                utils.vector.scaled_by(side.inward, -1),
                depth,
                f"Hatch Hinge - {self._side_name(side)} Carcass Holes",
                "carcassHoleDepth",
                start_face=side.face if index > 0 else None,
            )
            extent = adsk.fusion.DistanceExtentDefinition.cast(cut.extentOne)
            if not extent or not extent.distance:
                raise RuntimeError(f"'{cut.name}' has no depth parameter.")
            # The distance parameter is signed by the cut's direction, which
            # differs between the two panels.
            depth = f"abs({extent.distance.name})"

        hatch_sketch, hatch_points = self._create_hatch_sketch(
            spec,
            layout,
            corner,
        )
        hatch_holes = hole_features.create_simple_hole(
            layout.hatch_face,
            hatch_sketch,
            hatch_points,
            self.inputs.pilot_diameter.expression,
            self.inputs.pilot_depth.expression,
            "Hatch Hinge - Hatch Pilot Holes",
        )
        if not self.group_features(carcass_sketch, hatch_holes, "Hatch Hinge"):
            raise RuntimeError(
                "Fusion created the hinge features but could not group them."
            )

    def _side_name(self, side: _HingeSide) -> str:
        return "Left" if side.is_left else "Right"

    def _create_carcass_sketch(
        self,
        spec: HingeSpec,
        layout: _Layout,
    ) -> tuple[adsk.fusion.Sketch, adsk.fusion.SketchPoint]:
        """The hole circles on the first side panel's inner face: a column
        `back` behind the front edge, the holes below the hinge reference.
        The other side panel is cut with the same circles. Returns the
        sketch and the reference corner on the hole column."""
        side = layout.sides[0]
        component = side.face.body.parentComponent
        sketch = component.sketches.addWithoutEdges(side.face)
        if not sketch:
            raise RuntimeError("Fusion failed to create the carcass hinge sketch.")
        sketch.name = "Hatch Hinge - Carcass Positions"
        sketcher = self._sketcher
        edge_line = sketcher.project_reference_line(
            sketch,
            side.edge,
            "carcass front edge",
        )
        reference = sketcher.project_point(
            sketch,
            side.reference,
            "Top Reference",
        )
        # Defer the sketch solve while the geometry is added; see
        # EdgeSketcher.create_sketch.
        sketch.isComputeDeferred = True
        lines = sketch.sketchCurves.sketchLines
        constraints = sketch.geometricConstraints

        front = reference
        front_target = self._sketch_point(sketch, side.front_point)
        if reference.geometry.distanceTo(front_target) > TOLERANCE:
            # The reference lies off the front edge: carry its level over.
            level_line = lines.addByTwoPoints(reference, front_target)
            level_line.isConstruction = True
            constraints.addPerpendicular(level_line, edge_line)
            constraints.addCoincident(level_line.endSketchPoint, edge_line)
            front = level_line.endSketchPoint

        back_line = lines.addByTwoPoints(
            front,
            self._sketch_point(sketch, side.corner),
        )
        back_line.isConstruction = True
        constraints.addPerpendicular(back_line, edge_line)
        column = lines.addByTwoPoints(
            back_line.endSketchPoint,
            self._sketch_point(sketch, side.carcass_holes[0]),
        )
        column.isConstruction = True
        constraints.addParallel(column, edge_line)
        sketcher.add_distance_dimension(
            sketch,
            back_line.startSketchPoint,
            back_line.endSketchPoint,
            _mm(spec.carcass_hole_back),
            "carcassHoleBack",
        )
        sketcher.add_distance_dimension(
            sketch,
            column.startSketchPoint,
            column.endSketchPoint,
            _mm(spec.carcass_first_hole_below),
            "carcassFirstHoleBelow",
        )
        points = [column.endSketchPoint]
        pitch_lines: list[adsk.fusion.SketchLine] = []
        for hole in side.carcass_holes[1:]:
            pitch_line = lines.addByTwoPoints(
                points[-1],
                self._sketch_point(sketch, hole),
            )
            pitch_line.isConstruction = True
            constraints.addParallel(pitch_line, column)
            if pitch_lines:
                constraints.addEqual(pitch_lines[0], pitch_line)
            else:
                sketcher.add_distance_dimension(
                    sketch,
                    pitch_line.startSketchPoint,
                    pitch_line.endSketchPoint,
                    _mm(spec.carcass_hole_pitch),
                    "carcassHolePitch",
                )
            pitch_lines.append(pitch_line)
            points.append(pitch_line.endSketchPoint)

        radius = spec.carcass_hole_diameter / 2
        circles = [
            sketch.sketchCurves.sketchCircles.addByCenterRadius(point, radius)
            for point in points
        ]
        if not all(circles):
            raise RuntimeError("Fusion failed to create the carcass hole circles.")
        text_point = points[0].geometry.copy()
        text_point.x += radius * 2
        text_point.y += radius * 2
        diameter = sketch.sketchDimensions.addDiameterDimension(
            circles[0],
            text_point,
        )
        if not diameter or not diameter.parameter:
            raise RuntimeError("Fusion failed to dimension the carcass holes.")
        self._set_parameter_expression(
            diameter.parameter,
            _mm(spec.carcass_hole_diameter),
        )
        self._name_parameter(diameter.parameter, "carcassHoleDiameter")
        for circle in circles[1:]:
            constraints.addEqual(circles[0], circle)

        sketcher.require_fully_constrained(sketch)
        self._verify_points(
            sketch,
            [back_line.endSketchPoint, *points],
            [side.corner, *side.carcass_holes],
        )
        return sketch, back_line.endSketchPoint

    def _create_hatch_sketch(
        self,
        spec: HingeSpec,
        layout: _Layout,
        corner: adsk.fusion.SketchPoint,
    ) -> tuple[adsk.fusion.Sketch, list[adsk.fusion.SketchPoint]]:
        """The pilot holes on the hatch's inner face: `inward` from each side
        panel and below the hinge reference, which comes from the projected
        reference corner of the carcass sketch. That link keeps the two
        halves of each hinge together when either board moves."""
        component = layout.hatch_face.body.parentComponent
        sketch = component.sketches.addWithoutEdges(layout.hatch_face)
        if not sketch:
            raise RuntimeError("Fusion failed to create the hatch hinge sketch.")
        sketch.name = "Hatch Hinge - Hatch Positions"
        sketcher = self._sketcher
        edge_lines = [
            sketcher.project_reference_line(
                sketch,
                side.edge,
                "carcass front edge",
            )
            for side in layout.sides
        ]
        reference = sketcher.project_point(
            sketch,
            corner,
            "carcass hinge reference",
        )
        sketch.isComputeDeferred = True
        lines = sketch.sketchCurves.sketchLines
        constraints = sketch.geometricConstraints

        # The reference lies on the first side panel; carry its level over
        # to the other one.
        anchors = [reference]
        for side, edge_line in zip(layout.sides[1:], edge_lines[1:]):
            level_line = lines.addByTwoPoints(
                reference,
                self._sketch_point(
                    sketch,
                    self._hatch_point(
                        side,
                        layout.up,
                        -spec.hatch_hole_inward,
                        0,
                    ),
                ),
            )
            level_line.isConstruction = True
            constraints.addPerpendicular(level_line, edge_line)
            constraints.addCoincident(level_line.endSketchPoint, edge_line)
            anchors.append(level_line.endSketchPoint)

        points: list[adsk.fusion.SketchPoint] = []
        expected: list[adsk.core.Point3D] = []
        first_lines: list[adsk.fusion.SketchLine] = []
        for side, edge_line, anchor in zip(layout.sides, edge_lines, anchors):
            inward_line = lines.addByTwoPoints(
                anchor,
                self._sketch_point(sketch, side.hatch_column),
            )
            inward_line.isConstruction = True
            constraints.addPerpendicular(inward_line, edge_line)
            column = lines.addByTwoPoints(
                inward_line.endSketchPoint,
                self._sketch_point(sketch, side.hatch_holes[0]),
            )
            column.isConstruction = True
            constraints.addParallel(column, edge_line)
            side_lines = [inward_line, column]
            side_points = [column.endSketchPoint]
            for hole in side.hatch_holes[1:]:
                pitch_line = lines.addByTwoPoints(
                    side_points[-1],
                    self._sketch_point(sketch, hole),
                )
                pitch_line.isConstruction = True
                constraints.addParallel(pitch_line, column)
                side_lines.append(pitch_line)
                side_points.append(pitch_line.endSketchPoint)

            if first_lines:
                # The second hinge mirrors the first one.
                for first_line, line in zip(first_lines, side_lines):
                    constraints.addEqual(first_line, line)
            else:
                dimensioned = [
                    (inward_line, spec.hatch_hole_inward, "hatchHoleInward"),
                    (column, spec.hatch_first_hole_below, "hatchFirstHoleBelow"),
                ]
                if len(side_lines) > 2:
                    dimensioned.append(
                        (side_lines[2], spec.hatch_hole_pitch, "hatchHolePitch")
                    )
                for line, value, role in dimensioned:
                    sketcher.add_distance_dimension(
                        sketch,
                        line.startSketchPoint,
                        line.endSketchPoint,
                        _mm(value),
                        role,
                    )
                for line in side_lines[3:]:
                    constraints.addEqual(side_lines[2], line)
                first_lines = side_lines
            points.extend(side_points)
            expected.extend(side.hatch_holes)

        sketcher.require_fully_constrained(sketch)
        self._verify_points(sketch, points, expected)
        return sketch, points

    def _sketch_point(
        self,
        sketch: adsk.fusion.Sketch,
        point: adsk.core.Point3D,
    ) -> adsk.core.Point3D:
        local = sketch.modelToSketchSpace(point)
        local.z = 0
        return local

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
                    f"'{sketch.name}' differs from the computed hinge "
                    f"position by {error:.6g} cm."
                )

    def _set_parameter_expression(
        self,
        parameter: adsk.fusion.ModelParameter,
        expression: str,
    ) -> None:
        """Writes only expressions that carry a parametric link.

        Every dimension here is created on geometry already placed at the
        intended value, so writing a pure literal changes nothing but the
        displayed text, at the cost of a document update (see
        Addin._expression_references_parameter)."""
        if self._expression_references_parameter(expression):
            parameter.expression = expression

    def _name_parameter(
        self,
        parameter: adsk.fusion.ModelParameter,
        role: str,
    ) -> None:
        """Renaming is disabled like in the other native add-ins: it is pure
        cosmetics, and each rename is a document update that costs ~0.5 s
        in large assemblies. Every cross-reference reads `parameter.name`
        live, so Fusion's generated names carry the links just as well."""
        return
