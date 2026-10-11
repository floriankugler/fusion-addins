"""Connectors: Domino, Clamex P and Cabineo, joining two boards where one
meets the other edge-on (see `lang.core.contact`).

`bottom.join(left, right, using=cabineo(count=3))` joins the bottom to the
two sides it stands between; `left.join(bottom, top, using=...)` says the
same from the side. Every board named must touch the receiver, one of the
two edge-on; the contact decides which board gets which machining. Along
each contact the connectors sit at `count=` stations, the first and last
`end=` from the contact's ends and the rest evenly between (a single one
centred), or at the positions `at=` along the contact.

Both boards are machined from their big faces only; nothing is cut into a
narrow face, which a 3-axis machine cannot reach. "The edge-on board" is
the one whose end meets the other's face:

- `domino`: a slot in the other board's face, centred on the edge-on
  board's thickness or `fence=` from its reference face. The mortise in
  the edge-on board's end is cut later with the Domino machine, lined up
  with a V-groove mark on its reference face at each Domino.
- `clamex`: an access hole (P-14) or slot (P-10) in the edge-on board's
  access face near its end, half the board's thickness deep, and two guide
  holes in the other board's face.
- `cabineo`: three overlapping holes in the edge-on board's access face,
  open toward its end, where the connector sits, and the hole for its
  screw in the other board's face.

The access face is the big face that is not the show face, unless `face=`
names one: a box side or direction it faces (`face=cab.bottom`), or
`"inner"`/`"outer"`. A Domino's reference face is the show face unless
`face=` names another. Dimensions are those of the connectors_native
add-in, from `lib/connector_data.py`. Operations are named by kind, the
other board and the station: `cabineo_left_1a` to `_1c` in the bottom,
`cabineo_bottom_1` in the left side.
"""
from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import ClassVar, Literal, Protocol

from lib import connector_data as data

from ..core.contact import Contact, contacts
from ..core.directions import Axis, Direction
from ..core.errors import LangError
from ..core.part import Board, Face
from ..core.refs import DepthSpec, Pos, PosLike, Side, as_pos, through, to
from ..core.shapes import circle, slot_shape

DominoSize = Literal["4x20", "5x30", "6x40", "8x36", "8x40", "8x50", "8x80", "8x100", "10x50", "10x80",
                     "10x100", "12x100", "12x140", "14x75", "14x100", "14x140"]
ClamexModel = Literal["P-10", "P-14"]
CabineoModel = Literal["8", "12", "8 M6"]
CabineoInsert = Literal["M6 x 12.3", "M6 x 15.3", "threaded insert"]
CabineoSurface = Literal["flush", "anti-break"]
#: Which Dominos get a mark: all, or all but the first and last, which the
#: machine's end stops locate.
DominoMarks = Literal["all", "middle"]
#: A big face named for a connector: a box side or direction it faces, or
#: inner/outer; None for the connector's default.
FaceChoice = Side | Direction | Literal["inner", "outer"] | None

_EPS = 1e-6
#: A Domino mark starts this far outside the board, so it runs out of the
#: board's end cleanly, mm.
_RUN_OUT = 1.0
_INSERT_KEYS: dict[str, str] = {"M6 x 12.3": "8 M6 x 12.3", "M6 x 15.3": "8 M6 x 15.3",
                                "threaded insert": "8 M6 threaded insert"}
Point2 = tuple[float, float]


# -- where along a contact -----------------------------------------------------------------------

