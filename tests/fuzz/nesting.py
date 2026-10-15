"""Random cases for fuzzing the nest (`lang.nest`), each with what it must
promise, checked from the outside. A case is plain data (frozen
dataclasses), so a failing example prints as something to build again.

- `parts`: a board lying or standing on any side of its module, in any of
  the 48 world frames, far out or at the origin, with `boards.py`'s
  features (holes, pockets, slots, cuts, notches, V-grooves, rounded
  corners) and maybe a big opening, a grain or none, an extra pocket on one
  big face. The nest must see it from its machining face: its frame maps
  the board's outline at that face onto the item's outline, at the board's
  thickness above the blank, by a proper rotation that turns the
  machining face's normal up; a placed part's transform maps it onto the
  part turned and moved as the nest says; the solver's polygon contains
  the outline and lies at most `items.OUTSIDE` outside it; an opening stays open
  exactly when the smallest part could go in; the turns follow the grain.
- `trees`: random saw plans (sheets cut into strips into pieces, the kerf
  between, pieces holding a blank in their corner or rests). `simplify`
  and `trim_to_bed` must leave pieces and cuts that cover the sheet, every
  blank in one piece that contains it, no more cuts than before, no piece
  holding blanks larger than the bed unless it was before (or, trimmed,
  unless its blank is), and rests marked kept as the workshop keeps them.
- `saws`: blanks and stock (sheets with counts or as many as needed,
  offcuts) for `sawing.best_plan`: every blank sawn once or listed unsawn,
  unsawn only when no stock to be had in any number takes it, each in a
  piece the bed takes, the pieces and cuts covering each sheet, no stock
  used more often than there is.
- `nests`: a few parts of one or two materials and a random workshop
  (bed, sheet sizes with and without counts, offcuts smaller and larger
  than the bed, spacing, margin, kerf, cuts, the keep threshold), nested
  with short times. Refused only when a part truly fits no blank (its
  outline with the margins against the bed and the stock, either way round
  unless its grain says, give or take the solver polygon's growth), or a
  material has no stock; else `verify` finds nothing, parts are left over
  only where every sheet for their material has a count, every transform
  puts its part where the nest says, and the emitter's plan, the drawing
  and the file's JSON follow.
"""
from __future__ import annotations

import json
import math
from collections.abc import Callable
from dataclasses import dataclass, replace
from typing import Literal

import numpy as np
from hypothesis import strategies as st
from shapely import Point, Polygon
from shapely.geometry import box as shapely_box
from shapely.geometry.base import BaseGeometry
from shapely.ops import unary_union

from boards import Feature, apply, features
from fuzzing import floats, fresh, sizes
from lang import Board, Box, Frame, LangError, Shape, board, module, set_frame, sheet_material
from lang.core.directions import ExtentName
from lang.core.geometry import parts_of
from lang.core.layout import build_layout
from lang.core.layout_types import Layout, PartLayout
from lang.emit.nested import apply as apply_matrix
from lang.emit.nested import plan_nest
from lang.nest import Options, Sheet, Workshop, nest_layout
from lang.nest import sawing
from lang.nest.draw import draw_nest
from lang.nest.items import MITRE, OUTSIDE, TOLERANCE, Item, parts_of_layout, turned
from lang.nest.nest_types import BlankOut, RestOut, SheetOut
from lang.nest.sawing import Node, cut_list, cuts, leaves, simplify, trim_to_bed
from lang.nest.verify import _check_sheet  # pyright: ignore[reportPrivateUsage]
from lang.nest.workshop import Offcut, fits
from placement import ALIASES, WORLD_FRAMES

Side = Literal["bottom", "top", "left", "right", "front", "back"]
SIDES: tuple[Side, ...] = ("bottom", "top", "left", "right", "front", "back")
#: The extents of a module that lie in the plane of a board on each side.
_PLANE: dict[str, tuple[ExtentName, ExtentName]] = {"bottom": ("depth", "width"), "top": ("depth", "width"),
                                      "left": ("depth", "height"), "right": ("depth", "height"),
                                      "front": ("width", "height"), "back": ("width", "height")}
MATERIALS = (sheet_material("birch", t=9), sheet_material("birch", t=15), sheet_material("mdf", t=16, grain=False))


# -- parts -------------------------------------------------------------------------------------------

