# Slots

Status: added by Florian 2026-10-14, worked out by Claude the same day and
reviewed with Florian (his answers are marked [decided]); nothing built.
Depends on nothing.

An operation for slots, as `hole()` is for holes [Florian]: vents in rows,
slotted screw holes for adjustable mounting, and pass-throughs for straps
and cables [decided]. Today a slot is a cut or pocket of `rect(depth=80,
width=12).rounded(6)` (as in `examples/dogbones.py`), which runs along an
axis of the face and is placed by its box at the anchor. The joints draw
theirs with `shapes.slot_shape(start, end, width)`, a line widened to a
width with round ends, in raw face coordinates and not part of the public
API.

## Spelling

Two forms, both measured between the centres of the round ends [decided]:

- `side.slot(8, side.inner.front(40).bottom(100),
  side.inner.front(40).bottom(300), depth=through)` is 8 wide and runs
  between the two anchors, which are the centres of its round ends, so it may
  lie at any angle on the face. A slot between two edges needs no
  arithmetic: `side.slot(8, side.inner.bottom(z).front(40),
  side.inner.bottom(z).back(40), depth=through)`.
- `side.slot(8, at=..., centres=52, along="height", depth=10)` is centred on
  `at=`, as a hole is [decided], with its end centres 52 apart, so 60 long
  overall. The keyword says centre to centre because catalogues give overall
  lengths and `length=60` would read as one [decided]. `at=` defaults to the
  show face's centre, as for a hole. `along=` takes what `grain()` takes, an
  extent name or a side, direction or face (`along=cab.top`) [decided]; one
  that is not in the face's plane is an error.

```python
for z in spread(back.bottom + 60, back.top - 60, pitch=20):     # vents, centred across the back
    back.slot(6, at=back.inner.bottom(z), centres=120, along="width", depth=through)

a, b = side.inner.front(40).bottom(100), side.inner.front(40).bottom(140)
side.slot(12, a, b, depth=4, name="mount_head")                 # a stepped mounting slot:
side.slot(6, a, b, depth=through, name="mount")                 # two calls, the same anchors
```

- It takes `chamfer=` and `name=` like a hole and `depth=` like a pocket (a
  number, `through` or `to()`), with a pocket's `floor` and edges (the edges
  are its bounding box, at an angle the arcs' extremes). Its ends are arcs,
  so it needs no dog bones; where it meets another pocket or slot,
  `dogbones()` finds the corners as for any pocket.
- Stepped slots, for a screw head, are two calls with the same anchors, as
  above; no `counterbore=` [decided], and `hole()` has none either.
- Typed as two overloads [proposed], `slot(width, start, end, /, *, depth,
  name=None, chamfer=0.0)` and `slot(width, *, at=None, centres, along,
  depth, name=None, chamfer=0.0)`, so mixing them is a type error, and a
  `LangError` at run time; lines for both in `tests/typing_checks.py`.
- Curved slots are left out [proposed].

## Rules

- Big faces only [decided]: an anchor on a narrow face is an error; a slot
  there stays `pocket()` with a rounded rectangle.
- Both end centres lie on the board's outline, as a hole's centre must
  [decided]: an end off the board is refused, and a slot open at the edge is
  a `cut()` of a rounded rectangle, which changes the outline. An end centre
  in a pocket made before is allowed, unlike a hole's, so the narrow part of
  a stepped slot can be cut through the wide one. As with a hole, the rest of
  the slot may run over the edge and cuts what it reaches; through the
  board, that leaves the outline as it was, as a through hole does
  [proposed].
- Refused besides [proposed]: a width under 0.01 mm; `centres=` not
  positive, or two anchors on one point (a round hole is `hole()`); anchors
  on two faces or on another part; and whatever a pocket is refused for (off
  the board, a through slot splitting the board, a slot wholly in what was
  cut from its face before). Two anchors on one axis but for float noise
  (within 1e-9) are put onto it, so a straight slot has straight sides.
- Errors call it a slot, not a pocket [proposed].
- Operation names that are attributes of a board (`slot`, `hole`, `front`,
  `outline`, ...) are refused, for every operation [decided]: such an
  operation could only be reached as `side.op("slot")`, never as
  `side.slot`. Today they are accepted without a word. The cut named "slot"
  in `examples/dogbones.py` gets another name.

## Layout

- A slot is a pocket that keeps its centre line and width, and the layout
  carries them now [decided]: the pocket gains `slot: {start, end, width}`
  (or null), and the layout goes to version 4, which the emitter's plan and
  the viewer repeat. The preview and the emitter draw it as a pocket, its
  ends recovered as arcs; a reader of the layout, and later the CAM plan,
  sees which pockets are slots.
- The joints' Domino slots, Clamex P-10 access slots and Cabineo reliefs go
  through the same helper instead of `slot_shape()` plus `add_pocket()`, so
  they carry their centre lines too, their geometry unchanged [proposed].

## Machining

- Until the CAM plan exists, Auto Setup cuts a slot as a pocket and wants a
  tool at least 0.1 mm narrower than the slot (`TOOL_CLEARANCE` in
  `lib/auto_setup/rules.py`), so a slot is made at least 0.1 mm wider than
  the cutter that clears it. That is stated here and in `design/operations.md`
  only; nothing checks it, since the language knows no tools yet [decided].
- With tools known (`cam.md`), a slot narrower than the smallest cutter is an
  error, by the check every pocket and cut gets (`design/checks.md`), and a
  slot as wide as a cutter can be cut in one pass along its centre line
  (Fusion's 2D Slot) instead of as a pocket; the 0.1 mm then no longer
  applies.

## To build

- `Board.slot()` and the shared helper in `lang/core/part.py`; the name
  check; layout version 4.
- `design/operations.md` (the operation list, the sentence calling a rounded
  rectangle a slot, the 0.1 mm) and `design/api.md` (the ordered modifiers).
- `examples/operations.py` gets straight, angled, stepped and chamfered
  slots; `examples/dogbones.py` writes its slot with `slot()`.
- Fuzzing: `tests/fuzz/boards.py` draws slots, and a Fusion batch with angled
  and chamfered ones. Angled slots have never been compiled in Fusion; the
  plan recovers their arcs (`tests/test_arcs.py`), but every slot built so far
  (the Dominos) runs along an axis.
