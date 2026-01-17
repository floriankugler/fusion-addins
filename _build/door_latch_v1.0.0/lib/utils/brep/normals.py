from .. import vector
from . import properties as prop, relationships as rel
import adsk.core, adsk.fusion
from adsk.core import Vector3D

def normal_into_face(edge: adsk.fusion.BRepEdge, face: adsk.fusion.BRepFace) -> Vector3D:
    eval = face.evaluator
    _, face_normal = eval.getNormalAtParameter(eval.parametricRange().minPoint)
    edge_normal = normal_along_edge(edge)
    result = edge_normal.crossProduct(face_normal)
    edge_mid = prop.edge_middle_point(edge).asVector()
    test_point = vector.add(edge_mid, vector.scaled_by(result, 0.1)).asPoint()
    _, test_param = eval.getParameterAtPoint(test_point)
    if not eval.isParameterOnFace(test_param):
        result.scaleBy(-1)
    return result

def normal_away_from_body(face: adsk.fusion.BRepFace) -> Vector3D:
    centroid = face.centroid
    _, normal = face.evaluator.getNormalAtPoint(centroid)
    test_point = vector.add(centroid.asVector(), vector.scaled_by(normal, 0.01)).asPoint()
    if face.body.pointContainment(test_point) == adsk.fusion.PointContainment.PointInsidePointContainment:
        normal.scaleBy(-1)
    return normal

def normal_towards_face(from_face: adsk.fusion.BRepFace, to_face: adsk.fusion.BRepFace) -> Vector3D:
    assert(isinstance(from_face.geometry, adsk.core.Plane) and isinstance(to_face.geometry, adsk.core.Plane))
    normal: Vector3D = from_face.geometry.normal.copy()
    dist = rel.distance_along_normal_between_faces(from_face, to_face)
    normal.scaleBy(dist)
    normal.normalize()
    return normal

def normal_along_edge(edge: adsk.fusion.BRepEdge) -> Vector3D:
    result = edge.endVertex.geometry.asVector()
    result.subtract(edge.startVertex.geometry.asVector())
    result.normalize()
    return result
