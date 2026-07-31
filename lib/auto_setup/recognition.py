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
    # Smallest concave (inside) corner fillet radius of the boundary, None if
    # there are no concave arcs (e.g. all corners sharp): no tool constraint.
    min_corner_radius: float | None = None


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
                min_corner_radius=_min_concave_corner_radius(face),
            ))

    bottom_faces = [
        f for f in body.faces
        if _is_down_facing_plane(f, frame) and frame.height(f.pointOnFace) <= z_min + HEIGHT_TOL
    ]
    if not bottom_faces:
        result.warnings.append(f'{body.name}: no planar bottom face found; skipped cutout detection.')
    for face in bottom_faces:
        for loop in face.loops:
            if loop.isOuter:
                continue
            if _loop_matches_hole(loop, result.holes, frame):
                continue
            result.cutouts.append(Cutout(edges=list(loop.edges), body=body,
                                         depth=z_max - z_min))

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
    if not axis.isParallelTo(frame.z):
        warnings.append(f'{body.name}: cylindrical face with non-vertical axis skipped.')
        return None

    # Concave check: for a hole, the face normal points towards the axis.
    point = face.pointOnFace
    _, normal = face.evaluator.getNormalAtPoint(point)
    radial = cylinder.origin.vectorTo(point)
    radial = _perpendicular_component(radial, axis)
    if normal.dotProduct(radial) > 0:
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


def _has_full_circle_edge(face: adsk.fusion.BRepFace) -> bool:
    return any(adsk.core.Circle3D.cast(edge.geometry) for edge in face.edges)


def _min_concave_corner_radius(face: adsk.fusion.BRepFace) -> float | None:
    """Smallest radius among concave boundary arcs of a planar face.

    An arc is concave (an inside corner fillet the tool must fit into) when the
    face material lies on the arc's center side. Sharp corners are ignored:
    they carry no design radius, the tool simply leaves its own.
    """
    evaluator = face.evaluator
    min_radius: float | None = None
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
                radius = geometry.radius
                min_radius = radius if min_radius is None else min(min_radius, radius)
    return min_radius


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
