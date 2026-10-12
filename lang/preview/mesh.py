"""Meshes a layout into a glTF scene for the browser viewer.

Each board is its outline extruded by its thickness, with pockets, holes,
V-grooves and chamfers subtracted through mesh booleans (manifold). A
chamfer along a contour (a cut's or pocket's rim, a face's outline) is a
frustum: the contour at the chamfer's depth lofted to the contour moved the
chamfer's size into the material at the face, vertex by vertex, so its
sides are flat at 45 degrees. A chamfer along the edge between two faces
is a triangular prism; a hole's is a cone (a countersink). Operations on
narrow faces are not meshed yet.
"""
from __future__ import annotations

import math
from pathlib import Path
from typing import Any

import numpy as np
import trimesh
from shapely.geometry import Polygon
from shapely.geometry import box as shapely_box
from shapely.geometry.polygon import orient
from trimesh.creation import extrude_polygon, triangulate_polygon

from ..core.layout_types import (BoxDict, ChamferLayout, HardwareLayout, HoleLayout, Layout, OpLayout, PartLayout,
                                 Rings, VGrooveLayout)
from ..emit.plan import pieces

AXES = ("x", "y", "z")
#: How far a chamfer's tool reaches past the face it starts from and past
#: its depth, so the boolean cuts cleanly, mm.
_PAST = 0.01


def _polygon(rings: Rings) -> Polygon:
    return Polygon(rings[0], holes=rings[1:]) if len(rings) > 1 else Polygon(rings[0])


def _extruded(rings: Rings, height: float) -> Any:
    """Each polygon of a layout shape extruded by `height`."""
    polygons = [_polygon(piece) for piece in pieces(rings)]
    if len(polygons) == 1:
        return extrude_polygon(polygons[0], height)
    return trimesh.util.concatenate([extrude_polygon(p, height) for p in polygons])


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


def _countersink_tool(op: HoleLayout, frame: dict[str, str], t_axis: str, t: float) -> Any:
    """A hole's chamfer, a 90 degree countersink: a cone from the hole's
    radius plus the chamfer at the face down to the hole's radius, reaching
    a little above the face and on into the hole so the boolean cuts
    cleanly. Built in the part's (u, v, t) frame; a narrow face yields an
    empty tool."""
    code = frame[op["face"]]
    if code[1] != t_axis:
        return trimesh.Trimesh()
    r, c = op["d"] / 2, op["chamfer"]
    above, into = 0.01, c + 0.05
    # (radius, depth into the part), revolved about the hole's axis
    profile = np.array([[0.0, -above], [r + c + above, -above], [r + c - into, into], [0.0, into]])
    tool = trimesh.creation.revolve(profile, sections=32)
    if code[0] == "+":
        # into the part is down from the upper face: turn the cone over
        tool.apply_transform(trimesh.transformations.rotation_matrix(math.pi, [1, 0, 0]))
        tool.apply_translation([op["u"], op["v"], t])
    else:
        tool.apply_translation([op["u"], op["v"], 0.0])
    return tool


def _offset_ring(ring: Any, d: float) -> Any | None:
    """The ring's vertices moved `d` to the right of the ring's direction
    (out of the polygon for a counter-clockwise exterior or a clockwise
    hole), each along the mitre of its two edges, so that every edge moves
    `d` and stays parallel. None at a spike, where the mitre runs away."""
    before = ring - np.roll(ring, 1, axis=0)
    after = np.roll(ring, -1, axis=0) - ring
    n1 = np.stack([before[:, 1], -before[:, 0]], axis=1) / np.linalg.norm(before, axis=1)[:, None]
    n2 = np.stack([after[:, 1], -after[:, 0]], axis=1) / np.linalg.norm(after, axis=1)[:, None]
    denominator = 1.0 + np.sum(n1 * n2, axis=1)
    if np.any(denominator < 0.05):
        return None
    return ring + d * (n1 + n2) / denominator[:, None]