@dataclass(frozen=True)
class PartCase:
    material: int
    side: Side
    #: The board's size along its plane's two extents (`_PLANE`).
    size: tuple[float, float]
    origin: tuple[float, float, float] = (0.0, 0.0, 0.0)
    #: The world frame (`placement.WORLD_FRAMES`).
    frame: int = 0
    features: tuple[Feature, ...] = ()
    #: A through opening in the middle, as fractions of the size (0: none).
    opening: tuple[float, float] = (0.0, 0.0)
    #: grain() along the plane's first or second extent, or unset.
    grain: Literal["", "first", "second"] = ""
    #: The big face (0 or 1) given one more pocket, so that it is machined.
    machined: int = 0
    nested: bool = True


@st.composite
def part_cases(draw: st.DrawFn, longest: float = 1800.0, widest: float = 1100.0) -> PartCase:
    size = (draw(sizes(40, longest)), draw(sizes(40, widest)))
    if draw(st.booleans()):
        size = (size[1], size[0])
    t = 15.0
    far = sizes(-5000, 5000)
    opening = draw(st.one_of(st.just((0.0, 0.0)), st.tuples(floats(0.2, 0.85), floats(0.2, 0.85))))
    return PartCase(draw(st.integers(0, len(MATERIALS) - 1)), draw(st.sampled_from(SIDES)), size,
                    draw(st.one_of(st.just((0.0, 0.0, 0.0)), st.tuples(far, far, far))),
                    draw(st.one_of(st.just(0), st.integers(0, len(WORLD_FRAMES) - 1))),
                    tuple(draw(st.lists(features(size, t), max_size=4))), opening,
                    draw(st.sampled_from(["", "first", "second"])), draw(st.integers(0, 1)),
                    draw(st.booleans()) or draw(st.booleans()))


def build_part(case: PartCase, name: str) -> Board:
    """The board in a module of its own; features the language refuses are
    left out (a refusal changes nothing)."""
    mat = MATERIALS[case.material]
    first, second = _PLANE[case.side]
    extents: dict[str, float] = {"depth": 300.0, "width": 300.0, "height": 300.0}
    extents[first], extents[second] = case.size
    box = Box.from_size(width=extents["width"], depth=extents["depth"], height=extents["height"], origin=case.origin)
    with module(name, box) as m:
        b = board("b", mat).on(getattr(m, case.side))
        if case.grain and mat.grain:
            b.grain(first if case.grain == "first" else second)
        if not case.nested:
            b.nest(False)
        for k, f in enumerate(case.features):
            try:
                apply(b, f, f"f{k}")
            except LangError:
                pass
        u0, v0, u1, v1 = b.outline.bounds
        if case.opening[0] > 0:
            w, h = (u1 - u0) * case.opening[0], (v1 - v0) * case.opening[1]
            cu, cv = (u0 + u1) / 2, (v0 + v1) / 2
            try:
                b.add_cut(Shape(shapely_box(cu - w / 2, cv - h / 2, cu + w / 2, cv + h / 2)), "opening")
            except LangError:
                pass
        try:
            face = b.big_faces()[case.machined]
            b.add_pocket(face, Shape(shapely_box(u0 + 2, v0 + 2, u0 + 8, v0 + 8)), 1.0, "mark")
        except LangError:
            pass
    return b


def _in_frame(case_frame: int) -> None:
    front, left, top = WORLD_FRAMES[case_frame]
    set_frame(Frame(front=front, left=left, top=top, aliases=ALIASES))


def run_parts(cases: tuple[PartCase, ...]) -> list[str]:
    """Builds the parts (all in the first one's world frame) and checks how
    the nest sees each."""
    with fresh():
        try:
            _in_frame(cases[0].frame)
            for k, case in enumerate(cases):
                build_part(case, f"p{k}")
            layout = build_layout()
        except LangError:
            return []
        spacing = 10.0
        try:
            got = parts_of_layout(layout, spacing)
        except LangError as error:
            return _refused_in_pieces(layout, str(error))
        return _item_problems(layout, got.by_material, spacing)


def _refused_in_pieces(layout: Layout, text: str) -> list[str]:
    """A part refused for being in pieces must be: the layout lets a through
    pocket and a cut together cut a piece off a board (`design/bugs.md`,
    KNOWN 2026-10-14), which the nest cannot take."""
    if "machine outline is in" not in text:
        return [f"the nest refused the parts: {text}"]
    path = text.split(":")[0].strip()
    part = next(p for m in layout["modules"] for p in m["parts"] if p["path"] == path)
    pieces = [g for g in parts_of(_machine_outline(part, layout["frame"])) if g.area > 1e-6]
    return [] if len(pieces) > 1 else [f"refused as in pieces, though in one ({path})"]


