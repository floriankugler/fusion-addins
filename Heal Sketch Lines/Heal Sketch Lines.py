import sys, os
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
shared_folder = os.path.join(parent_dir, "SharedUtils")
if current_dir not in sys.path: sys.path.append(current_dir)
if shared_folder not in sys.path: sys.path.append(shared_folder)
import Addin, Inputs, utils
import adsk.core, adsk.fusion
from typing import cast
utils.misc.force_reload_modules('Addin', 'Inputs', 'utils')

_addin: Addin.Addin | None = None

def run(context):
    global _addin
    _addin = HealSketchLines()

def stop(context):
    global _addin
    del _addin

class HealingInputs(Inputs.Inputs):
    def __init__(self, units_manager: adsk.core.UnitsManager):
        units = units_manager.defaultLengthUnits
        self.edges = Inputs.SelectionByEntityTokenInput('edges', 'Edges', [adsk.core.SelectionCommandInput.SketchCurves], 1, 0, 'Select sketch curves to heal')
        self.tolerance = Inputs.FloatInput('tolerance', 'Tolerance', 0.1, 'Maximum distance between points to consider them for healing', units)
        super().__init__()


class HealSketchLines(Addin.Addin):
    plugin_id = 'antonHealSketchLines'
    plugin_name = 'Heal Sketch Lines'
    plugin_desc = 'Heals missing connections between sketch curves'
    plugin_tooltip = 'Heals missing connections between sketch curves.'
    plugin_ui_panel = 'SketchModifyPanel'
    plugin_ui_command = 'Offset'
    inputs: HealingInputs

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
