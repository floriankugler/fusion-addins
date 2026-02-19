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
            default_value=0.1,
            tool_tip='Maximum distance between points to consider them for healing',
            units=units,
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

        nurbs: list[adsk.core.NurbsCurve3D] = [
            curve.geometry if isinstance(curve.geometry, adsk.core.NurbsCurve3D) else curve.geometry.asNurbsCurve # type: ignore
            for curve in selection if curve not in handles
        ]
        while len(nurbs) > 0:
            joined = self.join_nurbs(nurbs)
            sketch.sketchCurves.sketchFixedSplines.addByNurbsCurve(joined)

        for curve in selection:
            curve.isConstruction = True

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
            if dist := self.within_tolerance(end, other_start):
                result.append((dist, other_curve, False, False))
            elif dist := self.within_tolerance(end, other_end):
                result.append((dist, other_curve, False, True))
            elif dist := self.within_tolerance(start, other_end):
                result.append((dist, other_curve, True, False))
            elif dist := self.within_tolerance(start, other_start):
                result.append((dist, other_curve, True, True))

        if result:
            result.sort(key=lambda x: x[0])
            return result[0][1:4]
    
    def within_tolerance(self, point1: adsk.core.Point3D, point2: adsk.core.Point3D) -> float | None:
        dist = point1.distanceTo(point2)
        if dist <= self.inputs.tolerance.value:
            return dist
        return None
