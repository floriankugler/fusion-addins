"""Random cabinets and the hardware mounted on them, for fuzzing
`lang.hardware` as `joints.py` fuzzes the joints: a case is plain data,
built with the language's own calls, and checked from the outside.

Each case is a cabinet in the shape of the examples (`hinged_door.py`,
`door_latch.py`, ...), its sizes, thicknesses, gaps and the hardware's
settings drawn from their ranges and a little beyond. It is built twice,
facing two different sides of its box (`cabinet(front=)`) at two places:
what the hardware drills and places, measured from the cabinet's own
front, left and bottom, must come out the same, and a refusal must be one
both ways.

`run_case` checks what every mount promises (`lang.hardware.common`): no
other error than a LangError; a refused mount changes no board and places
nothing; an accepted one plans, draws and meshes, leaves every board in
one piece, and reports nothing in the layout (the cabinets check
`no_interference`: no bought part reaches into a board or another part);
every hole it drills lies on its board's face, clear of what was there
before and of its other holes on that face, and a blind one stops short of
the far face; and its stations along the edge are `lib.stations`'.
"""
from __future__ import annotations

import math
import re
import traceback
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal

from hypothesis import strategies as st
from shapely.geometry import LineString
from shapely.geometry.base import BaseGeometry

from boards import _pipeline_problems  # pyright: ignore[reportPrivateUsage]
from fuzzing import floats, fresh, sizes
from lang import (BallCatch, Box, ConcealedHinge, DoorLatch, DrawerSlide, HatchHinge, LangError, SlidingBracket, board,
                  cabinet, check, sheet_material, no_interference, rect, scope)
from lang.core.cutouts import circle_geometry
from lang.core.directions import AXES, Axis, Direction, world_frame
from lang.core.layout import build_layout
from lang.core.ops import Cut, EdgeOp, Hole, Op, Pocket, VGroove
from lang.core.part import Board
from lang.core.scope import Scope
from lang.hardware.hinges import HINGE_SHAPES
from lib import stations as station_rule

#: The side of its box a cabinet opens toward, by index.
FRONTS = ("front", "right", "back", "left")


def _thickness() -> st.SearchStrategy[float]:
    """Mostly the sheet thicknesses a cabinet has, now and then any."""
    return st.one_of(st.sampled_from([15.0, 18.0, 19.0, 22.0]), st.sampled_from([12.0, 16.0, 25.0]),
                     sizes(4, 40))


def _origin() -> st.SearchStrategy[tuple[float, float, float]]:
    return st.one_of(st.just((0.0, 0.0, 0.0)), st.tuples(floats(-2000, 2000), floats(-2000, 2000), floats(-500, 2000)))


def _box(size: tuple[float, float, float], front: int, origin: tuple[float, float, float]) -> Box:
    """The world box of a cabinet `size` (its own width, depth, height)
    that opens toward `FRONTS[front]`."""
    w, d, h = size
    if FRONTS[front] in ("front", "back"):
        return Box.from_size(width=w, depth=d, height=h, origin=origin)
    return Box.from_size(width=d, depth=w, height=h, origin=origin)


@dataclass
class Built:
    """A cabinet built for one case: its scope and box, its boards, and
    the mount to try."""
    cab: Scope
    box: Box
    boards: list[Board]
    mount: Callable[[], None]
    #: Stations to check: (what, the holes' names in order, the edge's ends
    #: as world positions on `axis`, count, end); see `_station_problems`.
    stations: Callable[[], list[tuple[str, list[str], Axis, tuple[float, float], int, float]]] | None = None
    #: The boards the hardware is mounted on: its boxes must not reach into them.
    mounted: list[Board] = field(default_factory=list[Board])
    #: Numbered toward a world axis' positive end, as hardware on a part lying
    #: flat is (`lang.hardware.common.numbering`), so compared without names.
    unnamed: bool = False
    #: How far apart the stations must at least be (hinges: their plates' length).
    apart: float = 0.0


# -- doors: concealed hinges and latches -------------------------------------------------------------

@dataclass(frozen=True)
class DoorCase:
    """A carcass (sides, top and bottom) and a door in front of it, over
    the boards' front edges or set in between them, and hinges or latches
    between the door and one carcass board."""
    kind: Literal["hinge", "latch"]
    size: tuple[float, float, float]        # the cabinet's own width, depth, height
    side_t: float
    door_t: float
    inset: bool                             # the door set in between the carcass boards
    reveal: float                           # the gap all round the door
    gap: float                              # an overlay door this far in front of the carcass
    on: Literal["left", "right", "top", "bottom"]       # the carcass board
    params: tuple[tuple[str, Any], ...]     # the hardware's settings
    front: int                              # FRONTS
    turn: int                               # the second build faces FRONTS[(front + turn) % 4]
    origin: tuple[float, float, float]
    origin2: tuple[float, float, float]


