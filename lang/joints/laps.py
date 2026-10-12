"""Half laps: two boards that cross each other (`lang.core.crossing`), each
notched to half the height they share, so they slot together flush.

`long.join(battens, using=half_lap(toward=floor.top))` laps the board with
each board named, all of which it must cross: its own notches open toward
the given side, the other boards' notches the opposite way. The
split lies in the middle of the height both boards have at the crossing,
or at `at=`, a position. `clearance=` widens every notch by that much on
each side. Each notch is a through cut named `lap_<other board>`.

A router leaves its radius in a notch's two inside corners, at its floor,
so they get dog bones for a `tool=` mm cutter, `relief=` wider than the
tool, as part of the notch's cut: `dogbones="corner"` (the default) on each
corner's bisector, as tenons and the dog_bones_native add-in make them
(`lang.core.dogbones`); `"hidden"` along the floor, touching the notch's
side and bulging past the floor into the part of the crossing that stays
this board's, where the other board covers it on both faces; None for
none. A corner without material around it (a notch flush with the board's
end) gets none.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

from shapely.geometry import Point

from ..core.box import Box
from ..core.crossing import Crossing, crossing
from ..core.directions import AXES, Axis, Direction
from ..core.dogbones import DogBones, corner_relief, hidden_relief
from ..core.errors import LangError, one_of
from ..core.part import Board
from ..core.refs import PosLike, Side, as_pos
from ..core.shapes import Shape, box_shape
from .common import PROBE, Point2, reported

#: How far a notch reaches past the board's edge, so it opens cleanly.
_PAST = 1.0


@dataclass(frozen=True)
class HalfLap:
    toward: Direction
    at: float | None = None
    clearance: float = 0.0
    dogbones: DogBones | None = "corner"
    tool: float = 6.0
    relief: float = 0.1
    label: ClassVar[str] = "half_lap"

    @property
    def radius(self) -> float:
        """The dog bones' radius at a square corner: the tool's plus half the relief."""
        return (self.tool + self.relief) / 2

    def join(self, part: Board, /, partners: list[Board]) -> None:
        # Every crossing is checked and every notch worked out before any
        # board is cut, each against the outline the notches before it leave.
        laps: list[tuple[Board, Crossing, float]] = []
        for other in partners:
            with reported(self.label, part, other):
                c = crossing(part, other)
                if c is None:
                    raise LangError("the two do not cross.")
                laps.append((other, c, self._split(c)))
        outlines: dict[int, Shape] = {}
        notches: list[tuple[Board, Board, Shape, str]] = []
        for other, c, split in laps:
            d = self.toward
            pb, ob = part.box(), other.box()
            low = min(pb.lo[c.axis], ob.lo[c.axis]) - _PAST
            high = max(pb.hi[c.axis], ob.hi[c.axis]) + _PAST
            # This board's notch opens toward `toward`, the other's the other way.
            mine = (split, high) if d.sign > 0 else (low, split)
            theirs = (low, split) if d.sign > 0 else (split, high)
            for board, across, span, opens in ((part, other, mine, d.sign), (other, part, theirs, -d.sign)):
                outline = outlines.get(id(board), board.outline)
                with reported(self.label, part, other):
                    shape = self._notch(board, across, c.axis, span, split, opens, outline)
                outlines[id(board)] = outline.difference(shape)
                notches.append((other, board, shape, f"lap_{across.name}"))
        for other, board, shape, name in notches:
            with reported(self.label, part, other):
                board.add_cut(shape, name=board.unique_op_name(name))

    def _split(self, c: Crossing) -> float:
        if self.toward.axis != c.axis:
            raise LangError(f"toward={self.toward.name} does not run along the line where the two meet ({c.axis}).")
        split = self.at if self.at is not None else (c.lo + c.hi) / 2
        if not c.lo < split < c.hi:
            raise LangError(f"the split at {c.axis}={split:g} lies outside the height the two share "
                            f"({c.lo:g} to {c.hi:g}).")
        return split

    def _region(self, part: Board, other: Board, axis: Axis, span: tuple[float, float]) -> Box:
        """The region cut from `part`: through its thickness, as wide as
        `other` is thick (plus the clearance), over `span` along `axis`."""
        pb, ob = part.box(), other.box()
        t, w = part.t_axis, other.t_axis
        lo: dict[Axis, float] = {t: pb.lo[t], w: ob.lo[w] - self.clearance, axis: span[0]}
        hi: dict[Axis, float] = {t: pb.hi[t], w: ob.hi[w] + self.clearance, axis: span[1]}
        return Box({a: lo[a] for a in AXES}, {a: hi[a] for a in AXES})

    def _notch(self, part: Board, other: Board, axis: Axis, span: tuple[float, float], split: float,
               opens: int, outline: Shape) -> Shape:
        """The notch for `other` in `part`'s outline frame, with a dog bone
        in each corner at its floor, `split` on `axis`; it opens toward
        `opens` (+1 or -1) along `axis`. `outline` is the board's material
        before it."""
        box = self._region(part, other, axis, span)
        u, v, w = part.u_axis, part.v_axis, other.t_axis
        notch = box_shape(box.lo[u], box.lo[v], box.hi[u], box.hi[v])
        if self.dogbones is None:
            return notch

        def at(across: float, along: float) -> Point2:
            coords: dict[Axis, float] = {w: across, axis: along}
            return (coords[u], coords[v])

        width = box.hi[w] - box.lo[w]
        r = self.radius
        if self.dogbones == "hidden" and width < 2 * r - 1e-9:
            raise LangError(f"hidden dog bones are {2 * r:g} across, wider than the notch in {part.path} "
                            f"({width:g}); use corner dog bones or a smaller tool.")
        material = outline.geometry
        up = at(0.0, float(opens))                       # along the notch's sides, toward its opening
        for edge, inward in ((box.lo[w], 1.0), (box.hi[w], -1.0)):
            corner = at(edge, split)
            around = [at(edge - inward * PROBE, split + opens * PROBE),    # beside the notch
                      at(edge - inward * PROBE, split - opens * PROBE),    # beside and below its floor
                      at(edge + inward * PROBE, split - opens * PROBE)]    # below its floor
            if not all(material.contains(Point(p)) for p in around):
                continue                                 # not an inside corner of the material
            floor = at(inward, 0.0)                      # along the floor, into the notch
            if self.dogbones == "corner":
                notch = notch.union(corner_relief(corner, floor, up, self.tool, self.relief))
                continue
            relief = hidden_relief(corner, floor, self.tool, self.relief)
            if not material.contains(Point(at(edge + inward * r, split - opens * (r + PROBE)))):
                raise LangError(f"hidden dog bones would break out of {part.path} below its notch; use corner dog "
                                "bones or a smaller tool.")
            notch = notch.union(relief)
        return notch


def half_lap(toward: Side | Direction, at: PosLike | None = None, clearance: float = 0.0,
             dogbones: DogBones | None = "corner", tool: float = 6.0, relief: float = 0.1) -> HalfLap:
    """A half lap with each board named in `join()`. `toward` is the side this
    board's notches open to (`floor.top`: notched from the top, the other
    boards from below); `at` a position for the split instead of the middle
    of the shared height; `clearance` widens each notch per side. Dog bones
    for a `tool` mm cutter, `relief` wider, in the notches' inside corners:
    on the corners (`"corner"`), along the floor where the other board
    covers them (`"hidden"`), or None."""
    direction = toward.outward if isinstance(toward, Side) else toward
    split = as_pos(at, "half_lap(at=)") if at is not None else None
    if split is not None and split.axis != direction.axis:
        raise LangError(f"half_lap: at={split} is not on the axis of toward={direction.name}.")
    if clearance < 0:
        raise LangError("half_lap: clearance must not be negative.")
    if dogbones is not None:
        one_of(dogbones, DogBones, "half_lap(dogbones=)")
    if tool <= 0:
        raise LangError("half_lap: tool must be positive.")
    if relief < 0:
        raise LangError("half_lap: relief must not be negative.")
    return HalfLap(direction, split.value if split is not None else None, float(clearance), dogbones,
                   float(tool), float(relief))
