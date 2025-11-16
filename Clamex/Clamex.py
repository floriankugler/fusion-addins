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
        self.start_offset = Inputs.FloatInput('offset', 'Offset', 6, 'Distance of the first connector from the start of the edge.', units)
        self.through_guide_holes = Inputs.CheckboxInput('throughGuideHoles', 'Through Guide Holes', False, 'If checked the guide holes are punched all the way through to the opposite face.')
        super().__init__()


class ClamexFeature(CustomComputeFeature.CustomComputeFeature):
    plugin_id = 'antonClamex'
    plugin_name = 'Clamex'
    plugin_desc = 'Clamex access/guide holes'
    plugin_tooltip = 'Adds Clamex access holes and guide holes along an edge.'
    inputs: ClamexInputs

    def create_inputs(self) -> ClamexInputs:
        return ClamexInputs(self.app.activeProduct.unitsManager)

    def execute(self) -> list[CustomComputeFeature.Combine]:
        combines: list[CustomComputeFeature.Combine] = []
        for edge in self.inputs.edge.value:
            access_face, slot_face, guide_face = find_faces(edge)
            if not guide_face:
                continue
            access_holes, guide_holes = create_hole_bodies(edge, access_face, slot_face, guide_face, self.inputs)
            combines.append(CustomComputeFeature.Combine(access_face.body, access_holes, adsk.fusion.FeatureOperations.CutFeatureOperation))
            combines.append(CustomComputeFeature.Combine(guide_face.body, guide_holes, adsk.fusion.FeatureOperations.CutFeatureOperation))
        return combines
    
    def pre_select(self, input: adsk.core.SelectionCommandInput, entity: adsk.fusion.BRepEdge) -> bool:
        if input.id == self.inputs.edge.id:
            return find_faces(entity) is not None
        else:
            return True

def find_faces(edge: adsk.fusion.BRepEdge) -> tuple[adsk.fusion.BRepFace, adsk.fusion.BRepFace, adsk.fusion.BRepFace]:
    access_face, slot_face = get_access_and_slot_faces(edge)
    if not access_face or not slot_face:
        return None
    guide_face = find_guide_face(edge, access_face, slot_face)
    if not guide_face:
        return None
    return access_face, slot_face, guide_face

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
        if f != access_face and utils.brep.is_planar(f):
            slot_face = f
            break
    return (access_face, slot_face)

def access_hole_positions(edge: adsk.fusion.BRepEdge, spacing: float, offset: float) -> list[adsk.core.Point2D]:
    distance_from_edge = 0.75
    available_length = edge.length - 2 * offset
    number_of_holes = max(1, math.ceil(available_length/spacing))
    start = edge.length/2
    computed_spacing = 0
    if number_of_holes > 1:
        start = offset
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
    access_positions = access_hole_positions(edge, inputs.spacing.value, inputs.start_offset.value)
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


