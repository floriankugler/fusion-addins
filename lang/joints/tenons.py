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
where the shoulder covers them once assembled. A mortise corner where the
mortise breaks out of its board needs none, nor does a tenon flush with the
end of its board. The reliefs' geometry is `lang.core.dogbones`, shared
with half laps and `board.dogbones()`.

Along each contact: `count=` tenons `width=` wide, the outer ones `margin=`
from the contact's ends (a single one centred), `even=True` for tenons as
wide as the gaps between them, or tenons centred at the positions `at=`.

As the tenons_native add-in makes them, defaults included. Its screws and
connectors in the gaps between the tenons are joins of their own, which
take their stations from what this joint made (`cabineo(gaps=t)`,
`screws(gaps=t)`, `screws(tenons=t)`), so the tenon joint keeps a record
per contact.
"""
from __future__ import annotations

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
from .common import (EPS, PROBE, ContactGeometry, ContactJoint, Point2, Spacing, TenonPlacement, make_spacing,
                     opposite_face, union_all)

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
    clearance: tuple[float, float]
    extra_depth: float
    tool: float
    relief: float
    dogbones: DogBones
    #: What the joint made, per contact, for the joints that sit in its gaps.
    made: list[TenonPlacement] = field(default_factory=list[TenonPlacement], compare=False, repr=False)
    label: ClassVar[str] = "tenons"

    @property
    def radius(self) -> float:
        """The reliefs' radius: the tool's plus half the relief."""
        return (self.tool + self.relief) / 2

    def placements(self, part: Board, other: Board) -> list[TenonPlacement]:
        """What these tenons made between the two boards."""
        found = [p for p in self.made if {id(p.contact.edge_on), id(p.contact.face_on)} == {id(part), id(other)}]
        if not found:
            raise LangError(f"gaps=: {part.path} and {other.path} are not joined with these tenons; join them "
                            "with the tenons first.", part.path)
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
            return Spacing(None, 0.0, self.at).stations(self.label, c)
        assert self.count is not None
        if self.count == 1:
            return [(c.lo + c.hi) / 2]
        w = self.width_on(c)
        if w <= EPS or c.length - 2 * self.margin - w <= EPS:
            raise LangError(f"tenons: margin={self.margin:g} leaves no room for {self.count} tenons "
                            f"{w:g} wide on the {c.length:g} mm contact with {c.face_on.path}.",
                            c.edge_on.path)
        return Spacing(self.count, self.margin + w / 2, None).stations(self.label, c)

    def check(self, c: Contact, stations: list[float]) -> None:
        e, f = c.edge_on, c.face_on
        w = self.width_on(c)
        if self.remaining >= f.thickness - EPS:
            raise LangError(f"tenons: remaining={self.remaining:g} leaves no tenon in {f.path} "
                            f"({f.thickness:g} thick).", e.path)
        if stations[0] - w / 2 < c.lo - EPS or stations[-1] + w / 2 > c.hi + EPS:
            raise LangError(f"tenons: a {w:g} mm tenon reaches past the contact with {f.path} "
                            f"({c.lo:g} to {c.hi:g}).", e.path)
        if any(b - a < w - EPS for a, b in zip(stations, stations[1:])):
            raise LangError(f"tenons: the {w:g} mm tenons overlap.", e.path)
        if self.dogbones == "hidden":
            r = self.radius
            if w <= 2 * r:
                raise LangError(f"tenons: hidden dog bones cut {r:g} into each end of a tenon; the tenons must "
                                f"be wider than {2 * r:g}.", e.path)
            if e.thickness + self.clearance[1] < r:
                raise LangError("tenons: hidden dog bones would reach past the far side of the mortise; "
                                "use a smaller tool.", e.path)
            if f.thickness - self.remaining < r:
                raise LangError("tenons: hidden dog bones would reach past the end of the tenon; use a smaller "
                                "tool or less remaining.", e.path)

    def place(self, c: Contact, stations: list[float]) -> None:
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
        for i, s in enumerate(stations, 1):
            lo, hi = s - w / 2, s + w / 2
            e.add_to_outline(_box(g.on_board(lo, _OVERLAP), g.on_board(hi, -length)))
            reliefs = [self._root_relief(g, x, side) for x, side in ((lo, -1.0), (hi, 1.0))
                       if e_outline.geometry.contains(_point(g.on_board(x + side * PROBE, PROBE)))]
            if reliefs:
                e.add_cut(union_all(reliefs), name=e.unique_op_name(f"tenon_{f.name}_{i}_relief"))
            corners = (lo - along_clear, across_lo - across_clear), (hi + along_clear, across_hi + across_clear)
            mortise = _box(g.on_face(*corners[0]), g.on_face(*corners[1]))
            for along, across, into_along, into_across in _corners(corners):
                outside = g.on_face(along - into_along * PROBE, across - into_across * PROBE)
                if f_outline.geometry.contains(_point(outside)):
                    mortise = mortise.union(self._mortise_relief(g, along, across, into_along, into_across))
            name = f.unique_op_name(f"mortise_{e.name}_{i}")
            if mortise_depth is None:
                f.add_cut(mortise, name=name)
            else:
                f.add_pocket(c.face, mortise, mortise_depth, name=name)
        self.made.append(TenonPlacement(c, tuple(stations), w, length))

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


def tenons(count: int | None = None, *, width: float | None = None, margin: float = 30.0, even: bool = False,
           at: Sequence[PosLike] | None = None, remaining: float = 0.0, clearance: tuple[float, float] = (0.1, 0.1),
           extra_depth: float = 0.5, tool: float = 6.0, relief: float = 0.1,
           dogbones: DogBones = "corner") -> Tenons:
    """Integral tenons: `count` of them `width` wide with the outer ones
    `margin` from the contact's ends, or `even=True` for tenons as wide as
    the gaps between them, or `at=` positions for their centres. Through
    the other board, or `remaining` short of its far face, the mortise then
    `extra_depth` deeper than the tenon. `clearance` is the mortise's play
    (along the joint, across it). Dog bones for a `tool` mm cutter, `relief`
    wider, on the corners (`"corner"`) or under the shoulder (`"hidden"`)."""
    label = "tenons"
    # one of count= and at=, a count of 1 or more, a list of positions
    spacing = make_spacing(label, count, 0.0, at)
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
    if margin < 0 or remaining < 0 or extra_depth < 0 or min(clearance) < 0 or relief < 0:
        raise LangError("tenons: margin, remaining, extra_depth, clearance and relief must not be negative.")
    if tool <= 0:
        raise LangError("tenons: tool must be positive.")
    one_of(dogbones, DogBones, "tenons(dogbones=)")
    return Tenons(count, None if width is None else float(width), float(margin), even, spacing.at, float(remaining),
                  (float(clearance[0]), float(clearance[1])), float(extra_depth), float(tool), float(relief),
                  dogbones)
