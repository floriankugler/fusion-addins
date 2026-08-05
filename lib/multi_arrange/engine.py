"""The multi-arrange pipeline.

Fusion's Arrange feature is used purely as a nesting solver:

1. Every part (and every rigid group) is copied into a temporary, flat,
   grain-aligned single-body proxy component. Groups become one body joined by
   thin bridges, because the solver only collision-checks a single body per
   component.
2. One True Shape Arrange runs over all proxies against the selected envelope
   profile (the multi-sheet gutter profile produced by the envelope add-in, or
   any other single profile).
3. The placement transforms are read back, the Arrange feature and the proxies
   are deleted, and clean per-part bodies are placed at the solved positions —
   either as copies or by moving the original bodies.

Nothing of the solver machinery survives; the remaining timeline entries are
wrapped in one timeline group.
"""

import adsk.core, adsk.fusion
import math
from dataclasses import dataclass

from . import model


BRIDGE_WIDTH = 0.2       # cm; thin enough that no real part can span it
PROXY_PREFIX = 'ma_proxy'
RESULT_COMPONENT_NAME = 'Multi-Arrange'
TIMELINE_GROUP_NAME = 'Multi-Arrange'


@dataclass
class Options:
    object_spacing: float = 0.0       # cm
    frame_width: float = 0.0          # cm
    placement_clearance: float = 0.0  # cm
    part_in_part: bool = True
    create_copies: bool = True


class MultiArrangeError(RuntimeError):
    pass


# ------------------------------------------------------------------ matrices

def multiply(a: adsk.core.Matrix3D, b: adsk.core.Matrix3D) -> adsk.core.Matrix3D:
    """Returns a @ b (apply b first, then a), via explicit row-major math."""
    am = a.asArray()
    bm = b.asArray()
    rm = [0.0] * 16
    for row in range(4):
        for col in range(4):
            rm[row * 4 + col] = sum(am[row * 4 + k] * bm[k * 4 + col] for k in range(4))
    result = adsk.core.Matrix3D.create()
    result.setWithArray(rm)
    return result


def inverted(matrix: adsk.core.Matrix3D) -> adsk.core.Matrix3D:
    result = matrix.copy()
    if not result.invert():
        raise MultiArrangeError('Failed to invert a part placement matrix.')
    return result


# ------------------------------------------------------------------ frames

def face_normal(face: adsk.fusion.BRepFace) -> adsk.core.Vector3D:
    ok, normal = face.evaluator.getNormalAtPoint(face.pointOnFace)
    if not ok:
        raise MultiArrangeError(f"Could not evaluate the normal of a face on '{face.body.name}'.")
    normal.normalize()
    return normal


def longest_linear_edge_direction(face: adsk.fusion.BRepFace) -> adsk.core.Vector3D | None:
    best = None
    best_length = 0.0
    for edge in face.edges:
        geometry = edge.geometry
        if isinstance(geometry, adsk.core.Line3D) and edge.length > best_length:
            best_length = edge.length
            best = geometry.startPoint.vectorTo(geometry.endPoint)
    if best is None:
        return None
    best.normalize()
    return best


def project_onto_plane(vector: adsk.core.Vector3D, normal: adsk.core.Vector3D) -> adsk.core.Vector3D:
    projected = vector.copy()
    offset = normal.copy()
    offset.scaleBy(vector.dotProduct(normal))
    projected.subtract(offset)
    return projected


def component_x_direction(body: adsk.fusion.BRepBody) -> adsk.core.Vector3D:
    """World direction of the X axis of the body's parent component."""
    x_axis = adsk.core.Vector3D.create(1.0, 0.0, 0.0)
    context = body.assemblyContext
    if context is not None:
        x_axis.transformBy(context.transform2)
        x_axis.normalize()
    return x_axis


