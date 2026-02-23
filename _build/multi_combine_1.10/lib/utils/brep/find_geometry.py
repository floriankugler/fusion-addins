import math
from typing import Callable
from . import relationships as rel, normals as norm, properties as prop
from .. import fusion, misc, vector
import adsk.core, adsk.fusion
from functools import singledispatch

def adjecent_edge(edge: adsk.fusion.BRepEdge, face: adsk.fusion.BRepFace) -> adsk.fusion.BRepEdge:
    loop = next((l for l in face.loops if l.isOuter), None)
    if loop is None:
        raise ValueError("Face has no outer loop.")
    edges = fusion.as_list(loop.edges)
    if not edges:
        raise ValueError("Outer loop has no edges.")
    if edge not in edges:
        raise ValueError("Edge is not part of face outer loop.")
    edge_idx = edges.index(edge)
    return loop.edges[edge_idx + 1] if edge_idx < len(loop.edges) - 1 else loop.edges[0]


def get_opposite_face(face: adsk.fusion.BRepFace) -> adsk.fusion.BRepFace:
    if not rel.is_planar(face): 
        raise ValueError("Face must be planar.")

    faces = []
    for f in face.body.faces:
        if f != face and rel.is_parallel(face, f):
            faces.append(f)
    if not faces:
        raise ValueError("No opposite parallel face found.")
    faces.sort(key=lambda x: x.area)
    return faces[-1]

def largest_face_of_edge(edge: adsk.fusion.BRepEdge) -> adsk.fusion.BRepFace | None:
    first_idx = next((idx for idx, face in enumerate(edge.faces) if rel.is_planar(face)), None)
    if first_idx is None:
        return None
    face: adsk.fusion.BRepFace = edge.faces.item(first_idx)
    for idx in range(first_idx + 1, edge.faces.count):
        new_face = edge.faces.item(idx)
        if rel.is_planar(new_face) and new_face.area > face.area:
            face = new_face
    return face

def largest_face_of_body(body: adsk.fusion.BRepBody) -> adsk.fusion.BRepFace:
    planar_faces = [f for f in body.faces if rel.is_planar(f)]
    if not planar_faces:
        raise ValueError("Body has no planar faces.")
    planar_faces.sort(key=lambda f: f.area, reverse=True)
    return planar_faces[0]


def find_perpendicular_face(reference_face: adsk.fusion.BRepFace, condition: Callable[[adsk.fusion.BRepFace], bool] = lambda _: True) -> adsk.fusion.BRepFace | None:
    if not rel.is_planar(reference_face):
        raise ValueError("Only works with planar reference face")
    
    result = None

    def search(o: adsk.fusion.Occurrence | adsk.fusion.Component) -> bool:
        for body in o.bRepBodies:
            if body == reference_face.body:
                continue
            for face in body.faces:
                if rel.is_perpendicular(face, reference_face) and condition(face):
                    nonlocal result
                    result = face
                    return True
        return False

    fusion.traverse_occurrence_tree(reference_face.body.assemblyContext, search)
    return result

def find_perpendicular_face_containing_edge(edge: adsk.fusion.BRepEdge, reference_face: adsk.fusion.BRepFace, condition: Callable[[adsk.fusion.BRepFace], bool] = lambda _: True) -> adsk.fusion.BRepFace | None:
    if not rel.is_linear(edge):
        raise ValueError("Only works on linear edges")
    return find_perpendicular_face(reference_face, lambda f: rel.face_contains_edge(f, edge) and condition(f))

def surface_and_rim_faces_for_edge(edge: adsk.fusion.BRepEdge) -> tuple[adsk.fusion.BRepFace, adsk.fusion.BRepFace] | None:
    surface_face = largest_face_of_edge(edge)
    if not surface_face: return None
    for f in edge.faces:
        if f != surface_face and rel.is_planar(f):
            return surface_face, f
    return None

def find_mating_faces_at_edge(edge: adsk.fusion.BRepEdge) -> tuple[adsk.fusion.BRepFace, adsk.fusion.BRepFace, adsk.fusion.BRepFace] | None:
    surface_and_rim = surface_and_rim_faces_for_edge(edge)
    if not surface_and_rim:
        return None
    surface, rim = surface_and_rim[0:2]

    rim_normal = norm.normal_into_face(edge, rim)
    edge_normal = norm.normal_along_edge(edge)
    step = vector.scaled_by(edge_normal, 5)
    start = vector.add(edge.startVertex.geometry.asVector(), vector.scaled_by(rim_normal, 0.1))
    test_points = [vector.add(start, vector.scaled_by(step, x)).asPoint() for x in misc.float_range(0, math.floor(edge.length), edge.length / 10)]

    def check_face(face: adsk.fusion.BRepFace):
        for t in test_points:
            _, param = face.evaluator.getParameterAtPoint(t)
            if face.evaluator.isParameterOnFace(param):
                return True
        return False

    other_face = find_perpendicular_face_containing_edge(edge, surface, check_face)
    if not other_face:
        return None
    return surface, rim, other_face

