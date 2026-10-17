"""Random boards and the operations on their corners and rims, for fuzzing
`Board.dogbones()` and `Board.chamfer()` as `boards.py` fuzzes the
cutouts: the board is one of `boards.py`'s (an outline, holes, pockets,
cuts, notches, V-grooves, edge holes, rounded corners), then the operation
under test, with its settings drawn from their ranges and a little beyond.
Each case is built twice, the board lying, standing or upright and at two
places: in the outline's own frame, from its low corner, the result must be
the same, and a refusal must be one both ways.

`run_case` checks, from the outside:

- every call: no other error than a LangError; a refused call changes
  nothing; an accepted one plans, draws and meshes, and leaves the board in
  one piece;
- `dogbones()`: no corner it saw is left, and a second call refused
  changes nothing; every inside corner it saw
  (`lang.core.dogbones.corners`, those `at=` names) has its corner cut away,
  `relief / 2` round it, by a cut or by a pocket from the corner's face as
  deep as the corner's wall; and no relief takes material beyond its
  corner's disc, the add-in's circle (`(tool / 2) / sin(angle)` from the
  corner on its bisector, that plus `relief / 2` in radius);
- `chamfer()` of the outline's corners (the edges through the board): it
  takes off a triangle `size` along both edges at each corner named and
  nothing else, and adds nothing;
- `chamfer()` along a rim (a big face's outline or edge, a named
  operation): the preview's volume shrinks, by no more than a 45 degree
  chamfer that size takes along every edge of that face.
"""
from __future__ import annotations

import math
import traceback
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

from hypothesis import strategies as st
from shapely import affinity
from shapely.geometry import Point
from shapely.geometry.base import BaseGeometry
from shapely.geometry.polygon import orient
from shapely.ops import unary_union

from boards import BoardCase, Feature, OutlineKind, Place, _module_box, _outline_shape, _pipeline_problems  # pyright: ignore[reportPrivateUsage]
from boards import apply as apply_feature
from boards import features as feature_cases
from fuzzing import floats, fresh, sizes
from lang import Board, LangError, board, sheet_material, module
from lang.core import dogbones as dogbone_geometry
from lang.core.cutouts import circle_geometry
from lang.core.geometry import clean, polygons_of
from lang.core.scope import Scope
from lang.core.layout import build_layout
from lang.core.ops import MIN_CHAMFER, Cut, Op, Pocket
from lang.preview.mesh import FINE, mesh_part

OpKind = Literal["dogbones", "corner chamfer", "rim chamfer"]


@dataclass(frozen=True)
class CornerOpCase:
    """A board from `boards.py`'s parts and one operation on its corners or
    rims: `dogbones` (`tool`, `relief`, `at`: None for every corner, else
    the index of the feature whose operation it names), a chamfer `size`
    of the outline's corners `which` (indices 0 to 3: low u low v, low u
    high v, high u low v, high u high v), or a chamfer `size` along rims
    `which` (0, 1: a big face's outline; 2 to 9: an edge of a big face, 4
    per face; 10 and up: the operation of feature `which - 10`)."""
    t: float
    size: tuple[float, float]
    outline: OutlineKind
    outline_r: float
    features: tuple[Feature, ...]
    op: OpKind
    tool: float = 6.0
    relief: float = 0.1
    at: int | None = None
    chamfer: float = 1.0
    which: tuple[int, ...] = ()
    place: Place = "bottom"
    origin: tuple[float, float, float] = (0.0, 0.0, 0.0)
    place2: Place = "left"
    origin2: tuple[float, float, float] = (0.0, 0.0, 0.0)


