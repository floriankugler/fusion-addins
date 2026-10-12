"""Ball catches that hold an inspection hatch in its opening: where their
screws go, how wide the slot between the frame and the hatch must be, the
room each part needs, and the ball_catch add-in's dialog defaults.

A catch bridges the slot milled around the hatch. Its holder is screwed to
the frame, the board the opening is cut in, with its stop webs against the
opening's edge (the contour); its ball is screwed to the hatch. Both screws
sit on the perpendicular to the contour through the catch's position, the
holder's outside the contour, the ball's inside it. The holder's stop webs
must bear on a straight edge of the opening, so a catch needs half the
holder's width to the end of the edge's straight part (where a rounded
corner begins). Each part takes one screw; the add-in and the language
drill a flat-bottomed pilot hole for each.

Ganter GN 450-28-14 (plastic, b = 28, d = 14), read from Ganter's catalog
drawing (the product page's SVGs) on 2026-10-07: the holder's screw sits
8.4 mm from its stop-web face, and the two screws are s1 = 17.8 to 19.3 mm
apart, so the ball's screw goes s1 min - 8.4 = 9.4 mm into the hatch
(Florian confirmed 8.4 and 9.4 the same day). The slot must be 2.5 to 3.5
mm wide, and each part needs 15 mm of mounting surface beside it. The
holder is 28 mm wide along the contour, the ball part 14 mm, the ball's
base 10 mm across.

Shared by the ball_catch add-in, which works in cm (`CatchSpec.in_cm`),
and the modeling language (`lang/hardware/ball_catches.py`). Plain Python
without Fusion imports; `python3 -m lib.ball_catches` runs its self-checks.
"""
from dataclasses import dataclass, fields, replace


@dataclass(frozen=True)
class CatchSpec:
    """Mounting data of a ball catch, in mm (see the module docstring)."""

    name: str
    #: From the contour into the frame: the holder's screw.
    holder_hole_outward: float
    #: From the contour into the hatch: the ball's screw.
    ball_hole_inward: float
    #: Along the contour. The stop webs at its ends must bear on a straight
    #: edge.
    holder_width: float
    #: Width of the ball part along the contour.
    ball_width: float
    #: Diameter of the ball's base around its screw.
    ball_base_diameter: float
    #: Width range of the slot between frame and hatch.
    min_gap: float
    max_gap: float
    #: Mounting surface each part needs beside the slot.
    mounting_depth: float

    def in_cm(self) -> "CatchSpec":
        """The same catch with its lengths in cm, as the add-in works."""
        lengths = {f.name: getattr(self, f.name) / 10 for f in fields(self) if f.name != "name"}
        return replace(self, **lengths)


#: Ganter GN 450-28-14.
GN_450 = CatchSpec(
    name="GN 450",
    holder_hole_outward=8.4,
    ball_hole_inward=9.4,
    holder_width=28.0,
    ball_width=14.0,
    ball_base_diameter=10.0,
    min_gap=2.5,
    max_gap=3.5,
    mounting_depth=15.0,
)

#: Every catch by name, as the language's `CatchModel` names them.
CATCHES: dict[str, CatchSpec] = {GN_450.name: GN_450}

# -- the add-in's dialog defaults (Florian's choices, 2026-10-07) ---------------------

#: Catches shared between the selected edge and the one opposite; with an
#: odd number the selected edge gets one more.
DEFAULT_COUNT = 4
#: From the ends of an edge's straight part to its first and last catch, mm.
DEFAULT_END_OFFSET = 40.0
#: Pilot holes for the holder's and the ball's screws: diameter and depth, mm.
PILOT_DIAMETER = 2.0
PILOT_DEPTH = 4.0


def _self_check() -> None:
    spec = GN_450
    # The screws are s1 min apart; the ball's screw goes s1 min - 8.4 deep.
    assert abs(spec.holder_hole_outward + spec.ball_hole_inward - 17.8) < 1e-9
    # A catch needs 14 mm to the end of the straight edge.
    assert spec.holder_width / 2 == 14.0
    assert spec.min_gap < spec.max_gap
    # The ball's screw lies on the hatch, inside its 15 mm mounting surface,
    # for every slot the catch takes, and its base fits there.
    for gap in (spec.min_gap, spec.max_gap):
        assert gap < spec.ball_hole_inward - spec.ball_base_diameter / 2
        assert spec.ball_hole_inward + spec.ball_base_diameter / 2 <= gap + spec.mounting_depth
    # The holder's screw lies on its mounting surface.
    assert spec.holder_hole_outward < spec.mounting_depth
    # Two catches 40 mm from the ends need 80 mm of straight edge, and the
    # end offset leaves the holder on the straight part.
    assert DEFAULT_END_OFFSET >= spec.holder_width / 2
    assert 0 < PILOT_DIAMETER < spec.ball_base_diameter and PILOT_DEPTH > 0
    # The add-in's cm values (it read these numbers before they moved here).
    cm = spec.in_cm()
    assert cm.name == spec.name
    expected = {"holder_hole_outward": 0.84, "ball_hole_inward": 0.94, "holder_width": 2.8, "ball_width": 1.4,
                "ball_base_diameter": 1.0, "min_gap": 0.25, "max_gap": 0.35, "mounting_depth": 1.5}
    for name, value in expected.items():
        assert abs(getattr(cm, name) - value) < 1e-12, name
    assert (DEFAULT_END_OFFSET / 10, PILOT_DIAMETER / 10, PILOT_DEPTH / 10) == (4.0, 0.2, 0.4)
    assert CATCHES == {"GN 450": GN_450}
    print("ball_catches: all checks passed")
    print(f"  {spec.name}: holder hole {spec.holder_hole_outward:g} out, ball hole {spec.ball_hole_inward:g} in, "
          f"slot {spec.min_gap:g}-{spec.max_gap:g}, holder {spec.holder_width:g} wide")


if __name__ == "__main__":
    _self_check()
