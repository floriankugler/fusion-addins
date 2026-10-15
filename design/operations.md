# Boards, shapes and operations

What a part is and what can be done to it. Part of the modeling language's
design; the overview is `DESIGN.md`. Code: `lang/core/part.py`,
`shapes.py`, `ops.py`, `corners.py`, `cutouts.py`, `dogbones.py`.

## Boards

- A **board** is sheet material. Thickness comes from the material. The
  outline is a 2D shape, mostly a rectangle; other shapes are made by
  adding and taking away 2D shapes (`a + b`, `a - b`). The composition
  happens in 2D before thickness is applied, so a board is flat by
  construction. [decided]
- Board versus slat is a matter of stock form, not species: a glued-up solid
  wood panel is a board. A board's material is a `sheet_material()`; solid
  wood by section and length is a slat, and `lip()` glues it along a
  board's edge (see `design/slats.md`).
- The operations per board are the layout: `cut` (through, changes the
  outline), `pocket`, `hole` and `slot` (2D shape plus depth plus face), `chamfer`,
  `fillet`, `cutout`, `dogbones`, `lip`, V-grooves (made by joints), and what joins
  and hardware add. A cut starts at the face of the board it is declared on.
- Operations on a narrow face can be written (`side.front.right(50)` as an
  anchor) and are emitted, but no joint or connector uses them: the 3-axis
  machine cannot reach a narrow face, so every connector is machined from
  the big faces of both boards. [decided] The box joint's grooves along its
  fingers are the one exception, as the add-in models them (see
  `design/joints.md`).
- Operations from two big faces, of any kind, mean the board must be flipped
  on the machine.
- A board narrower than 0.01 mm is an error (see `design/geometry.md`).

## Shapes

- **Shapes name their extents** [decided]: `rect(depth=60, height=100)` says
  which plane it lies in and reads the same on every face; placing it on a
  face in another plane is an error. `circle(d)` has no orientation;
  `polygon(points)` is the raw escape hatch in the face's (u, v), its two
  world axes in x, y, z order.
- **Corner radii are properties of the 2D shape**, so a pocket's inside
  corner equals the cutter radius by construction and no 3D fillet feature
  exists. `shape.rounded(r)` rounds every corner with r, convex and concave
  alike (the inside corners of a cut in the shape and of a board with it as
  its outline), with exact arcs. Half the narrow width rounds the ends
  fully, so `rect(depth=80, width=12).rounded(6)` has a slot's shape (a slot
  open at the board's edge is a `cut()` of one; others are `slot()`, see
  below); a larger r, or one too large for an edge between two corners, is
  an error, and so is any operation given a shape without area.
- **Adding and taking away**: `a + b` is `a.union(b)` and `a - b` is
  `a.difference(b)`, as build123d spells them; the methods stay, and
  `intersection()` is a method only [decided by Florian, 2026-10-15,
  syntax.md item 13]. The result is cleaned as every shape is and lies in
  the plane of whichever shape has one; shapes in two planes are an error,
  and so is a number (`shape + 5`: a shape moves with `moved()` and grows
  with `offset()`).
- **Clipping a corner**: `shape.clip(top=380, back=120)` cuts off the corner
  where the two named edges meet, each value the length of the cut along
  that edge; a rectangle's edges are named as the frame names its plane, a
  raw shape's left, right, bottom and top.
- Still proposed: walking an outline step by step; trimming by reference
  planes with `between` beyond what placement does.

```python
with board("left", ply15, rect(depth=500, height=720)) as side:
    side.show("outer").grain("height")
    side.cut(rect(depth=60, height=100), at=side.outer.bottom.front, name="toekick")
    side.pocket(rect(depth=200, height=12), at=side.inner.front.bottom(shelf.bottom),
                depth=to(side.outer, -3), chamfer=0.5)    # dado whose bottom is the shelf's
    side.chamfer(side.outer.outline, 1)                   # the show face's outer contour
    side.chamfer(side.front.inner, 1)                     # one edge
    side.chamfer(side.toekick, 1)                         # the contour a named cut made
    side.fillet(side.back.top, 20)                        # a corner of the outline, rounded through the board
    for z in spread(side.bottom + 100, side.top - 100, pitch=32):
        side.hole(d=5, depth=10, at=side.inner.front(37).bottom(z))   # a shelf-pin column

shape = rect(depth=500, height=720).clip(top=380, back=120)   # the top back corner cut off, 380 x 120
```