def _frustum(region: Polygon, d_low: float, z_low: float, d_high: float, z_high: float) -> Any | None:
    """A solid whose section at `z_low` is `region` grown by `d_low` and at
    `z_high` grown by `d_high` (negative shrinks), the two sections joined
    vertex by vertex. None when an offset folds over itself."""
    region = orient(region, 1.0)
    rings = [np.array(r.coords[:-1], dtype=float) for r in [region.exterior, *region.interiors]]
    rings = [r[np.linalg.norm(r - np.roll(r, 1, axis=0), axis=1) > 1e-9] for r in rings]
    levels: list[list[Any]] = []
    for d in (d_low, d_high):
        moved = [_offset_ring(r, d) for r in rings]
        if any(m is None for m in moved):
            return None
        section = Polygon(moved[0], moved[1:])
        if not section.is_valid or section.area <= 0:
            return None
        levels.append(moved)
    vertices: list[Any] = []
    faces: list[list[int]] = []
    starts: list[list[int]] = []                 # per level, the first vertex of each ring
    for level, z in zip(levels, (z_low, z_high)):
        level_starts: list[int] = []
        for ring in level:
            level_starts.append(sum(len(v) for v in vertices))
            vertices.append(np.column_stack([ring, np.full(len(ring), z)]))
        starts.append(level_starts)
    # the sides: a quad per edge, facing out of the solid (to the right of a
    # ring's direction, seen from above, with z_low below z_high)
    lo, hi = (0, 1) if z_low < z_high else (1, 0)
    for k, ring in enumerate(rings):
        n = len(ring)
        for i in range(n):
            j = (i + 1) % n
            a, b = starts[lo][k] + i, starts[lo][k] + j
            c, d = starts[hi][k] + j, starts[hi][k] + i
            faces += [[a, b, c], [a, c, d]]
    # the caps: each section triangulated, its triangles turned down at the
    # bottom and up at the top
    for index, (level, z) in enumerate(zip(levels, (z_low, z_high))):
        lookup = {}
        for k, ring in enumerate(level):
            for i, point in enumerate(ring):
                lookup[(float(point[0]), float(point[1]))] = starts[index][k] + i
        points, triangles = triangulate_polygon(Polygon(level[0], level[1:]))
        up = z == max(z_low, z_high)
        for tri in triangles:
            try:
                ids = [lookup[(float(points[t][0]), float(points[t][1]))] for t in tri]
            except KeyError:
                return None
            (x0, y0), (x1, y1), (x2, y2) = (points[t] for t in tri)
            ccw = (x1 - x0) * (y2 - y0) - (y1 - y0) * (x2 - x0) > 0
            faces.append(ids if ccw == up else ids[::-1])
    mesh = trimesh.Trimesh(np.vstack(vertices), np.array(faces), process=False)
    return mesh if mesh.is_volume else None


def _face_level(face: str, frame: dict[str, str], t_axis: str, t: float) -> float | None:
    """For a big face, which way is out of the part along its thickness
    (+1 for the face at t, -1 for the one at 0); None for a narrow face."""
    code = frame[face]
    if code[1] != t_axis:
        return None
    return 1.0 if code[0] == "+" else -1.0


def _contour_chamfer(region: Polygon, size: float, out: float, t: float) -> Any | None:
    """The tool chamfering the contour of `region`, the side of the contour
    without material (an opening, or what lies outside an outline), on the
    face at the top (`out` +1) or bottom (-1) of the part: at the face the
    tool reaches `size` into the material, at depth `size` none."""
    face = t if out > 0 else 0.0
    return _frustum(region, size + _PAST, face + out * _PAST, -_PAST, face - out * (size + _PAST))


def _edge_chamfer(part: PartLayout, a: str, b: str, size: float, frame: dict[str, str]) -> Any | None:
    """The tool chamfering the edge where faces `a` and `b` meet: a prism
    along the edge, `size` into the part from either face, over the part's
    length."""
    axes = part["axes"]
    local = {axes["u"]: 0, axes["v"]: 1, axes["t"]: 2}
    box = part["box"]
    t_index = AXES.index(axes["t"])
    planes: list[tuple[int, float, float]] = []      # local axis, coordinate, outward sign
    for name in (a, b):
        code = frame[name]
        world = AXES.index(code[1])
        sign = 1.0 if code[0] == "+" else -1.0
        value = (box["max"] if sign > 0 else box["min"])[world]
        if world == t_index:
            value -= box["min"][t_index]
        planes.append((local[code[1]], value, sign))
    (ia, va, sa), (ib, vb, sb) = planes
    if ia == ib:
        return None
    along = 3 - ia - ib
    lo = {0: box["min"][AXES.index(axes["u"])], 1: box["min"][AXES.index(axes["v"])], 2: 0.0}[along] - 1
    hi = {0: box["max"][AXES.index(axes["u"])], 1: box["max"][AXES.index(axes["v"])], 2: part["thickness"]}[along] + 1
    points: list[list[float]] = []
    for da, db in ((-_PAST, -_PAST), (size + _PAST, -_PAST), (-_PAST, size + _PAST)):
        for s in (lo, hi):
            p = [0.0, 0.0, 0.0]
            p[ia] = va - sa * da
            p[ib] = vb - sb * db
            p[along] = s
            points.append(p)
    return trimesh.convex.convex_hull(np.array(points))


