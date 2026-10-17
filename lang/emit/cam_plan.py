"""A CAM plan (`lang.cam`, `cam.json`) as the CAM emitter builds it in the
nested document (`nested`): Fusion-free and unit tested, like `nested`;
`cam.emit_cam` builds it.

The plan gives every feature in its setup's frame, its blank's: x along
the blank's length, y across, from its corner, Z zero at the stock's top
(`lang.cam.plan_types`). The nested document lays the blank at its place
on its sheet and the sheets one above the other along y (`nested`), its
underside at z = 0, so a point of the plan is the blank's corner in the
document plus the point, at the height of the stock's top (the nominal
thickness) less its depth. This module maps every setup so, refuses a plan
that is not the nest's beside it, and says per feature what the emitter
binds it by:

- an outer contour: the part's silhouette, its outside loop (`Silhouette`);
- an inner contour, and a ring of a pocket taken out through: a loop of
  the part's edges along the ring, at the stock's top or at the blank's
  underside, whichever follows all of it (`FaceLoop`);
- a pocket: its floor's faces, the upward faces at its depth inside its
  region (`Floor`);
- a rest: its region drawn in the setup's sketch at the pocket's floor
  (`Region`), as no face of the part is where the wider cutter did not
  reach;
- a hole, and a dog bone plunged with a drill: the cylinders about its
  centre (`Cylinder`);
- a dog bone milled along its wall: its wall's arc edges (`WallArc`);
- a chamfer: the chamfer's lower edges, the edge before the chamfer moved
  down by its size (`EdgePath`), as Fusion's 2D Chamfer takes them;
- a V-groove: its bottom edge, which a Trace's tip follows (`EdgeLine`).

What the emitter writes on each operation is `param_writes` (the heights
as Fusion's mode and an offset in mm, Fusion's mode names being the plan's,
the depths, the order, the tabs); the edge tests it binds by are here too
(`edge_on_path`, `runs`), so `cam.py` only asks Fusion.
"""
from __future__ import annotations

import math
import os
from dataclasses import dataclass, field
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from .arcs import Arc2, Circle2, Line2, fit
from .nested import check_nest_version, sheet_places
from .plan import Arc, Circle, Curve, Line, Point3

if TYPE_CHECKING:
    from ..cam.plan_types import CamFile, Feature, OperationOut, SetupOut

#: The plan file version this reads (`lang.cam.plan_types.CAM_VERSION`); a
#: test keeps the two equal.
CAM_VERSION = 1
#: A template file's extension (`lang.cam.tooling`).
TEMPLATE_EXT = ".f3dhsm-template"
#: A bore's feed is never raised past this (mm/min), Auto Setup's
#: `rules.MAX_BORE_FEED`, which the plan's `feed_scale` counts on; a test
#: keeps the two equal.
MAX_BORE_FEED = 3000.0
#: How far (mm) a vertex of the model may lie off the plan's polyline, and a
#: face or an edge off the height it is looked for at.
TOL = 0.02
#: How much (relative) a loop of edges may be longer than the ring's
#: polygon, whose chords cut its arcs short.
LENGTH_SLACK = 0.01

Point2 = tuple[float, float]
#: Which Fusion parameter takes an operation's geometry, by its kind.
SELECTION = {"drill": "holeFaces", "bore": "circularFaces", "pocket": "pockets", "contour": "contours",
             "release": "contours", "dogbone": "contours", "chamfer": "contours", "groove": "curves"}


# -- what the emitter builds ----------------------------------------------------------------------------

@dataclass(frozen=True)
class Height:
    """A height parameter: Fusion's mode ("from stock top") and the offset (mm, up)."""
    mode: str
    offset: float


@dataclass
class Tabs:
    width: float
    height: float
    #: In the document (mm), at the stock's top.
    positions: list[Point3]


@dataclass
class Params:
    top: Height
    bottom: Height
    multiple_depths: bool | None
    stepdowns: int | None
    preserve_order: bool
    feed_scale: float | None
    tabs: Tabs | None


@dataclass
class Silhouette:
    """The part body's silhouette, its outside loop: an outer contour."""
    part: str
    ring: list[Point2]