def _item_problems(layout: Layout, by_material: dict[str, list[Item]], spacing: float) -> list[str]:
    problems: list[str] = []
    parts = {p["path"]: p for m in layout["modules"] for p in m["parts"]}
    for items in by_material.values():
        smallest = min(i.area for i in items)
        for item in items:
            problems += [f"{p} ({item.path})" for p in _one_item(parts[item.path], item, layout, spacing, smallest)]
    nested = {i.path for items in by_material.values() for i in items}
    for path, part in parts.items():
        if part["nest"] != (path in nested):
            problems.append(f"{path}: nest {part['nest']}, but {'not ' if path not in nested else ''}nested")
    return problems


def _one_item(part: PartLayout, item: Item, layout: Layout, spacing: float, smallest: float) -> list[str]:
    problems: list[str] = []
    frame = layout["frame"]
    sign = 1 if frame[part["machine"]][0] == "+" else -1
    axis = frame[part["machine"]][1]
    m = np.array(item.frame.matrix())
    rotation = m[:, :3]
    if not (np.allclose(rotation @ rotation.T, np.eye(3)) and np.isclose(np.linalg.det(rotation), 1.0)):
        problems.append("its frame is no proper rotation (a mirrored part)")
    normal = np.zeros(3)
    normal["xyz".index(axis)] = sign
    if not np.allclose(rotation @ normal, [0, 0, 1]):
        problems.append("its machining face does not look up")
    seen = _seen(part, item.frame.matrix(), sign, frame)
    if seen is None:
        problems.append("its outline does not lie at its thickness above the blank")
    elif seen.symmetric_difference(Polygon(item.shape.exterior)).area > 1e-4 * max(1.0, seen.length):
        problems.append(f"its outline maps {seen.symmetric_difference(Polygon(item.shape.exterior)).area:.3g} mm2 "
                        "off the nest's")
    # A placed part's transform: turned by its turn, moved anywhere.
    turn, at = item.turns[-1], (123.25, -45.5)
    placed = _seen(part, item.frame.placed(turn, at), sign, frame)
    want = Polygon(item.placed(turn, at).exterior)
    if placed is None or placed.symmetric_difference(want).area > 1e-4 * max(1.0, want.length):
        problems.append("its transform does not put it where the nest says")
    def takes(ring: object, inward: float) -> bool:
        return Polygon(ring).buffer(-inward, join_style="mitre").area >= smallest - 1e-6  # pyright: ignore[reportArgumentType]
    solid = Polygon(item.shape.exterior, [r for r in item.shape.interiors if takes(r, spacing)])
    if not item.solver.buffer(1e-6).contains(solid):
        problems.append("the solver's outline cuts into it")
    if not all(takes(r, spacing) for r in item.solver.interiors):
        problems.append("the solver has an opening no part could go in")
    for r in item.shape.interiors:          # one that surely takes a part is open
        if takes(r, spacing + OUTSIDE) and not any(Polygon(h).intersects(Polygon(r)) for h in item.solver.interiors):
            problems.append("an opening that takes a part is filled")
    shape = Polygon(item.shape.exterior)
    outside = max(shape.distance(Point(p)) for p in item.solver.exterior.coords)
    if outside > OUTSIDE + 1e-6:
        problems.append(f"the solver's outline lies {outside:.3g} mm outside, more than {OUTSIDE:g}")
    grain = part["grain"] if part["grained"] else None
    want_turns = ((0.0, 180.0) if grain == item.frame.u else (90.0, 270.0) if grain == item.frame.v
                  else (0.0, 90.0, 180.0, 270.0))
    if item.turns != want_turns:
        problems.append(f"turns {item.turns}, its grain {grain} wants {want_turns}")
    return problems


def _seen(part: PartLayout, matrix: list[list[float]], sign: int, frame: dict[str, str]) -> Polygon | None:
    """The part's machine outline (`_machine_outline`) at its machining
    face, mapped by `matrix`; None unless it lies at the thickness."""
    t, u, v = part["axes"]["t"], part["axes"]["u"], part["axes"]["v"]
    i = "xyz".index(t)
    face_t = part["box"]["max"][i] if sign > 0 else part["box"]["min"][i]
    outline = _machine_outline(part, frame)
    if not isinstance(outline, Polygon):
        return None
    points: list[tuple[float, float]] = []
    for pu, pv in list(outline.exterior.coords)[:-1]:
        p = [0.0, 0.0, 0.0]
        p["xyz".index(u)], p["xyz".index(v)], p[i] = pu, pv, face_t
        x, y, z = apply_matrix(matrix, (p[0], p[1], p[2]))
        if abs(z - part["thickness"]) > 1e-6:
            return None
        points.append((x, y))
    return Polygon(points)


