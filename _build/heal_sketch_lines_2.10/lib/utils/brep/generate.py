import math
from typing import Callable
from . import normals as norm, transform as trans, relationships as rel, properties as prop
from .. import matrix, vector
import adsk.core, adsk.fusion
from adsk.core import OrientedBoundingBox3D, Point3D, Vector3D

def fillet_cut_body(point: Point3D, leg1: Vector3D, leg2: Vector3D, fillet_radius: float, cut: Vector3D) -> adsk.fusion.BRepBody:
    mgr = adsk.fusion.TemporaryBRepManager.get()
    leg1 = vector.normalized(leg1)
    leg2 = vector.normalized(leg2)
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
    cyl2.add(cut)
    cyl = mgr.createCylinderOrCone(cyl1.asPoint(), fillet_radius, cyl2.asPoint(), fillet_radius)
    cut_cyl1 = point.copy()
    cut_cyl2 = point.copy()
    cut_cyl2.translateBy(cut)
    cut_cyl = mgr.createCylinderOrCone(cut_cyl1, cylinder_leg_distance, cut_cyl2, cylinder_leg_distance)
    mgr.booleanOperation(cut_cyl, cyl, adsk.fusion.BooleanTypes.DifferenceBooleanType) # type: ignore
    return cut_cyl

# Creates an isosceles triangle in the xy plane. Base is along x, origin is at mid-base, thickness is in positive z.
def isosceles_triangle(width: float, height: float, thickness: float, fillet_radius: float = 0) -> adsk.fusion.BRepBody:
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
        fillet1 = fillet_cut_body(Point3D.create(width/2, 0, 0), Vector3D.create(-width/2, 0, 0), Vector3D.create(-width/2, height, 0), fillet_radius, Vector3D.create(0, 0, thickness))
        mgr.booleanOperation(box, fillet1, adsk.fusion.BooleanTypes.DifferenceBooleanType) # type: ignore
        fillet2 = fillet_cut_body(Point3D.create(0, height, 0), Vector3D.create(-width/2, -height, 0), Vector3D.create(width/2, -height, 0), fillet_radius, Vector3D.create(0, 0, thickness))
        mgr.booleanOperation(box, fillet2, adsk.fusion.BooleanTypes.DifferenceBooleanType) # type: ignore

    mgr.booleanOperation(box, trim_body, adsk.fusion.BooleanTypes.IntersectionBooleanType) # type: ignore
    box2 = mgr.copy(box)
    mgr.transform(box2, matrix.mirror_matrix(Point3D.create(), Vector3D.create(-1, 1, 1)))
    mgr.booleanOperation(box, box2, adsk.fusion.BooleanTypes.UnionBooleanType) # type: ignore
    return box

def rectangle(width: float, height: float, thickness: float) -> adsk.fusion.BRepBody:
    """
    Creates a rectangle in the xy plane. Width is along x, height along y, origin is at the center. Thickness is in positive z.
    """
    x = Vector3D.create(1, 0, 0)
    y = Vector3D.create(0, 1, 0)
    bb = OrientedBoundingBox3D.create(Point3D.create(0, 0, thickness/2), x, y, width, height, thickness)
    mgr = adsk.fusion.TemporaryBRepManager.get()
    return mgr.createBox(bb)

# Creates a rounded rectangle in the xy plane. Width is along x, height along y, origin is at the center. Thickness is in positive z.
def rounded_rectangle(width: float, height: float, thickness: float, fillet_radius: float = 0) -> adsk.fusion.BRepBody:
    mgr = adsk.fusion.TemporaryBRepManager.get()
    box = trans.union([
        rectangle(width - 2*fillet_radius, height, thickness),
        rectangle(width, height - 2*fillet_radius, thickness)
    ])
    if fillet_radius > 0:
        cyl = cylinder(fillet_radius, thickness)
        fillet_points = [
            Vector3D.create(-width/2+fillet_radius, height/2-fillet_radius, 0),
            Vector3D.create(width/2-fillet_radius, height/2-fillet_radius, 0),
            Vector3D.create(width/2-fillet_radius, -height/2+fillet_radius, 0),
            Vector3D.create(-width/2+fillet_radius, -height/2+fillet_radius, 0),
        ]
        for p in fillet_points:
            mgr.booleanOperation(box, trans.transformed(cyl, matrix.translation_matrix(p)), adsk.fusion.BooleanTypes.UnionBooleanType) # type: ignore
    return box