`examples/operations.py` uses every operation kind.

## Positioning and depth

- **`at=`** [decided]: an operation is positioned on a face by an anchor
  named through that face: `side.outer.bottom.front` is the corner,
  `side.outer.front` the middle of the front edge, `side.outer.center` the
  centre, and the shape's matching side or corner is placed on it, so
  `.cut(rect(depth=60, height=100), at=side.outer.bottom.front)` is a toe
  kick notch. Distances follow the edge they are measured from,
  `side.inner.front(37).bottom(z)`, and a position from the reference
  algebra may stand in for a distance, which is how a hole lines up with
  another part. Patterns come from `spread()` along one axis of the face.
- **Depths** [decided]: `depth=` is a number, `through` or `to(face,
  offset)`. Through and `to()` measure the board from the face the operation
  is on to the opposite face: its thickness from a big face, its length or
  width from a narrow one, so a hole through a board's front edge runs out
  at its back edge. A depth past the opposite face, under 0.01 mm, or `to()`
  with a positive offset, is an error; `to()` names a face of the board the
  operation is on, and a face of another part is an error.
- **Refusals** that keep the layout buildable: holes, pockets and V-grooves
  wholly off the board; a hole whose centre is off its face or in a hole or
  pocket made into that face before; a pocket or V-groove wholly in what was
  cut from its face before, as deep, or through; a cut that takes the board
  away from an operation made before; through cuts, through pockets and
  holes, and reliefs that split the board; pockets and holes from opposite
  faces that meet as deep as the board are held to what a pocket through it
  is. A refused operation changes nothing.

## Slots

`slot()` is to slots what `hole()` is to holes: vents in rows, slotted
screw holes for adjustable mounting, pass-throughs for straps and cables
[decided]. Both of its forms measure between the centres of its round ends
[decided]:

- `side.slot(8, start, end, depth=...)` runs between two anchors on one
  face, the centres of its round ends, at any angle. One between two edges
  needs no arithmetic: `side.slot(8, side.inner.bottom(z).front(40),
  side.inner.bottom(z).back(40), depth=through)`.
