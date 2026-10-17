"""Random CAM plans as the preview's nest view shows them
(`lang/preview/viewer/cam.js`), checked from the outside. A case is
`machining.py`'s (plain data), so a failing example prints as something to
build again.

- `plan_views`: `machining.py`'s random nests, planned, drawn as the nest
  step draws them (`lang.nesting.draw`), and read by the view's own code in
  node (`plan_view.mjs`, given the sheets' places and the parts' names as
  the page reads them from the drawing). Its legend lists the setups in the
  plan's order, each with its operations in the order they run, their
  features and tabs counted; every setup finds its sheet in the drawing;
  the highlight of an operation draws each of its features as its kind
  says (a pocket or a rest a region of its rings, a contour a closed
  outline, a hole a circle of its radius, a dog bone a circle and its wall,
  a chamfer its paths, a V-groove a line), every point where the setup's
  frame puts it on the drawing, all but a V-groove's on its blank, and all
  of the setup's operations at once draw as many; each part's outer
  contour is the part the drawing draws, but for what the plan bores or
  pockets (a through hole across the part's edge is a notch in the
  drawing and a hole beside a straight contour in the plan); the parts are numbered 1 up
  by where their outer contour comes in the release order, an own blank's
  not, and each part's name gets its number, hold and tabs; the tab marks
  are the operations' tab positions, once each; a choice outside the
  setup's operations is none; the notes list every problem and every
  operation left out but those in a narrow face, which they never name.
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import xml.etree.ElementTree as ET
from collections.abc import Callable
from pathlib import Path
from typing import Any

from shapely import Point as ShapelyPoint, Polygon, box
from shapely.ops import unary_union

from lang.cam.plan_types import CamFile, SetupOut
from lang.nesting.draw import draw_nest
from machining import PlanCase, planned

NODE = shutil.which("node")
DRIVER = Path(__file__).with_name("plan_view.mjs")
SVG = "{http://www.w3.org/2000/svg}"
#: The page writes the drawing's coordinates to a hundredth, the drawing its own to a tenth.
ROUNDING = 0.006
DRAWN = 0.1


def run_view(case: PlanCase) -> list[str]:
    done = planned(case)
    if done is None:
        return []
    sheets, labels, drawn = _read_drawing(draw_nest(done.nest, done.items))
    view = view_of(done.plan, sheets, labels)
    return _check(done.plan, view, sheets, drawn)


def view_of(plan: CamFile, sheets: dict[str, dict[str, float]], labels: dict[str, dict[str, float]]) -> dict[str, Any]:
    """What the page lists and draws of `plan` (`plan_view.mjs`)."""
    assert NODE is not None, "node is not on PATH"
    result = subprocess.run([NODE, str(DRIVER)], input=json.dumps({"plan": plan, "sheets": sheets, "labels": labels}),
                            capture_output=True, text=True, timeout=60)
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout)


def _read_drawing(svg: str) -> tuple[dict[str, dict[str, float]], dict[str, dict[str, float]], dict[str, list[list[float]]]]:
    """As the page reads the drawing: per "<material>\\n<sheet>" its sheet's
    rect, per part its name's place, and per part its outline's outer ring
    as drawn."""
    root = ET.fromstring(svg)
    sheets: dict[str, dict[str, float]] = {}
    labels: dict[str, dict[str, float]] = {}
    drawn: dict[str, list[list[float]]] = {}
    for g in root.iter(SVG + "g"):
        if g.get("class") == "stock":
            rect = next(r for r in g.iter(SVG + "rect") if r.get("class") == "sheet")
            sheets[f"{g.get('data-material')}\n{g.get('data-sheet')}"] = {
                "x": float(rect.get("x", 0)), "y": float(rect.get("y", 0)), "height": float(rect.get("height", 0))}
        elif g.get("class") == "part":
            path, text, outline = g.get("data-path", ""), g.find(SVG + "text"), g.find(SVG + "path")
            assert text is not None and outline is not None
            labels[path] = {"x": float(text.get("x", 0)), "y": float(text.get("y", 0)),
                            "size": float(text.get("font-size", 0))}
            first = outline.get("d", "").split("Z")[0]
            drawn[path] = [[float(a), float(b)] for a, b in re.findall(r"(-?[\d.]+) (-?[\d.]+)", first)]
    return sheets, labels, drawn


def _check(plan: CamFile, view: dict[str, Any], sheets: dict[str, dict[str, float]],
           drawn: dict[str, list[list[float]]]) -> list[str]:
    problems: list[str] = []
    legend = view["legend"]
    if [e["setup"] for e in legend] != [s["name"] for s in plan["setups"]]:
        problems.append("the legend's setups are not the plan's, in its order")
    colors = dict(view["colors"])
    for setup, entry, seen in zip(plan["setups"], legend, view["setups"]):
        name = setup["name"]
        listed = [(o["index"], o["name"], o["kind"], o["features"], o["tabs"]) for o in entry["operations"]]
        wanted = [(k, op["name"], op["kind"], len(op["features"]),
                   len(op["params"]["tabs"]["positions"]) if op["params"]["tabs"] else 0)
                  for k, op in enumerate(setup["operations"])]
        if listed != wanted:
            problems.append(f"the legend of {name} lists other operations than the plan's, in its order")
        if any(o["color"] != colors.get(o["tool"]) for o in entry["operations"]):
            problems.append(f"an operation of {name} is not in its tool's colour")
        n = len(setup["operations"])
        if [c and c["index"] for c in seen["choices"]] != [None, *range(n), None, "all"]:
            problems.append(f"the choices of {name}'s operations are not its operations: {seen['choices']}")
        # the release order: 1 up, by the outer contour's place
        ranks: dict[str, int] = {}
        for r in setup["release_order"]:
            if r["what"] == "outer" and r["part"] not in ranks:
                ranks[r["part"]] = len(ranks) + 1
        if dict(seen["ranks"]) != ranks:
            problems.append(f"the parts of {name} are not numbered by their release")
        if setup["stock"]["own_blank"] and ranks:
            problems.append(f"an own blank's part has a release ({name})")
        tabs = {(round(p[0], 3), round(p[1], 3)) for op in setup["operations"] if op["params"]["tabs"]
                for p in op["params"]["tabs"]["positions"]}
        if {(round(p[0], 3), round(p[1], 3)) for p in seen["tabs"]} != tabs or len(seen["tabs"]) != len(tabs):
            problems.append(f"the tab marks of {name} are not its operations' tabs, once each")
        if not seen["sheet"]:
            problems.append(f"{name} finds no sheet in the drawing ({setup['stock']['material']} {setup['stock']['sheet']})")
            continue
        sheet = sheets[f"{setup['stock']['material']}\n{setup['stock']['sheet']}"]
        problems += _check_plain(setup, seen["plain"], ranks, sheet)
        for k, (op, elements) in enumerate(zip(setup["operations"], seen["ops"])):
            problems += [f"{name} op {k} ({op['kind']}): {p}" for p in _check_op(setup, op["features"], elements, sheet)]
        if seen["all"] != sum(len(e) for e in seen["ops"]):
            problems.append(f"all of {name}'s operations draw other than each of them")
        problems += _check_outer(setup, sheet, drawn)
    notes = view["notes"]
    for problem in plan["problems"]:
        own = problem.split(": ", 1)[1] if any(problem.startswith(s["name"] + ": ") for s in plan["setups"]) else problem
        if own not in notes:
            problems.append(f"the notes do not list the problem {problem!r}")
    for setup in plan["setups"]:
        for left in setup["left_out"]:
            if left["why"] != "narrow face" and f"left out: {left['part']} " not in notes:
                problems.append(f"the notes do not list what is left out of {left['part']}")
    if "narrow face" in notes:
        problems.append("the notes list what is in a narrow face")
    return problems


def _to_drawing(sheet: dict[str, float], setup: SetupOut) -> Callable[[list[float]], tuple[float, float]]:
    rx, ry = setup["stock"]["rect"][0], setup["stock"]["rect"][1]
    return lambda p: (sheet["x"] + rx + p[0], sheet["y"] + sheet["height"] - (ry + p[1]))


def _check_plain(setup: SetupOut, elements: list[dict[str, Any]], ranks: dict[str, int],
                 sheet: dict[str, float]) -> list[str]:
    problems: list[str] = []
    at = _to_drawing(sheet, setup)
    marks = [e for e in elements if e["attrs"]["class"] == "cam-tab"]
    positions = {(round(p[0], 3), round(p[1], 3)) for op in setup["operations"] if op["params"]["tabs"]
                 for p in op["params"]["tabs"]["positions"]}
    want = sorted((round(at([*p])[0], 2), round(at([*p])[1], 2)) for p in positions)
    got = sorted((round(e["attrs"]["cx"], 2), round(e["attrs"]["cy"], 2)) for e in marks)
    if len(want) != len(got) or any(abs(a - c) > 0.011 or abs(b - d) > 0.011 for (a, b), (c, d) in zip(want, got)):
        problems.append(f"the tab marks of {setup['name']} are not where its tabs are")
    texts = {e["attrs"]["data-path"]: e["text"] for e in elements if e["attrs"]["class"] == "cam-release"}
    for part in setup["parts"]:
        text = texts.get(part["path"])
        if text is None:
            problems.append(f"{part['path']} has no release label")
            continue
        rank = ranks.get(part["path"])
        if (rank is not None) != text.startswith(f"{rank}. ") or ("tabs" in text) != (part["tabs"] > 0):
            problems.append(f"{part['path']}'s label says other than its release and tabs: {text!r}")
    return problems


def _check_op(setup: SetupOut, features: list[Any], elements: list[dict[str, Any]],
              sheet: dict[str, float]) -> list[str]:
    """Each feature's elements, in order, where the setup's frame puts it."""
    at = _to_drawing(sheet, setup)
    x, y, w, h = setup["stock"]["rect"]
    blank = box(sheet["x"] + x, sheet["y"] + sheet["height"] - y - h, sheet["x"] + x + w, sheet["y"] + sheet["height"] - y)
    problems: list[str] = []
    k = 0

    def take(tag: str, cls: str) -> dict[str, Any] | None:
        nonlocal k
        if k >= len(elements) or elements[k]["tag"] != tag or cls not in elements[k]["attrs"]["class"].split():
            return None
        k += 1
        return elements[k - 1]

    def same(points: list[list[float]], d: str, closed: bool) -> bool:
        rings = [r for r in re.split(r"(?=M )", d) if r.strip()]
        got = [[[float(a), float(b)] for a, b in re.findall(r"(-?[\d.]+) (-?[\d.]+)", r)] for r in rings]
        if len(got) != 1 or got[0] and (rings[0].rstrip().endswith("Z") != closed):
            return False
        return len(got[0]) == len(points) and all(
            abs(a - c) < ROUNDING and abs(b - e) < ROUNDING for (a, b), (c, e) in zip(map(at, points), got[0]))

    def circle(center: list[float], r: float, cls: str) -> bool:
        main, halo = take("circle", cls), take("circle", "halo")
        if main is None or halo is None:
            return False
        cx, cy = at(center)
        return (abs(main["attrs"]["cx"] - cx) < ROUNDING and abs(main["attrs"]["cy"] - cy) < ROUNDING
                and abs(main["attrs"]["r"] - r) < ROUNDING and halo["attrs"]["r"] > main["attrs"]["r"])

    def on_blank(points: list[list[float]]) -> bool:
        return all(blank.buffer(0.01).covers(ShapelyPoint(*at(p))) for p in points)

    for f in features:
        cls = f"cam-{f['what']}"
        ok, points = True, []
        if f["what"] in ("outer", "inner"):
            e = take("path", cls)
            ok = e is not None and e["attrs"]["fill"] == "none" and same(f["ring"], e["attrs"]["d"], True)
            points = f["ring"]
        elif f["what"] in ("pocket", "rest"):
            e = take("path", cls)
            ok = e is not None and e["attrs"]["fill"] != "none"
            if e is not None:
                rings = [r for r in re.split(r"(?=M )", e["attrs"]["d"]) if r.strip()]
                ok = ok and len(rings) == len(f["rings"]) and all(same(ring, r, True) for ring, r in zip(f["rings"], rings))
            points = [p for ring in f["rings"] for p in ring]
        elif f["what"] == "hole":
            ok = circle(f["center"], f["d"] / 2, cls)
            points = [f["center"]]
        elif f["what"] == "dogbone":
            ok = circle(f["center"], f["d"] / 2, cls)
            if len(f["arc"]) > 1:
                e = take("path", cls)
                ok = ok and e is not None and same(f["arc"], e["attrs"]["d"], False)
            points = [f["center"]]
        elif f["what"] == "chamfer":
            for path in f["paths"]:
                e = take("path", cls)
                ok = ok and e is not None and same(path["points"], e["attrs"]["d"], path["closed"])
            if not f["paths"] and f["hole"] is not None:
                ok = circle(f["hole"]["center"], f["hole"]["d"] / 2, cls)
            points = [p for path in f["paths"] for p in path["points"]]
        else:                                       # a V-groove may run off its blank
            e = take("path", cls)
            ok = e is not None and same([f["start"], f["end"]], e["attrs"]["d"], False)
        if not ok:
            problems.append(f"a {f['what']} of {f['part']} is not drawn as its kind says, where it is")
        elif not on_blank(points):
            problems.append(f"a {f['what']} of {f['part']} is drawn off its blank")
    if k != len(elements):
        problems.append(f"{len(elements) - k} elements drawn for no feature")
    return problems


def _check_outer(setup: SetupOut, sheet: dict[str, float], drawn: dict[str, list[list[float]]]) -> list[str]:
    """Each part's outer contour on the part as the drawing draws it: where
    they differ, the plan bores or pockets what the drawing leaves out of
    the outline (a through hole across the part's edge, which the nest
    draws as a notch and the plan bores beside a straight contour)."""
    at = _to_drawing(sheet, setup)
    problems: list[str] = []
    taken: dict[str, list[Polygon]] = {}
    outer: dict[str, list[list[float]]] = {}
    for op in setup["operations"]:
        f: Any
        for f in op["features"]:
            if f["what"] == "outer":
                outer.setdefault(f["part"], f["ring"])
            elif f["what"] == "hole":
                taken.setdefault(f["part"], []).append(ShapelyPoint(*at(f["center"])).buffer(f["d"] / 2, 64))
            elif f["what"] in ("pocket", "rest"):
                rings = [[at(p) for p in ring] for ring in f["rings"]]
                taken.setdefault(f["part"], []).append(Polygon(rings[0], rings[1:]))
    for part, ring in outer.items():
        outline = drawn.get(part)
        if outline is None or len(outline) < 3:
            problems.append(f"{part} is not in the drawing")
            continue
        contour, shown = Polygon([at(p) for p in ring]), Polygon(outline)
        differ = contour.symmetric_difference(shown).difference(unary_union(taken.get(part, [])).buffer(DRAWN))
        if not differ.buffer(-DRAWN).is_empty:
            problems.append(f"{part}'s outer contour is not the part drawn, but for what the plan bores or pockets "
                            f"({differ.area:.1f} mm² apart)")
    return problems
