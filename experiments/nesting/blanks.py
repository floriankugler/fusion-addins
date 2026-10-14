"""Nest on sheets too big for the machine's bed, sawn into blanks first.

    experiments/nesting/.venv/bin/python experiments/nesting/blanks.py job.json \
        --strategy patterns --out out/blanks/b15

A sheet (`--sheet`, 2470 x 1240) is larger than the bed (`--bed`, 2000 x
1000) both ways, so it is sawn into blanks with straight cuts right through
(`--kerf` apart), each fitting the bed either way round. The blanks keep
the sheet's grain along x. Offcuts on hand (`--offcut WxH`) are used as they
are. Two strategies:

- `patterns`: sawing patterns of up to three cuts, from a grid of cut
  positions (`--lengths`, `--widths`); for each, the fewest sheets whose
  blanks take all the parts (bin packing on N copies of each blank,
  N = 1, 2, ..., a few seconds per try). The blanks a nest leaves unused
  go back to stock.
- `twostep`: nest first, on blank sizes from a grid priced by area (plus
  `--blank-cost` each, for the sawing), then push each blank's parts into
  its corner and cut the blank down to them, then saw the blanks out of
  sheets with PackingSolver's guillotine solver for rectangles (sawing.py:
  a few settings tried, at most `--max-cuts` cuts per sheet, the largest
  piece of stock kept). What is left of a sheet stays one piece where it
  can.

`baseline` nests on whole sheets as if the bed were large enough, for
comparison. Each run writes `summary.json`, a job and result per strategy
that check.py reads (the blanks as sheet types), and an SVG per strategy
with the sheets, their blanks and parts.
"""
from __future__ import annotations

import argparse
import json
import math
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import packingsolver as ps
import packingsolver.rectangleguillotine as rg
from shapely import Polygon, STRtree, affinity, box

import ps_nest
import sawing


def solver_args(**kw) -> argparse.Namespace:
    base = dict(continuous=False, arcs=False, no_holes=False, verbosity=0, mode="anytime", set=[])
    base.update(kw)
    return argparse.Namespace(**base)


def size(text: str) -> tuple[float, float]:
    w, h = text.lower().split("x")
    return float(w), float(h)


def fits_bed(w: float, h: float, bed: tuple[float, float]) -> bool:
    return (w <= bed[0] and h <= bed[1]) or (w <= bed[1] and h <= bed[0])


def placed(job: dict, item: dict) -> Polygon:
    """An item's outline as the solver had it (`ps_rings`), placed."""
    part = job["parts"][item["index"]]
    rings = part.get("ps_rings", part["check_rings"])
    p = affinity.rotate(Polygon(rings[0], rings[1:]), item["rotation"], origin=(0, 0))
    return affinity.translate(p, *item["translation"])


def part_fits(job: dict, index: int, w: float, h: float) -> bool:
    part = job["parts"][index]
    rings = part.get("ps_rings", part["check_rings"])
    poly = Polygon(rings[0])
    turns = part.get("rotations", [0.0, 180.0])
    turns = [0.0, 90.0] if turns == "any" else turns
    room = (w - 2 * job["margin"], h - 2 * job["margin"])
    for t in turns:
        x0, y0, x1, y1 = affinity.rotate(poly, t, origin=(0, 0)).bounds
        if x1 - x0 <= room[0] + 1e-6 and y1 - y0 <= room[1] + 1e-6:
            return True
    return False


# --- sawing patterns -------------------------------------------------------