def _pilot() -> st.SearchStrategy[tuple[float, float]]:
    return st.tuples(st.sampled_from([2.0, 3.0, 3.175, 4.0, 1.0, 6.0]), st.sampled_from([3.0, 4.0, 6.0, 10.0, 0.5, 20.0]))


@st.composite
def door_cases(draw: st.DrawFn) -> DoorCase:
    kinds: list[Literal["hinge", "latch"]] = ["hinge", "latch"]
    kind = draw(st.sampled_from(kinds))
    params: list[tuple[str, Any]] = []
    if kind == "hinge":
        params.append(("model", draw(st.sampled_from(["Blum CLIP top 110 Thin +0", "Blum CLIP top 110 Thin +3"]))))
        params.append(("count", draw(st.sampled_from([2, 2, 3, 4, 5]))))
        end = draw(st.one_of(st.none(), st.sampled_from([27.0, 60.0, 100.0]), sizes(20, 300)))
    else:
        params.append(("model", draw(st.sampled_from(["Everlock", "Pull Lock 44", "LL-66"]))))
        params.append(("count", draw(st.sampled_from([1, 1, 2, 3]))))
        end = draw(st.one_of(st.none(), st.sampled_from([50.0, 100.0]), sizes(10, 300)))
    if end is not None:
        params.append(("end", end))
    pilot = draw(st.one_of(st.none(), _pilot()))
    if pilot is not None:
        params.append(("pilot", pilot))
    return DoorCase(
        kind=kind,
        size=(draw(st.one_of(st.just(500.0), sizes(150, 1200))), draw(st.one_of(st.just(350.0), sizes(100, 700))),
              draw(st.one_of(st.just(700.0), sizes(150, 1600)))),
        side_t=draw(_thickness()), door_t=draw(_thickness()), inset=draw(st.booleans()),
        reveal=draw(st.one_of(st.just(1.5), st.just(2.0), floats(0, 10))),
        gap=draw(st.one_of(st.just(0.0), floats(0, 5))),
        on=draw(st.sampled_from(["left", "right", "top", "bottom"])), params=tuple(params),
        front=draw(st.integers(0, 3)), turn=draw(st.integers(1, 3)), origin=draw(_origin()), origin2=draw(_origin()))


def build_door(case: DoorCase, front: int, origin: tuple[float, float, float], name: str = "cab") -> Built:
    box = _box(case.size, front, origin)
    ply = sheet_material("birch", t=case.side_t)
    settings = dict(case.params)
    model = settings.pop("model")
    with cabinet(name, box, front=getattr(box, FRONTS[front])) as cab:
        behind = [] if case.inset else [cab.front.into(case.door_t + case.gap)]
        left = board("left", ply).on(cab.left).between(*behind) if behind else board("left", ply).on(cab.left)
        right = board("right", ply).on(cab.right).between(*behind) if behind else board("right", ply).on(cab.right)
        top = board("top", ply).on(cab.top).between(left, right, *behind)
        bottom = board("bottom", ply).on(cab.bottom).between(left, right, *behind)
        door = board("door", sheet_material("birch", t=case.door_t)).on(cab.front)
        if case.inset:
            door.between(left, right, top, bottom)
        door.inset(case.reveal)
        check(no_interference)
        hardware = ConcealedHinge(model, **settings) if case.kind == "hinge" else DoorLatch(model, **settings)
    carcass = {"left": left, "right": right, "top": top, "bottom": bottom}[case.on]

    def mount() -> None:
        with cab:
            cab.mount(hardware, door=door, carcass=carcass)

    def stations() -> list[tuple[str, list[str], Axis, tuple[float, float], int, float]]:
        # (the door's hinged or latched edge runs along the carcass board's face)
        edge: Axis = next(a for a in AXES if a not in (door.t_axis, carcass.t_axis))
        ends = (door.box().lo[edge], door.box().hi[edge])
        if isinstance(hardware, ConcealedHinge):
            names = [f"hinge_{carcass.name}_{i}" for i in range(1, hardware.count + 1)]
            return [("hinge", names, edge, ends, hardware.count, hardware.end)]
        return []

    # (the hinges' length along the edge, their plates', from their boxes)
    apart = 2 * max(max(abs(a), abs(c)) for _, _, (a, c) in HINGE_SHAPES[model].boxes().values()) \
        if case.kind == "hinge" else 0.0
    return Built(cab, box, [left, right, top, bottom, door], mount, stations, [door, carcass], apart=apart)


