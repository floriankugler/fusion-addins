"""Which template machines what: Auto Setup's rules (`lib/auto_setup/rules.py`),
lifted out of Fusion and corrected where `proposals/cam.md` says Auto Setup
goes wrong. Millimetres; the constants are Auto Setup's, in mm.

**Holes** [Florian's rules, `PREFER_DRILLING` off]: a hole is bored with the
widest bore cutter at least `BORE_CLEARANCE` smaller than it, which in a
blind hole must also reach the centre (the hole at most twice the cutter:
no core left standing); where none has that room but one fits at all, that
one bores only `TIGHT_CUT_DEPTH` deep, with a note; a hole no bore cutter
fits is drilled with a drill template of exactly its diameter, as deep at
most; else nothing fits. A through hole wider than `BIG_HOLE_LIMIT` is an
inner contour, a blind one wider than twice the widest bore cutter a
round pocket (the plan's, not this module's). A cutter's flute must reach
the hole's bottom, through it by the breakthrough; one that does not is
taken only where no other fits, with a note.

**Pockets** (`pocket_cutters`): the widest template that gets in (its
widest cutter fits the region at all), the configured one first, takes the
region; where its cutters (an adaptive template's clean-up too) leave more
than corners' fillets and the dog bones by the opening test
(`regions.unreached`), what is left goes to the next narrower template that
reaches it, as a rest, else it is reported. But a narrower template that
reaches all of it takes it alone where its cutter is at least `ALONE`
times the widest's: the 6 mm cutter cuts a groove the 8 mm leaves rests
in, while a 2 mm one only takes the channel a 200 mm pocket runs into.
The dog bones go by their own rule. An adaptive template (the 8 mm cutter
is a pure rougher for larger pockets [Florian, 2026-10-17]) only for a
region of `SMALL_POCKET_AREA` or more (all lead-in and corner below it)
with room for `ADAPTIVE_ROOM` of its cutters across (the region shrunk by
its cutter's diameter is not empty): never a slot, a groove or another
narrow pocket. A flute that reaches the floor.

**Contours** (`contour_cutter`): the widest template, the configured one
or a narrower one, whose cutter reaches the whole contour on its waste
side, with no clearance (it follows a fillet of its own radius, which a
box joint keeps), and whose flute cuts through.

**Dog bones** (`dogbone_route`): one its operation's cutter is too wide for
(narrower than it by more than `RELIEF_TOL`) is plunged with a drill
template of its diameter, else milled along its wall with the widest dog
bone cutter `RELIEF_TOL` narrower than it, else nothing fits.

**The V-bit** (`v_bit`, `chamfer_fits`, `groove_passes`): the 90 degree bit
that reaches deepest; a chamfer needs its size plus the template's tip
offset of flank, a hole's rim room for the tip; a V-groove is traced in as
many passes as the template's stepdown takes, so grooves of other counts
go into operations of their own.
"""
from __future__ import annotations

import math
import os
from collections.abc import Sequence
from dataclasses import dataclass, field

from shapely.geometry import Polygon
from shapely.geometry.base import BaseGeometry
from shapely.ops import unary_union

from ..core.geometry import polygons_of
from .regions import TOOL_CLEARANCE, gets_in, unreached
from .tooling import Kind, Registry, Template