@dataclass
class FaceLoop:
    """A closed loop of the part's edges along `ring`, at one of `levels`
    (z, mm), the first that has it: an inner contour, or a ring of a pocket
    taken out through; the waste inside it, or outside (an island's)."""
    part: str
    ring: list[Point2]
    levels: tuple[float, ...]
    waste_inside: bool = True


@dataclass
class Floor:
    """The faces of the part facing up at `z` inside the region (its outer
    ring first, then its islands): a pocket's floor."""
    part: str
    rings: list[list[Point2]]
    z: float


@dataclass
class Region:
    """A region to draw in the setup's sketch at `z`, each ring a closed
    chain of lines and arcs: a rest."""
    part: str
    loops: list[list[Curve]]
    z: float


@dataclass
class Cylinder:
    """The part's cylindrical faces about the vertical axis through
    `center`, `d` across: a hole's wall, or a dog bone's."""
    part: str
    center: Point2
    d: float


@dataclass
class WallArc:
    """The part's arc edges about `center`, `d` across, at one of `levels`
    (z, mm), the first that has some: a dog bone's wall, an open chain."""
    part: str
    center: Point2
    d: float
    arc: list[Point2]
    levels: tuple[float, ...]


@dataclass
class EdgePath:
    """The part's edges at `z` along the path (the material on its left):
    a chamfer's lower edges, one chain per run of them."""
    part: str
    points: list[Point2]
    closed: bool
    z: float


@dataclass
class EdgeLine:
    """The part's straight edges at `z` along the line from `start` to
    `end`: a V-groove's bottom, one open chain per run of them."""
    part: str
    start: Point2
    end: Point2
    z: float


Binding = Silhouette | FaceLoop | Floor | Region | Cylinder | WallArc | EdgePath | EdgeLine


@dataclass
class FeaturePlan:
    #: The plan's kind of feature (`outer`, `pocket`, `hole`, ...).
    what: str
    part: str
    #: What it machines, for the report: the part and its operations' names.
    label: str
    bindings: list[Binding]


@dataclass
class OperationPlan:
    name: str
    kind: str
    #: The template file's name without its extension.
    template: str
    label: str
    tool: float
    #: The Fusion parameter its geometry goes into (`SELECTION`).
    selection: str
    params: Params
    features: list[FeaturePlan]


@dataclass
class SetupPlan:
    name: str
    material: str
    sheet: str
    blank: str
    #: The blank's corner in the document (mm), at its underside, and its
    #: length, width and nominal thickness: the stock.
    corner: Point3
    size: Point3
    own_blank: bool
    #: The part bodies on the blank, by path: the setup's models.
    parts: list[str]
    operations: list[OperationPlan]
    #: The plan's own problems for the setup.
    problems: list[str] = field(default_factory=list[str])

    @property
    def top(self) -> float:
        """The stock's top in the document (mm): the setup's Z zero."""
        return self.corner[2] + self.size[2]

    def tab_positions(self) -> list[Point3]:
        """Every tab position of the setup, each once, in the order the
        operations name them."""
        out: list[Point3] = []
        seen: set[Point3] = set()
        for op in self.operations:
            for p in op.params.tabs.positions if op.params.tabs is not None else []:
                if p not in seen:
                    seen.add(p)
                    out.append(p)
        return out

    def regions(self) -> list[Region]:
        """Every region to draw in the setup's sketch."""
        return [b for op in self.operations for f in op.features for b in f.bindings if isinstance(b, Region)]


@dataclass
class CamDocPlan:
    """One material's setups, built in its nested document."""
    material: str
    setups: list[SetupPlan]


# -- reading a plan ------------------------------------------------------------------------------------

