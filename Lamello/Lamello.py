import sys, os
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
shared_folder = os.path.join(parent_dir, "SharedUtils")
if current_dir not in sys.path: sys.path.append(current_dir)
if shared_folder not in sys.path: sys.path.append(shared_folder)
import CustomComputeFeature, Inputs, Combine, utils, lamello
import adsk.core, adsk.fusion
import math
from typing import cast
utils.misc.force_reload_modules('CustomComputeFeature', 'Inputs', 'Combine', 'utils', 'lamello')

_feature: CustomComputeFeature.CustomComputeFeature

def run(context):
    global _feature
    _feature = LamelloFeature()

def stop(context):
    global _feature
    del _feature

class LamelloInputs(Inputs.Inputs):
    class Types:
        CLAMEX_P10 = Inputs.DropDownInput.Item('Clamex P10', lamello.Type.CLAMEX_P10.value)
        CLAMEX_P14 = Inputs.DropDownInput.Item('Clamex P14', lamello.Type.CLAMEX_P14.value)
        CABINEO_8 = Inputs.DropDownInput.Item('Cabineo 8', lamello.Type.CABINEO_8.value)
        CABINEO_12 = Inputs.DropDownInput.Item('Cabineo 12', lamello.Type.CABINEO_12.value)
        CABINEO_8_M6 = Inputs.DropDownInput.Item('Cabineo 8 M6', lamello.Type.CABINEO_8_M6.value)        

    class InsertTypes:
        M6x123 = Inputs.DropDownInput.Item('M6x12.3', lamello.Insert.M6x123.value)
        M6x153 = Inputs.DropDownInput.Item('M6x15.3', lamello.Insert.M6x153.value)
        HAEFELE_MUFFE_10x8 = Inputs.DropDownInput.Item('Haefele Muffe 10x8', lamello.Insert.HAEFELE_EINDREHMUFFE_10x8.value)

    class DistanceType:
        MINIMUM = Inputs.DropDownInput.Item('Minimum distance', 1)
        MAXIMUM = Inputs.DropDownInput.Item('Maximum distance', 2)
        NUMBER_OF_CONNECTORS = Inputs.DropDownInput.Item('Number of connectors', 3)
        POINTS = Inputs.DropDownInput.Item('Points', 5)


    def __init__(self, units_manager: adsk.core.UnitsManager):
        units = units_manager.defaultLengthUnits
        self.edge = Inputs.SelectionByEntityTokenInput('edge', 'Edge', ['LinearEdges'], 1, 0, 'Select edge along which access holes should be placed.')
        self.size = Inputs.DropDownInput('size', 'Variant', utils.misc.class_property_values(LamelloInputs.Types, Inputs.DropDownInput.Item), LamelloInputs.Types.CLAMEX_P10.value, 'Variant of the Lamello connector.')
        
        self.distance_type = Inputs.DropDownInput('distanceType', 'Distance', utils.misc.class_property_values(LamelloInputs.DistanceType, Inputs.DropDownInput.Item), LamelloInputs.DistanceType.MINIMUM.value, 'Method for determining lamello placement along the edge.')
        self.points = Inputs.SelectionByEntityTokenInput('points', 'Points', ['SketchPoints'], 0, 0, 'Select points at which connectors should be placed', lambda: self.distance_type.value == LamelloInputs.DistanceType.POINTS.value)
        self.spacing = Inputs.FloatInput('spacing', 'Spacing', 20, 'Minimum spacing between the connectors.', units, lambda: self.distance_type.value not in [LamelloInputs.DistanceType.POINTS.value, LamelloInputs.DistanceType.NUMBER_OF_CONNECTORS.value])
        self.number_of_connectors = Inputs.IntegerInput('numberOfConnectors', 'Number of connectors', 3, 1, 100, 'Number of connectors to place along the edge', lambda: self.distance_type.value == LamelloInputs.DistanceType.NUMBER_OF_CONNECTORS.value)
        self.offset = Inputs.FloatInput('offset', 'Offset', 6, 'Distance of the first connector from the start of the edge.', units, lambda: self.distance_type.value != LamelloInputs.DistanceType.POINTS.value)

        is_cabineo = lambda: self.size.value in [LamelloInputs.Types.CABINEO_8.value, LamelloInputs.Types.CABINEO_12.value, LamelloInputs.Types.CABINEO_8_M6.value]
        self.through_guide_holes = Inputs.CheckboxInput('throughGuideHoles', 'Through Holes', False, 'If checked the guide holes ae punched all the way through the board', lambda: not is_cabineo())
        self.cabineo_flush = Inputs.CheckboxInput('cabineoFlush', 'Flush', False, 'Flush with the surface', is_cabineo)
        self.cabineo_through_hole = Inputs.CheckboxInput('cabineoThroughHole', 'Through Hole', False, 'If checked the Cabineo hole is punched all the way through to the opposite face.', is_cabineo)
        self.cabineo_insert_type = Inputs.DropDownInput('insertType', 'Insert Type', utils.misc.class_property_values(LamelloInputs.InsertTypes, Inputs.DropDownInput.Item), LamelloInputs.InsertTypes.M6x123.value, 'Variant of the Cabineo insert.', is_cabineo)
        super().__init__()


