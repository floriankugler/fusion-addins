"""Sawing blanks out of stock: PackingSolver's guillotine solver for
rectangles, then the plan made as simple as it can be, judged by the
number of cuts and the leftover.

A plan is a cutting tree: a sheet, cut into strips (the first cuts), each
cut into pieces (the second cuts), and so on, straight cuts right through,
the kerf between the pieces. A leaf is a piece that holds blanks (machined
at once) or a rest, kept as stock when the workshop keeps it (300 mm across
and 0.25 m2 [Florian, 2026-10-14]) and waste otherwise. Each blank keeps
the sheet's grain along x.

Before the cuts are counted, those that are not needed are left out,
between pieces side by side, from the leaves up:

- two rests: one rest, bigger;
- pieces that hold blanks, and rests too small to keep, when the bed takes
  them together: one piece, machined at once, each blank's parts staying
  where they are [Florian, 2026-10-14: two blanks side by side that the bed
  takes together are not cut apart]; two pieces holding blanks only where
  two margins and the kerf make up the spacing (`join`), since the parts
  across the cut left out are that far apart [found by fuzzing,
  2026-10-14: with margin and kerf 0 they came 1.4 mm apart];
- a rest too small to keep beside a piece that is cut further: the pieces
  along it take it along (each grows across it), when every piece holding
  blanks still fits the bed.

A node left with one child is that child. A node with k children takes
k - 1 cuts; a sheet's cuts are the sum. A piece the solver left larger than
the bed (it records no cut beside a blank shorter than its slot) is cut
down to its blank; where what is cut off is narrower than the kerf, the
blade takes it all and the piece's one child stops short of its edge: a
trim, one cut more [found by fuzzing, 2026-10-15: a 2.5 mm strip at the
sheet's edge left a piece over the bed].

`best_plan` saws with a few settings side by side (two or three stages,
rips or cross cuts first, with or without a limit on the cuts per stage),
`seconds` each, and keeps, in this order: every blank sawn; no sheet over `max_cuts`; the cheapest stock;
the largest single piece kept; the fewest cuts [proposed, and the ranking
of leftovers chosen by Florian, 2026-10-14]. When the stock on hand cannot
take every blank, knapsack saws as many as it can.
"""
from __future__ import annotations

import importlib
import math
from collections.abc import Callable, Sequence
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from typing import Any

# PackingSolver is a compiled extension without stubs (see packing.py).
ps: Any = importlib.import_module("packingsolver")
rg: Any = importlib.import_module("packingsolver.rectangleguillotine")

Rect = list[float]      # x, y, w, h
#: The guillotine solver takes whole numbers: it saws in tenths of a
#: millimetre, the kerf rounded up to one (`Workshop.saw_kerf`) [found by
#: fuzzing, 2026-10-14: in whole millimetres a 3.2 kerf became 4, and the
#: pieces between the cuts grew by the difference, past the bed].
UNIT = 10


@dataclass(frozen=True)
class PartOn:
    """A part on a sheet: the item's index, its turn, and where its nest
    frame's origin lies on the sheet."""
    item: int
    turn: float
    at: tuple[float, float]


@dataclass
class Node:
    #: x, y, w, h on the sheet: the piece between its cuts.
    rect: Rect
    #: For a leaf, the blanks of the nest it holds (their indices).
    blanks: list[int] = field(default_factory=list[int])
    #: For a leaf, the parts on it, on the sheet.
    parts: list[PartOn] = field(default_factory=list[PartOn])
    children: list[Node] = field(default_factory=list["Node"])

    @property
    def leaf(self) -> bool:
        return not self.children

    @property
    def used(self) -> bool:
        """A piece that holds blanks (and their parts), machined at once."""
        return self.leaf and bool(self.blanks or self.parts)

    @property
    def rest(self) -> bool:
        return self.leaf and not self.used


@dataclass(frozen=True)
class Stock:
    """A piece of stock to saw: `length` along the grain (x), `width` across."""
    length: float
    width: float
    #: How many; -1: as many as needed.
    copies: int
    cost: float
    #: "sheet" or "offcut".
    kind: str
    #: What the caller knows it by.
    key: int


@dataclass
class Sawn:
    """One piece of stock sawn: its plan and which stock it is."""
    tree: Node
    stock: int


@dataclass
class Plan:
    sheets: list[Sawn]
    #: Blanks no stock took.
    unsawn: list[int]
    setting: dict[str, Any]
    cuts: list[int]
    cost: float
    largest_kept: float
    over: int
    #: Each blank's corner on its sheet.
    origins: dict[int, tuple[float, float]]


