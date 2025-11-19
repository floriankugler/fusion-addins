import sys, os
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
shared_folder = os.path.join(parent_dir, "SharedUtils")
if current_dir not in sys.path: sys.path.append(current_dir)
if shared_folder not in sys.path: sys.path.append(shared_folder)
import CustomComputeFeature, Inputs, utils
import adsk.core, adsk.fusion
from adsk.core import Point3D, Vector3D
utils.misc.force_reload_modules('CustomComputeFeature', 'Inputs', 'utils')

_feature: CustomComputeFeature.CustomComputeFeature = None

def run(context):
    global _feature
    _feature = ConcealedHingeFeature()

def stop(context):
    global _feature
    del _feature

class ConcealedHingeInputs(Inputs.Inputs):
    types = {
        'Blum CLIP top 110 Thin +0': 0,
        'Blum CLIP top 110 Thin +3': 1,
    }

    def __init__(self, units_manager: adsk.core.UnitsManager):
        units = units_manager.defaultLengthUnits
        self.door_edges = Inputs.SelectionByEntityTokenInput('edges', 'Door hinge edges', 'LinearEdges', 1, 0, 'Select the hinged edge of the doors.')
        self.type = Inputs.DropDownInput('type', 'Hinge type', self.types.items(), 0, 'The type of pattern to use.')
        self.offset = Inputs.FloatInput('offset', 'Offset', 6, 'Distance of the first connector from the start of the edge.', units) 
        self.offset.minimum_value = 2.7
        self.predrill_diameter = Inputs.FloatInput('predrillDiameter', 'Predrill Diameter', 2.54/8, 'Predrill diameter used for screw holes.', units) 
        self.predrill_depth = Inputs.FloatInput('predrillDepth', 'Predrill Depth', 0.3, 'Predrill depth used for screw holes.', units) 
        super().__init__()


