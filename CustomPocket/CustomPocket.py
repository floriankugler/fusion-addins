import sys, os
shared_path = os.path.dirname(__file__)
if shared_path not in sys.path:
    sys.path.append(shared_path)

import adsk.core, adsk.fusion
import CustomComputeFeature, Inputs
import math, utils
from typing import Tuple
import importlib
importlib.reload(utils)
importlib.reload(CustomComputeFeature)
importlib.reload(Inputs)


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
        self.edge = Inputs.SelectionInput('edge', 'Edge', 'LinearEdges', 1, 0, False, 'Select edge along which access holes should be placed.')
        # self.size = Inputs.DropDownInput('size', 'Size', [['Clamex P10', 10], ['Clamex P14', 14]], 10, 'Tool Tip TODO')
        # self.spacing = Inputs.FloatInput('spacing', 'Spacing', 20, 'Tool Tip TODO', units)
        # self.start_offset = Inputs.FloatInput('startOffset', 'Start Offset', 6, 'Tool Tip TODO', units)
        # self.end_offset = Inputs.FloatInput('endOffset', 'End Offset', 6, 'Tool Tip TODO', units)
        self.selections = [self.edge]
        self.values = []
        # self.values = [self.size, self.spacing, self.start_offset, self.end_offset]


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
        pass
        # base_feature = utils.get_base_feature(feature)
        # for edge in self.inputs.edge.get_from_dependencies(feature):
        #     access_face, slot_face = get_access_and_slot_faces(edge)
        #     newBody = create_hole_bodies_union(edge, access_face, slot_face, self.inputs)
        #     base_feature.startEdit()
        #     base_feature.updateBody(base_feature.bodies.item(0), newBody)
        #     base_feature.finishEdit()

    def execute(self, base_feature: adsk.fusion.BaseFeature) -> adsk.fusion.Feature:
        return base_feature
        # last_feature: adsk.fusion.CombineFeature = None
        # for edge in self.inputs.edge.value:
        #     access_face, slot_face = get_access_and_slot_faces(edge)
        #     base_feature.startEdit()
        #     hole_bodies = create_hole_bodies_union(edge, access_face, slot_face, self.inputs)
        #     self.component.bRepBodies.add(hole_bodies, base_feature)
        #     base_feature.finishEdit()

        #     access_combine_input = self.component.features.combineFeatures.createInput(access_face.body, utils.as_object_collection(base_feature.bodies))
        #     access_combine_input.operation = adsk.fusion.FeatureOperations.CutFeatureOperation
        #     access_combine_input.isKeepToolBodies = True
        #     self.component.features.combineFeatures.add(access_combine_input)

        #     guide_body = utils.find_perpendicular_face_containing_edge(edge, access_face).body
        #     guide_combine_input = self.component.features.combineFeatures.createInput(guide_body, utils.as_object_collection(base_feature.bodies))
        #     guide_combine_input.operation = adsk.fusion.FeatureOperations.CutFeatureOperation
        #     last_feature = self.component.features.combineFeatures.add(guide_combine_input)
        # return last_feature

    def pre_select(self, entity):
        if self.edited_custom_feature:
            return False
        else:
            return True


def get_access_and_slot_faces(edge: adsk.fusion.BRepEdge) -> Tuple[adsk.fusion.BRepFace, adsk.fusion.BRepFace]:
    access_face = utils.largest_face_of_edge(edge)
    slot_face = None
    for f in edge.faces:
        if f != access_face:
            slot_face = f
            break
    return (access_face, slot_face)

def access_hole_positions(edge: adsk.fusion.BRepEdge, spacing: float, start_offset: float, end_offset: float) -> list[adsk.core.Point2D]:
    distance_from_edge = 0.75
    available_length = edge.length - start_offset - end_offset
    number_of_holes = math.ceil(available_length/spacing)
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

def create_hole_bodies_union(edge: adsk.fusion.BRepEdge, access_face: adsk.fusion.BRepFace, slot_face: adsk.fusion.BRepFace, inputs: ClamexInputs) -> adsk.fusion.BRepBody:
    thickness = utils.get_board_thickness(access_face)
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

    def guide_hole() -> adsk.fusion.BRepBody:
        holeRadius = 0.77/2
        holeDepth = 0.8
        return mgr.createCylinderOrCone(adsk.core.Point3D.create(0, 0, 0), holeRadius, adsk.core.Point3D.create(0, 0, -holeDepth), holeRadius)

    access_bodies = utils.create_bodies_at_points_on_face(access_positions, access_face, edge, access_hole)
    guide_bodies = utils.create_bodies_at_points_on_face(guide_positions, slot_face, edge, guide_hole)
    result = access_bodies[0]
    for body in (access_bodies[1:] + guide_bodies):
        mgr.booleanOperation(result, body, adsk.fusion.BooleanTypes.UnionBooleanType)
    return result