def patterns(sheet, bed, kerf, lengths, widths) -> list[dict]:
    """Patterns of up to three cuts whose pieces all fit the bed: a cross cut
    at `a` then each part ripped (or kept when it fits), or a rip at `b`
    then each strip cross cut. Pieces are (x, y, w, h) on the sheet."""
    L, W = sheet
    seen, out = set(), []

    def add(pieces, name):
        if not all(fits_bed(w, h, bed) for _x, _y, w, h in pieces):
            return
        key = tuple(sorted((round(w), round(h)) for _x, _y, w, h in pieces))
        if key in seen:
            return
        seen.add(key)
        out.append({"name": name, "pieces": [[round(v, 1) for v in p] for p in pieces]})

    def rips(x, w):
        opts = [[(x, 0, w, W)]] if fits_bed(w, W, bed) else []
        for b in widths:
            if b < W - kerf:
                opts.append([(x, 0, w, b), (x, b + kerf, w, W - b - kerf)])
        return opts

    for a in lengths:
        if not 0 < a < L - kerf:
            continue
        for o1 in rips(0, a):
            for o2 in rips(a + kerf, L - a - kerf):
                add(o1 + o2, f"cross {a:g}, rip {'/'.join(f'{p[3]:g}' for p in o1 + o2)}")
    for b in widths:
        if not 0 < b < W - kerf:
            continue
        for a1 in lengths:
            for a2 in lengths:
                if not (0 < a1 < L - kerf and 0 < a2 < L - kerf):
                    continue
                strips = [(0, b), (b + kerf, W - b - kerf)]
                pieces = []
                for (y, h), a in zip(strips, (a1, a2)):
                    pieces += [(0, y, a, h), (a + kerf, y, L - a - kerf, h)]
                add(pieces, f"rip {b:g}, cross {a1:g}/{a2:g}")
    return out


def blank_types(pieces, offcuts, n: int) -> tuple[list[dict], list[tuple[float, float]]]:
    """The distinct blanks of a pattern, `n` of each per piece, then the
    offcuts on hand, one each; and each type's size."""
    counts: dict[tuple[float, float], int] = {}
    for _x, _y, w, h in pieces:
        counts[(w, h)] = counts.get((w, h), 0) + 1
    types = [{"width": w, "height": h, "copies": n * c} for (w, h), c in counts.items()]
    # An offcut on hand costs next to nothing (PackingSolver wants a cost above 0).
    types += [{"width": w, "height": h, "copies": 1, "cost": 1.0, "offcut": True} for w, h in offcuts]
    return types, [(t["width"], t["height"]) for t in types]


def try_pattern(args) -> dict:
    job, pattern, offcuts, n_max, seconds = args
    pieces = pattern["pieces"]
    _types, sizes = blank_types(pieces, offcuts, 1)
    misfits = [i for i in range(len(job["parts"])) if not any(part_fits(job, i, w, h) for w, h in sizes)]
    if misfits:
        return {**pattern, "sheets": None, "why": f"{len(misfits)} parts fit no blank"}
    usable = sum((w - 2 * job["margin"]) * (h - 2 * job["margin"]) for _x, _y, w, h in pieces)
    offcut_area = sum((w - 2 * job["margin"]) * (h - 2 * job["margin"]) for w, h in offcuts)
    area = sum(p["area"] for p in job["parts"])
    n = max(1, math.ceil((area - offcut_area) / usable))
    t0 = time.perf_counter()
    tries = []
    while n <= n_max:
        types, _sizes = blank_types(pieces, offcuts, n)
        bins, left, _h, _o = ps_nest.solve(job, list(range(len(job["parts"]))), types,
                                          ps.Objective.BinPacking, solver_args(), seconds)
        tries.append(n)
        if bins and not left:
            return {**pattern, "sheets": n, "tries": tries, "seconds": time.perf_counter() - t0,
                    "bins": bins, "types": types}
        n += 1
    return {**pattern, "sheets": None, "tries": tries, "seconds": time.perf_counter() - t0,
            "why": f"no nest on up to {n_max} sheets"}


def assign_sheets(result: dict, offcuts) -> list[dict]:
    """Which blank of which sheet each used bin is: the k-th bin of a blank
    size goes to the k-th piece of that size, sheet by sheet."""
    pieces = result["pieces"]
    n = result["sheets"]
    slots: dict[int, list[tuple[int, int]]] = {}  # type -> [(sheet, piece)]
    types = result["types"]
    for t, ty in enumerate(types[:len(types) - len(offcuts)]):
        same = [k for k, (_x, _y, w, h) in enumerate(pieces) if (w, h) == (ty["width"], ty["height"])]
        slots[t] = [(s, k) for s in range(n) for k in same]
    used: dict[tuple[int, int], dict] = {}
    on_offcuts = []
    for b in result["bins"]:
        if b["sheet"] >= len(types) - len(offcuts):
            on_offcuts.append(b)
            continue
        used[slots[b["sheet"]].pop(0)] = b
    sheets = []
    for s in range(n):
        sheets.append({"pieces": [{"rect": p, "bin": used.get((s, k))} for k, p in enumerate(pieces)]})
    return sheets, on_offcuts