class ConcealedHingeFeature(CustomComputeFeature.CustomComputeFeature):
    plugin_id = 'antonConcealedHinge'
    plugin_name = 'Concealed Hinge'
    plugin_desc = 'Holes for concealed hinges'
    plugin_tooltip = 'Positions holes for concealed hinges'
    inputs: ConcealedHingeInputs

    def create_inputs(self) -> ConcealedHingeInputs:
        return ConcealedHingeInputs(self.app.activeProduct.unitsManager)

    def execute(self) -> list[CustomComputeFeature.Combine]:
        result: list[CustomComputeFeature.Combine] = []
        for door_edge in self.inputs.door_edges.value:
            door_face = utils.brep.largest_face_of_edge(door_edge)
            carcass_edge = self.find_carcass_edge_and_door_face(door_edge, door_face)
            if not carcass_edge:
                return None
            positions = self.hinge_positions(carcass_edge, door_face)
            carcass_geometry = self.carcass_holes(carcass_edge, door_face, positions)
            door_geometry = self.door_holes(carcass_edge, door_face, positions)
            result.append(CustomComputeFeature.Combine(carcass_edge.body, carcass_geometry, adsk.fusion.FeatureOperations.CutFeatureOperation))
            result.append(CustomComputeFeature.Combine(door_face.body, door_geometry, adsk.fusion.FeatureOperations.CutFeatureOperation))
        return result
    
    def find_carcass_edge_and_door_face(self, door_edge: adsk.fusion.BRepEdge, door_face: adsk.fusion.BRepFace) -> adsk.fusion.BRepEdge:
        normal_into_door_face = utils.brep.normal_into_face(door_edge, door_face)
        _, door_edge_center = door_edge.geometry.evaluator.getPointAtParameter(0.5)

        carcass_edge: adsk.fusion.BRepEdge = None
        def check_face(face: adsk.fusion.BRepFace) -> bool:
            nonlocal carcass_edge
            
            # Check whether the face has the right orientation
            normal_into_carcass_body = utils.brep.normal_towards_face(face, utils.brep.get_opposite_face(face))
            if not utils.vector.is_opposite_direction(normal_into_door_face, normal_into_carcass_body):
                return False
            
            # Check whether the center point of the door edge is within the bounds of the carcass edge
            edge = utils.brep.closest_parallel_edge_of_face(door_edge, face)
            _, lower, upper = edge.geometry.evaluator.getParameterExtents()
            _, param = edge.geometry.evaluator.getParameterAtPoint(door_edge_center)
            if param <= lower or param >= upper:
                return False

            # Check whether the carcass edge lies within a reasonable distance from the door edge
            normal_into_carcass_face = utils.brep.normal_into_face(edge, face)
            delta = utils.vector.subtract(door_edge.startVertex.geometry.asVector(), edge.startVertex.geometry.asVector())
            distance_along_door = normal_into_door_face.dotProduct(delta)
            distance_along_carcass = normal_into_carcass_face.dotProduct(delta)
            carcass_thickness = utils.brep.get_board_thickness(face)
            if distance_along_carcass < 0: # we have an overlay front
                if distance_along_door < -carcass_thickness or distance_along_door > 0:
                    return False
            else: # we have an inset front
                if distance_along_door < 0 or distance_along_door > 0.6:
                    return False

            carcass_edge = edge
            return True

        utils.brep.find_perpendicular_face(door_face, check_face)
        return carcass_edge

    def hinge_positions(self, carcass_edge: adsk.fusion.BRepEdge, door_face: adsk.fusion.BRepFace) -> list[Vector3D]:
        door_edge = utils.brep.closest_parallel_edge_of_face(carcass_edge, door_face)
        start_point = utils.brep.project_point_onto_edge(door_edge.startVertex.geometry, carcass_edge)
        end_point = utils.brep.project_point_onto_edge(door_edge.endVertex.geometry, carcass_edge)
        dir = utils.vector.subtract(end_point.asVector(), start_point.asVector())
        offset = self.inputs.offset.value
        return utils.vector.compute_points_along_vector(start_point, dir, [offset, dir.length - offset])

    def carcass_holes(self, carcass_edge: adsk.fusion.BRepEdge, door_face: adsk.fusion.BRepFace, positions: list[Vector3D]) -> adsk.fusion.BRepBody:
        point_on_face = utils.brep.project_point_onto_face(positions[0].asPoint(), door_face)
        carcass_face = utils.brep.largest_face_of_edge(carcass_edge)
        normal_into_carcass_face = utils.brep.normal_into_face(carcass_edge, carcass_face)
        gap_vector = utils.vector.subtract(point_on_face.asVector(), positions[0])
        gap = - normal_into_carcass_face.dotProduct(gap_vector)

        cyl = utils.brep.cylinder(Point3D.create(0, 3.7 - (gap - 0.15)), self.inputs.predrill_diameter.value/2, -self.inputs.predrill_depth.value)
        group = utils.brep.union([
            utils.brep.transformed(cyl, utils.matrix.translation_matrix(Vector3D.create(-1.6, 0, 0))),
            utils.brep.transformed(cyl, utils.matrix.translation_matrix(Vector3D.create(1.6, 0, 0)))
        ])
        return utils.brep.place_body_on_face_at_positions(group, carcass_face, carcass_edge, positions)

    def door_holes(self, carcass_edge: adsk.fusion.BRepEdge, door_face: adsk.fusion.BRepFace, positions: list[Vector3D]) -> adsk.fusion.BRepBody:
        hinge_edge = utils.brep.closest_parallel_edge_of_face(carcass_edge, door_face)
        normal_into_door_face = utils.brep.normal_into_face(hinge_edge, door_face)
        distance_vector = utils.vector.subtract(hinge_edge.startVertex.geometry.asVector(), carcass_edge.startVertex.geometry.asVector())
        distance = - normal_into_door_face.dotProduct(distance_vector) 

        cyl: adsk.fusion.BRepBody
        match self.inputs.type.value:
            case 0:  # Blum CLIP top 110 Thin +0
                cyl = utils.brep.cylinder(Point3D.create(0, distance + 2.7, 0), 0.5, -0.5)
            case 1:  # Blum CLIP top 110 Thin +3
                cyl = utils.brep.cylinder(Point3D.create(0, distance + 3, 0), 0.5, -0.5)
        group = utils.brep.union([
            utils.brep.transformed(cyl, utils.matrix.translation_matrix(Vector3D.create(-1.6, 0, 0))),
            utils.brep.transformed(cyl, utils.matrix.translation_matrix(Vector3D.create(1.6, 0, 0)))
        ])
        return utils.brep.place_body_on_face_at_positions(group, door_face, hinge_edge, positions)
    
