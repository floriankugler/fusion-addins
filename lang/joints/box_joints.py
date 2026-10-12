"""Box joints: two boards meeting at a flush right-angled corner, as the
corners of a drawer box, joined with interlocking fingers as the box_joint
add-in makes them (see `lang.core.contact`).

`front.join(left, right, using=box_joint(7, margin=2, clearance=(0.1, 0.1)))`:
the board that meets the other edge-on (the front, its ends on the sides'
inner faces) grows fingers out of its end through the other board, flush
with its outer face; the other board, whose end must lie in the plane of
this board's outer face, gets the notches the fingers sit in. Either board
may make the call. `fingers` is the number of fingers along the joint, the
other board's and this one's together, odd so that both outer ones belong
to the notched board; all are as wide as the notches, (length - 2 *
margin) / fingers, and a plain `margin` at both ends of the joint widens
the outer two. `clearance=(along, across)`: every notch and gap is
`along` wider (half of it per side), and their bottoms lie `across`
deeper than the other board is thick, so the fingers' tips sit flush and
the gap is at their roots.

A cutter of `tool` diameter leaves its radius in every inside corner. The
joint keeps those fillets and hides everything else, as the add-in does
(after BoxJoint by EvilHacker), so that nothing shows on the assembled
joint, outside or inside:

- the notches and the gaps between the fingers keep the fillets at their
  bottom corners, through the board (`notch_<other>_1`..., `gap_<other>_1`
  ..., through cuts);
- every finger is rounded over along its mating corners with the tool's
  radius, so that it nests in the fillets of the board it enters: the
  fingers that grow from the end by grooves cut from their tips
  (`finger_<other>_grooves`), the notched board's by grooves cut from its
  end along the notch walls (`notch_<other>_grooves`), which also open the
  notch's fillet square in a band one radius deep at the inner face,
  where the root of the finger in it is not rounded;
- shallow dog bones, one radius deep, in both inner faces: centred on the
  notch walls against the notch bottoms (`notch_<other>_reliefs`) and on
  the fingers' sides against the gaps' bottoms (`finger_<other>_reliefs`),
  both pockets.

`tool=0` makes a plain square joint without any of them. The fingers are
part of the outline (`Board.add_to_outline`), the board's box stays where
it was placed. The grooves are pockets in narrow faces (`add_edge_pocket`),
the fingers' starting at their tips, in front of the board's end: the one
machining of this repo's joints that is not made from a big face. They
stay cuts from the end planes, as in the add-in: Florian mills them with
the board lying flat, the roundovers step by step with a flat cutter
(2026-10-12).

Defaults are the add-in's dialog's (kept by Florian, 2026-10-12): 5
fingers, no margin, a 6 mm tool, no clearance. With a margin smaller than half the clearance along the joint
the outer gaps reach past the board's ends (the add-in's sketch fails
there); here they are cut there all the same.
"""
from __future__ import annotations

import math
from collections.abc import Callable
from dataclasses import dataclass
from typing import ClassVar

from shapely.geometry import Polygon
from shapely.geometry import box as shapely_box

from ..core.contact import Contact
from ..core.directions import Axis
from ..core.errors import LangError
from ..core.part import Face
from ..core.shapes import Shape, circle
from .common import EPS, ContactJoint, Naming, Point2, face_toward, union_all

#: How far notches and gaps reach past the end they open toward, so they open cleanly, mm.
_PAST = 1.0
#: Sides per quarter circle of a fillet, groove or relief; the emitter draws them as arcs.
_QUARTER = 16
#: The largest angle one side of such a polygon spans, degrees.
_STEP = 90.0 / _QUARTER
#: Far enough to stand for "beyond the board", mm.
_FAR = 1e9