# -- saw plans ---------------------------------------------------------------------------------------

@dataclass(frozen=True)
class TreeCase:
    """A sheet cut by a plan: each node's pieces as fractions of its extent
    along alternating axes; a leaf a blank (its size as fractions of the
    leaf, in its corner) or a rest."""
    sheet: tuple[float, float]
    plan: tuple[object, ...]
    bed: tuple[float, float]
    kerf: float
    keep: tuple[float, float]
    first_axis: int


@st.composite
def _plan(draw: st.DrawFn, depth: int) -> tuple[object, ...]:
    if depth >= 3 or draw(st.integers(0, 3)) == 0:
        if draw(st.booleans()):
            return ("blank", draw(floats(0.3, 1.0)), draw(floats(0.3, 1.0)))
        return ("rest",)
    n = draw(st.integers(2, 4))
    shares = tuple(draw(floats(0.05, 1.0)) for _ in range(n))
    return ("split", shares, tuple(draw(_plan(depth + 1)) for _ in range(n)))


@st.composite
def tree_cases(draw: st.DrawFn) -> TreeCase:
    sheet = (draw(sizes(800, 3000)), draw(sizes(500, 1600)))
    bed = (draw(sizes(500, 2600)), draw(sizes(400, 1400)))
    return TreeCase(sheet, draw(_plan(0)), bed, draw(st.sampled_from([0.0, 3.0, 4.0, 4.5])),
                    (draw(sizes(0, 400)), draw(floats(0, 0.4))), draw(st.integers(0, 1)))


def build_tree(case: TreeCase) -> tuple[Node, list[tuple[float, float]], dict[int, tuple[float, float]]]:
    """The plan as a tree, the blanks' sizes and corners."""
    sizes_: list[tuple[float, float]] = []
    origins: dict[int, tuple[float, float]] = {}

    def make(rect: list[float], plan: tuple[object, ...], axis: int) -> Node:
        if plan[0] == "blank":
            w, h = rect[2] * float(plan[1]), rect[3] * float(plan[2])  # type: ignore[arg-type]
            origins[len(sizes_)] = (rect[0], rect[1])
            sizes_.append((w, h))
            return Node(list(rect), [len(sizes_) - 1])
        if plan[0] == "rest":
            return Node(list(rect))
        shares: tuple[float, ...] = plan[1]  # type: ignore[assignment]
        kids_plans: tuple[tuple[object, ...], ...] = plan[2]  # type: ignore[assignment]
        room = rect[axis + 2] - case.kerf * (len(shares) - 1)
        if room <= len(shares):
            return Node(list(rect))
        total = sum(shares)
        kids: list[Node] = []
        at = rect[axis]
        for k, (share, sub) in enumerate(zip(shares, kids_plans)):
            length = room * share / total if k < len(shares) - 1 else rect[axis] + rect[axis + 2] - at
            r = list(rect)
            r[axis], r[axis + 2] = at, length
            kids.append(make(r, sub, 1 - axis))
            at += length + case.kerf
        return Node(list(rect), children=kids)

    tree = make([0.0, 0.0, case.sheet[0], case.sheet[1]], case.plan, case.first_axis)
    return tree, sizes_, origins


def _fits_of(bed: tuple[float, float]) -> Callable[[float, float], bool]:
    return lambda w, h: fits(w, h, bed)


def _keeps_of(keep: tuple[float, float]) -> Callable[[float, float], bool]:
    return lambda w, h: min(w, h) >= keep[0] - 1e-9 and w * h >= keep[1] * 1e6 - 1e-6