def find_carcass_edge_for_front_edge(front_edge: adsk.fusion.BRepEdge, front_face: adsk.fusion.BRepFace) -> adsk.fusion.BRepEdge | None:
    normal_into_door_face = norm.normal_into_face(front_edge, front_face)
    _, door_edge_center = front_edge.geometry.evaluator.getPointAtParameter(0.5)

    carcass_edge: adsk.fusion.BRepEdge | None = None
    def check_face(face: adsk.fusion.BRepFace) -> bool:
        nonlocal carcass_edge
        
        # Check whether the face has the right orientation
        normal_into_carcass_body = norm.normal_towards_face(face, get_opposite_face(face))
        if not vector.is_opposite_direction(normal_into_door_face, normal_into_carcass_body):
            return False
        
        # Check whether the center point of the door edge is within the bounds of the carcass edge
        edge = closest_parallel_edge_of_face(front_edge, face)
        if not edge:
            return False
        _, lower, upper = edge.geometry.evaluator.getParameterExtents()
        _, param = edge.geometry.evaluator.getParameterAtPoint(door_edge_center)
        if param <= lower or param >= upper:
            return False

        # Check whether the carcass edge lies within a reasonable distance from the door edge
        normal_into_carcass_face = norm.normal_into_face(edge, face)
        delta = vector.subtract(front_edge.startVertex.geometry.asVector(), edge.startVertex.geometry.asVector())
        distance_along_door = normal_into_door_face.dotProduct(delta)
        distance_along_carcass = normal_into_carcass_face.dotProduct(delta)
        carcass_thickness = prop.get_board_thickness(face)
        if distance_along_carcass < 0: # we have an overlay front
            if distance_along_door < -carcass_thickness or distance_along_door > 0:
                return False
        else: # we have an inset front
            if distance_along_door < 0 or distance_along_door > 0.6:
                return False

        carcass_edge = edge
        return True

    find_perpendicular_face(front_face, check_face)
    return carcass_edge

def longest_and_adjecent_edge_of_face(face: adsk.fusion.BRepFace) -> tuple[adsk.fusion.BRepEdge, adsk.fusion.BRepEdge]:
    loop = next((l for l in face.loops if l.isOuter), None)
    if loop is None:
        raise ValueError("Face has no outer loop.")
    outer_edges = fusion.as_list(loop.edges)
    if not outer_edges:
        raise ValueError("Face outer loop has no edges.")
    longest_edge = sorted(outer_edges, key=lambda e: e.length, reverse=True)[0]
    next_edge = adjecent_edge(longest_edge, face)
    return (longest_edge, next_edge)

def outer_edges_of_face(face: adsk.fusion.BRepFace) -> list[adsk.fusion.BRepEdge]:
    loop = next((x for x in face.loops if x.isOuter), None)
    if loop is None:
        raise ValueError("Face has no outer loop.")
    return fusion.as_list(loop.edges)

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
    if not edges:
        raise ValueError("edges must not be empty")
    faces = [fusion.as_list(edge.faces) for edge in edges]
    result = faces[0]
    for x in faces[1:]:
        result = misc.intersect_lists(result, x)
    if not result:
        raise ValueError("Edges do not share a common face.")
    return result[0]

def common_face_of_vertices(vertices: list[adsk.fusion.BRepVertex]) -> adsk.fusion.BRepFace:
    if not vertices:
        raise ValueError("vertices must not be empty")
    faces = [fusion.as_list(v.faces) for v in vertices]
    result = faces[0]
    for x in faces[1:]:
        result = misc.intersect_lists(result, x)
    if not result:
        raise ValueError("Vertices do not share a common face.")
    return result[0]

def closest_parallel_edge_of_face(edge: adsk.fusion.BRepEdge, face: adsk.fusion.BRepFace) -> adsk.fusion.BRepEdge | None:
    face_edges = outer_edges_of_face(face)
    parallel_edges = [e for e in face_edges if rel.is_parallel(edge, e)]
    if not parallel_edges:
        return None
    face_normal = norm.normal_into_face(parallel_edges[0], face)
    distance = float('inf')
    reference = edge.startVertex.geometry.asVector()
    result: adsk.fusion.BRepEdge | None = None
    for e in parallel_edges:
        new_distance = abs(face_normal.dotProduct(vector.subtract(e.startVertex.geometry.asVector(), reference)))
        if new_distance < distance:
            distance = new_distance
            result = e
    if result is None:
        raise ValueError("Failed to determine closest parallel edge.")
    return result
