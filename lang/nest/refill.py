"""Refill: emptying a bought sheet into the room left on the others.

The parts of the bought sheet with the least part area are nested into
the room the others have left: the pieces holding blanks, around their
parts (the parts kept the spacing off, almost free), and each sheet's
largest rest, cut down to what it takes (priced by its area, offered only
while the sheet has two cuts to spare under `max_cuts`). When all fit, that
sheet is not needed; again while it works. An offcut on hand is never
emptied, only a sheet bought [the experiments, 2026-10-14: it took a sheet
back now and then, 11 to 10].
"""
from __future__ import annotations

import math
from collections.abc import Callable
from dataclasses import dataclass

from .items import Item
from .packing import VARIABLE, Bin, pack
from .sawing import Node, PartOn, cuts, leaves
from .workshop import Workshop, fits

Log = Callable[[str], None]


@dataclass
class SheetState:
    """A piece of stock as it is being sawn: its plan, size and kind."""
    tree: Node
    size: tuple[float, float]
    #: "sheet" (bought) or "offcut" (on hand).
    kind: str
    #: Its label (`2470x1240`), for the bought count.
    label: str


def area_on(sheet: SheetState, items: list[Item]) -> float:
    return sum(items[p.item].area for leaf in leaves(sheet.tree) for p in leaf.parts)


def refill(items: list[Item], sheets: list[SheetState], workshop: Workshop, seconds: float, mode: str,
           log: Log) -> list[SheetState]:
    """The sheets with as many bought ones emptied as works (see the
    module's doc)."""
    sheets = list(sheets)
    margin = workshop.margin
    while len(sheets) > 1:
        bought = [k for k, s in enumerate(sheets) if s.kind == "sheet"]
        if not bought:
            break
        k = min(bought, key=lambda k: area_on(sheets[k], items))
        moving = [p.item for leaf in leaves(sheets[k].tree) for p in leaf.parts]
        if not moving:
            sheets.pop(k)
            continue
        slots: list[tuple[Node, bool, tuple[float, float]]] = []     # (leaf, used, the room offered)
        bins: list[Bin] = []
        for si, s in enumerate(sheets):
            if si == k:
                continue
            for leaf in leaves(s.tree):
                if leaf.parts:
                    x, y, w, h = leaf.rect
                    defects = [items[p.item].placed(p.turn, (p.at[0] - x, p.at[1] - y), solver=True)
                               for p in leaf.parts]
                    slots.append((leaf, True, (w, h)))
                    bins.append(Bin(w, h, 1, 1.0, defects))
            if cuts(s.tree) + 2 <= workshop.max_cuts:
                rests = [(leaf, _room(leaf, workshop)) for leaf in leaves(s.tree) if not leaf.parts]
                rests = [(leaf, room) for leaf, room in rests if min(room) > 2 * margin + 10]
                if rests:
                    leaf, room = max(rests, key=lambda r: r[1][0] * r[1][1])
                    slots.append((leaf, False, room))
                    bins.append(Bin(room[0], room[1], 1, room[0] * room[1]))
        if not bins:
            break
        result = pack(items, moving, bins, workshop.spacing, margin, VARIABLE, seconds, mode)
        if result.unplaced or not result.packed:
            log(f"refill: the {len(moving)} parts of a {sheets[k].label} sheet do not fit the room on the others")
            break
        rests_cut = 0
        for packed in result.packed:
            leaf, used, room = slots[packed.bin]
            x, y = leaf.rect[0], leaf.rect[1]
            placed = [PartOn(p.item, p.turn, (x + p.at[0], y + p.at[1])) for p in packed.placements]
            if used:
                leaf.parts = leaf.parts + placed
            else:
                rests_cut += 1
                shapes = [items[p.item].placed(p.turn, p.at, solver=True) for p in packed.placements]
                w2 = min(room[0], math.ceil(max(s.bounds[2] for s in shapes) + margin))
                h2 = min(room[1], math.ceil(max(s.bounds[3] for s in shapes) + margin))
                _cut_down(leaf, w2, h2, placed, workshop)
        log(f"refill: the {len(moving)} parts of a {sheets[k].label} sheet moved into the room on the others "
            f"({rests_cut} rests cut into)")
        sheets.pop(k)
    return sheets


def _room(leaf: Node, workshop: Workshop) -> tuple[float, float]:
    """The part of a rest from its corner that a blank can be: what the bed
    takes, leaving room for the kerf where it must be cut."""
    assert workshop.bed is not None
    w, h = leaf.rect[2], leaf.rect[3]
    if fits(w, h, workshop.bed):
        return w, h
    options: list[tuple[float, float]] = []
    for bw, bh in (workshop.bed, (workshop.bed[1], workshop.bed[0])):
        cw = w if w <= bw else min(bw, w - workshop.kerf - 1)
        ch = h if h <= bh else min(bh, h - workshop.kerf - 1)
        options.append((cw, ch))
    return max(options, key=lambda o: o[0] * o[1])


def _cut_down(leaf: Node, w2: float, h2: float, parts: list[PartOn], workshop: Workshop) -> None:
    """Turns a rest into the piece holding `parts`, w2 x h2 from its corner,
    and what is cut off it: off to the right, then above, where that is
    worth keeping or the piece would not fit the bed; anything else stays
    with the piece."""
    assert workshop.bed is not None
    kerf = workshop.kerf
    x, y, w, h = leaf.rect
    right = w - w2 - kerf
    if right > 0 and (workshop.keeps(right, h) or not fits(w, h, workshop.bed)):
        main = Node([x, y, w2, h])
        leaf.children = [main, Node([x + w2 + kerf, y, right, h])]
        w = w2
    else:
        main = leaf
    above = h - h2 - kerf
    if above > 0 and (workshop.keeps(w, above) or not fits(w, h, workshop.bed)):
        piece = Node([x, y, w, h2], parts=parts)
        main.children = [piece, Node([x, y + h2 + kerf, w, above])]
    else:
        if main is leaf:
            leaf.parts = parts
        else:
            main.parts = parts
