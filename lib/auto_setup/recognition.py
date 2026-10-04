"""Geometry recognition for automatic manufacturing setups.

Detects machinable features (holes, pockets, through cutouts, outer contours,
rim chamfers and V-grooves) on bodies, relative to a user-defined machining
frame. All lengths are in cm (Fusion internal units). Pure geometry - no CAM
API calls.
"""

import math
import adsk.core, adsk.fusion
from dataclasses import dataclass, field

# Tolerances (cm / dimensionless)
HEIGHT_TOL = 1e-3
DIRECTION_TOL = 1e-3
# The vertical component of the normal of a face cut by a 90 degree V-bit: the
# face stands at 45 degrees to the tool axis.
BEVEL_NORMAL_Z = math.sqrt(0.5)


class RecognitionError(Exception):
    pass


@dataclass(frozen=True)
class Frame:
    x: adsk.core.Vector3D
    y: adsk.core.Vector3D
    z: adsk.core.Vector3D

    @staticmethod
    def from_x_axis(x_axis, top_normal: adsk.core.Vector3D) -> 'Frame':
        """Build the machining frame from the X axis (linear edge or
        construction axis) and the top face normal (Z); Y follows right-handed."""
        x = axis_direction(x_axis)
        z = top_normal.copy()
        z.normalize()
        if abs(x.dotProduct(z)) > DIRECTION_TOL:
            raise RecognitionError('The selected X axis is not parallel to the top face.')
        y = z.crossProduct(x)
        return Frame(x=x, y=y, z=z)

    def height(self, point: adsk.core.Point3D) -> float:
        return point.asVector().dotProduct(self.z)


def face_normal(face: adsk.fusion.BRepFace) -> adsk.core.Vector3D:
    _, normal = face.evaluator.getNormalAtPoint(face.pointOnFace)
    return normal


def axis_direction(entity) -> adsk.core.Vector3D:
    """Direction of an X axis selection: a linear edge or a construction axis."""
    edge = adsk.fusion.BRepEdge.cast(entity)
    if edge:
        return edge_direction(edge)
    axis = adsk.fusion.ConstructionAxis.cast(entity)
    if axis:
        direction = axis.geometry.direction
        direction.normalize()
        return direction
    raise RecognitionError('The X axis selection must be a linear edge or a construction axis.')


@dataclass
class Hole:
    face: adsk.fusion.BRepFace  # cylindrical wall face
    diameter: float
    depth: float
    is_through: bool
    body: adsk.fusion.BRepBody
    # The circular edge at the hole bottom (used when large through holes are
    # machined as inner contours instead of bores).
    bottom_edge: adsk.fusion.BRepEdge | None = None
    # How far below the top face the wall starts: the height of a chamfered or
    # countersunk rim, 0 for a plain hole.
    rim: float = 0.0


@dataclass
class Pocket:
    bottom_face: adsk.fusion.BRepFace
    depth: float
    body: adsk.fusion.BRepBody
    # Radii of the concave (inside) corner arcs of the boundary. Empty when
    # there are none (e.g. all corners sharp): no tool constraint. The small
    # ones among them are corner reliefs that get their own operation, so the
    # list is kept whole rather than reduced to its minimum here.
    corner_radii: list[float] = field(default_factory=list)
    # Floor area, which decides how wide a tool is worth using.
    area: float = 0.0

    @property
    def min_corner_radius(self) -> float | None:
        return min(self.corner_radii, default=None)


@dataclass
class Cutout:
    """Interior through opening, machined as an inside contour."""
    edges: list[adsk.fusion.BRepEdge]  # closed loop at the body bottom
    body: adsk.fusion.BRepBody
    depth: float = 0.0  # stock thickness at this feature


@dataclass
class Contour:
    """Outer profile of a body, machined via silhouette."""
    body: adsk.fusion.BRepBody
    # Outer loop of the bottom face (used for tab placement); empty if the
    # body has no planar bottom face.
    edges: list[adsk.fusion.BRepEdge] = field(default_factory=list)
    depth: float = 0.0  # stock thickness