# --- nest first, saw after -------------------------------------------------

def gravity(job: dict, items: list[dict], step: float = 20.0) -> list[dict]:
    """Slide each part toward x = margin, then y = margin, as far as it
    goes without coming nearer another part than the spacing; a few passes.
    Slides in steps of `step` (less than the thinnest part plus twice the
    spacing, so nothing is jumped), then halves the last step."""
    spacing, margin = job["spacing"], job["margin"]
    items = [dict(i, translation=list(i["translation"])) for i in items]
    for _ in range(3):
        for axis in (0, 1):
            order = sorted(range(len(items)), key=lambda k: placed(job, items[k]).bounds[axis])
            for k in order:
                shapes = [placed(job, it) for it in items]
                others = [s for j, s in enumerate(shapes) if j != k]
                tree = STRtree(others) if others else None
                me = shapes[k]
                room = me.bounds[axis] - margin

                def ok(d: float) -> bool:
                    moved = affinity.translate(me, -d if axis == 0 else 0, -d if axis == 1 else 0)
                    if tree is None:
                        return True
                    near = tree.query(moved, predicate="dwithin", distance=spacing - 1e-6)
                    return len(near) == 0

                d = 0.0
                while d + step <= room and ok(d + step):
                    d += step
                lo, hi = d, min(d + step, room)
                if hi > lo and ok(hi):
                    lo = hi
                else:
                    for _b in range(12):
                        mid = (lo + hi) / 2
                        if ok(mid):
                            lo = mid
                        else:
                            hi = mid
                if lo > 0:
                    items[k]["translation"][axis] -= lo
    return items


def candidate_blanks(sheet, bed, lengths, widths, per_blank: float) -> list[dict]:
    out = []
    for w in lengths:
        for h in widths:
            if w <= sheet[0] and h <= sheet[1] and fits_bed(w, h, bed):
                out.append({"width": w, "height": h, "copies": -1, "cost": w * h + per_blank})
    return out


# --- refilling -------------------------------------------------------------

def clip_to_bed(w: float, h: float, bed) -> tuple[float, float]:
    """The largest piece of w x h, from its corner, that fits the bed."""
    if fits_bed(w, h, bed):
        return w, h
    options = [(min(w, bed[0]), min(h, bed[1])), (min(w, bed[1]), min(h, bed[0]))]
    return max(options, key=lambda o: o[0] * o[1])


