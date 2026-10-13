"""Tenons: integral mortise and tenon between two boards where one meets the
other edge-on (see `lang.core.contact`).

`shelf.join(left, right, using=tenons(count=3, width=50))`: the board that
meets the other edge-on grows tenons out of its end, as thick as the board
and as long as the other board is thick (`remaining=` shorter, for a blind
mortise); the other board gets a mortise per tenon, `clearance=` larger
along the joint and across it, through, or `extra_depth=` deeper than the
tenon when blind. Either board may make the call. Both are cut from their
big faces: the tenons are part of the board's outline, the mortises are
through cuts or pockets.

A router leaves its radius in every inside corner, so both boards get
dog-bone reliefs for a `tool=` mm cutter, `relief=` wider than the tool:
`dogbones="corner"` puts each on the corner's bisector, through the corner;
`"hidden"` puts them into the tenon's root and past the mortise's ends,
where the shoulder covers them once assembled; None leaves the corners
square (`board.dogbones()` can relieve them later). A mortise corner where the
mortise breaks out of its board needs none, nor does a tenon flush with the
end of its board. The reliefs' geometry is `lang.core.dogbones`, shared
with half laps and `board.dogbones()`. With dog bones, the tool routes the
gaps between the tenons, which must be at least as wide as it, and a
corner dog bone bites into the tenon's side at its root, so a tenon must
be wider than its two bites.

Along each contact: `count=` tenons `width=` wide, the outer ones `margin=`
from the contact's ends (a single one centred), `even=True` for tenons as
wide as the gaps between them, or tenons centred at the positions `at=`.
`clearance=(along, across)` is the mortise's play in total, half of it on
each side.

As the tenons_native add-in makes them, defaults included. Its screws and
connectors in the gaps between the tenons are joins of their own, which
take their stations from what this joint made (`cabineo(gaps=t)`,
`screws(gaps=t)`, `screws(tenons=t)`), so the tenon joint keeps a record
per contact.
"""
from __future__ import annotations

import math

from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import ClassVar

from shapely.geometry import Point

from ..core.contact import Contact
from ..core.dogbones import DogBones, corner_relief, hidden_relief
from ..core.errors import LangError, one_of
from ..core.part import Board
from ..core.refs import DepthSpec, Pos, PosLike, to
from ..core.shapes import Shape, box_shape
from .common import (EPS, PROBE, ContactGeometry, ContactJoint, Naming, Point2, Spacing, TenonPlacement,
                     hidden_fits, hidden_width, join_contacts, make_spacing, opposite_face, union_all)

#: How far a tenon reaches back into its board, so it joins the outline cleanly, mm.
_OVERLAP = 1.0