# Creates a rhombus, origin as at its center, width is along x, height along y. 
def rhombus(width: float, height: float, thickness: float, fillet_radius: float = 0) -> adsk.fusion.BRepBody:
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
    mgr.booleanOperation(box, box2, adsk.fusion.BooleanTypes.IntersectionBooleanType) # type: ignore
    if fillet_radius > 0:
        cut1 = fillet_cut_body(Point3D.create(0, height/2, -thickness/2), Vector3D.create(-width/2, -height/2, 0), Vector3D.create(width/2, -height/2, 0), fillet_radius, Vector3D.create(0, 0, thickness))    
        mgr.booleanOperation(box, cut1, adsk.fusion.BooleanTypes.DifferenceBooleanType) # type: ignore
        mgr.transform(cut1, matrix.mirror_matrix(Point3D.create(), Vector3D.create(1, -1, 1)))
        mgr.booleanOperation(box, cut1, adsk.fusion.BooleanTypes.DifferenceBooleanType) # type: ignore
        cut2 = fillet_cut_body(Point3D.create(-width/2, 0, -thickness/2), Vector3D.create(width/2, height/2, 0), Vector3D.create(width/2, -height/2, 0), fillet_radius, Vector3D.create(0, 0, thickness))
        mgr.booleanOperation(box, cut2, adsk.fusion.BooleanTypes.DifferenceBooleanType) # type: ignore
        mgr.transform(cut2, matrix.mirror_matrix(Point3D.create(), Vector3D.create(-1, 1, 1)))
        mgr.booleanOperation(box, cut2, adsk.fusion.BooleanTypes.DifferenceBooleanType) # type: ignore
    return box

# Creates a cylinder with the cylinder's lower circle's center at origin, height is positive z.
def cylinder(radius: float, height: float) -> adsk.fusion.BRepBody:
    mgr = adsk.fusion.TemporaryBRepManager.get()
    return mgr.createCylinderOrCone(Point3D.create(), radius, Point3D.create(0, 0, height), radius)
    
# Creates a slot with the length along x, thickness positive in z. Origin is at the center bottom of the first cylinder.
def slot(length: float, radius: float, thickness: float) -> adsk.fusion.BRepBody:
    mgr = adsk.fusion.TemporaryBRepManager.get()
    cyl1 = cylinder(radius, thickness)
    cyl1 = trans.transformed(cyl1, matrix.translation_matrix(Vector3D.create(-length/2, 0, -thickness/2)))
    cyl2 = trans.transformed(cyl1, matrix.translation_matrix(Vector3D.create(length, 0, 0)))
    box = mgr.createBox(adsk.core.OrientedBoundingBox3D.create(adsk.core.Point3D.create(), adsk.core.Vector3D.create(1, 0, 0), adsk.core.Vector3D.create(0, 1, 0), length, radius * 2, thickness ))
    mgr.booleanOperation(box, cyl1, adsk.fusion.BooleanTypes.UnionBooleanType) # type: ignore
    mgr.booleanOperation(box, cyl2, adsk.fusion.BooleanTypes.UnionBooleanType) # type: ignore
    mgr.transform(box, matrix.translation_matrix(Vector3D.create(length/2, 0, thickness/2)))
    return box

def body_definition(body: adsk.fusion.BRepBody, include_lump: Callable[[adsk.fusion.BRepLump], bool] = lambda _: True) -> adsk.fusion.BRepBodyDefinition:
    """
    Given a `body` create a `BRepBodyDefinition` for it.
    The body definition can be used to create a similar body with modifications.
    Source: https://github.com/EvilHacker/BoxJoint/blob/main/fusion_brep_util.py
    """
    bodyDefinition = adsk.fusion.BRepBodyDefinition.create()
    bodyDefinition.doFullHealing = False
    for lump in body.lumps:
        if not include_lump(lump):
            continue
        lumpDefinition = bodyDefinition.lumpDefinitions.add()
        for shell in lump.shells:
            shellDefinition = lumpDefinition.shellDefinitions.add()
            for face in shell.faces:
                faceDefinition = shellDefinition.faceDefinitions.add(
                    face.geometry, face.isParamReversed)
                for loop in face.loops:
                    loopDefinition = faceDefinition.loopDefinitions.add()
                    for coEdge in loop.coEdges:
                        edge = coEdge.edge
                        loopDefinition.bRepCoEdgeDefinitions.add(
                            bodyDefinition.createEdgeDefinitionByCurve(
                                bodyDefinition.createVertexDefinition(edge.startVertex.geometry),
                                bodyDefinition.createVertexDefinition(edge.endVertex.geometry),
                                edge.geometry),
                            coEdge.isParamReversed)
            wire = shell.wire
            if wire:
                wireDefinition = shellDefinition.wireDefinition
                for coEdge in wire.coEdges:
                    edge = coEdge.edge
                    wireDefinition.wireEdgeDefinitions.add(
                        bodyDefinition.createVertexDefinition(edge.startVertex.geometry),
                        bodyDefinition.createVertexDefinition(edge.endVertex.geometry),
                        edge.geometry)
    return bodyDefinition

