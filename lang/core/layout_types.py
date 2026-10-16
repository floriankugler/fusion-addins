"""The layout file's shape, version 8.

This is the contract between the language and its consumers (the preview
mesher, the Fusion emitter, the viewer page, the nest). Bump LAYOUT_VERSION
on incompatible changes; `lang.emit.plan` and the viewer repeat it and
refuse other versions.

Version 8 (2026-10-16): each module lists its `nests`, declared and
default, with their parts and own settings, and the layout its sheet
`sheet_materials` with their sizes. Version 7 (2026-10-16): a part carries `settings`, the settings set along
its chain with the node that set each, and `op_settings`, its named
operations' own. Version 6 (2026-10-15): a part carries `nest`, whether it goes into the
nest. Version 5 (2026-10-14): parts are boards or slats (`kind`), and a slat
carries its `section`. Version 4 (2026-10-14): a pocket carries `slot`, its centre line when it
is a slot. Version 3 (2026-10-12): every key below is written; the top-level
`problems` list every problem once, the modules' repeat their own; a
depth through a narrow face is the part's extent across it. Version 2
layouts were written while parts gained `machine`, `grained` and `faces`
and modules `hardware`, so some lack them.
"""
from __future__ import annotations

from typing import Literal, NotRequired, TypedDict

LAYOUT_VERSION = 8

#: One or more polygons as rings of [u, v] points, one polygon after the
#: other: its exterior ring, counter-clockwise, then its holes, clockwise.
#: A pocket or cut with several pieces (a cutout's openings) has several
#: counter-clockwise rings.
Rings = list[list[list[float]]]

#: What a setting's value is in the layout: JSON data.
type JsonValue = None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]


class SettingLayout(TypedDict):
    """A setting's value for a part (`lang.core.settings`), and where it
    came from: the node that set it (a scope's or part's path, an
    operation's, "root" outside every module), or "default", or the master
    parameter that gave the default ("master: Spalt")."""
    value: JsonValue
    source: str


class BoxDict(TypedDict):
    min: list[float]
    max: list[float]


class AxesDict(TypedDict):
    t: str
    u: str
    v: str


class CutLayout(TypedDict):
    kind: Literal["cut"]
    name: str | None
    chamfer: float
    shape: Rings


class SlotLayout(TypedDict):
    """A slot's centre line: the centres of its round ends, as [u, v] in
    the frame of the face it is cut from, and its width."""
    start: list[float]
    end: list[float]
    width: float


class PocketLayout(TypedDict):
    kind: Literal["pocket"]
    name: str | None
    face: str
    #: mm from the face; through a big face it is the thickness, through a
    #: narrow face the board's extent across it.
    depth: float
    #: How the build file gave the depth, for a reader only (`lang.core.ops`).
    depth_spec: str
    chamfer: float
    shape: Rings
    #: The centre line of a slot (`shape` is the slot itself), else None.
    slot: SlotLayout | None


class HoleLayout(TypedDict):
    kind: Literal["hole"]
    name: str | None
    face: str
    u: float
    v: float
    d: float
    #: mm from the face, as for a pocket.
    depth: float
    #: How the build file gave the depth, for a reader only.
    depth_spec: str
    through: bool
    chamfer: float


class ChamferLayout(TypedDict):
    kind: Literal["chamfer"]
    what: str
    size: float
    face: str


class VGrooveLayout(TypedDict):
    """A 90 degree V-groove along the line from `start` to `end` (u, v) in a
    big face, `depth` deep, its ends cut square."""
    kind: Literal["vgroove"]
    name: str | None
    face: str
    start: list[float]
    end: list[float]
    depth: float


class EdgeOpLayout(TypedDict):
    kind: Literal["edge"]
    face: str
    s: float
    t: float
    op: HoleLayout | PocketLayout
    #: How far in front of the face the operation starts (mm, absent when
    #: it starts at the face): a box joint's finger grooves start at the
    #: fingers' tips, past the board's box.
    offset: NotRequired[float]


OpLayout = CutLayout | PocketLayout | HoleLayout | ChamferLayout | VGrooveLayout | EdgeOpLayout


