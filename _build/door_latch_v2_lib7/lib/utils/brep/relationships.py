from .. import vector
from .. import misc
from . import normals as norm
import adsk.core, adsk.fusion
from adsk.core import Vector3D

def distance_along_normal_between_faces(face1: adsk.fusion.BRepFace, face2: adsk.fusion.BRepFace) -> float:
    assert(is_parallel(face1, face2))
    assert(isinstance(face1.geometry, adsk.core.Plane) and isinstance(face2.geometry, adsk.core.Plane))
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
            return a.geometry.normal.isPerpendicularTo(b.geometry.normal)
        case (adsk.fusion.BRepEdge(), adsk.fusion.BRepEdge()):
            if not is_linear(a) or not is_linear(b):
                return False
            return norm.normal_along_edge(a).isPerpendicularTo(norm.normal_along_edge(b))
        case (adsk.fusion.BRepFace(), adsk.fusion.BRepEdge()):
            if not is_planar(a) or not is_linear(b):
                return False
            return norm.normal_away_from_body(a).isParallelTo(norm.normal_along_edge(b))
        case (adsk.fusion.BRepEdge(), adsk.fusion.BRepFace()):
            if not is_linear(a) or not is_planar(b):
                return False
            return norm.normal_away_from_body(b).isParallelTo(norm.normal_along_edge(a))
        case _:
            raise TypeError(f"Unsupported type: {type(a)}, {type(b)}")

def is_parallel(a: adsk.fusion.BRepFace | adsk.fusion.BRepEdge | Vector3D, b: adsk.fusion.BRepFace | adsk.fusion.BRepEdge | Vector3D) -> bool:
    match (a, b):
        case (adsk.fusion.BRepFace(), adsk.fusion.BRepFace()):
            if not isinstance(a.geometry, adsk.core.Plane) or not isinstance(b.geometry, adsk.core.Plane):
                return False
            return a.geometry.normal.isParallelTo(b.geometry.normal)
        case (adsk.fusion.BRepEdge(), Vector3D()):
            if not is_linear(a):
                return False
            v1 = vector.subtract(a.endVertex.geometry.asVector(), a.startVertex.geometry.asVector())
            return v1.isParallelTo(b)
        case (Vector3D(), adsk.fusion.BRepEdge()):
            return is_parallel(b, a)
        case (adsk.fusion.BRepEdge(), adsk.fusion.BRepEdge()):
            if not is_linear(a) or not is_linear(b):
                return False
            v1 = vector.subtract(a.endVertex.geometry.asVector(), a.startVertex.geometry.asVector())
            v2 = vector.subtract(b.endVertex.geometry.asVector(), b.startVertex.geometry.asVector())
            return v1.isParallelTo(v2)
        case _:
            raise TypeError(f"Unsupported type: {type(a)}, {type(b)}")

def face_contains_edge(face: adsk.fusion.BRepFace, edge: adsk.fusion.BRepEdge) -> bool:
    if not is_planar(face):
        return False
    edge_normal = norm.normal_along_edge(edge)
    test_points = [
        vector.add(edge.startVertex.geometry.asVector(), vector.scaled_by(edge_normal, x)).asPoint()
        for x in misc.float_range(0, edge.length, edge.length / 10)
    ]
    evaluated = [1 if face.isPointOnFace(p, 1e-6) else 0 for p in test_points]
    return sum(evaluated) > 5

def are_sketch_curves_right_handed(curves: list[adsk.fusion.SketchCurve], face: adsk.fusion.BRepFace) -> bool:
    if len(curves) == 1:
        return False
    curve = curves[0]
    eval: adsk.core.CurveEvaluator3D = curve.worldGeometry.evaluator # type: ignore
    _, min, max = eval.getParameterExtents()
    middle = min + 0.5 * (max - min)
    point = eval.getPointAtParameter(middle)[1]
    tangent = eval.getTangent(middle)[1]
    sketch = curve.parentSketch
    normal = sketch.xDirection.crossProduct(sketch.yDirection)
    across = vector.normalized(tangent.crossProduct(normal))
    test_point = vector.add(point.asVector(), vector.scaled_by(across, 0.01)).asPoint()
    is_on_face = face.isPointOnFace(test_point)
    return not is_on_face

def is_smooth_edge(edge: adsk.fusion.BRepEdge) -> bool:
    """
    Determines whether the given edge is smooth between its two adjacent faces.
    This only works for edges where the adjacent faces have a uniform normal vector along the edge's extent.
    """
    p = edge.startVertex.geometry
    _, n1 = edge.faces[0].evaluator.getNormalAtPoint(p)
    _, n2 = edge.faces[1].evaluator.getNormalAtPoint(p)
    return n1.isParallelTo(n2)

def is_co_planar(face1: adsk.fusion.BRepFace, face2: adsk.fusion.BRepFace) -> bool:
    if not is_parallel(face1, face2):
        return False
    _, normal = face1.evaluator.getNormalAtParameter(face1.evaluator.parametricRange().minPoint)
    face1_point_projection = face1.centroid.asVector().dotProduct(normal)
    face2_point_projection = face2.centroid.asVector().dotProduct(normal)
    return abs(face1_point_projection - face2_point_projection) < 1e-6
