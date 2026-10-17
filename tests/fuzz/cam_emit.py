"""Random CAM plans mapped into the nested document (`lang.emit.cam_plan`),
checked from the outside. A case is plain data, so a failing example prints
as something to build again.

- `emit_plans`: random nests (one to three materials of any thickness, one
  to three pieces of stock each, of any size, with blanks anywhere on them)
  and plans of their blanks with features of every kind anywhere on them
  (contours, pockets blind and through, rests, holes, dog bones drilled or
  milled, chamfers along open and closed paths, V-grooves), in operations
  of the kinds that machine them, with random heights, depths, order, feed
  scales and tabs. Worked out here apart from the mapping: each setup's
  corner is its blank's on its sheet, the sheets one above the other `GAP`
  apart, its top the material's thickness; every point of every binding is
  the corner plus the plan's point, every height the top less the depth;
  the tab positions likewise, at the top; each operation writes each mode
  before its offset with the plan's values, no heights on a Trace, the
  depths and the stepdowns and the tabs only as the plan has them, after
  what enables them; and a plan with its version, nest, nest's time,
  layout's hash, a blank's place or a part changed is refused.
- `emit_nests`: `machining.py`'s random parts nested and planned, mapped:
  each setup is where `nested.plan_nest` draws its blank, every hole's
  cylinder and every V-groove's bottom is where the nested document draws
  that hole or groove, and every pocket's floor is as deep as a pocket or
  a hole drawn from the stock's top (the layout's steps moved by the nest's
  transform).
"""
from __future__ import annotations

import json
import math
from dataclasses import dataclass
from typing import Any

from hypothesis import strategies as st

from fuzzing import fresh
from lang import LangError
from lang.cam.plan import plan_nest as plan_cam_nest
from lang.core.layout import build_layout
from lang.emit import cam_plan
from lang.emit.cam_plan import (Cylinder, EdgeLine, EdgePath, FaceLoop, Floor, Region, Silhouette, WallArc,
                                param_writes, plan_cam)
from lang.emit.nested import GAP, apply, plan_nest
from lang.emit.plan import Circle, HoleStep, PocketStep, VGrooveStep, loop_points
from lang.nesting.nest import Options, nest_parts
from lang.nesting.workshop import Sheet, Workshop
from machining import BED, REGISTRY, PlanCase, _build  # pyright: ignore[reportPrivateUsage]
from nesting import MATERIALS, _in_frame  # pyright: ignore[reportPrivateUsage]

#: The kinds of feature each kind of operation machines.
MACHINES = {"contour": ("outer", "inner"), "release": ("outer", "inner"), "pocket": ("pocket", "through", "rest"),
            "drill": ("hole", "dogbone"), "bore": ("hole",), "dogbone": ("dogbone",), "chamfer": ("chamfer",),
            "groove": ("vgroove",)}
#: The height modes a plan may give per kind of operation.
MODES = {"drill": ("from stock top", "from stock bottom", "from hole bottom"),
         "bore": ("from stock top", "from stock bottom", "from hole bottom")}
OTHER_MODES = ("from stock top", "from stock bottom", "from contour")


@dataclass(frozen=True)
class EmitCase:
    """A nest file and a plan of it, as JSON."""
    nest: str
    plan: str


# -- synthetic plans --------------------------------------------------------------------------------------

@st.composite
def emit_plans(draw: st.DrawFn) -> EmitCase:
    coords = st.floats(-50.0, 2500.0, allow_nan=False, allow_infinity=False)
    materials: list[Any] = []
    setups: list[Any] = []
    for m in range(draw(st.integers(1, 3))):
        name, t = f"birch {m}", draw(st.sampled_from([4.0, 9.0, 12.0, 15.0, 18.0, 21.5]))
        sheets: list[Any] = []
        for s in range(draw(st.integers(1, 3))):
            size = [draw(st.floats(300.0, 3000.0)), draw(st.floats(200.0, 2000.0))]
            blanks: list[Any] = []
            for b in range(draw(st.integers(1, 3))):
                rect = [draw(st.floats(0.0, size[0] - 100.0)), draw(st.floats(0.0, size[1] - 100.0)),
                        draw(st.floats(50.0, 2000.0)), draw(st.floats(50.0, 1000.0))]
                parts = [f"m.p{m}_{s}_{b}_{k}" for k in range(draw(st.integers(1, 3)))]
                blank = {"name": f"{s + 1}.{b + 1}", "rect": rect, "own_blank": False,
                         "parts": [{"path": p} for p in parts]}
                blanks.append(blank)
                setups.append(_setup(draw, name, t, blank, parts, coords))
            sheets.append({"name": str(s + 1), "stock": "sheet", "size": size, "blanks": blanks})
        materials.append({"material": name, "thickness": t, "sheets": sheets})
    nest = {"version": 3, "name": "fuzz.birch", "written": "2026-10-17T12:00:00+02:00", "layout_hash": "abc",
            "materials": materials}
    plan = {"version": cam_plan.CAM_VERSION, "nest": "fuzz.birch", "nest_written": nest["written"],
            "layout_hash": "abc", "written": "2026-10-17T12:01:00+02:00",
            "settings": {"templates": "/nowhere", "values": {}}, "setups": setups, "problems": []}
    return EmitCase(json.dumps(nest), json.dumps(plan))