def refill(job: dict, sheets: list[dict], seconds: float, kerf: float, bed, max_cuts: int) -> tuple[list[dict], list[str]]:
    """Take the parts off the sheet with the least of them and nest them
    into the room left on the others: their used blanks first (the parts
    already there as defects, kept the spacing off; almost free), then their
    stock pieces (priced by area, as far as they fit the bed, on sheets with
    two cuts to spare), each then cut down to what it holds where what it
    frees is worth keeping. When all fit, that sheet is not needed; again
    while it works."""
    log = []
    while len(sheets) > 1:
        area = lambda s: sum(job["parts"][i["index"]]["area"] for p in s["pieces"] if p.get("bin")
                             for i in p["bin"]["items"])
        k = min(range(len(sheets)), key=lambda k: area(sheets[k]))
        moving = [i["index"] for p in sheets[k]["pieces"] if p.get("bin") for i in p["bin"]["items"]]
        if not moving:
            sheets = sheets[:k] + sheets[k + 1:]
            continue
        slots, types = [], []
        for si, s in enumerate(sheets):
            if si == k:
                continue
            for pi, p in enumerate(s["pieces"]):
                if p.get("kind") == "waste":
                    continue
                _x, _y, w, h = p["rect"]
                if not p.get("bin"):
                    if s["cuts"] + 2 > max_cuts:
                        continue
                    w, h = clip_to_bed(w, h, bed)
                if min(w, h) < 2 * job["margin"] + 10:
                    continue
                defects = [[list(c) for c in list(placed(job, item).exterior.coords)[:-1]]
                           for item in (p.get("bin") or {}).get("items", [])]
                slots.append((si, pi))
                types.append({"width": w, "height": h, "copies": 1, "defects": defects,
                              "cost": 1.0 if p.get("bin") else w * h})
        t0 = time.perf_counter()
        bins, left, _h, _o = ps_nest.solve(job, moving, types, ps.Objective.VariableSizedBinPacking,
                                          solver_args(), seconds)
        if not bins or left:
            log.append(f"sheet {k}: {len(moving)} parts do not fit the room on the others "
                       f"({time.perf_counter() - t0:.1f} s)")
            break
        into_stock = 0
        for b in bins:
            si, pi = slots[b["sheet"]]
            piece = sheets[si]["pieces"][pi]
            if piece.get("bin"):
                piece["bin"]["items"] = piece["bin"]["items"] + b["items"]
                continue
            into_stock += 1
            x, y, w, h = piece["rect"]
            shapes = [placed(job, it) for it in b["items"]]
            bw, bh = clip_to_bed(w, h, bed)
            w2 = min(bw, math.ceil(max(sh.bounds[2] for sh in shapes) + job["margin"]))
            h2 = min(bh, math.ceil(max(sh.bounds[3] for sh in shapes) + job["margin"]))
            # Cut off to the right, then above, what is worth keeping or what
            # the bed does not take; anything else stays with the blank.
            right = [x + w2 + kerf, y, w - w2 - kerf, h]
            if right[2] > 0 and (sawing.useful(right[2], right[3]) or not fits_bed(w, h, bed)):
                sheets[si]["pieces"].append({"rect": right, "bin": None,
                                             "kind": "stock" if sawing.useful(right[2], right[3]) else "waste"})
                sheets[si]["cuts"] += 1
                w = w2
            above = [x, y + h2 + kerf, w, h - h2 - kerf]
            if above[3] > 0 and (sawing.useful(above[2], above[3]) or not fits_bed(w, h, bed)):
                sheets[si]["pieces"].append({"rect": above, "bin": None,
                                             "kind": "stock" if sawing.useful(above[2], above[3]) else "waste"})
                sheets[si]["cuts"] += 1
                h = h2
            piece.update(rect=[x, y, w, h], bin={"items": b["items"]}, kind="used")
        log.append(f"sheet {k}: its {len(moving)} parts moved into the room on the others, "
                   f"{into_stock} stock pieces cut into ({time.perf_counter() - t0:.1f} s)")
        sheets = sheets[:k] + sheets[k + 1:]
    return sheets, log


# --- drawing ---------------------------------------------------------------

