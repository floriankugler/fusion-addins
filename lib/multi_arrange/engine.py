"""The multi-arrange pipeline.

Fusion's Arrange feature is used purely as a nesting solver:

1. Every part (and every rigid group) is copied into a temporary, flat,
   grain-aligned single-body proxy (a TemporaryBRepManager body). Groups
   become one body joined by thin bridges, because the solver only
   collision-checks a single body per component.
2. The proxies are placed into a SCRATCH DOCUMENT together with a freshly
   built envelope sketch, and one True Shape Arrange runs there. Every
   document write costs time proportional to the size of the whole document
   (measured: 0.7-1.8 s per write in an 1800-feature design vs ~10 ms in an
   empty one), so running the sacrificial solver machinery in a throwaway
   document instead of the user's design turns a ~50 s solve into ~2 s. The
   scratch document is closed without saving; the user's design never sees
   any solver artifacts. Opening and closing a document does not disturb an
   open command dialog: each document has its own command stack, and the
   dialog is active again once the scratch document closes (verified).
3. The placements are read back in envelope-sketch space, mapped through the
   envelope sketch's frame in the user's design, and clean per-part bodies
   are placed at the solved positions — as copies into the result component
   (all inside ONE base feature), or by moving the original bodies.

The timeline entries created in the user's design (result component, envelope
sketch, one base feature) are wrapped in one timeline group.
"""

import adsk.core, adsk.fusion
import math
from dataclasses import dataclass, field

from . import model
from ..envelope import builder as envelope_builder


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


@dataclass
class EnvelopeSpec:
    """What the envelope sketch is built from, so the solver can rebuild an
    identical sketch in the scratch document."""
    rectangles: list[envelope_builder.RectangleSpec]
    x_offset: envelope_builder.OffsetSpec | None = None
    y_offset: envelope_builder.OffsetSpec | None = None


class MultiArrangeError(RuntimeError):
    pass


class NoRoomError(MultiArrangeError):
    """The solver reported NO_ROOM for the envelope."""


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
    merged_body: adsk.fusion.BRepBody    # flat, local-frame temporary body
    frame: adsk.core.Matrix3D            # local->world frame of the source part(s)
    parts: list[model.Part]
    rotation_type: int
    flip: bool = False                   # counteract the solver's largest-face-up normalization
    rotation_correction: float = 0.0     # counteract the solver's in-plane re-orientation
    occurrence: adsk.fusion.Occurrence | None = None  # scratch-document occurrence, only during solve
    placement: adsk.core.Matrix3D | None = None  # solved transform, in envelope-SKETCH space


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


def build_proxy(parts: list[model.Part], frame: adsk.core.Matrix3D) -> Proxy:
    """Builds the flat, grain-aligned proxy body — pure temp-BRep geometry,
    no document writes."""
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
            bridge = bridge_body(temp_manager, bodies[i], bodies[j])
            if bridge is not None:
                temp_manager.booleanOperation(merged, bridge, adsk.fusion.BooleanTypes.UnionBooleanType)
        for body in bodies[1:]:
            temp_manager.booleanOperation(merged, body, adsk.fusion.BooleanTypes.UnionBooleanType)
        if merged.lumps.count > 1:
            raise MultiArrangeError(
                f"Could not bridge the parts of group '{parts[0].settings.group}' into "
                'a single connected proxy body.'
            )

    rotations = [part.settings.rotation for part in parts]
    return Proxy(merged_body=merged, frame=frame, parts=parts,
                 rotation_type=rotation_type_for(rotations),
                 flip=largest_face_is_bottom(merged))


def build_proxies(singles: list[model.Part], groups: list[model.Group]) -> list[Proxy]:
    proxies = [build_proxy([part], part_frame(part)) for part in singles]
    proxies.extend(build_proxy(group.parts, group_frame(group.parts)) for group in groups)
    return proxies


