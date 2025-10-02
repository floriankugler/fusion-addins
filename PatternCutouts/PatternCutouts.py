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
    _feature = TrianglePattern()

def stop(context):
    global _feature
    del _feature

class TriangleInputs(Inputs.Inputs):
    types = {
        'Triangles': 0,
        'Rhombuses': 1,
        'Cross': 2,
        'Rounded Rectangle': 3,
    }

    def __init__(self, units_manager: adsk.core.UnitsManager):
        units = units_manager.defaultLengthUnits
        self.faces = Inputs.SelectionByEntityTokenInput('faces', 'Faces', 'PlanarFaces', 1, 0, False, 'Select faces to create triangle pockets on.')
        self.profiles = Inputs.SelectionInput('profiles', 'Profiles', 'Profiles', 0, 0, True, 'Select profiles on a single face to restrict the pattern to these profiles. Only makes sense if a single face is selected.')
        self.type = Inputs.DropDownInput('type', 'Type', TriangleInputs.types.items(), TriangleInputs.types['Triangles'], 'The type of pattern to use.')
        self.preferred_width = Inputs.FloatInput('preferred_width', 'Preferred Width', 10, 'Indicates the preferred width of the shape.', units)
        self.preferred_height = Inputs.FloatInput('preferred_height', 'Preferred Height', 15, 'Indicates the preferred height of the shape.', units)
        self.spacing = Inputs.FloatInput('spacing', 'Spacing', 2, 'Spacing between the shapes.', units)
        self.inset = Inputs.FloatInput('inset', 'Inset', 2, 'Inset of the pattern from the face\'s edges', units)
        self.fillet = Inputs.FloatInput('fillet', 'Fillet', 0.8, 'Fillet radius', units)
        self.compensate_fillet = Inputs.CheckboxInput('compensate_fillet', 'Compensate Fillet', False, 'Makes all triangles in one row appear to be bottom and top aligned, irrespective of the fillet applied to the corners')
        self.adaptive = Inputs.CheckboxInput('adaptive', 'Adaptive', True, 'Prioritzes filling up the available space with the pattern over adhering to the width/height values, treating them more a starting point.')
        self.remainder = Inputs.FloatInput('remainder', 'Remaining Material', 0, 'Thickness of the remaining material to leave untouched.', units)
        self.selections = [self.faces, self.profiles]
        self.values = [self.type, self.preferred_width, self.preferred_height, self.spacing, self.inset, self.fillet, self.compensate_fillet, self.adaptive, self.remainder]


