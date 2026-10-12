"""Drilling data of lift-up hatch hinges, in mm, and the defaults for
drilling them.

Everything is measured from the hinge reference: the level of the
underside of the carcass top, where it meets the inner front edge of the
side panel (the manufacturer's drilling template is pushed up against the
underside of the top). "Below" runs down from that level, "back" into the
carcass from its front edge, and "inward" into the cabinet from the side
panel's inner face. The hatch is modelled closed, its inner face against
the carcass front (up to `MAX_HATCH_GAP` in front of it).

Each hinge drills a column of holes into the inner face of the side panel
it is mounted on, and pilot holes for the mounting plate's screws into the
hatch's inner face. How far the hatch top may reach above the reference
(the overlap A) depends on the hatch thickness and the opening angle; it
is only checked, never chosen.

Shared by the hatch_hinge add-in (which converts a spec to cm with
`HingeSpec.in_cm()`) and the modeling language (lang/hardware/
hatch_hinges.py). Plain Python without Fusion imports; `python3 -m
lib.hatch_hinges` runs its self-checks.
"""
from dataclasses import dataclass, replace


#: How far in front of the carcass the closed hatch may be modelled, mm.
#: The hinges' depth adjustment takes up a small gap.
MAX_HATCH_GAP = 2.0

#: Depth of the carcass holes unless set otherwise, mm (their diameter is
#: the hinge's).
CARCASS_HOLE_DEPTH = 12.0
#: Diameter and depth of the pilot holes for the mounting plate's screws
#: in the hatch unless set otherwise, mm.
PILOT_DIAMETER = 2.0
PILOT_DEPTH = 4.0


@dataclass(frozen=True)
class HingeSpec:
    """Drilling data of a lift-up hatch hinge, mm (see the module
    docstring for the reference and the directions)."""

    name: str
    carcass_hole_diameter: float
    carcass_hole_back: float
    carcass_first_hole_below: float
    carcass_hole_pitch: float
    carcass_hole_count: int
    hatch_hole_inward: float
    hatch_first_hole_below: float
    hatch_hole_pitch: float
    hatch_hole_count: int
    #: (hatch thickness, overlap) pairs, ascending: how far the hatch top
    #: may reach above the hinge reference before the hatch hits the
    #: carcass while opening fully. Interpolated linearly in between; the
    #: thickness range is the supported one.
    max_overlap: tuple[tuple[float, float], ...]
    #: The same limit with the opening limited (`limited_opening`).
    limited_max_overlap: float
    #: Footprint of the mounting plate on the hatch (inward range, below
    #: range). It must lie on the hatch.
    plate_inward: tuple[float, float]
    plate_below: tuple[float, float]
    #: Points inside the closed hinge (inward, back, below). No other body
    #: may contain them.
    probe_points: tuple[tuple[float, float, float], ...]
    #: The full opening angle and the one with the limiter fitted, degrees.
    opening: int
    limited_opening: int

    @property
    def min_hatch_thickness(self) -> float:
        return self.max_overlap[0][0]

    @property
    def max_hatch_thickness(self) -> float:
        return self.max_overlap[-1][0]

    def overlap_limit(self, hatch_thickness: float, limited: bool) -> float:
        """How far the hatch top may reach above the reference, for a hatch
        `hatch_thickness` thick, with the opening limited or not."""
        if limited:
            return self.limited_max_overlap
        table = self.max_overlap
        if hatch_thickness <= table[0][0]:
            return table[0][1]
        for (thickness0, overlap0), (thickness1, overlap1) in zip(
            table,
            table[1:],
        ):
            if hatch_thickness <= thickness1:
                fraction = (hatch_thickness - thickness0) / (
                    thickness1 - thickness0
                )
                return overlap0 + (overlap1 - overlap0) * fraction
        return table[-1][1]

    def in_cm(self) -> "HingeSpec":
        """This spec with every length in cm, Fusion's internal unit.
        Dividing by 10 gives exactly the cm literals (3.7 for 37), which
        multiplying by 0.1 would not."""
        def cm(value: float) -> float:
            return value / 10

        return replace(
            self,
            carcass_hole_diameter=cm(self.carcass_hole_diameter),
            carcass_hole_back=cm(self.carcass_hole_back),
            carcass_first_hole_below=cm(self.carcass_first_hole_below),
            carcass_hole_pitch=cm(self.carcass_hole_pitch),
            hatch_hole_inward=cm(self.hatch_hole_inward),
            hatch_first_hole_below=cm(self.hatch_first_hole_below),
            hatch_hole_pitch=cm(self.hatch_hole_pitch),
            max_overlap=tuple(
                (cm(thickness), cm(overlap))
                for thickness, overlap in self.max_overlap
            ),
            limited_max_overlap=cm(self.limited_max_overlap),
            plate_inward=(cm(self.plate_inward[0]), cm(self.plate_inward[1])),
            plate_below=(cm(self.plate_below[0]), cm(self.plate_below[1])),
            probe_points=tuple(
                (cm(inward), cm(back), cm(below))
                for inward, back, below in self.probe_points
            ),
        )


