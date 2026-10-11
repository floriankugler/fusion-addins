"""The layout file's shape, version 1.

This is the contract between the language and its consumers (the preview
mesher, the Fusion emitter). Bump LAYOUT_VERSION on incompatible changes.
"""
from __future__ import annotations

from typing import Literal, TypedDict

LAYOUT_VERSION = 1

#: A polygon as rings of [u, v] points: exterior first, then holes.
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


class EdgeOpLayout(TypedDict):
    kind: Literal["edge"]
    face: str
    s: float
    t: float
    op: HoleLayout | PocketLayout


OpLayout = CutLayout | PocketLayout | HoleLayout | ChamferLayout | EdgeOpLayout


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
    manual: bool
    ops: list[OpLayout]


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


class Layout(TypedDict):
    version: int
    units: Literal["mm"]
    frame: dict[str, str]
    modules: list[ModuleLayout]
    problems: list[str]
