"""Drilling patterns of the door latches the door_latch_native add-in
places: Everlock, the Pull Lock 44 mm and the Sugatsune LL-66 one-touch
latch, in mm.

A latch holds a door or a drawer face shut against a carcass board beside
one of its edges, e.g. the carcass top above a door's upper edge. Its body
sits on the door's inner face (the big face toward the carcass), its
strike (the LL-66's counter plate) on the carcass board's big face toward
the door, the carcass face. Every position belongs to a latch station, a
point on the door's edge, and is measured

- along the edge, from the station; every pattern is symmetric about it;
- below: on the door's inner face, square to the edge, from the plane of
  the carcass face, away from the carcass board. The door's holes hang
  from the carcass face, not from the door's edge, so an overlay door and
  an inset door get them in the same place relative to the carcass;
- behind: on the carcass face, square to the edge, from the plane of the
  door's inner face, into the carcass.

The add-in measures the same way from the two edges the user selects: the
door's edge on its inner face and the carcass face's edge next to it.

Per station:

- Everlock: a 25 mm finger hole through the door, 30 below the carcass
  face, and four pilot holes for the body's screws, 26 to either side and
  26 and 42 below (the add-in calls the row nearer the carcass face the
  lower one); the strike's pilot pair 14 to either side, 25 behind.
- Pull Lock 44: a 38.1 mm (1 1/2") hole through the door, 34 below, and
  from the door's inner face a 48 mm counterbore that leaves 10 mm of
  material at the front; a door no thicker than that gets no counterbore.
  The strike's pilot pair 9.5 to either side, 29 behind.
- Sugatsune LL-66: the body's two mounting holes, 56 apart, 10 below: they
  lie 6.5 below the body's top edge and the body's top sits 3.5 below the
  carcass face (the datasheet's mounting drawing dimensions both). The
  counter plate's holes 20 apart, 24 behind the door's inner face (19 + 5
  when a gasket is used; the gap variant is not modelled).

Pilot holes take the pre-drill diameter and depth, by default 1/8" (3.175)
and 3 mm. One latch sits in the middle of the door's edge; more run from
END_OFFSET from each end, evenly spaced (`stations`).

Sources: the add-in's constants, moved here 2026-10-12 (the Everlock and
Pull Lock numbers date from its predecessor `door_latch`, which recorded
no source; the LL-66 numbers from Sugatsune's datasheet, as the add-in's
comment said). Shared by door_latch_native (in cm, converted where it
reads them) and the modeling language (lang/hardware/latches.py). Plain
Python without Fusion imports; `python3 -m lib.door_latches` runs its
self-checks.
"""
import math
from dataclasses import dataclass
from typing import Literal

# -- Everlock ----------------------------------------------------------------------

#: The body's pilot holes: their columns' distance to either side of the station.
EVERLOCK_PILOT_COLUMN_OFFSET = 26.0
#: The body's pilot rows below the carcass face: the one nearer to it
#: ("lower" in the add-in) and the farther one ("upper").
EVERLOCK_LOWER_ROW_INSET = 26.0
EVERLOCK_UPPER_ROW_INSET = 42.0
#: The finger hole through the door: below the carcass face, and its diameter.
EVERLOCK_MAIN_INSET = 30.0
EVERLOCK_MAIN_DIAMETER = 25.0
#: The strike's pilot pair: to either side of the station, behind the door's inner face.
EVERLOCK_CARCASS_PAIR_OFFSET = 14.0
EVERLOCK_CARCASS_INSET = 25.0

# -- Pull Lock 44 mm ---------------------------------------------------------------

#: The lock's hole through the door: below the carcass face, and its diameter (1 1/2").
PULL_LOCK_MAIN_INSET = 34.0
PULL_LOCK_DIAMETER = 38.1
#: The counterbore around it, from the door's inner face, and the material
#: it leaves at the door's front; a door no thicker than that has none.
PULL_LOCK_COUNTERBORE_DIAMETER = 48.0
PULL_LOCK_MIN_REMAINING = 10.0
#: The strike's pilot pair: to either side of the station, behind the door's inner face.
PULL_LOCK_CARCASS_PAIR_OFFSET = 9.5
PULL_LOCK_CARCASS_INSET = 29.0

# -- Sugatsune LL-66 -----------------------------------------------------------------

