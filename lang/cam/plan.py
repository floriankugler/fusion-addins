"""A nest planned for the machine: one setup per blank (`design/cam.md`).

Each blank is one load on the vacuum bed, machined from its top, where the
nest lays every part machining face up (`machine` in the layout) [decided
2026-10-15: one side only]. Per part on it the plan takes what the layout
says it is, nothing recognised:

- an operation made from the part's other big face is left out and
  reported; one in a narrow face (a box joint's grooves) is left out
  silently [decided]; a through hole or pocket goes through from either;
- holes (`rules.hole_choice`) are bored or drilled from the stock's top,
  their heights from it, a chamfered one too: its chamfer is the V-bit's
  afterwards [`proposals/cam.md`, Where Auto Setup goes wrong]; a through
  hole wider than `BIG_HOLE_LIMIT` is an opening of the outline, a blind one
  wider than twice the widest bore cutter a round pocket;
- pockets on the machining face take the cutters that reach them
  (`rules.pocket_cutters`), each piece its own region, a slot its line;
- the outline's rings (the outline less the through pockets and the wide
  through holes) are contours: the outer one, and the inner ones whose
  waste survives the contour's cutter (the waste shrunk by the cutter's
  diameter is not empty) and holds at least `cam.waste_area` (its
  footprint shrunk by `cam.tab_margin`); an inner one whose waste the
  cutter mills away, or whose waste is smaller, is taken out whole as a
  pocket through, with no release and no tabs [decided 2026-10-17];
- a contour is roughed to the skin, `cam.skin` above the stock's bottom
  (Fusion's order, the template's stepdowns), and cut free at the end of
  the setup by a release pass from the skin through to the breakthrough,
  one depth, the contours in the release order (`holding`) [decided
  2026-10-17]; both from the contour's template;
- a dog bone the layout marks goes with its operation where that
  operation's cutter cuts it, else to a drill or a dog bone cutter
  (`rules.dogbone_route`);
- chamfers and V-grooves are the V-bit's: one 2D Chamfer for every chamfer
  (its bottom from the contour), one Trace per number of passes;
- a part that holds too little (`holding`) gets tabs (`tabbing`) on its
  roughing and its release operation both.

The operations: one per tool, kind, template and parameters across the
blank's parts (the parameters Fusion sets per operation keep apart what
needs other heights; a bore's feed follows its hole, so bores are kept
apart by hole diameter as Auto Setup keeps them), tabbed contours in
operations of their own; ordered by tool, widest first, within a tool
drills, bores, pockets, contour roughing, dog bones; then the V-bit's,
the chamfers first; then the release passes, the widest cutter's first,
each in the release order, a tabbed run in its own operation.

An own blank (a `nest(False)` board named in a nest) has its operations
machined and its outline left to hand work: no outline contour, no
release of the board, no tabs.
"""
from __future__ import annotations

import math
from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from shapely.geometry import LineString, Point, Polygon
from shapely.geometry import box as shapely_box
from shapely.geometry.base import BaseGeometry
from shapely.geometry.polygon import orient
from shapely.ops import linemerge, unary_union

from ..core.cutouts import circle_geometry
from ..core.geometry import polygons_of
from ..core.layout_types import (ChamferLayout, CutLayout, HoleLayout, Layout, OpLayout, PartLayout, PocketLayout)
from ..emit.nested import check_nest_version
from ..emit.plan import (EdgeTarget, LayoutFrame, OpTarget, OutlineTarget, chamfer_target, check_version,
                         named_ops)
from ..nesting.nest_types import BlankOut, NestFile, PlacedPart
from . import holding, keys, rules, tabbing
from .plan_types import (CAM_VERSION, CamFile, ChamferFeature, ContourFeature, DogboneFeature, Feature,
                         GrooveFeature, HeightOut, HoleFeature, LeftOutOut, OperationKind, OperationOut, OpRef,
                         ParamsOut, PartOut, PathOut, PocketFeature, ReleaseOut, SetupOut, StockOut, TabsOut, ToolOut)
from .regions import CLEAN, Placed, hold, lines_of, ring_points
from .resolve import Values, resolve, summary
from .tooling import Registry, Template, registry_of

Point2 = tuple[float, float]
#: A tab needs the part's full thickness around it: no tab within this
#: distance (mm) of a pocket that comes within `THIN_NEAR` of the contour
#: (Auto Setup's full-thickness test, `THICKNESS_MARGIN`).
THIN_ALONG = 10.0
THIN_NEAR = 1.0
#: Default tab size (mm) where neither the setting nor the template says.
TAB_WIDTH = 5.0
TAB_HEIGHT = 2.0


# -- the plan ----------------------------------------------------------------------------------------

def plan_nest(nest: NestFile, layout: Layout, *, settings: Layout | None = None, registry: Registry | None = None,
              written: datetime | None = None) -> CamFile:
    """The plan of a nest (`nest.json`) and the layout it nested
    (`nest.layout.json`); the CAM settings from `settings` (the build as it
    is now) where given, else from the nested layout. The templates are
    `registry`, else those of the folder `cam.templates` names. A nest or
    layout of another version than this code reads is a ValueError."""
    check_nest_version(nest)
    check_version(layout)
    parts = [p["path"] for m in nest["materials"] for s in m["sheets"] for b in s["blanks"] for p in b["parts"]]
    base = nest["follows"] or nest["name"]
    values = resolve(settings or layout, base, parts, fallback=layout if settings is not None else None,
                     read_from="build" if settings is not None else "nest")
    if registry is None:
        registry = registry_of(str(values.templates_folder()))
    by_path = {p["path"]: p for m in layout["modules"] for p in m["parts"]}
    boxes = [(p["path"], p["box"]) for m in layout["modules"] for p in m["parts"]]
    setups: list[SetupOut] = []
    problems: list[str] = []
    for m in nest["materials"]:
        for sheet in m["sheets"]:
            for blank in sheet["blanks"]:
                setup = _Setup(nest["name"], m["material"], m["thickness"], sheet["name"], blank, layout, by_path,
                               boxes, values, registry).out()
                setups.append(setup)
                problems += [f"{setup['name']}: {p}" for p in setup["problems"]]
    out_values, sources, part_values, op_values = summary(values)
    return {
        "version": CAM_VERSION, "nest": nest["name"], "nest_written": nest["written"],
        "layout_hash": nest["layout_hash"],
        "written": (written or datetime.now()).astimezone().isoformat(timespec="seconds"),
        "settings": {"values": out_values, "sources": sources, "parts": part_values, "ops": op_values,
                     "read_from": "build" if values.read_from == "build" else "nest", "templates": registry.folder,
                     "smallest_cutter": smallest_cutter(values, registry)},
        "setups": setups, "problems": problems,
    }


def smallest_cutter(values: Values, registry: Registry) -> float:
    """`cam.smallest_cutter`, else the narrowest cutter of the pocket and
    contour templates for the cutter the nest's parts take most."""
    given = values.value(keys.smallest_cutter)
    if given is not None:
        return float(given)
    cutter = str(summary(values)[0]["cam.cutter"])
    tools = [t.narrowest for kind in ("pocket", "contour") for t in registry.of(kind, cutter)]
    return min(tools) if tools else 0.0