# Häfele Free space 1.11 (372.27.xxx, every spring strength drills the
# same), from the installation manual, checked against Häfele's STEP model
# (372.27.300): carcass 3 x 5 mm, 32 apart, 37 behind the front edge, the
# top one 102 below the reference (closed, the hinge then stops 1.8 mm
# below the carcass top); the plate slots sit 90 and 26 mm above the top
# carcass hole, so the hatch holes are 12 and 76 below the reference; at
# 90 degrees the hatch clears the carcass front up to a 37 mm overlap. The
# STEP centres the plate 24.15 mm from the side panel; the manual's 25 mm
# is used, the hinge's +-1.5 mm side adjustment covers the difference.
# Plate footprint and probe points come from the STEP model, where the
# hatch's inner face sits 0.3 mm in front of the carcass. Read 2026-10-07.
FREE_SPACE_1_11 = HingeSpec(
    name="Häfele Free space 1.11",
    carcass_hole_diameter=5.0,
    carcass_hole_back=37.0,
    carcass_first_hole_below=102.0,
    carcass_hole_pitch=32.0,
    carcass_hole_count=3,
    hatch_hole_inward=25.0,
    hatch_first_hole_below=12.0,
    hatch_hole_pitch=64.0,
    hatch_hole_count=2,
    max_overlap=(
        (16.0, 24.5),
        (18.0, 24.0),
        (19.0, 23.5),
        (22.0, 22.5),
        (24.0, 22.0),
        (26.0, 21.5),
        (28.0, 21.0),
    ),
    limited_max_overlap=37.0,
    plate_inward=(15.5, 34.5),
    plate_below=(5.0, 83.0),
    probe_points=(
        (16.0, 37.0, 3.0),
        (25.0, 1.0, 3.0),
        (13.0, 25.0, 6.0),
        (12.0, 25.0, 42.0),
        (12.0, 25.0, 82.0),
        (12.0, 25.0, 152.0),
        (30.0, 3.0, 62.0),
    ),
    opening=107,
    limited_opening=90,
)

HINGE_SPECS: tuple[HingeSpec, ...] = (FREE_SPACE_1_11,)


