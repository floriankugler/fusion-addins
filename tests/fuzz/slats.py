"""Random slats placed as build files place them, for fuzzing `Slat`'s
placement (`on()` a wide face, `edge_on()` a narrow face, `center()` the
middle, `between()` the ends) as `placement.py` fuzzes boards'. A case is a
module or a cabinet, perhaps with a side board on its left, and slats
written in its own terms: each with a section (its sizes in either order)
and two of the three modifiers, by a box side, the side board's inner face,
or a position with `toward=`, and none, one or two ends (box sides or
positions, now and then one off the length's axis).

`run_case` builds it two ways that must give the same result, measured in
the module's own terms (inward from its front, left and bottom sides): as
written in the default world frame, and in another world frame at another
place, a cabinet facing another side of its box, the modifiers called in
another order, the section's sizes and the ends given the other way round.
A refusal must be one both ways. And it checks what placement promises,
worked out again from the case: the wide face on what `on()` names, the
narrow face on what `edge_on()` names, the middle on what `center()` names
(the width when `on()` is given, else the thickness), the length between
its ends, from a single end to the far side of the room, the whole room
without any; refused where two modifiers place one axis, where an end is
off the length's axis, where a single end lies at the room's middle, or
where the length comes out under 0.01 mm, and only there. The layout plans,
draws and meshes.
"""
from __future__ import annotations

import random
import traceback
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

from hypothesis import strategies as st

from boards import _pipeline_problems  # pyright: ignore[reportPrivateUsage]
from fuzzing import floats, fresh, sizes
from lang import (Box, Frame, LangError, Pos, board, cabinet, module, no_interference, set_frame, sheet_material, slat,
                  slat_material, uncheck)
from lang.core.geometry import NARROWEST
from lang.core.scope import Scope
from placement import ALIASES, FRONTS, HIGH, LOW, MEASURE, WORLD_FRAMES, _Local  # pyright: ignore[reportPrivateUsage]

OAK = slat_material("oak")
PLY = sheet_material("birch", t=15)
SIDE_T = 15.0

RefKind = Literal["side", "pos", "face"]
Modifier = Literal["on", "edge_on", "center"]


@dataclass(frozen=True)
class Ref:
    """A plane in the module's own terms: a box side by name, the side
    board's inner face, or a position `value` mm along `measure` (0 depth
    from the front, 1 width from the left, 2 height from the bottom) with
    the size going toward `toward`, a side's name."""
    kind: RefKind
    name: str = ""
    measure: int = 0
    value: float = 0.0
    toward: str = ""


@dataclass(frozen=True)
class SlatSpec:
    section: tuple[float, float]
    mods: tuple[tuple[Modifier, Ref], tuple[Modifier, Ref]]
    #: Each end a box side by name, or a fraction along the length's measure
    #: (by the room's size), or a side off the length's measure: ("off", name).
    ends: tuple[tuple[str, Any], ...]


@dataclass(frozen=True)
class SlatCase:
    kind: Literal["module", "cabinet"]
    size: tuple[float, float, float]           # width, depth, height
    side: bool
    slats: tuple[SlatSpec, ...]
    frame: int = 0
    origin: tuple[float, float, float] = (0.0, 0.0, 0.0)
    front: int = 0
    seed: int = 0


@st.composite
def _ref(draw: st.DrawFn, size: tuple[float, float, float], side: bool, plane: bool) -> Ref:
    """A plane for on() or edge_on() (`plane`), or a position for center()."""
    extent = (size[1], size[0], size[2])
    k = draw(st.integers(0, 2))
    value = draw(st.one_of(floats(0, extent[k]), sizes(0, extent[k]), st.just(extent[k] / 2)))
    if not plane:
        return Ref("pos", measure=k, value=value)
    kinds: list[RefKind] = ["side", "side", "pos"]
    kind = draw(st.sampled_from(kinds + ["face"] if side else kinds))
    if kind == "side":
        return Ref("side", name=draw(st.sampled_from(LOW + HIGH)))
    if kind == "face":
        return Ref("face")
    return Ref("pos", measure=k, value=value, toward=draw(st.sampled_from([LOW[k], HIGH[k]])))


def _measure(r: Ref) -> int:
    return MEASURE[r.name] if r.kind == "side" else 1 if r.kind == "face" else r.measure