Keeps = Callable[[float, float], bool]
FitsBed = Callable[[float, float], bool]


def kept(node: Node, keeps: Keeps) -> bool:
    return node.rest and keeps(node.rect[2], node.rect[3])


def _joined(a: Node, b: Node) -> Rect:
    x0, y0 = min(a.rect[0], b.rect[0]), min(a.rect[1], b.rect[1])
    x1 = max(a.rect[0] + a.rect[2], b.rect[0] + b.rect[2])
    y1 = max(a.rect[1] + a.rect[3], b.rect[1] + b.rect[3])
    return [x0, y0, x1 - x0, y1 - y0]


def axis_of(kids: list[Node]) -> int:
    """The axis along which a node's pieces lie side by side (0: x)."""
    a, b = kids[0], kids[1]
    return 0 if a.rect[0] + a.rect[2] <= b.rect[0] + 1e-6 else 1


def _axis(node: Node) -> int:
    """The axis a node is cut along; for one child, a trim, the axis on
    which the child is shorter."""
    if len(node.children) > 1:
        return axis_of(node.children)
    return 0 if node.children[0].rect[2] < node.rect[2] - 1e-6 else 1


def _trims(node: Node) -> tuple[bool, bool]:
    """Whether a node's children stop short of its start and of its end."""
    axis = _axis(node)
    first, last = node.children[0], node.children[-1]
    return (first.rect[axis] > node.rect[axis] + 1e-6,
            last.rect[axis] + last.rect[axis + 2] < node.rect[axis] + node.rect[axis + 2] - 1e-6)


def _grown(node: Node, axis: int, at_start: bool, amount: float, fits_bed: FitsBed) -> Node | None:
    """`node` grown by `amount` along `axis` (at its start or its end), the
    growth passed on to the pieces along that side; None when a piece
    holding blanks would no longer fit the bed."""
    r = list(node.rect)
    if at_start:
        r[axis] -= amount
    r[axis + 2] += amount
    if node.leaf:
        if node.used and not fits_bed(r[2], r[3]):
            return None
        return Node(r, list(node.blanks), list(node.parts))
    kids = list(node.children)
    if len(kids) > 1 and axis_of(kids) == axis:
        k = 0 if at_start else len(kids) - 1
        g = _grown(kids[k], axis, at_start, amount, fits_bed)
        if g is None:
            return None
        kids[k] = g
    else:
        new: list[Node] = []
        for c in kids:
            g = _grown(c, axis, at_start, amount, fits_bed)
            if g is None:
                return None
            new.append(g)
        kids = new
    return Node(r, children=kids)


def simplify(node: Node, fits_bed: FitsBed, keeps: Keeps, join: bool = True) -> Node:
    """Leaves out the cuts that are not needed (see the module's doc);
    `join`: whether two pieces holding blanks may be one."""
    if node.leaf:
        return node
    kids = [simplify(c, fits_bed, keeps, join) for c in node.children]
    changed = True
    while changed:
        changed = False
        for i in range(len(kids) - 1):
            a, b = kids[i], kids[i + 1]
            r = _joined(a, b)
            if a.leaf and b.leaf:
                if a.rest and b.rest:
                    kids[i:i + 2] = [Node(r)]
                elif (not kept(a, keeps) and not kept(b, keeps) and fits_bed(r[2], r[3])
                      and (join or not (a.used and b.used))):
                    kids[i:i + 2] = [Node(r, a.blanks + b.blanks, a.parts + b.parts)]
                else:
                    continue
            elif a.rest and not kept(a, keeps) and not b.leaf:
                axis = axis_of(kids)
                g = _grown(b, axis, True, b.rect[axis] - a.rect[axis], fits_bed)
                if g is None:
                    continue
                kids[i:i + 2] = [simplify(g, fits_bed, keeps, join)]
            elif b.rest and not kept(b, keeps) and not a.leaf:
                axis = axis_of(kids)
                g = _grown(a, axis, False, (b.rect[axis] + b.rect[axis + 2]) - (a.rect[axis] + a.rect[axis + 2]),
                           fits_bed)
                if g is None:
                    continue
                kids[i:i + 2] = [simplify(g, fits_bed, keeps, join)]
            else:
                continue
            changed = True
            break
    if len(kids) == 1:
        only = kids[0]
        # The one child takes the node's whole place.
        if only.leaf and (only.rest or fits_bed(node.rect[2], node.rect[3])):
            return Node(list(node.rect), only.blanks, only.parts)
        return only
    return Node(list(node.rect), children=kids)


