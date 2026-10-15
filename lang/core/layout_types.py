"""The layout file's shape, version 6.

This is the contract between the language and its consumers (the preview
mesher, the Fusion emitter, the viewer page, the nest). Bump LAYOUT_VERSION
on incompatible changes; `lang.emit.plan` and the viewer repeat it and
refuse other versions.

Version 6 (2026-10-15): a part carries `nest`, whether it goes into the
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

LAYOUT_VERSION = 6

#: One or more polygons as rings of [u, v] points, one polygon after the
#: other: its exterior ring, counter-clockwise, then its holes, clockwise.
#: A pocket or cut with several pieces (a cutout's openings) has several
#: counter-clockwise rings.
Rings = list[list[list[float]]]


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
    #: machine (world name).
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


class ModuleLayout(TypedDict):
    path: str
    box: BoxDict | None
    parts: list[PartLayout]
    hardware: list[HardwareLayout]
    exports: dict[str, ExportValue | float | str]
    #: This module's problems: its checks' and the notes its parts left.
    #: The layout's `problems` repeat them.
    problems: list[str]


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
