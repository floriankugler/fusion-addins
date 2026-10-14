"""Random sketches and masters for fuzzing the snapshot's Fusion-free half
(`lang.emit.snapshot_format`) and its reading (`lang.master`), as the other
harnesses fuzz the language: a case is plain data, and the checks look
from the outside.

A `ChainCase` is a chain of points, open or closed, cut into curves where
a sketch's curves meet, the curves given in any order, some run the other
way, their ends moved by less than half the join tolerance, with curves
that do not count among them (a single point, a curve of no length); now
and then with a curve shorter than the join tolerance at a join, or every
curve drawn twice; or several such chains, or one with a curve branching
off. `chain_problems` checks that `chain()` gives back the chain (from
either end, a closed one from any of its joins, each point within the
noise of its own) or refuses several chains, branches and curves closing
around nothing as its docstring says.

A `MasterCase` is what Fusion would hand the writer: planes, sketches (as
chain cases), bodies, user parameters and problems, by component path and
name, among them names made twice and names left out (`__...`). The
checks: the snapshot is the same whichever order the items come in;
`dumps` writes JSON that reads back as the snapshot, the same text for an
equal snapshot; `content_hash` does not depend on the order of keys and
covers everything but the source's name; and `master()` reads the file
back to the planes, contours, boxes and parameters given (rounded as the
writer rounds them), with the problems and missing names as errors."""
from __future__ import annotations

import copy
import dataclasses
import json
import math
import random
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

from hypothesis import assume
from hypothesis import strategies as st

from fuzzing import floats, sizes
from lang.core.errors import LangError
from lang.core.snapshot_types import SnapshotDict
from lang.emit.snapshot_format import (DECIMALS, JOIN_TOLERANCE, SKIP_PREFIX, ChainError, Collector, chain,
                                       content_hash, dumps, path_name)
from lang.master import master

Point3 = tuple[float, float, float]


# -- chains ---------------------------------------------------------------------------------------------

@dataclass(frozen=True)
class Chain:
    """A chain's points in order (a closed one without repeating its
    first), and where it is cut into curves: the indices of the points
    where one curve ends and the next begins (a closed chain's first cut
    is where its first curve starts)."""
    points: tuple[Point3, ...]
    closed: bool
    cuts: tuple[int, ...]

    def curves(self) -> list[list[Point3]]:
        pts, cuts = list(self.points), list(self.cuts)
        if not self.closed:
            bounds = [0] + cuts + [len(pts) - 1]
            return [pts[a:b + 1] for a, b in zip(bounds, bounds[1:])]
        ring = pts[cuts[0]:] + pts[:cuts[0]] + [pts[cuts[0]]]
        local = [c - cuts[0] if c >= cuts[0] else c - cuts[0] + len(pts) for c in cuts] + [len(pts)]
        return [ring[a:b + 1] for a, b in zip(local, local[1:])]

    def joins(self) -> list[Point3]:
        """The points where curves meet, and the open ends."""
        if self.closed:
            return [self.points[c] for c in self.cuts]
        return [self.points[0]] + [self.points[c] for c in self.cuts] + [self.points[-1]]


