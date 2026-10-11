"""Meshes a layout into a glTF scene for the browser viewer.

Each board is its outline extruded by its thickness, with pockets, holes
and V-grooves subtracted through mesh booleans (manifold). Chamfers are not
shown, and operations on narrow faces are not meshed yet.
"""
from __future__ import annotations

import math
from pathlib import Path
from typing import Any

import numpy as np
import trimesh
from shapely.geometry import Polygon
from trimesh.creation import extrude_polygon

from ..core.layout_types import BoxDict, HardwareLayout, Layout, PartLayout, Rings, VGrooveLayout

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


def _vgroove_tool(op: VGrooveLayout, frame: dict[str, str], t_axis: str, t: float) -> Any:
    """The groove as a prism in the part's (u, v, t) frame, its opening a
    little above the face so the boolean cuts cleanly. A narrow face
    yields an empty tool."""
    code = frame[op["face"]]
    if code[1] != t_axis:
        return trimesh.Trimesh()
    out = 1.0 if code[0] == "+" else -1.0
    face = t if out > 0 else 0.0
    (u0, v0), (u1, v1) = op["start"], op["end"]
    length = math.hypot(u1 - u0, v1 - v0)
    wu, wv = -(v1 - v0) / length, (u1 - u0) / length       # across the groove, in the face
    above = 0.01
    half = op["depth"] + above                              # 90 degrees: as wide on each side as deep
    points: list[tuple[float, float, float]] = []
    for u, v in ((u0, v0), (u1, v1)):
        points += [(u + wu * half, v + wv * half, face + out * above),
                   (u - wu * half, v - wv * half, face + out * above),
                   (u, v, face - out * op["depth"])]
    return trimesh.convex.convex_hull(np.array(points))


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
        elif op["kind"] == "vgroove":
            tools.append(_vgroove_tool(op, frame, t_axis, t))
    tools = [tool for tool in tools if len(tool.faces)]
    if tools:
        try:
            mesh = trimesh.boolean.difference([mesh] + tools, engine="manifold")
        except BaseException:
            pass
    mesh.apply_transform(_part_transform(part))
    mesh.metadata["path"] = part["path"]
    return mesh


def _axis_vector(code: str) -> Any:
    v = np.zeros(3)
    v["xyz".index(code[1])] = 1.0 if code[0] == "+" else -1.0
    return v


_mesh_cache: dict[str, list[Any]] = {}


def _model_pieces(path: Path) -> list[Any]:
    """The connected pieces of a glTF model file, in the model's frame
    (the file's numbers are millimetres whatever its unit says). Häfele's
    files put every body into one node with a generated name, so bodies
    are told apart by where they lie, not by name."""
    key = str(path)
    if key not in _mesh_cache:
        scene: Any = trimesh.load(str(path), force="scene")
        pieces: list[Any] = []
        graph = scene.graph
        for node in graph.nodes_geometry:
            transform, geometry_name = graph[node]
            mesh = scene.geometry[geometry_name].copy()
            mesh.apply_transform(transform)
            if len(mesh.faces) < 4:
                continue
            pieces.extend(mesh.split(only_watertight=False, repair=False))
        _mesh_cache[key] = pieces
    return _mesh_cache[key]


def _body_mesh(item: HardwareLayout, body: Any, root: Path) -> Any:
    """A body's mesh: the model's pieces inside the body's envelope, or the
    envelope box when there is no model file."""
    if item["mesh"]:
        path = root / item["mesh"]
        if path.is_file():
            pieces = [p for p in _model_pieces(path) if _inside_envelope(p, body["envelope"])]
            if pieces:
                return trimesh.util.concatenate(pieces)
    lo = np.array(body["envelope"]["min"])
    hi = np.array(body["envelope"]["max"])
    box = trimesh.creation.box(extents=hi - lo)
    box.apply_translation((lo + hi) / 2)
    return box


def _inside_envelope(mesh: Any, envelope: BoxDict, tolerance: float = 1.0) -> bool:
    lo, hi = mesh.bounds
    return bool(np.all(lo >= np.array(envelope["min"]) - tolerance)
                and np.all(hi <= np.array(envelope["max"]) + tolerance))


def mesh_hardware(item: HardwareLayout, root: Path) -> list[tuple[str, Any]]:
    """Each body of a bought part in world coordinates: the model's mesh
    when `mesh` names a file under `root`, else its envelope box."""
    m = np.eye(4)
    for col, key in enumerate(("x", "y", "z")):
        m[:3, col] = _axis_vector(item["axes"][key])
    m[:3, 3] = item["origin"]
    out: list[tuple[str, Any]] = []
    for body in item["bodies"]:
        mesh = _body_mesh(item, body, root)
        mesh.apply_translation(body["offset"])
        mesh.apply_transform(m)
        mesh.metadata["path"] = f"{item['path']}.{body['name']}"
        out.append((mesh.metadata["path"], mesh))
    return out


#: Where model files named in the layout are found: the repository root.
REPO_ROOT = Path(__file__).resolve().parents[2]


def build_scene(layout: Layout, root: Path = REPO_ROOT) -> Any:
    scene = trimesh.Scene()
    for module in layout["modules"]:
        for part in module["parts"]:
            mesh = mesh_part(part, layout["frame"])
            if mesh is not None and len(mesh.faces):
                scene.add_geometry(mesh, node_name=part["path"], geom_name=part["path"])
        for item in module.get("hardware", []):
            for name, mesh in mesh_hardware(item, root):
                scene.add_geometry(mesh, node_name=name, geom_name=name)
    return scene


def write_scene(layout: Layout, path: str | Path, root: Path = REPO_ROOT) -> None:
    scene = build_scene(layout, root)
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    scene.export(str(path))