def check_plan(cam: Any, nest: Any) -> None:
    """A ValueError for a plan of another version, or of another nest than
    `nest` (its name, when it was written, its layout's hash), or naming a
    blank the nest has not got where it has it: plan the nest again."""
    if not isinstance(cam, dict) or cam.get("version") != CAM_VERSION:  # pyright: ignore[reportUnknownMemberType]
        found = cam.get("version") if isinstance(cam, dict) else None  # pyright: ignore[reportUnknownMemberType]
        raise ValueError(f"CAM plan version {found} is not supported (this reads {CAM_VERSION}); plan the nest "
                         "again (python -m lang.cam).")
    check_nest_version(nest)
    for key, nest_key in (("nest", "name"), ("nest_written", "written"), ("layout_hash", "layout_hash")):
        if cam[key] != nest[nest_key]:
            raise ValueError(f"the CAM plan is of another nest than the file beside it ({key} "
                             f"{cam[key]!r}, the nest's {nest[nest_key]!r}); plan the nest again "
                             "(python -m lang.cam).")
    blanks = {(m["material"], b["name"]): b for m in nest["materials"] for s in m["sheets"] for b in s["blanks"]}
    for setup in cam["setups"]:
        stock = setup["stock"]
        blank = blanks.get((stock["material"], stock["blank"]))
        if blank is None:
            raise ValueError(f"{setup['name']}: the nest has no blank {stock['blank']} of {stock['material']}.")
        if [float(v) for v in blank["rect"]] != [float(v) for v in stock["rect"]]:
            raise ValueError(f"{setup['name']}: the blank lies at {blank['rect']} in the nest, at {stock['rect']} "
                             "in the plan.")
        paths = {p["path"] for p in blank["parts"]}
        for op in setup["operations"]:
            for f in op["features"]:
                if f["part"] not in paths:
                    raise ValueError(f"{setup['name']}: {op['name']} machines {f['part']}, which is not on the "
                                     "blank.")


def plan_cam(cam: CamFile, nest: Any, material: str | None = None) -> list[CamDocPlan]:
    """The setups to build per material's document (or the one named), in
    the nest's order of materials and the plan's of setups."""
    check_plan(cam, nest)
    corners: dict[tuple[str, str], tuple[str, Point3, Point3]] = {}
    for m in nest["materials"]:
        t = float(m["thickness"])
        for s, y in zip(m["sheets"], sheet_places(m)):
            for b in s["blanks"]:
                bx, by, bw, bh = (float(v) for v in b["rect"])
                corners[(m["material"], b["name"])] = (str(s["name"]), (bx, y + by, 0.0), (bw, bh, t))
    docs: list[CamDocPlan] = []
    for m in nest["materials"]:
        if material is not None and m["material"] != material:
            continue
        setups: list[SetupPlan] = []
        for setup in cam["setups"]:
            stock = setup["stock"]
            if stock["material"] != m["material"]:
                continue
            sheet, corner, size = corners[(stock["material"], stock["blank"])]
            setups.append(_setup(setup, sheet, corner, size))
        docs.append(CamDocPlan(str(m["material"]), setups))
    if material is not None and not docs:
        raise ValueError(f"the nest has no material {material!r}.")
    return docs


def _setup(setup: SetupOut, sheet: str, corner: Point3, size: Point3) -> SetupPlan:
    frame = _Frame(corner, size[2])
    stock = setup["stock"]
    return SetupPlan(setup["name"], stock["material"], sheet, stock["blank"], corner, size, stock["own_blank"],
                     [p["path"] for p in setup["parts"]], [_operation(op, frame) for op in setup["operations"]],
                     list(setup["problems"]))


@dataclass(frozen=True)
class _Frame:
    """The setup's frame in the document: its blank's corner, the stock's top."""
    corner: Point3
    top: float

    def xy(self, p: list[float] | tuple[float, float]) -> Point2:
        return (self.corner[0] + float(p[0]), self.corner[1] + float(p[1]))

    def at(self, p: list[float] | tuple[float, float], depth: float = 0.0) -> Point3:
        x, y = self.xy(p)
        return (x, y, self.top - depth)

    def ring(self, ring: list[list[float]]) -> list[Point2]:
        return [self.xy(p) for p in ring]

    def depth(self, depth: float | None) -> float:
        """The height (mm) of a floor `depth` below the stock's top; through
        the blank's underside."""
        return self.corner[2] if depth is None else self.top - depth


