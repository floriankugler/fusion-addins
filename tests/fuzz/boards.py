"""Random boards for the fuzz tests: a board lying or standing, its outline
a rectangle, a rounded or tapered shape or a slot, with holes, pockets,
through cuts, notches, V-grooves, holes into its narrow faces and rounded
corners, in random order; then the operation under test (a cutout); then
one more operation. A case is plain data (frozen dataclasses), so a
failing example prints as something to build again by hand.

`run_cutout` builds a case and returns what is wrong with the result, as
`cutout()` promises it (see its docstring), checked from the outside: the
openings keep `border` from the outline and `around` from everything the
board had and from `keep=`, a router of the corner radius reaches every
part of them, the bands of a cross stay, no material falls out, a failed
cutout changes nothing, an operation made later in an opening is refused
and one beside it is not; and the layout plans, draws and meshes."""
from __future__ import annotations

import math
import traceback
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

from hypothesis import strategies as st
from shapely import affinity
from shapely.geometry import LineString, Point, Polygon
from shapely.geometry import box as shapely_box
from shapely.geometry.base import BaseGeometry
from shapely.ops import unary_union

from fuzzing import floats, fresh, fit_problems, rings_of, sizes
from lang import Board, Box, LangError, Shape, board, cross, material, module, through, to, triangles
from lang.core.geometry import polygons_of
from lang.core.layout import build_layout
from lang.core.ops import Cut, Pocket
from lang.core.shapes import slot_shape
from lang.emit.plan import plan_layout
from lang.preview.mesh import mesh_part

Place = Literal["bottom", "left", "back"]
OutlineKind = Literal["rect", "rounded", "taper", "slot"]
FeatureKind = Literal["hole", "pocket", "cut", "notch", "vgroove", "edge_hole", "fillet"]


@dataclass(frozen=True)
class Feature:
    """An operation at (u, v) mm from the outline's low corner, on big face
    `face` (0 or 1, as `big_faces()` gives them): a hole `a` across, a
    pocket `a` by `b` turned by `angle` (a circle when `b` is 0), a through
    cut of that shape, a notch (a cut over the outline's edge), a V-groove
    `a` long and `b` deep, a hole `a` across into narrow face `face` (0 to
    3) `b` deep, or every corner of the outline rounded with `a`. `depth`
    is a fraction of the thickness, None for through."""
    kind: FeatureKind
    face: int
    u: float
    v: float
    a: float
    b: float = 0.0
    angle: float = 0.0
    depth: float | None = None


@dataclass(frozen=True)
class CutoutCall:
    """`cutout()`'s arguments: the face (None for the default), the pattern
    (None, ("cross", width) or ("triangles", columns, rows, spacing,
    aligned)), the depth as a fraction of the thickness (None for through;
    negative: to the other face, stopping that many mm short), and the
    regions kept, as (u0, v0, u1, v1) mm from the outline's low corner."""
    face: int | None = None
    pattern: tuple[str, float] | tuple[str, int, int, float, bool] | None = None
    border: float = 20.0
    around: float = 20.0
    radius: float = 8.0
    depth: float | None = None
    chamfer: float = 0.0
    keep: tuple[tuple[float, float, float, float], ...] = ()


@dataclass(frozen=True)
class BoardCase:
    t: float
    place: Place
    origin: tuple[float, float, float]
    size: tuple[float, float]
    outline: OutlineKind = "rect"
    outline_r: float = 0.0
    features: tuple[Feature, ...] = ()
    cutout: CutoutCall = field(default_factory=CutoutCall)
    after: Feature | None = None


# -- strategies --------------------------------------------------------------------------------

def _offset(extent: float) -> st.SearchStrategy[float]:
    """A distance from the low edge: anywhere, or near either edge, where
    borders and rings meet."""
    near = sizes(0, min(60.0, extent))
    return st.one_of(floats(0, extent), near, near.map(lambda d: extent - d))