@dataclass(frozen=True)
class BoxJoint(ContactJoint):
    fingers: int
    margin: float
    tool: float
    #: (along the joint, across it)
    clearance: tuple[float, float]
    label: ClassVar[str] = "box_joint"

    @property
    def radius(self) -> float:
        return self.tool / 2

    def stations(self, c: Contact) -> list[float]:
        """The ends of the fingers along the contact, from its start: the
        margin, then a finger's width each. Each is measured from the
        nearer end of the contact, so the joint is symmetric to the last
        bit and its ends land on the contact's."""
        n, m = self.fingers, self.margin
        if 2 * m >= c.length - EPS:
            raise LangError(f"margin={m:g} leaves no room for the fingers on the {c.length:g} mm joint.")
        w = (c.length - 2 * m) / n
        return [c.lo + m + k * w if 2 * k <= n else c.hi - m - (n - k) * w for k in range(n + 1)]

    def check(self, c: Contact, stations: list[float]) -> None:
        corner = _Corner(c)
        a, b = corner.a, corner.b
        w = (c.length - 2 * self.margin) / self.fingers
        along, r = self.clearance[0], self.radius
        if r > 0:
            if w - along < 2 * r + EPS:
                raise LangError(f"{self.fingers} fingers on the {c.length:g} mm joint are {w:g} mm wide, too narrow "
                                f"for the corner reliefs: each must be wider than the tool ({self.tool:g}) plus the "
                                f"clearance along the joint ({along:g}). Use fewer fingers or a smaller tool.")
            for part in (a, b):
                if part.thickness <= r + EPS:
                    raise LangError(f"{part.path} is {part.thickness:g} thick, not thicker than the tool's radius "
                                    f"({r:g}): the grooves along its fingers would take all of it.")
        elif w - along <= EPS:
            raise LangError(f"the clearance along the joint ({along:g}) leaves nothing of the {w:g} mm fingers.")

    def place(self, c: Contact, stations: list[float], naming: Naming) -> None:
        corner = _Corner(c)
        a, b = corner.a, corner.b
        n, r = self.fingers, self.radius
        half, across = self.clearance[0] / 2, self.clearance[1]
        seat = corner.ta + across               # the gaps' bottoms, through the notched board
        bottom = corner.tb + across             # the notches' bottoms, across the finger board
        notches = [(stations[k] - half, stations[k + 1] + half) for k in range(1, n, 2)]
        gaps = [(stations[k] - half, stations[k + 1] + half) for k in range(0, n, 2)]
        sides = [z for k in range(1, n, 2) for z in (stations[k] + half, stations[k + 1] - half)]

        # The finger board: stock from one radius before the first notch
        # wall to one past the last, then the gaps out of it. The outer
        # gaps leave the outer fingers' root fillets whole, and only
        # recess the seat in the board as it was.
        lo, hi = notches[0][0] - r, notches[-1][1] + r
        b.add_to_outline(corner.on_b([(0.0, lo), (corner.ta, lo), (corner.ta, hi), (0.0, hi)]))
        for i, (z0, z1) in enumerate(gaps, 1):
            # With a clearance across, the board's end runs through an
            # outer gap's outer fillet: a vertex there keeps the piece the
            # cut leaves an arc.
            cut = corner.ta if across > EPS else None
            shape = _slot(seat, z0, z1, r, cut if i == 1 else None, cut if i == len(gaps) else None)
            b.add_cut(corner.on_b(shape), name=naming(b, f"gap_{a.name}_{i}"))
        if r > 0:
            grooves = union_all([corner.on_tips(_lens(corner.tb, z, r)) for z in sides])
            b.add_edge_pocket(c.end, grooves, seat - r, name=naming(b, f"finger_{a.name}_grooves"),
                              offset=corner.tips_offset)
            reliefs = union_all([circle(2 * r, corner.point_b(seat - r, z), _QUARTER) for z in sides])
            b.add_pocket(corner.b_inner, reliefs, r, name=naming(b, f"finger_{a.name}_reliefs"))

        # The notched board: the notches, the grooves along their walls
        # (open toward the notch) and the dog bones on those walls.
        for i, (z0, z1) in enumerate(notches, 1):
            a.add_cut(corner.on_a(_slot(bottom, z0, z1, r)), name=naming(a, f"notch_{b.name}_{i}"))
        if r > 0:
            grooves = union_all([corner.on_a_end(_lens(corner.ta, z, r, opens)) for z0, z1 in notches
                              for z, opens in ((z0, 1), (z1, -1))])
            a.add_edge_pocket(corner.a_end, grooves, bottom, name=naming(a, f"notch_{b.name}_grooves"),
                              offset=corner.a_end_offset)
            reliefs = union_all([circle(2 * r, corner.point_a(bottom - r, z), _QUARTER) for z0, z1 in notches
                              for z in (z0, z1)])
            a.add_pocket(c.face, reliefs, r, name=naming(a, f"notch_{b.name}_reliefs"))