@dataclass
class Chamfer:
    """A 45 degree chamfer between the top face and a wall below it - the rim
    of a hole (where it is a countersink), a pocket, a cutout or the outer
    contour - machined with a 90 degree V-bit along its lower edge."""
    # The lower edges in chain order, each with the chamfer face above it.
    edges: list[adsk.fusion.BRepEdge]
    faces: list[adsk.fusion.BRepFace]
    height: float       # from the lower edge up to the top face; also its width
    is_closed: bool
    body: adsk.fusion.BRepBody
    up: adsk.core.Vector3D   # the tool axis, pointing away from the part
    # The walls below the lower edges; they tell which feature the chamfer
    # belongs to.
    walls: list[adsk.fusion.BRepFace] = field(default_factory=list)
    # Radius of the lower edge when the chamfer runs around a round hole.
    hole_radius: float | None = None


@dataclass
class Groove:
    """A pointed 90 degree groove in the top face: two 45 degree flanks meeting
    in a sharp bottom edge, which the tip of a 90 degree V-bit follows."""
    edges: list[adsk.fusion.BRepEdge]   # the bottom edges in chain order
    faces: list[adsk.fusion.BRepFace]   # the flanks
    depth: float
    body: adsk.fusion.BRepBody


@dataclass
class RecognitionResult:
    holes: list[Hole] = field(default_factory=list)
    pockets: list[Pocket] = field(default_factory=list)
    cutouts: list[Cutout] = field(default_factory=list)
    contours: list[Contour] = field(default_factory=list)
    chamfers: list[Chamfer] = field(default_factory=list)
    grooves: list[Groove] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def extend(self, other: 'RecognitionResult'):
        self.holes.extend(other.holes)
        self.pockets.extend(other.pockets)
        self.cutouts.extend(other.cutouts)
        self.contours.extend(other.contours)
        self.chamfers.extend(other.chamfers)
        self.grooves.extend(other.grooves)
        self.warnings.extend(other.warnings)


def recognize(bodies: list[adsk.fusion.BRepBody], frame: Frame) -> RecognitionResult:
    result = RecognitionResult()
    for body in bodies:
        result.extend(_recognize_body(body, frame))
    return result


def _recognize_body(body: adsk.fusion.BRepBody, frame: Frame) -> RecognitionResult:
    result = RecognitionResult()
    z_min, z_max = _body_height_range(body, frame)

    hole_faces: list[adsk.fusion.BRepFace] = []
    for face in body.faces:
        hole = _hole_from_face(face, frame, z_min, z_max, result.warnings, body)
        if hole:
            result.holes.append(hole)
            hole_faces.append(face)

    for face in body.faces:
        if _is_up_facing_plane(face, frame):
            face_z = frame.height(face.pointOnFace)
            if face_z >= z_max - HEIGHT_TOL or face_z <= z_min + HEIGHT_TOL:
                continue
            if _is_hole_bottom(face, hole_faces):
                continue
            result.pockets.append(Pocket(
                bottom_face=face,
                depth=z_max - face_z,
                body=body,
                corner_radii=_concave_corner_radii(face),
                area=face.area,
            ))

    bottom_faces = [
        f for f in body.faces
        if _is_down_facing_plane(f, frame) and frame.height(f.pointOnFace) <= z_min + HEIGHT_TOL
    ]
    if not bottom_faces:
        result.warnings.append(f'{body.name}: no planar bottom face found; skipped cutout detection.')
    bottom_tokens = {f.entityToken for f in bottom_faces}
    covered = 0
    for face in bottom_faces:
        for loop in face.loops:
            if loop.isOuter:
                continue
            if _loop_matches_hole(loop, result.holes, frame):
                continue
            if not _opens_to_top(loop, bottom_tokens, frame, z_max):
                covered += 1
                continue
            result.cutouts.append(Cutout(edges=list(loop.edges), body=body,
                                         depth=z_max - z_min))
    if covered:
        result.warnings.append(
            f'{body.name}: {covered} opening(s) in the bottom face are covered by '
            'material from above and were not machined; they are only reachable '
            'from the other side.')

    outer_edges: list[adsk.fusion.BRepEdge] = []
    if bottom_faces:
        for loop in bottom_faces[0].loops:
            if loop.isOuter:
                outer_edges = list(loop.edges)
                break
    result.contours.append(Contour(body=body, edges=outer_edges, depth=z_max - z_min))
    _recognize_bevels(body, frame, z_max, result)
    return result


def _body_height_range(body: adsk.fusion.BRepBody, frame: Frame) -> tuple[float, float]:
    heights = [frame.height(v.geometry) for v in body.vertices]
    if not heights:
        raise RecognitionError(f'{body.name}: body has no vertices.')
    return min(heights), max(heights)


