import sys, os
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
shared_folder = os.path.join(parent_dir, "SharedUtils")
if current_dir not in sys.path: sys.path.append(current_dir)
if shared_folder not in sys.path: sys.path.append(shared_folder)
import CustomComputeFeature, Inputs, Combine, utils
import adsk.core, adsk.fusion
from adsk.core import Vector3D
from typing import cast
import math
utils.misc.force_reload_modules('CustomComputeFeature', 'Inputs', 'Combine', 'utils')

_feature: CustomComputeFeature.CustomComputeFeature

def run(context):
    global _feature
    _feature = Dogbones()

def stop(context):
    global _feature
    del _feature

class DogbonesInputs(Inputs.Inputs):
    def __init__(self, units_manager: adsk.core.UnitsManager):
        units = units_manager.defaultLengthUnits
        self.entities = Inputs.SelectionByEntityTokenInput('entities', 'Edges/Faces', ['LinearEdges', 'PlanarFaces'], 1, 0, 'Select edge along which access holes should be placed.')
        self.diameter = Inputs.FloatInput('diameter', 'Tool diameter', 0.6, 'Diameter of the tool used to machine the contour', units)
        self.offset = Inputs.FloatInput('offset', 'Offset', 0.01, 'Additional clearing offset', units)
        super().__init__()


class Dogbones(CustomComputeFeature.CustomComputeFeature):
    plugin_id = 'antonDogbones'
    plugin_name = 'Dog Bones'
    plugin_desc = 'Creates dog bone cutouts for corners'
    plugin_tooltip = 'Creates dog bone cutouts for corners.'
    inputs: DogbonesInputs

    def create_inputs(self) -> DogbonesInputs:
        return DogbonesInputs(self.app.activeProduct.unitsManager)

    def execute(self) -> list[Combine.Combine]:
        combines: list[Combine.Combine] = []
        for ent in cast(list[adsk.fusion.BRepEdge | adsk.fusion.BRepFace], self.inputs.entities.value):
            dogbone_bodies = self.create_dogbone_bodies(ent)
            if dogbone_bodies:
                combines.append(Combine.Combine(ent.body, dogbone_bodies, Combine.Operation.CUT))
        return combines
    
    def create_dogbone_bodies(self, entity: adsk.fusion.BRepEdge | adsk.fusion.BRepFace) -> adsk.fusion.BRepBody | None:
        if isinstance(entity, adsk.fusion.BRepEdge):
            return self.create_dogbone_for_edge(entity)
        else:            
            return self.create_dogbones_for_face(entity)
        
    def create_dogbones_for_face(self, face: adsk.fusion.BRepFace) -> adsk.fusion.BRepBody | None:
        result: list[adsk.fusion.BRepBody] = []
        for vertex in utils.brep.vertices_of_face(face):
            for edge in vertex.edges:
                if utils.brep.is_perpendicular(edge, face):
                    bone = self.create_dogbone_for_edge(edge)
                    if bone:
                        result.append(bone)
        if result:
            return utils.brep.union(result)
    
    def create_dogbone_for_edge(self, edge: adsk.fusion.BRepEdge) -> adsk.fusion.BRepBody | None:
        dogbone_radius = self.inputs.diameter.value/2
        edge_normal = utils.brep.normal_along_edge(edge)
        f1 = edge.faces[0]
        f2 = edge.faces[1]
        n1 = utils.brep.normal_into_face(edge, f1)
        n2 = utils.brep.normal_into_face(edge, f2)
        center_dir = utils.vector.normalized(utils.vector.add(n1, n2))
        test_dir = utils.vector.scaled_by(center_dir, 0.001)
        edge_middle = utils.brep.edge_middle_point(edge).asVector()
        test_point = utils.vector.add(edge_middle, test_dir).asPoint()
        if edge.body.pointContainment(test_point) == adsk.fusion.PointContainment.PointOutsidePointContainment:
            cos_angle = n1.dotProduct(n2)
            if cos_angle > -1 and cos_angle < 1:
                angle = math.acos(cos_angle)
                min_radius = dogbone_radius / (math.sin(angle)) # Compute the minimum radius necessary to ensure the tool with the specified diameter can reach the corner
                radius = max(dogbone_radius, min_radius) 
                radius_extended = radius + self.inputs.offset.value
                cyl = utils.brep.transformed(utils.brep.cylinder(radius_extended, edge.length), utils.matrix.translation_matrix(Vector3D.create(0, 0, -edge.length/2)))
                dogbone_center = utils.vector.add(edge_middle, utils.vector.scaled_by(center_dir, radius)).asPoint()
                return utils.brep.transformed(cyl, utils.matrix.transform_from_root(dogbone_center, center_dir, edge_normal.crossProduct(center_dir)))

    def pre_select(self, input: adsk.core.SelectionCommandInput, selection: adsk.fusion.BRepEdge | adsk.fusion.BRepFace) -> bool:
        if input.id == self.inputs.entities.id:
            if isinstance(selection, adsk.fusion.BRepEdge):
                return selection.faces.count == 2
            elif isinstance(selection, adsk.fusion.BRepFace):
                return True
        else:
            return True
        