@dataclass(frozen=True)
class ChainCase:
    """Chains as a sketch's curves: the curves of all of them in the order
    `order`, those in `flips` run the other way, each curve's first and
    last points moved by its `noise` (per curve, in the chains' order), and
    `junk` curves that do not count; with `branch`, a curve from the join of
    that index of the first chain to a point off it."""
    chains: tuple[Chain, ...]
    order: tuple[int, ...]
    flips: tuple[bool, ...]
    noise: tuple[tuple[Point3, Point3], ...]
    junk: tuple[tuple[Point3, ...], ...] = ()
    branch: int | None = None
    #: A curve no longer than the join tolerance at the join of that index
    #: of the first chain, from the join to the join moved by the vector:
    #: the next curve starts there (as Fusion's curves share their ends).
    tiny: tuple[int, Point3] | None = None
    #: The first chain's curves given twice over (the same lines drawn twice).
    doubled: bool = False

    def curves(self) -> list[list[Point3]]:
        made = [c for ch in self.chains for c in ch.curves()]
        if self.tiny is not None:
            made = self._with_tiny(made)
        if self.doubled:
            made += [list(c) for c in self.chains[0].curves()]
        if self.branch is not None:
            j = self.chains[0].joins()[self.branch]
            made.append([j, (j[0] + 37.0, j[1] + 11.0, j[2] - 5.0)])
        moved: list[list[Point3]] = []
        for k, c in enumerate(made):
            (a, b) = self.noise[k] if k < len(self.noise) else ((0.0, 0.0, 0.0), (0.0, 0.0, 0.0))
            c = list(c)
            c[0] = (c[0][0] + a[0], c[0][1] + a[1], c[0][2] + a[2])
            c[-1] = (c[-1][0] + b[0], c[-1][1] + b[1], c[-1][2] + b[2])
            moved.append(c)
        out = [moved[k][::-1] if self.flips[k] else moved[k] for k in self.order]
        for i, j in enumerate(self.junk):
            out.insert(i * 3 % (len(out) + 1), list(j))
        return out

    def _with_tiny(self, made: list[list[Point3]]) -> list[list[Point3]]:
        assert self.tiny is not None
        k, (dx, dy, dz) = self.tiny
        j = self.chains[0].joins()[k]
        moved = (j[0] + dx, j[1] + dy, j[2] + dz)
        out: list[list[Point3]] = []
        for c in made:
            # the curve leaving the join starts at the tiny curve's end
            out.append([moved] + c[1:] if c[0] == j else c)
        return out + [[j, moved]]

    @property
    def amplitude(self) -> float:
        """How far a point given may lie from the chain's own."""
        noise = max((math.dist(n, (0.0, 0.0, 0.0)) for pair in self.noise for n in pair), default=0.0)
        return noise + (math.dist(self.tiny[1], (0.0, 0.0, 0.0)) if self.tiny is not None else 0.0)


#: Joins this far apart (mm) are distinct ones, whatever the noise.
_APART = 3 * JOIN_TOLERANCE


@st.composite
def chains(draw: st.DrawFn, closed: bool | None = None, at: Point3 = (0.0, 0.0, 0.0)) -> Chain:
    """A random walk, planar or not, its steps from a twentieth of a
    millimetre to half a metre, cut into curves at random."""
    is_closed = draw(st.booleans()) if closed is None else closed
    n = draw(st.integers(3 if is_closed else 2, 14))
    flat = draw(st.booleans())
    pts: list[Point3] = [at]
    for _ in range(n - 1):
        step = draw(st.one_of(sizes(0.05, 500), floats(0.05, 5)))
        a, b = draw(floats(0, 2 * math.pi)), 0.0 if flat else draw(floats(-1.4, 1.4))
        p = pts[-1]
        pts.append((p[0] + step * math.cos(a) * math.cos(b), p[1] + step * math.sin(a) * math.cos(b),
                    p[2] + step * math.sin(b)))
    if is_closed:
        cuts = sorted(set(draw(st.lists(st.integers(0, n - 1), min_size=1, max_size=n))))
    else:
        cuts = sorted(set(draw(st.lists(st.integers(1, n - 2), max_size=n - 2)))) if n > 2 else []
    made = Chain(tuple(pts), is_closed, tuple(cuts))
    joins = made.joins()
    # (joins must be told apart, and a closed chain must not be its own neighbour's join)
    assume(all(math.dist(p, q) > _APART for i, p in enumerate(joins) for q in joins[i + 1:]))
    assume(all(len(c) >= 2 and math.dist(c[0], c[-1]) + math.dist(c[0], c[1]) > _APART for c in made.curves()))
    return made


