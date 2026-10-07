"""Cabinet-side hole patterns of concealed drawer slides, and the choice of
the pre-drill holes among them.

Blum Movento and Grass Dynapro share one cabinet drilling grid, measured
from the cabinet front edge with the runner mounted for overlay fronts:

- The screw holes form a row 38 mm above the carcass bottom the runner rests
  on (both catalogs: "min. 38").
- The holes come in groups at 9 mm pitch. Each group ends at a 32 mm system
  position P = 37 + 32k and holds P, P - 9, P - 18 (P - 27 at the front).
- Every runner starts with the groups at 37 (10/19/28/37) and 69 (60/69 on
  Grass, 51/60/69 on Blum); the rear groups depend on the model and the
  nominal length.

Sources: Blum TD-132/1 DE/06.22 p.13 and Grass "Dynapro Führungs-System" p.13
and p.15, cross-checked on 2026-10-07 against Häfele's STEP models of every
length. Where the two disagreed (Movento 766H NL 700/750, Dynapro 70 kg
NL 450) the catalog wins. Only the upper row is modelled; the runners' lower
row (12 mm below) is not used.

This module is plain Python without Fusion imports, so the selection logic
can be checked outside Fusion: `python3 -m lib.drawer_slides`.
"""
from dataclasses import dataclass


#: Height of the screw row above the line the runner rests on, in mm.
HOLE_ROW_HEIGHT = 38.0
#: Minimum cabinet depth beyond the nominal length, in mm (MET = NL + 3).
DEPTH_ALLOWANCE = 3.0
#: Distance between neighbouring holes of a group, in mm.
GROUP_PITCH = 9.0


@dataclass(frozen=True)
class Hole:
    #: Distance from the cabinet front edge, in mm.
    position: float
    #: Place in its group, counted from the group's 32 mm system hole: 0 for
    #: the system hole, 1 for the hole 9 mm in front of it, and so on.
    index_in_group: int

    @property
    def is_odd(self) -> bool:
        """The 1st and 3rd hole of a group are odd, the 2nd and 4th even.

        Because 9 and 32 share no factor, every position on the grid has
        exactly one group and index, so an odd hole never coincides with an
        even one - whatever model or length sits on the other side of a
        shared carcass board."""
        return self.index_in_group % 2 == 0


@dataclass(frozen=True)
class HoleGroup:
    #: The group's system hole (37 + 32k), its rearmost hole, in mm.
    system_position: float
    count: int = 3

    def holes(self) -> list[Hole]:
        return [
            Hole(self.system_position - index * GROUP_PITCH, index)
            for index in range(self.count)
        ]


@dataclass(frozen=True)
class LengthRange:
    nominal_lengths: tuple[int, ...]
    #: System positions of the rear groups (three holes each), in mm.
    rear_groups: tuple[float, ...]


@dataclass(frozen=True)
class SlideModel:
    #: Dropdown value; stored with editable results, so never reuse one.
    value: int
    name: str
    front_groups: tuple[HoleGroup, ...]
    ranges: tuple[LengthRange, ...]

    @property
    def nominal_lengths(self) -> list[int]:
        return sorted(
            length
            for length_range in self.ranges
            for length in length_range.nominal_lengths
        )

    def holes(self, nominal_length: int) -> list[Hole]:
        """All upper-row holes of the cabinet rail, front to back."""
        length_range = next(
            (
                candidate
                for candidate in self.ranges
                if nominal_length in candidate.nominal_lengths
            ),
            None,
        )
        if length_range is None:
            raise ValueError(
                f"{self.name} is not available in NL {nominal_length}."
            )
        groups = list(self.front_groups) + [
            HoleGroup(position) for position in length_range.rear_groups
        ]
        holes = [hole for group in groups for hole in group.holes()]
        return sorted(holes, key=lambda hole: hole.position)


_BLUM_FRONT = (HoleGroup(37, 4), HoleGroup(69, 3))
_GRASS_FRONT = (HoleGroup(37, 4), HoleGroup(69, 2))

MOVENTO_760H = SlideModel(
    value=0,
    name="Blum Movento 760H (40 kg)",
    front_groups=_BLUM_FRONT,
    ranges=(
        LengthRange((250, 270), (197,)),
        LengthRange((300, 320, 350), (261,)),
        LengthRange(
            (380, 400, 420, 450, 480, 500, 520, 550, 600),
            (261, 293),
        ),
    ),
)
MOVENTO_766H = SlideModel(
    value=1,
    name="Blum Movento 766H (60/70 kg)",
    front_groups=_BLUM_FRONT,
    ranges=(
        LengthRange((450,), (261, 293)),
        LengthRange((500, 520, 550, 580, 600), (261, 293, 357)),
        LengthRange((650, 700, 750), (261, 293, 357, 453)),
    ),
)
DYNAPRO_40 = SlideModel(
    value=2,
    name="Grass Dynapro (40 kg)",
    front_groups=_GRASS_FRONT,
    ranges=(
        LengthRange((250, 270, 300, 320), (133, 165, 197)),
        LengthRange((350, 380, 400, 420, 450), (165, 229, 261)),
        LengthRange((480, 500, 520), (165, 261, 293, 325)),
        LengthRange((550,), (165, 261, 293, 325, 389)),
        LengthRange((600,), (165, 261, 293, 325, 389, 421)),
    ),
)
DYNAPRO_50_70 = SlideModel(
    value=3,
    name="Grass Dynapro (50/70 kg)",
    front_groups=_GRASS_FRONT,
    ranges=(
        LengthRange((450, 500, 520, 550, 580), (165, 261, 293, 325, 389)),
        LengthRange((600, 650, 700, 750), (165, 261, 293, 325, 389, 421)),
    ),
)

