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

import math
from typing import Tuple


_feature: CustomComputeFeature.CustomComputeFeature = None

def run(context):
    global _feature
    _feature = ClamexFeature()

def stop(context):
    global _feature
    del _feature

class ClamexInputs(Inputs.Inputs):
    def __init__(self, units_manager: adsk.core.UnitsManager):
        units = units_manager.defaultLengthUnits
        self.edge = Inputs.SelectionByEntityTokenInput('edge', 'Edge', 'LinearEdges', 1, 0, False, 'Select edge along which access holes should be placed.')
        self.size = Inputs.DropDownInput('size', 'Size', [['Clamex P10', 10], ['Clamex P14', 14]], 10, 'Size variant of the Clamex connector.')
        self.spacing = Inputs.FloatInput('spacing', 'Spacing', 20, 'Minimum spacing between the connectors.', units)
        self.start_offset = Inputs.FloatInput('startOffset', 'Start Offset', 6, 'Offset of the first connector from the start of the edge.', units)
        self.end_offset = Inputs.FloatInput('endOffset', 'End Offset', 6, 'Offset of the last connector to the end of the edge.', units)
        self.through_guide_holes = Inputs.CheckboxInput('throughGuideHoles', 'Through Guide Holes', False, 'If checked the guide holes are punched all the way through to the opposite face.')
        self.selections = [self.edge]
        self.values = [self.size, self.spacing, self.start_offset, self.end_offset, self.through_guide_holes]


class ClamexFeature(CustomComputeFeature.CustomComputeFeature):
    plugin_id = 'antonClamex'
    plugin_name = 'Clamex'
    plugin_desc = 'Clamex access/guide holes'
    plugin_tooltip = 'Adds Clamex access holes and guide holes along an edge.'
    inputs: ClamexInputs

    @property
    def component(self) -> adsk.fusion.Component:
        return self.inputs.edge.value[0].body.parentComponent

    def create_inputs(self) -> ClamexInputs:
        return ClamexInputs(self.app.activeProduct.unitsManager)

    def compute(self, feature: adsk.fusion.CustomFeature) -> None:
        base_feature = utils.fusion.get_base_feature(feature)
        for idx, edge in enumerate(self.inputs.edge.get_from_dependencies(feature)):
            access_face, slot_face = get_access_and_slot_faces(edge)
            guide_face = utils.brep.find_perpendicular_face_containing_edge(edge, access_face)
            new_access, new_guide = create_hole_bodies(edge, access_face, slot_face, guide_face, self.inputs)
            base_feature.startEdit()
            base_feature.updateBody(base_feature.bodies.item(idx * 2), new_access)
            base_feature.updateBody(base_feature.bodies.item(idx * 2 + 1), new_guide)
            base_feature.finishEdit()

    def execute(self, base_feature: adsk.fusion.BaseFeature) -> adsk.fusion.Feature:
        last_feature: adsk.fusion.CombineFeature = base_feature
        for edge in self.inputs.edge.value:
            access_face, slot_face = get_access_and_slot_faces(edge)
            guide_face = utils.brep.find_perpendicular_face_containing_edge(edge, access_face)
            
            access_holes, guide_holes = create_hole_bodies(edge, access_face, slot_face, guide_face, self.inputs)
            base_feature.startEdit()
            self.component.bRepBodies.add(access_holes, base_feature)
            self.component.bRepBodies.add(guide_holes, base_feature)
            base_feature.finishEdit()

            cut_coll = adsk.core.ObjectCollection.createWithArray([base_feature.bodies.item(0)])
            access_combine_input = self.component.features.combineFeatures.createInput(access_face.body, cut_coll)
            access_combine_input.operation = adsk.fusion.FeatureOperations.CutFeatureOperation
            self.component.features.combineFeatures.add(access_combine_input)

            cut_coll = adsk.core.ObjectCollection.createWithArray([base_feature.bodies.item(0)])
            guide_combine_input = self.component.features.combineFeatures.createInput(guide_face.body, cut_coll)
            guide_combine_input.operation = adsk.fusion.FeatureOperations.CutFeatureOperation
            last_feature = self.component.features.combineFeatures.add(guide_combine_input)
        return last_feature