def draw(job: dict, sheets: list[dict], sheet, path: Path, title: str, offcut_bins=()) -> None:
    """Each sheet with its pieces: blanks with their parts (blue), blanks
    left whole (green: stock), waste (grey)."""
    pad = 60
    W, H = sheet
    total_h = len(sheets) * (H + pad) + sum(b["size"][1] + pad for b in offcut_bins) + pad + 60
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-pad} 0 {W + 2 * pad} {total_h}" '
           f'width="{(W + 2 * pad) / 4:.0f}" height="{total_h / 4:.0f}" font-family="sans-serif">',
           '<rect x="-1e5" y="-1e5" width="2e5" height="2e5" fill="#fff"/>',
           f'<text x="0" y="45" font-size="40">{title}</text>']

    def poly_d(p: Polygon, ox: float, dy: float) -> str:
        d = []
        for ring in [p.exterior, *p.interiors]:
            pts = list(ring.coords)[:-1]
            d.append("M " + " L ".join(f"{x + ox:.1f} {dy - y:.1f}" for x, y in pts) + " Z")
        return " ".join(d)

    top = 60 + pad
    for s in sheets:
        dy = top + H
        out.append(f'<rect x="0" y="{top}" width="{W}" height="{H}" fill="#ddd" stroke="#333" stroke-width="3"/>')
        for piece in s["pieces"]:
            x, y, w, h = piece["rect"]
            kind = piece.get("kind") or ("used" if piece.get("bin") else "stock")
            fill = {"used": "#f3efe6", "stock": "#cfe8c4", "waste": "#bbb"}[kind]
            out.append(f'<rect x="{x}" y="{dy - y - h}" width="{w}" height="{h}" fill="{fill}" stroke="#555" stroke-width="2"/>')
            out.append(f'<text x="{x + 8}" y="{dy - y - h + 26}" font-size="22" fill="#555">{w:g} x {h:g}</text>')
            for item in (piece["bin"] or {}).get("items", []) if piece.get("bin") else []:
                shape = placed(job, item)
                out.append(f'<path d="{poly_d(shape, x, dy - y)}" fill="#7aa6d8" fill-opacity="0.8" '
                           f'fill-rule="evenodd" stroke="#1d4f8a" stroke-width="1.5"/>')
        top += H + pad
    for b in offcut_bins:
        w, h = b["size"]
        dy = top + h
        out.append(f'<rect x="0" y="{top}" width="{w}" height="{h}" fill="#f6e3c4" stroke="#333" stroke-width="3"/>')
        out.append(f'<text x="8" y="{top + 26}" font-size="22" fill="#555">offcut {w:g} x {h:g}</text>')
        for item in b["items"]:
            out.append(f'<path d="{poly_d(placed(job, item), 0, dy)}" fill="#7aa6d8" fill-opacity="0.8" '
                       f'fill-rule="evenodd" stroke="#1d4f8a" stroke-width="1.5"/>')
        top += h + pad
    out.append("</svg>")
    path.write_text("\n".join(out))


def checked_job(job: dict, types: list[dict]) -> dict:
    """The job with the blanks as its sheet types, for check.py."""
    return dict(job, sheet_types=types, sheets=[[t["width"], t["height"]] for t in types])


# --- strategies ------------------------------------------------------------

