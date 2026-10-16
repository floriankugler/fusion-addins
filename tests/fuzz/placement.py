"""Random designs placed as build files place them, for fuzzing the
placement algebra (`lang.core.scope`, `box`, `refs`, `directions`, `faces`
and the placement half of `part`) as `hardware.py` fuzzes the hardware: a
case is plain data, written in its module's own terms, built with the
language's own calls and checked from the outside.

A case is a module or a cabinet with a carcass in the examples' shapes
(sides, perhaps with a toe kick a bottom stands on and a dado a shelf sits
in; a bottom and a top on the box's sides or raised; a back, perhaps
grooved into the sides; a shelf and a divider centred between boards; a
door over the front or set in between the carcass); a bay of the interior
(split along any extent) in a scope, a module or a cabinet of its own,
turned or mirrored, with a face and a drawer box in it; and boards placed
at random: on a side, on another board's face or a position, centred on a
mix of positions, between sides, boards, faces, mixes and boxes, inset,
some of them a rect. Then operations placed through anchors
(`side.inner.front(37).bottom(z)`), `to()` depths and `spread()` rows:
holes, pockets, slots, notches, holes into narrow faces, a board cut by
another, chamfers along an edge and on a corner, fillets.

`run_case` builds it three ways that must give the same result, measured
in the module's own terms (inward from its front, left and bottom sides;
an outline in the two measures of its plane):

- at another place (fractional and far origins), a cabinet facing another
  side of its box;
- in another world frame (`set_frame`, its directions bound to other axes
  and signs, left- or right-handed, with aliases), at a third place, the
  module mirrored the other way or not (the cabinets in it mirrored back
  to stay as they were), and written otherwise: placement modifiers,
  `between()`'s limits, boards and operations in another order where the
  order must not matter, boards resolved in another order, a face moved as
  a bare position (`face.position + n`), a side or a face moved there in
  two steps (`face.gap(2 * n).into(n)`), `on()` a side or a face moved without
  `toward=`, an alias for a side, a board for its face, a mix of positions
  (`a + b - c` among them) or a box's middle spelt another way, a box for
  its four sides, an anchor measured from the opposite edge or given as a
  position, its edges in the other order, a depth `to()` the other face
  for its number, a row spread from its other end, an edge named from its
  other face, a slot's `along=` as an extent, a side or a face.

A refusal must be one all three ways (the same boards and operations
refused), and the preview must mesh every board as large in the other
world frame. And it checks what placement promises, the first way: a
board lies on what `on()` names, its thickness toward the side named, or
is centred on what `center()` names; between two limits it reaches from
one to the other, less its inset; between a board it touches that board's
face and reaches into it no further than `into()` says; with one limit, it
reaches to the box's side away from it; its inner face is the one toward
its scope's middle, and across the middle without `show()` it shows its
top, else back, else right; it is machined from the face `machine()` names,
given at any time; a board made of a shape has its outline's box
and fills its two limits less its inset, sits against a single one, or at
its scope's front, left or bottom side; limits that leave it open where a
board lies are refused, and only such ones (`_ambiguity` works them out
again: a board twice, boards overlapping, a position or a face moved by
`gap()` inside a board, a single limit at the box's middle, a board as the
only limit centred in it) [the rules decided by Florian, 2026-10-14]; an
operation lies where its anchor says, as deep as its depth says, and a row
has as many holes as fit; a refused operation changes nothing; a side or
a face plus or minus a length is refused, naming `into()` and `gap()`
[decided by Florian, 2026-10-15, syntax.md item 1]; and the layout plans,
draws and meshes.
"""
from __future__ import annotations

import math
import random
import traceback
from collections.abc import Callable, Sequence
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import Any, Literal

from hypothesis import strategies as st
from shapely import affinity
from shapely.geometry.base import BaseGeometry

from boards import _pipeline_problems  # pyright: ignore[reportPrivateUsage]
from fuzzing import floats, fresh, sizes
from lang import Box, Frame, LangError, Pos, Side, board, check, inside_box, sheet_material, module, \
    no_interference, rect, scope, set_frame, spread, through, to
from lang.core.directions import AXES, Axis, as_axis, world_frame
from lang.core.faces import Face
from lang.core.geometry import clean
from lang.core.layout import build_layout
from lang.core.ops import Chamfer, Cut, EdgeOp, Hole, Op, Pocket
from lang.core.part import Board, PartLimit
from lang.core.refs import as_pos
from lang.core.scope import Scope

# -- the module's own terms ---------------------------------------------------------------------

#: The measure each direction lies on: 0 inward from the front, 1 from the
#: left, 2 from the bottom.
MEASURE: dict[str, int] = {"front": 0, "back": 0, "left": 1, "right": 1, "bottom": 2, "top": 2}
#: The side each measure starts from and the one it ends at, and its extent.
LOW = ("front", "left", "bottom")
HIGH = ("back", "right", "top")
EXTENT: tuple[Literal["depth"], Literal["width"], Literal["height"]] = ("depth", "width", "height")
OPPOSITE = {"front": "back", "back": "front", "left": "right", "right": "left", "top": "bottom", "bottom": "top",
            "inner": "outer", "outer": "inner"}
#: The side of its box a cabinet opens toward, by index, in world terms.
FRONTS = ("front", "right", "back", "left")
#: The world frame's aliases (a module's frame keeps them, a cabinet's has none).
ALIASES = {"fs": "left", "bfs": "right"}


def _world_frames() -> list[tuple[str, str, str]]:
    """Every world frame as (front, left, top): the default first, then
    the other 47 bindings of the names to axes and signs."""
    codes = ("-x", "+x", "-y", "+y", "-z", "+z")
    frames = [("-x", "-y", "+z")]
    for front in codes:
        for top in codes:
            for left in codes:
                if len({front[1], top[1], left[1]}) == 3 and (front, left, top) not in frames:
                    frames.append((front, left, top))
    return frames


WORLD_FRAMES = _world_frames()


# -- the case -----------------------------------------------------------------------------------

RefKind = Literal["side", "part", "face", "mid", "op", "box"]


@dataclass(frozen=True)
class Ref:
    """Something a build file places by, in the terms of the scope it is
    used in:

    - "side": the side `name` of box `of` (0 the module's, 1 the bay's, 2
      the box in the bay) moved `by` into the box (negative: out of it);
    - "part": board `of` as a limit (its face toward the board placed),
      `by` into it (negative: `gap()`);
    - "face": board `of`'s face `name` (in its own scope's terms), moved
      `by` out of the board (negative: into it);
    - "mid": `by` of the way from `a` to `b` (0.5: halfway);
    - "op": board `of`'s operation and edge `name` ("toekick.top");
    - "box": box `of` as a limit."""
    kind: RefKind
    name: str = ""
    of: int = 0
    by: float = 0.0
    a: Ref | None = None
    b: Ref | None = None


@dataclass(frozen=True)
class Value:
    """A distance along an anchor's edge: `frac` of the board's extent
    from the edge plus `mm`, or the position `ref`."""
    frac: float = 0.0
    mm: float = 0.0
    ref: Ref | None = None


@dataclass(frozen=True)
class At:
    """An anchor: the board's face `face` (a direction in its scope's terms,
    "inner" or "outer"), then up to two edges, each a direction and a
    distance (None: the edge itself)."""
    face: str
    edges: tuple[tuple[str, Value | None], ...] = ()


@dataclass(frozen=True)
class Depth:
    """`mm` deep, `frac` of the extent behind the face, `to` the other face
    stopping `value` short of it, or `through`."""
    kind: Literal["mm", "frac", "to", "through"]
    value: float = 0.0


OpKind = Literal["hole", "row", "pocket", "slot", "notch", "edge_hole", "cut_part", "chamfer_edge", "chamfer_corner",
                 "fillet"]


@dataclass(frozen=True)
class OpSpec:
    """An operation on board `board`: a hole `d` across at `at`, a row of
    them along the first edge of `at` (`row`: from, to, pitch, count), a
    pocket or a through notch (`notch`, named `name`) of extents `size`
    (the board's two in-plane measures, in order) with its matching side
    or corner at `at`, a slot `d` wide centred on `at`, its end centres
    `size[0]` apart along the board's first or second in-plane measure
    (`along`), a hole `d` across into a narrow face, a cut of board
    `other` (`cut_part`), or a chamfer or fillet `size[0]` of the edge
    where `at`'s face meets its edge's (a corner through the board: two
    narrow faces)."""
    kind: OpKind
    board: int
    at: At = At("outer")
    d: float = 5.0
    size: tuple[float, float] = (0.0, 0.0)
    depth: Depth = Depth("through")
    name: str | None = None
    row: tuple[Ref, Ref, float, int] | None = None
    other: int = 0
    #: A pocket's or notch's rect with a corner cut off: `clip(**{a: k, b: m})`.
    clip: tuple[str, float, str, float] | None = None
    #: Which of the board's two in-plane measures a slot runs along.
    along: int = 0


@dataclass(frozen=True)
class BoardSpec:
    """A board in scope `scope` (0 the module, 1 the bay): on `at`, or
    centred on it, a bare position with its thickness `toward` a
    direction; between `limits`; inset; a rect of `shape`'s extents (the
    two in-plane measures in order); its show face and grain; the face
    `machine()` names ("inner", "outer" or a direction in its scope's
    terms); and the operations made right after it is placed (a toe kick
    another board stands on)."""
    name: str
    t: float
    at: Ref
    center: bool = False
    toward: str | None = None
    limits: tuple[Ref, ...] = ()
    inset: float = 0.0
    shape: tuple[float, float] | None = None
    show: str | None = None
    grain: str | None = None
    scope: int = 0
    ops: tuple[OpSpec, ...] = ()
    machine: str | None = None


@dataclass(frozen=True)
class BaySpec:
    """A bay of the module's interior after the carcass: split along
    `extent` into `split` bays (or bays of `sizes` and the rest), the
    `index`th; in a scope, a module (`module`, mirrored or not), or a
    cabinet facing `front` (a direction of the module) with its left toward
    `left`; and the box in it, the bay shrunk by `shrink` (front, back,
    left, right, top, bottom in the bay's own terms)."""
    split: int = 1
    index: int = 0
    front: str | None = None
    left: str = ""
    shrink: tuple[float, float, float, float, float, float] = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    extent: Literal["depth", "width", "height"] = "height"
    sizes: tuple[float, ...] = ()
    module: bool = False
    mirrored: bool = False
    gap: float = 0.0


@dataclass(frozen=True)
class PlacementCase:
    """A module (`kind`) of `size` (its own width, depth, height): the
    carcass `boards[:first_bay]`, the bay's `boards[first_bay:first_extra]`
    after `bay`, the rest after them; then `ops`. Built at `origin`
    (facing `front` for a cabinet, mirrored or not), at `origin2` facing
    `front + turn`, and in world frame `frame` at `origin3`, the module's
    mirroring flipped by `flip`, spelt as `seed` draws it."""
    kind: Literal["module", "cabinet"]
    size: tuple[float, float, float]
    boards: tuple[BoardSpec, ...]
    first_bay: int
    first_extra: int
    bay: BaySpec | None = None
    ops: tuple[OpSpec, ...] = ()
    mirrored: bool = False
    front: int = 0
    origin: tuple[float, float, float] = (0.0, 0.0, 0.0)
    turn: int = 1
    origin2: tuple[float, float, float] = (0.0, 0.0, 0.0)
    frame: int = 1
    flip: bool = False
    origin3: tuple[float, float, float] = (0.0, 0.0, 0.0)
    seed: int = 0


