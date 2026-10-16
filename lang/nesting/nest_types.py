"""The nest file's shape, version 2: what `python -m lang.nesting` writes
per nest (`nest.json`), read by the preview and the Fusion emitter
(`lang.emit.nested`, which repeats `NEST_VERSION` and refuses others).

Version 2 (2026-10-16): a nest of the build, named (`name`) and dated
(`written`); `settings` the values resolved from the build's settings with
their sources and the stock given; per material `bought` counts the sheets
bought only and `on_hand_used` lists the pieces of the inventory used
(was `offcuts_used`); a piece of stock says whether it was `bought`; a
blank whether it is a `nest(False)` board's own (`own_blank`). What the
emitter reads (`materials`: `material`, `thickness`, `sheets`: `name`,
`stock`, `size`, `blanks`: `name`, `rect`, `parts`: `path`, `transform`;
`problems`) is as in version 1.

Millimetres. A sheet's frame: x along its length (the grain), y across,
from its corner. A blank's frame likewise, from the blank's corner; each
part on it is given by `transform`, world millimetres to the blank's
frame, the part flat with its machining face up at z = its thickness.
"""
from __future__ import annotations

from typing import Literal, TypedDict

NEST_VERSION = 2


class PlacedPart(TypedDict):
    path: str
    #: The machining face (world name), which faces up.
    up: str
    #: The turn (degrees, counter-clockwise) of the part's outline as seen
    #: from its machining face, and where its frame's origin lies on the
    #: blank (`lang.nesting.items`).
    turn: float
    at: list[float]
    #: World mm to the blank's frame: a 3 x 4 matrix, rows x, y, z.
    transform: list[list[float]]


class BlankOut(TypedDict):
    #: `<sheet>.<blank>`, both counted from 1 in the order they are sawn.
    name: str
    #: x, y, w, h on its sheet.
    rect: list[float]
    parts: list[PlacedPart]
    #: A `nest(False)` board's own blank: sawn to its size, no margin, its
    #: outline cut by hand; it may be larger than the bed.
    own_blank: bool


class CutOut(TypedDict):
    #: The cut's middle line, x0, y0, x1, y1 on the sheet, edge to edge of
    #: the piece it splits.
    line: list[float]
    #: The piece it splits, x, y, w, h.
    piece: list[float]


class RestOut(TypedDict):
    rect: list[float]
    #: Kept as stock (the nest's keep_across and keep_area), else waste.
    keep: bool


class SheetOut(TypedDict):
    #: Counted from 1.
    name: str
    #: A sheet (the material's size) or an offcut (smaller).
    stock: Literal["sheet", "offcut"]
    #: Bought, or from the stock on hand (the inventory).
    bought: bool
    #: Length (along the grain) and width.
    size: list[float]
    #: The saw cuts, in the order they are made.
    cuts: list[CutOut]
    blanks: list[BlankOut]
    rests: list[RestOut]


class MaterialOut(TypedDict):
    material: str
    thickness: float
    sheets: list[SheetOut]
    #: How many sheets are bought, by size (`2500x1250`); stock on hand apart.
    bought: dict[str, int]
    #: The pieces on hand used (`1250x600`), sheets and offcuts alike.
    on_hand_used: list[str]
    #: Areas in m2: the parts', the stock sawn or used, what is left as
    #: stock (kept rests and pieces on hand sawn), the stock used less that.
    parts_area: float
    stock_area: float
    kept_area: float
    used_area: float
    #: Parts the stock could not take.
    unplaced: list[str]
    #: How the saw plan was found (the setting kept), and the solver's times.
    notes: list[str]


class LeftOutPart(TypedDict):
    path: str
    material: str
    #: `nest(False)`, `manual` or `slat` (slats go on the cut list by length).
    why: str


class NestSettings(TypedDict):
    """The values the nest ran with (`lang.nesting.keys`), resolved from the
    build's settings, and the stock it was given."""
    bed: list[float]
    #: The least spacing between two parts; `part_spacing` the parts that
    #: asked for more (between two parts the larger holds).
    spacing: float
    part_spacing: dict[str, float]
    margin: float
    kerf: float
    max_cuts: int
    keep_across: float
    keep_area: float
    #: The nest's time per material at most (s), `rate` a part, at least
    #: `least_seconds`; each material's own time is in its notes.
    seconds: float
    rate: float
    least_seconds: float
    refill: bool
    #: Where each value came from: the nest, a scope's or part's path,
    #: "root", or "default"; several parts' sources each once.
    sources: dict[str, str]
    #: The sheets that could be bought, by material (`2500x1250`).
    buy: dict[str, str]
    #: The stock on hand given (`birch 15:1250x600*2`).
    on_hand: list[str]


class NestFile(TypedDict):
    version: int
    #: The nest's path in the build (`kitchen.carcass`); "" for a nest of
    #: parts given another way (tests).
    name: str
    #: When the nest was written, ISO 8601 with the time zone.
    written: str
    #: The layout nested: its build file (or layout file) and the hash of
    #: its content (`lang.core.layout.layout_hash`), which tells a reader
    #: whether the nest is the layout's it shows.
    source: str
    layout_hash: str
    settings: NestSettings
    materials: list[MaterialOut]
    #: The boards of the nest's kind that it leaves out, and why.
    left_out: list[LeftOutPart]
    #: What the nest could not do or found wrong in its own result.
    problems: list[str]


__all__ = ["NEST_VERSION", "PlacedPart", "BlankOut", "CutOut", "RestOut", "SheetOut", "MaterialOut", "LeftOutPart",
           "NestSettings", "NestFile"]