def create_body_from_curves(curves: list[adsk.core.Curve3D], extrude: Vector3D) -> adsk.fusion.BRepBody:
    mgr = adsk.fusion.TemporaryBRepManager.get()
    start_wires, _ = mgr.createWireFromCurves(curves, False)
    if start_wires.wires.count == 0:
        raise ValueError("No wires generated from curves.")
    end_wires = trans.transformed(start_wires, matrix.translation_matrix(extrude))
    ruled_surface = mgr.createRuledSurface(start_wires.wires[0], end_wires.wires[0])
    for idx in range(1, start_wires.wires.count):
        ruled = mgr.createRuledSurface(start_wires.wires[idx], end_wires.wires[idx])
        mgr.booleanOperation(ruled_surface, ruled, adsk.fusion.BooleanTypes.UnionBooleanType) # type: ignore
    start_face_body = mgr.createFaceFromPlanarWires([start_wires])
    end_face_body = mgr.createFaceFromPlanarWires([end_wires])
    body = trans.union([ruled_surface, start_face_body, end_face_body])
    return body_definition(body).createBody()

def create_body_from_face(face: adsk.fusion.BRepFace, extrude: Vector3D) -> adsk.fusion.BRepBody:
    curves = [e.geometry for l in face.loops for e in l.edges]
    return create_body_from_curves(curves, extrude)

def create_body_from_profile(profile: adsk.fusion.Profile) -> adsk.fusion.BRepBody:
    sketch = profile.parentSketch
    return trans.transformed(profile.face.body, matrix.transform_from_root(sketch.origin, sketch.xDirection, sketch.yDirection))

def create_dogbone_for_edge(edge: adsk.fusion.BRepEdge, tool_diameter: float, offset: float, negative: bool = False) -> adsk.fusion.BRepBody | None:
    if not rel.is_linear(edge) or edge.faces.count != 2:
        return None
    dogbone_radius = tool_diameter/2
    edge_normal = norm.normal_along_edge(edge)
    f1 = edge.faces[0]
    f2 = edge.faces[1]
    n1 = norm.normal_into_face(edge, f1)
    n2 = norm.normal_into_face(edge, f2)
    center_dir = vector.normalized(vector.add(n1, n2))
    test_dir = vector.scaled_by(center_dir, 0.001)
    edge_middle = prop.edge_middle_point(edge).asVector()
    test_point = vector.add(edge_middle, test_dir).asPoint()
    expected_containment = adsk.fusion.PointContainment.PointInsidePointContainment if negative else adsk.fusion.PointContainment.PointOutsidePointContainment
    if edge.body.pointContainment(test_point) == expected_containment:
        cos_angle = n1.dotProduct(n2)
        if cos_angle > -1 and cos_angle < 1:
            angle = math.acos(cos_angle)
            min_radius = dogbone_radius / (math.sin(angle)) # Compute the minimum radius necessary to ensure the tool with the specified diameter can reach the corner
            radius = max(dogbone_radius, min_radius) 
            radius_extended = radius + offset
            cyl = trans.transformed(cylinder(radius_extended, edge.length), matrix.translation_matrix(Vector3D.create(0, 0, -edge.length/2)))
            dogbone_center = vector.add(edge_middle, vector.scaled_by(center_dir, radius)).asPoint()
            return trans.transformed(cyl, matrix.transform_from_root(dogbone_center, center_dir, edge_normal.crossProduct(center_dir)))
