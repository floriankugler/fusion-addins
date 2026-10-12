"""Meshes a layout into a glTF scene for the browser viewer.

Each board is its outline extruded by its thickness, with pockets, holes,
V-grooves and chamfers subtracted through mesh booleans (manifold). A
chamfer along a contour (a cut's or pocket's rim, a face's outline) is a
frustum: the contour at the chamfer's depth lofted to the contour moved the
chamfer's size into the material at the face, vertex by vertex, so its
sides are flat at 45 degrees. A chamfer along the edge between two faces
is a triangular prism; a hole's is a cone (a countersink). Pockets and
holes in narrow faces are prisms and cylinders along the face's axis,
from the plane they start at (`offset` in front of the face), with their
chamfers. Hardware is the union of its boxes.

The layout is read as the emitter's plan reads it (`lang.emit.plan`:
`LayoutFrame`, `PartFrame`, `named_ops`, `chamfer_target`), so the preview
shows the faces, depths and chamfers Fusion gets. A boolean that fails
leaves the board uncut and is reported, not hidden.
"""
from __future__ import annotations

import math
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any

import numpy as np
import shapely
import trimesh
from shapely.geometry import Polygon
from shapely.geometry import box as shapely_box
from shapely.geometry.polygon import orient
from trimesh.creation import extrude_polygon, triangulate_polygon

from ..core.geometry import polygons_of
from ..core.layout_types import (BoxDict, ChamferLayout, EdgeOpLayout, HardwareLayout, Layout, OpLayout, PartLayout,
                                 Rings, VGrooveLayout)
from ..emit.plan import (EdgeTarget, LayoutFrame, OpTarget, OutlineTarget, PartFrame, chamfer_target, check_version,
                         named_ops, pieces)

AXES = ("x", "y", "z")
#: How far a tool reaches past the face it starts from, and past the far
#: face when it goes through, so the boolean cuts cleanly and leaves no
#: skin, mm. (It stops at its depth otherwise: once it reached half of
#: this past, 5 um, which on a large pocket made the preview a few cm3
#: lighter than Fusion's part.)
_PAST = 0.01
#: How far a countersink's cone reaches into its hole beyond the chamfer,
#: so it meets the hole's cylinder inside the material, mm.
_INTO_HOLE = 0.05
#: Sides of a hole's cylinder and of a countersink's cone.
_HOLE_SECTIONS = 24
_CONE_SECTIONS = 32
#: Something that takes a problem the preview ran into.
Report = Callable[[str], None]


#: Vertices closer than this (mm) are one: the emitter leaves out lines this
#: short, and the triangulation would make faces without area of them.
_SAME_POINT = 1e-6


def _polygon(rings: Rings) -> Polygon:
    poly = Polygon(rings[0], holes=rings[1:]) if len(rings) > 1 else Polygon(rings[0])
    out = shapely.remove_repeated_points(poly, _SAME_POINT)
    return out if out.is_valid and not out.is_empty else poly


def _extruded(rings: Rings, height: float) -> Any:
    """Each polygon of a layout shape extruded by `height`."""
    meshes = [_extruded_polygon(_polygon(piece), height) for piece in pieces(rings)]
    return meshes[0] if len(meshes) == 1 else trimesh.util.concatenate(meshes)


def _extruded_polygon(poly: Polygon, height: float) -> Any:
    """A polygon extruded by `height`. Where its ring touches itself, within
    `_SAME_POINT`, the triangulation leaves an open edge there [found by
    fuzzing: a cutout's opening pinched at a point, 1e-14 across]: then it is
    extruded inset by `_SAME_POINT`, which opens the pinch."""
    mesh = extrude_polygon(poly, height)
    if mesh.is_volume:
        return mesh
    inset = polygons_of(poly.buffer(-_SAME_POINT, join_style="mitre", mitre_limit=10.0))
    meshes = [extrude_polygon(p, height) for p in inset]
    if not meshes or not all(m.is_volume for m in meshes):
        return mesh
    return meshes[0] if len(meshes) == 1 else trimesh.util.concatenate(meshes)


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