def setup_name(nest: str, material: str, blank: str) -> str:
    return f"{nest} {material} {blank}"


# -- one setup ---------------------------------------------------------------------------------------

def ref(index: int, op: OpLayout | None, aspect: str) -> OpRef:
    """An operation's aspect (`plan_types.OpRef`); -1 the outline."""
    if op is None:
        return {"index": index, "name": None, "kind": "outline", "aspect": aspect}
    name = op["op"]["name"] if op["kind"] == "edge" else None if op["kind"] == "chamfer" else op["name"]
    return {"index": index, "name": name, "kind": op["kind"], "aspect": aspect}


def _height(mode: str, offset: float) -> HeightOut:
    assert mode in ("from stock top", "from stock bottom", "from hole bottom", "from contour")
    return {"mode": mode, "offset": round(offset, 6)}  # pyright: ignore[reportReturnType]


def _params(top: HeightOut, bottom: HeightOut, *, multiple_depths: bool | None = None, stepdowns: int | None = None,
            preserve_order: bool = False, feed_scale: float | None = None, tabs: TabsOut | None = None) -> ParamsOut:
    return {"top": top, "bottom": bottom, "multiple_depths": multiple_depths, "stepdowns": stepdowns,
            "preserve_order": preserve_order, "feed_scale": feed_scale, "tabs": tabs}


def _tool(t: Template) -> ToolOut:
    tool = t.tool
    return {"type": tool.type, "diameter": tool.diameter, "flute": t.flute, "taper": tool.taper, "tip": tool.tip}


def _pt(p: Point2) -> list[float]:
    """A point for the file, as it is: rounded, the rings would recover
    their arcs otherwise where a circle meets an edge at a glancing angle
    [found by fuzzing, 2026-10-17]."""
    return [float(p[0]), float(p[1])]


@dataclass
class _Work:
    """An operation being gathered."""
    kind: OperationKind
    template: Template
    params: ParamsOut
    name: str
    #: Within its tool and kind: tabbed first, then this.
    sub: tuple[Any, ...] = ()
    tabbed: bool = False
    features: list[Feature] = field(default_factory=list[Feature])


@dataclass
class _Relief:
    """A dog bone of an operation, on the blank."""
    index: int
    op: CutLayout | PocketLayout
    k: int
    center: Point2
    d: float
    tool: float
    disc: BaseGeometry


@dataclass
class _Pending:
    """A piece of a blind pocket on the machining face, or a round pocket
    (a wide blind hole), before those of one floor are merged."""
    k: int
    op: HoleLayout | PocketLayout
    piece: int
    region: BaseGeometry
    depth: float
    name: str | None
    reliefs: list[_Relief]
    slot: Any


@dataclass
class _Ring:
    """A contour of a part's outline to cut: its index, the ring (the
    part on its left), the waste side, the operations it shares."""
    index: int
    outer: bool
    ring: list[list[float]]
    waste: BaseGeometry
    ops: list[OpRef]
    reliefs: list[_Relief]
    #: The name of the operation it settles for, where one has its own settings.
    op_name: str | None = None


@dataclass
class _Released:
    part: str
    ring: _Ring
    template: Template
    feature: ContourFeature