@st.composite
def features(draw: st.DrawFn, size: tuple[float, float], t: float) -> Feature:
    kind: FeatureKind = draw(st.sampled_from(["hole", "hole", "pocket", "pocket", "cut", "notch", "vgroove",
                                              "edge_hole", "fillet"]))
    u, v = draw(_offset(size[0])), draw(_offset(size[1]))
    depth = draw(st.one_of(st.none(), floats(0.05, 0.95), st.just(0.5)))
    angle = draw(st.one_of(st.just(0.0), st.just(45.0), floats(0, 180)))
    if kind == "hole":
        return Feature(kind, draw(st.integers(0, 1)), u, v, draw(sizes(2, 40)), depth=depth)
    if kind in ("pocket", "cut", "notch"):
        a, b = draw(sizes(2, 120)), draw(st.one_of(st.just(0.0), sizes(2, 120)))
        return Feature(kind, draw(st.integers(0, 1)), u, v, a, b, angle, depth)
    if kind == "vgroove":
        return Feature(kind, draw(st.integers(0, 1)), u, v, draw(sizes(1, 200)), draw(floats(0.2, 0.45)) * t,
                       angle)
    if kind == "edge_hole":
        return Feature(kind, draw(st.integers(0, 3)), u, v, draw(sizes(2, t - 1)), draw(sizes(3, 60)))
    return Feature(kind, 0, 0, 0, draw(sizes(1, 60)))


@st.composite
def cutout_calls(draw: st.DrawFn, size: tuple[float, float], t: float) -> CutoutCall:
    pattern: tuple[str, float] | tuple[str, int, int, float, bool] | None = draw(st.one_of(
        st.none(),
        st.tuples(st.just("cross"), sizes(5, 80)),
        st.tuples(st.just("triangles"), st.integers(1, 9), st.integers(1, 7), sizes(5, 40), st.booleans())))
    depth = draw(st.one_of(st.none(), st.none(), floats(0.2, 0.9), sizes(1, t - 1).map(lambda k: -k)))
    keep = tuple(draw(st.lists(st.tuples(_offset(size[0]), _offset(size[1]), sizes(5, 300), sizes(5, 300))
                               .map(lambda k: (k[0], k[1], k[0] + k[2], k[1] + k[3])), max_size=2)))
    return CutoutCall(draw(st.one_of(st.none(), st.integers(0, 1))), pattern,
                      draw(st.one_of(st.just(20.0), sizes(0, 40))), draw(st.one_of(st.just(20.0), sizes(0, 40))),
                      draw(st.one_of(st.just(8.0), st.just(0.0), sizes(0, 15))), depth,
                      draw(st.one_of(st.just(0.0), st.just(1.0), floats(0.1, 3))), keep)


@st.composite
def board_cases(draw: st.DrawFn) -> BoardCase:
    t = draw(st.sampled_from([6.0, 9.0, 12.0, 15.0, 18.0, 24.0]))
    size = (draw(sizes(40, 2400)), draw(sizes(40, 1200)))
    far = sizes(-6000, 6000)
    origin = draw(st.one_of(st.just((0.0, 0.0, 0.0)), st.tuples(far, far, far)))
    outline: OutlineKind = draw(st.sampled_from(["rect", "rect", "rounded", "taper", "slot"]))
    outline_r = draw(floats(0.05, 0.45)) * min(size) if outline in ("rounded", "taper") else 0.0
    feats = tuple(draw(st.lists(features(size, t), max_size=7)))
    after = draw(st.one_of(st.none(), features(size, t)))
    return BoardCase(t, draw(st.sampled_from(["bottom", "left", "back"])), origin, size, outline, outline_r,
                     feats, draw(cutout_calls(size, t)), after)


# -- building ------------------------------------------------------------------------------------

