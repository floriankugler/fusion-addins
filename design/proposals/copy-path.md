# Copy Path and named geometry on hand-modeled bodies

Status: proposed; the rules were tested read-only on Planung (2026-10-09).
Nothing built. The compiler add-in's docstring says "Copy Path comes later".

A board made by the compiler knows its sides by construction. Finding named
faces geometrically is only needed for hand-modeled bodies (escape hatches
3, 5 and 6 in `hand-made-geometry.md`) and for a Copy Path helper. Its
heuristics stay out of the language.

## Wanted

- A command in the compiler add-in that copies the path of the current
  selection to the clipboard, so a face or edge picked in Fusion can be
  written into a build file. Click-to-path in the browser preview is the
  same thing outside Fusion, grown to faces, edges and anchors in
  `preview-assist.md`.
- Nested copies of parts carry the full path as body name, which is also the
  part label at the machine (done for compiled parts).

## Rules for finding named geometry on a body

- nearest direction wins; a face at 45 degrees is an error, not a guess;
- the outermost face wins when several point the same way;
- a side is a plane and may consist of several coplanar faces;
- an edge is the line where two side planes meet; the real edges are found
  along it (there may be none, because of chamfers, or several);
- `inner` and `outer` mean toward and away from the module's centre;
- a side made by a reference takes the reference's name
  (`batten3.floor_profile`).

## What the read-only check on "Planung" showed

The rules were tested on the existing hand-modeled document (2,279 timeline
items). 451 bodies were classified as boards by a heuristic, which lets a few
brackets and box-shaped electrical parts through. Linked components were
skipped.

| Result per board                                               | Boards | Share |
|----------------------------------------------------------------|--------|-------|
| All six sides are one axis-aligned face each                   | 174    | 39%   |
| All six resolve, but some sides are tilted or split into several faces | 219 | 49% |
| At least one side does not resolve                             | 58     | 13%   |

- Furniture modules resolve in 84-100% of boards (Küche 2 84%, Bank FS 93%,
  Bank BFS 96%, Hochschrank 97%, Heckstauraum 98%, Bett 100%).
- Parts fitted to the vehicle do not: Decke 44%, Abdeckungen 0 of 8. Fenster
  reaches 83%, but only 1 of its 66 boards is axis-aligned.
- 443 of 452 board placements sit in unrotated components and none are
  mirrored, so one global direction definition is enough for documents
  modeled in place.
- "Outermost wins" had to choose on 41% of the cleanly resolved sides.
- 9% of sides are several coplanar faces.
- Where both sides of an edge were single faces, 88% shared exactly one edge
  and 11% shared none.

Attributes surviving operations are irrelevant for compiler output, which is
never edited; only Copy Path on hand-modeled bodies cares.
