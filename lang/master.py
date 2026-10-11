"""The master document, as its snapshot: `van = master("snapshot.json")`.

The snapshot (`lang.core.snapshot_types`) is written in Fusion by the
compiler add-in's Snapshot button and is the build's only view of the
master. Four kinds of reference, each looked up by the name it has in
Fusion:

- `van.plane(name)`: a construction plane. An axis-aligned plane is a
  position, usable wherever one is expected (`on`, `between`, `spread`,
  arithmetic); a tilted one is an error when it is used as a position.
- `van.box(name)`: a placeholder body as a `Box`, for a module to stand
  in (`module("kitchen", van.box("Kueche"), front=...)`). A body that is
  not an axis-aligned cuboid gives its bounding box and a note in the
  layout's problems.
- `van.param(name)`: a user parameter as a number (mm for lengths,
  degrees for angles).
- `van.contour(name)`: a sketch as a `Contour`, a limit for `between()`.

A missing name, a name the master uses twice and a sketch that is not one
chain of curves are errors when the name is used. A relative path is taken
from the directory of the file that calls `master()`. The layout records
the snapshot's hash and carries its boxes and contours for the preview.
"""
from __future__ import annotations

import difflib
import inspect
import json
from pathlib import Path
from typing import overload

from .core.box import Box
from .core.contours import Contour
from .core.directions import AXES, Axis
from .core.errors import LangError
from .core.layout_types import SnapshotLayout
from .core.refs import Affine, HasPosition, Pos
from .core.scope import registry
from .core.snapshot_types import SNAPSHOT_VERSION, SnapshotDict

_KIND_WORDS = {"planes": "plane", "contours": "contour", "boxes": "box", "parameters": "parameter"}


class Plane:
    """A construction plane of the master. When it is axis aligned it is a
    position on its axis (`position`), so it works wherever a position
    does."""

    def __init__(self, name: str, origin: list[float], normal: list[float]):
        self.name = name
        self.origin = (origin[0], origin[1], origin[2])
        self.normal = (normal[0], normal[1], normal[2])

    @property
    def axis(self) -> Axis | None:
        """The world axis the plane is perpendicular to, or None when tilted."""
        for i, axis in enumerate(AXES):
            if abs(abs(self.normal[i]) - 1.0) < 1e-6:
                return axis
        return None

    @property
    def position(self) -> Pos:
        axis = self.axis
        if axis is None:
            raise LangError(f"plane {self.name!r} is tilted (normal {self.normal}); "
                            "only an axis-aligned plane is a position.")
        return Pos(axis, self.origin[AXES.index(axis)])

    @property
    def value(self) -> float:
        return self.position.value

    @overload
    def __add__(self, other: float) -> Pos: ...
    @overload
    def __add__(self, other: Pos | Affine | HasPosition) -> Pos | Affine: ...

    def __add__(self, other: float | Pos | Affine | HasPosition) -> Pos | Affine:
        return self.position + other

    def __radd__(self, other: float) -> Pos:
        return self.position + other

    @overload
    def __sub__(self, other: float) -> Pos: ...
    @overload
    def __sub__(self, other: Pos | HasPosition) -> float: ...

    def __sub__(self, other: float | Pos | HasPosition) -> Pos | float:
        return self.position - other

    def __mul__(self, other: float) -> Affine:
        return self.position * other

    __rmul__ = __mul__

    def __truediv__(self, other: float) -> Affine:
        return self.position / other

    def __repr__(self) -> str:
        axis = self.axis
        where = f"{axis}={self.origin[AXES.index(axis)]:g}" if axis else "tilted"
        return f"Plane({self.name!r}, {where})"


