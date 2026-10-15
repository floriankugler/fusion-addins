"""Lift-up hatch hinges (lang/hardware/hatch_hinges.py) against the
hatch_hinge add-in: the positions are worked out by hand from the add-in's
code and the Free space 1.11 data (lib/hatch_hinges.py), the checks are
the add-in's."""
from pathlib import Path
from typing import Any

import pytest

from lang import *
from lang.build import run_build
from lang.core.checks import _has_material  # type: ignore[reportPrivateUsage]
from lang.core.layout import build_layout
from lang.core.layout_types import HardwareBodyLayout, HardwareLayout
from lang.core.ops import Hole
from lang.core.scope import registry
from lang.emit.plan import FaceRef, HoleStep, plan_layout
from lang.hardware.hatch_hinges import HINGE_SHAPES, HatchHinge, HatchHingeModel, HingeBox
from lib.hatch_hinges import FREE_SPACE_1_11
from helpers import bounds, ply18


#: The test cabinet in world terms: 320 deep (x 0..320, the front at -x),
#: 600 wide (y 0..600) and 350 high, an 18 mm hatch over its front.
BOX = Box.from_size(width=600, depth=320, height=350)


def _cabinet(hinge: HatchHinge | None = None, *, frame: str = "cabinet", hatch_t: float = 18,
             top_t: float = 18, hatch_drop: float = 0.0, gap: float = 0.0, right_set_back: float = 0.0,
             shelf_at: float | None = None, height: float = 350, mount: bool = True,
             **options: object) -> tuple[Scope, dict[str, Board]]:
    """The test cabinet: two 18 mm sides and a top and a bottom between
    them behind the hatch, the hatch's inner face `gap` in front of the
    carcass, its top `hatch_drop` below the carcass top. `frame` is
    "cabinet" (front=box.front), "van" (no front=, the van's terms) or
    "mirrored"; `options` replace the mount's."""
    box = Box.from_size(width=600, depth=320, height=height)
    hinge = hinge or HatchHinge("Free space 1.11")
    if frame == "van":
        cab = module("cab", box)
    else:
        cab = cabinet("cab", box, front=box.front, mirrored=frame == "mirrored")
    with cab:
        carcass = cab.front.into(hatch_t + gap)
        left = board("left", ply18).on(cab.left).between(carcass, cab.back)
        right = board("right", ply18).on(cab.right).between(cab.front.into(hatch_t + gap + right_set_back), cab.back)
        top = board("top", sheet_material("birch", t=top_t)).on(cab.top).between(left, right, carcass, cab.back)
        bottom = board("bottom", ply18).on(cab.bottom).between(left, right, carcass, cab.back)
        hatch = (board("hatch", sheet_material("birch", t=hatch_t)).on(cab.front)
                 .between(cab.left, cab.right, cab.bottom, cab.top.into(hatch_drop)))
        parts = {"left": left, "right": right, "top": top, "bottom": bottom, "hatch": hatch}
        if shelf_at is not None:
            parts["shelf"] = (board("shelf", ply18).on(Pos("z", shelf_at), toward=cab.top)
                              .between(left, right, carcass, cab.back))
        if mount:
            mount_options: dict[str, Any] = {"hatch": hatch, "sides": (left, right), "top": top}
            mount_options.update(options)
            cab.mount(hinge, **mount_options)
    return cab, parts


def _holes(part: Board) -> list[Hole]:
    return [op for op in part.ops if isinstance(op, Hole)]


#: The Free space 1.11's boxes. The tests read their numbers from the table
#: (HINGE_SHAPES), so measured extents can replace it without touching them.
SHAPE = HINGE_SHAPES[FREE_SPACE_1_11.name]
#: (world axis index, start, sign) of one of a hinge box's directions.
Along = tuple[int, float, int]


