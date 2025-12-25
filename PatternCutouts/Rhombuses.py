import math
import adsk.fusion
from adsk.core import Point3D, Vector3D
from dataclasses import dataclass
import utils
from Shared import CoordinateSystem, PatternInputs


@dataclass
class RhombusParameters:
    width: float
    height: float
    spacing: float
    inset: float
    fillet: float
    adaptive: bool

def create_rhombuses_from_inputs(coords: CoordinateSystem,  inputs: PatternInputs) -> adsk.fusion.BRepBody:
    params = RhombusParameters(
        width=inputs.preferred_width.value,
        height=inputs.preferred_height.value,
        spacing=inputs.spacing.value,
        inset=inputs.inset.value,
        fillet=inputs.fillet.value,
        adaptive=inputs.adaptive.value,
    )
    return create_rhombuses(coords, params)

def create_rhombuses(coords: CoordinateSystem,  params: RhombusParameters) -> adsk.fusion.BRepBody:
    mgr = adsk.fusion.TemporaryBRepManager.get()
    face_length = coords[1].length
    face_width = coords[2].length
    vertical_space = face_width - 2 * params.inset
    horizontal_space = face_length - 2 * params.inset
    cut_length = coords[3].length

    def pattern_spacing(ratio: float) -> tuple[float, float]:
        angle = 2 * math.atan(ratio)
        sx = 2 * params.spacing * math.sin(angle/2) / math.sin(angle)
        sy = sx / ratio
        return (sx, sy)

    def pattern_dimensions(ratio: float) -> tuple[float, float, float, float]:
        sx, sy = pattern_spacing(ratio)
        w = (horizontal_space - (columns - 1) * sx) / columns
        h = w / ratio
        return (w, h, sx, sy)

    width = params.width
    height = params.height
    initial_ratio = width / height
    sx, sy = pattern_spacing(initial_ratio)
    rows = max(1, math.floor((vertical_space + sy) / (height + sy)))
    columns = max(1, math.floor((horizontal_space + sx) / (width + sx)))

    if params.adaptive:
        def height_deviation(ratio):
            _, h, _, sy = pattern_dimensions(ratio)
            actual_height = h * rows + sy * (rows - 1)
            return vertical_space - actual_height

        ratio_lower = initial_ratio * 0.5
        ratio_upper = initial_ratio * 1.5
        optimized_ratio = utils.misc.binary_search(ratio_lower, ratio_upper, height_deviation, 0, 0.1)
        width, height, sx, sy = pattern_dimensions(optimized_ratio)

    rhombus = utils.brep.rhombus(width, height, cut_length, params.fillet)
    row = mgr.copy(rhombus)
    for idx in range(columns):
        x = idx * (width + sx)
        t = mgr.copy(rhombus)
        mgr.transform(t, utils.matrix.translation_matrix(Vector3D.create(x, 0, 0)))
        mgr.booleanOperation(row, t, adsk.fusion.BooleanTypes.UnionBooleanType) # type: ignore

    result = mgr.copy(row)
    for idx in range(1, rows):
        y = idx * (height + sy)
        r = mgr.copy(row)
        mgr.transform(r, utils.matrix.translation_matrix(Vector3D.create(0, y, 0)))
        mgr.booleanOperation(result, r, adsk.fusion.BooleanTypes.UnionBooleanType) # type: ignore

    intermediate_row = mgr.copy(rhombus)
    for idx in range(columns - 1):
        t = mgr.copy(rhombus)
        mgr.transform(t, utils.matrix.translation_matrix(Vector3D.create(idx * (width + sx), 0, 0)))
        mgr.booleanOperation(intermediate_row, t, adsk.fusion.BooleanTypes.UnionBooleanType) # type: ignore
    mgr.transform(intermediate_row, utils.matrix.translation_matrix(Vector3D.create((width + sx)/2, 0, 0)))

    for idx in range(rows - 1):
        r = mgr.copy(intermediate_row)
        mgr.transform(r, utils.matrix.translation_matrix(Vector3D.create(0, (height + sy)/2 + idx * (height + sy)))) 
        mgr.booleanOperation(result, r, adsk.fusion.BooleanTypes.UnionBooleanType) # type: ignore

    if columns > 1:
        triangle_height = (height - sy) / 2
        triangle_angle = 2 * math.atan(width/height)
        triangle_width = math.tan(triangle_angle/2) * 2 * triangle_height
        triangle = utils.brep.isosceles_triangle(triangle_width, triangle_height, cut_length, params.fillet)
        triangle_row = mgr.copy(triangle)
        for idx in range(columns - 1):
            t = mgr.copy(triangle)
            mgr.transform(t, utils.matrix.translation_matrix(Vector3D.create(idx * (width + sx), 0, 0)))
            mgr.booleanOperation(triangle_row, t, adsk.fusion.BooleanTypes.UnionBooleanType) # type: ignore
        mgr.transform(triangle_row, utils.matrix.translation_matrix(Vector3D.create((width + sx)/2, -height/2, -cut_length/2)))
        mgr.booleanOperation(result, triangle_row, adsk.fusion.BooleanTypes.UnionBooleanType) # type: ignore
        mgr.transform(triangle_row, utils.matrix.mirror_matrix(Point3D.create(0, (rows - 1) * (height + sy)/2, 0), Vector3D.create(1, -1, 1)))
        mgr.booleanOperation(result, triangle_row, adsk.fusion.BooleanTypes.UnionBooleanType) # type: ignore

    if rows > 1:
        triangle_height = (width - sx) / 2
        triangle_angle = 2 * math.atan(height/width)
        triangle_width = math.tan(triangle_angle/2) * 2 * triangle_height
        triangle = utils.brep.isosceles_triangle(triangle_width, triangle_height, cut_length, params.fillet)
        mgr.transform(triangle, utils.matrix.rotation_matrix(-math.pi/2, Vector3D.create(0, 0, 1), Point3D.create()))
        triangle_row = mgr.copy(triangle)
        for idx in range(rows - 1):
            t = mgr.copy(triangle)
            mgr.transform(t, utils.matrix.translation_matrix(Vector3D.create(0, idx * (height + sy), 0)))
            mgr.booleanOperation(triangle_row, t, adsk.fusion.BooleanTypes.UnionBooleanType) # type: ignore
        mgr.transform(triangle_row, utils.matrix.translation_matrix(Vector3D.create(-width/2, (height + sy)/2, -cut_length/2)))
        mgr.booleanOperation(result, triangle_row, adsk.fusion.BooleanTypes.UnionBooleanType) # type: ignore
        mgr.transform(triangle_row, utils.matrix.mirror_matrix(Point3D.create((columns - 1) * (width + sx)/2, 0, 0), Vector3D.create(-1, 1, 1)))
        mgr.booleanOperation(result, triangle_row, adsk.fusion.BooleanTypes.UnionBooleanType) # type: ignore

    result_bb = result.preciseBoundingBox
    offset_x = face_length/2 - (result_bb.maxPoint.x + result_bb.minPoint.x)/2
    offset_y = face_width/2 - (result_bb.maxPoint.y + result_bb.minPoint.y)/2
    offset_z = -result_bb.minPoint.z
    mgr.transform(result, utils.matrix.translation_matrix(Vector3D.create(offset_x, offset_y, offset_z)))
    return result
