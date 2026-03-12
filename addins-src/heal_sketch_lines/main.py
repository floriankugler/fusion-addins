from lib import addin, inputs, utils, ui_placement
from lib.fusionbootstrap.runtime import RuntimeInfo
import adsk.core, adsk.fusion
from typing import cast

_addin: addin.Addin | None = None

def run(context, runtime_info: RuntimeInfo):
    global _addin
    _addin = HealSketchLines(runtime_info)

def stop(context):
    global _addin
    if _addin:
        _addin.shutdown()
    _addin = None

class HealingInputs(inputs.Inputs):
    class Modes:
        PATCH_GAPS = inputs.DropDownInput.Item('Patch gaps with lines', 0)
        CREATE_SPLINE = inputs.DropDownInput.Item('Create healed spline', 1)

    def __init__(self, units_manager: adsk.core.UnitsManager):
        units = units_manager.defaultLengthUnits
        self.edges = inputs.SelectionByEntityTokenInput(
            id='edges',
            name='Edges',
            filter=[adsk.core.SelectionCommandInput.SketchCurves],
            lower_bound=1,
            upper_bound=0,
            tool_tip='Select sketch curves to heal',
        )
        self.tolerance = inputs.FloatInput(
            id='tolerance',
            name='Tolerance',
            default_value=1,
            tool_tip='Maximum distance between points to consider them for healing',
            units=units,
        )
        self.mode = inputs.DropDownInput(
            id='mode',
            name='Mode',
            options=[HealingInputs.Modes.PATCH_GAPS, HealingInputs.Modes.CREATE_SPLINE],
            default_value=HealingInputs.Modes.PATCH_GAPS.value,
            tool_tip='Choose whether to create one healed spline or patch gaps with lines.',
        )
        self.max_segment_length = inputs.FloatInput(
            id='max_segment_length',
            name='Max segment length',
            default_value=2,
            tool_tip='Distance between sampled fit points along the healed curve',
            units=units,
            update_visibility=lambda: self.mode.value == HealingInputs.Modes.CREATE_SPLINE.value,
        )
        super().__init__()