def edge_direction(edge: adsk.fusion.BRepEdge) -> adsk.core.Vector3D:
    line = adsk.core.Line3D.cast(edge.geometry)
    if not line:
        raise RecognitionError('Selected axis edge is not a straight line.')
    direction = line.startPoint.vectorTo(line.endPoint)
    direction.normalize()
    return direction


def _edge_point(edge: adsk.fusion.BRepEdge) -> adsk.core.Point3D:
    return edge.startVertex.geometry if edge.startVertex else _edge_midpoint(edge)


def _hole_from_face(
    face: adsk.fusion.BRepFace,
    frame: Frame,
    z_min: float,
    z_max: float,
    warnings: list[str],
    body: adsk.fusion.BRepBody,
) -> Hole | None:
    cylinder = adsk.core.Cylinder.cast(face.geometry)
    if not cylinder:
        return None
    axis = cylinder.axis
    axis.normalize()
    # Compared with a tolerance, not Vector3D.isParallelTo: that compares
    # exactly, and modelled geometry carries rounding noise, so a vertical
    # hole would be skipped over an angle of ~1e-11 rad.
    if abs(abs(axis.dotProduct(frame.z)) - 1) > DIRECTION_TOL:
        warnings.append(f'{body.name}: cylindrical face with non-vertical axis skipped.')
        return None

    if not _is_concave_cylinder(face, cylinder):
        return None  # convex cylinder: outer fillet, part of the contour

    # Full-circle check: partial concave cylinders are inside-corner fillets.
    # A hole wall is bounded by at least one complete circular edge, while
    # fillets are bounded by arcs and lines only.
    if not _has_full_circle_edge(face):
        return None

    face_z = [frame.height(v.geometry) for v in face.vertices]
    if not face_z:
        return None
    top, bottom = max(face_z), min(face_z)
    if top < z_max - HEIGHT_TOL and not _rim_reaches_top(face, frame, top, z_max):
        warnings.append(
            f'{body.name}: hole (d{cylinder.radius * 20:.1f}mm) does not start at the top face; skipped.')
        return None
    is_through = bottom <= z_min + HEIGHT_TOL

    bottom_edge = None
    for edge in face.edges:
        if adsk.core.Circle3D.cast(edge.geometry) and frame.height(_edge_point(edge)) <= bottom + HEIGHT_TOL:
            bottom_edge = edge
            break

    return Hole(
        face=face,
        diameter=2 * cylinder.radius,
        # Measured from the top face, like a pocket: under a chamfered rim the
        # wall itself starts lower, but the tool still comes in from the top.
        depth=z_max - bottom,
        is_through=is_through,
        body=body,
        bottom_edge=bottom_edge,
        rim=max(z_max - top, 0.0),
    )


def _rim_reaches_top(face: adsk.fusion.BRepFace, frame: Frame, top: float,
                     z_max: float) -> bool:
    """True if a hole wall that stops short of the top face continues to it
    through its rim - a chamfer, a countersink or a rounding.

    A counterbore does not: there the wall ends on the flat floor of a wider
    hole, and the narrow hole below it is not reachable as a hole of its own.
    """
    rim = [edge for edge in face.edges
           if _edge_height_range(edge, frame)[0] >= top - HEIGHT_TOL]
    if not rim:
        return False
    for edge in rim:
        others = [f for f in edge.faces if f.tempId != face.tempId]
        if not others or _face_top_height(others[0], frame) < z_max - HEIGHT_TOL:
            return False
    return True


def _is_concave_cylinder(face: adsk.fusion.BRepFace, cylinder: adsk.core.Cylinder) -> bool:
    """True if the material lies outside the cylinder (hole wall, inside corner
    relief) rather than inside it (an outer fillet of the contour)."""
    axis = cylinder.axis
    axis.normalize()
    point = face.pointOnFace
    _, normal = face.evaluator.getNormalAtPoint(point)
    radial = _perpendicular_component(cylinder.origin.vectorTo(point), axis)
    return normal.dotProduct(radial) < 0


@dataclass
class Relief:
    """Inside corner relief of a contour - typically a dogbone: a small concave
    arc that a wider cutter cannot reach into. Machined along the arc as an open
    chain, or by plunging the wall like a hole when a tool of exactly the
    relief's diameter is available."""
    edge: adsk.fusion.BRepEdge   # the arc of the contour loop
    face: adsk.fusion.BRepFace   # the concave cylindrical wall
    diameter: float
    depth: float
    # False for a relief on a pocket floor, which the tool must stop at instead
    # of cutting through.
    is_through: bool = True


