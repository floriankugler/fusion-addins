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
from typing import ClassVar, Literal

from lib import connector_data as data

from ..core.contact import Contact
from ..core.errors import LangError, one_of
from ..core.geometry import NARROWEST
from ..core.part import Board, Face
from ..core.refs import DepthSpec, PosLike, through, to
from ..core.shapes import circle
from .common import (EPS, ContactGeometry, FaceChoice, Naming, SpacedJoint, Spacing, check_across, check_along,
                     check_gaps, face_choice, hidden_face, make_spacing, opposite_face, pick_face, start_index)
from .tenons import Tenons

DominoSize = Literal["4x20", "5x30", "6x40", "8x36", "8x40", "8x50", "8x80", "8x100", "10x50", "10x80",
                     "10x100", "12x100", "12x140", "14x75", "14x100", "14x140"]
ClamexModel = Literal["P-10", "P-14"]
CabineoModel = Literal["8", "12", "8 M6"]
CabineoInsert = Literal["M6 x 12.3", "M6 x 15.3", "threaded insert"]
CabineoSurface = Literal["flush", "anti-break"]
#: Which Dominos get a mark: all, or all but the first and last, which the
#: machine's end stops locate.
DominoMarks = Literal["all", "middle"]
#: A Domino mark starts this far outside the board, so it runs out of the
#: board's end cleanly, mm.
_RUN_OUT = 1.0
_INSERT_KEYS: dict[str, str] = {"M6 x 12.3": "8 M6 x 12.3", "M6 x 15.3": "8 M6 x 15.3",
                                "threaded insert": "8 M6 threaded insert"}


# -- Domino ------------------------------------------------------------------------------------------

@dataclass(frozen=True)
class Domino(SpacedJoint):
    size: data.DominoSize
    spacing: Spacing
    fence: float | None = None
    face: FaceChoice = None
    remaining: float | None = None
    loose: float = 0.0
    undersize: float = data.DOMINO_SLOT_UNDERSIZE
    marks: DominoMarks | None = "all"
    mark_depth: float = data.DOMINO_MARK_DEPTH
    mark_length: float = data.DOMINO_MARK_LENGTH
    label: ClassVar[str] = "domino"

    @property
    def slot_height(self) -> float:
        """Across the contact: the Domino's thickness less the undersize."""
        return self.size.thickness - self.undersize

    @property
    def slot_length(self) -> float:
        """Along the contact: the Domino's width less the undersize; the
        loose slots are `loose` longer."""
        return self.size.width - self.undersize

    def _reference(self, e: Board) -> Face:
        """The face the machine's fence rests on, which carries the marks."""
        return pick_face(e, self.face, e.show_face)

    def _centre(self, g: ContactGeometry) -> float:
        if self.fence is None:
            return g.middle
        return g.inside(self._reference(g.c.edge_on), self.fence)

    def _lengths(self, c: Contact, stations: list[float]) -> list[float]:
        """Each slot's length: the first from the front, left or bottom
        exact, the others `loose` longer."""
        exact = start_index(c.edge_on, c.axis, len(stations))
        return [self.slot_length + (self.loose if i != exact else 0.0) for i in range(len(stations))]

    def check(self, c: Contact, stations: list[float]) -> None:
        e, f = c.edge_on, c.face_on
        self._reference(e)
        h = self.slot_height
        if h >= e.thickness - EPS:
            raise LangError(f"the {h:g} mm high slot is not thinner than {e.path} ({e.thickness:g}).")
        centre = self._centre(ContactGeometry(c))
        b, t = e.box(), c.across
        if centre - h / 2 < b.lo[t] - EPS or centre + h / 2 > b.hi[t] + EPS:
            raise LangError(f"at fence={self.fence} the slot does not fit within {e.path}'s thickness.")
        if self.marks is not None and self.mark_depth >= e.thickness - EPS:
            raise LangError(f"mark_depth={self.mark_depth:g} is not less than {e.path}'s thickness.")
        if self.remaining is None:
            depth = self.size.length / 2 + data.DOMINO_DEPTH_OFFSET
            if depth >= f.thickness - EPS:
                raise LangError(f"a {self.size.key} needs a {depth:g} mm deep slot, {f.path} is "
                                f"{f.thickness:g} thick; pick a shorter Domino or give remaining=.")
        elif self.remaining >= f.thickness - EPS:
            raise LangError(f"remaining={self.remaining:g} leaves no slot in {f.path} ({f.thickness:g} thick).")
        check_along(c, "the slot", [(s - n / 2, s + n / 2) for s, n in zip(stations, self._lengths(c, stations))])
        check_across(c, "the slot", centre - h / 2, centre + h / 2)

    def place(self, c: Contact, stations: list[float], naming: Naming) -> None:
        g = ContactGeometry(c)
        e, f = c.edge_on, c.face_on
        centre, h = self._centre(g), self.slot_height
        depth: DepthSpec = (self.size.length / 2 + data.DOMINO_DEPTH_OFFSET if self.remaining is None
                            else to(opposite_face(c.face), -self.remaining))
        for i, (s, length) in enumerate(zip(stations, self._lengths(c, stations))):
            half_span = (length - h) / 2
            f.add_slot(c.face, g.on_face(s - half_span, centre), g.on_face(s + half_span, centre), h, depth,
                       name=naming(f, f"domino_{e.name}_{naming.number(i)}"))
        if self.marks is None:
            return
        reference = self._reference(e)
        for i, s in enumerate(stations):
            if self.marks == "middle" and len(stations) > 1 and i in (0, len(stations) - 1):
                continue
            # Across the reference face from the board's end, where the
            # machine's centre mark is lined up with it.
            e.add_vgroove(reference, g.on_board(s, -_RUN_OUT), g.on_board(s, self.mark_length), self.mark_depth,
                          naming(e, f"domino_{f.name}_{naming.number(i)}_mark"))