class _Setup:
    def __init__(self, nest: str, material: str, thickness: float, sheet: str, blank: BlankOut, layout: Layout,
                 by_path: dict[str, PartLayout], boxes: list[tuple[str, Any]], values: Values, registry: Registry):
        self.nest, self.material, self.thickness = nest, material, thickness
        self.blank = blank
        self.layout = layout
        self.frame = LayoutFrame(layout["frame"])
        self.values = values
        self.registry = registry
        self.boxes = boxes
        self.name = setup_name(nest, material, blank["name"])
        self.works: dict[tuple[Any, ...], _Work] = {}
        self.left_out: list[LeftOutOut] = []
        self.problems: list[str] = []
        self.parts_out: list[PartOut] = []
        self.released: list[_Released] = []
        self.release_order: list[ReleaseOut] = []
        self.breakthrough = float(values.value(keys.breakthrough))
        self.skin = float(values.value(keys.skin))
        self.rect = shapely_box(0.0, 0.0, blank["rect"][2], blank["rect"][3])
        self.placed = [(p, Placed.of(by_path[p["path"]], p["transform"], layout["frame"])) for p in blank["parts"]]
        # every part's footprint on the blank, for what lies across a kerf
        self.footprints = {pp.path: pp.footprint() for _p, pp in self.placed}
        #: ... and in its own frame, where its hold is measured.
        self.footprints_uv = {pp.path: pp.machine_outline(0.0, uv=True) for _p, pp in self.placed}
        self.tabbed: dict[str, tuple[Template, list[Point2], float, float]] = {}
        #: Each part's outer contour's cutter.
        self.outer_tool: dict[str, float] = {}
        #: The part's blind pockets, gathered (`pockets`), and each operation's count of pieces.
        self.pending: list[_Pending] = []
        self.pieces: dict[int, int] = {}
        #: Where each part's blind pockets may reach (`pocket_base`).
        self.bases: dict[str, BaseGeometry] = {}

    # -- helpers ---------------------------------------------------------------------------------

    def value(self, key: Any, part: str, op: str | None = None) -> Any:
        return self.values.value(key, part, op)

    def note(self, part: str, text: str) -> None:
        line = f"{part}: {text}"
        if line not in self.problems:
            self.problems.append(line)

    def leave(self, part: str, r: OpRef, why: str, note: str = "") -> None:
        self.left_out.append({"part": part, "op": r, "why": why, "note": note})  # pyright: ignore[reportArgumentType]

    def add(self, key: tuple[Any, ...], make: Callable[[], _Work], feature: Feature) -> None:
        work = self.works.get(key)
        if work is None:
            work = self.works[key] = make()
        work.features.append(feature)

    def cutter(self, part: str, op: str | None = None) -> str:
        return str(self.value(keys.cutter, part, op))

    def through_bottom(self) -> HeightOut:
        return _height("from stock bottom", -self.breakthrough)

    # -- the setup ---------------------------------------------------------------------------------

    def out(self) -> SetupOut:
        own = self.blank["own_blank"]
        for placed_part, pp in self.placed:
            self.part(placed_part, pp, own)
        if not own:
            self.release()
        operations = self.ordered()
        stock: StockOut = {"material": self.material, "sheet": self.blank["name"].split(".")[0],
                           "blank": self.blank["name"], "rect": list(self.blank["rect"]), "thickness": self.thickness,
                           "own_blank": own}
        return {"name": self.name, "stock": stock, "parts": self.parts_out, "operations": operations,
                "release_order": self.release_order, "left_out": self.left_out, "problems": self.problems}

    def part(self, placed_part: PlacedPart, pp: Placed, own: bool) -> None:
        part = pp.part
        path = pp.path
        ops = part["ops"]
        named = named_ops(part)
        reliefs = self.reliefs(pp)
        # holes and pockets, the narrow faces, the V-grooves
        for k, op in enumerate(ops):
            if op["kind"] == "edge":
                self.leave(path, ref(k, op, "op"), "narrow face")
                if op["op"]["chamfer"] > 0:
                    self.leave(path, ref(k, op, "chamfer"), "narrow face")
                for j, _bone in enumerate(op["op"]["dogbones"] if op["op"]["kind"] == "pocket" else []):
                    self.leave(path, ref(k, op, f"relief {j}"), "narrow face")
            elif op["kind"] == "hole":
                self.hole(pp, k, op)
            elif op["kind"] == "pocket":
                self.pocket(pp, k, op, [r for r in reliefs if r.index == k])
            elif op["kind"] == "vgroove":
                if pp.face(op["face"]) != "machine":
                    self.leave(path, ref(k, op, "op"), "other face" if pp.face(op["face"]) == "other" else
                               "narrow face")
                else:
                    self.groove(pp, k, op)
            elif op["kind"] == "chamfer":
                self.chamfer_op(pp, k, op, named)
            elif op["kind"] == "cut" and op["chamfer"] > 0:
                self.cut_chamfer(pp, k, op)
        self.pockets(pp)
        # the outline's rings
        self.rings(pp, own, [r for r in reliefs if r.op["kind"] == "cut" or pp.is_through(r.op["depth"])])
        # holding
        # (in the part's own frame: shrunk on the blank, a narrow neck pinched off or not as the part lay
        # [found by fuzzing, 2026-10-17])
        footprint = self.footprints_uv[path]
        margin = float(self.value(keys.tab_margin, path))
        held = hold(footprint, margin)
        policy = str(self.value(keys.tabs, path))
        tabs = 0
        if not own and (policy == "forced" or (policy == "auto" and holding.needs_tabs(
                footprint, margin, float(self.value(keys.tab_area, path))))):
            tabs = self.tabs(pp)
        self.parts_out.append({"path": path, "hold": round(held, 4), "tab_policy": policy,  # pyright: ignore[reportArgumentType]
                               "tabs": tabs})

    def reliefs(self, pp: Placed) -> list[_Relief]:
        out: list[_Relief] = []
        for k, op in enumerate(pp.part["ops"]):
            if op["kind"] != "cut" and op["kind"] != "pocket":
                continue
            for j, bone in enumerate(op["dogbones"]):
                c = pp.point(bone["center"][0], bone["center"][1])
                disc = Point(c).buffer(bone["d"] / 2, quad_segs=90)
                out.append(_Relief(k, op, j, c, bone["d"], bone["tool"], disc))
        return out

    # -- holes -------------------------------------------------------------------------------------

    def hole(self, pp: Placed, k: int, op: HoleLayout) -> None:
        path = pp.path
        face = pp.face(op["face"])
        through = op["through"] or pp.is_through(op["depth"])
        if face == "narrow":
            self.leave(path, ref(k, op, "op"), "narrow face")
            return
        center = pp.point(op["u"], op["v"])
        big = through and op["d"] > rules.BIG_HOLE_LIMIT     # an opening of the outline
        if not big and (through or face != "other") and \
                Point(center).buffer(op["d"] / 2, quad_segs=90).intersection(self.pocket_base(pp)).area < CLEAN * CLEAN:
            # (in what a through pocket takes off the board [found by fuzzing, 2026-10-17: bored off the blank])
            self.leave(path, ref(k, op, "op"), "gone", "nothing of it is left on the board")
            if op["chamfer"] > 0:
                self.leave(path, ref(k, op, "chamfer"), "gone")
            return
        if op["chamfer"] > 0:
            self.hole_chamfer(pp, k, op, face)
        if big:
            return
        if not through and face == "other":
            self.leave(path, ref(k, op, "op"), "other face")
            return
        name = op["name"]
        cutter = self.cutter(path, name)
        bores = rules.by_diameter(self.registry.of("bore", cutter, self.value(keys.bore_template, path, name)))
        drills = rules.by_diameter(self.registry.of("drill", cutter, self.value(keys.drill_template, path, name)))
        if not through and bores and op["d"] > 2 * max(bores):
            circle = Point(center).buffer(op["d"] / 2, quad_segs=90).intersection(self.pocket_base(pp))
            self.pending.append(_Pending(k, op, 0, circle, op["depth"], name, [], None))
            self.pieces[k] = 1
            return
        choice = rules.hole_choice(op["d"], op["depth"], through, self.breakthrough, bores, drills)
        if choice is None:
            self.leave(path, ref(k, op, "op"), "nothing fits",
                       f"no bore cutter fits a {op['d']:g} mm hole and no drill template has its diameter")
            return
        for n in choice.notes:
            self.note(path, n)
        t = choice.template
        kind: OperationKind = "drill" if t.kind == "drill" else "bore"
        if through:
            bottom, depth = self.through_bottom(), None
        elif choice.depth_limit is not None:
            bottom, depth = _height("from stock top", -choice.depth_limit), choice.depth_limit
        else:
            bottom, depth = _height("from hole bottom", 0.0), op["depth"]
        scale = rules.feed_scale(op["d"], choice.tool) if kind == "bore" else None
        params = _params(_height("from stock top", 0.0), bottom, feed_scale=scale)
        what = "through" if through else f"{choice.depth_limit:g} deep" if choice.depth_limit else "blind"
        label = f"{t.diameter:g} mm: {kind}s ({t.label}, " + (f"⌀{op['d']:g}, " if scale else "") + f"{what})"
        feature: HoleFeature = {"what": "hole", "part": path, "ops": [ref(k, op, "op")], "center": _pt(center),
                                "d": op["d"], "depth": depth}
        self.add((kind, t.stem, scale, bottom["mode"], bottom["offset"]),
                 lambda: _Work(kind, t, params, label, (scale or 0.0, bottom["mode"], -bottom["offset"])), feature)

    # -- pockets -----------------------------------------------------------------------------------

    def pocket(self, pp: Placed, k: int, op: PocketLayout, reliefs: list[_Relief]) -> None:
        path = pp.path
        face = pp.face(op["face"])
        if pp.is_through(op["depth"]) and face != "narrow":
            if op["chamfer"] > 0:
                self.op_chamfer(pp, k, op, face, op["chamfer"])
            return                                       # an opening of the outline
        if face != "machine":
            why = "other face" if face == "other" else "narrow face"
            self.leave(path, ref(k, op, "op"), why)
            if op["chamfer"] > 0:
                self.leave(path, ref(k, op, "chamfer"), why)
            for r in reliefs:
                self.leave(path, ref(k, op, f"relief {r.k}"), why)
            return
        if op["chamfer"] > 0:
            self.op_chamfer(pp, k, op, face, op["chamfer"])
        region = pp.region(op["shape"]).intersection(self.pocket_base(pp))
        pieces = [p for p in polygons_of(region) if p.area > CLEAN * CLEAN]
        if not pieces:
            self.leave(path, ref(k, op, "op"), "gone", "nothing of it is left on the board")
            for r in reliefs:
                self.leave(path, ref(k, op, f"relief {r.k}"), "gone")
            return
        slot = None
        if op["slot"] is not None and len(pieces) == 1:
            s = op["slot"]
            slot = {"start": _pt(pp.point(s["start"][0], s["start"][1])),
                    "end": _pt(pp.point(s["end"][0], s["end"][1])), "width": s["width"]}
        own: dict[int, list[_Relief]] = {i: [] for i in range(len(pieces))}
        for r in reliefs:
            best = max(range(len(pieces)), key=lambda i: pieces[i].intersection(r.disc).area)
            own[best].append(r)
        for i, piece in enumerate(pieces):
            self.pending.append(_Pending(k, op, i, piece, op["depth"], op["name"], own[i], slot))
        self.pieces[k] = len(pieces)

    def pocket_base(self, pp: Placed) -> BaseGeometry:
        """Where the part's blind pockets may reach: its outline within its
        outer loop, the openings under them included, as they are material
        yet when the blind pockets run (a counterbore over a through slot is
        one pocket), but an opening another part lies in [found by fuzzing,
        2026-10-17: clipped by the outline alone, a pocket reached past an
        opening at the board's edge, off the blank]."""
        base = self.bases.get(pp.path)
        if base is None:
            outline = pp.outline()
            loop = pp.machine_outline(rules.BIG_HOLE_LIMIT)
            base = outline.intersection(Polygon(loop.exterior)) if not loop.is_empty else outline
            others = unary_union([fp for path, fp in self.footprints.items() if path != pp.path])
            for _k, opening in pp.openings(0.0):
                if not others.is_empty and opening.intersects(others):
                    base = base.difference(opening)
            self.bases[pp.path] = base
        return base

    def pockets(self, pp: Placed) -> None:
        """The part's blind pockets on its machining face, those of one depth
        that overlap or touch as one region, as their floor is one face (a
        Cabineo's three access holes)."""
        path = pp.path
        groups: list[list[_Pending]] = []
        for entry in self.pending:
            near = [g for g in groups if abs(g[0].depth - entry.depth) < 1e-6 and
                    any(e.region.distance(entry.region) < 1e-6 for e in g)]
            merged = [entry] + [e for g in near for e in g]
            groups = [g for g in groups if not any(g is n for n in near)] + [merged]
        missed: dict[int, list[int]] = {}
        for group in groups:
            group.sort(key=lambda e: (e.k, e.piece))
            refs = list({e.k: ref(e.k, e.op, "op") for e in group}.values())
            region = unary_union([e.region for e in group]) if len(group) > 1 else group[0].region
            slot = group[0].slot if len(group) == 1 else None
            reliefs = [r for e in group for r in e.reliefs]
            if not self.pocket_region(pp, refs, region, group[0].depth, group[0].name, reliefs, slot):
                for e in group:
                    missed.setdefault(e.k, []).append(e.piece)
        for k, gone in missed.items():
            op = pp.part["ops"][k]
            if len(gone) == self.pieces[k]:
                self.leave(path, ref(k, op, "op"), "nothing fits", "no pocket cutter gets into it")
            else:
                # a piece no cutter gets into, beside others planned
                for i in gone:
                    self.leave(path, ref(k, op, f"piece {i}"), "nothing fits", "no pocket cutter gets into it")
        self.pending = []
        self.pieces = {}

    def pocket_region(self, pp: Placed, refs: list[OpRef], region: BaseGeometry, depth: float | None,
                      name: str | None, reliefs: list[_Relief], slot: Any) -> bool:
        """A region to take out, `depth` deep from the stock's top (None:
        through), with the dog bones in it; whether it is planned (else the
        caller leaves `refs` out: nothing fits)."""
        path = pp.path
        discs = unary_union([r.disc.buffer(2 * CLEAN) for r in reliefs]) if reliefs else None
        if discs is not None and region.difference(discs).area < 1e-6:
            # all of it is dog bones: each its own way, the region with the first
            return self.route(pp, reliefs, depth, refs)
        cutter = self.cutter(path, name)
        finish = bool(self.value(keys.finish_pockets if depth is not None else keys.finish_inner, path, name))
        tried, notes = rules.candidates(self.registry, "pocket", str(self.value(keys.pocket_template, path, name)),
                                        finish, cutter)
        for n in notes:
            self.note(path, n)
        reach = self.thickness + self.breakthrough if depth is None else depth
        plan = rules.pocket_cutters(region, reach, tried, discs)
        for n in plan.notes:
            self.note(path, n)
        if plan.main is None:
            self.route(pp, reliefs, depth, [])
            return False
        mine = [r for r in reliefs if rules.self_cut(r.d, plan.main.narrowest)]
        routed = [r for r in reliefs if r not in mine]
        bottom = self.through_bottom() if depth is None else _height("from contour", 0.0)
        feature: PocketFeature = {"what": "pocket", "part": path,
                                  "ops": refs + [ref(r.index, r.op, f"relief {r.k}") for r in mine],
                                  "rings": _rings(region), "depth": depth, "slot": slot}
        self.add_pocket(plan.main, bottom, feature)
        for t, piece in plan.rests:
            rest: PocketFeature = {"what": "rest", "part": path, "ops": list(refs), "rings": _rings(piece),
                                   "depth": depth, "slot": None}
            self.add_pocket(t, bottom, rest)
        for piece in plan.unreached:
            self.note(path, f"no pocket cutter reaches {piece.area:.1f} mm² of {_names(refs)} near "
                            f"({piece.centroid.x:.0f}, {piece.centroid.y:.0f})")
        self.route(pp, routed, depth, [])
        return True

    def add_pocket(self, t: Template, bottom: HeightOut, feature: PocketFeature) -> None:
        through = bottom["mode"] == "from stock bottom"
        label = f"{t.diameter:g} mm: pockets ({t.label}{', through' if through else ''})"
        self.add(("pocket", t.stem, bottom["mode"]),
                 lambda: _Work("pocket", t, _params(_height("from stock top", 0.0), bottom), label, (through,)),
                 feature)

    # -- dog bones ---------------------------------------------------------------------------------

    def route(self, pp: Placed, reliefs: list[_Relief], depth: float | None, refs: list[OpRef]) -> bool:
        """Dog bones their operation's cutter does not cut: a drill of their
        diameter, else a dog bone cutter, along their wall. `refs` go with
        the first one routed (a pocket that is all dog bones); whether they
        went (else the caller leaves them out)."""
        path = pp.path
        material = self.footprints[pp.path]
        for r in reliefs:
            name = r.op["name"]
            cutter = self.cutter(path, name)
            drills = rules.by_diameter(self.registry.of("drill", cutter, self.value(keys.drill_template, path, name)))
            dogbones = self.registry.of("dogbone", cutter, self.value(keys.dogbone_template, path, name))
            routed = rules.dogbone_route(r.d, drills, dogbones)
            if routed is None:
                self.leave(path, ref(r.index, r.op, f"relief {r.k}"), "nothing fits",
                           f"no drill template of {r.d:g} mm and no dog bone cutter {rules.RELIEF_TOL:g} narrower")
                continue
            mine = [ref(r.index, r.op, f"relief {r.k}")] + refs
            refs = []
            t: Template = routed
            if t.flute is not None and t.flute < (depth if depth is not None else self.thickness + self.breakthrough) \
                    - rules.DEPTH_TOL:
                self.note(path, f"a dog bone {depth or 'through'} deep is deeper than {t.stem}'s flute; check the "
                                "operation")
            feature: DogboneFeature = {"what": "dogbone", "part": path, "ops": mine, "center": _pt(r.center),
                                       "d": r.d, "tool": r.tool, "depth": depth, "arc": _arc(r, material)}
            kind: OperationKind = "drill" if t.kind == "drill" else "dogbone"
            bottom = self.through_bottom() if depth is None else _height("from stock top", -depth)
            what = "through" if depth is None else f"{depth:g} deep"
            label = f"{t.diameter:g} mm: dog bones ({t.label}, {what})"
            self.add((kind, "relief", t.stem, bottom["mode"], bottom["offset"]),
                     lambda: _Work(kind, t, _params(_height("from stock top", 0.0), bottom), label,
                                   (1, -bottom["offset"])), feature)
        return not refs

    # -- the outline -------------------------------------------------------------------------------

    def rings(self, pp: Placed, own: bool, reliefs: list[_Relief]) -> None:
        path = pp.path
        rings, unclaimed = contours(pp, reliefs)
        for k, op in unclaimed:
            if own and op["kind"] == "cut":
                self.leave(path, ref(k, op, "op"), "hand work", "an own blank's outline is cut by hand")
            else:
                self.leave(path, ref(k, op, "op"), "gone", "nothing of it is left on the board")
        for ring in rings:
            if own and (ring.outer or all(r["kind"] == "cut" for r in ring.ops if r["index"] >= 0)):
                for r in ring.ops:
                    self.leave(path, r, "hand work", "an own blank's outline is cut by hand")
                for rel in ring.reliefs:
                    self.leave(path, ref(rel.index, rel.op, f"relief {rel.k}"), "hand work")
                continue
            self.ring(pp, ring, own)

    def ring(self, pp: Placed, ring: _Ring, own: bool = False) -> None:
        path, name = pp.path, ring.op_name
        cutter = self.cutter(path, name)
        finish = bool(self.value(keys.finish_outer if ring.outer else keys.finish_inner, path, name))
        tried, notes = rules.candidates(self.registry, "contour", str(self.value(keys.contour_template, path, name)),
                                        finish, cutter)
        for n in notes:
            self.note(path, n)
        discs = unary_union([r.disc.buffer(2 * CLEAN) for r in ring.reliefs]) if ring.reliefs else None
        through = self.thickness + self.breakthrough
        t, notes = rules.contour_cutter(ring.waste, through, tried, discs)
        for n in notes:
            self.note(path, f"{'the outer contour' if ring.outer else 'an inner contour'}: {n}")
        if ring.outer and t is not None:
            self.outer_tool[path] = t.diameter
        if not ring.outer:
            # its waste is milled away, or too small to keep, or it would be cut free after its part (by a
            # narrower cutter, whose release comes later), or the part is its own blank, which is not
            # released: taken out whole
            survives = ring.waste.buffer(-t.diameter) if t is not None else Polygon()
            margin = float(self.value(keys.tab_margin, path, name))
            if own or t is None or survives.is_empty or t.diameter < self.outer_tool.get(path, 0.0) - 1e-9 or \
                    hold(survives, margin) < float(self.value(keys.waste_area, path, name)):
                if not self.pocket_region(pp, ring.ops, ring.waste, None, name, ring.reliefs, None):
                    for r in ring.ops:
                        self.leave(path, r, "nothing fits", "no pocket cutter gets into its waste")
                return
        if t is None:
            for r in ring.ops:
                self.leave(path, r, "nothing fits", "no contour template")
            return
        mine = [r for r in ring.reliefs if rules.self_cut(r.d, t.narrowest)]
        routed = [r for r in ring.reliefs if r not in mine]
        feature: ContourFeature = {"what": "outer" if ring.outer else "inner", "part": path,
                                   "ops": ring.ops + [ref(r.index, r.op, f"relief {r.k}") for r in mine],
                                   "ring": ring.ring}
        self.released.append(_Released(path, ring, t, feature))
        self.route(pp, routed, None, [])

    def roughing(self, released: _Released, tabs: TabsOut | None) -> None:
        t = released.template
        own: TabsOut | None = {"width": tabs["width"], "height": tabs["height"], "positions": list(tabs["positions"])} \
            if tabs is not None else None
        params = _params(_height("from stock top", 0.0), _height("from stock bottom", self.skin), tabs=own)
        tab_key = (tabs["width"], tabs["height"]) if tabs is not None else None
        label = f"{t.diameter:g} mm: contours, roughing ({t.label}{', tabs' if tabs else ''})"
        key = ("contour", t.stem, tab_key)
        work = self.works.get(key)
        if work is None:
            work = self.works[key] = _Work("contour", t, params, label, (0 if tabs else 1,), tabbed=tabs is not None)
        elif tabs is not None and work.params["tabs"] is not None:
            work.params["tabs"]["positions"] += tabs["positions"]
        work.features.append(released.feature)

    # -- holding -----------------------------------------------------------------------------------

    def tabs(self, pp: Placed) -> int:
        """Tabs on the part's outer contour; their count."""
        path = pp.path
        outer = next((r for r in self.released if r.part == path and r.ring.outer), None)
        if outer is None:
            return 0
        t = outer.template
        width = self.value(keys.tab_width, path) or t.number("tabWidth") or TAB_WIDTH
        height = self.value(keys.tab_height, path) or t.number("tabHeight") or TAB_HEIGHT
        least = int(self.value(keys.tab_min_count, path))
        footprint = self.footprints[path]
        hidden = _hidden(pp, self.boxes, self.frame)
        chamfered = _chamfered(pp, self.frame)
        ring_line = LineString(outer.ring.ring + outer.ring.ring[:1])
        thin = _thinned(pp, ring_line)
        diameter = t.diameter

        def weight(p: Point2) -> float:
            at = Point(p)
            if chamfered is not None and chamfered.distance(at) < width / 2 + 0.5:
                return 0.0
            if thin is not None and thin.distance(at) < THIN_ALONG:
                return 0.0
            neighbour = self.neighbour(path, p, ring_line, diameter)
            if neighbour == "none":
                return 0.0
            tier = tabbing.HIDDEN if hidden is not None and hidden.distance(at) < 0.5 else tabbing.PLAIN
            return tier * (tabbing.LOOSE if neighbour == "loose" else 1.0)

        c = footprint.centroid
        positions, _want = tabbing.place(outer.ring.ring, float(width), least, (c.x, c.y), weight)
        if len(positions) < least:
            self.note(path, f"{len(positions)} tab(s) of the {least} it should have: no more sites off chamfered "
                            "edges, thinned stretches and kerfs with nothing across")
        self.tabbed[path] = (t, positions, float(width), float(height))
        return len(positions)

    def neighbour(self, path: str, p: Point2, ring: LineString, diameter: float) -> str:
        """What lies across the kerf from a point of a part's outer contour
        when the part is released: `sheet` (still held on by its skin),
        `loose` (a part released before), or `none`."""
        d = ring.project(Point(p))
        a, b = ring.interpolate(max(d - 0.1, 0.0)), ring.interpolate(min(d + 0.1, ring.length))
        tx, ty = b.x - a.x, b.y - a.y
        n = math.hypot(tx, ty) or 1.0
        out = (ty / n, -tx / n)                    # the part on the left: outward is to the right
        q = Point(p[0] + out[0] * (diameter + 0.5), p[1] + out[1] * (diameter + 0.5))
        if not self.rect.contains(q):
            return "none"
        for other, footprint in self.footprints.items():
            if other != path and footprint.buffer(diameter).contains(q):
                return "loose" if other in self.order_before(path) else "sheet"
        return "sheet"

    def order_before(self, path: str) -> set[str]:
        """The parts released before this one."""
        order = self.part_order()
        return set(order[:order.index(path)]) if path in order else set()

    def part_order(self) -> list[str]:
        cached = getattr(self, "_order", None)
        if cached is not None:
            return cached
        entries = [(pp.path, hold(self.footprints_uv[pp.path], float(self.value(keys.tab_margin, pp.path))),
                    self.footprints[pp.path].centroid) for _p, pp in self.placed if self.footprints[pp.path].area > 0]
        order = holding.release_order([(path, h, (c.x, c.y)) for path, h, c in entries])
        self._order = order
        return order

    def release(self) -> None:
        """The roughing and release operations of the contours, in the
        release order, tabbed runs apart."""
        order = self.part_order()
        rank = {path: k for k, path in enumerate(order)}
        tabs_of: dict[str, TabsOut] = {}
        for path, (t, positions, width, height) in self.tabbed.items():
            if positions:
                tabs_of[path] = {"width": width, "height": height, "positions": [_pt(p) for p in positions]}
        for released in self.released:
            self.roughing(released, tabs_of.get(released.part) if released.ring.outer else None)
        # the release order: per part its inner contours (nearest first) and then its outer one
        ordered: list[_Released] = []
        for path in sorted({r.part for r in self.released}, key=lambda p: rank.get(p, len(rank))):
            mine = [r for r in self.released if r.part == path]
            inner = holding.by_travel([(r, _ring_start(r.ring.ring)) for r in mine if not r.ring.outer])
            ordered += inner + [r for r in mine if r.ring.outer]
        tools = sorted({r.template.diameter for r in ordered}, reverse=True)
        run = 0
        for tool in tools:
            last: tuple[str, bool] | None = None
            for r in ordered:
                if r.template.diameter != tool:
                    continue
                tabs = tabs_of.get(r.part) if r.ring.outer else None
                key_now = (r.template.stem, tabs is not None)
                if key_now != last:
                    run += 1
                    last = key_now
                t = r.template
                params = _params(_height("from stock bottom", self.skin), self.through_bottom(), multiple_depths=False,
                                 preserve_order=True,
                                 tabs={"width": tabs["width"], "height": tabs["height"], "positions": []}
                                 if tabs is not None else None)
                label = f"{t.diameter:g} mm: release ({t.label}{', tabs' if tabs else ''})"
                work = self.works.get(("release", run))
                if work is None:
                    work = self.works[("release", run)] = _Work("release", t, params, label, (run,),
                                                                tabbed=tabs is not None)
                if tabs is not None and work.params["tabs"] is not None:
                    work.params["tabs"]["positions"] += tabs["positions"]
                work.features.append(r.feature)
                self.release_order.append({"part": r.part, "what": "outer" if r.ring.outer else "inner",
                                           "ring": r.ring.index, "tool": tool})

    # -- the V-bit ---------------------------------------------------------------------------------

    def groove(self, pp: Placed, k: int, op: Any) -> None:
        path = pp.path
        t, notes = rules.v_bit(self.registry, "groove", self.cutter(path, op["name"]),
                               self.value(keys.groove_template, path, op["name"]))
        for n in notes:
            self.note(path, n)
        if t is None:
            self.leave(path, ref(k, op, "op"), "nothing fits", "no groove template")
            return
        if t.reach is not None and op["depth"] > t.reach + rules.DEPTH_TOL:
            self.note(path, f"a V-groove {op['depth']:g} deep is deeper than {t.stem} cuts ({t.reach:g})")
        passes = rules.groove_passes(op["depth"], t)
        feature: GrooveFeature = {"what": "vgroove", "part": path, "ops": [ref(k, op, "op")],
                                  "start": _pt(pp.point(op["start"][0], op["start"][1])),
                                  "end": _pt(pp.point(op["end"][0], op["end"][1])), "depth": op["depth"]}
        label = f"V-grooves ({t.label}, {passes} pass{'es' if passes > 1 else ''})"
        params = _params(_height("from stock top", 0.0), _height("from contour", 0.0),
                         multiple_depths=passes > 1, stepdowns=passes - 1)
        self.add(("groove", t.stem, passes), lambda: _Work("groove", t, params, label, (1, passes)), feature)

    def add_chamfer(self, pp: Placed, refs: list[OpRef], size: float, paths: list[PathOut],
                    rim: tuple[Point2, float] | None, name: str | None) -> None:
        path = pp.path
        t, notes = rules.v_bit(self.registry, "chamfer", self.cutter(path, name),
                               self.value(keys.chamfer_template, path, name))
        for n in notes:
            self.note(path, n)
        if t is None:
            for r in refs:
                self.leave(path, r, "nothing fits", "no chamfer template")
            return
        fits, notes = rules.chamfer_fits(size, rim[1] / 2 if rim is not None else None, t)
        for n in notes:
            self.note(path, n)
        if not fits:
            for r in refs:
                self.leave(path, r, "nothing fits", notes[0] if notes else "")
            return
        if not paths:
            for r in refs:
                self.leave(path, r, "gone", "nothing of its edge is left")
            return
        feature: ChamferFeature = {"what": "chamfer", "part": path, "ops": refs, "size": size, "paths": paths,
                                   "hole": {"center": _pt(rim[0]), "d": rim[1]} if rim is not None else None}
        label = f"chamfers ({t.label})"
        params = _params(_height("from stock top", 0.0), _height("from contour", 0.0))
        self.add(("chamfer", t.stem), lambda: _Work("chamfer", t, params, label, (0,)), feature)

    def chamfer_op(self, pp: Placed, k: int, op: ChamferLayout, named: dict[str, OpLayout]) -> None:
        path = pp.path
        face = pp.face(op["face"])
        r = ref(k, op, "op")
        if face != "machine":
            self.leave(path, r, "other face" if face == "other" else "narrow face")
            return
        target = chamfer_target(op, named, self.frame)
        outline = pp.machine_outline(rules.BIG_HOLE_LIMIT)
        if isinstance(target, OutlineTarget):
            self.add_chamfer(pp, [r], op["size"], [_closed(orient(outline, 1.0).exterior)], None, None)
        elif isinstance(target, EdgeTarget):
            narrow = target.a if pp.face(target.a) == "narrow" else target.b
            self.add_chamfer(pp, [r], op["size"], _edge_paths(pp, narrow), None, None)
        elif isinstance(target, OpTarget):
            inner = target.op
            if inner["kind"] == "hole":
                c = pp.point(inner["u"], inner["v"])
                self.add_chamfer(pp, [r], op["size"], [_circle_path(c, inner["d"])], (c, inner["d"]), inner["name"])
            elif inner["kind"] == "edge":
                self.leave(path, r, "narrow face")
            elif inner["kind"] == "cut" or inner["kind"] == "pocket":
                self.add_chamfer(pp, [r], op["size"], _rim_paths(pp.region(inner["shape"]), outline), None,
                                 inner["name"])
            else:
                self.leave(path, r, "gone", f"a chamfer along {op['what']!r} follows nothing")
        else:
            self.leave(path, r, "gone", f"a chamfer along {op['what']!r} names nothing on the part")

    def cut_chamfer(self, pp: Placed, k: int, op: CutLayout) -> None:
        """A cut's chamfer, on the part's show face."""
        face = pp.face(pp.part["show"])
        if face != "machine":
            self.leave(pp.path, ref(k, op, "chamfer"), "other face")
            return
        self.add_chamfer(pp, [ref(k, op, "chamfer")], op["chamfer"],
                         _rim_paths(pp.region(op["shape"]), pp.machine_outline(rules.BIG_HOLE_LIMIT)), None, op["name"])

    def op_chamfer(self, pp: Placed, k: int, op: PocketLayout, face: str, size: float) -> None:
        if face != "machine":
            self.leave(pp.path, ref(k, op, "chamfer"), "other face" if face == "other" else "narrow face")
            return
        self.add_chamfer(pp, [ref(k, op, "chamfer")], size,
                         _rim_paths(pp.region(op["shape"]), pp.machine_outline(rules.BIG_HOLE_LIMIT)), None, op["name"])

    def hole_chamfer(self, pp: Placed, k: int, op: HoleLayout, face: str) -> None:
        if face != "machine":
            self.leave(pp.path, ref(k, op, "chamfer"), "other face")
            return
        c = pp.point(op["u"], op["v"])
        self.add_chamfer(pp, [ref(k, op, "chamfer")], op["chamfer"], [_circle_path(c, op["d"])], (c, op["d"]),
                         op["name"])

    # -- the order -----------------------------------------------------------------------------

    def ordered(self) -> list[OperationOut]:
        def key(w: _Work) -> tuple[Any, ...]:
            if w.kind == "release":
                return (2, -w.template.diameter, w.sub)
            if w.kind in ("chamfer", "groove"):
                return (1, 0 if w.kind == "chamfer" else 1, w.sub)
            return (0, -round(w.template.diameter, 4), rules.KIND_ORDER[w.kind], 0 if w.tabbed else 1, w.sub,
                    w.template.stem)
        out: list[OperationOut] = []
        for w in sorted(self.works.values(), key=key):
            out.append({"name": w.name, "kind": w.kind, "template": w.template.stem, "label": w.template.label,
                        "tool": _tool(w.template), "params": w.params, "features": w.features})
        return out