def part_frame(part: model.Part) -> adsk.core.Matrix3D:
    """Local->world frame: origin at the body's lowest point along the face
    normal, z along the top face normal, x along the grain direction."""
    z_axis = face_normal(part.top_face)

    # Grain candidates, most authoritative first: a stored explicit reference,
    # the appearance texture's grain axis (only meaningful when it lies in the
    # face plane, i.e. the user oriented the wood texture), the longest
    # straight edge of the top face, the parent component's X axis, then any
    # world axis. Parts without straight edges (e.g. discs) always end up with
    # a usable, stable direction.
    candidates = []
    if part.grain is not None:
        candidates.append(part.grain)
    texture_direction = model.texture_grain_direction(part.body)
    if texture_direction is not None:
        candidates.append(texture_direction)
    edge_direction = longest_linear_edge_direction(part.top_face)
    if edge_direction is not None:
        candidates.append(edge_direction)
    candidates.append(component_x_direction(part.body))
    candidates.append(adsk.core.Vector3D.create(1.0, 0.0, 0.0))
    candidates.append(adsk.core.Vector3D.create(0.0, 1.0, 0.0))
    candidates.append(adsk.core.Vector3D.create(0.0, 0.0, 1.0))
    x_axis = None
    for candidate in candidates:
        projected = project_onto_plane(candidate, z_axis)
        if projected.length > 1e-2:
            x_axis = projected
            break
    if x_axis is None:
        raise MultiArrangeError(
            f"Could not derive a grain direction for part '{part.body.name}'."
        )
    x_axis.normalize()
    # Grain runs along the sheet's Y axis (its height): the solver aligns a
    # proxy's local X with the envelope X, so the grain goes into the frame's
    # Y axis and the across-grain direction into X.
    y_axis = x_axis
    x_axis = y_axis.crossProduct(z_axis)
    x_axis.normalize()

    # Drop the origin to the body's lowest bounding-box corner along the
    # normal, so the proxy body sits on z >= 0 and the solver keeps it upright.
    box = part.body.boundingBox
    corners = [
        adsk.core.Point3D.create(x, y, z)
        for x in (box.minPoint.x, box.maxPoint.x)
        for y in (box.minPoint.y, box.maxPoint.y)
        for z in (box.minPoint.z, box.maxPoint.z)
    ]
    centroid = part.top_face.centroid
    min_height = min(corner.asVector().dotProduct(z_axis) for corner in corners)
    drop = centroid.asVector().dotProduct(z_axis) - min_height
    origin = centroid.copy()
    origin.translateBy(scaled(z_axis, -drop))

    frame = adsk.core.Matrix3D.create()
    frame.setWithCoordinateSystem(origin, x_axis, y_axis, z_axis)
    return frame


def scaled(vector: adsk.core.Vector3D, factor: float) -> adsk.core.Vector3D:
    result = vector.copy()
    result.scaleBy(factor)
    return result


def group_frame(parts: list[model.Part]) -> adsk.core.Matrix3D:
    """Shared frame for a rigid group, based on the first member's orientation
    but with the origin dropped low enough for every member."""
    reference = part_frame(parts[0])
    z_axis = adsk.core.Vector3D.create(reference.getCell(0, 2), reference.getCell(1, 2), reference.getCell(2, 2))

    for part in parts[1:]:
        normal = face_normal(part.top_face)
        if abs(normal.dotProduct(z_axis)) < 0.999:
            raise MultiArrangeError(
                f"The top faces of group parts '{parts[0].body.name}' and "
                f"'{part.body.name}' are not parallel."
            )
        if normal.dotProduct(z_axis) < 0:
            raise MultiArrangeError(
                f"The top face of group part '{part.body.name}' points away from "
                f"the rest of its group."
            )

    min_height = math.inf
    for part in parts:
        box = part.body.boundingBox
        for x in (box.minPoint.x, box.maxPoint.x):
            for y in (box.minPoint.y, box.maxPoint.y):
                for z in (box.minPoint.z, box.maxPoint.z):
                    height = adsk.core.Point3D.create(x, y, z).asVector().dotProduct(z_axis)
                    min_height = min(min_height, height)

    origin = adsk.core.Point3D.create(
        reference.translation.x, reference.translation.y, reference.translation.z)
    current_height = origin.asVector().dotProduct(z_axis)
    origin.translateBy(scaled(z_axis, min_height - current_height))

    frame = reference.copy()
    frame.setCell(0, 3, origin.x)
    frame.setCell(1, 3, origin.y)
    frame.setCell(2, 3, origin.z)
    return frame