#: The body's top edge below the carcass face, and its mounting holes below
#: that edge (datasheet).
LL66_BODY_TOP_BELOW_CARCASS = 3.5
LL66_HOLES_BELOW_BODY_TOP = 6.5
#: The body's two pilot holes: to either side of the station (56 apart) and
#: below the carcass face (3.5 + 6.5).
LL66_DOOR_PILOT_HALF_SPACING = 28.0
LL66_DOOR_PILOT_INSET = LL66_BODY_TOP_BELOW_CARCASS + LL66_HOLES_BELOW_BODY_TOP
#: The counter plate's pilot pair: to either side (20 apart) and behind the
#: door's inner face (19, plus 5 for the gasket variant, which is not modelled).
LL66_CARCASS_PAIR_OFFSET = 10.0
LL66_CARCASS_INSET = 24.0

# -- the dialog's defaults -------------------------------------------------------------

#: Pilot holes for the latches' screws: 1/8" across, 3 deep.
PREDRILL_DIAMETER = 25.4 / 8
PREDRILL_DEPTH = 3.0
#: The first and last latch from the ends of the door's edge, when there are several.
END_OFFSET = 100.0


# -- the patterns, per latch ---------------------------------------------------------------

#: What a hole in the door is: a pilot hole for a screw (the pre-drill
#: diameter and depth), a hole through the door, or a counterbore from the
#: door's inner face that leaves `remaining` at its front.
HoleKind = Literal["pilot", "through", "counterbore"]


@dataclass(frozen=True)
class DoorHole:
    """A hole in the door's inner face at a station: `along` the edge and
    `below` the carcass face. Through holes and counterbores have their
    own `diameter`; pilot holes take the pre-drill's."""
    along: float
    below: float
    kind: HoleKind
    diameter: float | None = None
    #: The material a counterbore leaves at the door's front.
    remaining: float | None = None


@dataclass(frozen=True)
class Latch:
    """One latch's drilling pattern at a station: the holes in the door
    and the strike's pilot pair in the carcass face."""
    name: str
    door: tuple[DoorHole, ...]
    #: The strike's pilot pair: half its spacing along the edge, and its
    #: distance behind the door's inner face.
    carcass_pair_offset: float
    carcass_inset: float
    #: Where the add-in's layout anchors each station, below the carcass
    #: face: the main hole, or the middle of the LL-66's pilot pair. The
    #: add-in checks that a pilot-sized circle there lies on the door face.
    station_inset: float

    def carcass_holes(self) -> tuple[tuple[float, float], tuple[float, float]]:
        """The strike's pilot pair as (along, behind)."""
        return ((-self.carcass_pair_offset, self.carcass_inset), (self.carcass_pair_offset, self.carcass_inset))

    @property
    def max_predrill(self) -> float:
        """The pre-drill diameter must stay below the narrowest spacing
        between two pilot holes of a station, in the door or the carcass:
        the Everlock's rows (16), the other latches' strike pair (19 and
        20), as the add-in has it."""
        pilots = [(h.along, h.below) for h in self.door if h.kind == "pilot"]
        spacings = [math.hypot(a[0] - b[0], a[1] - b[1]) for i, a in enumerate(pilots) for b in pilots[i + 1:]]
        return min(spacings + [2 * self.carcass_pair_offset])


EVERLOCK = Latch(
    "Everlock",
    door=(
        DoorHole(-EVERLOCK_PILOT_COLUMN_OFFSET, EVERLOCK_LOWER_ROW_INSET, "pilot"),
        DoorHole(EVERLOCK_PILOT_COLUMN_OFFSET, EVERLOCK_LOWER_ROW_INSET, "pilot"),
        DoorHole(-EVERLOCK_PILOT_COLUMN_OFFSET, EVERLOCK_UPPER_ROW_INSET, "pilot"),
        DoorHole(EVERLOCK_PILOT_COLUMN_OFFSET, EVERLOCK_UPPER_ROW_INSET, "pilot"),
        DoorHole(0.0, EVERLOCK_MAIN_INSET, "through", EVERLOCK_MAIN_DIAMETER),
    ),
    carcass_pair_offset=EVERLOCK_CARCASS_PAIR_OFFSET,
    carcass_inset=EVERLOCK_CARCASS_INSET,
    station_inset=EVERLOCK_MAIN_INSET,
)
PULL_LOCK_44 = Latch(
    "Pull Lock 44",
    door=(
        DoorHole(0.0, PULL_LOCK_MAIN_INSET, "through", PULL_LOCK_DIAMETER),
        DoorHole(0.0, PULL_LOCK_MAIN_INSET, "counterbore", PULL_LOCK_COUNTERBORE_DIAMETER,
                 remaining=PULL_LOCK_MIN_REMAINING),
    ),
    carcass_pair_offset=PULL_LOCK_CARCASS_PAIR_OFFSET,
    carcass_inset=PULL_LOCK_CARCASS_INSET,
    station_inset=PULL_LOCK_MAIN_INSET,
)
LL_66 = Latch(
    "LL-66",
    door=(
        DoorHole(-LL66_DOOR_PILOT_HALF_SPACING, LL66_DOOR_PILOT_INSET, "pilot"),
        DoorHole(LL66_DOOR_PILOT_HALF_SPACING, LL66_DOOR_PILOT_INSET, "pilot"),
    ),
    carcass_pair_offset=LL66_CARCASS_PAIR_OFFSET,
    carcass_inset=LL66_CARCASS_INSET,
    station_inset=LL66_DOOR_PILOT_INSET,
)
LATCHES: dict[str, Latch] = {latch.name: latch for latch in (EVERLOCK, PULL_LOCK_44, LL_66)}


