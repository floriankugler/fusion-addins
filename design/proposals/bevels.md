# Bevels and hand work

Status: added by Florian 2026-10-14, worked out by Claude the same day;
nothing built. Only the points marked [Florian] are his. The spellings are
working titles, to be settled in a detailed plan before implementing
[Florian]. Comes before miters (`miters.md`) and before fitted ends on tilted
boards (`tilted-boards.md`).

A narrow face cut at an angle through the whole thickness, which a sloped
front and a mitred corner need. Today a chamfer as deep as the board is thick
is refused.

- `bevel()`, an ordered operation. `side.bevel(side.top, 30,
  long=side.outer)` tilts the top narrow face 30 degrees from square, about
  its edge at the outer face, which keeps its full size (the long point).
  `side.bevel(side.top, to=plane)` tilts it until it lies in a plane or in
  another part's face, so that an end fits a part at an angle.
- Bevels are not machined: the machine cuts the larger contour and the bevel
  is cut by hand afterwards [Florian]. So a part has two shapes. Its true
  shape is what the preview, the module documents and every check use. Its
  machine outline is the outline at the face where it reaches furthest,
  which nesting and CAM take.
- A bevel goes on a hand-work list per part (which edge, angle, which face
  has the long point), together with lipping and roundover notes (see
  `cam.md`).
- An operation near a bevel must lie on the true face.
- The emitter gets one new instruction, a wedge cut off the body, and the
  mesher one boolean.
- The end cut of a slat (`design/slats.md`) is the same operation and would be
  spelled `bevel()` too.