def _hole_choice() -> st.SearchStrategy[Any]:
    return st.one_of(st.just("pilot"), st.just("euro"), _pilot())


# -- removable panels: sliding brackets ----------------------------------------------------------------

@dataclass(frozen=True)
class PanelCase:
    """A carcass and a removable panel over its front edges or set in
    between its boards, hung with sliding brackets on two or one of them."""
    size: tuple[float, float, float]
    frame_t: float
    panel_t: float
    set_in: bool
    gap: float                              # over the edges: in front of them; set in: all round
    on: Literal["sides", "top and bottom", "left"]
    params: tuple[tuple[str, Any], ...]
    front: int
    turn: int
    origin: tuple[float, float, float]
    origin2: tuple[float, float, float]


@st.composite
def panel_cases(draw: st.DrawFn) -> PanelCase:
    params: list[tuple[str, Any]] = [("model", draw(st.sampled_from(["Pacofix PF-L-R", "Pacofix PF-L"])))]
    for key, strategy in (("count", st.sampled_from([1, 2, 2, 3, 4])), ("end", st.one_of(st.just(50.0), sizes(10, 200))),
                          ("frame_hole", _hole_choice()), ("panel_hole", _hole_choice())):
        if draw(st.booleans()):
            params.append((key, draw(strategy)))
    return PanelCase(
        size=(draw(st.one_of(st.just(800.0), sizes(150, 1200))), draw(st.one_of(st.just(400.0), sizes(100, 700))),
              draw(st.one_of(st.just(450.0), sizes(150, 1200)))),
        frame_t=draw(_thickness()), panel_t=draw(_thickness()), set_in=draw(st.booleans()),
        gap=draw(st.one_of(st.just(0.0), st.just(1.5), floats(0, 4), floats(0, 30))),
        on=draw(st.sampled_from(["sides", "top and bottom", "left"])), params=tuple(params),
        front=draw(st.integers(0, 3)), turn=draw(st.integers(1, 3)), origin=draw(_origin()), origin2=draw(_origin()))


def build_panel(case: PanelCase, front: int, origin: tuple[float, float, float], name: str = "cab") -> Built:
    box = _box(case.size, front, origin)
    ply = sheet_material("birch", t=case.frame_t)
    settings = dict(case.params)
    model = settings.pop("model")
    with cabinet(name, box, front=getattr(box, FRONTS[front])) as cab:
        behind = [] if case.set_in else [cab.front.into(case.panel_t + case.gap)]
        left = board("left", ply).on(cab.left).between(*behind) if behind else board("left", ply).on(cab.left)
        right = board("right", ply).on(cab.right).between(*behind) if behind else board("right", ply).on(cab.right)
        top = board("top", ply).on(cab.top).between(left, right, *behind)
        bottom = board("bottom", ply).on(cab.bottom).between(left, right, *behind)
        panel = board("panel", sheet_material("birch", t=case.panel_t)).on(cab.front)
        if case.set_in:
            panel.between(left, right, bottom, top).inset(case.gap)
        check(no_interference)
        bracket = SlidingBracket(model, **settings)
    frames = {"sides": [left, right], "top and bottom": [top, bottom], "left": [left]}[case.on]

    def mount() -> None:
        with cab:
            cab.mount(bracket, panel=panel, frame=frames)

    def stations() -> list[tuple[str, list[str], Axis, tuple[float, float], int, float]]:
        if bracket.count is None:
            return []
        out: list[tuple[str, list[str], Axis, tuple[float, float], int, float]] = []
        for k, frame in enumerate(frames):
            edge: Axis = next(a for a in AXES if a not in (panel.t_axis, frame.t_axis))
            ends = (max(panel.box().lo[edge], frame.box().lo[edge]), min(panel.box().hi[edge], frame.box().hi[edge]))
            names = [f"bracket_panel_{k * bracket.count + i}" for i in range(1, bracket.count + 1)]
            out.append(("bracket", names, edge, ends, bracket.count, bracket.end))
        return out

    return Built(cab, box, [left, right, top, bottom, panel], mount, stations, mounted=[panel, *frames])


# -- lift-up hatches: hatch hinges -----------------------------------------------------------------

@dataclass(frozen=True)
class HatchCase:
    """A wall cabinet with a lift-up hatch over its front, its top `drop`
    below the cabinet's, hung on hatch hinges from the carcass top."""
    size: tuple[float, float, float]
    t: float
    hatch_t: float
    side_gap: float                         # between the hatch and the cabinet's sides
    drop: float                             # the hatch's top below the cabinet's
    gap: float                              # the hatch's inner face in front of the carcass
    params: tuple[tuple[str, Any], ...]
    front: int
    turn: int
    origin: tuple[float, float, float]
    origin2: tuple[float, float, float]


