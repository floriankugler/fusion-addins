"""Builds a CAM plan's setups in its nested document (`cam_plan`).

Runs inside Fusion's Python, like `fusion`. Per material's document, after
`fusion.NestEmitter` has drawn the nest:

- the sketches first, every setup's, as they change the design and an
  operation made before a change keeps the model it was made against: per
  setup a hidden sketch `<setup> tabs` with its tab positions (Fusion takes
  a tab position only as a model entity, and a sketch point serves), and
  one `<setup> rests` with the regions a narrower cutter clears after a
  wider one; then `cam.checkValidity()` [`lib/auto_setup/builder.py`, found
  2026-08-15]. The sketches are never deleted (deleting one an operation
  refers to crashed Fusion);
- per blank a setup named as the plan names it: its models the parts'
  bodies on the blank, its stock a fixed box of the blank's rectangle and
  nominal thickness placed from the model's origin at the blank's corner,
  its top at the parts' top, its WCS the stock's top corner at the
  blank's corner, x along the blank's length. The box's height (Stock,
  Height (Z)) is the value the operator corrects to the measured
  thickness: the box's bottom offset is the parts' top less the height, so
  the box grows down from the top, and every height from the stock's
  bottom (the roughing's skin, the release, the through cuts) follows it,
  while what is measured from the model (a pocket's floor, a hole's
  bottom) keeps its depth from the top [verified 2026-10-17];
- each operation made from its template file (`createFromCAMTemplate2`),
  its parameters written as `cam_plan.param_writes` says, a bore's feed
  scaled, its geometry bound by position (`cam_plan`'s bindings), its tabs
  the sketch points of its positions; an operation that fails is reported
  and the next one goes on;
- `cam.generateToolpath(setup)` at the end, since Fusion may generate an
  operation the moment it is made, against the bare template.

`toolpath_report` checks the toolpaths once they are generated: each there,
valid, not empty (it cuts some length), with Fusion's errors and warnings.
"""
from __future__ import annotations

import gc
import math
import os
import time
from dataclasses import dataclass, field
from typing import Any, Callable, cast

import adsk.cam
import adsk.core
import adsk.fusion

from .cam_plan import (OPTIONAL, Binding, CamDocPlan, Cylinder, EdgePath, EdgeSample, FaceLoop, Floor,
                       OperationPlan, Region, SetupPlan, Silhouette, WallArc, bore_feed, chain_reverted, chamfer_reverted,
                       edge_on_line, edge_on_path, inside, loop_follows, on_circle, param_writes, plan_cam,
                       read_plan, region_samples, runs, template_path)
from .fusion import MM, Log, NestEmitter, new_document
from .nested import plan_nest
from .plan import Arc, Circle, Line, Point3

#: Fusion's workspace whose activation makes a document's CAM product.
CAM_WORKSPACE = "CAMEnvironment"
#: How close (mm) to vertical an axis or a normal is taken to be, as a
#: component of its unit vector.
VERTICAL = 1 - 1e-6
#: A 45 degree chamfer face's normal has this upward component.
CHAMFER_UP = (0.5, 0.9)

_MILLING = cast(adsk.cam.OperationTypes, adsk.cam.OperationTypes.MillingOperation)
_FIXED_BOX = cast(adsk.cam.SetupStockModes, adsk.cam.SetupStockModes.FixedBoxStock)
_OUTSIDE = cast(adsk.cam.LoopTypes, adsk.cam.LoopTypes.OnlyOutsideLoops)


@dataclass
class OperationReport:
    name: str
    kind: str
    features: int
    #: Features bound wholly; what was not, and what could not be set, in problems.
    bound: int = 0
    problems: list[str] = field(default_factory=list[str])


@dataclass
class SetupReport:
    name: str
    operations: list[OperationReport] = field(default_factory=list[OperationReport])
    problems: list[str] = field(default_factory=list[str])
    seconds: float = 0.0

    def summary(self) -> str:
        lines = [f"{self.name}: {len(self.operations)} operations in {self.seconds:.1f} s"]
        for op in self.operations:
            lines.append(f"  {op.name}: {op.bound} of {op.features} features")
            lines += [f"    problem: {p}" for p in op.problems]
        lines += [f"  problem: {p}" for p in self.problems]
        return "\n".join(lines)


