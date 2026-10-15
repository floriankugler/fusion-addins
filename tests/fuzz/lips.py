"""Random boards and lips on them, for fuzzing `Board.lip()` as
`corners.py` fuzzes dog bones and chamfers: the board is one of
`boards.py`'s (an outline, holes, pockets, cuts, notches, V-grooves, edge
holes, rounded corners), then one or two `lip()` calls naming some of its
narrow faces, thin banding to deep lips. Each case is built twice, the
board lying, standing or upright and at two places: in the outline's own
frame, from its low corner, the result must be the same, and a refusal
must be one both ways.

`run_case` checks, from the outside, after each call:

- no other error than a LangError; a refused call changes nothing, neither
  the board nor its scope (no strip is left behind);
- an accepted one keeps the board's box; the board and its strips are the
  board as it was (in its plane, nothing lost, nothing added) and share no
  material; each strip is a slat of the lip's material, its section the
  lip's thickness by the board's, flush with both big faces, in the band
  `t` deep behind the face it lips; there is one strip per straight edge
  the face had (its stretches along the face, as `contact.end_spans` finds
  them), and the outline has no edge left in a lipped face;
- the layout plans, draws and meshes.
"""
from __future__ import annotations

import traceback
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from hypothesis import strategies as st
from shapely.geometry import box as shapely_box
from shapely.geometry.base import BaseGeometry
from shapely.ops import unary_union

from boards import BoardCase, Feature, OutlineKind, Place, _module_box, _outline_shape, _pipeline_problems  # pyright: ignore[reportPrivateUsage]
from boards import apply as apply_feature
from boards import features as feature_cases
from fuzzing import floats, fresh, sizes
from lang import Board, LangError, Slat, board, module, sheet_material, slat_material
from lang.core.contact import end_spans
from lang.core.geometry import NARROWEST
from lang.core.scope import Scope

OAK = slat_material("oak")


@dataclass(frozen=True)
class LipCase:
    """A board from `boards.py`'s parts and `lip()` calls on it, each the
    narrow faces it names (0 to 3: low u, high u, low v, high v of the
    outline's frame, in the order named) and the lip's thickness."""
    t: float
    size: tuple[float, float]
    outline: OutlineKind
    outline_r: float
    features: tuple[Feature, ...]
    calls: tuple[tuple[tuple[int, ...], float], ...]
    place: Place = "bottom"
    origin: tuple[float, float, float] = (0.0, 0.0, 0.0)
    place2: Place = "left"
    origin2: tuple[float, float, float] = (0.0, 0.0, 0.0)


@st.composite
def lip_cases(draw: st.DrawFn) -> LipCase:
    t = draw(st.sampled_from([6.0, 9.0, 12.0, 15.0, 18.0, 24.0]))
    size = (draw(sizes(40, 1600)), draw(sizes(40, 1000)))
    outline: OutlineKind = draw(st.sampled_from(["rect", "rect", "rect", "rect", "rounded", "taper", "taper",
                                                 "slot"]))
    outline_r = draw(floats(0.05, 0.45)) * min(size) if outline in ("rounded", "taper") else 0.0
    feats = tuple(draw(st.lists(feature_cases(size, t), max_size=4)))
    # (mostly lips as built, now and then the thinnest and the deepest)
    thick = st.one_of(st.just(0.5), st.just(2.0), st.just(10.0), st.just(t), sizes(0.3, 40), sizes(0.3, 40),
                      st.sampled_from([0.005, 0.01, 0.0101, 0.02, min(size)]))
    faces = st.permutations([0, 1, 2, 3]).flatmap(lambda p: st.integers(1, 4).map(lambda n: tuple(p[:n])))
    calls = tuple(draw(st.lists(st.tuples(faces, thick), min_size=1, max_size=2)))
    far = sizes(-4000, 4000)
    places: list[Place] = ["bottom", "left", "back"]
    return LipCase(t, size, outline, outline_r, feats, calls,
                   draw(st.sampled_from(places)), draw(st.one_of(st.just((0.0, 0.0, 0.0)), st.tuples(far, far, far))),
                   draw(st.sampled_from(places)), draw(st.tuples(far, far, far)))


# -- building ------------------------------------------------------------------------------------

@dataclass
class Built:
    module: Scope
    board: Board
    low: tuple[float, float]                # the outline's low corner when the board was made


def build(case: LipCase, place: Place, origin: tuple[float, float, float]) -> Built:
    """The case's board with every feature the language accepts (a refused
    one is left out, as in `boards.py`)."""
    bc = BoardCase(case.t, place, origin, case.size, case.outline, case.outline_r, case.features)
    with module("m", _module_box(bc)) as m:
        b = board("panel", sheet_material("birch", t=case.t), _outline_shape(bc)).on(getattr(m, place))
        u0, v0, _, _ = b.outline.bounds
        for i, f in enumerate(case.features):
            try:
                apply_feature(b, f, f"{f.kind}_{i}")
            except LangError:
                pass
    return Built(m, b, (u0, v0))


def _face(b: Board, k: int) -> Any:
    axis = b.u_axis if k < 2 else b.v_axis
    return b.face(b.scope.frame.direction_of(axis, 1 if k % 2 else -1))


def _state(built: Built) -> tuple[str, list[object], list[str]]:
    b = built.board
    return b.outline.geometry.wkt, list(b.ops), sorted(built.module.parts)


def _uv(b: Board, s: Board) -> BaseGeometry:
    """A strip's footprint in the board's plane."""
    sb = s.box()
    return shapely_box(sb.lo[b.u_axis], sb.lo[b.v_axis], sb.hi[b.u_axis], sb.hi[b.v_axis])


