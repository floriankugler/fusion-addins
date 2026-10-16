"""Nest first, saw after: a layout's parts on blanks the bed takes, the
blanks sawn out of the stock on hand.

Per material [proposed, measured in the experiments, 2026-10-14]:

1. The parts are nested on blank sizes that fit the bed (a grid, plus the
   stock's and the bed's own sizes, each priced by the area it takes of a
   sheet, `_price`, plus `PER_BLANK` for the sawing), on the offcuts on
   hand that the bed takes
   as they are, and on the bed-sized pieces of offcuts it does not take
   (priced next to nothing, so they go first). PackingSolver's variable
   sized bin packing picks the cheapest set; one setting, not several
   tried [Florian, 2026-10-14].
2. Each blank is cut down to its parts, so that what is left of a sheet
   stays in one piece.
3. The blanks are sawn out of the stock (`sawing`), at most `max_cuts`
   cuts a sheet, keeping the cheapest stock, then the largest single
   leftover, then the fewest cuts.
4. When the stock on hand is short (sheets with a count), the parts of the
   blanks it could not take are nested again on what is left, twice more
   at most; what still finds no stock is reported.
5. Refill (`refill`): the bought sheet with the least on it is emptied into
   the room on the others, while that works.
"""
from __future__ import annotations

import math
import time
from collections.abc import Callable
from dataclasses import dataclass

from ..core.errors import LangError
from ..core.layout import layout_hash
from ..core.layout_types import Layout
from . import sawing
from .items import Item, LeftOut, Parts, check_sizes, parts_of_layout
from .nest_types import (NEST_VERSION, BlankOut, CutOut, LeftOutPart, MaterialOut, Nest, NestSettings, PlacedPart,
                         RestOut, SheetOut)
from .packing import KNAPSACK, VARIABLE, Bin, pack
from .refilling import SheetState, refill
from .sawing import Node, PartOn, Stock, leaves
from .verify import verify
from .workshop import Workshop, check_workshop, fits

Log = Callable[[str], None]

#: The blank grid, mm: lengths along the grain and widths across, besides
#: the stock's and the bed's own sizes (the experiments' grid).
LENGTHS = (400.0, 600.0, 800.0, 1000.0, 1200.0, 1400.0, 1600.0, 1800.0, 2000.0)
WIDTHS = (250.0, 400.0, 600.0, 800.0, 1000.0)
#: What sawing a blank out costs, in mm2 of material (0.05 m2).
PER_BLANK = 50_000.0
#: The cost of a piece on hand: next to nothing against a sheet's area
#: (PackingSolver refuses 0).
ON_HAND = 1.0
#: Seconds per saw setting tried, and per refill try.
SAW_SECONDS = 1.0
REFILL_SECONDS = 5.0
#: Rounds of nesting again on what is left when the stock is short.
ROUNDS = 3
#: Tries of a nest that found nothing in its time, each twice as long.
RETRIES = 4


@dataclass
class Options:
    """How hard the solvers try: the nest's time per material (unless
    given, `Workshop.nest_seconds`: 0.6 s a part, 5 s to the workshop's
    `seconds`), the mode (`anytime`: the best within the time;
    `deterministic`: one fixed search, as long as it takes), the saw's time
    per setting, refill's per try (0: no refill)."""
    seconds: float | None = None
    mode: str = "anytime"
    saw_seconds: float = SAW_SECONDS
    refill_seconds: float = REFILL_SECONDS