def _setup(draw: st.DrawFn, material: str, t: float, blank: Any, parts: list[str],
           coords: st.SearchStrategy[float]) -> Any:
    def pt() -> list[float]:
        return [draw(coords), draw(coords)]

    def ring() -> list[list[float]]:
        return [pt() for _ in range(draw(st.integers(3, 6)))]

    def depth() -> float:
        return draw(st.floats(0.1, t))

    def feature(what: str) -> Any:
        part = draw(st.sampled_from(parts))
        ops = [{"index": 0, "name": draw(st.sampled_from(["a", "b", None])), "kind": "pocket", "aspect": "op"}]
        f: Any = {"what": what, "part": part, "ops": ops}
        if what in ("outer", "inner"):
            f["ring"] = ring()
        elif what in ("pocket", "through", "rest"):
            f.update(what="rest" if what == "rest" else "pocket", rings=[ring() for _ in range(draw(st.integers(1, 3)))],
                     depth=None if what == "through" else depth(), slot=None)
        elif what == "hole":
            f.update(center=pt(), d=draw(st.floats(1.0, 30.0)), depth=draw(st.one_of(st.none(), st.floats(0.1, t))))
        elif what == "dogbone":
            f.update(center=pt(), d=draw(st.floats(2.0, 12.0)), tool=6.0, depth=draw(st.one_of(st.none(),
                     st.floats(0.1, t))), arc=[pt() for _ in range(draw(st.integers(2, 5)))])
        elif what == "chamfer":
            f.update(size=draw(st.floats(0.2, 3.0)), hole=None,
                     paths=[{"points": [pt() for _ in range(draw(st.integers(2, 5)))], "closed": draw(st.booleans())}
                            for _ in range(draw(st.integers(1, 3)))])
        else:
            f.update(start=pt(), end=pt(), depth=draw(st.floats(0.1, 3.0)))
        return f

    operations: list[Any] = []
    for _ in range(draw(st.integers(0, 6))):
        kind = draw(st.sampled_from(sorted(MACHINES)))
        modes = MODES.get(kind, OTHER_MODES)

        def height() -> Any:
            return {"mode": draw(st.sampled_from(modes)), "offset": draw(st.floats(-5.0, 5.0))}

        tabs = None
        if kind in ("contour", "release") and draw(st.booleans()):
            tabs = {"width": draw(st.floats(1.0, 10.0)), "height": draw(st.floats(0.5, 4.0)),
                    "positions": [pt() for _ in range(draw(st.integers(0, 6)))]}
        multiple = draw(st.one_of(st.none(), st.booleans()))
        operations.append({
            "name": f"op {len(operations)}", "kind": kind, "template": f"{kind}_X", "label": "X",
            "tool": {"type": "flat end mill", "diameter": draw(st.floats(1.0, 10.0)), "flute": None, "taper": None,
                     "tip": 0.0},
            "params": {"top": height(), "bottom": height(), "multiple_depths": multiple,
                       "stepdowns": draw(st.one_of(st.none(), st.integers(0, 4))),
                       "preserve_order": draw(st.booleans()),
                       "feed_scale": draw(st.one_of(st.none(), st.floats(0.5, 5.0))) if kind == "bore" else None,
                       "tabs": tabs},
            "features": [feature(draw(st.sampled_from(MACHINES[kind]))) for _ in range(draw(st.integers(0, 4)))]})
    stock = {"material": material, "sheet": blank["name"].split(".")[0], "blank": blank["name"],
             "rect": list(blank["rect"]), "thickness": t, "own_blank": False}
    return {"name": f"fuzz.birch {material} {blank['name']}", "stock": stock,
            "parts": [{"path": p, "hold": 0.0, "tab_policy": "auto", "tabs": 0} for p in parts],
            "operations": operations, "release_order": [], "left_out": [], "problems": []}