@dataclass
class CamReport:
    material: str
    setups: list[SetupReport] = field(default_factory=list[SetupReport])
    problems: list[str] = field(default_factory=list[str])
    seconds: float = 0.0

    def failures(self) -> int:
        return len(self.problems) + sum(len(s.problems) + sum(len(o.problems) for o in s.operations)
                                        for s in self.setups)

    def summary(self) -> str:
        head = (f"CAM {self.material}: {len(self.setups)} setups, "
                f"{sum(len(s.operations) for s in self.setups)} operations in {self.seconds:.1f} s, "
                f"{self.failures()} problems; the measured thickness goes into each setup's stock height")
        return "\n".join([head] + [s.summary() for s in self.setups] + [f"  problem: {p}" for p in self.problems])


# -- the model, as the binding sees it --------------------------------------------------------------------

def _param(params: adsk.cam.CAMParameters, name: str) -> adsk.cam.CAMParameter | None:
    """A parameter by name, None where the operation has none (the stubs
    say it always has)."""
    return cast("adsk.cam.CAMParameter | None", params.itemByName(name))


def _number(parameter: adsk.cam.CAMParameter) -> float:
    return adsk.cam.FloatParameterValue.cast(parameter.value).value


def _entities(items: list[adsk.fusion.BRepEdge] | list[adsk.fusion.BRepFace] | list[adsk.fusion.SketchCurve]
              | list[adsk.fusion.BRepBody] | list[adsk.fusion.SketchPoint]) -> list[adsk.core.Base]:
    return list[adsk.core.Base](items)


def _mm(p: adsk.core.Point3D) -> Point3:
    return (p.x / MM, p.y / MM, p.z / MM)


def _pt(p: Point3) -> adsk.core.Point3D:
    return adsk.core.Point3D.create(p[0] * MM, p[1] * MM, p[2] * MM)


class _Body:
    """A part's body with its faces and edges read once (mm)."""

    def __init__(self, body: adsk.fusion.BRepBody):
        self.body = body
        self._planes: list[tuple[adsk.fusion.BRepFace, float, float, tuple[float, float]]] | None = None
        self._cylinders: list[tuple[adsk.fusion.BRepFace, tuple[float, float], float]] | None = None
        self._edges: list[tuple[adsk.fusion.BRepEdge, EdgeSample]] | None = None

    def planes(self) -> list[tuple[adsk.fusion.BRepFace, float, float, tuple[float, float]]]:
        """Its horizontal planar faces: the face, its height, its normal's
        z (+1 up, -1 down), a point on it."""
        if self._planes is None:
            self._planes = []
            self._cylinders = []
            for face in self.body.faces:
                geometry = face.geometry
                if isinstance(geometry, adsk.core.Plane):
                    point = face.pointOnFace
                    _ok, normal = face.evaluator.getNormalAtPoint(point)
                    if abs(normal.z) >= VERTICAL:
                        p = _mm(point)
                        self._planes.append((face, p[2], 1.0 if normal.z > 0 else -1.0, (p[0], p[1])))
                elif isinstance(geometry, adsk.core.Cylinder) and abs(geometry.axis.z) >= VERTICAL * geometry.axis.length:
                    o = _mm(geometry.origin)
                    self._cylinders.append((face, (o[0], o[1]), geometry.radius / MM))
        return self._planes

    def cylinders(self) -> list[tuple[adsk.fusion.BRepFace, tuple[float, float], float]]:
        self.planes()
        assert self._cylinders is not None
        return self._cylinders

    def edges(self) -> list[tuple[adsk.fusion.BRepEdge, EdgeSample]]:
        if self._edges is None:
            self._edges = [(edge, sample(edge)) for edge in self.body.edges]
        return self._edges


def sample(edge: adsk.fusion.BRepEdge) -> EdgeSample:
    """An edge as `cam_plan` tests it (mm)."""
    evaluator = edge.evaluator
    _ok, lo, hi = evaluator.getParameterExtents()
    _ok, mid = evaluator.getPointAtParameter((lo + hi) / 2)
    _ok, length = evaluator.getLengthAtParameter(lo, hi)
    geometry = edge.geometry
    radius = geometry.radius / MM if isinstance(geometry, (adsk.core.Arc3D, adsk.core.Circle3D)) else None
    return EdgeSample(_mm(edge.startVertex.geometry), _mm(edge.endVertex.geometry), _mm(mid), radius, length / MM)


