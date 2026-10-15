"""Sliding brackets (Häfele Pacofix, the same parts as Keku AS) that hold
a removable panel on frame boards, as hardware.

The panel and each frame board stand square to each other, the panel's
back face against the frame board's front edge or a little in front of
it, or the frame boards reaching past it with the panel set in between
them.
`cab.mount(sliding_bracket(), panel=cover, frame=[left, right])` hangs the
panel on each frame board named and drills both parts as
`lib.sliding_brackets` has them: the frame part's two holes into the
frame board's inner face (the big face toward the panel's middle, or the
face named: `frame=[partition.left]`), the panel part's two holes into
the panel's back face (the big face toward the frame board), each pair 32
apart along the edge. Where they go depends on the frame part:

- `"Pacofix PF-L-R"`, the bent one and the default: the frame holes 8
  behind the panel's back face, where the frame part's plate begins, the
  panel holes 19 out from the frame board's face (the tongue lies on the
  frame part's plate). The panel's back face may stand up to 3 mm in
  front of the frame board's edge, the plate hanging over the edge by
  that gap and the holes 8 - gap from it.
- `"Pacofix PF-L"`, the straight one: the frame holes 37 behind the
  panel's back face, the System 32 line, whatever the gap (up to 29,
  where the plate begins); the panel holes 15 out from the frame board's
  face, where the tongue lies.

The gap is read from the model, never given. The holes are `"pilot"`
holes for chipboard screws (Ø2 x 6) unless `frame_hole=` or
`panel_hole=` say `"euro"` (Ø5, for 6.3 mm Euro screws and the parts
made for them, 11 deep but 2 short of the board's far face at most: 10
on a 12 mm board) or give (diameter, depth). Per frame board `count`
brackets (2) sit along the stretch the panel and the frame board share,
the outer ones' centres `end` (50) from its ends, the rest evenly
between, one alone in the middle (`lib.stations`); `at=` takes positions
along the edge instead, the same on every frame board named. Brackets are
numbered on through the frame boards in the order `frame=` names them,
on each by their place along the edge: from the bottom, or from the
panel's own left, seen standing in front of it.

It refuses, before it drills anything: a frame board parallel to the
panel, a frame board whose edge lies further behind the panel's back
face than the gap allows (3 for the PF-L-R, 29 for the PF-L) or that
ends before the plate does (29 and 45 behind it), a panel that stops
more than 3 mm short of where the panel part's plate begins (it hangs
over the edge of a panel set in between), plates that do not lie on
their boards (the outline, less the pockets made into the face; the
part over a gap hangs free) or overlap each other, holes that do not fit
on their face (`Board.hole_fits`: off it, or in another hole or pocket),
and holes as deep as a board is thick; `end` under half a plate (24). The makers' advice (Keku: at least
four per panel, at most 600 apart; Häfele: no hanging loads such as
ceiling panels) is left to the build and not checked.

Each latched pair is one body of four boxes (`BRACKET_SHAPES`, measured
on Häfele's CAD models): the frame part's plate and its hook, the panel
part's plate and its tongue, which lies under the hook. They are placed
as `<panel>_brackets`, bodies named by the bracket's number (`bracket_1`).
Operations are named by the other board and the bracket's number:
`bracket_cover_1a` and `_1b` in the frame board, `bracket_left_1a` in the
panel.
"""
from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal

from shapely.geometry import box as shapely_box
from shapely.geometry.base import BaseGeometry
from shapely.ops import unary_union

from lib import sliding_brackets as data

from ..core.directions import AXES, Axis
from ..core.errors import LangError, one_of
from ..core.layout_types import BoxDict, HardwareBodyLayout
from ..core.ops import Pocket
from ..core.part import Board, Face
from ..core.refs import PosLike
from ..joints.common import make_spacing
from .common import (TOLERANCE, LocalBox, Point2, along, check_hole, check_hole_size, check_pilot_depth, middle, mm,
                     numbering, uv, world_box)

if TYPE_CHECKING:
    from ..core.scope import Scope

#: The brackets of `lib.sliding_brackets`, by name: the frame part, bent or
#: straight, with the panel part PF.
BracketModel = Literal["Pacofix PF-L-R", "Pacofix PF-L"]
#: The holes of one part: for chipboard screws or for Euro screws, as
#: `lib.sliding_brackets` sizes them, or (diameter, depth) in mm.
HoleChoice = Literal["pilot", "euro"]
BracketHole = HoleChoice | tuple[float, float]