def _module_box(case: BoardCase) -> Box:
    """A box the board fills: its outline's size on the board's plane."""
    u, v = case.size
    if case.place == "bottom":            # x (depth) by y (width)
        return Box.from_size(width=v, depth=u, height=100, origin=case.origin)
    if case.place == "left":              # x (depth) by z (height)
        return Box.from_size(width=100, depth=u, height=v, origin=case.origin)
    return Box.from_size(width=u, depth=100, height=v, origin=case.origin)     # y (width) by z (height)


def _outline_shape(case: BoardCase) -> Shape | None:
    u, v = case.size
    if case.outline == "rect":
        return None
    if case.outline == "rounded":
        return Shape(shapely_box(0, 0, u, v)).rounded(case.outline_r)
    if case.outline == "taper":
        return Shape(Polygon([(0, 0), (u, 0), (u, case.outline_r), (0, v)]))
    if u < v:
        return slot_shape((u / 2, u / 2), (u / 2, v - u / 2), u, 32)
    return slot_shape((v / 2, v / 2), (u - v / 2, v / 2), v, 32)


def _shape_at(f: Feature, p: tuple[float, float]) -> BaseGeometry:
    if f.b <= 0:
        return Point(p).buffer(f.a / 2, quad_segs=32)
    g = shapely_box(p[0] - f.a / 2, p[1] - f.b / 2, p[0] + f.a / 2, p[1] + f.b / 2)
    return affinity.rotate(g, f.angle, origin=p) if f.angle else g


def _depth(b: Board, fraction: float | None) -> float | object:
    return through if fraction is None else max(0.1, fraction * b.thickness)


def apply(b: Board, f: Feature, name: str) -> BaseGeometry | None:
    """Makes the feature on the board; its footprint in the outline's frame
    (None for a fillet)."""
    u0, v0, _, _ = b.outline.bounds
    p = (u0 + f.u, v0 + f.v)
    faces = b.big_faces()
    if f.kind == "hole":
        b.add_hole(faces[f.face], p, f.a, _depth(b, f.depth), name)  # pyright: ignore[reportArgumentType]
        return Point(p).buffer(f.a / 2, quad_segs=64)
    if f.kind == "pocket":
        g = _shape_at(f, p)
        b.add_pocket(faces[f.face], Shape(g), _depth(b, f.depth), name)  # pyright: ignore[reportArgumentType]
        return g
    if f.kind in ("cut", "notch"):
        g = _shape_at(f, p)
        b.add_cut(Shape(g), name)
        return g
    if f.kind == "vgroove":
        end = (p[0] + f.a * math.cos(math.radians(f.angle)), p[1] + f.a * math.sin(math.radians(f.angle)))
        b.add_vgroove(faces[f.face], p, end, f.b, name)
        return LineString([p, end]).buffer(f.b, cap_style="flat")
    if f.kind == "edge_hole":
        return _edge_hole(b, f, name)
    b.fillet(faces[0].outline, f.a)
    return None


def _edge_hole(b: Board, f: Feature, name: str) -> BaseGeometry:
    frame = b.scope.frame
    narrow = [frame.direction_of(a, s) for a in (b.u_axis, b.v_axis) for s in (-1, 1)][f.face]
    other = b.v_axis if narrow.axis == b.u_axis else b.u_axis
    low = frame.direction_of(other, -1)
    face = b.face(narrow)
    box = b.box()
    along = f.v if other == b.v_axis else f.u
    along = min(max(along, f.a / 2 + 0.1), box.hi[other] - box.lo[other] - f.a / 2 - 0.1)
    edge = getattr(face, low.name)
    b.hole(f.a, at=edge(along), depth=f.b, name=name)
    start = box.hi[narrow.axis] if narrow.sign > 0 else box.lo[narrow.axis]
    reach = (start - f.b, start) if narrow.sign > 0 else (start, start + f.b)
    across = (box.lo[other] + along - f.a / 2, box.lo[other] + along + f.a / 2)
    if narrow.axis == b.u_axis:
        return shapely_box(reach[0], across[0], reach[1], across[1])
    return shapely_box(across[0], reach[0], across[1], reach[1])


