"""The parts of a layout as the nest takes them: per material, each part's
machine outline seen from its machining face, the turns it may take, and
how it maps back into the world.

A part lies on its blank with its machining face up (`machine` in the
layout), so the nest sees its outline from that face: its (u, v) outline as
it is where u x v points out of that face, else mirrored (u negated). The
outline is the layout's, less the through pockets and through holes; an
opening stays open for other parts where it could take the smallest of
them (its inside, the spacing in from its edge, at least that part's area)
and is filled where it could not, which spares the solver its vertices.

The solver gets a polygon that contains the true outline: grown by 1.5
times `TOLERANCE` (mitred up to `MITRE` times that, so square corners stay
square and a sharp one is cut off) and simplified by `TOLERANCE`: at most
`OUTSIDE` (0.81 mm) outside it, 0.53 mm off a square corner (the
experiments: true arcs nested no better than polygons simplified to
0.25 mm). Openings go in as
polygons, never as circles (PackingSolver puts nothing into a circular
hole). Everything is moved so that the solver's polygon starts at (0, 0).

A part that asks for a larger spacing than the nest's least (its own
`nesting.spacing`) has its solver polygon grown by the difference, so that
between two parts the larger of their spacings holds.

Turns [Florian, 2026-10-14]: a part with grain keeps it along the sheet's
length (x): turned by 0 or 180 degrees when its grain runs along its u,
by 90 or 270 along its v. A part of a material without grain, or one whose
grain the build left unset, turns by any 90 degree step. No part is ever
mirrored: its machining face stays up.

A `nest(False)` board a nest names is its own blank [decided 2026-10-16]:
sawn to size out of the stock, with no margin, its outline whole (cut by
hand), and it may be larger than the bed (`Item.own`).
"""
from __future__ import annotations

import math
from collections.abc import Collection, Mapping
from dataclasses import dataclass, field

from shapely import Point, Polygon, affinity, box, union_all
from shapely.geometry.base import BaseGeometry
from shapely.geometry.polygon import orient

from ..core.errors import LangError
from ..core.geometry import parts_of
from ..core.layout_types import Layout, PartLayout, Rings
from .fingerprint import fingerprint as part_fingerprint
from .workshop import Workshop, fits

#: How far (mm) the solver's polygon may be simplified (see the module's doc).
TOLERANCE = 0.25
#: The longest mitre when the outline is grown, in times the growth: a
#: square corner (1.41) stays square [found by fuzzing, 2026-10-14: with
#: 10, a hole tangent to an edge left a needle of material whose mitre
#: reached 3.75 mm out].
MITRE = 1.5
#: How far (mm) the solver's polygon may lie outside the part.
OUTSIDE = 1.5 * TOLERANCE * MITRE + TOLERANCE
AXES = ("x", "y", "z")
#: Cyclic orders of the world axes: (u, v, t) in one of these is right-handed.
_RIGHT_HANDED = {("x", "y", "z"), ("y", "z", "x"), ("z", "x", "y")}


@dataclass(frozen=True)
class PartFrame:
    """How a part's world coordinates map to its nest frame: x, y in the
    plane seen from the machining face (from the solver polygon's corner),
    z up from the face the part lies on, the machining face at z = t."""
    t: str
    u: str
    v: str
    #: Whether u is negated (the outline seen from the machining face is mirrored).
    mirror: bool
    #: +1 when the machining face is the part's +t face, else -1.
    up: int
    #: The part's extent along t (world mm).
    t_lo: float
    t_hi: float
    #: What is taken off the (possibly mirrored) u and v so the solver's polygon starts at 0.
    x0: float
    y0: float

    def matrix(self) -> list[list[float]]:
        """World mm to the nest frame, a 3 x 4 matrix (rows x, y, z)."""
        def row(axis: str, scale: float, offset: float) -> list[float]:
            r = [0.0, 0.0, 0.0, offset]
            r[AXES.index(axis)] = scale
            return r
        x = row(self.u, -1.0 if self.mirror else 1.0, -self.x0)
        y = row(self.v, 1.0, -self.y0)
        z = row(self.t, float(self.up), -self.t_lo if self.up > 0 else self.t_hi)
        return [x, y, z]

    def placed(self, turn: float, at: tuple[float, float]) -> list[list[float]]:
        """World mm to a blank's frame for the part turned by `turn` degrees
        (counter-clockwise, about the nest frame's origin) and moved to `at`."""
        c, s = _cos_sin(turn)
        x, y, z = self.matrix()
        rx = [c * a - s * b for a, b in zip(x, y)]
        ry = [s * a + c * b for a, b in zip(x, y)]
        rx[3] += at[0]
        ry[3] += at[1]
        return [rx, ry, z]