@dataclass(frozen=True)
class Spacing:
    """`count` connectors with the outer ones `end` from the contact's ends,
    or one at each position of `at`."""
    count: int | None
    end: float
    at: tuple[Pos, ...] | None

    def stations(self, label: str, c: Contact) -> list[float]:
        """The positions along the contact, ascending."""
        path, other = c.edge_on.path, c.face_on.path
        if self.at is not None:
            values: list[float] = []
            for pos in self.at:
                if pos.axis != c.axis:
                    raise LangError(f"{label}: at={pos} is not on the axis the contact with {other} runs "
                                    f"along ({c.axis}).", path)
                if not c.lo - _EPS <= pos.value <= c.hi + _EPS:
                    raise LangError(f"{label}: at={pos} lies outside the contact with {other} "
                                    f"({c.lo:g} to {c.hi:g}).", path)
                values.append(pos.value)
            values.sort()
            if any(b - a <= _EPS for a, b in zip(values, values[1:])):
                raise LangError(f"{label}: two positions in at= coincide.", path)
            return values
        assert self.count is not None
        if self.count > 1 and 2 * self.end >= c.length - _EPS:
            raise LangError(f"{label}: end={self.end:g} leaves no room for {self.count} connectors on the "
                            f"{c.length:g} mm contact with {other}.", path)
        return [c.lo + s for s in data.stations(c.length, self.count, self.end)]


def _spacing(label: str, count: int | None, end: float, at: Sequence[PosLike] | None) -> Spacing:
    if (count is None) == (at is None):
        raise LangError(f"{label}: give count= or at=.")
    if count is not None and count < 1:
        raise LangError(f"{label}: count must be at least 1.")
    if end < 0:
        raise LangError(f"{label}: end must not be negative.")
    positions = tuple(as_pos(p, f"{label}(at=)") for p in at) if at is not None else None
    if positions == ():
        raise LangError(f"{label}: at= is empty.")
    return Spacing(count, float(end), positions)


# -- geometry of one contact ---------------------------------------------------------------------

class _Geometry:
    """Points of a contact: on the other board's face by (along, across),
    on this board's big faces by (along, distance from the edge)."""

    def __init__(self, c: Contact):
        self.c = c
        #: Across the contact plane: the axis the face-on board is thick on.
        self.normal: Axis = c.face_on.t_axis
        #: From the contact plane into the edge-on board, along `normal`.
        self.away = -c.end.direction.sign

    def on_face(self, along: float, across: float) -> Point2:
        """A point on the face-on board's face, in that face's frame."""
        f = self.c.face_on
        coords: dict[Axis, float] = {self.c.axis: along, self.c.across: across}
        return (coords[f.u_axis], coords[f.v_axis])

    def on_board(self, along: float, from_edge: float) -> Point2:
        """A point on a big face of the edge-on board, `from_edge` in from
        its end, in that face's frame."""
        e = self.c.edge_on
        coords: dict[Axis, float] = {self.c.axis: along, self.normal: self.c.plane + self.away * from_edge}
        return (coords[e.u_axis], coords[e.v_axis])

    @staticmethod
    def inside(face: Face, distance: float) -> float:
        """The coordinate `distance` into a board's thickness from its big
        face `face`."""
        return face.value - face.direction.sign * distance

    @property
    def middle(self) -> float:
        """The middle of the edge-on board's thickness."""
        b, t = self.c.edge_on.box(), self.c.across
        return (b.lo[t] + b.hi[t]) / 2


def _face_toward(part: Board, sign: int, axis: Axis) -> Face:
    return part.face(part.scope.frame.direction_of(axis, sign))


def _opposite(face: Face) -> Face:
    return _face_toward(face.part, -face.direction.sign, face.axis)


def _big_face(label: str, part: Board, choice: FaceChoice, default: Face) -> Face:
    if choice is None:
        return default
    if isinstance(choice, str):
        return part.face(choice)
    d = choice.outward if isinstance(choice, Side) else choice
    if d.axis != part.t_axis:
        raise LangError(f"{label}: face={d.name} is not a big face of this board.", part.path)
    return _face_toward(part, d.sign, d.axis)


def _hidden(part: Board) -> Face:
    """The big face that is not the show face."""
    return _opposite(part.show_face)


# -- joining ---------------------------------------------------------------------------------------

class _Connector(Protocol):
    label: ClassVar[str]

    @property
    def spacing(self) -> Spacing: ...

    def check(self, c: Contact, stations: list[float]) -> None: ...

    def place(self, c: Contact, stations: list[float]) -> None: ...