class TrianglePattern(CustomComputeFeature.CustomComputeFeature):
    plugin_id = 'antonPatternCutouts'
    plugin_name = 'PatternCutouts'
    plugin_desc = 'Pattern Cutouts'
    plugin_tooltip = 'Creates patterned cutouts of various shapes.'
    inputs: TriangleInputs

    @property
    def component(self) -> adsk.fusion.Component:
        return self.inputs.faces.value[0].body.parentComponent

    def create_inputs(self) -> TriangleInputs:
        return TriangleInputs(self.app.activeProduct.unitsManager)

    def compute(self, feature: adsk.fusion.CustomFeature) -> None:
        base_feature = utils.fusion.get_base_feature(feature)
        for idx, face in enumerate(self.inputs.faces.value):
            newBody = self.create_pattern_for_face(face, self.inputs.profiles.value)
            base_feature.startEdit()
            base_feature.updateBody(base_feature.bodies[idx], newBody)
            base_feature.finishEdit()

    def execute(self, base_feature: adsk.fusion.BaseFeature) -> adsk.fusion.Feature:
        last_feature: adsk.fusion.CombineFeature = None

        for face in self.inputs.faces.value:
            triangles = self.create_pattern_for_face(face, self.inputs.profiles.value)
            base_feature.startEdit()
            self.component.bRepBodies.add(triangles, base_feature)
            base_feature.finishEdit()

            combine_input = self.component.features.combineFeatures.createInput(face.body, utils.fusion.as_object_collection(base_feature.bodies))
            combine_input.operation = adsk.fusion.FeatureOperations.CutFeatureOperation
            last_feature = self.component.features.combineFeatures.add(combine_input)

        return last_feature 

    def create_pattern_for_face(self, face: adsk.fusion.BRepFace, profiles: list[adsk.fusion.Profile]) -> adsk.fusion.BRepBody:
        mgr = adsk.fusion.TemporaryBRepManager.get()
        opposite_face = utils.brep.get_opposite_face(face)
        depth = abs(utils.brep.distance_along_normal_between_faces(face, opposite_face))
        depth -= self.inputs.remainder.value
        cut_normal = utils.brep.normal_towards_face(face, opposite_face)
        cut = utils.vector.scaled_by(cut_normal, depth)

        type = self.inputs.type.value
        generator = None
        if type == TriangleInputs.types['Triangles']:
            generator = create_triangles    
        elif type == TriangleInputs.types['Rhombuses']:
            generator = create_rhombuses
        elif type == TriangleInputs.types['Cross']:
            generator = create_cross
        elif type == TriangleInputs.types['Rounded Rectangle']:
            generator = create_rounded_rect
        else:
            return

        if len(profiles) > 0:
            result = None
            for profile in profiles:
                sketch = profile.parentSketch
                profile_body = mgr.copy(profile.face.body)
                mgr.transform(profile_body, utils.matrix.transform_from_root(sketch.origin, sketch.xDirection, sketch.yDirection))
                profile_face = profile_body.faces[0]
                next_triangles = generator(profile_face, cut, self.inputs)
                mgr.transform(next_triangles, utils.matrix.transform_into_face(profile_face, cut))
                if result:
                    mgr.booleanOperation(result, next_triangles, adsk.fusion.BooleanTypes.UnionBooleanType)
                else:
                    result = next_triangles
            return result
        else:
            result = generator(face, cut, self.inputs)
            mgr.transform(result, utils.matrix.transform_into_face(face, cut))
            return result


def create_triangles(face: adsk.fusion.BRepFace, cut: Vector3D,  inputs: TriangleInputs) -> adsk.fusion.BRepBody:
    mgr = adsk.fusion.TemporaryBRepManager.get()
    spacing = inputs.spacing.value * 2
    fillet = inputs.fillet.value
    compensate_fillet = inputs.compensate_fillet.value

    long_edge, short_edge = utils.brep.longest_and_adjecent_edge_of_face(face)
    face_length = long_edge.length
    face_width = short_edge.length
    vertical_space = face_width - 2 * inputs.inset.value
    horizontal_space = face_length - 2 * inputs.inset.value
    rows = max(1, math.floor((vertical_space + spacing/2) / (inputs.preferred_height.value + spacing/2)))
    columns = max(1, math.floor((horizontal_space + spacing) / (inputs.preferred_width.value + spacing)))
    width = inputs.preferred_width.value
    height = inputs.preferred_height.value
    ratio = width/height

    def point_angle(width, height):
        base_angle = math.atan(height/(width/2))
        return math.pi - 2 * base_angle

    def fillet_height_offset(point_angle):
        return (fillet/math.sin(point_angle/2) - fillet) if compensate_fillet else 0

    def compute_vertical_spacing(height, point_angle):
        if rows == 1:
            return 0
        return (vertical_space - rows * (height - fillet_height_offset(point_angle))) / (rows - 1)

    def visual_spacing(point_angle):
        spacing_correction = math.tan(point_angle/2) * fillet_height_offset(point_angle)
        return math.cos(point_angle/2) * (spacing/2 - spacing_correction)

    def spacing_deviation(h):
        angle = point_angle(width, h)
        return visual_spacing(angle) - compute_vertical_spacing(h, angle)

    def height_deviation(h):
        actual_height = h - fillet_height_offset(point_angle(width, h))
        return actual_height - vertical_space

    vertical_spacing = visual_spacing(point_angle(width, height))
    
    if inputs.adaptive.value:
        width = (horizontal_space - (columns - 1) * spacing) / columns
        height_lower = width/ratio * 0.5
        height_upper = width/ratio * 2
        if rows > 1:
            height = utils.misc.binary_search(height_lower, height_upper, spacing_deviation, 0, 0.1)
        else:
            height = utils.misc.binary_search(height_lower, height_upper, height_deviation, 0, 0.1)
        vertical_spacing = compute_vertical_spacing(height, point_angle(width, height))

    triangle = utils.brep.isosceles_triangle(width, height, cut.length, fillet)
    triangle_height = (triangle.boundingBox.maxPoint.y - triangle.boundingBox.minPoint.y) if compensate_fillet else height

    upside_down_triangle = mgr.copy(triangle)
    flip_transform = utils.matrix.mirror_matrix(Point3D.create(0, triangle_height/2, 0), Vector3D.create(1, -1, 1))
    mgr.transform(upside_down_triangle, flip_transform)

    row = mgr.copy(triangle)
    for idx in range(columns * 2 - 1):
        x = idx * (width + spacing) / 2
        t = mgr.copy(triangle if idx % 2 == 0 else upside_down_triangle)
        mgr.transform(t, utils.matrix.translation_matrix(Vector3D.create(x, 0, 0)))
        mgr.booleanOperation(row, t, adsk.fusion.BooleanTypes.UnionBooleanType)

    inverted_row = mgr.copy(row)
    mgr.transform(inverted_row, flip_transform)

    result = mgr.copy(row)
    for idx in range(1, rows):
        y = idx * (triangle_height + vertical_spacing)
        r = mgr.copy(row if idx % 2 == 0 else inverted_row)
        mgr.transform(r, utils.matrix.translation_matrix(Vector3D.create(0, y, 0)))
        mgr.booleanOperation(result, r, adsk.fusion.BooleanTypes.UnionBooleanType)

    result_bb = result.preciseBoundingBox
    offset_x = face_length/2 - (result_bb.maxPoint.x + result_bb.minPoint.x)/2
    offset_y = face_width/2 - (result_bb.maxPoint.y + result_bb.minPoint.y)/2
    mgr.transform(result, utils.matrix.translation_matrix(Vector3D.create(offset_x, offset_y, 0)))
    return result