#: Where an operation goes, per in-plane axis of its face: the range a
#: shape covers (a point for a hole).
Where = dict[Axis, tuple[float, float]]


def side(name: str, by: float = 0.0, of: int = 0) -> Ref:
    return Ref("side", name, of, by)


def part(of: int, by: float = 0.0) -> Ref:
    return Ref("part", "", of, by)


def face(of: int, name: str, by: float = 0.0) -> Ref:
    return Ref("face", name, of, by)


def mid(a: Ref, b: Ref, by: float = 0.5) -> Ref:
    return Ref("mid", "", 0, by, a, b)


def deps(spec: BoardSpec, boxes: bool = False) -> set[int]:
    """The boards a board's placement names (with `boxes`, the boxes)."""
    found: set[int] = set()

    def walk(r: Ref | None) -> None:
        if r is None:
            return
        if (r.kind in ("side", "box")) == boxes and r.kind != "mid":
            found.add(r.of)
        walk(r.a)
        walk(r.b)
    for r in (spec.at, *spec.limits):
        walk(r)
    return found


# -- strategies ---------------------------------------------------------------------------------

def _thickness() -> st.SearchStrategy[float]:
    return st.one_of(st.sampled_from([15.0, 18.0, 19.0, 12.0, 9.0]), sizes(4, 40))


def _origin() -> st.SearchStrategy[tuple[float, float, float]]:
    far = st.one_of(sizes(-4000, 4000), floats(-4000, 4000))
    return st.one_of(st.just((0.0, 0.0, 0.0)), st.tuples(far, far, far))


def _mm(hi: float) -> st.SearchStrategy[float]:
    """A distance from 0 to `hi` (mm), as `sizes` draws them, but none
    under 0.01 mm but 0 (see `_by`)."""
    return sizes(0, hi).map(lambda v: 0.0 if v < 0.01 else v)


def _by(lo: float, hi: float) -> st.SearchStrategy[float]:
    """How far a plane is moved (mm): none, or at least 0.01 mm, as nothing
    narrower is meant (a limit 1e-6 out of the box is out of it or not by
    the rounding of the place, within the checks' tolerance, and a bottom
    1e-9 above the box's lies on its side or not for `interior`)."""
    return floats(lo, hi).map(lambda v: 0.0 if abs(v) < 0.01 else v)


def _fraction() -> st.SearchStrategy[float]:
    return st.one_of(st.just(0.5), st.sampled_from([0.25, 1 / 3, 0.75]), floats(0.05, 0.95))


class _Draft:
    """The boards drawn so far, with each board's thickness measure in its
    own scope's terms and in the module's, and the names of the bay's
    directions in the module's terms."""

    def __init__(self) -> None:
        self.specs: list[BoardSpec] = []
        self.t: list[int] = []          # in the board's own scope's terms
        self.t0: list[int] = []         # in the module's terms
        self.bay_names: dict[str, str] = {n: n for n in MEASURE}

    def add(self, spec: BoardSpec, t: int) -> int:
        self.specs.append(spec)
        self.t.append(t)
        self.t0.append(t if spec.scope == 0 else MEASURE[self.bay_names[LOW[t]]])
        return len(self.specs) - 1

    def module_name(self, i: int, name: str) -> str:
        """A direction of board i's scope in the module's terms."""
        return name if self.specs[i].scope == 0 else self.bay_names[name]


@st.composite
def _carcass(draw: st.DrawFn, d: _Draft) -> None:
    """Sides, a bottom, a top, a back, a shelf, a divider and a door, in
    the examples' shapes."""
    t = draw(_thickness())
    door = draw(st.sampled_from(["none", "overlay", "inset"]))
    door_t = draw(_thickness())
    gap = draw(st.one_of(st.just(0.0), st.just(1.5), floats(0, 5)))
    behind = (side("front", door_t + gap),) if door == "overlay" else ()
    toekick = draw(st.one_of(st.none(), st.none(), st.tuples(sizes(20, 120), sizes(30, 150))))
    shelf_t = draw(_thickness())
    dado = draw(st.one_of(st.none(), st.tuples(sizes(30, 600), _mm(40), sizes(50, 800), sizes(1, t - 1))))
    sides: list[int] = []
    for name in ("left", "right"):
        ops: tuple[OpSpec, ...] = ()
        if toekick is not None:
            ops = (OpSpec("notch", len(d.specs), At("outer", (("bottom", None), ("front", None))),
                          size=(toekick[0], toekick[1]), name="toekick"),)
        if dado is not None:
            # (a dado across the inner face, for a shelf that sits in it)
            length, start, z, deep = dado
            ops += (OpSpec("pocket", len(d.specs), At("inner", (("bottom", Value(mm=z)), ("front", Value(mm=start)))),
                           size=(length, shelf_t), depth=Depth("mm", deep), name="dado"),)
        sides.append(d.add(BoardSpec(name, t, side(name), limits=behind, ops=ops), 1))
    left, right = sides
    across = [part(left), part(right)]
    bottom = top = back = None
    if draw(st.integers(0, 9)) < 9:
        if toekick is not None and draw(st.booleans()):
            at, toward = Ref("op", "toekick.top", left), "top"
        else:
            at, toward = side("bottom", draw(st.one_of(st.just(0.0), _mm(120)))), None
        bottom = d.add(BoardSpec("bottom", t, at, toward=toward,
                                 limits=tuple(draw(st.permutations([*across, *behind])))), 2)
    if draw(st.integers(0, 9)) < 8:
        top = d.add(BoardSpec("top", t, side("top"), limits=tuple(draw(st.permutations([*across, *behind])))), 2)
    if draw(st.integers(0, 9)) < 7:
        groove = draw(st.one_of(st.just(0.0), st.just(0.0), sizes(1, t - 1) if t > 2 else st.just(0.0)))
        limits = [part(left, groove), part(right, groove)] + [part(i) for i in (bottom, top) if i is not None]
        k = len(d.specs)
        cuts = (OpSpec("cut_part", left, other=k), OpSpec("cut_part", right, other=k)) if groove else ()
        back = d.add(BoardSpec("back", draw(st.sampled_from([9.0, 6.0, 12.0])),
                               side("back", draw(st.one_of(st.just(0.0), _mm(30)))),
                               limits=tuple(draw(st.permutations(limits))), ops=cuts), 0)
    if dado is not None:
        limits = [Ref("op", "dado.floor", left), Ref("op", "dado.floor", right), side("front", draw(_mm(40)))]
        limits += [part(back)] if back is not None else []
        d.add(BoardSpec("shelf", shelf_t, mid(Ref("op", "dado.bottom", left), Ref("op", "dado.top", right)),
                        center=True, limits=tuple(draw(st.permutations(limits)))), 2)
    elif draw(st.booleans()):
        low = face(bottom, "top") if bottom is not None else side("bottom")
        high = face(top, "bottom") if top is not None else side("top")
        ends = [part(left, -1), part(right, -1)] if draw(st.booleans()) else [part(left), part(right)]
        limits = ends + ([part(back)] if back is not None else []) + [side("front", draw(_mm(40)))]
        d.add(BoardSpec("shelf", shelf_t, mid(low, high, draw(_fraction())), center=True,
                        limits=tuple(draw(st.permutations(limits))), show=draw(st.sampled_from([None, "top"]))), 2)
    if draw(st.integers(0, 9)) < 3:
        limits = [part(i) for i in (bottom, top, back) if i is not None] + list(behind)
        d.add(BoardSpec("divider", draw(_thickness()), mid(face(left, "right"), face(right, "left"), draw(_fraction())),
                        center=True, limits=tuple(draw(st.permutations(limits))),
                        show=draw(st.sampled_from([None, "left", "right"]))), 1)
    if door == "overlay":
        d.add(BoardSpec("door", door_t, side("front"), inset=draw(st.one_of(st.just(1.5), floats(0, 5)))), 0)
    elif door == "inset" and bottom is not None and top is not None:
        d.add(BoardSpec("door", door_t, side("front"),
                        limits=tuple(draw(st.permutations([part(left), part(right), part(bottom), part(top)]))),
                        inset=draw(st.one_of(st.just(1.5), floats(0, 5)))), 0)


@st.composite
def _bay(draw: st.DrawFn, d: _Draft) -> BaySpec:
    """A bay with a face over its front and perhaps a drawer box behind
    it, in the bay's own terms."""
    split = draw(st.integers(1, 3))
    extent: Literal["depth", "width", "height"] = draw(st.sampled_from(["height", "height", "width", "depth"]))
    bays = tuple(draw(st.lists(sizes(20, 400), max_size=2))) if draw(st.integers(0, 3)) == 0 else ()
    front: str | None = None
    left = ""
    kind = draw(st.sampled_from(["scope", "module", "cabinet"]))
    mirrored = kind == "module" and draw(st.booleans())
    if kind == "cabinet":
        front = draw(st.sampled_from(["front", "back", "left", "right"]))
        left = draw(st.sampled_from([n for n in ("front", "back", "left", "right") if MEASURE[n] != MEASURE[front]]))
        d.bay_names = {"front": front, "back": OPPOSITE[front], "left": left, "right": OPPOSITE[left],
                       "top": "top", "bottom": "bottom"}
    elif mirrored:
        d.bay_names = {**{n: n for n in MEASURE}, "left": "right", "right": "left"}
    face_t = draw(_thickness())
    shrink = (face_t + draw(_mm(5)), draw(_mm(30)), draw(_mm(15)), draw(_mm(15)),
              draw(_mm(40)), draw(_mm(15)))
    d.add(BoardSpec("face", face_t, side("front", of=1), limits=(Ref("box", of=1),),
                    inset=draw(st.one_of(st.just(1.5), floats(0, 4))), scope=1), 0)
    if draw(st.booleans()):
        t = draw(st.sampled_from([12.0, 15.0, 10.0]))
        box = Ref("box", of=2)
        lft = d.add(BoardSpec("left", t, side("left", of=2), limits=(box,), scope=1), 1)
        rgt = d.add(BoardSpec("right", t, side("right", of=2), limits=(box,), scope=1), 1)
        ends: list[int] = []
        for name in ("front", "back"):
            limits = [part(lft), part(rgt), side("bottom", of=2), side("top", of=2)]
            ends.append(d.add(BoardSpec(name, t, side(name, of=2), limits=tuple(draw(st.permutations(limits))),
                                        scope=1), 0))
        g = draw(st.one_of(st.just(0.0), _mm(5)))
        limits = [part(lft, g), part(rgt, g), part(ends[0], g), part(ends[1], g)]
        k = len(d.specs)
        cuts = tuple(OpSpec("cut_part", i, other=k) for i in (lft, rgt, *ends)) if g else ()
        d.add(BoardSpec("floor", 9.0, side("bottom", draw(_mm(20)), of=2), limits=tuple(draw(st.permutations(limits))),
                        scope=1, ops=cuts), 2)
    index = draw(st.integers(0, (len(bays) if bays else split - 1)))
    return BaySpec(split, index, front, left, shrink, extent, bays, kind == "module", mirrored,
                   draw(st.one_of(st.just(0.0), _mm(30))))


