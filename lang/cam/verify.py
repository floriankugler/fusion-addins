"""The plan's own check, Fusion-free, as the nest's `verify` (`design/cam.md`,
Checked): what it finds is a problem in the plan file; the tests and fuzz
tests require it to find nothing.

- The setups are the nest's blanks, one each, with the blank's parts.
- Every operation of every part on a blank is in the plan or left out with
  a reason, not both: each hole, V-groove, chamfer, an operation's chamfer
  and each of its dog bones exactly once, a pocket or a cut (whose
  material the outline's contours take) at least once; every ring of the
  outline (`plan.contours`) exactly once, but in a release operation,
  which cuts again what a roughing one cut.
- Every cutter reaches the region it is given (`regions.unreached`): a
  pocket by its template's narrowest cutter, what it does not reach in a
  rest that a narrower template reaches or in a problem; a contour on its
  waste side; the dog bones excused.
- Every contour roughed is released and every one released roughed; the
  release operations' contours are the release order, in it, each part's
  inner contours before its outer one, the parts by their hold (smallest
  first) within a cutter's.
- A tabbed part's tabs are on its roughing and its release operation both,
  each on its outer contour; an operation's tabs lie on its contours.
- The operations are in order: by tool, widest first, within a tool by
  kind; then the V-bit's; then the release passes.
- An own blank has no outer contour and no release.
- Every feature but a V-groove lies on its blank.
"""
from __future__ import annotations

import math
from collections import Counter
from typing import Any

from shapely.geometry import LineString, Point, Polygon
from shapely.geometry import box as shapely_box
from shapely.geometry.base import BaseGeometry
from shapely.ops import unary_union

from ..core.layout_types import Layout, OpLayout, PartLayout
from ..nesting.nest_types import NestFile
from . import holding
from .plan import contours, setup_name
from .plan_types import CamFile, Feature, OperationOut, SetupOut
from .regions import CLEAN, Placed, polygons, unreached
from .rules import KIND_ORDER, RELIEF_TOL
from .tooling import Registry, Template, registry_of

_ON = 1e-6


def verify(plan: CamFile, nest: NestFile, layout: Layout, registry: Registry | None = None) -> list[str]:
    """What is wrong with a plan of a nest (see the module's doc)."""
    problems: list[str] = []
    registry = registry or registry_of(plan["settings"]["templates"])
    by_stem = {t.stem: t for ts in registry.by_kind.values() for t in ts}
    parts = {p["path"]: p for m in layout["modules"] for p in m["parts"]}
    blanks = [(m["material"], b) for m in nest["materials"] for s in m["sheets"] for b in s["blanks"]]
    if len(blanks) != len(plan["setups"]):
        problems.append(f"{len(plan['setups'])} setups for {len(blanks)} blanks")
    for (material, blank), setup in zip(blanks, plan["setups"]):
        name = setup_name(nest["name"], material, blank["name"])
        if setup["name"] != name:
            problems.append(f"a setup is named {setup['name']!r}, its blank {name!r}")
        if [p["path"] for p in setup["parts"]] != [p["path"] for p in blank["parts"]]:
            problems.append(f"{name}: its parts are not its blank's")
            continue
        placed = {p["path"]: Placed.of(parts[p["path"]], p["transform"], layout["frame"]) for p in blank["parts"]}
        problems += [f"{name}: {p}" for p in _setup(setup, placed, blank["rect"], by_stem)]
    return problems


