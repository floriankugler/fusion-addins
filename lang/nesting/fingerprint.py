"""A part's fingerprint: a hash of itself as machined, not of where it sits
in the build [decided 2026-10-16, `design/nesting.md`, Pinning].

What goes in: its material and thickness, its grain where it is set, its
outline and every operation (cuts with a chamfer, pockets, holes,
V-grooves, chamfers, a narrow face's operations), each with its sizes and
its face, all in its nest frame: seen from its machining face, which is
`top`, the opposite face `bottom`, the narrow faces `+X`, `-X`, `+Y`, `-Y`,
from the outline's lower corner (`lang.nesting.items`, as the nest lays
it). So the machining face goes in too: machined from its other face, a
part is another part. What stays out: where the part is and which way it
faces in the build, its name and its operations' names (a chamfer along a
named operation takes that operation's geometry), the order its
operations were made in, how a depth was written, a cut without a chamfer
(the outline has it), and its settings. A part moved, turned in its plane
or set facing another way keeps its fingerprint, as long as its grain turns
with it; one with a hole added, another size or another material changes
it.

How: the part is described in each of the four quarter turns in its plane
and the least of the four hashes kept, so a turn is the same part. In a
turn every coordinate is taken from the outline's lower corner and, like
every size, rounded to `GRID` (1/1024 mm), each ring started at its least
point and run the way that comes first, a shape's rings and the
operations sorted, so that the noise of another position, the order of a
polygon's points and of the operations do not count. The grid is binary
so that no value written with up to four decimals of a millimetre lies
halfway between two of its steps, where the noise could tip it either
way [found by fuzzing, 2026-10-16: a length of 410.4875 mm rounded to
micrometres came out 410.487 in one world frame and 410.488 in another].
Hashes are SHA-256; the fingerprint is the first 16 hex digits
(`LENGTH`).
"""
from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any

import numpy as np
import numpy.typing as npt

from ..core.errors import LangError
from ..core.layout_types import Layout, OpLayout, PartLayout, Rings

#: Steps per millimetre a coordinate or size is rounded to (see the module's doc).
GRID = 1024
#: Hex digits of the hash kept.
LENGTH = 16
AXES = ("x", "y", "z")
_RIGHT_HANDED = {("x", "y", "z"), ("y", "z", "x"), ("z", "x", "y")}
#: The narrow faces in the order a quarter turn counter-clockwise takes them.
_SIDES = ("+X", "+Y", "-X", "-Y")

Floats = npt.NDArray[np.float64]
Ints = npt.NDArray[np.int64]
#: A face's label: "top" or "bottom", or a narrow face by its index in `_SIDES` before any turn.
Face = str | int


def fingerprints(layout: Layout) -> dict[str, str]:
    """Every board's fingerprint by path (slats are not machined)."""
    return {p["path"]: fingerprint(p, layout["frame"]) for m in layout["modules"] for p in m["parts"]
            if p["kind"] == "board"}


def fingerprint(part: PartLayout, frame: Mapping[str, str], mirror: bool = False) -> str:
    """The part's fingerprint (see the module's doc); `frame` is the
    layout's, direction names to world axes (`front`: `-x`). `mirror`: its
    mirror image's, as a build in a world frame of the other hand makes it
    (the fuzz tests compare such builds)."""
    described = _Described(part, frame, mirror)
    return min(described.digest(turn) for turn in range(4))[:LENGTH]


# -- the part in its nest frame, before any turn ------------------------------------------------------

@dataclass
class _Shape:
    """Rings: whether each is an exterior (else a hole) as the layout
    writes it, and its points."""
    rings: list[tuple[bool, Floats]]


@dataclass
class _Op:
    """An operation: its sizes (`head`), its face, its shape and points,
    and for a chamfer what it follows: "outline", another operation (its
    index), or faces."""
    head: dict[str, Any]
    face: Face | None = None
    shape: _Shape | None = None
    #: Points; `sorted` when their order says nothing (a line's ends).
    points: list[Floats] = field(default_factory=list[Floats])
    sorted: bool = False
    follows: int | None = None
    faces: list[Face] | None = None