def run_tree(case: TreeCase) -> list[str]:
    tree, sizes_, origins = build_tree(case)
    fits_bed, keeps = _fits_of(case.bed), _keeps_of(case.keep)
    problems = _tree_problems(tree, case, sizes_, origins, "the plan as made")
    if problems:
        return ["the harness made a bad plan: " + p for p in problems]
    before = cuts(tree)
    oversize = {bi for leaf in leaves(tree) if leaf.used and not fits_bed(leaf.rect[2], leaf.rect[3])
                for bi in leaf.blanks}
    simple = simplify(tree, fits_bed, keeps)
    problems += _tree_problems(simple, case, sizes_, origins, "simplified")
    if cuts(simple) > before:
        problems.append(f"simplified: {cuts(simple)} cuts, more than the {before} before")
    for leaf in leaves(simple):
        if leaf.used and not fits_bed(leaf.rect[2], leaf.rect[3]) and not set(leaf.blanks) & oversize:
            problems.append(f"simplified: a piece {leaf.rect} holding blanks grew larger than the bed")
    trimmed = trim_to_bed(simple, sizes_, origins, case.kerf, fits_bed)
    problems += _tree_problems(trimmed, case, sizes_, origins, "trimmed")
    for leaf in leaves(trimmed):
        if leaf.used and not fits_bed(leaf.rect[2], leaf.rect[3]):
            if len(leaf.blanks) == 1:
                (bx, by), (bw, bh) = origins[leaf.blanks[0]], sizes_[leaf.blanks[0]]
                x, y, w, h = leaf.rect
                # Only what is narrower than the kerf may stay beside the blank.
                slack = max(bx - x, by - y, x + w - bx - bw, y + h - by - bh)
                if fits_bed(bw, bh) and slack > case.kerf + 1e-6:
                    problems.append(f"trimmed: a piece {leaf.rect} is larger than the bed, its blank "
                                    f"{(bx, by, bw, bh)} is not")
    return problems


def _tree_problems(tree: Node, case: TreeCase, sizes_: list[tuple[float, float]],
                   origins: dict[int, tuple[float, float]], what: str) -> list[str]:
    problems: list[str] = []
    keeps = _keeps_of(case.keep)
    holders: dict[int, int] = {}
    blanks: list[BlankOut] = []
    rests: list[RestOut] = []
    for leaf in leaves(tree):
        if leaf.used:
            blanks.append({"name": str(len(blanks)), "rect": list(leaf.rect), "parts": []})
            for bi in leaf.blanks:
                holders[bi] = holders.get(bi, 0) + 1
                (bx, by), (bw, bh) = origins[bi], sizes_[bi]
                x, y, w, h = leaf.rect
                if bx < x - 1e-6 or by < y - 1e-6 or bx + bw > x + w + 1e-6 or by + bh > y + h + 1e-6:
                    problems.append(f"{what}: blank {bi} lies outside its piece {leaf.rect}")
        else:
            rests.append({"rect": list(leaf.rect), "keep": keeps(leaf.rect[2], leaf.rect[3])})
    if sorted(holders) != list(range(len(sizes_))) or any(n != 1 for n in holders.values()):
        problems.append(f"{what}: the blanks are held {holders}, not each once")
    sheet: SheetOut = {"name": "1", "stock": "sheet", "size": list(case.sheet),
                       "cuts": [{"line": list(c.line), "piece": list(c.piece)} for c in cut_list(tree, case.kerf)],
                       "blanks": blanks, "rests": rests}
    workshop = Workshop(bed=case.bed, kerf=case.kerf, max_cuts=10_000, keep_across=case.keep[0],
                        keep_area=case.keep[1])
    problems += [f"{what}: {p}" for p in _check_sheet(sheet, workshop)]
    return problems


@dataclass(frozen=True)
class SawCase:
    blanks: tuple[tuple[float, float], ...]
    #: Length, width, copies (-1: as many as needed), kind.
    stock: tuple[tuple[float, float, int, str], ...]
    bed: tuple[float, float]
    kerf: float
    max_cuts: int
    keep: tuple[float, float]


@st.composite
def saw_cases(draw: st.DrawFn) -> SawCase:
    bed = (draw(sizes(600, 2500)), draw(sizes(400, 1300)))
    # Blanks fit the bed (the nest's do), mostly whole millimetres as cut down.
    blank = st.tuples(sizes(30, bed[0]), sizes(30, bed[1])).map(
        lambda b: (math.ceil(b[0]), math.ceil(b[1])) if math.ceil(b[0]) <= bed[0] and math.ceil(b[1]) <= bed[1]
        else b)
    blanks = tuple(draw(st.lists(blank.map(lambda b: (float(b[0]), float(b[1]))), min_size=1, max_size=8)))
    stock = tuple(draw(st.lists(st.tuples(sizes(300, 3000), sizes(200, 1600),
                                          st.one_of(st.just(-1), st.integers(1, 3)),
                                          st.sampled_from(["sheet", "offcut"])), min_size=1, max_size=3)))
    return SawCase(blanks, stock, bed, draw(st.sampled_from([0.0, 3.0, 4.0])), draw(st.integers(1, 8)),
                   (draw(sizes(0, 400)), draw(floats(0, 0.4))))


