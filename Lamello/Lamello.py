import sys, os
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
shared_folder = os.path.join(parent_dir, "SharedUtils")
if current_dir not in sys.path: sys.path.append(current_dir)
if shared_folder not in sys.path: sys.path.append(shared_folder)
import CustomComputeFeature, Inputs, Combine, utils
import adsk.core, adsk.fusion
from adsk.core import Point3D, Vector3D
import math
from typing import cast, Optional
utils.misc.force_reload_modules('CustomComputeFeature', 'Inputs', 'Combine', 'utils')

_feature: CustomComputeFeature.CustomComputeFeature

def run(context):
    global _feature
    _feature = Lamello()

def stop(context):
    global _feature
    del _feature

class LamelloInputs(Inputs.Inputs):
    class Types:
        CLAMEX_P10 = Inputs.DropDownInput.Item('Clamex P10', 10)
        CLAMEX_P14 = Inputs.DropDownInput.Item('Clamex P14', 14)
        CABINEO_8 = Inputs.DropDownInput.Item('Cabineo 8', 8)
        CABINEO_12 = Inputs.DropDownInput.Item('Cabineo 12', 12)
        CABINEO_8_M6 = Inputs.DropDownInput.Item('Cabineo 8 M6', 9)        

    class InsertTypes:
        M6x123 = Inputs.DropDownInput.Item('M6x12.3', 123)
        M6x153 = Inputs.DropDownInput.Item('M6x15.3', 153)

    def __init__(self, units_manager: adsk.core.UnitsManager):
        units = units_manager.defaultLengthUnits
        self.edge = Inputs.SelectionByEntityTokenInput('edge', 'Edge', ['LinearEdges'], 1, 0, 'Select edge along which access holes should be placed.')
        self.points = Inputs.SelectionByEntityTokenInput('points', 'Points', ['SketchPoints'], 0, 0, 'To manually place the connectors, select sketch points.')
        self.size = Inputs.DropDownInput('size', 'Variant', utils.misc.class_property_values(LamelloInputs.Types, Inputs.DropDownInput.Item), LamelloInputs.Types.CLAMEX_P10.value, 'Variant of the Lamello connector.')
        self.spacing = Inputs.FloatInput('spacing', 'Spacing', 20, 'Minimum spacing between the connectors.', units)
        self.offset = Inputs.FloatInput('offset', 'Offset', 6, 'Distance of the first connector from the start of the edge.', units)
        self.through_guide_holes = Inputs.CheckboxInput('throughGuideHoles', 'Through Guide Holes', False, 'If checked the guide holes are punched all the way through to the opposite face.')
        self.cabineo_flush = Inputs.CheckboxInput('cabineoFlush', 'Flush', False, 'Flush with the surface')
        self.cabineo_through_hole = Inputs.CheckboxInput('cabineoThroughHole', 'Through Hole', False, 'If checked the Cabineo hole is punched all the way through to the opposite face.')
        self.cabineo_insert_type = Inputs.DropDownInput('insertType', 'Insert Type', utils.misc.class_property_values(LamelloInputs.InsertTypes, Inputs.DropDownInput.Item), LamelloInputs.InsertTypes.M6x123.value, 'Variant of the Cabineo insert.')
        super().__init__()