@st.composite
def hatch_cases(draw: st.DrawFn) -> HatchCase:
    params: list[tuple[str, Any]] = []
    for key, strategy in (("opening", st.sampled_from([107, 90])), ("carcass_depth", st.sampled_from([12.0, 10.0, 8.0, 20.0])),
                          ("pilot", _pilot())):
        if draw(st.booleans()):
            params.append((key, draw(strategy)))
    return HatchCase(
        size=(draw(st.one_of(st.just(800.0), sizes(250, 1400), sizes(40, 250))),
              draw(st.one_of(st.just(330.0), sizes(150, 600))), draw(st.one_of(st.just(400.0), sizes(200, 900)))),
        t=draw(_thickness()), hatch_t=draw(st.one_of(st.sampled_from([16.0, 18.0, 19.0, 22.0, 25.0, 28.0]), sizes(10, 34))),
        side_gap=draw(st.one_of(st.just(1.5), floats(0, 5))), drop=draw(st.one_of(st.just(0.0), floats(0, 30))),
        gap=draw(st.one_of(st.just(0.0), floats(0, 3))), params=tuple(params),
        front=draw(st.integers(0, 3)), turn=draw(st.integers(1, 3)), origin=draw(_origin()), origin2=draw(_origin()))


def build_hatch(case: HatchCase, front: int, origin: tuple[float, float, float], name: str = "cab") -> Built:
    box = _box(case.size, front, origin)
    ply = sheet_material("birch", t=case.t)
    with cabinet(name, box, front=getattr(box, FRONTS[front])) as cab:
        hatch = board("hatch", sheet_material("birch", t=case.hatch_t)).on(cab.front).between(
            cab.left.into(case.side_gap), cab.right.into(case.side_gap), cab.bottom, cab.top.into(case.drop))
        behind = cab.front.into(case.hatch_t + case.gap)
        left = board("left", ply).on(cab.left).between(behind, cab.back)
        right = board("right", ply).on(cab.right).between(behind, cab.back)
        top = board("top", ply).on(cab.top).between(left, right, behind, cab.back)
        bottom = board("bottom", ply).on(cab.bottom).between(left, right, behind, cab.back)
        check(no_interference)
        hinge = HatchHinge("Free space 1.11", **dict(case.params))

    def mount() -> None:
        with cab:
            cab.mount(hinge, hatch=hatch, sides=(left, right), top=top)

    return Built(cab, box, [left, right, top, bottom, hatch], mount, mounted=[hatch, left, right, top])


# -- inspection hatches: ball catches --------------------------------------------------------------

@dataclass(frozen=True)
class CatchCase:
    """A floor or back panel with a rounded opening in its middle, a hatch
    in it from `BallCatch.hatch`, and ball catches on two of its edges."""
    size: tuple[float, float, float]
    panel_t: float
    on: Literal["bottom", "back"]
    opening: tuple[float, float, float]     # its width and depth (or height) as fractions, the radius in mm
    edge: Literal["left", "right", "near", "far"]
    params: tuple[tuple[str, Any], ...]
    front: int
    turn: int
    origin: tuple[float, float, float]
    origin2: tuple[float, float, float]


@st.composite
def catch_cases(draw: st.DrawFn) -> CatchCase:
    params: list[tuple[str, Any]] = []
    for key, strategy in (("count", st.sampled_from([1, 2, 3, 4, 4, 5, 6, 8])), ("end", st.one_of(st.just(40.0), sizes(10, 150))),
                          ("pilot", _pilot()), ("gap", st.one_of(st.sampled_from([2.5, 3.0, 3.5]), floats(2.4, 3.6)))):
        if draw(st.booleans()):
            params.append((key, draw(strategy)))
    return CatchCase(
        size=(draw(st.one_of(st.just(800.0), sizes(150, 1400))), draw(st.one_of(st.just(1000.0), sizes(150, 1400))),
              draw(st.one_of(st.just(100.0), sizes(50, 1000)))),
        panel_t=draw(_thickness()), on=draw(st.sampled_from(["bottom", "back"])),
        opening=(draw(st.one_of(st.just(0.5), floats(0.1, 0.95))), draw(st.one_of(st.just(0.3), floats(0.1, 0.95))),
                 draw(st.one_of(st.just(20.0), st.just(0.0), sizes(1, 150)))),
        edge=draw(st.sampled_from(["left", "right", "near", "far"])), params=tuple(params),
        front=draw(st.integers(0, 3)), turn=draw(st.integers(1, 3)), origin=draw(_origin()), origin2=draw(_origin()))