def _big_face(pf: PartFrame, face: str) -> float | None:
    """For a big face, which way is out of the part along its thickness
    (+1 for the face at t, -1 for the one at 0); None for a narrow face."""
    ref = pf.face(face)
    return float(ref.sign) if pf.is_big(ref) else None


def _reach(depth: float, through: float) -> float:
    """How high a tool `depth` into a part `through` deep is built: from
    `_PAST` in front of its face, and `_PAST` past the far one when it goes
    through."""
    return depth + _PAST + (_PAST if depth >= through else 0.0)


def _from_face(tool: Any, out: float, t: float, depth: float) -> Any:
    """Moves a tool built upward from z=0, `_reach(depth, t)` high, so that
    it starts a little outside the big face on the side `out` and goes
    `depth` into the part."""
    beyond = _PAST if depth >= t else 0.0
    tool.apply_translation([0, 0, t - depth - beyond if out > 0 else -_PAST])
    return tool


def _cylinder(d: float, height: float) -> Any:
    """A hole's cylinder standing on z=0, `height` high."""
    tool = trimesh.creation.cylinder(radius=d / 2, height=height, sections=_HOLE_SECTIONS)
    tool.apply_translation([0.0, 0.0, height / 2])
    return tool


def _countersink(d: float, c: float) -> Any:
    """A hole's chamfer, a 90 degree countersink, for a hole of diameter
    `d` going up from z=0 at the origin: a cone from the hole's radius plus
    `c` at z=0 to the hole's radius at z=c, reaching a little below z=0 and
    on into the hole so the boolean cuts cleanly."""
    r = d / 2
    into = c + _INTO_HOLE
    # (radius, depth into the part), revolved about the hole's axis
    profile = np.array([[0.0, -_PAST], [r + c + _PAST, -_PAST], [r + c - into, into], [0.0, into]])
    return trimesh.creation.revolve(profile, sections=_CONE_SECTIONS)


def _big_countersink(u: float, v: float, d: float, c: float, out: float, t: float) -> Any:
    """A countersink on a big face (`out` +1 the face at t, -1 the one at
    0), in the part's (u, v, t) frame."""
    tool = _countersink(d, c)
    if out > 0:
        # into the part is down from the upper face: turn the cone over
        tool.apply_transform(trimesh.transformations.rotation_matrix(math.pi, [1, 0, 0]))
        tool.apply_translation([u, v, t])
    else:
        tool.apply_translation([u, v, 0.0])
    return tool


def _edge_transform(pf: PartFrame, op: EdgeOpLayout) -> Any:
    """4x4 from a narrow-face operation's own frame to the part's (u, v, t)
    frame. Its own frame: x along the face (s) and y across the thickness
    (t), both measured from the operation's (s, t), and z into the part
    from the plane the operation starts at (its face, `offset` in front)."""
    face = pf.edge_face(op)
    s_axis, _ = pf.in_face(face)
    local = {pf.u_axis: 0, pf.v_axis: 1}
    m = np.zeros((4, 4))
    m[3, 3] = 1.0
    m[local[s_axis], 0] = 1.0
    m[local[s_axis], 3] = op["s"]
    m[2, 1] = 1.0
    m[2, 3] = op["t"] - pf.lo[pf.t_axis]
    m[local[face.axis], 2] = -face.sign
    m[local[face.axis], 3] = face.value
    return m


def _edge_tools(pf: PartFrame, op: EdgeOpLayout) -> list[Any]:
    """A pocket or hole in a narrow face and its chamfer, in the part's
    (u, v, t) frame: its shape (or circle) in the face's (s, t) frame,
    extruded along the face's axis from a little in front of where it
    starts to its depth, through to the far face when it goes through."""
    face = pf.edge_face(op)
    inner = op["op"]
    depth = pf.depth(face, inner["depth"], inner["kind"] == "hole" and inner["through"])
    extent = pf.extent(face)
    height = _reach(extent if depth is None else depth, extent)
    if inner["kind"] == "pocket":
        tool = _extruded(inner["shape"], height)
    else:
        tool = _cylinder(inner["d"], height)
    tool.apply_translation([0.0, 0.0, -_PAST])
    tools = [tool]
    if inner["chamfer"] > 0:
        tools += _edge_chamfers(op, inner["chamfer"])
    m = _edge_transform(pf, op)
    for tool in tools:
        tool.apply_transform(m)
    return tools


