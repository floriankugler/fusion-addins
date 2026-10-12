"""Reads the master document into a snapshot file (`lang.core.snapshot_types`).

Runs inside Fusion's Python; load it like the emitter (see the package
docstring), then `snapshot.write_snapshot(path)`. It only reads the design.

What it takes, from the root component and every component below it,
in world millimetres (proxies carry each occurrence's placement):

- every construction plane, as origin and normal;
- every sketch, as one contour: its curves that are not construction
  geometry, sampled at 0.1 mm and chained (`snapshot_format.chain`);
- every solid body, as its axis-aligned bounding box, flagged when the
  body is not an axis-aligned cuboid;
- every user parameter, lengths in mm and angles in degrees.

Items in the root keep their names; items inside components are named by
the dotted path of component names (`Bett.oben`), and a component's only
body by the component's path (`Moebel.Kueche`), otherwise each body by its
own name after the path (`Sitzbank.Sitz`). Names starting with a double
underscore are left out, also a component's (with everything in it), and
so are linked components, which belong to other documents. Duplicate names
and sketches that are not one chain are listed as problems; the build
reports them when such a name is used.
"""
from __future__ import annotations

import math
import os
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, cast

import adsk.core
import adsk.fusion

from .snapshot_format import SKIP_PREFIX, Collector, Point3, dumps

if TYPE_CHECKING:
    from ..core.snapshot_types import SnapshotDict

#: mm per centimetre (the API unit).
CM = 10.0
#: Curves are sampled so that no point of the curve is further than this
#: from the polyline (cm; 0.1 mm).
STROKE_TOLERANCE = 0.01
_LENGTH_UNITS = {"mm", "cm", "m", "in", "ft", "um", "mil", "yd"}
_ANGLE_UNITS = {"deg", "rad"}

Log = Callable[[str], None]


@dataclass
class Summary:
    planes: int = 0
    contours: int = 0
    boxes: int = 0
    parameters: int = 0
    skipped: int = 0
    linked: int = 0
    problems: list[str] = field(default_factory=list[str])
    path: str = ""

    def text(self) -> str:
        lines = [f"{self.planes} planes, {self.contours} contours, {self.boxes} boxes, "
                 f"{self.parameters} parameters -> {self.path}"]
        if self.skipped:
            lines.append(f"left out: {self.skipped} item(s) named __...")
        if self.linked:
            lines.append(f"left out: {self.linked} linked component(s)")
        lines += [f"problem: {p}" for p in self.problems]
        return "\n".join(lines)


def _mm(p: adsk.core.Point3D) -> Point3:
    return (p.x * CM, p.y * CM, p.z * CM)


def _vec(v: adsk.core.Vector3D) -> Point3:
    return (v.x, v.y, v.z)


@dataclass
class _Context:
    """A component as it sits in the root: the occurrence it is reached
    through (None for the root), the dotted path of component names that
    names its items ("" for the root), and where it is, for messages."""
    component: adsk.fusion.Component
    occurrence: adsk.fusion.Occurrence | None
    path: str
    where: str


def _contexts(root: adsk.fusion.Component, collector: Collector, summary: Summary) -> list[_Context]:
    contexts = [_Context(root, None, "", "root")]
    for occurrence in root.allOccurrences:
        # Skip linked components and anything below a skipped one.
        chain: list[adsk.fusion.Occurrence] = []
        o: adsk.fusion.Occurrence | None = occurrence
        while o is not None:
            chain.append(o)
            # The stubs say Occurrence; it is None at the top level.
            o = cast(adsk.fusion.Occurrence | None, o.assemblyContext)
        # Counted once, at the outermost occurrence that is left out.
        linked = [o.isReferencedComponent for o in chain]
        if any(linked):
            if linked[0] and not any(linked[1:]):
                summary.linked += 1
            continue
        skipped = [o.component.name.startswith(SKIP_PREFIX) for o in chain]
        if any(skipped):
            if skipped[0] and not any(skipped[1:]):
                collector.skipped += 1
            continue
        path = ".".join(o.component.name for o in reversed(chain))
        contexts.append(_Context(occurrence.component, occurrence, path, occurrence.fullPathName))
    return contexts


def _planes(ctx: _Context, collector: Collector) -> None:
    planes = ctx.component.constructionPlanes
    for i in range(planes.count):
        plane = planes.item(i)
        if ctx.occurrence is not None:
            plane = plane.createForAssemblyContext(ctx.occurrence)
        geometry = plane.geometry
        collector.plane(ctx.path, plane.name, ctx.where, _mm(geometry.origin), _vec(geometry.normal))


def _strokes(curve: adsk.fusion.SketchCurve) -> list[Point3]:
    """The curve sampled to a polyline in world mm; a RuntimeError when
    Fusion cannot sample it."""
    # Every concrete sketch curve has worldGeometry; the stubs declare it per class.
    geometry = cast(adsk.core.Curve3D, getattr(curve, "worldGeometry"))
    evaluator = geometry.evaluator
    ok, t0, t1 = evaluator.getParameterExtents()
    if not ok:
        raise RuntimeError(f"no parameter range for {curve.objectType}")
    ok, points = evaluator.getStrokes(t0, t1, STROKE_TOLERANCE)
    if not ok:
        raise RuntimeError(f"could not sample {curve.objectType}")
    return [_mm(p) for p in points]