@st.composite
def corner_op_cases(draw: st.DrawFn) -> CornerOpCase:
    t = draw(st.sampled_from([6.0, 9.0, 12.0, 15.0, 18.0, 24.0]))
    size = (draw(sizes(40, 1600)), draw(sizes(40, 1000)))
    outline: OutlineKind = draw(st.sampled_from(["rect", "rect", "rect", "rounded", "taper", "slot"]))
    outline_r = draw(floats(0.05, 0.45)) * min(size) if outline in ("rounded", "taper") else 0.0
    feats = tuple(draw(st.lists(feature_cases(size, t), max_size=6)))
    op: OpKind = draw(st.sampled_from(["dogbones", "dogbones", "corner chamfer", "rim chamfer"]))
    far = sizes(-4000, 4000)
    places: list[Place] = ["bottom", "left", "back"]
    common: dict[str, Any] = dict(
        t=t, size=size, outline=outline, outline_r=outline_r, features=feats, op=op,
        place=draw(st.sampled_from(places)), origin=draw(st.one_of(st.just((0.0, 0.0, 0.0)), st.tuples(far, far, far))),
        place2=draw(st.sampled_from(places)), origin2=draw(st.tuples(far, far, far)))
    if op == "dogbones":
        at = draw(st.one_of(st.none(), st.none(), st.integers(0, max(0, len(feats) - 1)))) if feats else None
        return CornerOpCase(**common, tool=draw(st.one_of(st.just(6.0), st.sampled_from([3.0, 8.0, 12.0]), sizes(0.5, 30))),
                          relief=draw(st.one_of(st.just(0.1), st.just(0.0), floats(0, 2))), at=at)
    chamfer = draw(st.one_of(st.just(1.0), st.just(MIN_CHAMFER), floats(0.01, 5), sizes(1, 100)))
    if op == "corner chamfer":
        which = tuple(sorted(set(draw(st.lists(st.integers(0, 3), min_size=1, max_size=4)))))
        return CornerOpCase(**common, chamfer=chamfer, which=which)
    rims = st.integers(0, 9) if not feats else st.one_of(st.integers(0, 9), st.integers(10, 9 + len(feats)))
    which = tuple(sorted(set(draw(st.lists(rims, min_size=1, max_size=3)))))
    return CornerOpCase(**common, chamfer=min(chamfer, t / 2 + 1), which=which)


# -- building ------------------------------------------------------------------------------------

@dataclass
class Built:
    module: Scope
    board: Board
    low: tuple[float, float]                # the outline's low corner when the board was made
    names: dict[int, str]                   # feature index -> the name of the operation it made


#: The module's side toward +t of a board on each side.
_PLUS_T: dict[Place, str] = {"bottom": "top", "left": "right", "back": "back"}


def build(case: CornerOpCase, place: Place, origin: tuple[float, float, float], name: str = "m") -> Built:
    """The case's board in a module `name`, with every feature the language
    accepts (a refused one is left out, as in `boards.py`)."""
    bc = BoardCase(case.t, place, origin, case.size, case.outline, case.outline_r, case.features)
    with module(name, _module_box(bc)) as m:
        b = board("panel", sheet_material("birch", t=case.t), _outline_shape(bc)).on(getattr(m, place))
        # (the face a cut's chamfer is on, the show face, the first of `big_faces()`, toward
        # +t, as the features' faces are numbered: by default it is the second lying flat but
        # the first on the back)
        b.show(getattr(m, _PLUS_T[place]))
        u0, v0, _, _ = b.outline.bounds
        names: dict[int, str] = {}
        for i, f in enumerate(case.features):
            try:
                apply_feature(b, f, f"{f.kind}_{i}")
                names[i] = f"{f.kind}_{i}"
            except LangError:
                pass
    return Built(m, b, (u0, v0), names)


def _state(b: Board) -> tuple[str, list[Op]]:
    return b.outline.geometry.wkt, list(b.ops)