def body_center_2d(body: adsk.fusion.BRepBody) -> tuple[float, float]:
    box = body.boundingBox
    return ((box.minPoint.x + box.maxPoint.x) / 2.0, (box.minPoint.y + box.maxPoint.y) / 2.0)


# How far the bridge plate reaches INTO each body past their closest points,
# so the union has real material overlap on both ends.
BRIDGE_OVERLAP = 1.0  # cm


def bridge_body(temp_manager: adsk.fusion.TemporaryBRepManager,
                body_a: adsk.fusion.BRepBody, body_b: adsk.fusion.BRepBody) -> adsk.fusion.BRepBody | None:
    """A thin plate crossing the closest gap between the two bodies, or None
    when they already touch.

    The bridge spans the bodies' closest approach (extended a little into
    each side), NOT their centroids: when one part lies inside a cutout of
    the other — a hatch in a wall, say — both centroids can fall in the hole
    and a centroid bridge floats without touching either body. The closest
    approach by construction has material on both ends."""
    app = adsk.core.Application.get()
    measurement = app.measureManager.measureMinimumDistance(body_a, body_b)
    point_a = measurement.positionOne
    point_b = measurement.positionTwo
    dx = point_b.x - point_a.x
    dy = point_b.y - point_a.y
    gap = math.hypot(dx, dy)
    if gap < 1e-6:
        # Touching or overlapping: the plain union already connects them.
        return None
    direction = adsk.core.Vector3D.create(dx / gap, dy / gap, 0.0)
    width_direction = adsk.core.Vector3D.create(-direction.y, direction.x, 0.0)

    height = min(body_a.boundingBox.maxPoint.z, body_b.boundingBox.maxPoint.z)
    if height <= 1e-6:
        raise MultiArrangeError('Group parts have no thickness overlap for bridging.')
    center = adsk.core.Point3D.create(
        (point_a.x + point_b.x) / 2.0,
        (point_a.y + point_b.y) / 2.0,
        height / 2.0,
    )
    box = adsk.core.OrientedBoundingBox3D.create(
        center, direction, width_direction, gap + 2.0 * BRIDGE_OVERLAP, BRIDGE_WIDTH, height)
    return temp_manager.createBox(box)


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
        envelope_spec: EnvelopeSpec, options: Options,
        plane_transform: adsk.core.Matrix3D | None = None,
        timeline_start: int | None = None,
        settings_list: list[model.PartSettings] | None = None,
        result_occurrence: adsk.fusion.Occurrence | None = None,
        cached_placements: list[tuple[float, ...]] | None = None) -> int:
    """Runs the whole pipeline. Returns the number of placed parts.

    The envelope exists only in the scratch document during the solve; the
    user's design receives nothing but the placed copies. plane_transform is
    the sketch frame the sheet plane would give a sketch (see
    the probe in main._plane_transform); None means the root X-Y plane.

    Pass timeline_start to extend the resulting timeline group backwards over
    features the caller created as part of this run (e.g. the result
    component's occurrence). cached_placements (sketch-space matrices, one per
    proxy, as returned in Layout.placements) skips the solve entirely — valid
    only when the inputs are unchanged since the layout was computed.
    """
    root = design.rootComponent
    timeline = design.timeline if design.designType == adsk.fusion.DesignTypes.ParametricDesignType else None
    # New features are inserted AT THE MARKER, not at the end: a design can
    # have rolled-back features parked after the marker, and count-based
    # indices would span them (timelineGroups.add then fails with "rolled
    # back features not allowed").
    if timeline_start is None:
        timeline_start = timeline.markerPosition if timeline else 0

    singles, groups = collect_parts(design, faces, settings_list)
    if not singles and not groups:
        raise MultiArrangeError('No parts selected.')
    proxies = build_proxies(singles, groups)

    if cached_placements is not None and len(cached_placements) == len(proxies):
        for proxy, cells in zip(proxies, cached_placements):
            matrix = adsk.core.Matrix3D.create()
            matrix.setWithArray(list(cells))
            proxy.placement = matrix
    else:
        solve_in_scratch(proxies, envelope_spec, options)

    placed = place_results(design, root, proxies, options, result_occurrence,
                           plane_transform)

    if timeline:
        timeline_end = timeline.markerPosition - 1
        if timeline_end > timeline_start:
            group = timeline.timelineGroups.add(timeline_start, timeline_end)
            group.name = TIMELINE_GROUP_NAME

    return placed