def domino(size: DominoSize, *, count: int | None = None, at: Sequence[PosLike] | None = None,
           end: float | None = None, fence: float | None = None, face: FaceChoice = None,
           remaining: float | None = None, loose: float = 0.0,
           undersize: float = data.DOMINO_SLOT_UNDERSIZE, marks: DominoMarks | None = "all",
           mark_depth: float = data.DOMINO_MARK_DEPTH, mark_length: float = data.DOMINO_MARK_LENGTH) -> Domino:
    """Dominos of `size` ("5x30": thickness x length): per station a slot
    in the face of the board that is met, half the Domino's length plus 0.5
    deep, or as deep as leaves `remaining` of that board, and a mark on the
    edge-on board for the Domino machine. `end` is the distance of the
    outer Dominos from the contact's ends with `count=` 2 or more, 37 by
    default (the machine's stop latches; 20 with the additional stop). The
    slots are centred on
    the edge-on board's thickness, or `fence` from its reference face (the
    show face, or `face=`), the face the machine's fence rests on.

    The marks are 90 degree V-grooves in the reference face, `mark_depth`
    deep (0.3) and running `mark_length` (4) in from the board's end, one
    per Domino (`marks="all"`), all but the first and last, which the
    machine's stops locate (`"middle"`), or none (`None`).

    `undersize` (0.2) makes every slot that much shorter and narrower
    than the Domino, its outline inset by half of it on every side, so the
    Domino fits tight (negative: larger); the depth stays. `loose` makes
    every slot but the first (from the front, left or bottom) that much
    longer still, as the machine's wider settings do (6 or 10)."""
    spec = data.domino_size(one_of(size, DominoSize, "domino()"))
    face = face_choice("domino", face)
    if marks is not None:
        one_of(marks, DominoMarks, "domino(marks=)")
    spacing = make_spacing("domino", count, at, end=end, default_end=data.DOMINO_STOP_LATCH)
    # The slot stays longer than it is high: it is as much shorter than
    # the Domino is wide as it is narrower than the Domino is thick.
    if spec.thickness - undersize < NARROWEST - EPS:
        raise LangError(f"domino: undersize={undersize:g} leaves no slot of a {spec.key}.")
    if fence is not None and fence <= 0:
        raise LangError("domino: fence must be positive.")
    if remaining is not None and remaining < 0:
        raise LangError("domino: remaining must not be negative.")
    if loose < 0:
        raise LangError("domino: loose must not be negative.")
    if marks is not None and (mark_depth <= 0 or mark_length <= 0):
        raise LangError("domino: mark_depth and mark_length must be positive.")
    return Domino(spec, spacing, None if fence is None else float(fence), face,
                  None if remaining is None else float(remaining), float(loose), float(undersize), marks,
                  float(mark_depth), float(mark_length))


# -- Clamex P ------------------------------------------------------------------------------------------