def corner_reliefs(edges: list[adsk.fusion.BRepEdge], max_diameter: float,
                   depth: float, is_through: bool = True) -> list[Relief]:
    """Reliefs of a contour loop up to max_diameter, at the given cut depth.

    An arc qualifies when its wall face is a concave cylinder, i.e. the material
    is on the far side of the arc's centre; convex arcs (rounded outside
    corners) are machinable with any tool. Full circles are holes or cutouts,
    not corner reliefs, and are left to the hole/cutout handling.
    """
    reliefs: list[Relief] = []
    for edge in edges:
        arc = adsk.core.Arc3D.cast(edge.geometry)
        if not arc or 2 * arc.radius > max_diameter:
            continue
        for face in edge.faces:
            cylinder = adsk.core.Cylinder.cast(face.geometry)
            if (cylinder and abs(cylinder.radius - arc.radius) < HEIGHT_TOL
                    and _is_concave_cylinder(face, cylinder)):
                reliefs.append(Relief(edge=edge, face=face, diameter=2 * arc.radius,
                                      depth=depth, is_through=is_through))
                break
    return reliefs


def _has_full_circle_edge(face: adsk.fusion.BRepFace) -> bool:
    return any(adsk.core.Circle3D.cast(edge.geometry) for edge in face.edges)


def _concave_corner_radii(face: adsk.fusion.BRepFace) -> list[float]:
    """Radii of the concave boundary arcs of a planar face.

    An arc is concave (an inside corner fillet the tool must fit into) when the
    face material lies on the arc's center side. Sharp corners are ignored:
    they carry no design radius, the tool simply leaves its own.
    """
    evaluator = face.evaluator
    radii: list[float] = []
    for loop in face.loops:
        for edge in loop.edges:
            geometry = adsk.core.Circle3D.cast(edge.geometry) or adsk.core.Arc3D.cast(edge.geometry)
            if not geometry:
                continue
            midpoint = _edge_midpoint(edge)
            towards_center = midpoint.vectorTo(geometry.center)
            if towards_center.length < 1e-9:
                continue
            towards_center.normalize()
            towards_center.scaleBy(min(geometry.radius * 0.5, 0.05))
            probe = midpoint.copy()
            probe.translateBy(towards_center)
            ok, parameter = evaluator.getParameterAtPoint(probe)
            if ok and evaluator.isParameterOnFace(parameter):
                radii.append(geometry.radius)
    return radii


def _edge_midpoint(edge: adsk.fusion.BRepEdge) -> adsk.core.Point3D:
    evaluator = edge.evaluator
    _, param_min, param_max = evaluator.getParameterExtents()
    _, point = evaluator.getPointAtParameter((param_min + param_max) / 2)
    return point


def _perpendicular_component(v: adsk.core.Vector3D, axis: adsk.core.Vector3D) -> adsk.core.Vector3D:
    parallel = axis.copy()
    parallel.scaleBy(v.dotProduct(axis))
    result = v.copy()
    result.subtract(parallel)
    return result


def _is_up_facing_plane(face: adsk.fusion.BRepFace, frame: Frame) -> bool:
    return _is_plane_with_normal(face, frame.z)


def _is_down_facing_plane(face: adsk.fusion.BRepFace, frame: Frame) -> bool:
    down = frame.z.copy()
    down.scaleBy(-1.0)
    return _is_plane_with_normal(face, down)


def _is_plane_with_normal(face: adsk.fusion.BRepFace, direction: adsk.core.Vector3D) -> bool:
    plane = adsk.core.Plane.cast(face.geometry)
    if not plane:
        return False
    _, normal = face.evaluator.getNormalAtPoint(face.pointOnFace)
    return normal.dotProduct(direction) > 1 - DIRECTION_TOL


def _is_hole_bottom(face: adsk.fusion.BRepFace, hole_faces: list[adsk.fusion.BRepFace]) -> bool:
    """A planar face whose every adjacent face is a hole wall is the flat bottom of a blind hole."""
    hole_tokens = {f.entityToken for f in hole_faces}
    adjacent = set()
    for edge in face.edges:
        for f in edge.faces:
            if f.entityToken != face.entityToken:
                adjacent.add(f.entityToken)
    return len(adjacent) > 0 and adjacent.issubset(hole_tokens)