# -- the outline's contours ----------------------------------------------------------------------------

def contours(pp: Placed, reliefs: Sequence[_Relief]) -> tuple[list[_Ring], list[tuple[int, OpLayout]]]:
    """The part's contours from its machining face: the rings of its
    outline less its through pockets and wide through holes (the outer one
    first), each with the operations whose material it takes (cuts,
    through pockets, wide holes; the outline itself as ring k) and their
    dog bones; and the operations no ring takes."""
    shape = pp.machine_outline(rules.BIG_HOLE_LIMIT)
    if shape.is_empty:
        return [], []
    ops = pp.part["ops"]
    takers: list[tuple[int, BaseGeometry]] = []
    for k, op in enumerate(ops):
        if op["kind"] == "cut":
            takers.append((k, pp.region(op["shape"])))
    takers += pp.openings(rules.BIG_HOLE_LIMIT)
    rings: list[_Ring] = []
    exterior = Polygon(shape.exterior)
    x0, y0, x1, y1 = exterior.bounds
    frame = shapely_box(x0 - 30, y0 - 30, x1 + 30, y1 + 30)
    wastes: list[tuple[bool, list[list[float]], BaseGeometry]] = [(True, ring_points(shape.exterior),
                                                                 frame.difference(exterior))]
    for interior in shape.interiors:
        wastes.append((False, ring_points(interior), Polygon(interior)))
    claimed: set[int] = set()
    for i, (outer, ring, waste) in enumerate(wastes):
        mine: list[OpRef] = [ref(-1, None, f"ring {i}")]
        names: list[str] = []
        for k, region in takers:
            if region.intersection(waste).area > 1e-6:
                mine.append(ref(k, ops[k], "op"))
                claimed.add(k)
                name = mine[-1]["name"]
                if name:
                    names.append(name)
        rings.append(_Ring(i, outer, ring, waste, mine, [], names[0] if names else None))
    for r in reliefs:
        best = max(rings, key=lambda ring: ring.waste.intersection(r.disc).area)
        if best.waste.intersection(r.disc).area > 1e-6:
            best.reliefs.append(r)
    unclaimed = [(k, ops[k]) for k, _g in takers if k not in claimed]
    return rings, unclaimed


