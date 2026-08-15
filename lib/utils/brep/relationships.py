import math
from .. import vector
from . import normals as norm, sampling
import adsk.core, adsk.fusion
from adsk.core import Vector3D

def distance_along_normal_between_faces(face1: adsk.fusion.BRepFace, face2: adsk.fusion.BRepFace) -> float:
    if not is_parallel(face1, face2):
        raise ValueError("Faces must be parallel.")
    if not isinstance(face1.geometry, adsk.core.Plane) or not isinstance(face2.geometry, adsk.core.Plane):
        raise ValueError("Faces must be planar.")
    dir = face1.geometry.origin.vectorTo(face2.geometry.origin)
    return face1.geometry.normal.dotProduct(dir)

def is_planar(face: adsk.fusion.BRepFace) -> bool:
    return face.geometry.surfaceType == adsk.core.SurfaceTypes.PlaneSurfaceType
 
def is_linear(edge: adsk.fusion.BRepEdge) -> bool:
    return edge.geometry.curveType == adsk.core.Curve3DTypes.Line3DCurveType

def is_perpendicular(a: adsk.fusion.BRepFace | adsk.fusion.BRepEdge, b: adsk.fusion.BRepFace | adsk.fusion.BRepEdge) -> bool:
    match (a,b):
        case (adsk.fusion.BRepFace(), adsk.fusion.BRepFace()):
            if not isinstance(a.geometry, adsk.core.Plane) or not isinstance(b.geometry, adsk.core.Plane):
                return False
            return vector.is_perpendicular_direction(a.geometry.normal, b.geometry.normal)
        case (adsk.fusion.BRepEdge(), adsk.fusion.BRepEdge()):
            if not is_linear(a) or not is_linear(b):
                return False
            return vector.is_perpendicular_direction(
                norm.normal_along_edge(a), norm.normal_along_edge(b))
        case (adsk.fusion.BRepFace(), adsk.fusion.BRepEdge()):
            if not is_planar(a) or not is_linear(b):
                return False
            return vector.is_parallel_direction(
                norm.normal_away_from_body(a), norm.normal_along_edge(b))
        case (adsk.fusion.BRepEdge(), adsk.fusion.BRepFace()):
            if not is_linear(a) or not is_planar(b):
                return False
            return vector.is_parallel_direction(
                norm.normal_away_from_body(b), norm.normal_along_edge(a))
        case _:
            raise TypeError(f"Unsupported type: {type(a)}, {type(b)}")

def is_parallel(a: adsk.fusion.BRepFace | adsk.fusion.BRepEdge | Vector3D, b: adsk.fusion.BRepFace | adsk.fusion.BRepEdge | Vector3D) -> bool:
    match (a, b):
        case (adsk.fusion.BRepFace(), adsk.fusion.BRepFace()):
            if not isinstance(a.geometry, adsk.core.Plane) or not isinstance(b.geometry, adsk.core.Plane):
                return False
            return vector.is_parallel_direction(a.geometry.normal, b.geometry.normal)
        case (adsk.fusion.BRepEdge(), Vector3D()):
            if not is_linear(a):
                return False
            v1 = vector.subtract(a.endVertex.geometry.asVector(), a.startVertex.geometry.asVector())
            return vector.is_parallel_direction(v1, b)
        case (Vector3D(), adsk.fusion.BRepEdge()):
            return is_parallel(b, a)
        case (adsk.fusion.BRepEdge(), adsk.fusion.BRepEdge()):
            if not is_linear(a) or not is_linear(b):
                return False
            v1 = vector.subtract(a.endVertex.geometry.asVector(), a.startVertex.geometry.asVector())
            v2 = vector.subtract(b.endVertex.geometry.asVector(), b.startVertex.geometry.asVector())
            return vector.is_parallel_direction(v1, v2)
        case _:
            raise TypeError(f"Unsupported type: {type(a)}, {type(b)}")