def nest_layout(layout: Layout, workshop: Workshop, *, source: str = "", material: str | None = None,
                options: Options | None = None, log: Log | None = None) -> tuple[Nest, Parts]:
    """Nests the layout's parts (of every material, or the one named) for
    the workshop; returns the nest file's content and the parts nested."""
    options = options or Options()
    say: Log = log or (lambda _: None)
    check_workshop(workshop)
    parts = parts_of_layout(layout, workshop.spacing, material)
    if material is not None and material not in parts.by_material:
        names = sorted({p["material"] for m in layout["modules"] for p in m["parts"]})
        raise LangError(f"No part of {material} to nest (the materials: {', '.join(names)}).")
    check_sizes(parts, workshop)
    materials: list[MaterialOut] = []
    problems: list[str] = []
    for name in sorted(parts.by_material):
        items = parts.by_material[name]
        t0 = time.perf_counter()
        out = nest_material(items, name, workshop, options, say)
        say(f"{name}: {len(items)} parts on {len(out['sheets'])} pieces of stock "
            f"(cuts {[len(s['cuts']) for s in out['sheets']]}) in {time.perf_counter() - t0:.1f} s")
        if out["unplaced"]:
            problems.append(f"{name}: the stock on hand takes not every part; left over: "
                            f"{', '.join(out['unplaced'])}")
        problems += [f"{name}: {p}" for p in verify(out, items, workshop)]
        materials.append(out)
    assert workshop.bed is not None
    settings: NestSettings = {
        "bed": list(workshop.bed), "spacing": workshop.spacing, "margin": workshop.margin, "kerf": workshop.kerf,
        "max_cuts": workshop.max_cuts, "keep_across": workshop.keep_across, "keep_area": workshop.keep_area,
        "seconds": options.seconds if options.seconds is not None else workshop.seconds,
        "sheets": [(f"{s.material}:" if s.material else "") + s.label() for s in workshop.sheets],
        "offcuts": [o.label() for o in workshop.offcuts],
    }
    nest: Nest = {
        "version": NEST_VERSION, "source": source, "layout_hash": layout_hash(layout), "settings": settings,
        "materials": materials, "left_out": [_left_out(p) for p in parts.left_out], "problems": problems,
    }
    return nest, parts


def _left_out(p: LeftOut) -> LeftOutPart:
    return {"path": p.path, "material": p.material, "why": p.why}


# -- one material ----------------------------------------------------------------------------------

@dataclass
class _Stock:
    """The stock of one material as it is used up."""
    sawn: list[Stock]          # sheets, and offcuts larger than the bed
    direct: list[tuple[float, float]]   # offcuts the bed takes as they are
    direct_left: list[bool]


def nest_material(items: list[Item], material: str, workshop: Workshop, options: Options, log: Log) -> MaterialOut:
    assert workshop.bed is not None
    seconds = options.seconds if options.seconds is not None else workshop.nest_seconds(len(items))
    stock = _stock_of(material, workshop)
    remaining = list(range(len(items)))
    states: list[SheetState] = []
    notes: list[str] = []
    for round_ in range(ROUNDS):
        if not remaining:
            break
        new, remaining, round_notes = _nest_round(items, remaining, stock, workshop, seconds, options)
        states += new
        notes += [f"round {round_ + 1}: {n}" if round_ else n for n in round_notes]
    if options.refill_seconds > 0 and len(states) > 1:
        before = len(states)
        states = refill(items, states, workshop, options.refill_seconds, options.mode, log)
        if len(states) < before:
            notes.append(f"refill: {before - len(states)} sheet(s) emptied into the others")
    # Offcuts first, as they are used first; then the sheets as sawn.
    states.sort(key=lambda s: s.kind != "offcut")
    return _material_out(items, material, states, remaining, workshop, notes)


def _stock_of(material: str, workshop: Workshop) -> _Stock:
    sawn: list[Stock] = []
    for k, s in enumerate(workshop.sheets_for(material)):
        sawn.append(Stock(s.length, s.width, s.count if s.count is not None else -1, s.length * s.width, "sheet", k))
    direct: list[tuple[float, float]] = []
    for k, o in enumerate(workshop.offcuts_for(material)):
        if workshop.fits_bed(o.length, o.width):
            direct.append((o.length, o.width))
        else:
            sawn.append(Stock(o.length, o.width, 1, ON_HAND, "offcut", k))
    return _Stock(sawn, direct, [True] * len(direct))