@dataclass(frozen=True)
class Tenons(ContactJoint):
    count: int | None
    width: float | None
    margin: float
    even: bool
    at: tuple[Pos, ...] | None
    remaining: float
    #: The mortise's play (along the joint, across it), each in total: half on each side.
    clearance: tuple[float, float]
    extra_depth: float
    tool: float
    relief: float
    dogbones: DogBones | None
    #: What the joint made, per contact, for the joints that sit in its gaps;
    #: only joins that succeeded.
    made: list[TenonPlacement] = field(default_factory=list[TenonPlacement], compare=False, repr=False)
    label: ClassVar[str] = "tenons"

    @property
    def radius(self) -> float:
        """The reliefs' radius: the tool's plus half the relief."""
        return (self.tool + self.relief) / 2

    def join(self, part: Board, /, partners: list[Board]) -> None:
        planned = join_contacts(self, part, partners)
        # Recorded once the whole join has succeeded: a join that fails,
        # whichever board it fails on, leaves no placement behind.
        self.made.extend(TenonPlacement(c, tuple(stations), self.width_on(c), c.face_on.thickness - self.remaining)
                         for c, stations in planned)

    def placements(self, part: Board, other: Board) -> list[TenonPlacement]:
        """What these tenons made between the two boards."""
        found = [p for p in self.made if {id(p.contact.edge_on), id(p.contact.face_on)} == {id(part), id(other)}]
        if not found:
            raise LangError("the two are not joined with the tenons given; join them with the tenons first.")
        return found

    def width_on(self, c: Contact) -> float:
        """The tenons' width on a contact: as given, or with `even` as wide
        as the gaps: n tenons and n - 1 gaps share the room between the
        margins."""
        if self.even:
            assert self.count is not None
            return (c.length - 2 * self.margin) / (2 * self.count - 1)
        assert self.width is not None
        return self.width

    def stations(self, c: Contact) -> list[float]:
        """The tenons' centres along the contact."""
        if self.at is not None:
            return Spacing(None, 0.0, self.at).stations(c)
        assert self.count is not None
        if self.count == 1:
            return [(c.lo + c.hi) / 2]
        w = self.width_on(c)
        if w <= EPS or c.length - 2 * self.margin - w <= EPS:
            raise LangError(f"margin={self.margin:g} leaves no room for {self.count} tenons {w:g} wide on the "
                            f"{c.length:g} mm contact ({c.axis} {c.lo:g} to {c.hi:g}).")
        return Spacing(self.count, self.margin + w / 2, None).stations(c)

    def check(self, c: Contact, stations: list[float]) -> None:
        e, f = c.edge_on, c.face_on
        w = self.width_on(c)
        if self.remaining >= f.thickness - EPS:
            raise LangError(f"remaining={self.remaining:g} leaves no tenon in {f.path} ({f.thickness:g} thick).")
        if stations[0] - w / 2 < c.lo - EPS or stations[-1] + w / 2 > c.hi + EPS:
            raise LangError(f"a {w:g} mm tenon reaches past the contact ({c.lo:g} to {c.hi:g}).")
        if any(b - a < w - EPS for a, b in zip(stations, stations[1:])):
            raise LangError(f"the {w:g} mm tenons overlap.")
        # [found by fuzzing, 2026-10-13: tenons 1.1 wide, 1.1 apart, with
        # 8 mm corner dog bones, which ate them and left islands of the board]
        gap = min((b - a - w for a, b in zip(stations, stations[1:])), default=math.inf)
        if self.dogbones is not None and gap < self.tool - EPS:
            raise LangError(f"the {gap:g} mm gaps between the tenons are narrower than the {self.tool:g} mm tool "
                            "that cuts them; give fewer or narrower tenons, a smaller tool= or dogbones=None.")
        if self.dogbones == "corner":
            bite = self.radius - self.tool / (2 * math.sqrt(2))
            if w <= 2 * bite + EPS:
                raise LangError(f"corner dog bones cut {bite:.3g} into each side of a tenon at its root; the "
                                f"tenons must be wider than {2 * bite:.3g}.")
        if self.dogbones == "hidden":
            # Each is a circle as wide as the tool plus the relief: one bites
            # into each side of a tenon and reaches that far along it from
            # the shoulder; a mortise's spans its width across the joint.
            d = hidden_width(self.tool, self.relief)
            if w <= d + EPS:
                raise LangError(f"hidden dog bones cut {d / 2:g} into each side of a tenon; the tenons must be "
                                f"wider than {d:g}.")
            across = e.thickness + self.clearance[1]
            if not hidden_fits(across, self.tool, self.relief):
                raise LangError(f"hidden dog bones are {d:g} across, wider than the mortises across the joint "
                                f"({across:g}): they would show past the shoulder; use corner dog bones or a "
                                "smaller tool.")
            length = f.thickness - self.remaining
            if not hidden_fits(length, self.tool, self.relief):
                raise LangError(f"hidden dog bones reach {d:g} along the tenons from the shoulder, past the end of "
                                f"the {length:g} mm tenons; use corner dog bones, a smaller tool or less "
                                "remaining.")

    def place(self, c: Contact, stations: list[float], naming: Naming) -> None:
        g = ContactGeometry(c)
        e, f = c.edge_on, c.face_on
        w = self.width_on(c)
        length = f.thickness - self.remaining
        depth = length + self.extra_depth
        mortise_depth: DepthSpec | None = (
            None if depth >= f.thickness - EPS else to(opposite_face(c.face), self.extra_depth - self.remaining))
        # The reliefs and the material probes use the outlines as they were
        # before this joint.
        e_outline, f_outline = e.outline, f.outline
        across_lo, across_hi = e.box().lo[c.across], e.box().hi[c.across]
        along_clear, across_clear = self.clearance[0] / 2, self.clearance[1] / 2
        for i, s in enumerate(stations):
            n = naming.number(i)
            lo, hi = s - w / 2, s + w / 2
            e.add_to_outline(_box(g.on_board(lo, _OVERLAP), g.on_board(hi, -length)))
            reliefs = [self._root_relief(g, x, side) for x, side in ((lo, -1.0), (hi, 1.0))
                       if self.dogbones is not None
                       and e_outline.geometry.contains(_point(g.on_board(x + side * PROBE, PROBE)))]
            if reliefs:
                e.add_cut(union_all(reliefs), name=naming(e, f"tenon_{f.name}_{n}_relief"))
            corners = (lo - along_clear, across_lo - across_clear), (hi + along_clear, across_hi + across_clear)
            mortise = _box(g.on_face(*corners[0]), g.on_face(*corners[1]))
            for along, across, into_along, into_across in _corners(corners) if self.dogbones is not None else []:
                outside = g.on_face(along - into_along * PROBE, across - into_across * PROBE)
                if f_outline.geometry.contains(_point(outside)):
                    mortise = mortise.union(self._mortise_relief(g, along, across, into_along, into_across))
            name = naming(f, f"mortise_{e.name}_{n}")
            if mortise_depth is None:
                f.add_cut(mortise, name=name)
            else:
                f.add_pocket(c.face, mortise, mortise_depth, name=name)

    def _root_relief(self, g: ContactGeometry, along: float, side: float) -> Shape:
        """The relief at a tenon's root, the corner where its side at
        `along` meets the board's end; `side` is -1 at the tenon's start,
        +1 at its end. The tenon grows toward negative distances from the
        edge."""
        corner = g.on_board(along, 0.0)
        out = g.along_board(0.0, -1.0)                        # along the tenon's side, away from the board
        if self.dogbones == "hidden":
            return hidden_relief(corner, out, self.tool, self.relief)     # biting into the tenon's side
        return corner_relief(corner, g.along_board(side, 0.0), out, self.tool, self.relief)

    def _mortise_relief(self, g: ContactGeometry, along: float, across: float, into_along: float,
                        into_across: float) -> Shape:
        """The relief at a mortise corner; `into_*` point into the mortise."""
        corner = g.on_face(along, across)
        end = g.along_face(0.0, into_across)                  # along the mortise's end, across the joint
        if self.dogbones == "hidden":
            # On the mortise's end: it stays tangent to the long side and
            # reaches past the end, under the shoulder.
            return hidden_relief(corner, end, self.tool, self.relief)
        return corner_relief(corner, g.along_face(into_along, 0.0), end, self.tool, self.relief)