def cuts(node: Node) -> int:
    if node.leaf:
        return 0
    return len(node.children) - 1 + sum(_trims(node)) + sum(cuts(c) for c in node.children)


def leaves(node: Node) -> list[Node]:
    return [node] if node.leaf else [leaf for c in node.children for leaf in leaves(c)]


@dataclass(frozen=True)
class Cut:
    """A straight cut through `piece`: the line along its middle, from edge
    to edge."""
    line: tuple[float, float, float, float]
    piece: tuple[float, float, float, float]


def cut_list(node: Node, kerf: float) -> list[Cut]:
    """The cuts in the order they are made: a piece's cuts, then each of
    its pieces' in turn."""
    if node.leaf:
        return []
    axis = _axis(node)
    x, y, w, h = node.rect

    def cut(at: float) -> Cut:
        return Cut((at, y, at, y + h) if axis == 0 else (x, at, x + w, at), (x, y, w, h))
    out = [cut(c.rect[axis] + c.rect[axis + 2] + kerf / 2) for c in node.children[:-1]]
    before, after = _trims(node)
    if before:
        out.append(cut(node.children[0].rect[axis] - kerf / 2))
    if after:
        last = node.children[-1]
        out.append(cut(last.rect[axis] + last.rect[axis + 2] + kerf / 2))
    for c in node.children:
        out += cut_list(c, kerf)
    return out


# -- the solver --------------------------------------------------------------------------------

def _solve(blanks: Sequence[tuple[float, float]], stock: list[Stock], kerf: float, seconds: float,
           knapsack: bool, stages: int, first: str, max1: int, max2: int
           ) -> tuple[list[tuple[Node, int]], dict[int, tuple[float, float]]]:
    """The solver's plans: (cutting tree, stock index) per piece of stock
    sawn, and each blank's corner on its sheet. One kind of sheet in any
    number: fewest sheets, then the largest leftover on the last; else the
    cheapest stock."""
    b = rg.InstanceBuilder()
    one = len(stock) == 1 and stock[0].copies == -1
    if knapsack:
        b.set_objective(ps.Objective.Knapsack)
    else:
        b.set_objective(ps.Objective.BinPackingWithLeftovers if one else ps.Objective.VariableSizedBinPacking)
    b.set_cut_thickness(round(kerf * UNIT))
    b.set_number_of_stages(stages)
    b.set_first_stage_orientation({"vertical": rg.CutOrientation.Vertical,
                                   "horizontal": rg.CutOrientation.Horizontal}[first])
    if max1 > 0:
        b.set_maximum_number_1_cuts(max1)
    if max2 > 0:
        b.set_maximum_number_2_cuts(max2)
    type_of: list[int] = []
    for k, s in enumerate(stock):
        if s.copies == 0:
            continue
        type_of.append(k)
        kwargs: dict[str, Any] = {"copies": s.copies}
        if knapsack and s.copies < 0:
            kwargs["copies"] = 1000
        if not one or knapsack:
            kwargs["cost"] = max(s.cost, 1.0)
        b.add_bin_type(math.floor(s.length * UNIT + 1e-9), math.floor(s.width * UNIT + 1e-9), **kwargs)
    if not type_of or not blanks:
        return [], {}
    for w, h in blanks:
        b.add_item_type(math.ceil(w * UNIT - 1e-9), math.ceil(h * UNIT - 1e-9), oriented=True, copies=1)
    params = rg.OptimizeParameters()
    params.time_limit = seconds
    params.verbosity_level = 0
    solution = rg.optimize(b.build(), params).solution
    trees: list[tuple[Node, int]] = []
    origins: dict[int, tuple[float, float]] = {}
    for k in range(solution.number_of_different_bins()):
        sb = solution.bin(k)
        # A blank is a leaf with an item type; the root carries the id 0 too
        # [found 2026-10-14: blank 0 was placed at the sheet's corner], the
        # other nodes -1 (waste) or -2 (cut further).
        items = [n.item_type_id >= 0 and not n.children and n.f >= 0 for n in sb.nodes]
        for n, item in zip(sb.nodes, items):
            if item:
                origins[int(n.item_type_id)] = (n.l / UNIT, n.b / UNIT)
        nodes = [Node([n.l / UNIT, n.b / UNIT, (n.r - n.l) / UNIT, (n.t - n.b) / UNIT],
                      [int(n.item_type_id)] if item else []) for n, item in zip(sb.nodes, items)]
        root: Node | None = None
        for raw, node in zip(sb.nodes, nodes):
            if raw.f < 0:
                root = node
            else:
                nodes[raw.f].children.append(node)
        assert root is not None
        # The solver sawed whole millimetres of the stock: the last pieces
        # take the rest [found by fuzzing, 2026-10-14: a sheet 400.5 wide
        # lost its half millimetre].
        stock_ = stock[type_of[sb.bin_type_id]]
        root.rect = [0.0, 0.0, stock_.length, stock_.width]
        _widen(root, kerf)
        for _ in range(sb.copies):
            trees.append((_copy(root), type_of[sb.bin_type_id]))
    return trees, origins


