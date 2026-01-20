import adsk.fusion
from adsk.core import Vector3D
from dataclasses import dataclass
import Rhombuses
import math
from Shared import CoordinateSystem, PatternInputs


@dataclass
class FroliParameters:
    inset: float
    fillet: float
    spacing: float

def create_froli_from_inputs(coords: CoordinateSystem,  inputs: PatternInputs) -> adsk.fusion.BRepBody:
    params = FroliParameters(
        inset=inputs.inset.value,
        fillet=inputs.fillet.value,
        spacing=inputs.spacing.value,
    )
    return create_froli_grid(coords, params)


def create_froli_grid(coords: CoordinateSystem,  params: FroliParameters) -> adsk.fusion.BRepBody:
    face_length = coords[1].length
    face_width = coords[2].length
    vertical_space = face_width - 1 # Give at least 5mm spacing on each side
    horizontal_space = face_length - 1

    def spacing(length: float) -> float:
        available = length - 13.6 # Subtract width of one froli element
        remainders = [((available/x % 1) * x, x) for x in [16.3, 17.5, 18.7]]
        remainders.sort(key=lambda x: x[0])
        return remainders[0][1]

    horizontal_grid = spacing(horizontal_space)
    vertical_grid = spacing(vertical_space)

    tan_alpha = horizontal_grid/vertical_grid
    alpha = math.atan(tan_alpha)
    x_inset = params.spacing / (2 * math.cos(alpha))
    y_inset = x_inset / tan_alpha
    width = horizontal_grid - 2 * x_inset
    height = vertical_grid - 2 * y_inset

    return Rhombuses.create_rhombuses(coords, Rhombuses.RhombusParameters(
        width=width,
        height=height,
        spacing=params.spacing,
        inset=params.inset,
        fillet=params.fillet,
        adaptive=False
    ))