def build_catch(case: CatchCase, front: int, origin: tuple[float, float, float], name: str = "cab") -> Built:
    box = _box(case.size, front, origin)
    w, d, h = case.size
    fu, fv, r = case.opening
    with cabinet(name, box, front=getattr(box, FRONTS[front])) as cab:
        panel = board("panel", sheet_material("birch", t=case.panel_t))
        if case.on == "bottom":
            panel.on(cab.bottom).show(cab.top)
            shape = rect(width=fu * w, depth=fv * d)
            near, far = "front", "back"
        else:
            panel.on(cab.back).show(cab.front)
            shape = rect(width=fu * w, height=fv * h)
            near, far = "bottom", "top"
        panel.cut(shape.rounded(r) if r > 0 else shape, at=panel.inner.center, name="opening")
        catch = BallCatch(**dict(case.params))
        hatch = catch.hatch("hatch", panel.opening)
        check(no_interference)
    side = {"left": "left", "right": "right", "near": near, "far": far}[case.edge]

    def mount() -> None:
        with cab:
            cab.mount(catch, opening=panel.opening, edge=panel.opening.side(side), hatch=hatch)

    return Built(cab, box, [panel, hatch], mount, mounted=[panel, hatch], unnamed=case.on == "bottom")


# -- drawers: slides -------------------------------------------------------------------------------

SLIDES: dict[str, list[int]] = {
    "Movento 760H": [250, 270, 300, 320, 350, 380, 400, 420, 450, 480, 500, 520, 550, 600],
    "Movento 766H": [450, 500, 520, 550, 580, 600, 650, 700, 750],
    "Dynapro 40": [250, 270, 300, 320, 350, 380, 400, 420, 450, 480, 500, 520, 550, 600],
    "Dynapro 50/70": [450, 500, 520, 550, 580, 600, 650, 700, 750],
}


@dataclass(frozen=True)
class DrawerCase:
    """A carcass with one drawer bay between its bottom and top, the
    drawer's face set into the bay, its box as the slide dictates and
    machined for it, and the slide mounted on the carcass sides."""
    size: tuple[float, float, float]
    side_t: float
    model: str
    nl: int
    box_t: float                            # the drawer box's sides
    height: float                           # the drawer box's height below the bay's top
    reveal: float
    params: tuple[tuple[str, Any], ...]
    front: int
    turn: int
    origin: tuple[float, float, float]
    origin2: tuple[float, float, float]


@st.composite
def drawer_cases(draw: st.DrawFn) -> DrawerCase:
    model = draw(st.sampled_from(sorted(SLIDES)))
    nl = draw(st.sampled_from(SLIDES[model]))
    params: list[tuple[str, Any]] = []
    for key, strategy in (("holes", st.sampled_from([2, 3, 4, 5, 6])), ("odd", st.booleans()), ("pilot", _pilot())):
        if draw(st.booleans()):
            params.append((key, draw(strategy)))
    return DrawerCase(
        size=(draw(st.one_of(st.just(500.0), sizes(250, 1200))),
              nl + 27.0 + draw(st.one_of(st.just(10.0), floats(0, 200), floats(-20, 3))),     # (the back, the face)
              draw(st.one_of(st.just(250.0), sizes(100, 600)))),
        side_t=draw(_thickness()), model=model, nl=nl, box_t=draw(st.sampled_from([12.0, 15.0, 16.0, 10.0])),
        height=draw(st.one_of(st.just(30.0), floats(30, 100))), reveal=draw(st.one_of(st.just(1.5), floats(0, 5))),
        params=tuple(params), front=draw(st.integers(0, 3)), turn=draw(st.integers(1, 3)), origin=draw(_origin()),
        origin2=draw(_origin()))


