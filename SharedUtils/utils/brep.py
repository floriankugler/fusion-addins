import math
from typing import Any, Callable, Optional
from . import fusion, misc, matrix, vector
import adsk.core, adsk.fusion
from adsk.core import OrientedBoundingBox3D, Point3D, Vector3D, Matrix3D

def normal_into_face(edge: adsk.fusion.BRepEdge, face: adsk.fusion.BRepFace) -> Vector3D:
    eval = face.evaluator
    _, face_normal = eval.getNormalAtParameter(eval.parametricRange().minPoint)
    edge_normal = normal_along_edge(edge)
    result = edge_normal.crossProduct(face_normal)
    edge_mid = vector.add(edge.startVertex.geometry.asVector(), vector.scaled_by(edge_normal, edge.length/2))
    test_point = vector.add(edge_mid, vector.scaled_by(result, 0.1)).asPoint()
    _, test_param = eval.getParameterAtPoint(test_point)
    if not eval.isParameterOnFace(test_param):
        result.scaleBy(-1)
    return result

def adjecent_edge(edge: adsk.fusion.BRepEdge, face: adsk.fusion.BRepFace) -> adsk.fusion.BRepEdge:
    loop = next(l for l in face.loops if l.isOuter)
    edge_idx = misc.as_list(loop.edges).index(edge)
    return loop.edges[edge_idx + 1] if edge_idx < len(loop.edges) - 1 else loop.edges[0]

def distance_along_normal_between_faces(face1: adsk.fusion.BRepFace, face2: adsk.fusion.BRepFace) -> float:
    if not is_parallel(face1, face2):
        raise ValueError("Only works for parallel faces")
    dir = face1.geometry.origin.vectorTo(face2.geometry.origin)
    return face1.geometry.normal.dotProduct(dir)

def normal_towards_face(from_face: adsk.fusion.BRepFace, to_face: adsk.fusion.BRepFace) -> Vector3D:
    normal: Vector3D = from_face.geometry.normal.copy()
    dist = distance_along_normal_between_faces(from_face, to_face)
    normal.scaleBy(dist)
    normal.normalize()
    return normal

def is_planar(face: adsk.fusion.BRepFace) -> bool:
    return face.geometry.surfaceType == adsk.core.SurfaceTypes.PlaneSurfaceType
 
def is_linear(edge: adsk.fusion.BRepEdge) -> bool:
    return edge.geometry.curveType == adsk.core.Curve3DTypes.Line3DCurveType

def is_perpendicular(face1: adsk.fusion.BRepFace, face2: adsk.fusion.BRepFace) -> bool:
    if not is_planar(face1) or not is_planar(face2):
         return False
    return face1.geometry.normal.isPerpendicularTo(face2.geometry.normal)

def is_parallel(face1: adsk.fusion.BRepFace, face2: adsk.fusion.BRepFace) -> bool:
    if not is_planar(face1) or not is_planar(face2):
        return False
    return face1.geometry.normal.isParallelTo(face2.geometry.normal)

def get_opposite_face(face: adsk.fusion.BRepFace) -> adsk.fusion.BRepFace:
    if not is_planar(face): 
        raise ValueError("Face must be planar.")

    faces = []
    for f in face.body.faces:
        if f != face and is_parallel(face, f):
            faces.append(f)
    faces.sort(key=lambda x: x.area)
    return faces[-1]

def get_board_thickness(face: adsk.fusion.BRepFace) -> float:
    if not is_planar(face): 
        raise ValueError("Face must be planar.")

    opposite_face = get_opposite_face(face)
    if opposite_face is None:
        raise RuntimeError("No opposite planar face found.")

    return abs(distance_along_normal_between_faces(face, opposite_face))

def largest_face_of_edge(edge: adsk.fusion.BRepEdge) -> adsk.fusion.BRepFace:
    face: adsk.fusion.BRepFace = edge.faces.item(0)
    for idx in range(1, edge.faces.count):
        newFace = edge.faces.item(idx)
        if newFace.area > face.area:
            face = newFace
    return face

def face_contains_edge(face: adsk.fusion.BRepFace, edge: adsk.fusion.BRepEdge) -> bool:
    if not is_planar(face):
        return False

    return face.boundingBox.contains(edge.startVertex.geometry) and face.boundingBox.contains(edge.endVertex.geometry)