#: Whether a hole of a drill template's diameter is drilled rather than
#: bored: off [Florian, 2026-10-04: plunging burns], so drilling is the
#: last resort for holes; dog bones are still plunged.
PREFER_DRILLING = False
#: A hole or dog bone this close to a drill's diameter takes it (mm).
DRILL_MATCH_TOL = 0.05
#: How much smaller a bore cutter is than the hole, to clear its chips (mm).
BORE_CLEARANCE = 1.0
#: How deep a hole goes when its cutter has less room than that (mm).
TIGHT_CUT_DEPTH = 4.0
#: Slack in comparing a cutter with the room a hole leaves it (mm).
FIT_TOL = 1e-5
#: Through holes wider than this are inner contours (mm).
BIG_HOLE_LIMIT = 30.0
#: Slack in comparing a flute with a depth (mm).
DEPTH_TOL = 0.05
#: A dog bone this much narrower than an operation's cutter, or more,
#: needs another operation (mm): a cutter of exactly its diameter cuts it.
RELIEF_TOL = 0.05
#: The floor (mm²) an adaptive template needs to be worth it ...
SMALL_POCKET_AREA = 2500.0
#: ... and the room, in its cutter's diameters across: the 8 mm adaptive
#: rougher takes larger pockets only, nothing narrower than 16 mm
#: [Florian, 2026-10-17: a pure pocket rougher, not for narrower slots].
ADAPTIVE_ROOM = 2.0
#: A narrower pocket template that reaches all of a pocket takes it alone,
#: instead of the widest that gets in with rests, where its cutter is at
#: least this share of the widest's (the 6 mm of the 8 mm).
ALONE = 0.75
#: The decimals a bore's feed scale is rounded to: holes that agree to it
#: share an operation.
FEED_SCALE_DECIMALS = 3
#: The V-bit's flank against its axis (degrees), and the slack.
V_BIT_TAPER = 45.0
V_BIT_TAPER_TOL = 0.1

#: The order of the kinds within one tool: holes into solid material
#: first, the pockets, the contours that free the part, the dog bones the
#: contours' cutters left.
KIND_ORDER = {"drill": 0, "bore": 1, "pocket": 2, "contour": 3, "dogbone": 4}


def by_diameter(templates: Sequence[Template]) -> dict[float, Template]:
    """The hole templates by their first tool's diameter; one tagged for the
    cutter over an untagged one."""
    out: dict[float, Template] = {}
    for t in sorted(templates, key=lambda t: t.cutter_tag is None):
        out.setdefault(round(t.ops[0].tool.diameter, 6), t)
    return out


@dataclass(frozen=True)
class HoleChoice:
    template: Template
    #: Its tool's diameter.
    tool: float
    #: How deep it goes where it has too little room (`TIGHT_CUT_DEPTH`),
    #: else None: the hole's depth.
    depth_limit: float | None
    notes: tuple[str, ...] = ()


def hole_choice(d: float, depth: float, through: bool, breakthrough: float, bores: dict[float, Template],
                drills: dict[float, Template]) -> HoleChoice | None:
    """The template for a hole `d` across (see the module's doc), or None."""
    required = depth + (breakthrough if through else 0.0)
    no_core = not through

    def flute_ok(t: Template) -> bool:
        return t.flute is None or t.flute >= required - DEPTH_TOL

    def bore(clearance: float, depth_needed: bool, core: bool) -> tuple[float, Template] | None:
        fitting = [(dia, t) for dia, t in bores.items() if dia <= d - clearance + FIT_TOL
                   and not (core and 2 * dia < d - FIT_TOL) and (not depth_needed or flute_ok(t))]
        return max(fitting, key=lambda e: e[0]) if fitting else None

    if PREFER_DRILLING:
        for dia, t in drills.items():
            if abs(d - dia) < DRILL_MATCH_TOL and flute_ok(t):
                return HoleChoice(t, dia, None)
    picked = bore(BORE_CLEARANCE, True, no_core)
    if picked is not None:
        return HoleChoice(picked[1], picked[0], None)
    picked = bore(BORE_CLEARANCE, False, no_core)
    if picked is not None:
        return HoleChoice(picked[1], picked[0], None,
                          (f"a {d:g} mm hole {required:g} deep is deeper than every bore cutter's flute "
                           f"({picked[1].stem}, {picked[1].flute:g}); check the operation",))
    picked = bore(TOOL_CLEARANCE, False, False)
    if picked is not None:
        if depth <= TIGHT_CUT_DEPTH + DEPTH_TOL:
            return HoleChoice(picked[1], picked[0], None)
        return HoleChoice(picked[1], picked[0], TIGHT_CUT_DEPTH,
                          (f"a {d:g} mm hole leaves the {picked[0]:g} mm cutter less than {BORE_CLEARANCE:g} mm of "
                           f"room; bored {TIGHT_CUT_DEPTH:g} deep only, against burn marks",))
    for dia, t in drills.items():
        if abs(d - dia) < DRILL_MATCH_TOL:
            if depth <= TIGHT_CUT_DEPTH + DEPTH_TOL:
                return HoleChoice(t, dia, None)
            return HoleChoice(t, dia, TIGHT_CUT_DEPTH,
                              (f"a {d:g} mm hole is drilled with a cutter of its own diameter ({t.stem}); "
                               f"{TIGHT_CUT_DEPTH:g} deep only, against burn marks",))
    return None