def create_rhombuses(face: adsk.fusion.BRepFace, cut: Vector3D,  inputs: TriangleInputs) -> adsk.fusion.BRepBody:
    mgr = adsk.fusion.TemporaryBRepManager.get()
    long_edge, short_edge = utils.brep.longest_and_adjecent_edge_of_face(face)
    face_length = long_edge.length
    face_width = short_edge.length
    vertical_space = face_width - 2 * inputs.inset.value
    horizontal_space = face_length - 2 * inputs.inset.value

    def pattern_spacing(ratio):
        angle = 2 * math.atan(ratio)
        sx = 2 * inputs.spacing.value * math.sin(angle/2) / math.sin(angle)
        sy = sx / ratio
        return (sx, sy)

    def pattern_dimensions(ratio):
        sx, sy, pattern_spacing(ratio)
        w = (horizontal_space - (columns - 1) * sx) / columns
        h = w / ratio
        return (w, h, sx, sy)

    width = inputs.preferred_width.value
    height = inputs.preferred_height.value
    initial_ratio = width / height
    sx, sy = pattern_spacing(initial_ratio)
    rows = max(1, math.floor((vertical_space + sy) / (height + sy)))
    columns = max(1, math.floor((horizontal_space + sx) / (width + sx)))

    if inputs.adaptive.value:
        def height_deviation(ratio):
            _, h, _, sy = pattern_dimensions(ratio)
            actual_height = h * rows + sy * (rows - 1)
            return vertical_space - actual_height

        ratio_lower = initial_ratio * 0.5
        ratio_upper = initial_ratio * 1.5
        optimized_ratio = utils.misc.binary_search(ratio_lower, ratio_upper, height_deviation, 0, 0.1)
        width, height, sx, sy = pattern_dimensions(optimized_ratio)

    rhombus = utils.brep.rhombus(width, height, cut.length, inputs.fillet.value)
    row = mgr.copy(rhombus)
    for idx in range(columns):
        x = idx * (width + sx)
        t = mgr.copy(rhombus)
        mgr.transform(t, utils.matrix.translation_matrix(Vector3D.create(x, 0, 0)))
        mgr.booleanOperation(row, t, adsk.fusion.BooleanTypes.UnionBooleanType)

    result = mgr.copy(row)
    for idx in range(1, rows):
        y = idx * (height + sy)
        r = mgr.copy(row)
        mgr.transform(r, utils.matrix.translation_matrix(Vector3D.create(0, y, 0)))
        mgr.booleanOperation(result, r, adsk.fusion.BooleanTypes.UnionBooleanType)

    intermediate_row = mgr.copy(rhombus)
    for idx in range(columns - 1):
        t = mgr.copy(rhombus)
        mgr.transform(t, utils.matrix.translation_matrix(Vector3D.create(idx * (width + sx), 0, 0)))
        mgr.booleanOperation(intermediate_row, t, adsk.fusion.BooleanTypes.UnionBooleanType)
    mgr.transform(intermediate_row, utils.matrix.translation_matrix(Vector3D.create((width + sx)/2, 0, 0)))

    for idx in range(rows - 1):
        r = mgr.copy(intermediate_row)
        mgr.transform(r, utils.matrix.translation_matrix(Vector3D.create(0, (height + sy)/2 + idx * (height + sy)))) 
        mgr.booleanOperation(result, r, adsk.fusion.BooleanTypes.UnionBooleanType)

    if columns > 1:
        triangle_height = (height - sy) / 2
        triangle_angle = 2 * math.atan(width/height)
        triangle_width = math.tan(triangle_angle/2) * 2 * triangle_height
        triangle = utils.brep.isosceles_triangle(triangle_width, triangle_height, cut.length, inputs.fillet.value)
        triangle_row = mgr.copy(triangle)
        for idx in range(columns - 1):
            t = mgr.copy(triangle)
            mgr.transform(t, utils.matrix.translation_matrix(Vector3D.create(idx * (width + sx), 0, 0)))
            mgr.booleanOperation(triangle_row, t, adsk.fusion.BooleanTypes.UnionBooleanType)
        mgr.transform(triangle_row, utils.matrix.translation_matrix(Vector3D.create((width + sx)/2, -height/2, -cut.length/2)))
        mgr.booleanOperation(result, triangle_row, adsk.fusion.BooleanTypes.UnionBooleanType)
        mgr.transform(triangle_row, utils.matrix.mirror_matrix(Point3D.create(0, (rows - 1) * (height + sy)/2, 0), Vector3D.create(1, -1, 1)))
        mgr.booleanOperation(result, triangle_row, adsk.fusion.BooleanTypes.UnionBooleanType)

    if rows > 1:
        triangle_height = (width - sx) / 2
        triangle_angle = 2 * math.atan(height/width)
        triangle_width = math.tan(triangle_angle/2) * 2 * triangle_height
        triangle = utils.brep.isosceles_triangle(triangle_width, triangle_height, cut.length, inputs.fillet.value)
        mgr.transform(triangle, utils.matrix.rotation_matrix(-math.pi/2, Vector3D.create(0, 0, 1), Point3D.create()))
        triangle_row = mgr.copy(triangle)
        for idx in range(rows - 1):
            t = mgr.copy(triangle)
            mgr.transform(t, utils.matrix.translation_matrix(Vector3D.create(0, idx * (height + sy), 0)))
            mgr.booleanOperation(triangle_row, t, adsk.fusion.BooleanTypes.UnionBooleanType)
        mgr.transform(triangle_row, utils.matrix.translation_matrix(Vector3D.create(-width/2, (height + sy)/2, -cut.length/2)))
        mgr.booleanOperation(result, triangle_row, adsk.fusion.BooleanTypes.UnionBooleanType)
        mgr.transform(triangle_row, utils.matrix.mirror_matrix(Point3D.create((columns - 1) * (width + sx)/2, 0, 0), Vector3D.create(-1, 1, 1)))
        mgr.booleanOperation(result, triangle_row, adsk.fusion.BooleanTypes.UnionBooleanType)

    result_bb = result.preciseBoundingBox
    offset_x = face_length/2 - (result_bb.maxPoint.x + result_bb.minPoint.x)/2
    offset_y = face_width/2 - (result_bb.maxPoint.y + result_bb.minPoint.y)/2
    offset_z = -result_bb.minPoint.z
    mgr.transform(result, utils.matrix.translation_matrix(Vector3D.create(offset_x, offset_y, offset_z)))
    return result


