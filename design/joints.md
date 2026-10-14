# Joints

How boards are joined. Part of the modeling language's design; the overview
is `DESIGN.md`. Code: `lang/core/contact.py`, `crossing.py`, `lang/joints/`.
Hardware is in `design/hardware.md`.

## Joints and the add-ins

- The joint and hardware vocabulary is this repo's add-ins: tenons with dog
  bones, box joints, Domino, Clamex, Cabineo, screws, concealed hinges,
  hatch hinges, drawer slides, ball catches, door latches, face cutouts.
- Each add-in is split into layers: settings (what the dialog collects),
  layout (Fusion-free code that turns settings into holes and slots at
  positions and depths on a face) and emitter (the Fusion features). The
  dimensions live in Fusion-free `lib/` modules that the add-ins and the
  language both read (`lib/connector_data.py`, `lib/domino.py`,
  `lib/drawer_slides.py`, `lib/stations.py` and the hardware's).
- The language does not call the add-ins. It works out the joints itself
  and hands the generic emitter plain operations, which is also what Auto
  Setup recognises. Every joint is verified in Fusion against its add-in on
  the same boards.
- Joinery rules are dropped [decided]: which connector goes where is hard to
  formalize, so joints are stated one call per board. (Polyboard-style rule
  lists, first match wins, are not pursued.)

## Contacts and crossings

- A joint is a relation between two parts along the rectangle where they
  touch. A **contact** (`lang/core/contact.py`) is a board that meets
  another edge-on, one of its narrow faces on the other's big face. It holds
  both parts, the two faces, the axis along the line where they meet and the
  rectangle: along that axis where the edge-on board's end has material and
  the other board's outline covers it, across it the edge-on board's
  thickness as far as the other board covers it (`across_lo`, `across_hi`).
  A connector stays where the edge-on board's thickness puts it and is an
  error where it would reach past the other board's edge.
- Exact for outlines (a toe kick notch in the side shortens the bottom's
  contact); an end interrupted by a notch gives one contact per piece. A
  contact narrower than 0.01 mm either way is none.
- A board meeting another across a pocket, hole or V-groove made before, in
  the face it lies on or in its own end, is an error, as across a cutout's
  opening: make it after the join [decided]. What joins made does not count
  (joins go across each other's: screws in the tenons' gaps, a drawer's
  floor in its groove past a box joint's reliefs).
- **Crossings** (`lang/core/crossing.py`) are two boards in perpendicular
  planes whose material passes through each other, like battens across and
  along a floor. They share one axis, the line their planes meet along; each
  board's material at the other's thickness, projected onto that axis, gives
  the height they share.

## Joining

- **A join names its partners** [decided]: `bottom.join(left, right,
  using=cabineo(count=3))`, partners one by one or in lists
  (`long.join(battens, using=half_lap(...))`), the joint as the required
  keyword `using=`, so the type checker catches a missing joint. Nothing is
  joined that is not named.
- Every board named must meet the receiver the way the joint needs (a
  contact for a connector, a crossing for a half lap), else the join fails
  naming it, and a failed join changes no board. A board named twice, or the
  receiver itself, is an error. A second join of a pair with the same kind
  of joint is an error naming both boards. Every joint error is reported on
  the board whose `join()` was called, naming the other (`cab.back: cabineo
  with cab.left: ...`).
- A connector join may be written from either board, since the contact says
  which one meets the other edge-on: `left.join(bottom, top, using=...)`
  equals the two joins from the bottom and the top. A half lap stays
  relative to its receiver (`toward=` is where the receiver's notches open).
  Where a board crosses only some of a list, the build picks them, e.g.
  `[b for b in battens if b.box().overlaps(piece.box())]`.
- Joint types are objects with their settings: `tenons(count=3)`,
  `box_joint()`, `domino("5x30", count=4)`, `cabineo(count=2)`,
  `clamex(count=2)`, `screws(count=4)`, `groove(5)`, `half_lap(toward=)`.
  Connectors are joint types, not an option of tenons. [decided]
- `Board.join(*partners, using=joint)` hands the board and the boards named
  to the joint object (the `Joint` protocol in `part.py`), as `Scope.mount`
  does with hardware, so core knows no joint types. The join happens when it
  is called: the boards it joins must exist by then.
- Joints that grow a board (tenons, box joint fingers, a grooved floor) widen
  its outline (`Board.add_to_outline`); its box stays the placement box.

## Half lap

`lang/joints/laps.py`. `long.join(battens, using=half_lap(toward=
floor.top))` laps the board with each board named, all of which it must
cross, each reaching through the other's thickness (one ending inside the
other, short of its far face, would leave the notch cut through the other
open there: an error [decided]).

- Its own notches open toward `toward`, the other boards' the opposite way.
  The split lies in the middle of the height both share at each crossing
  (`split=` a position instead), and `clearance=` is the play in each notch
  in total, half on each side (default 0), as with tenons and box joints.
  The settings after `toward` are keyword-only.
- Each notch is a through cut named `lap_<other board>`.
- Dog bones at the notch's two inside corners at its floor, as part of the
  notch's cut: `dogbones="corner"` (default, as on tenons [decided]),
  `"hidden"` (centred on the floor, touching the notch's side, bulging past
  the floor into the half of the crossing that stays this board's, where the
  other board covers it on both faces; the notch must be wider than the
  relief) or None; `tool=6`, `relief=0.1`.
- Example: the van's floor battens (`examples/van.py`), all 48 crossings.

## Connectors

`lang/joints/connectors.py`:
`bottom.join(left, right, using=cabineo(count=3))`,
`back.join(left, right, bottom, top, using=domino("4x20", count=2))`,
`top.join(right, using=clamex("P-14", at=[...]))`.

- Stations: along each contact the connectors sit at `count=` stations, the
  outer ones `end=` from the contact's ends (37 for Dominos, the machine's
  stop latches; 60 for the others, the add-in's default), or at the
  positions `at=` (a list, also for one). `end=` given with `at=`, `gaps=`
  or `count=1`, which would ignore it, is an error, as is tenons' `margin=`
  with `at=` or `count=1`. Stations come from `lib/stations.py`.
- What each connector makes must lie within its contact, along it and across
  it (Clamex guide holes, a Cabineo pocket, every Domino slot at its own
  length). Every operation is on a big face.
- `domino(size, ...)`: a slot in the face-on board, centred on the edge-on
  board's thickness or `fence=` from its reference face (the show face
  unless `face=`), half the Domino's length plus 0.5 deep or `remaining=`
  short of the far face; `loose=` lengthens all slots but the first (front,
  left or bottom) per contact. The edge-on board's mortise is cut with the
  Domino machine, which is lined up by a mark: a 90 degree V-groove in the
  edge-on board's reference face, 0.3 deep, running 4 in from its end (it
  starts 1 mm outside the board so it runs out cleanly), one per Domino by
  default; `marks="middle"` leaves out the first and last, which the
  machine's end stops locate, `marks=None` all of them. The marks are the
  layout's `vgroove` operation (`Board.add_vgroove`): a straight V-groove
  from a start to an end point on a big face, a depth, ends cut square. Auto
  Setup recognises such a groove and traces it with the V-bit.