def _arc_center(edge: adsk.fusion.BRepEdge) -> Point3 | None:
    geometry = edge.geometry
    if isinstance(geometry, (adsk.core.Arc3D, adsk.core.Circle3D)) and abs(geometry.normal.z) >= VERTICAL:
        return _mm(geometry.center)
    return None


# -- the emitter ------------------------------------------------------------------------------------------

class CamEmitter:
    """Builds one material's setups in its nested document (see the module
    docstring); `templates` names a template's file by its stem."""

    def __init__(self, design: adsk.fusion.Design, templates: Callable[[str], str], log: Log | None = None):
        self.design = design
        self.root = design.rootComponent
        self.templates = templates
        self.log: Log = log or (lambda _: None)
        self._loaded: dict[str, adsk.cam.CAMTemplate] = {}
        self._tab_points: dict[str, dict[Point3, adsk.fusion.SketchPoint]] = {}
        self._regions: dict[int, list[list[adsk.fusion.SketchCurve]]] = {}
        self._sketches: list[adsk.fusion.Sketch] = []
        self._bodies: dict[str, _Body] = {}

    def emit(self, doc: CamDocPlan) -> CamReport:
        t0 = time.perf_counter()
        report = CamReport(doc.material)
        blanks = find_blanks(self.design)
        # every design change before the first operation
        for setup in doc.setups:
            try:
                self._sketch(setup)
            except RuntimeError as error:
                report.problems.append(f"{setup.name}: its sketch could not be drawn ({error}).")
        cam = cam_product(self.design)
        cam.checkValidity()
        for setup in doc.setups:
            self.log(f"setup {setup.name}")
            bodies = blanks.get(setup.blank, {})
            report.setups.append(self._setup(cam, setup, bodies))
        for sketch in self._sketches:
            sketch.isLightBulbOn = False
        report.seconds = time.perf_counter() - t0
        return report

    # -- sketches -------------------------------------------------------------------------------------

    def _sketch(self, setup: SetupPlan) -> None:
        positions = setup.tab_positions()
        if positions:
            sketch = self._new_sketch(f"{setup.name} tabs")
            self._tab_points[setup.name] = {p: sketch.sketchPoints.add(sketch.modelToSketchSpace(_pt(p)))
                                            for p in positions}
        regions = setup.regions()
        if regions:
            sketch = self._new_sketch(f"{setup.name} rests")
            for region in regions:
                self._regions[id(region)] = [self._draw(sketch, loop) for loop in region.loops]

    def _new_sketch(self, name: str) -> adsk.fusion.Sketch:
        sketch = self.root.sketches.add(self.root.xYConstructionPlane)
        sketch.name = name
        self._sketches.append(sketch)
        return sketch

    @staticmethod
    def _draw(sketch: adsk.fusion.Sketch, loop: list[Line | Arc | Circle]) -> list[adsk.fusion.SketchCurve]:
        """A closed loop of sketch curves, each starting at the point the
        one before ends at."""
        curves: list[adsk.fusion.SketchCurve] = []
        first: adsk.fusion.SketchPoint | None = None
        last: adsk.fusion.SketchPoint | None = None
        for k, c in enumerate(loop):
            end = first if k == len(loop) - 1 and first is not None else None
            if isinstance(c, Circle):
                curves.append(sketch.sketchCurves.sketchCircles.addByCenterRadius(_pt(c.center), c.radius * MM))
                continue
            start: adsk.fusion.SketchPoint | adsk.core.Point3D = last if last is not None else _pt(c.a)
            stop: adsk.fusion.SketchPoint | adsk.core.Point3D = end if end is not None else _pt(c.b)
            if isinstance(c, Line):
                curve = sketch.sketchCurves.sketchLines.addByTwoPoints(start, stop)
                a, b = curve.startSketchPoint, curve.endSketchPoint
            else:
                curve = sketch.sketchCurves.sketchArcs.addByThreePoints(start, _pt(c.mid), stop)
                # Fusion stores an arc counter-clockwise: its ends may be the other way round
                a, b = curve.startSketchPoint, curve.endSketchPoint
                if a.geometry.distanceTo(_pt(c.a)) > b.geometry.distanceTo(_pt(c.a)):
                    a, b = b, a
            if first is None:
                first = a
            last = b
            curves.append(curve)
        return curves

    # -- the setup ------------------------------------------------------------------------------------

    def _setup(self, cam: adsk.cam.CAM, setup: SetupPlan, bodies: dict[str, adsk.fusion.BRepBody]) -> SetupReport:
        t0 = time.perf_counter()
        report = SetupReport(setup.name)
        missing = [p for p in setup.parts if p not in bodies]
        if missing:
            report.problems.append(f"no body for {', '.join(missing)} on blank {setup.blank}")
        models = [bodies[p] for p in setup.parts if p in bodies]
        if not models:
            report.problems.append("no part on the blank was drawn: no setup")
            return report
        try:
            fusion_setup = self._make_setup(cam, setup, models, report)
        except RuntimeError as error:
            report.problems.append(f"the setup could not be made ({error})")
            return report
        for op in setup.operations:
            self.log(f"  {op.name}")
            op_report = OperationReport(op.name, op.kind, len(op.features))
            report.operations.append(op_report)
            try:
                self._operation(fusion_setup, setup, op, bodies, op_report)
            except RuntimeError as error:
                op_report.problems.append(f"the operation could not be made ({error})")
        try:
            cam.generateToolpath(fusion_setup)
        except RuntimeError as error:
            report.problems.append(f"the toolpaths could not be generated ({error}); generate the setup by hand")
        report.seconds = time.perf_counter() - t0
        return report

    def _make_setup(self, cam: adsk.cam.CAM, setup: SetupPlan, models: list[adsk.fusion.BRepBody],
                    report: SetupReport) -> adsk.cam.Setup:
        inp = cam.setups.createInput(_MILLING)
        inp.models = _entities(models)
        inp.name = setup.name
        inp.stockMode = _FIXED_BOX
        (x, y, _z), (w, h, t) = setup.corner, setup.size
        for name, expression in (
                ("wcs_orientation_mode", "'modelOrientation'"), ("wcs_origin_mode", "'stockPoint'"),
                # the top corner the stock's x and y run away from (Auto Setup measured it)
                ("wcs_origin_boxPoint", "'top 1'"),
                ("job_groundStockModelOrigin", "true"),
                ("job_stockFixedX", f"{w:.6g} mm"), ("job_stockFixedY", f"{h:.6g} mm"), ("job_stockFixedZ", f"{t:.6g} mm"),
                ("job_stockFixedXMode", "'model'"), ("job_stockFixedXOffset", f"{x:.6g} mm"),
                ("job_stockFixedYMode", "'model'"), ("job_stockFixedYOffset", f"{y:.6g} mm"),
                # grounded, the box's bottom lies where its offset says: its top stays at the parts' top
                # whatever height the operator gives it
                ("job_stockFixedZMode", "'model'"), ("job_stockFixedZOffset", f"{setup.top:.6g} mm - job_stockFixedZ")):
            inp.parameters.itemByName(name).expression = expression
        fusion_setup = cam.setups.add(inp)
        if fusion_setup.name != setup.name:
            # (written again where it was not taken: Fusion makes a name it takes for another's unique)
            fusion_setup.name = setup.name
        # where Fusion put the stock: the blank, its top at the parts' top
        params = fusion_setup.parameters
        got = [_number(params.itemByName(n)) / MM for n in
               ("stockXLow", "stockXHigh", "stockYLow", "stockYHigh", "stockZLow", "stockZHigh")]
        want = [x, x + w, y, y + h, setup.top - t, setup.top]
        if any(abs(g - e) > 0.01 for g, e in zip(got, want)):
            report.problems.append(f"the stock lies at {[round(g, 3) for g in got]}, not at the blank's {want}")
        return fusion_setup

    # -- an operation ---------------------------------------------------------------------------------

    def _template(self, stem: str) -> adsk.cam.CAMTemplate:
        template = self._loaded.get(stem)
        if template is None:
            path = self.templates(stem)
            if not os.path.exists(path):
                raise RuntimeError(f"no template file {path}")
            template = self._loaded[stem] = adsk.cam.CAMTemplate.createFromFile(path)
        return template

    def _operation(self, fusion_setup: adsk.cam.Setup, setup: SetupPlan, op: OperationPlan,
                   bodies: dict[str, adsk.fusion.BRepBody], report: OperationReport) -> None:
        inp = adsk.cam.CreateFromCAMTemplateInput.create()
        inp.camTemplate = self._template(op.template)
        created = [o for o in (adsk.cam.Operation.cast(c) for c in fusion_setup.createFromCAMTemplate2(inp)) if o]
        if not created:
            raise RuntimeError(f"template {op.template} made no operation")
        bound: list[int] = []
        for k, operation in enumerate(created):
            operation.name = op.name if len(created) == 1 else f"{op.name} – {operation.name}"
            self._write(operation, op, report)
            n = self._bind(operation, setup, op, bodies, report, k == 0)
            bound.append(n)
            self._tabs(operation, setup, op, report)
        report.bound = min(bound)

    def _write(self, operation: adsk.cam.Operation, op: OperationPlan, report: OperationReport) -> None:
        params = operation.parameters
        for name, expression in param_writes(op):
            parameter = _param(params, name)
            if parameter is None:
                if name not in OPTIONAL:
                    report.problems.append(f"{operation.name}: has no {name} to set to {expression}")
                continue
            if parameter.expression == expression:
                continue
            try:
                parameter.expression = expression
            except RuntimeError as error:
                report.problems.append(f"{operation.name}: {name} could not be set to {expression} ({error})")
        if op.kind == "bore" and op.params.feed_scale is not None:
            parameter = _param(params, "tool_feedCutting")
            if parameter is None:
                report.problems.append(f"{operation.name}: has no cutting feed to scale")
                return
            feed = bore_feed(_number(parameter), op.params.feed_scale)
            if feed is not None:
                parameter.expression = f"{feed:.0f} mm/min"

    def _tabs(self, operation: adsk.cam.Operation, setup: SetupPlan, op: OperationPlan,
              report: OperationReport) -> None:
        if op.params.tabs is None:
            return
        parameter = _param(operation.parameters, "tabPositions")
        points = self._tab_points.get(setup.name, {})
        chosen = [points[p] for p in op.params.tabs.positions if p in points]
        if parameter is None or len(chosen) < len(op.params.tabs.positions):
            report.problems.append(f"{operation.name}: {len(chosen)} of {len(op.params.tabs.positions)} tab "
                                   "positions" + ("" if parameter is not None else "; it takes none"))
        if parameter is not None and chosen:
            adsk.cam.CadObjectParameterValue.cast(parameter.value).value = _entities(chosen)

    # -- geometry -------------------------------------------------------------------------------------

    def _body(self, path: str, body: adsk.fusion.BRepBody) -> _Body:
        found = self._bodies.get(path)
        if found is None:
            found = self._bodies[path] = _Body(body)
        return found

    def _bind(self, operation: adsk.cam.Operation, setup: SetupPlan, op: OperationPlan,
              bodies: dict[str, adsk.fusion.BRepBody], report: OperationReport, first: bool) -> int:
        """Binds the operation's features; how many were bound wholly.
        What could not be bound is reported once, for the template's first
        operation."""
        parameter = _param(operation.parameters, op.selection)
        if parameter is None:
            raise RuntimeError(f"its template's operation has no {op.selection} for the geometry")
        bound = 0
        faces: list[adsk.fusion.BRepFace] = []
        #: The faces bound so far, by part and face: each once.
        chosen: set[tuple[str, int]] = set()
        contours: adsk.cam.CadContours2dParameterValue | None = None
        selections: adsk.cam.CurveSelections | None = None
        if op.selection not in ("holeFaces", "circularFaces"):
            contours = adsk.cam.CadContours2dParameterValue.cast(parameter.value)
            selections = contours.getCurveSelections()
            selections.clear()
        for feature in op.features:
            body = bodies.get(feature.part)
            if body is None:
                if first:
                    report.problems.append(f"{feature.label}: no body")
                continue
            whole = True
            for binding in feature.bindings:
                try:
                    why = self._bind_one(binding, self._body(feature.part, body), faces, selections, chosen)
                except RuntimeError as error:
                    why = f"Fusion refused it ({error})"
                if why is not None:
                    whole = False
                    if first:
                        report.problems.append(f"{feature.label}: {why}")
            bound += whole
        if contours is not None and selections is not None:
            contours.applyCurveSelections(selections)
        elif faces:
            adsk.cam.CadObjectParameterValue.cast(parameter.value).value = _entities(faces)
        return bound

    def _bind_one(self, b: Binding, body: _Body, faces: list[adsk.fusion.BRepFace],
                  selections: adsk.cam.CurveSelections | None, chosen: set[tuple[str, int]]) -> str | None:
        """Binds one binding; None, or why it was not."""
        if isinstance(b, Cylinder):
            found = [f for f, axis, r in body.cylinders() if on_circle(b.center, b.d, axis, r)]
            if not found:
                return f"no cylinder {b.d:g} across at {_xy(b.center)}"
            for f in found:
                if (b.part, f.tempId) not in chosen:
                    chosen.add((b.part, f.tempId))
                    faces.append(f)
            return None
        assert selections is not None
        if isinstance(b, Silhouette):
            silhouette = selections.createNewSilhouetteSelection()
            silhouette.inputGeometry = _entities([body.body])
            silhouette.loopType = _OUTSIDE
            # else the silhouette is every model's of the setup
            silhouette.isSetupModelSelected = False
            return None
        if isinstance(b, Floor):
            samples = region_samples(b.rings)
            found = [f for f, z, up, p in body.planes()
                     if up > 0 and abs(z - b.z) <= 0.01 and (inside(p, b.rings) or _holds(f, samples, z))]
            if not found:
                return f"no floor at {b.z:g} in its region near {_xy(b.rings[0][0])}"
            for f in found:
                key = (b.part, f.tempId)
                if key in chosen:
                    continue                          # a floor pockets that overlap share
                chosen.add(key)
                pocket = selections.createNewPocketSelection()
                pocket.inputGeometry = _entities([f])
            return None
        if isinstance(b, FaceLoop):
            for z in b.levels:
                edges = self._face_loop(body, b.ring, z)
                if edges is not None:
                    chain = selections.createNewChainSelection()
                    chain.inputGeometry = _entities(edges)
                    rings = [b.ring]
                    chain.isReverted = chain_reverted(*_middle(edges[0]),
                                                      lambda p: inside(p, rings) == b.waste_inside)
                    return None
            return f"no loop of edges follows its ring at the top or the bottom near {_xy(b.ring[0])}"
        if isinstance(b, Region):
            curves = self._regions.get(id(b))
            if curves is None:
                return "its region was not drawn"
            for k, loop in enumerate(curves):
                chain = selections.createNewChainSelection()
                chain.inputGeometry = _entities(loop)
                polygon = [[_xy2(c.a if not isinstance(c, Circle) else c.center) for c in b.loops[k]]]
                if len(polygon[0]) >= 3:
                    chain.isReverted = chain_reverted(*_middle(loop[0]), lambda p: inside(p, polygon) == (k == 0))
            return None
        if isinstance(b, WallArc):
            for z in b.levels:
                found = [(e, s) for e, s in body.edges() if self._on_wall(e, b, z)]
                if found:
                    # the cutter is narrower than the dog bone: it runs inside its circle
                    self._open_chains(selections, found, lambda p: math.dist(p, b.center) < b.d / 2)
                    return None
            return f"no arc {b.d:g} across about {_xy(b.center)}"
        if isinstance(b, EdgePath):
            found = [(e, s) for e, s in body.edges() if edge_on_path(s, b.points, b.closed, b.z)]
            if not found:
                return f"no edge at {b.z:g} along its path near {_xy(b.points[0])}"
            self._chamfer_chains(selections, found)
            return None
        found = [(e, s) for e, s in body.edges() if edge_on_line(s, b.start, b.end, b.z)]
        if not found:
            return f"no edge at {b.z:g} from {_xy(b.start)} to {_xy(b.end)}"
        self._open_chains(selections, found, None)
        return None

    @staticmethod
    def _on_wall(edge: adsk.fusion.BRepEdge, b: WallArc, z: float) -> bool:
        center = _arc_center(edge)
        if center is None or abs(center[2] - z) > 0.01:
            return False
        geometry = edge.geometry
        assert isinstance(geometry, (adsk.core.Arc3D, adsk.core.Circle3D))
        return on_circle(b.center, b.d, (center[0], center[1]), geometry.radius / MM)

    def _face_loop(self, body: _Body, ring: list[tuple[float, float]], z: float) -> list[adsk.fusion.BRepEdge] | None:
        samples = {e.tempId: s for e, s in body.edges()}
        for face, fz, _up, _p in body.planes():
            if abs(fz - z) > 0.01:
                continue
            for loop in face.loops:
                edges = list(loop.edges)
                if loop_follows([samples.get(e.tempId) or sample(e) for e in edges], ring, z):
                    return edges
        return None

    @staticmethod
    def _open_chains(selections: adsk.cam.CurveSelections, found: list[tuple[adsk.fusion.BRepEdge, EdgeSample]],
                     waste: Callable[[tuple[float, float]], bool] | None) -> None:
        """A chain per run of the edges; turned so the tool runs on the
        `waste` side, where one is given (a Trace follows its curve's
        middle)."""
        for run, closed in runs([s for _e, s in found]):
            chain = selections.createNewChainSelection()
            if not closed and chain.isOpenAllowed:
                chain.isOpen = True
            edges = [found[k][0] for k in run]
            chain.inputGeometry = _entities(edges)
            if waste is not None:
                chain.isReverted = chain_reverted(*_middle(edges[0]), waste)

    @staticmethod
    def _chamfer_chains(selections: adsk.cam.CurveSelections,
                        found: list[tuple[adsk.fusion.BRepEdge, EdgeSample]]) -> None:
        """One chain per run of a chamfer's lower edges, every edge handed
        over (left to itself Fusion closes an open chain along whatever
        edges it finds), turned so the tool runs on the chamfer's open
        side."""
        for run, closed in runs([s for _e, s in found]):
            edges = [found[k][0] for k in run]
            chain = selections.createNewChainSelection()
            if not closed and chain.isOpenAllowed:
                chain.isOpen = True
            chain.inputGeometry = _entities(edges)
            reverted = _chamfer_side(edges[0])
            if reverted is not None:
                chain.isReverted = reverted


