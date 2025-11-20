import sys, os
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
shared_folder = os.path.join(parent_dir, "SharedUtils")
if current_dir not in sys.path: sys.path.append(current_dir)
if shared_folder not in sys.path: sys.path.append(shared_folder)
import CustomComputeFeature, Inputs, utils
import adsk.core, adsk.fusion
from adsk.core import Point3D, Vector3D
import math
utils.misc.force_reload_modules('CustomComputeFeature', 'Inputs', 'utils')

_feature: CustomComputeFeature.CustomComputeFeature = None

def run(context):
    global _feature
    _feature = Lamello()

def stop(context):
    global _feature
    del _feature

class LamelloInputs(Inputs.Inputs):
    def __init__(self, units_manager: adsk.core.UnitsManager):
        units = units_manager.defaultLengthUnits
        self.edge = Inputs.SelectionByEntityTokenInput('edge', 'Edge', 'LinearEdges', 1, 0, 'Select edge along which access holes should be placed.')
        self.points = Inputs.SelectionByEntityTokenInput('points', 'Points', 'SketchPoints', 0, 0, 'To manually place the connectors, select sketch points.')
        self.size = Inputs.DropDownInput('size', 'Variant', [['Clamex P10', 10], ['Clamex P14', 14]], 10, 'Variant of the Lamello connector.')
        self.spacing = Inputs.FloatInput('spacing', 'Spacing', 20, 'Minimum spacing between the connectors.', units)
        self.offset = Inputs.FloatInput('offset', 'Offset', 6, 'Distance of the first connector from the start of the edge.', units)
        self.through_guide_holes = Inputs.CheckboxInput('throughGuideHoles', 'Through Guide Holes', False, 'If checked the guide holes are punched all the way through to the opposite face.')
        super().__init__()


class Lamello(CustomComputeFeature.CustomComputeFeature):
    plugin_id = 'antonLamello'
    plugin_name = 'Lamello'
    plugin_desc = 'Lamello connectors'
    plugin_tooltip = 'Adds access guide holes for Lamello connectors along an edge.'
    inputs: LamelloInputs

    def create_inputs(self) -> LamelloInputs:
        return LamelloInputs(self.app.activeProduct.unitsManager)

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
        
    def input_changed(self, _):
        spacing_enabled = self.inputs.points.input.selectionCount == 0
        self.inputs.spacing.input.isEnabled = spacing_enabled
        self.inputs.offset.input.isEnabled = spacing_enabled

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

def access_positions_by_spacing(edge: adsk.fusion.BRepEdge, spacing: float, offset: float) -> list[adsk.core.Vector3D]:
    available_length = edge.length - 2 * offset
    number_of_holes = max(1, math.ceil(available_length/spacing))
    edge_normal = utils.brep.normal_along_edge(edge)
    start = utils.vector.add(edge.startVertex.geometry.asVector(), utils.vector.scaled_by(edge_normal, offset if number_of_holes > 1 else edge.length/2))
    computed_spacing = available_length / (number_of_holes-1) if number_of_holes > 1 else 0
    return [utils.vector.add(start, utils.vector.scaled_by(edge_normal, idx * computed_spacing)) for idx in range(number_of_holes)]

def create_hole_bodies(edge: adsk.fusion.BRepEdge, access_face: adsk.fusion.BRepFace, slot_face: adsk.fusion.BRepFace, guide_face: adsk.fusion.BRepFace, inputs: LamelloInputs) -> tuple[adsk.fusion.BRepBody, adsk.fusion.BRepBody]:
    mgr = adsk.fusion.TemporaryBRepManager.get()
    thickness = utils.brep.get_board_thickness(access_face)
    positions: list[adsk.core.Point3D]
    if len(inputs.points.value) > 0:
        positions = [p.worldGeometry.asVector() for p in inputs.points.value]
    else:
        positions = access_positions_by_spacing(edge, inputs.spacing.value, inputs.offset.value)

    access_hole = None
    access_depth = thickness/2
    access_hole_radius = 0.6/2
    access_edge_distance = 0.75
    if inputs.size.value == 14:
        cyl = utils.brep.cylinder(access_hole_radius, -access_depth)
        access_hole = utils.brep.transformed(cyl, utils.matrix.translation_matrix(Vector3D.create(0, access_edge_distance, 0)))
    else:
        access_hole = utils.brep.slot(0.25, access_hole_radius, access_depth)
        mgr.transform(access_hole, utils.matrix.combine_transforms([
            utils.matrix.rotation_matrix(-math.pi/2, Vector3D.create(0, 0, 1), Point3D.create(0, 0, 0)),
            utils.matrix.translation_matrix(Vector3D.create(0, access_edge_distance, -access_depth))
        ]))

    guide_hole_depth = utils.brep.get_board_thickness(guide_face) if inputs.through_guide_holes.value else 0.8
    guide_hole_radius = 0.77/2
    guide_hole_distance = 10.1
    guide_hole_edge_distance = thickness/2
    cyl = utils.brep.cylinder(guide_hole_radius, guide_hole_depth)
    guide_hole = utils.brep.transformed(cyl, utils.matrix.translation_matrix(Vector3D.create(guide_hole_distance/2, guide_hole_edge_distance, 0)))
    guide_holes = utils.brep.union([
        guide_hole,
        utils.brep.transformed(guide_hole, utils.matrix.translation_matrix(Vector3D.create(-guide_hole_distance, 0, 0)))
    ])

    access_bodies = utils.brep.place_body_on_face_at_positions(access_hole, access_face, edge, positions)
    guide_bodies = utils.brep.place_body_on_face_at_positions(guide_holes, slot_face, edge, positions)
    return access_bodies, guide_bodies