def get_access_and_slot_faces(edge: adsk.fusion.BRepEdge) -> Tuple[adsk.fusion.BRepFace, adsk.fusion.BRepFace]:
    access_face = utils.brep.largest_face_of_edge(edge)
    slot_face = None
    for f in edge.faces:
        if f != access_face:
            slot_face = f
            break
    return (access_face, slot_face)

def access_hole_positions(edge: adsk.fusion.BRepEdge, spacing: float, start_offset: float, end_offset: float) -> list[adsk.core.Point2D]:
    distance_from_edge = 0.75
    available_length = edge.length - start_offset - end_offset
    number_of_holes = max(1, math.ceil(available_length/spacing))
    start = edge.length/2
    computed_spacing = 0
    if number_of_holes > 1:
        start = start_offset
        computed_spacing = available_length/(number_of_holes-1)
    result = []
    for idx in range(number_of_holes):
        distance = idx * computed_spacing + start
        result.append(adsk.core.Point2D.create(distance, distance_from_edge))
    return result

def guide_hole_positions(access_positions: list[adsk.core.Point2D], thickness) -> list[adsk.core.Point2D]:
    offset = 10.1/2
    return [y for p in access_positions for y in (adsk.core.Point2D.create(p.x-offset, thickness/2), adsk.core.Point2D.create(p.x+offset, thickness/2))]

def create_hole_bodies(edge: adsk.fusion.BRepEdge, access_face: adsk.fusion.BRepFace, slot_face: adsk.fusion.BRepFace, guide_face: adsk.fusion.BRepFace, inputs: ClamexInputs) -> tuple[adsk.fusion.BRepBody, adsk.fusion.BRepBody]:
    thickness = utils.brep.get_board_thickness(access_face)
    access_positions = access_hole_positions(edge, inputs.spacing.value, inputs.start_offset.value, inputs.end_offset.value)
    guide_positions = guide_hole_positions(access_positions, thickness)

    mgr = adsk.fusion.TemporaryBRepManager.get()
    access_depth = thickness/2

    def access_hole() -> adsk.fusion.BRepBody:
        hole_radius = 0.6/2
        if inputs.size.value == 14:
            return mgr.createCylinderOrCone(adsk.core.Point3D.create(0, 0, 0), hole_radius, adsk.core.Point3D.create(0, 0, access_depth), hole_radius)
        else:
            hole1 = mgr.createCylinderOrCone(adsk.core.Point3D.create(0, 0, 0), hole_radius, adsk.core.Point3D.create(0, 0, access_depth), hole_radius)
            hole2 = mgr.createCylinderOrCone(adsk.core.Point3D.create(0, -0.25, 0), hole_radius, adsk.core.Point3D.create(0, -0.25, access_depth), hole_radius)
            box = mgr.createBox(adsk.core.OrientedBoundingBox3D.create(
                adsk.core.Point3D.create(0, -0.25/2, access_depth/2),
                adsk.core.Vector3D.create(0, 1, 0),
                adsk.core.Vector3D.create(1, 0, 0),
                0.25,
                hole_radius * 2,
                access_depth
            ))
            mgr.booleanOperation(box, hole1, adsk.fusion.BooleanTypes.UnionBooleanType)
            mgr.booleanOperation(box, hole2, adsk.fusion.BooleanTypes.UnionBooleanType)
            return box

    guide_hole_depth = utils.brep.get_board_thickness(guide_face) if inputs.through_guide_holes.value else 0.8
    def guide_hole() -> adsk.fusion.BRepBody:
        hole_radius = 0.77/2
        return mgr.createCylinderOrCone(adsk.core.Point3D.create(0, 0, 0), hole_radius, adsk.core.Point3D.create(0, 0, -guide_hole_depth), hole_radius)

    access_bodies = utils.brep.create_bodies_at_points_on_face(access_positions, access_face, edge, access_hole)
    guide_bodies = utils.brep.create_bodies_at_points_on_face(guide_positions, slot_face, edge, guide_hole)
    access_union = access_bodies[0]
    for body in (access_bodies[1:]):
        mgr.booleanOperation(access_union, body, adsk.fusion.BooleanTypes.UnionBooleanType)
    guide_union = guide_bodies[0]
    for body in (guide_bodies[1:]):
        mgr.booleanOperation(guide_union, body, adsk.fusion.BooleanTypes.UnionBooleanType)
    return access_union, guide_union

