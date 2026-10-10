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
- chamfers: equal-distance chamfers on the edges a contour names.

Faces and edges are found by position, never by index, because every
feature gives the body new face identities. The feature calls and their
gotchas come from tools/perf/compile_bench.py.
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

from .plan import (AXES, Axis, ChamferStep, CircleContour, Contour, EdgeContour, FaceRef, HoleStep,
                   OutlineContour, PartPlan, Plan, PocketStep, Point3, Rings3, ShapeContour, Step,
                   Vec, plan_layout)

if TYPE_CHECKING:
    from ..core.layout_types import Layout

#: Centimetres (the API unit) per millimetre.
MM = 0.1
#: Positions closer than this (cm) coincide.
TOL = 1e-3

Log = Callable[[str], None]

# Fusion's stubs declare enum members as ints; the casts keep pyright quiet.
_NEW_BODY = cast(adsk.fusion.FeatureOperations, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
_CUT = cast(adsk.fusion.FeatureOperations, adsk.fusion.FeatureOperations.CutFeatureOperation)
_POSITIVE = cast(adsk.fusion.ExtentDirections, adsk.fusion.ExtentDirections.PositiveExtentDirection)
_NEGATIVE = cast(adsk.fusion.ExtentDirections, adsk.fusion.ExtentDirections.NegativeExtentDirection)
_DIRECT = cast(adsk.fusion.DesignTypes, adsk.fusion.DesignTypes.DirectDesignType)
_PARAMETRIC = cast(adsk.fusion.DesignTypes, adsk.fusion.DesignTypes.ParametricDesignType)
_DESIGN_DOCUMENT = cast(adsk.core.DocumentTypes, adsk.core.DocumentTypes.FusionDesignDocumentType)


@dataclass
class Report:
    parts: int = 0
    features: int = 0
    seconds: float = 0.0
    problems: list[str] = field(default_factory=list[str])
    document: str = ""

    def summary(self) -> str:
        text = f"{self.parts} parts, {self.features} features in {self.seconds:.1f} s -> {self.document}"
        return text + "".join(f"\n  problem: {p}" for p in self.problems)


# -- small geometry helpers ---------------------------------------------------------------------

def _pt(p: Point3) -> adsk.core.Point3D:
    return adsk.core.Point3D.create(p[0] * MM, p[1] * MM, p[2] * MM)


def _cm(p: Point3) -> Point3:
    return (p[0] * MM, p[1] * MM, p[2] * MM)


def _coord(point: adsk.core.Point3D, axis: Axis) -> float:
    return (point.x, point.y, point.z)[AXES.index(axis)]


def _dot(a: Vec, b: Vec) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def _collection(items: list[adsk.core.Base]) -> adsk.core.ObjectCollection:
    coll = adsk.core.ObjectCollection.create()
    for item in items:
        coll.add(item)
    return coll


def _newell_normal(ring: list[Point3]) -> Vec:
    nx = ny = nz = 0.0
    for i, a in enumerate(ring):
        b = ring[(i + 1) % len(ring)]
        nx += (a[1] - b[1]) * (a[2] + b[2])
        ny += (a[2] - b[2]) * (a[0] + b[0])
        nz += (a[0] - b[0]) * (a[1] + b[1])
    return (nx, ny, nz)


def _oriented(ring: list[Point3], normal: Vec) -> list[Point3]:
    """The ring without a repeated closing point, wound so that the face
    made from it has `normal` (right-hand rule)."""
    pts = list(ring)
    if len(pts) > 1 and all(abs(pts[0][i] - pts[-1][i]) < 1e-9 for i in range(3)):
        pts.pop()
    if _dot(_newell_normal(pts), normal) < 0:
        pts.reverse()
    return pts


def _dist_to_segment(p: Point3, a: Point3, b: Point3) -> float:
    ab = (b[0] - a[0], b[1] - a[1], b[2] - a[2])
    ap = (p[0] - a[0], p[1] - a[1], p[2] - a[2])
    length2 = _dot(ab, ab)
    t = 0.0 if length2 == 0 else max(0.0, min(1.0, _dot(ap, ab) / length2))
    c = (a[0] + t * ab[0], a[1] + t * ab[1], a[2] + t * ab[2])
    return math.dist(p, c)


def _describe(step: Step) -> str:
    if isinstance(step, PocketStep):
        return f"pocket x{len(step.shapes)} on {step.face} depth {step.depth}"
    if isinstance(step, HoleStep):
        return f"hole d{step.d} x{len(step.points)} on {step.face} depth {step.depth} at {step.points[0]}"
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
        self.report.problems.extend(plan.problems)
        for part in plan.parts:
            if part.manual:
                self.report.problems.append(f"{part.path}: manual part, not generated.")
                continue
            self.log(f"part {part.path}")
            self._emit_part(part)
        self.report.seconds = time.perf_counter() - t0
        self.report.document = self.design.parentDocument.name
        return self.report

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
        comp = self._component(part.component)
        body = self._make_body(comp, part)
        for step in part.steps:
            self.log(f"  {_describe(step)}")
            if isinstance(step, PocketStep):
                self._pockets(comp, body, step, part.path)
            elif isinstance(step, HoleStep):
                self._holes(comp, body, step, part.path)
            else:
                self._chamfer(comp, body, step, part.path)
        self.report.parts += 1

    def _make_body(self, comp: adsk.fusion.Component, part: PartPlan) -> adsk.fusion.BRepBody:
        direction = part.body.direction
        added = self._add_faces(comp, [part.body.rings], direction)
        profile = added[0].faces.item(0)
        extrudes = comp.features.extrudeFeatures
        inp = extrudes.createInput(profile, _NEW_BODY)
        extent = adsk.fusion.DistanceExtentDefinition.create(
            adsk.core.ValueInput.createByReal(part.body.thickness * MM))
        inp.setOneSideExtent(extent, self._direction_toward(profile, direction))
        extrude = extrudes.add(inp)
        body = extrude.bodies.item(0)
        body.name = part.path
        self._drop_faces(comp, added)
        self.report.features += 1
        return body

    # -- temporary face bodies -----------------------------------------------------------------

    def _face_body(self, rings: Rings3, normal: Vec) -> adsk.fusion.BRepBody:
        wires: list[adsk.fusion.BRepBody] = []
        for ring in rings:
            pts = _oriented(ring, normal)
            curves: list[adsk.core.Curve3D] = []
            for i, a in enumerate(pts):
                b = pts[(i + 1) % len(pts)]
                if math.dist(a, b) < 1e-6:
                    continue
                curves.append(adsk.core.Line3D.create(_pt(a), _pt(b)))
            wire, _ = self.tmp.createWireFromCurves(curves)
            wires.append(wire)
        return self.tmp.createFaceFromPlanarWires(wires)

    def _add_faces(self, comp: adsk.fusion.Component, shapes: list[Rings3],
                   normal: Vec) -> list[adsk.fusion.BRepBody]:
        """Adds one planar face body per shape to the component. A
        parametric design needs a base feature; a direct design does not."""
        faces = [self._face_body(rings, normal) for rings in shapes]
        if not self.parametric:
            return [comp.bRepBodies.add(fb) for fb in faces]
        base = comp.features.baseFeatures.add()
        base.startEdit()
        for fb in faces:
            comp.bRepBodies.add(fb, base)
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
    def _normal(face: adsk.fusion.BRepFace) -> Vec:
        ok, n = face.evaluator.getNormalAtPoint(face.centroid)
        if not ok:
            raise RuntimeError("no normal for face")
        return (n.x, n.y, n.z)

    def _direction_toward(self, face: adsk.fusion.BRepFace, into: Vec) -> adsk.fusion.ExtentDirections:
        """The extent direction that moves the face's profile along `into`.
        A temporary face's normal follows its wire winding."""
        return _POSITIVE if _dot(self._normal(face), into) > 0 else _NEGATIVE

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
            if _dot(self._normal(face), want) < 0.99:
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

    def _contour_edges(self, body: adsk.fusion.BRepBody, contour: Contour) -> list[adsk.fusion.BRepEdge]:
        if isinstance(contour, OutlineContour):
            face = self._face(body, contour.face)
            if face is None:
                return []
            for loop in face.loops:
                if loop.isOuter:
                    return list(loop.edges)
            return []
        if isinstance(contour, EdgeContour):
            return [e for e in body.edges
                    if self._edge_on_plane(e, contour.a) and self._edge_on_plane(e, contour.b)]
        if isinstance(contour, ShapeContour):
            segments: list[tuple[Point3, Point3]] = []
            for ring in contour.rings:
                pts = [_cm(p) for p in ring]
                segments += [(pts[i], pts[(i + 1) % len(pts)]) for i in range(len(pts))]
            found: list[adsk.fusion.BRepEdge] = []
            for e in body.edges:
                if not self._edge_on_plane(e, contour.face):
                    continue
                mid = self._edge_midpoint(e)
                if min(_dist_to_segment(mid, a, b) for a, b in segments) < TOL:
                    found.append(e)
            return found
        circle_contour: CircleContour = contour
        center = _cm(circle_contour.center)
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
            if math.dist((c.x, c.y, c.z), center) < TOL and abs(r - circle_contour.r * MM) < TOL:
                found.append(e)
        return found

    # -- steps ---------------------------------------------------------------------------------------

    def _pockets(self, comp: adsk.fusion.Component, body: adsk.fusion.BRepBody, step: PocketStep,
                 path: str) -> None:
        added = self._add_faces(comp, step.shapes, step.face.into)
        profiles = [b.faces.item(0) for b in added]
        extrudes = comp.features.extrudeFeatures
        profile_input: adsk.core.Base = profiles[0] if len(profiles) == 1 else _collection(list(profiles))
        inp = extrudes.createInput(profile_input, _CUT)
        if step.depth is None:
            # Through all, limited to this body by participantBodies.
            extent: adsk.fusion.ExtentDefinition = adsk.fusion.ThroughAllExtentDefinition.create()
        else:
            extent = adsk.fusion.DistanceExtentDefinition.create(
                adsk.core.ValueInput.createByReal(step.depth * MM))
        inp.setOneSideExtent(extent, self._direction_toward(profiles[0], step.face.into))
        inp.participantBodies = [body]
        extrudes.add(inp)
        self._drop_faces(comp, added)
        self.report.features += 1

    def _holes(self, comp: adsk.fusion.Component, body: adsk.fusion.BRepBody, step: HoleStep,
               path: str) -> None:
        holes = comp.features.holeFeatures
        for point in step.points:
            face = self._face(body, step.face)
            if face is None:
                self._problem(f"{path}: no face at {step.face} for a hole.")
                return
            inp = holes.createSimpleInput(adsk.core.ValueInput.createByReal(step.d * MM))
            inp.setPositionByPoint(face, _pt(point))
            # The hole's natural direction is opposite the face normal.
            natural = tuple(-c for c in self._normal(face))
            inp.isDefaultDirection = _dot(natural, step.face.into) > 0  # type: ignore[arg-type]
            if step.depth is None:
                opposite = self._find_face(body, step.face.axis, -step.face.sign)
                if opposite is None:
                    self._problem(f"{path}: no face opposite {step.face} for a through hole.")
                    return
                # Without the direction hint Fusion finds no target body
                # (probed 2026-10-10), whatever isDefaultDirection says.
                inp.setOneSideToExtent(opposite, False, adsk.core.Vector3D.create(*step.face.into))
            else:
                inp.setDistanceExtent(adsk.core.ValueInput.createByReal(step.depth * MM))
            inp.tipAngle = adsk.core.ValueInput.createByString("180 deg")
            inp.participantBodies = [body]
            holes.add(inp)
            self.report.features += 1

    def _chamfer(self, comp: adsk.fusion.Component, body: adsk.fusion.BRepBody, step: ChamferStep,
                 path: str) -> None:
        edges = self._contour_edges(body, step.contour)
        if not edges:
            self._problem(f"{path}: chamfer finds no edges along {step.contour}.")
            return
        chamfers = comp.features.chamferFeatures
        inp = chamfers.createInput2()
        inp.chamferEdgeSets.addEqualDistanceChamferEdgeSet(
            _collection(list(edges)), adsk.core.ValueInput.createByReal(step.size * MM), False)
        chamfers.add(inp)
        self.report.features += 1


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