def _opens_to_top(loop: adsk.fusion.BRepLoop, bottom_tokens: set[str],
                  frame: Frame, z_max: float) -> bool:
    """True if the opening bounded by this inner loop of a bottom face reaches
    the top of the body.

    Only a through opening may be cut as an inside contour: an opening that is
    covered by material from above - a pocket or a blind hole worked from the
    bottom - would be milled straight through the part if it were treated like
    one, so it belongs to a setup on the other side and is left alone here.

    The surface bounding the opening is walked from the loop upwards. A through
    cutout reaches the top within a step or two (one more when its rim is
    chamfered or filleted), while a cavity worked from the bottom is closed off
    by its own ceiling and the walk ends inside it. The bottom faces are never
    crossed, so the walk stays on the opening it started from instead of
    escaping around the body.
    """
    seen = set(bottom_tokens)
    queue: list[adsk.fusion.BRepFace] = []

    def push(face: adsk.fusion.BRepFace):
        if face.entityToken not in seen:
            seen.add(face.entityToken)
            queue.append(face)

    for edge in loop.edges:
        for face in edge.faces:
            push(face)
    while queue:
        face = queue.pop()
        if _face_top_height(face, frame) >= z_max - HEIGHT_TOL:
            return True
        for edge in face.edges:
            for neighbor in edge.faces:
                push(neighbor)
    return False


def _face_top_height(face: adsk.fusion.BRepFace, frame: Frame) -> float:
    """Height of the highest point of a face's boundary.

    Edge midpoints are measured alongside the vertices because a periodic edge
    - the full circle of a hole wall - carries no vertex at all, and a face
    bounded only by such edges would otherwise report no height.
    """
    heights = [frame.height(vertex.geometry) for vertex in face.vertices]
    heights += [frame.height(_edge_midpoint(edge)) for edge in face.edges]
    return max(heights) if heights else float('-inf')


def _loop_matches_hole(loop: adsk.fusion.BRepLoop, holes: list[Hole], frame: Frame) -> bool:
    """True if the loop is the bottom rim of an already recognized through hole."""
    edges = list(loop.edges)
    hole_face_tokens = {h.face.entityToken for h in holes if h.is_through}
    for edge in edges:
        circle = adsk.core.Circle3D.cast(edge.geometry)
        arc = adsk.core.Arc3D.cast(edge.geometry)
        if not circle and not arc:
            return False
        if not any(f.entityToken in hole_face_tokens for f in edge.faces):
            return False
    return True


# ---- Chamfers and V-grooves ---------------------------------------------------