def _operation(op: OperationOut, frame: _Frame) -> OperationPlan:
    kind = op["kind"]
    p = op["params"]
    tabs = p["tabs"]
    params = Params(Height(p["top"]["mode"], float(p["top"]["offset"])),
                    Height(p["bottom"]["mode"], float(p["bottom"]["offset"])), p["multiple_depths"], p["stepdowns"],
                    bool(p["preserve_order"]), p["feed_scale"],
                    Tabs(float(tabs["width"]), float(tabs["height"]), [frame.at(q) for q in tabs["positions"]])
                    if tabs is not None else None)
    if kind not in SELECTION:
        raise ValueError(f"{op['name']}: an operation of kind {kind!r} is not known.")
    return OperationPlan(op["name"], kind, op["template"], op["label"], float(op["tool"]["diameter"]),
                         SELECTION[kind], params, [_feature(kind, f, frame, op["name"]) for f in op["features"]])


def _label(f: Feature) -> str:
    names = [r["name"] or (r["kind"] if r["aspect"] == "op" else f"{r['kind']} {r['aspect']}") for r in f["ops"]]
    return f"{f['part']} " + ", ".join(dict.fromkeys(names))


def _feature(kind: str, f: Feature, frame: _Frame, op_name: str) -> FeaturePlan:
    """The feature's bindings for an operation of `kind`."""
    part = f["part"]
    levels = (frame.top, frame.corner[2])
    bindings: list[Binding]
    if f["what"] == "outer" and kind in ("contour", "release"):
        bindings = [Silhouette(part, frame.ring(f["ring"]))]
    elif f["what"] == "inner" and kind in ("contour", "release"):
        bindings = [FaceLoop(part, frame.ring(f["ring"]), levels)]
    elif f["what"] == "pocket" and kind == "pocket":
        if f["depth"] is None:
            bindings = [FaceLoop(part, frame.ring(r), levels, k == 0) for k, r in enumerate(f["rings"])]
        else:
            bindings = [Floor(part, [frame.ring(r) for r in f["rings"]], frame.depth(f["depth"]))]
    elif f["what"] == "rest" and kind == "pocket":
        z = frame.depth(f["depth"])
        bindings = [Region(part, [_lift(fit(frame.ring(r)), z) for r in f["rings"]], z)]
    elif f["what"] == "hole" and kind in ("drill", "bore"):
        bindings = [Cylinder(part, frame.xy(f["center"]), float(f["d"]))]
    elif f["what"] == "dogbone" and kind == "drill":
        bindings = [Cylinder(part, frame.xy(f["center"]), float(f["d"]))]
    elif f["what"] == "dogbone" and kind == "dogbone":
        bindings = [WallArc(part, frame.xy(f["center"]), float(f["d"]), frame.ring(f["arc"]),
                            (frame.depth(f["depth"]), frame.top))]
    elif f["what"] == "chamfer" and kind == "chamfer":
        z = frame.top - float(f["size"])
        bindings = [EdgePath(part, frame.ring(path["points"]), bool(path["closed"]), z) for path in f["paths"]]
    elif f["what"] == "vgroove" and kind == "groove":
        bindings = [EdgeLine(part, frame.xy(f["start"]), frame.xy(f["end"]), frame.top - float(f["depth"]))]
    else:
        raise ValueError(f"{op_name}: an operation of kind {kind!r} cannot machine a {f['what']!r} feature.")
    return FeaturePlan(f["what"], part, _label(f), bindings)


def _lift(curves: list[Line2 | Arc2 | Circle2], z: float) -> list[Curve]:
    def p(q: Point2) -> Point3:
        return (q[0], q[1], z)
    out: list[Curve] = []
    for c in curves:
        if isinstance(c, Line2):
            out.append(Line(p(c.a), p(c.b)))
        elif isinstance(c, Arc2):
            out.append(Arc(p(c.a), p(c.mid), p(c.b), p(c.center), c.radius))
        else:
            out.append(Circle(p(c.center), c.radius))
    return out


