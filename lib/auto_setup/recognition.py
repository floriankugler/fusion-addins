"""Geometry recognition for automatic manufacturing setups.

Detects machinable features (holes, pockets, through cutouts, outer contours)
on bodies, relative to a user-defined machining frame. All lengths are in cm
(Fusion internal units). Pure geometry - no CAM API calls.
"""

import adsk.core, adsk.fusion
from dataclasses import dataclass, field

# Tolerances (cm / dimensionless)
HEIGHT_TOL = 1e-3
DIRECTION_TOL = 1e-3


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
class RecognitionResult:
    holes: list[Hole] = field(default_factory=list)
    pockets: list[Pocket] = field(default_factory=list)
    cutouts: list[Cutout] = field(default_factory=list)
    contours: list[Contour] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def extend(self, other: 'RecognitionResult'):
        self.holes.extend(other.holes)
        self.pockets.extend(other.pockets)
        self.cutouts.extend(other.cutouts)
        self.contours.extend(other.contours)
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
    if top < z_max - HEIGHT_TOL:
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
        depth=top - bottom,
        is_through=is_through,
        body=body,
        bottom_edge=bottom_edge,
    )


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
