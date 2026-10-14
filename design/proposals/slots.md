# Slots

Status: added by Florian 2026-10-14, worked out by Claude the same day;
nothing built. Depends on nothing.

An operation for slots, as `hole()` is for holes [Florian]. Today a slot is a
cut or pocket of `rect(depth=80, width=12).rounded(6)` (as in
`examples/dogbones.py`), which runs along an axis of the face and is placed
by its box at the anchor. The joints draw theirs with
`shapes.slot_shape(start, end, width)`, a line widened to a width with round
ends, in raw face coordinates and not part of the public API.

Proposed, spelled like `hole()`:

- `side.slot(8, side.inner.front(40).bottom(100),
  side.inner.front(40).bottom(300), depth=through)` is 8 wide and runs
  between the two anchors, which are the centres of its round ends, so it may
  lie at any angle on the face.
- For the common straight case, `side.slot(8, at=..., length=60,
  along="height", depth=10)` is centred on `at=` and 60 long overall, the way
  catalogues give slot lengths.
- It takes `chamfer=` and `name=` like a hole and `depth=` like a pocket (a
  number, `through` or `to()`), with a pocket's `floor` and edges. Its ends
  are arcs, so it needs no dog bones.
- A slot narrower than the smallest cutter is an error once tools are known
  (see `cam.md`). In the CAM plan a slot as wide as a cutter can be cut in
  one pass along its centre line instead of as a pocket.
