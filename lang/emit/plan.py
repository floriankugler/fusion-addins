"""The emit plan: a layout resolved into world geometry and batched steps.

Everything here is plain Python in world millimetres. The Fusion half
(`fusion.py`) only converts units, draws, and finds faces and edges by the
positions recorded here.

Per part the plan holds the body (the outline on the part's lower big
face, extruded along the thickness axis) and an ordered list of steps:

- `PocketStep`: shapes cut from one face to one depth, batched while
  consecutive pockets share face and depth; a pocket with several pieces
  (a cutout's openings) gives one shape per piece;
- `HoleStep`: holes of one diameter and depth from one face, batched alike;
- `VGrooveStep`: one straight 90 degree V-groove, from its start to its end
  along the face, `depth` deep (twice as wide at the face), ends square;
- `ChamferStep`: a size and a contour that names the edges: a face's outer
  loop, the line where two faces meet, a shape's contour on a face, or a
  circle on a face.

Through cuts are already part of the outline and produce no step, except a
chamfer along their contour.

Outlines and shapes are loops of lines, arcs and circles: the layout's
polygons with the runs that lie on a circle recovered as arcs (`arcs.fit`),
so a slot's round end becomes one cylindrical face in Fusion instead of a
fan of flat ones.

How a layout is read is shared with the preview's mesher
(`lang.preview.mesh`), so both see the same faces, depths and chamfer
targets: `LayoutFrame` decodes the layout's world direction names,
`PartFrame` a part's faces, points, depths and narrow-face start planes,
`named_ops` and `chamfer_target` what a chamfer names.

This module is loaded inside Fusion without the `lang` package (see
`lang.emit`), so it imports the layout's types only for the type checker
and repeats `LAYOUT_VERSION`; a test keeps the two equal.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Literal

from .arcs import Arc2, Curve2, Line2, fit

if TYPE_CHECKING:
    from ..core.layout_types import (ChamferLayout, EdgeOpLayout, HardwareLayout, HoleLayout, Layout, OpLayout,
                                     PartLayout, PocketLayout, Rings)

#: The layout version this plan reads (`lang.core.layout_types.LAYOUT_VERSION`).
LAYOUT_VERSION = 4

Axis = Literal["x", "y", "z"]
AXES: tuple[Axis, Axis, Axis] = ("x", "y", "z")
Vec = tuple[float, float, float]
Point3 = tuple[float, float, float]


@dataclass(frozen=True)
class Line:
    a: Point3
    b: Point3


@dataclass(frozen=True)
class Arc:
    """From `a` through `mid` to `b` about `center`."""
    a: Point3
    mid: Point3
    b: Point3
    center: Point3
    radius: float


@dataclass(frozen=True)
class Circle:
    """A full circle in the plane of the face it is drawn on."""
    center: Point3
    radius: float


Curve = Line | Arc | Circle
#: A closed loop of curves, each starting where the one before ends.
Loop = list[Curve]
#: A planar region: its outer loop first, then its holes.
Loops = list[Loop]


def loop_points(loop: Loop) -> list[Point3]:
    """The loop's corners in order, with each arc's middle point: a polygon
    that winds the same way. Empty for a full circle."""
    points: list[Point3] = []
    for curve in loop:
        if isinstance(curve, Line):
            points.append(curve.a)
        elif isinstance(curve, Arc):
            points += [curve.a, curve.mid]
    return points


@dataclass(frozen=True)
class FaceRef:
    """A planar face of a part named by position: the plane `axis = value`
    (world mm) with the outward normal pointing along `sign`."""
    axis: Axis
    sign: int
    value: float

    @property
    def normal(self) -> Vec:
        return _unit(self.axis, self.sign)

    @property
    def into(self) -> Vec:
        return _unit(self.axis, -self.sign)

    @property
    def opposite(self) -> FaceRef:
        """The face across the part; only its direction is meaningful, the
        emitter finds it by normal."""
        return FaceRef(self.axis, -self.sign, self.value)


@dataclass
class Body:
    """The part's outline on its lower big face, extruded along
    `direction` by `thickness`."""
    loops: Loops
    direction: Vec
    thickness: float


@dataclass
class PocketStep:
    face: FaceRef
    shapes: list[Loops]
    depth: float | None  #: None means through


@dataclass
class HoleStep:
    face: FaceRef
    points: list[Point3]
    d: float
    depth: float | None  #: None means through


@dataclass
class VGrooveStep:
    face: FaceRef
    start: Point3
    end: Point3
    depth: float


@dataclass
class OutlineContour:
    face: FaceRef


@dataclass
class EdgeContour:
    a: FaceRef
    b: FaceRef


@dataclass
class ShapeContour:
    face: FaceRef
    loops: Loops


@dataclass
class CircleContour:
    face: FaceRef
    center: Point3
    r: float


Contour = OutlineContour | EdgeContour | ShapeContour | CircleContour


@dataclass
class ChamferStep:
    size: float
    contour: Contour


Step = PocketStep | HoleStep | VGrooveStep | ChamferStep


@dataclass
class PartFacts:
    """What the emitter stores on a part's body for the tools that work on
    the compiled document (Multi Arrange, later Auto Setup): world vectors,
    the material as the layout labels it, the thickness in mm."""
    material: str
    thickness: float
    #: Whether the material has a grain at all.
    grained: bool
    #: The grain direction, or None when the build left it unset.
    grain: Vec | None
    #: The outward normal of the face machined from, which faces up on the machine.
    up: Vec


@dataclass
class PartPlan:
    path: str
    component: tuple[str, ...]
    body: Body
    steps: list[Step] = field(default_factory=list[Step])
    manual: bool = False
    facts: PartFacts | None = None


@dataclass
class HardwareBodyPlan:
    name: str
    #: Boxes along the world axes as (min, max) corners, mm; the body is their union.
    boxes: list[tuple[Point3, Point3]]


@dataclass
class HardwarePlan:
    """A bought part to draw as boxes, one body per piece, in a component
    of its own below its scope's."""
    path: str
    component: tuple[str, ...]
    name: str
    bodies: list[HardwareBodyPlan]