def _dump(node: Node, depth: int = 0) -> str:
    """A tree as text, for a bug report."""
    own = f"{'  ' * depth}{[round(v, 1) for v in node.rect]} {node.blanks or ''}"
    return "\n".join([own] + [_dump(c, depth + 1) for c in node.children])


def _copy(node: Node) -> Node:
    return Node(list(node.rect), list(node.blanks), list(node.parts), [_copy(c) for c in node.children])


def _widen(node: Node, kerf: float) -> None:
    """Gives each child the whole piece between its cuts: across the cuts
    the parent's extent, along them up to the next cut (the solver leaves
    space beside a blank in its slot unrecorded; no cut takes it off)."""
    kids = node.children
    if not kids:
        return
    axis = 0 if len({round(c.rect[0], 3) for c in kids}) > 1 else 1
    kids.sort(key=lambda c: c.rect[axis])
    other = 1 - axis
    for c in kids:
        c.rect[other], c.rect[other + 2] = node.rect[other], node.rect[other + 2]
    start, end = node.rect[axis], node.rect[axis] + node.rect[axis + 2]
    for i, c in enumerate(kids):
        lo = start if i == 0 else c.rect[axis]
        hi = end if i == len(kids) - 1 else kids[i + 1].rect[axis] - kerf
        c.rect[axis], c.rect[axis + 2] = lo, hi - lo
        _widen(c, kerf)


#: The order a piece too large for the bed is cut down to its blank in:
#: after the blank along x, along y, then before it.
_TRIMS = ((0, True), (1, True), (0, False), (1, False))


def trim_to_bed(node: Node, sizes: Sequence[tuple[float, float]], origins: dict[int, tuple[float, float]],
                kerf: float, fits_bed: FitsBed) -> Node:
    """Cuts a piece holding one blank down to the blank where the piece is
    larger than the bed."""
    if not node.leaf:
        return Node(list(node.rect), children=[trim_to_bed(c, sizes, origins, kerf, fits_bed)
                                               for c in node.children])
    if not node.blanks or fits_bed(node.rect[2], node.rect[3]):
        return node
    assert len(node.blanks) == 1, "pieces holding several blanks are only joined where they fit the bed"
    bw, bh = sizes[node.blanks[0]]
    bx, by = origins[node.blanks[0]]
    return _trim(node, (bx, by, bw, bh), kerf, fits_bed, _TRIMS)


def _trim(leaf: Node, blank: tuple[float, float, float, float], kerf: float, fits_bed: FitsBed,
          steps: Sequence[tuple[int, bool]]) -> Node:
    if fits_bed(leaf.rect[2], leaf.rect[3]) or not steps:
        return leaf
    (axis, after), rest_steps = steps[0], steps[1:]
    x, y, w, h = leaf.rect
    lo, hi = leaf.rect[axis], leaf.rect[axis] + leaf.rect[axis + 2]
    b_lo, b_hi = blank[axis], blank[axis] + blank[axis + 2]
    if after and hi - b_hi > 1e-6:
        keep, cut = (lo, b_hi), (b_hi + kerf, hi)
    elif not after and b_lo - lo > 1e-6:
        cut, keep = (lo, b_lo - kerf), (b_lo, hi)
    else:
        return _trim(leaf, blank, kerf, fits_bed, rest_steps)

    def piece(span: tuple[float, float]) -> Rect:
        return [span[0], y, span[1] - span[0], h] if axis == 0 else [x, span[0], w, span[1] - span[0]]
    used = _trim(Node(piece(keep), leaf.blanks, leaf.parts), blank, kerf, fits_bed, rest_steps)
    if cut[1] - cut[0] <= 1e-6:            # no wider than the kerf: the blade takes it
        return Node(list(leaf.rect), children=[used])
    rest = Node(piece(cut))
    return Node(list(leaf.rect), children=[used, rest] if after else [rest, used])


