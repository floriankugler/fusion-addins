"""Contacts: a board meeting another edge-on, one of its narrow faces lying
on the other's big face, as a carcass bottom meets the sides between them.

The contact is the rectangle the two share in the plane of the big face:
along the line where they meet (`axis`), the stretch where the edge-on
board's end has material and the other board's outline covers it; across
it, the edge-on board's thickness, again as far as the other board covers
it. That is exact for the outlines (through cuts included); pockets are not
taken into account. An end interrupted by a notch meets the other board in
several places, one contact each.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from shapely.geometry import box as shapely_box

from .directions import AXES, Axis

if TYPE_CHECKING:
    from .part import Board, Face

Span = tuple[float, float]


@dataclass(frozen=True)
class Contact:
    """Where `edge_on` meets `face_on`: its narrow face `end` lies on the
    big face `face` of the other board, from `lo` to `hi` along `axis` and
    from `across_lo` to `across_hi` along the edge-on board's thickness."""
    edge_on: Board
    face_on: Board
    end: Face
    face: Face
    axis: Axis
    lo: float
    hi: float
    across_lo: float
    across_hi: float

    @property
    def across(self) -> Axis:
        """The edge-on board's thickness axis, the other axis of the contact."""
        return self.edge_on.t_axis

    @property
    def length(self) -> float:
        return self.hi - self.lo

    @property
    def plane(self) -> float:
        """The contact plane's coordinate on the face-on board's thickness axis."""
        return self.face.value

    def __repr__(self) -> str:
        return (f"Contact({self.edge_on.path}.{self.end.name} on {self.face_on.path}.{self.face.name}, "
                f"{self.axis} {self.lo:g} to {self.hi:g})")


def contacts(edge_on: Board, face_on: Board, tolerance: float = 1e-6) -> list[Contact]:
    """Where `edge_on` meets `face_on` with a narrow face on one of the
    other's big faces; empty when it does not."""
    normal = face_on.t_axis
    if edge_on.t_axis == normal:
        return []
    eb, fb = edge_on.box(), face_on.box()
    if abs(eb.hi[normal] - fb.lo[normal]) <= tolerance:
        plane, sign = fb.lo[normal], 1          # the edge-on board's end points toward +normal
    elif abs(eb.lo[normal] - fb.hi[normal]) <= tolerance:
        plane, sign = fb.hi[normal], -1
    else:
        return []
    across = edge_on.t_axis
    axis: Axis = next(a for a in AXES if a not in (normal, across))
    end = edge_on.face(edge_on.scope.frame.direction_of(normal, sign))
    face = face_on.face(face_on.scope.frame.direction_of(normal, -sign))
    found: list[Contact] = []
    for lo, hi in _end_spans(edge_on, normal, plane, axis, tolerance):
        # The face-on board's outline lies in the plane of `axis` and `across`.
        corners = {axis: (lo, hi), across: (eb.lo[across], eb.hi[across])}
        u, v = face_on.u_axis, face_on.v_axis
        window = shapely_box(corners[u][0], corners[v][0], corners[u][1], corners[v][1])
        covered = face_on.outline.geometry.intersection(window)
        for piece in getattr(covered, "geoms", [covered]):
            if piece.is_empty or piece.area <= tolerance:
                continue
            b = piece.bounds
            bounds = {u: (float(b[0]), float(b[2])), v: (float(b[1]), float(b[3]))}
            found.append(Contact(edge_on, face_on, end, face, axis, bounds[axis][0], bounds[axis][1],
                                 bounds[across][0], bounds[across][1]))
    found.sort(key=lambda c: c.lo)
    return found


def _end_spans(part: Board, normal: Axis, plane: float, axis: Axis, tolerance: float) -> list[Span]:
    """The stretches along `axis` where the part's outline runs in the line
    `normal = plane`: where its end face is."""
    i_normal = 0 if part.u_axis == normal else 1
    i_axis = 1 - i_normal
    spans: list[Span] = []
    for ring in part.outline.rings():
        for p, q in zip(ring, ring[1:] + ring[:1]):
            if (abs(p[i_normal] - plane) <= tolerance and abs(q[i_normal] - plane) <= tolerance
                    and abs(p[i_axis] - q[i_axis]) > tolerance):
                a, b = sorted((p[i_axis], q[i_axis]))
                spans.append((a, b))
    spans.sort()
    merged: list[Span] = []
    for a, b in spans:
        if merged and a <= merged[-1][1] + tolerance:
            merged[-1] = (merged[-1][0], max(merged[-1][1], b))
        else:
            merged.append((a, b))
    return merged
