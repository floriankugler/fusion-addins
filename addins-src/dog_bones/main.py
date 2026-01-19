from lib import custom_compute_feature, inputs, combine, utils, ui_placement
import adsk.core, adsk.fusion
from typing import cast

_feature: custom_compute_feature.CustomComputeFeature
def run(context):
    global _feature
    _feature = Dogbones()

def stop(context):
    global _feature
    del _feature

class DogbonesInputs(inputs.Inputs):
    def __init__(self, units_manager: adsk.core.UnitsManager):
        units = units_manager.defaultLengthUnits
        self.entities = inputs.SelectionByEntityTokenInput('entities', 'Edges/Faces', ['LinearEdges', 'PlanarFaces'], 1, 0, 'Select edges or faces to add dogbones to.')
        self.diameter = inputs.FloatInput('diameter', 'Tool diameter', 0.6, 'Diameter of the tool used to machine the contour', units)
        self.offset = inputs.FloatInput('offset', 'Offset', 0.01, 'Additional clearing offset', units)
        super().__init__()


class Dogbones(custom_compute_feature.CustomComputeFeature):
    plugin_name = 'Dog Bones'
    plugin_desc = 'Creates dog bone cutouts for corners'
    plugin_tooltip = 'Creates dog bone cutouts for corners.'
    inputs: DogbonesInputs
    
    def get_ui_placement(self) -> ui_placement.UIPlacement:
        section = ui_placement.PlacementSpec(
            id='SeparatorBeforeCustomAddins',
            anchor_id='FusionMoveCommand',
            insert_before=True,
        )
        command = ui_placement.PlacementSpec(
            id=self.create_command_id,
            anchor_id=section.id,
            insert_before=True,
        )
        return ui_placement.UIPlacement(
            panel_id='SolidModifyPanel',
            command=command,
            section=section,
        )

    def create_inputs(self) -> DogbonesInputs:
        return DogbonesInputs(self.app.activeProduct.unitsManager)

    def execute(self) -> list[combine.Combine]:
        combines: list[combine.Combine] = []
        for ent in cast(list[adsk.fusion.BRepEdge | adsk.fusion.BRepFace], self.inputs.entities.value):
            dogbone_bodies = self.create_dogbone_bodies(ent)
            if dogbone_bodies:
                combines.append(combine.Combine(ent.body, dogbone_bodies, combine.Operation.CUT))
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
                return False
        return True
        
