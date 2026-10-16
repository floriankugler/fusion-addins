"""Checks a nest result the way a sawyer and the machine would, apart from
the solvers that made it: every nest is checked before it is written, and
the tests and fuzz tests check with it too.

Per piece of stock: its pieces (blanks and rests) lie on it apart from each
other, and with the saw's cuts they cover it whole; each cut is a straight
line through the piece it splits, edge to edge, crossing no other piece; at
most `max_cuts` cuts; each blank goes on the bed but a `nest(False)`
board's own; a rest is marked kept exactly when the nest keeps it. Per
blank: each part's true machine outline, turned and moved as the nest
says, lies on the blank the margin in from its edge and at least the
larger of the two parts' spacings from every other part, turned by one of
its own turns; an own blank holds its board alone, its outline whole,
within it. Per material: every part is placed once, or listed as left
over; the sheets bought are the material's size, and no more pieces of
the stock on hand are used than there are.
"""
from __future__ import annotations

from collections import Counter

from shapely import Polygon, STRtree, box, unary_union

from .items import Item
from .nest_types import MaterialOut, SheetOut
from .workshop import Workshop, fits

#: How far (mm) a part may come nearer an edge or another part than asked:
#: the solver's own arithmetic.
TOLERANCE = 1e-4


def verify(out: MaterialOut, items: list[Item], workshop: Workshop) -> list[str]:
    assert workshop.bed is not None
    problems: list[str] = []
    by_path = {item.path: item for item in items}
    seen: Counter[str] = Counter()
    for sheet in out["sheets"]:
        problems += _check_sheet(sheet, workshop)
        for blank in sheet["blanks"]:
            name = f"blank {blank['name']}"
            _x, _y, w, h = blank["rect"]
            own = [by_path[p["path"]].own for p in blank["parts"] if p["path"] in by_path]
            if any(own) != blank["own_blank"] or (any(own) and len(blank["parts"]) != 1):
                problems.append(f"{name}: an own blank holds its board alone, and is marked so")
            if not blank["own_blank"] and not fits(w, h, workshop.bed):
                problems.append(f"{name} ({w:g} x {h:g}) does not fit the bed")
            m = 0.0 if blank["own_blank"] else workshop.margin
            inner = box(m - TOLERANCE, m - TOLERANCE, w - m + TOLERANCE, h - m + TOLERANCE)
            shapes: list[Polygon] = []
            paths: list[str] = []
            for part in blank["parts"]:
                item = by_path.get(part["path"])
                if item is None:
                    problems.append(f"{name}: {part['path']} is no part of this material")
                    continue
                seen[part["path"]] += 1
                if not any(abs((part["turn"] - t + 180) % 360 - 180) < 1e-9 for t in item.turns):
                    problems.append(f"{part['path']}: turned {part['turn']:g}, not one of its turns {item.turns}")
                shape = item.placed(part["turn"], (part["at"][0], part["at"][1]))
                if not inner.contains(shape):
                    problems.append(f"{part['path']}: not the margin {m:g} inside {name}")
                shapes.append(shape)
                paths.append(part["path"])
            problems += _check_spacing(shapes, [by_path[p] for p in paths])
    for item in items:
        n = seen[item.path]
        if item.path in out["unplaced"]:
            if n:
                problems.append(f"{item.path}: placed {n} times and listed as left over")
        elif n != 1:
            problems.append(f"{item.path}: placed {n} times")
    problems += _check_stock(out, workshop)
    return problems