def find_perpendicular_face_containing_edge(edge: adsk.fusion.BRepEdge, reference_face: adsk.fusion.BRepFace) -> Optional[adsk.fusion.BRepFace]:
    tol = 1e-6
    if not is_planar(reference_face):
        raise ValueError("Only works with planar reference face")
    if not is_linear(edge):
        raise ValueError("Only works on linear edges")
    
    occ = edge.body.assemblyContext
    result = None

    def search_occurrence(o: adsk.fusion.Occurrence) -> bool:
        for body in occ.bRepBodies:
            if body == edge.body:
                continue
            for face in body.faces:
                if face_contains_edge(face, edge) and is_perpendicular(face, reference_face):
                    nonlocal result
                    result = face
                    return True

    fusion.traverse_occurrence_tree(occ, search_occurrence)
    return result

def longest_and_adjecent_edge_of_face(face: adsk.fusion.BRepFace) -> tuple[adsk.fusion.BRepEdge, adsk.fusion.BRepEdge]:
    loop = next(l for l in face.loops if l.isOuter)
    longest_edge = sorted(loop.edges, key=lambda e: e.length, reverse=True)[0]
    next_edge = adjecent_edge(longest_edge, face)
    return (longest_edge, next_edge)

def outer_edges_of_face(face: adsk.fusion.BRepFace) -> list[adsk.fusion.BRepEdge]:
    loop = next((x for x in face.loops if x.isOuter), None)
    return misc.as_list(loop.edges)

def vertices_of_face(face: adsk.fusion.BRepFace) -> list[adsk.fusion.BRepVertex]:
    edges = outer_edges_of_face(face)
    vertices = []
    for edge in edges:
        if edge.startVertex not in vertices: 
            vertices.append(edge.startVertex)
        if edge.endVertex not in vertices: 
            vertices.append(edge.endVertex)
    return vertices

def common_face_of_edges(edges: list[adsk.fusion.BRepEdge]) -> adsk.fusion.BRepFace:
    faces = [misc.as_list(edge.faces) for edge in edges]
    result = faces[0]
    for x in faces[1:]:
        result = misc.intersect_lists(result, x)
    return result[0]

def common_face_of_vertices(vertices: list[adsk.fusion.BRepVertex]) -> adsk.fusion.BRepFace:
    faces = [misc.as_list(v.faces) for v in vertices]
    result = faces[0]
    for x in faces[1:]:
        result = misc.intersect_lists(result, x)
    return result[0]

def normal_along_edge(edge: adsk.fusion.BRepEdge) -> Vector3D:
    result = edge.endVertex.geometry.asVector()
    result.subtract(edge.startVertex.geometry.asVector())
    result.normalize()
    return result

def fillet_cut_body(point: Point3D, leg1: Vector3D, leg2: Vector3D, fillet_radius: float, thickness) -> adsk.fusion.BRepBody:
    mgr = adsk.fusion.TemporaryBRepManager.get()
    leg1.normalize()
    leg2.normalize()
    angle = math.acos(leg1.dotProduct(leg2))
    cylinder_mid_distance = fillet_radius/math.sin(angle/2)
    cylinder_leg_distance = fillet_radius/math.tan(angle/2)
    cyl1 = leg1.copy()
    cyl1.add(leg2)
    cyl1.scaleBy(0.5)
    cyl1.normalize()
    cyl1.scaleBy(cylinder_mid_distance)
    cyl1.add(point.asVector())
    cyl2 = cyl1.copy()
    cyl2.add(Vector3D.create(0, 0, thickness))
    cyl = mgr.createCylinderOrCone(cyl1.asPoint(), fillet_radius, cyl2.asPoint(), fillet_radius)
    cut_cyl1 = point.copy()
    cut_cyl2 = point.copy()
    cut_cyl2.translateBy(Vector3D.create(0, 0, thickness))
    cut_cyl = mgr.createCylinderOrCone(cut_cyl1, cylinder_leg_distance, cut_cyl2, cylinder_leg_distance)
    mgr.booleanOperation(cut_cyl, cyl, adsk.fusion.BooleanTypes.DifferenceBooleanType)
    return cut_cyl