def _sketches(ctx: _Context, collector: Collector) -> None:
    sketches = ctx.component.sketches
    for i in range(sketches.count):
        sketch = sketches.item(i)
        if sketch.name.startswith(SKIP_PREFIX):
            collector.skipped += 1
            continue
        if ctx.occurrence is not None:
            sketch = sketch.createForAssemblyContext(ctx.occurrence)
        polylines: list[list[Point3]] = []
        curves = sketch.sketchCurves
        try:
            for k in range(curves.count):
                curve = curves.item(k)
                if curve.isConstruction:
                    continue
                polylines.append(_strokes(curve))
        except RuntimeError as error:
            # one sketch's bad curve is a problem of that contour, not of the snapshot
            collector.problem("contours", ctx.path, sketch.name, ctx.where, str(error))
            continue
        origin, normal = _sketch_plane(sketch)
        collector.contour(ctx.path, sketch.name, ctx.where, polylines, origin, normal)


def _sketch_plane(sketch: adsk.fusion.Sketch) -> tuple[Point3, Point3]:
    """The sketch's origin and normal in world space. `transform` maps
    sketch space to model space and, on a proxy, already includes the
    occurrence's placement (checked in Fusion 2026-10-11)."""
    m = sketch.transform
    origin = adsk.core.Point3D.create(0, 0, 0)
    normal = adsk.core.Vector3D.create(0, 0, 1)
    origin.transformBy(m)
    normal.transformBy(m)
    return _mm(origin), _vec(normal)


def _bodies(ctx: _Context, collector: Collector) -> None:
    bodies = ctx.component.bRepBodies
    count = bodies.count
    measure = adsk.core.Application.get().measureManager
    x_axis = adsk.core.Vector3D.create(1, 0, 0)
    y_axis = adsk.core.Vector3D.create(0, 1, 0)
    # A component's only body is named by the component's path.
    only = count == 1 and ctx.occurrence is not None
    path = ctx.path.rpartition(".")[0] if only else ctx.path
    for i in range(count):
        body = bodies.item(i)
        name = ctx.component.name if only else body.name
        if ctx.occurrence is not None:
            body = body.createForAssemblyContext(ctx.occurrence)
        if not body.isSolid:
            collector.problem("boxes", path, name, ctx.where, "a surface body, not a solid")
            continue
        box = measure.getOrientedBoundingBox(body, x_axis, y_axis)
        c = box.centerPoint
        size = (box.length, box.width, box.height)
        lo = (c.x - size[0] / 2, c.y - size[1] / 2, c.z - size[2] / 2)
        hi = (c.x + size[0] / 2, c.y + size[1] / 2, c.z + size[2] / 2)
        # An axis-aligned cuboid, and only that, fills its axis-aligned box.
        cuboid = math.isclose(body.volume, size[0] * size[1] * size[2], rel_tol=1e-6)
        collector.box(path, name, ctx.where, [v * CM for v in lo], [v * CM for v in hi], cuboid)


def _parameters(design: adsk.fusion.Design, collector: Collector) -> None:
    params = design.userParameters
    for i in range(params.count):
        p = params.item(i)
        unit = p.unit
        if unit in _LENGTH_UNITS:
            value = p.value * CM
        elif unit in _ANGLE_UNITS:
            value = math.degrees(p.value)
        else:
            value = p.value
        collector.parameter(p.name, value, unit, p.expression)


def read_design(design: adsk.fusion.Design, source: str, summary: Summary | None = None) -> SnapshotDict:
    summary = summary or Summary()
    collector = Collector()
    for ctx in _contexts(design.rootComponent, collector, summary):
        _planes(ctx, collector)
        _sketches(ctx, collector)
        _bodies(ctx, collector)
    _parameters(design, collector)
    snapshot = collector.build(source)
    summary.planes = len(snapshot["planes"])
    summary.contours = len(snapshot["contours"])
    summary.boxes = len(snapshot["boxes"])
    summary.parameters = len(snapshot["parameters"])
    summary.skipped = collector.skipped
    summary.problems = [f"{p['kind']} {p['name']!r}: {p['message']}" for p in snapshot["problems"]]
    return snapshot


def write_snapshot(path: str, source: str | None = None, log: Log | None = None) -> Summary:
    """Writes the snapshot of the active design to `path`. `source` names
    the master in the file; by default the document's name."""
    app = adsk.core.Application.get()
    design = cast(adsk.fusion.Design | None, adsk.fusion.Design.cast(app.activeProduct))
    if design is None:
        raise RuntimeError("the active document is not a design")
    summary = Summary(path=path)
    snapshot = read_design(design, source or app.activeDocument.name, summary)
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(dumps(snapshot) + "\n")
    if log is not None:
        log(summary.text())
    return summary
