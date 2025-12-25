import math
import adsk.fusion
from adsk.core import Point3D, Vector3D
from dataclasses import dataclass
import utils
from Shared import CoordinateSystem, PatternInputs

@dataclass
class TriangleParameters:
    width: float
    height: float
    spacing: float
    inset: float
    fillet: float
    compensate_fillet: bool
    adaptive: bool

def create_triangles_from_inputs(coords: CoordinateSystem, inputs: PatternInputs) -> adsk.fusion.BRepBody:
    params = TriangleParameters(
        width=inputs.preferred_width.value,
        height=inputs.preferred_height.value,
        spacing=inputs.spacing.value,
        inset=inputs.inset.value,
        fillet=inputs.fillet.value,
        compensate_fillet=inputs.compensate_fillet.value,
        adaptive=inputs.adaptive.value,
    )
    return create_triangles(coords, params)

def create_triangles(coords: CoordinateSystem, params: TriangleParameters) -> adsk.fusion.BRepBody:
    mgr = adsk.fusion.TemporaryBRepManager.get()
    spacing = params.spacing * 2

    face_length = coords[1].length
    face_width = coords[2].length
    vertical_space = face_width - 2 * params.inset
    horizontal_space = face_length - 2 * params.inset
    rows = max(1, math.floor((vertical_space + spacing/2) / (params.height + spacing/2)))
    columns = max(1, math.floor((horizontal_space + spacing) / (params.width + spacing)))
    width = params.width
    height = params.height
    ratio = width/height


    def point_angle(width, height):
        """
        Compute the angle at the tip of the triangle given width and height.
        """
        base_angle = math.atan(height/(width/2))
        return math.pi - 2 * base_angle

    def fillet_height_offset(point_angle):
        """
        Compute how much height is "lost" due to the fillet at the triangle point.
        Returns a positive number.
        """
        return (params.fillet/math.sin(point_angle/2) - params.fillet) if params.compensate_fillet else 0

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
    
    if params.adaptive:
        width = (horizontal_space - (columns - 1) * spacing) / columns
        height_lower = width/ratio * 0.5
        height_upper = width/ratio * 2
        if rows > 1:
            height = utils.misc.binary_search(height_lower, height_upper, spacing_deviation, 0, 0.1)
        else:
            height = utils.misc.binary_search(height_lower, height_upper, height_deviation, 0, 0.1)
        vertical_spacing = compute_vertical_spacing(height, point_angle(width, height))

    triangle = utils.brep.isosceles_triangle(width, height, coords[3].length, params.fillet)
    triangle_height = (triangle.boundingBox.maxPoint.y - triangle.boundingBox.minPoint.y) if params.compensate_fillet else height

    upside_down_triangle = mgr.copy(triangle)
    flip_transform = utils.matrix.mirror_matrix(Point3D.create(0, triangle_height/2, 0), Vector3D.create(1, -1, 1))
    mgr.transform(upside_down_triangle, flip_transform)

    row = mgr.copy(triangle)
    for idx in range(columns * 2 - 1):
        x = idx * (width + spacing) / 2
        t = mgr.copy(triangle if idx % 2 == 0 else upside_down_triangle)
        mgr.transform(t, utils.matrix.translation_matrix(Vector3D.create(x, 0, 0)))
        mgr.booleanOperation(row, t, adsk.fusion.BooleanTypes.UnionBooleanType) # type: ignore

    inverted_row = mgr.copy(row)
    mgr.transform(inverted_row, flip_transform)

    result = mgr.copy(row)
    for idx in range(1, rows):
        y = idx * (triangle_height + vertical_spacing)
        r = mgr.copy(row if idx % 2 == 0 else inverted_row)
        mgr.transform(r, utils.matrix.translation_matrix(Vector3D.create(0, y, 0)))
        mgr.booleanOperation(result, r, adsk.fusion.BooleanTypes.UnionBooleanType) # type: ignore

    result_bb = result.preciseBoundingBox
    offset_x = face_length/2 - (result_bb.maxPoint.x + result_bb.minPoint.x)/2
    offset_y = face_width/2 - (result_bb.maxPoint.y + result_bb.minPoint.y)/2
    mgr.transform(result, utils.matrix.translation_matrix(Vector3D.create(offset_x, offset_y, 0)))
    return result