class _Described:
    """The part as its nest frame sees it: x along u (negated where u runs
    the other way seen from the machining face), y along v, z up from the
    face it lies on, before the outline's corner is taken off."""

    def __init__(self, part: PartLayout, frame: Mapping[str, str], mirror: bool = False):
        self.path = part["path"]
        #: The cuts named, by their index in `ops`, for a chamfer along one.
        self.cuts: dict[int, OpLayout] = {}
        self.dirs = {name: (code[1], 1 if code[0] == "+" else -1) for name, code in frame.items()}
        axes = part["axes"]
        self.t, self.u, self.v = axes["t"], axes["u"], axes["v"]
        axis, self.up = self.dirs[part["machine"]]
        if axis != self.t:
            raise LangError(f"{part['path']}: its machining face {part['machine']} is not a big face.")
        handed = 1 if (self.u, self.v, self.t) in _RIGHT_HANDED else -1
        self.sx = -1.0 if (handed * self.up < 0) != mirror else 1.0
        self.lo: dict[str, float] = dict(zip(AXES, part["box"]["min"]))
        self.hi: dict[str, float] = dict(zip(AXES, part["box"]["max"]))
        self.z0 = self.lo[self.t] if self.up > 0 else -self.hi[self.t]
        grain = part["grain"] if part["grained"] else None
        if grain is not None and grain not in (self.u, self.v):
            raise LangError(f"{part['path']}: its grain {grain} is not in its plane.")
        #: 0 along x, 1 along y, before any turn.
        self.grain = None if grain is None else (0 if grain == self.u else 1)
        self.head = {"material": part["material"], "thickness": _round(part["thickness"])}
        self.outline = self._shape(part["outline"], self.u, self.v, None, (0.0, 0.0))
        self.corners = np.concatenate([points[:, :2] for _ext, points in self.outline.rings]) \
            if self.outline.rings else np.zeros((1, 2))
        self.show = part["show"]
        self.ops: list[_Op] = []
        #: The operations that count; a cut without a chamfer is kept only
        #: for a chamfer along it.
        self.counted: list[int] = []
        named: dict[str, int] = {}
        chamfers: list[OpLayout] = []
        for op in part["ops"]:
            if op["kind"] == "chamfer":
                chamfers.append(op)
                continue
            name = op["op"]["name"] if op["kind"] == "edge" else op["name"]
            described = self._op(op)
            if described is None and not (name and op["kind"] == "cut"):
                continue
            k = len(self.ops)
            self.ops.append(described or _Op({"kind": "cut"}))
            if described is not None:
                self.counted.append(k)
            if name:
                named[name] = k
                if op["kind"] == "cut":
                    self.cuts[k] = op
        for op in chamfers:
            self.counted.append(len(self.ops))
            self.ops.append(self._chamfer(op, named))

    # -- frames ------------------------------------------------------------------------------------

    def _face(self, name: str) -> tuple[str, float, Face]:
        """A face by direction name: its world axis, its plane, its label."""
        axis, sign = self.dirs[name]
        value = self.hi[axis] if sign > 0 else self.lo[axis]
        if axis == self.t:
            return axis, value, "top" if sign == self.up else "bottom"
        return axis, value, (0 if self.sx * sign > 0 else 2) if axis == self.u else (1 if sign > 0 else 3)

    def _points(self, ab: Floats, first: str, second: str, fixed: tuple[str, float] | None) -> Floats:
        """Points given along two world axes (and one more held at a value)
        in the nest frame: (x, y), or (x, y, z) where the thickness's axis
        is known."""
        world: dict[str, Floats] = {first: ab[:, 0], second: ab[:, 1]}
        if fixed is not None:
            world[fixed[0]] = np.full(len(ab), fixed[1])
        n = len(ab)
        x = self.sx * world[self.u] if self.u in world else np.zeros(n)
        y = world[self.v] if self.v in world else np.zeros(n)
        if self.t not in world:
            return np.column_stack([x, y])
        return np.column_stack([x, y, self.up * world[self.t] - self.z0])

    def _in_face(self, axis: str, value: float, ab: Floats) -> Floats:
        """Points in a face's 2D frame ((u, v) on a big face, (s, t) on a
        narrow one, as `lang.emit.plan` reads them) in the nest frame."""
        if axis == self.t:
            return self._points(ab, self.u, self.v, (axis, value))
        return self._points(ab, self.v if axis == self.u else self.u, self.t, (axis, value))

    def _shape(self, rings: Rings, first: str, second: str, fixed: tuple[str, float] | None,
               at: tuple[float, float]) -> _Shape:
        out: list[tuple[bool, Floats]] = []
        for ring in rings:
            ab = np.asarray(ring, dtype=np.float64).reshape(-1, 2)
            out.append((_area(ab) > 0, self._points(ab + np.asarray(at), first, second, fixed)))
        return _Shape(out)

    def _face_shape(self, rings: Rings, face: str, at: tuple[float, float], offset: float = 0.0) -> _Shape:
        axis, value, _label = self._face(face)
        value += self.dirs[face][1] * offset
        if axis == self.t:
            return self._shape(rings, self.u, self.v, (axis, value), at)
        return self._shape(rings, self.v if axis == self.u else self.u, self.t, (axis, value), at)

    # -- the operations ----------------------------------------------------------------------------

    def _op(self, op: OpLayout) -> _Op | None:
        if op["kind"] == "cut":
            if op["chamfer"] <= 0:
                return None             # the outline has it
            return _Op({"kind": "cut", "chamfer": _round(op["chamfer"])}, self._face(self.show)[2],
                       self._face_shape(op["shape"], self.show, (0.0, 0.0)))
        if op["kind"] == "pocket" or op["kind"] == "hole":
            return self._cut_in(op, op["face"], None, 0.0)
        if op["kind"] == "edge":
            return self._cut_in(op["op"], op["face"], (op["s"], op["t"]), op.get("offset", 0.0))
        if op["kind"] == "vgroove":
            axis, value, label = self._face(op["face"])
            ends = np.asarray([op["start"], op["end"]], dtype=np.float64)
            return _Op({"kind": "vgroove", "depth": _round(op["depth"])}, label,
                       points=[self._in_face(axis, value, ends)], sorted=True)
        raise AssertionError(op["kind"])

    def _cut_in(self, op: OpLayout, face: str, at: tuple[float, float] | None, offset: float) -> _Op:
        """A pocket or a hole from `face`; for a narrow face's operation
        (`at` given, as `lang.emit.plan` reads it) a hole at `at`, a
        pocket's points moved by it, the face moved out by `offset`."""
        axis, value, label = self._face(face)
        value += self.dirs[face][1] * offset
        head: dict[str, Any] = {"offset": _round(offset)} if offset else {}
        if op["kind"] == "hole":
            a, b = at if at is not None else (op["u"], op["v"])
            head |= {"kind": "hole", "d": _round(op["d"]), "depth": _round(op["depth"]), "through": op["through"],
                     "chamfer": _round(op["chamfer"])}
            return _Op(head, label, points=[self._in_face(axis, value, np.asarray([[a, b]], dtype=np.float64))])
        assert op["kind"] == "pocket"
        moved = at if at is not None else (0.0, 0.0)
        head |= {"kind": "pocket", "depth": _round(op["depth"]), "chamfer": _round(op["chamfer"])}
        out = _Op(head, label, self._face_shape(op["shape"], face, moved, offset))
        slot = op["slot"]
        if slot is not None:
            head["slot"] = _round(slot["width"])
            ends = np.asarray([slot["start"], slot["end"]], dtype=np.float64) + np.asarray(moved)
            out.points, out.sorted = [self._in_face(axis, value, ends)], True
        return out

    def _chamfer(self, op: OpLayout, named: dict[str, int]) -> _Op:
        """A chamfer: along the outline, a named operation (its geometry,
        a cut's on the chamfer's face), or where two faces meet."""
        assert op["kind"] == "chamfer"
        _axis, _value, label = self._face(op["face"])
        out = _Op({"kind": "chamfer", "size": _round(op["size"])}, label)
        what = op["what"]
        if what in named:
            k = named[what]
            cut = self.cuts.get(k)
            if cut is not None and cut["kind"] == "cut":
                out.shape = self._face_shape(cut["shape"], op["face"], (0.0, 0.0))
            else:
                out.follows = k
            return out
        names = what.split(".")
        if what != "outline" and len(names) == 2 and all(n in self.dirs for n in names):
            out.faces = [self._face(n)[2] for n in names]
        else:
            out.head["what"] = what
        return out

    # -- one turn --------------------------------------------------------------------------------

    def digest(self, turn: int) -> str:
        """The hash of the part turned by `turn` quarter turns."""
        corners = _turned(self.corners, turn)
        origin = corners.min(axis=0) if len(corners) else np.zeros(2)
        digests: list[str] = []
        for op in self.ops:
            digests.append(self._op_digest(op, turn, origin, digests))
        head = dict(self.head, grain=None if self.grain is None else "XY"[(self.grain + turn) % 2])
        h = hashlib.sha256(_json(head))
        h.update(_shape_digest(self.outline, turn, origin).encode())
        for d in sorted(digests[k] for k in self.counted):
            h.update(d.encode())
        return h.hexdigest()

    def _op_digest(self, op: _Op, turn: int, origin: Floats, done: list[str]) -> str:
        head = dict(op.head, face=_label(op.face, turn))
        if op.faces is not None:
            head["faces"] = sorted(str(_label(f, turn)) for f in op.faces)
        h = hashlib.sha256(_json(head))
        if op.shape is not None:
            h.update(_shape_digest(op.shape, turn, origin).encode())
        if op.follows is not None:
            h.update(done[op.follows].encode())
        for points in op.points:
            ints = _ints(points, turn, origin)
            if op.sorted:
                ints = ints[np.lexsort(ints.T[::-1])]
            h.update(_bytes(ints))
        return h.hexdigest()