def _join(connector: _Connector, part: Board, partners: list[Board]) -> None:
    """Finds the contacts with the boards named, either one edge-on, checks
    every one, then machines them."""
    label = connector.label
    found: list[Contact] = []
    for other in partners:
        here = contacts(part, other) or contacts(other, part)
        if not here:
            raise LangError(f"{label}: {other.path} does not touch this board with an end or edge on a face.",
                            part.path)
        found.extend(here)
    planned = [(c, connector.spacing.stations(label, c)) for c in found]
    for c, stations in planned:
        connector.check(c, stations)
    for c, stations in planned:
        connector.place(c, stations)


def _start_index(part: Board, axis: Axis, count: int) -> int:
    """The index of the first of `count` ascending stations as the part's
    frame counts them: from the front, the left or the bottom."""
    frame = part.scope.frame
    start = next(d for d in (frame.direction(n) for n in ("front", "left", "bottom")) if d.axis == axis)
    return 0 if start.sign < 0 else count - 1


# -- Domino ------------------------------------------------------------------------------------------

@dataclass(frozen=True)
class Domino:
    size: data.DominoSize
    spacing: Spacing
    fence: float | None = None
    face: FaceChoice = None
    remaining: float | None = None
    loose: float = 0.0
    length_offset: float = 0.0
    height_offset: float = 0.0
    marks: DominoMarks | None = "all"
    mark_depth: float = data.DOMINO_MARK_DEPTH
    mark_length: float = data.DOMINO_MARK_LENGTH
    label: ClassVar[str] = "domino"

    @property
    def slot_height(self) -> float:
        """Across the contact: the Domino's thickness plus the offset."""
        return self.size.thickness + self.height_offset

    @property
    def slot_length(self) -> float:
        """Along the contact: the Domino's width plus the offset; the loose
        slots are `loose` longer."""
        return self.size.width + self.length_offset

    def join(self, part: Board, /, partners: list[Board]) -> None:
        _join(self, part, partners)

    def _reference(self, e: Board) -> Face:
        """The face the machine's fence rests on, which carries the marks."""
        return _big_face(self.label, e, self.face, e.show_face)

    def _centre(self, g: _Geometry) -> float:
        if self.fence is None:
            return g.middle
        return g.inside(self._reference(g.c.edge_on), self.fence)

    def check(self, c: Contact, stations: list[float]) -> None:
        e, f = c.edge_on, c.face_on
        h = self.slot_height
        if h >= e.thickness - _EPS:
            raise LangError(f"domino: the {h:g} mm high slot is not thinner than this board ({e.thickness:g}).",
                            e.path)
        centre = self._centre(_Geometry(c))
        b, t = e.box(), c.across
        if centre - h / 2 < b.lo[t] - _EPS or centre + h / 2 > b.hi[t] + _EPS:
            raise LangError(f"domino: at fence={self.fence} the slot does not fit within {e.path}'s "
                            "thickness.", e.path)
        if self.marks is not None and self.mark_depth >= e.thickness - _EPS:
            raise LangError(f"domino: mark_depth={self.mark_depth:g} is not less than {e.path}'s thickness.",
                            e.path)
        if self.remaining is None:
            depth = self.size.length / 2 + data.DOMINO_DEPTH_OFFSET
            if depth >= f.thickness - _EPS:
                raise LangError(f"domino: a {self.size.key} needs a {depth:g} mm deep slot, {f.path} is "
                                f"{f.thickness:g} thick; pick a shorter Domino or give remaining=.", e.path)
        elif self.remaining >= f.thickness - _EPS:
            raise LangError(f"domino: remaining={self.remaining:g} leaves no slot in {f.path} "
                            f"({f.thickness:g} thick).", e.path)
        for s in stations:
            if s - self.slot_length / 2 < c.lo - _EPS or s + self.slot_length / 2 > c.hi + _EPS:
                raise LangError(f"domino: the slot at {c.axis}={s:g} reaches past the contact with {f.path} "
                                f"({c.lo:g} to {c.hi:g}).", e.path)

    def place(self, c: Contact, stations: list[float]) -> None:
        g = _Geometry(c)
        e, f = c.edge_on, c.face_on
        centre, h = self._centre(g), self.slot_height
        depth: DepthSpec = (self.size.length / 2 + data.DOMINO_DEPTH_OFFSET if self.remaining is None
                            else to(_opposite(c.face), -self.remaining))
        exact = _start_index(e, c.axis, len(stations))
        for i, s in enumerate(stations):
            length = self.slot_length + (self.loose if i != exact else 0.0)
            half_span = (length - h) / 2
            shape = slot_shape(g.on_face(s - half_span, centre), g.on_face(s + half_span, centre), h)
            f.add_pocket(c.face, shape, depth, name=f.unique_op_name(f"domino_{e.name}_{i + 1}"))
        if self.marks is None:
            return
        reference = self._reference(e)
        for i, s in enumerate(stations):
            if self.marks == "middle" and len(stations) > 1 and i in (0, len(stations) - 1):
                continue
            # Across the reference face from the board's end, where the
            # machine's centre mark is lined up with it.
            e.add_vgroove(reference, g.on_board(s, -_RUN_OUT), g.on_board(s, self.mark_length), self.mark_depth,
                          e.unique_op_name(f"domino_{f.name}_{i + 1}_mark"))