@st.composite
def _ref_on(draw: st.DrawFn, d: _Draft, measure: int, scope: int) -> Ref:
    """A position on one of the module's measures, as a board in `scope`
    names it: a side, a board's face, or a mix of two."""
    def plain() -> st.SearchStrategy[Ref]:
        names = [n for n in MEASURE if MEASURE[n] == measure]
        options: list[st.SearchStrategy[Ref]] = [
            st.builds(side, st.sampled_from(names) if scope == 0 else st.sampled_from(
                [n for n, m in d.bay_names.items() if m in names]),
                st.one_of(st.just(0.0), _mm(200), _by(-20, 20)), st.just(scope))]
        faces = [(i, n) for i in range(len(d.specs)) for n in MEASURE if MEASURE[d.module_name(i, n)] == measure]
        if faces:
            options.append(st.sampled_from(faces).flatmap(
                lambda f: st.builds(face, st.just(f[0]), st.just(f[1]), st.one_of(st.just(0.0), _by(-10, 10)))))
        return st.one_of(*options)
    if draw(st.integers(0, 3)) == 0:
        return mid(draw(plain()), draw(plain()), draw(_fraction()))
    return draw(plain())


@st.composite
def _extra(draw: st.DrawFn, d: _Draft, name: str) -> tuple[BoardSpec, int]:
    """A board placed at random in the module."""
    kind = draw(st.sampled_from(["side", "side", "face", "center", "pos"]))
    toward: str | None = None
    center = False
    if kind == "side":
        n = draw(st.sampled_from(list(MEASURE)))
        at, t = side(n, draw(st.one_of(st.just(0.0), _mm(300), _by(-20, 20)))), MEASURE[n]
    elif kind == "face" and d.specs:
        i = draw(st.integers(0, len(d.specs) - 1))
        n = draw(st.sampled_from([n for n in MEASURE if MEASURE[n] == d.t[i]] * 3 + list(MEASURE)))
        at = face(i, n, draw(st.one_of(st.just(0.0), _by(-5, 20))))
        t = MEASURE[d.module_name(i, n)]
    else:
        t = draw(st.integers(0, 2))
        at = draw(_ref_on(d, t, 0))
        center = kind == "center" or not d.specs
        if not center:
            toward = draw(st.sampled_from([n for n in MEASURE if MEASURE[n] == t]))
    limits: list[Ref] = []
    for _ in range(draw(st.integers(0, 4))):
        pick = draw(st.integers(0, 9))
        others = [i for i in range(len(d.specs)) if d.t0[i] != t]
        if pick < 3 and others:
            limits.append(part(draw(st.sampled_from(others)), draw(st.one_of(st.just(0.0), st.just(0.0), _by(-5, 10)))))
        elif pick == 3:
            limits.append(Ref("box", of=0))
        elif pick == 4 and d.specs:
            limits.append(part(draw(st.integers(0, len(d.specs) - 1))))     # perhaps parallel: refused
        else:
            limits.append(draw(_ref_on(d, draw(st.sampled_from([m for m in range(3) if m != t] + [t] * (pick == 5))), 0)))
    if draw(st.integers(0, 19)) == 0:
        # limits that leave it open where the board lies (refused): a board twice, a single
        # limit at the box's middle, a board centred in the box as the only one
        m = draw(st.sampled_from([m for m in range(3) if m != t]))
        others = [i for i in range(len(d.specs)) if d.t0[i] == m]
        options = [[mid(side(LOW[m]), side(HIGH[m]))]]
        if others:
            j = draw(st.sampled_from(others))
            options += [[part(j), part(j, draw(_by(-5, 5)))], [part(j)]]
            # (a board centred between two others, a divider halfway, lies across the middle)
            options += [[part(j)] for j in others if d.specs[j].center and d.specs[j].at.by == 0.5]
        limits = draw(st.sampled_from(options))
    shape: tuple[float, float] | None = None
    inset = draw(st.one_of(st.just(0.0), st.just(0.0), _mm(30)))
    if draw(st.integers(0, 9)) == 0:
        shape = (draw(sizes(20, 400)), draw(sizes(20, 400)))
        fit = draw(st.sampled_from(["fill", "fill", "one", "none", "as drawn"]))
        if fit == "fill":
            # between limits as far apart as the shape is wide, less its inset
            limits = []
            for m, size in zip([m for m in range(3) if m != t], shape):
                start = draw(st.one_of(st.just(0.0), _mm(200)))
                end = draw(st.sampled_from([LOW[m], HIGH[m]]))
                limits += [side(end, start), side(end, start + size + 2 * inset)]
        elif fit == "one":
            limits = [draw(_ref_on(d, m, 0)) for m in range(3) if m != t and draw(st.booleans())]
        elif fit == "none":
            limits = []
    return BoardSpec(name, draw(_thickness()), at, center, toward, tuple(limits), inset, shape,
                     draw(st.sampled_from([None, None, "inner", "outer", LOW[t], HIGH[t]])),
                     draw(st.sampled_from([None, None, *[EXTENT[m] for m in range(3) if m != t]]))), t


def _value(d: _Draft, i: int, measure: int) -> st.SearchStrategy[Value | None]:
    """A distance along board i's measure (in its scope's terms): a share
    of its extent, millimetres, its own face moved into it, or another
    board's face on that measure (lined up with it, as a shelf pin with
    its shelf)."""
    names = [n for n in MEASURE if MEASURE[n] == measure]
    fraction = st.builds(Value, _fraction(), st.one_of(st.just(0.0), _by(-5, 5)))
    mm = st.builds(Value, st.just(0.0), st.one_of(_mm(100), _by(0, 400)))
    own = st.builds(Value, st.just(0.0), st.just(0.0), st.builds(face, st.just(i), st.sampled_from(names),
                                                                    _by(-200, 0)))
    options = [fraction, fraction, mm, own, st.none()]
    if d.specs[i].scope == 0:
        others = [(j, n) for j in range(len(d.specs)) if j != i for n in MEASURE
                  if MEASURE[d.module_name(j, n)] == measure]
        if others:
            options.append(st.builds(Value, st.just(0.0), st.just(0.0), st.sampled_from(others).flatmap(
                lambda f: st.builds(face, st.just(f[0]), st.just(f[1]), st.one_of(st.just(0.0), _by(-20, 20))))))
    return st.one_of(*options)


@st.composite
def _at(draw: st.DrawFn, d: _Draft, i: int, edges: int, big: bool = True) -> At:
    t = d.t[i]
    plane = [m for m in range(3) if m != t]
    if big:
        name = draw(st.sampled_from(["inner", "outer", LOW[t], HIGH[t]]))
        chosen = draw(st.permutations(plane))[:edges]
    else:
        m = draw(st.sampled_from(plane))
        name = draw(st.sampled_from([LOW[m], HIGH[m]]))
        chosen = [n for n in plane if n != m][:edges]
    found: list[tuple[str, Value | None]] = []
    for m in chosen:
        found.append((draw(st.sampled_from([LOW[m], HIGH[m]])), draw(_value(d, i, m))))
    if not big and draw(st.booleans()):
        # across the thickness of a narrow face, from a big face (`side.front.right(50).inner(5)`)
        found.append((draw(st.sampled_from(["inner", "outer", LOW[t], HIGH[t]])),
                      Value(draw(st.sampled_from([0.25, 0.5, 0.75])), 0.0)))
    return At(name, tuple(found))


def _depths(t: float) -> st.SearchStrategy[Depth]:
    return st.one_of(st.builds(Depth, st.just("frac"), floats(0.1, 0.9)),
                     st.builds(Depth, st.just("mm"), sizes(1, max(1.0, t - 1))),
                     st.builds(Depth, st.just("to"), sizes(1, max(1.0, t - 1))),
                     st.builds(Depth, st.just("to"), sizes(t - 1, t + 5)), st.just(Depth("through")))


@st.composite
def _op(draw: st.DrawFn, d: _Draft, k: int) -> OpSpec:
    i = draw(st.integers(0, len(d.specs) - 1))
    t = d.t[i]
    plane = [m for m in range(3) if m != t]
    kind: Any = draw(st.sampled_from(["hole", "hole", "row", "pocket", "slot", "notch", "edge_hole", "cut_part",
                                      "corner"]))
    thick = d.specs[i].t
    if kind == "hole":
        return OpSpec(kind, i, draw(_at(d, i, draw(st.integers(0, 2)))), d=draw(sizes(2, 35)), depth=draw(_depths(thick)))
    if kind == "row":
        at = draw(_at(d, i, 2))
        m = MEASURE[at.edges[0][0]]
        start = face(i, LOW[m], -draw(_mm(80)))
        end = face(i, HIGH[m], -draw(_mm(80)))
        pitch = draw(st.one_of(st.sampled_from([32.0, 64.0, 100.0]), sizes(10, 300)))
        return OpSpec(kind, i, at, d=draw(sizes(2, 10)), depth=draw(_depths(thick)),
                      row=(start, end, pitch if draw(st.booleans()) else 0.0, draw(st.integers(1, 6))))
    if kind in ("pocket", "notch"):
        size = (draw(sizes(5, 200)), draw(sizes(5, 200)))
        m1, m2 = plane
        clip = None
        if draw(st.integers(0, 2)) == 0:
            clip = (draw(st.sampled_from([LOW[m1], HIGH[m1]])), draw(floats(0.1, 0.9)) * size[1],
                    draw(st.sampled_from([LOW[m2], HIGH[m2]])), draw(floats(0.1, 0.9)) * size[0])
        if kind == "notch":
            corner = ((draw(st.sampled_from([LOW[m1], HIGH[m1]])), None), (draw(st.sampled_from([LOW[m2], HIGH[m2]])), None))
            at = At(draw(st.sampled_from(["inner", "outer", LOW[t], HIGH[t]])), tuple(draw(st.permutations(corner))))
            return OpSpec(kind, i, at, size=size, name=f"notch{k}", clip=clip)
        return OpSpec(kind, i, draw(_at(d, i, draw(st.integers(0, 2)))), size=size, depth=draw(_depths(thick)),
                      clip=clip)
    if kind == "slot":
        return OpSpec(kind, i, draw(_at(d, i, draw(st.integers(0, 2)))), d=draw(sizes(1, 30)),
                      size=(draw(sizes(0.5, 200)), 0.0), depth=draw(_depths(thick)), along=draw(st.integers(0, 1)))
    if kind == "edge_hole":
        return OpSpec(kind, i, draw(_at(d, i, 1, big=False)), d=draw(sizes(2, max(2.0, thick - 1))),
                      depth=Depth("mm", draw(sizes(3, 60))))
    if kind == "corner":
        m1, m2 = plane
        a, c = draw(st.sampled_from([LOW[m1], HIGH[m1]])), draw(st.sampled_from([LOW[m2], HIGH[m2]]))
        kind = draw(st.sampled_from(["chamfer_edge", "chamfer_corner", "fillet"]))
        if kind == "chamfer_edge":
            a = draw(st.sampled_from([LOW[t], HIGH[t], "inner", "outer"]))
        size = draw(st.one_of(st.just(1.0), sizes(0.5, 30))) if kind != "chamfer_edge" else draw(sizes(0.5, thick))
        return OpSpec(kind, i, At(a, ((c, None),)), size=(size, 0.0))
    return OpSpec(kind, i, other=draw(st.integers(0, len(d.specs) - 1)))