def _blank_types(stock: _Stock, workshop: Workshop) -> tuple[list[Bin], list[str]]:
    """The bins the nest picks from, and what each is: `grid`, `piece`
    (of an offcut larger than the bed) or `direct` (an offcut the bed takes)."""
    assert workshop.bed is not None
    bed = workshop.bed
    available = [s for s in stock.sawn if s.copies != 0]
    sheets = [s for s in available if s.kind == "sheet"]
    # In the saw's tenths of a millimetre, rounded down, so that a blank as
    # long as the bed is not sawn longer [found by fuzzing, 2026-10-15: a
    # bed 846.352 wide took a blank sawn 846.4].
    lengths = sorted(set(LENGTHS) | {_tenth(s.length) for s in sheets} | {_tenth(v) for v in bed})
    widths = sorted(set(WIDTHS) | {_tenth(s.width) for s in sheets} | {_tenth(v) for v in bed})
    bins: list[Bin] = []
    kinds: list[str] = []
    for w in lengths:
        for h in widths:
            holding = [s for s in sheets if w <= s.length + 1e-9 and h <= s.width + 1e-9]
            if min(w, h) > 2 * workshop.margin and fits(w, h, bed) and holding:
                bins.append(Bin(w, h, -1, _price(w, h, holding, workshop.kerf) + PER_BLANK))
                kinds.append("grid")
    for s in available:
        if s.kind == "offcut":
            for w, h in _split_to_bed(s.length, s.width, bed, workshop.saw_kerf):
                if min(w, h) > 2 * workshop.margin:
                    bins.append(Bin(_tenth(w), _tenth(h), 1, ON_HAND))
                    kinds.append("piece")
    for k, (w, h) in enumerate(stock.direct):
        if stock.direct_left[k]:
            bins.append(Bin(w, h, 1, ON_HAND))
            kinds.append(f"direct{k}")
    return bins, kinds


def _nest_round(items: list[Item], indices: list[int], stock: _Stock, workshop: Workshop, seconds: float,
                options: Options) -> tuple[list[SheetState], list[int], list[str]]:
    """Nests `indices` on blanks and saws them; returns the stock used, the
    parts left over, and notes."""
    assert workshop.bed is not None
    bins, kinds = _blank_types(stock, workshop)
    t0 = time.perf_counter()
    # The grid's blanks are as many as needed, so every part fits one: a nest
    # that leaves parts over found nothing in its time (62 parts on 30 blank
    # sizes need several seconds), and is given twice as long.
    tries = 0
    while True:
        result = pack(items, indices, bins, workshop.spacing, workshop.margin, VARIABLE, seconds * 2 ** tries,
                      options.mode)
        tries += 1
        if not result.unplaced or tries == RETRIES or options.mode != "anytime":
            break
    if result.unplaced:
        # As many as fit.
        result = pack(items, indices, bins, workshop.spacing, workshop.margin, KNAPSACK, seconds, options.mode)
    notes = [f"nest: {len(result.packed)} blanks in {time.perf_counter() - t0:.1f} s"
             + (f" ({tries} tries)" if tries > 1 else "")]
    left = list(result.unplaced)
    states: list[SheetState] = []
    blank_sizes: list[tuple[float, float]] = []
    blank_parts: list[list[PartOn]] = []
    for packed in result.packed:
        kind = kinds[packed.bin]
        bin_ = bins[packed.bin]
        parts = [PartOn(p.item, p.turn, p.at) for p in packed.placements]
        if kind.startswith("direct"):
            k = int(kind[len("direct"):])
            stock.direct_left[k] = False
            w, h = stock.direct[k]
            states.append(SheetState(Node([0.0, 0.0, w, h], parts=parts), (w, h), "offcut", f"{w:g}x{h:g}"))
            continue
        shapes = [items[p.item].placed(p.turn, p.at, solver=True) for p in packed.placements]
        w = min(bin_.width, math.ceil(max(s.bounds[2] for s in shapes) + workshop.margin - 1e-9))
        h = min(bin_.height, math.ceil(max(s.bounds[3] for s in shapes) + workshop.margin - 1e-9))
        blank_sizes.append((w, h))
        blank_parts.append(parts)
    if blank_sizes:
        t1 = time.perf_counter()
        # Blanks side by side are one piece only where the parts across the
        # cut left out keep the spacing.
        join = 2 * workshop.margin + workshop.saw_kerf >= workshop.spacing - 1e-9
        plan = sawing.best_plan(blank_sizes, stock.sawn, workshop.saw_kerf, workshop.max_cuts, workshop.fits_bed,
                                workshop.keeps, options.saw_seconds, join=join)
        notes.append(f"saw: {plan.setting}, cuts {plan.cuts}, {time.perf_counter() - t1:.1f} s")
        used: dict[int, int] = {}
        for sawn in plan.sheets:
            s = stock.sawn[sawn.stock]
            used[sawn.stock] = used.get(sawn.stock, 0) + 1
            for leaf in leaves(sawn.tree):
                for bi in leaf.blanks:
                    ox, oy = plan.origins[bi]
                    leaf.parts = leaf.parts + [PartOn(p.item, p.turn, (ox + p.at[0], oy + p.at[1]))
                                               for p in blank_parts[bi]]
            states.append(SheetState(sawn.tree, (s.length, s.width), s.kind, f"{s.length:g}x{s.width:g}"))
        for k, n in used.items():
            s = stock.sawn[k]
            if s.copies > 0:
                stock.sawn[k] = Stock(s.length, s.width, max(0, s.copies - n), s.cost, s.kind, s.key)
        for bi in plan.unsawn:
            left += [p.item for p in blank_parts[bi]]
    return states, sorted(left), notes


