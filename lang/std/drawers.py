"""A drawer box behind its face, sized by its slide, joined at its
corners, its floor in grooves, machined for the slide and mounted on the
carcass, so that the slide's three calls (`slide.drawer_box()`,
`slide.machine_box()`, `scope.mount(slide, ...)`) are written here once
[decided by Florian, 2026-10-15, syntax.md item 3].
"""
from __future__ import annotations

from collections.abc import Sequence
from typing import NamedTuple

from lang import Board, Box, DrawerSlide, Face, Joint, Pos, Scope, SheetMaterial, Side, board


class DrawerBox(NamedTuple):
    """The five boards of a drawer box and the box they fill."""
    left: Board
    right: Board
    front: Board
    back: Board
    floor: Board
    box: Box


def drawer_box(scope: Scope, bay: Box, slide: DrawerSlide, *, front: Face | Side | Pos, height: float,
               material: SheetMaterial, floor: SheetMaterial, corners: Joint | None, floor_joint: Joint | None,
               carcass: Sequence[Board]) -> DrawerBox:
    """The drawer box in `bay`, the drawer's scope, behind `front` (the
    face's back), `height` high, of `material` with a `floor`: the slide
    sizes it (`slide.drawer_box`), `left` and `right` run its full length,
    `front` and `back` stand between them and are joined to them with
    `corners` (a `box_joint()`, or None for corners left to the shop), the
    floor lies `slide.recess` above the box's bottom and is joined to all
    four with `floor_joint` (a `groove()`, or None), the slide machines the
    box (`slide.machine_box`: the couplings' and hooks' cut-outs and the
    hook holes) and is mounted on `scope` with its runners on the two
    `carcass` boards, which it pre-drills."""
    box = slide.drawer_box(bay, front=front, side_thickness=material.thickness, height=height)
    left = board("left", material).on(box.left).between(box)
    right = board("right", material).on(box.right).between(box)
    end_front = board("front", material).on(box.front).between(left, right, box.bottom, box.top)
    end_back = board("back", material).on(box.back).between(left, right, box.bottom, box.top)
    if corners is not None:
        for end in (end_front, end_back):
            end.join(left, right, using=corners)
    panel = board("floor", floor).on(box.bottom.into(slide.recess)).between(left, right, end_front, end_back)
    if floor_joint is not None:
        panel.join(left, right, end_front, end_back, using=floor_joint)
    slide.machine_box(sides=(left, right), front=end_front, back=end_back, floor=panel)
    scope.mount(slide, sides=carcass, front=front)
    return DrawerBox(left, right, end_front, end_back, panel, box)