# ------------------------------------------------------------------ proxies

@dataclass
class Proxy:
    occurrence: adsk.fusion.Occurrence
    frame: adsk.core.Matrix3D            # local->world frame of the source part(s)
    parts: list[model.Part]
    rotation_type: int
    flip: bool = False                   # counteract the solver's largest-face-up normalization
    rotation_correction: float = 0.0     # counteract the solver's in-plane re-orientation
    placement: adsk.core.Matrix3D | None = None  # world transform of the solved copy


def largest_face_is_bottom(body: adsk.fusion.BRepBody) -> bool:
    """Whether the body's largest horizontal face is its bottom face.

    The solver normalizes every part so its largest face points UP (in all
    rotation modes; the API docs claim downward, which is wrong). A part whose
    largest face is at the bottom would therefore be placed upside-down;
    setting isDirectionFlipped on its arrange component compensates (verified:
    the flag composes with the normalization in every rotation mode)."""
    top_area = 0.0
    bottom_area = 0.0
    for index in range(body.faces.count):
        face = body.faces.item(index)
        if not isinstance(face.geometry, adsk.core.Plane):
            continue
        ok, normal = face.evaluator.getNormalAtPoint(face.pointOnFace)
        if not ok:
            continue
        if normal.z > 0.99:
            top_area = max(top_area, face.area)
        elif normal.z < -0.99:
            bottom_area = max(bottom_area, face.area)
    return bottom_area > top_area + 1e-9


def rotation_type_for(rotations: list[int]) -> int:
    types = adsk.fusion.ArrangeRotationTypes
    if model.ROTATION_GRAIN_ONE_WAY in rotations:
        return types.NoneArrangeRotationType
    if model.ROTATION_GRAIN in rotations:
        return types.Only180ArrangeRotationType
    return types.AllRotationsArrangeRotationType


def add_body_to_component(component: adsk.fusion.Component, body: adsk.fusion.BRepBody) -> adsk.fusion.BRepBody:
    """Adds a temporary BRep body, honoring parametric vs direct design mode."""
    design = component.parentDesign
    if design.designType == adsk.fusion.DesignTypes.ParametricDesignType:
        base = component.features.baseFeatures.add()
        base.startEdit()
        try:
            added = component.bRepBodies.add(body, base)
        finally:
            base.finishEdit()
        return added
    return component.bRepBodies.add(body)


def build_proxy(root: adsk.fusion.Component, index: int, parts: list[model.Part],
                frame: adsk.core.Matrix3D) -> Proxy:
    temp_manager = adsk.fusion.TemporaryBRepManager.get()
    to_local = inverted(frame)

    bodies = []
    for part in parts:
        copy = temp_manager.copy(part.body)
        temp_manager.transform(copy, to_local)
        bodies.append(copy)

    merged = bodies[0]
    if len(bodies) > 1:
        centers = [body_center_2d(body) for body in bodies]
        connected = {0}
        for _ in range(len(bodies) - 1):
            best = None
            for i in connected:
                for j in range(len(bodies)):
                    if j in connected:
                        continue
                    distance = math.hypot(centers[i][0] - centers[j][0], centers[i][1] - centers[j][1])
                    if best is None or distance < best[0]:
                        best = (distance, i, j)
            if best is None:
                break
            _, i, j = best
            connected.add(j)
            bridge = bridge_body(temp_manager, bodies[i], bodies[j], centers[i], centers[j])
            temp_manager.booleanOperation(merged, bridge, adsk.fusion.BooleanTypes.UnionBooleanType)
        for body in bodies[1:]:
            temp_manager.booleanOperation(merged, body, adsk.fusion.BooleanTypes.UnionBooleanType)

    occurrence = root.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    occurrence.component.name = f'{PROXY_PREFIX}_{index}'
    added = add_body_to_component(occurrence.component, merged)
    if len(parts) > 1 and count_lumps(added) > 1:
        raise MultiArrangeError(
            f"Could not bridge the parts of group '{parts[0].settings.group}' into "
            'a single connected proxy body.'
        )
    rotations = [part.settings.rotation for part in parts]
    return Proxy(occurrence=occurrence, frame=frame, parts=parts,
                 rotation_type=rotation_type_for(rotations),
                 flip=largest_face_is_bottom(added))


