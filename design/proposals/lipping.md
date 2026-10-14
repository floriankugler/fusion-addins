# Lipping and edge banding

Status: added by Florian 2026-10-14, worked out by Claude the same day;
nothing built. Only the points marked [Florian] are his. The spellings are
working titles, to be settled in a detailed plan before implementing
[Florian]. Needs slats (`slats.md`); a good first item for the standard
library (`standard-library.md`).

Solid wood glued along a narrow face, either lipping (10 x 12 on a 12 mm
board, say) or banding (0.5 to 2 mm). For construction they are the same
thing in different thicknesses [Florian]. The strip's material is solid wood
given by its cross-section, as a slat's [Florian]: `oak = slat_material("oak",
10, 12)` (`slats.md`). `side.lip(side.front, side.top, using=oak)` [spelling
open; it may be a standard-library function instead]:

- The lipping takes its thickness off the board and puts a slat of the
  section in its place [Florian]. The board keeps its placement box and the
  slat lies inside it, as tenons and grooves keep the box, so `side.front`
  stays the finished face that hinges, gaps and limits measure from. The slat
  is named after the board and face (`side.lip_front`), its grain runs along
  it, and it goes on the cut list by section and length. The section must be
  at least as wide as the board is thick; a wider one is trimmed flush (a
  hand-work note).
- Where two lipped faces meet, the strips are either mitred or butted; both
  happen [Florian]. Mitred, both are bevelled at the corner, which is hand
  work like any mitre. Butted, one runs through and the other butts against
  it. The call chooses, `corners="miter"` or `"butt"`, with the strip on the
  face lipped first running through [proposed].
- Only on a straight edge of the outline: not along a fillet or other curve
  (banding could follow curves later), not on a bevelled or mitred edge, not
  on a bent board [Florian]. On a tilted board it works in the board's own
  frame.
- Ordered like a cut: an operation made before it where the strip goes is an
  error, and so is a join at a lipped face.
- The board is machined to its cut-back outline; glue-up and flush trimming
  go on the hand-work list. Whether thin banding (0.5 mm) cuts the board back
  or is left out of the geometry is a choice per material [open].