def _edge_chamfers(op: EdgeOpLayout, size: float) -> list[Any]:
    """The chamfer of a narrow-face operation's rim, in its own frame (see
    `_edge_transform`): a frustum along a pocket's contour, a countersink
    on a hole."""
    inner = op["op"]
    if inner["kind"] == "hole":
        return [_countersink(inner["d"], size)]
    tools = [tool for region in _regions(inner["shape"]) for tool in _contour_chamfer(region, size, -1.0, 0.0)]
    return [tool for tool in tools if tool is not None]


def _vgroove_tool(op: VGrooveLayout, out: float, t: float) -> Any:
    """The groove as a prism in the part's (u, v, t) frame, on the big face
    on the side `out`, its opening a little above the face so the boolean
    cuts cleanly."""
    face = t if out > 0 else 0.0
    (u0, v0), (u1, v1) = op["start"], op["end"]
    length = math.hypot(u1 - u0, v1 - v0)
    wu, wv = -(v1 - v0) / length, (u1 - u0) / length       # across the groove, in the face
    half = op["depth"] + _PAST                               # 90 degrees: as wide on each side as deep
    points: list[tuple[float, float, float]] = []
    for u, v in ((u0, v0), (u1, v1)):
        points += [(u + wu * half, v + wv * half, face + out * _PAST),
                   (u - wu * half, v - wv * half, face + out * _PAST),
                   (u, v, face - out * op["depth"])]
    return trimesh.convex.convex_hull(np.array(points))


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


#: Slabs a chamfer is cut in where its frustum would fold over itself.
_CHAMFER_SLABS = 6


def _contour_chamfer(region: Polygon, size: float, out: float, t: float) -> list[Any]:
    """The tools chamfering the contour of `region`, the side of the contour
    without material (an opening, or what lies outside an outline), on the
    face at the top (`out` +1) or bottom (-1) of the part: at the face the
    tool reaches `size` into the material, at depth `size` none. One
    frustum; where moving the contour's vertices folds it over itself
    (short edges at an inside corner), `_CHAMFER_SLABS` slabs, each the
    region grown as at its middle depth, which take as much material."""
    face = t if out > 0 else 0.0
    tool = _frustum(region, size + _PAST, face + out * _PAST, -_PAST, face - out * (size + _PAST))
    if tool is not None:
        return [tool]
    slabs: list[Any] = []
    for k in range(_CHAMFER_SLABS):
        top, bottom = size * k / _CHAMFER_SLABS, size * (k + 1) / _CHAMFER_SLABS
        section = region.buffer(size - (top + bottom) / 2, join_style="mitre", mitre_limit=10.0)
        if k == 0:
            top = -_PAST
        for piece in polygons_of(section):
            slab = extrude_polygon(piece, bottom - top)
            if not slab.is_volume:
                # rings touching at a point, which the triangulation cannot
                # close: grown a ten-thousandth, they part
                slab = extrude_polygon(polygons_of(piece.buffer(1e-4, join_style="mitre"))[0], bottom - top)
            slab.apply_translation([0.0, 0.0, face - bottom if out > 0 else face + top])
            if slab.is_volume:
                slabs.append(slab)
    return slabs


