# Slats and lips

Solid wood: slats, and the lips and banding glued along boards' edges. Part
of the modeling language's design; the overview is `DESIGN.md`. Code:
`lang/core/material.py`, `part.py` (`Slat`, `Board.lip`). Example:
`examples/slats.py`.

## Materials

- Sheet stock is a `sheet_material()`, solid wood a `slat_material()`
  [decided]:

  ```python
  ply15 = sheet_material("birch", t=15, size=(2500, 1250))
  oak = slat_material("oak")
  ```

  A sheet material is bought by thickness, so a board's thickness comes
  from it: `ply15.thickness`, as `board.thickness` (`t=` is only the
  constructor's keyword, as it is `lip()`'s argument) [decided by Florian,
  2026-10-15, syntax.md item 11]; `size=` is the sheet `fits_sheet` checks
  against. A slat
  material is only a species [decided]: solid wood is ripped to whatever a
  part needs, so a slat's section is the slat's own and a lip's thickness
  the lip's, as a board's shape is the board's. Solid wood always has
  grain. The types are `SheetMaterial` and `SlatMaterial`; a part's
  attribute is `.material` either way.
- `board()` with a slat material and `slat()` with a sheet material are
  errors, for the type checker and when the build runs.

## Slats

A **slat** is solid wood defined by cross-section and length, with no
canonical top or bottom [decided]. Board versus slat is a matter of stock
form, not species: a glued-up solid wood panel is a board, and so is a
batten cut from plywood to follow the floor profile.

- `slat(name, material, section=(w, h))` [decided]. The sizes come in
  either order: the larger is the width of the slat's wide faces, the
  smaller that of its narrow faces; which way it lies is said by its
  placement.
- Each of the slat's three axes is placed by its own modifier, which names
  what the slat's faces do [decided]:
  - `.on(ref, toward=)`: a wide face lies on `ref`, as a board's big face
    does;
  - `.edge_on(ref, toward=)`: a narrow face lies on `ref`;
  - `.center(pos)`: its middle lies on `pos`, on that position's axis (the
    width when `on()` is given, else the thickness);
  - `.between(start, end)`: its two ends, and nothing else.

  Two of the first three, on different axes; the length runs along the
  third, the axis `between()` limits, so nothing is worked out from
  counting limits. `on()` and `edge_on()` take what a board's `on()` takes:
  a part's face puts the slat away from that part, a box side inward, a
  bare position needs `toward=`. Ends work as a board's limits on one axis:
  missing ones come from the scope's box, a single one runs to the far side
  of the room (at its middle it is an error), and a part, a position or a
  contour across the slat is an end.
- Errors: fewer than two of `on()`, `edge_on()` and `center()`, or all
  three, or two on one axis; an end off the length's axis; a contour along
  the length or in the slat's own plane (a slat's section is the same all
  along); `inset()` (the section is the slat's; a clearance moves the
  reference, `left.gap(2)`); `grain()` (it runs along the length).

```python
# a cleat: wide face on the side, narrow face under the shelf
slat("cleat", oak, section=(20, 40)).on(side.inner).edge_on(shelf.bottom).between(cab.front, cab.back)
# the same cleat turned: wide face under the shelf, narrow face against the side
slat("cleat", oak, section=(20, 40)).on(shelf.bottom).edge_on(side.inner).between(cab.front, cab.back)
# a batten standing on edge on the floor, centred on x
slat("batten", pine, section=(20, 60)).edge_on(floor.top).center(x).between(floor_front, floor_back)
# a slat lying flat on a frame, centred on y
slat(f"slat{i}", pine, section=(20, 60)).on(frame.top).center(y).between(frame.left, frame.right)
```

### Cosmetic for now

- A slat only stands in, in the preview and in Fusion, for the real one,
  which is made by hand [decided]: it has a material, a placement and
  faces, and nothing is done to it. Operations, lips, joins (either way)
  and hardware mounted on it are errors saying so [decided]. Its ends are
  square.
- Other parts use it: its faces as references, the slat as a `between()`
  limit on either of its cross axes (a board between two slats meets their
  wide or their narrow faces), and the checks see it like any part
  (`no_interference`, `inside_box`, `inside()`); `fits_sheet` passes it, a
  slat being on no sheet.
