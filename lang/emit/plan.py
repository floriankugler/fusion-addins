"""The emit plan: a layout resolved into world geometry and batched steps.

Everything here is plain Python in world millimetres. The Fusion half
(`fusion.py`) only converts units, draws, and finds faces and edges by the
positions recorded here.

Per part the plan holds the body (outline rings on the part's lower big
face, extruded along the thickness axis) and an ordered list of steps:

- `PocketStep`: shapes cut from one face to one depth, batched while
  consecutive pockets share face and depth;
- `HoleStep`: holes of one diameter and depth from one face, batched alike;
- `VGrooveStep`: one straight 90 degree V-groove, from its start to its end
  along the face, `depth` deep (twice as wide at the face), ends square;
- `ChamferStep`: a size and a contour that names the edges: a face's outer
  loop, the line where two faces meet, a shape's contour on a face, or a
  circle on a face.

Through cuts are already part of the outline and produce no step, except a
chamfer along their contour.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from ..core.layout_types import (ChamferLayout, HardwareLayout, HoleLayout, Layout, OpLayout,
                                     PartLayout, PocketLayout, Rings)

Axis = Literal["x", "y", "z"]
AXES: tuple[Axis, Axis, Axis] = ("x", "y", "z")
Vec = tuple[float, float, float]
Point3 = tuple[float, float, float]
#: A polygon as rings of 3D points, exterior first, then holes.
Rings3 = list[list[Point3]]


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
    rings: Rings3
    direction: Vec
    thickness: float


@dataclass
class PocketStep:
    face: FaceRef
    shapes: list[Rings3]
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
    rings: Rings3


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
    offset: Point3  #: in the model's frame, mm


@dataclass
class HardwarePlan:
    """A model file to import and place: the model's axes as world vectors
    and its origin in world mm, plus per-body offsets in the model's frame."""
    path: str
    component: tuple[str, ...]
    name: str
    model: str
    origin: Point3
    axes: tuple[Vec, Vec, Vec]
    bodies: list[HardwareBodyPlan]


@dataclass
class Plan:
    parts: list[PartPlan]
    problems: list[str]
    hardware: list[HardwarePlan] = field(default_factory=list[HardwarePlan])


def _unit(axis: Axis, sign: int) -> Vec:
    v = [0.0, 0.0, 0.0]
    v[AXES.index(axis)] = 1.0 if sign > 0 else -1.0
    return (v[0], v[1], v[2])


def _as_axis(value: str) -> Axis:
    if value == "x" or value == "y" or value == "z":
        return value
    raise ValueError(f"not an axis: {value!r}")


class _Frame:
    def __init__(self, frame: dict[str, str]):
        self._dirs: dict[str, tuple[Axis, int]] = {}
        for name, code in frame.items():
            self._dirs[name] = (_as_axis(code[1]), 1 if code[0] == "+" else -1)

    def is_direction(self, name: str) -> bool:
        return name in self._dirs

    def direction(self, name: str) -> tuple[Axis, int]:
        try:
            return self._dirs[name]
        except KeyError:
            raise ValueError(f"unknown direction {name!r}") from None


class _Part:
    """One part of the layout with its frame conversions."""

    def __init__(self, part: PartLayout, frame: _Frame):
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

    def point(self, face: FaceRef, a: float, b: float) -> Point3:
        """A point given in the face's 2D frame as world coordinates: (u, v)
        on a big face, (s, t) on a narrow face."""
        if face.axis == self.t_axis:
            first, second = self.u_axis, self.v_axis
        else:
            first = self.v_axis if face.axis == self.u_axis else self.u_axis
            second = self.t_axis
        coords = {first: a, second: b, face.axis: face.value}
        return (coords["x"], coords["y"], coords["z"])

    def rings(self, face: FaceRef, rings: Rings, offset: tuple[float, float] = (0.0, 0.0)) -> Rings3:
        return [[self.point(face, p[0] + offset[0], p[1] + offset[1]) for p in ring] for ring in rings]

    def depth(self, face: FaceRef, depth: float, through: bool = False) -> float | None:
        """A depth from `face`, or None when it reaches the opposite face:
        the thickness for a big face, the part's extent for a narrow one."""
        extent = self.hi[face.axis] - self.lo[face.axis]
        return None if through or depth >= extent - 1e-9 else depth