@dataclass(frozen=True)
class Clamex(SpacedJoint):
    model: data.ClamexModel
    spacing: Spacing
    face: FaceChoice = None
    guide_d: float = data.CLAMEX_GUIDE_DIAMETER
    through: bool = False
    label: ClassVar[str] = "clamex"

    def check(self, c: Contact, stations: list[float]) -> None:
        e, f = c.edge_on, c.face_on
        pick_face(e, self.face, hidden_face(e))
        check_gaps(self.label, self.spacing, c, data.CLAMEX_MIN_GAP)
        if not self.through and data.CLAMEX_GUIDE_DEPTH >= f.thickness - EPS:
            raise LangError(f"the {data.CLAMEX_GUIDE_DEPTH:g} mm guide holes go through {f.path}; "
                            "give through=True.")
        # the guide holes reach furthest along the contact, the access slot or hole less far
        half = max(data.CLAMEX_GUIDE_SPACING / 2 + self.guide_d / 2, self.model.access_width / 2)
        check_along(c, "the guide holes", [(s - half, s + half) for s in stations])
        middle = ContactGeometry(c).middle
        check_across(c, "the guide holes", middle - self.guide_d / 2, middle + self.guide_d / 2)

    def place(self, c: Contact, stations: list[float], naming: Naming) -> None:
        g = ContactGeometry(c)
        e, f = c.edge_on, c.face_on
        access = pick_face(e, self.face, hidden_face(e))
        centres, width = self.model.access_centers, self.model.access_width
        guide_depth: DepthSpec = through if self.through else data.CLAMEX_GUIDE_DEPTH
        for i, s in enumerate(stations):
            n = naming.number(i)
            name = naming(e, f"clamex_{f.name}_{n}")
            if len(centres) == 1:
                e.add_hole(access, g.on_board(s, centres[0]), width, e.thickness / 2, name)
            else:
                e.add_slot(access, g.on_board(s, centres[0]), g.on_board(s, centres[-1]), width, e.thickness / 2,
                           name)
            for suffix, offset in (("a", -0.5), ("b", 0.5)):
                at = g.on_face(s + offset * data.CLAMEX_GUIDE_SPACING, g.middle)
                f.add_hole(c.face, at, self.guide_d, guide_depth, naming(f, f"clamex_{e.name}_{n}{suffix}"))


def clamex(model: ClamexModel = "P-10", *, count: int | None = None, at: Sequence[PosLike] | None = None,
           gaps: Tenons | None = None, end: float | None = None, face: FaceChoice = None,
           guide_d: float = data.CLAMEX_GUIDE_DIAMETER, through: bool = False) -> Clamex:
    """Lamello Clamex P (`"P-10"` or `"P-14"`): per station an access slot
    (P-10) or hole (P-14) in this board's access face, half its thickness
    deep, and two guide holes in the other board's face, 101 apart and
    centred on this board's thickness, `guide_d` wide and 8 deep or
    `through`. `end` is the distance of the outer connectors from the
    contact's ends with `count=` 2 or more, 60 by default; with `gaps=`
    tenons joined before, one sits in the middle of each gap between and
    beside them, which must be 120 long."""
    if guide_d <= 0:
        raise LangError("clamex: guide_d must be positive.")
    face = face_choice("clamex", face)
    spacing = make_spacing("clamex", count, at, gaps, end=end, default_end=data.DEFAULT_END_OFFSET)
    return Clamex(data.CLAMEX_MODELS[one_of(model, ClamexModel, "clamex()")], spacing, face, float(guide_d), through)


# -- Cabineo ---------------------------------------------------------------------------------------------

