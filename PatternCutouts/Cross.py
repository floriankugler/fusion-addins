import math
import adsk.fusion
from adsk.core import Point3D, Vector3D
from dataclasses import dataclass
import utils
from Shared import CoordinateSystem, PatternInputs


@dataclass
class CrossParameters:
    spacing: float
    inset: float
    fillet: float

def create_cross_from_inputs(coords: CoordinateSystem,  inputs: PatternInputs) -> adsk.fusion.BRepBody:
    params = CrossParameters(
        spacing=inputs.spacing.value,
        inset=inputs.inset.value,
        fillet=inputs.fillet.value,
    )
    return create_cross(coords, params)


def create_cross(coords: CoordinateSystem,  params: CrossParameters) -> adsk.fusion.BRepBody:
    mgr = adsk.fusion.TemporaryBRepManager.get()
    face_length = coords[1].length
    face_width = coords[2].length
    height = face_width - 2 * params.inset
    width = face_length - 2 * params.inset
    spacing = params.spacing

    alpha = math.atan(height/width)
    long_dx = (spacing/2) / math.sin(alpha)
    long_dy  = (spacing/2) / math.cos(alpha)
    beta = math.pi/2 - alpha
    short_dx = (spacing/2) / math.sin(beta)
    short_dy = (spacing/2) / math.cos(beta)

    long_triangle = utils.brep.isosceles_triangle(width - 2*long_dx, height/2 - long_dy, coords[3].length, params.fillet)
    mgr.transform(long_triangle, utils.matrix.translation_matrix(Vector3D.create(0, -height/2, 0)))
    short_triangle = utils.brep.isosceles_triangle(height - 2*short_dx, width/2 - short_dy, coords[3].length, params.fillet)
    mgr.transform(short_triangle, utils.matrix.combine_transforms([
        utils.matrix.translation_matrix(Vector3D.create(0, -width/2, 0)),
        utils.matrix.rotation_matrix(-math.pi/2, Vector3D.create(0, 0, 1), Point3D.create()),
    ]))
    result = mgr.copy(long_triangle)
    mgr.transform(long_triangle, utils.matrix.mirror_matrix(Point3D.create(), Vector3D.create(1, -1, 1)))
    mgr.booleanOperation(result, long_triangle, adsk.fusion.BooleanTypes.UnionBooleanType) # type: ignore
    mgr.booleanOperation(result, short_triangle, adsk.fusion.BooleanTypes.UnionBooleanType) # type: ignore
    mgr.transform(short_triangle, utils.matrix.mirror_matrix(Point3D.create(), Vector3D.create(-1, 1, 1)))
    mgr.booleanOperation(result, short_triangle, adsk.fusion.BooleanTypes.UnionBooleanType) # type: ignore

    result_bb = result.preciseBoundingBox
    offset_x = face_length/2 - (result_bb.maxPoint.x + result_bb.minPoint.x)/2
    offset_y = face_width/2 - (result_bb.maxPoint.y + result_bb.minPoint.y)/2
    mgr.transform(result, utils.matrix.translation_matrix(Vector3D.create(offset_x, offset_y, 0)))
    return result
