"""Nest a job (jobs.py) with PackingSolver (pip install packingsolver, in
experiments/nesting/.venv) and write a result check.py reads.

    experiments/nesting/.venv/bin/python experiments/nesting/ps_nest.py job.json result.json \
        --objective leftovers --time-limit 30

Each sheet of the job is a bin type of its own, with its count (`2500x1250*2`;
no count: as many as needed) and its area as cost. Parts are the job's true
rings (`check_rings`) with their holes; spacing between parts and to the
sheet's edge: PackingSolver's `item_item_minimum_spacing`, and each sheet
shrunk by the margin (its `item_bin_minimum_spacing` is not kept, see
`sheet_shape`). Turns: each part's own (`rotations` in the job: 0
and 180 for a part with grain, steps or any angle for one without), or any
angle for all (`--continuous`), never mirrored. Parts with arcs (irregular.py) go in as true arcs with `--arcs`,
else as the polygon that contains them (`ps_rings`).

Objectives: `binpacking` (fewest sheets, then nothing else: parts end up
anywhere on a sheet), `leftovers` (fewest sheets, then the largest leftover
on the last one; the parts are pushed toward `--leftover-corner`), `variable` (cheapest
set of sheets, by cost, when the sheets differ in size), `knapsack` (as much
part area as the sheets on hand take, when they may not take all; bin
packing then finds nothing at all).

A part's placement: turned about its own origin by `angle` (counter-
clockwise), then moved by `bl_corner` (despite its name, not the corner of
its bounding box), in the sheet's own coordinates.
"""
from __future__ import annotations

import argparse
import json
import math
import time
from pathlib import Path

import packingsolver as ps
import packingsolver.irregular as psi
from shapely import Polygon
from shapely.geometry.polygon import orient

OBJECTIVES = {
    "binpacking": ps.Objective.BinPacking,
    "leftovers": ps.Objective.BinPackingWithLeftovers,
    "variable": ps.Objective.VariableSizedBinPacking,
    "knapsack": ps.Objective.Knapsack,
}
CORNERS = {name.lower(): getattr(psi.LeftoverMode, name) for name in
           ["Bottom", "BottomLeft", "BottomRight", "Left", "Right", "Top", "TopLeft", "TopRight"]}
MODES = {"anytime": ps.OptimizationMode.Anytime, "not-anytime": ps.OptimizationMode.NotAnytime,
         "deterministic": ps.OptimizationMode.NotAnytimeDeterministic,
         "sequential": ps.OptimizationMode.NotAnytimeSequential}


def shape_of(ring: list[list[float]]) -> psi.Shape:
    # PackingSolver wants every contour counter-clockwise, holes too.
    poly = orient(Polygon(ring))
    return psi.build_shape([list(p) for p in list(poly.exterior.coords)[:-1]])


def arc_shape(ring: list | dict) -> psi.Shape:
    """A ring of irregular.py's arcs: points and arc centres, or a circle.
    Holes come counter-clockwise like the exterior: a circle always is, a
    path is reversed when it runs clockwise."""
    if isinstance(ring, dict):
        cx, cy, r = ring["circle"]
        return psi.build_circle(r).shift(cx, cy)
    shape = psi.build_shape(ring)
    if shape.compute_area() < 0:
        shape = shape.reverse()
    return shape


def item_shape(part: dict, arcs: bool, holes: bool) -> psi.ShapeWithHoles:
    if arcs and part.get("arcs"):
        rings = [arc_shape(r) for r in part["arcs"]]
    else:
        rings = [shape_of(r) for r in part.get("ps_rings", part["check_rings"])]
    return psi.ShapeWithHoles(rings[0], rings[1:] if holes else [])


def sheet_shape(t: dict, margin: float) -> psi.Shape:
    """A sheet type, a rectangle or an offcut's outline, shrunk by the margin
    to the edge. PackingSolver's own `item_bin_minimum_spacing` is not used:
    a part that fits the sheet but not within the spacing is placed anyway,
    centred, the gaps shrunk alike on both sides (a 410 high rectangle in a
    413 high sheet with spacing 10: 1.5 above and below) [2026-10-14]."""
    if t.get("outline"):
        inner = Polygon(t["outline"]).buffer(-margin, join_style="mitre")
        return shape_of([list(c) for c in list(orient(inner).exterior.coords)[:-1]])
    return psi.build_rectangle(margin, t["width"] - margin, margin, t["height"] - margin)