- Nesting leaves slats out: the layout calls a part `kind: "slat"` with its
  `section`, the compiled body's `lang`/`part` attribute says `kind`, and
  Multi Arrange's compiled parts skip slats. Its label is its species
  (`oak`), so the preview colours all slats and lips of a species alike.

### In code

`Slat(Board)`: a board whose thickness and width come from its section.
Its thickness axis is the one its wide faces face along, and its outline
lies in the plane of its length and width, so faces and anchors (named by
direction, `inner` and `outer` the wide faces), limits, checks, the layout,
the emitter and the preview treat it as a board. It overrides its
placement, fixes its grain along its length and refuses what it inherits
through one hook every operation and join calls first (`_operable`).
`Scope.mount` refuses a slat among the hardware's arguments. The type
checker does not see the refusals, which come when the build runs [open:
a base class under both would let pyright flag an operation on a slat].

## Lips and banding

Solid wood glued along a narrow face of a board: lipping (10 mm on a 12 mm
board, say) or banding (0.5 to 2 mm). For construction they are the same
thing in different thicknesses [decided], so one operation makes both, in
the core [decided].

```python
shelf.lip(shelf.front, 10, oak)
door.lip([door.left, door.right, door.top, door.bottom], 10, oak)   # all round, butted
side.lip(side.front, 0.5, oak)                                       # banding
```

- `board.lip(what, t, material)`: a narrow face of the board, or a list of
  them, the strip's thickness, and a slat material [decided].
- The strip is as wide as the board is thick, flush with both big faces;
  nothing about which way it lies is worked out [decided].
- The board is cut back by `t` along the face, banding too [decided], so
  the machine cuts it smaller and its box stays the finished size:
  `shelf.front` is still the face that gaps, hinges and limits measure
  from. The cut is named `lip_front`.
- In its place goes a slat of section `t` by the board's thickness,
  `shelf_lip_front`, in the board's scope wherever `lip()` is called, its
  faces named in that scope's frame, its grain along it.
- A strip goes along every straight edge of the outline lying in the face,
  one each (`_1`, `_2`... when there are several): along a side's front
  edge above its toe kick only, two strips round a notch in the middle.
  Only straight edges [Florian]: an edge running into an arc as the
  emitter finds them (a rounded corner, a round outline) is an error; a
  corner at any angle is fine. Not yet on bevelled or mitred edges or bent
  boards, which do not exist yet.
- Corners are butted [decided]: where two lipped faces meet, the strip
  lipped first runs through and the other stops against it, so in one
  call the face named first runs through.
- Errors when lipping: a big face; a face named twice or lipped already;
  not a slat material; `t` under 0.01 mm, too thin for its cut to survive
  cleaning, or taking all of the board; no straight edge left in the face;
  a joint's material past the face (tenons, fingers); what was made before
  where the strip goes (an operation in the cut-back or into the face, a
  through cut or opening there, a chamfer along the face's edges or the
  outline). A refused `lip()` changes nothing: neither the board nor its
  scope (the strips it made are taken back).
- Nothing after it may reach the strip, which takes no operations: a cut,
  fillet or outline change that reaches into a strip or takes the board
  away from behind one, an operation whose footprint crosses into it or
  that goes into the lipped face, a chamfer along a lipped edge, the
  outline or the lip's cut, are errors. Operations further in are fine,
  and joins keep to the board's material, now shorter by the lip: a lipped
  side still takes a shelf on its inner face, its connectors behind the
  lip.
- Hardware whose holes would reach a strip is refused with them, so a
  hinge cup across a lipped door's edge (drilled through lip and board in
  the shop) waits for operations on slats [open].
- Glue-up and flush trimming will go on the hand-work list (see
  `design/proposals/cam.md`).

## Tests

`tests/test_slats.py` and `tests/test_lips.py`; the fuzz tests
`tests/fuzz/slats.py` (slats placed at random in modules and cabinets,
built as written and in another of the 48 world frames, which must agree
with each other and with placement worked out again from the case) and
`tests/fuzz/lips.py` (lips on `boards.py`'s random boards: the board and
its strips are the board as it was, sharing no material, each strip in its
band and flush, one per straight edge; a refusal changes nothing; the same
lying, standing or upright). Verified in Fusion on `examples/slats.py`
(2026-10-15): 33 bodies, the slats' volumes exact and the boards' within
0.005 % of the preview's (its polygons for the Cabineo holes' circles),
every body's `kind` attribute right, and Multi Arrange's compiled parts the
six boards only.
