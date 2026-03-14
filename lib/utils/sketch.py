import adsk.core, adsk.fusion
from typing import cast, NamedTuple
from .. import errors

def nurbs_length(nurbs: adsk.core.NurbsCurve3D) -> float:
    _, start, end = nurbs.evaluator.getParameterExtents()
    _, length = nurbs.evaluator.getLengthAtParameter(start, end)
    return length

class OrientedCurve(NamedTuple):
    curve: adsk.fusion.SketchCurve
    flipped: bool

class NextCurve(NamedTuple):
    curve: adsk.fusion.SketchCurve
    point: adsk.fusion.SketchPoint
    distance: float

def sequenced_curves(curves: list[adsk.fusion.SketchCurve], tolerance: float) -> list[OrientedCurve]:
    if not curves:
        return []

    def find_next_curve(point: adsk.fusion.SketchPoint, curves: list[adsk.fusion.SketchCurve]) -> NextCurve | None:
        candidates: list[NextCurve] = []
        for curve in curves:
            start = curve.startSketchPoint  # type: ignore
            end = curve.endSketchPoint # type: ignore
            dist = point.geometry.distanceTo(start.geometry)
            if dist < tolerance:
                candidates.append(NextCurve(curve=curve, point=start, distance=dist))
            dist = point.geometry.distanceTo(end.geometry)
            if dist < tolerance:
                candidates.append(NextCurve(curve=curve, point=end, distance=dist))
        candidates.sort(key=lambda x: x.distance)
        if not candidates:
            return None
        return candidates[0]

    remaining_curves = list(curves)
    ordered = [OrientedCurve(curve=remaining_curves.pop(), flipped=False)]

    while remaining_curves:
        first_curve = ordered[0]
        last_curve = ordered[-1]
        start_point = first_curve.curve.startSketchPoint if not first_curve.flipped else first_curve.curve.endSketchPoint # type: ignore
        end_point = last_curve.curve.endSketchPoint if not last_curve.flipped else last_curve.curve.startSketchPoint # type: ignore

        next = find_next_curve(end_point, remaining_curves)
        previous = find_next_curve(start_point, remaining_curves)

        if next and (not previous or next.distance <= previous.distance):
            flipped = next.point == next.curve.endSketchPoint # type: ignore
            ordered.append(OrientedCurve(curve=next.curve, flipped=flipped))
            remaining_curves.remove(next.curve)
        elif previous:
            flipped = previous.point == previous.curve.startSketchPoint # type: ignore
            ordered.insert(0, OrientedCurve(curve=previous.curve, flipped=flipped))
            remaining_curves.remove(previous.curve)

        if not next and not previous:
            break

    if remaining_curves:
        raise errors.InvalidInputError("Failed to sequence transfer curves into a continuous path.")
    return ordered
    
def rebuild_curves_as_spline(
    curves: list[adsk.fusion.SketchCurve],
    sketch: adsk.fusion.Sketch,
    sample_spacing: float,
    min_fit_point_spacing: float,
    tolerance: float,
    close_loop: bool,
) -> adsk.fusion.SketchCurve | None:
    if not curves:
        return None
    sequenced = sequenced_curves(curves, tolerance)

    sampled_points: list[adsk.core.Point3D] = []
    for oriented_curve in sequenced:
        points = sample_curve_points(
            oriented_curve.curve, sample_spacing, oriented_curve.flipped
        )
        for point in points:
            if (
                sampled_points
                and sampled_points[-1].distanceTo(point) < min_fit_point_spacing
            ):
                continue
            sampled_points.append(point)

    if len(sampled_points) < 2:
        return None

    if close_loop and sampled_points[0].distanceTo(sampled_points[-1]) < tolerance:
        sampled_points.append(sampled_points[0])

    spline: adsk.fusion.SketchCurve | None = None
    try:
        # Degree-5 control-point spline provides C2 continuity.
        if len(sampled_points) >= 6:
            spline = sketch.sketchCurves.sketchControlPointSplines.add(
                cast(list[adsk.core.Base], sampled_points),
                adsk.fusion.SplineDegrees.SplineDegreeFive,  # type: ignore
            )

        elif len(sampled_points) >= 4:
            spline = sketch.sketchCurves.sketchControlPointSplines.add(
                cast(list[adsk.core.Base], sampled_points),
                adsk.fusion.SplineDegrees.SplineDegreeThree,  # type: ignore
            )
    except:
        spline = None

    if not spline:
        fit_points = adsk.core.ObjectCollection.create()
        for point in sampled_points:
            fit_points.add(point)
        spline = sketch.sketchCurves.sketchFittedSplines.add(fit_points)

    return spline


def sample_curve_points(
    curve: adsk.fusion.SketchCurve,
    spacing: float,
    reverse: bool,
) -> list[adsk.core.Point3D]:
    geometry = curve.geometry  # type: ignore
    nurbs = geometry if isinstance(geometry, adsk.core.NurbsCurve3D) else geometry.asNurbsCurve  # type: ignore
    evaluator = nurbs.evaluator
    _, start_param, end_param = evaluator.getParameterExtents()
    _, total_length = evaluator.getLengthAtParameter(start_param, end_param)

    points: list[adsk.core.Point3D] = []
    _, start_point = evaluator.getPointAtParameter(start_param)
    points.append(start_point)
    offset = spacing
    while offset < total_length:
        _, param = evaluator.getParameterAtLength(start_param, offset)
        _, point = evaluator.getPointAtParameter(param)
        points.append(point)
        offset += spacing

    _, end_point = evaluator.getPointAtParameter(end_param)
    points.append(end_point)

    if reverse:
        points.reverse()
    return points