def feed_scale(d: float, tool: float) -> float:
    """A bore's feed in times the template's: the hole in tool diameters."""
    return round(d / tool, FEED_SCALE_DECIMALS)


# -- pockets and contours ------------------------------------------------------------------------

def candidates(registry: Registry, kind: Kind, label: str, finish: bool, cutter: str) -> tuple[list[Template], list[str]]:
    """The templates a pocket or contour may take, in the order they are
    tried: the one the label names (resolved for the cutter and the
    finishing pass, `Registry.resolve`), then the others of the kind for the
    cutter with the same finishing pass, no wider, widest first, those whose
    label is most like the label's first."""
    chosen, notes = registry.resolve(kind, label, finish, cutter)
    pool = registry.of(kind, cutter)
    if chosen is None:
        notes.append(f"no {kind} template {label!r}; the widest that fits is taken")
        same = [t for t in pool if t.finish == finish] or pool
        limit = math.inf
    else:
        same = [t for t in pool if t.finish == chosen.finish]
        limit = chosen.diameter
    rest = sorted((t for t in same if t is not chosen and t.diameter <= limit + 1e-9),
                  key=lambda t: (-t.diameter, -len(os.path.commonprefix([t.label, label])), t.cutter_tag is None,
                                 t.stem))
    return ([chosen] if chosen is not None else []) + rest, notes


@dataclass
class PocketPlan:
    """The templates a pocket takes: the first gets into it, the others
    take rests (what the wider ones left, with a cutter's radius of room
    around it in what they cleared), the pieces no candidate reaches are
    left."""
    main: Template | None = None
    rests: list[tuple[Template, Polygon]] = field(default_factory=list[tuple[Template, Polygon]])
    unreached: list[Polygon] = field(default_factory=list[Polygon])
    notes: list[str] = field(default_factory=list[str])


def pocket_cutters(region: BaseGeometry, depth: float, tried: Sequence[Template],
                   excused: BaseGeometry | None = None) -> PocketPlan:
    """The pocket templates for a region `depth` deep (mm, the flute's
    reach: through it plus the breakthrough), as the module's doc says."""
    out = PocketPlan()
    usable: list[Template] = []
    for t in tried:
        if t.adaptive and (region.area < SMALL_POCKET_AREA or
                           region.buffer(-ADAPTIVE_ROOM * t.diameter / 2).is_empty):
            continue
        if t.flute is not None and t.flute < depth - DEPTH_TOL:
            out.notes.append(f"{t.stem}: its flute ({t.flute:g}) does not reach {depth:g} deep")
            continue
        usable.append(t)
    getting_in = [t for t in usable if gets_in(region, t.diameter / 2)]
    for t in getting_in:
        if t.diameter < ALONE * getting_in[0].diameter - 1e-9:
            break
        if not unreached(region, t.narrowest / 2, excused):
            out.main = t
            return out
    if not getting_in:
        out.unreached = polygons_of(region)
        return out
    out.main = getting_in[0]
    left = unreached(region, out.main.narrowest / 2, excused)
    for t in usable[usable.index(out.main) + 1:]:
        if not left:
            break
        theirs = unreached(region, t.narrowest / 2, excused)
        blocked = unary_union(theirs) if theirs else Polygon()
        took = [p for p in left if p.intersection(blocked).area < 1e-6] if theirs else list(left)
        if took:
            # with the room around them the narrower cutter works in, in the region the wider one cleared
            grown = unary_union([p.buffer(t.diameter / 2 + TOOL_CLEARANCE) for p in took]).intersection(region)
            out.rests += [(t, g) for g in polygons_of(grown)]
        left = [p for p in left if p not in took]
    out.unreached = left
    return out