def domino(size: DominoSize, *, count: int | None = None, at: Sequence[PosLike] | None = None,
           end: float = data.DOMINO_STOP_LATCH, fence: float | None = None, face: FaceChoice = None,
           remaining: float | None = None, loose: float = 0.0, length_offset: float = 0.0,
           height_offset: float = 0.0, marks: DominoMarks | None = "all",
           mark_depth: float = data.DOMINO_MARK_DEPTH, mark_length: float = data.DOMINO_MARK_LENGTH) -> Domino:
    """Dominos of `size` ("5x30": thickness x length): per station a slot
    in the face of the board that is met, half the Domino's length plus 0.5
    deep, or as deep as leaves `remaining` of that board, and a mark on the
    edge-on board for the Domino machine. `end` is the distance of the
    outer Dominos from the contact's ends, 37 by default (the machine's
    stop latches; 20 with the additional stop). The slots are centred on
    the edge-on board's thickness, or `fence` from its reference face (the
    show face, or `face=`), the face the machine's fence rests on.

    The marks are 90 degree V-grooves in the reference face, `mark_depth`
    deep (0.3) and running `mark_length` (4) in from the board's end, one
    per Domino (`marks="all"`), all but the first and last, which the
    machine's stops locate (`"middle"`), or none (`None`).

    `loose` makes every slot but the first (from the front, left or bottom)
    that much longer, as the machine's wider settings do (6 or 10);
    `length_offset` and `height_offset` change every slot's size."""
    spec = data.domino_size(size)
    spacing = _spacing("domino", count, end, at)
    if spec.thickness + height_offset <= 0:
        raise LangError("domino: height_offset leaves no slot.")
    if spec.width + length_offset - (spec.thickness + height_offset) <= _EPS:
        raise LangError("domino: length_offset leaves the slot no longer than it is high.")
    if fence is not None and fence <= 0:
        raise LangError("domino: fence must be positive.")
    if remaining is not None and remaining < 0:
        raise LangError("domino: remaining must not be negative.")
    if loose < 0:
        raise LangError("domino: loose must not be negative.")
    if marks is not None and (mark_depth <= 0 or mark_length <= 0):
        raise LangError("domino: mark_depth and mark_length must be positive.")
    return Domino(spec, spacing, None if fence is None else float(fence), face,
                  None if remaining is None else float(remaining), float(loose), float(length_offset),
                  float(height_offset), marks, float(mark_depth), float(mark_length))


# -- Clamex P ------------------------------------------------------------------------------------------