@dataclass
class Item:
    """A part to nest."""
    path: str
    material: str
    thickness: float
    #: The machine outline in the nest frame, with every opening.
    shape: Polygon
    #: What the solver gets: a polygon containing `shape`, with the openings that may take parts.
    solver: Polygon
    #: The turns it may take, degrees.
    turns: tuple[float, ...]
    #: Whether its grain must run along the sheet's length.
    grained: bool
    frame: PartFrame
    #: The machining face (world name), which faces up.
    up: str
    #: The least gap to another part (mm): between two parts the larger of
    #: theirs holds.
    spacing: float = 10.0
    #: A `nest(False)` board named in the nest: its own blank, sawn to size,
    #: its solver polygon its bounding rectangle.
    own: bool = False
    #: Its hash as machined (`fingerprint`), "" where not taken.
    fingerprint: str = ""
    area: float = field(init=False)

    def __post_init__(self) -> None:
        self.area = float(self.shape.area)

    def placed(self, turn: float, at: tuple[float, float], solver: bool = False) -> Polygon:
        """Its outline (or the solver's polygon) turned and moved as on a blank."""
        return turned(self.solver if solver else self.shape, turn, at)

    def size(self, turn: float) -> tuple[float, float]:
        """The solver polygon's extent turned by `turn`: (along x, along y)."""
        x0, y0, x1, y1 = turned(self.solver, turn).bounds
        return x1 - x0, y1 - y0


def turned(shape: Polygon, turn: float, at: tuple[float, float] = (0.0, 0.0)) -> Polygon:
    """`shape` turned by `turn` degrees counter-clockwise about the origin,
    then moved by `at`; a quarter turn exactly."""
    c, s = _cos_sin(turn)
    out = affinity.affine_transform(shape, [c, -s, s, c, at[0], at[1]])
    assert isinstance(out, Polygon)
    return out


@dataclass(frozen=True)
class LeftOut:
    path: str
    material: str
    why: str


@dataclass
class Parts:
    """A layout's parts by material, and those left out of the nest."""
    by_material: dict[str, list[Item]]
    left_out: list[LeftOut]


def parts_of_layout(layout: Layout, spacing: float, material: str | None = None, *,
                    paths: Collection[str] | None = None, spacing_of: Mapping[str, float] | None = None) -> Parts:
    """The layout's parts to nest, by material: all, or those of the
    material named, or the `paths` of a nest, whose `nest(False)` boards
    are their own blanks; and, of all, those left out (`nest(False)`,
    manual, slats). `spacing` is the nest's least, `spacing_of` a part's own
    where it asks for more."""
    frame = {name: (value[1], 1 if value[0] == "+" else -1) for name, value in layout["frame"].items()}
    wanted = None if paths is None else set(paths)
    raw: dict[str, list[tuple[PartLayout, Polygon, PartFrame]]] = {}
    own: dict[str, list[Item]] = {}
    left_out: list[LeftOut] = []
    for module in layout["modules"]:
        for part in module["parts"]:
            if (wanted is not None and part["path"] not in wanted) or \
                    (material is not None and part["material"] != material):
                continue
            if not part["nest"]:
                why = "slat" if part["kind"] == "slat" else "manual" if part["manual"] else "nest(False)"
                if wanted is None:
                    left_out.append(LeftOut(part["path"], part["material"], why))
                elif why != "nest(False)":
                    raise LangError(f"{part['path']} is a {why} part, which is never nested.")
                else:
                    item = _own_item(part, frame)
                    item.fingerprint = part_fingerprint(part, layout["frame"])
                    own.setdefault(part["material"], []).append(item)
                continue
            shape, pf = _machine_outline(part, frame)
            raw.setdefault(part["material"], []).append((part, shape, pf))
    by_material: dict[str, list[Item]] = {}
    for name in sorted(set(raw) | set(own)):
        entries = raw.get(name, [])
        smallest = min((shape.area for _p, shape, _f in entries), default=0.0)
        by_material[name] = [_item(part, shape, pf, max(spacing, (spacing_of or {}).get(part["path"], spacing)),
                                   spacing, smallest, part_fingerprint(part, layout["frame"]))
                             for part, shape, pf in entries] + own.get(name, [])
    return Parts(by_material, left_out)


