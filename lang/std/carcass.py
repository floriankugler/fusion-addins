"""A carcass: two sides, a bottom and a top between them, and a back
between all four, placed and joined as every cabinet in `examples/`
writes them, so that a build file says `carcass(cab, ply15, back=ply9)`
instead of eight lines [decided by Florian, 2026-10-15, syntax.md item 2].
"""
from __future__ import annotations

from typing import NamedTuple, overload

from lang import Board, Face, Joint, LangError, Pos, Scope, SheetMaterial, Side, board, cabineo, domino, rect

#: What limits a carcass at its front: a position or a side
#: (`cab.front.into(12)`, the carcass behind a door), a part's face, or a
#: board standing in front of it (a hatch).
Front = Board | Side | Face | Pos


class Carcass(NamedTuple):
    """The five boards of a carcass with a back, in the order they are
    made: `left, right, bottom, top, back = carcass(...)`."""
    left: Board
    right: Board
    bottom: Board
    top: Board
    back: Board


class OpenCarcass(NamedTuple):
    """The four boards of a carcass without a back (`back=None`)."""
    left: Board
    right: Board
    bottom: Board
    top: Board


@overload
def carcass(scope: Scope, material: SheetMaterial, *, back: SheetMaterial, front: Front | None = None,
            toekick: tuple[float, float] | None = None, joins: Joint | None = None,
            back_joins: Joint | None = None) -> Carcass: ...


@overload
def carcass(scope: Scope, material: SheetMaterial, *, back: None = None, front: Front | None = None,
            toekick: tuple[float, float] | None = None, joins: Joint | None = None) -> OpenCarcass: ...


def carcass(scope: Scope, material: SheetMaterial, *, back: SheetMaterial | None = None,
            front: Front | None = None, toekick: tuple[float, float] | None = None,
            joins: Joint | None = None, back_joins: Joint | None = None) -> Carcass | OpenCarcass:
    """The carcass of `scope`, a cabinet or module with a box: the sides
    `left` and `right` on the box's sides, `bottom` and `top` on its bottom
    and top between them, and `back` on its back between all four, of
    `material` but for the back, of `back` (None: no back). `front=` limits
    the sides, the bottom and the top at the front, where a door or a hatch
    stands (`cab.front.into(ply12.thickness)`, or the hatch itself);
    without it the box does. `toekick=(depth, height)` notches both sides at
    `side.outer.bottom.front`, named `toekick`, and puts the bottom on the
    notch. `joins` joins the bottom and the top to the sides, `cabineo(count=2)`
    unless given; `back_joins` the back to all four, `domino("4x20", count=2)`
    unless given. The boards are made and joined in that order, which is
    the order of their operations."""
    left = board("left", material).on(scope.left)
    right = board("right", material).on(scope.right)
    if front is not None:
        left.between(front)
        right.between(front)
    if toekick is not None:
        depth, height = toekick
        for side in (left, right):
            side.cut(rect(depth=depth, height=height), at=side.outer.bottom.front, name="toekick")
        bottom = board("bottom", material).on(left.toekick.top, toward=scope.top)
    else:
        bottom = board("bottom", material).on(scope.bottom)
    top = board("top", material).on(scope.top)
    if front is None:
        bottom.between(left, right)
        top.between(left, right)
    else:
        bottom.between(left, right, front)
        top.between(left, right, front)
    rear = None
    if back is not None:
        rear = board("back", back).on(scope.back).between(left, right, bottom, top)
    elif back_joins is not None:
        raise LangError("carcass(): back_joins= given, but back=None makes no back to join.", scope.path)
    joint = joins if joins is not None else cabineo(count=2)
    bottom.join(left, right, using=joint)
    top.join(left, right, using=joint)
    if rear is None:
        return OpenCarcass(left, right, bottom, top)
    rear.join(left, right, bottom, top, using=back_joins if back_joins is not None else domino("4x20", count=2))
    return Carcass(left, right, bottom, top, rear)
