from lib import inputs, combine, custom_compute_feature, utils, lamello, ui_placement
from lib.fusionbootstrap.runtime import RuntimeInfo
import adsk.core, adsk.fusion
import math
from typing import cast

_feature: custom_compute_feature.CustomComputeFeature

def run(context, runtime_info: RuntimeInfo):
    global _feature
    _feature = LamelloFeature(runtime_info)

def stop(context):
    global _feature
    del _feature

class LamelloInputs(inputs.Inputs):
    class Types:
        CLAMEX_P10 = inputs.DropDownInput.Item('Clamex P10', lamello.Type.CLAMEX_P10.value)
        CLAMEX_P14 = inputs.DropDownInput.Item('Clamex P14', lamello.Type.CLAMEX_P14.value)
        CABINEO_8 = inputs.DropDownInput.Item('Cabineo 8', lamello.Type.CABINEO_8.value)
        CABINEO_12 = inputs.DropDownInput.Item('Cabineo 12', lamello.Type.CABINEO_12.value)
        CABINEO_8_M6 = inputs.DropDownInput.Item('Cabineo 8 M6', lamello.Type.CABINEO_8_M6.value)        

    class InsertTypes:
        M6x123 = inputs.DropDownInput.Item('M6x12.3', lamello.Insert.M6x123.value)
        M6x153 = inputs.DropDownInput.Item('M6x15.3', lamello.Insert.M6x153.value)
        THREADED_INSERT = inputs.DropDownInput.Item('Threaded Insert', lamello.Insert.THREADED_INSERT.value)

    class SurfaceTypes:
        NONE = inputs.DropDownInput.Item('None', lamello.Params.CabineoSurface.NONE.value)
        FLUSH = inputs.DropDownInput.Item('Flush', lamello.Params.CabineoSurface.FLUSH.value)
        ANTI_BREAK = inputs.DropDownInput.Item('Anti-Break', lamello.Params.CabineoSurface.ANTI_BREAK.value)

    class DistanceType:
        MINIMUM = inputs.DropDownInput.Item('Minimum distance', 1)
        MAXIMUM = inputs.DropDownInput.Item('Maximum distance', 2)
        NUMBER_OF_CONNECTORS = inputs.DropDownInput.Item('Number of connectors', 3)
        POINTS = inputs.DropDownInput.Item('Points', 5)


    def __init__(self, units_manager: adsk.core.UnitsManager):
        units = units_manager.defaultLengthUnits
        self.edge = inputs.SelectionByEntityTokenInput('edge', 'Edge', ['LinearEdges'], 1, 0, 'Select edge along which access holes should be placed.')
        self.size = inputs.DropDownInput('size', 'Variant', utils.misc.class_property_values(LamelloInputs.Types, inputs.DropDownInput.Item), LamelloInputs.Types.CLAMEX_P10.value, 'Variant of the Lamello connector.')
        
        self.distance_type = inputs.DropDownInput('distanceType', 'Distance', utils.misc.class_property_values(LamelloInputs.DistanceType, inputs.DropDownInput.Item), LamelloInputs.DistanceType.MINIMUM.value, 'Method for determining lamello placement along the edge.')
        self.points = inputs.SelectionByEntityTokenInput('points', 'Points', ['SketchPoints'], 0, 0, 'Select points at which connectors should be placed', lambda: self.distance_type.value == LamelloInputs.DistanceType.POINTS.value)
        self.spacing = inputs.FloatInput('spacing', 'Spacing', 20, 'Minimum spacing between the connectors.', units, lambda: self.distance_type.value not in [LamelloInputs.DistanceType.POINTS.value, LamelloInputs.DistanceType.NUMBER_OF_CONNECTORS.value])
        self.number_of_connectors = inputs.IntegerInput('numberOfConnectors', 'Number of connectors', 3, 1, 100, 'Number of connectors to place along the edge', lambda: self.distance_type.value == LamelloInputs.DistanceType.NUMBER_OF_CONNECTORS.value)
        self.offset = inputs.FloatInput('offset', 'Offset', 6, 'Distance of the first connector from the start of the edge.', units, lambda: self.distance_type.value != LamelloInputs.DistanceType.POINTS.value)

        is_cabineo = lambda: self.size.value in [LamelloInputs.Types.CABINEO_8.value, LamelloInputs.Types.CABINEO_12.value, LamelloInputs.Types.CABINEO_8_M6.value]
        self.through_guide_holes = inputs.CheckboxInput('throughGuideHoles', 'Through Holes', False, 'If checked the guide holes ae punched all the way through the board', lambda: not is_cabineo())
        
        self.cabineo_surface = inputs.DropDownInput('cabineoSurface', 'Surface', utils.misc.class_property_values(LamelloInputs.SurfaceTypes, inputs.DropDownInput.Item), LamelloInputs.SurfaceTypes.NONE.value, 'Surface variant of the cabineo connector', is_cabineo)
        self.cabineo_through_hole = inputs.CheckboxInput('cabineoThroughHole', 'Through Hole', False, 'If checked the Cabineo hole is punched all the way through to the opposite face.', is_cabineo)
        self.cabineo_insert_type = inputs.DropDownInput('insertType', 'Insert Type', utils.misc.class_property_values(LamelloInputs.InsertTypes, inputs.DropDownInput.Item), LamelloInputs.InsertTypes.THREADED_INSERT.value, 'Variant of the Cabineo insert.', lambda: self.size.value == lamello.Type.CABINEO_8_M6.value)
        is_threaded_insert = lambda: is_cabineo() and self.cabineo_insert_type.value == LamelloInputs.InsertTypes.THREADED_INSERT.value
        self.threaded_insert_core_diameter = inputs.FloatInput('threaded_insert_core_diameter', 'Core diameter', 0.79, 'Core diameter of the threaded insert', units, is_threaded_insert)
        self.threaded_insert_core_depth = inputs.FloatInput('threaded_insert_core_depth', 'Core depth', 1.27+0.08, 'Depth of the threaded insert from the surface', units, is_threaded_insert)
        self.threaded_insert_collar_diameter = inputs.FloatInput('threaded_insert_collar_diameter', 'Collar diameter', 1.27, 'Collar diameter of the threaded insert', units, is_threaded_insert)
        self.threaded_insert_collar_depth = inputs.FloatInput('threaded_insert_collar_depth', 'Collar depth', 0.08, 'Collar depth of the threaded insert', units, is_threaded_insert)
        super().__init__()


