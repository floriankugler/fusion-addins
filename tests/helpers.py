"""What several test files share: the usual materials, a carcass, and
helpers that look at outlines, meshes and hardware bodies."""
from __future__ import annotations

import copy
import runpy
import sys
import warnings
from pathlib import Path
from typing import Any

import trimesh
from shapely.geometry import Point

from lang import Board, Box, Scope, board, check, sheet_material, module, no_interference, rect
from lang.core.layout import build_layout
from lang.core.layout_types import HardwareBodyLayout, Layout
from lang.core.scope import registry
from lang.preview.mesh import mesh_part

#: The example build files, which import their stock and each other from their folder.
EXAMPLES = Path(__file__).resolve().parents[1] / "examples"

ply9 = sheet_material("birch", t=9)
ply12 = sheet_material("birch", t=12)
ply15 = sheet_material("birch", t=15)
ply18 = sheet_material("birch", t=18)


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


def run_example(path: Path, run_name: str = "__build__") -> None:
    """Runs a build file in this process, and its lazy modules' bodies, as
    `lang.build.run` does, its registry kept for the test, with the
    examples' folder on the import path as `lang.build` puts the build
    file's folder there (a copy in a temporary folder still finds `stock`
    and `drawer_cabinet`)."""
    folders = [str(EXAMPLES)] + ([str(path.parent)] if path.parent != EXAMPLES else [])
    before = set(sys.modules)
    sys.path[:0] = folders
    try:
        runpy.run_path(str(path), run_name=run_name)
        registry.run_bodies()
    finally:
        del sys.path[:len(folders)]
        for name in set(sys.modules) - before:       # imported afresh by the next test
            file = getattr(sys.modules[name], "__file__", None)
            if file and any(Path(file).resolve().is_relative_to(f) for f in folders):
                del sys.modules[name]


def merged_layouts(build_files: list[Path]) -> Layout:
    """The layouts of several build files as one, each part's and nest's
    path after its file's name (`shelf:shelf.left`): for nesting the
    examples' parts together, which the nest command does not (one source
    per nest [decided 2026-10-16]). The files must share their world frame."""
    from lang.build import layout_of
    layouts = [(path.stem, layout_of(path)) for path in build_files]
    first = layouts[0][1]
    out: Layout = {"version": first["version"], "units": first["units"], "frame": first["frame"], "modules": [],
                   "problems": [], "snapshots": [], "sheet_materials": {}}
    for name, layout in layouts:
        assert layout["frame"] == first["frame"], f"{name} is written in another world frame"
        for module_ in copy.deepcopy(layout["modules"]):
            module_["path"] = f"{name}:{module_['path']}"
            for part in module_["parts"]:
                part["path"] = f"{name}:{part['path']}"
            for nest in module_["nests"]:
                nest["path"], nest["module"] = f"{name}:{nest['path']}", f"{name}:{nest['module']}"
                nest["parts"] = [f"{name}:{p}" for p in nest["parts"]]
                nest["left_out"] = [f"{name}:{p}" for p in nest["left_out"]]
            out["modules"].append(module_)
        out["problems"] += [f"{name}: {p}" for p in layout["problems"]]
        out["snapshots"] += layout["snapshots"]
        for label, material in layout["sheet_materials"].items():
            assert out["sheet_materials"].setdefault(label, material) == material, f"two materials {label}"
    return out