def check_sizes(parts: Parts, workshop: Workshop) -> None:
    """Refuses parts that no blank takes: larger than the bed with its
    margins, or than every piece of stock for their material (a sheet to
    buy, the pieces on hand); an own blank, larger than every piece of
    stock. The message names each and how to leave it out."""
    assert workshop.bed is not None
    bed = workshop.bed
    problems: list[str] = []
    for name, items in parts.by_material.items():
        sheet = workshop.sheet_for(name)
        stock = ([(sheet.length, sheet.width)] if sheet is not None else []) + \
                [(o.length, o.width) for o in workshop.on_hand_for(name)]
        if not stock:
            raise LangError(f"No stock for {name}: no sheet size to buy (sheet_material(..., size=(2500, 1250))) "
                            "and none on hand in the inventory (inventory.toml).")
        for item in items:
            x0, y0, x1, y1 = item.shape.bounds
            size = f"{item.path} ({x1 - x0:.0f} x {y1 - y0:.0f})"
            grain = " with its grain along the stock's" if item.grained else ""
            if item.own:
                if not any(bw <= sl + 1e-6 and bh <= sw + 1e-6 for bw, bh in map(item.size, item.turns)
                           for sl, sw in stock):
                    problems.append(f"{size}, its own blank, fits no stock for {name}{grain}")
                continue
            blanks = [(w + 2 * workshop.margin, h + 2 * workshop.margin) for w, h in map(item.size, item.turns)]
            if not any(fits(bw, bh, bed) for bw, bh in blanks):
                problems.append(f"{size} does not fit the bed {bed[0]:g} x {bed[1]:g} with its margins; "
                                "nest(False) saws it by hand")
            elif not any(bw <= sl + 1e-6 and bh <= sw + 1e-6 for bw, bh in blanks if fits(bw, bh, bed)
                         for sl, sw in stock):
                problems.append(f"{size} fits no stock for {name}{grain}")
    if problems:
        raise LangError("These parts cannot be nested:\n  " + "\n  ".join(problems))


# -- one part ------------------------------------------------------------------------------

def _machine_outline(part: PartLayout, frame: dict[str, tuple[str, int]],
                     openings: bool = True) -> tuple[Polygon, PartFrame]:
    """The part's outline seen from its machining face, less its through
    pockets and holes unless `openings` is False, and its frame."""
    axes = part["axes"]
    t, u, v = axes["t"], axes["u"], axes["v"]
    machine_axis, up = frame[part["machine"]]
    if machine_axis != t:
        raise LangError(f"{part['path']}: its machining face {part['machine']} is not a big face.")
    handed = 1 if (u, v, t) in _RIGHT_HANDED else -1
    mirror = handed * up < 0
    outline = _polygons(part["outline"])
    through: list[BaseGeometry] = []
    for op in part["ops"] if openings else []:
        if op["kind"] == "pocket" and frame[op["face"]][0] == t and op["depth"] >= part["thickness"] - 1e-6:
            through += _polygons(op["shape"])
        elif op["kind"] == "hole" and op["through"] and frame[op["face"]][0] == t:
            through.append(Point(op["u"], op["v"]).buffer(op["d"] / 2, quad_segs=16))
    shape = union_all(outline)
    if through:
        shape = shape.difference(union_all(through))
    pieces = [p for p in parts_of(shape) if p.area > 1e-6]
    if len(pieces) != 1:
        raise LangError(f"{part['path']}: its machine outline is in {len(pieces)} pieces; the nest takes a part "
                        "in one.")
    shape = pieces[0]
    if mirror:
        shape = affinity.scale(shape, -1.0, 1.0, origin=(0, 0))
    assert isinstance(shape, Polygon)
    shape = orient(shape)
    lo, hi = part["box"]["min"][AXES.index(t)], part["box"]["max"][AXES.index(t)]
    pf = PartFrame(t, u, v, mirror, up, lo, hi, 0.0, 0.0)
    return shape, pf


