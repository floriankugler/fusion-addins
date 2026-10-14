"""Saw blanks out of sheets: PackingSolver's guillotine solver for
rectangles, then the plan made as simple as it can be, judged by the number
of cuts and the leftover.

A plan is the solver's cutting tree: a sheet, cut into strips (first
cuts), each cut into pieces (second cuts), and so on; a leaf is the rest
(waste, or the residual of the last sheet) or holds blanks. Before the cuts
are counted, the cuts that are not needed are left out, between pieces side
by side (and so, from the leaves up, within any piece of the sheet):

- two rests: one piece of rest, bigger;
- pieces that hold blanks, and rests too small to keep, as long as they
  then fit the bed together: one piece, machined at once (each blank's
  parts stay where they are). Two blanks the nest made apart but the saw
  put side by side are one blank when the bed takes them [Florian,
  2026-10-14: two 591 high blanks side by side, 1416 x 646 together, had
  been cut apart];
- a rest too small to keep, beside a piece that is cut further: the pieces
  along it take it along (each grows across it), when every blank that
  grows still fits the bed (a 17 mm strip along three blanks).

A node left with one child is that child. A node with k children takes
k - 1 cuts; a sheet's cuts are the sum. A rest at least `KEEP` across and
of `KEEP_AREA` is stock, kept; smaller ones are waste.

`best_plan` saws with a few settings (two or three stages, cross cuts or
rips first, with or without a limit on the cuts per stage), each in a
second or so, and keeps, in this order: no sheet over `max_cuts`; fewest
sheets; the largest single piece of stock; fewest cuts.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field

import packingsolver as ps
import packingsolver.rectangleguillotine as rg

KEEP = 200.0
KEEP_AREA = 0.1e6


@dataclass
class Node:
    rect: list[float]                  # x, y, w, h on the sheet: the piece between its cuts
    # For a leaf, the blanks it holds: each blank's index and its own corner
    # on the sheet, where its parts are measured from.
    blanks: list[tuple[int, tuple[float, float]]] = field(default_factory=list)
    children: list["Node"] = field(default_factory=list)

    @property
    def leaf(self) -> bool:
        return not self.children

    @property
    def rest(self) -> bool:
        return self.leaf and not self.blanks

    @property
    def stock(self) -> bool:
        return self.rest and useful(self.rect[2], self.rect[3])


def useful(w: float, h: float) -> bool:
    return min(w, h) >= KEEP and w * h >= KEEP_AREA


def fits_bed(w: float, h: float, bed) -> bool:
    return (w <= bed[0] and h <= bed[1]) or (w <= bed[1] and h <= bed[0])


def joined(a: Node, b: Node) -> list[float]:
    x0, y0 = min(a.rect[0], b.rect[0]), min(a.rect[1], b.rect[1])
    x1 = max(a.rect[0] + a.rect[2], b.rect[0] + b.rect[2])
    y1 = max(a.rect[1] + a.rect[3], b.rect[1] + b.rect[3])
    return [x0, y0, x1 - x0, y1 - y0]


def side_by_side(kids: list[Node]) -> int:
    """The axis along which a node's pieces lie side by side (0: x)."""
    a, b = kids[0], kids[1]
    return 0 if a.rect[0] + a.rect[2] <= b.rect[0] + 1e-6 else 1


def grown(node: Node, axis: int, at_start: bool, amount: float, bed) -> Node | None:
    """`node` grown by `amount` along `axis` (at its start or its end), the
    growth passed on to the pieces along that side; None when a blank would
    no longer fit the bed."""
    r = list(node.rect)
    if at_start:
        r[axis] -= amount
    r[axis + 2] += amount
    if node.leaf:
        if node.blanks and not fits_bed(r[2], r[3], bed):
            return None
        return Node(r, node.blanks)
    kids = list(node.children)
    if len(kids) > 1 and side_by_side(kids) == axis:
        k = 0 if at_start else len(kids) - 1
        g = grown(kids[k], axis, at_start, amount, bed)
        if g is None:
            return None
        kids[k] = g
    else:
        new = []
        for c in kids:
            g = grown(c, axis, at_start, amount, bed)
            if g is None:
                return None
            new.append(g)
        kids = new
    return Node(r, [], kids)


