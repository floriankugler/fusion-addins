from .. import vector
from . import relationships as rel, find_geometry as find
import adsk.fusion
from adsk.core import Point3D


def is_rectangular_face(face: adsk.fusion.BRepFace) -> bool:
    if not rel.is_planar(face) or face.loops.count != 1 or face.edges.count != 4:
        return False
    edges = [co.edge for co in face.loops[0].coEdges]
    return all(rel.is_perpendicular(e1, e2) for e1, e2 in zip(edges[:1], edges[1:]))

def edge_middle_point(edge: adsk.fusion.BRepEdge) -> Point3D:
    return vector.scaled_by(vector.add(edge.startVertex.geometry.asVector(), edge.endVertex.geometry.asVector()), 0.5).asPoint()

def get_board_thickness(face: adsk.fusion.BRepFace) -> float:
    if not rel.is_planar(face): 
        raise ValueError("Face must be planar.")

    opposite_face = find.get_opposite_face(face)
    if opposite_face is None:
        raise RuntimeError("No opposite planar face found.")

    return abs(rel.distance_along_normal_between_faces(face, opposite_face))
