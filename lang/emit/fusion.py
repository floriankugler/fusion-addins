"""Draws an emit plan into a Fusion document with Fusion's own features.

Runs inside Fusion's Python; see the package docstring for how to load it.
Units: the plan is in millimetres, Fusion's API in centimetres.

What it draws, per part:

- the body: the outline as a temporary B-rep face, extruded by the
  thickness; the body is named by the part's path and lives in a component
  per scope;
- pockets: temporary B-rep faces on the part's face, extruded as one cut
  per batch (through-all or a distance);
- holes: one hole feature per hole, positioned by a point on the face, with
  a flat bottom, a distance extent or "to" the opposite face;
- chamfers: equal-distance chamfers on the edges a contour names;
- the part's facts (`PartFacts`) as a JSON attribute `lang`/`part` on the
  body, for the tools that work on the compiled document: Multi Arrange
  reads the grain and the face to machine from it.

Hardware (a slide's runners) is drawn as boxes, one body per piece, in a
component of its own below its scope's, named as the hardware is named in
its scope (`runners`).

Faces and edges are found by position, never by index, because every
feature gives the body new face identities. The feature calls and their
gotchas come from tools/perf/compile_bench.py.

A feature Fusion refuses does not stop the compile: the part goes on
without it and the report lists it under problems, beside the build's own
checks, so the document shows everything that worked.
"""
from __future__ import annotations

import gc
import json
import math
import time
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Callable, cast

import adsk.core
import adsk.fusion

from .loops import cross, dot, on_curve, oriented, polygon_loop
from .plan import (AXES, Arc, Axis, ChamferStep, CircleContour, Contour, EdgeContour, FaceRef, HardwarePlan,
                   HoleStep, Line, Loops, OutlineContour, PartPlan, Plan, PocketStep, Point3, ShapeContour, Step, Vec,
                   VGrooveStep, plan_layout)

if TYPE_CHECKING:
    from ..core.layout_types import Layout

#: Centimetres (the API unit) per millimetre.
MM = 0.1
#: The attribute that carries a part's facts on its body (read by
#: lib/multi_arrange/model.py). Its vectors are in the body's component
#: space, which is world space: every component is placed at the origin.
ATTRIBUTE_GROUP = "lang"
ATTRIBUTE_NAME = "part"
#: Positions closer than this (cm) coincide.
TOL = 1e-3

Log = Callable[[str], None]