def _world(box: HingeBox, inward: Along, back: Along, down: Along) -> list[list[float]]:
    """A hinge box in world coordinates, min then max corner, rounded."""
    lo, hi = [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]
    for (axis, start, sign), (a, b) in zip((inward, back, down), box):
        lo[axis], hi[axis] = sorted((start + sign * a, start + sign * b))
    return [[round(c, 6) for c in lo], [round(c, 6) for c in hi]]


def _expected(inward: Along, back: Along, down: Along, gap: float = 0.0) -> list[list[list[float]]]:
    return [_world(box, inward, back, down) for box in SHAPE.boxes(gap).values()]


def _drawn(body: HardwareBodyLayout) -> list[list[list[float]]]:
    return [[[round(c, 6) for c in b["min"]], [round(c, 6) for c in b["max"]]] for b in body["boxes"]]


def _union(boxes: list[list[list[float]]]) -> list[list[float]]:
    return [[min(b[0][i] for b in boxes) for i in range(3)], [max(b[1][i] for b in boxes) for i in range(3)]]


#: In the test cabinet: back is +x from the carcass front at 18, down is -z
#: from the top's underside at 332; the left side panel's inner face at y
#: 582 points -y, the right one's at 18 points +y.
BACK, DOWN = (0, 18.0, 1), (2, 332.0, -1)
LEFT_INWARD, RIGHT_INWARD = (1, 582.0, -1), (1, 18.0, 1)


def test_mount_drills_the_side_panels_and_the_hatch():
    """In the cabinet frame left is +y: the left side panel at y 582..600,
    its inner face at 582. The carcass front is the hatch's inner face, x =
    18; the top's underside, the reference, z = 332. Carcass holes: 5 x 12,
    37 behind the front edge, 102, 134 and 166 below the reference, named
    by the hatch, a to c from the top; pilot holes in the hatch's inner
    face: 2 x 4, 25 in from each side panel's inner face, 12 and 76 below
    the reference, named by the side panel."""
    _, parts = _cabinet()
    for name, face in (("left", "left"), ("right", "right")):     # inner faces: -y and +y
        holes = _holes(parts[name])
        assert [(h.name, h.face, h.u, h.v, h.d, h.depth) for h in holes] == [
            ("hinge_hatch_a", face, 55, 230, 5, 12), ("hinge_hatch_b", face, 55, 198, 5, 12),
            ("hinge_hatch_c", face, 55, 166, 5, 12)]
    holes = _holes(parts["hatch"])
    assert [(h.name, h.face, h.u, h.v, h.d, h.depth) for h in holes] == [
        ("hinge_left_a", "back", 557, 320, 2, 4), ("hinge_left_b", "back", 557, 256, 2, 4),
        ("hinge_right_a", "back", 43, 320, 2, 4), ("hinge_right_b", "back", 43, 256, 2, 4)]
    assert parts["left"].hinge_hatch_a.top.value == 232.5      # named operations, as positions


def test_settings_and_a_gap_move_the_holes():
    """A 1.5 mm gap: the carcass front is at x 19.5, the hatch's inner face
    stays at 18. Carcass depth and pilot holes follow the settings."""
    hinge = HatchHinge("Free space 1.11", carcass_depth=10, pilot=(2.5, 5))
    _, parts = _cabinet(hinge, gap=1.5)
    assert {(h.u, h.depth, h.d) for h in _holes(parts["left"])} == {(19.5 + 37, 10, 5)}
    assert {(h.u, h.v, h.d, h.depth) for h in _holes(parts["hatch"])} == {
        (557, 320, 2.5, 5), (557, 256, 2.5, 5), (43, 320, 2.5, 5), (43, 256, 2.5, 5)}
    assert all(h.face == "back" for h in _holes(parts["hatch"]))


def test_top_as_the_height_of_its_underside():
    registry.reset()
    _, by_board = _cabinet()
    registry.reset()
    _, by_face = _cabinet(top=Pos("z", 332))
    assert [(h.u, h.v) for h in _holes(by_face["left"])] == [(h.u, h.v) for h in _holes(by_board["left"])]