def _tenth(v: float) -> float:
    """`v` rounded down to a tenth of a millimetre, the saw's unit."""
    return math.floor(v * sawing.UNIT + 1e-9) / sawing.UNIT


def _price(w: float, h: float, sheets: list[Stock], kerf: float) -> float:
    """A grid blank's price: the area it takes of the sheet that suits it
    best, counting with it a strip beside it too narrow for the smallest
    blank, which can only be waste. Priced by their own area, blanks of the
    bed's size won (2000 x 1000 on a 2470 x 1240 sheet, one a sheet, the
    strips beside them waste): for the examples' 62 parts of birch 15, 7
    sheets before refill and 14.8 m2 used, against 5 sheets and 13.0 m2
    priced so [measured 2026-10-14; with every part's grain along the sheet
    14.3 against 11.9 m2]."""
    best = math.inf
    for s in sheets:
        ew = s.length if s.length - w - kerf < LENGTHS[0] else w
        eh = s.width if s.width - h - kerf < WIDTHS[0] else h
        best = min(best, ew * eh)
    return best


def _split_to_bed(w: float, h: float, bed: tuple[float, float], kerf: float) -> list[tuple[float, float]]:
    """A piece of stock in pieces the bed takes: the largest from its
    corner, then the rest to the right and above, again (straight cuts)."""
    if w <= 0 or h <= 0:
        return []
    if fits(w, h, bed):
        return [(w, h)]
    options = [(min(w, bed[0]), min(h, bed[1])), (min(w, bed[1]), min(h, bed[0]))]
    cw, ch = max(options, key=lambda o: o[0] * o[1])
    return ([(cw, ch)] + _split_to_bed(w - cw - kerf, h, bed, kerf) + _split_to_bed(cw, h - ch - kerf, bed, kerf))


# -- the material's part of the nest file --------------------------------------------------------------

def _material_out(items: list[Item], material: str, states: list[SheetState], remaining: list[int],
                  workshop: Workshop, notes: list[str]) -> MaterialOut:
    sheets: list[SheetOut] = []
    bought: dict[str, int] = {}
    offcuts: list[str] = []
    stock_area = kept_area = parts_area = 0.0
    for n, state in enumerate(states, 1):
        blanks: list[BlankOut] = []
        rests: list[RestOut] = []
        for leaf in leaves(state.tree):
            x, y, w, h = leaf.rect
            if leaf.used:
                placed: list[PlacedPart] = []
                for p in leaf.parts:
                    item = items[p.item]
                    at = (p.at[0] - x, p.at[1] - y)
                    placed.append({"path": item.path, "up": item.up, "turn": p.turn, "at": [at[0], at[1]],
                                   "transform": item.frame.placed(p.turn, at)})
                    parts_area += item.area
                blanks.append({"name": f"{n}.{len(blanks) + 1}", "rect": [x, y, w, h], "parts": placed})
            else:
                keep = workshop.keeps(w, h)
                rests.append({"rect": [x, y, w, h], "keep": keep})
                if keep:
                    kept_area += w * h
        cuts: list[CutOut] = [{"line": list(c.line), "piece": list(c.piece)}
                              for c in sawing.cut_list(state.tree, workshop.saw_kerf)]
        sheets.append({"name": str(n), "stock": "offcut" if state.kind == "offcut" else "sheet",
                       "size": [state.size[0], state.size[1]], "cuts": cuts, "blanks": blanks, "rests": rests})
        stock_area += state.size[0] * state.size[1]
        if state.kind == "sheet":
            bought[state.label] = bought.get(state.label, 0) + 1
        else:
            offcuts.append(state.label)
    return {
        "material": material, "thickness": items[0].thickness if items else 0.0, "sheets": sheets,
        "bought": bought, "offcuts_used": offcuts,
        "parts_area": parts_area / 1e6, "stock_area": stock_area / 1e6, "kept_area": kept_area / 1e6,
        "used_area": (stock_area - kept_area) / 1e6,
        "unplaced": [items[i].path for i in remaining], "notes": notes,
    }