@st.composite
def placement_cases(draw: st.DrawFn) -> PlacementCase:
    size = (draw(st.one_of(st.just(600.0), sizes(150, 1600))), draw(st.one_of(st.just(400.0), sizes(100, 800))),
            draw(st.one_of(st.just(720.0), sizes(100, 2000))))
    d = _Draft()
    draw(_carcass(d))
    first_bay = len(d.specs)
    bay = draw(_bay(d)) if draw(st.integers(0, 9)) < 4 else None
    first_extra = len(d.specs)
    for k in range(draw(st.integers(0, 3))):
        d.add(*draw(_extra(d, f"extra{k}")))
    ops = tuple(draw(_op(d, k)) for k in range(draw(st.integers(0, 6))))
    boards = tuple(replace(spec, machine=draw(st.sampled_from([None, None, None, "inner", "outer", LOW[t], HIGH[t]])))
                   for spec, t in zip(d.specs, d.t))
    return PlacementCase(
        kind=draw(st.sampled_from(["module", "cabinet"])), size=size, boards=boards, first_bay=first_bay,
        first_extra=first_extra, bay=bay, ops=ops, mirrored=draw(st.booleans()), front=draw(st.integers(0, 3)),
        origin=draw(_origin()), turn=draw(st.integers(1, 3)), origin2=draw(_origin()),
        frame=draw(st.integers(1, len(WORLD_FRAMES) - 1)), flip=draw(st.booleans()), origin3=draw(_origin()),
        seed=draw(st.integers(0, 2 ** 16)))


# -- building -----------------------------------------------------------------------------------

@dataclass(frozen=True)
class How:
    """One way to build a case: the world frame (`WORLD_FRAMES`), the
    place, the side a cabinet faces (`FRONTS`), whether the module's
    mirroring is flipped, and the spelling's seed (None: as written)."""
    frame: int
    origin: tuple[float, float, float]
    front: int
    flip: bool
    seed: int | None


@dataclass
class Built:
    """A case as one way built it: the module, the bay's scope, the boxes
    (the module's, the bay's, the box in it), the boards (None where
    refused or left out), the operations each spec made (None where
    refused), and the paths refused."""
    case: PlacementCase
    how: How
    rng: random.Random | None
    module: Scope | None = None
    bay: Scope | None = None
    boxes: list[Box | None] = field(default_factory=lambda: [None, None, None])
    boards: list[Board | None] = field(default_factory=list[Board | None])
    made: dict[str, tuple[int, int] | None] = field(default_factory=dict[str, tuple[int, int] | None])
    refused: list[str] = field(default_factory=list[str])
    #: The board each entry of `refused` refuses, by its index there: the
    #: path refused may be another board's (a shelf refused because the
    #: dado it names is missing names the side).
    refused_boards: dict[int, int] = field(default_factory=dict[int, int])
    #: Every board made, refused or not.
    made_boards: list[Board | None] = field(default_factory=list[Board | None])
    #: Per board, the limits as given; per operation, where its anchor puts
    #: it and how deep it goes (the key, its index in the board's
    #: operations, `Where`, mm and through); per row, its ends, pitch,
    #: count and the positions spread; for the promises.
    given: dict[int, list[object]] = field(default_factory=dict[int, list[object]])
    meant: list[tuple[str, int, Where, tuple[float, bool]]] = field(
        default_factory=list[tuple[str, int, Where, tuple[float, bool]]])
    rows: dict[str, tuple[float, float, float, int, list[float]]] = field(
        default_factory=dict[str, tuple[float, float, float, int, list[float]]])
    problems: list[str] = field(default_factory=list[str])
    #: Why each board was refused, for reading, and by board.
    why: list[str] = field(default_factory=list[str])
    reasons: dict[int, str] = field(default_factory=dict[int, str])
    #: The outline's bounds of each board made of a shape, as placed.
    placed: dict[int, tuple[float, float, float, float]] = field(
        default_factory=dict[int, tuple[float, float, float, float]])

    def pick(self, n: int) -> int:
        """A spelling of `n`: the first as written, any another way."""
        return self.rng.randrange(n) if self.rng is not None and n > 1 else 0

    def shuffled[T](self, items: Sequence[T]) -> list[T]:
        out = list(items)
        if self.rng is not None:
            self.rng.shuffle(out)
        return out

    def scope_of(self, i: int) -> Scope:
        s = self.module if self.case.boards[i].scope == 0 else self.bay
        assert s is not None
        return s


def _world_box(case: PlacementCase, how: How) -> Box:
    """The module's box in world terms, its own width, depth and height
    along the axes it faces."""
    w, d, h = case.size
    if case.kind == "module" or FRONTS[how.front] in ("front", "back"):
        return Box.from_size(width=w, depth=d, height=h, origin=how.origin)
    return Box.from_size(width=d, depth=w, height=h, origin=how.origin)


def build(case: PlacementCase, how: How, name: str = "m") -> Built:
    """The case built one way, in the current build; boards and operations
    the language refuses are left out (and listed in `refused`)."""
    front, left, top = WORLD_FRAMES[how.frame]
    set_frame(Frame(front=front, left=left, top=top, aliases=ALIASES))
    b = Built(case, how, random.Random(how.seed) if how.seed is not None else None)
    b.boards = [None] * len(case.boards)
    b.made_boards = [None] * len(case.boards)
    box = _world_box(case, how)
    if b.pick(2):
        box = Box.from_sides(front=box.front, back=box.back, left=box.left, right=box.right, top=box.top,
                             bottom=box.bottom)
    mirrored = case.mirrored != how.flip
    if case.kind == "module":
        m = module(name, box, mirrored=mirrored)
    else:
        facing = box.side(FRONTS[how.front])
        m = module(name, box, front=[facing, facing.outward][b.pick(2)], mirrored=mirrored)
    b.module = m
    b.boxes[0] = m.box
    with m:
        check(no_interference, inside_box)
        _place_all(b, range(case.first_bay))
        if case.bay is not None:
            _make_bay(b, case.bay)
    if case.bay is not None and b.bay is not None:
        _place_all(b, range(case.first_bay, case.first_extra))
    _place_all(b, range(case.first_extra, len(case.boards)))
    _leave_out_dependents(b)
    for k in _op_order(b):
        _make_op(b, f"op{k}", case.ops[k])
    return b


def _op_order(b: Built) -> list[int]:
    """The case's operations in their order, or another in which each
    comes after the ones before it on the boards it touches (a board cut
    by another touches both)."""
    ops = b.case.ops

    def touches(op: OpSpec) -> set[int]:
        return {op.board, op.other} if op.kind == "cut_part" else {op.board}
    todo = list(range(len(ops)))
    order: list[int] = []
    while todo:
        ready = [k for k in todo if not any(j < k and touches(ops[j]) & touches(ops[k]) for j in todo)]
        k = ready[b.pick(len(ready))]
        todo.remove(k)
        order.append(k)
    return order


def _place_all(b: Built, indexes: range) -> None:
    """Places the boards, in the case's order, or another order in which
    each board comes after those it names; then resolves them, in that
    order or another."""
    todo = list(indexes)
    order: list[int] = []
    while todo:
        ready = [i for i in todo if not (deps(b.case.boards[i]) & set(todo))]
        i = ready[b.pick(len(ready))] if ready else todo[0]
        todo.remove(i)
        order.append(i)
    for i in order:
        _place(b, i)
    for i in b.shuffled(order):
        x = b.boards[i]
        if x is None:
            continue
        try:
            x.box()
            x.show_face                 # ("inner" or "outer" of a board across the middle is refused here)
            x.machine_face
            if b.case.boards[i].shape is not None:
                b.placed[i] = x.outline.bounds
        except LangError as e:
            _refuse(b, i, e)


def _leave_out_dependents(b: Built) -> None:
    """Leaves out every board that names one left out, made before that one
    was refused or not, and drops its own refusal: in another order it
    would not have been made, so what is built does not hang on the order
    the refusals came in. Its refusal is found by the board, not by the
    path the error names [found 2026-10-15: a shelf refused for a side's
    missing dado kept its refusal, under the side's path, where the back it
    stands on was refused later, and had none where `machine()` resolved
    the back early and refused it before the shelf was made]."""
    gone = {i for i, x in enumerate(b.boards) if x is None}
    grown = True
    while grown:
        grown = False
        for j, spec in enumerate(b.case.boards):
            x = b.boards[j]
            if x is not None and deps(spec) & gone:
                if x.name in _scope(x).parts:
                    del _scope(x).parts[x.name]
                b.boards[j] = None
                gone.add(j)
                grown = True
    index = {x.path: i for i, x in enumerate(b.made_boards) if x is not None}
    kept = [(k, p) for k, p in enumerate(b.refused)
            if (i := b.refused_boards.get(k, index.get(p))) is None or not deps(b.case.boards[i]) & gone]
    b.refused_boards = {n: b.refused_boards[k] for n, (k, _) in enumerate(kept) if k in b.refused_boards}
    b.refused = [p for _, p in kept]


def _refuse(b: Built, i: int, e: LangError) -> None:
    """Leaves board i out: refused itself, or for a board it names."""
    x = b.boards[i]
    if x is not None and x.name in _scope(x).parts:
        del _scope(x).parts[x.name]
    b.boards[i] = None
    b.refused.append(e.path or f"{b.case.boards[i].name} (no path): {e}")
    b.refused_boards[len(b.refused) - 1] = i
    b.why.append(str(e))
    b.reasons.setdefault(i, str(e))


def _make_bay(b: Built, bay: BaySpec) -> None:
    m = b.module
    assert m is not None
    try:
        space = m.interior
    except LangError as e:
        b.refused.append("the interior")
        b.why.append(str(e))
        return
    try:
        bays = space.split(bay.extent, list(bay.sizes) if bay.sizes else bay.split, gap=bay.gap)
        space = bays[bay.index]
    except (LangError, IndexError) as e:
        b.refused.append("the bay")
        b.why.append(str(e))
        return
    if bay.module:
        s = module("bay", space, mirrored=bay.mirrored)
    elif bay.front is None:
        s = scope("bay", space)
    else:
        facing = space.side(bay.front)
        up = m.frame.direction("top")
        own = Frame.derived(facing.outward, up)
        mirrored = own.direction("left") != m.frame.direction(bay.left)
        s = module("bay", space, front=facing, mirrored=mirrored)
    b.bay = s
    b.boxes[1] = s.box
    f, k, lft, rgt, tp, bt = bay.shrink
    own = s.require_box("bay")
    spellings: list[Callable[[], Box]] = [
        lambda: own.shrunk(front=f, back=k, left=lft, right=rgt, top=tp, bottom=bt),
        lambda: own.grown(front=-f, back=-k, left=-lft, right=-rgt, top=-tp, bottom=-bt),
        lambda: own.with_sides(front=own.front.into(f), back=own.back.into(k), left=own.left.into(lft),
                               right=own.right.into(rgt), top=own.top.into(tp), bottom=own.bottom.into(bt))]
    try:
        b.boxes[2] = spellings[b.pick(3)]()
    except LangError as e:
        b.refused.append("the box in the bay")
        b.why.append(str(e))


# -- references, spelt one way or another ---------------------------------------------------------

def _scope(x: Board) -> Scope:
    """The scope a board is in (always one here, never the root)."""
    assert isinstance(x.scope, Scope)
    return x.scope


