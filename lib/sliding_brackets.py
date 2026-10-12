"""Sliding brackets that hold a removable panel on a frame: where their
screws go, the room their plates need, and the defaults for drilling
them, in mm.

A bracket is a pair of plastic parts that click together. The panel and
the frame board it hangs on stand square to each other, the panel's back
face against (or near) the frame board's front edge. The frame part is
screwed to the frame board's inner face, the big face toward the panel's
middle; the panel part is screwed to the panel's back face, its tongue
lying flat beside the frame board. Pushing the panel onto the frame
slides the tongue under the frame part's hook until the hook's lip snaps
in; pulled off, the panel comes away square to itself. Latched, the two
parts fix each other's position, so everything is measured

- out: on the panel's back face, square to the frame board, from the
  plane of the frame board's inner face into the cabinet;
- back: on the frame board's inner face, square to the panel, from the
  plane of the panel's back face, away from the panel;
- along: along the frame board's edge, from the bracket's centre; both
  parts are symmetric about it and their holes lie at the same places.

Two frame parts take the same panel part (Häfele Pacofix PF):

- PF-L-R, bent (`PACOFIX_PF_L_R`): the hook is bent back over the frame
  part's own plate, which reaches from the panel's back face 33 back (its
  last 4 rounded underneath), so the plate's front end lies at the
  panel's back face and the frame holes 8 behind it. The tongue lies on
  that plate, 4 off the frame board, so the panel holes are 19 out from
  the frame board's face. The panel sits on the frame board's edge (no
  gap: the plate would hang over the edge), or the frame boards reach
  past its back face, the panel set in between them.
- PF-L, straight (`PACOFIX_PF_L`): the hook points from the plate toward
  the panel; the tongue lies on the frame board's face and ends at the
  plate, which is 29 to 45 behind the panel's back face, its holes 37
  behind it (the System 32 line when the panel sits on the frame board's
  edge); the panel holes 15 out from the frame board's face. The frame
  holes depend on the panel's back face, not on the frame board's edge: a
  gap between the panel and that edge moves them closer to it (37 - gap),
  and the plate stays on the board up to a gap of 29.

Per bracket each part has two holes, `hole_pitch` (32) apart along the
edge: the frame part's `frame_hole_back` behind the panel's back face,
the panel part's `panel_hole_out` out from the frame board's face. Each
part needs its plate on its board: the frame part `frame_plate_back`
behind the panel's back face (where its underside is flat), the panel
part `panel_plate_out` out from the frame board's face, both
`plate_length` long. `max_gap` is where the frame part's plate begins.
A panel set in between the frame boards ends a little short of the frame
board's face; up to `MAX_PLATE_OVERHANG` of the panel part's plate may
hang over its edge there.

Each part takes two countersunk screws through 4.2 mm holes (countersunk
to 8.4) in its 4 mm plate. The holes default to Ø2 x 6 mm pilots for
chipboard screws; Euro screws (6.3 mm; the frame parts 262.50.391 and
262.50.377, the panel part 262.50.358 are made for them) take Ø5 holes,
`EURO_DEPTH` deep for a 6.3 x 13.5 screw through the plate. Fixed-depth
holes are flat-bottomed.

Keku's rules for the pairs: at least `MIN_PER_PANEL` per panel, at most
`MAX_SPACING` apart. Häfele: not for hanging loads (ceiling panels); a
pair carries 20 kg vertically, 30 kg lying horizontally.

Häfele Pacofix and Keku are the same parts: Häfele says the Pacofix
"clicks with all Keku plastic fittings", Keku's data sheet lists its AS
parts (and the bent ASR frame part) under Häfele's numbers, and the
dimension drawings are identical. Articles, for chipboard / Euro screws:
panel part PF 262.50.359 / .358, frame part PF-L-R 262.50.390 / .391,
frame part PF-L 262.50.368 / .377; the sets 262.50.380 (PF with PF-L-R)
and 262.50.313 (PF with PF-L). Measured 2026-10-12 on Häfele's CAD models
(glTF) of 262.50.359, 262.50.390 and 262.50.368, fitted together latched:

- panel part: 48 long, its plate 23 wide out from the tongue's side and 4
  thick, the tongue 10 high, 22.1 wide and 29 long, with a channel down
  its middle that narrows toward the panel and a ramp in its floor; holes
  15 from the tongue's side;
- PF-L-R: plate 48 x 33 x 4, holes 8 from its front end; the bent hook
  16 wide, 10.05 to 14 off the board, from its closed end 33 behind the
  panel's back face to its free end 9.1 behind it. Latched, the lip's
  back flank lies on the tongue's ramp all along with the panel's back
  face 8.15 to 8.2 in front of the holes (8 taken: the plate's front
  end), the hook's tapered sides 0.2 mm clear of the channel, its roof on
  the channel's floor, and the tongue's walls as high as the roof;
- PF-L: plate 48 x 16 x 4, holes on its centre line; the hook 16 wide,
  reaching 10.2 off the board and 28 from the holes toward the panel.
  Latched, the tongue's tip meets the plate, the hook's sides are 0.1 to
  0.2 mm clear of the channel and the lip's back flank lies on the ramp,
  with the frame holes 37 behind the panel's back face, as Häfele's
  mounting drawing has them.

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
    #: Back: where the frame part's plate bears on the frame board's face.
    frame_plate_back: tuple[float, float]
    #: Out: the panel part's plate on the panel's back face; it begins at
    #: the tongue's side, which lies on the frame board or the frame part.
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


#: Häfele Pacofix PF (panel part) with the bent PF-L-R frame part.
PACOFIX_PF_L_R = BracketSpec(
    name="Pacofix PF-L-R",
    title="Häfele Pacofix PF / PF-L-R (Keku ASR)",
    hole_pitch=32.0,
    frame_hole_back=8.0,
    panel_hole_out=19.0,
    plate_length=48.0,
    frame_plate_back=(0.0, 29.0),
    panel_plate_out=(4.0, 27.0),
)

#: Häfele Pacofix PF (panel part) with the straight PF-L frame part, the
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

#: Every bracket by name, as the language's `BracketModel` names them; the
#: first is the default.
BRACKETS: dict[str, BracketSpec] = {spec.name: spec for spec in (PACOFIX_PF_L_R, PACOFIX_PF_L)}

#: The panel part's tongue: 10 high from its side, 29 long from the
#: panel's back face; its holes 15 from its side; its plate 23 wide.
TONGUE_LENGTH = 29.0
PANEL_PART_HOLE = 15.0
PANEL_PLATE_WIDTH = 23.0

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
#: How far the panel part's plate may hang over the edge of a panel set in
#: between the frame boards that stops short of the plate's start.
MAX_PLATE_OVERHANG = 3.0
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
    bent, straight = PACOFIX_PF_L_R, PACOFIX_PF_L
    assert list(BRACKETS) == ["Pacofix PF-L-R", "Pacofix PF-L"]
    for spec in BRACKETS.values():
        # One panel part: its holes 15 from the tongue's side, its plate 23
        # wide from there, 8 beyond the holes.
        tongue_side = spec.panel_plate_out[0]
        assert spec.panel_hole_out == tongue_side + PANEL_PART_HOLE, spec.name
        assert spec.panel_plate_out[1] - spec.panel_plate_out[0] == PANEL_PLATE_WIDTH, spec.name
        assert spec.panel_plate_out[1] - spec.panel_hole_out == 8, spec.name
        # The frame part's holes 8 from the plate's front end.
        assert spec.frame_hole_back - spec.frame_plate_back[0] == 8, spec.name
        assert spec.frame_plate_back[0] < spec.frame_hole_back < spec.frame_plate_back[1], spec.name
        assert spec.hole_pitch == 32 and spec.plate_length == 48, spec.name
        assert spec.max_gap == spec.frame_plate_back[0], spec.name
    # PF-L-R: the tongue lies on the 4 mm plate, which begins at the
    # panel's back face, so there is no gap; the tongue reaches the end of
    # the plate's flat underside (29), the hook's closed end.
    assert bent.panel_plate_out[0] == 4 and bent.max_gap == 0 and bent.frame_plate_back[1] == TONGUE_LENGTH
    # PF-L: the tongue lies on the frame board and ends where the plate
    # begins; 37 = 29 + 8 behind the panel's back face, the System 32 line.
    assert straight.panel_plate_out[0] == 0 and straight.max_gap == TONGUE_LENGTH
    assert straight.frame_hole_back == 37 and straight.frame_plate_back == (29, 45)
    cm = bent.in_cm()
    assert (cm.hole_pitch, cm.frame_hole_back, cm.panel_hole_out, cm.plate_length) == (3.2, 0.8, 1.9, 4.8)
    assert (cm.frame_plate_back, cm.panel_plate_out) == ((0.0, 2.9), (0.4, 2.7))
    cm = straight.in_cm()
    assert (cm.hole_pitch, cm.frame_hole_back, cm.panel_hole_out, cm.plate_length) == (3.2, 3.7, 1.5, 4.8)
    assert (cm.frame_plate_back, cm.panel_plate_out) == ((2.9, 4.5), (0.0, 2.3))
    assert (cm.name, cm.title) == (straight.name, straight.title)
    # Holes and placement.
    assert 0 < PILOT_DIAMETER < EURO_DIAMETER and 0 < PILOT_DEPTH < EURO_DEPTH
    assert DEFAULT_END_OFFSET >= bent.plate_length / 2
    assert 0 < MAX_PLATE_OVERHANG < PANEL_PART_HOLE
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
    for spec in BRACKETS.values():
        print(f"  {spec.title}: frame holes {spec.frame_hole_back:g} behind the panel, panel holes "
              f"{spec.panel_hole_out:g} out from the frame, {spec.hole_pitch:g} apart; gap up to {spec.max_gap:g}")


if __name__ == "__main__":
    _self_check()
