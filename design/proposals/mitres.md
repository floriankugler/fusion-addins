# Mitred corners

Status: added by Florian 2026-10-14 ("angled boards"), worked out by Claude
the same day; nothing built. Only the points marked [Florian] are his. The
spellings are working titles, to be settled in a detailed plan before
implementing [Florian]. Needs bevels (`bevels.md`), and tilted boards
(`tilted-boards.md`) for angles other than 90 degrees.

Two boards meeting at an angle along an edge, each end cut to the plane that
halves the angle, glued. Proposed as a joint, the sharp sibling of `bend()`
(`bent-boards.md`).

- The legs are placed as for a bend, their outer faces meeting in a line,
  each reaching the corner, and `front.join(side, using=miter())` cuts both
  ends to the halving plane, which makes one bevel on each, the long points
  at the outer faces.
- Like any bevel it is hand work: the mitre cannot be machined, so the
  machine cuts the larger contour and the mitre is cut by hand later
  [Florian]. So each board's machine outline is that of its outer face.
- At 90 degrees both boards stay square to the frame and need bevels only;
  any other angle needs a tilted board.
- No connectors in a mitre for now (glue and tape; Dominos square to the
  mitre would be hand work too) [open].
- A mitre on a lipped edge or on a bent board is an error.
- The two boards stay two parts, so this is a joint and not a bend.