def run_patterns(job, a, offcuts, out: Path) -> dict:
    pats = patterns(a.sheet, a.bed, a.kerf, a.lengths, a.widths)
    print(f"{len(pats)} patterns")
    t0 = time.perf_counter()
    with ProcessPoolExecutor(max_workers=a.workers) as pool:
        results = list(pool.map(try_pattern, [(job, p, offcuts, a.max_sheets, a.seconds) for p in pats]))
    elapsed = time.perf_counter() - t0
    ok = [r for r in results if r["sheets"]]
    blank_area = lambda r: sum(p[2] * p[3] for p in r["pieces"])

    def stock_area(r):
        used = {(b["sheet"]) for b in r["bins"]}
        # Blanks left whole: copies of each type less those used.
        total = 0.0
        counts: dict[int, int] = {}
        for b in r["bins"]:
            counts[b["sheet"]] = counts.get(b["sheet"], 0) + 1
        for t, ty in enumerate(r["types"]):
            if ty.get("offcut"):
                continue
            total += (ty["copies"] - counts.get(t, 0)) * ty["width"] * ty["height"]
        _ = used
        return total

    for r in ok:
        r["stock_area"] = stock_area(r)
        r["blanks_used"] = len(r["bins"])
    ok.sort(key=lambda r: (r["sheets"], -r["stock_area"], r["blanks_used"]))
    lines = [f"{r['sheets']} sheets, {r['stock_area'] / 1e6:.2f} m2 of blanks left whole, "
             f"{r['blanks_used']} blanks used, {r['seconds']:.1f} s (tried {r['tries']}): {r['name']}" for r in ok[:12]]
    print(f"patterns: {len(ok)} of {len(pats)} nest, {elapsed:.0f} s in all")
    print("\n".join("  " + l for l in lines))
    best = ok[0]
    sheets, on_offcuts = assign_sheets(best, offcuts)
    for sh in sheets:
        sh["cuts"] = 3
        for piece in sh["pieces"]:
            piece["kind"] = "used" if piece.get("bin") else "stock"
    sawn = len(sheets)
    if a.refill > 0:
        sheets, log = refill(job, sheets, a.refill, a.kerf, a.bed, a.max_cuts)
        for line in log:
            print(f"  refill: {line}")
    stock = sum(p["rect"][2] * p["rect"][3] for sh in sheets for p in sh["pieces"] if p["kind"] == "stock")
    used = len(sheets) * a.sheet[0] * a.sheet[1] - stock
    print(f"patterns, best: {len(sheets)} sheets (sawn {sawn}), {stock / 1e6:.2f} m2 left as stock, "
          f"{used / 1e6:.2f} m2 used")
    nt = len(best["types"]) - len(offcuts)
    draw(job, sheets, a.sheet, out / "patterns.svg",
         f"patterns: {len(sheets)} sheets, {best['name']}",
         [{"size": offcuts[b['sheet'] - nt], "items": b["items"]} for b in on_offcuts])
    used_pieces = [p for sh in sheets for p in sh["pieces"] if p.get("bin")]
    ptypes = [{"width": p["rect"][2], "height": p["rect"][3], "copies": 1} for p in used_pieces]
    ptypes += [{"width": o[0], "height": o[1], "copies": 1} for o in offcuts]
    pbins = [{"sheet": k, "items": p["bin"]["items"]} for k, p in enumerate(used_pieces)]
    pbins += [{"sheet": len(used_pieces) + b["sheet"] - nt, "items": b["items"]} for b in on_offcuts]
    (out / "patterns_job.json").write_text(json.dumps(checked_job(job, ptypes)))
    (out / "patterns_result.json").write_text(json.dumps({"bins": pbins, "unplaced": []}))
    return {"strategy": "patterns", "patterns": len(pats), "nesting": len(ok), "seconds": elapsed,
            "best": {k: best[k] for k in ("name", "sheets", "stock_area", "blanks_used", "seconds", "tries")},
            "after_refill": {"sheets": len(sheets), "stock_area": stock, "used_area": used},
            "ranking": lines, "unnested": [{"name": r["name"], "why": r.get("why")} for r in results if not r["sheets"]][:10]}