def _recognize_bevels(body: adsk.fusion.BRepBody, frame: Frame, z_max: float,
                      result: RecognitionResult):
    """Chamfers and V-grooves of the top face: what a 90 degree V-bit cuts.

    Both are made of faces standing at 45 degrees that come down from the top
    face. What such a face ends on at its lower edge tells them apart: a wall
    dropping away below it makes it a chamfer, a second 45 degree face coming
    down from the other side makes the two a pointed groove. A face that ends
    on a floor or at the foot of a wall has no room for the tool tip and is
    reported instead.
    """
    bevels: dict[int, adsk.fusion.BRepFace] = {}
    other_angles = 0
    for face in body.faces:
        slope = _constant_slope(face, frame)
        if slope is None or _face_top_height(face, frame) < z_max - HEIGHT_TOL:
            continue
        if abs(slope - BEVEL_NORMAL_Z) < DIRECTION_TOL:
            bevels[face.tempId] = face
        elif DIRECTION_TOL < slope < 1 - DIRECTION_TOL:
            other_angles += 1
    if other_angles:
        result.warnings.append(
            f'{body.name}: {other_angles} slanted face(s) at the top are not at 45° and '
            'were not machined; the chamfer bit only cuts 45° chamfers and 90° grooves.')
    if not bevels:
        return

    # Lower edge tempId -> (edge, chamfer face, wall), and the bottom edges of
    # grooves with their two flanks.
    chamfer_edges: dict[int, tuple] = {}
    groove_edges: dict[int, tuple] = {}
    heights: dict[int, float] = {}
    blocked = 0
    for face in bevels.values():
        ranges = [(edge, _edge_height_range(edge, frame)) for edge in face.edges]
        bottom = min(low for _, (low, _) in ranges)
        for edge, (_, high) in ranges:
            if high > bottom + HEIGHT_TOL or edge.tempId in groove_edges:
                continue  # not a lower edge, or a groove seen from its other flank
            others = [f for f in edge.faces if f.tempId != face.tempId]
            if not others:
                continue
            other = others[0]
            midpoint = _edge_midpoint(edge)
            rise = _rise_direction(edge, face, midpoint, frame)
            other_normal = _normal_at(other, midpoint)
            if rise is None or other_normal is None:
                continue
            heights[edge.tempId] = z_max - bottom
            if other.tempId in bevels:
                normal = _normal_at(face, midpoint)
                # Concave, and the flanks lean against each other: a groove
                # with a different opening angle has flanks at other slopes
                # and never gets here.
                if (normal is not None and rise.dotProduct(other_normal) > 0
                        and _horizontal_length(_sum(normal, other_normal), frame) < DIRECTION_TOL):
                    groove_edges[edge.tempId] = (edge, face, other)
                else:
                    blocked += 1
            elif (abs(other_normal.dotProduct(frame.z)) < DIRECTION_TOL
                    and rise.dotProduct(other_normal) < 0):
                # A vertical wall the chamfer leans away from: the wall drops
                # away below the edge.
                chamfer_edges[edge.tempId] = (edge, face, other)
            else:
                blocked += 1
    if blocked:
        result.warnings.append(
            f'{body.name}: {blocked} 45° face(s) end on a floor or against a wall, which '
            'leaves no room for the tip of the chamfer bit; not machined.')

    for edges, is_closed in _chains_by_height(chamfer_edges, heights):
        result.chamfers.append(Chamfer(
            edges=edges,
            faces=[chamfer_edges[edge.tempId][1] for edge in edges],
            walls=[chamfer_edges[edge.tempId][2] for edge in edges],
            height=heights[edges[0].tempId],
            is_closed=is_closed,
            body=body,
            up=frame.z,
            hole_radius=_hole_radius(edges) if is_closed else None,
        ))
    for edges, _ in _chains_by_height(groove_edges, heights):
        flanks: dict[int, adsk.fusion.BRepFace] = {}
        for edge in edges:
            for flank in groove_edges[edge.tempId][1:]:
                flanks[flank.tempId] = flank
        result.grooves.append(Groove(
            edges=edges, faces=list(flanks.values()),
            depth=heights[edges[0].tempId], body=body))


def _constant_slope(face: adsk.fusion.BRepFace, frame: Frame) -> float | None:
    """The vertical component of the face normal if it is the same all over the
    face, None otherwise.

    Planes and upright cones have one; so does the chamfer along a curved
    contour, whatever surface type it is modelled as, which is why this samples
    the normal instead of looking at the geometry. Only up-facing slanted faces
    are sampled beyond the first point - walls and floors are most of a body.
    """
    slope = _normal_at(face, face.pointOnFace)
    if slope is None:
        return None
    slope = slope.dotProduct(frame.z)
    if not DIRECTION_TOL < slope < 1 - DIRECTION_TOL:
        return slope
    for edge in face.edges:
        normal = _normal_at(face, _edge_midpoint(edge))
        if normal is None or abs(normal.dotProduct(frame.z) - slope) > DIRECTION_TOL:
            return None
    return slope


def _normal_at(face: adsk.fusion.BRepFace,
               point: adsk.core.Point3D) -> adsk.core.Vector3D | None:
    ok, normal = face.evaluator.getNormalAtPoint(point)
    return normal if ok else None


def _rise_direction(edge: adsk.fusion.BRepEdge, face: adsk.fusion.BRepFace,
                    midpoint: adsk.core.Point3D, frame: Frame) -> adsk.core.Vector3D | None:
    """The direction in which a slanted face climbs away from its lower edge."""
    normal = _normal_at(face, midpoint)
    ok, tangent = edge.evaluator.getTangent(_edge_mid_parameter(edge))
    if normal is None or not ok:
        return None
    rise = tangent.crossProduct(normal)
    if rise.length < 1e-9:
        return None
    rise.normalize()
    if rise.dotProduct(frame.z) < 0:
        rise.scaleBy(-1.0)
    return rise


def _sum(a: adsk.core.Vector3D, b: adsk.core.Vector3D) -> adsk.core.Vector3D:
    result = a.copy()
    result.add(b)
    return result