# -- judging ------------------------------------------------------------------------------------

#: The settings tried: two or three stages, rips or cross cuts first, with
#: or without a limit on the cuts per stage (a limit on the second cuts needs
#: three stages: the solver refuses it with two).
SETTINGS: list[dict[str, Any]] = [dict(stages=s, first=f, max1=m1, max2=m2)
                                  for s in (2, 3) for f in ("vertical", "horizontal")
                                  for m1, m2 in ((-1, -1), (2, -1), (2, 2)) if not (s == 2 and m2 > 0)]


def best_plan(blanks: Sequence[tuple[float, float]], stock: list[Stock], kerf: float, max_cuts: int,
              fits_bed: FitsBed, keeps: Keeps, seconds: float = 1.0,
              settings: Sequence[dict[str, Any]] = SETTINGS, join: bool = True) -> Plan:
    """Saws `blanks` (w along the grain, h) out of `stock` with each setting
    and keeps the best (see the module's doc); `kerf` in tenths of a
    millimetre (`Workshop.saw_kerf`)."""
    assert abs(kerf * UNIT - round(kerf * UNIT)) < 1e-9, "the kerf is rounded to the plan's unit"
    def solve(knapsack: bool, s: dict[str, Any]) -> tuple[list[tuple[Node, int]], dict[int, tuple[float, float]]]:
        return _solve(blanks, stock, kerf, seconds, knapsack, **s)

    def run(knapsack: bool) -> list[Plan]:
        # The solver lets go of the GIL: the settings run side by side.
        with ThreadPoolExecutor(max_workers=len(settings)) as pool:
            solved = list(pool.map(solve, [knapsack] * len(settings), settings))
        return [_judge(trees, origins, len(blanks), stock, max_cuts, fits_bed, keeps, blanks, kerf, s, join)
                for (trees, origins), s in zip(solved, settings)]

    tried = run(knapsack=False)
    complete = [p for p in tried if not p.unsawn]
    if not complete:
        # The stock on hand cannot take every blank: as many as it can.
        tried = run(knapsack=True)
        tried.sort(key=lambda p: (len(p.unsawn), p.over > 0, p.cost, -p.largest_kept, sum(p.cuts)))
        return tried[0]
    complete.sort(key=lambda p: (p.over > 0, p.cost, -p.largest_kept, sum(p.cuts)))
    return complete[0]


def _judge(trees: list[tuple[Node, int]], origins: dict[int, tuple[float, float]], n_blanks: int,
           stock: list[Stock], max_cuts: int, fits_bed: FitsBed, keeps: Keeps, sizes: Sequence[tuple[float, float]],
           kerf: float, setting: dict[str, Any], join: bool) -> Plan:
    sheets = [Sawn(trim_to_bed(simplify(t, fits_bed, keeps, join), sizes, origins, kerf, fits_bed), k)
              for t, k in trees]
    for (raw, _k), sawn in zip(trees, sheets):
        for leaf in leaves(sawn.tree):
            for bi in leaf.blanks:
                (bx, by), (bw, bh) = origins[bi], sizes[bi]
                x, y, w, h = leaf.rect
                if bx < x - 1e-6 or by < y - 1e-6 or bx + bw > x + w + 1e-6 or by + bh > y + h + 1e-6:
                    raise RuntimeError(f"blank {bi} {(bx, by, bw, bh)} is not in its piece {leaf.rect} "
                                       f"(setting {setting}); the solver's tree: {_dump(raw)}")
    n_cuts = [cuts(s.tree) for s in sheets]
    kept_rects = [leaf.rect for s in sheets for leaf in leaves(s.tree) if kept(leaf, keeps)]
    largest = max((r[2] * r[3] for r in kept_rects), default=0.0)
    cost = sum(stock[s.stock].cost for s in sheets)
    sawn = {bi for s in sheets for leaf in leaves(s.tree) for bi in leaf.blanks}
    return Plan(sheets, [i for i in range(n_blanks) if i not in sawn], dict(setting), n_cuts, cost, largest,
                sum(1 for c in n_cuts if c > max_cuts), origins)