def simplify(node: Node, bed) -> Node:
    """Leave out the cuts that are not needed (see the module's doc)."""
    if node.leaf:
        return node
    kids = [simplify(c, bed) for c in node.children]
    changed = True
    while changed:
        changed = False
        for i in range(len(kids) - 1):
            a, b = kids[i], kids[i + 1]
            r = joined(a, b)
            if a.leaf and b.leaf:
                if a.rest and b.rest:
                    kids[i:i + 2] = [Node(r)]
                elif not a.stock and not b.stock and fits_bed(r[2], r[3], bed):
                    kids[i:i + 2] = [Node(r, a.blanks + b.blanks)]
                else:
                    continue
            elif a.rest and not a.stock and not b.leaf:
                axis = side_by_side(kids)
                g = grown(b, axis, True, b.rect[axis] - a.rect[axis], bed)
                if g is None:
                    continue
                kids[i:i + 2] = [simplify(g, bed)]
            elif b.rest and not b.stock and not a.leaf:
                axis = side_by_side(kids)
                g = grown(a, axis, False, (b.rect[axis] + b.rect[axis + 2]) - (a.rect[axis] + a.rect[axis + 2]), bed)
                if g is None:
                    continue
                kids[i:i + 2] = [simplify(g, bed)]
            else:
                continue
            changed = True
            break
    if len(kids) == 1:
        only = kids[0]
        # The one child takes the node's whole place.
        if only.leaf and (only.rest or fits_bed(node.rect[2], node.rect[3], bed)):
            return Node(list(node.rect), only.blanks)
        return only
    return Node(list(node.rect), [], kids)


def cuts(node: Node) -> int:
    return 0 if node.leaf else len(node.children) - 1 + sum(cuts(c) for c in node.children)


def leaves(node: Node) -> list[Node]:
    return [node] if node.leaf else [l for c in node.children for l in leaves(c)]


def solve(blanks, sheet, kerf, seconds, stages=3, first="vertical", max1=-1, max2=-1, objective="leftovers"):
    """The solver's plans: one cutting tree per sheet."""
    b = rg.InstanceBuilder()
    b.set_objective(ps.Objective.BinPackingWithLeftovers if objective == "leftovers" else ps.Objective.BinPacking)
    b.set_cut_thickness(int(kerf))
    b.set_number_of_stages(stages)
    b.set_first_stage_orientation({"vertical": rg.CutOrientation.Vertical,
                                   "horizontal": rg.CutOrientation.Horizontal,
                                   "any": rg.CutOrientation.Any}[first])
    if max1 > 0:
        b.set_maximum_number_1_cuts(max1)
    if max2 > 0:
        b.set_maximum_number_2_cuts(max2)
    b.add_bin_type(int(sheet[0]), int(sheet[1]), copies=-1)
    for w, h in blanks:
        b.add_item_type(int(math.ceil(w)), int(math.ceil(h)), oriented=True, copies=1)
    params = rg.OptimizeParameters()
    params.time_limit = seconds
    params.verbosity_level = 0
    sol = rg.optimize(b.build(), params).solution
    trees = []
    for k in range(sol.number_of_different_bins()):
        sb = sol.bin(k)
        nodes = [Node([n.l, n.b, n.r - n.l, n.t - n.b],
                      [(n.item_type_id, (n.l, n.b))] if n.item_type_id >= 0 else []) for n in sb.nodes]
        root = None
        for raw, node in zip(sb.nodes, nodes):
            if raw.f < 0:
                root = node
            else:
                nodes[raw.f].children.append(node)
        widen(root, kerf)
        for _ in range(sb.copies):
            trees.append(root)
    return trees


def widen(node: Node, kerf: float) -> None:
    """Give each child the whole piece between its cuts: across the cuts the
    parent's extent, along them up to the next cut (the solver leaves space
    beside a blank in its slot unrecorded; no cut takes it off)."""
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
        widen(c, kerf)


# A limit on the 2-cuts needs three stages (the solver refuses it with two).
SETTINGS = [dict(stages=s, first=f, max1=m1, max2=m2)
            for s in (2, 3) for f in ("vertical", "horizontal")
            for m1, m2 in ((-1, -1), (2, -1), (2, 2)) if not (s == 2 and m2 > 0)]


def judge(trees: list[Node], bed, max_cuts: int) -> dict:
    plans = [simplify(t, bed) for t in trees]
    n_cuts = [cuts(p) for p in plans]
    stock = [l.rect for p in plans for l in leaves(p) if l.stock]
    largest = max((r[2] * r[3] for r in stock), default=0.0)
    return {"plans": plans, "cuts": n_cuts, "sheets": len(plans), "largest_stock": largest,
            "stock": sum(r[2] * r[3] for r in stock), "stock_pieces": len(stock),
            "over": sum(1 for c in n_cuts if c > max_cuts)}


def best_plan(blanks, sheet, bed, kerf, max_cuts=5, seconds=1.0, settings=SETTINGS):
    """Saw with each setting; keep: no sheet over `max_cuts`, fewest sheets,
    the largest single piece of stock, fewest cuts."""
    tried = []
    for s in settings:
        r = judge(solve(blanks, sheet, kerf, seconds, **s), bed, max_cuts)
        r["setting"] = s
        tried.append(r)
    tried.sort(key=lambda r: (r["over"] > 0, r["sheets"], -r["largest_stock"], sum(r["cuts"])))
    return tried[0], tried
