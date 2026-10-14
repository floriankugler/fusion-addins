"""Checks a nest result the way a sawyer and the machine would, apart from
the solvers that made it: every nest is checked before it is written, and
the tests and fuzz tests check with it too.

Per piece of stock: its pieces (blanks and rests) lie on it apart from each
other, and with the saw's cuts they cover it whole; each cut is a straight
line through the piece it splits, edge to edge, crossing no other piece; at
most `max_cuts` cuts; each blank goes on the bed; a rest is marked kept
exactly when the workshop keeps it. Per blank: each part's true machine
outline, turned and moved as the nest says, lies on the blank the margin
in from its edge and at least the spacing from every other part, turned by
one of its own turns. Per material: every part is placed once, or listed
as left over; no more sheets of a size are used than are on hand, nor
offcuts.
"""
from __future__ import annotations

from collections import Counter

from shapely import Polygon, STRtree, box

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
            if not fits(w, h, workshop.bed):
                problems.append(f"{name} ({w:g} x {h:g}) does not fit the bed")
            m = workshop.margin
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
            problems += _check_spacing(shapes, paths, workshop.spacing)
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
    kerf = workshop.kerf
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
    covered = sum(p.area for p in pieces) + sum(st.area for st in strips)
    if abs(covered - length * width) > 1e-3 * max(1.0, kerf) * (length + width):
        problems.append(f"{name}: its pieces and cuts cover {covered / 1e6:.4f} m2 of {length * width / 1e6:.4f}")
    if len(s["cuts"]) > workshop.max_cuts:
        problems.append(f"{name}: {len(s['cuts'])} cuts, more than {workshop.max_cuts}")
    for r in s["rests"]:
        if r["keep"] != workshop.keeps(r["rect"][2], r["rect"][3]):
            problems.append(f"{name}: the rest {r['rect']} is marked {'kept' if r['keep'] else 'waste'}")
    return problems


def _check_spacing(shapes: list[Polygon], paths: list[str], spacing: float) -> list[str]:
    problems: list[str] = []
    if len(shapes) < 2:
        return problems
    tree = STRtree(shapes)
    for i, s in enumerate(shapes):
        for j in tree.query(s, predicate="dwithin", distance=spacing - TOLERANCE):
            j = int(j)
            if j > i:
                gap = s.distance(shapes[j])
                problems.append(f"{paths[i]} and {paths[j]}: {gap:.4f} apart, less than {spacing:g}"
                                if gap > 0 else f"{paths[i]} and {paths[j]} overlap")
    return problems


def _check_stock(out: MaterialOut, workshop: Workshop) -> list[str]:
    problems: list[str] = []
    material = out["material"]
    on_hand: dict[str, int | None] = {}
    for s in workshop.sheets_for(material):
        key = f"{s.length:g}x{s.width:g}"
        if (key in on_hand and on_hand[key] is None) or s.count is None:
            on_hand[key] = None
        else:
            on_hand[key] = (on_hand.get(key) or 0) + s.count
    for key, n in out["bought"].items():
        if key not in on_hand:
            problems.append(f"{n} sheets {key}, a size not on hand")
        elif (limit := on_hand[key]) is not None and n > limit:
            problems.append(f"{n} sheets {key}, {limit} on hand")
    offcuts = Counter(f"{o.length:g}x{o.width:g}" for o in workshop.offcuts_for(material))
    for key, n in Counter(out["offcuts_used"]).items():
        if n > offcuts[key]:
            problems.append(f"{n} offcuts {key} used, {offcuts[key]} on hand")
    return problems