def _side_of(b: Built, r: Ref) -> Side:
    if r.of == 2:
        box = b.boxes[2]
        assert box is not None
        return box.side(r.name)
    s = b.module if r.of == 0 else b.bay
    assert s is not None
    aliases = [a for a, n in ALIASES.items() if n == r.name and s.frame.is_direction(a)]
    return s.side(([r.name] + aliases)[b.pick(1 + len(aliases))])


def _board(b: Built, i: int) -> Board:
    x = b.boards[i]
    if x is None:
        raise _Missing(i)
    return x


class _Missing(Exception):
    """A board named was refused or left out."""

    def __init__(self, i: int):
        self.index = i


def _limit(b: Built, r: Ref) -> Any:
    """A `between()` limit."""
    if r.kind == "part":
        x = _board(b, r.of)
        if r.by == 0:
            return [x, x.into(0), x.gap(0)][b.pick(3)]
        return [x.into(r.by), x.gap(-r.by)][b.pick(2)]
    if r.kind == "box":
        box = b.boxes[r.of]
        assert box is not None
        return box
    return _position(b, r)


def _position(b: Built, r: Ref) -> Any:
    """A position: a Side, a Face, a Pos."""
    if r.kind == "side":
        s = _side_of(b, r)
        if r.by == 0:
            return [s, s.position, s.gap(0), s.into(0)][b.pick(4)]
        # (a side plus a length is refused, syntax.md item 1: `_directed_promises`)
        return [s.into(r.by), s.gap(-r.by), s.into(2 * r.by).gap(r.by), s.gap(r.by).into(2 * r.by)][b.pick(4)]
    if r.kind == "face":
        f = _board(b, r.of).face(r.name)
        sign = f.direction.sign
        if r.by == 0:
            return [f, f.position, f.into(0), f.gap(0)][b.pick(4)]
        # (moved again, a face's side keeps the face's in and out [Florian, 2026-10-15]; a bare position
        # keeps its arithmetic)
        return [f.gap(r.by), f.into(-r.by), f.position + sign * r.by, f.gap(2 * r.by).into(r.by),
                f.into(r.by).gap(2 * r.by)][b.pick(5)]
    if r.kind == "op":
        name, edge = r.name.split(".")
        x = _board(b, r.of)
        if edge == "floor":
            return [x.op(name).floor, getattr(x, name).floor][b.pick(2)]
        return [x.op(name).side(edge), getattr(getattr(x, name), edge)][b.pick(2)]
    if r.kind == "mid":
        assert r.a is not None and r.b is not None
        a, c, f = _position(b, r.a), _position(b, r.b), r.by
        # (a length goes on a bare position: on a side or a face it is refused, syntax.md item 1)
        pa, pc = as_pos(a), as_pos(c)
        if f == 0.5:
            spellings: list[Callable[[], Any]] = [lambda: (a + c) / 2, lambda: pa + (c - a) / 2, lambda: (c + a) / 2,
                                                  lambda: 0.5 * a + 0.5 * c, lambda: (a + c) * 0.5,
                                                  lambda: a + c - c + (c - a) / 2]
            if (r.a.kind == r.b.kind == "side" and r.a.of == r.b.of and r.a.by == r.b.by == 0
                    and OPPOSITE[r.a.name] == r.b.name):
                box, extent = b.boxes[r.a.of], EXTENT[MEASURE[r.a.name]]
                assert box is not None
                spellings.append(lambda: box.center(extent))
        else:
            spellings = [lambda: pa + (c - a) * f, lambda: (1 - f) * a + f * c, lambda: pc + (a - c) * (1 - f),
                         lambda: c + a - c + (c - a) * f]
        return spellings[b.pick(len(spellings))]()
    raise AssertionError(r.kind)


def _place(b: Built, i: int) -> None:
    """Makes board i and places it, its modifiers in the case's order or
    another; leaves it out when it names a board left out, or when the
    language refuses it."""
    spec = b.case.boards[i]
    if any(b.boards[j] is None for j in deps(spec)) or any(b.boxes[j] is None for j in deps(spec, boxes=True)):
        return
    sc = b.scope_of(i)
    with sc:
        try:
            shape = _shape(b, sc, spec)
        except LangError as e:
            b.refused.append(f"{sc.path}.{spec.name}: {e}")
            return
        x = board(spec.name, sheet_material("birch", t=spec.t), shape)
        b.boards[i] = b.made_boards[i] = x
        try:
            steps: list[Callable[[], object]] = [lambda: _on(b, x, spec)]
            limits: list[Any] = []
            for r in spec.limits:
                limit = _limit(b, r)
                if isinstance(limit, Box) and b.pick(2):
                    t = _axis_of(b, spec.at)
                    limits += [limit.side(n) for n in MEASURE if limit.side(n).axis != t]
                else:
                    limits.append(limit)
            b.given[i] = limits
            if limits or b.pick(2):
                steps.append(lambda: x.between(*b.shuffled(limits)))
            if spec.inset or b.pick(2):
                steps.append(lambda: x.inset(spec.inset))
            if spec.grain is not None:
                steps.append(lambda: _grain(b, x, spec.grain or ""))
            late: list[Callable[[], object]] = []
            if spec.show in ("inner", "outer") and b.pick(2):
                late.append(lambda: x.show(x.face(spec.show or "")))      # (it resolves the board: last)
            elif spec.show is not None:
                steps.append(lambda: _big_face(b, x, spec.show or "", x.show))
            after: list[Callable[[], object]] = []
            if spec.machine is not None:
                # at any time: among the placement's modifiers, last, or after the operations
                if spec.machine in ("inner", "outer") and b.pick(2):
                    [late, after][b.pick(2)].append(lambda: x.machine(x.face(spec.machine or "")))  # (it resolves)
                else:
                    [steps, late, after][b.pick(3)].append(lambda: _big_face(b, x, spec.machine or "", x.machine))
            for step in b.shuffled(steps) + late:
                step()
            if spec.machine in ("inner", "outer"):
                # a board across the middle is refused here, before its operations, however machine() was given
                x.face(spec.machine)
            if spec.ops:
                x.box()
                for j, op in enumerate(spec.ops):
                    _make_op(b, f"{i}.{j}", op)
            for step in after:
                step()
        except LangError as e:
            _refuse(b, i, e)


def _shape(b: Built, sc: Scope, spec: BoardSpec) -> Any:
    """The rect a board is made of, its extents named in its scope's terms."""
    if spec.shape is None:
        return None
    t = MEASURE[sc.frame.direction_of(_axis_of(b, spec.at), 1).name]
    m1, m2 = [k for k in range(3) if k != t]
    return rect(**{EXTENT[m1]: spec.shape[0], EXTENT[m2]: spec.shape[1]})


def _axis_of(b: Built, r: Ref) -> Axis:
    if r.kind == "side":
        return _side_of(b, r).axis
    if r.kind == "face":
        return _board(b, r.of).face(r.name).axis
    if r.kind == "op":
        name, edge = r.name.split(".")
        return as_pos(getattr(getattr(_board(b, r.of), name), edge)).axis
    assert r.a is not None
    return _axis_of(b, r.a)


def _on(b: Built, x: Board, spec: BoardSpec) -> None:
    r = spec.at
    if spec.center:
        x.center(_position(b, r))
        return
    if spec.toward is not None:
        toward = _scope(x).side(spec.toward)
        x.on(_position(b, r), toward=[toward, toward.outward][b.pick(2)])
        return
    if r.kind == "side":
        s = _side_of(b, r)
        sign = s.inward.sign
        opposite = _side_of(b, Ref("side", OPPOSITE[r.name], r.of))
        if r.by == 0:
            [lambda: x.on(s), lambda: x.on(s.position, toward=opposite), lambda: x.on(s.into(0), toward=s.inward),
             lambda: x.on(s.into(0))][b.pick(4)]()
        else:
            # (a side moved into or out of its box is a side: no toward= needed)
            [lambda: x.on(s.position + sign * r.by, toward=s.inward), lambda: x.on(s.into(r.by), toward=opposite),
             lambda: x.on(s.into(r.by), toward=s.inward), lambda: x.on(s.into(r.by)), lambda: x.on(s.gap(-r.by)),
             lambda: x.on(s.into(2 * r.by).gap(r.by))][b.pick(6)]()
        return
    if r.kind == "face":
        f = _board(b, r.of).face(r.name)
        if r.by == 0:
            [lambda: x.on(f), lambda: x.on(f.position, toward=f.direction), lambda: x.on(f.gap(0)),
             lambda: x.on(f.into(0))][b.pick(4)]()
        else:
            # (a face moved by gap() or into() keeps its side: no toward= needed)
            [lambda: x.on(f.gap(r.by), toward=f.direction),
             lambda: x.on(f.position + f.direction.sign * r.by, toward=f.direction), lambda: x.on(f.gap(r.by)),
             lambda: x.on(f.into(-r.by)), lambda: x.on(f.gap(2 * r.by).into(r.by))][b.pick(5)]()
        return
    raise AssertionError(r.kind)


def _grain(b: Built, x: Board, extent: str) -> None:
    m = [n for n in EXTENT].index(extent)  # pyright: ignore[reportArgumentType]
    s = _scope(x).side(LOW[m])
    [lambda: x.grain(EXTENT[m]), lambda: x.grain(s), lambda: x.grain(s.outward), lambda: x.grain(x.face(HIGH[m]))][
        b.pick(4)]()


def _big_face(b: Built, x: Board, name: str, give: Callable[[Any], object]) -> None:
    """`show()` or `machine()` (`give`) given a big face, named one of the
    ways they take that leave the placement open: inner or outer, the
    board's own face, a direction, its scope's side, the module's side."""
    if name in ("inner", "outer"):
        give("inner" if name == "inner" else "outer")
        return
    s = _scope(x).side(name)
    m = b.module
    assert m is not None
    module_side = m.side(m.frame.name_of(s.outward))         # (an enclosing box's side, named its own way)
    [lambda: give(x.face(name)), lambda: give(s.outward), lambda: give(s), lambda: give(module_side)][b.pick(4)]()


# -- operations ---------------------------------------------------------------------------------

def _make_op(b: Built, key: str, op: OpSpec) -> None:
    """Makes an operation; a refused one (a row: all its holes) is left
    out, and must have changed nothing."""
    x = b.boards[op.board]
    if x is None or (op.kind == "cut_part" and b.boards[op.other] is None):
        b.made[key] = None
        return
    before = _state(x)
    saved = x._state()  # pyright: ignore[reportPrivateUsage]
    n = len(x.ops)
    try:
        with _scope(x):
            _do(b, key, x, op)
    except (LangError, _Missing) as e:
        if op.kind == "row":
            x._restore(saved)  # pyright: ignore[reportPrivateUsage]
        elif _state(x) != before:
            b.problems.append(f"a refused {op.kind} changed {x.path}: {e}")
        b.made[key] = None
        b.meant = [m for m in b.meant if m[0] != key]
        b.rows.pop(key, None)
        return
    b.made[key] = (n, len(x.ops))


def _state(x: Board) -> tuple[str, list[Op], list[str]]:
    return x.outline.geometry.wkt, list(x.ops), [op.name or "" for op in x.ops if not isinstance(op, (Chamfer, EdgeOp))]


