# Chamfers at any angle

Status: added by Florian 2026-10-14, worked out by Claude the same day;
nothing built. Only the points marked [Florian] are his. The spellings are
working titles, to be settled in a detailed plan before implementing
[Florian].

What exists [checked 2026-10-14]: corners of the outline are rounded by
`fillet()` and `shape.rounded()`, and cut off by `chamfer()` on an edge
through the board (`panel.front.left`), at 45 degrees, `size` along both
edges. `shape.clip(top=, back=)` cuts a corner with two lengths, but only on
a shape before it is placed. A chamfer along an edge at a big face
(`side.front.inner`, a face's outline, an operation's rim) is a 45 degree rim
chamfer, shallower than the board is thick.

Proposed:

- Both kinds also take two lengths in place of `size`, each named by the
  face it is measured on, as `clip()` names its edges:
  `panel.chamfer(panel.front.left, front=30, left=80)`, and
  `side.chamfer(side.front.inner, front=4, inner=8)`, which is 4 into the
  thickness and 8 across the inner face. An angle is given as two lengths
  [open: whether `angle=` with one length is worth having too].
- A corner chamfer is part of the outline, so the machine cuts it at any
  angle.
- A rim chamfer at an angle other than 45 degrees needs a V-bit of that
  angle, which Auto Setup does not recognise (it takes 45 degree flanks
  only). So it gets a template of its own or is hand work (see `bevels.md`)
  [open].