class HealSketchLines(addin.Addin):
    inputs: HealingInputs
    
    @property
    def plugin_name(self) -> str:
        return 'Heal Sketch Lines'

    @property
    def plugin_desc(self) -> str:
        return 'Heals missing connections between sketch curves'

    @property
    def plugin_tooltip(self) -> str:
        return 'Heals missing connections between sketch curves.'

    def get_ui_placement(self) -> ui_placement.UIPlacement:
        command = ui_placement.PlacementSpec(
            id=self.create_command_id,
            anchor_id='Offset',
        )
        return ui_placement.UIPlacement(
            panel_id='SketchModifyPanel',
            command=command,
        )

    def create_inputs(self) -> HealingInputs:
        return HealingInputs(self.app.activeProduct.unitsManager)

    def execute(self):
        selection = cast(list[adsk.fusion.SketchCurve], self.inputs.edges.value)
        if not selection:
            return
        sketch = selection[0].parentSketch
        handles: list[adsk.fusion.SketchCurve] = []
        for spline in sketch.sketchCurves.sketchFittedSplines:
            for p in spline.fitPoints:
                if tangent := spline.getTangentHandle(p):
                    handles.append(tangent)
                if curvature := spline.getCurvatureHandle(p):
                    handles.append(curvature)
        for spline in sketch.sketchCurves.sketchControlPointSplines:
            handles.extend(spline.controlFrameLines)

        filtered_selection = [curve for curve in selection if curve not in handles]
        if self.inputs.mode.value == HealingInputs.Modes.PATCH_GAPS.value:
            self.patch_gaps_with_lines(sketch, filtered_selection)
            return

        nurbs: list[adsk.core.NurbsCurve3D] = [
            curve.geometry if isinstance(curve.geometry, adsk.core.NurbsCurve3D) else curve.geometry.asNurbsCurve # type: ignore
            for curve in filtered_selection
        ]
        while len(nurbs) > 0:
            joined = self.join_nurbs(nurbs)
            points = self.fit_points_from_nurbs(joined)
            if len(points) < 2:
                continue

            fit_points = adsk.core.ObjectCollection.create()
            for point in points:
                fit_points.add(point)

            spline = sketch.sketchCurves.sketchFittedSplines.add(fit_points)
            if spline and self.is_closed_curve(joined):
                spline.isClosed = True

        for curve in selection:
            curve.isConstruction = True

    def patch_gaps_with_lines(self, sketch: adsk.fusion.Sketch, selection: list[adsk.fusion.SketchCurve]) -> None:
        remaining = [self.curve_endpoints(curve) for curve in selection]
        remaining = [entry for entry in remaining if entry is not None]

        while len(remaining) > 0:
            chain_start, chain_start_curve, chain_end, chain_end_curve = remaining.pop(0)
            while True:
                next_curve = self.find_next_curve_for_patch(chain_start, chain_end, remaining)
                if next_curve is None:
                    break
                idx, chain_side, other_side = next_curve
                other_start, other_start_curve, other_end, other_end_curve = remaining.pop(idx)

                if chain_side == 'end':
                    chain_sketch_point = chain_end
                    chain_curve = chain_end_curve
                else:
                    chain_sketch_point = chain_start
                    chain_curve = chain_start_curve

                if other_side == 'start':
                    other_sketch_point = other_start
                    other_far_sketch_point = other_end
                    other_far_curve = other_end_curve
                    other_curve = other_start_curve
                else:
                    other_sketch_point = other_end
                    other_far_sketch_point = other_start
                    other_far_curve = other_start_curve
                    other_curve = other_end_curve

                self.create_patch_line(
                    sketch,
                    chain_sketch_point,
                    chain_curve,
                    other_sketch_point,
                    other_curve,
                )

                if chain_side == 'end':
                    chain_end = other_far_sketch_point
                    chain_end_curve = other_far_curve
                else:
                    chain_start = other_far_sketch_point
                    chain_start_curve = other_far_curve

            self.create_patch_line(
                sketch,
                chain_start,
                chain_start_curve,
                chain_end,
                chain_end_curve,
            )

    def create_patch_line(
        self,
        sketch: adsk.fusion.Sketch,
        point1: adsk.fusion.SketchPoint,
        curve1: adsk.fusion.SketchCurve,
        point2: adsk.fusion.SketchPoint,
        curve2: adsk.fusion.SketchCurve,
    ) -> None:
        if point1.geometry.distanceTo(point2.geometry) <= 1e-9:
            return
        if self.within_tolerance(point1.geometry, point2.geometry) is None:
            return

        line: adsk.fusion.SketchLine | None = None
        try:
            line = sketch.sketchCurves.sketchLines.addByTwoPoints(point1, point2)
            if not line:
                return
            if line.startSketchPoint != point1:
                sketch.geometricConstraints.addCoincident(line.startSketchPoint, point1)
            if line.endSketchPoint != point2:
                sketch.geometricConstraints.addCoincident(line.endSketchPoint, point2)
        except Exception as error:
            utils.fusion.log(f'Error creating patch line: {error}')
            if line and line.isValid and line.isDeletable:
                line.deleteMe()

    def curve_endpoints(
        self, curve: adsk.fusion.SketchCurve
    ) -> tuple[adsk.fusion.SketchPoint, adsk.fusion.SketchCurve, adsk.fusion.SketchPoint, adsk.fusion.SketchCurve] | None:
        start_sketch_point = adsk.fusion.SketchPoint.cast(getattr(curve, 'startSketchPoint', None))
        end_sketch_point = adsk.fusion.SketchPoint.cast(getattr(curve, 'endSketchPoint', None))
        if not start_sketch_point or not end_sketch_point:
            return None
        return start_sketch_point, curve, end_sketch_point, curve

    def find_next_curve_for_patch(
        self,
        start: adsk.fusion.SketchPoint,
        end: adsk.fusion.SketchPoint,
        curves: list[tuple[adsk.fusion.SketchPoint, adsk.fusion.SketchCurve, adsk.fusion.SketchPoint, adsk.fusion.SketchCurve]],
    ) -> tuple[int, str, str] | None:
        result: list[tuple[float, int, str, str]] = []
        for idx, (other_start, _, other_end, _) in enumerate(curves):
            dist = self.within_tolerance(end.geometry, other_start.geometry)
            if dist is not None:
                result.append((dist, idx, 'end', 'start'))
            dist = self.within_tolerance(end.geometry, other_end.geometry)
            if dist is not None:
                result.append((dist, idx, 'end', 'end'))
            dist = self.within_tolerance(start.geometry, other_end.geometry)
            if dist is not None:
                result.append((dist, idx, 'start', 'end'))
            dist = self.within_tolerance(start.geometry, other_start.geometry)
            if dist is not None:
                result.append((dist, idx, 'start', 'start'))

        if result:
            result.sort(key=lambda x: x[0])
            _, idx, chain_side, other_side = result[0]
            return idx, chain_side, other_side

    def join_nurbs(self, nurbs: list[adsk.core.NurbsCurve3D]) -> adsk.core.NurbsCurve3D:
        joined = nurbs.pop(0)
        if not nurbs:
            return joined
        while next := self.find_next_curve(joined, nurbs):
            next_curve, before, reversed = next
            nurbs.remove(next_curve)
            if reversed:
                next_curve.reverse()
            if before:
                joined = self.merge_curves(next_curve, joined)
            else:
                joined = self.merge_curves(joined, next_curve)
        return joined

    def merge_curves(self, curve1: adsk.core.NurbsCurve3D, curve2: adsk.core.NurbsCurve3D) -> adsk.core.NurbsCurve3D:
        _, _, end = curve1.evaluator.getEndPoints()
        _, start, _ = curve2.evaluator.getEndPoints()
        if start.distanceTo(end) < 1e-9:
            return curve1.merge(curve2)
        else:
            gap = adsk.core.Line3D.create(start, end)
            gap_nurbs = gap.asNurbsCurve
            return curve1.merge(gap_nurbs).merge(curve2)


    def find_next_curve(self, curve: adsk.core.NurbsCurve3D, curves: list[adsk.core.NurbsCurve3D]) -> tuple[adsk.core.NurbsCurve3D, bool, bool] | None:
        _, start, end = curve.evaluator.getEndPoints()
        if self.within_tolerance(start, end) and utils.sketch.nurbs_length(curve) > self.inputs.tolerance.value:
            return None
        
        result: list[tuple[float, adsk.core.NurbsCurve3D, bool, bool]] = []
        for other_curve in curves:
            _, other_start, other_end = other_curve.evaluator.getEndPoints()
            dist = self.within_tolerance(end, other_start)
            if dist is not None:
                result.append((dist, other_curve, False, False))
            dist = self.within_tolerance(end, other_end)
            if dist is not None:
                result.append((dist, other_curve, False, True))
            dist = self.within_tolerance(start, other_end)
            if dist is not None:
                result.append((dist, other_curve, True, False))
            dist = self.within_tolerance(start, other_start)
            if dist is not None:
                result.append((dist, other_curve, True, True))

        if result:
            result.sort(key=lambda x: x[0])
            return result[0][1:4]
    
    def within_tolerance(self, point1: adsk.core.Point3D, point2: adsk.core.Point3D) -> float | None:
        dist = point1.distanceTo(point2)
        if dist <= self.inputs.tolerance.value:
            return dist
        return None

    def fit_points_from_nurbs(self, curve: adsk.core.NurbsCurve3D) -> list[adsk.core.Point3D]:
        evaluator = curve.evaluator
        ok, start_param, end_param = evaluator.getParameterExtents()
        if not ok:
            return []

        ok, total_length = evaluator.getLengthAtParameter(start_param, end_param)
        if not ok:
            return []

        ok, start_point = evaluator.getPointAtParameter(start_param)
        if not ok:
            return []
        ok, end_point = evaluator.getPointAtParameter(end_param)
        if not ok:
            return []

        spacing = max(1e-6, self.inputs.max_segment_length.value)
        points: list[adsk.core.Point3D] = [start_point]
        if total_length > spacing:
            offset = spacing
            while offset < total_length:
                ok, param = evaluator.getParameterAtLength(start_param, offset)
                if not ok:
                    break
                ok, point = evaluator.getPointAtParameter(param)
                if not ok:
                    break
                points.append(point)
                offset += spacing
        points.append(end_point)
        points = self.dedupe_points(points)
        if len(points) > 2 and self.is_effectively_closed_points(points):
            # Fitted splines should not repeat the first point as the last point.
            # Closure is handled via spline.isClosed = True.
            points.pop()
        return points

    def dedupe_points(self, points: list[adsk.core.Point3D]) -> list[adsk.core.Point3D]:
        if not points:
            return []
        result = [points[0]]
        for point in points[1:]:
            if point.distanceTo(result[-1]) > 1e-9:
                result.append(point)
        return result

    def is_effectively_closed_points(self, points: list[adsk.core.Point3D]) -> bool:
        return points[0].distanceTo(points[-1]) <= 1e-6

    def is_closed_curve(self, curve: adsk.core.NurbsCurve3D) -> bool:
        ok, start, end = curve.evaluator.getEndPoints()
        return bool(ok and start.distanceTo(end) <= 1e-6 and utils.sketch.nurbs_length(curve) > 1e-6)