def _noise(draw: st.DrawFn, n: int, most: float = 0.0045) -> tuple[tuple[Point3, Point3], ...]:
    amp = min(most, draw(st.sampled_from([0.0, 0.0, 1e-9, 0.001, 0.0045])))
    vec = st.tuples(floats(-1, 1), floats(-1, 1), floats(-1, 1)).map(
        lambda v: (0.0, 0.0, 0.0) if math.hypot(*v) == 0 else
        (v[0] * amp / math.hypot(*v), v[1] * amp / math.hypot(*v), v[2] * amp / math.hypot(*v)))
    return tuple(draw(st.lists(st.tuples(vec, vec), min_size=n, max_size=n)))


@st.composite
def chain_cases(draw: st.DrawFn) -> ChainCase:
    """One chain, now and then several apart or one with a branch."""
    kind = draw(st.sampled_from(["one", "one", "one", "several", "branch", "tiny", "doubled"]))
    found: list[Chain] = [draw(chains())]
    tiny: tuple[int, Point3] | None = None
    if kind == "tiny":
        joins = found[0].joins()
        inner = list(range(len(joins))) if found[0].closed else list(range(1, len(joins) - 1))
        if inner:
            length = draw(st.one_of(st.just(0.004), floats(1e-6, 0.6 * JOIN_TOLERANCE)))
            tiny = (draw(st.sampled_from(inner)), (length, 0.0, 0.0))
    if kind == "several":
        for k in range(draw(st.integers(1, 3))):
            found.append(draw(chains(at=(5000.0 * (k + 1), 0.0, 0.0))))
    branch = None
    if kind == "branch":
        joins = found[0].joins()
        inner = list(range(len(joins))) if found[0].closed else list(range(1, len(joins) - 1))
        if inner:
            branch = draw(st.sampled_from(inner))
    doubled = kind == "doubled"
    n = sum(len(c.curves()) for c in found) + (1 if branch is not None else 0) + (1 if tiny is not None else 0) \
        + (len(found[0].curves()) if doubled else 0)
    junk_point = st.tuples(floats(-100, 100), floats(-100, 100), floats(-100, 100))
    junk = tuple(draw(st.lists(st.one_of(junk_point.map(lambda p: (p,)), junk_point.map(lambda p: (p, p, p))),
                               max_size=2)))
    # (with a tiny curve, its neighbours' ends as Fusion gives them, on its own a rounding apart;
    # its own ends are not moved: it is no longer than the noise would make it)
    noise = _noise(draw, n, 1e-9 if tiny is not None else 0.0045)
    if tiny is not None:
        noise = noise[:-1] + (((0.0, 0.0, 0.0), (0.0, 0.0, 0.0)),)
    return ChainCase(tuple(found), tuple(draw(st.permutations(range(n)))),
                     tuple(draw(st.lists(st.booleans(), min_size=n, max_size=n))), noise, junk, branch, tiny, doubled)


def chain_problems(case: ChainCase) -> list[str]:
    """What `chain()` gets wrong about the case's curves."""
    curves = case.curves()
    several = len(case.chains) > 1
    try:
        points, closed = chain(curves)
    except ChainError as e:
        message = str(e)
        if several and f"{len(case.chains)} separate chains" in message:
            return []
        if case.branch is not None and "3 curves meet" in message:
            return []
        if case.doubled and ("close around nothing" in message or "curves meet" in message):
            return []
        return [f"refused one chain: {message}"]
    if several:
        return [f"joined {len(case.chains)} separate chains into one"]
    if case.branch is not None:
        return ["joined a branching chain"]
    ch = case.chains[0]
    if case.doubled:
        # the same curves twice close on themselves: around nothing, or with points out and back
        return [] if closed and len(points) >= 3 and len(ch.curves()) == 1 else \
            [f"took {len(ch.curves())} curves drawn twice as {len(points)} points, {'closed' if closed else 'open'}"]
    if closed != ch.closed:
        return [f"{'closed' if closed else 'open'} for an {'closed' if ch.closed else 'open'} chain"]
    if len(points) != len(ch.points):
        return [f"{len(points)} points for a chain of {len(ch.points)}"]
    slack = 2 * case.amplitude + 1e-12
    if not any(all(math.dist(p, q) <= slack for p, q in zip(points, run)) for run in _runs(ch)):
        return ["the points are not the chain's, from one of its ends or joins"]
    return []