def build_drawer(case: DrawerCase, front: int, origin: tuple[float, float, float], name: str = "cab") -> Built:
    box = _box(case.size, front, origin)
    ply = sheet_material("birch", t=case.side_t)
    slide = DrawerSlide(case.model, case.nl, **dict(case.params))  # pyright: ignore[reportArgumentType]
    with cabinet(name, box, front=getattr(box, FRONTS[front])) as cab:
        left = board("left", ply).on(cab.left)
        right = board("right", ply).on(cab.right)
        bottom = board("bottom", ply).on(cab.bottom).between(left, right)
        top = board("top", ply).on(cab.top).between(left, right)
        back = board("back", sheet_material("birch", t=9)).on(cab.back).between(left, right, bottom, top)
        bay = cab.interior
        with scope("drawer", bay) as d:
            face = board("face", sheet_material("birch", t=15)).on(bay.front).between(bay).inset(case.reveal)
            dbox = slide.drawer_box(bay, front=face.back, side_thickness=case.box_t, height=bay.height - case.height)
            t = sheet_material("birch", t=case.box_t)
            l = board("left", t).on(dbox.left).between(dbox)
            r = board("right", t).on(dbox.right).between(dbox)
            f = board("front", t).on(dbox.front).between(l, r, dbox.bottom, dbox.top)
            k = board("back", t).on(dbox.back).between(l, r, dbox.bottom, dbox.top)
            floor = board("floor", sheet_material("birch", t=9)).on(dbox.bottom.into(slide.recess)).between(l, r, f, k)
            slide.machine_box(sides=(l, r), front=f, back=k, floor=floor)
        check(no_interference)

    def mount() -> None:
        with d:
            d.mount(slide, sides=(left, right), front=face.back)

    boards = [left, right, bottom, top, back, face, l, r, f, k, floor]
    return Built(cab, box, boards, mount, mounted=[left, right, l, r, f, k, floor])


# -- checking -----------------------------------------------------------------------------------

Case = DoorCase | PanelCase | HatchCase | CatchCase | DrawerCase
BUILDERS: dict[type, Callable[[Any, int, tuple[float, float, float], str], Built]] = {
    DoorCase: build_door, PanelCase: build_panel, HatchCase: build_hatch, CatchCase: build_catch,
    DrawerCase: build_drawer}


def run_case(case: Case) -> list[str]:
    """What is wrong with the case's mount, built facing two ways."""
    try:
        first = _attempt(case, case.front, case.origin)
        second = _attempt(case, (case.front + case.turn) % 4, case.origin2)
    except Exception as e:
        frame = next((fr for fr in reversed(traceback.extract_tb(e.__traceback__))
                      if "/lang/" in fr.filename), traceback.extract_tb(e.__traceback__)[-1])
        return [f"{type(e).__name__} at {Path(frame.filename).name}:{frame.lineno}: {e}"]
    problems = first[0] + second[0]
    if problems:
        return problems
    (status1, summary1), (status2, summary2) = first[1], second[1]
    if status1 != status2:
        return [f"facing {FRONTS[case.front]} it is {status1}, facing {FRONTS[(case.front + case.turn) % 4]} "
                f"{status2}: {summary1 if status1 != 'accepted' else summary2}"]
    if status1 == "accepted":
        difference = _difference(summary1, summary2)
        if difference:
            return [f"facing {FRONTS[(case.front + case.turn) % 4]} instead of {FRONTS[case.front]} it comes out "
                    f"otherwise: {difference}"]
    return []


Result = tuple[str, Any]


def _attempt(case: Case, front: int, origin: tuple[float, float, float]) -> tuple[list[str], Result]:
    """Builds the case facing `front` and mounts its hardware: the problems
    and ("unbuilt" | "refused", message) or ("accepted", summary)."""
    with fresh():
        try:
            built = BUILDERS[type(case)](case, front, origin, "cab")
            for x in built.boards:
                x.box()                 # (resolved here: a board with no room is the build's, not the mount's)
        except LangError as e:
            return [], ("unbuilt", str(e))
        before = _state(built)
        try:
            built.mount()
        except LangError as e:
            if _state(built) != before:
                return [f"a refused mount changed a board or placed hardware: {e}"], ("refused", str(e))
            return [], ("refused", str(e))
        return _accepted_problems(built, before), ("accepted", _summary(built))


State = tuple[list[tuple[str, str, list[Op]]], str]


def _state(b: Built) -> State:
    return [(x.path, x.outline.geometry.wkt, list(x.ops)) for x in b.boards], repr(b.cab.all_hardware())


def _accepted_problems(b: Built, before: State) -> list[str]:
    layout_problems = build_layout()["problems"]
    problems = [p for p in _pipeline_problems() if p not in layout_problems]      # (the plan lists them too)
    items = [item["path"] for item in b.cab.all_hardware()]
    mounted = {x.path for x in b.mounted}
    for p in layout_problems:
        one, _, two = p.partition(" overlaps ")
        if two and any(one.startswith(i + ".") for i in items) and two not in mounted:
            # (hardware meeting itself or a board it is not mounted on, where the build spaces it
            # closer than it is long or puts a board in its way: the check reports it, as it
            # should; hinges are refused that close, `Built.apart`)
            continue
        problems.append(p)
    old = {path: ops for path, _, ops in before[0]}
    for x in b.boards:
        if len(x.outline.polygons()) != 1:
            problems.append(f"{x.path} is in {len(x.outline.polygons())} pieces")
        new = x.ops[len(old[x.path]):] if x.ops[:len(old[x.path])] == old[x.path] else list(x.ops)
        problems += _hole_problems(x, old[x.path], new)
    if b.stations is not None and not problems:
        problems += _station_problems(b)
    return problems