def _state(b: Board) -> tuple[str, list[object], int]:
    return (b.outline.geometry.wkt, list(b.ops), len(b.notes))


# -- the cutout's promises -------------------------------------------------------------------------

#: How much nearer than `border` or `around` an opening may come (mm): the
#: offsets put arcs onto their true circles, a few hundredths off, and the
#: shapes' own polygons lie inside their arcs by their chords' sagitta.
NEAR = 0.05


def slack_of(case: BoardCase) -> float:
    """`NEAR` and the sagitta of the case's coarsest arc: circles of 32
    segments a quarter (2.8 degrees a step) as large as its largest arc."""
    radii = [min(case.size) / 2 if case.outline == "slot" else case.outline_r]
    radii += [f.a / 2 for f in case.features if f.kind in ("hole", "pocket", "cut", "notch")]
    return NEAR + max(radii) * (1 - math.cos(math.pi / 128))


def run_cutout(case: BoardCase) -> list[str]:
    """What is wrong with the cutout on the case's board; [] when the
    cutout was refused with a LangError that changed nothing."""
    problems: list[str] = []
    with fresh():
        try:
            problems = _run_cutout(case)
        except LangError:
            return []          # a refusal outside the operation under test (placing the board)
        except Exception as e:
            frame = next((fr for fr in reversed(traceback.extract_tb(e.__traceback__))
                          if "/lang/" in fr.filename), traceback.extract_tb(e.__traceback__)[-1])
            return [f"{type(e).__name__} at {Path(frame.filename).name}:{frame.lineno}: {e}"]
    return problems


def _run_cutout(case: BoardCase, name: str = "m", pipeline: bool = True) -> list[str]:
    """`run_cutout` in the current build, the board in a module `name`;
    with `pipeline`, the layout is planned, drawn and meshed too (a batch
    of cases built into one layout for Fusion leaves that to the end)."""
    problems: list[str] = []
    with module(name, _module_box(case)) as m:
        b = board("panel", material("birch", t=case.t), _outline_shape(case)).on(getattr(m, case.place))
        footprints: list[tuple[str, BaseGeometry]] = []
        for i, f in enumerate(case.features):
            name = f"{f.kind}_{i}"
            before = _state(b)
            try:
                g = apply(b, f, name)
            except LangError:
                if _state(b) != before:
                    problems.append(f"a refused {f.kind} changed the board")
                continue
            if g is not None and f.kind in ("hole", "pocket", "vgroove") and g.intersection(b.outline.geometry).area <= 1e-6:
                problems.append(f"a {f.kind} wholly off the board was accepted")
            if g is not None and f.kind not in ("cut", "notch"):
                footprints.append((name, g))
        outline = b.outline.geometry
        exterior = unary_union([Polygon(p.exterior) for p in polygons_of(outline)])
        footprints += [("a hole of the outline", Polygon(h)) for p in polygons_of(outline) for h in p.interiors]
        c = case.cutout
        u0, v0, _, _ = b.outline.bounds
        keep_boxes = [_world_box(b, (u0 + k[0], v0 + k[1], u0 + k[2], v0 + k[3])) for k in c.keep]
        pattern = None if c.pattern is None else cross(float(c.pattern[1])) if c.pattern[0] == "cross" \
            else triangles(int(c.pattern[1]), int(c.pattern[2]), float(c.pattern[3]),  # pyright: ignore[reportGeneralTypeIssues]
                           aligned=bool(c.pattern[4]))  # pyright: ignore[reportGeneralTypeIssues]
        faces = b.big_faces()
        face = None if c.face is None else faces[c.face]
        cut_face = face or next(f for f in faces if f.direction != b.show_face.direction)
        other = next(f for f in faces if f.direction != cut_face.direction)
        depth = through if c.depth is None else to(other, c.depth) if c.depth < 0 else c.depth * case.t
        before = _state(b)
        try:
            b.cutout(face, pattern=pattern, border=c.border, around=c.around, radius=c.radius, depth=depth,
                     chamfer=c.chamfer, keep=keep_boxes, name="cutout")
        except LangError:
            if _state(b) != before:
                problems.append("a refused cutout changed the board")
            return problems
        made = b.op("cutout").op
        assert isinstance(made, (Cut, Pocket))
        opening = made.shape.geometry
        problems += _cutout_problems(b, case, opening, exterior, footprints, keep_boxes, isinstance(made, Cut))
        if case.after is not None:
            problems += _after_problems(b, case.after, opening)
    if pipeline:
        problems += _pipeline_problems()
    return problems