@dataclass
class Plan:
    parts: list[PartPlan]
    problems: list[str]
    hardware: list[HardwarePlan] = field(default_factory=list[HardwarePlan])


def pieces(rings: Rings) -> list[Rings]:
    """A layout shape's polygons, each its exterior ring and its holes: an
    exterior winds the way the first ring does, a hole the other way."""
    def area(ring: list[list[float]]) -> float:
        return sum(p[0] * q[1] - q[0] * p[1] for p, q in zip(ring, ring[1:] + ring[:1])) / 2

    out: list[Rings] = []
    first = area(rings[0]) > 0 if rings else True
    for ring in rings:
        if not out or (area(ring) > 0) == first:
            out.append([ring])
        else:
            out[-1].append(ring)
    return out


def _unit(axis: Axis, sign: int) -> Vec:
    v = [0.0, 0.0, 0.0]
    v[AXES.index(axis)] = 1.0 if sign > 0 else -1.0
    return (v[0], v[1], v[2])


def _as_axis(value: str) -> Axis:
    if value == "x" or value == "y" or value == "z":
        return value
    raise ValueError(f"not an axis: {value!r}")


class LayoutFrame:
    """The layout's world direction names (`front`: `-x`), decoded."""

    def __init__(self, frame: dict[str, str]):
        self._dirs: dict[str, tuple[Axis, int]] = {}
        for name, code in frame.items():
            self._dirs[name] = (_as_axis(code[1]), 1 if code[0] == "+" else -1)

    def is_direction(self, name: str) -> bool:
        return name in self._dirs

    def direction(self, name: str) -> tuple[Axis, int]:
        """The world axis and sign (+1, -1) a direction name stands for."""
        try:
            return self._dirs[name]
        except KeyError:
            raise ValueError(f"unknown direction {name!r}") from None