- `clamex("P-10" | "P-14", ...)`: the access slot or hole in the edge-on
  board, half its thickness deep, two guide holes 101 apart in the other.
- `cabineo("8" | "12" | "8 M6", ...)`: three overlapping 15 mm holes, 10.5
  deep [decided], in the edge-on board, open toward its end, and the screw
  hole in the other, 5 mm from the access face across the edge-on board's
  thickness; `insert=` for the 8 M6, `surface="flush"` or `"anti-break"`,
  `through=`. The threaded insert's collar reaches past a 15 mm board's face
  by 1.35 mm, as in the add-in [decided: kept].
- The access holes go on the edge-on board's big face that is not its show
  face, unless `face=` names one (`face=cab.bottom`, `"inner"`). With the
  default show face (outer) that is the inner face of a carcass bottom or
  top, which is also where the back's Domino slots are, so each board is
  machined from one side.
- Operations are named `cabineo_left_1a` (kind, other board, station,
  letter), the stations numbered across all contacts of a pair
  (`domino_divider_1` to `_4` along a notched end). Round access pockets are
  hole features; the slots are made as slots (`Board.add_slot`, see
  `design/operations.md`), so the layout carries their centre lines, and
  their round ends come out as true arcs.
- Verified in Fusion against connectors_native on the same board pair
  (Cabineo 8 x 3, Domino 4x20 x 3 with marks, Clamex P-10 x 2): zero boolean
  difference both ways and as many faces per body as the add-in's.

## Tenons

`lang/joints/tenons.py`: integral mortise and tenon as the tenons_native
add-in makes it, spelled like the connectors: `shelf.join(left, right,
using=tenons(count=3, width=50))`, from either board.

- The edge-on board grows full-thickness tenons out of its end, as long as
  the other board is thick (`remaining=` shorter for a blind mortise). The
  other board gets a mortise per tenon, `clearance=(0.1, 0.1)` larger along
  and across the joint: a through cut, or a pocket `extra_depth=0.5` deeper
  than the tenon.
- Placement: `count=` and `width=` with the outer tenons `margin=30` from
  the contact's ends (one is centred), `even=True` for tenons as wide as the
  gaps, or `at=` centres.
