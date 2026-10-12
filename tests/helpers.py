"""What several test files share: the usual materials, a carcass, and
helpers that look at outlines, meshes and hardware bodies."""
from __future__ import annotations

import warnings
from typing import Any

import trimesh
from shapely.geometry import Point

from lang import Board, Box, Scope, board, check, material, module, no_interference, rect
from lang.core.layout import build_layout
from lang.core.layout_types import HardwareBodyLayout
from lang.preview.mesh import mesh_part

ply9 = material("birch", t=9)
ply12 = material("birch", t=12)
ply15 = material("birch", t=15)
ply18 = material("birch", t=18)


def carcass(toekick: bool = False, back: bool = True) -> tuple[Scope, dict[str, Board]]:
    """Sides on the left and right (y), bottom and top between them and,
    with `back`, a 9 mm back between all four, in a 600 wide, 500 deep, 720
    high box: depth runs along x (front at 0), width along y, height along
    z. `toekick` notches both sides 60 deep and 100 high at the front."""
    with module("cab", Box.from_size(width=600, depth=500, height=720)) as cab:
        left = board("left", ply15).on(cab.left)
        right = board("right", ply15).on(cab.right)
        if toekick:
            for side in (left, right):
                side.cut(rect(depth=60, height=100), at=side.outer.bottom.front)
        bottom = board("bottom", ply15).on(cab.bottom).between(left, right)
        top = board("top", ply15).on(cab.top).between(left, right)
        parts = {"left": left, "right": right, "bottom": bottom, "top": top}
        if back:
            parts["back"] = board("back", ply9).on(cab.back).between(left, right, bottom, top)
        check(no_interference)
    return cab, parts


def has_material(part: Board, *points: tuple[float, float]) -> list[bool]:
    """Whether the part's outline covers each point (u, v)."""
    return [bool(part.outline.geometry.contains(Point(p))) for p in points]


def state(*parts: Board) -> list[tuple[str, list[Any]]]:
    """Each part's outline (as WKT) and operations: what a failed join
    must leave as it was."""
    return [(p.outline.geometry.wkt, list(p.ops)) for p in parts]


def part_meshes() -> dict[str, Any]:
    """Every part of the build meshed as the preview meshes it, by path."""
    layout = build_layout()
    return {p["path"]: mesh_part(p, layout["frame"]) for m in layout["modules"] for p in m["parts"]}


def overlap(a: Any, b: Any) -> float:
    """The volume two meshes share (mm³)."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)       # trimesh on a result without volume
        common = trimesh.boolean.intersection([a, b], engine="manifold")
        return float(common.volume) if len(common.faces) else 0.0


def bounds(body: HardwareBodyLayout) -> tuple[list[float], list[float]]:
    """A hardware body's bounding box, (min, max)."""
    boxes = body["boxes"]
    return ([min(b["min"][i] for b in boxes) for i in range(3)], [max(b["max"][i] for b in boxes) for i in range(3)])