def _runs(ch: Chain) -> list[list[Point3]]:
    """The chain's points as `chain()` may give them: from either end, a
    closed one from any join either way."""
    pts = list(ch.points)
    if not ch.closed:
        return [pts, pts[::-1]]
    out: list[list[Point3]] = []
    for c in ch.cuts:
        run = pts[c:] + pts[:c]
        out += [run, [run[0]] + run[1:][::-1]]
    return out


# -- masters ------------------------------------------------------------------------------------------

Kind = Literal["planes", "contours", "boxes", "parameters"]


@dataclass(frozen=True)
class Item:
    """One thing the writer reads from Fusion: a plane (`values`: origin,
    normal), a sketch (`sketch`, and `values`: the plane's origin and
    normal), a body (`values`: min, max; `cuboid`), a user parameter
    (`values`: (value,); `unit`, `expression`), or a problem with an item
    (`problem`: the message)."""
    kind: Kind
    path: str
    name: str
    where: str
    values: tuple[Point3, ...] = ()
    sketch: ChainCase | None = None
    cuboid: bool = True
    unit: str = "mm"
    expression: str = ""
    problem: str | None = None


@dataclass(frozen=True)
class MasterCase:
    items: tuple[Item, ...]
    source: str
    #: The order the items are given in the second time.
    order: tuple[int, ...]


_NAMES = ["Bodenniveau", "Boden vorne", "Wand FS", "Dach geneigt", "oben", "Kueche", "Küche", "Bett", "Sitz",
          "Bodenumriss", "Bodenprofil", "Kante", "Lattenabstand", "Neigung", "a.b", 'Zitat "x"', "back\\slash",
          "__Hilfe", "__", "Fenster", "Radkasten FS", "Boden"]


def _names() -> st.SearchStrategy[str]:
    text = st.text(st.characters(blacklist_categories=("Cs",)), min_size=1, max_size=10)
    return st.one_of(st.sampled_from(_NAMES), st.sampled_from(_NAMES), text)


def _paths() -> st.SearchStrategy[str]:
    return st.sampled_from(["", "", "", "Bett", "Moebel", "Moebel.Kueche", "Sitzbank", "Moebel.Sitzbank"])


def _point() -> st.SearchStrategy[Point3]:
    c = st.one_of(sizes(-6000, 6000), floats(-6000, 6000), st.just(0.0), st.just(-0.0))
    return st.tuples(c, c, c)


def _normal() -> st.SearchStrategy[Point3]:
    axis = st.sampled_from([(1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0), (0.0, 0.0, -1.0), (0.0, -2.0, 0.0),
                            (1e-12, 0.0, 1.0)])
    tilted = st.tuples(floats(-1, 1), floats(-1, 1), floats(-1, 1)).filter(lambda v: math.hypot(*v) > 0.1)
    return st.one_of(axis, axis, tilted)


@st.composite
def items(draw: st.DrawFn) -> Item:
    kind: Kind = draw(st.sampled_from(["planes", "contours", "boxes", "parameters"]))
    path = "" if kind == "parameters" else draw(_paths())
    name, where = draw(_names()), draw(st.sampled_from(["root", "Bett:1", "Moebel:1+Kueche:1"]))
    if draw(st.integers(0, 9)) == 0:
        return Item(kind, path, name, where, problem=draw(st.sampled_from(["a surface body, not a solid",
                                                                          "could not sample SketchArc"])))
    if kind == "planes":
        return Item(kind, path, name, where, (draw(_point()), draw(_normal())))
    if kind == "contours":
        sketch = draw(chain_cases())
        return Item(kind, path, name, where, (draw(_point()), draw(_normal())), sketch=sketch)
    if kind == "boxes":
        lo, size = draw(_point()), draw(st.tuples(sizes(0, 3000), sizes(0, 3000), sizes(0, 3000)))
        return Item(kind, path, name, where, (lo, (lo[0] + size[0], lo[1] + size[1], lo[2] + size[2])),
                    cuboid=draw(st.booleans()))
    unit = draw(st.sampled_from(["mm", "deg", ""]))
    return Item(kind, path, name, where, ((draw(st.one_of(sizes(-5000, 5000), floats(-1e6, 1e6))), 0.0, 0.0),),
                unit=unit, expression=draw(st.sampled_from(["40 mm", "Bodenaufbau + 400 mm", "10 deg", ""])))