def read_plan(path: str) -> tuple[CamFile, Any, Any]:
    """A plan file (`cam.json`) with the nest and the layout beside it
    (`nest.json`, `nest.layout.json`), checked against each other."""
    import json
    folder = os.path.dirname(path)
    with open(path, encoding="utf-8") as fh:
        cam: CamFile = json.load(fh)
    with open(os.path.join(folder, "nest.json"), encoding="utf-8") as fh:
        nest = json.load(fh)
    check_plan(cam, nest)
    with open(os.path.join(folder, "nest.layout.json"), encoding="utf-8") as fh:
        layout = json.load(fh)
    return cam, nest, layout


def is_plan(data: Any) -> bool:
    """Whether a file read is a CAM plan (else a nest or a layout)."""
    return isinstance(data, dict) and "setups" in data and "nest_written" in data


def template_path(cam: CamFile, stem: str, repo: str) -> str:
    """The template file an operation is made from: in the folder the plan
    read, else in the folder its `cam.templates` names in `repo` (a plan
    made in another checkout), else the first, for Fusion to say."""
    folders = [cam["settings"]["templates"]]
    named = cam["settings"]["values"].get("cam.templates")
    if isinstance(named, str):
        folders.append(named if os.path.isabs(named) else os.path.join(repo, named))
    paths = [os.path.join(folder, stem + TEMPLATE_EXT) for folder in folders]
    return next((p for p in paths if os.path.exists(p)), paths[0])


# -- what is written on an operation ------------------------------------------------------------------------

def _mm(v: float) -> str:
    return f"{v:.10g} mm" if v != 0 else "0 mm"


def _bool(v: bool) -> str:
    return "true" if v else "false"


def param_writes(op: OperationPlan) -> list[tuple[str, str]]:
    """The parameters to write on an operation made from its template, in
    the order to write them (a mode before its offset, `doMultipleDepths`
    before the number of stepdowns, `group_tabs` before the tabs), as
    Fusion expressions. A Trace has no heights (its tip follows the
    groove's bottom), so none are written there; a bore's feed is
    `bore_feed`, as it needs the template's."""
    p = op.params
    writes: list[tuple[str, str]] = []
    if op.kind != "groove":
        for name, h in (("topHeight", p.top), ("bottomHeight", p.bottom)):
            writes += [(f"{name}_mode", f"'{h.mode}'"), (f"{name}_offset", _mm(h.offset))]
    if p.multiple_depths is not None:
        writes.append(("doMultipleDepths", _bool(p.multiple_depths)))
    if p.stepdowns is not None and p.multiple_depths is not False:
        writes.append(("numberOfStepdowns", str(p.stepdowns)))
    if op.kind not in ("drill", "bore"):
        writes.append(("preserveOrder", _bool(p.preserve_order)))
    if op.kind in ("drill", "bore"):
        # 'select same diameter' would pull in every hole of the setup of that diameter
        writes.append(("selectSameDiameter", "false"))
    if op.kind == "groove":
        # chamfering mode is the flank's; the groove is cut with the tip, in several depths
        writes.append(("doChamfer", "false"))
    if op.kind == "chamfer":
        # the chamfer is modelled: no width of its own, no clearance to it
        writes += [("chamferWidth", "0 mm"), ("chamferClearance", "0 mm")]
    if p.tabs is not None:
        writes += [("group_tabs", "true"), ("tabWidth", _mm(p.tabs.width)), ("tabHeight", _mm(p.tabs.height)),
                   ("tabPositioning", "'tabCount'"), ("tabsPerContour", "0")]
    else:
        writes.append(("group_tabs", "false"))
    return writes


#: Parameters a template's operation may not have, written only where it
#: has them: tabs where the strategy takes none, the order where it has none.
OPTIONAL = frozenset({"group_tabs", "preserveOrder", "selectSameDiameter"})


def bore_feed(template_feed: float, scale: float | None) -> float | None:
    """A bore's cutting feed (mm/min): the template's times the plan's
    scale, capped at `MAX_BORE_FEED`; None where it stays the template's
    (no scale, or no faster)."""
    if scale is None:
        return None
    feed = min(template_feed * scale, MAX_BORE_FEED)
    return feed if feed > template_feed else None


# -- binding by position ---------------------------------------------------------------------------------

def _segments(points: list[Point2], closed: bool) -> list[tuple[Point2, Point2]]:
    n = len(points)
    return [(points[i], points[(i + 1) % n]) for i in range(n if closed else n - 1)]