def _targets(case: CornerOpCase, built: Built) -> list[Any] | None:
    """What the call names, or None when it names nothing that exists."""
    b = built.board
    if case.op == "dogbones":
        if case.at is None:
            return []
        name = built.names.get(case.at)
        return [getattr(b, name)] if name is not None and b.has_operation(name) else None
    frame = b.scope.frame
    if case.op == "corner chamfer":
        out: list[Any] = []
        for k in case.which:
            du = frame.direction_of(b.u_axis, 1 if k >= 2 else -1)
            dv = frame.direction_of(b.v_axis, 1 if k % 2 else -1)
            out.append(getattr(b.face(du), dv.name))
        return out
    out = []
    faces = b.big_faces()
    for k in case.which:
        if k < 2:
            out.append(faces[k].outline)
        elif k < 10:
            face = faces[(k - 2) // 4]
            narrow = [frame.direction_of(a, s) for a in (b.u_axis, b.v_axis) for s in (-1, 1)][(k - 2) % 4]
            out.append(getattr(face, narrow.name))
        else:
            name = built.names.get(k - 10)
            if name is None or not b.has_operation(name):
                return None
            out.append(getattr(b, name))
    return out


# -- checking -----------------------------------------------------------------------------------

def run_case(case: CornerOpCase) -> list[str]:
    """What is wrong with the case's operation, built two ways."""
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
    (s1, r1), (s2, r2) = first[1], second[1]
    if s1 != s2:
        return [f"{case.place} it is {s1}, {case.place2} {s2}: {r1 if s1 != 'accepted' else r2}"]
    if s1 == "accepted":
        difference = _difference(r1, r2)
        if difference:
            return [f"{case.place2} instead of {case.place} it comes out otherwise: {difference}"]
    return []


def _attempt(case: CornerOpCase, place: Place, origin: tuple[float, float, float]) -> tuple[list[str], tuple[str, Any]]:
    built = build(case, place, origin)
    b = built.board
    targets = _targets(case, built)
    if targets is None:
        return [], ("unnamed", None)
    if case.op == "dogbones":
        return _dogbones(case, built, targets)
    before = _state(b)
    outline = b.outline.geometry
    volume = _volume(b)
    try:
        with built.module:
            b.chamfer(targets, case.chamfer)
    except LangError as e:
        return ([] if _state(b) == before else [f"a refused chamfer changed the board: {e}"]), ("refused", str(e))
    problems = _common_problems(b)
    if case.op == "corner chamfer":
        problems += _corner_problems(case, b, outline)
    elif not problems:
        problems += _rim_problems(case, b, volume)
    return problems, ("accepted", _summary(built))


def _common_problems(b: Board) -> list[str]:
    problems = _pipeline_problems()
    if len(b.outline.polygons()) != 1:
        problems.append(f"the board is in {len(b.outline.polygons())} pieces")
    return problems


# -- dogbones ------------------------------------------------------------------------------------

def _dogbones(case: CornerOpCase, built: Built, targets: list[Any]) -> tuple[list[str], tuple[str, Any]]:
    b = built.board
    at = targets or None
    request = dogbone_geometry.Request(case.tool, case.relief, None)
    seen = [c for c in dogbone_geometry.corners(b)
            if at is None or (case.at is not None and built.names[case.at] in c.ops)]
    before = _state(b)
    try:
        with built.module:
            b.dogbones(case.tool, case.relief, at=at)
    except LangError as e:
        return ([] if _state(b) == before else [f"a refused dogbones() changed the board: {e}"]), ("refused", str(e))
    problems = _common_problems(b)
    new = b.ops[len(before[1]):]
    # No corner it saw is left. (Its reliefs may make new ones, as where reliefs
    # from both faces overlap and go through together, or where a through relief,
    # kept to its own level, takes a shallower pocket's corner down with it: the
    # corner it saw, relieved as deep as it was, is there again, deeper; corners
    # made later. `_relieved` checks that each seen corner went as deep as it was.)
    left = [c for c in dogbone_geometry.corners(b)
            if any(math.dist(c.point, s.point) < 1e-6 and c.face == s.face and _same_depth(c.bottom, s.bottom)
                   for s in seen)]
    if left:
        problems.append(f"{len(left)} corners are left after dogbones(), e.g. at "
                        f"({left[0].point[0]:.3f}, {left[0].point[1]:.3f}) on {left[0].face}")
    once = _state(b)
    try:
        with built.module:
            b.dogbones(case.tool, case.relief, at=at)
    except LangError as e:
        # (refused it may be: a relief for a corner the first made may split the board)
        if _state(b) != once:
            problems.append(f"a second dogbones() refused changed the board: {e}")
    discs = [_disc(c, request) for c in seen]
    allowed = unary_union(discs).buffer(1e-3) if discs else Point(0, 0).buffer(0)
    for op in new:
        if not isinstance(op, (Cut, Pocket)):
            problems.append(f"dogbones() made a {op.kind}")
            continue
        beyond = op.shape.geometry.difference(allowed).area
        if beyond > 1e-6:
            problems.append(f"the relief {op.name!r} takes {beyond:.3g} mm2 beyond its corners' discs")
    if case.relief >= 0.02:
        for c in seen:
            problems += _relieved(b, c, new, case.relief)
    return problems, ("accepted", _summary(built))


def _same_depth(a: float | None, b: float | None) -> bool:
    return a is None and b is None or a is not None and b is not None and abs(a - b) < 1e-9


def _disc(c: dogbone_geometry.Corner, request: dogbone_geometry.Request) -> BaseGeometry:
    """The add-in's circle at the corner, worked out again from its rule."""
    reach = request.tool / 2 / math.sin(c.angle)
    bx, by = c.a[0] + c.b[0], c.a[1] + c.b[1]
    k = reach / math.hypot(bx, by)
    return circle_geometry((c.point[0] + bx * k, c.point[1] + by * k), reach + request.relief / 2)


def _relieved(b: Board, c: dogbone_geometry.Corner, new: list[Op], relief: float) -> list[str]:
    """The corner is cut away `relief / 4` round it, by a new cut or a new
    pocket from its face as deep as its wall, or through."""
    ball = Point(c.point).buffer(relief / 4, quad_segs=16)
    cover: list[BaseGeometry] = []
    for op in new:
        if isinstance(op, Cut):
            cover.append(op.shape.geometry)
        elif isinstance(op, Pocket) and (op.depth >= b.thickness - 1e-9 or (
                op.face == c.face and (c.bottom is None or op.depth >= c.bottom - 1e-9))):
            cover.append(op.shape.geometry)
    level = c.level.intersection(ball)
    left = level.difference(unary_union(cover)).area if cover else level.area
    if left > 1e-9 * max(1.0, relief):
        return [f"the corner at ({c.point[0]:.3f}, {c.point[1]:.3f}) on {c.face} keeps {left:.3g} mm2 of its "
                f"{relief / 4:g} round"]
    return []


# -- chamfers ------------------------------------------------------------------------------------

def _corner_problems(case: CornerOpCase, b: Board, before: BaseGeometry) -> list[str]:
    """Each corner named loses a triangle `size` along both its edges, and
    nothing else changes."""
    after = b.outline.geometry
    problems: list[str] = []
    gained = after.difference(before).area
    if gained > 1e-6:
        problems.append(f"the chamfer adds {gained:.3g} mm2")
    lost = before.difference(after)
    s = case.chamfer
    box = before.bounds
    corners = [(box[0] if k < 2 else box[2], box[1] if k % 2 == 0 else box[3]) for k in case.which]
    near = unary_union([Point(p).buffer(s * 1.01 + 1e-6, quad_segs=16) for p in corners])
    stray = lost.difference(near).area
    if stray > 1e-6:
        problems.append(f"the chamfer takes {stray:.3g} mm2 away from the corners it names")
    for p in corners:
        angle = _angle_at(before, p)
        if angle is None:
            continue
        want = 0.5 * s * s * math.sin(angle)
        got = lost.intersection(Point(p).buffer(s * 1.01 + 1e-6, quad_segs=16)).area
        if abs(got - want) > 1e-6 + 1e-6 * want:
            problems.append(f"the chamfer at ({p[0]:.3f}, {p[1]:.3f}) takes {got:.6g} mm2, a triangle {s:g} along "
                            f"its edges is {want:.6g}")
    return problems


def _angle_at(g: BaseGeometry, p: tuple[float, float]) -> float | None:
    """The angle of the outline's corner at `p`, inside the material."""
    for poly in polygons_of(g):
        ring = list(orient(poly, 1.0).exterior.coords)[:-1]
        for i, q in enumerate(ring):
            if math.dist(q, p) < 1e-6:
                a, c = ring[i - 1], ring[(i + 1) % len(ring)]
                v1 = (a[0] - q[0], a[1] - q[1])
                v2 = (c[0] - q[0], c[1] - q[1])
                return math.acos(max(-1.0, min(1.0, (v1[0] * v2[0] + v1[1] * v2[1])
                                               / (math.hypot(*v1) * math.hypot(*v2)))))
    return None


def _volume(b: Board) -> float:
    layout = build_layout()
    part = next(p for m in layout["modules"] for p in m["parts"] if p["path"] == b.path)
    return float(mesh_part(part, layout["frame"], level=FINE).volume)


def _rim_problems(case: CornerOpCase, b: Board, before: float) -> list[str]:
    """The preview takes material away, no more than a 45 degree chamfer
    `size` along every edge of both big faces would."""
    after = _volume(b)
    s = case.chamfer
    rims = sum(p.length for p in polygons_of(b.outline.geometry))
    ops = [op for op in b.ops if isinstance(op, (Cut, Pocket))]
    rims += sum(op.shape.geometry.length for op in ops)
    noise = 1e-3 + 1e-5 * before                # (the meshes' booleans round so much)
    most = 2 * 0.5 * s * s * rims * 1.01 + noise
    if after > before + noise:
        return [f"the chamfer adds {after - before:.4g} mm3 in the preview"]
    if before - after > most:
        return [f"the chamfer takes {before - after:.4g} mm3 in the preview, more than {most:.4g}"]
    return []


# -- the summary, in the outline's frame from its low corner -----------------------------------------

def _summary(built: Built) -> list[tuple[Any, ...]]:
    b = built.board
    du, dv = -built.low[0], -built.low[1]
    faces = [f.world_name for f in b.big_faces()]

    def moved(g: BaseGeometry) -> BaseGeometry:
        return affinity.translate(g, du, dv)

    out: list[tuple[Any, ...]] = [("outline", moved(b.outline.geometry))]
    reliefs: dict[tuple[Any, ...], list[BaseGeometry]] = {}
    for op in b.ops:
        name = getattr(op, "name", None) or ""
        if isinstance(op, (Cut, Pocket)) and "dogbones" in name:
            # (the reliefs by what they cut, whatever the operation they went into: a corner
            # through the board is relieved from the face it starts deepest on, either on a tie,
            # and its relief joins the operation of that face)
            key: tuple[Any, ...] = ("through",)
            if isinstance(op, Pocket) and op.depth < b.thickness - 1e-9:
                key = ("pocket", faces.index(op.face), round(op.depth, 6))
            reliefs.setdefault(key, []).append(op.shape.geometry)
        elif isinstance(op, (Cut, Pocket)):
            face = faces.index(op.face) if isinstance(op, Pocket) else None
            depth = op.depth if isinstance(op, Pocket) else None
            out.append((op.kind, op.name, face, depth, moved(op.shape.geometry)))
        else:
            out.append((op.kind, getattr(op, "name", None)))
    for key in sorted(reliefs, key=repr):
        out.append(("reliefs", *key, moved(unary_union(reliefs[key]))))
    return out


def _difference(a: list[tuple[Any, ...]], b: list[tuple[Any, ...]]) -> str | None:
    if len(a) != len(b):
        return f"{len(a)} items against {len(b)}"
    for p, q in zip(a, b):
        if len(p) != len(q):
            return f"{p[:3]} against {q[:3]}"
        for x, y in zip(p, q):
            if isinstance(x, BaseGeometry) and isinstance(y, BaseGeometry):
                # (what is narrower than 0.01 mm all over is nothing the language means, and
                # where three boundaries meet within that, the noise of another frame can
                # settle it either way: a 0.016 mm triangle of a relief kept or left out)
                d = x.symmetric_difference(y)
                if d.area > 1e-6 and clean(d).area > 1e-6:
                    return f"{p[:3]}: the shapes differ by {d.area:.3g} mm2"
            elif isinstance(x, float) and isinstance(y, float):
                if not math.isclose(x, y, abs_tol=1e-6):
                    return f"{p[:3]}: {x} against {y}"
            elif x != y:
                return f"{p[:3]} against {q[:3]}"
    return None


def apply(case: CornerOpCase, name: str) -> None:
    """Builds the case's board as module `name`, as it lies first, and
    makes its operation: for the Fusion batch check (`fusion_batch.py
    corners`)."""
    built = build(case, case.place, case.origin, name)
    targets = _targets(case, built)
    assert targets is not None
    with built.module:
        if case.op == "dogbones":
            built.board.dogbones(case.tool, case.relief, at=targets or None)
        else:
            built.board.chamfer(targets, case.chamfer)


def accepted(case: CornerOpCase) -> bool:
    """Whether the case's operation is accepted and keeps every promise."""
    if run_case(case):
        return False
    with fresh():
        return _attempt(case, case.place, case.origin)[1][0] == "accepted"


__all__ = ["CornerOpCase", "accepted", "apply", "corner_op_cases", "run_case"]
