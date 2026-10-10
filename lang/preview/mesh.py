"""Meshes a layout into a glTF scene for the browser viewer.

Each board is its outline extruded by its thickness, with pockets and holes
subtracted through mesh booleans (manifold). Chamfers are not shown.
"""
from __future__ import annotations

import hashlib
from pathlib import Path

import numpy as np
import trimesh
from shapely.geometry import Polygon
from trimesh.creation import extrude_polygon

AXES = ("x", "y", "z")


def _material_color(label: str) -> list[int]:
    h = hashlib.md5(label.encode()).digest()
    # muted wood-like palette, varied by material
    return [170 + h[0] % 60, 130 + h[1] % 50, 80 + h[2] % 40, 255]


def _polygon(rings) -> Polygon:
    return Polygon(rings[0], holes=rings[1:]) if len(rings) > 1 else Polygon(rings[0])


def _part_transform(part: dict) -> np.ndarray:
    """4x4 taking the part's (u, v, t) frame to world: u, v, t are world
    axes, so the matrix is a permutation plus the part's box minimum."""
    axes = part["axes"]
    m = np.eye(4)
    m[:3, :3] = 0.0
    for col, key in enumerate(("u", "v", "t")):
        m[AXES.index(axes[key]), col] = 1.0
    box_min = part["box"]["min"]
    # the outline is in world u/v coordinates already; only t needs the offset
    m[AXES.index(axes["t"]), 3] = box_min[AXES.index(axes["t"])]
    return m


def mesh_part(part: dict) -> trimesh.Trimesh | None:
    t = part["thickness"]
    outline = _polygon(part["outline"])
    if outline.is_empty:
        return None
    mesh = extrude_polygon(outline, t)
    tools = []
    axes = part["axes"]
    for op in part["ops"]:
        if op["kind"] == "pocket":
            depth = min(op["depth"], t)
            tool = extrude_polygon(_polygon(op["shape"]), depth + 0.01)
            tools.append(_from_face(tool, op["face"], axes, t, depth))
        elif op["kind"] == "hole":
            depth = min(op["depth"], t)
            tool = trimesh.creation.cylinder(radius=op["d"] / 2, height=depth + 0.01, sections=24)
            tool.apply_translation([op["u"], op["v"], (depth + 0.01) / 2])
            tools.append(_from_face(tool, op["face"], axes, t, depth))
    if tools:
        try:
            mesh = trimesh.boolean.difference([mesh] + tools, engine="manifold")
        except BaseException:
            pass
    mesh.apply_transform(_part_transform(part))
    mesh.visual.face_colors = _material_color(part["material"])
    mesh.metadata["path"] = part["path"]
    return mesh


def _from_face(tool: trimesh.Trimesh, face: str, axes: dict, t: float, depth: float) -> trimesh.Trimesh:
    """Moves a tool built upward from z=0 so that it starts at the named
    big face and goes into the part. Faces named by a direction whose sign
    on the t axis is positive are the top (t = thickness) face."""
    from ..core import directions
    d = directions.frame.direction(face)
    if d.axis != axes["t"]:
        # operation on a narrow face: not meshed in phase 1
        return trimesh.Trimesh()
    if d.sign > 0:
        tool.apply_translation([0, 0, t - depth - 0.005])
    else:
        tool.apply_translation([0, 0, -0.005])
    return tool


def build_scene(layout: dict) -> trimesh.Scene:
    scene = trimesh.Scene()
    for module in layout["modules"]:
        for part in module["parts"]:
            mesh = mesh_part(part)
            if mesh is not None and len(mesh.faces):
                scene.add_geometry(mesh, node_name=part["path"], geom_name=part["path"])
    return scene


def write_scene(layout: dict, path: str | Path) -> None:
    scene = build_scene(layout)
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    scene.export(str(path))