# -- geometry for the features ---------------------------------------------------------------------------

def _rings(g: BaseGeometry) -> list[list[list[float]]]:
    out: list[list[list[float]]] = []
    for poly in polygons_of(g):
        poly = orient(poly, 1.0)
        for ring in [poly.exterior, *poly.interiors]:
            out.append([_pt((float(c[0]), float(c[1]))) for c in list(ring.coords)[:-1]])
    return out


def _closed(ring: object) -> PathOut:
    return {"points": [_pt((p[0], p[1])) for p in ring_points(ring)], "closed": True}


def _circle_path(center: Point2, d: float) -> PathOut:
    """A hole's rim, the material on its left: clockwise about the hole."""
    ring = orient(circle_geometry(center, d / 2), -1.0).exterior
    return _closed(ring)


def _rim_paths(removed: BaseGeometry, outline: BaseGeometry) -> list[PathOut]:
    """The edges a cut or pocket leaves at the stock's top, the material on
    their left: its boundary where the part is."""
    out: list[PathOut] = []
    rim = outline.buffer(1e-6)
    for poly in polygons_of(removed):
        poly = orient(poly, -1.0)                 # clockwise: the material outside it on the left
        for ring in [poly.exterior, *poly.interiors]:
            line = LineString(ring.coords)
            kept = line.intersection(rim)
            if kept.length >= line.length - 1e-6:
                out.append(_closed(ring))
                continue
            for piece in lines_of(_merged(kept)):
                if piece.length > 1e-6:
                    out.append({"points": [_pt((c[0], c[1])) for c in piece.coords], "closed": False})
    return out


