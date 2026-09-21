"""Box Joint - CNC-friendly box/finger joints as native timeline features.

Functionally modeled on the BoxJoint custom-feature add-in
(https://github.com/EvilHacker/BoxJoint/), restricted to 90-degree butt
joints, but built entirely from native Fusion features: fully constrained
sketches, join/cut extrudes, and to-object extents.

The joint is described in a local frame that is only used to compute
model-space positions (all sketch geometry is positioned by constraints):

    x: along the notch board's outside face into the overlap, 0..tB
       (tB = finger board thickness)
    y: through the notch board's thickness, 0..tA (0 = outside face)
    z: along the joint, 0..L

Roles: board A (the "notch board") owns the corner overlap; its outside
face shows the finger pattern and its notches are cut through its
thickness. Board B (the "finger board") butts with its end face against
A's inside face and receives the fingers.

CNC relief scheme (reproduces BoxJoint's hidden reliefs; each board is
machined flat from its INSIDE face with a bit of radius r, and NOTHING is
visible on the finished joint - no through dog bones on either face):

    * A's through-notches KEEP the fillets the bit leaves at the two
      notch-bottom corners, over the full thickness.
    * Every finger is ROUNDED OVER along its mating corners all the way
      to its front, so it nests into the kept fillets of the part it
      enters: B's fingers via the lens grooves cut from the finger-tip
      plane (they shave the corner sliver, radius r), A's fingers via the
      finger-side half of the wall grooves.
    * Shallow lens grooves along each notch wall at A's inside face (cut
      from A's end face, depth r) receive B's kept finger-root fillets;
      their notch-side half is opened square so it also clears the kept
      notch fillet in the band next to the inside face, where the mating
      finger corner is not rounded.
    * Hidden dog bones, one tool-radius deep, on BOTH inside faces - never
      through, never reaching the visible part of an inside face: circles
      on A's inside face centered on the notch walls against the notch
      bottom, and circles on B's inside face centered on the finger sides
      against the root seat. They clear the un-rounded corner band at the
      mating finger's root and give the bit room where the shallow relief
      passes end with a rounded stop.
"""

from dataclasses import dataclass
import math
import os
from typing import cast

import adsk.core
import adsk.fusion

from lib import addin, inputs, ui_placement, utils
from lib.fusionbootstrap.runtime import RuntimeInfo


_addin: addin.Addin | None = None

# An offset at or below this is treated as zero (cm): the geometry then
# lands exactly on its reference and is constrained coincident/collinear
# instead of dimensioned - an offset dimension between coincident entities
# is degenerate.
_ZERO_OFFSET = 1e-6


def run(context, runtime_info: RuntimeInfo):
    global _addin
    _addin = BoxJoint(runtime_info)
    # Dev support: allow external tooling to restart this add-in by firing
    # the custom event '<id>_reload' (see lib/fusionbootstrap/reloader.py).
    from lib.fusionbootstrap import reloader
    entry = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "box_joint.py",
    )
    reloader.ensure(runtime_info.id + "_reload", entry)


def stop(context):
    global _addin
    if _addin:
        _addin.shutdown()
    _addin = None


@dataclass(frozen=True)
class _ResolvedGeometry:
    face_a: adsk.fusion.BRepFace          # outside face of the notch board
    a_inside: adsk.fusion.BRepFace        # opposite face; B's end butts it
    a_end: adsk.fusion.BRepFace           # A's end face, coplanar with face_b
    face_b: adsk.fusion.BRepFace          # outside face of the finger board
    b_inside: adsk.fusion.BRepFace        # opposite face of the finger board
    b_end: adsk.fusion.BRepFace           # B's butting end face
    corner_edge: adsk.fusion.BRepEdge     # face_a ∩ a_end, along the joint
    shoulder_edge: adsk.fusion.BRepEdge   # face_b ∩ b_end
    inner_edge: adsk.fusion.BRepEdge      # b_inside ∩ b_end
    inside_end_edge: adsk.fusion.BRepEdge # a_inside ∩ a_end
    thickness_a: float
    thickness_b: float
    joint_length: float
    origin: adsk.core.Point3D             # corner line at the joint start
    x_dir: adsk.core.Vector3D
    y_dir: adsk.core.Vector3D
    z_dir: adsk.core.Vector3D


@dataclass(frozen=True)
class _JointSpec:
    count: int
    finger_width: float
    margin: float
    axial: float        # axial clearance (along the joint)
    lateral: float      # lateral clearance (finger tips / notch bottoms)
    radius: float       # bit radius; 0 disables all reliefs
    node_zs: list[float]
    zero_margin: bool
    zero_axial: bool
    zero_lateral: bool

    @property
    def has_relief(self) -> bool:
        return self.radius > _ZERO_OFFSET


@dataclass(frozen=True)
class _NotchWall:
    node: int                        # grid node index 1..n-1
    z: float                         # wall position (node z +- axial/2)
    anchor: adsk.fusion.SketchPoint  # sketch point on the corner line at z
    line: adsk.fusion.SketchLine     # the notch wall line


@dataclass(frozen=True)
class _NotchLayout:
    sketch: adsk.fusion.Sketch
    grid_points: list[adsk.fusion.SketchPoint]
    walls: list[_NotchWall]          # ordered by node index
    bottom_line: adsk.fusion.SketchLine | None  # first notch-bottom line
    radius_param: str | None         # bit-radius parameter (first fillet)
    axial_param: str | None          # axial/2 offset parameter
    lateral_param: str | None        # lateral offset parameter


@dataclass(frozen=True)
class _GapWall:
    node: int
    z: float
    line: adsk.fusion.SketchLine     # the gap wall (= finger side)
    tip: adsk.fusion.SketchPoint     # its end on the finger-tip line


@dataclass(frozen=True)
class _GapLayout:
    sketch: adsk.fusion.Sketch
    walls: list[_GapWall]            # ordered by node index
    bottom_line: adsk.fusion.SketchLine  # first gap-bottom line


class BoxJointInputs(inputs.Inputs):
    def __init__(self, units_manager: adsk.core.UnitsManager):
        units = units_manager.defaultLengthUnits

        self.faces = inputs.SelectionByEntityTokenInput(
            id="faces",
            name="Faces",
            filter=["SolidFaces"],
            lower_bound=2,
            upper_bound=2,
            tool_tip=(
                "Select the two OUTSIDE faces of the boards to join: the "
                "face the finger pattern shows on, and the outside face of "
                "the board that butts against it. The boards must meet in "
                "a flush 90-degree butt joint."
            ),
        )
        self.number_of_fingers = inputs.IntegerInput(
            id="numberOfFingers",
            name="Number of Fingers",
            default_value=5,
            minimum=3,
            maximum=99,
            tool_tip=(
                "Total number of fingers along the joint (odd, so both "
                "outer fingers stay on the notch board). Fingers and "
                "notches are equally wide."
            ),
        )
        self.margin = inputs.FloatInput(
            id="margin",
            name="Margin",
            default_value=0.0,
            tool_tip=(
                "Plain, uninterrupted margin at both ends of the joint "
                "before the first finger."
            ),
            units=units,
        )
        self.margin.minimum_value = 0
        self.tool_diameter = inputs.FloatInput(
            id="toolDiameter",
            name="Tool Diameter",
            default_value=0.6,
            tool_tip=(
                "CNC bit diameter. Drives the hidden corner reliefs: kept "
                "fillets, wall grooves, and T-bone plunges. Zero disables "
                "all reliefs (plain square joint)."
            ),
            units=units,
        )
        self.tool_diameter.minimum_value = 0
        self.clearance_axial = inputs.FloatInput(
            id="clearanceAxial",
            name="Axial Clearance",
            default_value=0.0,
            tool_tip=(
                "Clearance along the joint: every notch is widened and "
                "every finger narrowed by half this value per side."
            ),
            units=units,
        )
        self.clearance_axial.minimum_value = 0
        self.clearance_lateral = inputs.FloatInput(
            id="clearanceLateral",
            name="Lateral Clearance",
            default_value=0.0,
            tool_tip=(
                "Clearance across the joint: the notch bottoms and the "
                "finger-root seats are cut this much deeper, leaving a gap "
                "at the finger tips."
            ),
            units=units,
        )
        self.clearance_lateral.minimum_value = 0

        super().__init__()


