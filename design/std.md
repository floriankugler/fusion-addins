# The standard library

Building blocks above the core: what a build file would write again and
again, written once on the public API. Part of the modeling language's
design; the overview is `DESIGN.md`. Code: `lang/std/`. Tests:
`tests/test_std.py`, `tests/fuzz/carcasses.py`. Proposed in
`design/proposals/standard-library.md`, which keeps what is still open.

## The rule

- `lang/std` is written as a build file is: `from lang import ...` and
  nothing from `lang.core`, `lang.joints` or `lang.hardware`
  [decided]. A block that needs an internal shows something the core
  lacks, and the core grows for it (`Joint` is exported from `lang` for
  the blocks' `joins=`). `tests/test_std.py` reads every module's imports
  and holds them to the rule.
- Each block comes with a test that compares it, board for board and
  operation for operation, with the lines it replaces, and with an example
  that uses it. The blocks add no geometry of their own: joints and
  hardware stay in the language, where they work out geometry from
  catalogue data.
- Cabinet types for one build stay in that build's repo
  (`proposals/build-repo.md`); `lang/std` holds what is reused across
  builds. Build files use it as `from lang.std import carcass, drawer_box`.

## Carcass

`carcass(scope, material, *, back=None, front=None, toekick=None, joins=None,
back_joins=None)` is the carcass every cabinet in `examples/` starts with,
the first block because of that [decided by Florian, 2026-10-15,
syntax.md item 2]:

```python
left, right, bottom, top, back = carcass(cab, ply15, back=ply9, toekick=(60, 100), joins=cabineo(count=3))
left, right, bottom, top = carcass(cab, ply18, front=cab.front.into(ply12.thickness))   # no back
```

- The boards are made in that order and named `left`, `right`, `bottom`,
  `top` and `back`: the sides `.on()` the scope's left and right sides, the
  bottom and the top on its bottom and top `.between(left, right)`, the
  back on its back `.between(left, right, bottom, top)`, of `material` but
  for the back, which is of `back`; `back=None` makes no back, and the
  call then returns the four boards (`OpenCarcass`) instead of the five
  (`Carcass`), both NamedTuples, so unpacking and `c.left` both work.
- `front=` limits the sides, the bottom and the top at the front: a
  position or side (`cab.front.into(ply12.thickness)`, the carcass behind a
  door), a part's face, or a board standing in front (a hatch:
  `front=hatch`). Without it the scope's box limits them.
- `toekick=(depth, height)` notches both sides with `rect(depth=, height=)`
  at `side.outer.bottom.front`, named `toekick`, before the bottom is made,
  and puts the bottom `.on(left.toekick.top, toward=scope.top)`.
- `joins` joins the bottom, then the top, to the sides (`cabineo(count=2)`
  unless given); `back_joins` the back to all four (`domino("4x20", count=2)`
  unless given); `back_joins=` without a back is an error. The joint
  objects are made inside the call, not as default arguments.
- Not covered, and written out by hand as before: a top overhanging the
  sides (`examples/slats.py`), shelves on tenons (`examples/shelf.py`), a
  bottom raised without a notch, boards of several materials. A refused
  join raises out of the call with the boards made so far in the scope, as
  the same lines by hand would.
- `examples/drawer_cabinet.py`, `door_latch.py`, `cutouts.py`, `hatch.py`,
  `hinged_door.py` and `removable_panels.py` use it. Their layouts are the
  same as before, byte for byte where the example made its boards and
  joins in the carcass's order, and the same up to the order of the parts
  and of the sides' operations where it did not (`cutouts.py` and
  `hatch.py` joined a shelf before the back, `removable_panels.py` and
  `hatch.py` made the top before the bottom).

## Drawer box

`drawer_box(scope, bay, slide, *, front, height, material, floor, corners,
floor_joint, carcass)` is the drawer box behind a face, hiding the drawer
slide's three calls, which stay as they are in the core [decided by
Florian, 2026-10-15, syntax.md item 3]:

```python
with scope(f"drawer{i}", bay) as d:
    face = board("face", ply15).on(bay.front).between(panel).inset(GAP / 2)
    drawer_box(d, bay, slide, front=face.back, height=bay.height - 30, material=ply12, floor=ply9,
               corners=box_joint(7, margin=2, clearance=(0.1, 0.1)), floor_joint=groove(5, clearance=(0.5, 0.5)),
               carcass=(left, right))
```

- Called inside the drawer's scope, which the build makes with its face,
  since faces differ (a share of the cabinet front, an inset front). The
  slide sizes the box (`slide.drawer_box(bay, front=, side_thickness=,
  height=)`); `left` and `right` run its full length, `front` and `back`
  stand between them, the `floor` lies `slide.recess` above the box's
  bottom between all four; the slide machines the box
  (`slide.machine_box`) and is mounted on the scope with its runners on the
  two `carcass` boards (`scope.mount(slide, sides=carcass, front=front)`),
  which it pre-drills.
- `corners` joins the front and the back to the sides (`box_joint(...)`,
  or None for corners left to the shop); `floor_joint` joins the floor to
  all four (`groove(...)`, or None for a floor resting on the runners).
  Both are said at every call, since Florian's drawers are box-jointed
  with grooved floors and an example's may not be; no defaults
  (syntax.md item 16).
- It returns `DrawerBox(left, right, front, back, floor, box)`.
- `examples/drawer_cabinet.py` and `door_latch.py` use it, with layouts the
  same as before byte for byte.

## Tests

`tests/test_std.py`: the import rule; each block against the same lines
by hand (`carcass()` with the drawer cabinet's and the hinged cabinet's
carcass, `drawer_box()` with the drawer cabinet's drawer), the defaults,
`back=None`, `front=` as a position and as a board, the toe kick, the
drawer box without corner and floor joints. `tests/fuzz/carcasses.py`
draws random carcasses (sizes, thicknesses, a front limit of each kind, a
toe kick, joint counts) and builds each facing two ways at two places: the
boards share no material and lie inside the box, the bottom lies on the
toe kick, the front limit holds, the back lies on the other four, and the
result measured from the cabinet's own sides is the same both ways, a
refusal too.
