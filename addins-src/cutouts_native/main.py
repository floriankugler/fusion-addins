import math
import os
from dataclasses import dataclass
from typing import cast

import adsk.core
import adsk.fusion

from lib import addin, inputs, ui_placement, utils
from lib.fusionbootstrap.runtime import RuntimeInfo


_addin: addin.Addin | None = None


@dataclass(frozen=True)
class _SeedTriangle:
    base: adsk.fusion.SketchLine
    altitude: adsk.fusion.SketchLine
    right_side: adsk.fusion.SketchLine
    left_side: adsk.fusion.SketchLine
    midpoint: adsk.fusion.SketchPoint
    apex: adsk.fusion.SketchPoint


@dataclass(frozen=True)
class _FaceTarget:
    face: adsk.fusion.BRepFace
    opposite_face: adsk.fusion.BRepFace
    target_body: adsk.fusion.BRepBody
    cut_direction: adsk.core.Vector3D


@dataclass(frozen=True)
class _BodyLocator:
    minimum: tuple[float, float, float]
    maximum: tuple[float, float, float]
    volume: float


@dataclass
class _BodyCut:
    target_body_locator: _BodyLocator
    tool_body_locators: list[_BodyLocator]


@dataclass(frozen=True)
class _SeedRhombus:
    center: adsk.fusion.SketchPoint
    horizontal: adsk.fusion.SketchLine
    vertical: adsk.fusion.SketchLine
    left_top: adsk.fusion.SketchLine
    top_right: adsk.fusion.SketchLine
    right_bottom: adsk.fusion.SketchLine
    bottom_left: adsk.fusion.SketchLine


@dataclass(frozen=True)
class _PatternBoundary:
    """The oriented rectangle every pattern is laid out in. It comes either
    from the offset outer loop of a rectangular face or from the user's
    Pattern Axis and Bounding Box Points."""

    origin: adsk.fusion.SketchPoint
    u_direction: adsk.fusion.SketchLine
    v_direction: adsk.fusion.SketchLine
    extent_u: float
    extent_v: float
    u_parameter: adsk.fusion.ModelParameter
    v_parameter: adsk.fusion.ModelParameter
    u_vector: adsk.core.Vector3D
    v_vector: adsk.core.Vector3D
    corners: list[adsk.fusion.SketchPoint]
    boundary_lines: list[adsk.fusion.SketchLine]


def run(context, runtime_info: RuntimeInfo):
    global _addin
    _addin = CutoutsNative(runtime_info)
    # Dev support: allow external tooling to restart this add-in by firing the
    # custom event '<id>_reload' (see lib/fusionbootstrap/reloader.py).
    from lib.fusionbootstrap import reloader
    entry = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "cutouts_native.py",
    )
    reloader.ensure(runtime_info.id + "_reload", entry)


def stop(context):
    global _addin
    if _addin:
        _addin.shutdown()
    _addin = None


class CutoutsNativeInputs(inputs.Inputs):
    FULL_CUTOUT = inputs.DropDownInput.Item("Full Cutout", 0)
    TRIANGLES = inputs.DropDownInput.Item("Triangles", 1)
    CROSS = inputs.DropDownInput.Item("Cross", 2)
    RHOMBUSES = inputs.DropDownInput.Item("Rhombuses", 3)

    def __init__(self, units_manager: adsk.core.UnitsManager):
        units = units_manager.defaultLengthUnits

        self.face = inputs.SelectionByEntityTokenInput(
            id="face",
            name="Faces",
            filter=["PlanarFaces"],
            lower_bound=1,
            upper_bound=0,
            tool_tip=(
                "Select one or more parallel planar faces. The first face "
                "defines the shared cutout sketches."
            ),
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
            options=[
                self.FULL_CUTOUT,
                self.TRIANGLES,
                self.CROSS,
                self.RHOMBUSES,
            ],
            default_value=self.FULL_CUTOUT.value,
            tool_tip=(
                "Create one full cutout, a triangle or rhombus pattern, or "
                "four cutout wedges that leave a diagonal cross."
            ),
        )
        triangle_input_visible = lambda: (
            self.pattern_type.value == self.TRIANGLES.value
        )
        # Columns, Rows and Spacing drive both tiled patterns.
        grid_input_visible = lambda: self.pattern_type.value in (
            self.TRIANGLES.value,
            self.RHOMBUSES.value,
        )
        self.pattern_axis = inputs.SelectionByEntityTokenInput(
            id="pattern_axis",
            name="Pattern Axis",
            filter=["LinearEdges", "SketchLines", "ConstructionLines"],
            lower_bound=0,
            upper_bound=1,
            tool_tip=(
                "Optional direction the bounding box and pattern are "
                "aligned to. Without it the box is aligned to the sketch "
                "axes. Only used together with Bounding Box Points, except "
                "on a rectangular face, where it picks the pattern "
                "direction."
            ),
        )
        self.bounding_points = inputs.SelectionByEntityTokenInput(
            id="bounding_points",
            name="Bounding Box Points",
            filter=["Vertices", "SketchPoints", "ConstructionPoints"],
            lower_bound=0,
            upper_bound=4,
            tool_tip=(
                "Optional: select two to four points that define the "
                "bounding box extremes. The cutout is limited to this box. "
                "Point order does not matter."
            ),
        )
        self.inset_bounding_box = inputs.CheckboxInput(
            id="inset_bounding_box",
            name="Inset Bounding Box",
            default_value=False,
            tool_tip=(
                "Apply the Outer Inset to the rectangle defined by the "
                "Bounding Box Points as well, instead of only to the outer "
                "contour of the selected face."
            ),
            update_visibility=lambda: len(self.bounding_points.value) >= 2,
        )
        self.triangle_columns = inputs.IntegerInput(
            id="triangle_columns",
            name="Columns",
            default_value=8,
            minimum=1,
            maximum=100,
            tool_tip=(
                "Number of pattern columns along the Pattern Axis. The "
                "first and last are halved by the boundary."
            ),
            update_visibility=grid_input_visible,
        )
        self.triangle_rows = inputs.IntegerInput(
            id="triangle_rows",
            name="Rows",
            default_value=6,
            minimum=1,
            maximum=100,
            tool_tip="Number of pattern rows perpendicular to the Pattern Axis.",
            update_visibility=grid_input_visible,
        )
        self.triangle_spacing = inputs.FloatInput(
            id="triangle_spacing",
            name="Spacing",
            default_value=2,
            tool_tip="True edge-to-edge clearance between adjacent cutouts.",
            units=units,
            update_visibility=grid_input_visible,
        )
        self.triangle_spacing.minimum_value = 0
        self.triangle_spacing.minimum_inclusive = False
        self.align_triangles = inputs.CheckboxInput(
            id="align_triangles",
            name="Align Triangles",
            default_value=False,
            tool_tip=(
                "Round triangle tips in the seed sketch and align each rounded "
                "tip tangent to the neighboring triangle baseline."
            ),
            update_visibility=triangle_input_visible,
        )
        self.cross_width = inputs.FloatInput(
            id="cross_width",
            name="Cross Width",
            default_value=2,
            tool_tip="Width of each diagonal material band in the cross.",
            units=units,
            update_visibility=lambda: (
                self.pattern_type.value == self.CROSS.value
            ),
        )
        self.cross_width.minimum_value = 0
        self.cross_width.minimum_inclusive = False

        super().__init__()