def _middle(curve: adsk.fusion.BRepEdge | adsk.fusion.SketchCurve) -> tuple[Point3, Point3]:
    """A curve's middle point (mm) and its direction there, as it runs."""
    # (a sketch's curves have their geometry in their own classes)
    evaluator = curve.evaluator if isinstance(curve, adsk.fusion.BRepEdge) else cast(Any, curve).worldGeometry.evaluator
    _ok, lo, hi = evaluator.getParameterExtents()
    _ok, point = evaluator.getPointAtParameter((lo + hi) / 2)
    _ok, tangent = evaluator.getTangent((lo + hi) / 2)
    return _mm(point), (tangent.x, tangent.y, tangent.z)


def _xy2(p: Point3) -> tuple[float, float]:
    return (p[0], p[1])


def _holds(face: adsk.fusion.BRepFace, points: list[tuple[float, float]], z: float) -> bool:
    """Whether one of the points (mm, at `z`) lies on the face."""
    evaluator = face.evaluator
    for p in points:
        ok, param = evaluator.getParameterAtPoint(_pt((p[0], p[1], z)))
        if ok and evaluator.isParameterOnFace(param):
            return True
    return False


def _chamfer_side(edge: adsk.fusion.BRepEdge) -> bool | None:
    """Whether the chain from `edge`, a chamfer's lower edge, must be
    reversed; None where no chamfer face borders it."""
    evaluator = edge.evaluator
    _ok, lo, hi = evaluator.getParameterExtents()
    _ok, tangent = evaluator.getTangent((lo + hi) / 2)
    _ok, point = evaluator.getPointAtParameter((lo + hi) / 2)
    for face in edge.faces:
        _ok, normal = face.evaluator.getNormalAtPoint(point)
        if CHAMFER_UP[0] <= normal.z <= CHAMFER_UP[1]:
            return chamfer_reverted((tangent.x, tangent.y, tangent.z), (normal.x, normal.y, normal.z))
    return None


