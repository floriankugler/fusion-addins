from .. import matrix, vector
from . import coordinates
import adsk.fusion
from adsk.core import Vector3D, Matrix3D


def transformed(body: adsk.fusion.BRepBody, transform: Matrix3D) -> adsk.fusion.BRepBody:
    mgr = adsk.fusion.TemporaryBRepManager.get()
    copy = mgr.copy(body)
    mgr.transform(copy, transform)
    return copy

def union(bodies: list[adsk.fusion.BRepBody]) -> adsk.fusion.BRepBody:
    mgr = adsk.fusion.TemporaryBRepManager.get()
    result = mgr.copy(bodies[0])
    for body in bodies[1:]:
        mgr.booleanOperation(result, body, adsk.fusion.BooleanTypes.UnionBooleanType) # type: ignore
    return result

def subtract(b1: adsk.fusion.BRepBody, b2: adsk.fusion.BRepBody) -> adsk.fusion.BRepBody:
    mgr = adsk.fusion.TemporaryBRepManager.get()
    result = mgr.copy(b1)
    mgr.booleanOperation(result, b2, adsk.fusion.BooleanTypes.DifferenceBooleanType) # type: ignore
    return result

def intersect(b1: adsk.fusion.BRepBody, b2: adsk.fusion.BRepBody) -> adsk.fusion.BRepBody:
    mgr = adsk.fusion.TemporaryBRepManager.get()
    result = mgr.copy(b1)
    mgr.booleanOperation(result, b2, adsk.fusion.BooleanTypes.IntersectionBooleanType) # type: ignore
    return result

def place_body_on_face_at_positions(body: adsk.fusion.BRepBody, face: adsk.fusion.BRepFace, edge: adsk.fusion.BRepEdge, positions: list[Vector3D]) -> adsk.fusion.BRepBody:
    origin, x, y, _ = coordinates.coordinate_system_on_face(face, edge)
    x_coords = [vector.subtract(p, origin.asVector()).dotProduct(x) for p in positions]
    groups = [transformed(body, matrix.translation_matrix(Vector3D.create(x, 0, 0))) for x in x_coords]
    result = union(groups)
    return transformed(result, matrix.transform_from_root(origin, x, y))

def place_body_on_face_at_position(body: adsk.fusion.BRepBody, face: adsk.fusion.BRepFace, edge: adsk.fusion.BRepEdge, position: Vector3D) -> adsk.fusion.BRepBody:
    origin, x, y, _ = coordinates.coordinate_system_on_face(face, edge)
    x_coord = vector.subtract(position, origin.asVector()).dotProduct(x)
    result = transformed(body, matrix.translation_matrix(Vector3D.create(x_coord, 0, 0)))
    return transformed(result, matrix.transform_from_root(origin, x, y))