class Lamello(CustomComputeFeature.CustomComputeFeature):
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
            access_holes, guide_holes = self.create_hole_bodies(edge, access_face, slot_face, guide_face)
            combines.append(Combine.Combine(access_face.body, access_holes, Combine.Operation.CUT))
            combines.append(Combine.Combine(guide_face.body, guide_holes, Combine.Operation.CUT))
        return combines
    
    def access_positions_by_spacing(self, edge: adsk.fusion.BRepEdge) -> list[adsk.core.Vector3D]:
        offset = self.inputs.offset.value
        spacing = self.inputs.spacing.value
        available_length = edge.length - 2 * offset
        number_of_holes = max(1, math.ceil(available_length/spacing))
        edge_normal = utils.brep.normal_along_edge(edge)
        start = utils.vector.add(edge.startVertex.geometry.asVector(), utils.vector.scaled_by(edge_normal, offset if number_of_holes > 1 else edge.length/2))
        computed_spacing = available_length / (number_of_holes-1) if number_of_holes > 1 else 0
        return [utils.vector.add(start, utils.vector.scaled_by(edge_normal, idx * computed_spacing)) for idx in range(number_of_holes)]
    
    def create_clamex_access_hole(self, thickness: float) -> adsk.fusion.BRepBody:
        access_depth = thickness/2
        access_hole_radius = 0.6/2
        access_edge_distance = 0.75
        if self.inputs.size.value == LamelloInputs.Types.CLAMEX_P14.value:
            cyl = utils.brep.cylinder(access_hole_radius, -access_depth)
            return utils.brep.transformed(cyl, utils.matrix.translation_matrix(Vector3D.create(0, access_edge_distance, 0)))
        else:
            return utils.brep.transformed(
                utils.brep.slot(0.25, access_hole_radius, access_depth), 
                utils.matrix.combine_transforms([
                    utils.matrix.rotation_matrix(-math.pi/2, Vector3D.create(0, 0, 1), Point3D.create(0, 0, 0)),
                    utils.matrix.translation_matrix(Vector3D.create(0, access_edge_distance, -access_depth))
                ])
            )
        
    def create_clamex_guide_holes(self, access_thickness: float, guide_thickness: float) -> adsk.fusion.BRepBody:
        guide_hole_depth = guide_thickness if self.inputs.through_guide_holes.value else 0.8
        guide_hole_radius = 0.77/2
        guide_hole_distance = 10.1
        guide_hole_edge_distance = access_thickness/2
        cyl = utils.brep.cylinder(guide_hole_radius, guide_hole_depth)
        guide_hole = utils.brep.transformed(cyl, utils.matrix.translation_matrix(Vector3D.create(guide_hole_distance/2, guide_hole_edge_distance, 0)))
        return utils.brep.union([
            guide_hole,
            utils.brep.transformed(guide_hole, utils.matrix.translation_matrix(Vector3D.create(-guide_hole_distance, 0, 0)))
        ])
    
    def create_cabineo_connector_hole(self) -> adsk.fusion.BRepBody:
        depth = 1.15 if self.inputs.cabineo_flush.value else 1.1
        cyl = utils.brep.cylinder(1.5/2, -depth)
        triple_holes = utils.brep.union([
            utils.brep.transformed(cyl, utils.matrix.translation_matrix(Vector3D.create(0, 0.36, 0))),
            utils.brep.transformed(cyl, utils.matrix.translation_matrix(Vector3D.create(0, 1.48, 0))),
            utils.brep.transformed(cyl, utils.matrix.translation_matrix(Vector3D.create(0, 2.6, 0))),
        ])
        if not self.inputs.cabineo_flush.value:
            return triple_holes
        inset = 0.08
        return utils.brep.union([
            triple_holes,
            utils.brep.transformed(
                utils.brep.cylinder(1.67/2, -inset),
                utils.matrix.translation_matrix(Vector3D.create(0, 2.6, 0))
            ),
            utils.brep.transformed(
                utils.brep.rectangle(1.67, 2.6, inset),
                utils.matrix.translation_matrix(Vector3D.create(0, 2.6/2, -inset))
            )
        ])

    def create_cabineo_screw_hole(self, guide_thickness: float) -> adsk.fusion.BRepBody:
        edge_distance = (0.5+0.08) if self.inputs.cabineo_flush.value else 0.5
        depth: float
        diameter = 0.5
        if self.inputs.size.value == LamelloInputs.Types.CABINEO_8.value:
            depth = 0.8
        elif self.inputs.size.value == LamelloInputs.Types.CABINEO_12.value:
            depth = 1.2
        else:
            diameter = 0.8
            if self.inputs.cabineo_insert_type.value == LamelloInputs.InsertTypes.M6x123.value:
                depth = 1.35
            else:
                depth = 1.65
        if self.inputs.cabineo_through_hole.value:
            depth = guide_thickness
        return utils.brep.transformed(
            utils.brep.cylinder(diameter/2, depth),
            utils.matrix.translation_matrix(Vector3D.create(0, edge_distance, 0))
        )

    def create_hole_bodies(self, edge: adsk.fusion.BRepEdge, access_face: adsk.fusion.BRepFace, slot_face: adsk.fusion.BRepFace, guide_face: adsk.fusion.BRepFace) -> tuple[adsk.fusion.BRepBody, adsk.fusion.BRepBody]:
        access_thickness = utils.brep.get_board_thickness(access_face)
        guide_thickness = utils.brep.get_board_thickness(guide_face)
        positions: list[adsk.core.Vector3D]
        if len(self.inputs.points.value) > 0:
            positions = [cast(adsk.fusion.SketchPoint, p).worldGeometry.asVector() for p in self.inputs.points.value]
        else:
            positions = self.access_positions_by_spacing(edge)

        access_shape: adsk.fusion.BRepBody
        guide_shape: adsk.fusion.BRepBody

        if self.inputs.size.value in [LamelloInputs.Types.CLAMEX_P10.value, LamelloInputs.Types.CLAMEX_P14.value]:
            access_shape = self.create_clamex_access_hole(access_thickness)
            guide_shape = self.create_clamex_guide_holes(access_thickness, guide_thickness)
        else:
            access_shape = self.create_cabineo_connector_hole()
            guide_shape = self.create_cabineo_screw_hole(guide_thickness)

        access_bodies = utils.brep.place_body_on_face_at_positions(access_shape, access_face, edge, positions)
        guide_bodies = utils.brep.place_body_on_face_at_positions(guide_shape, slot_face, edge, positions)
        return access_bodies, guide_bodies

    def pre_select(self, input: adsk.core.SelectionCommandInput, selection: adsk.fusion.BRepEdge) -> bool:
        if input.id == self.inputs.edge.id:
            return utils.brep.find_mating_faces_at_edge(selection) is not None
        else:
            return True
        
    def input_changed(self, input):
        spacing_enabled = self.inputs.points.input.selectionCount == 0
        is_cabineo = self.inputs.size.value in [LamelloInputs.Types.CABINEO_8.value, LamelloInputs.Types.CABINEO_12.value, LamelloInputs.Types.CABINEO_8_M6.value]
        self.inputs.spacing.input.isVisible = spacing_enabled
        self.inputs.offset.input.isVisible = spacing_enabled
        self.inputs.through_guide_holes.input.isVisible = not is_cabineo
        self.inputs.cabineo_flush.input.isVisible = is_cabineo
        self.inputs.cabineo_through_hole.input.isVisible = is_cabineo
        self.inputs.cabineo_insert_type.input.isVisible = self.inputs.size.value in [LamelloInputs.Types.CABINEO_8_M6.value]

