"""The Fusion-free half of the snapshot writer: what `snapshot.py` reads
from the master goes through a `Collector`, which names items by their
component path, skips double-underscore names, chains each sketch's sampled
curves into one contour, reports duplicate names, and builds the snapshot
with its hash. Unit tested.

Names: an item in the root component keeps its own name; an item inside
components is named by the path of component names from the root, dotted,
then its own name (`Bett.oben`, `Moebel.Sitzbank.Sitz`). A body that is a
component's only body takes the component's path (`Moebel.Kueche`).

The snapshot's shape is `lang.core.snapshot_types`.
"""
from __future__ import annotations

import hashlib
import json
import math
from collections.abc import Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, cast

if TYPE_CHECKING:
    from ..core.snapshot_types import (BoxDict, ContourDict, ParameterDict, PlaneDict, ProblemDict,
                                       SnapshotDict)

SNAPSHOT_VERSION = 1
#: Names starting with this are left out of the snapshot.
SKIP_PREFIX = "__"
#: Curve ends closer than this (mm) meet.
JOIN_TOLERANCE = 0.01
#: Coordinates are written with this many decimals (0.1 micrometre).
DECIMALS = 4

Point3 = tuple[float, float, float]
KINDS = ("planes", "contours", "boxes", "parameters")


class ChainError(Exception):
    """A sketch's curves do not form one chain."""


def _close(a: Point3, b: Point3, tolerance: float) -> bool:
    return math.dist(a, b) <= tolerance


def _fmt(p: Point3) -> str:
    return "(" + ", ".join(f"{c:g}" for c in p) + ")"


def chain(polylines: Sequence[Sequence[Point3]], tolerance: float = JOIN_TOLERANCE) -> tuple[list[Point3], bool]:
    """Orders sampled curves into one chain: the points in order and
    whether the chain is closed (a closed chain does not repeat its first
    point). Curves may run either way. Raises ChainError when the curves
    are empty, branch, or form several chains."""
    curves = [list(c) for c in polylines if len(c) >= 2 and math.dist(c[0], c[-1]) + math.dist(c[0], c[1]) > 0]
    if not curves:
        raise ChainError("no curves (construction curves do not count)")
    # Endpoints that meet share a node.
    nodes: list[Point3] = []

    def node_of(p: Point3) -> int:
        for i, q in enumerate(nodes):
            if _close(p, q, tolerance):
                return i
        nodes.append(p)
        return len(nodes) - 1

    ends = [(node_of(c[0]), node_of(c[-1])) for c in curves]
    degree = [0] * len(nodes)
    for a, b in ends:
        degree[a] += 1
        degree[b] += 1
    for i, d in enumerate(degree):
        if d > 2:
            raise ChainError(f"{d} curves meet at {_fmt(nodes[i])}; a contour is one chain without branches")
    # Connected components (union-find over nodes).
    parent = list(range(len(nodes)))

    def find(i: int) -> int:
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    for a, b in ends:
        parent[find(a)] = find(b)
    groups = {find(a) for a, _ in ends}
    if len(groups) > 1:
        raise ChainError(f"{len(groups)} separate chains of curves; a contour is one chain")
    # Walk from an open end, or anywhere on a loop.
    start = next((i for i, d in enumerate(degree) if d == 1), ends[0][0])
    closed = all(d == 2 for d in degree)
    used = [False] * len(curves)
    points: list[Point3] = [nodes[start]]
    here = start
    for _ in curves:
        k = next(k for k, (a, b) in enumerate(ends) if not used[k] and here in (a, b))
        used[k] = True
        a, b = ends[k]
        pts = curves[k] if a == here else list(reversed(curves[k]))
        points.extend(pts[1:])
        here = b if a == here else a
    if closed:
        points.pop()   # back at the start
    return points, closed


def _r(x: float) -> float:
    value = round(float(x), DECIMALS)
    return 0.0 if value == 0 else value


def _point(p: Sequence[float]) -> list[float]:
    return [_r(c) for c in p]


def _unit(v: Sequence[float]) -> list[float]:
    length = math.sqrt(sum(c * c for c in v))
    if length == 0:
        raise ValueError("zero normal")
    # Normals get more decimals: they are directions, not positions.
    return [0.0 if round(c / length, 9) == 0 else round(c / length, 9) for c in v]


@dataclass
class _Entry:
    where: str
    data: Any = None
    problem: str | None = None


def path_name(path: str, name: str) -> str:
    """An item's name in the snapshot: its component path, dotted, then its
    own name; just its own name in the root (`path` empty)."""
    return f"{path}.{name}" if path else name


