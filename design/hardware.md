# Hardware

Bought parts with their own rules: drawer slides, hinges, catches, latches,
brackets. Part of the modeling language's design; the overview is
`DESIGN.md`. Code: `lang/hardware/`, data in `lib/`.

## The pattern

- Hardware carries its own rules. A drawer slide determines the drawer box
  width, length, position and floor recess, so those numbers never appear
  in cabinet code. [decided]
- A hardware object holds the add-in's settings and is mounted with
  `scope.mount(hardware, ...)`, typed by the hardware's own `mount(self,
  scope, /, *, ...)` (`Mountable`, a ParamSpec), so the type checker checks
  the keywords and core knows nothing about hardware types.
- A mount refuses what the add-in refuses, and plans every hole and checks
  them all before it drills one (every hole checked with `Board.hole_fits`:
  on its face, clear of what was made before and of the mount's other holes,
  pilots short of the far face; `lang/hardware/common.py` holds what the
  hardware shares). A refusal changes nothing.
- It drills what the add-in drills, and places the bought part as boxes
  from one table per hardware, separate from the drilling data, measured
  from the makers' CAD models and drawings. The layout has a `hardware` list
  per module, each item with bodies made of boxes in world coordinates; the
  emitter makes each body as the union of temporary B-rep boxes in a
  component of its own, the preview as the union of box meshes. The preview
  shows or hides all hardware with one switch (Display, key `w`,
  `preview.hardware(on)`). `no_interference` checks the boxes (see
  `design/checks.md`).
- Why boxes and not the makers' CAD files: a file per variant would be some
  45 files of about 1 MB for the slides alone, each needing its frame
  measured; the language decides nothing from the detail, and the hole
  patterns were verified against every model once. [decided]
- Each add-in reads its dimensions from a Fusion-free `lib/` module the
  language reads too; their constants and dialog defaults were compared in
  Fusion against the old literals and are identical.
- Every placement is physical (numbered from the bottom or from the part's
  own left), so a module in the van's terms and a cabinet with `front=` come
  out alike.

## Drawer slides

`lang/hardware/slides.py`: `DrawerSlide(model, nl)`, the model by name
(`"Dynapro 40"`, `"Dynapro 50/70"`, `"Movento 760H"`, `"Movento 766H"`,
every nominal length) or a `lib.drawer_slides` model for one of its own.

- `slide.drawer_box(bay, front=face.back, side_thickness=, height=)` is the
  drawer box: the sides' inner faces 21 mm from the carcass sides (inner
  width LW - 42 in both catalogs, sides up to 16 mm), NL - 10 long, with the
  bottom panel's underside above the bay bottom by `slide.bottom_height`
  (Blum 28.5, "min. 28.5" with the screw row at 38; Grass 28, 10 below the
  screw row as the Grass sheet says, kept although Häfele's Dynapro models
  put the drawer member's top at 28.5 too [decided]) and the sides hanging
  below it by `slide.recess` (Grass 10-13, Blum 12-15, default the middle),
  so the sides' lower edge is `slide.side_lift` above the bay bottom; it
  refuses a bay shallower than NL + 3.
- `slide.machine_box(sides=(l, r), front=f, back=k, floor=floor)` machines
  the drawer box: a cut-out at each end of the front board for the couplings
  and one at each end of the back board for the rear hooks, from the side's
  inner face (Grass 69 and 35 mm wide, Blum 75 and 75) and from the board's
  lower edge up to the floor's underside; and the holes for each hook into
  the back board's rear face (`hook_hole`, diameter and depth): Grass three
  pre-drill holes for the hook's screws, default 2 x 8, 42 mm from the
  side's inner face at 15 and 47 above the floor's underside and 10 mm from
  the inner face at 47; Blum one 6 x 10 hole for the hook's pin, 7 from the
  inner face at 11 above the floor's underside [decided].
  - The depth may be `through` (`hook_hole=(2, through)`) [decided, for
    either family]: the holes then go all the way through the back board,
    drilled from its inner face, so the back board needs nothing from its
    rear face; fixed-depth holes stay in the rear face, where the hook sits.
  - A hook hole that would run into the floor, where the floor goes into the
    back board, or into the groove it lies in there (its clearance
    included), is an error naming the back board and the hole, and nothing
    is cut [decided]: with Blum the floor does not go into the back, as its
    6 mm hole 11 above the floor's underside meets any floor of 8 mm and
    more there. Grass's holes (15 and 47 above) clear a floor up to 14
    thick.
  - Cut-outs are named `coupling_left`, `hook_right` and so on, the hook
    holes `hook_left_a`.... Blum's TIP-ON BLUMOTION variant (a 125 mm back
    cut-out) is not covered.
- `drawer.mount(slide, sides=(left, right), front=face.back)` pre-drills the
  carcass sides: a row 38 mm above the bay bottom at the hole positions the
  add-in uses, measured from the runner's front, into each side's face
  toward the bay's middle (a partition between two bays takes a drawer on
  either face), holes `slide_<drawer>_a`...; a drawer runs on one pair, a
  second mount is an error.
- The runner pair is placed as boxes [decided], one body per runner, named
  by the drawer's own left and right. Five boxes per runner (`RunnerShape`):
  the cabinet rail's flange against the carcass side and its base with the
  carriage, the drawer member whose top carries the floor, the coupling
  under the floor's front end, as wide as the front board's cut-out (the
  space reserved for it), and the rear hook behind the drawer box. Each
  family keeps one cross-section across all lengths and load classes; the
  lengths follow from NL. The real cabinet rail ends 2/3 to 9/10 of the way
  back, irregularly by model and length (Dynapro NL 300/450/600 at
  250/285/456, Movento 760H NL 250/450/600 at 232/304/404), so the boxes run
  it the whole length. Checked: with the drawer box machined, the runner
  boxes overlap none of its parts nor the carcass, and without the cut-outs
  the couplings hit the front board and the drawer members the back board.
- Sources: Häfele's CAD box (`teccad.hafele.com`,
  `ccHandler.aspx?CadBox=2&CssClass=topco&Mandant=HDE&ArtikelNr=...`;
  Dynapro 433.19.600-613 and 433.20.615-635, Movento 760H 433.24.010-024,
  766H 433.24.2xx, Movento coupling 433.24.980/981); Grass "Dynapro
  Planungshinweise" 113378 12/2021 (the definitive sheet: installation
  dimensions, fastening positions and assembly steps); Blum TD-132/1
  DE/06.22 p.5; the Blum catalogue 2024/2025 p.413 (Movento planning and
  drawer assembly). The hole patterns in `lib/drawer_slides.py` were
  verified against every model (the 24 pre-drill holes of the example
  coincided with the Dynapro model's screw holes).

## Concealed hinges

`lang/hardware/hinges.py`: `ConcealedHinge(model, count=2, end=60,
pilot=(3.175, 3))` with the models of `lib/concealed_hinges.py` (Blum CLIP
top 110 for thin doors, +0 and +3).

- `cab.mount(hinge, door=door, carcass=left)` (`carcass=` a board, or the
  face the plates go on, `wall.left`) hinges a door on a carcass board
  standing square to it (a side, a partition or, for a flap, the top or
  bottom) and drills what concealed_hinge_native drills: per hinge two
  10 x 5 holes in the door's inner face, 32 apart along the edge, in a row
  27 mm (+0) or 30 mm (+3) from the carcass board's face toward the door's
  middle, whatever the overlay or gap; and two pre-drill holes for the
  mounting plate's screws in that face, 32 apart, 38.5 mm behind the door's
  inner face.
- The hinges' centres lie `end` from the ends of the door's edge (the add-in
  makes two; `count=` spreads more evenly between).
- Refused: `end` under 27 (the add-in dialog's minimum [decided]), hinges
  closer than their mounting plates are long, 56.2 mm [decided] (the
  add-in's 42 is where their hole pairs meet), holes that do not fit on
  their face. The hinge dictates no overlay or door size, since the add-in
  knows none.
- Each hinge is a body of four boxes, cup, arm, clip and mounting plate
  (`HINGE_SHAPES`), measured on Häfele's CAD models of the hinge 342.46.681
  and the plates 342.20.800 (0 mm, 8.5 high) and 342.20.830 (3 mm; the +3
  model is the hinge on it), named `hinge_1`... under `<door>_hinges`.
- Example: `examples/hinged_door.py`, a wall cabinet with an overlay door.

## Hatch hinges

`lang/hardware/hatch_hinges.py`: `HatchHinge("Free space 1.11",
opening=107, carcass_depth=12, pilot=(2, 4))` with the specs of
`lib/hatch_hinges.py` (or a `lib.hatch_hinges` `HingeSpec`, which takes
more), placed as `<hatch>_hinges`, holes `hinge_<hatch>_a`... and
`hinge_<side>_a`....

- `cab.mount(hinge, hatch=hatch, sides=(left, right), top=top)` drills what
  hatch_hinge drills, from the underside of the carcass top (`top=` the
  board or the height of its underside): into each side panel's inner face
  three 5 mm holes 37 behind its front edge, 102, 134 and 166 below that
  reference; into the closed hatch's inner face each mounting plate's pilot
  holes, 25 in from the side panel, 12 and 76 below.
- It checks what the add-in checks: the hatch 16 to 28 thick and closed (0
  to 2 mm in front of the carcass), flush front edges, the overlap A (how far
  the hatch top reaches above the reference) at most A_max for the thickness
  (24.5 at 16 down to 21 at 28; 37 with `opening=90`), checked and never
  chosen, holes and plate on their boards, depths less than the boards, no
  part containing one of the add-in's probe points; and that the two hinges'
  mounting plates do not meet.
- `max_overlap(t)`, `highest_hatch_top(top, t)` and `lowest(top)` (169
  below the reference) give the cabinet what the hinge dictates.
- One body per hinge, named by the hatch's own left and right, of four boxes
  (plate, arm, upper and lower housing) measured on Häfele's CAD model of
  372.27.300.
- Example: `examples/hatch.py`, a wall cabinet with a lift-up hatch, its
  shelf at `hinge.lowest(top)`.

## Ball catches

`lang/hardware/ball_catches.py`: Ganter GN 450 catches holding an
inspection hatch in its opening, as ball_catch drills them.

- The opening is a named through cut with its rounded corners in the shape;
  `catch.hatch("hatch", panel.opening)` is the hatch, the opening shrunk by
  the slot (`catch.gap`, 3 mm, within 2.5 to 3.5), offset exactly on its
  lines and arcs, flush with the panel.
- `scope.mount(catch, opening=panel.opening, edge=panel.opening.left,
  hatch=hatch)` (the hatch's outline is `lang.core.cutouts.inset`; holes
  `catch_<hatch>_<n>` and `catch_<panel>_<n>`) drills
  per catch a pilot hole for the holder's screw into the panel, 8.4 mm
  outside the opening's contour, and one for the ball's screw into the
  hatch, 9.4 mm inside it, Ø2 x 4 by default, from the face that is not the
  show face unless `face=` names one.
- `count=` (4) catches go on the named edge and the one across from it, the
  extra one of an odd count on the named edge; on each the outer ones sit
  `end=` (40) from the ends of its straight part, the arc tangent points.
  They are numbered along each edge as the other hardware is
  (`common.numbering`) [decided]. `BallCatch(at=[...])` takes points
  instead.
- Checked as in the add-in: the hatch under every ball, the slot within
  range, 14 mm to the end of a straight edge and 28 between catches,
  mounting surface for holder and ball part, pilots shallower than the
  boards, catches whose holes meet.
- One body per catch (holder, its stop webs down the opening's edge into the
  slot, its jaw over the slot, ball part; `CATCH_SHAPES`, measured on
  Ganter's CAD model).
- Example: `examples/inspection_hatch.py`, a floor panel on battens with a
  rounded opening and its hatch.

## Door latches

`lang/hardware/latches.py`: `DoorLatch(model, count=1, end=100,
pilot=(3.175, 3))`, placed as `<door>_latches`, with door_latch_native's
latches `"Everlock"`, `"Pull Lock 44"` and `"LL-66"` (Sugatsune),
`cab.mount(latch, door=door, carcass=top)`.

- The body goes on the door's inner face, the strike on the carcass face
  (the carcass board's big face toward the door's middle, or the face given,
  `carcass=shelf.top`), beside the door's edge on that side; holes are
  measured from the carcass face and the door's inner face as the add-in
  measures from its two edges, so inset and overlay doors get the same
  latch:
  - Everlock: a 25 mm finger hole through the door 30 below [decided: 25,
    for the lock without its aluminium inset, which needs 30] and four
    pilots 26 to either side at 26 and 42, strike pair 14 to either side at
    25;
  - Pull Lock: a 38.1 hole through 34 below and a 48 counterbore from the
    inner face leaving 10 at the front (none on a door of 10 or less),
    keeper 9.5 at 29 behind the door's front face, where the lock sits
    [decided; the add-in was corrected to match]; a door thicker than 20.4
    mm is refused (the pawl, swinging behind the housing from 20.4 behind
    the front, would lie in the door; `LatchShape.max_door`) [decided];
  - LL-66: two pilots 28 to either side at 10, counter plate 10 at 24.
- One latch in the middle of the edge, more from `end=` from its ends.
  Refused like the add-in: a pilot not below the narrowest pilot spacing, an
  edge no longer than twice `end=`, a carcass board parallel to the door,
  holes that do not fit on their face, latches whose holes meet.
- Each latch with its strike is one body (they interlock when closed) of
  boxes (`LATCH_SHAPES`): Everlock from the maker's installation drawing,
  without the aluminium inset; the Pull Lock from its drawing (bezel 44,
  panels 1 to 10 thick, which the counterbore leaves), its parts in the
  door's holes as squares inside them and its lock measured from the door's
  front, the keeper too; the LL-66 from Sugatsune's CAD model. `latch.reach`
  is how far the part behind the door's front reaches from the carcass face
  (Everlock 60, Pull Lock 50.9, LL-66 24.6), which a drawer box behind a
  latched face stays clear of.
- Example: `examples/door_latch.py`, an inset door with two pull locks and
  two latched drawers.

## Sliding brackets

`lang/hardware/sliding_brackets.py`, data in `lib/sliding_brackets.py`; no
add-in yet. Häfele Pacofix, the same parts as Keku AS (Häfele: they "click
with all Keku plastic fittings"), holding a removable panel on frame boards
standing square to it: `cab.mount(SlidingBracket(), panel=cover,
frame=[left, right])`, like the hinges.

- The frame part goes on each frame board's inner face (toward the panel's
  middle, or the face named, `frame=[wall.left]`), the panel part (PF) on
  the panel's back face (toward the frame boards), its tongue under the
  frame part's hook; the panel comes off square to itself.
- Two frame parts, both on the frame board's inner face, are the models:
  - `"Pacofix PF-L-R"`, the bent one, the default [decided: Florian uses
    it]: the hook is bent back over the frame part's own plate, which
    reaches from the panel's back face 33 back. The frame holes lie 8 behind
    the panel's back face, at the plate's front end, whatever the gap
    [decided]; the panel holes 19 out from the frame board's face, since the
    tongue lies on the 4 mm plate. The panel sits on the frame board's edge
    or up to 3 mm in front of it [decided], the plate then hanging over the
    edge by the gap and the frame holes 8 - gap from it, or the frame boards
    reach past its back face (a panel set in between). The frame board must
    reach 29 behind the panel (the plate's flat underside; its last 4 mm are
    rounded).
  - `"Pacofix PF-L"`, the straight one: the hook points from the plate
    toward the panel, the tongue lies on the frame board. Frame holes 37
    behind the panel's back face (the System 32 line), panel holes 15 out
    from the frame board's face. The gap is read from the model, never
    given: the frame holes depend on the panel's back face only, so a gap
    moves them toward the frame board's edge (37 - gap, up to 29, where the
    plate begins); the frame board must reach 45 behind the panel.
- Each pair of holes is 32 apart along the edge. A panel set in between may
  stop up to 3 mm short of where the panel part's plate begins (3 mm short
  of the frame board's face for the PF-L, 7 for the PF-L-R), the plate
  hanging over its edge [decided].
- `count=` brackets (2) per frame board, the outer ones `end=` (50
  [decided]) from the ends of the stretch panel and board share, or `at=`
  positions along the edge, the same on every frame board; numbered from the
  bottom or from the panel's own left.
- Holes per part, because Euro screws usually go only into the frame board:
  `frame_hole=` and `panel_hole=` each `"pilot"` (Ø2 x 6, the default, for
  chipboard screws), `"euro"` (Ø5 x 11, a 6.3 x 13.5 Euro screw through the
  4 mm plate, but never deeper than the board less 2 mm, 10 on a 12 mm
  board [decided]; a board under 11.5 then takes a shorter screw) or
  (diameter, depth), which stays as given.
- Refused before anything is drilled: a frame board parallel to the panel, a
  gap the frame part does not allow, a frame board ending before the plate
  does, a panel too far short of the plate's start, plates off their boards
  or over pockets (a hole under a plate is fine; the part over a gap hangs
  free), brackets closer than a plate's 48, holes off their face or in
  another hole, holes as deep as the board is thick, `end` under 24.
- The makers' rules are advice for the build, not checks, and nothing about
  them appears in the build's output [decided]: Keku asks for at most 600
  between brackets and at least four per panel (two frame boards with two
  each); Häfele rules out hanging loads, such as a panel hung overhead, and
  gives 20 kg per pair vertically, 30 kg lying horizontally.
- Each latched pair is one body of four boxes (`BRACKET_SHAPES`: frame
  plate, hook, panel plate, tongue), `bracket_1`... under
  `<panel>_brackets`, numbered on through the frame boards in the order
  `frame=` names them; holes `bracket_<other>_<n>a/b` with the same numbers.
- Articles, for chipboard / Euro screws: panel part PF 262.50.359 / .358,
  frame part PF-L-R 262.50.390 / .391, PF-L 262.50.368 / .377; sets
  262.50.380 (PF with PF-L-R) and 262.50.313 (PF with PF-L). Measured on
  Häfele's CAD models of 262.50.359, 262.50.390 and 262.50.368, fitted
  together latched. PF-L: the tongue's tip against the plate, the hook's
  tapered sides 0.1 to 0.2 mm clear of the tongue's tapered channel, the
  lip's back flank on the tongue's ramp; that confirms the 37 of Häfele's
  mounting drawing and the 15. PF-L-R: the lip's back flank lies on the ramp
  all along with the panel's back face 8.15 to 8.2 in front of the holes (8
  taken, the plate's front end), the hook's sides 0.2 clear, its roof on the
  channel's floor, the tongue's walls as high as the roof; the tongue's
  square bottom corner meets the hook's rounded closed end there by about
  1 mm in the model.
- Left out for now: snapping the frame holes to an existing System 32 row,
  Häfele's 1.5 mm spacer plate under the panel part (the PF-L's frame holes
  then 38.5), the hang-in fittings for panels parallel to the frame (SF/EH).
- Example: `examples/removable_panels.py`, a seat base with a cover on its
  sides' edges (PF-L-R) and a rear panel set in between them (PF-L, Euro
  screws on the sides' System 32 line).