def test_one_hinge():
    """sides= may name the one side panel that carries a hinge."""
    cab, parts = _cabinet(mount=False)
    cab.mount(HatchHinge("Free space 1.11"), hatch=parts["hatch"], sides=parts["right"], top=parts["top"])
    assert len(_holes(parts["right"])) == 3 and _holes(parts["left"]) == []
    assert [h.name for h in _holes(parts["hatch"])] == ["hinge_right_a", "hinge_right_b"]
    (hinges,) = cab.hardware
    assert [b["name"] for b in hinges["bodies"]] == ["right"]


def test_what_the_hinge_dictates():
    """A_max from the manual's table, linear in between (19: 23.5, 22:
    22.5), 37 with the limiter; the highest hatch top above the top's
    underside; the closed hinge's lowest point."""
    hinge = HatchHinge("Free space 1.11")
    assert hinge.max_overlap(18) == 24
    assert hinge.max_overlap(20) == pytest.approx(23.5 - 1 / 3)
    assert HatchHinge("Free space 1.11", opening=90).max_overlap(18) == 37
    with pytest.raises(LangError, match="fits hatches from 16 mm to 28 mm"):
        hinge.max_overlap(30)
    _, parts = _cabinet(mount=False)
    assert hinge.highest_hatch_top(parts["top"], 18) == Pos("z", 332 + 24)
    assert hinge.lowest(parts["top"]) == hinge.lowest(Pos("z", 332)) == Pos("z", 332 - SHAPE.lowest)
    assert SHAPE.lowest == max(below for _, _, (_, below) in hinge.hinge_boxes().values())


def test_hinges_are_boxes_against_the_side_panels():
    """Each hinge's boxes as the table gives them: inward from its side
    panel's inner face, back from the carcass front, below the top's
    underside. With today's table the left hinge takes y 546.8..582, x
    18..80.8 and z 163..330.1; the plate's front lies on the hatch's inner
    face, also across a gap."""
    cab, _ = _cabinet()
    (hinges,) = cab.hardware
    assert hinges["path"] == "cab.hatch_hinges" and [b["name"] for b in hinges["bodies"]] == ["left", "right"]
    left, right = hinges["bodies"]
    assert _drawn(left) == _expected(LEFT_INWARD, BACK, DOWN)
    assert _drawn(right) == _expected(RIGHT_INWARD, BACK, DOWN)
    assert build_layout()["modules"][0]["hardware"] == [hinges]
    registry.reset()
    cab, _ = _cabinet(gap=1.5)
    plate = cab.hardware[0]["bodies"][0]["boxes"][0]
    assert plate["min"][0] == 18                                # the hatch's inner face
    assert _drawn(cab.hardware[0]["bodies"][0]) == _expected(LEFT_INWARD, (0, 19.5, 1), DOWN, gap=1.5)


def test_probe_points_lie_in_or_at_the_boxes():
    """The add-in's probe points, inside the closed STEP hinge, against the
    boxes measured on Häfele's CAD model (the hatch 0.3 in front, as in the
    STEP): all but one lie inside. (25, 1, 3), 1 behind the carcass front
    and 3 below the reference, lies 2 mm above the plate's box, which
    starts 5 below: the boxes leave that corner of the hinge out."""
    boxes = HatchHinge("Free space 1.11").hinge_boxes(gap=0.3)

    def distance(point: tuple[float, float, float], box: HingeBox) -> float:
        return sum((c - min(max(c, lo), hi)) ** 2 for c, (lo, hi) in zip(point, box)) ** 0.5

    for point in FREE_SPACE_1_11.probe_points:
        assert min(distance(point, box) for box in boxes.values()) <= 2.0, point