def _do(b: Built, key: str, x: Board, op: OpSpec) -> None:
    if op.kind == "cut_part":
        other = _board(b, op.other)
        # (its box for it where the outline fills the box: no cut has taken a side's end away)
        ob, ub = other.outline.bounds, other.box()
        fills = abs(other.outline.area - other.outline.width * other.outline.height) < 1e-6 and all(
            abs(p - q) < 1e-9 for p, q in zip(ob, (ub.lo[other.u_axis], ub.lo[other.v_axis], ub.hi[other.u_axis],
                                                   ub.hi[other.v_axis])))
        x.cut(other.box() if fills and other.t_axis != x.t_axis and b.pick(2) else other)
        return
    f = _face(b, x, op.at.face)
    if op.kind in ("chamfer_edge", "chamfer_corner", "fillet"):
        name = op.at.edges[0][0]
        g = x.face(name)
        edge = [lambda: getattr(f, name), lambda: f.edge(g), lambda: g.edge(f)][b.pick(3)]()
        if op.kind == "fillet":
            x.fillet(edge, op.size[0])
        else:
            x.chamfer(edge, op.size[0])
        return
    if op.kind == "row":
        assert op.row is not None
        start, end, pitch, count = op.row
        ends = [_position(b, start), _position(b, end)]
        if b.pick(2):
            ends.reverse()
        rows = spread(ends[0], ends[1], pitch=pitch) if pitch > 0 else spread(ends[0], ends[1], count=count)
        b.rows[key] = (as_pos(ends[0]).value, as_pos(ends[1]).value, pitch, count, [p.value for p in rows])
        depth, want = _depth(b, x, f, op.depth)
        first = op.at.edges[0][0]
        for p in rows:
            at, where = _anchor(b, x, f, ((first, p), *op.at.edges[1:]), {}, hole=True)
            x.hole(op.d, at=at, depth=depth)
            b.meant.append((key, len(x.ops) - 1, where, want))
        return
    if op.kind == "slot":
        t = MEASURE[x.scope.frame.direction_of(x.t_axis, 1).name]
        m = [k for k in range(3) if k != t][op.along]
        sc = _scope(x)
        along: Any = [lambda: EXTENT[m], lambda: sc.side(LOW[m]), lambda: sc.side(HIGH[m]),
                      lambda: x.face(LOW[m])][b.pick(4)]()
        at, where = _anchor(b, x, f, op.at.edges, {}, hole=True)
        depth, want = _depth(b, x, f, op.depth)
        x.slot(op.d, at=at, centers=op.size[0], along=along, depth=depth)
        b.meant.append((key, len(x.ops) - 1, where, want))
        return
    sizes_: dict[Axis, float] = {}
    shape: Any = None
    if op.kind in ("pocket", "notch"):
        t = MEASURE[x.scope.frame.direction_of(x.t_axis, 1).name]
        m1, m2 = [k for k in range(3) if k != t]
        shape = rect(**{EXTENT[m1]: op.size[0], EXTENT[m2]: op.size[1]})
        if op.clip is not None:
            a, k, c, n = op.clip
            shape = shape.clip(**{a: k, c: n})
        sizes_ = {_scope(x).side(LOW[m1]).axis: op.size[0], _scope(x).side(LOW[m2]).axis: op.size[1]}
    at, where = _anchor(b, x, f, op.at.edges, sizes_, hole=op.kind in ("hole", "edge_hole"))
    if op.kind == "notch":
        x.cut(shape, at=at, name=op.name)
        return
    depth, want = _depth(b, x, f, op.depth)
    if op.kind == "pocket":
        x.pocket(shape, at=at, depth=depth, name=op.name)
    else:
        x.hole(op.d, at=at, depth=depth)
    b.meant.append((key, len(x.ops) - 1, where, want))


def _face(b: Built, x: Board, name: str) -> Face:
    """A face of the board, by its direction, "inner" or "outer", spelt one
    way or another (`x.top`, `x.face("top")`, `x.inner` when it is that)."""
    if name in ("inner", "outer"):
        return [lambda: x.face(name), lambda: x.inner if name == "inner" else x.outer][b.pick(2)]()
    f = x.face(name)
    spellings: list[Callable[[], Face]] = [lambda: f, lambda: getattr(x, name)]
    for alias in (a for a, n in ALIASES.items() if n == name and _scope(x).frame.is_direction(a)):
        spellings.append(lambda alias=alias: x.face(alias))
    for which in ("inner", "outer"):
        try:
            if x.face(which).direction == f.direction:
                spellings.append(lambda which=which: x.face(which))
        except LangError:
            pass
    return spellings[b.pick(len(spellings))]()



def _anchor(b: Built, x: Board, f: Face, edges: Sequence[tuple[str, Value | Pos | None]], size: dict[Axis, float],
            hole: bool) -> tuple[Any, Where]:
    """The anchor `edges` name on face `f`, spelt one way or another (the
    edges in another order, a distance from the opposite edge, a position
    for a distance), and where it puts what is placed: per in-plane axis
    of the face, the range a shape `size` along it covers (a point for a
    hole)."""
    box = x.box()
    order = list(edges)
    if len(order) == 2 and b.pick(2):
        order.reverse()
    target: Any = f
    where: Where = {}
    for name, value in order:
        e = x.face(name)
        axis = e.axis
        extent = box.hi[axis] - box.lo[axis]
        s = size.get(axis, 0.0)
        inward = -e.direction.sign
        here: Any = target
        if value is None:
            coord = e.value
            options: list[Callable[[], Any]] = [lambda: getattr(here, name)]
            if hole:
                options.append(lambda: getattr(here, OPPOSITE[name])(extent))
        elif isinstance(value, Value) and value.ref is None:
            v = value.frac * extent + value.mm
            coord = e.value + inward * v
            options = [lambda: getattr(here, name)(v), lambda: getattr(here, OPPOSITE[name])(extent - v - s)]
            if hole:
                options += [lambda: getattr(here, name)(e.into(v)), lambda: getattr(here, OPPOSITE[name])(e.into(v))]
        else:
            pos = as_pos(_position(b, value.ref) if isinstance(value, Value) and value.ref is not None else value)
            coord = pos.value
            options = [lambda: getattr(here, name)(pos)]
            if hole:
                options.append(lambda: getattr(here, OPPOSITE[name])(pos))
        target = options[b.pick(len(options))]()
        lo, hi = sorted((coord, coord + inward * s))
        where[axis] = (lo, hi)
    for axis in x.face_axes(f):
        if axis not in where:
            c, s = (box.lo[axis] + box.hi[axis]) / 2, size.get(axis, 0.0)
            where[axis] = (c - s / 2, c + s / 2)
    if isinstance(target, Face):
        target = target.center
    return target, where


def _depth(b: Built, x: Board, f: Face, depth: Depth) -> tuple[Any, tuple[float, bool]]:
    """A depth spelt one way or another (a number or `to()` the other face,
    by its direction or as inner or outer), and what it means: mm and
    whether through."""
    box = x.box()
    extent = box.hi[f.axis] - box.lo[f.axis]
    other = x.face(-f.direction)
    names: list[Any] = [other]
    for which in ("inner", "outer"):
        try:
            if x.face(which).direction == other.direction:
                names.append(which)
        except LangError:
            pass
    toward = names[b.pick(len(names))]
    if depth.kind in ("mm", "frac"):
        v = depth.value if depth.kind == "mm" else depth.value * extent
        options: list[Any] = [v] + ([to(toward, leave=extent - v)] if v < extent - 1e-6 else [])
        return options[b.pick(len(options))], (v, False)
    if depth.kind == "to":
        return [to(toward, leave=depth.value), extent - depth.value][b.pick(2)], (extent - depth.value, False)
    return [through, to(toward)][b.pick(2)], (extent, True)


# -- the summary, in the module's own terms -------------------------------------------------------------

class _Local:
    """The module's measures: inward from its front, left and bottom
    sides; outlines in the two measures of their plane, in that order."""

    def __init__(self, m: Scope):
        self.frame = m.frame
        self.sides = [m.side(n) for n in LOW]
        self.of_axis: dict[Axis, int] = {s.axis: k for k, s in enumerate(self.sides)}

    def coord(self, axis: Axis, value: float) -> float:
        s = self.sides[self.of_axis[axis]]
        return s.inward.sign * (value - s.value)

    def span(self, axis: Axis, lo: float, hi: float) -> tuple[float, float]:
        a, c = self.coord(axis, lo), self.coord(axis, hi)
        return (min(a, c), max(a, c))

    def name(self, world_name: str) -> str:
        return self.frame.name_of(world_frame().direction(world_name))

    def edge(self, what: str) -> str:
        """A chamfer's target: an edge by two world names, or a name."""
        parts = what.split(".")
        if len(parts) == 2 and all(world_frame().is_direction(p) for p in parts):
            return ".".join(self.name(p) for p in parts)
        return what

    def plane(self, g: BaseGeometry, u: Axis, v: Axis) -> BaseGeometry:
        iu, iv = self.of_axis[u], self.of_axis[v]
        su, sv = self.sides[iu], self.sides[iv]
        a, c = su.inward.sign, sv.inward.sign
        if iu < iv:
            return affinity.affine_transform(g, [a, 0, 0, c, -a * su.value, -c * sv.value])
        return affinity.affine_transform(g, [0, c, a, 0, -c * sv.value, -a * su.value])

    def point(self, values: dict[Axis, float]) -> tuple[float, ...]:
        return tuple(self.coord(a, values[a]) for a in sorted(values, key=lambda a: self.of_axis[a]))


def _summary(b: Built) -> dict[str, Any]:
    assert b.module is not None
    loc = _Local(b.module)
    out: dict[str, Any] = {"refused": sorted(set(b.refused))}
    for x in b.boards:
        if x is None:
            continue
        bx = x.box()
        layout = x.to_layout()
        show, machine = loc.name(layout["show"]), loc.name(layout["machine"])
        grain = layout["grain"]
        out[x.path] = ("board", loc.of_axis[x.t_axis], tuple(loc.span(a, bx.lo[a], bx.hi[a]) for a in
                                                              sorted(AXES, key=lambda a: loc.of_axis[a])),
                       loc.plane(x.outline.geometry, x.u_axis, x.v_axis), show, machine,
                       None if grain is None else loc.of_axis[as_axis(grain)],
                       tuple(sorted((loc.name(k), tuple(v)) for k, v in layout["faces"].items())))
    for key, made in b.made.items():
        op = _spec_of(b.case, key)
        x = b.boards[op.board]
        if made is None or x is None:
            out[f"op {key}"] = None
            continue
        items = [_op_summary(loc, x, o) for o in x.ops[made[0]:made[1]]]
        out[f"op {key}"] = sorted(items, key=_rounded) if op.kind == "row" else items
    problems: list[str] = []
    for p in build_layout()["problems"]:
        one, _, two = p.partition(" overlaps ")
        head, _, sides = p.partition(" box: ")          # (inside_box lists the sides by world axis)
        problems.append(" overlaps ".join(sorted((one, two))) if two else
                        f"{head} box: {', '.join(sorted(sides.split(', ')))}" if sides else p)
    out["problems"] = sorted(problems)
    return out


def _rounded(v: Any) -> str:
    """A text to sort by, alike for values within rounding."""
    if isinstance(v, float):
        return f"{round(v, 5) + 0.0:.5f}"
    if isinstance(v, (tuple, list)):
        return "(" + ", ".join(_rounded(p) for p in v) + ")"
    return repr(v)


