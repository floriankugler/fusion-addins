"""Screws: through the board that is met into the end of the board that
meets it edge-on, or through the tenons of a tenon joint where they lie
open (see `lang.core.contact`, `lang.joints.tenons`).

`bottom.join(left, right, using=screws(count=3))` drills each side through
from its outer face, centred on the bottom's thickness, for screws into the
bottom's end; `countersink=True` sinks their heads into that face. With
`gaps=t` they sit in the gaps between and beside the tenons `t` joined
before, one in the middle of each, or with `offset=` two beside each tenon,
that far out from its edges.

With `tenons=t` they go through the tenons themselves, square to the tenon
board's faces, halfway along each tenon: one in its middle, or with
`offset=` two, that far in from its edges. That needs a tenon whose face
lies open, its mortise running out of the other board's edge, as with a
top flush with the sides' top: the tenon board is drilled from that open
face, and the screw is driven on into the other board.

As the tenons_native add-in's screws: 4 mm, 12 from the tenons' edges, a
90 degree countersink twice the screw plus 0.4 wide.
"""
from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import ClassVar

from shapely.geometry import Point

from lib import connector_data as data

from ..core.contact import Contact
from ..core.errors import LangError
from ..core.part import Board, Face
from ..core.refs import PosLike, through
from .common import (EPS, ContactGeometry, SpacedJoint, Spacing, TenonPlacement, TenonSource, face_toward,
                     make_spacing, opposite_face, placement_of)
from .tenons import Tenons

#: How far beyond the tenon board's face the other board is probed for
#: material, to tell an open tenon from a closed one, mm.
_OPEN_PROBE = 1.0


@dataclass(frozen=True)
class Screws(SpacedJoint):
    d: float
    spacing: Spacing
    tenons: TenonSource | None = None
    offset: float | None = None
    countersink: bool = False
    label: ClassVar[str] = "screws"

    @property
    def sink(self) -> float:
        """The countersink as a chamfer on the hole's edge."""
        return (data.countersink_diameter(self.d) - self.d) / 2 if self.countersink else 0.0

    def contacts_with(self, part: Board, other: Board) -> list[Contact]:
        if self.tenons is not None:
            return [p.contact for p in self.tenons.placements(part, other)]
        return super().contacts_with(part, other)

    def stations(self, c: Contact) -> list[float]:
        if self.tenons is not None:
            p = placement_of(self.tenons, c)
            if self.offset is None:
                return list(p.centres)
            return sorted(x for lo, hi in p.tenons() for x in (lo + self.offset, hi - self.offset))
        if self.spacing.gaps is not None and self.offset is not None:
            p = placement_of(self.spacing.gaps, c)
            return sorted(x for lo, hi in p.tenons() for x in (lo - self.offset, hi + self.offset))
        return super().stations(c)

    def check(self, c: Contact, stations: list[float]) -> None:
        e, f = c.edge_on, c.face_on
        if self.tenons is not None:
            p = placement_of(self.tenons, c)
            if self.offset is not None and 2 * self.offset >= p.width - EPS:
                raise LangError(f"offset={self.offset:g} must be less than half the {p.width:g} mm tenons.")
            self._open_face(c, p)
            if self.sink >= e.thickness - EPS:
                raise LangError(f"the countersink is deeper than {e.path} is thick.")
            return
        if self.sink >= f.thickness - EPS:
            raise LangError(f"the countersink is deeper than {f.path} is thick.")
        for s in stations:
            if not c.lo - EPS <= s <= c.hi + EPS:
                raise LangError(f"a screw at {c.axis}={s:g} lies outside the contact ({c.lo:g} to {c.hi:g}).")

    def place(self, c: Contact, stations: list[float]) -> None:
        g = ContactGeometry(c)
        e, f = c.edge_on, c.face_on
        if self.tenons is None:
            # Through the board that is met, from its outer face.
            outer = opposite_face(c.face)
            for i, s in enumerate(stations, 1):
                f.add_hole(outer, g.on_face(s, g.middle), self.d, through, f.unique_op_name(f"screw_{e.name}_{i}"),
                           chamfer=self.sink)
            return
        p = placement_of(self.tenons, c)
        face = self._open_face(c, p)
        for i, s in enumerate(stations, 1):
            e.add_hole(face, g.on_board(s, -p.length / 2), self.d, through, e.unique_op_name(f"screw_{f.name}_{i}"),
                       chamfer=self.sink)

    def _open_face(self, c: Contact, p: TenonPlacement) -> Face:
        """The tenon board's big face that lies open: on the side where the
        mortise runs out of the other board's edge."""
        e, f = c.edge_on, c.face_on
        g = ContactGeometry(c)
        b, t = e.box(), c.across
        open_sides = [sign for sign, value in ((-1, b.lo[t]), (1, b.hi[t]))
                      if not f.outline.geometry.contains(Point(g.on_face(p.centres[0], value + sign * _OPEN_PROBE)))]
        if not open_sides:
            raise LangError(f"the tenons in {f.path} are closed in on both sides; a screw through a tenon needs its "
                            f"mortise to run out of {f.path}'s edge, so that the tenon's face lies open.")
        # Open on both sides: drill from the face that is not shown.
        sign = open_sides[0] if len(open_sides) == 1 else -e.show_face.direction.sign
        return face_toward(e, sign, t)


def screws(d: float = data.SCREW_DIAMETER, *, count: int | None = None, at: Sequence[PosLike] | None = None,
           gaps: Tenons | None = None, tenons: Tenons | None = None, end: float = data.DEFAULT_END_OFFSET,
           offset: float | None = None, countersink: bool = False) -> Screws:
    """Screws `d` thick: `count` of them with the outer ones `end` from the
    contact's ends, or at the positions `at=`, through the board that is met
    into the other's end; or relative to tenons joined before, in their
    `gaps=` or through the `tenons=` themselves, one each or, with
    `offset=`, two per tenon that far from its edges (outside them in the
    gaps, inside them through the tenons). `countersink=True` sinks the
    heads at 90 degrees, twice `d` plus 0.4 wide."""
    if [count is not None, at is not None, gaps is not None, tenons is not None].count(True) != 1:
        raise LangError("screws: give one of count=, at=, gaps= or tenons=.")
    if d <= 0:
        raise LangError("screws: d must be positive.")
    if offset is not None:
        if gaps is None and tenons is None:
            raise LangError("screws: offset= places screws beside or in tenons; give gaps= or tenons= too.")
        if offset <= 0:
            raise LangError("screws: offset must be positive.")
    spacing = Spacing(None, 0.0, None) if tenons is not None else make_spacing("screws", count, end, at, gaps)
    return Screws(float(d), spacing, tenons, None if offset is None else float(offset), countersink)