def test_hinge_boxes_leave_room_for_the_cabinet():
    """The boxes touch the side panels, the hatch and a shelf right below
    them, but overlap none of them."""
    hinge = HatchHinge("Free space 1.11")
    cab, parts = _cabinet(hinge, shelf_at=332 - SHAPE.lowest - 18)
    for body in cab.hardware[0]["bodies"]:
        for b in body["boxes"]:
            box = Box(dict(zip("xyz", b["min"])), dict(zip("xyz", b["max"])))  # type: ignore[arg-type]
            for name, part in parts.items():
                assert not (box.overlaps(part.box()) and _has_material(part, box.intersection(part.box()))), name


def _physical(cab: Scope, parts: dict[str, Board]) -> tuple[set[tuple[object, ...]], list[HardwareBodyLayout]]:
    """Every hole by the board's box (its name with the board names
    replaced by where the boards are), and the hinge bodies."""
    where = {p.name: str(p.box().as_dict()["min"]) for p in parts.values()}
    holes: set[tuple[object, ...]] = set()
    for p in parts.values():
        for h in _holes(p):
            name = h.name or ""
            for board_name, place in where.items():
                name = name.replace(f"_{board_name}_", f"_{place}_")
            holes.add((tuple(p.box().as_dict()["min"]), name, h.face, h.u, h.v, h.d, h.depth))
    return holes, cab.hardware[0]["bodies"]


def test_same_hinges_in_any_frame():
    """A module in the van's terms (its left is -y, the hatch's right), a
    cabinet (front=) and a mirrored cabinet drill the same holes and place
    the same hinges, named by the hatch's own left and right. The hatch's
    holes are named by the side panels, which are called left and right
    the other way round in the van's terms."""
    results: list[tuple[set[tuple[object, ...]], list[HardwareBodyLayout]]] = []
    for frame in ("cabinet", "van", "mirrored"):
        registry.reset()
        results.append(_physical(*_cabinet(frame=frame)))
    assert results[0] == results[1] == results[2]
    registry.reset()
    _, van = _cabinet(frame="van")
    assert van["left"].box().lo["y"] == 0 and len(_holes(van["left"])) == 3      # the van's left is -y
    assert {(h.name, h.u) for h in _holes(van["hatch"])} >= {("hinge_left_a", 43), ("hinge_right_a", 557)}
    left_body = results[1][1][0]
    assert left_body["name"] == "left" and bounds(left_body)[1][1] == 582      # the hatch's left is +y


def test_rotated_cabinet():
    """A cabinet opening toward +y (front=box.right): the hatch at y
    302..320, the carcass front at 302, back is -y; the cabinet's left side
    panel at x 582..600 carries the left hinge: carcass holes 37 behind the
    front at y 265, pilot holes 25 in from x 582."""
    box = Box.from_size(width=320, depth=600, height=350)
    with cabinet("cab", box, front=box.right) as cab:
        left = board("left", ply18).on(cab.left).between(cab.front.into(18), cab.back)
        right = board("right", ply18).on(cab.right).between(cab.front.into(18), cab.back)
        top = board("top", ply18).on(cab.top).between(left, right, cab.front.into(18), cab.back)
        hatch = board("hatch", ply18).on(cab.front)
        cab.mount(HatchHinge("Free space 1.11"), hatch=hatch, sides=(left, right), top=top)
    assert left.box().lo["x"] == 582
    assert [(h.face, h.u, h.v) for h in _holes(left)] == [("front", 265, 230), ("front", 265, 198),
                                                          ("front", 265, 166)]
    assert {(h.name, h.face, h.u, h.v) for h in _holes(hatch)} == {
        ("hinge_left_a", "left", 557, 320), ("hinge_left_b", "left", 557, 256),
        ("hinge_right_a", "left", 43, 320), ("hinge_right_b", "left", 43, 256)}
    (hinges,) = cab.hardware
    assert _drawn(hinges["bodies"][0]) == _expected((0, 582.0, -1), (1, 302.0, -1), DOWN)