def body_center_2d(body: adsk.fusion.BRepBody) -> tuple[float, float]:
    box = body.boundingBox
    return ((box.minPoint.x + box.maxPoint.x) / 2.0, (box.minPoint.y + box.maxPoint.y) / 2.0)


def bridge_body(temp_manager: adsk.fusion.TemporaryBRepManager,
                body_a: adsk.fusion.BRepBody, body_b: adsk.fusion.BRepBody,
                center_a: tuple[float, float], center_b: tuple[float, float]) -> adsk.fusion.BRepBody:
    """A thin plate connecting the two bodies, spanning centroid to centroid."""
    dx = center_b[0] - center_a[0]
    dy = center_b[1] - center_a[1]
    length = math.hypot(dx, dy)
    if length < 1e-6:
        raise MultiArrangeError('Two group parts occupy the same position.')
    direction = adsk.core.Vector3D.create(dx / length, dy / length, 0.0)
    width_direction = adsk.core.Vector3D.create(-direction.y, direction.x, 0.0)

    height = min(body_a.boundingBox.maxPoint.z, body_b.boundingBox.maxPoint.z)
    if height <= 1e-6:
        raise MultiArrangeError('Group parts have no thickness overlap for bridging.')
    center = adsk.core.Point3D.create(
        (center_a[0] + center_b[0]) / 2.0,
        (center_a[1] + center_b[1]) / 2.0,
        height / 2.0,
    )
    box = adsk.core.OrientedBoundingBox3D.create(
        center, direction, width_direction, length, BRIDGE_WIDTH, height)
    return temp_manager.createBox(box)


def count_lumps(body: adsk.fusion.BRepBody) -> int:
    return body.lumps.count


# ------------------------------------------------------------------ pipeline

def collect_parts(design: adsk.fusion.Design, faces: list[adsk.fusion.BRepFace],
                  settings_list: list[model.PartSettings] | None = None) -> tuple[list[model.Part], list[model.Group]]:
    """Resolves faces (plus optional PER-INDEX settings) into parts and groups.

    settings_list is positional (parallel to faces) on purpose: entity-token
    strings only compare equal when derived from the same proxy object, so any
    token-keyed join silently misses. Without settings_list, the settings
    stored on each body are used.
    """
    singles: list[model.Part] = []
    groups: dict[str, model.Group] = {}
    seen_tokens: set[str] = set()
    for index, face in enumerate(faces):
        body = face.body
        token = body.entityToken
        if token in seen_tokens:
            continue
        seen_tokens.add(token)
        if settings_list is not None and index < len(settings_list):
            settings = settings_list[index]
        else:
            settings = model.load_settings(body)
        grain = None
        if settings.direction_token:
            grain = model.resolve_direction(design, settings.direction_token)
        part = model.Part(body=body, top_face=face, settings=settings, grain=grain)
        if settings.group:
            groups.setdefault(settings.group, model.Group(name=settings.group)).parts.append(part)
        else:
            singles.append(part)
    for group in groups.values():
        if len(group.parts) == 1:
            singles.append(group.parts[0])
    real_groups = [group for group in groups.values() if len(group.parts) > 1]
    return singles, real_groups


