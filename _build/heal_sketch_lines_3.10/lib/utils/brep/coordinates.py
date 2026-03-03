from .. import vector
from . import normals as norm, find_geometry as find
import adsk.core, adsk.fusion
from adsk.core import Point3D, Vector3D


# Constructs a right handed coordinate system on the face with the z axis pointing away from the body. The origin is either at the edges start or end vertex in order for positive z and y to point into the face's boundaries.
def coordinate_system_on_face(face: adsk.fusion.BRepFace, edge: adsk.fusion.BRepEdge) -> tuple[Point3D, Vector3D, Vector3D, Vector3D]:
    origin = edge.startVertex.geometry
    face_normal_into_body = norm.normal_towards_face(face, find.get_opposite_face(face))
    x = norm.normal_along_edge(edge)
    y = norm.normal_into_face(edge, face)
    z = x.crossProduct(y)
    # Make sure we have a right hand coordinate system with z pointing away from the body, otherwise flip the x axis.
    if vector.dot_product(z, face_normal_into_body) > 0:
        origin = edge.endVertex.geometry
        x.scaleBy(-1)
        z = x.crossProduct(y)
    return (origin, x, y, z)

def coordinate_system_into_face(face: adsk.fusion.BRepFace, z: Vector3D) -> tuple[Point3D, Vector3D, Vector3D, Vector3D]:
    """
    Creates a right-handed coordinate system on the face, so that x is along the long edge, y points towards the center of the face, z points along cut
    """
    long_edge, _ = find.longest_and_adjecent_edge_of_face(face)
    # y is from the longest_edge into the face
    y = norm.normal_into_face(long_edge, face)
    # z points down into the body
    z = vector.normalized(z)
    x = y.crossProduct(z)
    origin = long_edge.startVertex.geometry
    # if x, computed by y and z, doesn't lign up with the long_edge normal (which is derived from the edge's start to end points), we have to set the origin to the end point
    if vector.dot_product(x, norm.normal_along_edge(long_edge)) < 0:
        origin = long_edge.endVertex.geometry
    return origin , x, y, z
    
def coordinate_system_around_face(face: adsk.fusion.BRepFace, z: Vector3D, x: Vector3D | None = None) -> tuple[Point3D, Vector3D, Vector3D, Vector3D]:
    """
    Creates a right-handed coordinate system on the face, so that the entire face, no matter the shape, lies in the positive x-y quadrant of the coordinate system.
    The x axis is along the longest dimension of the face's bounding box if not specified. The z axis is returned as passed in.
    """
    origin: Point3D
    xv: Vector3D
    yv: Vector3D
    if x:
        measure = adsk.core.Application.get().measureManager
        y = x.crossProduct(z)
        bb = measure.getOrientedBoundingBox(face, x, y)
        center = bb.centerPoint.asVector()
        center.subtract(vector.scaled_by(bb.lengthDirection, bb.length/2))
        center.subtract(vector.scaled_by(bb.widthDirection, bb.width/2))
        origin = center.asPoint()
        xv = vector.scaled_by(bb.lengthDirection, bb.length)
        yv = vector.scaled_by(bb.widthDirection, bb.width)
    else:
        eval = face.evaluator
        param_range = eval.parametricRange()
        _, origin = eval.getPointAtParameter(param_range.minPoint)
        _, max_x_point = eval.getPointAtParameter(adsk.core.Point2D.create(param_range.maxPoint.x, param_range.minPoint.y))
        _, max_y_point = eval.getPointAtParameter(adsk.core.Point2D.create(param_range.minPoint.x, param_range.maxPoint.y))
        xv = vector.subtract(max_x_point.asVector(), origin.asVector())
        yv = vector.subtract(max_y_point.asVector(), origin.asVector())
        if xv.length < yv.length:
            xv, yv = yv, xv
    zv = xv.crossProduct(yv)
    if zv.dotProduct(z) < 0:
        origin = vector.add(origin.asVector(), xv).asPoint()
        xv = vector.scaled_by(xv, -1)
    return origin, xv, yv, z