@pytest.mark.parametrize("hatch_t, message", [
    (30, "The hatch is 30 mm thick; the Häfele Free space 1.11 fits hatches from 16 mm to 28 mm."),
    (15, "The hatch is 15 mm thick"),
])
def test_refuses_a_hatch_of_the_wrong_thickness(hatch_t: float, message: str):
    with pytest.raises(LangError, match=message):
        _cabinet(hatch_t=hatch_t)


def test_overlap_is_checked_never_chosen():
    """A 25 mm top: the hatch top reaches 25 above the top's underside, the
    hinge allows 24 for an 18 mm hatch, 37 with the opening limited."""
    with pytest.raises(LangError, match=r"reaches 25 mm above the underside of the carcass top\. The Häfele Free "
                                        r"space 1\.11 allows at most 24 mm for a 18 mm hatch \(37 mm with the "
                                        r"opening limited to 90°\)\."):
        _cabinet(top_t=25)
    registry.reset()
    _cabinet(HatchHinge("Free space 1.11", opening=90), top_t=25)
    registry.reset()
    with pytest.raises(LangError, match="allows at most 23.2 mm for a 20 mm hatch"):    # interpolated
        _cabinet(hatch_t=20, top_t=24)


def test_the_hatch_must_be_closed():
    with pytest.raises(LangError, match=r"closed position, against the carcass front \(it is 3 mm in front"):
        _cabinet(gap=3)
    registry.reset()
    _cabinet(gap=2)                                            # the depth adjustment takes up to 2 mm
    registry.reset()
    with pytest.raises(LangError, match="The hatch reaches 2 mm into the carcass"):
        _cabinet(gap=-2)


def test_side_panels_need_flush_front_edges():
    with pytest.raises(LangError, match="1 mm apart in depth"):
        _cabinet(right_set_back=1)


def test_the_mounting_plate_must_fit_on_the_hatch():
    """A hatch 10 below the carcass top: the plate starts 5 below it."""
    with pytest.raises(LangError, match="mounting plate does not fit on the hatch. It covers 5 mm to 83 mm"):
        _cabinet(hatch_drop=28)


def test_holes_must_fit_on_their_boards():
    """A shelf-pin hole where a carcass hole goes, a hole in the hatch where
    a pilot hole goes, and a cabinet too low for the carcass holes."""
    cab, parts = _cabinet(mount=False)
    left = parts["left"]
    left.hole(d=5, depth=10, at=left.inner.front(37).bottom(Pos("z", 198)))
    with pytest.raises(LangError, match="carcass holes do not fit"):
        cab.mount(HatchHinge("Free space 1.11"), hatch=parts["hatch"], sides=(left, parts["right"]), top=parts["top"])
    registry.reset()
    cab, parts = _cabinet(mount=False)
    hatch = parts["hatch"]
    hatch.hole(d=6, depth=5, at=hatch.inner.left(Pos("y", 557)).bottom(Pos("z", 320)))
    with pytest.raises(LangError, match="pilot holes do not fit"):
        cab.mount(HatchHinge("Free space 1.11"), hatch=hatch, sides=(parts["left"], parts["right"]), top=parts["top"])
    registry.reset()
    with pytest.raises(LangError, match="carcass holes do not fit"):
        _cabinet(height=180)


def test_hole_depths_must_stay_inside_the_boards():
    with pytest.raises(LangError, match=r"the carcass hole depth \(18 mm\) must be less than cab.left's thickness "
                                        r"\(18 mm\)"):
        _cabinet(HatchHinge("Free space 1.11", carcass_depth=18))
    registry.reset()
    with pytest.raises(LangError, match=r"the pilot depth \(18 mm\) must be less than cab.hatch's thickness "
                                        r"\(18 mm\)"):
        _cabinet(HatchHinge("Free space 1.11", pilot=(2, 18)))
    with pytest.raises(LangError, match="greater than zero"):
        HatchHinge("Free space 1.11", carcass_depth=0)
    with pytest.raises(LangError, match="greater than zero"):
        HatchHinge("Free space 1.11", pilot=(0, 4))
    with pytest.raises(LangError, match="expected 107 or 90, not 95"):
        HatchHinge("Free space 1.11", opening=95)  # type: ignore[arg-type]