def _footprint(x: Board, op: Op) -> BaseGeometry | None:
    """What an operation takes from a big face, in the outline's frame."""
    if isinstance(op, (Pocket, Cut)):
        return op.shape.geometry
    if isinstance(op, Hole):
        return circle_geometry((op.u, op.v), op.d / 2 + op.chamfer)
    if isinstance(op, VGroove):
        return LineString([(op.u0, op.v0), (op.u1, op.v1)]).buffer(op.depth, cap_style="flat")
    return None


def _reaches(x: Board, op: Op, face: str) -> bool:
    """Whether an operation takes material from the big face `face`."""
    if isinstance(op, (Pocket, Hole, VGroove)) and op.face == face:
        return True
    return isinstance(op, (Pocket, Hole)) and op.depth >= x.thickness - 1e-9


def _hole_problems(x: Board, old: list[Op], new: list[Op]) -> list[str]:
    """Each hole a mount drilled lies on the board's face, clear of what
    was there before and of the mount's other holes on that face, and a
    blind one stops short of the far face."""
    problems: list[str] = []
    material = x.outline.geometry.buffer(1e-3)
    holes = [op for op in new if isinstance(op, Hole)]
    for i, h in enumerate(holes):
        circle = circle_geometry((h.u, h.v), h.d / 2 + h.chamfer)
        if not material.contains(circle):
            problems.append(f"{x.path}: the hole {h.name!r} ({h.d:g} mm) reaches off the board")
        if not h.through and h.depth >= x.thickness - 1e-6:
            problems.append(f"{x.path}: the hole {h.name!r} is {h.depth:g} deep in {x.thickness:g}")
        for op in old:
            g = _footprint(x, op)
            if g is not None and _reaches(x, op, h.face) and g.intersection(circle).area > 1e-6:
                problems.append(f"{x.path}: the hole {h.name!r} lies in {getattr(op, 'name', None)!r}, made before")
        for other in holes[i + 1:]:
            if other.face == h.face and circle.intersection(circle_geometry((other.u, other.v), other.d / 2)).area > 1e-6:
                problems.append(f"{x.path}: the holes {h.name!r} and {other.name!r} overlap")
    return problems


def _station_problems(b: Built) -> list[str]:
    """The hardware's stations along its edge are `lib.stations`': the
    middle of each station's holes (named `<name>a`, `<name>b`, ...)."""
    assert b.stations is not None
    problems: list[str] = []
    by_name = {op.name: (x, op) for x in b.boards for op in x.ops if isinstance(op, Hole) and op.name}
    for what, names, axis, (lo, hi), count, end in b.stations():
        found: list[float] = []
        for name in names:
            pair = [v for k, v in by_name.items() if re.fullmatch(re.escape(name) + "[a-z]", k)]
            if not pair:
                problems.append(f"no holes {name}* for the {what}")
                return problems
            found.append(sum(_world(x, op)[axis] for x, op in pair) / len(pair))
        want = [lo + s for s in station_rule.stations(hi - lo, count, end)]
        if len(found) != len(want) or any(abs(a - w) > 1e-6 for a, w in zip(sorted(found), sorted(want))):
            problems.append(f"the {what}s stand at {[round(v, 3) for v in sorted(found)]} along {axis}, "
                            f"lib.stations puts them at {[round(v, 3) for v in sorted(want)]}")
        close = [round(q - p, 3) for p, q in zip(sorted(found), sorted(found)[1:]) if q - p < b.apart - 1e-6]
        if close:
            problems.append(f"the {what}s stand {close} apart, closer than {b.apart:g}")
    return problems


# -- the summary, in the cabinet's own frame ---------------------------------------------------------

def _world(x: Board, op: Hole) -> dict[Axis, float]:
    """A hole's centre where it enters its face, in world coordinates."""
    direction = world_frame().direction(op.face)
    box = x.box()
    plane = box.hi[direction.axis] if direction.sign > 0 else box.lo[direction.axis]
    return {x.u_axis: op.u, x.v_axis: op.v, direction.axis: plane}


