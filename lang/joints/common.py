"""What the joints between boards that meet edge-on share: finding the
contacts with the boards a join names, from either board, the geometry of
a contact, stations along it, and the choice of a big face.

`join_contacts` drives a `ContactJoint`: it finds every contact, asks the
joint for its stations along each, lets it check them all and only then
machine them, so a failed join changes no board.
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
from ..core.refs import Pos, PosLike, Side, as_pos

#: A big face named for a joint: a box side or direction it faces, or
#: inner/outer; None for the joint's default.
FaceChoice = Side | Direction | Literal["inner", "outer"] | None
EPS = 1e-6
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
                if not c.lo - EPS <= pos.value <= c.hi + EPS:
                    raise LangError(f"{label}: at={pos} lies outside the contact with {other} "
                                    f"({c.lo:g} to {c.hi:g}).", path)
                values.append(pos.value)
            values.sort()
            if any(b - a <= EPS for a, b in zip(values, values[1:])):
                raise LangError(f"{label}: two positions in at= coincide.", path)
            return values
        assert self.count is not None
        if self.count > 1 and 2 * self.end >= c.length - EPS:
            raise LangError(f"{label}: end={self.end:g} leaves no room for {self.count} connectors on the "
                            f"{c.length:g} mm contact with {other}.", path)
        return [c.lo + s for s in data.stations(c.length, self.count, self.end)]


def make_spacing(label: str, count: int | None, end: float, at: Sequence[PosLike] | None) -> Spacing:
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

class ContactGeometry:
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


def face_toward(part: Board, sign: int, axis: Axis) -> Face:
    return part.face(part.scope.frame.direction_of(axis, sign))


def opposite_face(face: Face) -> Face:
    return face_toward(face.part, -face.direction.sign, face.axis)


def big_face(label: str, part: Board, choice: FaceChoice, default: Face) -> Face:
    if choice is None:
        return default
    if isinstance(choice, str):
        return part.face(choice)
    d = choice.outward if isinstance(choice, Side) else choice
    if d.axis != part.t_axis:
        raise LangError(f"{label}: face={d.name} is not a big face of this board.", part.path)
    return face_toward(part, d.sign, d.axis)


def hidden_face(part: Board) -> Face:
    """The big face that is not the show face."""
    return opposite_face(part.show_face)


# -- joining ---------------------------------------------------------------------------------------

class ContactJoint(Protocol):
    """A joint made per contact: where along it, a check, the machining."""
    label: ClassVar[str]

    def stations(self, c: Contact) -> list[float]:
        """The positions along the contact, ascending."""
        ...

    def check(self, c: Contact, stations: list[float]) -> None: ...

    def place(self, c: Contact, stations: list[float]) -> None: ...


def join_contacts(joint: ContactJoint, part: Board, partners: list[Board]) -> None:
    """Finds the contacts with the boards named, either one edge-on, checks
    every one, then machines them."""
    label = joint.label
    found: list[Contact] = []
    for other in partners:
        here = contacts(part, other) or contacts(other, part)
        if not here:
            raise LangError(f"{label}: {other.path} does not touch this board with an end or edge on a face.",
                            part.path)
        found.extend(here)
    planned = [(c, joint.stations(c)) for c in found]
    for c, stations in planned:
        joint.check(c, stations)
    for c, stations in planned:
        joint.place(c, stations)


def start_index(part: Board, axis: Axis, count: int) -> int:
    """The index of the first of `count` ascending stations as the part's
    frame counts them: from the front, the left or the bottom."""
    frame = part.scope.frame
    start = next(d for d in (frame.direction(n) for n in ("front", "left", "bottom")) if d.axis == axis)
    return 0 if start.sign < 0 else count - 1