def _edge_chamfer(pf: PartFrame, a: str, b: str, size: float) -> Any | None:
    """The tool chamfering the edge where faces `a` and `b` meet: a prism
    along the edge, `size` into the part from either face, over the part's
    length."""
    local = {pf.u_axis: 0, pf.v_axis: 1, pf.t_axis: 2}
    t0 = pf.lo[pf.t_axis]
    planes: list[tuple[int, float, float]] = []      # local axis, coordinate, outward sign
    for name in (a, b):
        face = pf.face(name)
        planes.append((local[face.axis], face.value - (t0 if face.axis == pf.t_axis else 0.0), float(face.sign)))
    (ia, va, sa), (ib, vb, sb) = planes
    if ia == ib:
        return None
    along = 3 - ia - ib
    lo = {0: pf.lo[pf.u_axis], 1: pf.lo[pf.v_axis], 2: 0.0}[along] - 1
    hi = {0: pf.hi[pf.u_axis], 1: pf.hi[pf.v_axis], 2: pf.thickness}[along] + 1
    points: list[list[float]] = []
    for da, db in ((-_PAST, -_PAST), (size + _PAST, -_PAST), (-_PAST, size + _PAST)):
        for s in (lo, hi):
            p = [0.0, 0.0, 0.0]
            p[ia] = va - sa * da
            p[ib] = vb - sb * db
            p[along] = s
            points.append(p)
    return trimesh.convex.convex_hull(np.array(points))


def _chamfer_tools(part: PartLayout, pf: PartFrame) -> list[Any]:
    """The tools for the part's chamfers along cuts, pockets, outlines and
    edges, and along the operations a chamfer names (a hole's own chamfer
    is its countersink, a narrow-face operation's goes with it)."""
    t = part["thickness"]
    named = named_ops(part)
    jobs: list[tuple[list[Polygon], str, float]] = []     # regions without material, face, size
    tools: list[Any] = []
    for op in part["ops"]:
        if op["kind"] == "cut" and op["chamfer"] > 0:
            jobs.append((_regions(op["shape"]), part["show"], op["chamfer"]))
        elif op["kind"] == "pocket" and op["chamfer"] > 0:
            jobs.append((_regions(op["shape"]), op["face"], op["chamfer"]))
        elif op["kind"] == "chamfer":
            tools += _named_chamfer(part, pf, op, named, jobs)
    for regions, face, size in jobs:
        out = _big_face(pf, face)
        if out is None:
            continue
        for region in regions:
            tools += _contour_chamfer(region, size, out, t)
    return tools


def _regions(rings: Rings) -> list[Polygon]:
    return [_polygon(piece) for piece in pieces(rings)]


def _named_chamfer(part: PartLayout, pf: PartFrame, op: ChamferLayout, named: dict[str, OpLayout],
                   jobs: list[tuple[list[Polygon], str, float]]) -> list[Any]:
    """A chamfer op: along the outline of a face, along a named operation,
    or along an edge named by two faces (`plan.chamfer_target`). Contours
    on big faces go to `jobs`; the other tools are returned."""
    size, face = op["size"], op["face"]
    target = chamfer_target(op, named, pf.frame)
    if isinstance(target, OutlineTarget):
        # what lies around the outline, out to a frame beyond its chamfer
        outline = _polygon(pieces(part["outline"])[0])
        b = outline.bounds
        margin = 2 * size + 1
        around = shapely_box(b[0] - margin, b[1] - margin, b[2] + margin, b[3] + margin)
        jobs.append(([Polygon(around.exterior.coords, [outline.exterior.coords])], face, size))
        return []
    if isinstance(target, EdgeTarget):
        tool = _edge_chamfer(pf, target.a, target.b, size)
        return [tool] if tool is not None else []
    if not isinstance(target, OpTarget):
        return []
    named_op = target.op
    if named_op["kind"] == "hole":
        out = _big_face(pf, named_op["face"])
        return [] if out is None else [
            _big_countersink(named_op["u"], named_op["v"], named_op["d"], size, out, part["thickness"])]
    if named_op["kind"] == "edge":
        tools = _edge_chamfers(named_op, size)
        m = _edge_transform(pf, named_op)
        for tool in tools:
            tool.apply_transform(m)
        return tools
    if named_op["kind"] == "cut" or named_op["kind"] == "pocket":
        jobs.append((_regions(named_op["shape"]), face, size))
    return []


