"""Sliding brackets (Häfele Pacofix PF / PF-L, the same part as Keku AS)
that hold a removable panel on frame boards, as hardware.

The panel and each frame board stand square to each other, the panel's
back face against the frame board's front edge, a gap in front of it, or
the frame boards reaching past it with the panel set in between them.
`cab.mount(SlidingBracket(), panel=cover, frame=[left, right])` hangs the
panel on each frame board named and drills both parts as
`lib.sliding_brackets` has them:

- into the frame board's inner face (the big face toward the panel's
  middle, or the face named: `frame=[partition.left]`) the frame part's
  two holes, 32 apart along the edge, 37 behind the panel's back face (the
  big face toward the frame board), whatever the gap: it is read from the
  model, never given;
- into the panel's back face the panel part's two holes, 32 apart, 15
  out from the frame board's face, where the tongue lies.

The holes are `"pilot"` holes for chipboard screws (Ø2 x 6) unless
`frame_hole=` or `panel_hole=` say `"euro"` (Ø5 x 11, for 6.3 mm Euro
screws and the frame part made for them) or give (diameter, depth). Per
frame board `count` brackets (2) sit along the stretch the panel and the
frame board share, the outer ones' centres `end` (50) from its ends, the
rest evenly between, one alone in the middle; `at=` takes positions along
the edge instead, the same on every frame board named. Brackets are
numbered by their place along the edge: from the bottom, or from the
panel's own left, seen standing in front of it.

It refuses, before it drills anything: a frame board parallel to the
panel, a frame board whose edge lies more than 29 behind the panel's
back face or that ends before the frame part's plate does (45 behind
it), a panel that stops more than 3 mm short of the frame board's face
(the tongue lies on that face), plates that do not lie on their boards
(the outline, less the pockets made into the face) or overlap each
other, holes that land off their face or in another hole or pocket, and
holes as deep as a board is thick; `end` under half a plate (24).
Keku's rule that brackets be at most 600 apart, and Häfele's that they
carry no hanging load (a ceiling panel), become notes in the layout's
problems; Keku's minimum of four per panel is left to the build (two
frame boards with the default two brackets each).

Each latched pair is one body of four boxes (`BRACKET_SHAPES`, measured
on Häfele's CAD models): the frame part's plate and its hook, the panel
part's plate and its tongue, which lies under the hook. They are placed
as `<panel>_brackets`, bodies named by the frame board and the bracket's
number (`left_1`). Operations are named by the other board and the
bracket: `bracket_cover_1a` and `_1b` in the frame board,
`bracket_left_1a` in the panel.
"""
from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal, cast

from shapely.geometry import Point
from shapely.geometry import box as shapely_box
from shapely.geometry.base import BaseGeometry
from shapely.ops import unary_union

from lib import sliding_brackets as data

from ..core import directions
from ..core.box import Box
from ..core.directions import AXES, Axis, Direction
from ..core.errors import LangError, one_of
from ..core.layout_types import BoxDict, HardwareBodyLayout
from ..core.ops import Hole, Pocket
from ..core.part import Board, Face
from ..core.refs import PosLike, as_pos

if TYPE_CHECKING:
    from ..core.scope import Scope

#: The brackets of `lib.sliding_brackets`, by name.
BracketModel = Literal["Pacofix PF-L"]
#: The holes of one part: for chipboard screws or for Euro screws, as
#: `lib.sliding_brackets` sizes them, or (diameter, depth) in mm.
HoleChoice = Literal["pilot", "euro"]
BracketHole = HoleChoice | tuple[float, float]

#: Geometric tolerance of the checks, mm.
TOLERANCE = 1e-3
Point2 = tuple[float, float]
#: Two ends of a box along one direction, mm.
Extent = tuple[float, float]
#: A box of a latched bracket, mm: its extents out from the frame board's
#: face (toward the panel's middle), back from the panel's back face (away
#: from the panel) and along the edge from the bracket's centre.
BracketBox = tuple[Extent, Extent, Extent]