def stations(length: float, count: int, end: float = END_OFFSET) -> list[float]:
    """The stations along an edge `length` long, from one of its ends: one
    in the middle, or `count` from `end` to `length - end`, evenly spaced.
    Raises ValueError where the add-in refuses: no latch, an end offset
    that is not positive, or an edge no longer than twice the end offset."""
    if count < 1:
        raise ValueError("There must be at least one latch.")
    if count == 1:
        return [length / 2]
    if end <= 0:
        raise ValueError("The end offset must be greater than zero.")
    if length <= 2 * end:
        raise ValueError(f"The edge ({length:g}) is too short for the end offset ({end:g}).")
    spacing = (length - 2 * end) / (count - 1)
    return [end + spacing * i for i in range(count)]


def _self_check() -> None:
    for latch in LATCHES.values():
        # symmetric about the station
        door = {(h.along, h.below, h.kind, h.diameter) for h in latch.door}
        assert door == {(-a, b, k, d) for a, b, k, d in door}, latch.name
        assert all((h.diameter is None) == (h.kind == "pilot") for h in latch.door), latch.name
        assert all((h.remaining is not None) == (h.kind == "counterbore") for h in latch.door), latch.name
        assert any(h.along == 0 and h.below == latch.station_inset for h in latch.door) or latch is LL_66
        assert PREDRILL_DIAMETER < latch.max_predrill, latch.name
    # the add-in's limits on the pre-drill diameter
    assert EVERLOCK.max_predrill == EVERLOCK_UPPER_ROW_INSET - EVERLOCK_LOWER_ROW_INSET == 16
    assert PULL_LOCK_44.max_predrill == 2 * PULL_LOCK_CARCASS_PAIR_OFFSET == 19
    assert LL_66.max_predrill == 2 * LL66_CARCASS_PAIR_OFFSET == 20
    # Everlock: the finger hole between the pilot rows, clear of the pilots
    assert EVERLOCK_LOWER_ROW_INSET < EVERLOCK_MAIN_INSET < EVERLOCK_UPPER_ROW_INSET
    for row in (EVERLOCK_LOWER_ROW_INSET, EVERLOCK_UPPER_ROW_INSET):
        gap = ((EVERLOCK_PILOT_COLUMN_OFFSET ** 2 + (row - EVERLOCK_MAIN_INSET) ** 2) ** 0.5
               - EVERLOCK_MAIN_DIAMETER / 2 - PREDRILL_DIAMETER / 2)
        assert gap > 0, gap
    # Pull Lock: the counterbore around the through hole, leaving material
    assert PULL_LOCK_COUNTERBORE_DIAMETER > PULL_LOCK_DIAMETER and PULL_LOCK_MIN_REMAINING > 0
    assert PULL_LOCK_MAIN_INSET - PULL_LOCK_COUNTERBORE_DIAMETER / 2 > 0     # below the carcass face
    # LL-66, from the datasheet's dimensions
    assert LL66_DOOR_PILOT_INSET == 10 and 2 * LL66_DOOR_PILOT_HALF_SPACING == 56
    assert 2 * LL66_CARCASS_PAIR_OFFSET == 20 and LL66_CARCASS_INSET == 19 + 5
    # stations
    assert stations(566, 1) == [283]
    assert stations(566, 2, 80) == [80, 486]
    assert stations(566, 3, 80) == [80, 283, 486]
    assert stations(100, 1, 0) == [50]          # one latch: the end offset is not used
    for bad in ((566, 0, 80), (566, 2, 0), (160, 2, 80)):
        try:
            stations(*bad)
        except ValueError:
            continue
        raise AssertionError(bad)
    print("door_latches: all checks passed")
    for latch in LATCHES.values():
        holes = ", ".join(f"{h.kind} {h.diameter or PREDRILL_DIAMETER:g} at ({h.along:g}, {h.below:g})"
                          for h in latch.door)
        print(f"  {latch.name}: door {holes}; strike +-{latch.carcass_pair_offset:g} at "
              f"{latch.carcass_inset:g} behind; pre-drill below {latch.max_predrill:g}")


if __name__ == "__main__":
    _self_check()