class PartFrame:
    """One part of the layout with its frame conversions: its faces as
    planes, points in a face's 2D frame, depths, and the plane a
    narrow-face operation starts from."""

    def __init__(self, part: PartLayout, frame: LayoutFrame):
        self.part = part
        self.frame = frame
        self.t_axis: Axis = _as_axis(part["axes"]["t"])
        self.u_axis: Axis = _as_axis(part["axes"]["u"])
        self.v_axis: Axis = _as_axis(part["axes"]["v"])
        self.lo: dict[Axis, float] = {a: part["box"]["min"][i] for i, a in enumerate(AXES)}
        self.hi: dict[Axis, float] = {a: part["box"]["max"][i] for i, a in enumerate(AXES)}
        self.thickness = part["thickness"]

    def face(self, name: str) -> FaceRef:
        axis, sign = self.frame.direction(name)
        return FaceRef(axis, sign, self.hi[axis] if sign > 0 else self.lo[axis])

    def is_big(self, face: FaceRef) -> bool:
        return face.axis == self.t_axis

    def in_face(self, face: FaceRef) -> tuple[Axis, Axis]:
        """The two world axes of the face's 2D frame: (u, v) on a big face,
        (s, t) on a narrow one, s along the face and t across the
        thickness."""
        if face.axis == self.t_axis:
            return self.u_axis, self.v_axis
        return (self.v_axis if face.axis == self.u_axis else self.u_axis), self.t_axis

    def point(self, face: FaceRef, a: float, b: float) -> Point3:
        """A point given in the face's 2D frame as world coordinates: (u, v)
        on a big face, (s, t) on a narrow face."""
        first, second = self.in_face(face)
        coords = {first: a, second: b, face.axis: face.value}
        return (coords["x"], coords["y"], coords["z"])

    def loops(self, face: FaceRef, rings: Rings, offset: tuple[float, float] = (0.0, 0.0)) -> Loops:
        """A layout shape (rings in the face's frame, moved by `offset`) as
        loops on the face, with its arcs recovered."""
        return [[self._curve(face, c) for c in fit([(p[0] + offset[0], p[1] + offset[1]) for p in ring])]
                for ring in rings]

    def _curve(self, face: FaceRef, c: Curve2) -> Curve:
        if isinstance(c, Line2):
            return Line(self.point(face, *c.a), self.point(face, *c.b))
        if isinstance(c, Arc2):
            return Arc(self.point(face, *c.a), self.point(face, *c.mid), self.point(face, *c.b),
                       self.point(face, *c.center), c.radius)
        return Circle(self.point(face, *c.center), c.radius)

    def extent(self, face: FaceRef) -> float:
        """How far the part reaches from `face` to the opposite face: the
        thickness from a big face, the part's length or width from a narrow
        one (plus the offset of a plane in front of the face)."""
        far = self.lo[face.axis] if face.sign > 0 else self.hi[face.axis]
        return abs(face.value - far)

    def depth(self, face: FaceRef, depth: float, through: bool = False) -> float | None:
        """A depth from `face`, or None when it reaches the opposite face
        (`through`, or as deep as `extent`)."""
        return None if through or depth >= self.extent(face) - 1e-9 else depth

    def edge_face(self, op: EdgeOpLayout) -> FaceRef:
        """The plane a narrow-face operation starts from: its face, moved
        by its offset in front of it."""
        face = self.face(op["face"])
        offset = op.get("offset", 0.0)
        return FaceRef(face.axis, face.sign, face.value + face.sign * offset) if offset else face


def named_ops(part: PartLayout) -> dict[str, OpLayout]:
    """The part's named operations by name; a narrow-face operation under
    its own operation's name."""
    named: dict[str, OpLayout] = {}
    for op in part["ops"]:
        name = op["op"]["name"] if op["kind"] == "edge" else (op["name"] if op["kind"] != "chamfer" else None)
        if name:
            named[name] = op
    return named


@dataclass(frozen=True)
class OutlineTarget:
    """A chamfer along the outer contour of a face."""


@dataclass(frozen=True)
class OpTarget:
    """A chamfer along a named operation's contour: a cut, a pocket, a hole
    or a narrow-face operation."""
    op: OpLayout


@dataclass(frozen=True)
class EdgeTarget:
    """A chamfer along the edge where two faces meet, by world name."""
    a: str
    b: str


ChamferTarget = OutlineTarget | OpTarget | EdgeTarget


def chamfer_target(op: ChamferLayout, named: dict[str, OpLayout], frame: LayoutFrame) -> ChamferTarget | None:
    """What a chamfer operation names, or None when it names nothing the
    chamfer can follow (an unknown name, a V-groove)."""
    what = op["what"]
    if what == "outline":
        return OutlineTarget()
    if what in named:
        target = named[what]
        return OpTarget(target) if target["kind"] in ("cut", "pocket", "hole", "edge") else None
    parts = what.split(".")
    if len(parts) == 2 and all(frame.is_direction(n) for n in parts):
        return EdgeTarget(parts[0], parts[1])
    return None


def plan_part(part: PartLayout, frame: LayoutFrame, problems: list[str]) -> PartPlan:
    p = PartFrame(part, frame)
    segments = part["path"].split(".")
    lower = FaceRef(p.t_axis, -1, p.lo[p.t_axis])
    body = Body(p.loops(lower, part["outline"]), _unit(p.t_axis, 1), p.thickness)
    plan = PartPlan(part["path"], tuple(segments[:-1]), body, manual=part["manual"])
    show = p.face(part["show"])
    machine = p.face(part["machine"])
    grain = part["grain"]
    plan.facts = PartFacts(part["material"], part["thickness"], part["grained"],
                           _unit(_as_axis(grain), 1) if grain else None, machine.normal)
    named = named_ops(part)
    for op in part["ops"]:
        _plan_op(p, plan, op, show, named, problems)
    return plan