def plan_part(part: PartLayout, frame: _Frame, problems: list[str]) -> PartPlan:
    p = _Part(part, frame)
    segments = part["path"].split(".")
    lower = FaceRef(p.t_axis, -1, p.lo[p.t_axis])
    body = Body(p.rings(lower, part["outline"]), _unit(p.t_axis, 1), p.thickness)
    plan = PartPlan(part["path"], tuple(segments[:-1]), body, manual=part["manual"])
    show = p.face(part["show"])
    # Layouts written before the machine face existed: the show face is up.
    machine = p.face(part.get("machine", part["show"]))
    grain = part["grain"]
    plan.facts = PartFacts(part["material"], part["thickness"], part.get("grained", True),
                           _unit(_as_axis(grain), 1) if grain else None, machine.normal)
    named: dict[str, OpLayout] = {}
    for op in part["ops"]:
        name = op["op"]["name"] if op["kind"] == "edge" else (op["name"] if op["kind"] != "chamfer" else None)
        if name:
            named[name] = op
    for op in part["ops"]:
        _plan_op(p, plan, op, show, named, problems)
    return plan


def _plan_op(p: _Part, plan: PartPlan, op: OpLayout, show: FaceRef,
             named: dict[str, OpLayout], problems: list[str]) -> None:
    steps = plan.steps
    if op["kind"] == "cut":
        if op["chamfer"] > 0:
            steps.append(ChamferStep(op["chamfer"], ShapeContour(show, p.rings(show, op["shape"]))))
    elif op["kind"] == "pocket":
        _add_pocket(p, steps, p.face(op["face"]), op, (0.0, 0.0))
    elif op["kind"] == "hole":
        _add_hole(p, steps, p.face(op["face"]), op, (op["u"], op["v"]))
    elif op["kind"] == "vgroove":
        face = p.face(op["face"])
        steps.append(VGrooveStep(face, p.point(face, op["start"][0], op["start"][1]),
                                 p.point(face, op["end"][0], op["end"][1]), op["depth"]))
    elif op["kind"] == "edge":
        face = p.face(op["face"])
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


def _add_pocket(p: _Part, steps: list[Step], face: FaceRef, op: PocketLayout,
                offset: tuple[float, float]) -> None:
    rings = p.rings(face, op["shape"], offset)
    depth = p.depth(face, op["depth"])
    last = steps[-1] if steps else None
    if isinstance(last, PocketStep) and last.face == face and last.depth == depth:
        last.shapes.append(rings)
    else:
        steps.append(PocketStep(face, [rings], depth))
    if op["chamfer"] > 0:
        steps.append(ChamferStep(op["chamfer"], ShapeContour(face, rings)))


def _add_hole(p: _Part, steps: list[Step], face: FaceRef, op: HoleLayout,
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


def _chamfer_contour(p: _Part, op: ChamferLayout, show: FaceRef,
                     named: dict[str, OpLayout]) -> Contour | None:
    what = op["what"]
    face = p.face(op["face"])
    if what == "outline":
        return OutlineContour(face)
    if what in named:
        target = named[what]
        if target["kind"] == "cut":
            return ShapeContour(face, p.rings(face, target["shape"]))
        if target["kind"] == "pocket":
            f = p.face(target["face"])
            return ShapeContour(f, p.rings(f, target["shape"]))
        if target["kind"] == "hole":
            f = p.face(target["face"])
            return CircleContour(f, p.point(f, target["u"], target["v"]), target["d"] / 2)
        if target["kind"] == "edge":
            f = p.face(target["face"])
            inner = target["op"]
            if inner["kind"] == "pocket":
                return ShapeContour(f, p.rings(f, inner["shape"], (target["s"], target["t"])))
            return CircleContour(f, p.point(f, target["s"], target["t"]), inner["d"] / 2)
        return None
    parts = what.split(".")
    if len(parts) == 2 and all(p.frame.is_direction(n) for n in parts):
        return EdgeContour(p.face(parts[0]), p.face(parts[1]))
    return None


def plan_layout(layout: Layout) -> Plan:
    if layout["version"] != 1:
        raise ValueError(f"layout version {layout['version']} is not supported (expected 1).")
    frame = _Frame(layout["frame"])
    problems: list[str] = list(layout["problems"])
    parts: list[PartPlan] = []
    hardware: list[HardwarePlan] = []
    for module in layout["modules"]:
        problems.extend(module["problems"])
        for part in module["parts"]:
            parts.append(plan_part(part, frame, problems))
        for item in module.get("hardware", []):
            hardware.append(plan_hardware(item))
    return Plan(parts, problems, hardware)


def _code_vector(code: str) -> Vec:
    return _unit(_as_axis(code[1]), 1 if code[0] == "+" else -1)


def plan_hardware(item: HardwareLayout) -> HardwarePlan:
    segments = item["path"].split(".")
    o = item["origin"]
    return HardwarePlan(
        item["path"], tuple(segments[:-1]), item["name"], item["model"], (o[0], o[1], o[2]),
        (_code_vector(item["axes"]["x"]), _code_vector(item["axes"]["y"]), _code_vector(item["axes"]["z"])),
        [HardwareBodyPlan(b["name"], (b["offset"][0], b["offset"][1], b["offset"][2])) for b in item["bodies"]],
    )
