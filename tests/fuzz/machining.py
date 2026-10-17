"""Random nests planned for the machine (`lang.cam`), checked from the
outside. A case is plain data (frozen dataclasses), so a failing example
prints as something to build again.

- `plans`: a few of `nesting.py`'s parts (a board lying or standing on any
  side of its module, in any of the 48 world frames, with `boards.py`'s
  holes, pockets, slots, cuts, notches, V-grooves, holes into narrow faces
  and rounded corners, a big opening, a grain, `machine()` naming either
  face, `nest(False)` ones named in the nest now and then as their own
  blanks), some with dog bones (`dogbones()`) and a chamfer along their
  machining face's outline, some with `cam.tabs` of their own, a cutter,
  finishing, a tab margin and a waste area used at the root; nested on a
  bed with sheets to buy, with short times, and planned. The plan's own
  check (`verify`) must find nothing; and, worked out here apart from the
  plan: an operation of the part's other big face (not through it) is left
  out as such, one in a narrow face as that; the outer contour of each part
  is its outline less its openings where the nest's transform puts it; each
  hole lies where the transform puts it; a part has tabs exactly when its
  footprint shrunk by the margin keeps less than 10 cm² or it says
  `forced` (unless the plan says it found no room for them), none when it
  says `none`; the plan survives JSON.
"""
from __future__ import annotations

import json
from dataclasses import dataclass

from hypothesis import strategies as st
from shapely import normalize
from shapely.geometry import Point, Polygon
from shapely.ops import unary_union

from fuzzing import fresh, sizes
from lang import Board, LangError, cam, use
from lang.cam.plan import plan_nest
from lang.cam.plan_types import CamFile
from lang.cam.resolve import REPO
from lang.cam.tooling import scan
from lang.cam.verify import verify
from lang.core.layout import build_layout
from lang.core.layout_types import Layout, PartLayout
from lang.emit.nested import apply as apply_matrix
from lang.nesting.nest import Options, nest_parts
from lang.nesting.nest_types import NestFile, PlacedPart
from lang.nesting.workshop import Sheet, Workshop
from nesting import MATERIALS, PartCase, _in_frame, build_part, part_cases  # pyright: ignore[reportPrivateUsage]

REGISTRY = scan(REPO / "addins-src" / "auto_setup" / "templates")
BED = (2000.0, 1000.0)


@dataclass(frozen=True)
class PlanCase:
    parts: tuple[PartCase, ...]
    #: Per part: dog bones after its operations, a chamfer along its
    #: machining face's outline (0: none), its `cam.tabs` ("" for none given).
    dogbones: tuple[bool, ...]
    chamfer: tuple[float, ...]
    tabs: tuple[str, ...]
    cutter: str = "dc"
    finish: tuple[bool, bool, bool] = (False, False, False)
    tab_margin: float = 6.0
    waste_area: float = 10.0
    #: Whether the nest names its parts, so its `nest(False)` ones are their own blanks.
    named: bool = False


@st.composite
def plan_cases(draw: st.DrawFn) -> PlanCase:
    small, large = part_cases(BED[0] * 0.3, BED[1] * 0.3), part_cases(BED[0] * 0.9, BED[1] * 0.9)
    frame = draw(st.one_of(st.just(0), st.integers(0, 47)))
    parts = draw(st.lists(st.one_of(small, small, large), min_size=1, max_size=5))
    parts = [PartCase(p.material, p.side, p.size, p.origin, frame, p.features, p.opening, p.grain, p.machined,
                      p.nested, p.machine) for p in parts]
    n = len(parts)
    return PlanCase(tuple(parts), tuple(draw(st.lists(st.booleans(), min_size=n, max_size=n))),
                    tuple(draw(st.lists(st.sampled_from([0.0, 0.0, 1.0, 2.0]), min_size=n, max_size=n))),
                    tuple(draw(st.lists(st.sampled_from(["", "", "auto", "none", "forced"]), min_size=n, max_size=n))),
                    draw(st.sampled_from(["dc", "udc"])), (draw(st.booleans()), draw(st.booleans()), draw(st.booleans())),
                    draw(st.sampled_from([6.0, 6.0, 3.0, 12.0])), draw(st.sampled_from([10.0, 10.0, 0.0, 40.0])),
                    draw(st.booleans()))


