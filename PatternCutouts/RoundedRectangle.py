import adsk.fusion
from adsk.core import Vector3D
from dataclasses import dataclass
import utils
from Shared import CoordinateSystem, PatternInputs


@dataclass
class RoundedRectangleParameters:
    inset: float
    fillet: float

def create_rounded_rectangle_from_inputs(coords: CoordinateSystem,  inputs: PatternInputs) -> adsk.fusion.BRepBody:
    params = RoundedRectangleParameters(
        inset=inputs.inset.value,
        fillet=inputs.fillet.value,
    )
    return create_rounded_rect(coords, params)

def create_rounded_rect(coords: CoordinateSystem,  params: RoundedRectangleParameters) -> adsk.fusion.BRepBody:
    face_length = coords[1].length
    face_width = coords[2].length
    height = face_width - 2 * params.inset
    width = face_length - 2 * params.inset

    result = utils.brep.rounded_rectangle(width, height, coords[3].length, params.fillet)
    result_bb = result.preciseBoundingBox
    offset_x = face_length/2 - (result_bb.maxPoint.x + result_bb.minPoint.x)/2
    offset_y = face_width/2 - (result_bb.maxPoint.y + result_bb.minPoint.y)/2
    return utils.brep.transformed(result, utils.matrix.translation_matrix(Vector3D.create(offset_x, offset_y, 0)))