@st.composite
def _slat(draw: st.DrawFn, size: tuple[float, float, float], side: bool) -> SlatSpec:
    section = (draw(sizes(0.5, 120)), draw(sizes(0.5, 120)))
    pair = draw(st.sampled_from([("on", "edge_on"), ("on", "center"), ("edge_on", "center")]))
    first = draw(_ref(size, side, pair[0] != "center"))
    second = draw(_ref(size, side, pair[1] != "center"))
    for _ in range(draw(st.integers(0, 3))):        # mostly on another axis than the first, now and then the same
        if _measure(second) != _measure(first):
            break
        second = draw(_ref(size, side, pair[1] != "center"))
    mods = ((pair[0], first), (pair[1], second))
    end = st.one_of(st.tuples(st.just("side"), st.sampled_from(["low", "high"])),
                    st.tuples(st.just("pos"), st.one_of(floats(-0.2, 1.2), st.sampled_from([0.0, 0.25, 0.5, 1.0]))),
                    st.tuples(st.just("off"), st.sampled_from(LOW + HIGH)))
    ends = tuple(draw(st.lists(end, max_size=2)))
    return SlatSpec(section, mods, ends)  # type: ignore[arg-type]


@st.composite
def slat_cases(draw: st.DrawFn) -> SlatCase:
    size = (draw(sizes(100, 2400)), draw(sizes(100, 1200)), draw(sizes(100, 2000)))
    side = draw(st.booleans())
    far = sizes(-5000, 5000)
    return SlatCase(draw(st.sampled_from(["module", "cabinet"])), size, side,
                    tuple(draw(st.lists(_slat(size, side), min_size=1, max_size=4))),
                    draw(st.integers(0, len(WORLD_FRAMES) - 1)), draw(st.tuples(far, far, far)),
                    draw(st.integers(0, 3)), draw(st.integers(0, 2**16)))


# -- what the case means ------------------------------------------------------------------------------

def _extent(case: SlatCase) -> tuple[float, float, float]:
    """The module's sizes along its measures: depth, width, height."""
    return (case.size[1], case.size[0], case.size[2])


def _plane(case: SlatCase, r: Ref) -> tuple[int, float, int]:
    """A plane as (measure, value, the way the size goes: 1 or -1)."""
    ext = _extent(case)
    if r.kind == "side":
        k = MEASURE[r.name]
        return (k, 0.0, 1) if r.name in LOW else (k, ext[k], -1)
    if r.kind == "face":
        return (1, SIDE_T, 1)
    return (r.measure, r.value, 1 if r.toward in HIGH else -1)


def expected(case: SlatCase, spec: SlatSpec) -> tuple[str, list[tuple[float, float]] | None]:
    """The slat's ranges along the three measures, or why it is refused."""
    ext = _extent(case)
    t, w = min(spec.section), max(spec.section)
    given = dict(spec.mods)
    ranges: dict[int, tuple[float, float]] = {}

    def lay(k: int, value: float, way: int, size: float) -> None:
        ranges[k] = (value, value + size) if way > 0 else (value - size, value)

    measures: list[int] = []
    if "on" in given:
        k, v, way = _plane(case, given["on"])
        lay(k, v, way, t)
        measures.append(k)
        if "edge_on" in given:
            k2, v2, way2 = _plane(case, given["edge_on"])
            measures.append(k2)
            if k2 != k:
                lay(k2, v2, way2, w)
        else:
            c = given["center"]
            measures.append(c.measure)
            ranges.setdefault(c.measure, (c.value - w / 2, c.value + w / 2))
    else:
        k, v, way = _plane(case, given["edge_on"])
        lay(k, v, way, w)
        c = given["center"]
        measures.append(k)
        measures.append(c.measure)
        ranges.setdefault(c.measure, (c.value - t / 2, c.value + t / 2))
    if measures[0] == measures[1]:
        return "two on one axis", None
    length = next(k for k in range(3) if k not in measures)
    values: list[float] = []
    for kind, what in spec.ends:
        if kind == "off":
            if MEASURE[what] != length:
                return "an end off the length's axis", None
            values.append(0.0 if what in LOW else ext[length])
        elif kind == "side":
            values.append(0.0 if what == "low" else ext[length])
        else:
            values.append(what * ext[length])
    if not values:
        a, b = 0.0, ext[length]
    elif len(values) == 1:
        v = values[0]
        mid = ext[length] / 2
        if abs(v - mid) < 1e-9:
            return "a single end at the middle", None
        a, b = (v, ext[length]) if v < mid else (0.0, v)
    else:
        a, b = sorted(values)
    if b - a < NARROWEST:
        return "no length", None
    ranges[length] = (a, b)
    return "accepted", [ranges[k] for k in range(3)]


# -- building --------------------------------------------------------------------------------------

