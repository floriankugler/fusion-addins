# Placement and references

Where parts sit: boxes, `on` and `between`, the position algebra, and
contours as limits. Part of the modeling language's design; the overview is
`DESIGN.md`. Code: `lang/core/refs.py`, `box.py`, `part.py`, `contours.py`.

## Boxes and bays

- A module is a box with six named sides. Boards sit `on` a side or
  reference and are trimmed `between` neighbours, so most parts carry no
  dimensions of their own. `interior.split()` divides space, for example
  into drawer bays.
- `interior` is the box inside the boards lying on its sides that cover the
  side's middle (a carcass side, a bottom between the sides, a back); a foot
  or a cleat in a corner does not count.
- A box exposes its sides as positions (`box.left`, `box.top`) and its
  lengths as `box.width`, `box.depth`, `box.height`, which measure along the
  left-right, front-back and top-bottom axes of the box's frame. Where an
  extent is an argument it is one of those three names, checked by the type
  checker: `bay.split("height", 3)`, `.grain("depth")`. Axis letters do not
  appear in build files. [decided]
- `split("height", 3)` makes equal bays; `split("height", [230])` cuts a
  230 mm bay off and returns it with the remaining space, which is split
  again: `first, rest = space.split("height", [230]); rest.split("height",
  2)`. Several sizes work the same, the remainder last. No "fill the rest"
  marker: the steps say it. Bays run from bottom to top, left to right,
  front to back in the box's own frame. [decided]

## Placing a board

- The constructor is `board(name, material, shape=None)`; the placement
  modifiers are `.on(ref, toward=)`, `.between(*limits)`, `.center(pos)`,
  `.inset(n)`, `.grain(along)`, `.show(face)`, `.manual()`, `.nest(False)`
  (left out of the nest, `design/nesting.md`; like `.show()` it changes no
  shape, so it may come after the placement is used). `.inset(n)`
  shrinks the outline by `n` on every side of its box, which is how an inset
  front gets its gap; there are no one-off modifiers such as margin or lift,
  because `.on(box.bottom + slide.recess)` already says lift.
- A slat (`slat(name, material, section=(w, h))`) is placed by naming what
  its faces do: `.on()` a wide face, `.edge_on()` a narrow face, `.center()`
  its middle, two of them on different axes, and `.between()` its two ends
  only; as a limit for another part it gives its faces on both of its cross
  axes (see `design/slats.md`).
- Which side the thickness goes: `.on()` a module side puts the thickness
  inward, also a side moved into or out of the box (`on(cab.bottom.into(60))`);
  `.on()` a bare plane requires a side (`toward=`).
- Limits missing from `.between()` default to the enclosing scope's box.
- When a part is given as a limit, its face toward the board is meant: the
  face toward the other limit on that axis, or toward the middle of the
  enclosing box when it is the only one; the board then lies on the far side
  of that face from the part. A single position as a limit leaves the board
  on the side of it the box's middle is on. A box as a limit gives both ends
  on each in-plane axis, `between(drawer_box)`.
- Errors rather than guesses:
  - a limit that limits neither in-plane axis (a position on the thickness
    axis, a board parallel to this one);
  - limits that leave it open where the board lies, each error naming what
    is ambiguous [decided]: the same board twice on an axis; two boards
    overlapping each other on it (nothing lies between them); a position, or
    a board's face moved by `gap()`, lying inside a board given as another
    limit, past what its `into()` reaches; a single limit at the middle of
    the box (the board could lie on either side); and a board as the only
    limit whose middle is the box's (not clear which face is meant).
- A board made of a shape is placed by its limits [decided]: between two
  limits on an axis it fills them less its inset, or it is an error naming
  both widths; with one limit it sits against it, on the side the board
  would lie; with none, at the scope's front, left and bottom side (or the
  origin without a box); and its box is its outline's.
- Grain is required whenever the material has grain, as an axis in module
  space, with a scope-level default; defaulting by the longer side is wrong
  for fronts.

## References instead of numbers

Anywhere a length or a position is expected, a reference can be given
instead of a number. This replaces the extrude options Florian uses a lot in
Fusion (start from offset or from object plus offset, extent to object plus
offset). [decided as a need]

| Fusion extrude option       | In the language                              |
|-----------------------------|----------------------------------------------|
| Start from offset           | `.on()` a reference, moved with `+`/`-`      |
| Start from object + offset  | the same; the reference is the object        |
| Extent to object + offset   | `.between()` for parts, `depth=to(...)` for cuts |
| Extent through all          | `depth=through`                              |