class PartLayout(TypedDict):
    path: str
    #: A board, or a slat (solid wood by section and length, cosmetic for
    #: now: it has no operations).
    kind: Literal["board", "slat"]
    #: A slat's section, the smaller size first; None for a board.
    section: list[float] | None
    material: str
    thickness: float
    axes: AxesDict
    box: BoxDict
    origin: list[float]
    outline: Rings
    grain: str | None
    show: str
    #: The big face the part is machined from, which faces up on the
    #: machine (world name): what `machine()` names, else the face more
    #: operations are made from, else the show face.
    machine: str
    #: Whether the material has a grain (`grain` may still be None, unset).
    grained: bool
    manual: bool
    #: Whether the part goes into the nest: False for `nest(False)`, a
    #: manual part and a slat (slats go on the cut list by length).
    nest: bool
    ops: list[OpLayout]
    #: What the build file calls each face, by world name: the direction in
    #: the frame of the part's scope (a cabinet's own front and left), then
    #: `inner` or `outer` for a big face when they resolve. For the preview's
    #: labels.
    faces: dict[str, list[str]]
    #: The settings set along the part's chain (the part, its scopes, the
    #: root), by key name, as they hold for the part, and the keys it read
    #: from their defaults; a key whose value the layout does not take
    #: (one that is not JSON data) is left out.
    settings: dict[str, SettingLayout]
    #: The named operations' own settings (`left.toekick.use(...)`), by
    #: operation name; an operation that uses none is not listed.
    op_settings: dict[str, dict[str, SettingLayout]]


class ExportValue(TypedDict):
    axis: str
    value: float


class HardwareBodyLayout(TypedDict):
    #: The body's name within its hardware item.
    name: str
    #: The body's shape: boxes along the world axes (mm), touching or
    #: overlapping, whose union is the body.
    boxes: list[BoxDict]


class HardwareLayout(TypedDict):
    """A bought part, drawn as simple boxes: the space it takes, not its
    detail. Each body is one piece of it (a left and a right runner)."""
    path: str
    kind: Literal["hardware"]
    name: str
    bodies: list[HardwareBodyLayout]


class NestLayout(TypedDict):
    """A nest of the build (`lang.core.nests`): declared on a scope, or the
    default nest of a module's nested boards of a material that no declared
    nest names."""
    #: Its scope's path and its name (`kitchen.carcass`); a default nest's
    #: name is its material's label made file-safe (`kitchen.birch_15`, at
    #: the root `birch_15`).
    path: str
    #: The module it belongs to ("" at the root).
    module: str
    #: How its parts were chosen: the nested boards of a material in its
    #: scope, boards named, or what no declared nest names.
    by: Literal["material", "parts", "default"]
    #: Its material's label (`birch 15`), None for one of boards named.
    material: str | None
    #: Its parts' paths, in the build's order; a `nest(False)` board named
    #: is its own blank.
    parts: list[str]
    #: The boards of its material in its scope that no nest takes
    #: (`nest(False)`, manual), for a nest by material or by default.
    left_out: list[str]
    #: The settings the nest itself uses, with their source.
    settings: dict[str, SettingLayout]


class MaterialLayout(TypedDict):
    """A sheet material the boards are made of, by its label."""
    thickness: float
    grain: bool
    #: Its sheet's size (mm, along the grain first), the sheets bought;
    #: None when the build gives none.
    size: list[float] | None


class ModuleLayout(TypedDict):
    path: str
    box: BoxDict | None
    parts: list[PartLayout]
    hardware: list[HardwareLayout]
    exports: dict[str, ExportValue | float | str]
    #: This module's problems: its checks' and the notes its parts left.
    #: The layout's `problems` repeat them.
    problems: list[str]
    #: The nests of the module and the modules in it.
    nests: list[NestLayout]


class SnapshotBoxLayout(TypedDict):
    min: list[float]
    max: list[float]
    cuboid: bool


class SnapshotContourLayout(TypedDict):
    points: list[list[float]]
    closed: bool


class SnapshotLayout(TypedDict):
    """A snapshot of the master the build read: its hash, and its boxes and
    contours for the preview to draw around the modules."""
    #: The snapshot file's name.
    file: str
    #: The master document's name.
    source: str
    hash: str
    boxes: dict[str, SnapshotBoxLayout]
    contours: dict[str, SnapshotContourLayout]


class Layout(TypedDict):
    version: int
    units: Literal["mm"]
    frame: dict[str, str]
    modules: list[ModuleLayout]
    #: Every problem of the build, once: the modules' and the snapshots'
    #: notes. What a consumer shows or reports.
    problems: list[str]
    #: Snapshots of the master the build read.
    snapshots: list[SnapshotLayout]
    #: The sheet materials of the boards, by label. (Not `materials`: the
    #: compiler add-in tells a nest file by that key.)
    sheet_materials: dict[str, MaterialLayout]