# -- checking -----------------------------------------------------------------------------------

def run_case(case: LipCase) -> list[str]:
    """What is wrong with the case's lips, built two ways."""
    try:
        with fresh():
            first = _attempt(case, case.place, case.origin)
        with fresh():
            second = _attempt(case, case.place2, case.origin2)
    except Exception as e:
        frame = next((fr for fr in reversed(traceback.extract_tb(e.__traceback__))
                      if "/lang/" in fr.filename), traceback.extract_tb(e.__traceback__)[-1])
        return [f"{type(e).__name__} at {Path(frame.filename).name}:{frame.lineno}: {e}"]
    problems = first[0] + second[0]
    if problems:
        return problems
    if first[1] != second[1]:
        return [f"{case.place2} instead of {case.place} it comes out otherwise: {first[1]} / {second[1]}"]
    return []


def _attempt(case: LipCase, place: Place, origin: tuple[float, float, float]) -> tuple[list[str], list[Any]]:
    built = build(case, place, origin)
    b = built.board
    problems: list[str] = []
    results: list[Any] = []
    lipped: list[Any] = []
    for faces, t in case.calls:
        named = [_face(b, k) for k in faces]
        before = _state(built)
        outline = b.outline.geometry
        box = b.box()
        spans = {k: [s for s in end_spans(b, f.axis, f.value, b.v_axis if f.axis == b.u_axis else b.u_axis, 1e-6)
                     if s[1] - s[0] >= NARROWEST] for k, f in zip(faces, named)}
        parts = set(built.module.parts)
        try:
            with built.module:
                b.lip(named, t, OAK)
        except LangError as e:
            if _state(built) != before:
                problems.append(f"a refused lip changed the board or its scope: {e}")
            results.append(("refused", str(e).split(":")[1][:60] if ":" in str(e) else str(e)))
            continue
        lipped += named
        strips = [built.module.parts[n] for n in sorted(set(built.module.parts) - parts)]
        problems += _promises(b, box, outline, strips, named, faces, spans, t)
        results.append(("accepted", _summary(built, strips)))
    problems += _pipeline_problems()
    return problems, results


def _promises(b: Board, box: Any, outline: BaseGeometry, strips: list[Board], named: list[Any], faces: tuple[int, ...],
              spans: dict[int, list[tuple[float, float]]], t: float) -> list[str]:
    problems: list[str] = []
    if b.box().lo != box.lo or b.box().hi != box.hi:
        problems.append("the board's box changed")
    after = b.outline.geometry
    feet = [_uv(b, s) for s in strips]
    whole = unary_union([after, *feet])
    lost, added = outline.difference(whole).area, whole.difference(outline).area
    if lost > 1e-6 or added > 1e-6:
        problems.append(f"the board and its strips are not the board as it was: {lost:.3g} mm2 lost, {added:.3g} added")
    shared = sum(after.intersection(g).area for g in feet) + sum(
        feet[i].intersection(feet[j]).area for i in range(len(feet)) for j in range(i + 1, len(feet)))
    if shared > 1e-6:
        problems.append(f"the board and its strips share {shared:.3g} mm2")
    tb = b.t_axis
    for s in strips:
        if not isinstance(s, Slat) or s.material is not OAK:
            problems.append(f"{s.path} is not a slat of the lip's material")
            continue
        if s.section != tuple(sorted((t, b.thickness))):
            problems.append(f"{s.path}'s section is {s.section}, not {t:g} by {b.thickness:g}")
        sb = s.box()
        if abs(sb.lo[tb] - box.lo[tb]) > 1e-9 or abs(sb.hi[tb] - box.hi[tb]) > 1e-9:
            problems.append(f"{s.path} is not flush with the board's big faces")
    count = 0
    for k, f in zip(faces, named):
        mine = [s for s in strips if s.name.startswith(f"{b.name}_lip_{f.name}")
                and s.name[len(f"{b.name}_lip_{f.name}"):] in ("",) + tuple(f"_{i}" for i in range(1, 99))]
        count += len(mine)
        for s in mine:
            sb = s.box()
            band = (f.value - t, f.value) if f.direction.sign > 0 else (f.value, f.value + t)
            if abs(sb.lo[f.axis] - band[0]) > 1e-6 or abs(sb.hi[f.axis] - band[1]) > 1e-6:
                problems.append(f"{s.path} is not in the band {t:g} behind the {f.name} face")
        if any(s1 - s0 >= NARROWEST for s0, s1 in end_spans(b, f.axis, f.value,
                                                                b.v_axis if f.axis == b.u_axis else b.u_axis, 1e-6)):
            problems.append(f"the outline still has an edge in the lipped {f.name} face")
        if len(mine) != len(spans[k]) and k == faces[0]:
            # (later faces lose the stretches the earlier strips cover, so only the first is exact)
            problems.append(f"{len(mine)} strips on the {f.name} face, which had {len(spans[k])} straight edges")
    if count != len(strips):
        problems.append(f"{len(strips) - count} strips are not named after their faces")
    return problems


def _summary(built: Built, strips: list[Board]) -> Any:
    """The outline and the strips in the outline's own frame, from its low
    corner as the board was made, rounded."""
    b = built.board
    u0, v0 = built.low

    def r(x: float) -> float:
        return round(x, 4) + 0.0

    rings = sorted(tuple((r(p[0] - u0), r(p[1] - v0)) for p in ring) for ring in b.outline.rings())
    feet = sorted(tuple(r(c) for c in (g.bounds[0] - u0, g.bounds[1] - v0, g.bounds[2] - u0, g.bounds[3] - v0))
                  for g in (_uv(b, s) for s in strips))
    return round(b.outline.area, 3), len(rings), feet
