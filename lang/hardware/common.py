"""What the hardware modules share: one tolerance and one way to write a
length in a message, the numbering along an edge, a box of a bought part
in world coordinates, and the checks every mount makes of its holes.

Every mount works out all its holes and boxes first, checks them all with
`check_hole` and `check_pilot_depth` (on top of its own rules), and only
then drills and places, so a refused mount changes nothing.
"""
from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from ..core import directions
from ..core.box import Box
from ..core.directions import AXES, Axis, Direction
from ..core.errors import LangError
from ..core.layout_types import BoxDict

if TYPE_CHECKING:
    from ..core.part import Board, Face

#: Geometric tolerance of the hardware's checks, mm (the add-ins' 1e-4 cm).
TOLERANCE = 1e-3
Point2 = tuple[float, float]
#: Two ends of a box along one direction, mm.
Extent = tuple[float, float]
#: A box in a bought part's own frame: its extents along three directions,
#: which each hardware names (`world_box`).
LocalBox = tuple[Extent, Extent, Extent]


def mm(value: float) -> str:
    """A length for messages, as the add-ins write it: `24.5 mm`, `18 mm`."""
    return f"{value:.1f}".rstrip("0").rstrip(".") + " mm"


def middle(box: Box, axis: Axis) -> float:
    return (box.lo[axis] + box.hi[axis]) / 2


def uv(board: Board, coords: Mapping[Axis, float]) -> Point2:
    """A world point, given on (at least) the board's in-plane axes, in the
    frame of its outline and big faces."""
    return (coords[board.u_axis], coords[board.v_axis])


def world_box(starts: Sequence[tuple[Direction, float]], box: LocalBox) -> BoxDict:
    """A box of a bought part in world coordinates: each of its three
    extents measured along a direction from a world position."""
    lo, hi = [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]
    for (direction, start), (a, b) in zip(starts, box):
        i = AXES.index(direction.axis)
        lo[i], hi[i] = sorted((start + direction.sign * a, start + direction.sign * b))
    return {"min": lo, "max": hi}


def along(axis: Axis) -> Direction:
    """The positive direction of a world axis, for `world_box`."""
    return directions.world_frame().direction_of(axis, 1)


def numbering(back: Direction, edge: Axis) -> int:
    """Which way hardware is numbered along an edge on the `edge` axis, +1
    toward the axis' positive end or -1: from the bottom up on an upright
    edge; along a level edge from the part's own left to its right, seen
    standing in front of it (its right is back x up, `back` pointing from
    the part to the board it hangs on); for a part lying flat, toward the
    world axis' positive end. Physical, so a module in the van's terms and
    a cabinet with `front=` number alike."""
    up = directions.world_frame().direction("top")
    if edge == up.axis:
        return up.sign
    if back.axis == up.axis:
        return 1
    return directions.world_frame().cross(back, up).sign


def check_hole_size(label: str, what: str, size: tuple[float, float]) -> tuple[float, float]:
    """A hole's (diameter, depth) as given to a hardware's constructor,
    both greater than zero."""
    diameter, depth = size
    if diameter <= 0 or depth <= 0:
        raise LangError(f"{label}: {what}= needs a diameter and a depth greater than zero, not "
                        f"{diameter:g} x {depth:g}.")
    return (float(diameter), float(depth))


def check_pilot_depth(label: str, board: Board, depth: float, what: str) -> None:
    """A fixed-depth hole for a screw or a pin must stop short of the
    board's far face: an error when it is as deep as the board is thick
    (core refuses only deeper ones)."""
    if depth >= board.thickness - TOLERANCE:
        raise LangError(f"{label}: the {what} depth ({mm(depth)}) must be less than {board.path}'s thickness "
                        f"({mm(board.thickness)}).", board.path)


def check_hole(label: str, board: Board, face: Face, point: Point2, d: float, what: str) -> None:
    """An error when the hole does not fit on the face (`Board.hole_fits`):
    off the board or its edge, or in a hole or pocket made before."""
    if not board.hole_fits(face, point, d):
        raise LangError(f"{label}: the {what} ({mm(d)}) does not fit on {board.path}'s {face.name} face: it lies "
                        "off the board, over its edge, or in a hole or pocket made before.", board.path)
