"""Meshes a layout into a glTF scene for the browser viewer.

Each board is its outline extruded by its thickness, with pockets and holes
subtracted through mesh booleans (manifold). Chamfers are not shown, and
operations on narrow faces are not meshed yet.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
import trimesh
from shapely.geometry import Polygon
from trimesh.creation import extrude_polygon

from ..core.layout_types import Layout, PartLayout, Rings

AXES = ("x", "y", "z")


def _polygon(rings: Rings) -> Polygon:
    return Polygon(rings[0], holes=rings[1:]) if len(rings) > 1 else Polygon(rings[0])


def _part_transform(part: PartLayout) -> Any:
    """4x4 taking the part's (u, v, t) frame to world: u, v, t are world
    axes, so the matrix is a permutation plus the thickness offset. The
    outline is already in world u/v coordinates."""
    axes = part["axes"]
    m = np.eye(4)
    m[:3, :3] = 0.0
    for col, key in enumerate(("u", "v", "t")):
        m[AXES.index(axes[key]), col] = 1.0
    t_index = AXES.index(axes["t"])
    m[t_index, 3] = part["box"]["min"][t_index]
    return m


def _from_face(tool: Any, face: str, frame: dict[str, str], t_axis: str, t: float, depth: float) -> Any:
    """Moves a tool built upward from z=0 so that it starts at the named big
    face and goes into the part. A narrow face yields an empty tool. Face
    names are the layout's world names, decoded with its frame."""
    code = frame[face]
    if code[1] != t_axis:
        return trimesh.Trimesh()
    tool.apply_translation([0, 0, t - depth - 0.005 if code[0] == "+" else -0.005])
    return tool


def mesh_part(part: PartLayout, frame: dict[str, str]) -> Any:
    t = part["thickness"]
    outline = _polygon(part["outline"])
    if outline.is_empty:
        return None
    mesh = extrude_polygon(outline, t)
    tools: list[Any] = []
    t_axis = part["axes"]["t"]
    for op in part["ops"]:
        if op["kind"] == "pocket":
            depth = min(op["depth"], t)
            tool = extrude_polygon(_polygon(op["shape"]), depth + 0.01)
            tools.append(_from_face(tool, op["face"], frame, t_axis, t, depth))
        elif op["kind"] == "hole":
            depth = min(op["depth"], t)
            tool = trimesh.creation.cylinder(radius=op["d"] / 2, height=depth + 0.01, sections=24)
            tool.apply_translation([op["u"], op["v"], (depth + 0.01) / 2])
            tools.append(_from_face(tool, op["face"], frame, t_axis, t, depth))
    tools = [tool for tool in tools if len(tool.faces)]
    if tools:
        try:
            mesh = trimesh.boolean.difference([mesh] + tools, engine="manifold")
        except BaseException:
            pass
    mesh.apply_transform(_part_transform(part))
    mesh.metadata["path"] = part["path"]
    return mesh


def build_scene(layout: Layout) -> Any:
    scene = trimesh.Scene()
    for module in layout["modules"]:
        for part in module["parts"]:
            mesh = mesh_part(part, layout["frame"])
            if mesh is not None and len(mesh.faces):
                scene.add_geometry(mesh, node_name=part["path"], geom_name=part["path"])
    return scene


def write_scene(layout: Layout, path: str | Path) -> None:
    scene = build_scene(layout)
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    scene.export(str(path))
