"""Nest a job (jobs.py) with PackingSolver (pip install packingsolver, in
experiments/nesting/.venv) and write a result check.py reads.

    experiments/nesting/.venv/bin/python experiments/nesting/ps_nest.py job.json result.json \
        --objective leftovers --time-limit 30

Each sheet of the job is a bin type of its own, with its count (`2500x1250*2`;
no count: as many as needed) and its area as cost. Parts are the job's true
rings (`check_rings`) with their holes; spacing between parts and to the
sheet's edge are PackingSolver's own (`item_item_minimum_spacing`, the bin
type's `item_bin_minimum_spacing`). Turns: the job's `rotations` as fixed
angles (2: 0 and 180, for the grain), never mirrored.

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


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("job", type=Path)
    ap.add_argument("result", type=Path)
    ap.add_argument("--objective", choices=OBJECTIVES, default="leftovers")
    ap.add_argument("--leftover-corner", choices=CORNERS, default="left",
                    help="where the parts are pushed (left: the leftover is a strip on the right)")
    ap.add_argument("--mode", choices=MODES, default="anytime")
    ap.add_argument("--time-limit", type=float, default=30.0)
    ap.add_argument("--no-holes", action="store_true", help="give the parts without their holes")
    ap.add_argument("--verbosity", type=int, default=0)
    a = ap.parse_args()

    job = json.loads(a.job.read_text())
    b = psi.InstanceBuilder()
    b.set_objective(OBJECTIVES[a.objective])
    if a.objective == "leftovers":
        b.set_leftover_mode(CORNERS[a.leftover_corner])
    b.set_item_item_minimum_spacing(job["spacing"])
    for t in job["sheet_types"]:
        kwargs = {"copies": t["copies"], "item_bin_minimum_spacing": job["margin"]}
        if t.get("cost") is not None:
            kwargs["cost"] = t["cost"]
        b.add_bin_type(psi.build_rectangle(t["width"], t["height"]), **kwargs)
    rotations = job["config"]["rotations"]
    angles = [i * 360 / rotations for i in range(rotations)]
    for p in job["parts"]:
        rings = p["check_rings"]
        holes = [] if a.no_holes else [shape_of(h) for h in rings[1:]]
        shape = psi.ShapeWithHoles(shape_of(rings[0]), holes)
        b.add_item_type(shape, allowed_rotations=[(r, r, False) for r in angles], copies=1)
    instance = b.build()

    params = psi.OptimizeParameters()
    params.time_limit = a.time_limit
    params.verbosity_level = a.verbosity
    params.optimization_mode = MODES[a.mode]
    history = []
    t0 = time.perf_counter()

    def on_solution(output) -> None:
        s = output.solution
        history.append({"seconds": time.perf_counter() - t0, "bins": s.number_of_bins(),
                        "items": s.number_of_items(), "cost": s.cost()})

    params.new_solution_callback = on_solution
    output = psi.optimize(instance, params)
    seconds = time.perf_counter() - t0
    sol = output.solution

    bins = []
    placed = set()
    for i in range(sol.number_of_different_bins()):
        sb = sol.bin(i)
        items = []
        for it in sb.items:
            if it.mirror:
                raise SystemExit("PackingSolver mirrored a part although no mirror was allowed")
            index = it.item_type_id
            placed.add(index)
            items.append({"id": job["parts"][index]["id"], "index": index, "rotation": it.angle,
                          "translation": [it.bl_corner.x, it.bl_corner.y]})
        for _ in range(sb.copies):
            bins.append({"sheet": sb.bin_type_id, "items": items})
    unplaced = [p["id"] for i, p in enumerate(job["parts"]) if i not in placed]
    result = {"solver": "packingsolver", "objective": a.objective, "mode": a.mode,
              "time_limit": a.time_limit, "seconds": seconds,
              "bestAt": {"seconds": history[-1]["seconds"]} if history else None,
              "bins": bins, "unplaced": unplaced, "history": history,
              "bound": output.bin_packing_bound}
    a.result.parent.mkdir(parents=True, exist_ok=True)
    a.result.write_text(json.dumps(result, indent=1, default=str))
    print(f"{len(bins)} sheets, {len(unplaced)} unplaced, {seconds:.1f} s "
          f"(best at {result['bestAt']['seconds'] if history else '-'} s, {len(history)} improvements)")


if __name__ == "__main__":
    main()
