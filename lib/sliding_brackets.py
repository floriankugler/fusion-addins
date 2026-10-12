"""Sliding brackets that hold a removable panel on a frame: where their
screws go, the room their plates need, and the defaults for drilling
them, in mm.

A bracket is a pair of plastic parts that click together. The panel and
the frame board it hangs on stand square to each other, the panel's back
face against (or near) the frame board's front edge. The frame part is
screwed to the frame board's inner face, the big face toward the panel's
middle, its hook pointing toward the panel; the panel part is screwed to
the panel's back face, its tongue lying on the frame board's inner face.
Pushing the panel onto the frame slides the tongue under the hook until
the hook's lip snaps in and the tongue's tip meets the frame part's
plate; pulled off, the panel comes away square to itself. Latched, the
two parts fix each other's position, so everything is measured

- out: on the panel's back face, square to the frame board, from the
  plane of the frame board's inner face into the cabinet;
- back: on the frame board's inner face, square to the panel, from the
  plane of the panel's back face, away from the panel;
- along: along the frame board's edge, from the bracket's centre; both
  parts are symmetric about it and their holes lie at the same places.

The frame part's two holes lie `frame_hole_back` (37) behind the panel's
back face, the System 32 line when the panel sits on the frame board's
edge; the panel part's two holes `panel_hole_out` (15) out from the frame
board's face; each pair `hole_pitch` (32) apart. The frame holes depend
on the panel's back face, not on the frame board's edge: a gap between
the panel and that edge moves them closer to it (37 - gap), and the
frame part's plate stays on the board up to a gap of `max_gap` (29, where
the plate begins); a panel set in between the frame boards, the frame
boards reaching past its back face, gets them 37 behind its back face
too. Each part needs its plate on its board: the frame part
`frame_plate_back` behind the panel's back face, the panel part
`panel_plate_out` out from the frame board's face, both `plate_length`
long. A panel set in between the frame boards ends a little short of
the frame board's face; up to `MAX_PANEL_CLEARANCE` of the panel part's
plate may hang over its edge there.

Each part takes two countersunk screws through 4.2 mm holes in its 4 mm
plate. The holes default to Ø2 x 6 mm pilots for chipboard screws;
Euro screws (6.3 mm, the frame part 262.50.377) take Ø5 holes,
`EURO_DEPTH` deep for a 6.3 x 13.5 screw through the plate. Fixed-depth
holes are flat-bottomed.

Keku's rules for the pairs: at least `MIN_PER_PANEL` per panel, at most
`MAX_SPACING` apart. Häfele: not for hanging loads (ceiling panels); a
pair carries 20 kg vertically, 30 kg lying horizontally.

Häfele Pacofix PF / PF-L and Keku AS are the same part: Häfele says the
Pacofix "clicks with all Keku plastic fittings", Keku's data sheet lists
the AS parts under Häfele's numbers, and the dimension drawings are
identical. Measured 2026-10-12 on Häfele's CAD models (glTF) of the panel
part 262.50.359 and the frame part 262.50.368 (both for chipboard screws;
262.50.377 is the frame part for Euro screws): the panel part 48 long
along the edge, its plate 23 wide out from its tongue's outer side and 4
thick, the tongue 10 high, 22.1 wide and 29 long, holes 15 from the
tongue's side; the frame part's plate 48 x 16 x 4 with its holes on its
centre line, the hook 16 wide, reaching 10.2 from the board and 28 from
the holes toward the panel. Latched (the tongue's tip against the frame
part's plate, the hook's tapered sides 0.1 to 0.2 mm clear of the
tongue's tapered channel, the lip's back flank on the tongue's ramp),
the tongue's side lies on the frame board's face and the frame holes 37
behind the panel's back face, as Häfele's mounting drawing has them.

Shared by the modeling language (lang/hardware/sliding_brackets.py) and a
later add-in, which would work in cm (`BracketSpec.in_cm`). Plain Python
without Fusion imports; `python3 -m lib.sliding_brackets` runs its
self-checks.
"""
from dataclasses import dataclass, replace


@dataclass(frozen=True)
class BracketSpec:
    """Mounting data of a sliding bracket, in mm (see the module docstring
    for out, back and along)."""

    #: The name the language's `BracketModel` uses.
    name: str
    #: How messages and documents name it.
    title: str
    #: Along the edge: each part's two holes, centred on the bracket.
    hole_pitch: float
    #: Back: the frame part's holes behind the panel's back face.
    frame_hole_back: float
    #: Out: the panel part's holes from the frame board's face.
    panel_hole_out: float
    #: Along the edge: both plates, centred on the bracket.
    plate_length: float
    #: Back: the frame part's plate on the frame board's face.
    frame_plate_back: tuple[float, float]
    #: Out: the panel part's plate on the panel's back face.
    panel_plate_out: tuple[float, float]

    @property
    def max_gap(self) -> float:
        """The widest gap between the panel's back face and the frame
        board's edge: the frame part's plate begins there."""
        return self.frame_plate_back[0]

    def in_cm(self) -> "BracketSpec":
        """This spec with every length in cm, Fusion's internal unit."""
        def cm(value: float) -> float:
            return value / 10

        return replace(
            self,
            hole_pitch=cm(self.hole_pitch),
            frame_hole_back=cm(self.frame_hole_back),
            panel_hole_out=cm(self.panel_hole_out),
            plate_length=cm(self.plate_length),
            frame_plate_back=(cm(self.frame_plate_back[0]), cm(self.frame_plate_back[1])),
            panel_plate_out=(cm(self.panel_plate_out[0]), cm(self.panel_plate_out[1])),
        )


