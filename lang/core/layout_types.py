"""The layout file's shape, version 1.

This is the contract between the language and its consumers (the preview
mesher, the Fusion emitter). Bump LAYOUT_VERSION on incompatible changes.
"""
from __future__ import annotations

from typing import Literal, NotRequired, TypedDict

LAYOUT_VERSION = 1

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


class ModelAxesDict(TypedDict):
    x: str
    y: str
    z: str


class CutLayout(TypedDict):
    kind: Literal["cut"]
    name: str | None
    chamfer: float
    shape: Rings


class PocketLayout(TypedDict):
    kind: Literal["pocket"]
    name: str | None
    face: str
    depth: float
    depth_spec: str
    chamfer: float
    shape: Rings


class HoleLayout(TypedDict):
    kind: Literal["hole"]
    name: str | None
    face: str
    u: float
    v: float
    d: float
    depth: float
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


OpLayout = CutLayout | PocketLayout | HoleLayout | ChamferLayout | VGrooveLayout | EdgeOpLayout


class PartLayout(TypedDict):
    path: str
    kind: Literal["board"]
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
    #: The body's name inside the model file.
    name: str
    #: Where the body goes, in the model's own frame (mm); non-zero when a
    #: file holds a pair whose spacing the build decides.
    offset: list[float]
    #: The body's bounding box in the model's frame (mm), for the preview.
    envelope: BoxDict


class HardwareLayout(TypedDict):
    """A bought part placed from a model file: the file's frame mapped to
    world directions and a world origin."""
    path: str
    kind: Literal["hardware"]
    name: str
    #: Model file, relative to the repository root.
    model: str
    #: The same model as a mesh (glTF) for the preview, or None.
    mesh: str | None
    #: World origin of the model's origin, mm.
    origin: list[float]
    #: World direction code (`+y`, `-x`, ...) of each model axis.
    axes: ModelAxesDict
    bodies: list[HardwareBodyLayout]


class ModuleLayout(TypedDict):
    path: str
    box: BoxDict | None
    parts: list[PartLayout]
    hardware: list[HardwareLayout]
    exports: dict[str, ExportValue | float | str]
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
    problems: list[str]
    #: Snapshots of the master the build read (absent in older layouts).
    snapshots: NotRequired[list[SnapshotLayout]]