class BoxJoint(addin.Addin):
    inputs: BoxJointInputs
    _body_tokens: dict[str, str]
    _face_tokens: dict[str, str]

    @property
    def preview_enabled(self) -> bool:
        # execute() builds native features only, so Fusion's executePreview
        # transaction can run it as a live preview and roll it back again.
        return True

    @property
    def plugin_name(self) -> str:
        return "Box Joint"

    @property
    def plugin_desc(self) -> str:
        return (
            "Create CNC-friendly box/finger joints between two butting "
            "boards with native Fusion features."
        )

    @property
    def plugin_tooltip(self) -> str:
        return (
            "Creates fully constrained sketches and join/cut extrudes for "
            "a 90-degree box joint, with hidden corner reliefs (kept "
            "fillets, wall grooves, and T-bones) so the joint closes "
            "without visible voids and cuts flat on a 3-axis CNC."
        )

    @property
    def resource_dir(self) -> str:
        return os.path.join(os.path.dirname(__file__), "Resources")

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

    def create_inputs(self) -> BoxJointInputs:
        design = adsk.fusion.Design.cast(self.app.activeProduct)
        if not design:
            raise RuntimeError("Box Joint requires an active Fusion design.")
        return BoxJointInputs(design.unitsManager)

    def pre_select(self, input, selection) -> bool:
        if not self.inputs or not input:
            return True
        if input.id == self.inputs.faces.id:
            face = adsk.fusion.BRepFace.cast(selection)
            return bool(
                face
                and face.body.isSolid
                and utils.brep.is_planar(face)
            )
        return True

    def _validate(self, args: adsk.core.ValidateInputsEventArgs):
        self._apply_validation(args, self._validation_error)

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def _validation_error(self) -> str | None:
        design = adsk.fusion.Design.cast(self.app.activeProduct)
        if not design:
            return "An active Fusion design is required."
        if design.designType != adsk.fusion.DesignTypes.ParametricDesignType:  # type: ignore
            return "Box Joint requires Design History (a parametric design)."
        if not self.inputs or len(self.inputs.faces.value) != 2:
            return "Select the two outside faces of the boards to join."

        try:
            geometry = self._resolve_geometry()
        except Exception as exc:
            return str(exc)

        if geometry.face_a.body.parentComponent != design.activeComponent:
            return (
                "Activate the component that owns the selected boards, "
                "then run Box Joint again."
            )
        if geometry.face_b.body.parentComponent != design.activeComponent:
            return "Both boards must be in the active component."

        count = self.inputs.number_of_fingers.value
        if count % 2 == 0:
            return (
                "Number of Fingers must be odd, so that both outer fingers "
                "stay on the notch board."
            )
        margin = self.inputs.margin.value
        if margin < 0:
            return "Margin cannot be negative."
        length = geometry.joint_length
        if 2 * margin >= length - _ZERO_OFFSET:
            return "The margins leave no room for the fingers."

        width = (length - 2 * margin) / count
        axial = self.inputs.clearance_axial.value
        radius = self.inputs.tool_diameter.value / 2
        if self.inputs.clearance_axial.value < 0:
            return "Axial Clearance cannot be negative."
        if self.inputs.clearance_lateral.value < 0:
            return "Lateral Clearance cannot be negative."
        if self.inputs.tool_diameter.value < 0:
            return "Tool Diameter cannot be negative."

        if radius > _ZERO_OFFSET:
            # Two relief circles sit on the walls of every notch, and two
            # lens grooves on the sides of every finger: below one tool
            # diameter (plus the axial clearance) they run into each other.
            if width - axial < 2 * radius + _ZERO_OFFSET:
                return (
                    "The fingers are too narrow for the corner reliefs: "
                    "each finger must be at least one Tool Diameter plus "
                    "the Axial Clearance wide. Reduce the Number of "
                    "Fingers or the Tool Diameter."
                )
            if geometry.thickness_a <= radius + _ZERO_OFFSET:
                return (
                    "The notch board is thinner than the tool radius; the "
                    "wall grooves would consume its full thickness."
                )
            if geometry.thickness_b <= radius + _ZERO_OFFSET:
                return (
                    "The finger board is thinner than the tool radius; the "
                    "finger grooves would consume its full thickness."
                )
        elif width - axial <= _ZERO_OFFSET:
            return "The Axial Clearance leaves no finger width."

        return None

    # ------------------------------------------------------------------
    # Geometry resolution
    # ------------------------------------------------------------------

    def _resolve_geometry(self) -> _ResolvedGeometry:
        if len(self.inputs.faces.value) != 2:
            raise ValueError("Select exactly two faces.")
        selected = [
            cast(
                adsk.fusion.BRepFace,
                face.nativeObject or face,
            )
            for face in (
                cast(adsk.fusion.BRepFace, self.inputs.faces.value[0]),
                cast(adsk.fusion.BRepFace, self.inputs.faces.value[1]),
            )
        ]
        for face in selected:
            if not utils.brep.is_planar(face) or not face.body.isSolid:
                raise ValueError(
                    "Both selections must be planar faces on solid bodies."
                )
        if selected[0].body == selected[1].body:
            raise ValueError(
                "The two faces must belong to two different bodies."
            )
        if not utils.brep.is_perpendicular(selected[0], selected[1]):
            raise ValueError(
                "The two boards must meet at 90 degrees (the selected "
                "faces must be perpendicular)."
            )

        for face_a, face_b in (selected, list(reversed(selected))):
            resolved = self._resolve_roles(face_a, face_b)
            if resolved:
                return resolved
        raise ValueError(
            "The boards do not butt against each other. Select the two "
            "OUTSIDE faces of two boards that meet in a flush 90-degree "
            "butt joint."
        )

    def _resolve_roles(
        self,
        face_a: adsk.fusion.BRepFace,
        face_b: adsk.fusion.BRepFace,
    ) -> _ResolvedGeometry | None:
        body_a = face_a.body
        body_b = face_b.body
        try:
            a_inside = utils.brep.get_opposite_face(face_a)
            b_inside = utils.brep.get_opposite_face(face_b)
        except ValueError:
            return None
        thickness_a = abs(
            utils.brep.distance_along_normal_between_faces(face_a, a_inside)
        )
        thickness_b = abs(
            utils.brep.distance_along_normal_between_faces(face_b, b_inside)
        )
        if thickness_a <= _ZERO_OFFSET or thickness_b <= _ZERO_OFFSET:
            return None

        into_a = utils.brep.normal_towards_face(a_inside, face_a)
        probe_depth = min(0.01, thickness_a / 10)
        b_end = None
        for face in body_b.faces:
            if not utils.brep.is_planar(face):
                continue
            if not utils.brep.is_parallel(face, face_a):
                continue
            if not utils.brep.is_co_planar(face, a_inside):
                continue
            probe = face.pointOnFace.copy()
            step = into_a.copy()
            step.scaleBy(probe_depth)
            probe.translateBy(step)
            if (
                body_a.pointContainment(probe)
                == adsk.fusion.PointContainment.PointInsidePointContainment
            ):
                b_end = face
                break
        if not b_end:
            return None

        # The corner must be flush: A ends exactly on the plane of B's
        # outside face.
        a_end = next(
            (
                face
                for face in body_a.faces
                if utils.brep.is_planar(face)
                and utils.brep.is_parallel(face, face_b)
                and utils.brep.is_co_planar(face, face_b)
            ),
            None,
        )
        if not a_end:
            raise ValueError(
                "The corner is not flush: the notch board must end exactly "
                "on the plane of the finger board's outside face. (Also "
                "make sure both selected faces are OUTSIDE faces.)"
            )

        corner_edge = self._shared_edge(face_a, a_end)
        shoulder_edge = self._shared_edge(face_b, b_end)
        inner_edge = self._shared_edge(b_inside, b_end)
        inside_end_edge = self._shared_edge(a_inside, a_end)
        if not all(
            (corner_edge, shoulder_edge, inner_edge, inside_end_edge)
        ):
            raise ValueError(
                "The boards' faces do not form a simple box corner (a "
                "required edge between two reference faces is missing)."
            )
        corner_edge = cast(adsk.fusion.BRepEdge, corner_edge)
        shoulder_edge = cast(adsk.fusion.BRepEdge, shoulder_edge)
        inner_edge = cast(adsk.fusion.BRepEdge, inner_edge)
        inside_end_edge = cast(adsk.fusion.BRepEdge, inside_end_edge)
        for edge in (corner_edge, shoulder_edge, inner_edge):
            if not utils.brep.is_linear(edge):
                raise ValueError("The joint edges must be straight.")

        start = shoulder_edge.startVertex.geometry
        end = shoulder_edge.endVertex.geometry
        z_dir = start.vectorTo(end)
        joint_length = z_dir.length
        if joint_length <= _ZERO_OFFSET:
            raise ValueError("The joint has zero length.")
        z_dir.normalize()
        if not utils.brep.is_parallel(corner_edge, z_dir):
            raise ValueError(
                "The corner edge and the butting end are not parallel."
            )

        y_dir = utils.brep.normal_towards_face(face_a, a_inside)
        x_dir = utils.brep.normal_towards_face(face_b, b_inside)
        origin = start.copy()
        back = y_dir.copy()
        back.scaleBy(-thickness_a)
        origin.translateBy(back)

        # The notch board must span the finger board's full width.
        tolerance = max(self.app.pointTolerance * 10, 1e-5)
        corner_zs = [
            z_dir.dotProduct(origin.vectorTo(vertex.geometry))
            for vertex in (corner_edge.startVertex, corner_edge.endVertex)
        ]
        if (
            min(corner_zs) > tolerance
            or max(corner_zs) < joint_length - tolerance
        ):
            raise ValueError(
                "The notch board must span the full width of the finger "
                "board along the joint."
            )

        return _ResolvedGeometry(
            face_a=face_a,
            a_inside=a_inside,
            a_end=a_end,
            face_b=face_b,
            b_inside=b_inside,
            b_end=b_end,
            corner_edge=corner_edge,
            shoulder_edge=shoulder_edge,
            inner_edge=inner_edge,
            inside_end_edge=inside_end_edge,
            thickness_a=thickness_a,
            thickness_b=thickness_b,
            joint_length=joint_length,
            origin=origin,
            x_dir=x_dir,
            y_dir=y_dir,
            z_dir=z_dir,
        )

    def _shared_edge(
        self,
        first: adsk.fusion.BRepFace,
        second: adsk.fusion.BRepFace,
    ) -> adsk.fusion.BRepEdge | None:
        for edge in first.edges:
            for face in edge.faces:
                if face == second:
                    return edge
        return None

    def _joint_spec(self, geometry: _ResolvedGeometry) -> _JointSpec:
        count = self.inputs.number_of_fingers.value
        margin = max(self.inputs.margin.value, 0)
        axial = max(self.inputs.clearance_axial.value, 0)
        lateral = max(self.inputs.clearance_lateral.value, 0)
        radius = max(self.inputs.tool_diameter.value, 0) / 2
        width = (geometry.joint_length - 2 * margin) / count
        node_zs = [margin + index * width for index in range(count + 1)]
        return _JointSpec(
            count=count,
            finger_width=width,
            margin=margin,
            axial=axial,
            lateral=lateral,
            radius=radius if radius > _ZERO_OFFSET else 0.0,
            node_zs=node_zs,
            zero_margin=margin <= _ZERO_OFFSET,
            zero_axial=axial <= _ZERO_OFFSET,
            zero_lateral=lateral <= _ZERO_OFFSET,
        )

    def _joint_point(
        self,
        geometry: _ResolvedGeometry,
        x: float,
        y: float,
        z: float,
    ) -> adsk.core.Point3D:
        point = geometry.origin.copy()
        for direction, distance in (
            (geometry.x_dir, x),
            (geometry.y_dir, y),
            (geometry.z_dir, z),
        ):
            step = direction.copy()
            step.scaleBy(distance)
            point.translateBy(step)
        return point

    # ------------------------------------------------------------------
    # Execution
    # ------------------------------------------------------------------

    def execute(self):
        error = self._validation_error()
        if error:
            raise ValueError(error)

        geometry = self._resolve_geometry()
        component = geometry.face_a.body.parentComponent
        spec = self._joint_spec(geometry)
        self._body_tokens = {
            "a": geometry.face_a.body.entityToken,
            "b": geometry.face_b.body.entityToken,
        }
        self._face_tokens = {
            "face_a": geometry.face_a.entityToken,
            "a_inside": geometry.a_inside.entityToken,
            "b_inside": geometry.b_inside.entityToken,
        }

        notch = self._create_notch_sketch(component, geometry, spec)
        self._require_fully_constrained(notch.sketch)

        groove_sketch: adsk.fusion.Sketch | None = None
        notch_relief_sketch: adsk.fusion.Sketch | None = None
        finger_groove_sketch: adsk.fusion.Sketch | None = None
        relief_sketch: adsk.fusion.Sketch | None = None
        if spec.has_relief:
            groove_sketch = self._create_wall_groove_sketch(
                component,
                geometry,
                spec,
                notch,
            )
            self._require_fully_constrained(groove_sketch)
            notch_relief_sketch = self._create_notch_relief_sketch(
                component,
                geometry,
                spec,
                notch,
            )
            self._require_fully_constrained(notch_relief_sketch)

        gaps = self._create_gap_sketch(component, geometry, spec, notch)
        self._require_fully_constrained(gaps.sketch)

        if spec.has_relief:
            finger_groove_sketch = self._create_finger_groove_sketch(
                component,
                geometry,
                spec,
                notch,
                gaps,
            )
            self._require_fully_constrained(finger_groove_sketch)
            relief_sketch = self._create_root_relief_sketch(
                component,
                geometry,
                spec,
                notch,
                gaps,
            )
            self._require_fully_constrained(relief_sketch)

        # Give the finger board the whole corner overlap, then carve the
        # gaps back out of it (the BoxJoint add-in's joiner/cutter scheme).
        strip_bodies = self._create_strip_extrude(component, geometry)
        self._create_join_combine(
            component,
            self._target_body(component, "b"),
            strip_bodies,
        )

        last_feature: adsk.fusion.Feature = self._create_to_entity_extrude(
            component=component,
            sketch=gaps.sketch,
            target_body=self._target_body(component, "b"),
            target_entity=self._cut_target(component, "b", "b_inside"),
            direction=geometry.x_dir,
            offset_expression=None,
            operation=adsk.fusion.FeatureOperations.CutFeatureOperation,  # type: ignore
            name="Box Joint - Gap Cuts",
            parameter_role="gaps",
        )
        last_feature = self._create_to_entity_extrude(
            component=component,
            sketch=notch.sketch,
            target_body=self._target_body(component, "a"),
            target_entity=self._cut_target(component, "a", "a_inside"),
            direction=geometry.y_dir,
            offset_expression=None,
            operation=adsk.fusion.FeatureOperations.CutFeatureOperation,  # type: ignore
            name="Box Joint - Notch Cuts",
            parameter_role="notches",
        )
        if spec.has_relief:
            assert (
                groove_sketch
                and notch_relief_sketch
                and finger_groove_sketch
                and relief_sketch
            )
            lateral_expression = (
                notch.lateral_param
                or self.inputs.clearance_lateral.expression
            )
            radius_param = cast(str, notch.radius_param)
            last_feature = self._create_to_entity_extrude(
                component=component,
                sketch=groove_sketch,
                target_body=self._target_body(component, "a"),
                target_entity=self._cut_target(component, "a", "b_inside"),
                direction=geometry.x_dir,
                offset_expression=(
                    None
                    if spec.zero_lateral
                    else f"({lateral_expression})"
                ),
                operation=adsk.fusion.FeatureOperations.CutFeatureOperation,  # type: ignore
                name="Box Joint - Wall Grooves Cut",
                parameter_role="wallGrooves",
            )
            last_feature = self._create_distance_extrude(
                component=component,
                sketch=notch_relief_sketch,
                target_body=self._target_body(component, "a"),
                direction=self._opposite(geometry.y_dir),
                distance=f"({radius_param})",
                operation=adsk.fusion.FeatureOperations.CutFeatureOperation,  # type: ignore
                name="Box Joint - Notch Reliefs Cut",
                parameter_role="notchReliefs",
            )
            if spec.zero_lateral:
                finger_groove_offset = f"-({radius_param})"
            else:
                finger_groove_offset = (
                    f"({lateral_expression}) - ({radius_param})"
                )
            last_feature = self._create_to_entity_extrude(
                component=component,
                sketch=finger_groove_sketch,
                target_body=self._target_body(component, "b"),
                target_entity=self._cut_target(component, "b", "a_inside"),
                direction=geometry.y_dir,
                offset_expression=finger_groove_offset,
                operation=adsk.fusion.FeatureOperations.CutFeatureOperation,  # type: ignore
                name="Box Joint - Finger Grooves Cut",
                parameter_role="fingerGrooves",
            )
            last_feature = self._create_distance_extrude(
                component=component,
                sketch=relief_sketch,
                target_body=self._target_body(component, "b"),
                direction=self._opposite(geometry.x_dir),
                distance=f"({radius_param})",
                operation=adsk.fusion.FeatureOperations.CutFeatureOperation,  # type: ignore
                name="Box Joint - Root Reliefs Cut",
                parameter_role="rootReliefs",
            )

        self._group_features(component, notch.sketch, last_feature)

    # ------------------------------------------------------------------
    # Sketch: notches on the notch board's outside face
    # ------------------------------------------------------------------

    def _create_notch_sketch(
        self,
        component: adsk.fusion.Component,
        geometry: _ResolvedGeometry,
        spec: _JointSpec,
    ) -> _NotchLayout:
        sketch = component.sketches.addWithoutEdges(geometry.face_a)
        if not sketch:
            raise RuntimeError(
                "Fusion failed to create 'Box Joint - Notches'."
            )
        sketch.name = "Box Joint - Notches"

        corner_line = self._project_line(sketch, geometry.corner_edge)
        corner_line.isConstruction = True
        inner_line = self._project_line(sketch, geometry.inner_edge)
        inner_line.isConstruction = True
        anchor_start = self._project_point(
            sketch,
            geometry.shoulder_edge.startVertex,
        )
        anchor_end = self._project_point(
            sketch,
            geometry.shoulder_edge.endVertex,
        )

        sketch.isComputeDeferred = True
        constraints = sketch.geometricConstraints
        lines = sketch.sketchCurves.sketchLines

        def to_sketch(x: float, z: float) -> adsk.core.Point3D:
            return sketch.modelToSketchSpace(
                self._joint_point(geometry, x, 0, z)
            )

        grid_points = self._add_grid_chain(
            sketch,
            corner_line,
            anchor_start,
            anchor_end,
            spec,
            to_sketch,
            "notch",
        )

        axial_param: str | None = None
        first_axial: adsk.fusion.SketchLine | None = None

        def wall_anchor(
            node: int,
            sign: int,
        ) -> tuple[float, adsk.fusion.SketchPoint]:
            nonlocal axial_param, first_axial
            if spec.zero_axial:
                return spec.node_zs[node], grid_points[node]
            z = spec.node_zs[node] + sign * spec.axial / 2
            segment = lines.addByTwoPoints(
                grid_points[node],
                to_sketch(0, z),
            )
            if not segment:
                raise RuntimeError(
                    "Fusion failed to create a notch wall offset."
                )
            segment.isConstruction = True
            constraints.addCoincident(segment.endSketchPoint, corner_line)
            if first_axial is None:
                first_axial = segment
                dimension = self._add_line_length_dimension(
                    sketch,
                    segment,
                    f"({self.inputs.clearance_axial.expression}) / 2",
                    "axialClearanceHalf",
                )
                axial_param = dimension.parameter.name
            else:
                constraints.addEqual(first_axial, segment)
            return z, segment.endSketchPoint

        walls: list[_NotchWall] = []
        radius = spec.radius
        depth = geometry.thickness_b + spec.lateral
        lateral_param: str | None = None
        radius_param: str | None = None
        first_bottom: adsk.fusion.SketchLine | None = None
        for node in range(1, spec.count - 1, 2):
            left_z, left_anchor = wall_anchor(node, -1)
            right_z, right_anchor = wall_anchor(node + 1, +1)

            wall_l = lines.addByTwoPoints(
                left_anchor,
                to_sketch(depth - radius, left_z),
            )
            bottom = lines.addByTwoPoints(
                to_sketch(depth, left_z + radius),
                to_sketch(depth, right_z - radius),
            )
            wall_r = lines.addByTwoPoints(
                right_anchor,
                to_sketch(depth - radius, right_z),
            )
            outer = lines.addByTwoPoints(right_anchor, left_anchor)
            walls.extend([
                _NotchWall(
                    node=node,
                    z=left_z,
                    anchor=left_anchor,
                    line=wall_l,
                ),
                _NotchWall(
                    node=node + 1,
                    z=right_z,
                    anchor=right_anchor,
                    line=wall_r,
                ),
            ])
            if not all((wall_l, bottom, wall_r, outer)):
                raise RuntimeError(
                    "Fusion failed to create a notch profile."
                )
            constraints.addPerpendicular(wall_l, corner_line)
            constraints.addPerpendicular(wall_r, corner_line)
            if first_bottom is None:
                first_bottom = bottom
                if spec.zero_lateral:
                    # Collinear already implies parallel; adding both trips
                    # Fusion's structural redundancy analysis.
                    constraints.addCollinear(inner_line, bottom)
                else:
                    constraints.addParallel(bottom, corner_line)
                    dimension = self._add_offset_dimension(
                        sketch,
                        inner_line,
                        bottom,
                        self.inputs.clearance_lateral.expression,
                        "lateralClearance",
                    )
                    lateral_param = dimension.parameter.name
            else:
                constraints.addCollinear(first_bottom, bottom)

            if radius <= 0:
                # Square notch: the walls run to the bottom directly.
                constraints.addCoincident(
                    wall_l.endSketchPoint,
                    bottom.startSketchPoint,
                )
                constraints.addCoincident(
                    wall_r.endSketchPoint,
                    bottom.endSketchPoint,
                )
                continue

            diagonal = radius - radius / math.sqrt(2)
            fillet_l = sketch.sketchCurves.sketchArcs.addByThreePoints(
                wall_l.endSketchPoint,
                to_sketch(depth - diagonal, left_z + diagonal),
                bottom.startSketchPoint,
            )
            fillet_r = sketch.sketchCurves.sketchArcs.addByThreePoints(
                bottom.endSketchPoint,
                to_sketch(depth - diagonal, right_z - diagonal),
                wall_r.endSketchPoint,
            )
            if not fillet_l or not fillet_r:
                raise RuntimeError(
                    "Fusion failed to create a notch corner fillet."
                )
            constraints.addTangent(fillet_l, wall_l)
            constraints.addTangent(fillet_l, bottom)
            constraints.addTangent(fillet_r, bottom)
            constraints.addTangent(fillet_r, wall_r)

            # The kept bottom-corner fillets carry the bit radius; the
            # first one holds the driving dimension, every other relief in
            # this and the other sketches references its parameter. Each
            # fillet gets its own radius dimension: with an arc-to-arc
            # equal chain Fusion's structural analysis left one arc center
            # under-constrained in some configurations (seen with a
            # non-zero axial clearance at three fingers).
            for fillet in (fillet_l, fillet_r):
                if radius_param is None:
                    dimension = self._add_arc_radius_dimension(
                        sketch,
                        fillet,
                        f"({self.inputs.tool_diameter.expression}) / 2",
                        "bitRadius",
                    )
                    radius_param = dimension.parameter.name
                else:
                    self._add_arc_radius_dimension(
                        sketch,
                        fillet,
                        radius_param,
                        "bitRadiusLink",
                    )

        sketch.isComputeDeferred = False
        return _NotchLayout(
            sketch=sketch,
            grid_points=grid_points,
            walls=walls,
            bottom_line=first_bottom,
            radius_param=radius_param,
            axial_param=axial_param,
            lateral_param=lateral_param,
        )

    def _add_grid_chain(
        self,
        sketch: adsk.fusion.Sketch,
        corner_line: adsk.fusion.SketchLine,
        anchor_start: adsk.fusion.SketchPoint,
        anchor_end: adsk.fusion.SketchPoint,
        spec: _JointSpec,
        to_sketch,
        parameter_role: str,
    ) -> list[adsk.fusion.SketchPoint]:
        """A chain of n equal construction segments along the corner line.

        No segment carries a width dimension: the solver derives the
        finger width from the anchors and the margins, so the layout stays
        parametric when the boards change. (A plain chain of equal-length
        collinear segments is also the only equal-spacing formulation
        Fusion's redundancy analysis accepts at every finger count.)
        """
        constraints = sketch.geometricConstraints
        grid_points: list[adsk.fusion.SketchPoint] = []
        for index, z in enumerate(spec.node_zs):
            point = sketch.sketchPoints.add(to_sketch(0, z))
            if not point:
                raise RuntimeError(
                    "Fusion failed to create a finger grid point."
                )
            grid_points.append(point)
        if spec.zero_margin:
            constraints.addCoincident(grid_points[0], anchor_start)
            constraints.addCoincident(grid_points[-1], anchor_end)
            for point in grid_points[1:-1]:
                constraints.addCoincident(point, corner_line)
        else:
            for point in grid_points:
                constraints.addCoincident(point, corner_line)
            start_dimension = self._add_distance_dimension(
                sketch,
                anchor_start,
                grid_points[0],
                self.inputs.margin.expression,
                f"{parameter_role}StartMargin",
            )
            self._add_distance_dimension(
                sketch,
                grid_points[-1],
                anchor_end,
                start_dimension.parameter.name,
                f"{parameter_role}EndMargin",
            )
        segments: list[adsk.fusion.SketchLine] = []
        for first, second in zip(grid_points, grid_points[1:]):
            segment = sketch.sketchCurves.sketchLines.addByTwoPoints(
                first,
                second,
            )
            if not segment:
                raise RuntimeError(
                    "Fusion failed to create a finger grid segment."
                )
            segment.isConstruction = True
            segments.append(segment)
        for segment in segments[1:]:
            constraints.addEqual(segments[0], segment)
        return grid_points

    # ------------------------------------------------------------------
    # Sketch: wall grooves on the notch board's end face
    # ------------------------------------------------------------------

    def _create_wall_groove_sketch(
        self,
        component: adsk.fusion.Component,
        geometry: _ResolvedGeometry,
        spec: _JointSpec,
        notch: _NotchLayout,
    ) -> adsk.fusion.Sketch:
        sketch = component.sketches.addWithoutEdges(geometry.a_end)
        if not sketch:
            raise RuntimeError(
                "Fusion failed to create 'Box Joint - Wall Grooves'."
            )
        sketch.name = "Box Joint - Wall Grooves"

        inside_line = self._project_line(sketch, geometry.inside_end_edge)
        inside_line.isConstruction = True
        wall_points = [
            self._project_point(sketch, wall.anchor)
            for wall in notch.walls
        ]

        sketch.isComputeDeferred = True
        radius = spec.radius
        surface = geometry.thickness_a

        def to_sketch(y: float, z: float) -> adsk.core.Point3D:
            return sketch.modelToSketchSpace(
                self._joint_point(geometry, 0, y, z)
            )

        self._add_lens_grooves(
            sketch,
            inside_line,
            [
                # Odd nodes are left notch walls (notch toward +z), even
                # nodes right walls: open the groove into the notch so it
                # clears the kept bottom-corner fillet near the inside face.
                (projected, wall.z, 1 if wall.node % 2 == 1 else -1)
                for projected, wall in zip(wall_points, notch.walls)
            ],
            to_sketch,
            surface,
            radius,
            cast(str, notch.radius_param),
            "wallGroove",
        )
        sketch.isComputeDeferred = False
        return sketch

    def _add_lens_grooves(
        self,
        sketch: adsk.fusion.Sketch,
        surface_line: adsk.fusion.SketchLine,
        sites: list[tuple[adsk.fusion.SketchPoint, float, int]],
        to_sketch,
        surface: float,
        radius: float,
        radius_param: str,
        parameter_role: str,
    ) -> None:
        """Lens-shaped relief profiles along a reference surface line.

        Each lens is the material a bit of the given radius cannot clear
        out of a right-angle corner: two tangent quarter arcs meeting one
        radius below the surface line, closed by the surface line itself.
        `to_sketch(depth, z)` maps (distance below the surface, joint
        position) to sketch space; each site is (projected reference point,
        z value, open_side).

        A site with a non-zero open_side (+1/-1 along z) opens that half of
        the lens into a full radius-by-radius rectangle. The wall grooves
        need this on their notch side: the notch cut keeps its bottom-corner
        fillet over the board's full thickness (a through-cut cannot vary),
        so the groove has to clear the fillet's crescent in the band next to
        the inside face - the shape BoxJoint gets by sweeping its kept
        fillet only up to one radius short of the face. The arc on the open
        side stays as construction geometry: it is what pins the meeting
        point, the rectangle alone would leave it under-constrained.
        """
        constraints = sketch.geometricConstraints
        lines = sketch.sketchCurves.sketchLines
        arcs = sketch.sketchCurves.sketchArcs
        diagonal = radius - radius / math.sqrt(2)
        for reference, z, open_side in sites:
            closing = lines.addByTwoPoints(
                to_sketch(surface, z - radius),
                to_sketch(surface, z + radius),
            )
            if not closing:
                raise RuntimeError(
                    "Fusion failed to create a groove closing line."
                )
            meeting = sketch.sketchPoints.add(
                to_sketch(surface - radius, z)
            )
            if not meeting:
                raise RuntimeError(
                    "Fusion failed to create a groove meeting point."
                )
            arc_1 = arcs.addByThreePoints(
                closing.startSketchPoint,
                to_sketch(surface - diagonal, z - diagonal),
                meeting,
            )
            arc_2 = arcs.addByThreePoints(
                meeting,
                to_sketch(surface - diagonal, z + diagonal),
                closing.endSketchPoint,
            )
            if not arc_1 or not arc_2:
                raise RuntimeError(
                    "Fusion failed to create a groove arc."
                )
            constraints.addCollinear(surface_line, closing)
            constraints.addTangent(arc_1, closing)
            constraints.addTangent(arc_2, closing)
            constraints.addTangent(arc_1, arc_2)
            # Per-arc radius dimensions instead of equal chains; see the
            # notch fillets.
            self._add_arc_radius_dimension(
                sketch,
                arc_2,
                radius_param,
                f"{parameter_role}Radius",
            )
            drop = lines.addByTwoPoints(reference, meeting)
            if not drop:
                raise RuntimeError(
                    "Fusion failed to create a groove position reference."
                )
            drop.isConstruction = True
            constraints.addPerpendicular(drop, surface_line)
            if open_side:
                open_arc = arc_2 if open_side > 0 else arc_1
                open_arc.isConstruction = True
                corner = to_sketch(
                    surface - radius,
                    z + open_side * radius,
                )
                floor = lines.addByTwoPoints(meeting, corner)
                closing_end = (
                    closing.endSketchPoint
                    if open_side > 0
                    else closing.startSketchPoint
                )
                side = lines.addByTwoPoints(
                    floor.endSketchPoint,
                    closing_end,
                )
                if not floor or not side:
                    raise RuntimeError(
                        "Fusion failed to create a groove rectangle."
                    )
                constraints.addParallel(floor, closing)
                constraints.addPerpendicular(side, closing)
            self._add_arc_radius_dimension(
                sketch,
                arc_1,
                radius_param,
                f"{parameter_role}Radius",
            )

    # ------------------------------------------------------------------
    # Sketch: gaps on the finger board's outside face
    # ------------------------------------------------------------------

    def _create_gap_sketch(
        self,
        component: adsk.fusion.Component,
        geometry: _ResolvedGeometry,
        spec: _JointSpec,
        notch: _NotchLayout,
    ) -> _GapLayout:
        sketch = component.sketches.addWithoutEdges(geometry.face_b)
        if not sketch:
            raise RuntimeError(
                "Fusion failed to create 'Box Joint - Gaps'."
            )
        sketch.name = "Box Joint - Gaps"

        # The projected corner edge stays a REGULAR curve: it is the tip-side
        # boundary of every gap profile. Closing each gap with its own line
        # between the wall tips is not an option: with zero axial clearance
        # the wall tips are projected (fixed) points, and a curve whose two
        # endpoints are both fixed makes Fusion's solver report the sketch
        # as over-constrained (verified empirically).
        tip_line = self._project_line(sketch, geometry.corner_edge)
        shoulder_line = self._project_line(sketch, geometry.shoulder_edge)
        shoulder_line.isConstruction = True
        anchor_start = self._project_point(
            sketch,
            geometry.shoulder_edge.startVertex,
        )
        anchor_end = self._project_point(
            sketch,
            geometry.shoulder_edge.endVertex,
        )
        node_points = {
            node: self._project_point(sketch, notch.grid_points[node])
            for node in range(1, spec.count)
        }

        sketch.isComputeDeferred = True
        constraints = sketch.geometricConstraints
        lines = sketch.sketchCurves.sketchLines
        arcs = sketch.sketchCurves.sketchArcs

        def to_sketch(y: float, z: float) -> adsk.core.Point3D:
            return sketch.modelToSketchSpace(
                self._joint_point(geometry, 0, y, z)
            )

        radius = spec.radius
        seat = geometry.thickness_a + spec.lateral
        diagonal = radius - radius / math.sqrt(2)
        axial_param = notch.axial_param
        first_axial: adsk.fusion.SketchLine | None = None
        first_bottom: adsk.fusion.SketchLine | None = None
        walls: dict[int, _GapWall] = {}

        def gap_anchor(node: int) -> tuple[float, adsk.fusion.SketchPoint]:
            # The gap walls sit on the opposite side of each grid node
            # from the notch walls: fingers narrow, notches widen.
            nonlocal first_axial
            if spec.zero_axial:
                return spec.node_zs[node], node_points[node]
            sign = 1 if node % 2 == 1 else -1
            z = spec.node_zs[node] + sign * spec.axial / 2
            segment = lines.addByTwoPoints(node_points[node], to_sketch(0, z))
            if not segment:
                raise RuntimeError(
                    "Fusion failed to create a gap wall offset."
                )
            segment.isConstruction = True
            constraints.addCoincident(segment.endSketchPoint, tip_line)
            if first_axial is None:
                first_axial = segment
                self._add_line_length_dimension(
                    sketch,
                    segment,
                    cast(str, axial_param),
                    "gapAxialClearanceHalf",
                )
            else:
                constraints.addEqual(first_axial, segment)
            return z, segment.endSketchPoint

        def add_wall(node: int) -> _GapWall:
            z, anchor = gap_anchor(node)
            wall = lines.addByTwoPoints(
                anchor,
                to_sketch(seat - radius, z),
            )
            if not wall:
                raise RuntimeError("Fusion failed to create a gap wall.")
            constraints.addPerpendicular(wall, tip_line)
            gap_wall = _GapWall(node=node, z=z, line=wall, tip=anchor)
            walls[node] = gap_wall
            return gap_wall

        def add_bottom(
            start: adsk.core.Point3D | adsk.fusion.SketchPoint,
            end: adsk.core.Point3D | adsk.fusion.SketchPoint,
        ) -> adsk.fusion.SketchLine:
            nonlocal first_bottom
            bottom = lines.addByTwoPoints(start, end)
            if not bottom:
                raise RuntimeError("Fusion failed to create a gap bottom.")
            if first_bottom is None:
                first_bottom = bottom
                if spec.zero_lateral:
                    # Collinear already implies parallel; adding both trips
                    # Fusion's structural redundancy analysis.
                    constraints.addCollinear(shoulder_line, bottom)
                else:
                    constraints.addParallel(bottom, shoulder_line)
                    self._add_offset_dimension(
                        sketch,
                        shoulder_line,
                        bottom,
                        notch.lateral_param
                        or self.inputs.clearance_lateral.expression,
                        "gapLateralClearance",
                    )
            else:
                constraints.addCollinear(first_bottom, bottom)
            return bottom

        def add_fillet(
            bottom: adsk.fusion.SketchLine,
            bottom_point: adsk.fusion.SketchPoint,
            wall: _GapWall,
            z_inward: int,
        ) -> None:
            # z_inward: direction from the wall into the gap (+1/-1).
            if radius <= 0:
                constraints.addCoincident(
                    bottom_point,
                    wall.line.endSketchPoint,
                )
                return
            fillet = arcs.addByThreePoints(
                bottom_point,
                to_sketch(seat - diagonal, wall.z + z_inward * diagonal),
                wall.line.endSketchPoint,
            )
            if not fillet:
                raise RuntimeError(
                    "Fusion failed to create a gap corner fillet."
                )
            constraints.addTangent(fillet, wall.line)
            constraints.addTangent(fillet, bottom)
            # Every fillet carries its own radius dimension; an arc-to-arc
            # equal chain can leave an arc center structurally
            # under-constrained (see the notch sketch).
            self._add_arc_radius_dimension(
                sketch,
                fillet,
                cast(str, notch.radius_param)
                if notch.radius_param
                else f"({self.inputs.tool_diameter.expression}) / 2",
                "gapFilletRadius",
            )

        # Start end gap: open at the board end, one filleted corner.
        start_wall = add_wall(1)
        start_outer = lines.addByTwoPoints(
            to_sketch(0, 0),
            to_sketch(seat, 0),
        )
        if not start_outer:
            raise RuntimeError("Fusion failed to create a gap side.")
        constraints.addPerpendicular(start_outer, tip_line)
        constraints.addCoincident(anchor_start, start_outer)
        constraints.addCoincident(start_outer.startSketchPoint, tip_line)
        start_bottom = add_bottom(
            start_outer.endSketchPoint,
            to_sketch(seat, start_wall.z - radius),
        )
        add_fillet(start_bottom, start_bottom.endSketchPoint, start_wall, -1)

        # Interior gaps: two filleted corners each.
        for node in range(2, spec.count - 1, 2):
            wall_l = add_wall(node)
            wall_r = add_wall(node + 1)
            bottom = add_bottom(
                to_sketch(seat, wall_l.z + radius),
                to_sketch(seat, wall_r.z - radius),
            )
            add_fillet(bottom, bottom.startSketchPoint, wall_l, +1)
            add_fillet(bottom, bottom.endSketchPoint, wall_r, -1)

        # End gap at the far board end.
        end_wall = add_wall(spec.count - 1)
        end_outer = lines.addByTwoPoints(
            to_sketch(0, geometry.joint_length),
            to_sketch(seat, geometry.joint_length),
        )
        if not end_outer:
            raise RuntimeError("Fusion failed to create a gap side.")
        constraints.addPerpendicular(end_outer, tip_line)
        constraints.addCoincident(anchor_end, end_outer)
        constraints.addCoincident(end_outer.startSketchPoint, tip_line)
        end_bottom = add_bottom(
            to_sketch(seat, end_wall.z + radius),
            end_outer.endSketchPoint,
        )
        add_fillet(end_bottom, end_bottom.startSketchPoint, end_wall, +1)

        sketch.isComputeDeferred = False
        return _GapLayout(
            sketch=sketch,
            walls=[walls[node] for node in sorted(walls)],
            bottom_line=cast(adsk.fusion.SketchLine, first_bottom),
        )

    # ------------------------------------------------------------------
    # Sketch: finger grooves on the finger-tip plane
    # ------------------------------------------------------------------

    def _create_finger_groove_sketch(
        self,
        component: adsk.fusion.Component,
        geometry: _ResolvedGeometry,
        spec: _JointSpec,
        notch: _NotchLayout,
        gaps: _GapLayout,
    ) -> adsk.fusion.Sketch:
        sketch = component.sketches.addWithoutEdges(geometry.face_a)
        if not sketch:
            raise RuntimeError(
                "Fusion failed to create 'Box Joint - Finger Grooves'."
            )
        sketch.name = "Box Joint - Finger Grooves"

        inner_line = self._project_line(sketch, geometry.inner_edge)
        inner_line.isConstruction = True
        side_points = [
            self._project_point(sketch, wall.tip)
            for wall in gaps.walls
        ]

        sketch.isComputeDeferred = True

        def to_sketch(x: float, z: float) -> adsk.core.Point3D:
            return sketch.modelToSketchSpace(
                self._joint_point(geometry, x, 0, z)
            )

        self._add_lens_grooves(
            sketch,
            inner_line,
            [
                (projected, wall.z, 0)
                for projected, wall in zip(side_points, gaps.walls)
            ],
            to_sketch,
            geometry.thickness_b,
            spec.radius,
            cast(str, notch.radius_param),
            "fingerGroove",
        )
        sketch.isComputeDeferred = False
        return sketch

    # ------------------------------------------------------------------
    # Sketch: root reliefs on the finger board's inside face
    # ------------------------------------------------------------------

    def _create_root_relief_sketch(
        self,
        component: adsk.fusion.Component,
        geometry: _ResolvedGeometry,
        spec: _JointSpec,
        notch: _NotchLayout,
        gaps: _GapLayout,
    ) -> adsk.fusion.Sketch:
        sketch = component.sketches.addWithoutEdges(geometry.b_inside)
        if not sketch:
            raise RuntimeError(
                "Fusion failed to create 'Box Joint - Root Reliefs'."
            )
        sketch.name = "Box Joint - Root Reliefs"

        bottom_line = self._project_line(sketch, gaps.bottom_line)
        bottom_line.isConstruction = True
        wall_lines = [
            self._project_line(sketch, wall.line)
            for wall in gaps.walls
        ]
        for line in wall_lines:
            line.isConstruction = True

        sketch.isComputeDeferred = True
        constraints = sketch.geometricConstraints
        radius = spec.radius
        center_y = geometry.thickness_a + spec.lateral - radius
        first_circle: adsk.fusion.SketchCircle | None = None
        for wall, wall_line in zip(gaps.walls, wall_lines):
            circle = sketch.sketchCurves.sketchCircles.addByCenterRadius(
                sketch.modelToSketchSpace(
                    self._joint_point(
                        geometry,
                        geometry.thickness_b,
                        center_y,
                        wall.z,
                    )
                ),
                radius,
            )
            if not circle:
                raise RuntimeError(
                    "Fusion failed to create a root relief circle."
                )
            constraints.addCoincident(circle.centerSketchPoint, wall_line)
            constraints.addTangent(circle, bottom_line)
            if first_circle is None:
                first_circle = circle
                self._add_circle_diameter_dimension(
                    sketch,
                    circle,
                    f"({cast(str, notch.radius_param)}) * 2",
                    "rootReliefDiameter",
                )
            else:
                constraints.addEqual(first_circle, circle)
        sketch.isComputeDeferred = False
        return sketch

    # ------------------------------------------------------------------
    # Sketch: notch reliefs on the notch board's inside face
    # ------------------------------------------------------------------

    def _create_notch_relief_sketch(
        self,
        component: adsk.fusion.Component,
        geometry: _ResolvedGeometry,
        spec: _JointSpec,
        notch: _NotchLayout,
    ) -> adsk.fusion.Sketch:
        """Hidden dog bones on the notch board's inside face.

        One circle per notch wall, centered on the wall against the notch
        bottom, cut one bit radius deep. Together with the wall grooves
        they clear the mating finger's un-rounded corner band at its root
        and give the bit room where the shallow passes end with a rounded
        stop. Nothing shows: the circles reach exactly to the notch bottom
        and stay under the finger board's seat."""
        sketch = component.sketches.addWithoutEdges(geometry.a_inside)
        if not sketch:
            raise RuntimeError(
                "Fusion failed to create 'Box Joint - Notch Reliefs'."
            )
        sketch.name = "Box Joint - Notch Reliefs"

        bottom_line = self._project_line(
            sketch,
            cast(adsk.fusion.SketchLine, notch.bottom_line),
        )
        bottom_line.isConstruction = True
        wall_lines = [
            self._project_line(sketch, wall.line)
            for wall in notch.walls
        ]
        for line in wall_lines:
            line.isConstruction = True

        sketch.isComputeDeferred = True
        constraints = sketch.geometricConstraints
        radius = spec.radius
        center_x = geometry.thickness_b + spec.lateral - radius
        first_circle: adsk.fusion.SketchCircle | None = None
        for wall, wall_line in zip(notch.walls, wall_lines):
            circle = sketch.sketchCurves.sketchCircles.addByCenterRadius(
                sketch.modelToSketchSpace(
                    self._joint_point(
                        geometry,
                        center_x,
                        geometry.thickness_a,
                        wall.z,
                    )
                ),
                radius,
            )
            if not circle:
                raise RuntimeError(
                    "Fusion failed to create a notch relief circle."
                )
            constraints.addCoincident(circle.centerSketchPoint, wall_line)
            constraints.addTangent(circle, bottom_line)
            if first_circle is None:
                first_circle = circle
                self._add_circle_diameter_dimension(
                    sketch,
                    circle,
                    f"({cast(str, notch.radius_param)}) * 2",
                    "notchReliefDiameter",
                )
            else:
                constraints.addEqual(first_circle, circle)
        sketch.isComputeDeferred = False
        return sketch

    # ------------------------------------------------------------------
    # Features
    # ------------------------------------------------------------------

    def _create_strip_extrude(
        self,
        component: adsk.fusion.Component,
        geometry: _ResolvedGeometry,
    ) -> list[adsk.fusion.BRepBody]:
        extrude_input = component.features.extrudeFeatures.createInput(
            geometry.b_end,
            adsk.fusion.FeatureOperations.NewBodyFeatureOperation,  # type: ignore
        )
        if not extrude_input:
            raise RuntimeError(
                "Fusion failed to initialize the finger stock extrude."
            )
        face_a = self._resolve_face("face_a")
        extent = adsk.fusion.ToEntityExtentDefinition.create(face_a, False)
        if not extent:
            raise RuntimeError(
                "Fusion failed to define the finger stock extent."
            )
        direction = self._opposite(geometry.y_dir)
        extent.directionHint = direction
        # A body face's natural extrude direction is its outward normal,
        # which points from the butting end face into the notch board.
        if not extrude_input.setOneSideExtent(
            extent,
            adsk.fusion.ExtentDirections.PositiveExtentDirection,  # type: ignore
        ):
            raise RuntimeError(
                "Fusion rejected the finger stock extent."
            )
        extrude = component.features.extrudeFeatures.add(extrude_input)
        if not extrude or extrude.bodies.count == 0:
            raise RuntimeError(
                "Fusion failed to extrude the finger stock."
            )
        extrude.name = "Box Joint - Finger Stock"
        # For a face-profile extrude, extrude.bodies contains the profile
        # face's source body alongside the newly created one; only the new
        # body may go into the join, or the combine gets its own target as
        # a tool and rejects the input.
        source_body = self._target_body(component, "b")
        strip_bodies = [
            body
            for body in cast(
                list[adsk.fusion.BRepBody],
                utils.fusion.as_list(extrude.bodies),
            )
            if body != source_body
        ]
        if len(strip_bodies) != 1:
            raise RuntimeError(
                "The finger stock extrude did not create exactly one body."
            )
        return strip_bodies

    def _create_join_combine(
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
            raise RuntimeError("Fusion failed to initialize the finger join.")
        combine_input.operation = (
            adsk.fusion.FeatureOperations.JoinFeatureOperation  # type: ignore
        )
        combine_input.isKeepToolBodies = False
        combine = component.features.combineFeatures.add(combine_input)
        if not combine:
            raise RuntimeError("Fusion failed to join the finger stock.")
        combine.name = "Box Joint - Join"
        return combine

    def _create_to_entity_extrude(
        self,
        component: adsk.fusion.Component,
        sketch: adsk.fusion.Sketch,
        target_body: adsk.fusion.BRepBody,
        target_entity: adsk.core.Base,
        direction: adsk.core.Vector3D,
        offset_expression: str | None,
        operation,
        name: str,
        parameter_role: str,
    ) -> adsk.fusion.ExtrudeFeature:
        profiles = self._all_profiles(sketch)
        extrude_input = component.features.extrudeFeatures.createInput(
            profiles,
            operation,
        )
        if not extrude_input:
            raise RuntimeError(f"Fusion failed to initialize '{name}'.")
        if offset_expression is None:
            extent = adsk.fusion.ToEntityExtentDefinition.create(
                target_entity,
                False,
            )
        else:
            extent = adsk.fusion.ToEntityExtentDefinition.create(
                target_entity,
                False,
                adsk.core.ValueInput.createByString(offset_expression),
            )
        if not extent:
            raise RuntimeError(f"Fusion failed to define '{name}' extent.")
        extent.directionHint = direction
        if adsk.fusion.BRepBody.cast(target_entity):
            extent.isMinimumSolution = False
        if not extrude_input.setOneSideExtent(
            extent,
            self._extent_direction(sketch, direction),
        ):
            raise RuntimeError(f"Fusion rejected the extent of '{name}'.")
        if operation == adsk.fusion.FeatureOperations.CutFeatureOperation:  # type: ignore
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
            offset = adsk.fusion.ModelParameter.cast(final_extent.offset)
            if offset and offset_expression is not None:
                self._set_parameter_expression(offset, offset_expression)
        return extrude

    def _create_distance_extrude(
        self,
        component: adsk.fusion.Component,
        sketch: adsk.fusion.Sketch,
        target_body: adsk.fusion.BRepBody,
        direction: adsk.core.Vector3D,
        distance: str,
        operation,
        name: str,
        parameter_role: str,
    ) -> adsk.fusion.ExtrudeFeature:
        directions = [self._extent_direction(sketch, direction)]
        directions.append(
            adsk.fusion.ExtentDirections.NegativeExtentDirection
            if directions[0]
            == adsk.fusion.ExtentDirections.PositiveExtentDirection
            else adsk.fusion.ExtentDirections.PositiveExtentDirection
        )
        healthy = adsk.fusion.FeatureHealthStates.HealthyFeatureHealthState
        last_error: str | None = None
        # A one-side distance extent does not always honor the requested
        # extent direction the way a to-entity extent does (the reliefs on
        # the inside faces computed into thin air with "No target body!").
        # Try the computed direction, and when the feature comes out
        # unhealthy, rebuild it flipped.
        for attempt, extent_direction in enumerate(directions):
            extrude_input = component.features.extrudeFeatures.createInput(
                self._all_profiles(sketch),
                operation,
            )
            if not extrude_input:
                raise RuntimeError(f"Fusion failed to initialize '{name}'.")
            extent = adsk.fusion.DistanceExtentDefinition.create(
                adsk.core.ValueInput.createByString(distance)
            )
            if not extent:
                raise RuntimeError(f"Fusion failed to define '{name}' depth.")
            if not extrude_input.setOneSideExtent(extent, extent_direction):
                raise RuntimeError(f"Fusion rejected the extent of '{name}'.")
            if operation == adsk.fusion.FeatureOperations.CutFeatureOperation:  # type: ignore
                extrude_input.participantBodies = [target_body]
            try:
                extrude = component.features.extrudeFeatures.add(
                    extrude_input
                )
            except RuntimeError as exc:
                last_error = str(exc)
                continue
            if not extrude:
                last_error = "Fusion returned no feature."
                continue
            # healthState can still read healthy right after add() and only
            # flip to "Compute Failed" on the next recompute; a cut that
            # went the wrong way reliably reports zero affected bodies.
            if (
                extrude.healthState != healthy
                or extrude.bodies.count == 0
            ):
                try:
                    last_error = extrude.errorOrWarningMessage or (
                        "the cut did not touch any body"
                    )
                except Exception:
                    last_error = "the cut did not touch any body"
                extrude.deleteMe()
                continue
            extrude.name = name
            sketch.isVisible = False
            final_extent = adsk.fusion.DistanceExtentDefinition.cast(
                extrude.extentOne
            )
            if final_extent and final_extent.distance:
                # The one-side distance is a SIGNED parameter: an extrude
                # built with NegativeExtentDirection stores it negative.
                # Writing the positive expression onto it silently flips
                # the cut into thin air ("No target body!"), so keep the
                # sign the feature solved with.
                expression = distance
                if final_extent.distance.value < 0:
                    expression = f"-({distance})"
                self._set_parameter_expression(
                    final_extent.distance,
                    expression,
                )
                if extrude.healthState != healthy:
                    raise RuntimeError(
                        f"'{name}' failed after writing its depth "
                        "expression."
                    )
            return extrude
        raise RuntimeError(
            f"Fusion failed to create '{name}': {last_error}"
        )

    # ------------------------------------------------------------------
    # Shared sketch/feature helpers
    # ------------------------------------------------------------------

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

    def _project_line(
        self,
        sketch: adsk.fusion.Sketch,
        line: adsk.core.Base,
    ) -> adsk.fusion.SketchLine:
        projected = sketch.project2(
            cast(list[adsk.core.Base], [line]),
            True,
        )
        if len(projected) != 1:
            raise RuntimeError("Fusion failed to project a reference line.")
        result = adsk.fusion.SketchLine.cast(projected[0])
        if not result:
            raise RuntimeError("A projected reference is not a straight line.")
        return result

    def _project_point(
        self,
        sketch: adsk.fusion.Sketch,
        point: adsk.core.Base,
    ) -> adsk.fusion.SketchPoint:
        projected = sketch.project2(
            cast(list[adsk.core.Base], [point]),
            True,
        )
        if len(projected) != 1:
            raise RuntimeError("Fusion failed to project a reference point.")
        result = adsk.fusion.SketchPoint.cast(projected[0])
        if not result:
            raise RuntimeError("A projected reference is not a point.")
        return result

    def _add_line_length_dimension(
        self,
        sketch: adsk.fusion.Sketch,
        line: adsk.fusion.SketchLine,
        expression: str,
        parameter_role: str,
    ) -> adsk.fusion.SketchLinearDimension:
        return self._add_distance_dimension(
            sketch,
            line.startSketchPoint,
            line.endSketchPoint,
            expression,
            parameter_role,
        )

    def _add_distance_dimension(
        self,
        sketch: adsk.fusion.Sketch,
        start: adsk.fusion.SketchPoint,
        end: adsk.fusion.SketchPoint,
        expression: str,
        parameter_role: str,
    ) -> adsk.fusion.SketchLinearDimension:
        text = adsk.core.Point3D.create(
            (start.geometry.x + end.geometry.x) / 2 + 0.2,
            (start.geometry.y + end.geometry.y) / 2 + 0.2,
            0,
        )
        dimension = sketch.sketchDimensions.addDistanceDimension(
            start,
            end,
            adsk.fusion.DimensionOrientations.AlignedDimensionOrientation,  # type: ignore
            text,
        )
        if not dimension or not dimension.parameter:
            raise RuntimeError("Fusion failed to create a distance dimension.")
        self._set_parameter_expression(dimension.parameter, expression)
        return dimension

    def _add_offset_dimension(
        self,
        sketch: adsk.fusion.Sketch,
        reference: adsk.fusion.SketchLine,
        line: adsk.fusion.SketchLine,
        expression: str,
        parameter_role: str,
    ) -> adsk.fusion.SketchOffsetDimension:
        text = self._sketch_line_midpoint(line)
        text.x += 0.2
        text.y += 0.2
        dimension = sketch.sketchDimensions.addOffsetDimension(
            reference,
            line,
            text,
        )
        if not dimension or not dimension.parameter:
            raise RuntimeError("Fusion failed to create an offset dimension.")
        self._set_parameter_expression(dimension.parameter, expression)
        return dimension

    def _add_circle_diameter_dimension(
        self,
        sketch: adsk.fusion.Sketch,
        circle: adsk.fusion.SketchCircle,
        expression: str,
        parameter_role: str,
    ) -> adsk.fusion.SketchDiameterDimension:
        text = circle.centerSketchPoint.geometry.copy()
        text.x += max(circle.radius * 2, 0.5)
        text.y += max(circle.radius * 2, 0.5)
        dimension = sketch.sketchDimensions.addDiameterDimension(
            circle,
            text,
        )
        if not dimension or not dimension.parameter:
            raise RuntimeError("Fusion failed to dimension a circle.")
        self._set_parameter_expression(dimension.parameter, expression)
        return dimension

    def _add_arc_radius_dimension(
        self,
        sketch: adsk.fusion.Sketch,
        arc: adsk.fusion.SketchArc,
        expression: str,
        parameter_role: str,
    ) -> adsk.fusion.SketchRadialDimension:
        text = arc.centerSketchPoint.geometry.copy()
        text.x += max(arc.radius * 2, 0.5)
        text.y += max(arc.radius * 2, 0.5)
        dimension = sketch.sketchDimensions.addRadialDimension(arc, text)
        if not dimension or not dimension.parameter:
            raise RuntimeError("Fusion failed to dimension an arc.")
        self._set_parameter_expression(dimension.parameter, expression)
        return dimension

    def _sketch_line_midpoint(
        self,
        line: adsk.fusion.SketchLine,
    ) -> adsk.core.Point3D:
        return adsk.core.Point3D.create(
            (
                line.startSketchPoint.geometry.x
                + line.endSketchPoint.geometry.x
            )
            / 2,
            (
                line.startSketchPoint.geometry.y
                + line.endSketchPoint.geometry.y
            )
            / 2,
            0,
        )

    def _extent_direction(
        self,
        sketch: adsk.fusion.Sketch,
        direction: adsk.core.Vector3D,
    ):
        sketch_normal = sketch.xDirection.crossProduct(sketch.yDirection)
        return (
            adsk.fusion.ExtentDirections.PositiveExtentDirection
            if sketch_normal.dotProduct(direction) >= 0
            else adsk.fusion.ExtentDirections.NegativeExtentDirection
        )

    def _target_body(
        self,
        component: adsk.fusion.Component,
        role: str,
    ) -> adsk.fusion.BRepBody:
        # Re-resolve via entity token: features created in between can
        # invalidate direct body references.
        entities = component.parentDesign.findEntityByToken(
            self._body_tokens[role]
        )
        body = next(
            (
                candidate
                for entity in entities
                if (candidate := adsk.fusion.BRepBody.cast(entity))
            ),
            None,
        )
        if not body:
            raise RuntimeError(f"Fusion could not re-resolve the {role} body.")
        return body

    def _resolve_face(self, role: str) -> adsk.fusion.BRepFace:
        design = adsk.fusion.Design.cast(self.app.activeProduct)
        entities = design.findEntityByToken(self._face_tokens[role])
        face = next(
            (
                candidate
                for entity in entities
                if (candidate := adsk.fusion.BRepFace.cast(entity))
            ),
            None,
        )
        if not face:
            raise RuntimeError(
                f"Fusion could not re-resolve the {role} face."
            )
        return face

    def _cut_target(
        self,
        component: adsk.fusion.Component,
        body_role: str,
        face_role: str,
    ) -> adsk.core.Base:
        """Target entity for a to-object cut: the face when it survived
        the preceding features, the owning body as the fallback."""
        try:
            return self._resolve_face(face_role)
        except RuntimeError:
            return self._target_body(component, body_role)

    def _set_parameter_expression(
        self,
        parameter: adsk.fusion.ModelParameter,
        expression: str,
    ) -> None:
        """Writes only expressions that carry a parametric link.

        Every dimension here is created on geometry that was already
        placed at the intended value, so for a pure literal the write
        changes nothing except the displayed text. An expression that
        NAMES a parameter carries a link that cannot be recovered from
        the geometry; those are always written. Each write is a document
        update costing ~0.5 s on a large assembly.
        """
        if self._expression_references_parameter(expression):
            parameter.expression = expression

    def _require_fully_constrained(
        self,
        sketch: adsk.fusion.Sketch,
    ) -> None:
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
        unconstrained_curves = [
            curve
            for curve in sketch.sketchCurves
            if not curve.isFullyConstrained
        ]

        def is_analysis_artifact(point: adsk.fusion.SketchPoint) -> bool:
            # Fusion's structural DOF analysis sometimes flags the center
            # point of an arc that it simultaneously reports as fully
            # constrained (which arc gets flagged depends on constraint
            # order; seen on the notch fillets with a non-zero axial
            # clearance). The arc's geometry is determined - its center is
            # not a real degree of freedom.
            for entity in point.connectedEntities or []:
                arc = adsk.fusion.SketchArc.cast(entity)
                if (
                    arc
                    and arc.isFullyConstrained
                    and arc.centerSketchPoint.entityToken
                    == point.entityToken
                ):
                    return True
            return False

        unconstrained_points = [
            point
            for point in sketch.sketchPoints
            if not point.isFullyConstrained
            and not is_analysis_artifact(point)
        ]
        if not unconstrained_curves and not unconstrained_points:
            return
        raise RuntimeError(
            f"'{sketch.name}' is under-constrained "
            f"({len(unconstrained_curves)} curves and "
            f"{len(unconstrained_points)} points)."
        )

    def _group_features(
        self,
        component: adsk.fusion.Component,
        first_sketch: adsk.fusion.Sketch,
        last_feature: adsk.fusion.Feature,
    ) -> None:
        group = component.parentDesign.timeline.timelineGroups.add(
            first_sketch.timelineObject.index,
            last_feature.timelineObject.index,
        )
        if group:
            group.name = "Box Joint"
            group.isCollapsed = True

    def _opposite(
        self,
        direction: adsk.core.Vector3D,
    ) -> adsk.core.Vector3D:
        result = direction.copy()
        result.scaleBy(-1)
        return result
