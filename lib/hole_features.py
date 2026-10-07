"""Native Hole features drilled into a board face from sketch points.

Follows the hole rules in AGENTS.md: fixed-depth holes are flat-bottomed
(tip angle 180 deg), through holes run to the opposite face instead of a
fixed depth. Adapted from door_latch_native's private helper.
"""
from typing import cast

import adsk.core
import adsk.fusion

from . import utils


def create_simple_hole(
    face: adsk.fusion.BRepFace,
    sketch: adsk.fusion.Sketch,
    center_points: list[adsk.fusion.SketchPoint],
    diameter_expression: str,
    depth_expression: str | None,
    name: str,
) -> adsk.fusion.HoleFeature:
    """Drills `center_points` (points of `sketch`, which lies on `face`)
    into the face's body. `depth_expression` None makes through holes."""
    if not center_points:
        raise RuntimeError(f"'{name}' requires at least one hole center.")
    component = face.body.parentComponent
    hole_features = component.features.holeFeatures
    hole_input = hole_features.createSimpleInput(
        adsk.core.ValueInput.createByString(diameter_expression)
    )
    if not hole_input:
        raise RuntimeError(f"Fusion failed to initialize '{name}'.")
    if not hole_input.setPositionBySketchPoints(
        adsk.core.ObjectCollection.createWithArray(
            cast(list[adsk.core.Base], center_points)
        )
    ):
        raise RuntimeError(f"Fusion rejected the positions of '{name}'.")

    opposite_face = utils.brep.get_opposite_face(face)
    normal_into_body = utils.brep.normal_towards_face(face, opposite_face)
    # The natural hole direction is opposite the sketch normal.
    sketch_normal = sketch.xDirection.crossProduct(sketch.yDirection)
    natural_direction = sketch_normal.copy()
    natural_direction.scaleBy(-1)
    hole_input.isDefaultDirection = (
        natural_direction.dotProduct(normal_into_body) > 0
    )
    if depth_expression is None:
        if not hole_input.setOneSideToExtent(
            opposite_face,
            False,
            normal_into_body,
        ):
            raise RuntimeError(f"Fusion rejected the to-face extent of '{name}'.")
    else:
        if not hole_input.setDistanceExtent(
            adsk.core.ValueInput.createByString(depth_expression)
        ):
            raise RuntimeError(f"Fusion rejected the depth of '{name}'.")
        hole_input.tipAngle = adsk.core.ValueInput.createByString("180 deg")
    hole_input.participantBodies = [face.body]

    hole = hole_features.add(hole_input)
    if not hole:
        raise RuntimeError(f"Fusion failed to create '{name}'.")
    hole.name = name
    sketch.isVisible = False
    return hole


def depth_parameter(hole: adsk.fusion.HoleFeature) -> adsk.fusion.ModelParameter | None:
    """The depth of a fixed-depth hole, None for other extents."""
    extent = adsk.fusion.DistanceExtentDefinition.cast(hole.extentDefinition)
    return extent.distance if extent else None