# -- helpers ----------------------------------------------------------------------------------------

def _label(face: Face | None, turn: int) -> str | None:
    if face is None or isinstance(face, str):
        return face
    return _SIDES[(face + turn) % 4]


def _turned(points: Floats, turn: int) -> Floats:
    """x, y turned by `turn` quarter turns counter-clockwise (exactly)."""
    out = points.copy()
    x, y = points[:, 0], points[:, 1]
    if turn % 4 == 1:
        out[:, 0], out[:, 1] = -y, x
    elif turn % 4 == 2:
        out[:, 0], out[:, 1] = -x, -y
    elif turn % 4 == 3:
        out[:, 0], out[:, 1] = y, -x
    return out


def _ints(points: Floats, turn: int, origin: Floats) -> Ints:
    """Points turned, from `origin` (x, y), in steps of the grid."""
    out = _turned(points, turn)
    out[:, :2] -= origin
    return np.rint(out * GRID).astype(np.int64)


def _shape_digest(shape: _Shape, turn: int, origin: Floats) -> str:
    rings = sorted(("o" if ext else "h") + _bytes(_ring(_ints(points, turn, origin))).hex()
                   for ext, points in shape.rings)
    return hashlib.sha256("|".join(rings).encode()).hexdigest()


def _ring(points: Ints) -> Ints:
    """A closed ring started at its least point, run the way whose next
    point comes first; a point equal to the one before it (the closing
    one, or two the rounding made one) dropped."""
    if len(points) < 2:
        return points
    keep = np.any(points != np.roll(points, 1, axis=0), axis=1)
    ring = points[keep] if keep.any() else points[:1]
    n = len(ring)
    if n < 2:
        return ring
    order = np.lexsort(ring.T[::-1])
    least = ring[order[0]]
    starts = [int(k) for k in np.nonzero(np.all(ring == least, axis=1))[0]]
    best: Ints | None = None
    for k in starts:
        forward = np.roll(ring, -k, axis=0)
        backward = np.concatenate([forward[:1], forward[:0:-1]])
        for candidate in (forward, backward):
            if best is None or candidate.tolist() < best.tolist():
                best = candidate
    assert best is not None
    return best


def _bytes(points: Ints) -> bytes:
    return np.ascontiguousarray(points, dtype="<i8").tobytes() + bytes([points.shape[1] if points.ndim == 2 else 0])


def _json(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def _round(v: float) -> int:
    """A size in steps of the grid."""
    return round(v * GRID)


def _area(ring: Floats) -> float:
    x, y = ring[:, 0], ring[:, 1]
    return float(np.dot(x, np.roll(y, -1)) - np.dot(np.roll(x, -1), y)) / 2


__all__ = ["fingerprint", "fingerprints", "GRID", "LENGTH"]