# Fusion's stubs declare enum members as ints; the casts keep pyright quiet.
_NEW_BODY = cast(adsk.fusion.FeatureOperations, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
_CUT = cast(adsk.fusion.FeatureOperations, adsk.fusion.FeatureOperations.CutFeatureOperation)
_POSITIVE = cast(adsk.fusion.ExtentDirections, adsk.fusion.ExtentDirections.PositiveExtentDirection)
_NEGATIVE = cast(adsk.fusion.ExtentDirections, adsk.fusion.ExtentDirections.NegativeExtentDirection)
_UNION = cast(adsk.fusion.BooleanTypes, adsk.fusion.BooleanTypes.UnionBooleanType)
_DIRECT = cast(adsk.fusion.DesignTypes, adsk.fusion.DesignTypes.DirectDesignType)
_PARAMETRIC = cast(adsk.fusion.DesignTypes, adsk.fusion.DesignTypes.ParametricDesignType)
_DESIGN_DOCUMENT = cast(adsk.core.DocumentTypes, adsk.core.DocumentTypes.FusionDesignDocumentType)


@dataclass
class Report:
    parts: int = 0
    features: int = 0
    seconds: float = 0.0
    #: The build's own problems, as the layout lists them (its checks, notes).
    checks: list[str] = field(default_factory=list[str])
    #: What the emitter could not draw.
    problems: list[str] = field(default_factory=list[str])
    document: str = ""

    def summary(self) -> str:
        text = f"{self.parts} parts, {self.features} features in {self.seconds:.1f} s -> {self.document}"
        return (text + "".join(f"\n  check: {c}" for c in self.checks)
                + "".join(f"\n  problem: {p}" for p in self.problems))


# -- small geometry helpers ---------------------------------------------------------------------

def _pt(p: Point3) -> adsk.core.Point3D:
    return adsk.core.Point3D.create(p[0] * MM, p[1] * MM, p[2] * MM)


def _vec(v: Vec) -> adsk.core.Vector3D:
    return adsk.core.Vector3D.create(v[0], v[1], v[2])


def _coord(point: adsk.core.Point3D, axis: Axis) -> float:
    return (point.x, point.y, point.z)[AXES.index(axis)]


def _mm(p: Point3) -> Point3:
    """A point in Fusion's centimetres as millimetres."""
    return (p[0] / MM, p[1] / MM, p[2] / MM)


def _collection(items: list[adsk.core.Base]) -> adsk.core.ObjectCollection:
    coll = adsk.core.ObjectCollection.create()
    for item in items:
        coll.add(item)
    return coll


def _describe(step: Step) -> str:
    if isinstance(step, PocketStep):
        return f"pocket x{len(step.shapes)} on {step.face} depth {step.depth}"
    if isinstance(step, HoleStep):
        return f"hole d{step.d} x{len(step.points)} on {step.face} depth {step.depth} at {step.points[0]}"
    if isinstance(step, VGrooveStep):
        return f"v-groove on {step.face} depth {step.depth} from {step.start} to {step.end}"
    return f"chamfer {step.size} along {step.contour}"


# -- the emitter ---------------------------------------------------------------------------------

class Emitter:
    def __init__(self, design: adsk.fusion.Design, log: Log | None = None):
        self.design = design
        self.root = design.rootComponent
        self.tmp = adsk.fusion.TemporaryBRepManager.get()
        self.parametric = design.designType == _PARAMETRIC
        self.log: Log = log or (lambda _: None)
        self.report = Report()
        self._components: dict[tuple[str, ...], adsk.fusion.Component] = {(): self.root}

    def emit(self, plan: Plan) -> Report:
        t0 = time.perf_counter()
        self.report.checks.extend(plan.problems)
        for part in plan.parts:
            if part.manual:
                self.report.problems.append(f"{part.path}: manual part, not generated.")
                continue
            self.log(f"part {part.path}")
            try:
                self._emit_part(part)
            except RuntimeError as error:
                self._problem(f"{part.path}: the body could not be made ({error}); the part is left out.")
        for item in plan.hardware:
            self.log(f"hardware {item.path}")
            try:
                self._emit_hardware(item)
            except RuntimeError as error:
                self._problem(f"{item.path}: could not be drawn ({error}).")
        self.report.seconds = time.perf_counter() - t0
        self.report.document = self.design.parentDocument.name
        return self.report

    # -- hardware ------------------------------------------------------------------------------------

    def _emit_hardware(self, item: HardwarePlan) -> None:
        """Draws each body as the union of its boxes, made as temporary
        B-rep boxes, in a component of its own below the scope's, named as
        the hardware is in its scope; its bodies carry the full path."""
        comp = self._component(item.component + (item.name,))
        for body_plan in item.bodies:
            body: adsk.fusion.BRepBody | None = None
            for lo, hi in body_plan.boxes:
                center = ((lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2, (lo[2] + hi[2]) / 2)
                box = self.tmp.createBox(adsk.core.OrientedBoundingBox3D.create(
                    _pt(center), _vec((1.0, 0.0, 0.0)), _vec((0.0, 1.0, 0.0)),
                    (hi[0] - lo[0]) * MM, (hi[1] - lo[1]) * MM, (hi[2] - lo[2]) * MM))
                if body is None:
                    body = box
                elif not self.tmp.booleanOperation(body, box, _UNION):
                    self._problem(f"{item.path}.{body_plan.name}: its boxes could not be joined.")
            if body is not None:
                self._add_bodies(comp, [body])[0].name = f"{item.path}.{body_plan.name}"
        self.report.features += 1

    def bodies(self) -> dict[str, list[adsk.fusion.BRepBody]]:
        """The bodies drawn so far, by name: a part's path, or a hardware
        body's (`tests/fuzz/fusion_check.py` compares them with the
        preview)."""
        out: dict[str, list[adsk.fusion.BRepBody]] = {}
        for path, comp in self._components.items():
            if path:
                for body in comp.bRepBodies:
                    out.setdefault(body.name, []).append(body)
        return out

    def _problem(self, text: str) -> None:
        self.report.problems.append(text)
        self.log("problem: " + text)

    # -- components and bodies ---------------------------------------------------------------

    def _component(self, path: tuple[str, ...]) -> adsk.fusion.Component:
        comp = self._components.get(path)
        if comp is None:
            parent = self._component(path[:-1])
            occ = parent.occurrences.addNewComponent(adsk.core.Matrix3D.create())
            comp = occ.component
            comp.name = path[-1]
            self._components[path] = comp
        return comp

    def _emit_part(self, part: PartPlan) -> None:
        """The body, then its steps in order; a step Fusion refuses is
        reported and left out, and the next one goes on."""
        comp = self._component(part.component)
        body = self._make_body(comp, part)
        for step in part.steps:
            self.log(f"  {_describe(step)}")
            try:
                if isinstance(step, PocketStep):
                    self._pockets(comp, body, step, part.path)
                elif isinstance(step, HoleStep):
                    self._holes(comp, body, step, part.path)
                elif isinstance(step, VGrooveStep):
                    self._vgroove(comp, body, step)
                else:
                    self._chamfer(comp, body, step, part.path)
            except RuntimeError as error:
                self._problem(f"{part.path}: {_describe(step)} failed ({error}); left out.")
        if part.facts is not None:
            facts = part.facts
            body.attributes.add(ATTRIBUTE_GROUP, ATTRIBUTE_NAME, json.dumps({
                "path": part.path, "material": facts.material, "thickness": facts.thickness,
                "grained": facts.grained, "grain": list(facts.grain) if facts.grain else None,
                "up": list(facts.up),
            }))
        self.report.parts += 1

    def _make_body(self, comp: adsk.fusion.Component, part: PartPlan) -> adsk.fusion.BRepBody:
        direction = part.body.direction
        added = self._add_faces(comp, [part.body.loops], direction)
        profile = added[0].faces.item(0)
        extrudes = comp.features.extrudeFeatures
        inp = extrudes.createInput(profile, _NEW_BODY)
        extent = adsk.fusion.DistanceExtentDefinition.create(
            adsk.core.ValueInput.createByReal(part.body.thickness * MM))
        inp.setOneSideExtent(extent, self._direction_toward(profile, direction))
        try:
            extrude = extrudes.add(inp)
        finally:
            self._drop_faces(comp, added)
        body = extrude.bodies.item(0)
        body.name = part.path
        self.report.features += 1
        return body

    # -- temporary face bodies -----------------------------------------------------------------

    def _face_body(self, loops: Loops, normal: Vec) -> adsk.fusion.BRepBody:
        wires: list[adsk.fusion.BRepBody] = []
        for loop in loops:
            curves: list[adsk.core.Curve3D] = []
            for c in oriented(loop, normal):
                if isinstance(c, Line):
                    if math.dist(c.a, c.b) < 1e-6:
                        continue
                    curves.append(adsk.core.Line3D.create(_pt(c.a), _pt(c.b)))
                elif isinstance(c, Arc):
                    curves.append(adsk.core.Arc3D.createByThreePoints(_pt(c.a), _pt(c.mid), _pt(c.b)))
                else:
                    curves.append(adsk.core.Circle3D.createByCenter(_pt(c.center), _vec(normal), c.radius * MM))
            wire, _ = self.tmp.createWireFromCurves(curves)
            wires.append(wire)
        return self.tmp.createFaceFromPlanarWires(wires)

    def _add_faces(self, comp: adsk.fusion.Component, shapes: list[Loops],
                   normal: Vec) -> list[adsk.fusion.BRepBody]:
        """Adds one planar face body per shape to the component."""
        return self._add_bodies(comp, [self._face_body(loops, normal) for loops in shapes])

    def _add_bodies(self, comp: adsk.fusion.Component,
                    bodies: list[adsk.fusion.BRepBody]) -> list[adsk.fusion.BRepBody]:
        """Adds temporary bodies to the component. A parametric design
        needs a base feature; a direct design does not."""
        if not self.parametric:
            return [comp.bRepBodies.add(b) for b in bodies]
        base = comp.features.baseFeatures.add()
        base.startEdit()
        for b in bodies:
            comp.bRepBodies.add(b, base)
        base.finishEdit()
        # Proxies returned inside the edit session go stale once it ends.
        return [base.bodies.item(i) for i in range(base.bodies.count)]

    def _drop_faces(self, comp: adsk.fusion.Component, bodies: list[adsk.fusion.BRepBody]) -> None:
        for b in bodies:
            if self.parametric:
                comp.features.removeFeatures.add(b)
            else:
                b.deleteMe()

    @staticmethod
    def _reach(body: adsk.fusion.BRepBody, face: FaceRef) -> float:
        """How far (mm) the body reaches past the plane of `face`, into it."""
        bb = body.boundingBox
        if face.sign > 0:
            return face.value - _coord(bb.minPoint, face.axis) / MM
        return _coord(bb.maxPoint, face.axis) / MM - face.value

    @staticmethod
    def _normal(face: adsk.fusion.BRepFace) -> Vec:
        ok, n = face.evaluator.getNormalAtPoint(face.centroid)
        if not ok:
            raise RuntimeError("no normal for face")
        return (n.x, n.y, n.z)

    def _direction_toward(self, face: adsk.fusion.BRepFace, into: Vec) -> adsk.fusion.ExtentDirections:
        """The extent direction that moves the face's profile along `into`.
        A temporary face's normal follows its wire winding."""
        return _POSITIVE if dot(self._normal(face), into) > 0 else _NEGATIVE

    # -- finding geometry by position ------------------------------------------------------------

    def _find_face(self, body: adsk.fusion.BRepBody, axis: Axis, sign: int,
                   value: float | None = None) -> adsk.fusion.BRepFace | None:
        """The planar face whose outward normal points along `sign` on
        `axis`, at `value` (mm); without a value the outermost one. Among
        candidates the largest wins."""
        want = FaceRef(axis, sign, 0.0).normal
        best: adsk.fusion.BRepFace | None = None
        best_key: tuple[float, float] | None = None
        for face in body.faces:
            if cast(adsk.core.Plane | None, adsk.core.Plane.cast(face.geometry)) is None:
                continue
            if dot(self._normal(face), want) < 0.99:
                continue
            c = _coord(face.centroid, axis)
            if value is not None and abs(c - value * MM) > TOL:
                continue
            key = (0.0 if value is not None else round(sign * c, 4), face.area)
            if best_key is None or key > best_key:
                best, best_key = face, key
        return best

    def _face(self, body: adsk.fusion.BRepBody, ref: FaceRef) -> adsk.fusion.BRepFace | None:
        return self._find_face(body, ref.axis, ref.sign, ref.value)

    @staticmethod
    def _edge_on_plane(edge: adsk.fusion.BRepEdge, ref: FaceRef) -> bool:
        bb = edge.boundingBox
        v = ref.value * MM
        return abs(_coord(bb.minPoint, ref.axis) - v) < TOL and abs(_coord(bb.maxPoint, ref.axis) - v) < TOL

    @staticmethod
    def _edge_midpoint(edge: adsk.fusion.BRepEdge) -> Point3:
        evaluator = edge.evaluator
        ok, p0, p1 = evaluator.getParameterExtents()
        ok2, pt = evaluator.getPointAtParameter((p0 + p1) / 2)
        if not (ok and ok2):
            raise RuntimeError("no midpoint for edge")
        return (pt.x, pt.y, pt.z)

    def _contour_edges(self, body: adsk.fusion.BRepBody, contour: Contour) -> list[list[adsk.fusion.BRepEdge]]:
        """The edges a contour names, in groups that are chamfered or left
        together: one per loop of a shape, else all of them."""
        if isinstance(contour, OutlineContour):
            face = self._face(body, contour.face)
            if face is None:
                return []
            for loop in face.loops:
                if loop.isOuter:
                    return [list(loop.edges)]
            return []
        if isinstance(contour, EdgeContour):
            return [[e for e in body.edges
                     if self._edge_on_plane(e, contour.a) and self._edge_on_plane(e, contour.b)]]
        if isinstance(contour, ShapeContour):
            normal = contour.face.normal
            groups: list[list[adsk.fusion.BRepEdge]] = [[] for _ in contour.loops]
            for e in body.edges:
                if not self._edge_on_plane(e, contour.face):
                    continue
                mid = _mm(self._edge_midpoint(e))
                for i, loop in enumerate(contour.loops):
                    if any(on_curve(mid, c, normal, TOL / MM) for c in loop):
                        groups[i].append(e)
                        break
            return [g for g in groups if g]
        circle_contour: CircleContour = contour
        center = _pt(circle_contour.center)
        found = []
        for e in body.edges:
            if not self._edge_on_plane(e, circle_contour.face):
                continue
            geometry = e.geometry
            circle = cast(adsk.core.Circle3D | None, adsk.core.Circle3D.cast(geometry))
            arc = cast(adsk.core.Arc3D | None, adsk.core.Arc3D.cast(geometry))
            if circle is not None:
                c, r = circle.center, circle.radius
            elif arc is not None:
                c, r = arc.center, arc.radius
            else:
                continue
            if c.distanceTo(center) < TOL and abs(r - circle_contour.r * MM) < TOL:
                found.append(e)
        return [found]

    # -- steps ---------------------------------------------------------------------------------------

    def _pockets(self, comp: adsk.fusion.Component, body: adsk.fusion.BRepBody, step: PocketStep,
                 path: str) -> None:
        added = self._add_faces(comp, step.shapes, step.face.into)
        profiles = [b.faces.item(0) for b in added]
        extrudes = comp.features.extrudeFeatures
        profile_input: adsk.core.Base = profiles[0] if len(profiles) == 1 else _collection(list(profiles))
        inp = extrudes.createInput(profile_input, _CUT)
        # Through: as far as the body reaches past the face and a millimetre
        # more, limited to this body by participantBodies. Fusion's
        # through-all extent finds no target body, or stops short, once
        # other components' bodies are in the document (a fuzz batch,
        # 2026-10-12).
        depth = self._reach(body, step.face) + 1.0 if step.depth is None else step.depth
        extent = adsk.fusion.DistanceExtentDefinition.create(adsk.core.ValueInput.createByReal(depth * MM))
        inp.setOneSideExtent(extent, self._direction_toward(profiles[0], step.face.into))
        inp.participantBodies = [body]
        try:
            extrudes.add(inp)
        finally:
            self._drop_faces(comp, added)
        self.report.features += 1

    def _holes(self, comp: adsk.fusion.Component, body: adsk.fusion.BRepBody, step: HoleStep,
               path: str) -> None:
        """One hole feature per point; a hole that cannot be made is
        reported and the others are still drilled."""
        holes = comp.features.holeFeatures
        for point in step.points:
            face = self._face(body, step.face)
            if face is None:
                self._problem(f"{path}: no face at {step.face} for the hole at {point}; left out.")
                continue
            inp = holes.createSimpleInput(adsk.core.ValueInput.createByReal(step.d * MM))
            inp.setPositionByPoint(face, _pt(point))
            # The hole's natural direction is opposite the face normal.
            n = self._normal(face)
            natural: Vec = (-n[0], -n[1], -n[2])
            inp.isDefaultDirection = dot(natural, step.face.into) > 0
            if step.depth is None:
                opposite = self._find_face(body, step.face.axis, -step.face.sign)
                if opposite is None:
                    self._problem(f"{path}: no face opposite {step.face} for the through hole at {point}; left out.")
                    continue
                # Without the direction hint Fusion finds no target body
                # (probed 2026-10-10), whatever isDefaultDirection says.
                inp.setOneSideToExtent(opposite, False, adsk.core.Vector3D.create(*step.face.into))
            else:
                inp.setDistanceExtent(adsk.core.ValueInput.createByReal(step.depth * MM))
            inp.tipAngle = adsk.core.ValueInput.createByString("180 deg")
            inp.participantBodies = [body]
            try:
                holes.add(inp)
            except RuntimeError as error:
                self._problem(f"{path}: the hole d{step.d:g} at {point} failed ({error}); left out.")
                continue
            self.report.features += 1

    def _vgroove(self, comp: adsk.fusion.Component, body: adsk.fusion.BRepBody, step: VGrooveStep) -> None:
        """The groove's cross-section at its start, a triangle with its
        opening on the face, cut along the groove to its end."""
        line: Vec = (step.end[0] - step.start[0], step.end[1] - step.start[1], step.end[2] - step.start[2])
        length = math.sqrt(dot(line, line))
        along: Vec = (line[0] / length, line[1] / length, line[2] / length)
        into = step.face.into
        across = cross(along, into)           # a unit vector in the face, across the groove
        half = step.depth                     # a 90 degree V is twice as wide as it is deep
        s = step.start
        ring: list[Point3] = [
            (s[0] + across[0] * half, s[1] + across[1] * half, s[2] + across[2] * half),
            (s[0] - across[0] * half, s[1] - across[1] * half, s[2] - across[2] * half),
            (s[0] + into[0] * step.depth, s[1] + into[1] * step.depth, s[2] + into[2] * step.depth),
        ]
        added = self._add_faces(comp, [[polygon_loop(ring)]], along)
        profile = added[0].faces.item(0)
        extrudes = comp.features.extrudeFeatures
        inp = extrudes.createInput(profile, _CUT)
        extent = adsk.fusion.DistanceExtentDefinition.create(adsk.core.ValueInput.createByReal(length * MM))
        inp.setOneSideExtent(extent, self._direction_toward(profile, along))
        inp.participantBodies = [body]
        try:
            extrudes.add(inp)
        finally:
            self._drop_faces(comp, added)
        self.report.features += 1

    def _chamfer(self, comp: adsk.fusion.Component, body: adsk.fusion.BRepBody, step: ChamferStep,
                 path: str) -> None:
        groups = [g for g in self._contour_edges(body, step.contour) if g]
        if not groups:
            self._problem(f"{path}: chamfer finds no edges along {step.contour}.")
            return
        failed = self._chamfer_groups(comp, groups, step.size)
        if failed:
            self._problem(f"{path}: {failed} of {len(groups)} contours could not be chamfered {step.size:g} "
                          f"and stay sharp ({step.contour}).")

    def _chamfer_groups(self, comp: adsk.fusion.Component, groups: list[list[adsk.fusion.BRepEdge]],
                        size: float) -> int:
        """Chamfers the groups of edges in one feature. Fusion fails a
        chamfer as a whole when one contour is too small for it, so on
        failure the groups are chamfered by halves; returns how many single
        groups could not be chamfered. The edges of the others stay valid
        after a partial chamfer."""
        chamfers = comp.features.chamferFeatures
        inp = chamfers.createInput2()
        inp.chamferEdgeSets.addEqualDistanceChamferEdgeSet(
            _collection([e for g in groups for e in g]), adsk.core.ValueInput.createByReal(size * MM), False)
        try:
            chamfers.add(inp)
            self.report.features += 1
            return 0
        except RuntimeError:
            if len(groups) == 1:
                return 1
        half = len(groups) // 2
        return self._chamfer_groups(comp, groups[:half], size) + self._chamfer_groups(comp, groups[half:], size)


# -- entry points ----------------------------------------------------------------------------------

def new_document(design_type: str = "direct") -> adsk.fusion.Design:
    """A fresh design document of the given type ('direct' or 'parametric')."""
    app = adsk.core.Application.get()
    app.documents.add(_DESIGN_DOCUMENT)
    design = adsk.fusion.Design.cast(app.activeProduct)
    wanted = _DIRECT if design_type == "direct" else _PARAMETRIC
    if design.designType != wanted:
        design.designType = wanted
    return design


def emit_layout(layout: Layout, design: adsk.fusion.Design | None = None,
                design_type: str = "direct", log: Log | None = None) -> Report:
    """Draws a layout into `design`, or into a new document."""
    plan = plan_layout(layout)
    if design is None:
        design = new_document(design_type)
    gc.disable()
    try:
        return Emitter(design, log).emit(plan)
    finally:
        gc.enable()


def emit_file(path: str, design: adsk.fusion.Design | None = None,
              design_type: str = "direct", log: Log | None = None) -> Report:
    with open(path) as fh:
        layout: Layout = json.load(fh)
    return emit_layout(layout, design, design_type, log)