def solve_in_scratch(proxies: list[Proxy], envelope_spec: EnvelopeSpec,
                     options: Options) -> list[adsk.core.Point3D]:
    """Runs the sacrificial solve in a throwaway document.

    Builds the envelope sketch (on the scratch X-Y plane) and one component
    per proxy in a new document, runs the closed-loop solve there, converts
    the placements into envelope-sketch space, and closes the document without
    saving. Returns the envelope outline as sketch-space segment endpoint
    pairs (for preview graphics).

    Creating the document briefly activates it; the user's document — and an
    open command dialog on it, which has its own per-document command stack —
    become active again when the scratch document closes.
    """
    app = adsk.core.Application.get()
    previous_document = app.activeDocument
    document = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
    try:
        design = adsk.fusion.Design.cast(
            document.products.itemByProductType('DesignProductType'))
        root = design.rootComponent

        sketch = envelope_builder.build_envelope_sketch_on(
            root, root.xYConstructionPlane, envelope_spec.rectangles, 'Envelope',
            x_offset=envelope_spec.x_offset, y_offset=envelope_spec.y_offset)
        if sketch.profiles.count != 1:
            raise MultiArrangeError('The envelope sketch did not produce a single profile.')
        profile = sketch.profiles.item(0)

        check_parts_fit(proxies, envelope_spec, options)

        for index, proxy in enumerate(proxies):
            occurrence = root.occurrences.addNewComponent(adsk.core.Matrix3D.create())
            occurrence.component.name = f'{PROXY_PREFIX}_{index}'
            add_body_to_component(occurrence.component, proxy.merged_body)
            proxy.occurrence = occurrence

        try:
            solve(root, proxies, profile, options)
        except NoRoomError:
            # The solver's FIRST pass places parts in its own opaque default
            # orientation; the closed-loop corrections that turn them to the
            # grain only apply from the second pass on. A default orientation
            # can demand far more room than the corrected one (measured: three
            # panels needing 1773 mm corrected were refused on a 2000 mm sheet
            # because their default orientation needs ~2236 mm) — so a tight
            # envelope dies in pass 1 without the corrections ever engaging.
            # The default orientation is geometry-derived, not envelope-
            # derived: learn the corrections on an oversized envelope, then
            # retry the real one warm-started. A NoRoomError from the retry is
            # genuine and propagates.
            learn_orientation_corrections(root, proxies, envelope_spec, options)
            solve(root, proxies, profile, options)

        # Placements come back in scratch-world space; store them relative to
        # the envelope sketch so they are meaningful in any document.
        plane_inverse = inverted(sketch.transform)
        for proxy in proxies:
            proxy.placement = multiply(plane_inverse, proxy.placement)

        outline: list[adsk.core.Point3D] = []
        lines = sketch.sketchCurves.sketchLines
        for index in range(lines.count):
            line = lines.item(index)
            if line.isConstruction or line.isReference:
                continue
            geometry = line.geometry  # sketch space
            outline.append(geometry.startPoint.copy())
            outline.append(geometry.endPoint.copy())
        return outline
    finally:
        for proxy in proxies:
            proxy.occurrence = None
        document.close(False)
        try:
            if previous_document.isValid and app.activeDocument != previous_document:
                previous_document.activate()
        except RuntimeError:
            pass


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
            raise NoRoomError(no_room_message(proxies, envelope_profile)) from error
        raise