class Master:
    """A snapshot of the master document, read once."""

    def __init__(self, path: Path, data: SnapshotDict):
        if data.get("version") != SNAPSHOT_VERSION:
            raise LangError(f"{path.name}: snapshot version {data.get('version')}, "
                            f"this language reads {SNAPSHOT_VERSION}. Take a new snapshot.")
        self.path = path
        self.data = data
        self.source = data["source"]
        self.hash = data["hash"]
        self._tables: dict[str, dict[str, object]] = {
            "planes": dict(data["planes"]), "contours": dict(data["contours"]),
            "boxes": dict(data["boxes"]), "parameters": dict(data["parameters"])}
        self._problems = {(p["kind"], p["name"]): p["message"] for p in data["problems"]}
        #: Remarks for the layout's problems, e.g. a box that is only a bounding box.
        self.notes: list[str] = []

    def __repr__(self) -> str:
        return f"Master({self.path.name}, {self.source!r})"

    def _lookup(self, kind: str, name: str) -> object:
        registry.use_snapshot(self)
        table = self._tables[kind]
        if name in table:
            return table[name]
        word = _KIND_WORDS[kind]
        problem = self._problems.get((kind, name))
        if problem is not None:
            raise LangError(f"{word} {name!r} in the master: {problem}.")
        close = difflib.get_close_matches(name, list(table), n=3)
        hint = f"; did you mean {', '.join(repr(c) for c in close)}?" if close else \
            f"; it has {', '.join(repr(n) for n in sorted(table)) or 'none'}."
        raise LangError(f"the master ({self.path.name}) has no {word} {name!r}{hint}")

    def names(self, kind: str) -> list[str]:
        """The names of one kind: "planes", "contours", "boxes" or "parameters"."""
        return sorted(self._tables[kind])

    def plane(self, name: str) -> Plane:
        data = self.data["planes"]
        self._lookup("planes", name)
        return Plane(name, data[name]["origin"], data[name]["normal"])

    def box(self, name: str) -> Box:
        self._lookup("boxes", name)
        data = self.data["boxes"][name]
        if not data["cuboid"]:
            note = f"box {name!r} is not an axis-aligned cuboid in the master; its bounding box is used"
            if note not in self.notes:
                self.notes.append(note)
        lo: dict[Axis, float] = {a: data["min"][i] for i, a in enumerate(AXES)}
        hi: dict[Axis, float] = {a: data["max"][i] for i, a in enumerate(AXES)}
        return Box(lo, hi)

    def param(self, name: str) -> float:
        self._lookup("parameters", name)
        return float(self.data["parameters"][name]["value"])

    def contour(self, name: str) -> Contour:
        self._lookup("contours", name)
        data = self.data["contours"][name]
        points = tuple((p[0], p[1], p[2]) for p in data["points"])
        o, n = data["plane"]["origin"], data["plane"]["normal"]
        return Contour(name, points, data["closed"], (o[0], o[1], o[2]), (n[0], n[1], n[2]))

    def to_layout(self) -> SnapshotLayout:
        """What the layout carries: the hash, and boxes and contours for the
        preview."""
        return {
            "file": self.path.name,
            "source": self.source,
            "hash": self.hash,
            "boxes": {name: {"min": b["min"], "max": b["max"], "cuboid": b["cuboid"]}
                      for name, b in self.data["boxes"].items()},
            "contours": {name: {"points": c["points"], "closed": c["closed"]}
                         for name, c in self.data["contours"].items()},
        }


def master(path: str | Path) -> Master:
    """Reads a snapshot of the master document. A relative path is taken
    from the directory of the calling file."""
    p = Path(path)
    if not p.is_absolute():
        frame = inspect.currentframe()
        caller = frame.f_back if frame is not None else None
        file = caller.f_globals.get("__file__") if caller is not None else None
        p = (Path(str(file)).resolve().parent if file else Path.cwd()) / p
    p = p.resolve()
    if not p.is_file():
        raise LangError(f"no snapshot at {p}; take one with the Snapshot button in Fusion.")
    found = Master(p, json.loads(p.read_text(encoding="utf-8")))
    registry.use_snapshot(found)
    return found