class LamelloFeature(CustomComputeFeature.CustomComputeFeature):
    plugin_id = 'antonLamello'
    plugin_name = 'Lamello'
    plugin_desc = 'Lamello connectors'
    plugin_tooltip = 'Adds access guide holes for Lamello connectors along an edge.'
    inputs: LamelloInputs

    def create_inputs(self) -> LamelloInputs:
        return LamelloInputs(self.app.activeProduct.unitsManager)

    def execute(self) -> list[Combine.Combine]:
        combines: list[Combine.Combine] = []
        for edge in cast(list[adsk.fusion.BRepEdge], self.inputs.edge.value):
            faces = utils.brep.find_mating_faces_at_edge(edge)
            if not faces:
                continue
            access_face, slot_face, guide_face = faces[0:3]

            positions: list[adsk.core.Vector3D]
            if len(self.inputs.points.value) > 0:
                positions = [cast(adsk.fusion.SketchPoint, p).worldGeometry.asVector() for p in self.inputs.points.value]
            else:
                positions = self.access_positions(edge)

            type = lamello.Type(self.inputs.size.value)
            params = lamello.Params(
                type=type,
                insert=lamello.Insert(self.inputs.cabineo_insert_type.value) if self.inputs.size.value == lamello.Type.CABINEO_8_M6.value else None,
                flush=self.inputs.cabineo_flush.value,
                through=self.inputs.cabineo_through_hole.value if type.is_cabineo else self.inputs.through_guide_holes.value
            )
            access_holes, guide_holes = lamello.create_hole_bodies(positions, edge, access_face, slot_face, guide_face, params)
            combines.append(Combine.Combine(access_face.body, access_holes, Combine.Operation.CUT))
            combines.append(Combine.Combine(guide_face.body, guide_holes, Combine.Operation.CUT))
        return combines
    
    def access_positions(self, edge: adsk.fusion.BRepEdge) -> list[adsk.core.Vector3D]:
        distance_type = self.inputs.distance_type.value
        positions: list[adsk.core.Vector3D] = []
        if distance_type == LamelloInputs.DistanceType.POINTS.value:
            positions = [cast(adsk.fusion.SketchPoint, p).worldGeometry.asVector() for p in self.inputs.points.value]
        else:
            offset = self.inputs.offset.value
            spacing = self.inputs.spacing.value
            available_length = edge.length - 2*offset
            number_of_connectors: int
            if distance_type == LamelloInputs.DistanceType.NUMBER_OF_CONNECTORS.value:
                number_of_connectors = self.inputs.number_of_connectors.value
            else:
                number_of_connectors = math.ceil(available_length/spacing)
                if distance_type == LamelloInputs.DistanceType.MAXIMUM.value:
                    number_of_connectors += 1
            if number_of_connectors > 0:
                edge_normal = utils.brep.normal_along_edge(edge)
                start = utils.vector.add(edge.startVertex.geometry.asVector(), utils.vector.scaled_by(edge_normal, offset if number_of_connectors > 1 else edge.length/2))
                computed_spacing = available_length / (number_of_connectors-1) if number_of_connectors > 1 else 0
                positions = [utils.vector.add(start, utils.vector.scaled_by(edge_normal, idx * computed_spacing)) for idx in range(number_of_connectors)]
        return positions

    def pre_select(self, input: adsk.core.SelectionCommandInput, selection: adsk.fusion.BRepEdge) -> bool:
        if input.id == self.inputs.edge.id:
            return utils.brep.find_mating_faces_at_edge(selection) is not None
        else:
            return True
        