def _to_segment(p: Point2, a: Point2, b: Point2) -> float:
    dx, dy = b[0] - a[0], b[1] - a[1]
    length2 = dx * dx + dy * dy
    t = 0.0 if length2 == 0 else max(0.0, min(1.0, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / length2))
    return math.hypot(p[0] - a[0] - t * dx, p[1] - a[1] - t * dy)


def to_polyline(p: Point2, points: list[Point2], closed: bool) -> tuple[float, float]:
    """How far `p` lies from the polyline, and the length of the segment it
    is nearest."""
    best, length = math.inf, 0.0
    for a, b in _segments(points, closed):
        d = _to_segment(p, a, b)
        if d < best:
            best, length = d, math.dist(a, b)
    return best, length


def polyline_length(points: list[Point2], closed: bool) -> float:
    return sum(math.dist(a, b) for a, b in _segments(points, closed))


@dataclass(frozen=True)
class EdgeSample:
    """An edge of the model as the binding sees it (mm): its ends, its
    middle, its height, its radius where it is an arc or a circle (None for
    a line), its length."""
    start: Point3
    end: Point3
    mid: Point3
    radius: float | None
    length: float


def edge_on_path(edge: EdgeSample, points: list[Point2], closed: bool, z: float) -> bool:
    """Whether the edge lies at `z` along the polyline: its ends on it, and
    its middle too, an arc's within the sagitta of the polyline's chord
    there (the polyline's vertices lie on the arcs the model has)."""
    if any(abs(q[2] - z) > TOL for q in (edge.start, edge.end, edge.mid)):
        return False
    for q in (edge.start, edge.end):
        if to_polyline((q[0], q[1]), points, closed)[0] > TOL:
            return False
    d, chord = to_polyline((edge.mid[0], edge.mid[1]), points, closed)
    slack = 0.0
    if edge.radius is not None and edge.radius > 0:
        half = min(chord / 2, edge.radius)
        slack = edge.radius - math.sqrt(edge.radius * edge.radius - half * half)
    return d <= TOL + slack


def loop_follows(edges: list[EdgeSample], ring: list[Point2], z: float) -> bool:
    """Whether a closed loop of edges is the ring at `z`: every edge on it,
    and as long as it (no shorter than its polygon, at most `LENGTH_SLACK`
    longer)."""
    if not edges or not all(edge_on_path(e, ring, True, z) for e in edges):
        return False
    length, expected = sum(e.length for e in edges), polyline_length(ring, True)
    return expected - TOL <= length <= expected * (1 + LENGTH_SLACK) + TOL


def edge_on_line(edge: EdgeSample, start: Point2, end: Point2, z: float) -> bool:
    """Whether a straight edge lies at `z` on the segment from `start` to `end`."""
    if edge.radius is not None or any(abs(q[2] - z) > TOL for q in (edge.start, edge.end)):
        return False
    return all(_to_segment((q[0], q[1]), start, end) <= TOL for q in (edge.start, edge.end, edge.mid))


def on_circle(center: Point2, d: float, axis_point: Point2, radius: float) -> bool:
    """Whether a circle or cylinder about `axis_point` of `radius` is the
    one about `center`, `d` across."""
    return math.dist(center, axis_point) <= TOL and abs(radius - d / 2) <= TOL


def inside(p: Point2, rings: list[list[Point2]]) -> bool:
    """Whether `p` lies in the region (its outer ring, not in its islands),
    by the even-odd rule."""
    count = 0
    for ring in rings:
        n = len(ring)
        for i in range(n):
            (ax, ay), (bx, by) = ring[i], ring[(i + 1) % n]
            if (ay > p[1]) != (by > p[1]) and p[0] < ax + (p[1] - ay) * (bx - ax) / (by - ay):
                count += 1
    return count % 2 == 1