# A face covering at least this much of the edge is the edge's dominant mate;
# see face_contains_edge.
DOMINANT_COVERAGE = 0.5

def bounding_boxes_overlap(a: adsk.core.BoundingBox3D, b: adsk.core.BoundingBox3D, tolerance: float = 1e-6) -> bool:
    """Whether two boxes overlap, within tolerance. Geometry that cannot touch
    fails this before any surface evaluation, which is the cheap way to skip
    the bulk of a design."""
    return all(
        getattr(a.minPoint, axis) - tolerance <= getattr(b.maxPoint, axis)
        and getattr(b.minPoint, axis) - tolerance <= getattr(a.maxPoint, axis)
        for axis in ("x", "y", "z")
    )

def point_in_bounding_box(box: adsk.core.BoundingBox3D, point: adsk.core.Point3D, tolerance: float = 1e-6) -> bool:
    return all(
        getattr(box.minPoint, axis) - tolerance <= getattr(point, axis) <= getattr(box.maxPoint, axis) + tolerance
        for axis in ("x", "y", "z")
    )

def edge_coverage_on_face(face: adsk.fusion.BRepFace, edge: adsk.fusion.BRepEdge, tolerance: float = 1e-6) -> float:
    """Fraction of the edge's probe points that lie on the face, 0.0 to 1.0."""
    if not is_planar(face) or not bounding_boxes_overlap(face.boundingBox, edge.boundingBox, tolerance):
        return 0.0
    test_points = sampling.sample_points_along_edge(edge)
    if not test_points:
        return 0.0
    hits = sum(1 for p in test_points if face.isPointOnFace(p, tolerance))
    return hits / len(test_points)

def face_contains_edge(face: adsk.fusion.BRepFace, edge: adsk.fusion.BRepEdge, min_coverage: float = 0.0, tolerance: float = 1e-6) -> bool:
    """Whether the face covers at least `min_coverage` of the edge's length.

    The default accepts any real overlap, because a mating board is often much
    shorter than the selected edge - a narrow rail butting into a wide panel,
    say. Pass DOMINANT_COVERAGE to ask for a face that runs along most of the
    edge, which is worth trying first when several faces could qualify.

    This gets called for every face of every body in some searches, so it
    stops probing as soon as the answer is settled either way.
    """
    if not is_planar(face) or not bounding_boxes_overlap(face.boundingBox, edge.boundingBox, tolerance):
        return False
    test_points = sampling.sample_points_along_edge(edge)
    if not test_points:
        return False
    needed = max(1, math.ceil(min_coverage * len(test_points)))
    hits = 0
    for index, point in enumerate(test_points):
        if face.isPointOnFace(point, tolerance):
            hits += 1
            if hits >= needed:
                return True
        elif hits + (len(test_points) - index - 1) < needed:
            return False
    return False

def is_smooth_edge(edge: adsk.fusion.BRepEdge) -> bool:
    """
    Determines whether the given edge is smooth between its two adjacent faces.
    This only works for edges where the adjacent faces have a uniform normal vector along the edge's extent.
    """
    if edge.faces.count < 2:
        raise ValueError("Edge must have at least two adjacent faces.")
    p = edge.startVertex.geometry
    _, n1 = edge.faces[0].evaluator.getNormalAtPoint(p)
    _, n2 = edge.faces[1].evaluator.getNormalAtPoint(p)
    return vector.is_parallel_direction(n1, n2)

def is_co_planar(face1: adsk.fusion.BRepFace, face2: adsk.fusion.BRepFace) -> bool:
    if not is_parallel(face1, face2):
        return False
    _, normal = face1.evaluator.getNormalAtParameter(face1.evaluator.parametricRange().minPoint)
    face1_point_projection = face1.centroid.asVector().dotProduct(normal)
    face2_point_projection = face2.centroid.asVector().dotProduct(normal)
    return abs(face1_point_projection - face2_point_projection) < 1e-6