def solve(job: dict, indices: list[int], sheet_types: list[dict], objective, a,
          time_limit: float, leftover=None) -> tuple[list[dict], list[int], list[dict], object]:
    """Nest the job's parts `indices` on `sheet_types`; the bins name their
    sheet type by its index in `sheet_types`, the items their part by its
    index in the job."""
    b = psi.InstanceBuilder()
    b.set_objective(objective)
    if leftover is not None:
        b.set_leftover_mode(leftover)
    b.set_item_item_minimum_spacing(job["spacing"])
    # PackingSolver refuses a sheet type of no copies; the bins name the job's own.
    type_of: list[int] = []
    for k, t in enumerate(sheet_types):
        if t["copies"] == 0:
            continue
        type_of.append(k)
        kwargs = {"copies": t["copies"]}
        if t.get("cost") is not None:
            kwargs["cost"] = t["cost"]
        bin_type = b.add_bin_type(sheet_shape(t, job["margin"]), **kwargs)
        for defect in t.get("defects", []):
            d = b.add_defect(bin_type, -1, psi.ShapeWithHoles(shape_of(defect), []))
            # A defect (a knot, a used corner) is kept as far off as another part.
            b.set_item_defect_minimum_spacing(bin_type, d, job["spacing"])
    rotations = job["config"]["rotations"]
    for i in indices:
        part = job["parts"][i]
        turns = part.get("rotations", [k * 360 / rotations for k in range(rotations)])
        if a.continuous or turns == "any":
            allowed = [(0.0, 360.0, False)]
        else:
            allowed = [(r, r, False) for r in turns]
        b.add_item_type(item_shape(part, a.arcs, not a.no_holes), allowed_rotations=allowed, copies=1)
    instance = b.build()

    params = psi.OptimizeParameters()
    params.time_limit = time_limit
    params.verbosity_level = a.verbosity
    params.optimization_mode = MODES[a.mode]
    for assignment in a.set:
        name, _, text = assignment.partition("=")
        current = getattr(params, name)
        value = (text.lower() in ("1", "true", "yes")) if isinstance(current, bool) else type(current)(text)
        setattr(params, name, value)
    history: list[dict] = []
    t0 = time.perf_counter()

    def on_solution(output) -> None:
        sol = output.solution
        history.append({"seconds": time.perf_counter() - t0, "bins": sol.number_of_bins(),
                        "items": sol.number_of_items(), "cost": sol.cost()})

    params.new_solution_callback = on_solution
    output = psi.optimize(instance, params)
    sol = output.solution
    bins, placed = [], set()
    for k in range(sol.number_of_different_bins()):
        sb = sol.bin(k)
        items = []
        for it in sb.items:
            if it.mirror:
                raise SystemExit("PackingSolver mirrored a part although no mirror was allowed")
            index = indices[it.item_type_id]
            placed.add(index)
            items.append({"id": job["parts"][index]["id"], "index": index, "rotation": it.angle,
                          "translation": [it.bl_corner.x, it.bl_corner.y]})
        for _ in range(sb.copies):
            bins.append({"sheet": type_of[sb.bin_type_id], "items": items})
    return bins, [i for i in indices if i not in placed], history, output


def reach(job: dict, items: list[dict]) -> float:
    """How far along x the parts reach (their outlines as the solver had them)."""
    xs = []
    for item in items:
        part = job["parts"][item["index"]]
        a = math.radians(item["rotation"])
        c, s = math.cos(a), math.sin(a)
        for x, y in part.get("ps_rings", part["check_rings"])[0]:
            xs.append(c * x - s * y + item["translation"][0])
    return max(xs) if xs else 0.0