class _Corner:
    """A joint's corner in the add-in's frame: x across the finger board
    (b, the one whose end meets the other's face) from its outer face, y
    through the notched board (a) from its outer face, and z along the
    joint, in world coordinates. Checks that the corner is one: a's end
    flush with b's outer face, a covering b's end, which runs across b's
    whole width, and nothing of b in the corner yet."""

    def __init__(self, c: Contact):
        self.c = c
        a, b = c.face_on, c.edge_on
        self.a, self.b = a, b
        self.ta, self.tb = a.thickness, b.thickness
        self.x_axis: Axis = c.across
        self.y_axis: Axis = a.t_axis
        self.z_axis: Axis = c.axis
        #: From a's outer face toward b, along y.
        self.ys = c.face.direction.sign
        bb = b.box()
        x, z = self.x_axis, self.z_axis
        if c.lo > bb.lo[z] + EPS or c.hi < bb.hi[z] - EPS:
            raise LangError(f"the end of {b.path} meets {a.path} from {z}={c.lo:g} to {c.hi:g}, not across its whole "
                            f"width ({bb.lo[z]:g} to {bb.hi[z]:g}): the joint runs along the whole end, which "
                            f"{a.path} must cover. Cut-outs at the joint go after the join.")
        overlap = self._a_region((bb.lo[x], bb.hi[x]))
        if a.outline.geometry.intersection(overlap).area < overlap.area - EPS:
            raise LangError(f"{a.path} does not cover the end of {b.path} at the corner; its end must lie in the "
                            f"plane of {b.path}'s outer face.")
        flush = [side for side in (-1, 1)
                 if a.outline.geometry.intersection(self._a_region(
                     (bb.hi[x], _FAR) if side > 0 else (-_FAR, bb.lo[x]))).area <= EPS]
        if len(flush) != 1:
            raise LangError(f"the corner is not flush: the end of {a.path} must lie in the plane of one of "
                            f"{b.path}'s big faces, its outer face, "
                            f"{'not reach past both' if not flush else 'not end at both'}.")
        #: Which of b's big faces is the outer one, flush with a's end.
        side = flush[0]
        self.x0 = bb.hi[x] if side > 0 else bb.lo[x]
        self.xs = -side
        self.b_inner: Face = face_toward(b, -side, x)
        self.a_end: Face = face_toward(a, side, x)
        self.a_end_offset = _offset(self.a_end, self.x0)
        self.tips_offset = _offset(c.end, self.y(0.0))
        u, v = b.u_axis, b.v_axis
        tips = self.y(0.0)
        corner = {self.y_axis: (min(tips, c.plane), max(tips, c.plane)), z: (c.lo, c.hi)}
        if b.outline.geometry.intersection(shapely_box(corner[u][0], corner[v][0], corner[u][1],
                                                       corner[v][1])).area > EPS:
            raise LangError(f"{b.path} already reaches into {a.path} at the corner.")

    def _a_region(self, xs: tuple[float, float]) -> Polygon:
        """The rectangle of a's outline frame from xs[0] to xs[1] across b
        and along the whole joint."""
        a = self.a
        lo = {self.x_axis: xs[0], self.z_axis: self.c.lo}
        hi = {self.x_axis: xs[1], self.z_axis: self.c.hi}
        return shapely_box(lo[a.u_axis], lo[a.v_axis], hi[a.u_axis], hi[a.v_axis])

    def x(self, value: float) -> float:
        return self.x0 + self.xs * value

    def y(self, value: float) -> float:
        """Measured from a's inner face, so that y = ta is that face exactly."""
        return self.c.plane + self.ys * (value - self.ta)

    def _shape(self, points: list[Point2], axis: Axis, convert: Callable[[float], float],
               target: tuple[Axis, Axis]) -> Shape:
        """A polygon of (p, z) points, p along `axis` in the joint's frame,
        in the frame of `target`'s two world axes."""
        ring: list[Point2] = []
        for p, z in points:
            coords = {axis: convert(p), self.z_axis: z}
            ring.append((coords[target[0]], coords[target[1]]))
        return Shape(Polygon(ring))

    def on_a(self, points: list[Point2]) -> Shape:
        """(x, z) points in a's outline frame."""
        return self._shape(points, self.x_axis, self.x, (self.a.u_axis, self.a.v_axis))

    def on_b(self, points: list[Point2]) -> Shape:
        """(y, z) points in b's outline frame."""
        return self._shape(points, self.y_axis, self.y, (self.b.u_axis, self.b.v_axis))

    def on_a_end(self, points: list[Point2]) -> Shape:
        """(y, z) points on a's end face, in its (s, t) frame."""
        return self._shape(points, self.y_axis, self.y, self.a.face_axes(self.a_end))

    def on_tips(self, points: list[Point2]) -> Shape:
        """(x, z) points on b's end face, in its (s, t) frame."""
        return self._shape(points, self.x_axis, self.x, self.b.face_axes(self.c.end))

    def point_a(self, x: float, z: float) -> Point2:
        """A point on a's big faces."""
        coords = {self.x_axis: self.x(x), self.z_axis: z}
        return (coords[self.a.u_axis], coords[self.a.v_axis])

    def point_b(self, y: float, z: float) -> Point2:
        """A point on b's big faces."""
        coords = {self.y_axis: self.y(y), self.z_axis: z}
        return (coords[self.b.u_axis], coords[self.b.v_axis])


