# Slats

Status: the primitive was decided in the first plan (2026-10-09); its
material, placement and making were worked out with Florian 2026-10-14;
nothing built. Lipping (`lipping.md`) depends on it.

A **slat** is solid wood defined by cross-section and length. It has no
canonical top or bottom. [decided] Board versus slat is a matter of stock
form, not species: a glued-up solid wood panel is a board, and so is a batten
cut from plywood to follow the floor profile.

## Material

- `material()` becomes `sheet_material()`, and a slat's stock is a
  `slat_material()` [decided]:

  ```python
  ply15 = sheet_material("birch", t=15, size=(2500, 1250))
  oak20x40 = slat_material("oak", 20, 40, length=2500)
  ```

  `sheet=` becomes `size=`, so "sheet" is not said twice; the types are
  `SheetMaterial` and `SlatMaterial`, and a part's attribute stays
  `.material` [proposed].
- A slat material has a species, the two sizes of its section, and
  optionally the stock length, for a length check as `size=` is for the
  sheet check. It always has grain. Its label is `oak 20x40`.
- The sizes come in either order: the larger is the width of the slat's
  wide faces, the smaller that of its narrow faces. Which way the slat lies
  is said by its placement, not by its material. In a square section all
  four faces are alike.
- `slat()` with a sheet material and `board()` with a slat material are
  errors.
- Lipping and banding take a slat material (`lipping.md`).

## Placement

Each of the slat's three axes is placed by its own modifier, which names
what the slat's faces do [decided]:

- `.on(ref, toward=)`: a wide face lies on `ref`, as a board's big face
  does;
- `.edge_on(ref, toward=)`: a narrow face lies on `ref`;
- `.center(pos)`: the slat's middle lies on `pos`, on that position's axis;
- `.between(start, end)`: its two ends, and nothing else.

Two of the first three, on different axes; the length runs along the third,
the axis `between()` limits, so nothing about the slat is worked out from
counting limits. `on()` and `edge_on()` take what a board's `on()` takes: a
part's face puts the slat away from that part, a box side inward, a bare
position needs `toward=`. Ends missing from `between()` default to the
enclosing scope's box; a part, a position or a contour works as an end, as
it does for a board [proposed].

```python
# a cleat: wide face on the side, narrow face under the shelf
slat("cleat", oak20x40).on(side.inner).edge_on(shelf.bottom).between(cab.front, cab.back)
# the same cleat turned: wide face under the shelf, narrow face against the side
slat("cleat", oak20x40).on(shelf.bottom).edge_on(side.inner).between(cab.front, cab.back)
# a batten standing on edge on the floor, centred on x
slat("batten", pine20x60).edge_on(floor.top).center(x).between(floor_front, floor_back)
# a slat lying flat on a frame, centred on y
slat(f"slat{i}", pine20x60).on(frame.top).center(y).between(frame.left, frame.right)
```

Errors [proposed]: fewer than two of `on()`, `edge_on()` and `center()`, or
two on one axis; an end in `between()` that is not on the length axis;
`inset()` (the section is the material's; a clearance moves the reference);
`grain()` (it runs along the length).

## Cosmetic for now

- For the time being a slat only stands in, in the preview and in Fusion,
  for the real one, which is made by hand [decided]: it has a material, a
  placement and faces, and nothing is done to it. No operations, no joins,
  no hardware [decided]; each is an error saying so [proposed]. Its ends
  are square, where `between()` puts them.
- Other parts still use it: its faces as references for `on()` and
  positions, the slat as a `between()` limit, and the checks
  (`no_interference`, `inside_box`, `inside()`) see it like any part
  [proposed].
- Nesting and the CAM plan leave slats out.

## A board in code

`Slat(Board)` [proposed]: a board whose width comes from its material as its
thickness does. Its thickness axis is the one its wide faces face along, and
its outline lies in the plane of its length and width. So faces and anchors
(named by direction once it is placed, like a board's), limits, checks, the
layout, the emitter and the preview take it unchanged. A slat overrides its
placement, fixes its grain along its length, refuses the operations, joins
and hardware it inherits, and is `kind: "slat"` in the layout.

A type of its own would need its own placement, faces and path through the
emitter and preview, or a base class under both with the `Board` annotations
sorted out. Its gain: pyright would flag an operation on a slat in the
editor, where the subclass refuses it only when the build runs [open]. The
subclass keeps the operations ready for when slats get them.

## Later

- Operations and joints on slats, all hand work: on the hand-work list
  (`cam.md`). The rule that every connector is machined from the big faces
  of both boards (`design/operations.md`) holds for boards only, so a slat's
  side of a joint may lie in a narrow face or an end, as a Domino in a
  rail's end does. End cuts at an angle are bevels (`bevels.md`). Joints
  that contacts do not cover yet: frame corners in one plane (a rail's end
  on a stile's narrow face) and a slat lying flat on a board (face to face,
  as the face-to-front screws dropped earlier) [open].
- The cut list [decided: later]: slats by material and length, the length
  being the slat's material along its grain. The layout carries what it
  needs; the cut list belongs to the committed outputs (`build-repo.md`).
- A check of each slat's length against its material's `length=`, as
  `fits_sheet` checks sheets [proposed].