def _self_check() -> None:
    spec = FREE_SPACE_1_11
    # The add-in's spec in cm, exactly as it was written there before the
    # data moved here (2026-10-12).
    cm = spec.in_cm()
    assert (
        cm.carcass_hole_diameter,
        cm.carcass_hole_back,
        cm.carcass_first_hole_below,
        cm.carcass_hole_pitch,
        cm.carcass_hole_count,
    ) == (0.5, 3.7, 10.2, 3.2, 3)
    assert (
        cm.hatch_hole_inward,
        cm.hatch_first_hole_below,
        cm.hatch_hole_pitch,
        cm.hatch_hole_count,
    ) == (2.5, 1.2, 6.4, 2)
    assert cm.max_overlap == (
        (1.6, 2.45),
        (1.8, 2.4),
        (1.9, 2.35),
        (2.2, 2.25),
        (2.4, 2.2),
        (2.6, 2.15),
        (2.8, 2.1),
    )
    assert cm.limited_max_overlap == 3.7
    assert cm.plate_inward == (1.55, 3.45)
    assert cm.plate_below == (0.5, 8.3)
    assert cm.probe_points == (
        (1.6, 3.7, 0.3),
        (2.5, 0.1, 0.3),
        (1.3, 2.5, 0.6),
        (1.2, 2.5, 4.2),
        (1.2, 2.5, 8.2),
        (1.2, 2.5, 15.2),
        (3.0, 0.3, 6.2),
    )
    assert (cm.name, cm.opening, cm.limited_opening) == (
        spec.name,
        spec.opening,
        spec.limited_opening,
    )
    assert (MAX_HATCH_GAP / 10, CARCASS_HOLE_DEPTH / 10) == (0.2, 1.2)
    assert (PILOT_DIAMETER / 10, PILOT_DEPTH / 10) == (0.2, 0.4)

    # The overlap limit: the table's values, linear in between, clamped
    # outside, the limiter's own value.
    assert spec.overlap_limit(18, False) == 24
    assert abs(spec.overlap_limit(20, False) - (23.5 - 1 / 3)) < 1e-12
    assert spec.overlap_limit(10, False) == 24.5
    assert spec.overlap_limit(40, False) == 21
    assert spec.overlap_limit(18, True) == 37
    assert abs(cm.overlap_limit(2.0, False) * 10 - spec.overlap_limit(20, False)) < 1e-12
    assert (spec.min_hatch_thickness, spec.max_hatch_thickness) == (16, 28)

    for hinge in HINGE_SPECS:
        thicknesses = [thickness for thickness, _ in hinge.max_overlap]
        overlaps = [overlap for _, overlap in hinge.max_overlap]
        assert thicknesses == sorted(set(thicknesses)), hinge.name
        assert overlaps == sorted(overlaps, reverse=True), hinge.name
        assert hinge.limited_max_overlap >= overlaps[0], hinge.name
        assert hinge.limited_opening < hinge.opening, hinge.name
        # The pilot holes lie on the mounting plate, the carcass holes
        # below the reference, and the probe points inside the cabinet,
        # behind the carcass front and below the top.
        lo, hi = hinge.plate_inward
        assert lo < hinge.hatch_hole_inward < hi, hinge.name
        for index in range(hinge.hatch_hole_count):
            below = hinge.hatch_first_hole_below + index * hinge.hatch_hole_pitch
            assert hinge.plate_below[0] < below < hinge.plate_below[1], hinge.name
        assert hinge.carcass_first_hole_below > hinge.carcass_hole_diameter / 2
        assert all(min(point) > 0 for point in hinge.probe_points), hinge.name
    # STEP: the plate slots 90 and 26 above the top carcass hole.
    assert [
        spec.carcass_first_hole_below - (spec.hatch_first_hole_below + i * spec.hatch_hole_pitch)
        for i in range(spec.hatch_hole_count)
    ] == [90, 26]

    print("hatch_hinges: all checks passed")
    for hinge in HINGE_SPECS:
        carcass = [
            hinge.carcass_first_hole_below + i * hinge.carcass_hole_pitch
            for i in range(hinge.carcass_hole_count)
        ]
        hatch = [
            hinge.hatch_first_hole_below + i * hinge.hatch_hole_pitch
            for i in range(hinge.hatch_hole_count)
        ]
        print(
            f"  {hinge.name}: carcass {hinge.carcass_hole_count} x "
            f"{hinge.carcass_hole_diameter:g} at {hinge.carcass_hole_back:g} back, "
            f"{carcass} below; hatch at {hinge.hatch_hole_inward:g} inward, "
            f"{hatch} below; hatches {hinge.min_hatch_thickness:g}-"
            f"{hinge.max_hatch_thickness:g} mm"
        )


if __name__ == "__main__":
    _self_check()