def _world_box(case: SlatCase, origin: tuple[float, float, float], front: int) -> Box:
    w, d, h = case.size
    if case.kind == "module" or FRONTS[front] in ("front", "back"):
        return Box.from_size(width=w, depth=d, height=h, origin=origin)
    return Box.from_size(width=d, depth=w, height=h, origin=origin)


def _position(m: Scope, loc: _Local, k: int, value: float) -> Pos:
    s = loc.sides[k]
    return Pos(s.axis, s.value + s.inward.sign * value)


def build(case: SlatCase, other: bool) -> tuple[Scope, list[tuple[str, Any]]]:
    """The case built as written (`other` False) or the other way; each
    slat's result: its ranges in the module's own terms, or the refusal."""
    rng = random.Random(case.seed)
    frame = case.frame if other else 0
    front, left, top = WORLD_FRAMES[frame]
    set_frame(Frame(front=front, left=left, top=top, aliases=ALIASES))
    origin = case.origin if other else (0.0, 0.0, 0.0)
    facing = case.front if other else 0
    box = _world_box(case, origin, facing)
    m = module("m", box) if case.kind == "module" else cabinet("m", box, front=box.side(FRONTS[facing]))
    results: list[tuple[str, Any]] = []
    with m:
        uncheck(no_interference)         # (slats placed at random overlap; their placement is what is checked)
        side = board("side", PLY).on(m.left) if case.side else None
        loc = _Local(m)
        ext = _extent(case)
        for i, spec in enumerate(case.slats):
            section = (spec.section[1], spec.section[0]) if other else spec.section
            s = slat(f"s{i}", OAK, section=section)
            mods = list(spec.mods)
            if other:
                rng.shuffle(mods)
            try:
                for mod, r in mods:
                    if mod == "center":
                        s.center(_position(m, loc, r.measure, r.value))
                        continue
                    if r.kind == "side":
                        ref, toward = m.side(r.name), None
                    elif r.kind == "face":
                        assert side is not None
                        ref, toward = side.inner, None
                    else:
                        ref, toward = _position(m, loc, r.measure, r.value), m.side(r.toward)
                    (s.on if mod == "on" else s.edge_on)(ref, toward=toward)
                ends: list[Any] = []
                length = expected_length(case, spec)
                for kind, what in spec.ends:
                    if kind == "off":
                        ends.append(m.side(what))
                    elif kind == "side":
                        ends.append(m.side(LOW[length] if what == "low" else HIGH[length]))
                    else:
                        ends.append(_position(m, loc, length, what * ext[length]))
                if ends:
                    s.between(*(ends[::-1] if other else ends))
                b = s.box()
                results.append(("accepted", [loc.span(loc.sides[k].axis, b.lo[loc.sides[k].axis],
                                                      b.hi[loc.sides[k].axis]) for k in range(3)]))
            except LangError as e:
                m.unregister(s)
                results.append(("refused", str(e)))
    return m, results


def expected_length(case: SlatCase, spec: SlatSpec) -> int:
    """The measure the slat's length runs along (any, where two modifiers
    share one)."""
    measures = [_measure(r) for _, r in spec.mods]
    return next(k for k in range(3) if k not in measures)


# -- checking -------------------------------------------------------------------------------------

def run_case(case: SlatCase) -> list[str]:
    try:
        with fresh():
            _, first = build(case, False)
            pipeline = _pipeline_problems()
        with fresh():
            _, second = build(case, True)
    except Exception as e:
        frame = next((fr for fr in reversed(traceback.extract_tb(e.__traceback__))
                      if "/lang/" in fr.filename), traceback.extract_tb(e.__traceback__)[-1])
        return [f"{type(e).__name__} at {Path(frame.filename).name}:{frame.lineno}: {e}"]
    problems = list(pipeline)
    for i, (spec, a, b) in enumerate(zip(case.slats, first, second)):
        why, ranges = expected(case, spec)
        if a[0] != b[0]:
            problems.append(f"s{i} is {a[0]} as written, {b[0]} the other way: {a[1] if a[0] == 'refused' else b[1]}")
            continue
        if (a[0] == "accepted") != (why == "accepted"):
            problems.append(f"s{i} is {a[0]}, but placement says {why}: {a[1]}")
            continue
        if a[0] != "accepted" or ranges is None:
            continue
        for k in range(3):
            for got, other in ((a[1][k], b[1][k]), (a[1][k], ranges[k])):
                if any(abs(x - y) > 1e-6 * max(1.0, abs(y)) for x, y in zip(got, other)):
                    problems.append(f"s{i} spans {got} along measure {k}, not {other}")
                    break
    return problems


def accepted_count(case: SlatCase) -> int:
    return sum(expected(case, s)[0] == "accepted" for s in case.slats)