class LamelloFeature(custom_compute_feature.CustomComputeFeature):
    inputs: LamelloInputs
    
    @property
    def plugin_name(self) -> str:
        return 'Lamello'

    @property
    def plugin_desc(self) -> str:
        return 'Lamello connectors'

    @property
    def plugin_tooltip(self) -> str:
        return 'Adds access guide holes for Lamello connectors along an edge.'
    
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

    def create_inputs(self) -> LamelloInputs:
        return LamelloInputs(self.app.activeProduct.unitsManager)

    def execute(self) -> list[combine.Combine]:
        combines: list[combine.Combine] = []
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
                threaded_insert=lamello.Params.ThreadedInsert(
                    core_diameter=self.inputs.threaded_insert_core_diameter.value,
                    core_depth=self.inputs.threaded_insert_core_depth.value,
                    collar_diameter=self.inputs.threaded_insert_collar_diameter.value,
                    collar_depth=self.inputs.threaded_insert_collar_depth.value
                ),
                cabineo_surface=lamello.Params.CabineoSurface(self.inputs.cabineo_surface.value),
                through=self.inputs.cabineo_through_hole.value if type.is_cabineo else self.inputs.through_guide_holes.value
            )
            access_holes, guide_holes = lamello.create_hole_bodies(positions, edge, access_face, slot_face, guide_face, params)
            combines.append(combine.Combine(access_face.body, access_holes, combine.Operation.CUT))
            combines.append(combine.Combine(guide_face.body, guide_holes, combine.Operation.CUT))
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
        
