# Lipping and edge banding

Status: added by Florian 2026-10-14, worked out with him the same day;
nothing built. Needs slats (`slats.md`).

Solid wood glued along a narrow face of a board: lipping (10 mm on a 12 mm
board, say) or banding (0.5 to 2 mm). For construction they are the same
thing in different thicknesses [decided], so one operation makes both.

```python
oak = slat_material("oak")
shelf.lip(shelf.front, 10, oak)
door.lip([door.left, door.right, door.top, door.bottom], 10, oak)   # all round, butted
side.lip(side.front, 0.5, birch)                                     # banding
```

- `board.lip(what, t, material)`: a narrow face of the board, or a list of
  them, the strip's thickness, and a slat material [decided: a face and a
  thickness; the argument order, as `chamfer(what, size)`, proposed].
- A core operation, not a standard-library function [decided]: it reads the
  board's outline (the edges in a face, which corners are lipped already),
  which the public API does not offer.
- The strip is as wide as the board is thick, flush with both big faces
  [decided]; nothing about which way it lies is worked out. Trimming it
  flush after glue-up is shop work.
- The board is cut back by `t` along the edge, banding as well as lipping
  [decided], so the machine cuts it smaller and its box stays the finished
  size: `shelf.front` is still the face that gaps, hinges and limits
  measure from. The cut is named `lip_front`.
- In the cut's place goes a slat of section `t` by the board's thickness,
  `shelf_lip_front`, its grain along it, cosmetic like every slat (no
  operations, no joins).

## Edges

- `what` names narrow faces of the board's box; a big face is an error.
- A strip goes along every straight edge of the outline lying in that face,
  one strip each: on a side with a toe kick only along the front edge above
  it; with a notch in the middle of the edge, two strips. A face with no
  straight edge left in it is an error [proposed].
- Only straight edges: not along a fillet or other curve (banding could
  follow curves later), not on a bevelled or mitred edge, not on a bent board
  [Florian]. On a tilted board it works in the board's own frame.

## Corners

- Butted only, for now [decided]: where two lipped faces meet, the strip
  lipped first runs through and the other stops against it; in one call,
  the face named first runs through [proposed]. In the door above, the left
  and right strips run full height and the top and bottom lie between them.
- Mitred corners also happen [Florian]. They need end cuts on slats
  (`bevels.md`) and come with them; the board's cut-back is the same either
  way, so only the strips change.

## Order

- Before: the cut-back is an ordinary cut, so its refusals hold: an
  operation made before where the strip goes is an error.
- After: nothing may reach the strip, since it takes no operations. A cut,
  fillet or chamfer at a lipped edge, and a join at a lipped face, are
  errors; operations further in are fine, and joins and connectors keep to
  the board's material, now shorter by the lip [proposed].
- Hardware reaching into a strip is reported by `no_interference`. A hinge
  cup across a lipped door's edge, drilled through lip and board in the
  shop, needs operations on slats [open].

## Later

- Glue-up and flush trimming on the hand-work list (`cam.md`); the strips
  on the cut list with the slats (`slats.md`).