@st.composite
def master_cases(draw: st.DrawFn) -> MasterCase:
    found = list(draw(st.lists(items(), max_size=12)))
    # the same name twice, now and then
    if found and draw(st.booleans()):
        found.append(dataclasses.replace(draw(st.sampled_from(found)), where="twin:1"))
    return MasterCase(tuple(found), draw(_names()), tuple(draw(st.permutations(range(len(found))))))


def collect(items_given: list[Item]) -> Collector:
    c = Collector()
    for it in items_given:
        if it.problem is not None:
            c.problem(it.kind, it.path, it.name, it.where, it.problem)
        elif it.kind == "planes":
            c.plane(it.path, it.name, it.where, it.values[0], it.values[1])
        elif it.kind == "contours":
            assert it.sketch is not None
            c.contour(it.path, it.name, it.where, it.sketch.curves(), it.values[0], it.values[1])
        elif it.kind == "boxes":
            c.box(it.path, it.name, it.where, it.values[0], it.values[1], it.cuboid)
        else:
            c.parameter(it.name, it.values[0][0], it.unit, it.expression)
    return c


def _rounded(p: tuple[float, ...]) -> list[float]:
    return [round(float(c), DECIMALS) + 0.0 for c in p]


def _shuffled(value: Any, rng: random.Random) -> Any:
    """The same JSON value with every object's keys in another order."""
    if isinstance(value, dict):
        keys = list(value)
        rng.shuffle(keys)
        return {k: _shuffled(value[k], rng) for k in keys}
    if isinstance(value, list):
        return [_shuffled(v, rng) for v in value]
    return value


def snapshot_problems(case: MasterCase) -> list[str]:
    """What the writer and the reader get wrong about the case's master."""
    problems: list[str] = []
    given = list(case.items)
    snap = collect(given).build(case.source)
    again = collect([given[k] for k in case.order]).build(case.source)
    if again != snap:
        diff = sorted(k for k in snap if snap[k] != again[k])  # pyright: ignore[reportUnknownVariableType]
        problems.append(f"the snapshot depends on the order the items come in: {diff}")
    text = dumps(snap)
    if json.loads(text) != snap:
        problems.append("dumps does not read back as the snapshot")
    if dumps(copy.deepcopy(snap)) != text:
        problems.append("dumps gives another text for an equal snapshot")
    rng = random.Random(len(text))
    if content_hash(_shuffled(snap, rng)) != snap["hash"]:
        problems.append("content_hash depends on the order of keys")
    renamed = dict(snap, source=snap["source"] + " (copy)")
    if content_hash(renamed) != snap["hash"]:  # pyright: ignore[reportArgumentType]
        problems.append("content_hash covers the source's name")
    if content_hash(json.loads(text)) != snap["hash"]:
        problems.append("the file's content hashes otherwise than the snapshot")
    problems += _read_back(case, snap, text)
    return problems


def _expected(case: MasterCase) -> dict[Kind, dict[str, list[Item]]]:
    """The items by kind and snapshot name, without those left out."""
    out: dict[Kind, dict[str, list[Item]]] = {"planes": {}, "contours": {}, "boxes": {}, "parameters": {}}
    for it in case.items:
        if it.name.startswith(SKIP_PREFIX):
            continue
        out[it.kind].setdefault(path_name(it.path, it.name), []).append(it)
    return out


