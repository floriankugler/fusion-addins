import math
from typing import Any, Callable, Optional
import adsk.core, adsk.fusion

def as_list(objs):
    return [objs.item(idx) for idx in range(len(objs))]

def as_object_collection(objs):
    coll = adsk.core.ObjectCollection.create()
    for body in as_list(objs):
        coll.add(body)
    return coll

def list_contains_by_identity(list, obj):
    for x in list:
        if x == obj:
            return True
    return False

def normal_into_face(edge: adsk.fusion.BRepEdge, face: adsk.fusion.BRepFace) -> adsk.core.Vector3D:
    start_point = edge.startVertex.geometry
    point: adsk.core.Point3D = None
    for e in face.edges:
        if e == edge:
            continue
        if edge.startVertex.geometry.isEqualTo(e.startVertex.geometry):
            point = e.endVertex.geometry
            break
        if edge.startVertex.geometry.isEqualTo(e.endVertex.geometry):
            point = e.startVertex.geometry
            break
    edge_dir = start_point.vectorTo(edge.endVertex.geometry)
    edge_dir.normalize()
    diff = start_point.vectorTo(point)
    projection = edge_dir.dotProduct(diff)
    normal = diff
    v = edge_dir.copy()
    v.scaleBy(projection)
    normal.subtract(v)
    normal.normalize()
    return normal

def distance_along_normal_between_faces(face1: adsk.fusion.BRepFace, face2: adsk.fusion.BRepFace) -> float:
    if not is_parallel(face1, face2):
        raise ValueError("Only works for parallel faces")
    dir = face1.geometry.origin.vectorTo(face2.geometry.origin)
    return face1.geometry.normal.dotProduct(dir)

def normal_towards_face(from_face: adsk.fusion.BRepFace, to_face: adsk.fusion.BRepFace) -> adsk.core.Vector3D:
    normal: adsk.core.Vector3D = from_face.geometry.normal.copy()
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

    opposite_face = None
    for f in face.body.faces:
        if f != face and is_parallel(face, f):
            opposite_face = f
            break
    return opposite_face

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

def get_base_feature(custom_feature: adsk.fusion.CustomFeature) -> adsk.fusion.BaseFeature:
    for feature in custom_feature.features:
        if feature.objectType == adsk.fusion.BaseFeature.classType():
            return feature

def face_contains_edge(face: adsk.fusion.BRepFace, edge: adsk.fusion.BRepEdge) -> bool:
    # Only deal with planar faces
    if not is_planar(face):
        return False

    return face.boundingBox.contains(edge.startVertex.geometry) and face.boundingBox.contains(edge.endVertex.geometry)

def traverse_occurrence_tree(occurence: adsk.fusion.Occurrence, process: Callable[[adsk.fusion.Occurrence], bool]):
    def search_down(occ: adsk.fusion.Occurrence) -> bool:
        # Search this component first
        if process(occ):
            return True

        # Recurse into children (occurrences)
        for occ in occ.childOccurrences:
            if search_down(occ):
                return True

        return False

    current = occurence
    while current:
        # 1. Search current + children
        if search_down(current):
            return 

        # 2. Move up to parent
        occ_ctx = current.assemblyContext
        if not occ_ctx:
            break  # at root
        parent = occ_ctx

        # 3. Search siblings in parent
        for sibling_occ in parent.childOccurrences:
            if sibling_occ == current:
                continue
            if search_down(sibling_occ):
                return

        current = parent

    return None

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

    traverse_occurrence_tree(occ, search_occurrence)
    return result

def coordinates_at_point_on_face(point: adsk.core.Point2D, face: adsk.fusion.BRepFace, edge: adsk.fusion.BRepEdge) -> adsk.core.Matrix3D:
    edge_dir = edge.startVertex.geometry.vectorTo(edge.endVertex.geometry)
    edge_dir.normalize()
    y = normal_into_face(edge, face)
    z = normal_towards_face(face, get_opposite_face(face))
    origin: adsk.core.Vector3D = edge.startVertex.geometry.asVector()
    x_offset = edge_dir.copy()
    x_offset.scaleBy(point.x)
    y_offset = y.copy()
    y_offset.scaleBy(point.y)
    origin.add(x_offset)
    origin.add(y_offset)
    matrix = adsk.core.Matrix3D.create()
    matrix.setWithCoordinateSystem(origin.asPoint(), edge_dir, y, z)
    return matrix

def create_bodies_at_points_on_face(points: list[adsk.core.Point2D], face: adsk.fusion.BRepFace, edge: adsk.fusion.BRepEdge, create_body: Callable[[], adsk.fusion.BRepBody]) -> list[adsk.fusion.BRepBody]:
    mgr: adsk.fusion.TemporaryBRepManager = adsk.fusion.TemporaryBRepManager.get()
    result = []
    for point in points:
        b = create_body()
        matrix = coordinates_at_point_on_face(point, face, edge)
        mgr.transform(b, matrix)
        result.append(b)
    return result