def run_saw(case: SawCase) -> list[str]:
    stock = [sawing.Stock(l, w, n, 1.0 if kind == "offcut" else l * w, kind, k)
             for k, (l, w, n, kind) in enumerate(case.stock)]
    fits_bed, keeps = _fits_of(case.bed), _keeps_of(case.keep)
    plan = sawing.best_plan(list(case.blanks), stock, case.kerf, case.max_cuts, fits_bed, keeps, 0.05)
    problems: list[str] = []
    sawn: dict[int, int] = {}
    used: dict[int, int] = {}
    for n, s in enumerate(plan.sheets):
        used[s.stock] = used.get(s.stock, 0) + 1
        length, width, _copies, _kind = case.stock[s.stock]
        tree_case = TreeCase((length, width), (), case.bed, case.kerf, case.keep, 0)
        unit = sawing.UNIT
        sizes_ = [(math.ceil(w * unit - 1e-9) / unit, math.ceil(h * unit - 1e-9) / unit) for w, h in case.blanks]
        problems += _sawn_problems(s.tree, tree_case, sizes_, plan.origins, f"sheet {n + 1}")
        for leaf in leaves(s.tree):
            for bi in leaf.blanks:
                sawn[bi] = sawn.get(bi, 0) + 1
            if leaf.used and not fits_bed(leaf.rect[2], leaf.rect[3]):
                problems.append(f"sheet {n + 1}: a piece {leaf.rect} holding blanks is larger than the bed")
        if cuts(s.tree) != plan.cuts[n]:
            problems.append(f"sheet {n + 1}: {cuts(s.tree)} cuts, the plan says {plan.cuts[n]}")
    if plan.over != sum(1 for c in plan.cuts if c > case.max_cuts):
        problems.append("the sheets over the cut limit are miscounted")
    if any(n != 1 for n in sawn.values()) or set(sawn) & set(plan.unsawn) or \
            sorted(set(sawn) | set(plan.unsawn)) != list(range(len(case.blanks))):
        problems.append(f"blanks sawn {sawn}, unsawn {plan.unsawn}: not each once")
    for k, n in used.items():
        if case.stock[k][2] >= 0 and n > case.stock[k][2]:
            problems.append(f"stock {k} used {n} times, {case.stock[k][2]} on hand")
    for bi in plan.unsawn:
        w, h = case.blanks[bi]
        unit = sawing.UNIT
        if any(c < 0 and math.ceil(w * unit - 1e-9) <= math.floor(l * unit + 1e-9)
               and math.ceil(h * unit - 1e-9) <= math.floor(s * unit + 1e-9) for l, s, c, _k in case.stock):
            problems.append(f"blank {bi} {w:g} x {h:g} unsawn, though stock in any number takes it")
    return problems


def _sawn_problems(tree: Node, case: TreeCase, sizes_: list[tuple[float, float]],
                   origins: dict[int, tuple[float, float]], what: str) -> list[str]:
    """As `_tree_problems`, for a sheet of a plan that holds some of the
    blanks only."""
    held = [bi for leaf in leaves(tree) for bi in leaf.blanks]
    sub = {bi: k for k, bi in enumerate(held)}
    relabelled = _relabel(tree, sub)
    return _tree_problems(relabelled, case, [sizes_[bi] for bi in held], {sub[bi]: origins[bi] for bi in held}, what)


def _relabel(node: Node, sub: dict[int, int]) -> Node:
    return Node(list(node.rect), [sub[b] for b in node.blanks], list(node.parts), [_relabel(c, sub) for c in node.children])


# -- whole nests -------------------------------------------------------------------------------------

