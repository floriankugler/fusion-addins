"""The snapshot file's shape, version 1.

A snapshot is the master document read once in Fusion (`lang.emit.snapshot`)
and the compile's only view of it (`lang.master`). World millimetres; the
master's axes are the world axes. Bump SNAPSHOT_VERSION on incompatible
changes.
"""
from __future__ import annotations

from typing import TypedDict

SNAPSHOT_VERSION = 1


class PlaneDict(TypedDict):
    #: A point on the plane.
    origin: list[float]
    #: Unit normal.
    normal: list[float]


class ContourDict(TypedDict):
    """One sketch: its curves as one chain, sampled to a polyline."""
    #: The chain's points in order; a closed chain does not repeat its first point.
    points: list[list[float]]
    closed: bool
    #: The sketch's plane.
    plane: PlaneDict


class BoxDict(TypedDict):
    """A body as its axis-aligned bounding box."""
    min: list[float]
    max: list[float]
    #: Whether the body is an axis-aligned cuboid, i.e. fills its box.
    cuboid: bool


class ParameterDict(TypedDict):
    #: mm for a length, degrees for an angle, else Fusion's value as it is.
    value: float
    #: Fusion's unit string ("mm", "deg", "" for unitless).
    unit: str
    expression: str


class ProblemDict(TypedDict):
    """A name the snapshot could not take; using it is an error that
    repeats this message."""
    #: "planes", "contours", "boxes" or "parameters".
    kind: str
    name: str
    message: str


class SnapshotDict(TypedDict):
    version: int
    units: str
    #: The master document's name.
    source: str
    #: sha256 of the content (everything but `source` and `hash`).
    hash: str
    planes: dict[str, PlaneDict]
    contours: dict[str, ContourDict]
    boxes: dict[str, BoxDict]
    parameters: dict[str, ParameterDict]
    problems: list[ProblemDict]