class Collector:
    """Gathers what the master holds, by kind and name. `path` is the
    dotted path of the component an item is in ("" for the root); `where`
    says where it was found, for messages about duplicates. An item whose
    own name starts with a double underscore is left out."""

    def __init__(self) -> None:
        self._entries: dict[str, dict[str, list[_Entry]]] = {kind: {} for kind in KINDS}
        self.skipped = 0

    def _add(self, kind: str, path: str, name: str, entry: _Entry) -> None:
        if name.startswith(SKIP_PREFIX):
            self.skipped += 1
            return
        self._entries[kind].setdefault(path_name(path, name), []).append(entry)

    def plane(self, path: str, name: str, where: str, origin: Sequence[float], normal: Sequence[float]) -> None:
        data: PlaneDict = {"origin": _point(origin), "normal": _unit(normal)}
        self._add("planes", path, name, _Entry(where, data))

    def contour(self, path: str, name: str, where: str, polylines: Sequence[Sequence[Point3]],
                plane_origin: Sequence[float], plane_normal: Sequence[float]) -> None:
        """A sketch: its non-construction curves, each sampled to a
        polyline, and the sketch plane."""
        try:
            points, closed = chain(polylines)
        except ChainError as error:
            self._add("contours", path, name, _Entry(where, problem=str(error)))
            return
        data: ContourDict = {
            "points": [_point(p) for p in points], "closed": closed,
            "plane": {"origin": _point(plane_origin), "normal": _unit(plane_normal)},
        }
        self._add("contours", path, name, _Entry(where, data))

    def box(self, path: str, name: str, where: str, lo: Sequence[float], hi: Sequence[float],
            cuboid: bool) -> None:
        data: BoxDict = {"min": _point(lo), "max": _point(hi), "cuboid": cuboid}
        self._add("boxes", path, name, _Entry(where, data))

    def parameter(self, name: str, value: float, unit: str, expression: str) -> None:
        """A user parameter; these belong to the whole design, so no path."""
        data: ParameterDict = {"value": _r(value), "unit": unit, "expression": expression}
        self._add("parameters", "", name, _Entry("user parameters", data))

    def problem(self, kind: str, path: str, name: str, where: str, message: str) -> None:
        """An item that cannot be taken, e.g. a surface body."""
        self._add(kind, path, name, _Entry(where, problem=message))

    def build(self, source: str) -> SnapshotDict:
        tables: dict[str, dict[str, Any]] = {kind: {} for kind in KINDS}
        problems: list[ProblemDict] = []
        for kind in KINDS:
            for name in sorted(self._entries[kind]):
                entries = self._entries[kind][name]
                if len(entries) > 1:
                    # (in order, not as Fusion listed them: the same master gave another hash when
                    # its components came in another order [found by fuzzing, 2026-10-14])
                    places = ", ".join(sorted(e.where for e in entries))
                    problems.append({"kind": kind, "name": name, "message": f"named twice ({places})"})
                elif entries[0].problem is not None:
                    problems.append({"kind": kind, "name": name,
                                     "message": f"{entries[0].problem} ({entries[0].where})"})
                else:
                    tables[kind][name] = entries[0].data
        snapshot: SnapshotDict = {
            "version": SNAPSHOT_VERSION, "units": "mm", "source": source, "hash": "",
            "planes": tables["planes"], "contours": tables["contours"],
            "boxes": tables["boxes"], "parameters": tables["parameters"], "problems": problems,
        }
        snapshot["hash"] = content_hash(snapshot)
        return snapshot


def content_hash(snapshot: SnapshotDict) -> str:
    """sha256 of everything but the source document's name and the hash."""
    content = {k: v for k, v in snapshot.items() if k not in ("source", "hash")}
    text = json.dumps(content, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _is_number(value: object) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def dumps(value: object, indent: int = 0) -> str:
    """JSON with one key per line and each point on one line, so that a
    snapshot diffs readably."""
    pad, inner = "  " * indent, "  " * (indent + 1)
    if isinstance(value, dict):
        items = cast(dict[str, object], value)
        if not items:
            return "{}"
        body = ",\n".join(f"{inner}{json.dumps(k, ensure_ascii=False)}: {dumps(v, indent + 1)}"
                          for k, v in items.items())
        return "{\n" + body + "\n" + pad + "}"
    if isinstance(value, list):
        elements = cast(list[object], value)
        if not elements:
            return "[]"
        if all(_is_number(e) for e in elements):
            return "[" + ", ".join(json.dumps(e) for e in elements) + "]"
        body = ",\n".join(inner + dumps(e, indent + 1) for e in elements)
        return "[\n" + body + "\n" + pad + "]"
    return json.dumps(value, ensure_ascii=False)