def compact(job: dict, bins: list[dict], a) -> dict:
    """Push the parts of the sheet with the most room left to the left, so that what is left
    of it is one piece across the sheet: a binary search on the sheet's
    length, asking bin packing whether the parts fit on the shorter sheet
    (`--compact` seconds per question; no answer counts as no).
    PackingSolver's own strip packing (OpenDimensionX) found nothing on the
    sheet's own length and 3090 mm on a longer one for parts that bin
    packing fits in 2366 mm."""
    area = lambda b: sum(job["parts"][i["index"]]["area"] for i in b["items"])
    free = lambda b: job["sheet_types"][b["sheet"]]["width"] * job["sheet_types"][b["sheet"]]["height"] - area(b)
    k = max(range(len(bins)), key=lambda k: free(bins[k]))
    t = job["sheet_types"][bins[k]["sheet"]]
    if t.get("outline"):
        return {"bin": k, "skipped": "an offcut's outline"}
    indices = [i["index"] for i in bins[k]["items"]]
    before = best = reach(job, bins[k]["items"])
    widest = max(max(x for x, _y in job["parts"][i].get("ps_rings", job["parts"][i]["check_rings"])[0]) -
                 min(x for x, _y in job["parts"][i].get("ps_rings", job["parts"][i]["check_rings"])[0]) for i in indices)
    lo = max(area(bins[k]) / (t["height"] - 2 * job["margin"]), widest) + job["margin"]
    hi = best + job["margin"]
    steps = []
    t0 = time.perf_counter()
    while hi - lo > 10:
        length = (lo + hi) / 2
        shorter = dict(t, width=length, copies=1)
        trial, left, _h, _o = solve(job, indices, [shorter], ps.Objective.BinPacking, a, a.compact)
        ok = bool(trial) and not left
        steps.append({"length": round(length, 1), "fits": ok})
        if ok:
            bins[k] = {"sheet": bins[k]["sheet"], "items": trial[0]["items"]}
            best = reach(job, trial[0]["items"])
            hi = best + job["margin"]
        else:
            lo = length
    print(f"compacted sheet {k}: parts reach {before:.0f} -> {best:.0f} mm of {t['width']:g} "
          f"({len(steps)} questions, {time.perf_counter() - t0:.1f} s)")
    return {"bin": k, "reach_before": before, "reach_after": best, "steps": steps}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("job", type=Path)
    ap.add_argument("result", type=Path)
    ap.add_argument("--objective", choices=OBJECTIVES, default="leftovers")
    ap.add_argument("--leftover-corner", choices=CORNERS, default="left",
                    help="where the parts are pushed (left: the leftover is a strip on the right)")
    ap.add_argument("--mode", choices=MODES, default="anytime")
    ap.add_argument("--time-limit", type=float, default=30.0)
    ap.add_argument("--compact", type=float, default=0.0, metavar="SECONDS",
                    help="then push the parts of the sheet with the most room left to the left (a search on its length, "
                         "this long per step), so the leftover is one piece across the sheet")
    ap.add_argument("--no-holes", action="store_true", help="give the parts without their holes")
    ap.add_argument("--arcs", action="store_true", help="give parts with arcs (irregular.py) as true arcs")
    ap.add_argument("--continuous", action="store_true", help="any angle (0 to 360) instead of the job's turns")
    ap.add_argument("--verbosity", type=int, default=0)
    ap.add_argument("--set", nargs="*", default=[], metavar="NAME=VALUE",
                    help="OptimizeParameters to set, e.g. use_local_search=true "
                         "not_anytime_tree_search_queue_size=64 (all use_* false: the solver chooses)")
    a = ap.parse_args()

    job = json.loads(a.job.read_text())
    t0 = time.perf_counter()
    leftover = CORNERS[a.leftover_corner] if a.objective == "leftovers" else None
    bins, unplaced, history, output = solve(job, list(range(len(job["parts"]))), job["sheet_types"],
                                            OBJECTIVES[a.objective], a, a.time_limit, leftover)
    seconds = time.perf_counter() - t0

    compacted = None
    if a.compact > 0 and bins:
        compacted = compact(job, bins, a)
    unplaced_ids = [job["parts"][i]["id"] for i in unplaced]
    result = {"solver": "packingsolver", "objective": a.objective, "mode": a.mode,
              "arcs": a.arcs, "continuous": a.continuous, "set": a.set,
              "time_limit": a.time_limit, "seconds": seconds,
              "bestAt": {"seconds": history[-1]["seconds"]} if history else None,
              "bins": bins, "unplaced": unplaced_ids, "history": history,
              "bound": output.bin_packing_bound, "compacted": compacted}
    a.result.parent.mkdir(parents=True, exist_ok=True)
    a.result.write_text(json.dumps(result, indent=1, default=str))
    print(f"{len(bins)} sheets, {len(unplaced_ids)} unplaced, {seconds:.1f} s "
          f"(best at {result['bestAt']['seconds'] if history else '-'} s, {len(history)} improvements)")


if __name__ == "__main__":
    main()