def _xy(p: tuple[float, float]) -> str:
    return f"({p[0]:.1f}, {p[1]:.1f})"


# -- the document -------------------------------------------------------------------------------------------

def find_blanks(design: adsk.fusion.Design) -> dict[str, dict[str, adsk.fusion.BRepBody]]:
    """A nested document's blanks (`fusion.NestEmitter`): per blank's name
    its parts' bodies by path, in the root's context."""
    out: dict[str, dict[str, adsk.fusion.BRepBody]] = {}
    for sheet in design.rootComponent.occurrences:
        for blank in sheet.childOccurrences:
            name = blank.component.name
            if not name.startswith("blank "):
                continue
            out[name[len("blank "):]] = {body.name: body for body in blank.bRepBodies}
    return out


def cam_product(design: adsk.fusion.Design) -> adsk.cam.CAM:
    """The document's CAM product, made by activating the Manufacture
    workspace where it has none yet."""
    products = design.parentDocument.products
    product = products.itemByProductType("CAMProductType") if _has_cam(products) else None
    if product is None:
        workspace = adsk.core.Application.get().userInterface.workspaces.itemById(CAM_WORKSPACE)
        workspace.activate()
        product = products.itemByProductType("CAMProductType")
    cam = cast("adsk.cam.CAM | None", adsk.cam.CAM.cast(product))
    if cam is None:
        raise RuntimeError("the document has no CAM product")
    return cam