#: Häfele Pacofix PF (panel part) with PF-L (frame part with lip), the
#: same as Keku AS.
PACOFIX_PF_L = BracketSpec(
    name="Pacofix PF-L",
    title="Häfele Pacofix PF / PF-L (Keku AS)",
    hole_pitch=32.0,
    frame_hole_back=37.0,
    panel_hole_out=15.0,
    plate_length=48.0,
    frame_plate_back=(29.0, 45.0),
    panel_plate_out=(0.0, 23.0),
)

#: Every bracket by name, as the language's `BracketModel` names them.
BRACKETS: dict[str, BracketSpec] = {PACOFIX_PF_L.name: PACOFIX_PF_L}

# -- holes -----------------------------------------------------------------------------

#: Pilot holes for countersunk chipboard screws: diameter and depth.
PILOT_DIAMETER = 2.0
PILOT_DEPTH = 6.0
#: Holes for Euro screws (6.3 mm thread): diameter and depth, for a 6.3 x
#: 13.5 screw through the 4 mm plate (9.5 into the board) with room to spare.
EURO_DIAMETER = 5.0
EURO_DEPTH = 11.0

# -- placement -------------------------------------------------------------------------

#: Brackets per frame board unless set otherwise.
DEFAULT_COUNT = 2
#: From the ends of the stretch the panel and the frame board share to the
#: first and last bracket's centre. At least half a plate.
DEFAULT_END_OFFSET = 50.0
#: How far the edge of a panel set in between the frame boards may stop
#: short of the frame board's face, the panel part's plate hanging over it.
MAX_PANEL_CLEARANCE = 3.0
#: Keku: brackets at most this far apart, at least this many per panel.
MAX_SPACING = 600.0
MIN_PER_PANEL = 4


def stations(length: float, count: int, end: float = DEFAULT_END_OFFSET) -> list[float]:
    """The brackets' centres along a stretch `length` long, from one of its
    ends: one in the middle, or `count` from `end` to `length - end`,
    evenly spaced. Raises ValueError for no bracket or a stretch no longer
    than twice `end`."""
    if count < 1:
        raise ValueError("There must be at least one bracket.")
    if count == 1:
        return [length / 2]
    if length <= 2 * end:
        raise ValueError(f"The stretch ({length:g}) is too short for the end offset ({end:g}).")
    spacing = (length - 2 * end) / (count - 1)
    return [end + spacing * i for i in range(count)]


def _self_check() -> None:
    spec = PACOFIX_PF_L
    # The frame part's holes on its plate's centre line, 8 from each long
    # edge; the panel part's 8 from its plate's inner edge.
    lo, hi = spec.frame_plate_back
    assert spec.frame_hole_back - lo == hi - spec.frame_hole_back == 8
    assert spec.panel_plate_out[1] - spec.panel_hole_out == 8
    assert spec.panel_plate_out[0] == 0          # the tongue's side on the frame board's face
    # 37 = 29 + 8: the tongue (29 long) ends where the frame part's plate begins.
    assert spec.max_gap == 29 and spec.frame_hole_back == spec.max_gap + 8
    # The holes lie on the plates, on the System 32 pitch.
    assert spec.hole_pitch / 2 < spec.plate_length / 2 and spec.hole_pitch == 32
    assert BRACKETS == {"Pacofix PF-L": spec}
    cm = spec.in_cm()
    assert (cm.hole_pitch, cm.frame_hole_back, cm.panel_hole_out, cm.plate_length) == (3.2, 3.7, 1.5, 4.8)
    assert (cm.frame_plate_back, cm.panel_plate_out) == ((2.9, 4.5), (0.0, 2.3))
    assert (cm.name, cm.title) == (spec.name, spec.title)
    # Holes and placement.
    assert 0 < PILOT_DIAMETER < EURO_DIAMETER and 0 < PILOT_DEPTH < EURO_DEPTH
    assert DEFAULT_END_OFFSET >= spec.plate_length / 2
    assert 0 < MAX_PANEL_CLEARANCE < spec.panel_hole_out
    assert stations(500, 2) == [50, 450]
    assert stations(500, 3, 100) == [100, 250, 400]
    assert stations(80, 1) == [40]
    for length, count, end in ((100, 2, 50), (100, 0, 10)):
        try:
            stations(length, count, end)
        except ValueError:
            continue
        raise AssertionError((length, count, end))
    print("sliding_brackets: all checks passed")
    print(f"  {spec.title}: frame holes {spec.frame_hole_back:g} behind the panel, panel holes "
          f"{spec.panel_hole_out:g} out from the frame, {spec.hole_pitch:g} apart; gap up to {spec.max_gap:g}")


if __name__ == "__main__":
    _self_check()