def region_samples(rings: list[list[Point2]], grid: int = 7, most: int = 48) -> list[Point2]:
    """Points inside the region to find its floor's faces by: a grid over
    its bounds, then points just inside its edges' middles (a narrow region
    the grid misses), at most `most`. A face is the floor where it holds one
    of them: a face shared by pockets that overlap lies in each one's region
    somewhere, but has its own point on it in one of them only."""
    xs = [p[0] for p in rings[0]]
    ys = [p[1] for p in rings[0]]
    out: list[Point2] = []
    for i in range(grid):
        for j in range(grid):
            q = (min(xs) + (max(xs) - min(xs)) * (i + 0.5) / grid, min(ys) + (max(ys) - min(ys)) * (j + 0.5) / grid)
            if inside(q, rings):
                out.append(q)
    edges = _segments(rings[0], True)
    step = max(1, len(edges) // max(1, most - len(out)))
    for a, b in edges[::step]:
        length = math.dist(a, b)
        if length < 4 * TOL:
            continue
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        nx, ny = -(b[1] - a[1]) / length * 2 * TOL, (b[0] - a[0]) / length * 2 * TOL
        for q in ((mx + nx, my + ny), (mx - nx, my - ny)):
            if inside(q, rings):
                out.append(q)
                break
    return out[:most]


def runs(edges: list[EdgeSample]) -> list[tuple[list[int], bool]]:
    """The edges (their indices) as connected runs, each in order from one
    end to the other (a closed run from any edge), an edge turned as it
    needs, and whether the run closes: a chain per run."""
    left = list(range(len(edges)))
    out: list[tuple[list[int], bool]] = []

    def meets(p: Point3, q: Point3) -> bool:
        return math.dist(p, q) <= TOL

    while left:
        run = [left.pop(0)]
        head, tail = edges[run[0]].start, edges[run[0]].end
        grown = True
        while grown:
            grown = False
            for k in list(left):
                e = edges[k]
                if meets(e.start, tail) or meets(e.end, tail):
                    run.append(k)
                    tail = e.end if meets(e.start, tail) else e.start
                elif meets(e.end, head) or meets(e.start, head):
                    run.insert(0, k)
                    head = e.start if meets(e.end, head) else e.end
                else:
                    continue
                left.remove(k)
                grown = True
        out.append((run, meets(head, tail)))
    return out


def left_of(mid: Point3, tangent: Point3, step: float = 2 * TOL) -> Point2:
    """A point just left of a curve's middle, seen from above, as the curve
    runs."""
    n = math.hypot(tangent[0], tangent[1]) or 1.0
    return (mid[0] - tangent[1] / n * step, mid[1] + tangent[0] / n * step)


def chain_reverted(mid: Point3, tangent: Point3, waste: Callable[[Point2], bool]) -> bool:
    """Whether a chain must be reversed for the tool to run on the waste:
    through the API Fusion places the tool on the left of the chain's first
    curve as it runs (its evaluator's direction), whatever the faces beside
    it say [found 2026-10-17: an inner contour's chain left as it came cut
    into the part, its toolpath as long as the ring offset outwards]."""
    return not waste(left_of(mid, tangent))


def chamfer_reverted(tangent: Point3, open_side: Point3) -> bool:
    """Whether a 2D Chamfer's chain along a chamfer's lower edge must be
    reversed: the tool runs on the left of the chain, which runs as its
    first edge does, and must run on the chamfer's open side, the way its
    face looks out (`lib/auto_setup/builder._tool_on_wrong_side`)."""
    return tangent[0] * open_side[1] - tangent[1] * open_side[0] < 0


__all__ = ["CAM_VERSION", "TEMPLATE_EXT", "MAX_BORE_FEED", "TOL", "SELECTION", "Height", "Tabs", "Params",
           "Silhouette", "FaceLoop", "Floor", "Region", "Cylinder", "WallArc", "EdgePath", "EdgeLine", "Binding",
           "FeaturePlan", "OperationPlan", "SetupPlan", "CamDocPlan", "check_plan", "plan_cam", "read_plan",
           "is_plan", "template_path", "param_writes", "OPTIONAL", "bore_feed", "EdgeSample", "edge_on_path",
           "loop_follows", "edge_on_line", "on_circle", "inside", "region_samples", "runs", "to_polyline", "polyline_length",
           "left_of", "chain_reverted", "chamfer_reverted"]