#: A box of a latched bracket, mm: its extents out from the frame board's
#: face (toward the panel's middle), back from the panel's back face (away
#: from the panel) and along the edge from the bracket's centre.
BracketBox = LocalBox


@dataclass(frozen=True)
class BracketShape:
    """A latched bracket as boxes in its frame (`BracketBox`): the space
    it takes, not its detail. The two parts interlock, the hook lying in
    the tongue's channel, so a bracket is one body. The drilling data
    stays in `lib.sliding_brackets`."""
    #: On the frame board's face: the plate, and the hook with its spine.
    frame_part: tuple[BracketBox, ...]
    #: On the panel's back face: the plate, and the tongue on the frame
    #: board's face or on the frame part's plate.
    panel_part: tuple[BracketBox, ...]

    def boxes(self) -> list[BracketBox]:
        return [*self.frame_part, *self.panel_part]


#: Per model, measured on Häfele's CAD models (glTF, 2026-10-12) of the
#: panel part 262.50.359 and the frame parts 262.50.390 (PF-L-R) and
#: 262.50.368 (PF-L), fitted together latched. The panel part: its plate
#: 23 out from the tongue's side, 4 thick, 48 long; its tongue 10 high,
#: 22.1 wide, 29 back from the panel. PF-L-R: the plate 4 thick from the
#: panel's back face to 33 behind it (the last 4 rounded underneath, its
#: far corners cut off), 48 long; the hook bent back over it, 16 wide,
#: 10.05 to 14 off the board, from its closed end at 33 to its free end
#: 9.1 behind the panel; the tongue lies on the plate, 4 to 14 off the
#: board, its tip in the hook's closed end. PF-L: the plate 4 thick, 16
#: across its holes, 48 long; its hook 16 wide, from the plate's top up to
#: 10.2 off the board and from the plate to 28 in front of its holes, its
#: lip dipping to 4.5 inside the tongue's channel (the box covers the
#: spine that ramps up along the plate); the tongue on the frame board's
#: face, back to the frame part's plate.
BRACKET_SHAPES: dict[str, BracketShape] = {
    data.PACOFIX_PF_L_R.name: BracketShape(
        frame_part=(((0.0, 4.0), (0.0, 33.0), (-24.0, 24.0)),        # plate
                    ((4.0, 14.0), (9.1, 33.0), (-8.0, 8.0))),        # bent hook
        panel_part=(((4.0, 27.0), (0.0, 4.0), (-24.0, 24.0)),        # plate
                    ((4.0, 14.0), (4.0, 29.0), (-11.05, 11.05))),    # tongue
    ),
    data.PACOFIX_PF_L.name: BracketShape(
        frame_part=(((0.0, 4.0), (29.0, 45.0), (-24.0, 24.0)),       # plate
                    ((4.0, 10.2), (9.0, 45.0), (-8.0, 8.0))),        # hook and spine
        panel_part=(((0.0, 23.0), (0.0, 4.0), (-24.0, 24.0)),        # plate
                    ((0.0, 10.0), (4.0, 29.0), (-11.05, 11.05))),    # tongue
    ),
}


@dataclass(frozen=True)
class _Edge:
    """Where the panel hangs on one frame board, in world terms."""
    frame: Board
    #: The frame board's face the frame parts go on; its outward normal
    #: points out, toward the panel's middle.
    frame_face: Face
    #: The panel's face toward the frame board; its outward normal points
    #: back, away from the panel.
    back_face: Face
    #: The axis the edge runs along.
    along: Axis
    #: The brackets' centres along it, in the order they are numbered.
    stations: tuple[float, ...]
    #: The number of the first of them.
    first: int
    #: +1 or -1: the direction they are numbered in along `along`.
    order: int
    #: From the panel's back face to the frame board's edge, back; negative
    #: where the frame board reaches past it (a panel set in between).
    gap: float
    #: How far the panel stops short of the frame board's face, out; 0 or
    #: less where it reaches over it.
    clearance: float

    def point(self, out: float, back: float, along: float) -> dict[Axis, float]:
        """A world point `out` from the frame board's face, `back` from the
        panel's back face, at `along` on the edge's axis."""
        f, b = self.frame_face, self.back_face
        return {f.axis: f.value + f.direction.sign * out, b.axis: b.value + b.direction.sign * back,
                self.along: along}

    def world_box(self, s: float, box: BracketBox) -> BoxDict:
        """A bracket box in world coordinates, the bracket centred at `s`."""
        f, b = self.frame_face, self.back_face
        return world_box(((f.direction, f.value), (b.direction, b.value), (along(self.along), s)), box)