def create_cross(face: adsk.fusion.BRepFace, cut: Vector3D,  inputs: TriangleInputs) -> adsk.fusion.BRepBody:
    mgr = adsk.fusion.TemporaryBRepManager.get()
    long_edge, short_edge = utils.brep.longest_and_adjecent_edge_of_face(face)
    face_length = long_edge.length
    face_width = short_edge.length
    height = face_width - 2 * inputs.inset.value
    width = face_length - 2 * inputs.inset.value
    spacing = inputs.spacing.value

    alpha = math.atan(height/width)
    long_dx = (spacing/2) / math.sin(alpha)
    long_dy  = (spacing/2) / math.cos(alpha)
    beta = math.pi/2 - alpha
    short_dx = (spacing/2) / math.sin(beta)
    short_dy = (spacing/2) / math.cos(beta)

    long_triangle = utils.brep.isosceles_triangle(width - 2*long_dx, height/2 - long_dy, cut.length, inputs.fillet.value)
    mgr.transform(long_triangle, utils.matrix.translation_matrix(Vector3D.create(0, -height/2, 0)))
    short_triangle = utils.brep.isosceles_triangle(height - 2*short_dx, width/2 - short_dy, cut.length, inputs.fillet.value)
    mgr.transform(short_triangle, utils.matrix.combine_transforms([
        utils.matrix.translation_matrix(Vector3D.create(0, -width/2, 0)),
        utils.matrix.rotation_matrix(-math.pi/2, Vector3D.create(0, 0, 1), Point3D.create()),
    ]))
    result = mgr.copy(long_triangle)
    mgr.transform(long_triangle, utils.matrix.mirror_matrix(Point3D.create(), Vector3D.create(1, -1, 1)))
    mgr.booleanOperation(result, long_triangle, adsk.fusion.BooleanTypes.UnionBooleanType)
    mgr.booleanOperation(result, short_triangle, adsk.fusion.BooleanTypes.UnionBooleanType)
    mgr.transform(short_triangle, utils.matrix.mirror_matrix(Point3D.create(), Vector3D.create(-1, 1, 1)))
    mgr.booleanOperation(result, short_triangle, adsk.fusion.BooleanTypes.UnionBooleanType)

    result_bb = result.preciseBoundingBox
    offset_x = face_length/2 - (result_bb.maxPoint.x + result_bb.minPoint.x)/2
    offset_y = face_width/2 - (result_bb.maxPoint.y + result_bb.minPoint.y)/2
    mgr.transform(result, utils.matrix.translation_matrix(Vector3D.create(offset_x, offset_y, 0)))
    return result
    