def _build(case: PlanCase) -> list[Board]:
    use(cam.cutter(case.cutter), cam.finish_outer(case.finish[0]), cam.finish_inner(case.finish[1]),  # pyright: ignore[reportArgumentType]
        cam.finish_pockets(case.finish[2]), cam.tab_margin(case.tab_margin), cam.waste_area(case.waste_area))
    boards: list[Board] = []
    for k, part in enumerate(case.parts):
        b = build_part(part, f"p{k}")
        if case.dogbones[k]:
            try:
                b.dogbones()
            except LangError:
                pass
        if case.chamfer[k]:
            try:
                b.chamfer(b.machine_face.outline, case.chamfer[k])
            except LangError:
                pass
        if case.tabs[k]:
            b.use(cam.tabs(case.tabs[k]))  # pyright: ignore[reportArgumentType]
        boards.append(b)
    return boards


def run_plan(case: PlanCase) -> list[str]:
    with fresh():
        try:
            _in_frame(case.parts[0].frame)
            boards = _build(case)
            layout = build_layout()
        except LangError:
            return []
        workshop = Workshop(bed=BED, sheets=tuple(Sheet(m.label, 2500.0, 1250.0) for m in MATERIALS))
        options = Options(seconds=0.2, saw_seconds=0.05, refill_seconds=0.0)
        paths = [b.path for b in boards] if case.named else None
        try:
            nest, _parts = nest_parts(layout, paths, workshop, name="fuzz", options=options)
        except LangError:
            return []                    # what the nest refuses is the nest's fuzz test's
        plan = plan_nest(nest, layout, registry=REGISTRY)
        problems = [f"the plan's check: {p}" for p in verify(plan, nest, layout, REGISTRY)]
        problems += _outside(plan, nest, layout, case)
        if json.loads(json.dumps(plan)) != plan:
            problems.append("the plan does not survive JSON")
        return problems


def _outside(plan: CamFile, nest: NestFile, layout: Layout, case: PlanCase) -> list[str]:
    problems: list[str] = []
    parts = {p["path"]: p for m in layout["modules"] for p in m["parts"]}
    frame = layout["frame"]
    policy = {f"p{k}.b": t or "auto" for k, t in enumerate(case.tabs)}
    blanks = [b for m in nest["materials"] for s in m["sheets"] for b in s["blanks"]]
    for blank, setup in zip(blanks, plan["setups"]):
        own = blank["own_blank"]
        for placed in blank["parts"]:
            part = parts[placed["path"]]
            path = part["path"]
            left = {(lo["op"]["index"], lo["op"]["aspect"]): lo["why"] for lo in setup["left_out"]
                    if lo["part"] == path}
            t = part["axes"]["t"]
            for k, op in enumerate(part["ops"]):
                if op["kind"] == "edge":
                    if left.get((k, "op")) != "narrow face":
                        problems.append(f"an operation in a narrow face is not left out as such ({path} {k})")
                    continue
                if op["kind"] == "cut":
                    continue
                face = op["face"]
                other = frame[face][1] == t and face != part["machine"]
                if op["kind"] == "hole":
                    through = op["through"] or op["depth"] >= part["thickness"] - 1e-6
                elif op["kind"] == "pocket":
                    through = op["depth"] >= part["thickness"] - 1e-6
                else:
                    through = False
                if other and not through and left.get((k, "op")) != "other face":
                    problems.append(f"an operation of the other big face is not left out as such ({path} {k})")
                if not other and left.get((k, "op")) in ("other face", "narrow face"):
                    problems.append(f"an operation of the machining face is left out as another's ({path} {k})")
            features = [f for op in setup["operations"] if op["kind"] != "release" for f in op["features"]
                        if f["part"] == path]
            # the outer contour where the nest's transform puts the outline
            outer = [f for f in features if f["what"] == "outer"]
            if not own:
                want = _outline_on_blank(part, placed, frame)
                if len(outer) != 1 or want is None:
                    problems.append(f"{len(outer)} outer contours of a part ({path})")
                else:
                    got = Polygon(outer[0]["ring"])
                    if got.symmetric_difference(want).area > 1e-3 * max(1.0, want.length):
                        problems.append(f"an outer contour is not the outline where the nest puts it ({path})")
            elif outer:
                problems.append(f"an own blank's outline is planned ({path})")
            # the holes where the transform puts them
            for f in features:
                if f["what"] != "hole":
                    continue
                for r in f["ops"]:
                    op = part["ops"][r["index"]]
                    if op["kind"] != "hole":
                        continue
                    x, y = _on_blank(part, placed, frame, op["u"], op["v"])
                    if abs(x - f["center"][0]) > 1e-6 or abs(y - f["center"][1]) > 1e-6:
                        problems.append(f"a hole is not where the nest puts it ({path})")
            # the tabs
            held = next(p for p in setup["parts"] if p["path"] == path)
            excused = any(path in p and "tab(s) of the" in p for p in setup["problems"])
            want_tabs = not own and (policy.get(path, "auto") == "forced" or (
                policy.get(path, "auto") == "auto" and _needs_tabs(part, frame, case.tab_margin)))
            if want_tabs and held["tabs"] == 0 and not excused:
                problems.append(f"a part that holds too little has no tabs ({path}, {held['hold']:g} cm²)")
            if not want_tabs and held["tabs"]:
                problems.append(f"a part that holds enough has tabs ({path}, {held['hold']:g} cm², "
                                f"{policy.get(path)})")
    return problems