- `side.slot(8, at=..., centres=52, along="height", depth=...)` is centred
  on `at=`, as a hole is (the show face's centre by default), its end
  centres 52 apart, so 60 long overall [decided]: catalogues give overall
  lengths, so the keyword says centre to centre. `along=` takes what
  `grain()` takes, an extent name or a side, direction or face
  (`along=cab.top`), and must lie in the face's plane.

```python
for z in spread(back.bottom + 60, back.top - 60, pitch=20):     # vents, centred across the back
    back.slot(6, at=back.inner.bottom(z), centres=120, along="width", depth=through)

a, b = side.inner.front(40).bottom(100), side.inner.front(40).bottom(140)
side.slot(12, a, b, depth=4, name="mount_head")                 # a stepped mounting slot:
side.slot(6, a, b, depth=through, name="mount")                 # two calls, the same anchors
```

- It takes `chamfer=` and `name=` like a hole and `depth=` like a pocket,
  with a pocket's `floor` and edges (its bounding box; at an angle the
  arcs' extremes). Its ends are arcs, so it needs no dog bones; where it
  meets another pocket or slot, `dogbones()` finds the corners as for any
  pocket. A stepped slot, for a screw head, is two calls with the same
  anchors [decided].
- Big faces only [decided]: a slot in a narrow face is a `pocket()` of a
  rounded rectangle.
- Both end centres lie on the board's outline, give or take 0.001 mm, as a
  hole's centre must [decided]; unlike a hole's they may lie in a pocket
  made before, so the narrow part of a stepped slot goes through the wide
  one. The rest of the slot may run over the edge and cuts what it reaches;
  through the board that leaves the outline as it was, as a through hole
  does. A slot open at the edge is a `cut()`.
- Refused besides, as for a pocket and: both forms mixed, one anchor, the
  anchors on two faces or on another board, a width under 0.01 mm, end
  centres less than 0.01 mm apart (a round hole is `hole()`). Two anchors
  on one axis but for float noise (1e-9) are put onto it, so a straight
  slot has straight sides. Errors call it a slot.
- In the layout a slot is a pocket of its shape that also carries `slot`,
  its centre line (the centres of its ends in the face's frame) and width
  [decided], for the CAM plan (`design/proposals/cam.md`); the preview and
  the emitter draw the pocket, its ends recovered as arcs. Joints cut their
  slots so too (`Board.add_slot`): Domino slots, Clamex P-10 access slots,
  Cabineo reliefs.
- Machining: Auto Setup cuts a slot as a pocket and wants a tool at least
  0.1 mm narrower than it (`TOOL_CLEARANCE` in `lib/auto_setup/rules.py`),
  so make a slot at least 0.1 mm wider than the cutter that clears it.
  Nothing checks this yet, since the language knows no tools [decided].

## Cutting with a part or a box

`side.cut(floor)` removes the region the floor occupies inside the side, its
outline through its thickness; a pocket from the face the region enters
through, or a through cut when it passes the whole thickness. `cut(box)`
does the same with a box. A region must reach 0.01 mm in. Room for a fit is
stated on the region, not on the operation:
`side.cut(floor.box().grown(top=0.5, left=0.5))`, so the gap is explicit per
side and the operation stays a plain cut. [decided] Drawer floors use the
`groove` joint instead (see `design/joints.md`).

## Chamfers

Chamfers are modeled geometry: along outer contours, along pocket contours,
and on holes. A chamfer belongs to a contour on a face. [decided]

- Spelling [decided]: `.chamfer(what, size)`, where `what` is an edge
  (`side.front.inner`), a face's outline (`side.outer.outline`), a named
  operation (`side.toekick`), or a list of them. `.cut()`, `.pocket()` and
  `.hole()` accept `chamfer=` as sugar for a chamfer along their own
  contour. The constructor takes no chamfer; a build-wide default such as
  "1 mm on the outline of every show face" would be a rule.
- An edge along a big face is chamfered on its big face, whichever face is
  named first (`side.front.inner` and `side.inner.front` are the same
  chamfer). A cut's chamfer is on the show face.
- An edge through the board, where two narrow faces meet
  (`panel.front.left` on a board lying flat), is a corner of the outline, so
  its chamfer cuts the corner off the outline, `size` along both edges, as
  `fillet()` rounds one. Contacts, crossings and checks then see the cut
  corner. [decided]
- A chamfer is 0 (none) or at least 0.01 mm (`ops.MIN_CHAMFER`), however it
  is made [decided]. A list is chamfered whole or not at all.
- A chamfer must be smaller than the depth of what it bevels (a pocket's or a
  hole's depth, the thickness for an edge, an outline or a cut's rim), and
  smaller than the wall it bevels where a pocket, hole or V-groove from the
  other face runs out under its rim and leaves the wall the thickness less
  its depth (one through the board leaves no wall there, and the chamfer
  stops at it). A chamfer along an edge that is gone (corners rounded with
  half the board's width, a cut across all of it) is an error. A V-groove
  cannot be chamfered.
- **Roundovers** are not modeled. [decided] They could be a note on an edge
  for labels and the hand-work list (see `design/proposals/cam.md`).

## Fillets

`board.fillet(what, radius)` rounds corners of a board's outline, through
its thickness, as the router cutting the outline leaves them. `what` is a
corner named as the edge where two narrow faces meet (`panel.front.left` on
a board lying flat, `side.front.bottom` on one standing), a named through
cut (`panel.notch`: every corner it made in the outline, the inside one
too), a big face's outline (`panel.top.outline`: every corner of the outer
boundary, not those of its holes), or a list of them, which are rounded
together. A convex corner loses material, a concave one gains it; the arcs
are exact and tangent to their edges, lines or arcs.

- It changes the outline at once, as a cut does: everything after it meets
  the rounded corner: contacts and the joints made on them (a connector
  keeps to the shorter contact), crossings, `no_interference`, cutouts, dog
  bones (a rounded inside corner gets none). Nothing new reaches the layout:
  the preview extrudes the outline, and the emitter recovers its arcs (see
  `design/geometry.md`), so Fusion gets one cylindrical face per corner and
  no fillet feature.
- Errors: an edge along a big face (`panel.front.top`, a roundover, which
  stays unmodeled; chamfer it); a corner the outline no longer has (a cut, a
  joint or an earlier fillet took it; the corners a cut made are named by
  the cut); a radius too large for the edges at a corner, or for two
  neighbours together; an arc running into a through cut; and an arc taking
  material where an operation made before it lies, such as a joint's holes
  at that corner. So a corner where a joint goes is rounded before the join,
  which then keeps clear of it. [decided]
- Corners are not named by a point (`panel.top.front(60).left(40)`) until a
  build needs it, so the corners a joint adds to the outline (tenon
  shoulders) are reached only through the whole outline. [decided]
- Verified in Fusion on `examples/operations.py`: each rounded corner is one
  cylindrical face of its radius about the arc's centre, the cut-off corner
  one face at 45 degrees, volumes within 0.002 % of the preview's.

## Cutouts

What the Face Cutout add-in (cutouts_native) does, as an operation.
`side.cutout()` cuts out a big face inside a `border=` (20), keeping
`around=` (20) mm of material around everything the board has so far: its
holes and through cuts, pockets and holes in either big face, holes into
its narrow faces, V-grooves.

- `pattern=cross(width)` leaves two diagonal bands; `pattern=triangles(
  columns, rows, spacing)` a lattice of triangles with a true gap between
  them (`aligned=True`: each rounded tip reaches the next row's base line;
  `along=` the extent the columns run along, the longer side by default;
  `start=` the corner, by default the bottom, front, left one).
- It is named `openings` unless `name=` says otherwise.
- `radius=` (8) rounds every corner of the openings, `chamfer=` puts a 45
  degree chamfer on their rims at the face cut from, `depth=` makes it a
  pocket (`to(side.outer, -3)` leaves 3 mm), and a region shape with `at=`
  limits it to part of the face (the add-in's Bounding Box Points).
- Defaults and the patterns' sizes are `lib/cutout_patterns.py`, which the
  add-in reads too.
- Decided with Florian:
  - the default face is the big face that is not the show face, the inner
    face by default: usually the machined one, and the chamfer stays off the
    visible face;
  - rhombuses, tabs and patterns at an angle to the board's edges are left
    out for now; without tabs, material kept around a feature in the middle
    of a through cutout would fall out, which is an error;
  - a cutout is an ordered operation like any other: it spares what exists
    when it is made, so it goes after the joins; an operation made later
    inside an opening, or a board joined later across one, is an error;
  - `keep=[shelf]` keeps a strip where another board meets the face (its
    footprint grown by `around`), stated like every other relation;
  - pieces too small for the radius are left out and noted in the layout's
    problems (the add-in leaves them sharp); a region that rings and keeps
    split into pieces is cut out whole (the add-in cuts its largest piece).
- Openings that touch the outline or each other at a point are refused,
  through or pocketed (Fusion cannot build them).
- The geometry follows the add-in's tool bodies: the outline inset, less the
  material kept, the pattern clipped to that, then every corner filleted.
  Offsets keep sharp corners, as Fusion's sketch Offset does (see
  `design/geometry.md`). Verified in Fusion against the add-in on the same
  boards (full, cross, triangles, aligned triangles, a pocketed cross, each
  with a hole and a pocket kept): zero boolean difference both ways and
  identical face counts. Example: `examples/cutouts.py`.

## Dog bones

A router leaves its radius in every inside corner, so a part with square
corners does not go in; a dog bone takes the corner out. Two ways [decided]:

- **Per board**: `side.dogbones(tool=6, relief=0.1)` relieves every inside
  corner of the board, `at=` only some: the corners of named operations
  (`side.toekick`), of a big face (`side.inner`: what that face shows,
  through cuts and its own pockets, as when the add-in is given a face) or
  of the outline's outer boundary (`side.outer.outline`), one or a list.
  `at=` takes objects only [decided]: the operation itself, never its name
  as a string, which is an error saying to write `side.toekick` instead.
- **Per joint**: joints that cut inside corners relieve them themselves,
  with `dogbones=`, `tool=` and `relief=`: tenons, half laps and grooves
  (see `design/joints.md`). Box joints keep the cutter's fillets and hide
  their own reliefs.

Rules:

- `dogbones()` acts where it is written, like every operation [decided]: it
  relieves the corners the board has at the call, so it goes after the cuts
  and joins whose corners it should relieve, and corners made later get
  none. A relief that cannot be made (one that would split the board) leaves
  the board as it was. A through relief kept to its own level can take the
  corner of a shallower pocket beside it down with it; that corner, deeper
  now, is one the call made, which a second `dogbones()` relieves.
- Reliefs go in as operations named after the operation the corner belongs
  to (the last whose contour runs through it), `toekick_dogbones`, or
  `outline_dogbones` for the outline's own corners and those of unnamed
  operations: a through cut where the corner
  is one of the outline (cuts, notches, laps, tenon roots), else a pocket
  from the face the corner is seen from, as deep as what lies beside it (the
  pocket's depth; through for a through pocket); a corner on a pocket's
  floor (a pocket inside a pocket) is cut from the face to the deeper one's
  depth. A corner through the board is relieved once, from the face on which
  it starts deepest. Reliefs come in the order of the operations they belong
  to, then by face and depth, however the board lies.
- Geometry, dog_bones_native's: from the corner along the bisector of its
  two edges, the centre `(tool / 2) / sin(angle)` out, `angle` the angle
  between the edges (at 90 degrees half a tool, at 60 or 120 degrees 1.155
  times that), the radius that plus `relief / 2`, so the circle reaches
  `relief / 2` past the corner at any angle; the add-in's Offset is
  `relief`. The relief takes only its own corner's material, as the
  add-in's in-face profile does: where its circle reaches material that is
  not on the corner's level and connected to the corner (a shallower pocket
  beside a deeper one, a web across a narrow opening), that is left out of
  the shape. Tenons, half laps, grooves and `dogbones()` share the helpers
  (`corner_relief`, `hidden_relief`).
- An inside corner is a vertex between two straight edges of the material,
  seen from either big face on every level (the face, each pocket's floor),
  where the boundary turns away from the material by more than an arc's
  segment does (`arcs.MAX_STEP`, 11.5 degrees). Straight means a line as the
  emitter draws it (`arcs.fit`): circles, slots' round ends, rounded
  corners, kept fillets, other reliefs and holes are arcs, and a junction of
  a line and an arc is no corner either. So a corner relieved before gets
  none, `dogbones()` on a tenoned, lapped or box-jointed board adds nothing
  at the joint, and a square box joint (`tool=0`) gets them in its notches
  and gaps. A floor's corner next to a higher island is not an inside corner
  (its wall goes up). Holes count as round regions; V-grooves, chamfers and
  operations on narrow faces do not count, and neither does a vertex with an
  edge shorter than 0.01 mm. A relief at a sharp cutout corner (`radius=0`)
  leaves the opening out of its shape, so the cutout's check for operations
  in its openings passes.
- Deviations from the add-in: vertices turning less than 11.5 degrees are
  not corners (the add-in would put a circle of 5 tools and more on a 170
  degree corner); a chamfer on the contour does not stop a relief (the
  add-in finds no corner on a chamfered face), the relief cuts through the
  chamfer, and a chamfer along a named operation does not follow the
  relief's arc.
- Verified in Fusion against dog_bones_native on `examples/dogbones.py`'s
  boards: zero boolean difference both ways and equal face counts on all
  seven parts.