def _close(a: tuple[float, ...], b: tuple[float, ...] | list[float]) -> bool:
    return len(a) == len(b) and all(abs(x - y) <= 1e-9 * max(1.0, abs(x)) for x, y in zip(a, b))


def run_emit_plan(case: EmitCase) -> list[str]:
    nest, plan = json.loads(case.nest), json.loads(case.plan)
    problems: list[str] = []
    docs = plan_cam(plan, nest)
    # the blanks' corners, worked out apart from the mapping
    corners: dict[tuple[str, str], tuple[float, float, float, float, float, float]] = {}
    for m in nest["materials"]:
        y = 0.0
        for s in m["sheets"]:
            for b in s["blanks"]:
                x0, y0, w, h = b["rect"]
                corners[(m["material"], b["name"])] = (x0, y + y0, 0.0, w, h, m["thickness"])
            y += s["size"][1] + GAP
    if [d.material for d in docs] != [m["material"] for m in nest["materials"]]:
        problems.append("a document per material, in the nest's order: not so")
    mapped = [s for d in docs for s in d.setups]
    if [s.name for s in mapped] != [s["name"] for m in nest["materials"] for s in plan["setups"]
                                    if s["stock"]["material"] == m["material"]]:
        problems.append("the setups are not the plan's, per material")
    by_name = {s["name"]: s for s in plan["setups"]}
    for setup in mapped:
        x0, y0, z0, w, h, t = corners[(setup.material, setup.blank)]
        if not (_close(setup.corner, (x0, y0, z0)) and _close(setup.size, (w, h, t)) and setup.top == z0 + t):
            problems.append(f"setup {setup.name} at {setup.corner} {setup.size}, its blank at {(x0, y0, z0, w, h, t)}")
            continue
        raw = by_name[setup.name]
        for op, out in zip(raw["operations"], setup.operations):
            problems += _check_op(op, out, (x0, y0), t)
        want = []
        for op in raw["operations"]:
            for p in op["params"]["tabs"]["positions"] if op["params"]["tabs"] else []:
                q = (x0 + p[0], y0 + p[1], t)
                if q not in want:
                    want.append(q)
        if not all(_close(a, b) for a, b in zip(setup.tab_positions(), want)) or len(setup.tab_positions()) != len(want):
            problems.append(f"setup {setup.name}: tab positions not at the top where the plan has them")
    problems += _refusals(nest, plan)
    return problems


def _check_op(op: Any, out: cam_plan.OperationPlan, corner: tuple[float, float], t: float) -> list[str]:
    problems: list[str] = []
    x0, y0 = corner

    def at(p: list[float]) -> tuple[float, float]:
        return (x0 + p[0], y0 + p[1])

    def same(a: list[tuple[float, float]], b: list[list[float]]) -> bool:
        return len(a) == len(b) and all(_close(q, at(p)) for q, p in zip(a, b))

    if len(out.features) != len(op["features"]):
        problems.append(f"{op['name']}: {len(out.features)} features of {len(op['features'])}")
    for f, got in zip(op["features"], out.features):
        bs = got.bindings
        w = f["what"]
        ok = True
        if w == "outer":
            ok = len(bs) == 1 and isinstance(bs[0], Silhouette) and same(bs[0].ring, f["ring"])
        elif w == "inner":
            ok = len(bs) == 1 and isinstance(bs[0], FaceLoop) and same(bs[0].ring, f["ring"]) and \
                bs[0].levels == (t, 0.0)
        elif w == "pocket" and f["depth"] is None:
            ok = len(bs) == len(f["rings"]) and all(isinstance(b, FaceLoop) and same(b.ring, r)
                                                     for b, r in zip(bs, f["rings"]))
        elif w == "pocket":
            ok = len(bs) == 1 and isinstance(bs[0], Floor) and _close((bs[0].z,), (t - f["depth"],)) and \
                all(same(r, fr) for r, fr in zip(bs[0].rings, f["rings"]))
        elif w == "rest":
            z = 0.0 if f["depth"] is None else t - f["depth"]
            ok = len(bs) == 1 and isinstance(bs[0], Region) and _close((bs[0].z,), (z,)) and \
                len(bs[0].loops) == len(f["rings"]) and all(abs((c.center if isinstance(c, Circle) else c.a)[2] - z) < 1e-9
                                                             for loop in bs[0].loops for c in loop)
        elif w == "hole" or (w == "dogbone" and op["kind"] == "drill"):
            ok = len(bs) == 1 and isinstance(bs[0], Cylinder) and _close(bs[0].center, at(f["center"])) and \
                bs[0].d == f["d"]
        elif w == "dogbone":
            z = 0.0 if f["depth"] is None else t - f["depth"]
            ok = len(bs) == 1 and isinstance(bs[0], WallArc) and _close(bs[0].center, at(f["center"])) and \
                _close(bs[0].levels, (z, t)) and same(bs[0].arc, f["arc"])
        elif w == "chamfer":
            ok = len(bs) == len(f["paths"]) and all(
                isinstance(b, EdgePath) and same(b.points, p["points"]) and b.closed == p["closed"] and
                _close((b.z,), (t - f["size"],)) for b, p in zip(bs, f["paths"]))
        else:
            ok = len(bs) == 1 and isinstance(bs[0], EdgeLine) and _close(bs[0].start, at(f["start"])) and \
                _close(bs[0].end, at(f["end"])) and _close((bs[0].z,), (t - f["depth"],))
        if not ok:
            problems.append(f"{op['name']}: a {w} feature bound otherwise than where the plan has it")
    problems += _check_writes(op, out)
    return problems