def run(design: adsk.fusion.Design, faces: list[adsk.fusion.BRepFace],
        envelope_profile: adsk.fusion.Profile, options: Options,
        timeline_start: int | None = None,
        settings_list: list[model.PartSettings] | None = None,
        result_occurrence: adsk.fusion.Occurrence | None = None) -> int:
    """Runs the whole pipeline. Returns the number of placed parts.

    Pass timeline_start to extend the resulting timeline group backwards over
    features the caller created as part of this run (e.g. an inline envelope
    sketch).
    """
    root = design.rootComponent
    timeline = design.timeline if design.designType == adsk.fusion.DesignTypes.ParametricDesignType else None
    if timeline_start is None:
        timeline_start = timeline.count if timeline else 0

    singles, groups = collect_parts(design, faces, settings_list)
    if not singles and not groups:
        raise MultiArrangeError('No parts selected.')

    proxies: list[Proxy] = []
    try:
        for part in singles:
            proxies.append(build_proxy(root, len(proxies), [part], part_frame(part)))
        for group in groups:
            proxies.append(build_proxy(root, len(proxies), group.parts, group_frame(group.parts)))

        solve(root, proxies, envelope_profile, options)

        placed = place_results(design, root, proxies, options, result_occurrence)
    finally:
        for proxy in proxies:
            if proxy.occurrence.isValid:
                proxy.occurrence.deleteMe()

    if timeline:
        timeline_end = timeline.count - 1
        if timeline_end > timeline_start:
            group = timeline.timelineGroups.add(timeline_start, timeline_end)
            group.name = TIMELINE_GROUP_NAME

    return placed


def create_arrange_feature(root: adsk.fusion.Component, proxies: list[Proxy],
                           envelope_profile: adsk.fusion.Profile,
                           options: Options) -> adsk.fusion.ArrangeFeature:
    arrange_features = root.features.arrangeFeatures
    solver_input = arrange_features.createInput(
        adsk.fusion.ArrangeSolverTypes.Arrange2DTrueShapeSolverType)
    envelope = solver_input.setProfileOrFaceEnvelope([envelope_profile])
    envelope.objectSpacing = adsk.core.ValueInput.createByReal(options.object_spacing)
    envelope.frameWidth = adsk.core.ValueInput.createByReal(options.frame_width)
    envelope.placementClearance = adsk.core.ValueInput.createByReal(options.placement_clearance)
    solver_input.definition.isPartInPartAllowed = options.part_in_part

    components = solver_input.arrangeComponents
    for proxy in proxies:
        component = components.add(proxy.occurrence)
        component.rotationType = proxy.rotation_type
        if proxy.flip:
            component.isDirectionFlipped = True
        if abs(proxy.rotation_correction) > 1e-9:
            component.rotation = proxy.rotation_correction

    try:
        return arrange_features.add(solver_input)
    except RuntimeError as error:
        if 'NO_ROOM' in str(error):
            raise MultiArrangeError(no_room_message(proxies, envelope_profile)) from error
        raise


def no_room_message(proxies: list[Proxy], envelope_profile: adsk.fusion.Profile) -> str:
    """A no-room error that says how much material is actually needed."""
    part_count = sum(len(proxy.parts) for proxy in proxies)
    details = ''
    try:
        parts_area = sum(part.top_face.area for proxy in proxies for part in proxy.parts)
        sheet_area = envelope_profile.areaProperties().area
        details = (
            f' The {part_count} parts cover {parts_area / 10000:.2f} m² of the '
            f'{sheet_area / 10000:.2f} m² of sheet (before spacing and offcuts).'
        )
    except RuntimeError:
        details = f' ({part_count} parts.)'
    return (
        'Not enough room on the sheets to arrange all parts.' + details +
        ' Add sheets, enlarge them, or reduce the spacing.'
    )


def _allowed_rotation_modulus(rotation_type: int) -> float | None:
    """The angular period of the placements a rotation type permits.

    None: no in-plane freedom (modulus None = exact zero); Only180: pi;
    everything else: pi/2."""
    types = adsk.fusion.ArrangeRotationTypes
    if rotation_type == types.NoneArrangeRotationType:
        return None
    if rotation_type == types.Only180ArrangeRotationType:
        return math.pi
    return math.pi / 2.0


def _orientation_residue(placement: adsk.core.Matrix3D, modulus: float | None) -> float:
    """How far the placement's rotation deviates from the allowed set."""
    angle = math.atan2(placement.getCell(1, 0), placement.getCell(0, 0))
    if modulus is None:
        # wrap to (-pi, pi]
        return math.atan2(math.sin(angle), math.cos(angle))
    half = modulus / 2.0
    return ((angle + half) % modulus) - half


