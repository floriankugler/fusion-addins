"""A nest (`lang.nesting`, `nest.json`) as the emitter draws it: one document
per material, each piece of stock with its blanks, each blank a stock body
with its parts flat on it, machining face up, named by path. Fusion-free
and unit tested, like `plan`; `fusion.emit_nest` draws it.

Where things go in the document (mm): the pieces of stock one above the
other along y, `GAP` apart, each blank at its place on its piece, z = 0 the
blank's underside. A part is drawn where the layout has it, with the
module documents' own steps, and its finished body is then moved into
place by `transform` (world to the document) and its facts with it
(`moved_facts`); every component sits at the origin. [Drawing inside a
component whose occurrence is moved failed: Fusion read the profiles in
the other space, "the path is tangent to the profile", 2026-10-14.]
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from .plan import PartFacts, PartPlan, Vec, plan_layout

if TYPE_CHECKING:
    from ..core.layout_types import Layout

#: The nest file version this reads (`lang.nesting.nest_types.NEST_VERSION`);
#: a test keeps the two equal. Versions 2 and 3 kept what this reads as it
#: was (3 added the parts' fingerprints and the second nests' fields).
NEST_VERSION = 3
#: mm between two pieces of stock in the document.
GAP = 200.0

Matrix = list[list[float]]      # 3 x 4, rows x, y, z, mm


@dataclass
class PlacedPartPlan:
    path: str
    part: PartPlan
    #: World mm to the document's, where the part lies on its blank.
    transform: Matrix


@dataclass
class BlankPlan:
    name: str
    #: Where the blank's corner lies in the document (mm), and its size.
    origin: tuple[float, float, float]
    size: tuple[float, float, float]
    parts: list[PlacedPartPlan] = field(default_factory=list[PlacedPartPlan])


@dataclass
class SheetPlan:
    name: str
    #: "sheet" or "offcut", its length and width, and its corner in the document.
    stock: str
    size: tuple[float, float]
    origin: tuple[float, float]
    blanks: list[BlankPlan] = field(default_factory=list[BlankPlan])


@dataclass
class NestDocPlan:
    """One material's document."""
    material: str
    thickness: float
    sheets: list[SheetPlan]
    #: The nest's own problems for this material.
    problems: list[str]


def check_nest_version(nest: Any) -> None:
    if not isinstance(nest, dict) or nest.get("version") != NEST_VERSION:  # pyright: ignore[reportUnknownMemberType]
        found = nest.get("version") if isinstance(nest, dict) else None  # pyright: ignore[reportUnknownMemberType]
        raise ValueError(f"nest version {found} is not supported (this reads {NEST_VERSION}).")


def plan_nest(nest: Any, layout: Layout, material: str | None = None) -> list[NestDocPlan]:
    """The documents a nest draws: one per material (or the one named)."""
    check_nest_version(nest)
    plan = plan_layout(layout)
    parts = {p.path: p for p in plan.parts}
    docs: list[NestDocPlan] = []
    for m in nest["materials"]:
        if material is not None and m["material"] != material:
            continue
        t = float(m["thickness"])
        sheets: list[SheetPlan] = []
        y = 0.0
        for s in m["sheets"]:
            length, width = float(s["size"][0]), float(s["size"][1])
            sheet = SheetPlan(str(s["name"]), str(s["stock"]), (length, width), (0.0, y))
            for b in s["blanks"]:
                bx, by, bw, bh = (float(v) for v in b["rect"])
                blank = BlankPlan(str(b["name"]), (bx, y + by, 0.0), (bw, bh, t))
                for p in b["parts"]:
                    path = str(p["path"])
                    if path not in parts:
                        raise ValueError(f"the nest places {path}, which the layout does not have.")
                    rows = [[float(v) for v in row] for row in p["transform"]]
                    rows[0][3] += bx
                    rows[1][3] += y + by
                    blank.parts.append(PlacedPartPlan(path, parts[path], rows))
                sheet.blanks.append(blank)
            sheets.append(sheet)
            y += width + GAP
        problems = [str(p) for p in nest["problems"] if str(p).startswith(f"{m['material']}:")]
        docs.append(NestDocPlan(str(m["material"]), t, sheets, problems))
    if material is not None and not docs:
        raise ValueError(f"the nest has no material {material!r}.")
    return docs


def apply(matrix: Matrix, point: tuple[float, float, float]) -> tuple[float, float, float]:
    """A world point (mm) in the frame `matrix` maps to."""
    x, y, z = (r[0] * point[0] + r[1] * point[1] + r[2] * point[2] + r[3] for r in matrix)
    return x, y, z


def turn(matrix: Matrix, v: Vec) -> Vec:
    """A world direction in the frame `matrix` maps to."""
    x, y, z = (r[0] * v[0] + r[1] * v[1] + r[2] * v[2] for r in matrix)
    return x, y, z


def moved_facts(facts: PartFacts, matrix: Matrix) -> PartFacts:
    """A part's facts for its body moved by `matrix`: its machining face
    up, its grain along the blank."""
    return PartFacts(facts.material, facts.thickness, facts.kind, facts.grained,
                     turn(matrix, facts.grain) if facts.grain is not None else None, turn(matrix, facts.up))
