"""The nest file's shape, version 1: what `python -m lang.nesting` writes
(`nest.json`), read by the preview and the Fusion emitter
(`lang.emit.nested`, which repeats `NEST_VERSION` and refuses others).

Millimetres. A sheet's frame: x along its length (the grain), y across,
from its corner. A blank's frame likewise, from the blank's corner; each
part on it is given by `transform`, world millimetres to the blank's
frame, the part flat with its machining face up at z = its thickness.
"""
from __future__ import annotations

from typing import Literal, TypedDict

NEST_VERSION = 1


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


class CutOut(TypedDict):
    #: The cut's middle line, x0, y0, x1, y1 on the sheet, edge to edge of
    #: the piece it splits.
    line: list[float]
    #: The piece it splits, x, y, w, h.
    piece: list[float]


class RestOut(TypedDict):
    rect: list[float]
    #: Kept as stock (the workshop's keep_across and keep_area), else waste.
    keep: bool


class SheetOut(TypedDict):
    #: Counted from 1.
    name: str
    #: A sheet bought, or an offcut on hand.
    stock: Literal["sheet", "offcut"]
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
    #: How many sheets of each size are used (`2470x1240`), offcuts apart.
    bought: dict[str, int]
    #: The offcuts on hand used (`1250x600`).
    offcuts_used: list[str]
    #: Areas in m2: the parts', the stock sawn or used, what is left as
    #: stock (kept rests and offcuts sawn), the stock used less that.
    parts_area: float
    stock_area: float
    kept_area: float
    used_area: float
    #: Parts the stock on hand could not take.
    unplaced: list[str]
    #: How the saw plan was found (the setting kept), and the solver's times.
    notes: list[str]


class LeftOutPart(TypedDict):
    path: str
    material: str
    #: `nest(False)`, `manual` or `slat` (slats go on the cut list by length).
    why: str


class NestSettings(TypedDict):
    bed: list[float]
    spacing: float
    margin: float
    kerf: float
    max_cuts: int
    keep_across: float
    keep_area: float
    seconds: float
    #: The stock given, as the command line spells it.
    sheets: list[str]
    offcuts: list[str]


class Nest(TypedDict):
    version: int
    #: The layout nested: its build file (or layout file) and the hash of
    #: its content (`lang.nesting.layout_hash`), which tells a reader whether
    #: the nest is the layout's it shows.
    source: str
    layout_hash: str
    settings: NestSettings
    materials: list[MaterialOut]
    left_out: list[LeftOutPart]
    #: What the nest could not do or found wrong in its own result.
    problems: list[str]