def test_nothing_may_take_the_hinges_space():
    """A shelf in the hinges' height (290, 42 below the reference, is a
    probe point), and the top's upper face given as the reference, which
    puts the hinges into the top. Like the add-in, only the probe points
    are checked: a shelf at 250 to 268 lies between them."""
    with pytest.raises(LangError, match="The left hinge would collide with cab.shelf"):
        _cabinet(shelf_at=280)
    registry.reset()
    _cabinet(shelf_at=332 - SHAPE.lowest - 18)                 # below them
    registry.reset()
    with pytest.raises(LangError, match="collide with cab.top"):
        _cabinet(top=Pos("z", 350))


def test_mount_refuses_what_it_cannot_take():
    cab, parts = _cabinet(mount=False)
    hinge = HatchHinge("Free space 1.11")
    hatch, left, right, top = parts["hatch"], parts["left"], parts["right"], parts["top"]
    options: dict[str, Any]
    for options, message in (
        ({"hatch": hatch, "sides": (left, left), "top": top}, "two different side panels"),
        ({"hatch": hatch, "sides": (left, right, top), "top": top}, "sides= must be"),
        ({"hatch": hatch, "sides": (left, hatch), "top": top}, "cannot be one of the side panels"),
        ({"hatch": hatch, "sides": (left, right), "top": left}, "top= must be the carcass top"),
        ({"hatch": hatch, "sides": (left, right), "top": Pos("x", 30)}, "is not a height"),
        ({"hatch": hatch, "sides": (left, top), "top": parts["bottom"]}, "perpendicular to the hatch"),
        ({"hatch": top, "sides": (left, right), "top": parts["bottom"]}, "stand upright"),
    ):
        with pytest.raises(LangError, match=message):
            cab.mount(hinge, **options)
    # the keywords are mount's own, checked by the type checker too (typing_checks.py)
    with pytest.raises(TypeError, match="top"):
        cab.mount(hinge, hatch=hatch, sides=(left, right))  # type: ignore[call-arg]
    with pytest.raises(TypeError, match="front"):
        cab.mount(hinge, hatch=hatch, sides=(left, right), top=top, front=hatch)  # type: ignore[call-arg]
    assert all(_holes(p) == [] for p in parts.values()) and cab.hardware == []   # a refused mount changes nothing
    cab.mount(hinge, hatch=hatch, sides=(left, right), top=top)
    before = [list(p.ops) for p in parts.values()]
    with pytest.raises(LangError, match="cab.hatch hangs on cab.left already"):
        cab.mount(hinge, hatch=hatch, sides=(left, right), top=top)
    assert [list(p.ops) for p in parts.values()] == before and len(cab.hardware) == 1
    registry.reset()
    cab, parts = _cabinet(mount=False)
    left = parts["left"]
    with cab:
        other = board("other", ply18).on(left.inner, toward=cab.right).between(cab.front.into(18), cab.back)
    with pytest.raises(LangError, match="opposite sides of the cabinet"):
        cab.mount(hinge, hatch=parts["hatch"], sides=(left, other), top=parts["top"])