def learn_orientation_corrections(root: adsk.fusion.Component, proxies: list[Proxy],
                                  envelope_spec: EnvelopeSpec, options: Options):
    """Runs the closed-loop solve on an oversized envelope to learn each
    part's flip/rotation correction, leaving the corrections on the proxies.

    The oversized envelope gives the solver room for its default
    orientations, so the loop can measure and correct them; the resulting
    per-part offsets carry over to any envelope because they only depend on
    the part's geometry."""
    width = 3.0 * sum(rect.width * max(1, rect.count) for rect in envelope_spec.rectangles)
    height = 3.0 * max(rect.height for rect in envelope_spec.rectangles)
    sketch = envelope_builder.build_envelope_sketch_on(
        root, root.xYConstructionPlane,
        [envelope_builder.RectangleSpec(
            width, f'{width * 10:.2f} mm', height, f'{height * 10:.2f} mm', 1)],
        'EnvelopeLearn')
    try:
        if sketch.profiles.count != 1:
            raise MultiArrangeError('The learning envelope did not produce a single profile.')
        solve(root, proxies, sketch.profiles.item(0), options)
    finally:
        try:
            sketch.deleteMe()
        except RuntimeError:
            pass


def check_parts_fit(proxies: list[Proxy], envelope_spec: EnvelopeSpec,
                    options: Options):
    """Raises an actionable error for any part that cannot fit ANY sheet.

    The generic solver NO_ROOM error only reports areas, which hides the
    most common real cause: a grain-constrained part is only allowed to
    rotate 180 degrees, so its grain dimension must fit the sheet HEIGHT —
    a part can be far smaller than the sheet and still not fit. The proxy is
    built grain-along-local-Y, so its bounding box gives both extents
    directly.
    """
    inset = 2.0 * options.frame_width
    sheets = [(rect.width - inset, rect.height - inset)
              for rect in envelope_spec.rectangles]
    for proxy in proxies:
        box = proxy.merged_body.boundingBox
        part_width = box.maxPoint.x - box.minPoint.x    # across the grain
        part_height = box.maxPoint.y - box.minPoint.y   # along the grain
        free = proxy.rotation_type == adsk.fusion.ArrangeRotationTypes.AllRotationsArrangeRotationType
        fits_upright = any(part_width <= w and part_height <= h for w, h in sheets)
        fits_rotated = any(part_height <= w and part_width <= h for w, h in sheets)
        if fits_upright or (free and fits_rotated):
            continue

        if len(proxy.parts) > 1:
            name = f"Group '{proxy.parts[0].settings.group}'"
        else:
            name = f"Part '{proxy.parts[0].body.name}'"
        size = f'{part_width * 10:.0f} x {part_height * 10:.0f} mm (across x along grain)'
        if not free and fits_rotated:
            raise MultiArrangeError(
                f'{name} is {size} and only fits the sheets rotated, which its '
                'grain setting forbids: grain-aligned parts run along the sheet '
                'HEIGHT (the second column of the sheets table). Enter the '
                'sheets with the grain direction as the height, or set the '
                "part's rotation to Free."
            )
        raise MultiArrangeError(
            f'{name} is {size}, larger than every sheet (frame width included). '
            'Enlarge the sheets or reduce the frame width.'
        )


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


@dataclass
class Layout:
    """A solved layout: preview bodies, the envelope outline, and the raw
    sketch-space placements (reusable by run() via cached_placements)."""
    bodies: list[tuple[adsk.fusion.BRepBody, str]]  # transformed temp copies + names
    outline: list[adsk.core.Point3D]                # world-space segment endpoints
    placements: list[tuple[float, ...]] = field(default_factory=list)