@dataclass(frozen=True)
class Cabineo(SpacedJoint):
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

    def check(self, c: Contact, stations: list[float]) -> None:
        e, f = c.edge_on, c.face_on
        pick_face(e, self.face, hidden_face(e))
        check_gaps(self.label, self.spacing, c, data.CABINEO_MIN_GAP)
        if self.access_depth >= e.thickness - EPS:
            raise LangError(f"the {self.access_depth:g} mm deep pocket goes through {e.path} "
                            f"({e.thickness:g} thick).")
        if not self.through and self.guide.depth >= f.thickness - EPS:
            raise LangError(f"the {self.guide.depth:g} mm deep hole goes through {f.path}; give through=True.")
        check_along(c, "the Cabineo", [(s - self._half_along, s + self._half_along) for s in stations])
        # The hole itself: a threaded insert's collar, 12.7 wide 5 from the
        # access face, reaches past a 15 mm board's face, as in the add-in.
        across, half = self._across(ContactGeometry(c)), self.guide.diameter / 2
        check_across(c, "the hole for its screw", across - half, across + half)

    @property
    def _half_along(self) -> float:
        """How far the Cabineo reaches along the contact from its station:
        the access pocket with its relief, or the screw hole's collar."""
        access = data.CABINEO_ACCESS_DIAMETER / 2
        if self.surface == "flush":
            access = max(access, data.CABINEO_FLUSH_RELIEF_WIDTH / 2)
        elif self.surface == "anti-break":
            access += self.anti_break[1]
        return max(access, self.guide.diameter / 2, (self.guide.collar_diameter or 0.0) / 2)

    def _across(self, g: ContactGeometry) -> float:
        """Where the screw hole lies across the contact: 5 mm (5.8 flush)
        from the access face."""
        e = g.c.edge_on
        offset = data.CABINEO_FLUSH_GUIDE_OFFSET if self.surface == "flush" else data.CABINEO_GUIDE_OFFSET
        return g.inside(pick_face(e, self.face, hidden_face(e)), offset)

    def place(self, c: Contact, stations: list[float], naming: Naming) -> None:
        g = ContactGeometry(c)
        e, f = c.edge_on, c.face_on
        access = pick_face(e, self.face, hidden_face(e))
        centres = data.CABINEO_ACCESS_CENTERS
        across = self._across(g)
        guide = self.guide
        guide_depth: DepthSpec = through if self.through else guide.depth
        for i, s in enumerate(stations):
            n = naming.number(i)
            base = f"cabineo_{f.name}_{n}"
            # Holes first: a hole is placed by a point on the face, which a
            # relief cut first would have removed.
            for letter, centre in zip("abc", centres):
                e.add_hole(access, g.on_board(s, centre), data.CABINEO_ACCESS_DIAMETER, self.access_depth,
                           naming(e, base + letter))
            if self.surface == "flush":
                e.add_slot(access, g.on_board(s, 0.0), g.on_board(s, centres[-1]), data.CABINEO_FLUSH_RELIEF_WIDTH,
                           data.CABINEO_FLUSH_RELIEF_DEPTH, naming(e, base + "_relief"))
            elif self.surface == "anti-break":
                depth, widening = self.anti_break
                circles = [circle(data.CABINEO_ACCESS_DIAMETER + 2 * widening, g.on_board(s, centre))
                           for centre in centres]
                shape = circles[0].union(circles[1]).union(circles[2])
                e.add_pocket(access, shape, depth, naming(e, base + "_relief"))
            name = naming(f, f"cabineo_{e.name}_{n}")
            at = g.on_face(s, across)
            f.add_hole(c.face, at, guide.diameter, guide_depth, name)
            if guide.collar_diameter is not None and guide.collar_depth is not None:
                f.add_pocket(c.face, circle(guide.collar_diameter, at), guide.collar_depth,
                             naming(f, name + "_collar"))


def cabineo(model: CabineoModel = "8", *, count: int | None = None, at: Sequence[PosLike] | None = None,
            gaps: Tenons | None = None, end: float | None = None, face: FaceChoice = None,
            insert: CabineoInsert | None = None,
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
    `end` is the distance of the outer connectors from the contact's ends
    with `count=` 2 or more, 60 by default; with `gaps=` tenons joined
    before, one sits in the middle of each gap between and beside them,
    which must be 40 long."""
    one_of(model, CabineoModel, "cabineo()")
    face = face_choice("cabineo", face)
    if insert is not None:
        one_of(insert, CabineoInsert, "cabineo(insert=)")
    if surface is not None:
        one_of(surface, CabineoSurface, "cabineo(surface=)")
    if model == "8 M6":
        key = _INSERT_KEYS[insert or "threaded insert"]
    elif insert is not None:
        raise LangError(f"cabineo: insert= is for the Cabineo 8 M6, not the {model}.")
    else:
        key = model
    depth, widening = anti_break
    if depth <= 0 or widening < 0:
        raise LangError("cabineo: anti_break needs a positive depth and a widening of at least 0.")
    spacing = make_spacing("cabineo", count, at, gaps, end=end, default_end=data.DEFAULT_END_OFFSET)
    return Cabineo(model, data.CABINEO_GUIDE_HOLES[key], spacing, face, surface, (float(depth), float(widening)),
                   through)