def _merged(g: BaseGeometry) -> BaseGeometry:
    lines = lines_of(g)
    return linemerge(lines) if len(lines) > 1 else (lines[0] if lines else g)


def _edge_paths(pp: Placed, narrow: str) -> list[PathOut]:
    """The outline's stretches in a narrow face's plane, the part on their left."""
    part = pp.part
    axis, sign = pp.frame[narrow]
    t, u, v = part["axes"]["t"], part["axes"]["u"], part["axes"]["v"]
    i = "xyz".index(axis)
    value = part["box"]["max"][i] if sign > 0 else part["box"]["min"][i]
    coord = 0 if axis == u else 1 if axis == v else None
    if coord is None or axis == t:
        return []
    ring = orient(pp.machine_outline(rules.BIG_HOLE_LIMIT, uv=True), 1.0).exterior
    pts = list(ring.coords)
    out: list[PathOut] = []
    current: list[Point2] = []
    for a, b in zip(pts, pts[1:]):
        on = abs(a[coord] - value) < 1e-6 and abs(b[coord] - value) < 1e-6
        if on:
            if not current:
                current = [pp.point(a[0], a[1])]
            current.append(pp.point(b[0], b[1]))
        elif current:
            out.append({"points": [_pt(p) for p in current], "closed": False})
            current = []
    if current:
        out.append({"points": [_pt(p) for p in current], "closed": False})
    if pp.mirrored:
        for p in out:
            p["points"].reverse()
    return out