def _setup(setup: SetupOut, placed: dict[str, Placed], rect: list[float], by_stem: dict[str, Template]) -> list[str]:
    problems: list[str] = []
    own = setup["stock"]["own_blank"]
    ops = setup["operations"]
    # -- every operation once, or left out
    found: dict[str, Counter[tuple[int, str]]] = {path: Counter() for path in placed}
    left: dict[str, Counter[tuple[int, str]]] = {path: Counter() for path in placed}
    for op in ops:
        if op["kind"] == "release":
            continue
        for f in op["features"]:
            if f["part"] not in found:
                problems.append(f"a feature of {f['part']}, which is not on the blank")
                continue
            for r in f["ops"]:
                found[f["part"]][(r["index"], r["aspect"])] += 1
    for lo in setup["left_out"]:
        if lo["part"] in left:
            left[lo["part"]][(lo["op"]["index"], lo["op"]["aspect"])] += 1
    for path, pp in placed.items():
        want = _expected(pp)
        for key, (least, most) in want.items():
            n, m = found[path][key], left[path][key]
            what = f"{path}: {_label(pp.part, key)}"
            if n and m:
                problems.append(f"{what} is planned and left out")
            elif m > 1:
                problems.append(f"{what} is left out {m} times")
            elif not n and not m:
                problems.append(f"{what} is neither planned nor left out")
            elif n and not (least <= n <= most):
                problems.append(f"{what} is planned {n} times")
        for key in set(found[path]) | set(left[path]):
            if key not in want:
                problems.append(f"{path}: {_label(pp.part, key)} is no operation of it")
    # -- the cutters reach their regions
    problems += _reach(setup, placed, by_stem)
    # -- roughing and release
    problems += _release(setup, own)
    # -- tabs
    problems += _tabs(setup)
    # -- the order
    problems += _order(ops)
    # -- own blanks, the blank
    if own and any(op["kind"] == "release" or any(f["what"] == "outer" for f in op["features"]) for op in ops):
        problems.append("an own blank's outline is planned")
    stock = shapely_box(-1e-6, -1e-6, rect[2] + 1e-6, rect[3] + 1e-6)
    for op in ops:
        for f in op["features"]:
            if f["what"] != "vgroove" and not all(stock.contains(Point(p)) for p in _points(f)):
                problems.append(f"a feature of {op['name']} for {f['part']} lies off the blank")
    return problems


def _expected(pp: Placed) -> dict[tuple[int, str], tuple[int, float]]:
    """Each aspect of the part's operations, with how often it is planned
    at least and at most."""
    out: dict[tuple[int, str], tuple[int, float]] = {}
    for k, op in enumerate(pp.part["ops"]):
        inner = op["op"] if op["kind"] == "edge" else op
        if inner["kind"] == "chamfer" or inner["kind"] == "vgroove":
            out[(k, "op")] = (1, 1)
            continue
        out[(k, "op")] = (1, 1 if inner["kind"] == "hole" else math.inf)
        if inner["chamfer"] > 0:
            out[(k, "chamfer")] = (1, 1)
        if inner["kind"] != "hole":
            for j in range(len(inner["dogbones"])):
                out[(k, f"relief {j}")] = (1, 1)
    rings, _unclaimed = contours(pp, [])
    for ring in rings:
        out[(-1, f"ring {ring.index}")] = (1, 1)
    return out


def _label(part: PartLayout, key: tuple[int, str]) -> str:
    k, aspect = key
    if k < 0:
        return f"the outline's {aspect}"
    if k >= len(part["ops"]):
        return f"operation {k} ({aspect})"
    op: OpLayout = part["ops"][k]
    name = op["op"]["name"] if op["kind"] == "edge" else None if op["kind"] == "chamfer" else op["name"]
    return f"{op['kind']} {name or k}" + ("" if aspect == "op" else f" ({aspect})")


def _discs(pp: Placed) -> BaseGeometry | None:
    discs = [Point(pp.point(*bone["center"])).buffer(bone["d"] / 2 + 2 * CLEAN, quad_segs=90)
             for op in pp.part["ops"] if op["kind"] == "cut" or op["kind"] == "pocket" for bone in op["dogbones"]]
    return unary_union(discs) if discs else None


def _region(rings: list[list[list[float]]]) -> BaseGeometry:
    return unary_union(polygons(rings))