- Dog bones for a `tool=6` cutter, `relief=0.1` wider: `"corner"` (default
  [decided], on the bisector, through the corner) or `"hidden"` (into the
  tenon's root and past the mortise's ends, covered by the shoulder) or
  None. A hidden relief is `tool + relief` across, which the mortise across
  the joint and the tenon's length must allow; none where a mortise breaks
  out of its board or a tenon is flush with its board's end. With dog bones,
  the gaps between the tenons must be at least the tool, which routes them,
  and a corner relief bites 0.15 times the tool plus half the relief into a
  tenon's side at its root, so a tenon must be wider than its two bites.
- Reliefs and mortises are round through cuts and pockets, so the tenon
  joint needs no new operation.
- Screws and Clamex/Cabineo in the gaps between tenons are joins of their
  own that take their stations from the tenons, not options of the tenon
  joint [decided] (next section).
- Verified in Fusion against tenons_native (corner and hidden dog bones,
  blind, even, mortises breaking out of the board's edge): zero boolean
  difference both ways, identical face counts. Example: `examples/shelf.py`.

## In the tenons' gaps, and screws

- A tenon joint records what it made per contact (centres, width, length),
  and a joint given `gaps=t` joins along those contacts, as they were before
  the tenons changed the outline, one per gap between and beside the
  tenons: `cabineo(gaps=t)` (gaps of at least 40), `clamex(gaps=t)` (120),
  `screws(gaps=t)`.
- `screws` (`lang/joints/screws.py`): `count=`/`at=` on a plain butt joint,
  or `gaps=t`, through the board that is met from its outer face into the
  other's end, centred on its thickness. `countersink=True` for a 90 degree
  countersink twice the screw plus 0.4 wide (a chamfer on the hole's edge),
  which must lie on the face it is sunk into (`hole_fits`). `offset=12` puts
  two beside each tenon instead.
- `screws(tenons=t)` drills through the tenons themselves, halfway along
  each, one in the middle or two `offset` in from its edges, square to the
  tenon board's faces: only where the tenon's face lies open because its
  mortise runs out of the other board's edge, as with a top flush with the
  sides (the screw is driven through the open tenon into the other board
  [decided]), else an error; drilled from that open face.
- The Lamello and screw dimensions come from `lib/connector_data.py`, which
  tenons_native reads too.
- Verified in Fusion against tenons_native: gap screws centred with
  countersink and two-sided, Clamex P-10 and Cabineo 8 in the gaps, tenon
  screws centred and two-sided: zero difference both ways, identical face
  counts.
- Screws through a drawer face into the box front were dropped [decided].

## Box joints

`lang/joints/box_joints.py`: the corners of a drawer box as the box_joint
add-in makes them: `front.join(left, right, using=box_joint(7, margin=2,
clearance=(0.1, 0.1)))`, from either board.

- The board that meets the other edge-on grows fingers through the other
  board, flush with its outer face; the other board gets the notches. The
  corner must be flush: the other board's end in the plane of this board's
  outer face, covering its end, which the joint runs along the whole width
  of, so cut-outs at the joint (a slide's coupling cut-out) go after the
  join; else the join fails naming the boards.
- Settings, the add-in dialog's defaults [decided]: `fingers` 5, the odd
  count of both boards' fingers together, all (length - 2 * margin) /
  fingers wide; `margin` 0, which widens the outer two; `tool` 6;
  `clearance=(along, across)` (0, 0), which widens notches and gaps by half
  the first per side and cuts their bottoms the second deeper than the other
  board is thick.
- The cutter's radius stays as fillets at the bottoms of the notches and
  gaps, through the board, and every finger is rounded over along its mating
  corners to nest in them, by grooves along it from the end: the fingers'
  from their tips, the other board's along the notch walls, opened square on
  the notch's side in a band one radius deep at the inner face, where the
  root of the finger in the notch is not rounded. Dog bones one radius deep
  sit in both inner faces, on the notch walls at the notch bottoms and on
  the fingers' sides at the gaps' bottoms. Nothing shows on the assembled
  joint; `tool=0` makes a square one.
- Names: the notches and gaps are through cuts (`notch_<other>_1`,
  `gap_<other>_1`...), the dog bones pockets (`notch_<other>_reliefs`,
  `finger_<other>_reliefs`), the grooves pockets in narrow faces
  (`notch_<other>_grooves`, `finger_<other>_grooves`). The finger grooves
  start at the fingers' tips, in front of the board's end, so an operation
  on a narrow face has an `offset`, how far in front of the face it starts
  (layout field `offset`, `Board.add_edge_pocket`).
- Machining [decided]: no change to the geometry. Florian machines box
  joints with the boards lying flat and mills the finger roundovers step by
  step with a flat cutter, so the grooves along the fingers and the notch
  walls stay as the add-in models them, cuts from the end planes.
- Two differences from the add-in: a margin smaller than half the clearance
  along the joint works, the outer gaps cut past the board's ends (the
  add-in's sketch fails there, and with margin 0 and a clearance the add-in
  fails altogether); and where the board's end runs through an outer gap's
  outer fillet (with a clearance across), the fillet has a vertex on the
  end, so that the emitter recovers the piece left of it as an arc.
- Verified in Fusion against the add-in in seven settings (the dialog's
  defaults, Florian's 7 / 2 / 6 / 0.1, square with and without clearance, 3
  and 9 fingers): zero boolean difference both ways and equal face counts.
  The drawer cabinet's drawer boxes are box-jointed as Florian's Dynapro
  boxes (7 fingers, margin 2, tool 6, clearance 0.1).

## Grooves

`lang/joints/grooves.py`: a panel set into grooves in the boards around it,
a drawer floor in its box: `floor.join(l, r, f, k, using=groove(5,
clearance=(0.5, 0.5)))`.

- The floor is placed between the boards' faces (`between(l, r, f, k)`), so
  it meets each edge-on (a contact); the join moves each edge of it that
  lies on a named board's face `depth` into that board, a corner between two
  such edges with both, and cuts every board a pocket for what the floor
  then occupies in it, from the face the floor meets, `groove_<panel>`. The
  floor goes into the front and back too, not only the sides [decided].
- The join grows the panel, rather than the panel being placed `into(n)` the
  boards and the join only cutting, so the depth is stated once, the
  placement reads as the box's inside, and the corners are filled the same
  way for every board; `side.cut(floor.box().grown(...))` stays for grooves
  by hand.
- Either board may make the call (`left.join(floor, using=groove(5))`
  grooves the left side alone, `side.join(low, high, using=groove(4))` cuts
  dados for two shelves); the boards at a corner of the panel go into one
  join, so that the corner goes into both, and a later join at a corner an
  earlier one moved is an error.
- `clearance=(depth, height)`, (0, 0) by default [decided: 0 unless given;
  Florian usually gives 0.5]: the groove's bottom lies `depth` beyond the
  panel's edge, and its ends as far beyond the panel's corners; it is
  `height` wider than the panel is thick, half of it on either side of every
  panel, a floor lying flat included [decided]. The floor stays where it was
  placed, so the slide's cut-outs and hook holes, measured from its
  underside, stay where they were; the groove reaches half the clearance
  below it (in the drawer cabinet a 0.25 mm slit under the floor along the
  boards' inner faces, seen only from below, and a 0.25 mm step at the top
  of each cut-out's sides on the inner face). The floor rests on the
  runners' drawer members, at the height the slide gives.
- `chamfer=3` [decided, so the floor goes in easily]: the panel's corners
  between two grooved edges are cut off at 45 degrees, 3 along each edge,
  once the panel has grown. At most twice the depth, or the chamfer would
  reach past the boards' faces and show; None or 0 for square corners.
  Corners next to an edge that goes into no groove stay square.
- Dog bones where a groove stops inside its board, as part of its pocket:
  `dogbones="hidden"` [decided: the default] centres them on the groove's
  end, touching its edges and bulging past the end only, and is an error
  where that would break out of the board (they reach `tool / 2 + relief /
  2` past the end); `"corner"` or None; `tool=6`, `relief=0.1`, a tool wider
  than the groove being an error. A corner relief bulges 0.93 past the
  groove's edges as well, which at a corner of the panel the end of the
  board the corner goes into covers. The drawer cabinet with 9 or 11 fingers
  does not build with hidden ones, where a floor lies across the lower end
  of a front finger (corner dog bones fit there). `board.dogbones()` adds
  nothing more at a groove's ends, since the reliefs are arcs, and relieves a
  groove joined with `dogbones=None` like any pocket.
- Nothing shows [decided: grooves must not show]: a groove is as long as
  the panel needs, so it stops inside its board where the board goes on past
  the panel's corner and runs out of it where the board ends first, as into
  a box joint's gap; at a corner of the panel either way is covered by the
  board the corner goes into. A groove as deep as its board is thick would
  show on the far face and is an error. An end that runs out of a board
  where the panel's edge beside it goes into no board of the join (a floor
  running on under a back standing on it, a through dado) may show, and the
  board gets a note in the layout's problems naming that end.
- The grooves take whatever lies in their way, so also the fillets a box
  joint's cutter keeps at the fingers' roots, which reach into the floor's
  corner where it lies near the end of a finger (the hand-built Dynapro
  drawer needed corner chamfers of 2 * (depth - clearance + 1) for them;
  here the 3 mm chamfer is only for assembly).
- A drawer slide's rear hook holes are checked against the floor by
  `slide.machine_box` (see `design/hardware.md`): with Blum the floor does
  not go into the back, so its groove join names the sides and the front
  only.
- Verified in Fusion: the drawer cabinet with its grooved floors, every body
  one solid, each floor overlapping none of its four boards (checked with 7,
  9 and 11 fingers through the preview's exact booleans).