def test_layout_plans_the_holes_and_the_hinges():
    """The emitter's plan: one hole step per board face, diameter and depth,
    the hinges as a component of the module's with a body per hinge."""
    _cabinet()
    plan = plan_layout(build_layout())
    assert plan.problems == []
    steps = {p.path: p.steps for p in plan.parts}
    (left,) = steps["cab.left"]
    assert isinstance(left, HoleStep) and left.face == FaceRef("y", -1, 582.0)
    assert left.points == [(55, 582, 230), (55, 582, 198), (55, 582, 166)] and (left.d, left.depth) == (5, 12)
    (hatch,) = steps["cab.hatch"]
    assert isinstance(hatch, HoleStep) and hatch.face == FaceRef("x", 1, 18.0) and (hatch.d, hatch.depth) == (2, 4)
    assert hatch.points == [(18, 557, 320), (18, 557, 256), (18, 43, 320), (18, 43, 256)]
    (hinges,) = plan.hardware
    assert (hinges.path, hinges.component, hinges.name) == ("cab.hatch_hinges", ("cab",), "hatch_hinges")
    assert [b.name for b in hinges.bodies] == ["left", "right"]
    assert len(hinges.bodies[0].boxes) == len(SHAPE.boxes(0.0))


def test_preview_draws_the_hinges_as_boxes():
    from lang.preview.mesh import build_scene
    _cabinet()
    scene = build_scene(build_layout())
    meshes = {}
    for node in scene.graph.nodes_geometry:
        if "hinges" in node:
            transform, geometry = scene.graph[node]
            mesh = scene.geometry[geometry].copy()
            mesh.apply_transform(transform)
            meshes[node.rsplit(".", 1)[1]] = mesh
    assert set(meshes) == {"left", "right"}
    assert meshes["left"].is_volume
    assert meshes["left"].bounds.round(4).tolist() == _union(_expected(LEFT_INWARD, BACK, DOWN))
    assert meshes["right"].bounds.round(4).tolist() == _union(_expected(RIGHT_INWARD, BACK, DOWN))


def _hinges(layout_modules: list[HardwareLayout]) -> HardwareLayout:
    (hinges,) = layout_modules
    return hinges


def test_example_builds(tmp_path: Path):
    """examples/hatch.py: a wall cabinet opening toward +y, its left side
    panel at x 782..800. The shelf's upper face is where the hinges end."""
    example = Path(__file__).resolve().parent.parent / "examples" / "hatch.py"
    layout = run_build(example, tmp_path, scene=True)
    assert layout["problems"] == [] and layout["modules"][0]["problems"] == []
    parts = {p["path"]: p for p in layout["modules"][0]["parts"]}
    holes = [op for op in parts["wallcab.left"]["ops"] if op["kind"] == "hole" and op["name"] == "hinge_hatch_a"]
    assert [(h["face"], h["u"], h["v"]) for h in holes] == [("front", 312 - 37, 1782 - 102)]
    hinges = _hinges(layout["modules"][0]["hardware"])
    assert hinges["path"] == "wallcab.hatch_hinges"
    assert bounds(hinges["bodies"][0])[0][2] == parts["wallcab.shelf"]["box"]["max"][2] == 1782 - SHAPE.lowest
    assert (tmp_path / "scene.glb").exists()
    # the hinges overlap none of the cabinet's parts, joints and all
    (cabinet,) = registry.roots
    for body in hinges["bodies"]:
        for b in body["boxes"]:
            box = Box(dict(zip("xyz", b["min"])), dict(zip("xyz", b["max"])))  # type: ignore[arg-type]
            for part in cabinet.all_parts():
                assert not (box.overlaps(part.box()) and _has_material(part, box.intersection(part.box()))), part


# -- the review's fixes (findings 27, 30, 43) --------------------------------------------------------------

def test_the_model_by_name_or_spec():
    from typing import get_args
    from lang.hardware.hatch_hinges import HATCH_HINGE_MODELS
    assert get_args(HatchHingeModel) == tuple(HATCH_HINGE_MODELS)
    assert HatchHinge("Free space 1.11").spec is FREE_SPACE_1_11
    assert HatchHinge(FREE_SPACE_1_11).spec is FREE_SPACE_1_11          # a spec of your own
    with pytest.raises(LangError, match=r"HatchHinge\(\): expected 'Free space 1.11'"):
        HatchHinge("Free space 1.12")  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        HatchHinge("Free space 1.11", 90)  # type: ignore[misc]            # settings are keyword-only