def compute_layout(design: adsk.fusion.Design, faces: list[adsk.fusion.BRepFace],
                   envelope_spec: EnvelopeSpec,
                   plane_transform: adsk.core.Matrix3D,
                   options: Options,
                   settings_list: list[model.PartSettings] | None = None
                   ) -> Layout:
    """Solves the arrangement (in the scratch document) and returns
    transformed TEMPORARY copies of the part bodies, leaving the user's
    design completely untouched.

    plane_transform is the sketch frame the envelope will occupy in the
    user's design (sketch space -> world) — obtained from a probe sketch on
    the selected plane, so the preview shows the parts exactly where OK will
    put them.

    Used for the preview: the temporary bodies are drawn as custom graphics,
    which live outside the model and its transactions — model-based previews
    of this pipeline get discarded by Fusion's preview transaction.
    """
    temp_manager = adsk.fusion.TemporaryBRepManager.get()
    singles, groups = collect_parts(design, faces, settings_list)
    if not singles and not groups:
        raise MultiArrangeError('No parts selected.')
    proxies = build_proxies(singles, groups)

    outline_sketch = solve_in_scratch(proxies, envelope_spec, options)

    bodies: list[tuple[adsk.fusion.BRepBody, str]] = []
    for proxy in proxies:
        world_placement = multiply(plane_transform, proxy.placement)
        delta = multiply(world_placement, inverted(proxy.frame))
        for part in proxy.parts:
            copy = temp_manager.copy(part.body)
            temp_manager.transform(copy, delta)
            bodies.append((copy, part.body.name))

    outline = []
    for point in outline_sketch:
        world_point = point.copy()
        world_point.transformBy(plane_transform)
        outline.append(world_point)

    placements = [tuple(proxy.placement.asArray()) for proxy in proxies]
    return Layout(bodies=bodies, outline=outline, placements=placements)


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
                  result_occurrence: adsk.fusion.Occurrence | None = None,
                  plane_transform: adsk.core.Matrix3D | None = None) -> int:
    """Places the parts at their solved positions.

    plane_transform maps envelope-sketch space (which the placements are
    stored in) to world space in the user's design."""
    temp_manager = adsk.fusion.TemporaryBRepManager.get()
    if plane_transform is None:
        plane_transform = adsk.core.Matrix3D.create()
    placed = 0

    if options.create_copies:
        if result_occurrence is None:
            result_occurrence = root.occurrences.addNewComponent(adsk.core.Matrix3D.create())
            result_occurrence.component.name = RESULT_COMPONENT_NAME
        result_component = result_occurrence.component
        to_result_space = inverted(result_occurrence.transform2)

        copies: list[tuple[adsk.fusion.BRepBody, model.Part, adsk.core.Matrix3D]] = []
        for proxy in proxies:
            world_placement = multiply(plane_transform, proxy.placement)
            delta = multiply(world_placement, inverted(proxy.frame))
            for part in proxy.parts:
                copy = temp_manager.copy(part.body)
                temp_manager.transform(copy, delta)
                copies.append((copy, part, delta))

        # All copies go into ONE base feature: every feature edit costs time
        # proportional to the document size, so per-body base features
        # dominate the runtime in large designs.
        existing = result_component.bRepBodies.count
        if design.designType == adsk.fusion.DesignTypes.ParametricDesignType:
            base = result_component.features.baseFeatures.add()
            base.startEdit()
            try:
                for copy, _part, _delta in copies:
                    result_component.bRepBodies.add(copy, base)
            finally:
                base.finishEdit()
        else:
            for copy, _part, _delta in copies:
                result_component.bRepBodies.add(copy)

        # Re-fetch the bodies: references returned from inside the
        # base-feature edit do not accept a name reliably. Bodies keep their
        # insertion order.
        bodies = result_component.bRepBodies
        for offset, (_copy, part, delta) in enumerate(copies):
            added = bodies.item(existing + offset)
            added.name = part.body.name
            apply_appearance(part.body, added, delta, to_result_space)
            placed += 1
        return placed

    # A move feature on a body proxy applies its transform in root (world)
    # coordinates, so the solved delta can be used directly.
    move_features = root.features.moveFeatures
    for proxy in proxies:
        world_placement = multiply(plane_transform, proxy.placement)
        delta = multiply(world_placement, inverted(proxy.frame))
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