# Creates an isosceles triangle in the xy plane. Base is along x, origin is at mid-base, thickness is in positive z.
def isosceles_triangle(width, height, thickness, fillet_radius = 0) -> adsk.fusion.BRepBody:
    mgr = adsk.fusion.TemporaryBRepManager.get()
    alpha = math.atan(height/(width/2))
    leg_length = height / math.sin(alpha)
    rectangle_extent = math.sin(alpha) * width

    trim_bb = adsk.core.OrientedBoundingBox3D.create(Point3D.create(100, height/2, thickness/2), Vector3D.create(1, 0, 0), Vector3D.create(0, 1, 0), 200, height, thickness)
    trim_body = mgr.createBox(trim_bb)

    bounding_box = adsk.core.OrientedBoundingBox3D.create(Point3D.create(0, 0, 0), Vector3D.create(1, 0, 0), Vector3D.create(0, 1, 0), leg_length, rectangle_extent, thickness)
    box = mgr.createBox(bounding_box)
    mgr.transform(box, matrix.translation_matrix(Vector3D.create(leg_length/2, -rectangle_extent/2, thickness/2)))
    mgr.transform(box, matrix.rotation_matrix(alpha, Vector3D.create(0, 0, -1), Point3D.create()))
    mgr.transform(box, matrix.translation_matrix(Vector3D.create(0, height, 0)))

    if fillet_radius > 0:
        fillet1 = fillet_cut_body(Point3D.create(width/2, 0, 0), Vector3D.create(-width/2, 0, 0), Vector3D.create(-width/2, height, 0), fillet_radius, thickness)
        mgr.booleanOperation(box, fillet1, adsk.fusion.BooleanTypes.DifferenceBooleanType)
        fillet2 = fillet_cut_body(Point3D.create(0, height, 0), Vector3D.create(-width/2, -height, 0), Vector3D.create(width/2, -height, 0), fillet_radius, thickness)
        mgr.booleanOperation(box, fillet2, adsk.fusion.BooleanTypes.DifferenceBooleanType)

    mgr.booleanOperation(box, trim_body, adsk.fusion.BooleanTypes.IntersectionBooleanType)
    box2 = mgr.copy(box)
    mgr.transform(box2, matrix.mirror_matrix(Point3D.create(), Vector3D.create(-1, 1, 1)))
    mgr.booleanOperation(box, box2, adsk.fusion.BooleanTypes.UnionBooleanType)
    return box

# Creates a rounded rectangle in the xy plane. Width is along x, height along y, origin is at the center. Thickness is in positive z.
def rounded_rectangle(width, height, thickness, fillet_radius = 0) -> adsk.fusion.BRepBody:
    mgr = adsk.fusion.TemporaryBRepManager.get()
    x = Vector3D.create(1, 0, 0)
    y = Vector3D.create(0, 1, 0)
    bb1 = OrientedBoundingBox3D.create(Point3D.create(), x, y, width - 2*fillet_radius, height, thickness)
    bb2 = OrientedBoundingBox3D.create(Point3D.create(), x, y, width, height - 2*fillet_radius, thickness)
    box = mgr.createBox(bb1)
    box2 = mgr.createBox(bb2)
    mgr.booleanOperation(box, box2, adsk.fusion.BooleanTypes.UnionBooleanType)
    mgr.transform(box, matrix.translation_matrix(Vector3D.create(0, 0, thickness/2)))
    if fillet_radius > 0:
        cyl = mgr.createCylinderOrCone(Point3D.create(), fillet_radius, Point3D.create(0, 0, thickness), fillet_radius)
        fillet_points = [
            Vector3D.create(-width/2+fillet_radius, height/2-fillet_radius, 0),
            Vector3D.create(width/2-fillet_radius, height/2-fillet_radius, 0),
            Vector3D.create(width/2-fillet_radius, -height/2+fillet_radius, 0),
            Vector3D.create(-width/2+fillet_radius, -height/2+fillet_radius, 0),
        ]
        for p in fillet_points:
            c = mgr.copy(cyl)
            mgr.transform(c, matrix.translation_matrix(p))
            mgr.booleanOperation(box, c, adsk.fusion.BooleanTypes.UnionBooleanType)
    return box

