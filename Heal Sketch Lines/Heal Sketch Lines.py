import sys, os
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
shared_folder = os.path.join(parent_dir, "SharedUtils")
if current_dir not in sys.path: sys.path.append(current_dir)
if shared_folder not in sys.path: sys.path.append(shared_folder)
import Addin, Inputs, Combine, utils
import adsk.core, adsk.fusion
from typing import cast
utils.misc.force_reload_modules('Addin', 'Inputs', 'Combine', 'utils')

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
    inputs: HealingInputs

    def create_inputs(self) -> HealingInputs:
        return HealingInputs(self.app.activeProduct.unitsManager)

    def execute(self):
        selection = cast(list[adsk.fusion.SketchCurve], self.inputs.edges.value)
        curves: list[tuple[adsk.fusion.SketchCurve, adsk.fusion.SketchPoint, adsk.fusion.SketchPoint]] = [(c, c.startSketchPoint, c.endSketchPoint) for c in selection if not c.isConstruction] # type: ignore
        if not curves:
            return
        sketch = curves[0][0].parentSketch
        constrained_points: list[adsk.fusion.SketchPoint] = []
        for curve, start, end in curves:
            for point in [start, end]:
                if point in constrained_points:
                    continue
                for other_curve, other_start, other_end in curves:
                    if curve == other_curve:
                        continue
                    for other_point in [other_start, other_end]:
                        if other_point in constrained_points:
                            continue
                        dist = point.geometry.distanceTo(other_point.geometry)
                        if dist <= self.inputs.tolerance.value:
                            for constraint in point.geometricConstraints:
                                if isinstance(constraint, adsk.fusion.CoincidentConstraint):
                                    if constraint.point == point and constraint.entity == other_point or constraint.point == other_point and constraint.entity == point:
                                        break
                            else:
                                sketch.geometricConstraints.addCoincident(point, other_point)
                                constrained_points.extend([point, other_point])

