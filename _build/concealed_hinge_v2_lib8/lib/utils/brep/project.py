import adsk.fusion
from adsk.core import Point3D

def project_point_onto_edge(point: Point3D, edge: adsk.fusion.BRepEdge) -> Point3D:
    _, param = edge.evaluator.getParameterAtPoint(point)
    _, projected_point = edge.evaluator.getPointAtParameter(param)
    return projected_point

def project_point_onto_face(point: Point3D, face: adsk.fusion.BRepFace) -> Point3D:
    _, param = face.evaluator.getParameterAtPoint(point)
    _, projected_point = face.evaluator.getPointAtParameter(param)
    return projected_point