def _summary(b: Built) -> list[tuple[Any, ...]]:
    """What the boards and the hardware are, measured inward from the
    cabinet's own front, left and bottom faces: boxes as (lo, hi) per
    measure, holes by centre and the face's measure and sign."""
    dirs: list[Direction] = [b.cab.front.outward, b.cab.left.outward, b.cab.bottom.outward]

    def local(p: dict[Axis, float]) -> tuple[float, ...]:
        out: list[float] = []
        for d in dirs:
            face = b.box.hi[d.axis] if d.sign > 0 else b.box.lo[d.axis]
            out.append(d.sign * (face - p[d.axis]))
        return tuple(out)

    def local_box(lo: dict[Axis, float], hi: dict[Axis, float]) -> tuple[tuple[float, float], ...]:
        a, c = local(lo), local(hi)
        return tuple((min(p, q), max(p, q)) for p, q in zip(a, c))

    def facing(name: str) -> tuple[int, int]:
        d = world_frame().direction(name)
        i = next(k for k, e in enumerate(dirs) if e.axis == d.axis)
        return i, d.sign * dirs[i].sign

    out: list[tuple[Any, ...]] = []
    for x in b.boards:
        bx = x.box()
        out.append(("board", x.name, local_box(dict(bx.lo), dict(bx.hi)), round(x.outline.area, 6)))
        for op in x.ops:
            if isinstance(op, Hole):
                out.append(("hole", x.name, op.name, local(_world(x, op)), facing(op.face), op.d, op.depth,
                            op.chamfer, op.through))
            elif isinstance(op, (Cut, Pocket)):
                u0, v0, u1, v1 = op.shape.geometry.bounds
                t = x.t_axis
                lo = {x.u_axis: u0, x.v_axis: v0, t: bx.lo[t]}
                hi = {x.u_axis: u1, x.v_axis: v1, t: bx.hi[t]}
                depth = op.depth if isinstance(op, Pocket) else None
                out.append((op.kind, x.name, op.name, local_box(lo, hi), depth))
            elif isinstance(op, EdgeOp):
                out.append(("edge", x.name, op.op.name))
            else:
                out.append((op.kind, x.name, getattr(op, "name", None)))
    for item in b.cab.all_hardware():
        for body in item["bodies"]:
            for k, bb in enumerate(body["boxes"]):
                lo: dict[Axis, float] = {a: v for a, v in zip(AXES, bb["min"])}
                hi: dict[Axis, float] = {a: v for a, v in zip(AXES, bb["max"])}
                out.append(("hardware", item["name"], body["name"], k, local_box(lo, hi)))
    if b.unnamed:
        out = sorted((_unnamed(item) for item in out), key=repr)
    return out


def _unnamed(item: tuple[Any, ...]) -> tuple[Any, ...]:
    """A hole or a hardware body without its name, rounded so that it sorts
    alike both ways."""
    if item[0] == "hole":
        return item[:2] + (None,) + tuple(_rounded(v) for v in item[3:])
    if item[0] == "hardware":
        return item[:2] + (None,) + tuple(_rounded(v) for v in item[3:])
    return item


def _rounded(v: Any) -> Any:
    if isinstance(v, float):
        return round(v, 5) + 0.0
    if isinstance(v, tuple):
        return tuple(_rounded(x) for x in v)
    return v


def _difference(a: list[tuple[Any, ...]], b: list[tuple[Any, ...]]) -> str | None:
    """The first item that differs, give or take 1e-6 mm, or None."""
    if len(a) != len(b):
        return f"{len(a)} items against {len(b)}"
    for p, q in zip(a, b):
        if not _close(p, q):
            return f"{p} against {q}"
    return None


def _close(p: Any, q: Any) -> bool:
    if isinstance(p, float) and isinstance(q, float):
        return math.isclose(p, q, abs_tol=1e-6)
    if isinstance(p, tuple) and isinstance(q, tuple):
        return len(p) == len(q) and all(_close(x, y) for x, y in zip(p, q))
    return p == q


def apply(case: Case, name: str) -> None:
    """Builds the case as cabinet `name`, facing as it says, and mounts its
    hardware: for the Fusion batch check (`fusion_batch.py hardware`)."""
    BUILDERS[type(case)](case, case.front, case.origin, name).mount()


def accepted(case: Case) -> bool:
    """Whether the case's mount is accepted and keeps every promise."""
    return not run_case(case) and _attempt(case, case.front, case.origin)[1][0] == "accepted"


def hardware_cases() -> st.SearchStrategy[Case]:
    return st.one_of(door_cases(), panel_cases(), hatch_cases(), catch_cases(), drawer_cases())


__all__ = ["CatchCase", "DoorCase", "DrawerCase", "HatchCase", "PanelCase", "accepted", "apply", "catch_cases",
           "door_cases", "drawer_cases", "hardware_cases", "hatch_cases", "panel_cases", "run_case"]