def _world_box(b: Board, r: tuple[float, float, float, float]) -> Box:
    box = b.box()
    lo = dict(box.lo)
    hi = dict(box.hi)
    lo[b.u_axis], lo[b.v_axis], hi[b.u_axis], hi[b.v_axis] = r
    return Box(lo, hi)


def _cutout_problems(b: Board, case: BoardCase, opening: BaseGeometry, exterior: BaseGeometry,
                     footprints: list[tuple[str, BaseGeometry]], keep: list[Box], thru: bool) -> list[str]:
    c = case.cutout
    slack = slack_of(case)
    problems: list[str] = []
    outline = b.outline.geometry
    if not outline.is_valid:
        problems.append("the outline is not valid after the cutout")
    if not opening.is_valid:
        problems.append("the opening is not valid")
    if thru and len(polygons_of(outline)) != len(polygons_of(exterior)):
        problems.append("material fell out: the outline has more pieces than before")
    if c.radius <= c.border:
        near = opening.distance(exterior.boundary)
        # (an opening's arcs are the true ones, the outline's polygon lies
        # inside its arcs: with no border the two differ by so much area)
        if opening.difference(exterior).area > slack * exterior.length or near < c.border - slack:
            problems.append(f"the opening comes {near:.3g} near the outline (border {c.border:g})")
    kept = footprints + [("a box kept", shapely_box(k.lo[b.u_axis], k.lo[b.v_axis], k.hi[b.u_axis], k.hi[b.v_axis]))
                         for k in keep]
    if c.radius <= c.around:
        for label, g in kept:
            near = opening.distance(g)
            if near < c.around - slack:
                problems.append(f"the opening comes {near:.3g} near {label} (around {c.around:g})")
    if c.radius > 0:
        for piece in polygons_of(opening):
            # (0.99 r: where `filleted` gives up, `fillet` rounds with 16
            # segments a quarter, a little inside the true circle)
            reached = piece.buffer(-c.radius * 0.99, quad_segs=64).buffer(c.radius * 0.99, quad_segs=64)
            # A corner left sharp leaves a spot of r^2 (tan(a/2) - a/2) for a
            # turn a, 0.21 r^2 for 90 degrees; polygon noise leaves slivers.
            # (the bound `cutouts._cut_by` uses)
            # (slivers thinner than a thousandth of r: the offsets drift along
            # a long edge)
            spots = [g.area for g in polygons_of(piece.difference(reached)) if not g.buffer(-1e-3 * c.radius).is_empty]
            if spots and max(spots) > 0.01 * c.radius ** 2 + 1e-3:
                problems.append(f"a router of radius {c.radius:g} leaves {max(spots):.3g} mm2 of an opening")
            if piece.buffer(-0.99 * c.radius).is_empty:
                problems.append(f"an opening piece is too small for radius {c.radius:g}")
    if c.pattern is not None and c.pattern[0] == "cross":
        problems += _cross_problems(b, c, opening, exterior)
    return problems