def _offset(face: Face, plane: float) -> float:
    """How far the plane `plane` lies in front of `face`."""
    return (plane - face.value) * face.direction.sign


def _arc(center: Point2, r: float, start: float, end: float, cut: float | None = None) -> list[Point2]:
    """The points inside the arc of the circle about `center` from the
    angle `start` to `end` (degrees, p = cos, q = sin), its ends left out,
    one at least every `_STEP` degrees. With `cut`, also one exactly on the
    line p = cut where the arc crosses it, and at least four sides either
    side of it, so that the piece a boolean leaves is still an arc."""
    cp, cq = center
    stops = [start, end]
    vertex: Point2 | None = None
    if cut is not None and abs(cut - cp) < r:
        crossing = math.degrees(math.acos((cut - cp) / r))
        for angle in (crossing, -crossing):
            if min(start, end) < angle < max(start, end):
                stops = [start, angle, end]
                vertex = (cut, cq + r * math.sin(math.radians(angle)))
    angles: list[float] = []
    for a0, a1 in zip(stops, stops[1:]):
        n = max(4, math.ceil(abs(a1 - a0) / _STEP - 1e-9))
        angles += [a0 + (a1 - a0) * i / n for i in range(n)]
    points: list[Point2] = []
    for angle in angles[1:]:
        if vertex is not None and angle == stops[1]:
            points.append(vertex)
        else:
            points.append((cp + r * math.cos(math.radians(angle)), cq + r * math.sin(math.radians(angle))))
    return points


def _slot(depth: float, lo: float, hi: float, r: float, cut_lo: float | None = None,
          cut_hi: float | None = None) -> list[Point2]:
    """A notch or gap as (p, q) points: open toward negative p from `_PAST`
    outside the board, `depth` deep, from q = lo to hi, its bottom corners
    keeping the fillets a cutter of radius r leaves. `cut_lo` and `cut_hi`
    give the fillet at lo or hi a vertex on the line p = cut."""
    if r <= 0:
        return [(-_PAST, lo), (depth, lo), (depth, hi), (-_PAST, hi)]
    return ([(-_PAST, lo), (depth - r, lo)] + _arc((depth - r, lo + r), r, -90, 0, cut_lo)
            + [(depth, lo + r), (depth, hi - r)] + _arc((depth - r, hi - r), r, 0, 90, cut_hi)
            + [(depth - r, hi), (-_PAST, hi)])


def _lens(surface: float, q: float, r: float, opens: int = 0) -> list[Point2]:
    """As (p, q) points, what a cutter of radius r leaves in the two
    right-angled corners either side of q under the surface p = `surface`:
    two quarter arcs meeting r below it at q, closed along the surface.
    `opens` +1 or -1 makes the half on that side a full r by r square."""
    upper = [(surface - r, q + r)] if opens > 0 else _arc((surface - r, q + r), r, 0, -90)
    lower = [(surface - r, q - r)] if opens < 0 else _arc((surface - r, q - r), r, 90, 0)
    return [(surface, q - r), (surface, q + r)] + upper + [(surface - r, q)] + lower


def box_joint(fingers: int = 5, *, margin: float = 0.0, tool: float = 6.0,
              clearance: tuple[float, float] = (0.0, 0.0)) -> BoxJoint:
    """A box joint with `fingers` fingers along the joint (odd, at least
    3), a plain `margin` at both ends, reliefs for a `tool` mm cutter (0
    for a square joint) and `clearance` (along the joint, across it)."""
    if fingers < 3:
        raise LangError(f"box_joint: at least 3 fingers, got {fingers}.")
    if fingers % 2 == 0:
        raise LangError(f"box_joint: the number of fingers must be odd, so that both outer ones belong to the "
                        f"notched board; got {fingers}.")
    if margin < 0 or tool < 0 or min(clearance) < 0:
        raise LangError("box_joint: margin, tool and clearance must not be negative.")
    return BoxJoint(fingers, float(margin), float(tool), (float(clearance[0]), float(clearance[1])))