def _has_cam(products: adsk.core.Products) -> bool:
    return any(products.item(i).productType == "CAMProductType" for i in range(products.count))


def emit_cam(cam_file: object, nest: object, layout: object, repo: str, material: str | None = None,
             design_type: str = "direct", log: Log | None = None) -> list[tuple[object, CamReport]]:
    """Draws a planned nest into a new document per material (or the one
    named), then builds its setups: per document the nest's report and the
    CAM report."""
    plan: Any = cam_file
    cams = {d.material: d for d in plan_cam(plan, nest, material)}

    def templates(stem: str) -> str:
        return template_path(plan, stem, repo)

    out: list[tuple[object, CamReport]] = []
    for doc in plan_nest(nest, cast(Any, layout), material):
        design = new_document(design_type)
        gc.disable()
        try:
            nest_report = NestEmitter(design, log).emit_nest(doc)
            out.append((nest_report, CamEmitter(design, templates, log).emit(cams[doc.material])))
        finally:
            gc.enable()
    return out


def emit_cam_file(path: str, repo: str, material: str | None = None, design_type: str = "direct",
                  log: Log | None = None) -> list[tuple[object, CamReport]]:
    """Draws a plan file (`cam.json`) with the nest and the layout beside it."""
    cam_file, nest, layout = read_plan(path)
    return emit_cam(cam_file, nest, layout, repo, material, design_type, log)


