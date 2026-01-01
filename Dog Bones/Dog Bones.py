import sys, os
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
shared_folder = os.path.join(parent_dir, "SharedUtils")
if current_dir not in sys.path: sys.path.append(current_dir)
if shared_folder not in sys.path: sys.path.append(shared_folder)
import CustomComputeFeature, Inputs, Combine, utils
import adsk.core, adsk.fusion
from typing import cast
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
            return utils.brep.create_dogbone_for_edge(entity, self.inputs.diameter.value, self.inputs.offset.value)
        else:            
            return self.create_dogbones_for_face(entity)
        
    def create_dogbones_for_face(self, face: adsk.fusion.BRepFace) -> adsk.fusion.BRepBody | None:
        result: list[adsk.fusion.BRepBody] = []
        largest_face = utils.brep.largest_face_of_body(face.body)
        edges_considered: list[adsk.fusion.BRepEdge] = []
        for vertex in utils.brep.vertices_of_face(face):
            for edge in vertex.edges:
                if edge in edges_considered:
                    continue
                edges_considered.append(edge)
                if utils.brep.is_perpendicular(edge, largest_face):
                    bone = utils.brep.create_dogbone_for_edge(edge, self.inputs.diameter.value, self.inputs.offset.value)
                    if bone:
                        result.append(bone)
        if result:
            return utils.brep.union(result)
        
    def pre_select(self, input: adsk.core.SelectionCommandInput, selection: adsk.fusion.BRepEdge | adsk.fusion.BRepFace) -> bool:
        if input.id == self.inputs.entities.id:
            if isinstance(selection, adsk.fusion.BRepEdge):
                return selection.faces.count == 2
            elif isinstance(selection, adsk.fusion.BRepFace):
                return True
        else:
            return True
        