def _spec_of(case: PlacementCase, key: str) -> OpSpec:
    if key.startswith("op"):
        return case.ops[int(key[2:])]
    i, j = key.split(".")
    return case.boards[int(i)].ops[int(j)]


def _op_summary(loc: _Local, x: Board, op: Op) -> tuple[Any, ...]:
    u, v = x.u_axis, x.v_axis
    if isinstance(op, Hole):
        return ("hole", loc.name(op.face), loc.point({u: op.u, v: op.v}), op.d, op.depth, op.through, op.chamfer)
    if isinstance(op, Pocket):
        line = None if op.slot is None else (
            tuple(sorted((loc.point({u: p[0], v: p[1]}) for p in (op.slot.start, op.slot.end)), key=_rounded)),
            op.slot.width)
        return ("pocket", loc.name(op.face), loc.plane(op.shape.geometry, u, v), op.depth, line)
    if isinstance(op, Cut):
        return ("cut", op.name, loc.plane(op.shape.geometry, u, v))
    if isinstance(op, EdgeOp):
        s_axis, t_axis = x.face_axes(x.face(world_frame().direction(op.face)))
        inner = op.op
        if isinstance(inner, Hole):
            return ("edge hole", loc.name(op.face), loc.point({s_axis: op.s, t_axis: op.t}), inner.d, inner.depth,
                    inner.through, op.offset)
        return ("edge pocket", loc.name(op.face), loc.plane(affinity.translate(inner.shape.geometry, op.s, op.t),
                                                             s_axis, t_axis), inner.depth, op.offset)
    if isinstance(op, Chamfer):
        what = loc.edge(op.what)
        return ("chamfer", ".".join(sorted(what.split("."))) if "." in what else what, op.size, loc.name(op.face))
    return (op.kind,)


def _difference(a: Any, c: Any) -> str | None:
    """The first difference between two summaries' values, give or take
    1e-6 mm (shapes: what `clean` takes away); None when they agree."""
    if isinstance(a, BaseGeometry) and isinstance(c, BaseGeometry):
        d = a.symmetric_difference(c)
        if d.area > 1e-6 and clean(d).area > 1e-6:
            return f"the shapes differ by {d.area:.3g} mm2"
        return None
    if isinstance(a, float) and isinstance(c, float):
        return None if math.isclose(a, c, abs_tol=1e-6) else f"{a!r} against {c!r}"
    if isinstance(a, (tuple, list)) and isinstance(c, (tuple, list)):
        if len(a) != len(c):
            return f"{len(a)} items against {len(c)}: {_short(a)} against {_short(c)}"
        for p, q in zip(a, c):
            found = _difference(p, q)
            if found is not None:
                return found
        return None
    return None if a == c else f"{_short(a)} against {_short(c)}"


def _short(v: Any) -> str:
    text = repr(v) if not isinstance(v, BaseGeometry) else f"<{v.geom_type} of {v.area:.6g} mm2>"
    return text if len(text) < 300 else text[:300] + "..."


# -- what placement promises --------------------------------------------------------------------

def _promises(b: Built) -> list[str]:
    """What the boards and operations of the case built as written must
    be (see the module's docstring)."""
    problems: list[str] = _ambiguity_promises(b) + _directed_promises(b)
    for i, x in enumerate(b.boards):
        if x is not None:
            problems += _board_promises(b, i, x)
    for i, reason in b.reasons.items():
        if "machine():" in reason:
            problems.append(f"board {i} was refused machine() of a big face: {reason}")
    for key, index, where, (depth, thru) in b.meant:
        made = b.made.get(key)
        x = b.boards[_spec_of(b.case, key).board]
        if made is None or x is None:
            continue
        op = x.ops[index]
        problems += _op_promises(x, key, op, where, depth, thru)
    for key, (start, end, pitch, count, got) in b.rows.items():
        lo, hi = sorted((start, end))
        if pitch > 0:
            n = math.floor((hi - lo) / pitch + 1e-9) + 1
            rest = (hi - lo) - (n - 1) * pitch
            want = [lo + rest / 2 + k * pitch for k in range(n)]
        else:
            want = [(lo + hi) / 2] if count == 1 else [lo + (hi - lo) * k / (count - 1) for k in range(count)]
        if start > end:
            want.reverse()
        if len(got) != len(want) or any(abs(p - q) > 1e-6 for p, q in zip(got, want)):
            problems.append(f"the row {key} spreads {[round(p - start, 6) for p in got]} from its start, "
                            f"{[round(p - start, 6) for p in want]} fit")
    return problems


def _directed_promises(b: Built) -> list[str]:
    """A side or a face a board is placed on, plus or minus a length, is
    refused, naming `into()` and `gap()` by that length; with positions it
    computes as they do [decided by Florian, 2026-10-15, syntax.md item 1]."""
    problems: list[str] = []
    for i, spec in enumerate(b.case.boards):
        r = spec.at
        if b.boards[i] is None or r.kind not in ("side", "face"):
            continue
        try:
            ref: Any = _side_of(b, r) if r.kind == "side" else _board(b, r.of).face(r.name)
        except _Missing:
            continue
        n = r.by or spec.t
        fix = (f".into({abs(n):g})", f".gap({abs(n):g})")
        for spelt, move in ((f"{ref!r} + {n:g}", lambda: ref + n), (f"{ref!r} - {n:g}", lambda: ref - n),
                            (f"{n:g} + {ref!r}", lambda: n + ref)):
            try:
                move()
            except LangError as e:
                if not all(f in str(e) for f in fix):
                    problems.append(f"{spelt} is refused without naming into() and gap() by {abs(n):g}: {e}")
            else:
                problems.append(f"{spelt} is not refused")
        p = ref.position
        if ref - p != 0 or (ref + p) / 2 != p or 0.5 * ref + 0.5 * p != p or abs(abs(ref.into(n) - ref) - abs(n)) > 1e-9:
            problems.append(f"{ref!r} computes with a position otherwise than its position does")
    return problems


def _board_promises(b: Built, i: int, x: Board) -> list[str]:
    spec = b.case.boards[i]
    problems: list[str] = []
    bx = x.box()
    t = x.t_axis
    lo_t, hi_t = bx.lo[t], bx.hi[t]
    if spec.center:
        c = as_pos(_position(b, spec.at)).value
        if abs((lo_t + hi_t) / 2 - c) > 1e-6:
            problems.append(f"{x.path} is centred at {(lo_t + hi_t) / 2:g}, not on {c:g}")
    else:
        plane, sign = _plane(b, x, spec)
        want = (plane, plane + spec.t) if sign > 0 else (plane - spec.t, plane)
        if abs(lo_t - want[0]) > 1e-6 or abs(hi_t - want[1]) > 1e-6:
            problems.append(f"{x.path} lies at {lo_t:g} to {hi_t:g} on {t}, on() names {want[0]:g} to {want[1]:g}")
    problems += _limit_promises(b, i, x) if spec.shape is None else _shape_promises(b, i, x)
    sb = x.scope.box
    if sb is not None:
        c = (sb.lo[t] + sb.hi[t]) / 2
        if not lo_t + 1e-9 < c < hi_t - 1e-9:
            inner, outer = x.inner, x.outer
            if abs(inner.value - c) > abs(outer.value - c) + 1e-9:
                problems.append(f"{x.path}'s inner face ({inner.name}) faces away from its scope's middle")
        elif spec.show is None:
            # across the middle: top, else back, else right, in its scope's terms
            want = next(n for n in ("top", "back", "right") if _scope(x).frame.direction(n).axis == t)
            if x.show_face.name != want:
                problems.append(f"{x.path} lies across its scope's middle and shows its {x.show_face.name} face, "
                                f"not its {want}")
    if spec.machine is not None:
        want_face = x.face(spec.machine)
        if x.machine_face.direction != want_face.direction:
            problems.append(f"{x.path} is machined from its {x.machine_face.name} face, machine() names "
                            f"{spec.machine} ({want_face.name})")
    return problems


def _plane(b: Built, x: Board, spec: BoardSpec) -> tuple[float, int]:
    """The plane `on()` names and the way the thickness goes from it."""
    r = spec.at
    if spec.toward is not None:
        return as_pos(_position(b, r)).value, _scope(x).side(spec.toward).outward.sign
    if r.kind == "side":
        s = _side_of(b, r)
        return s.value + s.inward.sign * r.by, s.inward.sign
    f = _board(b, r.of).face(r.name)
    return f.value + f.direction.sign * r.by, f.direction.sign


def _limit_promises(b: Built, i: int, x: Board) -> list[str]:
    """Between its limits on each in-plane axis, less the inset: from one
    to the other; at a board's face, into it no further than `into()`
    says; with one limit, from it to the box's side away from it; with
    none, the box."""
    spec = b.case.boards[i]
    problems: list[str] = []
    bx = x.box()
    sb = x.scope.box
    n = spec.inset
    for axis in (x.u_axis, x.v_axis):
        lo, hi = bx.lo[axis] - n, bx.hi[axis] + n
        ends: list[float] = []
        for limit in b.given.get(i, []):
            if isinstance(limit, Box):
                ends += [limit.lo[axis], limit.hi[axis]]
            elif isinstance(limit, (Board, PartLimit)):
                p, k = (limit, 0.0) if isinstance(limit, Board) else (limit.part, limit.offset)
                if p.t_axis != axis:
                    continue
                pb = p.box()
                reach = min(hi, pb.hi[axis]) - max(lo, pb.lo[axis])
                if reach > max(k, 0.0) + 1e-6:
                    problems.append(f"{x.path} reaches {reach:g} into {p.path} on {axis}, between() says {k:g}")
                ends.append(pb.lo[axis] + k if abs(hi - (pb.lo[axis] + k)) <= abs(lo - (pb.hi[axis] - k))
                            else pb.hi[axis] - k)
            else:
                pos = as_pos(limit)
                if pos.axis == axis:
                    ends.append(pos.value)
        if len(ends) == 1 and sb is not None:
            far = sb.hi[axis] if abs(ends[0] - lo) <= abs(ends[0] - hi) else sb.lo[axis]
            ends.append(far)
        if not ends and sb is not None:
            ends = [sb.lo[axis], sb.hi[axis]]
        if len(ends) == 2:
            want = sorted(ends)
            if abs(lo - want[0]) > 1e-6 or abs(hi - want[1]) > 1e-6:
                problems.append(f"{x.path} reaches from {lo:g} to {hi:g} on {axis} before its inset, its limits "
                                f"say {want[0]:g} to {want[1]:g}")
    return problems


