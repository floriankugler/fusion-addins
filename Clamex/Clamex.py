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
import math


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
        self.edge = Inputs.SelectionByEntityTokenInput('edge', 'Edge', 'LinearEdges', 1, 0, 'Select edge along which access holes should be placed.')
        self.size = Inputs.DropDownInput('size', 'Size', [['Clamex P10', 10], ['Clamex P14', 14]], 10, 'Size variant of the Clamex connector.')
        self.spacing = Inputs.FloatInput('spacing', 'Spacing', 20, 'Minimum spacing between the connectors.', units)
        self.start_offset = Inputs.FloatInput('startOffset', 'Start Offset', 6, 'Offset of the first connector from the start of the edge.', units)
        self.end_offset = Inputs.FloatInput('endOffset', 'End Offset', 6, 'Offset of the last connector to the end of the edge.', units)
        self.through_guide_holes = Inputs.CheckboxInput('throughGuideHoles', 'Through Guide Holes', False, 'If checked the guide holes are punched all the way through to the opposite face.')
        super().__init__()


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
        for idx, edge in enumerate(self.inputs.edge.value):
            access_face, slot_face = get_access_and_slot_faces(edge)
            guide_face = find_guide_face(edge, access_face, slot_face)
            new_access, new_guide = create_hole_bodies(edge, access_face, slot_face, guide_face, self.inputs)
            base_feature.startEdit()
            base_feature.updateBody(base_feature.bodies.item(idx * 2), new_access)
            base_feature.updateBody(base_feature.bodies.item(idx * 2 + 1), new_guide)
            base_feature.finishEdit()

    def execute(self, base_feature: adsk.fusion.BaseFeature) -> adsk.fusion.Feature:
        last_feature: adsk.fusion.CombineFeature = base_feature
        for edge in self.inputs.edge.value:
            access_face, slot_face = get_access_and_slot_faces(edge)
            guide_face = find_guide_face(edge, access_face, slot_face)
            
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

def find_guide_face(edge: adsk.fusion.BRepEdge, access_face: adsk.fusion.BRepFace, slot_face: adsk.fusion.BRepFace) -> adsk.fusion.BRepFace:
    slot_normal = utils.brep.normal_into_face(edge, slot_face)
    slot_dir = utils.vector.scaled_by(slot_normal, 0.5)
    edge_normal = utils.brep.normal_along_edge(edge)
    step = utils.vector.scaled_by(edge_normal, 5)
    start = utils.vector.add(edge.startVertex.geometry.asVector(), slot_dir)
    test_points = []
    for x in range(0, math.floor(edge.length/5)):
        test_points.append(utils.vector.add(start, utils.vector.scaled_by(step, x)).asPoint())

    def check_face(face: adsk.fusion.BRepFace):
        for t in test_points:
            _, param = face.evaluator.getParameterAtPoint(t)
            if face.evaluator.isParameterOnFace(param):
                return True
        return False

    return utils.brep.find_perpendicular_face_containing_edge(edge, access_face, check_face)


def get_access_and_slot_faces(edge: adsk.fusion.BRepEdge) -> tuple[adsk.fusion.BRepFace, adsk.fusion.BRepFace]:
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
    mgr = adsk.fusion.TemporaryBRepManager.get()
    thickness = utils.brep.get_board_thickness(access_face)
    access_positions = access_hole_positions(edge, inputs.spacing.value, inputs.start_offset.value, inputs.end_offset.value)
    guide_positions = guide_hole_positions(access_positions, thickness)

    access_hole = None
    access_depth = thickness/2
    hole_radius = 0.6/2
    if inputs.size.value == 14:
        access_hole = utils.brep.cylinder(Point3D.create(0, 0, -access_depth), hole_radius, access_depth)
    else:
        access_hole = utils.brep.slot(0.25, hole_radius, access_depth)
        mgr.transform(access_hole, utils.matrix.combine_transforms([
            utils.matrix.rotation_matrix(-math.pi/2, Vector3D.create(0, 0, 1), Point3D.create(0, 0, 0)),
            utils.matrix.mirror_matrix(Point3D.create(), Vector3D.create(1, 1, -1))
        ]))

    guide_hole_depth = utils.brep.get_board_thickness(guide_face) if inputs.through_guide_holes.value else 0.8
    hole_radius = 0.77/2
    guide_hole = utils.brep.cylinder(Point3D.create(0, 0, -guide_hole_depth), hole_radius, guide_hole_depth)

    access_bodies = utils.brep.union([utils.brep.transformed(access_hole, utils.matrix.translation_matrix(Vector3D.create(p.x, p.y, 0))) for p in access_positions])
    guide_bodies = utils.brep.union([utils.brep.transformed(guide_hole, utils.matrix.translation_matrix(Vector3D.create(p.x, p.y, 0))) for p in guide_positions])

    origin, x, access_y, _ = utils.brep.coordinate_system_on_face(access_face, edge)
    guide_y = utils.brep.normal_into_face(edge, slot_face)
    mgr.transform(access_bodies, utils.matrix.transform_from_root(origin, x, access_y))
    mgr.transform(guide_bodies, utils.matrix.transform_from_root(origin, x, guide_y))
    return access_bodies, guide_bodies