def _check_writes(op: Any, out: cam_plan.OperationPlan) -> list[str]:
    problems: list[str] = []
    writes = param_writes(out)
    names = [n for n, _e in writes]
    values = dict(writes)
    p = op["params"]
    if len(set(names)) != len(names):
        problems.append(f"{op['name']}: a parameter written twice")
    for h in ("topHeight", "bottomHeight"):
        plan_h = p["top" if h == "topHeight" else "bottom"]
        if op["kind"] == "groove":
            if f"{h}_mode" in values:
                problems.append(f"{op['name']}: heights written on a Trace")
            continue
        if f"{h}_mode" not in values or names.index(f"{h}_mode") > names.index(f"{h}_offset"):
            problems.append(f"{op['name']}: {h}'s mode not written before its offset")
            continue
        offset = float(values[f"{h}_offset"].removesuffix(" mm"))
        if values[f"{h}_mode"] != f"'{plan_h['mode']}'" or abs(offset - plan_h["offset"]) > 1e-5 * max(1.0, abs(offset)):
            problems.append(f"{op['name']}: {h} written as {values[f'{h}_mode']} {values[f'{h}_offset']}, the plan "
                            f"says {plan_h}")
    if ("doMultipleDepths" in values) != (p["multiple_depths"] is not None) or \
            values.get("doMultipleDepths", "x") not in ("x", "true" if p["multiple_depths"] else "false"):
        problems.append(f"{op['name']}: the depths written otherwise than the plan has them")
    steps = p["stepdowns"] is not None and p["multiple_depths"] is not False
    if ("numberOfStepdowns" in values) != steps or (steps and values["numberOfStepdowns"] != str(p["stepdowns"])):
        problems.append(f"{op['name']}: the stepdowns written otherwise than the plan has them")
    if steps and "doMultipleDepths" in values and names.index("doMultipleDepths") > names.index("numberOfStepdowns"):
        problems.append(f"{op['name']}: the stepdowns written before the depths are on")
    if values.get("group_tabs") != ("true" if p["tabs"] else "false"):
        problems.append(f"{op['name']}: tabs written otherwise than the plan has them")
    if p["tabs"] and not all(names.index("group_tabs") < names.index(n) for n in ("tabWidth", "tabHeight",
                                                                                  "tabsPerContour")):
        problems.append(f"{op['name']}: a tab parameter written before the tabs are on")
    if op["kind"] != "bore" and op["kind"] != "drill" and values.get("preserveOrder") != (
            "true" if p["preserve_order"] else "false"):
        problems.append(f"{op['name']}: the order written otherwise than the plan has it")
    return problems