def _check_sheet(s: SheetOut, workshop: Workshop) -> list[str]:
    problems: list[str] = []
    name = f"sheet {s['name']}"
    length, width = s["size"]
    whole = box(0, 0, length, width)
    pieces: list[Polygon] = []
    for rect in [b["rect"] for b in s["blanks"]] + [r["rect"] for r in s["rests"]]:
        x, y, w, h = rect
        if w <= 0 or h <= 0:
            problems.append(f"{name}: a piece of no size {rect}")
            continue
        p = box(x, y, x + w, y + h)
        if not whole.buffer(1e-6).contains(p):
            problems.append(f"{name}: the piece {rect} is off the sheet")
        pieces.append(p)
    tree = STRtree(pieces)
    for i, p in enumerate(pieces):
        for j in tree.query(p):
            if j > i and p.intersection(pieces[int(j)]).area > 1e-6:
                problems.append(f"{name}: two pieces overlap")
    kerf = workshop.saw_kerf
    strips: list[Polygon] = []
    for k, cut in enumerate(s["cuts"]):
        x0, y0, x1, y1 = cut["line"]
        px, py, pw, ph = cut["piece"]
        across = x0 == x1
        if not (across or y0 == y1):
            problems.append(f"{name}: cut {k + 1} is not straight along x or y")
            continue
        edge_to_edge = (abs(y0 - py) < 1e-6 and abs(y1 - (py + ph)) < 1e-6) if across else \
            (abs(x0 - px) < 1e-6 and abs(x1 - (px + pw)) < 1e-6)
        if not edge_to_edge:
            problems.append(f"{name}: cut {k + 1} does not run through its piece")
        strip = box(x0 - kerf / 2, y0, x1 + kerf / 2, y1) if across else box(x0, y0 - kerf / 2, x1, y1 + kerf / 2)
        for j in tree.query(strip):
            if strip.intersection(pieces[int(j)]).area > 1e-6:
                problems.append(f"{name}: cut {k + 1} goes through a piece")
                break
        strips.append(strip)
    # A trim's strip runs past the piece's edge, off the sheet or over the
    # strip of the cut before it.
    covered = unary_union(pieces + strips).intersection(whole).area
    if abs(covered - length * width) > 1e-3 * max(1.0, kerf) * (length + width):
        problems.append(f"{name}: its pieces and cuts cover {covered / 1e6:.4f} m2 of {length * width / 1e6:.4f}")
    if len(s["cuts"]) > workshop.max_cuts:
        problems.append(f"{name}: {len(s['cuts'])} cuts, more than {workshop.max_cuts}")
    for r in s["rests"]:
        if r["keep"] != workshop.keeps(r["rect"][2], r["rect"][3]):
            problems.append(f"{name}: the rest {r['rect']} is marked {'kept' if r['keep'] else 'waste'}")
    return problems


def _check_spacing(shapes: list[Polygon], items: list[Item]) -> list[str]:
    """Each two parts at least the larger of their spacings apart."""
    problems: list[str] = []
    if len(shapes) < 2:
        return problems
    tree = STRtree(shapes)
    widest = max(item.spacing for item in items)
    for i, s in enumerate(shapes):
        for j in tree.query(s, predicate="dwithin", distance=widest - TOLERANCE):
            j = int(j)
            spacing = max(items[i].spacing, items[j].spacing)
            if j > i and (gap := s.distance(shapes[j])) < spacing - TOLERANCE:
                problems.append(f"{items[i].path} and {items[j].path}: {gap:.4f} apart, less than {spacing:g}"
                                if gap > 0 else f"{items[i].path} and {items[j].path} overlap")
    return problems


def _check_stock(out: MaterialOut, workshop: Workshop) -> list[str]:
    problems: list[str] = []
    material = out["material"]
    sheet = workshop.sheet_for(material)
    for key, n in out["bought"].items():
        if sheet is None or key != sheet.label():
            problems.append(f"{n} sheets {key} bought, not the material's size "
                            f"({sheet.label() if sheet else 'none to buy'})")
    on_hand: Counter[str] = Counter()
    for o in workshop.on_hand_for(material):
        on_hand[o.label()] += o.count
    for key, n in Counter(out["on_hand_used"]).items():
        if n > on_hand[key]:
            problems.append(f"{n} pieces {key} on hand used, {on_hand[key]} on hand")
    if sum(out["bought"].values()) + len(out["on_hand_used"]) != len(out["sheets"]):
        problems.append("the stock bought and on hand used is not the stock sawn")
    return problems