def _plan_op(p: PartFrame, plan: PartPlan, op: OpLayout, show: FaceRef,
             named: dict[str, OpLayout], problems: list[str]) -> None:
    steps = plan.steps
    if op["kind"] == "cut":
        if op["chamfer"] > 0:
            steps.append(ChamferStep(op["chamfer"], ShapeContour(show, p.loops(show, op["shape"]))))
    elif op["kind"] == "pocket":
        _add_pocket(p, steps, p.face(op["face"]), op, (0.0, 0.0))
    elif op["kind"] == "hole":
        _add_hole(p, steps, p.face(op["face"]), op, (op["u"], op["v"]))
    elif op["kind"] == "vgroove":
        face = p.face(op["face"])
        steps.append(VGrooveStep(face, p.point(face, op["start"][0], op["start"][1]),
                                 p.point(face, op["end"][0], op["end"][1]), op["depth"]))
    elif op["kind"] == "edge":
        face = p.edge_face(op)
        inner = op["op"]
        if inner["kind"] == "pocket":
            _add_pocket(p, steps, face, inner, (op["s"], op["t"]))
        else:
            _add_hole(p, steps, face, inner, (op["s"], op["t"]))
    else:
        contour = _chamfer_contour(p, op, show, named)
        if contour is None:
            problems.append(f"{plan.path}: chamfer {op['what']!r} names nothing on this part.")
        else:
            steps.append(ChamferStep(op["size"], contour))


def _add_pocket(p: PartFrame, steps: list[Step], face: FaceRef, op: PocketLayout,
                offset: tuple[float, float]) -> None:
    shapes = [p.loops(face, piece, offset) for piece in pieces(op["shape"])]
    depth = p.depth(face, op["depth"])
    last = steps[-1] if steps else None
    if isinstance(last, PocketStep) and last.face == face and last.depth == depth:
        last.shapes.extend(shapes)
    else:
        steps.append(PocketStep(face, shapes, depth))
    if op["chamfer"] > 0:
        steps.append(ChamferStep(op["chamfer"], ShapeContour(face, [loop for s in shapes for loop in s])))


def _add_hole(p: PartFrame, steps: list[Step], face: FaceRef, op: HoleLayout,
              at: tuple[float, float]) -> None:
    point = p.point(face, at[0], at[1])
    depth = p.depth(face, op["depth"], op["through"])
    last = steps[-1] if steps else None
    if isinstance(last, HoleStep) and last.face == face and last.depth == depth and last.d == op["d"]:
        last.points.append(point)
    else:
        steps.append(HoleStep(face, [point], op["d"], depth))
    if op["chamfer"] > 0:
        steps.append(ChamferStep(op["chamfer"], CircleContour(face, point, op["d"] / 2)))


def _chamfer_contour(p: PartFrame, op: ChamferLayout, show: FaceRef,
                     named: dict[str, OpLayout]) -> Contour | None:
    target = chamfer_target(op, named, p.frame)
    face = p.face(op["face"])
    if isinstance(target, OutlineTarget):
        return OutlineContour(face)
    if isinstance(target, EdgeTarget):
        return EdgeContour(p.face(target.a), p.face(target.b))
    if target is None:
        return None
    named_op = target.op
    if named_op["kind"] == "cut":
        return ShapeContour(face, p.loops(face, named_op["shape"]))
    if named_op["kind"] == "pocket":
        f = p.face(named_op["face"])
        return ShapeContour(f, p.loops(f, named_op["shape"]))
    if named_op["kind"] == "hole":
        f = p.face(named_op["face"])
        return CircleContour(f, p.point(f, named_op["u"], named_op["v"]), named_op["d"] / 2)
    if named_op["kind"] == "edge":
        f = p.edge_face(named_op)
        inner = named_op["op"]
        if inner["kind"] == "pocket":
            return ShapeContour(f, p.loops(f, inner["shape"], (named_op["s"], named_op["t"])))
        return CircleContour(f, p.point(f, named_op["s"], named_op["t"]), inner["d"] / 2)
    return None


def check_version(layout: Layout) -> None:
    """A ValueError for a layout written in another version, which this
    code would misread: rebuild it."""
    if layout.get("version") != LAYOUT_VERSION:
        raise ValueError(f"layout version {layout.get('version')} is not supported (this reads "
                         f"{LAYOUT_VERSION}); build the layout again.")


def plan_layout(layout: Layout) -> Plan:
    check_version(layout)
    frame = LayoutFrame(layout["frame"])
    problems: list[str] = list(layout["problems"])       # every module's too
    parts: list[PartPlan] = []
    hardware: list[HardwarePlan] = []
    for module in layout["modules"]:
        for part in module["parts"]:
            parts.append(plan_part(part, frame, problems))
        for item in module["hardware"]:
            hardware.append(plan_hardware(item))
    return Plan(parts, problems, hardware)


def plan_hardware(item: HardwareLayout) -> HardwarePlan:
    def corner(c: list[float]) -> Point3:
        return (c[0], c[1], c[2])
    return HardwarePlan(
        item["path"], tuple(item["path"].split(".")[:-1]), item["name"],
        [HardwareBodyPlan(b["name"], [(corner(box["min"]), corner(box["max"])) for box in b["boxes"]])
         for b in item["bodies"]],
    )