def _op_promises(x: Board, key: str, op: Op, where: Where, depth: float, thru: bool) -> list[str]:
    """An operation lies where its anchor put it, as deep as its depth says."""
    problems: list[str] = []
    if isinstance(op, Hole):
        got = {x.u_axis: (op.u, op.u), x.v_axis: (op.v, op.v)}
        inner: Hole | Pocket = op
    elif isinstance(op, Pocket) and op.slot is not None:      # centred on its anchor, as a hole
        cu, cv = (op.slot.start[0] + op.slot.end[0]) / 2, (op.slot.start[1] + op.slot.end[1]) / 2
        got = {x.u_axis: (cu, cu), x.v_axis: (cv, cv)}
        inner = op
    elif isinstance(op, Pocket):
        u0, v0, u1, v1 = op.shape.bounds
        got = {x.u_axis: (u0, u1), x.v_axis: (v0, v1)}
        inner = op
    elif isinstance(op, EdgeOp) and isinstance(op.op, Hole):
        s_axis, t_axis = x.face_axes(x.face(world_frame().direction(op.face)))
        got = {s_axis: (op.s, op.s), t_axis: (op.t, op.t)}
        inner = op.op
    else:
        return []
    for axis, (lo, hi) in where.items():
        g = got.get(axis)
        if g is None or abs(g[0] - lo) > 1e-6 or abs(g[1] - hi) > 1e-6:
            problems.append(f"the {op.kind} {key} on {x.path} lies at {g} on {axis}, its anchor says {(lo, hi)}")
    if abs(inner.depth - depth) > 1e-6 or (thru and not (isinstance(inner, Hole) and inner.through)
                                         and inner.depth < depth - 1e-6):
        problems.append(f"the {op.kind} {key} on {x.path} is {inner.depth:g} deep, its depth says {depth:g}")
    return problems


# -- the rules decided on 2026-10-14 -------------------------------------------------------------

#: What the language says when it refuses limits that leave it open where a
#: board lies (`Board._check_parts`, `_check_inside`, `_extent`).
AMBIGUOUS = ("is given twice on", "overlap on", "lies inside", "lies at the middle of its room",
             "lies across the middle of the box")


def _limits_on(b: Built, i: int, axis: Axis) -> tuple[list[float], list[tuple[Board, float]]] | None:
    """Board i's limits on an axis as given: the positions (a box's two
    sides among them) and the boards with their `into()` offsets; None
    when one of them cannot be read (a board left out)."""
    positions: list[float] = []
    parts: list[tuple[Board, float]] = []
    try:
        for limit in b.given.get(i, []):
            if isinstance(limit, Box):
                positions += [limit.lo[axis], limit.hi[axis]]
            elif isinstance(limit, (Board, PartLimit)):
                p, k = (limit, 0.0) if isinstance(limit, Board) else (limit.part, limit.offset)
                if p.t_axis == axis:
                    parts.append((p, k))
            else:
                pos = as_pos(limit)
                if pos.axis == axis:
                    positions.append(pos.value)
    except LangError:
        return None
    return positions, parts


def _ambiguity(b: Built, i: int) -> str | None:
    """Which of the rules on ambiguous limits board i's limits break, worked
    out again from what they are: the same board twice, two boards
    overlapping, a position or another board's face (toward the other limit,
    moved by its offset) inside a board past its `into()`, a single
    position at the box's middle, a board as the only limit centred in the
    box; None when none, or when the board's limits cannot be read."""
    x = b.made_boards[i]
    t = x._t_axis if x is not None else None  # pyright: ignore[reportPrivateUsage]
    if x is None or t is None or any(b.boards[j] is None for j in deps(b.case.boards[i])):
        return None
    sb = x.scope.box
    plane: list[Axis] = [a for a in AXES if a != t]
    for axis in plane:
        found = _limits_on(b, i, axis)
        if found is None:
            return None
        positions, parts = found
        boxes = [p.box() for p, _ in parts]
        for k in range(len(parts)):
            for n in range(k + 1, len(parts)):
                if parts[k][0] is parts[n][0]:
                    return "twice"
                if min(boxes[k].hi[axis], boxes[n].hi[axis]) - max(boxes[k].lo[axis], boxes[n].lo[axis]) > 1e-6:
                    return "overlap"
        if len(positions) + len(parts) > 2:
            continue                    # (more than two limits: refused otherwise)
        middle = None if sb is None else (sb.lo[axis] + sb.hi[axis]) / 2
        faces: list[float] = []
        for k, (_, offset) in enumerate(parts):
            pb = boxes[k]
            mid = (pb.lo[axis] + pb.hi[axis]) / 2
            others = positions + [(q.lo[axis] + q.hi[axis]) / 2 for n, q in enumerate(boxes) if n != k]
            toward = others[0] if len(others) == 1 else middle if middle is not None else mid
            faces.append(pb.hi[axis] - offset if toward >= mid else pb.lo[axis] + offset)
        for k, (_, offset) in enumerate(parts):
            reach = max(offset, 0.0)
            for v in positions + [f for n, f in enumerate(faces) if n != k]:
                if boxes[k].lo[axis] + reach + 1e-6 < v < boxes[k].hi[axis] - reach - 1e-6:
                    return "inside"
        if middle is not None and len(parts) == 1 and not positions and \
                abs((boxes[0].lo[axis] + boxes[0].hi[axis]) / 2 - middle) < 1e-9:
            return "centred"
        if middle is not None and len(positions) == 1 and not parts and abs(positions[0] - middle) < 1e-9:
            return "middle"
    return None


def _ambiguity_promises(b: Built) -> list[str]:
    """A board whose limits leave it open where it lies is refused, and a
    board is refused for that only when they do."""
    problems: list[str] = []
    for i, x in enumerate(b.made_boards):
        if x is None:
            continue
        why = _ambiguity(b, i)
        refused = b.reasons.get(i, "")
        if why is not None and b.boards[i] is not None:
            problems.append(f"{x.path} was placed though its limits are ambiguous ({why})")
        elif why is None and any(a in refused for a in AMBIGUOUS) and \
                all(b.boards[j] is not None for j in deps(b.case.boards[i])):
            problems.append(f"{x.path} was refused as ambiguous, which its limits are not: {refused}")
    return problems


def _shape_promises(b: Built, i: int, x: Board) -> list[str]:
    """A board made of a shape: its box is its outline's; it fills its two
    limits on an axis less its inset, sits against a single one, or at the
    scope's front, left or bottom side without one."""
    spec = b.case.boards[i]
    placed = b.placed.get(i)
    bx = x.box()
    u, v = x.u_axis, x.v_axis
    if placed is None:
        return []
    problems: list[str] = []
    if any(abs(p - q) > 1e-9 for p, q in zip(placed, (bx.lo[u], bx.lo[v], bx.hi[u], bx.hi[v]))):
        problems.append(f"{x.path}'s box is not its outline's {placed}")
    sb = x.scope.box
    n = spec.inset
    for axis in (u, v):
        found = _limits_on(b, i, axis)
        if found is None:
            continue
        positions, parts = found
        lo, hi = bx.lo[axis] - n, bx.hi[axis] + n
        ends = positions + [p.box().lo[axis] + k if abs(hi - (p.box().lo[axis] + k)) <= abs(lo - (p.box().hi[axis] - k))
                            else p.box().hi[axis] - k for p, k in parts]
        if len(ends) == 2 and (abs(lo - min(ends)) > 1e-6 or abs(hi - max(ends)) > 1e-6):
            problems.append(f"{x.path}'s shape does not fill its limits on {axis}")
        if len(ends) == 1 and min(abs(lo - ends[0]), abs(hi - ends[0])) > 1e-6:
            problems.append(f"{x.path}'s shape does not sit against its limit on {axis}")
        if not ends and sb is not None:
            start = next(d for d in map(x.scope.frame.direction, LOW) if d.axis == axis)
            at = sb.lo[axis] if start.sign < 0 else sb.hi[axis]
            if abs((lo if start.sign < 0 else hi) - at) > 1e-6:
                problems.append(f"{x.path}'s shape does not sit at its scope's {start.name} on {axis}")
    return problems


# -- checking -----------------------------------------------------------------------------------

@dataclass
class Attempt:
    summary: dict[str, Any]
    problems: list[str]
    paths: dict[str, str]           # op key -> the path of its board
    #: The preview's volume of each board (mm3), where the pipeline ran.
    volumes: dict[str, float] = field(default_factory=dict[str, float])


def _attempt(case: PlacementCase, how: How, first: bool, pipeline: bool) -> Attempt:
    with fresh():
        b = build(case, how)
        try:
            summary = _summary(b)
        except LangError as e:
            return Attempt({}, [f"the layout failed: {e}"], {})
        problems = list(b.problems)
        if first:
            problems += _promises(b)
        meshes: dict[str, Any] = {}
        if pipeline:
            layout = build_layout()["problems"]
            problems += [p for p in _pipeline_problems(meshes) if p not in layout]
        paths = {f"op {k}": x.path for k in b.made if (x := b.made_boards[_spec_of(case, k).board]) is not None}
        volumes = {path: float(mesh.volume) for path, mesh in meshes.items() if mesh is not None}
        return Attempt(summary, problems, paths, volumes)


def ways(case: PlacementCase) -> list[How]:
    """The three ways a case is built: as written, moved (a cabinet facing
    another side), and in another world frame written otherwise."""
    return [How(0, case.origin, case.front, False, None),
            How(0, case.origin2, (case.front + case.turn) % 4, False, None),
            How(case.frame, case.origin3, case.front, case.flip, case.seed)]


def run_case(case: PlacementCase) -> list[str]:
    """What is wrong with the case, built three ways."""
    try:
        attempts = [_attempt(case, how, k == 0, k != 1) for k, how in enumerate(ways(case))]
    except Exception as e:
        frame = next((fr for fr in reversed(traceback.extract_tb(e.__traceback__))
                      if "/lang/" in fr.filename), traceback.extract_tb(e.__traceback__)[-1])
        return [f"{type(e).__name__} at {Path(frame.filename).name}:{frame.lineno}: {e}"]
    problems = [p for a in attempts for p in a.problems]
    if problems:
        return problems
    first = attempts[0]
    for k, other in ((1, attempts[1]), (2, attempts[2])):
        way = ("moved" + (" and facing another side" if case.kind == "cabinet" else "") if k == 1 else
               f"in the world frame {WORLD_FRAMES[case.frame]}{', mirrored the other way' if case.flip else ''}, "
               "written otherwise")
        for key in sorted(set(first.summary) | set(other.summary)):
            a, c = first.summary.get(key, "missing"), other.summary.get(key, "missing")
            found = _difference(a, c)
            if found is not None:
                return [f"{way}, {key} comes out otherwise: {found}"]
    for path, volume in first.volumes.items():
        # (the meshes' booleans round more far from the origin, in the same frame too: 0.4 mm3 of a 16 mm
        # hole's cut from a strip 0.33 mm wide 3.4 m out, 0.5 mm3 from one 1.8 mm wide 4 m out, 1.5 mm3 of
        # a 23 mm one's from a board 0.23 mm thick 3.5 m out; a mesh gone wrong costs more)
        other = attempts[2].volumes.get(path)
        if other is not None and abs(other - volume) > 2.0 + 1e-3 * volume:
            return [f"in the world frame {WORLD_FRAMES[case.frame]} the preview meshes {path} {other:.6g} mm3, "
                    f"not {volume:.6g}"]
    return []


def apply(case: PlacementCase, name: str) -> None:
    """Builds the case as written, as module `name`: for the Fusion batch
    check."""
    build(case, ways(case)[0], name)


def accepted(case: PlacementCase) -> bool:
    """Whether the case keeps every promise and builds all its boards."""
    if run_case(case):
        return False
    with fresh():
        return not build(case, ways(case)[0]).refused


__all__ = ["PlacementCase", "BoardSpec", "BaySpec", "OpSpec", "Ref", "Value", "At", "Depth", "accepted", "apply",
           "placement_cases", "run_case", "ways", "WORLD_FRAMES"]
