from lib import custom_compute_feature, inputs, combine, utils, lamello, errors, ui_placement
from lib.fusionbootstrap.runtime import RuntimeInfo
import adsk.core, adsk.fusion
from typing import cast
import math

_feature: custom_compute_feature.CustomComputeFeature

def run(context, runtime_info: RuntimeInfo):
    global _feature
    _feature = SheetGoodTenons(runtime_info)

def stop(context):
    global _feature
    del _feature

class SheetGoodTenonsInputs(inputs.Inputs):
    class DistanceType:
        MINIMUM = inputs.DropDownInput.Item('Minimum distance', 1)
        MAXIMUM = inputs.DropDownInput.Item('Maximum distance', 2)
        NUMBER_OF_TENONS = inputs.DropDownInput.Item('Number of tenons', 3)
        RELATIVE = inputs.DropDownInput.Item('Relative', 4)
        POINTS = inputs.DropDownInput.Item('Points', 5)

    class ConnectorType:
        NONE = inputs.DropDownInput.Item('None', 1)
        SCREW = inputs.DropDownInput.Item('Screw', 2)
        CLAMEX = inputs.DropDownInput.Item('Clamex', 3)
        CABINEO = inputs.DropDownInput.Item('Cabineo', 4)

    class ScrewType:
        NONE = inputs.DropDownInput.Item('None', 1)
        CENTERED = inputs.DropDownInput.Item('Centered', 2)
        TWO_SIDES = inputs.DropDownInput.Item('Two sides', 3)

    class ClamexType:
        CLAMEX_P10 = inputs.DropDownInput.Item('Clamex P10', lamello.Type.CLAMEX_P10.value)
        CLAMEX_P14 = inputs.DropDownInput.Item('Clamex P14', lamello.Type.CLAMEX_P14.value)

    class CabineoType:
        CABINEO_8 = inputs.DropDownInput.Item('Cabineo 8', lamello.Type.CABINEO_8.value)
        CABINEO_12 = inputs.DropDownInput.Item('Cabineo 12', lamello.Type.CABINEO_12.value)
        CABINEO_8_M6 = inputs.DropDownInput.Item('Cabineo 8 M6', lamello.Type.CABINEO_8_M6.value)

    class CabineoSurfaceTypes:
        NONE = inputs.DropDownInput.Item('None', lamello.Params.CabineoSurface.NONE.value)
        FLUSH = inputs.DropDownInput.Item('Flush', lamello.Params.CabineoSurface.FLUSH.value)
        ANTI_BREAK = inputs.DropDownInput.Item('Anti-Break', lamello.Params.CabineoSurface.ANTI_BREAK.value)

    class CabineoInsertType:
        M6x123 = inputs.DropDownInput.Item('M6x12.3', lamello.Insert.M6x123.value)
        M6x153 = inputs.DropDownInput.Item('M6x15.3', lamello.Insert.M6x153.value)
        THREADED_INSERT = inputs.DropDownInput.Item('Threaded Insert', lamello.Insert.THREADED_INSERT.value)

    def __init__(self, units_manager: adsk.core.UnitsManager):
        units = units_manager.defaultLengthUnits
        self.edges = inputs.SelectionByEntityTokenInput('edges', 'Edges', ['LinearEdges'], 1, 0, 'Select edges along which tenons should be placed.')
        
        self.distance_type = inputs.DropDownInput('distanceType', 'Distance', utils.misc.class_property_values(SheetGoodTenonsInputs.DistanceType, inputs.DropDownInput.Item), SheetGoodTenonsInputs.DistanceType.MINIMUM.value, 'Method for determining tenon placement along the edge.')
        self.points = inputs.SelectionByEntityTokenInput('points', 'Points', ['SketchPoints'], 0, 0, 'Select points at which tenons should be placed', lambda: self.distance_type.value == self.DistanceType.POINTS.value)
        self.width = inputs.FloatInput('width', 'Tenon width', 5.0, 'Width of the tenons', units)
        self.spacing = inputs.FloatInput('spacing', 'Spacing', 20.0, 'Maximum spacing between tenons', units, lambda: self.distance_type.value in [self.DistanceType.MINIMUM.value, self.DistanceType.MAXIMUM.value])
        self.number_of_tenons = inputs.IntegerInput('numberOfTenons', 'Number of tenons', 3, 1, 100, 'Number of tenons to create along the edge', lambda: self.distance_type.value == self.DistanceType.NUMBER_OF_TENONS.value)
        self.relative_width = inputs.FloatInput('relativeWidth', 'Relative width', 1, 'Relation between the tenon width and the spacing between the tenons', '', lambda: self.distance_type.value == self.DistanceType.RELATIVE.value)
        self.distance_from_edge = inputs.FloatInput('distanceFromEdge', 'Distance from edge', 3.0, 'Distance of the first tenon from the edge', units, lambda: self.distance_type.value != self.DistanceType.POINTS.value)
        
        self.remaining_material = inputs.FloatInput('remainingMaterial', 'Remaining material', 0, 'Amount of material to keep on the mortise side', units)
        self.mortise_length_offset = inputs.FloatInput('mortiseLengthOffset', 'Mortise length offset', 0.01, 'Extension of the length of the mortise relative to the width of the tenon', units)
        self.mortise_width_offset = inputs.FloatInput('mortiseWidthOffset', 'Mortise width offset', 0.01, 'Extension of the width of the mortise relative to the thickness of the tenon', units)
        self.mortise_depth_offset = inputs.FloatInput('mortiseDepthOffset', 'Mortise depth offset', 0.05, 'Extension of the depth of the mortise relative to the length of the tenon', units)
        self.tool_diameter = inputs.FloatInput('toolDiameter', 'Tool diameter', 0.6, 'Diameter of the tool used to cut the mortise and tenon', units)   
        self.dog_bone_offset = inputs.FloatInput('dogBoneOffset', 'Dog bone offset', 0.01, 'Extra clearance to apply to dog bones', units)
        
        self.connector = inputs.DropDownInput('connector', 'Connector', utils.misc.class_property_values(self.ConnectorType, inputs.DropDownInput.Item), self.ConnectorType.NONE.value, 'Connectors used to fix the two boards')
        
        is_screw_connector = lambda: self.connector.value == self.ConnectorType.SCREW.value
        self.screw_diameter = inputs.FloatInput('screwDiameter', 'Screw diameter', 0.4, 'Diameter of the connector screw', units, is_screw_connector)
        self.mortise_screw = inputs.DropDownInput('mortiseScrew', 'Mortise screw', utils.misc.class_property_values(self.ScrewType, inputs.DropDownInput.Item), self.ScrewType.CENTERED.value, 'Type of screw placement in the mortise board', is_screw_connector)
        self.tenon_screw = inputs.DropDownInput('tenonScrew', 'Tenon screw', utils.misc.class_property_values(self.ScrewType, inputs.DropDownInput.Item), self.ScrewType.NONE.value, 'Type of screw placement in the tenon board', is_screw_connector)
        self.screw_offset = inputs.FloatInput('screwOffset', 'Screw offset', 1.2, 'Offset of the connector screw to the tenon', units, lambda: is_screw_connector() and (self.mortise_screw.value == self.ScrewType.TWO_SIDES.value or self.tenon_screw.value == self.ScrewType.TWO_SIDES.value))

        is_clamex_connector = lambda: self.connector.value == self.ConnectorType.CLAMEX.value
        self.clamex = inputs.DropDownInput('clamex', 'Clamex type', utils.misc.class_property_values(self.ClamexType, inputs.DropDownInput.Item), self.ClamexType.CLAMEX_P10.value, 'Type of Clamex connector', is_clamex_connector)    

        is_cabineo_connector = lambda: self.connector.value == self.ConnectorType.CABINEO.value
        self.cabineo = inputs.DropDownInput('cabineo', 'Cabineo type', utils.misc.class_property_values(self.CabineoType, inputs.DropDownInput.Item), self.CabineoType.CABINEO_8.value, 'Type of Cabineo connector', is_cabineo_connector)    
        self.cabineo_surface = inputs.DropDownInput('cabineoSurface', 'Surface', utils.misc.class_property_values(self.CabineoSurfaceTypes, inputs.DropDownInput.Item), self.CabineoSurfaceTypes.NONE.value, 'Surface variant of the cabineo connector', is_cabineo_connector)
        self.lamello_through_hole = inputs.CheckboxInput('lamelloThroughHole', 'Through hole', False, 'Whether to cut through holes for clamex guide holes or cabineo screw holes', lambda: is_clamex_connector() or is_cabineo_connector())
        self.cabineo_insert = inputs.DropDownInput('cabineoInsert', 'Cabineo insert', utils.misc.class_property_values(self.CabineoInsertType, inputs.DropDownInput.Item), self.CabineoInsertType.M6x123.value, 'Type of Cabineo insert', lambda: is_cabineo_connector() and self.cabineo.value == self.CabineoType.CABINEO_8_M6.value)

        is_threaded_insert = lambda: is_cabineo_connector() and self.cabineo_insert.value == self.CabineoInsertType.THREADED_INSERT.value
        self.threaded_insert_core_diameter = inputs.FloatInput('threaded_insert_core_diameter', 'Core diameter', 0.79, 'Core diameter of the threaded insert', units, is_threaded_insert)
        self.threaded_insert_core_depth = inputs.FloatInput('threaded_insert_core_depth', 'Core depth', 1.27+0.08, 'Depth of the threaded insert from the surface', units, is_threaded_insert)
        self.threaded_insert_collar_diameter = inputs.FloatInput('threaded_insert_collar_diameter', 'Collar diameter', 1.27, 'Collar diameter of the threaded insert', units, is_threaded_insert)
        self.threaded_insert_collar_depth = inputs.FloatInput('threaded_insert_collar_depth', 'Collar depth', 0.08, 'Collar depth of the threaded insert', units, is_threaded_insert)        

        super().__init__()