@dataclass(frozen=True)
class Clamex:
    model: data.ClamexModel
    spacing: Spacing
    face: FaceChoice = None
    guide_d: float = data.CLAMEX_GUIDE_DIAMETER
    through: bool = False
    label: ClassVar[str] = "clamex"

    def join(self, part: Board, /, partners: list[Board]) -> None:
        _join(self, part, partners)

    def check(self, c: Contact, stations: list[float]) -> None:
        f = c.face_on
        if not self.through and data.CLAMEX_GUIDE_DEPTH >= f.thickness - _EPS:
            raise LangError(f"clamex: the {data.CLAMEX_GUIDE_DEPTH:g} mm guide holes go through {f.path}; "
                            "give through=True.", c.edge_on.path)

    def place(self, c: Contact, stations: list[float]) -> None:
        g = _Geometry(c)
        e, f = c.edge_on, c.face_on
        access = _big_face(self.label, e, self.face, _hidden(e))
        centres, width = self.model.access_centers, self.model.access_width
        guide_depth: DepthSpec = through if self.through else data.CLAMEX_GUIDE_DEPTH
        for i, s in enumerate(stations, 1):
            name = e.unique_op_name(f"clamex_{f.name}_{i}")
            if len(centres) == 1:
                e.add_hole(access, g.on_board(s, centres[0]), width, e.thickness / 2, name)
            else:
                shape = slot_shape(g.on_board(s, centres[0]), g.on_board(s, centres[-1]), width)
                e.add_pocket(access, shape, e.thickness / 2, name)
            for suffix, offset in (("a", -0.5), ("b", 0.5)):
                at = g.on_face(s + offset * data.CLAMEX_GUIDE_SPACING, g.middle)
                f.add_hole(c.face, at, self.guide_d, guide_depth, f.unique_op_name(f"clamex_{e.name}_{i}{suffix}"))


def clamex(model: ClamexModel = "P-10", *, count: int | None = None, at: Sequence[PosLike] | None = None,
           end: float = data.DEFAULT_END_OFFSET, face: FaceChoice = None,
           guide_d: float = data.CLAMEX_GUIDE_DIAMETER, through: bool = False) -> Clamex:
    """Lamello Clamex P (`"P-10"` or `"P-14"`): per station an access slot
    (P-10) or hole (P-14) in this board's access face, half its thickness
    deep, and two guide holes in the other board's face, 101 apart and
    centred on this board's thickness, `guide_d` wide and 8 deep or
    `through`. `end` is the distance of the outer connectors from the
    contact's ends."""
    if guide_d <= 0:
        raise LangError("clamex: guide_d must be positive.")
    return Clamex(data.CLAMEX_MODELS[model], _spacing("clamex", count, end, at), face, float(guide_d), through)


# -- Cabineo ---------------------------------------------------------------------------------------------