References can be computed with, for example `(bottom.top + top.bottom) / 2`:

- position +/- length gives a position;
- position - position gives a length;
- a weighted mix of positions whose weights add up to 1 gives a position,
  also with positions taken away: `a + b - c` [decided]; a length taken
  from a sum of positions whose weights do not add up to 1 is an error
  saying so;
- anything else (a bare sum of two positions, mixing axes) is an error.

This only works for flat, parallel references.

- `+` and `-` move along the world axis (`cab.bottom + 60` is 60 inside only
  where the world's top is its axis's positive end, the van's). Fits that
  hold in any frame use `.into(n)` and `.gap(n)`, which need no sign
  convention and also work on contours, by offsetting the curve; on a box
  side they give a side, its inward direction kept, so a board lies on them
  without `toward=` [decided].
- A part as a `between()` limit means its face toward the board;
  `part.into(n)` and `part.gap(n)` move it.
- `spread()` gives positions along one axis (`pitch=` or `count=`, not
  both), running from the end given first.

```python
mid = (bottom.top + top.bottom) / 2
height = top.bottom - bottom.top         # a length

shelf = (board("shelf", ply15)
         .center(mid)
         .between(left.into(5), right.into(5), back.gap(2)))
```

## Contours as limits

A contour from the master (see `design/master.md`) can be a limit. Both
cases are polyline math on the snapshot. [decided]

- **In the part's own plane** it bounds the outline directly. A closed
  contour is intersected with the outline and its bounds stand in for
  missing limits. An open contour is an edge: it limits the axis across its
  chord (first to last point), the part keeps the side its other limit on
  that axis is on (or the middle of its room), and the edge follows the
  contour; a chord at 45 degrees, or the other limit within the contour's
  reach, is an error.
- **In a perpendicular plane** the contour must hold the part over its whole
  thickness: its section across that plane, from one big face to the other,
  keeps clear of the contour. A closed contour gives a stretch on the axis
  the two planes share; an open contour gives a position there, and must
  cross each face once. The position is the part's end on the contour's
  side: the part lies on the side its other limit on that axis is on,
  without one on the side of an open contour in its own plane on that axis,
  else in the middle of its room; a clearance reaching past the other limit
  is an error, and so are two open contours across a part on one side of it.
- **Several stretches.** Where the contour leaves several stretches (a
  batten along the wall, cut in two by a wheel arch), the part's limits on
  that axis pick one: a single limit the stretch it lies in, two limits the
  one between them, and two limits spanning several stretches are an error
  naming them, since a part is one piece. So the two pieces of an
  interrupted batten are two parts, each given one end:
  `between(..., floor_outline, floor_front)` and `... floor_back)`.
- **Open contours run one way**: along its chord's axis in the part's plane,
  and through the part's thickness in a perpendicular plane. Run from its
  first point toward its last, no point may lie more than 0.01 mm behind the
  furthest the contour has reached along that axis; one that does runs back
  along itself, an overhang such as a lip, and is an error that says to draw
  the lip as a closed contour. The whole contour counts, whichever part takes
  it. Nor may it run straight back over itself, in any direction, for more
  than 0.01 mm (a spike, measured at the vertex where it turns as the shorter
  of the straight runs into and out of it). [decided]
- **Clearance.** `contour.gap(n)` keeps n of clearance, measured in the
  contour's plane with round joins, so it is exact at corners (GEOS offsets
  the area given in one form, without points along its edges, so the same
  contour gives the same part however its points run; the clearance is at
  least n and up to about a hundredth more, which is accepted [decided]);
  `contour.into(n)` reaches past it. Stretches from closed contours cut
  every other range down (tighter wins).
- A contour that splits the part in two, leaves nothing, lies in a tilted
  plane or is not planar is an error.
- The part's box is the bounds of what the contours leave, so a batten
  whose lower edge follows the floor profile has its `bottom` at the
  profile's lowest point.

The floor battens in `examples/van.py` are the worked case: each batten is
`.center(x)` on the front-back axis and `.between(top, floor_profile.gap(2),
floor_outline.gap(3))`, limited by three references with no numbers of its
own. Nothing in it is specific to one vehicle; the next van needs a new
master and the same floor code.