def _on_blank(part: PartLayout, placed: PlacedPart, frame: dict[str, str], u: float, v: float) -> tuple[float, float]:
    axes = part["axes"]
    p = [0.0, 0.0, 0.0]
    p["xyz".index(axes["u"])], p["xyz".index(axes["v"])] = u, v
    i = "xyz".index(axes["t"])
    sign = 1 if frame[part["machine"]][0] == "+" else -1
    p[i] = part["box"]["max"][i] if sign > 0 else part["box"]["min"][i]
    x, y, _z = apply_matrix(placed["transform"], (p[0], p[1], p[2]))
    return x, y


def _footprint(part: PartLayout, frame: dict[str, str], big_holes_only: bool) -> Polygon | None:
    """The outline less its through pockets and holes (only the wide ones
    with `big_holes_only`), in the part's frame."""
    from lang.cam.regions import polygons
    shape = unary_union(polygons(part["outline"]))
    t = part["axes"]["t"]
    for op in part["ops"]:
        if op["kind"] == "pocket" and frame[op["face"]][1] == t and op["depth"] >= part["thickness"] - 1e-6:
            shape = shape.difference(unary_union(polygons(op["shape"])))
        elif op["kind"] == "hole" and frame[op["face"]][1] == t and \
                (op["through"] or op["depth"] >= part["thickness"] - 1e-6) and (op["d"] > 30 or not big_holes_only):
            shape = shape.difference(Point(op["u"], op["v"]).buffer(op["d"] / 2, quad_segs=90))
    pieces = [g for g in getattr(shape, "geoms", [shape]) if isinstance(g, Polygon) and g.area > 1e-6]
    return max(pieces, key=lambda g: g.area) if pieces else None


def _outline_on_blank(part: PartLayout, placed: PlacedPart, frame: dict[str, str]) -> Polygon | None:
    shape = _footprint(part, frame, big_holes_only=True)
    if shape is None:
        return None
    return Polygon([_on_blank(part, placed, frame, x, y) for x, y in list(shape.exterior.coords)[:-1]])


def _needs_tabs(part: PartLayout, frame: dict[str, str], margin: float) -> bool:
    shape = _footprint(part, frame, big_holes_only=False)
    if shape is None:
        return False
    held = normalize(shape).buffer(-margin, quad_segs=32)
    return held.is_empty or held.area < 1000.0 - 1e-6


__all__ = ["PlanCase", "plan_cases", "run_plan", "sizes"]
