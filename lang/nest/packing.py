"""Nesting parts on rectangles with PackingSolver's irregular solver
(`pip install packingsolver`, MIT; see `design/nesting.md` for why this
solver and what was measured).

Each rectangle (a blank size, an offcut, the room left on a blank) is a bin
type with its copies and cost; parts are item types with their own turns.
How PackingSolver is used, and its quirks worked around [found in the
experiments, 2026-10-14]:

- The margin to a bin's edge is kept by shrinking the bin, not by
  `item_bin_minimum_spacing`: a part that fits a bin but not within that
  spacing is placed anyway, centred, the gaps shrunk on both sides.
- A defect (a part already on a blank) is kept the spacing off only with
  the spacing set on each defect.
- A cost of 0 and a bin type of no copies are refused, so a piece on hand
  costs 1 against a sheet's millions, and empty types are left out.
- Bin packing returns nothing when the bins cannot take every part;
  knapsack places what fits.
- A placement is the part turned about its own origin by `angle`
  (counter-clockwise), then moved by `bl_corner` (despite the name, not the
  corner of its bounding box).
"""
from __future__ import annotations

import importlib
from dataclasses import dataclass, field
from typing import Any

from shapely import Polygon
from shapely.geometry.polygon import orient

from .items import Item

# PackingSolver is a compiled extension without stubs; pyright sees its
# modules as Any.
ps: Any = importlib.import_module("packingsolver")
psi: Any = importlib.import_module("packingsolver.irregular")

#: Objectives by name.
VARIABLE = ps.Objective.VariableSizedBinPacking
KNAPSACK = ps.Objective.Knapsack
#: Optimisation modes by name (`seconds` limits the anytime one).
MODES = {"anytime": ps.OptimizationMode.Anytime,
         "deterministic": ps.OptimizationMode.NotAnytimeDeterministic}


@dataclass
class Bin:
    """A rectangle to nest on: (0, 0) to (width, height)."""
    width: float
    height: float
    #: How many there are; -1: as many as needed.
    copies: int
    cost: float
    #: Shapes already on it, kept the spacing off.
    defects: list[Polygon] = field(default_factory=list[Polygon])


@dataclass(frozen=True)
class Placement:
    #: The item's index in the list given.
    item: int
    turn: float
    at: tuple[float, float]


@dataclass
class Packed:
    """A bin used: its index in the list given, and what is on it."""
    bin: int
    placements: list[Placement]


@dataclass
class Result:
    packed: list[Packed]
    #: Indices of the items placed on no bin.
    unplaced: list[int]


def pack(items: list[Item], indices: list[int], bins: list[Bin], spacing: float, margin: float,
         objective: Any, seconds: float, mode: str = "anytime") -> Result:
    """Nests `items[i]` for i in `indices` on `bins` (each shrunk by
    `margin`), at least `spacing` apart and from the bins' defects."""
    b = psi.InstanceBuilder()
    b.set_objective(objective)
    b.set_item_item_minimum_spacing(spacing)
    type_of: list[int] = []
    for k, bin_ in enumerate(bins):
        w, h = bin_.width - 2 * margin, bin_.height - 2 * margin
        if bin_.copies == 0 or w <= 0 or h <= 0:
            continue
        type_of.append(k)
        bt = b.add_bin_type(psi.build_rectangle(margin, margin + w, margin, margin + h),
                            copies=bin_.copies, cost=max(bin_.cost, 1.0))
        for defect in bin_.defects:
            d = b.add_defect(bt, -1, psi.ShapeWithHoles(_shape(defect.exterior.coords), []))
            b.set_item_defect_minimum_spacing(bt, d, spacing)
    for i in indices:
        item = items[i]
        b.add_item_type(_item_shape(item.solver), allowed_rotations=[(t, t, False) for t in item.turns], copies=1)
    if not type_of or not indices:
        return Result([], list(indices))
    params = psi.OptimizeParameters()
    params.time_limit = seconds
    params.verbosity_level = 0
    params.optimization_mode = MODES[mode]
    solution = psi.optimize(b.build(), params).solution
    packed: list[Packed] = []
    placed: set[int] = set()
    for k in range(solution.number_of_different_bins()):
        sb = solution.bin(k)
        placements: list[Placement] = []
        for it in sb.items:
            if it.mirror:
                raise RuntimeError("PackingSolver mirrored a part although no mirror was allowed.")
            index = indices[it.item_type_id]
            placed.add(index)
            placements.append(Placement(index, _turn(float(it.angle), items[index].turns),
                                        (float(it.bl_corner.x), float(it.bl_corner.y))))
        if not placements:
            continue
        for _ in range(sb.copies):
            packed.append(Packed(type_of[sb.bin_type_id], list(placements)))
    return Result(packed, [i for i in indices if i not in placed])


def _turn(angle: float, turns: tuple[float, ...]) -> float:
    """The solver's angle as one of the item's turns (it may come as -90 or
    270.0000001)."""
    for t in turns:
        if abs((angle - t + 180.0) % 360.0 - 180.0) < 1e-6:
            return t
    raise RuntimeError(f"PackingSolver turned a part by {angle:g} degrees, not one of its turns {turns}.")


def _shape(coords: Any) -> Any:
    """A ring as PackingSolver takes it: counter-clockwise, not closed."""
    ring = orient(Polygon(coords))
    return psi.build_shape([[float(x), float(y)] for x, y in list(ring.exterior.coords)[:-1]])


def _item_shape(p: Polygon) -> Any:
    # Every contour counter-clockwise, holes too.
    return psi.ShapeWithHoles(_shape(p.exterior.coords), [_shape(r.coords) for r in p.interiors])