def solve(root: adsk.fusion.Component, proxies: list[Proxy],
          envelope_profile: adsk.fusion.Profile, options: Options):
    """Solves, then verifies and corrects part orientations in a closed loop.

    The solver re-orients parts by an internal, geometry-derived default that
    ignores the proxy's coordinate system (it survives temp-brep transforms,
    copies, booleans and even export/import roundtrips) — so grain alignment
    cannot be guaranteed by construction. Instead, each pass measures every
    placement's deviation from its allowed orientation set (flip and in-plane
    angle) and feeds the negated deviation back through isDirectionFlipped and
    the per-component rotation offset, both of which act as clean offsets on
    the solver's default. The solver is deterministic, so this converges —
    typically in a single extra pass, and only when a part deviates at all.

    Deviations are measured in the ENVELOPE SKETCH's coordinate frame, not the
    world frame: for a compliant placement, the proxy's local axes map onto
    the sheet's axes (grain along sheet Y), whatever plane the sheet lies on.
    Measuring against world axes silently assumed an X-Y sheet — on other
    planes it misread flips (no convergence) and angles (wrong grain).
    """
    # Rigid inverse of the sketch orientation: for rigid transforms the
    # rotation cells of plane_inverse @ W are translation-independent.
    plane_inverse = inverted(envelope_profile.parentSketch.transform)

    for _attempt in range(3):
        feature = create_arrange_feature(root, proxies, envelope_profile, options)
        try:
            read_placements(root, proxies)
        finally:
            feature.deleteMe()

        missing = [proxy for proxy in proxies if proxy.placement is None]
        if missing:
            names = ', '.join(p.parts[0].body.name for p in missing)
            raise MultiArrangeError(f'The solver did not place: {names}.')

        compliant = True
        for proxy in proxies:
            placement = multiply(plane_inverse, proxy.placement)
            if placement.getCell(2, 2) < 0:
                # Placed upside-down: toggle the flip compensation first; the
                # in-plane angle is re-measured on the next pass.
                proxy.flip = not proxy.flip
                compliant = False
                continue
            residue = _orientation_residue(
                placement, _allowed_rotation_modulus(proxy.rotation_type))
            if abs(residue) > 0.01:
                correction = proxy.rotation_correction - residue
                proxy.rotation_correction = math.atan2(math.sin(correction), math.cos(correction))
                compliant = False
        if compliant:
            return
    raise MultiArrangeError('Could not stabilize the part orientations against the solver.')


def compute_layout(design: adsk.fusion.Design, faces: list[adsk.fusion.BRepFace],
                   envelope_profile: adsk.fusion.Profile,
                   options: Options,
                   settings_list: list[model.PartSettings] | None = None
                   ) -> list[tuple[adsk.fusion.BRepBody, str]]:
    """Solves the arrangement and returns transformed TEMPORARY copies of the
    part bodies, leaving the model unchanged (all solver artifacts deleted).

    Used for the preview: the temporary bodies are drawn as custom graphics,
    which live outside the model and its transactions — model-based previews
    of this pipeline (new occurrences, an Arrange feature) get discarded by
    Fusion's preview transaction.
    """
    root = design.rootComponent
    temp_manager = adsk.fusion.TemporaryBRepManager.get()
    singles, groups = collect_parts(design, faces, settings_list)
    if not singles and not groups:
        raise MultiArrangeError('No parts selected.')

    proxies: list[Proxy] = []
    try:
        for part in singles:
            proxies.append(build_proxy(root, len(proxies), [part], part_frame(part)))
        for group in groups:
            proxies.append(build_proxy(root, len(proxies), group.parts, group_frame(group.parts)))

        solve(root, proxies, envelope_profile, options)

        results: list[tuple[adsk.fusion.BRepBody, str]] = []
        for proxy in proxies:
            delta = multiply(proxy.placement, inverted(proxy.frame))
            for part in proxy.parts:
                copy = temp_manager.copy(part.body)
                temp_manager.transform(copy, delta)
                results.append((copy, part.body.name))
        return results
    finally:
        for proxy in proxies:
            if proxy.occurrence.isValid:
                proxy.occurrence.deleteMe()