# Creates a rhombus, origin as at its center, width is along x, height along y. 
def rhombus(width, height, thickness, fillet_radius) -> adsk.fusion.BRepBody:
    mgr = adsk.fusion.TemporaryBRepManager.get()
    small_angle = math.atan(width/height) * 2
    leg_length = width/2 / math.sin(small_angle/2)
    box_width = math.sin(small_angle) * leg_length
    box_height = math.cos(small_angle/2) * height
    bb = OrientedBoundingBox3D.create(Point3D.create(), Vector3D.create(1, 0, 0), Vector3D.create(0, 1, 0), box_width, box_height, thickness)
    box = mgr.createBox(bb)
    box2 = mgr.copy(box)
    mgr.transform(box, matrix.rotation_matrix(small_angle/2, Vector3D.create(0, 0, 1), Point3D.create(0, 0, 0)))
    mgr.transform(box2, matrix.rotation_matrix(-small_angle/2, Vector3D.create(0, 0, 1), Point3D.create(0, 0, 0)))
    mgr.booleanOperation(box, box2, adsk.fusion.BooleanTypes.IntersectionBooleanType)
    if fillet_radius > 0:
        cut1 = fillet_cut_body(Point3D.create(0, height/2, -thickness/2), Vector3D.create(-width/2, -height/2, 0), Vector3D.create(width/2, -height/2, 0), fillet_radius, thickness)    
        mgr.booleanOperation(box, cut1, adsk.fusion.BooleanTypes.DifferenceBooleanType)
        mgr.transform(cut1, matrix.mirror_matrix(Point3D.create(), Vector3D.create(1, -1, 1)))
        mgr.booleanOperation(box, cut1, adsk.fusion.BooleanTypes.DifferenceBooleanType)
        cut2 = fillet_cut_body(Point3D.create(-width/2, 0, -thickness/2), Vector3D.create(width/2, height/2, 0), Vector3D.create(width/2, -height/2, 0), fillet_radius, thickness)
        mgr.booleanOperation(box, cut2, adsk.fusion.BooleanTypes.DifferenceBooleanType)
        mgr.transform(cut2, matrix.mirror_matrix(Point3D.create(), Vector3D.create(-1, 1, 1)))
        mgr.booleanOperation(box, cut2, adsk.fusion.BooleanTypes.DifferenceBooleanType)
    return box

# Creates a cylinder with point at the cylinder's lower circle's center, height is positive z.
def cylinder(point: Point3D, radius: float, height: float) -> adsk.fusion.BRepBody:
    mgr = adsk.fusion.TemporaryBRepManager.get()
    return mgr.createCylinderOrCone(point, radius, Point3D.create(point.x, point.y, point.z + height), radius)
    
# Creates a slot with the length along x, thickness positive in z. Origin is at the center bottom of the first cylinder.
def slot(length: float, radius: float, thickness: float) -> adsk.fusion.BRepBody:
    mgr = adsk.fusion.TemporaryBRepManager.get()
    cyl1 = cylinder(adsk.core.Point3D.create(-length/2, 0, -thickness/2), radius, thickness)
    cyl2 = transformed(cyl1, matrix.translation_matrix(Vector3D.create(length, 0, 0)))
    box = mgr.createBox(adsk.core.OrientedBoundingBox3D.create(adsk.core.Point3D.create(), adsk.core.Vector3D.create(1, 0, 0), adsk.core.Vector3D.create(0, 1, 0), length, radius * 2, thickness ))
    mgr.booleanOperation(box, cyl1, adsk.fusion.BooleanTypes.UnionBooleanType)
    mgr.booleanOperation(box, cyl2, adsk.fusion.BooleanTypes.UnionBooleanType)
    mgr.transform(box, matrix.translation_matrix(Vector3D.create(length/2, 0, thickness/2)))
    return box

def transformed(body: adsk.fusion.BRepBody, transform: Matrix3D) -> adsk.fusion.BRepBody:
    mgr = adsk.fusion.TemporaryBRepManager.get()
    copy = mgr.copy(body)
    mgr.transform(copy, transform)
    return copy

def union(bodies: list[adsk.fusion.BRepBody]) -> adsk.fusion.BRepBody:
    mgr = adsk.fusion.TemporaryBRepManager.get()
    result = mgr.copy(bodies[0])
    for body in bodies[1:]:
        mgr.booleanOperation(result, body, adsk.fusion.BooleanTypes.UnionBooleanType)
    return result

# Constructs a right handed coordinate system on the face with the z axis pointing away from the body. The origin is either at the edges start or end vertex to ensure right handedness.
def coordinate_system_on_face(face: adsk.fusion.BRepFace, edge: adsk.fusion.BRepEdge) -> tuple[Point3D, Vector3D, Vector3D, Vector3D]:
    origin = edge.startVertex.geometry
    face_normal_into_body = normal_towards_face(face, get_opposite_face(face))
    x = normal_along_edge(edge)
    y = normal_into_face(edge, face)
    z = x.crossProduct(y)
    # Make sure we have a right hand coordinate system with z pointing away from the body, otherwise flip the x axis.
    if vector.dot_product(z, face_normal_into_body) > 0:
        origin = edge.endVertex.geometry
        x.scaleBy(-1)
        z = x.crossProduct(y)
    return (origin, x, y, z)

    