def _item(part: PartLayout, shape: Polygon, pf: PartFrame, spacing: float, least: float, smallest: float,
          fingerprint: str = "") -> Item:
    """The part as the nest takes it; `spacing` its own, `least` the
    nest's, the solver's spacing: the solver's polygon is grown by the
    difference besides its own growth."""
    # Openings that cannot take the smallest part are filled.
    kept = [ring for ring in shape.interiors if _takes_a_part(ring, spacing, smallest)]
    solid = Polygon(shape.exterior, kept)
    extra = spacing - least
    grown = solid.buffer(1.5 * TOLERANCE + extra, join_style="mitre", mitre_limit=MITRE)
    simple = grown.simplify(TOLERANCE, preserve_topology=True)
    if not isinstance(simple, Polygon) or simple.is_empty:
        raise LangError(f"{part['path']}: its outline could not be simplified for the nest.")
    # Growing can close a notch's narrow mouth into a hole: the same rule
    # for the solver's holes [found by fuzzing, 2026-10-14].
    simple = orient(Polygon(simple.exterior, [r for r in simple.interiors if _takes_a_part(r, least, smallest)]))
    if not simple.buffer(1e-6).contains(solid):
        raise LangError(f"{part['path']}: the nest's outline would cut into the part.")
    x0, y0, _x1, _y1 = simple.bounds
    simple = affinity.translate(simple, -x0, -y0)
    shape = affinity.translate(shape, -x0, -y0)
    pf = PartFrame(pf.t, pf.u, pf.v, pf.mirror, pf.up, pf.t_lo, pf.t_hi, x0, y0)
    grained, turns = _turns(part, pf)
    return Item(part["path"], part["material"], part["thickness"], shape, simple, turns, grained, pf,
                part["machine"], spacing, fingerprint=fingerprint)


def _own_item(part: PartLayout, frame: dict[str, tuple[str, int]]) -> Item:
    """A `nest(False)` board named in a nest: its whole outline from its
    machining face, its blank the rectangle around it."""
    shape, pf = _machine_outline(part, frame, openings=False)
    x0, y0, x1, y1 = shape.bounds
    shape = affinity.translate(shape, -x0, -y0)
    pf = PartFrame(pf.t, pf.u, pf.v, pf.mirror, pf.up, pf.t_lo, pf.t_hi, x0, y0)
    grained, turns = _turns(part, pf)
    return Item(part["path"], part["material"], part["thickness"], shape, box(0.0, 0.0, x1 - x0, y1 - y0), turns,
                grained, pf, part["machine"], 0.0, own=True)


def _turns(part: PartLayout, pf: PartFrame) -> tuple[bool, tuple[float, ...]]:
    """Whether the part's grain is set, and the turns it may take."""
    grained = part["grained"] and part["grain"] is not None
    if not grained:
        return False, (0.0, 90.0, 180.0, 270.0)
    if part["grain"] == pf.u:
        return True, (0.0, 180.0)
    if part["grain"] == pf.v:
        return True, (90.0, 270.0)
    raise LangError(f"{part['path']}: its grain {part['grain']} is not in its plane.")


def _takes_a_part(ring: object, spacing: float, smallest: float) -> bool:
    """Whether an opening could take the smallest part: its inside, the
    spacing in from its edge, has at least that part's area."""
    return Polygon(ring).buffer(-spacing, join_style="mitre").area >= smallest - 1e-6  # pyright: ignore[reportArgumentType]


def _polygons(rings: Rings) -> list[Polygon]:
    """Rings as the layout writes them: an exterior (counter-clockwise),
    then its holes (clockwise), then the next polygon."""
    out: list[Polygon] = []
    shell: list[list[float]] | None = None
    holes: list[list[list[float]]] = []
    for ring in rings:
        if _ring_area(ring) > 0:
            if shell is not None:
                out.append(Polygon(shell, holes))
            shell, holes = ring, []
        else:
            holes.append(ring)
    if shell is not None:
        out.append(Polygon(shell, holes))
    return out


def _ring_area(ring: list[list[float]]) -> float:
    a = 0.0
    for (x0, y0), (x1, y1) in zip(ring, ring[1:] + ring[:1]):
        a += x0 * y1 - x1 * y0
    return a / 2


def _cos_sin(turn: float) -> tuple[float, float]:
    """cos and sin of a turn in degrees, exact for the quarter turns."""
    quarter = {0.0: (1.0, 0.0), 90.0: (0.0, 1.0), 180.0: (-1.0, 0.0), 270.0: (0.0, -1.0)}
    exact = quarter.get(turn % 360.0)
    if exact is not None:
        return exact
    a = math.radians(turn)
    return math.cos(a), math.sin(a)
