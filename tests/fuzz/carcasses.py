"""Random carcasses for fuzzing the standard library's `carcass()`
(`lang.std`): a case is the cabinet's size, its sheet thicknesses, what
stands at its front, its toe kick and its joint counts, drawn from the
examples' ranges and a little beyond. It is built facing two sides of
its box at two places, as `hardware.py` builds its cabinets, and what
`carcass()` promises is checked from the outside: five (or four) boards
that share no material and lie inside the box, the bottom on the toe
kick, the sides, bottom and top ending at the front limit, and the same
result measured from the cabinet's own sides whichever way it faces; a
refusal must be one both ways.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from hypothesis import strategies as st

from fuzzing import fresh, sizes
from hardware import FRONTS, _box, _origin, _thickness  # pyright: ignore[reportPrivateUsage]
from lang import Board, LangError, Scope, board, cabineo, check, domino, inside_box, module, sheet_material
from lang.core.layout import build_layout
from lang.std import carcass

FrontKind = Literal["box", "into", "board"]


@dataclass(frozen=True)
class CarcassCase:
    size: tuple[float, float, float]
    t: float
    back_t: float | None
    front_kind: FrontKind
    front_in: float
    toekick: tuple[float, float] | None
    joins: int
    back_joins: int
    front: int
    turn: int
    origin: tuple[float, float, float]
    origin2: tuple[float, float, float]


@st.composite
def carcass_cases(draw: st.DrawFn) -> CarcassCase:
    w, d, h = draw(sizes(300, 1500)), draw(sizes(300, 800)), draw(sizes(300, 2000))
    toekick = draw(st.one_of(st.none(), st.tuples(sizes(10, min(150, d / 3)), sizes(10, min(200, h / 3)))))
    return CarcassCase(
        size=(w, d, h), t=draw(_thickness()), back_t=draw(st.one_of(st.none(), _thickness())),
        front_kind=draw(st.sampled_from(("box", "into", "board"))), front_in=draw(sizes(0.5, 60)),
        toekick=toekick, joins=draw(st.integers(1, 3)), back_joins=draw(st.integers(1, 3)),
        front=draw(st.integers(0, 3)), turn=draw(st.integers(1, 3)), origin=draw(_origin()), origin2=draw(_origin()))


Summary = list[tuple[str, tuple[float, ...], int, float]]


def _build(case: CarcassCase, front: int, origin: tuple[float, float, float]) -> tuple[str, Summary | str, list[str]]:
    """Builds the case facing `FRONTS[front]` at `origin`: ("refused",
    message, []) or ("built", summary, problems)."""
    box = _box(case.size, front, origin)
    ply = sheet_material("birch", t=case.t)
    problems: list[str] = []
    with fresh():
        with module("cab", box, front=getattr(box, FRONTS[front])) as cab:
            check(inside_box)
            door: Board | None = None
            limit = None
            if case.front_kind == "into":
                limit = cab.front.into(case.front_in)
            elif case.front_kind == "board":
                door = board("door", ply).on(cab.front)
                limit = door
            try:
                if case.back_t is None:
                    c = carcass(cab, ply, front=limit, toekick=case.toekick, joins=cabineo(count=case.joins))
                    boards = list(c)
                else:
                    c = carcass(cab, ply, back=sheet_material("birch", t=case.back_t), front=limit,
                                toekick=case.toekick, joins=cabineo(count=case.joins),
                                back_joins=domino("4x20", count=case.back_joins))
                    boards = list(c)
            except LangError as e:
                return "refused", str(e), []
            names = [b.name for b in boards]
            if names != (["left", "right", "bottom", "top"] if case.back_t is None else
                         ["left", "right", "bottom", "top", "back"]):
                problems.append(f"the boards are {names}")
            bottom = boards[2]
            if case.toekick is not None:
                lift = bottom.bottom.value - cab.bottom.value
                if abs(lift - case.toekick[1]) > 1e-6:
                    problems.append(f"the bottom lies {lift:g} above the box's bottom, the toe kick is {case.toekick[1]:g} high")
                for side in boards[:2]:
                    if not side.has_operation("toekick"):
                        problems.append(f"{side.path} has no toekick")
            if limit is not None:
                want = door.back.value if door is not None else cab.front.into(case.front_in).value
                for b in boards[:4]:
                    if abs(b.front.value - want) > 1e-6:
                        problems.append(f"{b.path} ends at {b.front.value:g} in front, the limit is at {want:g}")
            if case.back_t is not None:
                back = boards[4]
                # the back's edges lie on the other four's inner faces
                for b, own, inner in ((boards[0], "left", "right"), (boards[1], "right", "left"),
                                      (boards[2], "bottom", "top"), (boards[3], "top", "bottom")):
                    if abs(back.face(own).value - b.face(inner).value) > 1e-6:
                        problems.append(f"the back's {own} is not on {b.path}'s {inner}")
        layout = build_layout()
        problems += layout["problems"]
        return "built", _summary(cab), problems


def _summary(cab: Scope) -> Summary:
    """Each part by name: its box's distances from the cabinet's six sides
    in the cabinet's own frame, its operation count and its outline's
    area, so two builds facing different ways compare."""
    cb = cab.box
    assert cb is not None
    out: Summary = []
    for p in cab.all_parts():
        pb = p.box().in_frame(cab.frame)
        dists = tuple(round(abs(pb.side(d).value - cb.side(d).value), 6)
                      for d in ("front", "back", "left", "right", "top", "bottom"))
        out.append((p.name, dists, len(p.ops), round(p.outline.geometry.area, 6)))
    return sorted(out)


def run_case(case: CarcassCase) -> list[str]:
    """What is wrong with the case, built facing two ways."""
    status1, result1, problems1 = _build(case, case.front, case.origin)
    other = (case.front + case.turn) % 4
    status2, result2, problems2 = _build(case, other, case.origin2)
    problems = problems1 + problems2
    if status1 != status2:
        problems.append(f"facing {FRONTS[case.front]} it is {status1}, facing {FRONTS[other]} {status2}: "
                        f"{result1 if status1 == 'refused' else result2}")
    elif status1 == "built" and result1 != result2:
        problems.append(f"facing {FRONTS[other]} instead of {FRONTS[case.front]} it comes out otherwise: "
                        f"{result1} vs {result2}")
    return problems