@dataclass(frozen=True)
class StockCase:
    bed: tuple[float, float]
    #: Length, width, count (None: as many as needed), material index (None: every one).
    sheets: tuple[tuple[float, float, int | None, int | None], ...]
    #: Material index, length, width.
    offcuts: tuple[tuple[int, float, float], ...] = ()
    spacing: float = 10.0
    margin: float = 10.0
    kerf: float = 4.0
    max_cuts: int = 5
    keep: tuple[float, float] = (300.0, 0.25)

    def workshop(self) -> Workshop:
        return Workshop(bed=self.bed, spacing=self.spacing, margin=self.margin, kerf=self.kerf,
                        max_cuts=self.max_cuts, keep_across=self.keep[0], keep_area=self.keep[1],
                        sheets=tuple(Sheet(l, w, n, None if m is None else MATERIALS[m].label)
                                     for l, w, n, m in self.sheets),
                        offcuts=tuple(Offcut(MATERIALS[m].label, l, w) for m, l, w in self.offcuts))


@dataclass(frozen=True)
class NestCase:
    parts: tuple[PartCase, ...]
    stock: StockCase
    seconds: float = 0.3


@st.composite
def stock_cases(draw: st.DrawFn) -> StockCase:
    bed = (draw(sizes(700, 2500)), draw(sizes(500, 1300)))
    if draw(st.booleans()):
        bed = (bed[1], bed[0])
    sheet = st.tuples(sizes(500, 3000), sizes(400, 1600), st.one_of(st.none(), st.none(), st.integers(1, 3)),
                      st.one_of(st.none(), st.none(), st.integers(0, len(MATERIALS) - 1)))
    offcut = st.tuples(st.integers(0, len(MATERIALS) - 1), sizes(150, 2600), sizes(150, 1300))
    return StockCase(bed, tuple(draw(st.lists(sheet, min_size=1, max_size=3))),
                     tuple(draw(st.lists(offcut, max_size=3))),
                     draw(st.one_of(st.just(10.0), sizes(0, 25))), draw(st.one_of(st.just(10.0), sizes(0, 25))),
                     draw(st.sampled_from([0.0, 3.2, 4.0, 6.0])), draw(st.integers(1, 8)),
                     (draw(st.one_of(st.just(300.0), sizes(0, 600))), draw(st.one_of(st.just(0.25), floats(0, 0.6)))))


@st.composite
def nest_cases(draw: st.DrawFn) -> NestCase:
    stock = draw(stock_cases())
    short = draw(st.integers(0, 3)) == 0
    if short:
        # One sheet a little larger than the bed: the stock runs short.
        length, width = max(stock.bed) * draw(floats(1.0, 1.4)), min(stock.bed) * draw(floats(1.0, 1.4))
        stock = replace(stock, sheets=((length, width, draw(st.integers(1, 2)), None),))
    longest, widest = max(stock.bed) * 0.95, min(stock.bed) * 0.95
    frame = draw(st.one_of(st.just(0), st.integers(0, len(WORLD_FRAMES) - 1)))
    small, large = part_cases(longest * 0.4, widest * 0.4), part_cases(longest, widest)
    parts = draw(st.lists(st.one_of(small, small, large), min_size=6 if short else 1, max_size=12 if short else 8))
    one = draw(st.one_of(st.none(), st.integers(0, len(MATERIALS) - 1)))
    return NestCase(tuple(PartCase(p.material if one is None else one, p.side, p.size, p.origin, frame, p.features,
                                   p.opening, p.grain, p.machined, p.nested) for p in parts),
                    stock, draw(st.sampled_from([0.2, 0.4])))