def _box(a: Point2, b: Point2) -> Shape:
    return box_shape(min(a[0], b[0]), min(a[1], b[1]), max(a[0], b[0]), max(a[1], b[1]))


def _point(p: Point2) -> Point:
    return Point(*p)


def _corners(corners: tuple[tuple[float, float], tuple[float, float]]
             ) -> list[tuple[float, float, float, float]]:
    """The four corners of the box from (along, across) to (along, across),
    each with the directions into the box."""
    (a0, c0), (a1, c1) = corners
    return [(a0, c0, 1.0, 1.0), (a1, c0, -1.0, 1.0), (a1, c1, -1.0, -1.0), (a0, c1, 1.0, -1.0)]


def tenons(count: int | None = None, *, width: float | None = None, margin: float | None = None, even: bool = False,
           at: Sequence[PosLike] | None = None, remaining: float = 0.0, clearance: tuple[float, float] = (0.1, 0.1),
           extra_depth: float = 0.5, tool: float = 6.0, relief: float = 0.1,
           dogbones: DogBones | None = "corner") -> Tenons:
    """Integral tenons: `count` of them `width` wide with the outer ones
    `margin` from the contact's ends (30 by default, with two or more), or
    `even=True` for tenons as wide as the gaps between them, or `at=`
    positions for their centres. Through the other board, or `remaining`
    short of its far face, the mortise then `extra_depth` deeper than the
    tenon. `clearance=(along, across)` is the mortise's play along the
    joint and across it, each in total, half of it on each side. Dog bones
    for a `tool` mm cutter, `relief` wider, on the corners (`"corner"`),
    under the shoulder (`"hidden"`), or None for square corners."""
    label = "tenons"
    # one of count= and at=, a count of 1 or more, a list of positions
    spacing = make_spacing(label, count, at)
    if margin is not None and (spacing.count is None or (spacing.count == 1 and not even)):
        raise LangError("tenons: margin= spaces two tenons or more from the contact's ends; with "
                        f"{'at=' if spacing.count is None else 'count=1, which centres the one,'} it has nothing to "
                        "do, leave it out.")
    if spacing.count is None:
        if even:
            raise LangError("tenons: give at= or even=, not both.")
        if width is None:
            raise LangError("tenons: tenons at= positions need a width=.")
    else:
        if even and spacing.count < 2:
            raise LangError("tenons: even= needs two tenons or more.")
        if even and width is not None:
            raise LangError("tenons: even= works the width out; give no width=.")
        if not even and width is None:
            raise LangError("tenons: give width=, or even=True.")
    if width is not None and width <= 0:
        raise LangError("tenons: width must be positive.")
    spaced = 30.0 if margin is None else float(margin)
    if spaced < 0 or remaining < 0 or extra_depth < 0 or min(clearance) < 0 or relief < 0:
        raise LangError("tenons: margin, remaining, extra_depth, clearance and relief must not be negative.")
    if tool <= 0:
        raise LangError("tenons: tool must be positive.")
    if dogbones is not None:
        one_of(dogbones, DogBones, "tenons(dogbones=)")
    return Tenons(count, None if width is None else float(width), spaced, even, spacing.at, float(remaining),
                  (float(clearance[0]), float(clearance[1])), float(extra_depth), float(tool), float(relief),
                  dogbones)