class SlidingBracket:
    """Sliding brackets of one model (the bent PF-L-R frame part unless
    `model` says `"Pacofix PF-L"`) with their placement and holes:
    `count` per frame board, the outer ones `end` from the ends of the
    stretch the panel and the frame board share, or one at each position
    of `at` along the edge; `frame_hole` and `panel_hole` are the holes in
    the frame board and the panel: `"pilot"` (Ø2 x 6), `"euro"` (Ø5 x 11,
    2 short of the board's far face at most) or (diameter, depth) in mm."""

    def __init__(self, model: BracketModel = "Pacofix PF-L-R", *, count: int | None = None,
                 end: float = data.DEFAULT_END_OFFSET, at: Sequence[PosLike] | None = None,
                 frame_hole: BracketHole = "pilot", panel_hole: BracketHole = "pilot"):
        self.spec = data.BRACKETS[one_of(model, BracketModel, "sliding_bracket()")]
        #: The boxes the brackets are drawn as.
        self.shape = BRACKET_SHAPES[model]
        # end= has a default here, so it is checked below, not by make_spacing
        spacing = make_spacing(self.name, data.DEFAULT_COUNT if count is None and at is None else count, at,
                               default_end=end)
        if end < 0:
            raise LangError(f"{self.name}: end must not be negative.")
        half = self.spec.plate_length / 2
        if spacing.at is None and spacing.count != 1 and end < half - TOLERANCE:
            raise LangError(f"{self.name}: end must be at least {mm(half)}, half the {mm(self.spec.plate_length)} "
                            f"plates, not {mm(end)}.")
        #: Brackets per frame board; None with at=.
        self.count: int | None = spacing.count
        #: From the ends of the shared stretch to the first and last bracket.
        self.end = spacing.end
        #: Positions along the edge, the same on every frame board.
        self.at = spacing.at
        #: The holes in the frame board and in the panel, as given; `"euro"`
        #: holes take their depth from the board (`_hole_size`).
        self.frame_hole: BracketHole = _hole(self.name, "frame_hole", frame_hole)
        self.panel_hole: BracketHole = _hole(self.name, "panel_hole", panel_hole)

    @property
    def name(self) -> str:
        return self.spec.title

    @property
    def max_gap(self) -> float:
        """The widest gap between the panel's back face and the frame
        board's edge: 3 for the PF-L-R, whose plate may hang that far over
        the edge, 29 for the PF-L, where its plate begins."""
        return self.spec.max_gap

    def _hole_size(self, board: Board, choice: BracketHole) -> tuple[float, float]:
        """(diameter, depth) of a part's holes in `board`: pilot holes and
        explicit sizes as given, Euro holes `EURO_DEPTH` deep but
        `EURO_WALL` short of the board's far face at most."""
        if choice == "pilot":
            return (data.PILOT_DIAMETER, data.PILOT_DEPTH)
        if choice == "euro":
            try:
                return (data.EURO_DIAMETER, data.euro_depth(board.thickness))
            except ValueError:
                raise LangError(f"{self.name}: {board.path} ({mm(board.thickness)}) is too thin for Euro holes, "
                                f"which stop {mm(data.EURO_WALL)} short of its far face.", board.path) from None
        return choice

    # -- mounting ------------------------------------------------------------------------------------

    def mount(self, scope: Scope, /, *, panel: Board, frame: Board | Face | Sequence[Board | Face]) -> None:
        """`cab.mount(bracket, panel=cover, frame=[left, right])`: drills the
        panel and each frame board for the brackets and places them.
        `frame=` takes a board, a big face of one (the face the frame parts
        go on), or a list of them. Nothing is drilled unless every bracket
        fits."""
        edges: list[_Edge] = []
        first = 1
        for board, face in self._frames(frame, panel, scope.path):
            edges.append(self._edge(panel, board, face, first))
            first += len(edges[-1].stations)
        for edge in edges:
            self._check(panel, edge)
        self._drill(panel, edges)
        self._place(scope, panel, edges)

    def _frames(self, value: Board | Face | Sequence[Board | Face], panel: Board,
                path: str) -> list[tuple[Board, Face | None]]:
        """`frame=`: boards or big faces of boards, one or a list."""
        items: list[Board | Face] = [value] if isinstance(value, (Board, Face)) else list(value)
        if not items:
            raise LangError(f"{self.name}: frame= names no frame board.", path)
        out: list[tuple[Board, Face | None]] = []
        for item in items:
            if isinstance(item, Board):
                out.append((item, None))
            else:
                if not item.is_big:
                    raise LangError(f"{self.name}: {item!r} is a narrow face; name the big face of the frame board "
                                    "the frame parts go on.", item.part.path)
                out.append((item.part, item))
        for i, (board, _) in enumerate(out):
            if board is panel:
                raise LangError(f"{self.name}: the panel cannot be one of its frame boards.", panel.path)
            if any(other is board for other, _ in out[:i]):
                raise LangError(f"{self.name}: {board.path} is named twice in frame=.", board.path)
        return out

    def _edge(self, panel: Board, frame: Board, face: Face | None, first: int) -> _Edge:
        """Where the panel meets the frame board, and the brackets' centres
        along that edge."""
        spec = self.spec
        if frame.t_axis == panel.t_axis:
            raise LangError(f"{self.name}: {frame.path} lies parallel to {panel.path}; the panel hangs on frame "
                            "boards standing square to it.", panel.path)
        edge: Axis = next(a for a in AXES if a not in (frame.t_axis, panel.t_axis))
        pb, fb = panel.box(), frame.box()
        # back: from the panel toward the frame board
        pt = panel.t_axis
        to_frame = middle(fb, pt) - middle(pb, pt)
        if abs(to_frame) < TOLERANCE:
            raise LangError(f"{self.name}: {frame.path} is centred on {panel.path}'s thickness; which face of the "
                            "panel is its back face?", panel.path)
        back_face = panel.face(panel.scope.frame.direction_of(pt, 1 if to_frame > 0 else -1))
        # out: from the frame board's face toward the panel's middle
        ft = frame.t_axis
        panel_middle = middle(pb, ft)
        if face is None:
            if fb.lo[ft] - TOLERANCE <= panel_middle <= fb.hi[ft] + TOLERANCE:
                raise LangError(f"{self.name}: the middle of {panel.path} lies within {frame.path}'s thickness; "
                                f"name the face the frame parts go on, e.g. frame={frame.name}.left.", panel.path)
            face = frame.face(frame.scope.frame.direction_of(ft, 1 if panel_middle > fb.hi[ft] else -1))
        elif (panel_middle - face.value) * face.direction.sign <= TOLERANCE:
            raise LangError(f"{self.name}: {panel.path} lies behind {frame.path}'s {face.name} face; the frame parts "
                            "go on the face toward the panel.", frame.path)
        back = back_face.direction
        near, far = (fb.lo[pt], fb.hi[pt]) if back.sign > 0 else (fb.hi[pt], fb.lo[pt])
        gap = (near - back_face.value) * back.sign
        if gap > spec.max_gap + TOLERANCE:
            start = spec.frame_plate_back[0]
            begins = "at the panel's back face" if start <= TOLERANCE else f"{mm(start)} behind it"
            over = (f" and may hang {mm(spec.frame_plate_overhang)} over the frame board's edge"
                    if spec.frame_plate_overhang > TOLERANCE else "")
            raise LangError(f"{self.name}: the edge of {frame.path} lies {mm(gap)} behind {panel.path}'s back face; "
                            f"the frame part's plate begins {begins}{over}, so the gap may be at most "
                            f"{mm(spec.max_gap)}.", frame.path)
        reach = (far - back_face.value) * back.sign
        if reach < spec.frame_plate_back[1] - TOLERANCE:
            raise LangError(f"{self.name}: {frame.path} ends {mm(reach)} behind {panel.path}'s back face; the frame "
                            f"part's plate reaches {mm(spec.frame_plate_back[1])} behind it.", frame.path)
        out = face.direction
        panel_near = pb.lo[ft] if out.sign > 0 else pb.hi[ft]
        clearance = (panel_near - face.value) * out.sign
        limit = spec.panel_plate_out[0] + data.MAX_PLATE_OVERHANG
        if clearance > limit + TOLERANCE:
            raise LangError(f"{self.name}: {panel.path} ends {mm(clearance)} short of {frame.path}'s face; the "
                            f"panel part's plate begins {mm(spec.panel_plate_out[0])} from that face, so the panel "
                            f"must reach to within {mm(limit)} of it.", panel.path)
        lo, hi = max(pb.lo[edge], fb.lo[edge]), min(pb.hi[edge], fb.hi[edge])
        if hi - lo < spec.plate_length - TOLERANCE:
            raise LangError(f"{self.name}: {panel.path} and {frame.path} share {mm(max(hi - lo, 0.0))} along the "
                            f"edge; a bracket is {mm(spec.plate_length)} long.", panel.path)
        values = self._stations(panel, frame, edge, lo, hi)
        order = numbering(back, edge)
        return _Edge(frame, face, back_face, edge, tuple(values if order > 0 else values[::-1]), first, order, gap,
                     clearance)

    def _stations(self, panel: Board, frame: Board, edge: Axis, lo: float, hi: float) -> list[float]:
        """The brackets' centres along the shared stretch, ascending."""
        spec = self.spec
        if self.at is not None:
            values: list[float] = []
            for pos in self.at:
                if pos.axis != edge:
                    raise LangError(f"{self.name}: at={pos} is not on the axis the edge of {frame.path} runs "
                                    f"along ({edge}).", panel.path)
                if not lo - TOLERANCE <= pos.value <= hi + TOLERANCE:
                    raise LangError(f"{self.name}: at={pos} lies outside the stretch {panel.path} and {frame.path} "
                                    f"share ({lo:g} to {hi:g}).", panel.path)
                values.append(pos.value)
            values.sort()
        else:
            assert self.count is not None
            try:
                values = [lo + s for s in data.stations(hi - lo, self.count, self.end)]
            except ValueError:
                raise LangError(f"{self.name}: the {mm(hi - lo)} that {panel.path} and {frame.path} share are too "
                                f"short for {self.count} brackets {mm(self.end)} from the ends.", panel.path) from None
        for a, b in zip(values, values[1:]):
            if b - a < spec.plate_length - TOLERANCE:
                raise LangError(f"{self.name}: two brackets on {frame.path} are {mm(b - a)} apart; their "
                                f"{mm(spec.plate_length)} plates would overlap.", panel.path)
        return values

    def _holes(self, edge: _Edge) -> list[tuple[int, str, Point2, Point2]]:
        """Per bracket on the edge its number and its two holes, a first
        along the numbering: the letter, the point on the frame board's
        face and the one on the panel's back face."""
        spec, frame, panel = self.spec, edge.frame, edge.back_face.part
        half = spec.hole_pitch / 2
        out: list[tuple[int, str, Point2, Point2]] = []
        for n, s in enumerate(edge.stations, edge.first):
            for letter, k in (("a", -edge.order), ("b", edge.order)):
                at = s + k * half
                out.append((n, letter, uv(frame, edge.point(0.0, spec.frame_hole_back, at)),
                            uv(panel, edge.point(spec.panel_hole_out, 0.0, at))))
        return out

    def _check(self, panel: Board, edge: _Edge) -> None:
        """The plates on their boards, the holes on their faces and less
        deep than the boards are thick."""
        spec = self.spec
        frame = edge.frame
        half = spec.plate_length / 2
        frame_region = _plate_region(frame, edge.frame_face)
        panel_region = _plate_region(panel, edge.back_face)
        frame_hole = self._hole_size(frame, self.frame_hole)
        panel_hole = self._hole_size(panel, self.panel_hole)
        for n, s in enumerate(edge.stations, edge.first):
            # over a gap in front of the frame board the plate may hang free
            b0, b1 = max(spec.frame_plate_back[0], edge.gap), spec.frame_plate_back[1]
            if not _covers(frame_region, frame, edge.point(0.0, b0, s - half), edge.point(0.0, b1, s + half)):
                raise LangError(f"{self.name}: the frame part of bracket {n} does not fit on {frame.path}'s "
                                f"{edge.frame_face.name} face ({mm(b0)} to {mm(b1)} behind {panel.path}'s back "
                                f"face, {mm(spec.plate_length)} long).", frame.path)
            # over a panel's clearance the plate may hang free
            o0, o1 = max(spec.panel_plate_out[0], edge.clearance), spec.panel_plate_out[1]
            if not _covers(panel_region, panel, edge.point(o0, 0.0, s - half), edge.point(o1, 0.0, s + half)):
                raise LangError(f"{self.name}: the panel part of bracket {n} on {frame.path} does not fit on "
                                f"{panel.path}'s {edge.back_face.name} face ({mm(o1 - o0)} out from {frame.path}, "
                                f"{mm(spec.plate_length)} long).", panel.path)
        for n, _, at_frame, at_panel in self._holes(edge):
            check_hole(self.name, frame, edge.frame_face, at_frame, frame_hole[0], f"frame_hole of bracket {n}")
            check_hole(self.name, panel, edge.back_face, at_panel, panel_hole[0], f"panel_hole of bracket {n}")
        check_pilot_depth(self.name, frame, frame_hole[1], "frame_hole")
        check_pilot_depth(self.name, panel, panel_hole[1], "panel_hole")

    # -- machining and placing -------------------------------------------------------------------------

    def _drill(self, panel: Board, edges: list[_Edge]) -> None:
        """Per bracket two holes into the frame board's face, named
        `bracket_<panel>_<n>a` and `b` (a first along the numbering), and
        two into the panel's back face, `bracket_<frame>_<n>a` and `b`."""
        panel_hole = self._hole_size(panel, self.panel_hole)
        for edge in edges:
            frame = edge.frame
            frame_hole = self._hole_size(frame, self.frame_hole)
            for n, letter, at_frame, at_panel in self._holes(edge):
                frame.add_hole(edge.frame_face, at_frame, *frame_hole,
                               name=frame.unique_op_name(f"bracket_{panel.name}_{n}{letter}"))
                panel.add_hole(edge.back_face, at_panel, *panel_hole,
                               name=panel.unique_op_name(f"bracket_{frame.name}_{n}{letter}"))

    def _place(self, scope: Scope, panel: Board, edges: list[_Edge]) -> None:
        """Records the brackets as `<panel>_brackets`, a body per latched
        pair, `bracket_1`, `bracket_2`, ... in the order they are numbered."""
        boxes = self.shape.boxes()
        bodies = [HardwareBodyLayout(name=f"bracket_{n}", boxes=[edge.world_box(s, b) for b in boxes])
                  for edge in edges for n, s in enumerate(edge.stations, edge.first)]
        scope.place_hardware(scope.unique_hardware_name(f"{panel.name}_brackets"), bodies)