def _read_back(case: MasterCase, snap: SnapshotDict, text: str) -> list[str]:
    problems: list[str] = []
    with tempfile.TemporaryDirectory() as folder:
        path = Path(folder) / "snapshot.json"
        path.write_text(text + "\n", encoding="utf-8")
        van = master(path)
    if van.hash != snap["hash"] or van.source != case.source:
        problems.append("master() reads another hash or source")
    look = {"planes": van.plane, "contours": van.contour, "boxes": van.box, "parameters": van.param}
    for kind, by_name in _expected(case).items():
        if van.names(kind) != sorted(n for n, its in by_name.items() if len(its) == 1 and its[0].problem is None
                                     and not (kind == "contours" and _refused(its[0]))):
            problems.append(f"master() lists other {kind}: {van.names(kind)}")
        for name, its in by_name.items():
            try:
                got = look[kind](name)
            except LangError as e:
                if len(its) > 1 and "named twice" in e.message:
                    continue
                if its[0].problem is not None and its[0].problem in e.message:
                    continue
                if kind == "contours" and _refused(its[0]):
                    continue
                problems.append(f"master() refuses {kind[:-1]} {name!r}: {e.message}")
                continue
            if len(its) > 1 or its[0].problem is not None:
                problems.append(f"master() reads {kind[:-1]} {name!r}, which the snapshot cannot take")
                continue
            problems += _compare(kind, name, its[0], got)
    if "Nichts da" not in van.names("planes"):
        try:
            van.plane("Nichts da")
            problems.append("master() reads a plane that is not there")
        except LangError:
            pass
    return problems


def _refused(it: Item) -> bool:
    assert it.sketch is not None
    try:
        chain(it.sketch.curves())
        return False
    except ChainError:
        return True


def _compare(kind: Kind, name: str, it: Item, got: Any) -> list[str]:
    """The item as `master()` reads it against what was given, rounded as
    the writer rounds it."""
    def unit(v: Point3) -> list[float]:
        n = math.sqrt(sum(c * c for c in v))
        return [c / n for c in v]

    def near(a: tuple[float, ...] | list[float], b: tuple[float, ...] | list[float], tol: float) -> bool:
        return len(a) == len(b) and all(abs(x - y) <= tol for x, y in zip(a, b))
    half = 0.5 * 10 ** -DECIMALS + 1e-9
    if kind == "planes":
        if not (near(got.origin, it.values[0], half) and near(got.normal, unit(it.values[1]), 1e-9)):
            return [f"plane {name!r} reads as {got.origin} {got.normal}"]
        axis = got.axis
        aligned = [i for i, c in enumerate(unit(it.values[1])) if abs(abs(c) - 1) < 1e-6]
        if (axis is None) != (not aligned):
            return [f"plane {name!r} is {'tilted' if axis is None else 'on ' + axis}, its normal {it.values[1]}"]
        return []
    if kind == "contours":
        assert it.sketch is not None
        points, closed = chain(it.sketch.curves())
        if got.closed != closed or [list(p) for p in got.points] != [_rounded(p) for p in points]:
            return [f"contour {name!r} reads otherwise than its chain"]
        if not (near(got.origin, it.values[0], half) and near(got.normal, unit(it.values[1]), 1e-9)):
            return [f"contour {name!r} has another plane"]
        return []
    if kind == "boxes":
        lo = [got.lo[a] for a in ("x", "y", "z")]
        hi = [got.hi[a] for a in ("x", "y", "z")]
        if not (near(lo, it.values[0], half) and near(hi, it.values[1], half)):
            return [f"box {name!r} reads as {lo} to {hi}"]
        return []
    if not math.isclose(got, it.values[0][0], abs_tol=half):
        return [f"parameter {name!r} reads as {got}, given {it.values[0][0]}"]
    return []


__all__ = ["ChainCase", "MasterCase", "chain_cases", "chain_problems", "master_cases", "snapshot_problems"]
