"""Box Joint - CNC-friendly box/finger joints as native timeline features.

Functionally modeled on the BoxJoint custom-feature add-in
(https://github.com/EvilHacker/BoxJoint/), restricted to 90-degree butt
joints, but built entirely from native Fusion features: fully constrained
sketches, join/cut extrudes, to-object extents, and rectangular feature
patterns.

The joint is built as ONE seed unit (a single notch with its reliefs and
a single gap) plus two feature patterns whose quantity and spacing are
expressions over user parameters - editing boxJointFingers in Change
Parameters re-derives the whole joint at a new finger count, and a driven
dimension of the joint length keeps everything tracking the boards. At
three fingers the fingers pattern has nothing to copy (the engine rejects
a quantity below two), so its one clamped copy is parked far off the
board and the pattern shows a harmless compute warning until the count
reaches five.

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
    zero_margin: bool
    zero_axial: bool
    zero_lateral: bool

    @property
    def has_relief(self) -> bool:
        return self.radius > _ZERO_OFFSET


@dataclass
class _ParamSet:
    """Named parameters the joint is driven by after creation.

    fingers/margin/tool/axial/lateral are USER parameters (editable in
    Change Parameters; the finger count is the headline knob). length is
    the DRIVEN model dimension measuring the joint along the corner, and
    width the model dimension deriving the finger width from it - both
    live in the notch sketch and are filled in while it is built."""
    fingers: str
    margin: str
    tool: str
    axial: str
    lateral: str
    length: str | None = None
    width: str | None = None


@dataclass(frozen=True)
class _NotchWall:
    z: float                         # wall position at creation time
    open_side: int                   # +1/-1: which z side the notch is on
    anchor: adsk.fusion.SketchPoint  # outer endpoint on the corner line
    line: adsk.fusion.SketchLine     # the notch wall line


@dataclass(frozen=True)
class _NotchLayout:
    sketch: adsk.fusion.Sketch
    walls: list[_NotchWall]          # the seed notch's two walls
    bottom_line: adsk.fusion.SketchLine | None
    direction_line: adsk.fusion.SketchLine  # pattern direction (start->end)


@dataclass(frozen=True)
class _GapWall:
    z: float
    line: adsk.fusion.SketchLine     # the gap wall (= finger side)
    tip: adsk.fusion.SketchPoint     # its end on the finger-tip line


@dataclass(frozen=True)
class _GapLayout:
    sketch: adsk.fusion.Sketch
    walls: list[_GapWall]            # the seed gap's two walls
    bottom_line: adsk.fusion.SketchLine


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
        # One parameter prefix per command invocation: preview cycles then
        # update the same user parameters instead of minting new ones.
        self._session_prefix = None
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
        return _JointSpec(
            count=count,
            finger_width=width,
            margin=margin,
            axial=axial,
            lateral=lateral,
            radius=radius if radius > _ZERO_OFFSET else 0.0,
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
        design = component.parentDesign
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

        params = self._create_user_parameters(design, spec)

        notch = self._create_notch_sketch(component, geometry, spec, params)
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
                params,
            )
            self._require_fully_constrained(groove_sketch)
            notch_relief_sketch = self._create_notch_relief_sketch(
                component,
                geometry,
                spec,
                notch,
                params,
            )
            self._require_fully_constrained(notch_relief_sketch)

        strip_sketch = self._create_strip_sketch(
            component,
            geometry,
            spec,
            params,
        )
        self._require_fully_constrained(strip_sketch)

        gaps = self._create_gap_sketch(component, geometry, spec, params)
        self._require_fully_constrained(gaps.sketch)

        if spec.has_relief:
            finger_groove_sketch = self._create_finger_groove_sketch(
                component,
                geometry,
                spec,
                params,
            )
            self._require_fully_constrained(finger_groove_sketch)
            relief_sketch = self._create_root_relief_sketch(
                component,
                geometry,
                spec,
                gaps,
                params,
            )
            self._require_fully_constrained(relief_sketch)

        # Give the finger board the joint span (first to last notch wall),
        # then carve the gaps back out of it. The span deliberately stops
        # at the outer notch walls: the end gaps then only recess the seat
        # in B's original body, so their outer kept fillets stay above the
        # notch board and the pattern can use one uniform gap shape.
        strip_extrude = self._create_to_entity_extrude(
            component=component,
            sketch=strip_sketch,
            target_body=self._target_body(component, "b"),
            target_entity=self._resolve_face("face_a"),
            direction=self._opposite(geometry.y_dir),
            offset_expression=None,
            operation=adsk.fusion.FeatureOperations.NewBodyFeatureOperation,  # type: ignore
            name="Box Joint - Finger Stock",
            parameter_role="fingerStock",
        )
        self._create_join_combine(
            component,
            self._target_body(component, "b"),
            cast(
                list[adsk.fusion.BRepBody],
                utils.fusion.as_list(strip_extrude.bodies),
            ),
        )

        gap_cut = self._create_to_entity_extrude(
            component=component,
            sketch=gaps.sketch,
            target_body=self._target_body(component, "b"),
            target_entity=self._cut_target(component, "b", "b_inside"),
            direction=geometry.x_dir,
            offset_expression=None,
            operation=adsk.fusion.FeatureOperations.CutFeatureOperation,  # type: ignore
            name="Box Joint - Gap Cut",
            parameter_role="gap",
        )
        self._create_pattern(
            component,
            [gap_cut],
            notch.direction_line,
            f"({params.fingers} + 1) / 2",
            f"2 * ({params.width})",
            "Box Joint - Gaps Pattern",
        )

        finger_features: list[adsk.fusion.Feature] = []
        finger_features.append(
            self._create_to_entity_extrude(
                component=component,
                sketch=notch.sketch,
                target_body=self._target_body(component, "a"),
                target_entity=self._cut_target(component, "a", "a_inside"),
                direction=geometry.y_dir,
                offset_expression=None,
                operation=adsk.fusion.FeatureOperations.CutFeatureOperation,  # type: ignore
                name="Box Joint - Notch Cut",
                parameter_role="notch",
            )
        )
        if spec.has_relief:
            assert (
                groove_sketch
                and notch_relief_sketch
                and finger_groove_sketch
                and relief_sketch
            )
            finger_features.append(
                self._create_to_entity_extrude(
                    component=component,
                    sketch=groove_sketch,
                    target_body=self._target_body(component, "a"),
                    target_entity=self._cut_target(
                        component, "a", "b_inside"),
                    direction=geometry.x_dir,
                    offset_expression=f"({params.lateral})",
                    operation=adsk.fusion.FeatureOperations.CutFeatureOperation,  # type: ignore
                    name="Box Joint - Wall Grooves Cut",
                    parameter_role="wallGrooves",
                )
            )
            finger_features.append(
                self._create_distance_extrude(
                    component=component,
                    sketch=notch_relief_sketch,
                    target_body=self._target_body(component, "a"),
                    direction=self._opposite(geometry.y_dir),
                    distance=f"({params.tool}) / 2",
                    operation=adsk.fusion.FeatureOperations.CutFeatureOperation,  # type: ignore
                    name="Box Joint - Notch Reliefs Cut",
                    parameter_role="notchReliefs",
                )
            )
            finger_features.append(
                self._create_to_entity_extrude(
                    component=component,
                    sketch=finger_groove_sketch,
                    target_body=self._target_body(component, "b"),
                    target_entity=self._cut_target(
                        component, "b", "a_inside"),
                    direction=geometry.y_dir,
                    offset_expression=(
                        f"({params.lateral}) - ({params.tool}) / 2"
                    ),
                    operation=adsk.fusion.FeatureOperations.CutFeatureOperation,  # type: ignore
                    name="Box Joint - Finger Grooves Cut",
                    parameter_role="fingerGrooves",
                )
            )
            finger_features.append(
                self._create_distance_extrude(
                    component=component,
                    sketch=relief_sketch,
                    target_body=self._target_body(component, "b"),
                    direction=self._opposite(geometry.x_dir),
                    distance=f"({params.tool}) / 2",
                    operation=adsk.fusion.FeatureOperations.CutFeatureOperation,  # type: ignore
                    name="Box Joint - Root Reliefs Cut",
                    parameter_role="rootReliefs",
                )
            )
        finger_pattern = self._create_pattern(
            component,
            finger_features,
            notch.direction_line,
            # The pattern engine rejects a quantity of one, so three
            # fingers clamp to two instances - and the spacing then jumps
            # by 10 m, parking the extra copy far off the board instead of
            # letting it bite the margins. A pattern whose only copy is
            # empty reports a compute error while leaving the (correct)
            # seed geometry alone, so that state is tolerated: the flag
            # clears itself as soon as the finger count reaches five.
            f"max(({params.fingers} - 1) / 2 ; 2)",
            (
                f"2 * ({params.width}) + "
                f"max(2 - ({params.fingers} - 1) / 2 ; 0) * 10 m"
            ),
            "Box Joint - Fingers Pattern",
            tolerate_empty=spec.count == 3,
            # Half a cell over: every patterned feature's copy then hits
            # virgin material somewhere (the pattern engine wants at least
            # one intersecting copy PER feature, and at one-cell spacing
            # the finger-side cuts land exactly on already-cut regions).
            placeholder_spacing=f"({params.width}) / 2",
        )

        self._group_features(component, notch.sketch, finger_pattern)

    # ------------------------------------------------------------------
    # Parameters
    # ------------------------------------------------------------------

    def _create_user_parameters(
        self,
        design: adsk.fusion.Design,
        spec: _JointSpec,
    ) -> _ParamSet:
        """The joint's editable knobs as named user parameters.

        boxJointFingers is the headline one: every sketch dimension and
        both pattern quantities/spacings are expressions over these, so
        editing a parameter in Change Parameters re-derives the whole
        joint - including the finger count. The prefix is chosen once per
        command invocation so preview cycles reuse the same parameters
        instead of minting boxJoint2, boxJoint3, ...
        """
        prefix = getattr(self, "_session_prefix", None)
        if not prefix:
            names = {
                parameter.name for parameter in design.allParameters
            }
            index = 1
            while True:
                candidate = (
                    "boxJoint" if index == 1 else f"boxJoint{index}"
                )
                if f"{candidate}Fingers" not in names:
                    break
                index += 1
            prefix = candidate
            self._session_prefix = prefix
        units = design.unitsManager.defaultLengthUnits

        def ensure(name: str, expression: str, unit: str, comment: str) -> str:
            parameter = design.userParameters.itemByName(name)
            if parameter:
                parameter.expression = expression
                return parameter.name
            parameter = design.userParameters.add(
                name,
                adsk.core.ValueInput.createByString(expression),
                unit,
                comment,
            )
            if not parameter:
                raise RuntimeError(
                    f"Fusion failed to create the parameter '{name}'."
                )
            return parameter.name

        return _ParamSet(
            fingers=ensure(
                f"{prefix}Fingers",
                str(spec.count),
                "",
                "Box Joint: total number of fingers (keep it odd)",
            ),
            margin=ensure(
                f"{prefix}Margin",
                self.inputs.margin.expression,
                units,
                "Box Joint: plain margin at both joint ends",
            ),
            tool=ensure(
                f"{prefix}ToolDiameter",
                self.inputs.tool_diameter.expression,
                units,
                "Box Joint: CNC bit diameter driving the hidden reliefs",
            ),
            axial=ensure(
                f"{prefix}ClearanceAxial",
                self.inputs.clearance_axial.expression,
                units,
                "Box Joint: clearance along the joint",
            ),
            lateral=ensure(
                f"{prefix}ClearanceLateral",
                self.inputs.clearance_lateral.expression,
                units,
                "Box Joint: clearance across the joint",
            ),
        )

    # ------------------------------------------------------------------
    # Sketch: the seed notch on the notch board's outside face
    # ------------------------------------------------------------------

    def _create_notch_sketch(
        self,
        component: adsk.fusion.Component,
        geometry: _ResolvedGeometry,
        spec: _JointSpec,
        params: _ParamSet,
    ) -> _NotchLayout:
        sketch = component.sketches.addWithoutEdges(geometry.face_a)
        if not sketch:
            raise RuntimeError(
                "Fusion failed to create 'Box Joint - Notch'."
            )
        sketch.name = "Box Joint - Notch"

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

        # DRIVEN joint length between the projected shoulder vertices: the
        # one measured value everything else is derived from, so the joint
        # re-derives when the boards change.
        text = anchor_start.geometry.copy()
        text.x += 0.5
        text.y += 0.5
        driven = sketch.sketchDimensions.addDistanceDimension(
            anchor_start,
            anchor_end,
            adsk.fusion.DimensionOrientations.AlignedDimensionOrientation,  # type: ignore
            text,
            False,
        )
        if not driven or not driven.parameter:
            raise RuntimeError(
                "Fusion failed to measure the joint length."
            )
        params.length = driven.parameter.name

        # The finger-width construction line doubles as the patterns'
        # direction entity: a pattern along a sketch line runs from its
        # start point towards its end point (verified), so anchoring the
        # start at the joint start makes the direction deterministic.
        width_line = lines.addByTwoPoints(
            anchor_start,
            to_sketch(0, spec.finger_width),
        )
        if not width_line:
            raise RuntimeError(
                "Fusion failed to create the finger width line."
            )
        width_line.isConstruction = True
        constraints.addCoincident(width_line.endSketchPoint, corner_line)
        width_dimension = self._add_line_length_dimension(
            sketch,
            width_line,
            f"(({params.length}) - 2 * ({params.margin}))"
            f" / ({params.fingers})",
            "fingerWidth",
        )
        params.width = width_dimension.parameter.name

        radius = spec.radius
        depth = geometry.thickness_b + spec.lateral
        left_z = spec.margin + spec.finger_width - spec.axial / 2
        right_z = spec.margin + 2 * spec.finger_width + spec.axial / 2

        step = lines.addByTwoPoints(anchor_start, to_sketch(0, left_z))
        if not step:
            raise RuntimeError(
                "Fusion failed to position the seed notch."
            )
        step.isConstruction = True
        constraints.addCoincident(step.endSketchPoint, corner_line)
        self._add_line_length_dimension(
            sketch,
            step,
            f"({params.margin}) + ({params.width}) - ({params.axial}) / 2",
            "notchPosition",
        )

        wall_l = lines.addByTwoPoints(
            step.endSketchPoint,
            to_sketch(depth - radius, left_z),
        )
        wall_r = lines.addByTwoPoints(
            to_sketch(0, right_z),
            to_sketch(depth - radius, right_z),
        )
        if not wall_l or not wall_r:
            raise RuntimeError("Fusion failed to create the notch walls.")
        outer = lines.addByTwoPoints(
            wall_r.startSketchPoint,
            wall_l.startSketchPoint,
        )
        if not outer:
            raise RuntimeError("Fusion failed to close the notch profile.")
        constraints.addPerpendicular(wall_l, corner_line)
        constraints.addPerpendicular(wall_r, corner_line)
        constraints.addCoincident(wall_r.startSketchPoint, corner_line)
        self._add_offset_dimension(
            sketch,
            wall_l,
            wall_r,
            f"({params.width}) + ({params.axial})",
            "notchWidth",
        )

        bottom = lines.addByTwoPoints(
            to_sketch(depth, left_z + radius),
            to_sketch(depth, right_z - radius),
        )
        if not bottom:
            raise RuntimeError("Fusion failed to create the notch bottom.")
        if spec.zero_lateral:
            # An offset dimension between coincident lines is degenerate.
            constraints.addCollinear(inner_line, bottom)
        else:
            constraints.addParallel(bottom, corner_line)
            self._add_offset_dimension(
                sketch,
                inner_line,
                bottom,
                f"({params.lateral})",
                "lateralClearance",
            )

        if radius <= 0:
            constraints.addCoincident(
                wall_l.endSketchPoint,
                bottom.startSketchPoint,
            )
            constraints.addCoincident(
                wall_r.endSketchPoint,
                bottom.endSketchPoint,
            )
        else:
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
            for fillet in (fillet_l, fillet_r):
                self._add_arc_radius_dimension(
                    sketch,
                    fillet,
                    f"({params.tool}) / 2",
                    "bitRadius",
                )

        sketch.isComputeDeferred = False
        return _NotchLayout(
            sketch=sketch,
            walls=[
                _NotchWall(
                    z=left_z,
                    open_side=1,
                    anchor=step.endSketchPoint,
                    line=wall_l,
                ),
                _NotchWall(
                    z=right_z,
                    open_side=-1,
                    anchor=wall_r.startSketchPoint,
                    line=wall_r,
                ),
            ],
            bottom_line=bottom,
            direction_line=width_line,
        )


    # ------------------------------------------------------------------
    # Sketch: wall grooves on the notch board's end face
    # ------------------------------------------------------------------

    def _create_wall_groove_sketch(
        self,
        component: adsk.fusion.Component,
        geometry: _ResolvedGeometry,
        spec: _JointSpec,
        notch: _NotchLayout,
        params: _ParamSet,
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
                # Open the groove into the notch so it clears the kept
                # bottom-corner fillet near the inside face.
                (projected, wall.z, wall.open_side)
                for projected, wall in zip(wall_points, notch.walls)
            ],
            to_sketch,
            surface,
            radius,
            f"({params.tool}) / 2",
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
        params: _ParamSet,
    ) -> _GapLayout:
        """The seed gap on the finger board's outside face.

        One closed gap shape with kept fillets at both bottom corners; the
        gaps pattern replicates it over every second cell. The end
        instances extend past the finger stock, where their outer fillets
        keep only material above the notch board's inside face - harmless,
        so no end special-casing is needed."""
        sketch = component.sketches.addWithoutEdges(geometry.face_b)
        if not sketch:
            raise RuntimeError(
                "Fusion failed to create 'Box Joint - Gap'."
            )
        sketch.name = "Box Joint - Gap"

        # The projected corner edge stays a REGULAR curve: it is the
        # tip-side boundary of the gap profile.
        tip_line = self._project_line(sketch, geometry.corner_edge)
        shoulder_line = self._project_line(sketch, geometry.shoulder_edge)
        shoulder_line.isConstruction = True
        anchor_start = self._project_point(
            sketch,
            geometry.shoulder_edge.startVertex,
        )

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
        left_z = spec.margin - spec.axial / 2
        right_z = spec.margin + spec.finger_width + spec.axial / 2

        # Position the right wall from the joint start; the left wall
        # hangs off it through the width dimension.
        step = lines.addByTwoPoints(
            anchor_start,
            to_sketch(geometry.thickness_a, right_z),
        )
        if not step:
            raise RuntimeError("Fusion failed to position the seed gap.")
        step.isConstruction = True
        constraints.addCoincident(step.endSketchPoint, shoulder_line)
        self._add_line_length_dimension(
            sketch,
            step,
            f"({params.margin}) + ({params.width}) + ({params.axial}) / 2",
            "gapPosition",
        )

        wall_r = lines.addByTwoPoints(
            to_sketch(0, right_z),
            to_sketch(seat - radius, right_z),
        )
        wall_l = lines.addByTwoPoints(
            to_sketch(0, left_z),
            to_sketch(seat - radius, left_z),
        )
        if not wall_l or not wall_r:
            raise RuntimeError("Fusion failed to create the gap walls.")
        constraints.addPerpendicular(wall_r, shoulder_line)
        constraints.addPerpendicular(wall_l, shoulder_line)
        constraints.addCoincident(step.endSketchPoint, wall_r)
        constraints.addCoincident(wall_r.startSketchPoint, tip_line)
        constraints.addCoincident(wall_l.startSketchPoint, tip_line)
        self._add_offset_dimension(
            sketch,
            wall_r,
            wall_l,
            f"({params.width}) + ({params.axial})",
            "gapWidth",
        )

        bottom = lines.addByTwoPoints(
            to_sketch(seat, left_z + radius),
            to_sketch(seat, right_z - radius),
        )
        if not bottom:
            raise RuntimeError("Fusion failed to create the gap bottom.")
        if spec.zero_lateral:
            constraints.addCollinear(shoulder_line, bottom)
        else:
            constraints.addParallel(bottom, shoulder_line)
            self._add_offset_dimension(
                sketch,
                shoulder_line,
                bottom,
                f"({params.lateral})",
                "gapLateralClearance",
            )

        if radius <= 0:
            constraints.addCoincident(
                wall_l.endSketchPoint,
                bottom.startSketchPoint,
            )
            constraints.addCoincident(
                wall_r.endSketchPoint,
                bottom.endSketchPoint,
            )
        else:
            diagonal = radius - radius / math.sqrt(2)
            fillet_l = arcs.addByThreePoints(
                bottom.startSketchPoint,
                to_sketch(seat - diagonal, left_z + diagonal),
                wall_l.endSketchPoint,
            )
            fillet_r = arcs.addByThreePoints(
                bottom.endSketchPoint,
                to_sketch(seat - diagonal, right_z - diagonal),
                wall_r.endSketchPoint,
            )
            if not fillet_l or not fillet_r:
                raise RuntimeError(
                    "Fusion failed to create a gap corner fillet."
                )
            constraints.addTangent(fillet_l, wall_l)
            constraints.addTangent(fillet_l, bottom)
            constraints.addTangent(fillet_r, bottom)
            constraints.addTangent(fillet_r, wall_r)
            for fillet in (fillet_l, fillet_r):
                self._add_arc_radius_dimension(
                    sketch,
                    fillet,
                    f"({params.tool}) / 2",
                    "gapFilletRadius",
                )

        sketch.isComputeDeferred = False
        return _GapLayout(
            sketch=sketch,
            walls=[
                _GapWall(
                    z=left_z,
                    line=wall_l,
                    tip=wall_l.startSketchPoint,
                ),
                _GapWall(
                    z=right_z,
                    line=wall_r,
                    tip=wall_r.startSketchPoint,
                ),
            ],
            bottom_line=bottom,
        )

    # ------------------------------------------------------------------
    # Sketch: finger grooves on the finger-tip plane
    # ------------------------------------------------------------------

    def _create_finger_groove_sketch(
        self,
        component: adsk.fusion.Component,
        geometry: _ResolvedGeometry,
        spec: _JointSpec,
        params: _ParamSet,
    ) -> adsk.fusion.Sketch:
        sketch = component.sketches.addWithoutEdges(geometry.face_a)
        if not sketch:
            raise RuntimeError(
                "Fusion failed to create 'Box Joint - Finger Grooves'."
            )
        sketch.name = "Box Joint - Finger Grooves"

        inner_line = self._project_line(sketch, geometry.inner_edge)
        inner_line.isConstruction = True
        corner_line = self._project_line(sketch, geometry.corner_edge)
        corner_line.isConstruction = True
        anchor_start = self._project_point(
            sketch,
            geometry.shoulder_edge.startVertex,
        )

        sketch.isComputeDeferred = True
        constraints = sketch.geometricConstraints
        lines = sketch.sketchCurves.sketchLines

        def to_sketch(x: float, z: float) -> adsk.core.Point3D:
            return sketch.modelToSketchSpace(
                self._joint_point(geometry, x, 0, z)
            )

        # The seed finger's two side positions, dimension-driven from the
        # joint start.
        sites: list[tuple[adsk.fusion.SketchPoint, float, int]] = []
        for expression, z, role in (
            (
                f"({params.margin}) + ({params.width})"
                f" + ({params.axial}) / 2",
                spec.margin + spec.finger_width + spec.axial / 2,
                "fingerGroovePositionLeft",
            ),
            (
                f"({params.margin}) + 2 * ({params.width})"
                f" - ({params.axial}) / 2",
                spec.margin + 2 * spec.finger_width - spec.axial / 2,
                "fingerGroovePositionRight",
            ),
        ):
            step = lines.addByTwoPoints(anchor_start, to_sketch(0, z))
            if not step:
                raise RuntimeError(
                    "Fusion failed to position a finger groove."
                )
            step.isConstruction = True
            constraints.addCoincident(step.endSketchPoint, corner_line)
            self._add_line_length_dimension(sketch, step, expression, role)
            sites.append((step.endSketchPoint, z, 0))

        self._add_lens_grooves(
            sketch,
            inner_line,
            sites,
            to_sketch,
            geometry.thickness_b,
            spec.radius,
            f"({params.tool}) / 2",
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
        gaps: _GapLayout,
        params: _ParamSet,
    ) -> adsk.fusion.Sketch:
        sketch = component.sketches.addWithoutEdges(geometry.b_inside)
        if not sketch:
            raise RuntimeError(
                "Fusion failed to create 'Box Joint - Root Reliefs'."
            )
        sketch.name = "Box Joint - Root Reliefs"

        bottom_line = self._project_line(sketch, gaps.bottom_line)
        bottom_line.isConstruction = True
        # The seed gap's right wall is the seed finger's left side; the
        # finger's right side hangs off it by width - axial.
        right_wall = max(gaps.walls, key=lambda wall: wall.z)
        wall_line = self._project_line(sketch, right_wall.line)
        wall_line.isConstruction = True

        sketch.isComputeDeferred = True
        constraints = sketch.geometricConstraints
        radius = spec.radius
        center_y = geometry.thickness_a + spec.lateral - radius

        circle_l = sketch.sketchCurves.sketchCircles.addByCenterRadius(
            sketch.modelToSketchSpace(
                self._joint_point(
                    geometry,
                    geometry.thickness_b,
                    center_y,
                    right_wall.z,
                )
            ),
            radius,
        )
        if not circle_l:
            raise RuntimeError(
                "Fusion failed to create a root relief circle."
            )
        constraints.addCoincident(circle_l.centerSketchPoint, wall_line)
        constraints.addTangent(circle_l, bottom_line)
        self._add_circle_diameter_dimension(
            sketch,
            circle_l,
            f"({params.tool})",
            "rootReliefDiameter",
        )

        span = sketch.sketchCurves.sketchLines.addByTwoPoints(
            circle_l.centerSketchPoint,
            sketch.modelToSketchSpace(
                self._joint_point(
                    geometry,
                    geometry.thickness_b,
                    center_y,
                    right_wall.z + spec.finger_width - spec.axial,
                )
            ),
        )
        if not span:
            raise RuntimeError(
                "Fusion failed to span the root relief pair."
            )
        span.isConstruction = True
        constraints.addParallel(span, bottom_line)
        self._add_line_length_dimension(
            sketch,
            span,
            f"({params.width}) - ({params.axial})",
            "rootReliefSpan",
        )

        circle_r = sketch.sketchCurves.sketchCircles.addByCenterRadius(
            span.endSketchPoint.geometry,
            radius,
        )
        if not circle_r:
            raise RuntimeError(
                "Fusion failed to create a root relief circle."
            )
        constraints.addCoincident(
            circle_r.centerSketchPoint,
            span.endSketchPoint,
        )
        self._add_circle_diameter_dimension(
            sketch,
            circle_r,
            f"({params.tool})",
            "rootReliefDiameter",
        )
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
        params: _ParamSet,
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
            self._add_circle_diameter_dimension(
                sketch,
                circle,
                f"({params.tool})",
                "notchReliefDiameter",
            )
        sketch.isComputeDeferred = False
        return sketch

    # ------------------------------------------------------------------
    # Features
    # ------------------------------------------------------------------

    def _create_strip_sketch(
        self,
        component: adsk.fusion.Component,
        geometry: _ResolvedGeometry,
        spec: _JointSpec,
        params: _ParamSet,
    ) -> adsk.fusion.Sketch:
        """Profile of the finger stock on B's butting end face.

        Spans from the first to the last notch wall, so the patterned end
        gaps only ever recess the seat in B's original body."""
        sketch = component.sketches.addWithoutEdges(geometry.b_end)
        if not sketch:
            raise RuntimeError(
                "Fusion failed to create 'Box Joint - Finger Stock'."
            )
        sketch.name = "Box Joint - Finger Stock"

        outer_line = self._project_line(sketch, geometry.shoulder_edge)
        outer_line.isConstruction = True
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
                self._joint_point(geometry, x, geometry.thickness_a, z)
            )

        # One bit radius PAST the outer notch walls: the end gap
        # instances carve that excess back but keep the first and last
        # finger's outer root fillet whole.
        inset = (
            "({margin}) + ({width}) - ({axial}) / 2 - ({tool}) / 2".format(
                margin=params.margin,
                width=params.width,
                axial=params.axial,
                tool=params.tool,
            )
        )
        start_z = (
            spec.margin + spec.finger_width - spec.axial / 2 - spec.radius
        )
        end_z = geometry.joint_length - start_z

        # The long sides come first, collinear with the projected board
        # edges; the steps and short sides then consume exactly their
        # remaining degrees of freedom (dimensioning a finished
        # point-to-point rectangle instead leaves the analyzer flagging
        # the long sides while rejecting further constraints).
        long_outer = lines.addByTwoPoints(
            to_sketch(0, start_z),
            to_sketch(0, end_z),
        )
        long_inner = lines.addByTwoPoints(
            to_sketch(geometry.thickness_b, start_z),
            to_sketch(geometry.thickness_b, end_z),
        )
        if not long_outer or not long_inner:
            raise RuntimeError(
                "Fusion failed to create the finger stock profile."
            )
        constraints.addCollinear(outer_line, long_outer)
        constraints.addCollinear(inner_line, long_inner)

        for anchor, endpoint in (
            (anchor_start, long_outer.startSketchPoint),
            (anchor_end, long_outer.endSketchPoint),
        ):
            step = lines.addByTwoPoints(anchor, endpoint)
            if not step:
                raise RuntimeError(
                    "Fusion failed to position the finger stock."
                )
            step.isConstruction = True
            self._add_line_length_dimension(
                sketch,
                step,
                inset,
                "fingerStockInset",
            )

        side_start = lines.addByTwoPoints(
            long_outer.startSketchPoint,
            long_inner.startSketchPoint,
        )
        side_end = lines.addByTwoPoints(
            long_outer.endSketchPoint,
            long_inner.endSketchPoint,
        )
        if not side_start or not side_end:
            raise RuntimeError(
                "Fusion failed to create the finger stock sides."
            )
        constraints.addPerpendicular(side_start, outer_line)
        constraints.addPerpendicular(side_end, outer_line)
        sketch.isComputeDeferred = False
        return sketch

    def _create_pattern(
        self,
        component: adsk.fusion.Component,
        features: list[adsk.fusion.Feature],
        direction_line: adsk.fusion.SketchLine,
        quantity_expression: str,
        spacing_expression: str,
        name: str,
        tolerate_empty: bool = False,
        placeholder_spacing: str | None = None,
    ) -> adsk.fusion.RectangularPatternFeature:
        """Feature pattern along the joint (direction: line start->end).

        Quantity and spacing are expressions over the joint's user
        parameters, so editing boxJointFingers re-derives the pattern.
        AdjustPatternCompute re-evaluates every instance: the end gap
        instances produce non-identical results, and instances that leave
        the boards entirely are silently skipped (verified) - which the
        three-finger case relies on."""
        entities = adsk.core.ObjectCollection.createWithArray(
            cast(list[adsk.core.Base], features)
        )
        patterns = component.features.rectangularPatternFeatures
        pattern_input = patterns.createInput(
            entities,
            direction_line,
            adsk.core.ValueInput.createByString(quantity_expression),
            adsk.core.ValueInput.createByString(spacing_expression),
            adsk.fusion.PatternDistanceType.SpacingPatternDistanceType,  # type: ignore
        )
        if not pattern_input:
            raise RuntimeError(f"Fusion failed to initialize '{name}'.")
        pattern_input.patternComputeOption = (
            adsk.fusion.PatternComputeOptions.AdjustPatternCompute  # type: ignore
        )
        try:
            pattern = patterns.add(pattern_input)
        except RuntimeError:
            if not tolerate_empty:
                raise
            # Adding a pattern whose every copy is empty is refused
            # outright. Add it with a one-cell placeholder spacing whose
            # copy genuinely cuts, then swap in the real expressions: the
            # recompute parks the copy off the board again, which an
            # EXISTING pattern tolerates (it merely reports a warning
            # until the finger count reaches five).
            placeholder = patterns.createInput(
                entities,
                direction_line,
                adsk.core.ValueInput.createByString("2"),
                adsk.core.ValueInput.createByString(
                    cast(str, placeholder_spacing)
                ),
                adsk.fusion.PatternDistanceType.SpacingPatternDistanceType,  # type: ignore
            )
            placeholder.patternComputeOption = (
                adsk.fusion.PatternComputeOptions.AdjustPatternCompute  # type: ignore
            )
            pattern = patterns.add(placeholder)
            pattern.quantityOne.expression = quantity_expression
            pattern.distanceOne.expression = spacing_expression
        if not pattern:
            raise RuntimeError(f"Fusion failed to create '{name}'.")
        pattern.name = name
        healthy = adsk.fusion.FeatureHealthStates.HealthyFeatureHealthState
        if pattern.healthState != healthy and not tolerate_empty:
            try:
                message = pattern.errorOrWarningMessage
            except Exception:
                message = "unhealthy pattern"
            raise RuntimeError(f"'{name}' failed to compute: {message}")
        return pattern

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