def test_a_height_is_read_in_the_mounts_frame():
    """`top=` as a position is a height in the frame of the scope the
    hinges are mounted in, not in whatever frame is current when `mount`
    runs (after the `with` block, the world's)."""
    from lang.hardware.hatch_hinges import _reference  # type: ignore[reportPrivateUsage]
    lying = Frame(front="-x", left="-z", top="+y")
    with pytest.raises(LangError, match="is not a height"):
        _reference(Pos("z", 332), "top=", lying)
    assert _reference(Pos("y", 332), "top=", lying)[1].axis == "y"
    cab, parts = _cabinet(mount=False)
    cab.mount(HatchHinge("Free space 1.11"), hatch=parts["hatch"], sides=(parts["left"], parts["right"]),
              top=Pos("z", 332))                                           # outside the module's block
    assert [h.v for h in _holes(parts["left"])] == [230, 198, 166]


def test_two_hatches_in_one_cabinet():
    """Two hatches side by side over a partition: each hangs on its side
    panels, the partition carrying a hinge of each on its two faces; the
    items are named by the hatches (a second hatch in one scope was
    refused before)."""
    box = Box.from_size(width=1000, depth=320, height=350)
    with cabinet("cab", box, front=box.front) as cab:
        carcass = cab.front.into(18)
        left = board("left", ply18).on(cab.left).between(carcass, cab.back)
        right = board("right", ply18).on(cab.right).between(carcass, cab.back)
        wall = board("wall", ply18).center(cab.center("width")).between(carcass, cab.back)
        top = board("top", ply18).on(cab.top).between(left, right, carcass, cab.back)
        halves = [(cab.left, cab.center("width") + 1), (cab.center("width") - 1, cab.right)]
        hatches = [board(name, ply18).on(cab.front).between(a, b) for name, (a, b) in zip(("one", "two"), halves)]
        for hatch, sides in zip(hatches, ((left, wall), (wall, right))):
            cab.mount(HatchHinge("Free space 1.11"), hatch=hatch, sides=sides, top=top)
    assert [item["name"] for item in cab.hardware] == ["one_hinges", "two_hinges"]
    assert {(h.name, h.face) for h in _holes(wall)} == {
        (f"hinge_{n}_{c}", f) for n, f in (("one", "right"), ("two", "left")) for c in "abc"}


def test_two_hinges_whose_plates_meet_on_a_narrow_hatch_are_refused():
    """Found by fuzzing: in a cabinet 85 wide the two hinges' pilot holes,
    25 in from each side panel, met on the hatch; each was checked against
    what was there before, and the core refused the second halfway, the
    first drilled. The mounting plates reach 34.5 in from their side panel:
    sides whose inner faces lie closer than 69 are refused before anything
    is drilled."""
    for width, inner in ((85, 49), (36 + 69, 69)):
        registry.reset()
        box = Box.from_size(width=width, depth=320, height=350)
        with cabinet("cab", box, front=box.front) as cab:
            carcass = cab.front.into(18)
            left = board("left", ply18).on(cab.left).between(carcass, cab.back)
            right = board("right", ply18).on(cab.right).between(carcass, cab.back)
            top = board("top", ply18).on(cab.top).between(left, right, carcass, cab.back)
            hatch = board("hatch", ply18).on(cab.front)
            if inner < 69:
                with pytest.raises(LangError, match=rf"^cab\.hatch: Häfele Free space 1\.11: the side panels' inner "
                                                    rf"faces are {inner} mm apart; the two hinges' mounting plates"):
                    cab.mount(HatchHinge("Free space 1.11"), hatch=hatch, sides=(left, right), top=top)
                assert hatch.ops == [] and left.ops == [] and right.ops == [] and cab.hardware == []
            else:
                cab.mount(HatchHinge("Free space 1.11"), hatch=hatch, sides=(left, right), top=top)