def run_twostep(job, a, offcuts, out: Path) -> dict:
    t0 = time.perf_counter()
    types = candidate_blanks(a.sheet, a.bed, a.lengths, a.widths, a.blank_cost)
    types += [{"width": w, "height": h, "copies": 1, "cost": 1.0, "offcut": True} for w, h in offcuts]
    bins, left, hist, _o = ps_nest.solve(job, list(range(len(job["parts"]))), types,
                                        ps.Objective.VariableSizedBinPacking, solver_args(), a.nest_seconds)
    t_nest = time.perf_counter() - t0
    best_at = hist[-1]["seconds"] if hist else None
    if left:
        raise SystemExit(f"twostep: {len(left)} parts placed on no blank")
    n_off = len(offcuts)
    blanks, on_offcuts = [], []
    for b in bins:
        if b["sheet"] >= len(types) - n_off:
            on_offcuts.append({"size": offcuts[b["sheet"] - (len(types) - n_off)], "items": b["items"]})
            continue
        items = gravity(job, b["items"]) if a.gravity else b["items"]
        shapes = [placed(job, it) for it in items]
        x1 = max(s.bounds[2] for s in shapes) + job["margin"]
        y1 = max(s.bounds[3] for s in shapes) + job["margin"]
        t = types[b["sheet"]]
        # Cut the blank down to its parts, unless what that frees is a
        # sliver (less than --min-strip): it would only be waste.
        w = math.ceil(x1) if t["width"] - x1 >= a.min_strip else t["width"]
        h = math.ceil(y1) if t["height"] - y1 >= a.min_strip else t["height"]
        blanks.append({"chosen": [t["width"], t["height"]], "size": [w, h], "items": items})
    t_shrink = time.perf_counter() - t0 - t_nest
    plan, tried = sawing.best_plan([tuple(b["size"]) for b in blanks], a.sheet, a.bed, a.kerf,
                                   a.max_cuts, a.saw_seconds)
    t_saw = time.perf_counter() - t0 - t_nest - t_shrink
    sheets = []
    for tree in plan["plans"]:
        pieces = []
        for leaf in sawing.leaves(tree):
            x, y, w, h = leaf.rect
            if leaf.blanks:
                # The parts of the blanks the piece holds, measured from the
                # piece's corner (it may hold several blanks, and rests).
                items = []
                for bi, (ox, oy) in leaf.blanks:
                    items += [dict(i, translation=[i["translation"][0] + ox - x, i["translation"][1] + oy - y])
                              for i in blanks[bi]["items"]]
                pieces.append({"rect": [x, y, w, h], "bin": {"items": items}, "kind": "used",
                               "blanks": len(leaf.blanks)})
            else:
                pieces.append({"rect": [x, y, w, h], "bin": None,
                               "kind": "stock" if sawing.useful(w, h) else "waste"})
        sheets.append({"pieces": pieces, "cuts": sawing.cuts(tree)})
    print(f"  saw: {plan['setting']}, cuts per sheet {plan['cuts']} "
          f"({len(tried)} settings tried, {sum(1 for r in tried if r['over'] == 0)} within {a.max_cuts} cuts)")
    sawn = len(sheets)
    if a.refill > 0:
        sheets, log = refill(job, sheets, a.refill, a.kerf, a.bed, a.max_cuts)
        for line in log:
            print(f"  refill: {line}")
    stock = sum(p["rect"][2] * p["rect"][3] for s in sheets for p in s["pieces"] if p["kind"] == "stock")
    elapsed = time.perf_counter() - t0
    draw(job, sheets, a.sheet, out / "twostep.svg",
         f"twostep: {len(sheets)} sheets, cuts {[sh['cuts'] for sh in sheets]}", on_offcuts)
    used_pieces = [p for s in sheets for p in s["pieces"] if p.get("bin")]
    btypes = [{"width": p["rect"][2], "height": p["rect"][3], "copies": 1} for p in used_pieces]
    btypes += [{"width": o["size"][0], "height": o["size"][1], "copies": 1} for o in on_offcuts]
    rbins = [{"sheet": k, "items": p["bin"]["items"]} for k, p in enumerate(used_pieces)]
    rbins += [{"sheet": len(used_pieces) + k, "items": o["items"]} for k, o in enumerate(on_offcuts)]
    (out / "twostep_job.json").write_text(json.dumps(checked_job(job, btypes)))
    (out / "twostep_result.json").write_text(json.dumps({"bins": rbins, "unplaced": []}))
    used = len(sheets) * a.sheet[0] * a.sheet[1] - stock  # blanks, kerf and waste
    stock_pieces = sorted((p["rect"] for sh in sheets for p in sh["pieces"] if p["kind"] == "stock"),
                          key=lambda r: -r[2] * r[3])
    largest = stock_pieces[0] if stock_pieces else None
    print(f"twostep: {len(sheets)} sheets (sawn {sawn}), {len(used_pieces)} blanks (+{len(on_offcuts)} offcuts), "
          f"cuts {[sh['cuts'] for sh in sheets]}, {stock / 1e6:.2f} m2 left as stock in {len(stock_pieces)} pieces"
          + (f" (largest {largest[2]:.0f} x {largest[3]:.0f})" if largest else "")
          + f", {used / 1e6:.2f} m2 used; nest {t_nest:.1f} s (best at {best_at:.1f} s), saw {t_saw:.1f} s")
    return {"strategy": "twostep", "sheets": len(sheets), "used_area": used, "blanks": [b["size"] for b in blanks],
            "cuts": [sh["cuts"] for sh in sheets], "saw_setting": plan["setting"],
            "stock_pieces": [r[2:] for r in stock_pieces],
            "pieces_per_sheet": [len(sh["pieces"]) for sh in sheets],
            "chosen": [b["chosen"] for b in blanks], "stock_area": stock, "seconds": elapsed,
            "nest_seconds": t_nest, "nest_best_at": best_at, "push_seconds": t_shrink, "saw_seconds": t_saw}