def create_rounded_rect(face: adsk.fusion.BRepFace, cut: Vector3D,  inputs: TriangleInputs) -> adsk.fusion.BRepBody:
    mgr = adsk.fusion.TemporaryBRepManager.get()
    long_edge, short_edge = utils.brep.longest_and_adjecent_edge_of_face(face)
    face_length = long_edge.length
    face_width = short_edge.length
    height = face_width - 2 * inputs.inset.value
    width = face_length - 2 * inputs.inset.value

    result = utils.brep.rounded_rectangle(width, height, cut.length, inputs.fillet.value)
    result_bb = result.preciseBoundingBox
    offset_x = face_length/2 - (result_bb.maxPoint.x + result_bb.minPoint.x)/2
    offset_y = face_width/2 - (result_bb.maxPoint.y + result_bb.minPoint.y)/2
    mgr.transform(result, utils.matrix.translation_matrix(Vector3D.create(offset_x, offset_y, 0)))
    return result



# def froli(face: adsk.fusion.BRepFace, cut: Vector3D,  inputs: TriangleInputs) -> adsk.fusion.BRepBody:
#     long_edge, short_edge = utils.brep.longest_and_adjecent_edge_of_face(face)
#     face_length = long_edge.length
#     face_width = short_edge.length
#     vertical_space = face_width - 2 * inputs.inset.value
#     horizontal_space = face_length - 2 * inputs.inset.value

#     def spacing(length):
#         available = length - 13.6
#         remainders = [((available/x % 1) * x, x) for x in [16.3, 17.5, 18.7]]
#         remainders.sort(key=lambda x: x[0])
#         return remainders[0][1]

#     horizontal_grid = spacing(horizontal_space)
#     vertical_grid = spacing(vertical_space)

