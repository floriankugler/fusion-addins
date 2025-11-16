import sys, os

current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
shared_folder = os.path.join(parent_dir, "SharedUtils")
if current_dir not in sys.path: sys.path.append(current_dir)
if shared_folder not in sys.path: sys.path.append(shared_folder)
import importlib, CustomComputeFeature, Inputs, utils
importlib.reload(CustomComputeFeature)
importlib.reload(Inputs)
importlib.reload(utils)
import adsk.core, adsk.fusion
from adsk.core import Point3D, Vector3D
from typing import Callable
import math

_feature: CustomComputeFeature.CustomComputeFeature = None

def run(context):
    global _feature
    _feature = ConcealedHingeFeature()

def stop(context):
    global _feature
    del _feature

class ConcealedHingeInputs(Inputs.Inputs):
    types = {
        'Blum CLIP top 110 Thin': 0,
    }

    def __init__(self, units_manager: adsk.core.UnitsManager):
        units = units_manager.defaultLengthUnits
        self.edge = Inputs.SelectionByEntityTokenInput('edge', 'Carcass edge', 'LinearEdges', 1, 1, 'Select edge of carcass.')
        self.face = Inputs.SelectionByEntityTokenInput('face', 'Door face', 'PlanarFaces', 1, 1, 'Select the inner face of the door.')
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
        edge: adsk.fusion.BRepEdge = self.inputs.edge.value[0]
        door_face: adsk.fusion.BRepFace = self.inputs.face.value[0]
        positions = self.hinge_positions(edge, door_face)
        carcass_geometry = self.carcass_holes(edge, door_face, positions)
        door_geometry = self.door_holes(edge, door_face, positions)
        return [
            CustomComputeFeature.Combine(edge.body, carcass_geometry, adsk.fusion.FeatureOperations.CutFeatureOperation),
            CustomComputeFeature.Combine(door_face.body, door_geometry, adsk.fusion.FeatureOperations.CutFeatureOperation),
        ]
    
    def input_changed(self, input):
        if self.inputs.edge.input == input and self.inputs.edge.value and not self.inputs.face.value:
            self.inputs.face.input.hasFocus = True

    def hinge_positions(self, edge: adsk.fusion.BRepEdge, face: adsk.fusion.BRepFace) -> list[Vector3D]:
        door_long_edge, _ = utils.brep.longest_and_adjecent_edge_of_face(face)
        start_point = utils.brep.project_point_onto_edge(door_long_edge.startVertex.geometry, edge)
        end_point = utils.brep.project_point_onto_edge(door_long_edge.endVertex.geometry, edge)
        dir = utils.vector.subtract(end_point.asVector(), start_point.asVector())
        offset = self.inputs.offset.value
        return utils.vector.compute_points_along_vector(start_point, dir, [offset, dir.length - offset])

    def carcass_holes(self, edge: adsk.fusion.BRepEdge, face: adsk.fusion.BRepFace, positions: list[Vector3D]) -> adsk.fusion.BRepBody:
        point_on_face = utils.brep.project_point_onto_face(positions[0].asPoint(), face)
        gap = utils.vector.subtract(point_on_face.asVector(), positions[0]).length
        carcass_face = utils.brep.largest_face_of_edge(edge)

        cyl = utils.brep.cylinder(Point3D.create(0, 3.7 - (gap - 0.15)), self.inputs.predrill_diameter.value/2, -self.inputs.predrill_depth.value)
        group = utils.brep.union([
            utils.brep.transformed(cyl, utils.matrix.translation_matrix(Vector3D.create(-1.6, 0, 0))),
            utils.brep.transformed(cyl, utils.matrix.translation_matrix(Vector3D.create(1.6, 0, 0)))
        ])
        return utils.brep.place_body_on_face_at_positions(group, carcass_face, edge, positions)

    def door_holes(self, edge: adsk.fusion.BRepEdge, face: adsk.fusion.BRepFace, positions: list[Vector3D]) -> adsk.fusion.BRepBody:
        hinge_edge, distance = utils.brep.closest_parallel_edge_of_face(edge, face)

        cyl = utils.brep.cylinder(Point3D.create(0, distance + 2.7, 0), 0.5, -0.6)
        group = utils.brep.union([
            utils.brep.transformed(cyl, utils.matrix.translation_matrix(Vector3D.create(-1.6, 0, 0))),
            utils.brep.transformed(cyl, utils.matrix.translation_matrix(Vector3D.create(1.6, 0, 0)))
        ])
        return utils.brep.place_body_on_face_at_positions(group, face, hinge_edge, positions)
    