def mesh_part(part: PartLayout, frame: dict[str, str], report: Report | None = None) -> Any:
    """The part as a mesh in world coordinates, its operations cut. When
    the boolean fails the board is left uncut and `report` (or stderr) is
    told so."""
    t = part["thickness"]
    outline = _polygon(part["outline"])
    if outline.is_empty:
        return None
    pf = PartFrame(part, LayoutFrame(frame))
    mesh = extrude_polygon(outline, t)
    tools: list[Any] = []
    for op in part["ops"]:
        if op["kind"] == "pocket" or op["kind"] == "hole":
            out = _big_face(pf, op["face"])
            if out is None:
                continue
            depth = min(op["depth"], t)
            if op["kind"] == "pocket":
                tools.append(_from_face(_extruded(op["shape"], _reach(depth, t)), out, t, depth))
            else:
                tool = _cylinder(op["d"], _reach(depth, t))
                tool.apply_translation([op["u"], op["v"], 0.0])
                tools.append(_from_face(tool, out, t, depth))
                if op["chamfer"] > 0:
                    tools.append(_big_countersink(op["u"], op["v"], op["d"], op["chamfer"], out, t))
        elif op["kind"] == "vgroove":
            out = _big_face(pf, op["face"])
            if out is not None:
                tools.append(_vgroove_tool(op, out, t))
        elif op["kind"] == "edge":
            tools += _edge_tools(pf, op)
    tools += _chamfer_tools(part, pf)
    tools = [tool for tool in tools if len(tool.faces)]
    if tools:
        try:
            mesh = trimesh.boolean.difference([mesh] + tools, engine="manifold")
        except Exception as error:
            _report(report, f"{part['path']}: the preview could not cut its operations ({error}); "
                            "it shows the board uncut.")
    mesh.apply_transform(_part_transform(part))
    mesh.metadata["path"] = part["path"]
    return mesh


def mesh_hardware(item: HardwareLayout, report: Report | None = None) -> list[tuple[str, Any]]:
    """Each body of a bought part in world coordinates: the union of its
    boxes, or the boxes side by side when the union fails (reported)."""
    out: list[tuple[str, Any]] = []
    for body in item["bodies"]:
        path = f"{item['path']}.{body['name']}"
        boxes = [_box_mesh(box) for box in body["boxes"]]
        try:
            mesh = boxes[0] if len(boxes) == 1 else trimesh.boolean.union(boxes, engine="manifold")
        except Exception as error:
            _report(report, f"{path}: the preview could not unite its boxes ({error}); it shows them apart.")
            mesh = trimesh.util.concatenate(boxes)
        mesh.metadata["path"] = path
        out.append((path, mesh))
    return out


def _report(report: Report | None, message: str) -> None:
    if report is not None:
        report(message)
    else:
        print(f"preview: {message}", file=sys.stderr)


def _box_mesh(box: BoxDict) -> Any:
    lo, hi = np.array(box["min"]), np.array(box["max"])
    mesh = trimesh.creation.box(extents=hi - lo)
    mesh.apply_translation((lo + hi) / 2)
    return mesh


def build_scene(layout: Layout, report: Report | None = None) -> Any:
    """Every part and hardware body of the layout as one scene; a ValueError
    for a layout of another version."""
    check_version(layout)
    scene = trimesh.Scene()
    for module in layout["modules"]:
        for part in module["parts"]:
            mesh = mesh_part(part, layout["frame"], report)
            if mesh is not None and len(mesh.faces):
                scene.add_geometry(mesh, node_name=part["path"], geom_name=part["path"])
        for item in module["hardware"]:
            for name, mesh in mesh_hardware(item, report):
                scene.add_geometry(mesh, node_name=name, geom_name=name)
    return scene


def write_scene(layout: Layout, path: str | Path) -> list[str]:
    """Writes the scene as glTF; returns the problems meshing it ran into."""
    problems: list[str] = []
    scene = build_scene(layout, problems.append)
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    scene.export(str(path))
    return problems