def _reach(setup: SetupOut, placed: dict[str, Placed], by_stem: dict[str, Template]) -> list[str]:
    problems: list[str] = []
    reported = " ".join(setup["problems"])
    discs = {path: _discs(pp) for path, pp in placed.items()}
    rests: dict[tuple[str, str], list[tuple[Template, BaseGeometry]]] = {}
    mains: list[tuple[Template, Feature, OperationOut]] = []
    for op in setup["operations"]:
        t = by_stem.get(op["template"])
        if t is None:
            problems.append(f"{op['name']}: no template {op['template']}")
            continue
        if t.diameter != op["tool"]["diameter"]:
            problems.append(f"{op['name']}: its tool is not its template's cutter")
        for f in op["features"]:
            if f["what"] == "rest":
                rests.setdefault((f["part"], _key(f)), []).append((t, _region(f["rings"])))
            elif f["what"] != "hole" and f["what"] != "dogbone" and f["what"] != "chamfer" and \
                    f["what"] != "vgroove" and op["kind"] != "release":
                mains.append((t, f, op))
    for t, f, op in mains:
        excused = discs.get(f["part"])
        if f["what"] == "pocket":
            region = _region(f["rings"])
            left = unreached(region, t.narrowest / 2, excused)
            covered = unary_union([g for _t, g in rests.get((f["part"], _key(f)), [])]) if left else None
            for piece in left:
                if covered is not None and piece.difference(covered.buffer(CLEAN)).area < 1e-4:
                    continue
                if "no pocket cutter reaches" in reported:
                    continue
                problems.append(f"{op['name']}: its cutter does not reach {piece.area:.2f} mm² of a pocket of "
                                f"{f['part']}")
            for rt, rest in rests.get((f["part"], _key(f)), []):
                if rt.narrowest >= t.narrowest:
                    problems.append(f"a rest of {f['part']} takes a cutter no narrower than its pocket's")
                miss = unary_union(unreached(region, rt.narrowest / 2, excused)).intersection(rest)
                if miss.area > 1e-4:
                    problems.append(f"a rest of {f['part']} is not reached by its cutter ({miss.area:.2f} mm²)")
        elif f["what"] == "outer" or f["what"] == "inner":
            ring = Polygon(f["ring"])
            if f["what"] == "outer":
                x0, y0, x1, y1 = ring.bounds
                waste: BaseGeometry = shapely_box(x0 - 30, y0 - 30, x1 + 30, y1 + 30).difference(ring)
            else:
                waste = ring
            left = unreached(waste, t.narrowest / 2, excused, clearance=0.0)
            if left and "no contour cutter reaches" not in reported:
                problems.append(f"{op['name']}: its cutter does not reach all of a contour of {f['part']} "
                                f"({sum(p.area for p in left):.2f} mm²)")
    # dog bones: each cut by a cutter that fits it
    for op in setup["operations"]:
        for f in op["features"]:
            if f["what"] == "dogbone" and op["kind"] == "dogbone" and op["tool"]["diameter"] > f["d"] - RELIEF_TOL + 1e-9:
                problems.append(f"{op['name']}: a dog bone {f['d']:g} across is no wider than its cutter")
    return problems


def _key(f: Feature) -> str:
    return ",".join(f"{r['index']}:{r['aspect']}" for r in f["ops"] if r["aspect"] == "op" or r["aspect"].startswith("ring"))