# -- checking the toolpaths ---------------------------------------------------------------------------------

def toolpath_report(cam: adsk.cam.CAM, setup_names: list[str] | None = None) -> list[dict[str, object]]:
    """Per operation of the setups named (all where None), once generated:
    its setup and name, whether it has a valid toolpath, how far it cuts
    (mm) and how long it runs (s), and Fusion's error and warning."""
    out: list[dict[str, object]] = []
    for setup in cam.setups:
        if setup_names is not None and setup.name not in setup_names:
            continue
        for item in setup.allOperations:
            op = cast("adsk.cam.Operation | None", adsk.cam.Operation.cast(item))
            if op is None:
                continue
            feed, seconds = 0.0, 0.0
            if op.hasToolpath:
                timing = cam.getMachiningTime(op, 100, 1000, 0)
                feed, seconds = timing.feedDistance / MM, timing.machiningTime
            out.append({"setup": setup.name, "operation": op.name, "toolpath": op.hasToolpath,
                        "valid": op.isToolpathValid, "generating": op.isGenerating, "feed_mm": round(feed, 1),
                        "seconds": round(seconds, 1), "error": op.error if op.hasError else "",
                        "warning": op.warning if op.hasWarning else ""})
    return out


__all__ = ["CamEmitter", "CamReport", "SetupReport", "OperationReport", "find_blanks", "cam_product", "emit_cam",
           "emit_cam_file", "toolpath_report", "sample"]