def _chamfer_tools(part: PartLayout, frame: dict[str, str]) -> list[Any]:
    """The tools for the part's chamfers along cuts, pockets, outlines and
    edges, and along holes named by a chamfer (a hole's own chamfer is its
    countersink)."""
    t, t_axis = part["thickness"], part["axes"]["t"]
    named: dict[str, OpLayout] = {}
    for op in part["ops"]:
        if (op["kind"] == "cut" or op["kind"] == "pocket" or op["kind"] == "hole") and op["name"]:
            named[op["name"]] = op
    jobs: list[tuple[list[Polygon], str, float]] = []     # regions without material, face, size
    tools: list[Any] = []
    for op in part["ops"]:
        if op["kind"] == "cut" and op["chamfer"] > 0:
            jobs.append((_regions(op["shape"]), part["show"], op["chamfer"]))
        elif op["kind"] == "pocket" and op["chamfer"] > 0:
            jobs.append((_regions(op["shape"]), op["face"], op["chamfer"]))
        elif op["kind"] == "chamfer":
            tools += _named_chamfer(part, op, named, jobs, frame)
    for regions, face, size in jobs:
        out = _face_level(face, frame, t_axis, t)
        if out is None:
            continue
        for region in regions:
            tool = _contour_chamfer(region, size, out, t)
            if tool is not None:
                tools.append(tool)
    return tools


def _regions(rings: Rings) -> list[Polygon]:
    return [_polygon(piece) for piece in pieces(rings)]


def _named_chamfer(part: PartLayout, op: ChamferLayout, named: dict[str, OpLayout],
                   jobs: list[tuple[list[Polygon], str, float]], frame: dict[str, str]) -> list[Any]:
    """A chamfer op: along the outline of a face, along a named cut, pocket
    or hole, or along an edge named by two faces. Contours go to `jobs`;
    the tools of edges and holes are returned."""
    what, size, face = op["what"], op["size"], op["face"]
    if what == "outline":
        # what lies around the outline, out to a frame beyond its chamfer
        outline = _polygon(pieces(part["outline"])[0])
        b = outline.bounds
        margin = 2 * size + 1
        around = shapely_box(b[0] - margin, b[1] - margin, b[2] + margin, b[3] + margin)
        jobs.append(([Polygon(around.exterior.coords, [outline.exterior.coords])], face, size))
        return []
    target = named.get(what)
    if target is not None:
        if target["kind"] == "hole":
            hole = target.copy()
            hole["face"], hole["chamfer"] = face, size
            return [_countersink_tool(hole, frame, part["axes"]["t"], part["thickness"])]
        if target["kind"] == "cut" or target["kind"] == "pocket":
            jobs.append((_regions(target["shape"]), face, size))
        return []
    names = what.split(".")
    if len(names) == 2 and all(n in frame for n in names):
        tool = _edge_chamfer(part, names[0], names[1], size, frame)
        return [tool] if tool is not None else []
    return []


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
            tool = _extruded(op["shape"], depth + 0.01)
            tools.append(_from_face(tool, op["face"], frame, t_axis, t, depth))
        elif op["kind"] == "hole":
            depth = min(op["depth"], t)
            tool = trimesh.creation.cylinder(radius=op["d"] / 2, height=depth + 0.01, sections=24)
            tool.apply_translation([op["u"], op["v"], (depth + 0.01) / 2])
            tools.append(_from_face(tool, op["face"], frame, t_axis, t, depth))
            if op["chamfer"] > 0:
                tools.append(_countersink_tool(op, frame, t_axis, t))
        elif op["kind"] == "vgroove":
            tools.append(_vgroove_tool(op, frame, t_axis, t))
    tools += _chamfer_tools(part, frame)
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