def sliding_bracket(model: BracketModel = "Pacofix PF-L-R", *, count: int | None = None,
                    end: float = data.DEFAULT_END_OFFSET, at: Sequence[PosLike] | None = None,
                    frame_hole: BracketHole = "pilot", panel_hole: BracketHole = "pilot") -> SlidingBracket:
    """Sliding brackets for a removable panel, `sliding_bracket("Pacofix
    PF-L", frame_hole="euro")`: see `SlidingBracket`, the type it returns."""
    return SlidingBracket(model, count=count, end=end, at=at, frame_hole=frame_hole, panel_hole=panel_hole)


def _hole(label: str, what: str, choice: BracketHole) -> BracketHole:
    """A part's holes, checked: a choice of `HoleChoice`, or (diameter,
    depth)."""
    if isinstance(choice, str):
        return one_of(choice, HoleChoice, f"{label}({what}=)")
    return check_hole_size(label, what, choice)


def _plate_region(board: Board, face: Face) -> BaseGeometry:
    """Where a plate can bear on a big face, in the board's (u, v): the
    outline less the pockets made into the face and those through from
    the other face. Holes do not count; a plate may cover one."""
    removed = [op.shape.geometry for op in board.ops
               if isinstance(op, Pocket) and (op.face == face.world_name or op.depth >= board.thickness - 1e-9)]
    region = board.outline.geometry
    return region.difference(unary_union(removed)) if removed else region


def _covers(region: BaseGeometry, board: Board, a: dict[Axis, float], b: dict[Axis, float]) -> bool:
    """Whether the rectangle between two corners lies on the region."""
    (u0, v0), (u1, v1) = uv(board, a), uv(board, b)
    plate = shapely_box(min(u0, u1), min(v0, v1), max(u0, u1), max(v0, v1))
    return plate.difference(region.buffer(TOLERANCE)).area <= TOLERANCE