SLIDE_MODELS = [MOVENTO_760H, MOVENTO_766H, DYNAPRO_40, DYNAPRO_50_70]


def slide_model(value: int) -> SlideModel:
    for model in SLIDE_MODELS:
        if model.value == value:
            return model
    raise ValueError(f"Unknown drawer slide model {value}.")


def candidate_holes(model: SlideModel, nominal_length: int, odd: bool) -> list[float]:
    """Positions of the odd or the even holes, front to back, in mm."""
    return [
        hole.position
        for hole in model.holes(nominal_length)
        if hole.is_odd == odd
    ]


def choose_holes(candidates: list[float], count: int) -> list[float]:
    """Picks `count` of the sorted `candidates`, spread as evenly as the
    rail allows: always the front-most and the rearmost hole, and in between
    the holes that come closest (least squares) to equal spacing."""
    if count < 1:
        raise ValueError("At least one hole per slide is required.")
    if count > len(candidates):
        raise ValueError(
            f"Only {len(candidates)} holes are available, not {count}."
        )
    if count == 1:
        return [candidates[0]]
    if count == len(candidates):
        return list(candidates)
    first, last = candidates[0], candidates[-1]
    targets = [
        first + (last - first) * index / (count - 1)
        for index in range(count)
    ]
    # cost[k][i]: best cost with target k placed on candidate i.
    size = len(candidates)
    infinity = float("inf")
    cost = [[infinity] * size for _ in range(count)]
    previous = [[-1] * size for _ in range(count)]
    cost[0][0] = 0.0
    for k in range(1, count):
        for i in range(k, size):
            error = (candidates[i] - targets[k]) ** 2
            for j in range(k - 1, i):
                if cost[k - 1][j] + error < cost[k][i]:
                    cost[k][i] = cost[k - 1][j] + error
                    previous[k][i] = j
    chosen = [size - 1]
    for k in range(count - 1, 0, -1):
        chosen.append(previous[k][chosen[-1]])
    return [candidates[i] for i in reversed(chosen)]


def _self_check() -> None:
    # Upper rows read off the Häfele STEP models (KV positions, mm).
    assert [hole.position for hole in MOVENTO_760H.holes(500)] == [
        10, 19, 28, 37, 51, 60, 69, 243, 252, 261, 275, 284, 293,
    ]
    assert [hole.position for hole in MOVENTO_760H.holes(250)] == [
        10, 19, 28, 37, 51, 60, 69, 179, 188, 197,
    ]
    assert [hole.position for hole in MOVENTO_766H.holes(650)][-3:] == [435, 444, 453]
    assert [hole.position for hole in DYNAPRO_40.holes(500)] == [
        10, 19, 28, 37, 60, 69, 147, 156, 165,
        243, 252, 261, 275, 284, 293, 307, 316, 325,
    ]
    assert [hole.position for hole in DYNAPRO_40.holes(300)][6:9] == [115, 124, 133]
    assert [hole.position for hole in DYNAPRO_40.holes(400)][9:12] == [211, 220, 229]
    assert len(DYNAPRO_50_70.holes(750)) == 24

    for model in SLIDE_MODELS:
        for length in model.nominal_lengths:
            holes = model.holes(length)
            positions = [hole.position for hole in holes]
            assert len(set(positions)) == len(positions), (model.name, length)
            # Every hole sits on the 9 mm sub-grid of a 37 + 32k position.
            for hole in holes:
                system = hole.position + hole.index_in_group * GROUP_PITCH
                assert (system - 37) % 32 == 0, (model.name, length, hole)
            odd = set(candidate_holes(model, length, True))
            even = set(candidate_holes(model, length, False))
            assert odd and even and not odd & even

    # Odd and even sets never share a position across models and lengths.
    all_odd = {
        position
        for model in SLIDE_MODELS
        for length in model.nominal_lengths
        for position in candidate_holes(model, length, True)
    }
    all_even = {
        position
        for model in SLIDE_MODELS
        for length in model.nominal_lengths
        for position in candidate_holes(model, length, False)
    }
    assert not all_odd & all_even

    odd = candidate_holes(DYNAPRO_40, 500, True)
    even = candidate_holes(DYNAPRO_40, 500, False)
    assert choose_holes(odd, 4) == [19, 147, 243, 325]
    assert choose_holes(even, 4) == [10, 156, 252, 316]
    assert choose_holes(odd, 2) == [odd[0], odd[-1]]
    assert choose_holes(odd, len(odd)) == odd
    for model in SLIDE_MODELS:
        for length in model.nominal_lengths:
            for is_odd in (True, False):
                candidates = candidate_holes(model, length, is_odd)
                for count in range(2, len(candidates) + 1):
                    chosen = choose_holes(candidates, count)
                    assert chosen == sorted(set(chosen)) and len(chosen) == count
                    assert chosen[0] == candidates[0]
                    assert chosen[-1] == candidates[-1]
    print("drawer_slides: all checks passed")
    for model in SLIDE_MODELS:
        print(f"  {model.name}: NL {model.nominal_lengths[0]}-{model.nominal_lengths[-1]}")
        length = 500 if 500 in model.nominal_lengths else model.nominal_lengths[-1]
        for is_odd in (True, False):
            candidates = candidate_holes(model, length, is_odd)
            print(
                f"    NL {length} {'odd ' if is_odd else 'even'}: "
                f"{len(candidates)} holes, 4 chosen {choose_holes(candidates, 4)}"
            )


if __name__ == "__main__":
    _self_check()