def _arc(r: _Relief, material: BaseGeometry) -> list[list[float]]:
    """A dog bone's wall: its circle where it borders the material, from one
    end to the other."""
    circle = LineString(list(r.disc.exterior.coords)) if isinstance(r.disc, Polygon) else None
    if circle is None:
        return []
    wall = circle.intersection(material.buffer(1e-3))
    pieces = lines_of(_merged(wall))
    if not pieces:
        return [_pt(r.center)]
    longest = max(pieces, key=lambda line: line.length)
    coords = list(longest.coords)
    step = max(1, len(coords) // 8)
    picked = coords[::step] + ([coords[-1]] if (len(coords) - 1) % step else [])
    return [_pt((c[0], c[1])) for c in picked]


def _ring_start(ring: list[list[float]]) -> Point2:
    return (ring[0][0], ring[0][1])


def _names(refs: list[OpRef]) -> str:
    named = [r["name"] for r in refs if r["name"]]
    return named[0] if named else refs[0]["kind"] if refs else "it"


# -- what the layout says about the edges -------------------------------------------------------------

def _hidden(pp: Placed, boxes: list[tuple[str, Any]], frame: LayoutFrame) -> BaseGeometry | None:
    """The stretches of the part's outline against another part (a board, a
    lip, in a groove): narrow faces another part's box reaches across,
    over the part's thickness, on the blank."""
    part = pp.part
    t, u, v = part["axes"]["t"], part["axes"]["u"], part["axes"]["v"]
    it, iu, iv = ("xyz".index(t), "xyz".index(u), "xyz".index(v))
    lo, hi = part["box"]["min"], part["box"]["max"]
    lines: list[BaseGeometry] = []
    ring = orient(pp.machine_outline(rules.BIG_HOLE_LIMIT, uv=True), 1.0).exterior
    pts = list(ring.coords)
    for path, box in boxes:
        if path == part["path"]:
            continue
        blo, bhi = box["min"], box["max"]
        if blo[it] > hi[it] - 1e-6 or bhi[it] < lo[it] + 1e-6:
            continue
        for a, b in zip(pts, pts[1:]):
            for axis_index, coord, other in ((iu, 0, iv), (iv, 1, iu)):
                if abs(a[coord] - b[coord]) > 1e-9:
                    continue
                value = a[coord]
                on_hi, on_lo = abs(value - hi[axis_index]) < 1e-6, abs(value - lo[axis_index]) < 1e-6
                if on_hi and not (blo[axis_index] <= value + 1e-6 and bhi[axis_index] > value + 1e-6):
                    continue
                if on_lo and not (bhi[axis_index] >= value - 1e-6 and blo[axis_index] < value - 1e-6):
                    continue
                if not (on_hi or on_lo):
                    continue
                s0, s1 = sorted((a[1 - coord], b[1 - coord]))
                c0, c1 = max(s0, blo[other]), min(s1, bhi[other])
                if c1 - c0 > 1e-6:
                    p0 = (value, c0) if coord == 0 else (c0, value)
                    p1 = (value, c1) if coord == 0 else (c1, value)
                    lines.append(LineString([pp.point(*p0), pp.point(*p1)]))
    return unary_union(lines) if lines else None


def _chamfered(pp: Placed, frame: LayoutFrame) -> BaseGeometry | None:
    """The stretches of the part's outer contour under a chamfer, on the
    blank: a chamfer along the outline, along an edge of it, along a cut;
    a cut's chamfer."""
    part = pp.part
    named = named_ops(part)
    outline = pp.machine_outline(rules.BIG_HOLE_LIMIT)
    exterior = LineString(list(orient(outline, 1.0).exterior.coords))
    lines: list[BaseGeometry] = []
    for op in part["ops"]:
        if op["kind"] == "chamfer":
            if pp.face(op["face"]) == "narrow":
                continue
            target = chamfer_target(op, named, frame)
            if isinstance(target, OutlineTarget):
                lines.append(exterior)
            elif isinstance(target, EdgeTarget):
                narrow = target.a if pp.face(target.a) == "narrow" else target.b
                lines += [LineString(p["points"]) for p in _edge_paths(pp, narrow) if len(p["points"]) > 1]
            elif isinstance(target, OpTarget) and target.op["kind"] == "cut":
                lines.append(exterior.intersection(pp.region(target.op["shape"]).boundary.buffer(1e-6)))
        elif op["kind"] == "cut" and op["chamfer"] > 0:
            lines.append(exterior.intersection(pp.region(op["shape"]).boundary.buffer(1e-6)))
    lines = [g for g in lines if not g.is_empty]
    return unary_union(lines) if lines else None


def _thinned(pp: Placed, contour: LineString) -> BaseGeometry | None:
    """Where a pocket from either big face comes within `THIN_NEAR` of the
    contour: no tab near it."""
    near = contour.buffer(THIN_NEAR)
    zones: list[BaseGeometry] = []
    for op in pp.part["ops"]:
        if op["kind"] == "pocket" and pp.face(op["face"]) != "narrow" and not pp.is_through(op["depth"]):
            zone = pp.region(op["shape"]).intersection(near)
            if not zone.is_empty:
                zones.append(zone)
    return unary_union(zones) if zones else None


__all__ = ["plan_nest", "setup_name", "contours"]