def _cross_problems(b: Board, c: CutoutCall, opening: BaseGeometry, exterior: BaseGeometry) -> list[str]:
    """The two bands along the diagonals of the inset's bounds stay."""
    inset = exterior.buffer(-c.border, join_style="mitre", mitre_limit=100.0)
    if inset.is_empty:
        return []
    u0, v0, u1, v1 = inset.bounds
    width = float(c.pattern[1]) if c.pattern is not None else 0.0
    problems: list[str] = []
    # (the corners where kept material meets a band are rounded too, which
    # takes up to about the radius off the band there)
    for a, z in (((u0, v0), (u1, v1)), ((u1, v0), (u0, v1))):
        if width / 2 <= c.radius + 2 * NEAR:
            continue
        band = LineString([a, z]).buffer(width / 2 - c.radius - 2 * NEAR, cap_style="flat")
        if opening.intersection(band).area > 1e-6:
            problems.append(f"the cross's band from {a} is cut into ({opening.intersection(band).area:.3g} mm2)")
    return problems


def _after_problems(b: Board, f: Feature, opening: BaseGeometry) -> list[str]:
    """An operation after the cutout is refused when it lies in the
    opening, and not for that reason when it does not."""
    before = _state(b)
    try:
        g = apply(b, f, "after")
    except LangError as e:
        if _state(b) != before:
            return [f"a refused {f.kind} after the cutout changed the board"]
        if "lies in the cutout" in str(e):
            fp = _footprint_of(b, f)
            if fp is not None and fp.intersection(opening).area <= 1e-6:
                return [f"a {f.kind} beside the opening was refused as lying in it"]
        return []
    if g is not None and f.kind not in ("cut", "notch", "fillet") and g.intersection(opening).area > 1e-3:
        return [f"a {f.kind} made after the cutout lies in its opening ({g.intersection(opening).area:.3g} mm2)"]
    return []


def _footprint_of(b: Board, f: Feature) -> BaseGeometry | None:
    u0, v0, _, _ = b.outline.bounds
    p = (u0 + f.u, v0 + f.v)
    if f.kind == "hole":
        return Point(p).buffer(f.a / 2, quad_segs=64)
    if f.kind in ("pocket", "cut", "notch"):
        return _shape_at(f, p)
    return None


def _pipeline_problems() -> list[str]:
    """The layout plans without problems, its loops join up and do not
    cross themselves, and every part meshes watertight."""
    problems: list[str] = []
    layout = build_layout()
    plan = plan_layout(layout)
    problems += [p for p in plan.problems if "left out" not in p]
    for module_layout in layout["modules"]:
        for part in module_layout["parts"]:
            shapes = [part["outline"]] + [op["shape"] for op in part["ops"] if op["kind"] == "cut" or op["kind"] == "pocket"]
            for rings in shapes:
                for ring in rings:
                    problems += [f"loop: {p}" for p in fit_problems([(q[0], q[1]) for q in ring], None)]
            reported: list[str] = []
            mesh = mesh_part(part, layout["frame"], reported.append)
            meshing = [f"mesh: {r}" for r in reported]
            if mesh is not None and not mesh.is_watertight:
                meshing.append("mesh: the part's mesh is not watertight")
            if meshing and _touching(part["outline"]):
                meshing = [f"{KNOWN} rings of the outline touch at a point; {meshing[0]}"]
            problems += meshing
    return problems


#: The start of a problem that is known and open (2026-10-12): rings of an
#: outline touching at a point (a cut circle touching the edge, a cutout
#: with no border), which the preview cannot mesh. Whether the language
#: should refuse such geometry is Florian's to decide.
KNOWN = "known:"


def _touching(rings: list[list[list[float]]]) -> bool:
    """Whether two rings of the outline touch, or one passes a point twice."""
    from shapely.geometry import LinearRing
    from fuzzing import degenerate
    lines = [LinearRing(r) for r in rings if len(r) >= 3]
    return any(degenerate([(p[0], p[1]) for p in r]) for r in rings) or any(
        lines[i].distance(lines[j]) < 1e-6 for i in range(len(lines)) for j in range(i + 1, len(lines)))


__all__ = ["BoardCase", "CutoutCall", "Feature", "board_cases", "run_cutout", "rings_of"]