@dataclass(frozen=True)
class Cabineo:
    model: CabineoModel
    guide: data.GuideHole
    spacing: Spacing
    face: FaceChoice = None
    surface: CabineoSurface | None = None
    #: Depth and widening of the anti-break relief.
    anti_break: tuple[float, float] = (data.CABINEO_ANTI_BREAK_DEPTH, data.CABINEO_ANTI_BREAK_DISTANCE)
    through: bool = False
    label: ClassVar[str] = "cabineo"

    @property
    def access_depth(self) -> float:
        return data.CABINEO_FLUSH_ACCESS_DEPTH if self.surface == "flush" else data.CABINEO_ACCESS_DEPTH

    def join(self, part: Board, /, partners: list[Board]) -> None:
        _join(self, part, partners)

    def check(self, c: Contact, stations: list[float]) -> None:
        e, f = c.edge_on, c.face_on
        if self.access_depth >= e.thickness - _EPS:
            raise LangError(f"cabineo: the {self.access_depth:g} mm deep pocket goes through this board "
                            f"({e.thickness:g} thick).", e.path)
        if not self.through and self.guide.depth >= f.thickness - _EPS:
            raise LangError(f"cabineo: the {self.guide.depth:g} mm deep hole goes through {f.path}; "
                            "give through=True.", e.path)

    def place(self, c: Contact, stations: list[float]) -> None:
        g = _Geometry(c)
        e, f = c.edge_on, c.face_on
        access = _big_face(self.label, e, self.face, _hidden(e))
        centres = data.CABINEO_ACCESS_CENTERS
        offset = data.CABINEO_FLUSH_GUIDE_OFFSET if self.surface == "flush" else data.CABINEO_GUIDE_OFFSET
        across = g.inside(access, offset)
        guide = self.guide
        guide_depth: DepthSpec = through if self.through else guide.depth
        for i, s in enumerate(stations, 1):
            base = f"cabineo_{f.name}_{i}"
            # Holes first: a hole is placed by a point on the face, which a
            # relief cut first would have removed.
            for letter, centre in zip("abc", centres):
                e.add_hole(access, g.on_board(s, centre), data.CABINEO_ACCESS_DIAMETER, self.access_depth,
                           e.unique_op_name(base + letter))
            if self.surface == "flush":
                shape = slot_shape(g.on_board(s, 0.0), g.on_board(s, centres[-1]), data.CABINEO_FLUSH_RELIEF_WIDTH)
                e.add_pocket(access, shape, data.CABINEO_FLUSH_RELIEF_DEPTH, e.unique_op_name(base + "_relief"))
            elif self.surface == "anti-break":
                depth, widening = self.anti_break
                circles = [circle(data.CABINEO_ACCESS_DIAMETER + 2 * widening, g.on_board(s, centre), 16)
                           for centre in centres]
                shape = circles[0].union(circles[1]).union(circles[2])
                e.add_pocket(access, shape, depth, e.unique_op_name(base + "_relief"))
            name = f.unique_op_name(f"cabineo_{e.name}_{i}")
            at = g.on_face(s, across)
            f.add_hole(c.face, at, guide.diameter, guide_depth, name)
            if guide.collar_diameter is not None and guide.collar_depth is not None:
                f.add_pocket(c.face, circle(guide.collar_diameter, at, 16), guide.collar_depth,
                             f.unique_op_name(name + "_collar"))


def cabineo(model: CabineoModel = "8", *, count: int | None = None, at: Sequence[PosLike] | None = None,
            end: float = data.DEFAULT_END_OFFSET, face: FaceChoice = None, insert: CabineoInsert | None = None,
            surface: CabineoSurface | None = None,
            anti_break: tuple[float, float] = (data.CABINEO_ANTI_BREAK_DEPTH, data.CABINEO_ANTI_BREAK_DISTANCE),
            through: bool = False) -> Cabineo:
    """Lamello Cabineo (`"8"`, `"12"` or `"8 M6"`): per station three
    overlapping 15 mm holes, 10.5 deep, in this board's access face where
    the connector sits, open toward its end, and the hole for its screw in
    the other board's face, 5 mm from the access face across this board's
    thickness: 5 x 8 for the Cabineo 8, 5 x 12 for the 12, and for the
    8 M6 by `insert`: 8 x 13.5 for "M6 x 12.3", 8 x 16.5 for "M6 x 15.3",
    7.9 x 13.5 with a 12.7 x 0.8 collar for a "threaded insert" (the
    default). `surface="flush"` sinks the connector 0.5 deeper under a
    0.8 deep relief; `"anti-break"` adds a relief `anti_break` = (depth,
    widening). `through` drills the screw hole through the other board.
    `end` is the distance of the outer connectors from the contact's ends."""
    if model == "8 M6":
        key = _INSERT_KEYS[insert or "threaded insert"]
    elif insert is not None:
        raise LangError(f"cabineo: insert= is for the Cabineo 8 M6, not the {model}.")
    else:
        key = model
    depth, widening = anti_break
    if depth <= 0 or widening < 0:
        raise LangError("cabineo: anti_break needs a positive depth and a widening of at least 0.")
    return Cabineo(model, data.CABINEO_GUIDE_HOLES[key], _spacing("cabineo", count, end, at), face, surface,
                   (float(depth), float(widening)), through)