def _refusals(nest: Any, plan: Any) -> list[str]:
    problems: list[str] = []
    changes: list[tuple[str, Any]] = [("version", {**plan, "version": plan["version"] + 1}),
                                      ("nest", {**plan, "nest": plan["nest"] + "x"}),
                                      ("nest_written", {**plan, "nest_written": "2020"}),
                                      ("layout_hash", {**plan, "layout_hash": "def"})]
    if plan["setups"]:
        moved = json.loads(json.dumps(plan))
        moved["setups"][0]["stock"]["rect"][2] += 1.0
        changes.append(("a blank's place", moved))
        gone = json.loads(json.dumps(plan))
        gone["setups"][-1]["stock"]["blank"] = "99.99"
        changes.append(("a blank", gone))
        with_feature = [k for k, s in enumerate(plan["setups"]) if any(op["features"] for op in s["operations"])]
        if with_feature:
            stranger = json.loads(json.dumps(plan))
            op = next(op for op in stranger["setups"][with_feature[0]]["operations"] if op["features"])
            op["features"][0]["part"] = "m.nobody"
            changes.append(("a part", stranger))
    for what, changed in changes:
        try:
            plan_cam(changed, nest)
        except ValueError:
            continue
        problems.append(f"a plan with {what} changed was not refused")
    return problems


# -- real plans ------------------------------------------------------------------------------------------

def run_emit_nest(case: PlanCase) -> list[str]:
    with fresh():
        try:
            _in_frame(case.parts[0].frame)
            _build(case)
            layout = build_layout()
        except LangError:
            return []
        workshop = Workshop(bed=BED, sheets=tuple(Sheet(m.label, 2500.0, 1250.0) for m in MATERIALS))
        options = Options(seconds=0.2, saw_seconds=0.05, refill_seconds=0.0)
        try:
            nest, _parts = nest_parts(layout, None, workshop, name="fuzz", options=options)
        except LangError:
            return []
        plan = plan_cam_nest(nest, layout, registry=REGISTRY)
        return _against_document(plan, nest, layout)


def _against_document(plan: Any, nest: Any, layout: Any) -> list[str]:
    problems: list[str] = []
    drawn = {(d.material, b.name): b for d in plan_nest(nest, layout) for s in d.sheets for b in s.blanks}
    for doc in plan_cam(plan, nest):
        for setup in doc.setups:
            blank = drawn[(doc.material, setup.blank)]
            if not (_close(setup.corner, blank.origin) and _close(setup.size, blank.size)):
                problems.append(f"setup {setup.name} at {setup.corner}, its blank drawn at {blank.origin}")
                continue
            placed = {p.path: p for p in blank.parts}
            for op in setup.operations:
                for f in op.features:
                    for b in f.bindings:
                        if f.what == "hole" and isinstance(b, Cylinder):
                            if not _a_hole_there(placed[f.part], b):
                                problems.append(f"{f.label}: no hole {b.d:g} drawn at {b.center}")
                        elif isinstance(b, EdgeLine):
                            if not _a_groove_there(placed[f.part], b, setup.top):
                                problems.append(f"{f.label}: no V-groove drawn from {b.start} to {b.end}")
                        elif isinstance(b, Floor):
                            if not _a_floor_there(placed[f.part], b, setup.top):
                                problems.append(f"{f.label}: no pocket or hole drawn down to {b.z:g}")
    return problems


def _a_floor_there(placed: Any, b: Floor, top: float) -> bool:
    """Whether a pocket or a hole is drawn from the stock's top down to the floor."""
    for step in placed.part.steps:
        if isinstance(step, (PocketStep, HoleStep)) and step.depth is not None and abs(top - step.depth - b.z) < 1e-6:
            points = step.points if isinstance(step, HoleStep) else loop_points(step.shapes[0][0]) or \
                [getattr(step.shapes[0][0][0], "center")]
            if all(abs(apply(placed.transform, q)[2] - top) < 1e-6 for q in points):
                return True
    return False


def _a_hole_there(placed: Any, b: Cylinder) -> bool:
    for step in placed.part.steps:
        if isinstance(step, HoleStep) and abs(step.d - b.d) < 1e-9:
            for p in step.points:
                q = apply(placed.transform, p)
                if math.dist((q[0], q[1]), b.center) < 1e-6:
                    return True
    return False


def _a_groove_there(placed: Any, b: EdgeLine, top: float) -> bool:
    for step in placed.part.steps:
        if isinstance(step, VGrooveStep):
            s, e = apply(placed.transform, step.start), apply(placed.transform, step.end)
            if math.dist(s[:2], b.start) < 1e-6 and math.dist(e[:2], b.end) < 1e-6 and \
                    abs(top - step.depth - b.z) < 1e-6 and abs(s[2] - top) < 1e-6:
                return True
    return False