def contour_cutter(waste: BaseGeometry, through: float, tried: Sequence[Template],
                   excused: BaseGeometry | None = None) -> tuple[Template | None, list[str]]:
    """The contour template for a contour whose waste side is `waste`
    (the region the cutter runs in), cutting `through` deep: the first
    tried whose cutter reaches all of it and whose flute cuts through;
    else the first whose flute cuts through, with a note; else the first."""
    notes: list[str] = []
    deep = [t for t in tried if t.flute is None or t.flute >= through - DEPTH_TOL]
    if not deep and tried:
        notes.append(f"no contour template's flute cuts {through:g} deep (keeping {tried[0].stem}, "
                     f"{tried[0].flute:g}); check the operation")
        deep = [tried[0]]
    for t in deep:
        if not unreached(waste, t.narrowest / 2, excused, clearance=0.0):
            return t, notes
    if not deep:
        return None, notes
    narrowest = min(deep, key=lambda t: t.diameter)
    notes.append(f"no contour cutter reaches all of it; {narrowest.stem} is taken")
    return narrowest, notes


# -- dog bones ---------------------------------------------------------------------------------------

def self_cut(d: float, cutter: float) -> bool:
    """Whether a dog bone `d` across is cut by its operation's own cutter."""
    return d >= cutter - RELIEF_TOL


def dogbone_route(d: float, drills: dict[float, Template], dogbones: Sequence[Template]) -> Template | None:
    """A drill template of the dog bone's diameter, else the widest dog
    bone template that fits it, else None."""
    for dia, t in drills.items():
        if abs(d - dia) < DRILL_MATCH_TOL:
            return t
    fitting = [t for t in dogbones if t.diameter <= d - RELIEF_TOL]
    return max(fitting, key=lambda t: (t.diameter, t.cutter_tag is not None)) if fitting else None


# -- the V-bit ---------------------------------------------------------------------------------------

def v_bit(registry: Registry, kind: Kind, cutter: str, label: str | None) -> tuple[Template | None, list[str]]:
    """The chamfer's or groove's template: the one labelled so, else the 90
    degree bit that reaches deepest."""
    pool = registry.of(kind, cutter, [label] if label is not None else None)
    if not pool:
        return None, [f"no {kind} template{f' {label!r}' if label else ''} for the {cutter} cutter"]

    def right(t: Template) -> bool:
        taper = t.ops[0].tool.taper
        return taper is not None and abs(taper - V_BIT_TAPER) <= V_BIT_TAPER_TOL

    chosen = max(pool, key=lambda t: (right(t), t.reach or 0.0))
    notes = [] if right(chosen) else [f"{chosen.stem} is not a 90 degree bit; it does not cut the modelled "
                                      f"{kind}s to shape"]
    return chosen, notes


def chamfer_fits(size: float, hole_radius: float | None, t: Template) -> tuple[bool, list[str]]:
    """Whether the V-bit cuts a chamfer of `size`: a hole's rim must leave
    its tip room, past the chamfer's foot by the template's tip offset."""
    offset = t.number("chamferTipOffset") or 0.0
    tip = t.ops[0].tool.tip
    if hole_radius is not None and hole_radius - offset - tip / 2 < TOOL_CLEARANCE:
        return False, [f"a {size:g} chamfer on a {2 * hole_radius:g} mm hole is too narrow for {t.stem} with its "
                       f"tip offset of {offset:g}"]
    notes: list[str] = []
    reach = t.reach
    if reach is not None and size + offset > reach + DEPTH_TOL:
        notes.append(f"a {size:g} chamfer needs {size + offset:g} of flank with the tip offset, {t.stem} has "
                     f"{reach:g}; check the operation")
    return True, notes


def groove_passes(depth: float, t: Template) -> int:
    """How many passes a V-groove `depth` deep takes: one per stepdown."""
    step = t.stepdown
    return 1 if step is None else max(1, math.ceil((depth - DEPTH_TOL) / step))