@dataclass(frozen=True)
class BracketShape:
    """A latched bracket as boxes in its frame (`BracketBox`): the space
    it takes, not its detail. The two parts interlock, the hook lying in
    the tongue's channel, so a bracket is one body. The drilling data
    stays in `lib.sliding_brackets`."""
    #: On the frame board's face: the plate, and the hook with its spine.
    frame_part: tuple[BracketBox, ...]
    #: On the panel's back face: the plate, and the tongue on the frame
    #: board's face.
    panel_part: tuple[BracketBox, ...]

    def boxes(self) -> list[BracketBox]:
        return [*self.frame_part, *self.panel_part]


#: Per model. Pacofix PF / PF-L measured on Häfele's CAD models (glTF,
#: 2026-10-12) of the panel part 262.50.359 and the frame part 262.50.368,
#: fitted together latched: the frame part's plate 4 thick, 16 across its
#: holes, 48 long; its hook 16 wide, from the plate's top up to 10.2 off
#: the board and from the plate to 28 in front of its holes, its lip
#: dipping to 4.5 inside the tongue's channel (the box covers the spine
#: that ramps up along the plate); the panel part's plate 23 out from the
#: frame board's face, 4 thick, 48 long; its tongue 10 off the frame
#: board, 22.1 wide, 29 back to the frame part's plate.
BRACKET_SHAPES: dict[str, BracketShape] = {
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
        (o0, o1), (b0, b1), (a0, a1) = box
        p, q = self.point(o0, b0, s + a0), self.point(o1, b1, s + a1)
        return {"min": [min(p[a], q[a]) for a in AXES], "max": [max(p[a], q[a]) for a in AXES]}


class SlidingBracket:
    """Sliding brackets of one model with their placement and holes:
    `count` per frame board, the outer ones `end` from the ends of the
    stretch the panel and the frame board share, or one at each position
    of `at` along the edge; `frame_hole` and `panel_hole` are the holes in
    the frame board and the panel: `"pilot"` (Ø2 x 6), `"euro"` (Ø5 x 11)
    or (diameter, depth) in mm."""

    def __init__(self, model: BracketModel = "Pacofix PF-L", count: int | None = None,
                 end: float = data.DEFAULT_END_OFFSET, at: Sequence[PosLike] | None = None,
                 frame_hole: BracketHole = "pilot", panel_hole: BracketHole = "pilot"):
        self.spec = data.BRACKETS[one_of(model, BracketModel, "SlidingBracket()")]
        #: The boxes the brackets are drawn as.
        self.shape = BRACKET_SHAPES[model]
        if count is not None and at is not None:
            raise LangError(f"{self.name}: give count= or at=, not both.")
        if count is not None and count < 1:
            raise LangError(f"{self.name}: count must be at least 1, not {count}.")
        half = self.spec.plate_length / 2
        if at is None and count != 1 and end < half - TOLERANCE:
            raise LangError(f"{self.name}: end must be at least {_mm(half)}, half the {_mm(self.spec.plate_length)} "
                            f"plates, not {end:g}.")
        if at is not None and not at:
            raise LangError(f"{self.name}: at= is empty.")
        #: Brackets per frame board; None with at=.
        self.count: int | None = None if at is not None else (count if count is not None else data.DEFAULT_COUNT)
        #: From the ends of the shared stretch to the first and last bracket.
        self.end = float(end)
        #: Positions along the edge, the same on every frame board.
        self.at = tuple(as_pos(p, f"{self.name}(at=)") for p in at) if at is not None else None
        #: (diameter, depth) of the holes in the frame board and in the panel.
        self.frame_hole = _hole(self.name, "frame_hole", frame_hole)
        self.panel_hole = _hole(self.name, "panel_hole", panel_hole)

    @property
    def name(self) -> str:
        return self.spec.title

    @property
    def max_gap(self) -> float:
        """The widest gap between the panel's back face and the frame
        board's edge (29), where the frame part's plate begins."""
        return self.spec.max_gap

    # -- mounting ------------------------------------------------------------------------------------

    def mount(self, scope: Scope, /, **options: object) -> None:
        """`cab.mount(bracket, panel=cover, frame=[left, right])`: drills the
        panel and each frame board for the brackets and places them.
        `frame=` takes a board, a big face of one (the face the frame parts
        go on), or a list of them. Nothing is drilled unless every bracket
        fits."""
        allowed = {"panel", "frame"}
        if set(options) - allowed or allowed - set(options):
            raise LangError(f"{self.name}: mount() takes panel= and frame=, got {sorted(options)}.", scope.path)
        panel = options["panel"]
        if not isinstance(panel, Board):
            raise LangError(f"{self.name}: panel= must be the panel board, not {panel!r}.", scope.path)
        frames = self._frames(options["frame"], panel, scope.path)
        edges = [self._edge(panel, board, face) for board, face in frames]
        for edge in edges:
            self._check(panel, edge)
        self._drill(panel, edges)
        self._notes(panel, edges)
        self._place(scope, panel, edges)

    def _frames(self, value: object, panel: Board, path: str) -> list[tuple[Board, Face | None]]:
        """`frame=`: boards or big faces of boards, one or a list."""
        items: list[object] = list(cast(Sequence[object], value)) if isinstance(value, (list, tuple)) else [value]
        if not items:
            raise LangError(f"{self.name}: frame= names no frame board.", path)
        out: list[tuple[Board, Face | None]] = []
        for item in items:
            if isinstance(item, Board):
                out.append((item, None))
            elif isinstance(item, Face):
                if not item.is_big:
                    raise LangError(f"{self.name}: {item!r} is a narrow face; name the big face of the frame board "
                                    "the frame parts go on.", item.part.path)
                out.append((item.part, item))
            else:
                raise LangError(f"{self.name}: frame= takes frame boards or their faces, not {item!r}.", path)
        for i, (board, _) in enumerate(out):
            if board is panel:
                raise LangError(f"{self.name}: the panel cannot be one of its frame boards.", panel.path)
            if any(other is board for other, _ in out[:i]):
                raise LangError(f"{self.name}: {board.path} is named twice in frame=.", board.path)
        return out

    def _edge(self, panel: Board, frame: Board, face: Face | None) -> _Edge:
        """Where the panel meets the frame board, and the brackets' centres
        along that edge."""
        spec = self.spec
        if frame.t_axis == panel.t_axis:
            raise LangError(f"{self.name}: {frame.path} lies parallel to {panel.path}; the panel hangs on frame "
                            "boards standing square to it.", panel.path)
        along: Axis = next(a for a in AXES if a not in (frame.t_axis, panel.t_axis))
        pb, fb = panel.box(), frame.box()
        # back: from the panel toward the frame board
        pt = panel.t_axis
        to_frame = _middle(fb, pt) - _middle(pb, pt)
        if abs(to_frame) < TOLERANCE:
            raise LangError(f"{self.name}: {frame.path} is centred on {panel.path}'s thickness; which face of the "
                            "panel is its back face?", panel.path)
        back_face = panel.face(panel.scope.frame.direction_of(pt, 1 if to_frame > 0 else -1))
        # out: from the frame board's face toward the panel's middle
        ft = frame.t_axis
        middle = _middle(pb, ft)
        if face is None:
            if fb.lo[ft] - TOLERANCE <= middle <= fb.hi[ft] + TOLERANCE:
                raise LangError(f"{self.name}: the middle of {panel.path} lies within {frame.path}'s thickness; "
                                f"name the face the frame parts go on, e.g. frame={frame.name}.left.", panel.path)
            face = frame.face(frame.scope.frame.direction_of(ft, 1 if middle > fb.hi[ft] else -1))
        elif (middle - face.value) * face.direction.sign <= TOLERANCE:
            raise LangError(f"{self.name}: {panel.path} lies behind {frame.path}'s {face.name} face; the frame parts "
                            "go on the face toward the panel.", frame.path)
        back = back_face.direction
        near, far = (fb.lo[pt], fb.hi[pt]) if back.sign > 0 else (fb.hi[pt], fb.lo[pt])
        gap = (near - back_face.value) * back.sign
        if gap > spec.max_gap + TOLERANCE:
            raise LangError(f"{self.name}: the edge of {frame.path} lies {_mm(gap)} behind {panel.path}'s back face; "
                            f"the frame part's plate begins {_mm(spec.max_gap)} behind it, so the gap may be at most "
                            f"that.", frame.path)
        reach = (far - back_face.value) * back.sign
        if reach < spec.frame_plate_back[1] - TOLERANCE:
            raise LangError(f"{self.name}: {frame.path} ends {_mm(reach)} behind {panel.path}'s back face; the frame "
                            f"part's plate reaches {_mm(spec.frame_plate_back[1])} behind it.", frame.path)
        out = face.direction
        panel_near = pb.lo[ft] if out.sign > 0 else pb.hi[ft]
        clearance = (panel_near - face.value) * out.sign
        if clearance > data.MAX_PANEL_CLEARANCE + TOLERANCE:
            raise LangError(f"{self.name}: {panel.path} ends {_mm(clearance)} short of {frame.path}'s face; the "
                            "tongue of the panel part lies on that face, so the panel must reach to within "
                            f"{_mm(data.MAX_PANEL_CLEARANCE)} of it.", panel.path)
        lo, hi = max(pb.lo[along], fb.lo[along]), min(pb.hi[along], fb.hi[along])
        if hi - lo < spec.plate_length - TOLERANCE:
            raise LangError(f"{self.name}: {panel.path} and {frame.path} share {_mm(max(hi - lo, 0.0))} along the "
                            f"edge; a bracket is {_mm(spec.plate_length)} long.", panel.path)
        values = self._stations(panel, frame, along, lo, hi)
        order = _order(back, along)
        return _Edge(frame, face, back_face, along, tuple(values if order > 0 else values[::-1]), order, gap,
                     clearance)

    def _stations(self, panel: Board, frame: Board, along: Axis, lo: float, hi: float) -> list[float]:
        """The brackets' centres along the shared stretch, ascending."""
        spec = self.spec
        if self.at is not None:
            values: list[float] = []
            for pos in self.at:
                if pos.axis != along:
                    raise LangError(f"{self.name}: at={pos} is not on the axis the edge of {frame.path} runs "
                                    f"along ({along}).", panel.path)
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
                raise LangError(f"{self.name}: the {_mm(hi - lo)} that {panel.path} and {frame.path} share are too "
                                f"short for {self.count} brackets {_mm(self.end)} from the ends.", panel.path) from None
        for a, b in zip(values, values[1:]):
            if b - a < spec.plate_length - TOLERANCE:
                raise LangError(f"{self.name}: two brackets on {frame.path} are {_mm(b - a)} apart; their "
                                f"{_mm(spec.plate_length)} plates would overlap.", panel.path)
        return values

    def _check(self, panel: Board, edge: _Edge) -> None:
        """The plates on their boards, the holes on their faces and less
        deep than the boards are thick."""
        spec = self.spec
        frame = edge.frame
        half = spec.plate_length / 2
        frame_region = _face_region(frame, edge.frame_face)
        panel_region = _face_region(panel, edge.back_face)
        for n, s in enumerate(edge.stations, 1):
            b0, b1 = spec.frame_plate_back
            if not _covers(frame_region, frame, edge.point(0.0, b0, s - half), edge.point(0.0, b1, s + half)):
                raise LangError(f"{self.name}: the frame part of bracket {n} does not fit on {frame.path}'s "
                                f"{edge.frame_face.name} face ({_mm(b0)} to {_mm(b1)} behind {panel.path}'s back "
                                f"face, {_mm(spec.plate_length)} long).", frame.path)
            # over a panel's clearance the plate may hang free
            o0, o1 = max(spec.panel_plate_out[0], edge.clearance), spec.panel_plate_out[1]
            if not _covers(panel_region, panel, edge.point(o0, 0.0, s - half), edge.point(o1, 0.0, s + half)):
                raise LangError(f"{self.name}: the panel part of bracket {n} on {frame.path} does not fit on "
                                f"{panel.path}'s {edge.back_face.name} face ({_mm(o1 - o0)} out from {frame.path}, "
                                f"{_mm(spec.plate_length)} long).", panel.path)
            for k in (-1, 1):
                along = s + k * spec.hole_pitch / 2
                if not _hole_fits(frame, edge.frame_face, edge.point(0.0, spec.frame_hole_back, along),
                                  self.frame_hole[0]):
                    raise LangError(f"{self.name}: a hole of bracket {n} lands off {frame.path}'s "
                                    f"{edge.frame_face.name} face or in one of its holes or pockets.", frame.path)
                if not _hole_fits(panel, edge.back_face, edge.point(spec.panel_hole_out, 0.0, along),
                                  self.panel_hole[0]):
                    raise LangError(f"{self.name}: a hole of bracket {n} on {frame.path} lands off {panel.path}'s "
                                    f"{edge.back_face.name} face or in one of its holes or pockets.", panel.path)
        for board, (_, depth), what in ((frame, self.frame_hole, "frame_hole"), (panel, self.panel_hole, "panel_hole")):
            if depth >= board.thickness - TOLERANCE:
                raise LangError(f"{self.name}: the {what} depth ({_mm(depth)}) must be less than "
                                f"{board.path}'s thickness ({_mm(board.thickness)}).", board.path)

    # -- machining and placing -------------------------------------------------------------------------

    def _drill(self, panel: Board, edges: list[_Edge]) -> None:
        """Per bracket two holes into the frame board's face, named
        `bracket_<panel>_<n>a` and `b` (a first along the numbering), and
        two into the panel's back face, `bracket_<frame>_<n>a` and `b`."""
        spec = self.spec
        half = spec.hole_pitch / 2
        for edge in edges:
            frame = edge.frame
            for n, s in enumerate(edge.stations, 1):
                for letter, k in (("a", -edge.order), ("b", edge.order)):
                    along = s + k * half
                    frame.add_hole(edge.frame_face, _uv(frame, edge.point(0.0, spec.frame_hole_back, along)),
                                   *self.frame_hole, name=frame.unique_op_name(f"bracket_{panel.name}_{n}{letter}"))
                    panel.add_hole(edge.back_face, _uv(panel, edge.point(spec.panel_hole_out, 0.0, along)),
                                   *self.panel_hole, name=panel.unique_op_name(f"bracket_{frame.name}_{n}{letter}"))

    def _notes(self, panel: Board, edges: list[_Edge]) -> None:
        """Keku's largest spacing and Häfele's hanging loads, as notes in
        the layout's problems."""
        for edge in edges:
            values = sorted(edge.stations)
            widest = max((b - a for a, b in zip(values, values[1:])), default=0.0)
            if widest > data.MAX_SPACING + TOLERANCE:
                panel.notes.append(f"{panel.path}: sliding brackets on {edge.frame.path} {_mm(widest)} apart; Keku "
                                   f"allows at most {_mm(data.MAX_SPACING)}.")
        up = directions.frame.direction("top")
        back = edges[0].back_face.direction
        if back.axis == up.axis and back.sign == up.sign:
            panel.notes.append(f"{panel.path}: hangs from its sliding brackets; Häfele rules out hanging loads such "
                               "as ceiling panels.")

    def _place(self, scope: Scope, panel: Board, edges: list[_Edge]) -> None:
        """Records the brackets as `<panel>_brackets`, a body per latched
        pair named by its frame board and number (`left_1`)."""
        boxes = self.shape.boxes()
        bodies: list[HardwareBodyLayout] = []
        for edge in edges:
            for n, s in enumerate(edge.stations, 1):
                name, k = f"{edge.frame.name}_{n}", 2
                while any(b["name"] == name for b in bodies):     # frame boards of one name in different scopes
                    name, k = f"{edge.frame.name}_{n}_{k}", k + 1
                bodies.append(HardwareBodyLayout(name=name, boxes=[edge.world_box(s, b) for b in boxes]))
        base = f"{panel.name}_brackets"
        name, k = base, 2
        while name in scope.parts or name in scope.children or any(i["name"] == name for i in scope.hardware):
            name, k = f"{base}_{k}", k + 1
        scope.place_hardware(name, bodies)


def _hole(label: str, what: str, choice: BracketHole) -> tuple[float, float]:
    """A part's holes as (diameter, depth)."""
    if isinstance(choice, str):
        if one_of(choice, HoleChoice, f"{label}({what}=)") == "euro":
            return (data.EURO_DIAMETER, data.EURO_DEPTH)
        return (data.PILOT_DIAMETER, data.PILOT_DEPTH)
    diameter, depth = choice
    if diameter <= 0 or depth <= 0:
        raise LangError(f"{label}: {what}= needs a diameter and a depth greater than zero, not {diameter:g} x "
                        f"{depth:g}.")
    return (float(diameter), float(depth))


def _mm(value: float) -> str:
    return f"{value:.1f}".rstrip("0").rstrip(".") + " mm"


def _middle(box: Box, axis: Axis) -> float:
    return (box.lo[axis] + box.hi[axis]) / 2


def _uv(board: Board, p: dict[Axis, float]) -> Point2:
    return (p[board.u_axis], p[board.v_axis])


def _order(back: Direction, along: Axis) -> int:
    """Which way the brackets are numbered along the edge: from the bottom
    up on an upright edge, else from the panel's own left to its right,
    seen standing in front of it (its right is back x up, `back` pointing
    from the panel to the frame board); for a panel lying flat, along the
    world axis."""
    up = directions.frame.direction("top")
    if along == up.axis:
        return up.sign
    if back.axis == up.axis:
        return 1
    (bx, by, bz), (ux, uy, uz) = back.vector, up.vector
    right = (by * uz - bz * uy, bz * ux - bx * uz, bx * uy - by * ux)
    return 1 if right[AXES.index(along)] > 0 else -1


def _face_region(board: Board, face: Face) -> BaseGeometry:
    """Where a plate can bear on a big face, in the board's (u, v): the
    outline less the pockets made into the face and those through from
    the other face. Holes do not count; a plate may cover one."""
    removed = [op.shape.geometry for op in board.ops
               if isinstance(op, Pocket) and (op.face == face.world_name or op.depth >= board.thickness - 1e-9)]
    region = board.outline.geometry
    return region.difference(unary_union(removed)) if removed else region


def _covers(region: BaseGeometry, board: Board, a: dict[Axis, float], b: dict[Axis, float]) -> bool:
    """Whether the rectangle between two corners lies on the region."""
    (u0, v0), (u1, v1) = _uv(board, a), _uv(board, b)
    plate = shapely_box(min(u0, u1), min(v0, v1), max(u0, u1), max(v0, v1))
    return plate.difference(region.buffer(TOLERANCE)).area <= TOLERANCE


def _hole_fits(board: Board, face: Face, p: dict[Axis, float], d: float) -> bool:
    """Whether a hole's centre and the points its radius away along both of
    the face's axes lie on the outline, and its circle clear of the holes
    and pockets made into the face (or through from the other face)."""
    u, v = _uv(board, p)
    r = d / 2
    outline = board.outline.geometry
    points = [Point(u, v), Point(u - r, v), Point(u + r, v), Point(u, v - r), Point(u, v + r)]
    if any(outline.distance(q) > TOLERANCE for q in points):
        return False
    for op in board.ops:
        if not isinstance(op, (Hole, Pocket)):
            continue
        if op.face != face.world_name and op.depth < board.thickness - 1e-9:
            continue
        if isinstance(op, Hole):
            if Point(op.u, op.v).distance(Point(u, v)) < op.d / 2 + r - TOLERANCE:
                return False
        elif op.shape.geometry.buffer(-TOLERANCE).intersects(Point(u, v).buffer(r, quad_segs=8)):
            return False
    return True