def run_baseline(job, a, offcuts, out: Path) -> dict:
    types = [{"width": a.sheet[0], "height": a.sheet[1], "copies": -1}]
    types += [{"width": w, "height": h, "copies": 1, "cost": 1.0, "offcut": True} for w, h in offcuts]
    t0 = time.perf_counter()
    bins, left, _h, _o = ps_nest.solve(job, list(range(len(job["parts"]))), types,
                                      ps.Objective.VariableSizedBinPacking, solver_args(), a.nest_seconds)
    sheets = sum(1 for b in bins if b["sheet"] == 0)
    print(f"baseline (no bed limit): {sheets} sheets, {len(left)} unplaced, {time.perf_counter() - t0:.1f} s")
    return {"strategy": "baseline", "sheets": sheets, "unplaced": len(left), "seconds": time.perf_counter() - t0}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("job", type=Path)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--strategy", nargs="+", choices=["patterns", "twostep", "baseline"], default=["patterns", "twostep", "baseline"])
    ap.add_argument("--sheet", type=size, default=(2470.0, 1240.0))
    ap.add_argument("--bed", type=size, default=(2000.0, 1000.0))
    ap.add_argument("--kerf", type=float, default=4.0)
    ap.add_argument("--offcut", type=size, action="append", default=[])
    ap.add_argument("--lengths", type=float, nargs="+", default=[2000, 1800, 1600, 1470, 1233])
    ap.add_argument("--widths", type=float, nargs="+", default=[1000, 800, 618])
    ap.add_argument("--seconds", type=float, default=3.0, help="per try of a pattern and a number of sheets")
    ap.add_argument("--max-sheets", type=int, default=12)
    ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--blank-lengths", type=float, nargs="+", default=[400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000])
    ap.add_argument("--blank-widths", type=float, nargs="+", default=[250, 400, 600, 800, 1000, 1240])
    ap.add_argument("--blank-cost", type=float, default=50_000, help="mm2 added to each blank's cost (sawing)")
    ap.add_argument("--nest-seconds", type=float, default=20.0)
    ap.add_argument("--saw-seconds", type=float, default=1.0, help="per saw setting tried")
    ap.add_argument("--no-gravity", dest="gravity", action="store_false")
    ap.add_argument("--min-strip", type=float, default=0.0,
                    help="cut a blank down only to free a strip this wide (150 made it worse: 6 sheets for 5)")
    ap.add_argument("--max-cuts", type=int, default=5, help="saw cuts per sheet at most")
    ap.add_argument("--refill", type=float, default=0.0, metavar="SECONDS",
                    help="then move the emptiest sheet's parts into the room on the others, this long a try")
    a = ap.parse_args()
    job = json.loads(a.job.read_text())
    a.out.mkdir(parents=True, exist_ok=True)
    summary = {"job": str(a.job), "sheet": a.sheet, "bed": a.bed, "kerf": a.kerf, "offcuts": a.offcut,
               "parts": len(job["parts"]), "area": sum(p["area"] for p in job["parts"])}
    print(f"{summary['parts']} parts, {summary['area'] / 1e6:.2f} m2; sheet {a.sheet[0]:g} x {a.sheet[1]:g} "
          f"({summary['area'] / (a.sheet[0] * a.sheet[1]):.2f} sheets of area)")
    for s in a.strategy:
        if s == "patterns":
            summary["patterns"] = run_patterns(job, a, a.offcut, a.out)
        elif s == "twostep":
            ta = argparse.Namespace(**vars(a))
            ta.lengths, ta.widths = a.blank_lengths, a.blank_widths
            summary["twostep"] = run_twostep(job, ta, a.offcut, a.out)
        else:
            summary["baseline"] = run_baseline(job, a, a.offcut, a.out)
    (a.out / "summary.json").write_text(json.dumps(summary, indent=1, default=str))


if __name__ == "__main__":
    main()