def _release(setup: SetupOut, own: bool) -> list[str]:
    problems: list[str] = []
    rough = Counter((f["part"], _ring(f)) for op in setup["operations"] if op["kind"] == "contour"
                    for f in op["features"])
    freed = [(f["part"], _ring(f), op["tool"]["diameter"], f["what"]) for op in setup["operations"]
             if op["kind"] == "release" for f in op["features"]]
    if any(n > 1 for n in rough.values()):
        problems.append("a contour is roughed twice")
    if Counter((p, r) for p, r, _t, _w in freed) != rough:
        problems.append("the contours roughed are not the contours released")
    order = [(r["part"], r["ring"], r["tool"], r["what"]) for r in setup["release_order"]]
    if order != freed:
        problems.append("the release operations do not cut the release order")
    holds = {p["path"]: p["hold"] for p in setup["parts"]}
    for tool in sorted({t for _p, _r, t, _w in freed}):
        seen = [p for p, _r, t, _w in freed if t == tool]
        values = [holds[p] for p in dict.fromkeys(seen)]
        if any(b < a - holding.SAME_HOLD - 1e-9 for a, b in zip(values, values[1:])):
            problems.append(f"the {tool:g} mm release does not go by the parts' hold")
    for path in {p for p, _r, _t, _w in freed}:
        mine = [(k, w) for k, (p, _r, _t, w) in enumerate(freed) if p == path]
        outer = [k for k, w in mine if w == "outer"]
        if outer and any(w == "inner" and k > outer[0] for k, w in mine):
            problems.append(f"an inner contour of {path} is released after its outer one")
    if own and freed:
        problems.append("an own blank is released")
    return problems


def _ring(f: Feature) -> int:
    for r in f["ops"]:
        if r["index"] == -1 and r["aspect"].startswith("ring "):
            return int(r["aspect"].split()[1])
    return -1


def _tabs(setup: SetupOut) -> list[str]:
    problems: list[str] = []
    for op in setup["operations"]:
        tabs = op["params"]["tabs"]
        if tabs is None:
            continue
        lines = [LineString(f["ring"] + f["ring"][:1]) for f in op["features"]
                 if f["what"] == "outer" or f["what"] == "inner"]
        for p in tabs["positions"]:
            if not any(line.distance(Point(p)) < _ON for line in lines):
                problems.append(f"{op['name']}: a tab at ({p[0]:.1f}, {p[1]:.1f}) lies on none of its contours")
    for part in setup["parts"]:
        if not part["tabs"]:
            continue
        for kind in ("contour", "release"):
            ops = [op for op in setup["operations"] if op["kind"] == kind and any(
                f["part"] == part["path"] and f["what"] == "outer" for f in op["features"])]
            if len(ops) != 1 or ops[0]["params"]["tabs"] is None:
                problems.append(f"{part['path']}: its tabs are not on its {kind} operation")
                continue
            ring = next(f["ring"] for f in ops[0]["features"] if f["part"] == part["path"] and f["what"] == "outer")
            line = LineString(ring + ring[:1])
            on = [p for p in ops[0]["params"]["tabs"]["positions"] if line.distance(Point(p)) < _ON]
            if len(on) != part["tabs"]:
                problems.append(f"{part['path']}: {len(on)} tabs on its {kind} operation, {part['tabs']} planned")
    return problems


def _order(ops: list[OperationOut]) -> list[str]:
    def key(op: OperationOut) -> tuple[Any, ...]:
        if op["kind"] == "release":
            return (2, -op["tool"]["diameter"])
        if op["kind"] in ("chamfer", "groove"):
            return (1, 0 if op["kind"] == "chamfer" else 1)
        return (0, -round(op["tool"]["diameter"], 4), KIND_ORDER[op["kind"]])
    keys = [key(op) for op in ops]
    return [f"{b[1]['name']} comes after {a[1]['name']}" for a, b in zip(zip(keys, ops), zip(keys[1:], ops[1:]))
            if b[0] < a[0]]


def _points(f: Feature) -> list[list[float]]:
    if f["what"] == "outer" or f["what"] == "inner":
        return f["ring"]
    if f["what"] == "pocket" or f["what"] == "rest":
        return [p for ring in f["rings"] for p in ring]
    if f["what"] == "chamfer":
        return [p for path in f["paths"] for p in path["points"]]
    if f["what"] == "vgroove":
        return [f["start"], f["end"]]
    if f["what"] == "hole" or f["what"] == "dogbone":
        return [f["center"]]
    return []