class CutoutsNative(addin.Addin):
    inputs: CutoutsNativeInputs
    _parameter_prefix: str
    _remainder_parameter_name: str | None = None
    #: Parameter of the outer-contour inset, so the optional bounding-box
    #: inset can be driven by the same value instead of a duplicate.
    _outer_inset_parameter: adsk.fusion.ModelParameter | None = None

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
    def plugin_name(self) -> str:
        return "Face Cutout (Native)"

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

    def create_inputs(self) -> CutoutsNativeInputs:
        design = adsk.fusion.Design.cast(self.app.activeProduct)
        if not design:
            raise RuntimeError("Face Cutout (Native) requires an active Fusion design.")
        return CutoutsNativeInputs(design.unitsManager)

    def pre_select(self, input, selection) -> bool:
        if not self.inputs or not input:
            return True
        if input.id == self.inputs.face.id:
            face = adsk.fusion.BRepFace.cast(selection)
            return bool(face and face.body.isSolid and utils.brep.is_planar(face))
        if input.id == self.inputs.pattern_axis.id:
            return bool(
                adsk.fusion.BRepEdge.cast(selection)
                or adsk.fusion.SketchLine.cast(selection)
                or adsk.fusion.ConstructionAxis.cast(selection)
            )
        if input.id == self.inputs.bounding_points.id:
            return bool(
                adsk.fusion.BRepVertex.cast(selection)
                or adsk.fusion.SketchPoint.cast(selection)
                or adsk.fusion.ConstructionPoint.cast(selection)
            )
        return True

    def _validate(self, args: adsk.core.ValidateInputsEventArgs):
        self._apply_validation(args, self._validation_error)

    def execute(self):
        error = self._validation_error()
        if error:
            raise ValueError(error)

        targets = self._face_targets()
        reference_face = targets[0].face
        component = reference_face.body.parentComponent
        self._parameter_prefix = self._unique_parameter_prefix(
            component.parentDesign
        )
        self._remainder_parameter_name = None
        self._outer_inset_parameter = None
        target_bodies: list[adsk.fusion.BRepBody] = []
        target_body_locators: list[_BodyLocator] = []
        target_body_indices: list[int] = []
        for target in targets:
            body_index = next(
                (
                    index
                    for index, body in enumerate(target_bodies)
                    if body == target.target_body
                ),
                None,
            )
            if body_index is None:
                body_index = len(target_bodies)
                target_bodies.append(target.target_body)
                target_body_locators.append(
                    self._body_locator(target.target_body)
                )
            target_body_indices.append(body_index)

        sketch, profiles, outer_curves = self._create_cutout_sketch(
            component,
            reference_face,
        )
        pattern_type = self.inputs.pattern_type.value
        # The bounding box clips the cutout so every pattern stays strictly
        # inside it. The cross wedges are already built on the box, so they
        # need no extra clipping body.
        bounds_sketch = (
            self._create_bounds_sketch(
                component,
                reference_face,
                outer_curves,
            )
            if self._has_manual_bounds()
            and pattern_type != CutoutsNativeInputs.CROSS.value
            else None
        )

        pattern_sketch = None
        cross_sketch = None
        cross_profiles: list[adsk.fusion.Profile] = []
        cross_samples: list[adsk.core.Point3D] = []
        pattern_quantity_u: int | None = None
        pattern_quantity_v: int | None = None
        pattern_multiplier = 2
        pattern_base_name = "Face Cutout (Native) - Triangle Pattern"
        pattern_role = "triangle"
        u_direction = None
        v_direction = None
        pitch_u_expression = None
        pitch_v_expression = None
        if pattern_type == CutoutsNativeInputs.TRIANGLES.value:
            (
                pattern_sketch,
                u_direction,
                v_direction,
                pitch_u_expression,
                pitch_v_expression,
            ) = self._create_triangle_pattern_sketch(
                component,
                reference_face,
                outer_curves,
            )
        elif pattern_type == CutoutsNativeInputs.RHOMBUSES.value:
            (
                pattern_sketch,
                u_direction,
                v_direction,
                pitch_u_expression,
                pitch_v_expression,
            ) = self._create_rhombus_pattern_sketch(
                component,
                reference_face,
                outer_curves,
            )
            # Both lattice families repeat at the full pitch; the extra
            # instance past each edge is removed by the clip.
            pattern_quantity_u = self.inputs.triangle_columns.value + 1
            pattern_quantity_v = self.inputs.triangle_rows.value + 1
            pattern_multiplier = 1
            pattern_base_name = "Face Cutout (Native) - Rhombus Pattern"
            pattern_role = "rhombus"
        elif pattern_type == CutoutsNativeInputs.CROSS.value:
            (
                cross_sketch,
                cross_profiles,
                cross_samples,
            ) = self._create_cross_pattern_sketch(
                component,
                reference_face,
                outer_curves,
            )

        cuts_by_body: dict[int, _BodyCut] = {}
        face_count = len(targets)
        for face_index, (target, target_body_index) in enumerate(
            zip(targets, target_body_indices),
            start=1,
        ):
            extrude = self._create_tool_extrude(
                component,
                sketch,
                profiles,
                target.face,
                target.opposite_face,
                target.cut_direction,
                face_index,
                face_count,
            )
            tool_bodies = cast(
                list[adsk.fusion.BRepBody],
                utils.fusion.as_list(extrude.bodies),
            )

            if bounds_sketch:
                bounds_extrude = self._create_pattern_extrude(
                    component,
                    bounds_sketch,
                    target.face,
                    target.opposite_face,
                    target.cut_direction,
                    face_index,
                    face_count,
                    base_name="Face Cutout (Native) - Bounding Box Tool",
                    role_prefix="bounds",
                )
                if len(tool_bodies) != 1:
                    raise RuntimeError(
                        "The full cutout tool for selected face "
                        f"{face_index} is not a single body "
                        f"({len(tool_bodies)} bodies found)."
                    )
                bounds_intersection = self._create_intersect_combine(
                    component,
                    tool_bodies[0],
                    cast(
                        list[adsk.fusion.BRepBody],
                        utils.fusion.as_list(bounds_extrude.bodies),
                    ),
                    face_index,
                    face_count,
                    base_name="Face Cutout (Native) - Bounding Box Intersection",
                )
                tool_bodies = cast(
                    list[adsk.fusion.BRepBody],
                    utils.fusion.as_list(bounds_intersection.bodies),
                )

            if cross_sketch:
                cross_extrude = self._create_pattern_extrude(
                    component,
                    cross_sketch,
                    target.face,
                    target.opposite_face,
                    target.cut_direction,
                    face_index,
                    face_count,
                    base_name="Face Cutout (Native) - Cross Tool",
                    role_prefix="cross",
                    selected_profiles=self._cross_wedge_profiles(
                        cross_sketch,
                        cross_samples,
                        cross_profiles,
                    ),
                )
                if len(tool_bodies) != 1:
                    raise RuntimeError(
                        "The full cutout tool for selected face "
                        f"{face_index} is not a single body "
                        f"({len(tool_bodies)} bodies found)."
                    )
                cross_intersection = self._create_intersect_combine(
                    component,
                    tool_bodies[0],
                    cast(
                        list[adsk.fusion.BRepBody],
                        utils.fusion.as_list(cross_extrude.bodies),
                    ),
                    face_index,
                    face_count,
                    base_name="Face Cutout (Native) - Cross Intersection",
                )
                tool_bodies = cast(
                    list[adsk.fusion.BRepBody],
                    utils.fusion.as_list(cross_intersection.bodies),
                )

            if pattern_sketch:
                if not (
                    u_direction
                    and v_direction
                    and pitch_u_expression
                    and pitch_v_expression
                ):
                    raise RuntimeError(
                        "The triangle pattern directions were not created."
                    )
                pattern_extrude = self._create_pattern_extrude(
                    component,
                    pattern_sketch,
                    target.face,
                    target.opposite_face,
                    target.cut_direction,
                    face_index,
                    face_count,
                    base_name=pattern_base_name,
                    role_prefix=pattern_role,
                )
                pattern_bodies = cast(
                    list[adsk.fusion.BRepBody],
                    utils.fusion.as_list(pattern_extrude.bodies),
                )
                pattern_feature = self._create_solid_triangle_pattern(
                    component,
                    pattern_bodies,
                    u_direction,
                    v_direction,
                    pitch_u_expression,
                    pitch_v_expression,
                    face_index,
                    face_count,
                    quantity_u=pattern_quantity_u,
                    quantity_v=pattern_quantity_v,
                    distance_multiplier=pattern_multiplier,
                )
                if pattern_feature:
                    for body in pattern_feature.bodies:
                        if not any(
                            body == existing
                            for existing in pattern_bodies
                        ):
                            pattern_bodies.append(body)
                if not pattern_bodies:
                    raise RuntimeError(
                        "The solid triangle pattern did not create any tool "
                        f"bodies for selected face {face_index}."
                    )
                if len(tool_bodies) != 1:
                    raise RuntimeError(
                        "The full cutout tool for selected face "
                        f"{face_index} is not a single body "
                        f"({len(tool_bodies)} bodies found)."
                    )
                intersection = self._create_intersect_combine(
                    component,
                    tool_bodies[0],
                    pattern_bodies,
                    face_index,
                    face_count,
                )
                tool_bodies = cast(
                    list[adsk.fusion.BRepBody],
                    utils.fusion.as_list(intersection.bodies),
                )

            tool_bodies = self._create_tool_fillets(
                component,
                tool_bodies,
                target.cut_direction,
                face_index,
                face_count,
            )

            body_cut = cuts_by_body.get(target_body_index)
            tool_body_locators = [
                self._body_locator(body)
                for body in tool_bodies
            ]
            if body_cut:
                body_cut.tool_body_locators.extend(tool_body_locators)
            else:
                cuts_by_body[target_body_index] = _BodyCut(
                    target_body_locator=target_body_locators[
                        target_body_index
                    ],
                    tool_body_locators=tool_body_locators,
                )

        last_combine = None
        body_cut_count = len(cuts_by_body)
        for body_index, body_cut in enumerate(
            cuts_by_body.values(),
            start=1,
        ):
            target_body = self._resolve_body(
                component,
                body_cut.target_body_locator,
                "target",
            )
            tool_bodies: list[adsk.fusion.BRepBody] = []
            for locator in body_cut.tool_body_locators:
                tool_bodies.append(
                    self._resolve_body(
                        component,
                        locator,
                        "cut tool",
                        [target_body, *tool_bodies],
                    )
                )
            last_combine = self._create_cut_combine(
                component,
                target_body,
                tool_bodies,
                body_index,
                body_cut_count,
            )
        if not last_combine:
            raise RuntimeError("Face Cutout (Native) did not create a final cut.")
        self._group_features(component, sketch, last_combine)

    def _body_locator(
        self,
        body: adsk.fusion.BRepBody,
    ) -> _BodyLocator:
        box = body.boundingBox
        return _BodyLocator(
            minimum=(
                box.minPoint.x,
                box.minPoint.y,
                box.minPoint.z,
            ),
            maximum=(
                box.maxPoint.x,
                box.maxPoint.y,
                box.maxPoint.z,
            ),
            volume=body.volume,
        )

    def _resolve_body(
        self,
        component: adsk.fusion.Component,
        locator: _BodyLocator,
        role: str,
        excluded: list[adsk.fusion.BRepBody] | None = None,
    ) -> adsk.fusion.BRepBody:
        def score(candidate: adsk.fusion.BRepBody) -> float:
            current = self._body_locator(candidate)
            coordinates = (
                *current.minimum,
                *current.maximum,
            )
            expected = (
                *locator.minimum,
                *locator.maximum,
            )
            coordinate_error = max(
                abs(value - target)
                for value, target in zip(coordinates, expected)
            )
            volume_scale = max(1, abs(locator.volume))
            volume_error = abs(current.volume - locator.volume) / volume_scale
            return max(coordinate_error, volume_error)

        candidates = sorted(
            (
                candidate
                for candidate in component.bRepBodies
                if not excluded or candidate not in excluded
            ),
            key=score,
        )
        if not candidates or score(candidates[0]) > 1e-5:
            raise RuntimeError(
                f"Fusion lost a Face Cutout (Native) {role} body reference."
            )
        return candidates[0]

    def _face_targets(self) -> list[_FaceTarget]:
        targets: list[_FaceTarget] = []
        for selected in self.inputs.face.value:
            selected_face = adsk.fusion.BRepFace.cast(selected)
            if not selected_face:
                raise ValueError("Every selected entity must be a planar face.")
            face = selected_face.nativeObject or selected_face
            opposite_face = utils.brep.get_opposite_face(face)
            targets.append(
                _FaceTarget(
                    face=face,
                    opposite_face=opposite_face,
                    target_body=face.body,
                    cut_direction=utils.brep.normal_towards_face(
                        face,
                        opposite_face,
                    ),
                )
            )
        return targets

    def _feature_name(
        self,
        base: str,
        index: int,
        count: int,
    ) -> str:
        return base if count == 1 else f"{base} (Face {index})"

    def _face_parameter_role(
        self,
        base: str,
        face_index: int,
        face_count: int,
    ) -> str:
        return base if face_count == 1 else f"{base}{face_index}"

    def _unique_parameter_prefix(
        self,
        design: adsk.fusion.Design,
    ) -> str:
        parameter_names = {
            parameter.name
            for parameter in design.allParameters
        }
        base = "cutoutsNative"
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
        # Nothing reads the assigned names back (later references use
        # parameter.name live, which stays valid for auto-generated names);
        # the preview is rolled back, so the renames (~300 ms each in large
        # documents) only matter on OK.
        if self.is_previewing:
            return
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
            return "Face Cutout (Native) requires Design History (a parametric design)."
        if not self.inputs or not self.inputs.face.value:
            return "Select at least one planar face."

        faces: list[adsk.fusion.BRepFace] = []
        for index, selected in enumerate(self.inputs.face.value, start=1):
            selected_face = adsk.fusion.BRepFace.cast(selected)
            if not selected_face or not utils.brep.is_planar(selected_face):
                return f"Selected entity {index} must be a planar face."
            if not selected_face.body.isSolid:
                return f"Selected face {index} must belong to a solid body."
            face = selected_face.nativeObject or selected_face
            if face.body.parentComponent != design.activeComponent:
                return (
                    "Activate the component that owns all selected faces, "
                    "then run Face Cutout (Native) again."
                )
            faces.append(face)

        face = faces[0]
        reference_normal = utils.brep.normal_away_from_body(face)
        if not reference_normal.normalize():
            return "Could not determine the first selected face's normal."
        for index, candidate in enumerate(faces[1:], start=2):
            candidate_normal = utils.brep.normal_away_from_body(candidate)
            if (
                not candidate_normal.normalize()
                or abs(reference_normal.dotProduct(candidate_normal))
                < 1 - 1e-6
            ):
                return (
                    f"Selected face {index} is not parallel to the first "
                    "selected face. One shared sketch can only drive "
                    "parallel faces."
                )

        for input_value, name in [
            (self.inputs.outer_inset.value, "Outer Inset"),
            (self.inputs.inner_feature_inset.value, "Inner Feature Inset"),
            (self.inputs.remaining_material.value, "Remaining Material"),
            (self.inputs.fillet_radius.value, "Fillet Radius"),
            (self.inputs.triangle_spacing.value, "Triangle Spacing"),
            (self.inputs.cross_width.value, "Cross Width"),
        ]:
            if input_value < 0:
                return f"{name} cannot be negative."

        for index, candidate in enumerate(faces, start=1):
            try:
                thickness = utils.brep.get_board_thickness(candidate)
            except Exception as exc:
                return (
                    "Could not find a parallel opposite face for selected "
                    f"face {index}: {exc}"
                )
            if self.inputs.remaining_material.value >= thickness - 1e-6:
                return (
                    "Remaining Material must be smaller than the body "
                    f"thickness at selected face {index}."
                )
        if (
            self.inputs.pattern_type.value == CutoutsNativeInputs.TRIANGLES.value
            and self.inputs.triangle_spacing.value <= 1e-6
        ):
            return "Triangle Spacing must be greater than zero."
        if (
            self.inputs.pattern_type.value == CutoutsNativeInputs.TRIANGLES.value
            and self.inputs.align_triangles.value
            and self.inputs.fillet_radius.value <= 1e-6
        ):
            return (
                "Fillet Radius must be greater than zero when Align Triangles "
                "is enabled."
            )
        if (
            self.inputs.pattern_type.value == CutoutsNativeInputs.CROSS.value
            and self.inputs.cross_width.value <= 1e-6
        ):
            return "Cross Width must be greater than zero."

        axis_count = len(self.inputs.pattern_axis.value)
        bounds_count = len(self.inputs.bounding_points.value)
        if axis_count > 1:
            return "Select at most one Pattern Axis."
        if bounds_count == 1:
            return (
                "Select at least two Bounding Box Points, or clear the "
                "point selection."
            )
        if bounds_count > 4:
            return "Select no more than four Bounding Box Points."
        needs_oriented_box = self.inputs.pattern_type.value in (
            CutoutsNativeInputs.TRIANGLES.value,
            CutoutsNativeInputs.CROSS.value,
            CutoutsNativeInputs.RHOMBUSES.value,
        )
        if (
            axis_count == 1
            and bounds_count == 0
            and not needs_oriented_box
        ):
            return (
                "Pattern Axis has no effect without Bounding Box Points."
            )
        if bounds_count >= 2:
            box_error = self._bounding_box_error(face)
            if box_error:
                return box_error
        if needs_oriented_box and bounds_count == 0:
            outer_loop = next(
                (loop for loop in face.loops if loop.isOuter),
                None,
            )
            rectangular_candidate = bool(
                outer_loop
                and outer_loop.edges.count == 4
                and all(
                    adsk.core.Line3D.cast(edge.geometry)
                    for edge in outer_loop.edges
                )
            )
            if not rectangular_candidate:
                return (
                    "For a non-rectangular face, select two to four "
                    "Bounding Box Points (optionally with a Pattern Axis)."
                )
        return None

    def _bounding_box_extents(
        self,
        face: adsk.fusion.BRepFace,
    ) -> tuple[float, float] | None:
        """Measure the manual bounding box analytically, before any sketch
        exists, so the dialog can validate against it."""
        plane = adsk.core.Plane.cast(face.geometry)
        if not plane:
            return None
        normal = plane.normal.copy()
        if not normal.normalize():
            return None

        axis_entity = (
            self.inputs.pattern_axis.value[0]
            if self.inputs.pattern_axis.value
            else None
        )
        u_vector: adsk.core.Vector3D | None = None
        if axis_entity:
            direction = self._axis_direction(axis_entity)
            if direction:
                # Project the axis onto the face plane.
                along_normal = normal.copy()
                along_normal.scaleBy(direction.dotProduct(normal))
                projected = direction.copy()
                projected.subtract(along_normal)
                if projected.normalize():
                    u_vector = projected
        if u_vector is None:
            # Matches the sketch-axis fallback used when no axis is given.
            reference = (
                adsk.core.Vector3D.create(1, 0, 0)
                if abs(normal.x) < 0.9
                else adsk.core.Vector3D.create(0, 1, 0)
            )
            u_vector = normal.crossProduct(reference)
            if not u_vector.normalize():
                return None
        v_vector = normal.crossProduct(u_vector)
        if not v_vector.normalize():
            return None

        coordinates: list[tuple[float, float]] = []
        for entity in self.inputs.bounding_points.value:
            point = self._point_geometry(entity)
            if not point:
                return None
            offset = plane.origin.vectorTo(point)
            coordinates.append(
                (offset.dotProduct(u_vector), offset.dotProduct(v_vector))
            )
        if len(coordinates) < 2:
            return None
        extent_u = max(item[0] for item in coordinates) - min(
            item[0] for item in coordinates
        )
        extent_v = max(item[1] for item in coordinates) - min(
            item[1] for item in coordinates
        )
        return extent_u, extent_v

    def _axis_direction(
        self,
        axis: adsk.core.Base,
    ) -> adsk.core.Vector3D | None:
        edge = adsk.fusion.BRepEdge.cast(axis)
        if edge:
            line = adsk.core.Line3D.cast(edge.geometry)
            if not line:
                return None
            return line.startPoint.vectorTo(line.endPoint)
        sketch_line = adsk.fusion.SketchLine.cast(axis)
        if sketch_line:
            return sketch_line.worldGeometry.startPoint.vectorTo(
                sketch_line.worldGeometry.endPoint
            )
        construction_axis = adsk.fusion.ConstructionAxis.cast(axis)
        if construction_axis:
            line = adsk.core.InfiniteLine3D.cast(construction_axis.geometry)
            return line.direction.copy() if line else None
        return None

    def _point_geometry(
        self,
        entity: adsk.core.Base,
    ) -> adsk.core.Point3D | None:
        vertex = adsk.fusion.BRepVertex.cast(entity)
        if vertex:
            return vertex.geometry
        sketch_point = adsk.fusion.SketchPoint.cast(entity)
        if sketch_point:
            return sketch_point.worldGeometry
        construction_point = adsk.fusion.ConstructionPoint.cast(entity)
        if construction_point:
            return construction_point.geometry
        return None

    def _bounding_box_error(
        self,
        face: adsk.fusion.BRepFace,
    ) -> str | None:
        extents = self._bounding_box_extents(face)
        if not extents:
            return None
        extent_u, extent_v = extents
        if extent_u <= 1e-6 or extent_v <= 1e-6:
            return (
                "The Bounding Box Points must define non-zero extents in "
                "both directions."
            )
        inset = self._bounding_box_inset()
        if inset > 1e-9:
            # The pattern checks below must judge the effective (inset) box.
            extent_u -= 2 * inset
            extent_v -= 2 * inset
            if extent_u <= 1e-6 or extent_v <= 1e-6:
                return "Outer Inset is too large to inset the bounding box."
        if self.inputs.pattern_type.value == CutoutsNativeInputs.RHOMBUSES.value:
            try:
                width, height = self._rhombus_dimensions(
                    extent_u / self.inputs.triangle_columns.value,
                    extent_v / self.inputs.triangle_rows.value,
                    self.inputs.triangle_spacing.value,
                )
            except ValueError as exc:
                return str(exc)
            if width <= 1e-6 or height <= 1e-6:
                return (
                    "Spacing is too large for the requested rhombus rows "
                    "and columns."
                )
            return None
        if self.inputs.pattern_type.value != CutoutsNativeInputs.CROSS.value:
            return None
        # For a rectangle every side midpoint has the same distance to both
        # diagonals, so the widest usable cross band is w*h/hypot(w, h).
        maximum_width = (
            extent_u * extent_v / math.hypot(extent_u, extent_v)
        )
        if self.inputs.cross_width.value >= maximum_width - 1e-6:
            design = cast(adsk.fusion.Design, self.app.activeProduct)
            units = design.unitsManager
            formatted = units.formatInternalValue(
                maximum_width,
                units.defaultLengthUnits,
                True,
            )
            return (
                "Cross Width is too large for the Bounding Box Points. It "
                f"must be smaller than {formatted}."
            )
        return None

    def _create_cutout_sketch(
        self,
        component: adsk.fusion.Component,
        face: adsk.fusion.BRepFace,
    ) -> tuple[
        adsk.fusion.Sketch,
        list[adsk.fusion.Profile],
        list[adsk.fusion.SketchCurve],
    ]:
        # Sketches.add projects every edge of a BRep face automatically. That
        # would mix all face loops into each per-loop area probe below and can
        # make a valid inner offset look like it has the wrong direction.
        sketch = component.sketches.addWithoutEdges(face)
        if not sketch:
            raise RuntimeError("Fusion failed to create a sketch on the selected face.")
        sketch.name = "Face Cutout (Native) - Insets"

        final_curves: list[adsk.fusion.SketchCurve] = []
        outer_curves: list[adsk.fusion.SketchCurve] = []
        inner_loop_curves: list[list[adsk.fusion.SketchCurve]] = []
        inner_loop_index = 0
        inner_inset_reference: str | None = None

        # Batch the edits: without this, every projection, construction
        # toggle, offset and tab entity triggers its own full compute cycle.
        sketch.isComputeDeferred = True
        try:
            loops = utils.fusion.as_list(face.loops)
            projected_by_loop = self._project_face_loops(sketch, loops)
            for loop, projected in zip(loops, projected_by_loop):
                self._set_construction(sketch, projected, True)
                if loop.isOuter:
                    input_value = self.inputs.outer_inset
                    parameter_role = "outerInset"
                    expression = input_value.expression
                else:
                    inner_loop_index += 1
                    input_value = self.inputs.inner_feature_inset
                    parameter_role = f"innerInset{inner_loop_index}"
                    # Later inner loops reference the first inner-inset parameter
                    # instead of duplicating the user expression.
                    expression = inner_inset_reference or input_value.expression
                if input_value.value <= 1e-9:
                    loop_curves = projected
                else:
                    loop_curves, offset_parameter = self._offset_loop(
                        sketch=sketch,
                        source_curves=projected,
                        expression=expression,
                        should_be_smaller=loop.isOuter,
                        parameter_role=parameter_role,
                    )
                    if loop.isOuter:
                        self._outer_inset_parameter = offset_parameter
                    elif inner_inset_reference is None:
                        inner_inset_reference = offset_parameter.name

                final_curves.extend(loop_curves)
                if loop.isOuter:
                    outer_curves.extend(loop_curves)
                else:
                    inner_loop_curves.append(loop_curves)
                self._set_construction(sketch, loop_curves, True)

            self._set_construction(sketch, final_curves, False)
            if self.inputs.tabs.value:
                # The tab layout measures the solved offset curves.
                self._solve_deferred(sketch)
                self._create_tabs(
                    sketch,
                    face,
                    outer_curves,
                    inner_loop_curves,
                )
        finally:
            sketch.isComputeDeferred = False
        profile = (
            self._profile_bounded_by(sketch, outer_curves)
            or self._largest_profile(sketch)
        )
        if not profile:
            raise RuntimeError(
                "The inset curves did not create a usable cutout profile."
            )
        profiles = [profile]
        self._require_fully_constrained(sketch)
        return sketch, profiles, outer_curves

    def _create_cross_pattern_sketch(
        self,
        component: adsk.fusion.Component,
        face: adsk.fusion.BRepFace,
        outer_curves: list[adsk.fusion.SketchCurve],
    ) -> tuple[
        adsk.fusion.Sketch,
        list[adsk.fusion.Profile],
        list[adsk.core.Point3D],
    ]:
        """The cross wedges live in their own sketch, laid out inside the
        pattern boundary. Intersecting them with the full cutout tool then
        applies the face insets and the tabs automatically."""
        sketch = component.sketches.addWithoutEdges(face)
        if not sketch:
            raise RuntimeError("Fusion failed to create the cross layout sketch.")
        sketch.name = "Face Cutout (Native) - Cross Layout"
        # Batch the edits; _add_cross_bands solves once before it probes the
        # wedge profiles.
        sketch.isComputeDeferred = True
        try:
            boundary = self._create_rectangular_pattern_boundary(
                sketch,
                outer_curves,
                role_prefix="crossBoundary",
            )
            # The boundary closes the wedge profiles, so it must not stay
            # construction geometry.
            self._set_construction(
                sketch,
                cast(list[adsk.fusion.SketchCurve], boundary.boundary_lines),
                False,
            )
            profiles, samples = self._add_cross_bands(sketch, boundary)
        finally:
            sketch.isComputeDeferred = False
        self._require_fully_constrained(sketch)
        return sketch, profiles, samples

    def _cross_wedge_profiles(
        self,
        sketch: adsk.fusion.Sketch,
        samples: list[adsk.core.Point3D],
        cached: list[adsk.fusion.Profile] | None = None,
    ) -> list[adsk.fusion.Profile]:
        # The wedges were already identified while the layout was built, so
        # reuse them as long as Fusion has not invalidated them.
        if cached and all(profile.isValid for profile in cached):
            return cached
        profiles: list[adsk.fusion.Profile] = []
        for sample in samples:
            profile = self._profile_containing_point(sketch, sample)
            if not profile:
                raise RuntimeError(
                    "Fusion could not re-resolve a cross cutout wedge."
                )
            if profile not in profiles:
                profiles.append(profile)
        if len(profiles) != len(samples):
            raise RuntimeError(
                "The cross cutout wedges could not be re-resolved uniquely."
            )
        return profiles

    def _create_bounds_sketch(
        self,
        component: adsk.fusion.Component,
        face: adsk.fusion.BRepFace,
        outer_curves: list[adsk.fusion.SketchCurve],
    ) -> adsk.fusion.Sketch:
        """A sketch holding only the bounding-box rectangle. Its extruded
        body is intersected with the cutout tool so every pattern is
        strictly limited to the box."""
        sketch = component.sketches.addWithoutEdges(face)
        if not sketch:
            raise RuntimeError(
                "Fusion failed to create the bounding-box sketch."
            )
        sketch.name = "Face Cutout (Native) - Bounding Box"
        # Batch the edits; the profile check below runs on the solved sketch.
        sketch.isComputeDeferred = True
        try:
            boundary = self._create_rectangular_pattern_boundary(
                sketch,
                outer_curves,
                role_prefix="bounds",
            )
            self._set_construction(
                sketch,
                cast(list[adsk.fusion.SketchCurve], boundary.boundary_lines),
                False,
            )
        finally:
            sketch.isComputeDeferred = False
        self._require_fully_constrained(sketch)
        if sketch.profiles.count != 1:
            raise RuntimeError(
                "The bounding box did not create exactly one profile "
                f"({sketch.profiles.count} found)."
            )
        return sketch

    def _add_cross_bands(
        self,
        sketch: adsk.fusion.Sketch,
        pattern_boundary: _PatternBoundary,
    ) -> tuple[list[adsk.fusion.Profile], list[adsk.core.Point3D]]:
        corners = pattern_boundary.corners
        boundary = pattern_boundary.boundary_lines
        lines = sketch.sketchCurves.sketchLines
        constraints = sketch.geometricConstraints
        diagonals = [
            lines.addByTwoPoints(corners[0], corners[2]),
            lines.addByTwoPoints(corners[1], corners[3]),
        ]
        for diagonal in diagonals:
            diagonal.isConstruction = True

        half_width = self.inputs.cross_width.value / 2
        minimum_midpoint_clearance = min(
            self._distance_to_line(
                self._line_midpoint(side),
                diagonal.startSketchPoint.geometry,
                diagonal.endSketchPoint.geometry,
            )
            for side in boundary
            for diagonal in diagonals
        )
        if half_width >= minimum_midpoint_clearance - 1e-6:
            maximum_width = 2 * minimum_midpoint_clearance
            units = sketch.parentComponent.parentDesign.unitsManager
            formatted_maximum = units.formatInternalValue(
                maximum_width,
                units.defaultLengthUnits,
                True,
            )
            raise ValueError(
                "Cross Width is too large for the pattern boundary. It must "
                f"be smaller than {formatted_maximum}."
            )

        parameter_index = 0
        half_width_expression = (
            f"({self.inputs.cross_width.expression}) / 2"
        )
        for diagonal in diagonals:
            start = diagonal.startSketchPoint.geometry
            end = diagonal.endSketchPoint.geometry
            direction = start.vectorTo(end)
            if not direction.normalize():
                raise RuntimeError("A cross diagonal has zero length.")
            normal = adsk.core.Vector3D.create(
                -direction.y,
                direction.x,
                0,
            )
            diagonal_boundaries: list[adsk.fusion.SketchLine] = []
            for sign in (-1, 1):
                offset = normal.copy()
                offset.scaleBy(sign * half_width)
                offset_start = start.copy()
                offset_start.translateBy(offset)
                offset_end = end.copy()
                offset_end.translateBy(offset)
                intersections = self._line_rectangle_intersections(
                    offset_start,
                    offset_end,
                    boundary,
                )
                if len(intersections) != 2:
                    raise RuntimeError(
                        "A cross boundary did not intersect the pattern "
                        "rectangle twice."
                    )
                first_point, first_side = intersections[0]
                second_point, second_side = intersections[1]
                cross_line = lines.addByTwoPoints(
                    first_point,
                    second_point,
                )
                constraints.addCoincident(
                    cross_line.startSketchPoint,
                    first_side,
                )
                constraints.addCoincident(
                    cross_line.endSketchPoint,
                    second_side,
                )
                diagonal_boundaries.append(cross_line)

            first_boundary, second_boundary = diagonal_boundaries
            constraints.addParallel(first_boundary, diagonal)
            constraints.addSymmetry(
                first_boundary,
                second_boundary,
                diagonal,
            )
            parameter_index += 1
            text_point = self._line_midpoint(first_boundary)
            text_offset = normal.copy()
            text_offset.scaleBy(-half_width / 2)
            text_point.translateBy(text_offset)
            dimension = sketch.sketchDimensions.addOffsetDimension(
                diagonal,
                first_boundary,
                text_point,
            )
            if not dimension or not dimension.parameter:
                raise RuntimeError(
                    "Fusion failed to dimension a cross boundary."
                )
            self._set_parameter_expression(
                dimension.parameter,
                half_width_expression,
            )
            self._name_parameter(
                dimension.parameter,
                (
                    "crossHalfWidth"
                    if parameter_index == 1
                    else f"crossHalfWidth{parameter_index}"
                ),
            )
            if parameter_index == 1:
                half_width_expression = dimension.parameter.name

        # The wedge probes below read profiles, which need a solved sketch.
        self._solve_deferred(sketch)
        center = adsk.core.Point3D.create(
            sum(point.geometry.x for point in corners) / 4,
            sum(point.geometry.y for point in corners) / 4,
            0,
        )
        sample_offset = min(side.length for side in boundary) * 1e-4
        profiles: list[adsk.fusion.Profile] = []
        samples: list[adsk.core.Point3D] = []
        for side in boundary:
            start = side.startSketchPoint.geometry
            end = side.endSketchPoint.geometry
            inward = self._line_midpoint(side).vectorTo(center)
            if not inward.normalize():
                raise RuntimeError(
                    "Could not determine the inside of the cross boundary."
                )
            inward.scaleBy(sample_offset)
            for step in range(1, 20):
                fraction = step / 20
                sample = adsk.core.Point3D.create(
                    start.x + (end.x - start.x) * fraction,
                    start.y + (end.y - start.y) * fraction,
                    0,
                )
                sample.translateBy(inward)
                if any(
                    self._distance_to_line(
                        sample,
                        diagonal.startSketchPoint.geometry,
                        diagonal.endSketchPoint.geometry,
                    )
                    < half_width + sample_offset
                    for diagonal in diagonals
                ):
                    continue
                profile = self._profile_containing_point(
                    sketch,
                    sample,
                )
                if profile and profile not in profiles:
                    profiles.append(profile)
                    # Keep the probe point: the wedge profiles are
                    # re-resolved from it for every selected face.
                    samples.append(sample)

        if len(profiles) < 4:
            raise RuntimeError(
                "The cross layout did not create all four cutout wedges "
                f"({len(profiles)} profiles found)."
            )
        return profiles, samples

    def _ordered_rectangular_boundary(
        self,
        curves: list[adsk.fusion.SketchCurve],
    ) -> tuple[
        list[adsk.fusion.SketchPoint],
        list[adsk.fusion.SketchLine],
    ]:
        lines = [
            line
            for curve in curves
            if (line := adsk.fusion.SketchLine.cast(curve))
        ]
        if len(lines) != 4:
            raise ValueError(
                "Cross requires an inset outer loop containing exactly four "
                "straight lines."
            )

        ordered = [lines[0]]
        corners = [
            lines[0].startSketchPoint,
            lines[0].endSketchPoint,
        ]
        remaining = lines[1:]
        while len(ordered) < 4:
            current = corners[-1]
            matches: list[
                tuple[adsk.fusion.SketchLine, adsk.fusion.SketchPoint]
            ] = []
            for line in remaining:
                if (
                    line.startSketchPoint.geometry.distanceTo(
                        current.geometry
                    )
                    <= 1e-5
                ):
                    matches.append((line, line.endSketchPoint))
                elif (
                    line.endSketchPoint.geometry.distanceTo(
                        current.geometry
                    )
                    <= 1e-5
                ):
                    matches.append((line, line.startSketchPoint))
            if len(matches) != 1:
                raise ValueError(
                    "The inset outer loop is not one closed rectangle."
                )
            line, next_corner = matches[0]
            ordered.append(line)
            remaining.remove(line)
            if len(ordered) < 4:
                corners.append(next_corner)
            elif (
                next_corner.geometry.distanceTo(corners[0].geometry)
                > 1e-5
            ):
                raise ValueError(
                    "The inset outer loop is not one closed rectangle."
                )

        directions = [
            self._normalized_line_vector(line)
            for line in ordered
        ]
        # Tolerant comparisons: these directions come from curves projected
        # off real BRep geometry, whose normals carry rounding noise, and
        # Vector3D.isPerpendicularTo/isParallelTo compare exactly.
        if (
            not utils.vector.is_perpendicular_direction(directions[0], directions[1])
            or not utils.vector.is_perpendicular_direction(directions[1], directions[2])
            or not utils.vector.is_perpendicular_direction(directions[2], directions[3])
            or not utils.vector.is_perpendicular_direction(directions[3], directions[0])
            or not utils.vector.is_parallel_direction(directions[0], directions[2])
            or not utils.vector.is_parallel_direction(directions[1], directions[3])
        ):
            raise ValueError(
                "Cross requires a rectangular inset outer loop."
            )
        return corners, ordered

    def _line_rectangle_intersections(
        self,
        line_start: adsk.core.Point3D,
        line_end: adsk.core.Point3D,
        boundary: list[adsk.fusion.SketchLine],
    ) -> list[tuple[adsk.core.Point3D, adsk.fusion.SketchLine]]:
        intersections: list[
            tuple[adsk.core.Point3D, adsk.fusion.SketchLine]
        ] = []
        line_x = line_end.x - line_start.x
        line_y = line_end.y - line_start.y
        for side in boundary:
            side_start = side.startSketchPoint.geometry
            side_end = side.endSketchPoint.geometry
            side_x = side_end.x - side_start.x
            side_y = side_end.y - side_start.y
            denominator = line_x * side_y - line_y * side_x
            if abs(denominator) <= 1e-9:
                continue
            relative_x = side_start.x - line_start.x
            relative_y = side_start.y - line_start.y
            side_parameter = (
                relative_x * line_y - relative_y * line_x
            ) / denominator
            if side_parameter < -1e-7 or side_parameter > 1 + 1e-7:
                continue
            line_parameter = (
                relative_x * side_y - relative_y * side_x
            ) / denominator
            point = adsk.core.Point3D.create(
                line_start.x + line_parameter * line_x,
                line_start.y + line_parameter * line_y,
                0,
            )
            if any(
                point.distanceTo(existing[0]) <= 1e-6
                for existing in intersections
            ):
                continue
            intersections.append((point, side))
        return intersections

    def _line_midpoint(
        self,
        line: adsk.fusion.SketchLine,
    ) -> adsk.core.Point3D:
        start = line.startSketchPoint.geometry
        end = line.endSketchPoint.geometry
        return adsk.core.Point3D.create(
            (start.x + end.x) / 2,
            (start.y + end.y) / 2,
            0,
        )

    def _profile_containing_point(
        self,
        sketch: adsk.fusion.Sketch,
        point: adsk.core.Point3D,
    ) -> adsk.fusion.Profile | None:
        # Note: Profile.face is positioned in sketch space (verified
        # empirically), so the sketch-space probe points are passed directly.
        for profile in sketch.profiles:
            face = profile.face
            if face and face.isPointOnFace(point, 1e-6):
                return profile
        return None

    def _distance_to_line(
        self,
        point: adsk.core.Point3D,
        line_start: adsk.core.Point3D,
        line_end: adsk.core.Point3D,
    ) -> float:
        line_x = line_end.x - line_start.x
        line_y = line_end.y - line_start.y
        length = math.hypot(line_x, line_y)
        if length <= 1e-9:
            raise RuntimeError("Could not measure a zero-length diagonal.")
        return abs(
            line_x * (line_start.y - point.y)
            - (line_start.x - point.x) * line_y
        ) / length

    def _create_tabs(
        self,
        sketch: adsk.fusion.Sketch,
        face: adsk.fusion.BRepFace,
        outer_curves: list[adsk.fusion.SketchCurve],
        inner_loop_curves: list[list[adsk.fusion.SketchCurve]],
    ) -> list[list[adsk.fusion.SketchLine]]:
        if not outer_curves:
            return []

        face_normal = utils.brep.normal_away_from_body(face)
        tab_boundaries: list[list[adsk.fusion.SketchLine]] = []

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

            first_inner = self._closest_curve_point(
                min_width_point,
                inner_curves,
            )
            second_inner = self._closest_curve_point(
                max_width_point,
                inner_curves,
            )
            if not first_inner or not second_inner:
                raise RuntimeError(
                    "Could not attach a tab to its inner loop."
                )
            first_inner_curve, first_corner, _ = first_inner
            second_inner_curve, second_corner, _ = second_inner

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
            first_outer = self._closest_curve_point(
                third_point,
                outer_curves,
            )
            second_outer = self._closest_curve_point(
                fourth_corner,
                outer_curves,
            )
            if not first_outer or not second_outer:
                raise RuntimeError(
                    "Could not attach a tab to the outer loop."
                )
            first_outer_curve, third_point, _ = first_outer
            second_outer_curve, fourth_corner, _ = second_outer

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
            centerline = tab_lines.addByTwoPoints(
                self._line_midpoint(first_line),
                self._line_midpoint(third_line),
            )
            centerline.isConstruction = True

            constraints = sketch.geometricConstraints
            anchored_first = self._add_curve_coincident(
                constraints,
                first_line.startSketchPoint,
                first_inner_curve,
                first_corner,
            )
            anchored_second = self._add_curve_coincident(
                constraints,
                first_line.endSketchPoint,
                second_inner_curve,
                second_corner,
            )
            self._add_curve_coincident(
                constraints,
                second_line.endSketchPoint,
                first_outer_curve,
                third_point,
            )
            self._add_curve_coincident(
                constraints,
                third_line.endSketchPoint,
                second_outer_curve,
                fourth_corner,
            )
            constraints.addMidPoint(
                centerline.startSketchPoint,
                first_line,
            )
            constraints.addMidPoint(
                centerline.endSketchPoint,
                third_line,
            )
            # The fourth tab side needs no constraint of its own: its
            # endpoints are shared with the constrained sides, and the
            # midpoint constraints already force the quad to close as a
            # parallelogram-free rectangle.
            constraints.addPerpendicular(first_line, centerline)
            constraints.addParallel(second_line, centerline)
            if not (anchored_first and anchored_second):
                # With both inner corners snapped to curve endpoints the tab
                # is already fixed and this constraint would be redundant.
                constraints.addPerpendicular(third_line, centerline)
            if not (anchored_first or anchored_second):
                # The tab width is not implied by curve endpoints (e.g. a
                # circular inner loop), so it needs a driving dimension.
                self._dimension_line_length(
                    sketch,
                    first_line,
                    f"{tab_width} cm",
                    parameter_role=f"tab{len(tab_boundaries) + 1}Width",
                )
            tab_boundaries.append(
                [first_line, second_line, third_line, fourth_line]
            )
        return tab_boundaries

    def _add_curve_coincident(
        self,
        constraints: adsk.fusion.GeometricConstraints,
        sketch_point: adsk.fusion.SketchPoint,
        curve: adsk.fusion.SketchCurve,
        model_point: adsk.core.Point3D,
    ) -> bool:
        # Snap to an existing curve endpoint when the tab corner lands on one
        # (e.g. the corner of a rectangular inner loop). This pins the tab
        # without an extra dimension. Returns True when snapped.
        tolerance = self.app.pointTolerance * 10
        for candidate in (
            getattr(curve, "startSketchPoint", None),
            getattr(curve, "endSketchPoint", None),
        ):
            if (
                candidate
                and candidate.worldGeometry.distanceTo(model_point)
                <= tolerance
            ):
                constraints.addCoincident(sketch_point, candidate)
                return True
        constraints.addCoincident(sketch_point, curve)
        return False

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
        closest = self._closest_curve_point(point, curves)
        return (closest[1], closest[2]) if closest else None

    def _closest_curve_point(
        self,
        point: adsk.core.Point3D,
        curves: list[adsk.fusion.SketchCurve],
    ) -> tuple[
        adsk.fusion.SketchCurve,
        adsk.core.Point3D,
        float,
    ] | None:
        closest: tuple[
            adsk.fusion.SketchCurve,
            adsk.core.Point3D,
            float,
        ] | None = None
        for curve in curves:
            projected = self._project_point_to_curve(
                point,
                curve.worldGeometry.evaluator,  # type: ignore
            )
            if not projected:
                continue
            distance = point.distanceTo(projected)
            if closest is None or distance < closest[2]:
                closest = (curve, projected, distance)
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
        expression: str,
        should_be_smaller: bool,
        parameter_role: str,
    ) -> tuple[list[adsk.fusion.SketchCurve], adsk.fusion.ModelParameter]:
        """Offsets a closed loop, inwards or outwards as asked.

        Which sign of the offset goes inwards depends on the loop's
        orientation, which Fusion does not expose, so the direction is
        established by measuring the offset that was built. Both the
        measurement and the correction are free of sketch computes: an
        offset's child curves carry their final geometry as soon as they
        exist, and rewriting the dimension's expression moves them, neither
        of which needs the sketch solved. That matters because this runs
        inside the builders' deferred-compute batches — measuring profile
        areas instead would force a solve per loop.

        The sign lives in the expression rather than in a value: `expression`
        may reference a parameter that is itself negative, since every offset
        bakes its own direction into its own expression.

        Both signs are attempted because neither is reliably the inward one,
        and because the wrong one frequently cannot be built at all: on a
        real face, offsetting a small hole the wrong way collapses it and
        Fusion refuses outright. Building and discarding an offset is cheap
        here precisely because no solve is involved.
        """
        source_extent = self._loop_extent(source_curves)
        for candidate_expression in (expression, f"-({expression})"):
            constraint = self._add_offset_constraint(
                sketch,
                source_curves,
                adsk.core.ValueInput.createByString(candidate_expression),
            )
            if not constraint:
                # This direction collapses the loop; Fusion rejected it.
                continue
            child_curves = cast(
                list[adsk.fusion.SketchCurve], list(constraint.childCurves)
            )
            dimension = constraint.dimension
            if (
                dimension
                and dimension.parameter
                and self._offset_is_on_expected_side(
                    child_curves, source_extent, should_be_smaller
                )
            ):
                self._name_parameter(dimension.parameter, parameter_role)
                return child_curves, dimension.parameter
            self._discard_offset(constraint, child_curves)

        boundary = "outer" if should_be_smaller else "inner"
        raise RuntimeError(
            f"Could not determine a valid offset direction for an {boundary} loop."
        )

    def _loop_extent(
        self,
        curves: list[adsk.fusion.SketchCurve],
    ) -> float | None:
        """Bounding-box area of a curve set, in sketch space.

        Read straight off the curves, so unlike a profile area it is
        available without computing the sketch.
        """
        xs: list[float] = []
        ys: list[float] = []
        for curve in curves:
            if not curve or not curve.isValid:
                continue
            box = curve.boundingBox
            xs.extend((box.minPoint.x, box.maxPoint.x))
            ys.extend((box.minPoint.y, box.maxPoint.y))
        if not xs:
            return None
        return (max(xs) - min(xs)) * (max(ys) - min(ys))

    def _offset_is_on_expected_side(
        self,
        child_curves: list[adsk.fusion.SketchCurve],
        source_extent: float | None,
        should_be_smaller: bool,
    ) -> bool:
        extent = self._loop_extent(child_curves)
        if extent is None or source_extent is None:
            return False
        if extent <= 1e-9:
            # The offset collapsed onto itself; not a usable loop whichever
            # side it nominally landed on.
            return False
        if abs(extent - source_extent) <= 1e-9:
            return False
        return (extent < source_extent) == should_be_smaller

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

    def _discard_offset(
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
        sketch.name = "Face Cutout (Native) - Triangle Seeds"

        # Batch the edits from here on; the solve happens once at the end.
        sketch.isComputeDeferred = True
        boundary = self._create_rectangular_pattern_boundary(
            sketch,
            outer_curves,
        )
        origin = boundary.origin
        u_direction = boundary.u_direction
        v_direction = boundary.v_direction
        extent_u = boundary.extent_u
        extent_v = boundary.extent_v
        extent_u_parameter = boundary.u_parameter
        extent_v_parameter = boundary.v_parameter
        u_vector = boundary.u_vector
        v_vector = boundary.v_vector

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
        align_triangles = self.inputs.align_triangles.value
        seed_height = (
            self._aligned_triangle_seed_height(
                triangle_width,
                triangle_height,
                self.inputs.fillet_radius.value,
            )
            if align_triangles
            else triangle_height
        )

        pitch_u_expression = (
            f"({extent_u_parameter.name}) / {columns}"
        )

        first = self._add_seed_triangle(
            sketch,
            origin,
            u_direction,
            v_direction,
            u_vector,
            v_vector,
            center_u=0,
            base_v=0,
            width=triangle_width,
            height=seed_height,
            points_up=True,
        )
        constraints = sketch.geometricConstraints
        constraints.addCoincident(first.midpoint, origin)

        pitch_u = extent_u / columns
        second = self._add_seed_triangle(
            sketch,
            origin,
            u_direction,
            v_direction,
            u_vector,
            v_vector,
            center_u=pitch_u,
            base_v=triangle_height,
            width=triangle_width,
            height=seed_height,
            points_up=False,
            size_seed=first,
            equal_altitude=not align_triangles,
        )
        row_height_locator = None
        pitch_start = first.apex
        if align_triangles:
            row_height_locator = (
                sketch.sketchCurves.sketchLines.addByTwoPoints(
                    first.midpoint,
                    self._seed_point(
                        origin.geometry,
                        u_vector,
                        v_vector,
                        0,
                        triangle_height,
                    ),
                )
            )
            row_height_locator.isConstruction = True
            constraints.addParallel(row_height_locator, v_direction)
            pitch_start = row_height_locator.endSketchPoint
        pitch_line = sketch.sketchCurves.sketchLines.addByTwoPoints(
            pitch_start,
            second.midpoint,
        )
        pitch_line.isConstruction = True
        constraints.addParallel(pitch_line, u_direction)
        pitch_dimension = self._dimension_line_length(
            sketch,
            pitch_line,
            pitch_u_expression,
            parameter_role="trianglePitchU",
        )
        pitch_parameter = pitch_dimension.parameter
        if not pitch_parameter:
            raise RuntimeError(
                "Fusion did not create the triangle pitch parameter."
            )
        pitch_u_expression = pitch_parameter.name
        height_dimension = None
        if row_height_locator:
            height_dimension = self._dimension_line_length(
                sketch,
                row_height_locator,
                f"{triangle_height} cm",
                parameter_role="triangleHeight",
            )

        spacing_dimension = sketch.sketchDimensions.addOffsetDimension(
            first.right_side,
            second.left_side,
            self._seed_point(
                origin.geometry,
                u_vector,
                v_vector,
                pitch_u / 2,
                triangle_height / 2,
            ),
        )
        if not spacing_dimension or not spacing_dimension.parameter:
            raise RuntimeError(
                "Fusion failed to dimension the spacing between adjacent "
                "triangle sides."
            )
        spacing_parameter = spacing_dimension.parameter
        self._set_parameter_expression(
            spacing_parameter,
            self.inputs.triangle_spacing.expression,
        )
        self._name_parameter(spacing_parameter, "triangleSpacing")

        height_expression = (
            f"(({extent_v_parameter.name}) - "
            f"{rows - 1} * ({spacing_parameter.name})) / {rows}"
        )
        if height_dimension:
            self._set_parameter_expression(
                height_dimension.parameter,
                height_expression,
            )
        else:
            height_dimension = self._dimension_line_length(
                sketch,
                first.altitude,
                height_expression,
                parameter_role="triangleHeight",
            )
        height_parameter = height_dimension.parameter
        if not height_parameter:
            raise RuntimeError(
                "Fusion did not create the triangle height parameter."
            )

        width_dimension = self._dimension_line_length(
            sketch,
            first.base,
            "",
            is_driving=False,
            parameter_role="triangleWidth",
        )
        if not width_dimension.parameter:
            raise RuntimeError(
                "Fusion did not create the driven triangle width parameter."
            )

        pitch_v = triangle_height + spacing
        fourth = self._add_seed_triangle(
            sketch,
            origin,
            u_direction,
            v_direction,
            u_vector,
            v_vector,
            center_u=pitch_u,
            base_v=pitch_v,
            width=triangle_width,
            height=seed_height,
            points_up=True,
            size_seed=first,
            equal_altitude=not align_triangles,
        )
        row_locator = sketch.sketchCurves.sketchLines.addByTwoPoints(
            second.midpoint,
            fourth.midpoint,
        )
        row_locator.isConstruction = True
        constraints.addParallel(row_locator, v_direction)
        row_spacing_dimension = (
            sketch.sketchDimensions.addOffsetDimension(
                second.base,
                fourth.base,
                self._seed_point(
                    origin.geometry,
                    u_vector,
                    v_vector,
                    pitch_u,
                    triangle_height + spacing / 2,
                ),
            )
        )
        if (
            not row_spacing_dimension
            or not row_spacing_dimension.parameter
        ):
            raise RuntimeError(
                "Fusion failed to dimension the spacing between triangle rows."
            )
        row_spacing_parameter = row_spacing_dimension.parameter
        self._set_parameter_expression(
            row_spacing_parameter,
            spacing_parameter.name,
        )
        self._name_parameter(
            row_spacing_parameter,
            "triangleRowSpacing",
        )

        third = self._add_seed_triangle(
            sketch,
            origin,
            u_direction,
            v_direction,
            u_vector,
            v_vector,
            center_u=0,
            base_v=2 * triangle_height + spacing,
            width=triangle_width,
            height=seed_height,
            points_up=False,
            size_seed=first,
            equal_altitude=not align_triangles,
        )
        if align_triangles:
            if not row_height_locator:
                raise RuntimeError(
                    "The aligned triangle row-height locator was not created."
                )
            second_row_height_locator = (
                sketch.sketchCurves.sketchLines.addByTwoPoints(
                    fourth.midpoint,
                    self._seed_point(
                        origin.geometry,
                        u_vector,
                        v_vector,
                        pitch_u,
                        2 * triangle_height + spacing,
                    ),
                )
            )
            second_row_height_locator.isConstruction = True
            constraints.addParallel(
                second_row_height_locator,
                v_direction,
            )
            constraints.addEqual(
                row_height_locator,
                second_row_height_locator,
            )
            second_row_locator = (
                sketch.sketchCurves.sketchLines.addByTwoPoints(
                    third.midpoint,
                    second_row_height_locator.endSketchPoint,
                )
            )
            second_row_locator.isConstruction = True
            constraints.addParallel(second_row_locator, u_direction)
            tip_geometry = [
                self._fillet_seed_triangle_tip(
                    sketch,
                    triangle,
                    v_direction,
                    self.inputs.fillet_radius.value,
                )
                for triangle in (first, second, third, fourth)
            ]
            tip_arcs = [item[0] for item in tip_geometry]
            tip_centerlines = [item[1] for item in tip_geometry]
            constraints.addCollinear(
                tip_centerlines[0],
                tip_centerlines[2],
            )
            radius_text = tip_arcs[0].centerSketchPoint.geometry.copy()
            radius_text.translateBy(
                adsk.core.Vector3D.create(
                    self.inputs.fillet_radius.value,
                    self.inputs.fillet_radius.value,
                    0,
                )
            )
            radius_dimension = sketch.sketchDimensions.addRadialDimension(
                tip_arcs[0],
                radius_text,
            )
            if not radius_dimension or not radius_dimension.parameter:
                raise RuntimeError(
                    "Fusion failed to dimension the aligned triangle tip."
                )
            self._set_parameter_expression(
                radius_dimension.parameter,
                self.inputs.fillet_radius.expression,
            )
            self._name_parameter(
                radius_dimension.parameter,
                "triangleTipRadius",
            )
            constraints.addTangent(tip_arcs[0], second.base)
            constraints.addTangent(tip_arcs[1], first.base)
            constraints.addTangent(tip_arcs[2], fourth.base)
            constraints.addTangent(tip_arcs[3], third.base)
            constraints.addEqual(tip_arcs[0], tip_arcs[2])
            constraints.addEqual(tip_arcs[0], tip_arcs[3])
        else:
            constraints.addCollinear(first.altitude, third.altitude)
            second_row_locator = (
                sketch.sketchCurves.sketchLines.addByTwoPoints(
                    third.apex,
                    fourth.midpoint,
                )
            )
            second_row_locator.isConstruction = True
            constraints.addParallel(second_row_locator, u_direction)

        pitch_v_expression = (
            f"({height_parameter.name}) + ({spacing_parameter.name})"
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

    def _has_manual_bounds(self) -> bool:
        return len(self.inputs.bounding_points.value) >= 2

    def _rhombus_dimensions(
        self,
        pitch_u: float,
        pitch_v: float,
        spacing: float,
    ) -> tuple[float, float]:
        """Solve rhombus width and height from the pitches and the true
        edge-to-edge spacing.

        For a rhombus with diagonals w (along u) and h (along v), the gap
        measured along u between two neighbours is s*hypot(w, h)/h and the
        gap along v is s*hypot(w, h)/w. Requiring pitch_u = w + gap_u and
        pitch_v = h + gap_v forces w/h == pitch_u/pitch_v, which reduces to
        the closed form below.
        """
        if pitch_u <= 0 or pitch_v <= 0:
            raise ValueError("The pattern boundary has no usable extent.")
        ratio = pitch_u / pitch_v
        height = pitch_v - spacing * math.sqrt(1 + ratio * ratio) / ratio
        width = ratio * height
        return width, height

    def _create_rhombus_pattern_sketch(
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
        """Two seed rhombuses form the unit cell of the diamond lattice: one
        centred on the boundary corner and one at the half-pitch offset. The
        rectangular pattern repeats both, so every boundary rhombus is
        halved by the clip and the corner ones quartered."""
        sketch = component.sketches.addWithoutEdges(face)
        if not sketch:
            raise RuntimeError("Fusion failed to create the rhombus sketch.")
        sketch.name = "Face Cutout (Native) - Rhombus Seeds"
        # Batch the edits from here on; the solve happens once at the end.
        sketch.isComputeDeferred = True
        boundary = self._create_rectangular_pattern_boundary(
            sketch,
            outer_curves,
        )
        columns = self.inputs.triangle_columns.value
        rows = self.inputs.triangle_rows.value
        pitch_u = boundary.extent_u / columns
        pitch_v = boundary.extent_v / rows
        width, height = self._rhombus_dimensions(
            pitch_u,
            pitch_v,
            self.inputs.triangle_spacing.value,
        )
        if width <= 1e-6 or height <= 1e-6:
            raise ValueError(
                "Spacing is too large for the requested rhombus rows and "
                "columns."
            )

        first = self._add_seed_rhombus(
            sketch,
            boundary,
            center_u=0,
            center_v=0,
            width=width,
            height=height,
        )
        constraints = sketch.geometricConstraints
        constraints.addCoincident(first.center, boundary.origin)

        second = self._add_seed_rhombus(
            sketch,
            boundary,
            center_u=pitch_u / 2,
            center_v=pitch_v / 2,
            width=width,
            height=height,
        )
        constraints.addEqual(first.horizontal, second.horizontal)
        constraints.addEqual(first.vertical, second.vertical)
        half_pitch_u, half_pitch_v = self._locate_offset_rhombus(
            sketch,
            boundary,
            first.center,
            second.center,
            pitch_u,
            pitch_v,
            f"({boundary.u_parameter.name}) / {2 * columns}",
            f"({boundary.v_parameter.name}) / {2 * rows}",
        )

        # The rhombus proportion follows the lattice: its edge is parallel
        # to the line joining the two seed centres exactly when
        # width / height equals pitch_u / pitch_v. That replaces an explicit
        # size formula with a constraint.
        lattice_diagonal = sketch.sketchCurves.sketchLines.addByTwoPoints(
            first.center,
            second.center,
        )
        if not lattice_diagonal:
            raise RuntimeError(
                "Fusion failed to create the rhombus lattice diagonal."
            )
        lattice_diagonal.isConstruction = True
        constraints.addParallel(first.left_top, lattice_diagonal)

        # The perpendicular gap between the facing edges of the two seeds is
        # the true edge-to-edge spacing, so it carries the user's value.
        self._add_spacing_dimension(sketch, first, second)

        # Reference dimensions so the resulting rhombus size is readable in
        # the parameter table without driving anything.
        self._dimension_line_length(
            sketch,
            first.horizontal,
            "",
            is_driving=False,
            parameter_role="rhombusWidth",
        )
        self._dimension_line_length(
            sketch,
            first.vertical,
            "",
            is_driving=False,
            parameter_role="rhombusHeight",
        )

        sketch.isComputeDeferred = False
        self._require_fully_constrained(sketch)
        if sketch.profiles.count != 2:
            raise RuntimeError(
                "The rhombus seed sketch did not create two profiles "
                f"({sketch.profiles.count} found)."
            )
        return (
            sketch,
            boundary.u_direction,
            boundary.v_direction,
            f"2 * {half_pitch_u.name}",
            f"2 * {half_pitch_v.name}",
        )

    def _add_spacing_dimension(
        self,
        sketch: adsk.fusion.Sketch,
        first: _SeedRhombus,
        second: _SeedRhombus,
    ) -> None:
        reference = first.top_right
        facing = second.bottom_left
        text_point = adsk.core.Point3D.create(
            (
                self._line_midpoint(reference).x
                + self._line_midpoint(facing).x
            )
            / 2,
            (
                self._line_midpoint(reference).y
                + self._line_midpoint(facing).y
            )
            / 2,
            0,
        )
        dimension = sketch.sketchDimensions.addOffsetDimension(
            reference,
            facing,
            text_point,
        )
        if not dimension or not dimension.parameter:
            raise RuntimeError(
                "Fusion failed to dimension the rhombus spacing."
            )
        self._set_parameter_expression(
            dimension.parameter,
            self.inputs.triangle_spacing.expression,
        )
        self._name_parameter(dimension.parameter, "rhombusSpacing")

    def _add_seed_rhombus(
        self,
        sketch: adsk.fusion.Sketch,
        boundary: _PatternBoundary,
        center_u: float,
        center_v: float,
        width: float,
        height: float,
    ) -> _SeedRhombus:
        lines = sketch.sketchCurves.sketchLines
        constraints = sketch.geometricConstraints
        origin = boundary.origin.geometry

        def at(u: float, v: float) -> adsk.core.Point3D:
            point = origin.copy()
            point.translateBy(
                adsk.core.Vector3D.create(
                    boundary.u_vector.x * u + boundary.v_vector.x * v,
                    boundary.u_vector.y * u + boundary.v_vector.y * v,
                    0,
                )
            )
            return point

        horizontal = lines.addByTwoPoints(
            at(center_u - width / 2, center_v),
            at(center_u + width / 2, center_v),
        )
        vertical = lines.addByTwoPoints(
            at(center_u, center_v - height / 2),
            at(center_u, center_v + height / 2),
        )
        if not horizontal or not vertical:
            raise RuntimeError("Fusion failed to create a rhombus diagonal.")
        horizontal.isConstruction = True
        vertical.isConstruction = True
        constraints.addParallel(horizontal, boundary.u_direction)
        constraints.addPerpendicular(vertical, horizontal)

        center = sketch.sketchPoints.add(at(center_u, center_v))
        if not center:
            raise RuntimeError("Fusion failed to create a rhombus centre.")
        constraints.addMidPoint(center, horizontal)
        constraints.addMidPoint(center, vertical)

        # The outline reuses the diagonal endpoints, so it needs no
        # constraints of its own.
        left = horizontal.startSketchPoint
        right = horizontal.endSketchPoint
        bottom = vertical.startSketchPoint
        top = vertical.endSketchPoint
        sides: list[adsk.fusion.SketchLine] = []
        for start, end in (
            (left, top),
            (top, right),
            (right, bottom),
            (bottom, left),
        ):
            side = lines.addByTwoPoints(start, end)
            if not side:
                raise RuntimeError("Fusion failed to create a rhombus side.")
            sides.append(side)
        return _SeedRhombus(
            center=center,
            horizontal=horizontal,
            vertical=vertical,
            left_top=sides[0],
            top_right=sides[1],
            right_bottom=sides[2],
            bottom_left=sides[3],
        )

    def _locate_offset_rhombus(
        self,
        sketch: adsk.fusion.Sketch,
        boundary: _PatternBoundary,
        anchor: adsk.fusion.SketchPoint,
        center: adsk.fusion.SketchPoint,
        offset_u: float,
        offset_v: float,
        offset_u_expression: str,
        offset_v_expression: str,
    ) -> tuple[adsk.fusion.ModelParameter, adsk.fusion.ModelParameter]:
        lines = sketch.sketchCurves.sketchLines
        constraints = sketch.geometricConstraints
        origin = anchor.geometry

        def at(u: float, v: float) -> adsk.core.Point3D:
            point = origin.copy()
            point.translateBy(
                adsk.core.Vector3D.create(
                    boundary.u_vector.x * u + boundary.v_vector.x * v,
                    boundary.u_vector.y * u + boundary.v_vector.y * v,
                    0,
                )
            )
            return point

        along_u = lines.addByTwoPoints(anchor, at(offset_u, 0))
        if not along_u:
            raise RuntimeError("Fusion failed to offset a rhombus along u.")
        along_u.isConstruction = True
        constraints.addParallel(along_u, boundary.u_direction)

        along_v = lines.addByTwoPoints(along_u.endSketchPoint, center)
        if not along_v:
            raise RuntimeError("Fusion failed to offset a rhombus along v.")
        along_v.isConstruction = True
        constraints.addPerpendicular(along_v, along_u)

        half_pitch_u = self._dimension_line_length(
            sketch,
            along_u,
            offset_u_expression,
            parameter_role="rhombusHalfPitchU",
        )
        half_pitch_v = self._dimension_line_length(
            sketch,
            along_v,
            offset_v_expression,
            parameter_role="rhombusHalfPitchV",
        )
        if not half_pitch_u.parameter or not half_pitch_v.parameter:
            raise RuntimeError(
                "Fusion did not create the rhombus pitch parameters."
            )
        return half_pitch_u.parameter, half_pitch_v.parameter

    def _create_rectangular_pattern_boundary(
        self,
        sketch: adsk.fusion.Sketch,
        outer_curves: list[adsk.fusion.SketchCurve],
        role_prefix: str = "pattern",
    ) -> _PatternBoundary:
        axis = (
            self.inputs.pattern_axis.value[0]
            if self.inputs.pattern_axis.value
            else None
        )
        bounds = self.inputs.bounding_points.value
        if bounds:
            return self._create_manual_pattern_boundary(
                sketch,
                cast(adsk.core.Base | None, axis),
                cast(list[adsk.core.Base], bounds),
                role_prefix,
            )
        return self._create_automatic_pattern_boundary(
            sketch,
            outer_curves,
            cast(adsk.core.Base | None, axis),
            role_prefix,
        )

    def _create_automatic_pattern_boundary(
        self,
        sketch: adsk.fusion.Sketch,
        outer_curves: list[adsk.fusion.SketchCurve],
        axis: adsk.core.Base | None,
        role_prefix: str = "pattern",
    ) -> _PatternBoundary:
        boundary = [
            line
            for entity in self._project_into_sketch(
                sketch,
                cast(list[adsk.core.Base], outer_curves),
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

        if axis:
            axis_line = self._project_axis_line(sketch, axis)
            axis_vector = self._normalized_line_vector(axis_line)
            alignment = [
                abs(self._normalized_line_vector(line).dotProduct(axis_vector))
                for line in boundary
            ]
            best_alignment = max(alignment)
            if best_alignment < 1 - 1e-5:
                raise ValueError(
                    "Without Bounding Box Points, the Pattern Axis must be "
                    "parallel to an edge of the rectangular offset boundary."
                )
            u_source = boundary[alignment.index(best_alignment)]
        else:
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
            parameter_role=f"{role_prefix}Length",
        )
        v_dimension = self._dimension_line_length(
            sketch,
            v_direction,
            "",
            is_driving=False,
            parameter_role=f"{role_prefix}Width",
        )
        if not u_dimension.parameter or not v_dimension.parameter:
            raise RuntimeError(
                "Fusion failed to measure the rectangular pattern boundary."
            )
        corners, ordered_boundary = self._ordered_rectangular_boundary(
            cast(list[adsk.fusion.SketchCurve], boundary)
        )
        return _PatternBoundary(
            origin=origin,
            u_direction=u_direction,
            v_direction=v_direction,
            extent_u=extent_u,
            extent_v=extent_v,
            u_parameter=u_dimension.parameter,
            v_parameter=v_dimension.parameter,
            u_vector=u_vector,
            v_vector=v_vector,
            corners=corners,
            boundary_lines=ordered_boundary,
        )

    def _create_manual_pattern_boundary(
        self,
        sketch: adsk.fusion.Sketch,
        axis: adsk.core.Base | None,
        bounds: list[adsk.core.Base],
        role_prefix: str = "pattern",
    ) -> _PatternBoundary:
        # Without a Pattern Axis the box is aligned to the sketch axes and
        # held there by horizontal/vertical constraints.
        axis_line = (
            self._project_axis_line(sketch, axis) if axis else None
        )
        u_vector = (
            self._normalized_line_vector(axis_line)
            if axis_line
            else adsk.core.Vector3D.create(1, 0, 0)
        )
        v_vector = adsk.core.Vector3D.create(
            -u_vector.y,
            u_vector.x,
            0,
        )
        if not v_vector.normalize():
            raise ValueError(
                "The Pattern Axis cannot be projected into the selected face."
            )

        projected_points = [
            point
            for entity in self._project_into_sketch(sketch, bounds)
            if (point := adsk.fusion.SketchPoint.cast(entity))
        ]
        if len(projected_points) != len(bounds):
            raise ValueError(
                "Fusion could not project every Bounding Box Point into the "
                "selected face."
            )

        reference = (
            axis_line.startSketchPoint.geometry
            if axis_line
            else adsk.core.Point3D.create(0, 0, 0)
        )
        coordinates: list[tuple[float, float, adsk.fusion.SketchPoint]] = []
        for point in projected_points:
            offset = reference.vectorTo(point.geometry)
            coordinates.append(
                (
                    offset.dotProduct(u_vector),
                    offset.dotProduct(v_vector),
                    point,
                )
            )

        min_u = min(item[0] for item in coordinates)
        max_u = max(item[0] for item in coordinates)
        min_v = min(item[1] for item in coordinates)
        max_v = max(item[1] for item in coordinates)
        extent_u = max_u - min_u
        extent_v = max_v - min_v
        if extent_u <= 1e-6 or extent_v <= 1e-6:
            raise ValueError(
                "The Bounding Box Points must define non-zero extents both "
                "along and perpendicular to the Pattern Axis."
            )

        def box_point(u: float, v: float) -> adsk.core.Point3D:
            point = reference.copy()
            point.translateBy(
                adsk.core.Vector3D.create(
                    u_vector.x * u + v_vector.x * v,
                    u_vector.y * u + v_vector.y * v,
                    0,
                )
            )
            return point

        lower_left = box_point(min_u, min_v)
        lower_right = box_point(max_u, min_v)
        upper_right = box_point(max_u, max_v)
        upper_left = box_point(min_u, max_v)
        lines = sketch.sketchCurves.sketchLines
        bottom = lines.addByTwoPoints(lower_left, lower_right)
        right = lines.addByTwoPoints(bottom.endSketchPoint, upper_right)
        top = lines.addByTwoPoints(right.endSketchPoint, upper_left)
        left = lines.addByTwoPoints(bottom.startSketchPoint, top.endSketchPoint)
        boundary = [bottom, right, top, left]
        self._set_construction(
            sketch,
            cast(list[adsk.fusion.SketchCurve], boundary),
            True,
        )

        constraints = sketch.geometricConstraints
        if axis_line:
            constraints.addParallel(bottom, axis_line)
            constraints.addPerpendicular(right, axis_line)
            constraints.addParallel(top, axis_line)
            constraints.addPerpendicular(left, axis_line)
        else:
            constraints.addHorizontal(bottom)
            constraints.addHorizontal(top)
            constraints.addVertical(right)
            constraints.addVertical(left)

        extreme_points = [
            (
                min(coordinates, key=lambda item: item[1])[2],
                bottom,
            ),
            (
                max(coordinates, key=lambda item: item[0])[2],
                right,
            ),
            (
                max(coordinates, key=lambda item: item[1])[2],
                top,
            ),
            (
                min(coordinates, key=lambda item: item[0])[2],
                left,
            ),
        ]
        for point, line in extreme_points:
            constraints.addCoincident(point, line)

        origin = bottom.startSketchPoint
        # Optionally shrink the box by the outer inset. A single offset
        # constraint driven by the outer-contour inset parameter keeps the
        # two insets one user-editable value; the box built from the points
        # stays behind as construction geometry.
        inset = self._bounding_box_inset()
        if inset > 1e-9:
            if 2 * inset >= min(extent_u, extent_v) - 1e-6:
                raise ValueError(
                    "Outer Inset is too large to inset the bounding box."
                )
            expression = (
                self._outer_inset_parameter.name
                if self._outer_inset_parameter
                else self.inputs.outer_inset.expression
            )
            inset_curves, _ = self._offset_loop(
                sketch=sketch,
                source_curves=cast(list[adsk.fusion.SketchCurve], boundary),
                expression=expression,
                should_be_smaller=True,
                parameter_role=f"{role_prefix}Inset",
            )
            self._set_construction(sketch, inset_curves, True)
            inset_lines = [
                line
                for curve in inset_curves
                if (line := adsk.fusion.SketchLine.cast(curve))
            ]
            if len(inset_lines) != 4:
                raise RuntimeError(
                    "The bounding box inset did not produce four lines."
                )
            bottom = self._nearest_parallel_line(inset_lines, bottom)
            left = self._nearest_parallel_line(inset_lines, left)
            boundary = inset_lines
            extent_u -= 2 * inset
            extent_v -= 2 * inset
            # The inset corner next to the outer box's origin corner takes
            # over the origin role.
            origin = min(
                (bottom.startSketchPoint, bottom.endSketchPoint),
                key=lambda point: point.geometry.distanceTo(lower_left),
            )

        u_dimension = self._dimension_line_length(
            sketch,
            bottom,
            "",
            is_driving=False,
            parameter_role=f"{role_prefix}Length",
        )
        v_dimension = self._dimension_line_length(
            sketch,
            left,
            "",
            is_driving=False,
            parameter_role=f"{role_prefix}Width",
        )
        if not u_dimension.parameter or not v_dimension.parameter:
            raise RuntimeError(
                "Fusion failed to measure the manual pattern boundary."
            )
        corners, ordered_boundary = self._ordered_rectangular_boundary(
            cast(list[adsk.fusion.SketchCurve], boundary)
        )
        return _PatternBoundary(
            origin=origin,
            u_direction=bottom,
            v_direction=left,
            extent_u=extent_u,
            extent_v=extent_v,
            u_parameter=u_dimension.parameter,
            v_parameter=v_dimension.parameter,
            u_vector=u_vector,
            v_vector=v_vector,
            corners=corners,
            boundary_lines=ordered_boundary,
        )

    def _project_axis_line(
        self,
        sketch: adsk.fusion.Sketch,
        axis: adsk.core.Base,
    ) -> adsk.fusion.SketchLine:
        projected = [
            line
            for entity in self._project_into_sketch(sketch, [axis])
            if (line := adsk.fusion.SketchLine.cast(entity))
        ]
        if len(projected) != 1 or projected[0].length <= 1e-6:
            raise ValueError(
                "The Pattern Axis must be a straight entity with a usable "
                "projection into the selected face."
            )
        projected[0].isConstruction = True
        return projected[0]

    def _bounding_box_inset(self) -> float:
        """Inset applied to the manual bounding box, in internal units."""
        if not self.inputs.inset_bounding_box.value:
            return 0.0
        return self.inputs.outer_inset.value

    def _nearest_parallel_line(
        self,
        candidates: list[adsk.fusion.SketchLine],
        reference: adsk.fusion.SketchLine,
    ) -> adsk.fusion.SketchLine:
        """The candidate parallel to `reference` that lies closest to it —
        e.g. the inset counterpart of an outer boundary side."""
        reference_direction = self._normalized_line_vector(reference)
        reference_midpoint = self._line_midpoint(reference)
        parallels = [
            line
            for line in candidates
            if abs(
                self._normalized_line_vector(line).dotProduct(
                    reference_direction
                )
            )
            > 1 - 1e-5
        ]
        if not parallels:
            raise RuntimeError(
                "The bounding box inset lost a boundary direction."
            )
        return min(
            parallels,
            key=lambda line: self._line_midpoint(line).distanceTo(
                reference_midpoint
            ),
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

    def _add_seed_triangle(
        self,
        sketch: adsk.fusion.Sketch,
        origin: adsk.fusion.SketchPoint,
        u_direction: adsk.fusion.SketchLine,
        v_direction: adsk.fusion.SketchLine,
        u_vector: adsk.core.Vector3D,
        v_vector: adsk.core.Vector3D,
        center_u: float,
        base_v: float,
        width: float,
        height: float,
        points_up: bool,
        size_seed: _SeedTriangle | None = None,
        equal_altitude: bool = True,
    ) -> _SeedTriangle:
        base_start_geometry = self._seed_point(
            origin.geometry,
            u_vector,
            v_vector,
            center_u - width / 2,
            base_v,
        )
        base_end_geometry = self._seed_point(
            origin.geometry,
            u_vector,
            v_vector,
            center_u + width / 2,
            base_v,
        )
        apex_geometry = self._seed_point(
            origin.geometry,
            u_vector,
            v_vector,
            center_u,
            base_v + (height if points_up else -height),
        )
        lines = sketch.sketchCurves.sketchLines
        base = lines.addByTwoPoints(
            base_start_geometry,
            base_end_geometry,
        )
        constraints = sketch.geometricConstraints
        constraints.addParallel(base, u_direction)

        midpoint = sketch.sketchPoints.add(
            self._seed_point(
                origin.geometry,
                u_vector,
                v_vector,
                center_u,
                base_v,
            )
        )
        constraints.addMidPoint(midpoint, base)
        apex = sketch.sketchPoints.add(apex_geometry)
        altitude = lines.addByTwoPoints(midpoint, apex)
        altitude.isConstruction = True
        constraints.addParallel(altitude, v_direction)
        right_side = lines.addByTwoPoints(base.endSketchPoint, apex)
        left_side = lines.addByTwoPoints(apex, base.startSketchPoint)

        if size_seed:
            constraints.addEqual(size_seed.base, base)
            if equal_altitude:
                constraints.addEqual(size_seed.altitude, altitude)
        return _SeedTriangle(
            base=base,
            altitude=altitude,
            right_side=right_side,
            left_side=left_side,
            midpoint=midpoint,
            apex=apex,
        )

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

    def _aligned_triangle_seed_height(
        self,
        width: float,
        visible_height: float,
        radius: float,
    ) -> float:
        half_width = width / 2
        if half_width <= 1e-6:
            raise ValueError("The requested triangle pattern has no usable width.")

        # This only supplies stable initial geometry to Fusion's solver. The
        # sketch constraints determine the final virtual apex position.
        seed_height = visible_height
        for _ in range(12):
            half_angle_sine = half_width / math.hypot(
                half_width,
                seed_height,
            )
            if half_angle_sine <= 1e-6:
                raise ValueError(
                    "The fillet radius is too large for the triangle pattern."
                )
            seed_height = (
                visible_height
                + radius * (1 / half_angle_sine - 1)
            )
        return seed_height

    def _fillet_seed_triangle_tip(
        self,
        sketch: adsk.fusion.Sketch,
        triangle: _SeedTriangle,
        v_direction: adsk.fusion.SketchLine,
        radius: float,
    ) -> tuple[adsk.fusion.SketchArc, adsk.fusion.SketchLine]:
        right_tip = triangle.right_side.endSketchPoint.geometry
        left_tip = triangle.left_side.startSketchPoint.geometry
        arc = sketch.sketchCurves.sketchArcs.addFillet(
            triangle.right_side,
            right_tip,
            triangle.left_side,
            left_tip,
            radius,
        )
        if not arc:
            raise ValueError(
                "The fillet radius is too large for the triangle tips."
            )

        if triangle.altitude.isValid and not triangle.altitude.deleteMe():
            raise RuntimeError(
                "Fusion failed to replace a triangle construction altitude."
            )

        # Replace the virtual sharp altitude with a compact symmetry line from
        # the base midpoint to the fillet center.
        centerline = sketch.sketchCurves.sketchLines.addByTwoPoints(
            triangle.midpoint,
            arc.centerSketchPoint,
        )
        centerline.isConstruction = True
        constraints = sketch.geometricConstraints
        constraints.addParallel(centerline, v_direction)
        return arc, centerline

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
            self._set_parameter_expression(dimension.parameter, expression)
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
        face_index: int,
        face_count: int,
        quantity_u: int | None = None,
        quantity_v: int | None = None,
        distance_multiplier: int = 2,
    ) -> adsk.fusion.RectangularPatternFeature | None:
        if quantity_u is None:
            quantity_u = max(
                1,
                math.ceil((self.inputs.triangle_columns.value + 1) / 2),
            )
        if quantity_v is None:
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
                    f"{distance_multiplier} * ({pitch_u_expression})"
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
                f"{distance_multiplier} * ({pitch_v_expression})"
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
        pattern.name = self._feature_name(
            "Face Cutout (Native) - Solid Triangle Pattern",
            face_index,
            face_count,
        )
        for parameter, role in (
            (
                pattern.quantityOne,
                "trianglePatternColumnGroups",
            ),
            (
                pattern.distanceOne,
                "trianglePatternPitchU",
            ),
            (
                pattern.quantityTwo,
                "trianglePatternRowGroups",
            ),
            (
                pattern.distanceTwo,
                "trianglePatternPitchV",
            ),
        ):
            if parameter:
                self._name_parameter(
                    parameter,
                    self._face_parameter_role(
                        role,
                        face_index,
                        face_count,
                    ),
                )
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

    def _create_tool_extrude(
        self,
        component: adsk.fusion.Component,
        sketch: adsk.fusion.Sketch,
        profiles: list[adsk.fusion.Profile],
        start_face: adsk.fusion.BRepFace,
        opposite_face: adsk.fusion.BRepFace,
        cut_direction: adsk.core.Vector3D,
        face_index: int,
        face_count: int,
    ) -> adsk.fusion.ExtrudeFeature:
        if not profiles:
            raise RuntimeError("The cutout sketch does not contain any tool profiles.")
        profile_input: adsk.core.Base | adsk.core.ObjectCollection
        if len(profiles) == 1:
            profile_input = profiles[0]
        else:
            profile_input = adsk.core.ObjectCollection.createWithArray(
                cast(list[adsk.core.Base], profiles)
            )
        extrude_input = component.features.extrudeFeatures.createInput(
            profile_input,
            adsk.fusion.FeatureOperations.NewBodyFeatureOperation,  # type: ignore
        )
        if not extrude_input:
            raise RuntimeError("Fusion failed to initialize the cutout tool extrude.")

        self._set_extrude_start(extrude_input, start_face)
        # A negative to-entity offset stops before the entity in the extrude
        # direction, leaving material at the opposite face. Later extrudes
        # reference the first named offset parameter instead of duplicating
        # the user expression.
        extent = adsk.fusion.ToEntityExtentDefinition.create(
            opposite_face,
            False,
            adsk.core.ValueInput.createByString(
                self._remainder_offset_expression()
            ),
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
        if not extrude or extrude.bodies.count == 0:
            raise RuntimeError(
                "The cutout profiles did not produce any solid tool bodies."
            )
        extrude.name = self._feature_name(
            "Face Cutout (Native) - Tool",
            face_index,
            face_count,
        )
        self._name_extrude_parameters(
            extrude,
            "tool",
            face_index,
            face_count,
        )
        return extrude

    def _create_pattern_extrude(
        self,
        component: adsk.fusion.Component,
        sketch: adsk.fusion.Sketch,
        start_face: adsk.fusion.BRepFace,
        opposite_face: adsk.fusion.BRepFace,
        cut_direction: adsk.core.Vector3D,
        face_index: int,
        face_count: int,
        base_name: str = "Face Cutout (Native) - Triangle Pattern",
        role_prefix: str = "triangle",
        selected_profiles: list[adsk.fusion.Profile] | None = None,
    ) -> adsk.fusion.ExtrudeFeature:
        profiles = adsk.core.ObjectCollection.create()
        for profile in (
            selected_profiles
            if selected_profiles is not None
            else sketch.profiles
        ):
            profiles.add(profile)
        if profiles.count == 0:
            raise RuntimeError(f"'{sketch.name}' does not contain any profiles.")

        extrude_input = component.features.extrudeFeatures.createInput(
            profiles,
            adsk.fusion.FeatureOperations.NewBodyFeatureOperation,  # type: ignore
        )
        if not extrude_input:
            raise RuntimeError("Fusion failed to initialize the triangle extrude.")

        self._set_extrude_start(extrude_input, start_face)
        extent = adsk.fusion.ToEntityExtentDefinition.create(
            opposite_face,
            False,
            adsk.core.ValueInput.createByString(
                self._remainder_offset_expression()
            ),
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
            raise RuntimeError(f"'{sketch.name}' did not produce tool bodies.")
        extrude.name = self._feature_name(
            base_name,
            face_index,
            face_count,
        )
        self._name_extrude_parameters(
            extrude,
            role_prefix,
            face_index,
            face_count,
        )
        return extrude

    def _remainder_offset_expression(self) -> str:
        return (
            self._remainder_parameter_name
            or f"-({self.inputs.remaining_material.expression})"
        )

    def _name_extrude_parameters(
        self,
        extrude: adsk.fusion.ExtrudeFeature,
        role_prefix: str,
        face_index: int,
        face_count: int,
    ) -> None:
        start = adsk.fusion.FromEntityStartDefinition.cast(
            extrude.startExtent
        )
        start_offset = (
            adsk.fusion.ModelParameter.cast(start.offset)
            if start
            else None
        )
        extent = adsk.fusion.ToEntityExtentDefinition.cast(
            extrude.extentOne
        )
        end_offset = (
            adsk.fusion.ModelParameter.cast(extent.offset)
            if extent
            else None
        )
        for parameter, role in (
            (start_offset, f"{role_prefix}StartOffset"),
            (end_offset, f"{role_prefix}RemainingMaterial"),
            (
                extrude.taperAngleOne,
                f"{role_prefix}TaperAngle",
            ),
        ):
            if parameter:
                self._name_parameter(
                    parameter,
                    self._face_parameter_role(
                        role,
                        face_index,
                        face_count,
                    ),
                )
        if end_offset and self._remainder_parameter_name is None:
            self._remainder_parameter_name = end_offset.name

    def _set_extrude_start(
        self,
        extrude_input: adsk.fusion.ExtrudeFeatureInput,
        start_face: adsk.fusion.BRepFace,
    ) -> None:
        start = adsk.fusion.FromEntityStartDefinition.create(
            start_face,
            adsk.core.ValueInput.createByReal(0),
        )
        if not start:
            raise RuntimeError(
                "Fusion failed to define a selected-face extrusion start."
            )
        extrude_input.startExtent = start

    def _create_intersect_combine(
        self,
        component: adsk.fusion.Component,
        target_body: adsk.fusion.BRepBody,
        tool_bodies: list[adsk.fusion.BRepBody],
        face_index: int,
        face_count: int,
        base_name: str = "Face Cutout (Native) - Pattern Intersection",
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
            raise RuntimeError(
                "The pattern did not intersect the full cutout tool."
            )
        combine.name = self._feature_name(
            base_name,
            face_index,
            face_count,
        )
        return combine

    def _create_tool_fillets(
        self,
        component: adsk.fusion.Component,
        tool_bodies: list[adsk.fusion.BRepBody],
        cut_direction: adsk.core.Vector3D,
        face_index: int,
        face_count: int,
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
            base_name = (
                "Face Cutout (Native) - Fillet"
                if len(fillets) == 1
                else f"Face Cutout (Native) - Fillet Part {index}"
            )
            fillet.name = self._feature_name(
                base_name,
                face_index,
                face_count,
            )
            edge_set = (
                adsk.fusion.ConstantRadiusFilletEdgeSet.cast(
                    fillet.edgeSets.item(0)
                )
                if fillet.edgeSets.count
                else None
            )
            if edge_set and edge_set.radius:
                base_role = (
                    "filletRadius"
                    if len(fillets) == 1
                    else f"filletRadiusPart{index}"
                )
                self._name_parameter(
                    edge_set.radius,
                    self._face_parameter_role(
                        base_role,
                        face_index,
                        face_count,
                    ),
                )
                if edge_set.tangencyWeight:
                    weight_role = (
                        "filletTangencyWeight"
                        if len(fillets) == 1
                        else f"filletTangencyWeightPart{index}"
                    )
                    self._name_parameter(
                        edge_set.tangencyWeight,
                        self._face_parameter_role(
                            weight_role,
                            face_index,
                            face_count,
                        ),
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
        body_index: int,
        body_count: int,
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
        combine.name = (
            "Face Cutout (Native) - Cut"
            if body_count == 1
            else f"Face Cutout (Native) - Cut (Body {body_index})"
        )
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
            group.name = "Face Cutout (Native)"
            group.isCollapsed = True

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
        candidates: list[adsk.fusion.Profile] = []
        for profile in sketch.profiles:
            outer_loop = next((loop for loop in profile.profileLoops if loop.isOuter), None)
            if not outer_loop:
                continue
            uses_outer_curve = any(
                profile_curve.sketchEntity
                and any(
                    profile_curve.sketchEntity == outer_curve
                    for outer_curve in outer_curves
                )
                for profile_curve in outer_loop.profileCurves
            )
            if uses_outer_curve:
                candidates.append(profile)
        if not candidates:
            return None
        return max(candidates, key=lambda profile: profile.areaProperties().area)

    def _project_face_loops(
        self,
        sketch: adsk.fusion.Sketch,
        loops: list[adsk.fusion.BRepLoop],
    ) -> list[list[adsk.fusion.SketchCurve]]:
        """Projects every loop of a face, grouped per loop.

        One call per loop, which costs one sketch compute per loop, because
        projecting is the one part of building these sketches that cannot run
        compute-deferred. Passing every loop's edges to a single project2 call
        would cost only one compute, but project2 does NOT guarantee that it
        returns curves in the order the entities were passed: on a nine-loop
        face it silently returned them in an order that put a stray line in a
        hole's group. There is no order to slice a flat result apart by, so
        the loops are asked for one at a time.
        """
        grouped: list[list[adsk.fusion.SketchCurve]] = []
        for loop in loops:
            edges = cast(list[adsk.core.Base], utils.fusion.as_list(loop.edges))
            curves = [
                curve
                for entity in self._project_into_sketch(sketch, edges)
                if (curve := adsk.fusion.SketchCurve.cast(entity))
            ]
            if not curves:
                raise RuntimeError("Fusion failed to project one of the face loops.")
            grouped.append(curves)
        return grouped

    def _project_into_sketch(
        self,
        sketch: adsk.fusion.Sketch,
        entities: list[adsk.core.Base],
    ) -> list[adsk.core.Base]:
        """sketch.project2 with compute temporarily live.

        project2 raises InternalValidationError on a compute-deferred
        sketch, so projections briefly leave the batching mode. Going live
        also computes the sketch, so profile reads right after a projection
        need no extra solve.
        """
        was_deferred = sketch.isComputeDeferred
        if was_deferred:
            sketch.isComputeDeferred = False
        try:
            return list(sketch.project2(entities, True))
        finally:
            if was_deferred:
                sketch.isComputeDeferred = True

    def _solve_deferred(self, sketch: adsk.fusion.Sketch) -> None:
        """Requests one sketch compute while edits are batched.

        Every geometry, constraint or dimension write to a live sketch makes
        Fusion run a full compute cycle, so the sketch builders keep
        isComputeDeferred set and solve explicitly right before the reads
        that need computed state (profiles, areas, the constraint status).
        No-op when the sketch is not deferred: compute already ran.
        """
        if sketch.isComputeDeferred:
            sketch.isComputeDeferred = False
            sketch.isComputeDeferred = True

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
            "Face Cutout (Native) generated an under-constrained sketch "
            f"({len(unconstrained)} unconstrained curves: {details})."
        )