def read_placements(root: adsk.fusion.Component, proxies: list[Proxy]):
    by_component_token = {proxy.occurrence.component.entityToken: proxy for proxy in proxies}
    proxy_occurrence_tokens = {proxy.occurrence.entityToken for proxy in proxies}

    def visit(occurrence: adsk.fusion.Occurrence):
        proxy = by_component_token.get(occurrence.component.entityToken)
        if proxy is not None and occurrence.entityToken not in proxy_occurrence_tokens:
            # transform2 of a traversal proxy is already root-relative.
            proxy.placement = occurrence.transform2.copy()
            return
        for index in range(occurrence.childOccurrences.count):
            visit(occurrence.childOccurrences.item(index))

    for index in range(root.occurrences.count):
        visit(root.occurrences.item(index))


def place_results(design: adsk.fusion.Design, root: adsk.fusion.Component,
                  proxies: list[Proxy], options: Options,
                  result_occurrence: adsk.fusion.Occurrence | None = None) -> int:
    temp_manager = adsk.fusion.TemporaryBRepManager.get()
    placed = 0

    if options.create_copies:
        if result_occurrence is None:
            result_occurrence = root.occurrences.addNewComponent(adsk.core.Matrix3D.create())
            result_occurrence.component.name = RESULT_COMPONENT_NAME
        result_component = result_occurrence.component
        to_result_space = inverted(result_occurrence.transform2)
        for proxy in proxies:
            delta = multiply(proxy.placement, inverted(proxy.frame))
            for part in proxy.parts:
                copy = temp_manager.copy(part.body)
                temp_manager.transform(copy, delta)
                add_body_to_component(result_component, copy)
                # Re-fetch the body: the reference returned from inside the
                # base-feature edit does not accept a name reliably.
                bodies = result_component.bRepBodies
                added = bodies.item(bodies.count - 1)
                added.name = part.body.name
                apply_appearance(part.body, added, delta, to_result_space)
                placed += 1
        return placed

    # A move feature on a body proxy applies its transform in root (world)
    # coordinates, so the solved delta can be used directly.
    move_features = root.features.moveFeatures
    for proxy in proxies:
        delta = multiply(proxy.placement, inverted(proxy.frame))
        for part in proxy.parts:
            bodies = adsk.core.ObjectCollection.create()
            bodies.add(part.body)
            move_input = move_features.createInput2(bodies)
            move_input.defineAsFreeMove(delta)
            move_features.add(move_input)
            placed += 1
    return placed


def apply_appearance(source: adsk.fusion.BRepBody, target: adsk.fusion.BRepBody,
                     delta: adsk.core.Matrix3D, to_target_space: adsk.core.Matrix3D):
    """Gives the arranged copy the source part's appearance and grain mapping.

    Carrying the texture mapping over means the wood grain of a nested part is
    drawn in the direction it was actually nested, so a wrong grain becomes
    visible on screen instead of only in the numbers. Texture transforms are
    stored in component space, so the source mapping is lifted to world space,
    moved by the part's placement, and pushed into the result component's
    space.
    """
    appearance = source.appearance
    if appearance is None:
        return
    try:
        target.appearance = appearance
    except RuntimeError:
        return

    source_control = source.textureMapControl
    target_control = target.textureMapControl
    if source_control is None or target_control is None:
        return
    source_transform = getattr(source_control, 'transform', None)
    if source_transform is None or not hasattr(target_control, 'transform'):
        return

    # Projection style (planar/box/cylindrical/spherical) before the transform,
    # since changing the type resets the mapping.
    source_type = getattr(source_control, 'projectedTextureMapType', None)
    if source_type is not None and hasattr(target_control, 'projectedTextureMapType'):
        try:
            target_control.projectedTextureMapType = source_type
            target_control.isCapped = source_control.isCapped
        except RuntimeError:
            pass

    world = source_transform
    context = source.assemblyContext
    if context is not None:
        world = multiply(context.transform2, source_transform)
    try:
        target_control.transform = multiply(to_target_space, multiply(delta, world))
    except RuntimeError:
        pass