class SheetGoodTenons(custom_compute_feature.CustomComputeFeature):
    inputs: SheetGoodTenonsInputs
    
    @property
    def plugin_name(self) -> str:
        return 'Sheet Good Tenons'

    @property
    def plugin_desc(self) -> str:
        return 'Creates tenons and mortises suitable for sheet good construction.'

    @property
    def plugin_tooltip(self) -> str:
        return 'Creates tenons and mortises suitable for sheet good construction.'
    
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

    def create_inputs(self) -> SheetGoodTenonsInputs:
        return SheetGoodTenonsInputs(self.app.activeProduct.unitsManager)

    def execute(self) -> list[combine.Combine]:
        combines: list[combine.Combine] = []
        edges = cast(list[adsk.fusion.BRepEdge], self.inputs.edges.value)
        for edge in edges:
            combines.extend(self.create_tenons_and_mortises_along_edge(edge))
        return combines
    
    def tenon_positions_along_edge(self, edge: adsk.fusion.BRepEdge) -> tuple[list[adsk.core.Vector3D], float]:
        normal = utils.brep.normal_along_edge(edge)
        tenon_width = self.inputs.width.value
        offset = self.inputs.distance_from_edge.value
        positions: list[adsk.core.Vector3D] = []
        
        if self.inputs.distance_type.value == SheetGoodTenonsInputs.DistanceType.POINTS.value:
            positions = [
                utils.brep.project_point_onto_edge(cast(adsk.fusion.SketchPoint, p).worldGeometry, edge).asVector()
                for p in self.inputs.points.value
            ]
            positions.sort(key=lambda v: utils.vector.subtract(v, edge.startVertex.geometry.asVector()).length)

        else:
            number_of_tenons: int
            if self.inputs.distance_type.value == SheetGoodTenonsInputs.DistanceType.NUMBER_OF_TENONS.value:
                number_of_tenons = self.inputs.number_of_tenons.value
            elif self.inputs.distance_type.value in [SheetGoodTenonsInputs.DistanceType.MINIMUM.value, SheetGoodTenonsInputs.DistanceType.MAXIMUM.value]:
                number = (edge.length - 2*offset - tenon_width) / (self.inputs.spacing.value + tenon_width)
                if self.inputs.distance_type.value == SheetGoodTenonsInputs.DistanceType.MINIMUM.value:
                    number_of_tenons = math.floor(number) + 1
                else:
                    number_of_tenons = math.ceil(number) + 1
            else: 
                available_length = edge.length - 2*offset
                number_of_tenons = math.ceil((available_length - tenon_width) / (tenon_width + tenon_width/self.inputs.relative_width.value))
                tenon_width = available_length / (number_of_tenons + (number_of_tenons - 1)/self.inputs.relative_width.value)
            
            if number_of_tenons > 1:
                distance_between_tenons = (edge.length - 2*offset - tenon_width) / (number_of_tenons - 1) if number_of_tenons > 1 else 0
                start = utils.vector.add(edge.startVertex.geometry.asVector(), utils.vector.scaled_by(normal, offset + tenon_width/2))
                positions = [utils.vector.add(start, utils.vector.scaled_by(normal, ix * distance_between_tenons)) for ix in range(number_of_tenons)]
            else:
                positions = [utils.brep.edge_middle_point(edge).asVector()]

        min_distance = 12.0 if self.inputs.connector.value == SheetGoodTenonsInputs.ConnectorType.CLAMEX.value else 4.0
        if self.inputs.connector.value in [SheetGoodTenonsInputs.ConnectorType.CLAMEX.value, SheetGoodTenonsInputs.ConnectorType.CABINEO.value]:
            if positions:
                first_distance = utils.vector.subtract(positions[0], edge.startVertex.geometry.asVector()).length - tenon_width/2
                last_distance = utils.vector.subtract(edge.endVertex.geometry.asVector(), positions[-1]).length - tenon_width/2
                if first_distance < min_distance or last_distance < min_distance:
                    raise errors.InvalidInputError(f"Distance from edge must be at least {min_distance} mm to fit the selected connector")
            if len(positions) > 1:
                distances = [
                    utils.vector.subtract(v2, v1).length - tenon_width
                    for (v1, v2) in zip(positions, positions[1:])
                ]
                if min(distances) < min_distance:
                    raise errors.InvalidInputError(f"Not enough space between the tenons for the selected connectors.")

        return positions, tenon_width
    
    def create_connectors(self, edge: adsk.fusion.BRepEdge, mating_faces: tuple[adsk.fusion.BRepFace, adsk.fusion.BRepFace, adsk.fusion.BRepFace], tenon_positions: list[adsk.core.Vector3D], tenon_width: float) -> list[combine.Combine]:
        tenon_board_face, tenon_face, mortise_face = mating_faces[0:3]
        result: list[combine.Combine] = []

        if self.inputs.connector.value == SheetGoodTenonsInputs.ConnectorType.SCREW.value:
            mortise_board_thickness = utils.brep.get_board_thickness(mortise_face)
            tenon_board_thickness = utils.brep.get_board_thickness(tenon_board_face)
            if self.inputs.mortise_screw.value != SheetGoodTenonsInputs.ScrewType.NONE.value:
                cyl = utils.brep.transformed(
                    utils.brep.cylinder(self.inputs.screw_diameter.value/2, mortise_board_thickness),
                    utils.matrix.translation_matrix(adsk.core.Vector3D.create(0, tenon_board_thickness/2, 0))
                )
                positions = tenon_positions
                if self.inputs.mortise_screw.value == SheetGoodTenonsInputs.ScrewType.TWO_SIDES.value:
                    left = adsk.core.Vector3D.create(tenon_width/2 + self.inputs.screw_offset.value, 0, 0)
                    right = left.copy()
                    right.x = -right.x
                    cyl = utils.brep.union([
                        utils.brep.transformed(cyl, utils.matrix.translation_matrix(left)),
                        utils.brep.transformed(cyl, utils.matrix.translation_matrix(right)),
                    ])
                else:
                    edge_normal = utils.brep.normal_along_edge(edge)
                    start_offset = (utils.vector.subtract(tenon_positions[0], edge.startVertex.geometry.asVector()).length - tenon_width/2)/2
                    end_offset = (utils.vector.subtract(edge.endVertex.geometry.asVector(), tenon_positions[-1]).length - tenon_width/2)/2
                    start_screw_position = utils.vector.add(edge.startVertex.geometry.asVector(), utils.vector.scaled_by(edge_normal, start_offset))
                    end_screw_position = utils.vector.add(edge.endVertex.geometry.asVector(), utils.vector.scaled_by(edge_normal, -end_offset))
                    positions = [start_screw_position] + [
                        utils.vector.average(pair[0], pair[1])
                        for pair in zip(tenon_positions, tenon_positions[1:])
                    ] + [end_screw_position]
                cut_body = utils.brep.place_body_on_face_at_positions(cyl, tenon_face, edge, positions)
                result = [combine.Combine(mortise_face.body, cut_body, combine.Operation.CUT)]
            if self.inputs.tenon_screw.value != SheetGoodTenonsInputs.ScrewType.NONE.value:
                cyl = utils.brep.transformed(
                    utils.brep.cylinder(self.inputs.screw_diameter.value/2, -tenon_board_thickness),
                    utils.matrix.translation_matrix(adsk.core.Vector3D.create(0, -mortise_board_thickness/2, 0))
                )
                positions = tenon_positions
                if self.inputs.tenon_screw.value == SheetGoodTenonsInputs.ScrewType.TWO_SIDES.value:
                    left = adsk.core.Vector3D.create(tenon_width/2 - self.inputs.screw_offset.value, 0, 0)
                    right = left.copy()
                    right.x = -right.x
                    cyl = utils.brep.union([
                        utils.brep.transformed(cyl, utils.matrix.translation_matrix(left)),
                        utils.brep.transformed(cyl, utils.matrix.translation_matrix(right)),
                    ])
                cut_body = utils.brep.place_body_on_face_at_positions(cyl, tenon_board_face, edge, positions)
                result.append(combine.Combine(tenon_board_face.body, cut_body, combine.Operation.CUT))

        elif self.inputs.connector.value in [SheetGoodTenonsInputs.ConnectorType.CLAMEX.value, SheetGoodTenonsInputs.ConnectorType.CABINEO.value]:
            half_tenon = utils.vector.scaled_by(utils.brep.normal_along_edge(edge), tenon_width/2)
            start_position = utils.vector.average(
                edge.startVertex.geometry.asVector(), 
                utils.vector.add(tenon_positions[0], utils.vector.inverted(half_tenon))
            )
            end_position = utils.vector.average(
                edge.endVertex.geometry.asVector(), 
                utils.vector.add(tenon_positions[-1], half_tenon)
            )
            positions = [start_position] + [
                utils.vector.average(pair[0], pair[1])
                for pair in zip(tenon_positions, tenon_positions[1:])
            ] + [end_position]
            params = lamello.Params(
                type=lamello.Type(self.inputs.clamex.value if self.inputs.connector.value == SheetGoodTenonsInputs.ConnectorType.CLAMEX.value else self.inputs.cabineo.value),
                insert=lamello.Insert(self.inputs.cabineo_insert.value) if self.inputs.cabineo.value == SheetGoodTenonsInputs.CabineoType.CABINEO_8_M6.value else None,
                threaded_insert=lamello.Params.ThreadedInsert(
                    core_diameter=self.inputs.threaded_insert_core_diameter.value,
                    core_depth=self.inputs.threaded_insert_core_depth.value,
                    collar_diameter=self.inputs.threaded_insert_collar_diameter.value,
                    collar_depth=self.inputs.threaded_insert_collar_depth.value
                ),
                cabineo_surface=lamello.Params.CabineoSurface(self.inputs.cabineo_surface.value),
                through=self.inputs.lamello_through_hole.value
            )
            access, guide = lamello.create_hole_bodies(positions, edge, tenon_board_face, tenon_face, mortise_face, params)
            result = [
                combine.Combine(tenon_board_face.body, access, combine.Operation.CUT),
                combine.Combine(mortise_face.body, guide, combine.Operation.CUT)
            ]
        else:
            pass
        return result
    
    def create_tenons_and_mortises_along_edge(self, edge: adsk.fusion.BRepEdge) -> list[combine.Combine]:
        mating_faces = utils.brep.find_mating_faces_at_edge(edge)
        if not mating_faces:
            return []
        tenon_board_face, tenon_face, mortise_face = mating_faces[0:3]
        positions, tenon_width = self.tenon_positions_along_edge(edge)
        if not positions:
            return []
        
        tenon_thickness = utils.brep.get_board_thickness(tenon_board_face)
        tenon_length = utils.brep.get_board_thickness(mortise_face) - self.inputs.remaining_material.value
        tenon = utils.brep.transformed(
            utils.brep.rectangle(tenon_width, tenon_length, tenon_thickness), 
            utils.matrix.translation_matrix(adsk.core.Vector3D.create(0, -tenon_length/2, -tenon_thickness))
        )

        mortise_length = tenon_width + self.inputs.mortise_length_offset.value
        mortise_width = tenon_thickness + self.inputs.mortise_width_offset.value
        mortise_depth = tenon_length + self.inputs.mortise_depth_offset.value
        mortise = utils.brep.transformed(
            utils.brep.rectangle(mortise_length, mortise_depth, mortise_width), 
            utils.matrix.translation_matrix(adsk.core.Vector3D.create(0, -mortise_depth/2, -(mortise_width-self.inputs.mortise_width_offset.value/2)))
        )
        
        tenons = utils.brep.place_body_on_face_at_positions(tenon, tenon_board_face, edge, positions)
        mortises = [utils.brep.place_body_on_face_at_position(mortise, tenon_board_face, edge, p) for p in positions]

        tenon_board = utils.brep.union([tenon_board_face.body, tenons])
        tenon_dog_bone_axis = utils.brep.normal_away_from_body(tenon_board_face)
        tenon_dog_bones = [
            cast(adsk.fusion.BRepBody, utils.brep.create_dogbone_for_edge(e, self.inputs.tool_diameter.value, self.inputs.dog_bone_offset.value, negative=False))
            for e in tenon_board.edges if utils.brep.is_linear(e) and
            utils.brep.normal_along_edge(e).isParallelTo(tenon_dog_bone_axis) and 
            tenons.pointContainment(e.startVertex.geometry) == adsk.fusion.PointContainment.PointOnPointContainment and 
            tenon_face.isPointOnFace(e.startVertex.geometry, 1e-6)
        ]

        mortise_dog_bone_axis = utils.brep.normal_away_from_body(mortise_face)
        mortise_dog_bones: list[adsk.fusion.BRepBody] = []
        for m in mortises:
            center = m.physicalProperties.centerOfMass.asVector()
            for e in m.edges:
                if not utils.brep.normal_along_edge(e).isParallelTo(mortise_dog_bone_axis):
                    continue
                test_point = utils.brep.edge_middle_point(e).asVector()
                test_point.add(utils.vector.scaled_by(utils.vector.normalized(utils.vector.subtract(test_point, center)), 0.1))
                if mortise_face.body.pointContainment(test_point.asPoint()) != adsk.fusion.PointContainment.PointInsidePointContainment:
                    continue
                dog_bone = cast(adsk.fusion.BRepBody, utils.brep.create_dogbone_for_edge(e, self.inputs.tool_diameter.value, self.inputs.dog_bone_offset.value, negative=True))
                mortise_dog_bones.append(dog_bone)

        mortises = utils.brep.union(mortises + mortise_dog_bones)
        
        result = [
            combine.Combine(tenon_board_face.body, tenons, combine.Operation.JOIN),
            combine.Combine(mortise_face.body, mortises, combine.Operation.CUT)
        ]
        if tenon_dog_bones:
            result.append(combine.Combine(tenon_board_face.body, utils.brep.union(tenon_dog_bones), combine.Operation.CUT))
        result += self.create_connectors(edge, mating_faces, positions, tenon_width)
        return result
            