def _horizontal_length(vector: adsk.core.Vector3D, frame: Frame) -> float:
    return _perpendicular_component(vector, frame.z).length


def _edge_mid_parameter(edge: adsk.fusion.BRepEdge) -> float:
    _, param_min, param_max = edge.evaluator.getParameterExtents()
    return (param_min + param_max) / 2


def _edge_height_range(edge: adsk.fusion.BRepEdge, frame: Frame) -> tuple[float, float]:
    """Lowest and highest point of an edge. Sampled strictly inside the
    parameter range: the evaluator rejects a parameter that lands a rounding
    error past either end."""
    evaluator = edge.evaluator
    _, param_min, param_max = evaluator.getParameterExtents()
    heights = [frame.height(vertex.geometry)
               for vertex in (edge.startVertex, edge.endVertex) if vertex]
    for step in (0.25, 0.5, 0.75):
        ok, point = evaluator.getPointAtParameter(param_min + (param_max - param_min) * step)
        if ok:
            heights.append(frame.height(point))
    return min(heights), max(heights)


def _chains_by_height(entries: dict[int, tuple],
                      heights: dict[int, float]) -> list[tuple[list, bool]]:
    """Chains of the collected edges, kept apart by height: edges at different
    levels belong to different chamfers even where they happen to touch."""
    levels: dict[float, list[adsk.fusion.BRepEdge]] = {}
    for edge_id, entry in entries.items():
        levels.setdefault(round(heights[edge_id], 4), []).append(entry[0])
    chains: list[tuple[list, bool]] = []
    for _, edges in sorted(levels.items()):
        chains += _chains(edges)
    return chains


def _chains(edges: list[adsk.fusion.BRepEdge]) -> list[tuple[list[adsk.fusion.BRepEdge], bool]]:
    """Sort edges into chains running end to end: (edges in chain order,
    whether the chain closes on itself)."""
    by_id = {edge.tempId: edge for edge in edges}
    ends: dict[int, list[int]] = {}
    at_vertex: dict[int, list[int]] = {}
    for edge in edges:
        vertices: list[int] = []
        for vertex in (edge.startVertex, edge.endVertex):
            if vertex and vertex.tempId not in vertices:
                vertices.append(vertex.tempId)
        ends[edge.tempId] = vertices
        for vertex in vertices:
            at_vertex.setdefault(vertex, []).append(edge.tempId)
    unused = set(by_id)

    def walk(edge_id: int, vertex: int | None) -> tuple[list[int], int | None]:
        chain = [edge_id]
        unused.discard(edge_id)
        while vertex is not None:
            following = [e for e in at_vertex[vertex] if e in unused]
            if not following:
                break
            edge_id = following[0]
            unused.discard(edge_id)
            chain.append(edge_id)
            vertex = next((v for v in ends[edge_id] if v != vertex), None)
        return chain, vertex

    chains: list[tuple[list[adsk.fusion.BRepEdge], bool]] = []
    # Open chains first, each from one of its loose ends, so that a chain is
    # not started in its middle and split in two.
    for edge_id in list(by_id):
        if edge_id not in unused or len(ends[edge_id]) < 2:
            continue
        loose = [v for v in ends[edge_id] if len(at_vertex[v]) == 1]
        if loose:
            chain, _ = walk(edge_id, next(v for v in ends[edge_id] if v != loose[0]))
            chains.append(([by_id[e] for e in chain], False))
    for edge_id in list(by_id):
        if edge_id not in unused:
            continue
        if len(ends[edge_id]) < 2:
            # A full circle: closed by itself.
            unused.discard(edge_id)
            chains.append(([by_id[edge_id]], True))
            continue
        first, second = ends[edge_id]
        chain, last = walk(edge_id, second)
        chains.append(([by_id[e] for e in chain], last == first and len(chain) > 1))
    return chains


def _hole_radius(edges: list[adsk.fusion.BRepEdge]) -> float | None:
    """The radius of a closed chain that is one circle, None for any other shape."""
    center = None
    radius = None
    for edge in edges:
        geometry = adsk.core.Circle3D.cast(edge.geometry) or adsk.core.Arc3D.cast(edge.geometry)
        if not geometry:
            return None
        if center is None:
            center, radius = geometry.center, geometry.radius
        elif (center.distanceTo(geometry.center) > HEIGHT_TOL
                or abs(radius - geometry.radius) > HEIGHT_TOL):
            return None
    return radius