def run_nest(case: NestCase) -> list[str]:
    with fresh():
        try:
            _in_frame(case.parts[0].frame)
            for k, part in enumerate(case.parts):
                build_part(part, f"p{k}")
            layout = build_layout()
        except LangError:
            return []
        workshop = case.stock.workshop()
        options = Options(seconds=case.seconds, saw_seconds=0.05, refill_seconds=0.1)
        must, may = _misfits(layout, workshop)
        try:
            nest, parts = nest_layout(layout, workshop, options=options)
        except LangError as error:
            text = str(error)
            if "machine outline is in" in text:
                return _refused_in_pieces(layout, text)
            if "cannot be nested" in text or "No stock on hand" in text:
                refused = {line.split(" (")[0].strip() for line in text.splitlines()[1:]}
                problems = [f"refused, though it fits a blank ({path})" for path in refused - may]
                if "No stock on hand" not in text:
                    problems += [f"not refused, though it fits no blank ({path})" for path in must - refused]
                return problems
            return [f"refused: {text}"]
        if must:
            return [f"nested, though {sorted(must)} fit no blank"]
        # The verifier's findings, without the material in front (explore.py
        # names a kind of problem by its first words).
        # A sheet over the cut limit is reported, not refused: the saw keeps a
        # plan within it where it finds one (`sawing.best_plan`), and some
        # cannot be (a sheet larger than the bed both ways needs two cuts).
        problems = ["the nest's own check: " + p.split(": ", 1)[-1] + f" ({p.split(': ', 1)[0]})"
                    for p in nest["problems"] if "left over" not in p and not _over_cuts(p, workshop)]
        items = {i.path: i for items_ in parts.by_material.values() for i in items_}
        by_path = {p["path"]: p for m in layout["modules"] for p in m["parts"]}
        for m in nest["materials"]:
            if m["unplaced"] and any(s.count is None for s in workshop.sheets_for(m["material"])):
                problems.append(f"{m['material']}: {len(m['unplaced'])} parts left over, though sheets are to be had")
            for s in m["sheets"]:
                for b in s["blanks"]:
                    for p in b["parts"]:
                        part, item = by_path[p["path"]], items[p["path"]]
                        sign = 1 if layout["frame"][part["machine"]][0] == "+" else -1
                        seen = _seen(part, p["transform"], sign, layout["frame"])
                        want = Polygon(item.placed(p["turn"], (p["at"][0], p["at"][1])).exterior)
                        if seen is None or seen.symmetric_difference(want).area > 1e-4 * max(1.0, want.length):
                            problems.append(f"a transform does not put its part where the nest says ({p['path']})")
        docs = plan_nest(nest, layout)
        if [d.material for d in docs] != [m["material"] for m in nest["materials"]]:
            problems.append("the emitter plans other materials than the nest has")
        if not draw_nest(nest, items).startswith("<svg"):
            problems.append("no drawing")
        if json.loads(json.dumps(nest)) != nest:
            problems.append("the nest does not survive JSON")
        return problems


def _machine_outline(part: PartLayout, frame: dict[str, str]) -> BaseGeometry:
    """The outline less the through pockets and holes, worked out here."""
    shape: BaseGeometry = Polygon(part["outline"][0], part["outline"][1:])
    t = part["axes"]["t"]
    for op in part["ops"]:
        if op["kind"] == "pocket" and frame[op["face"]][1] == t and op["depth"] >= part["thickness"] - 1e-6:
            shape = shape.difference(unary_union([Polygon(r) for r in op["shape"]]))
        elif op["kind"] == "hole" and op["through"] and frame[op["face"]][1] == t:
            shape = shape.difference(Point(op["u"], op["v"]).buffer(op["d"] / 2))
    return shape


def _over_cuts(problem: str, workshop: Workshop) -> bool:
    return f"cuts, more than {workshop.max_cuts}" in problem


def _misfits(layout: Layout, workshop: Workshop) -> tuple[set[str], set[str]]:
    """The parts that fit no blank for sure, and those that may not (the
    solver's polygon is up to 2 x 1.5 x TOLERANCE x MITRE larger than the
    outline)."""
    assert workshop.bed is not None
    bed = workshop.bed
    frame = layout["frame"]
    must: set[str] = set()
    may: set[str] = set()
    for module_ in layout["modules"]:
        for part in module_["parts"]:
            if not part["nest"]:
                continue
            material_ = part["material"]
            stock = [(s.length, s.width) for s in workshop.sheets_for(material_)] + \
                    [(o.length, o.width) for o in workshop.offcuts_for(material_)]
            u0, v0, u1, v1 = _machine_outline(part, frame).bounds
            w, h = u1 - u0, v1 - v0
            grain = part["grain"] if part["grained"] else None
            ways = [(w, h)] if grain == part["axes"]["u"] else [(h, w)] if grain == part["axes"]["v"] else \
                [(w, h), (h, w)]

            def fit(extra: float) -> bool:
                m2 = 2 * workshop.margin + extra
                return any(fits(a + m2, b + m2, bed) and any(a + m2 <= sl + 1e-6 and b + m2 <= sw + 1e-6 for sl, sw in stock)
                           for a, b in ways)
            if not fit(0.0):
                must.add(part["path"])
            if not fit(2 * 1.5 * TOLERANCE * MITRE + 1e-6):
                may.add(part["path"])
    return must, may


__all__ = ["PartCase", "part_cases", "run_parts", "TreeCase", "tree_cases", "run_tree", "SawCase", "saw_cases",
           "run_saw", "NestCase", "nest_cases", "run_nest", "turned"]
