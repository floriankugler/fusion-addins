# Modeling language: design brief

Status: partly implemented on branch `language`, see "First slice". Written
2026-10-09 from a design conversation between Florian and Claude, as the
starting point for implementation work in this repo. Revised 2026-10-10 after a design review and the compile-speed
benchmark. All function, package and reference names are placeholders.

Each point is marked:

- **[decided]** Florian stated or confirmed it.
- **[proposed]** Claude suggested it and it was not rejected. Treat as a working
  assumption and check with Florian before building a lot on it.
- **[open]** undecided or unverified.

Statements about the existing add-ins come from README.md, AGENTS.md, the file
structure and function signatures, and parts of `addins-src/connectors_native/main.py`.
The code was not read in full.

## Goal

A modeling language embedded in Python for Florian's van conversion work: furniture
made of plywood boards and solid wood slats, joined with the connectors and hardware
that this repo's add-ins already cover. The Python source is version controlled and
is the parametric model. Fusion documents are generated from it.

Why: driving Fusion step by step through MCP is slow and hard to review on large
projects. Source text is efficient for Claude to write, readable for Florian, and can
be tailored to exactly his constructions.

Not goals:

- A general-purpose CAD language.
- Replacing Fusion. It stays the kernel, the viewer, and the place for nesting and CAM.
- Describing parts that are curved in 3D (bent or upholstered parts). Those stay
  hand-modeled and are referenced by name. Boards bent about one axis may
  come in, see "Bent boards" under "Still to do" [2026-10-13].

## Terms and pipeline

- **Module**: one piece of furniture or assembly (kitchen, bed, floor). It compiles
  on its own into its own Fusion document.
- **Master document**: a hand-made Fusion document with named planes and sketches
  for the whole van. The compiler reads it and never writes to it.
- **Snapshot**: the master document read once into a JSON file: every plane as
  origin plus normal, every contour as a sampled polyline, every body as a
  box, every user parameter; later the vehicle body as a mesh for the
  preview. [implemented 2026-10-11, without the mesh]
- **Layout**: a pure-Python description of each part: its world placement, its
  outline, and a list of operations (2D shape, depth, face). Written to one
  JSON file per module. No Fusion involved.
- **Emitter**: an interpreter for the layout file that creates Fusion features.
  The only code that imports `adsk`.
- **Preview**: a second consumer of the layout file that meshes the parts and
  shows them in a browser, without Fusion. [proposed]

```
Master document --(snapshot, in Fusion, rarely)--> snapshot.json
                                                       |
Python source ---------------------------------------> layout step (plain Python,
                                                       anywhere, < 1 s)
                                                       |
                                         +-------------+-------------+
                                         v                           v
                               preview (browser, instant)    emit (in Fusion, seconds,
                                                             one direct document per module)

afterwards, unchanged: Multi Arrange (nesting) and Auto Setup (CAM)
```

Three steps with files between them. The layout step can use shapely and numpy
because nothing heavy runs inside Fusion's Python, and `core` can be tested
against real van data. [proposed]

## Decisions

### Language form

- Embedded in Python, built from a small set of primitives, extended with Florian's
  own functions. A cabinet type is a function. [decided]
- One-way flow from source to Fusion. Generated documents are disposable.
  Hand-drawn input lives only in the master document and in optional per-module
  reference documents. [decided]
- Division of labour inside the source [proposed]:
  - numbers are variables, each design decision stated once;
  - arrangement is expressed as relations between named parts, not as arithmetic
    on dimensions;
  - repeated constructions are functions;
  - geometry taken from the vehicle comes from the snapshot, as polylines; the
    kernel is only asked for things a polyline cannot give (booleans against
    hand-modeled bodies), and those are the exception.
- Eager position math, deferred emission. A part's position and faces are known
  as soon as its placement is stated, so references like `left.inner` work in
  the next line. Nothing touches Fusion until the whole module is declared,
  because joints change both parts they connect and checks run before geometry
  exists. The examples read as immediate mode; they are not. [proposed]

### API form

Constructors carry identity, modifiers carry everything else, in the style of
SwiftUI and jQuery. `board("left", ply15)` names a part and its material; where
it sits and what is done to it are method calls that return the part, so they
chain or stand on their own lines. [decided as the direction; the rules are
proposed]

- **Placement and property modifiers are order-free and settable once.** `on`,
  `between`, `center`, `inset`, `grain`, `show`, `manual`. Setting one twice is
  an error. The result never depends on the order they were written in.
- **Operation modifiers are ordered.** `cut`, `pocket`, `hole`, `chamfer`,
  `fillet`, `miter`. A cut changes the outline for everything after it, and
  so does a fillet (or chamfer) on a corner of the outline; a chamfer on a
  pocket must follow the pocket. The order on the page is the order in the
  layout.
- **Every modifier returns the part itself, and the part is mutable.** A later
  `side.hole(...)` on its own line is the same as the chained form, which is
  what the incremental workflow needs. Operations get a `name=` and are
  reachable as attributes, so `left.toekick.top` names the face a cut made:
  a named operation's edges are positions by direction, a pocket or hole
  also has a `floor`, and `board("bottom").on(left.toekick.top,
  toward=cab.top)` puts the bottom on the toe kick without repeating its
  height. [implemented 2026-10-11]
- **Operations keep a few keywords.** Face, position and depth interact and
  belong in one call: `pocket(shape, face=, at=, depth=)`. Splitting them into
  separate modifiers would double the length and lose the grouping.
- **Relations are methods on a part.** `bottom.join(left, right, using=...)`,
  `drawer.mount(...)`, `face.latch(...)`, `cab.port(...)`, `cab.export(...)`.
  Methods give autocomplete an entry point that free functions lack. A
  relation names every part it involves; nothing is related to whatever
  happens to touch (see `join` under Joints). [decided 2026-10-11]
- **Placement resolves lazily with early errors.** `board("left", ply15)` has no
  position until `.on()`. Using `left.inner` before that errors with the part
  path and the missing fact. Since emission is deferred anyway, this costs
  nothing.
- **Faces and edges are attributes, not only strings.** `side.front` is a face,
  `side.front.inner` an edge, so autocomplete shows the six directions and a
  typo fails at parse time. Strings stay allowed where names are computed.
  Direction names and modifier names do not collide. The six directions plus
  `inner` and `outer` are real properties on boxes, scopes, boards and faces,
  not dynamic attributes, so editors and the type checker see them; project
  aliases such as `fs` go through `face()`, `edge()` and `side()`.
  [decided while implementing]
- **Strict typing.** The package is checked with pyright in strict mode and
  ships a `py.typed` marker, so build files get completion and errors in the
  editor. Positions, sides, faces, anchor and depth specs and the layout file
  are all typed; the layout file's shape lives in `layout_types.py` and is the
  contract the emitter is checked against. [decided while implementing]
  Since the review of 2026-10-12 this covers the calls that used to slip
  through: a hardware object's `mount` names its parts as typed keywords,
  which `cab.mount(hardware, ...)` passes on through a ParamSpec, so
  `cab.mount(hinge, dor=door)` is a type error like a missing `using=`;
  `pocket()` and `hole()` take `depth=` as a required keyword; a misspelt
  method on a board is an `Operation` to the checker, which then reports
  the call. `tests/typing_checks.py` lists what pyright must reject (each
  line carries a `# type: ignore` that pyright reports once it is no longer
  needed). `cab.<name>` (parts, child scopes, exports) stays untyped,
  since an export can be any value; `cab.part(name)` is the typed form.
- **Two layouts on the page, one object.** A chain in parentheses for a few
  calls; a `with board(...) as side:` block when a part has many operations, so
  the receiver is not repeated. Both build the same part.
- **Direction names on a scope are its box sides.** `cab.left` is the side of
  the module's box, also after a part named `left` exists, because carcass
  parts are routinely named after directions and `board("left").on(cab.left)`
  must read naturally. Parts with such names are reached as `cab["left"]`;
  other names resolve to parts, child scopes and exports. An export cannot
  take a part's name. [decided while implementing phase 1]
- **`at=` is an anchor named through its face.** `side.inner.front(37).bottom(z)`
  is 37 mm behind the front edge of the inner face at the position `z`;
  `side.outer.bottom.front` is a corner; `side.front.right(50)` is a point
  on a narrow face, centred in the thickness because the thickness axis is
  not named. A number measures from the edge it follows, a position is
  taken as it is, an unnamed axis stays centred. The anchor also says which
  face the operation is on, so there is no `face=`. Strings and bare
  direction names were rejected: no autocomplete, and carcass parts are
  named after directions, so `bottom.front` would read as a face of the
  bottom board. [decided 2026-10-10, replacing the string form]
- What this is not: free functions for everything (no autocomplete entry point),
  operators such as `left @ cab.left` (cryptic), or dataclass specs (that is
  what the layout JSON is for, and the language should not look like it).

### Backend

- Use Fusion's own features (extrude, hole, chamfer, fillet, combine). Do not build
  bodies with our own B-rep code, which would mean reimplementing what Fusion
  already does. [decided]
- The timeline of a generated document is written top to bottom and thrown away on
  the next compile. It is never edited, so no reference ever has to be re-resolved:
  each feature is handed its faces and edges at the moment it is created. [proposed]
- Each module compiles in its own small document. Write cost grows with the
  number of features already in the document; measured 2026-10-10, see
  "Measured: compile speed" below. [measured]
- A document without history (direct modeling) is 5-10x faster and covered
  everything the synthetic module needed. Compile into direct documents; keep a
  parametric document as a debug mode, because its timeline is a readable log of
  how each part was built. [measured, decision proposed]
- The emitter is one generic interpreter with a small instruction set: part,
  cut, pocket, hole, chamfer, V-groove, name. Every joint and hardware pattern in this repo
  reduces to those operations on faces of flat parts, which is also what Auto
  Setup recognises. The emitter batches: one sketch per board face, one hole
  feature per diameter and depth, one cut per depth with many profiles, one
  chamfer per face and size. Sketches are drawn with compute deferred; complex
  outlines are built as temporary B-rep faces and extruded as such. [proposed,
  levers measured below]
- Compiler output has no sketch constraints and no dimensions. The AGENTS.md rule
  on fully constrained sketches is for the interactive add-ins, whose results
  users edit in the timeline. Generated documents are never edited. [proposed]
- After a compile, Multi Arrange nests and Auto Setup derives CAM from the
  geometry. Multi Arrange works in the compiled direct documents as they
  are (tested 2026-10-11): it solves in a parametric scratch document and
  places the nested copies without base feature or timeline group. Where
  Auto Setup runs is still open.
- The compiler hands each part's facts to those tools as a JSON attribute
  `lang`/`part` on its body [implemented 2026-10-11]: path, material,
  thickness, whether the material has a grain, the grain direction (null
  when the build left it unset) and `up`, the outward normal of the face it
  is machined from. That face is the big face more pockets, holes and
  chamfers are made from (a cut's chamfer counts for the show face), the
  show face on a tie; the layout carries it as `machine`. Multi Arrange
  uses the build's grain before its own guesses (texture, longest edge),
  lets parts of a material without grain turn freely, and adds all
  compiled parts of a material at once (Compiled parts + Add in its
  dialog), each by its machining face, so it lands machining side up.
- Later [open, noted 2026-10-11]: make the grain visible in Fusion, by
  giving compiled parts an appearance whose texture runs along the grain
  (Multi Arrange already reads 3D wood textures' direction, see its
  model.py). Not needed for nesting, which reads the attribute.

### Names and paths

- Every object has a path, for example `kitchen.drawercab.drawer2.left.front.inner`.
  Code runs inside a scope, so only the tail is written. [decided]
- Mapping to Fusion [decided]:
  - scopes (module, sub-assembly) are nested components;
  - a board is a body inside its module's component, not a component of its own
    (Florian does not rely on Fusion's parts list or on drawings per part);
  - bought parts (slides, hinges) are linked components, as in existing documents.
- The world frame is defined once per project: front is -x (toward the
  vehicle's front), left is -y (the driver's side), top is +z, as in the
  Planung document. Aliases are possible (`fs`, `bfs` for driver and passenger
  side). [decided; the axes confirmed 2026-10-10]
- A cabinet is written in its own frame and placed: `cabinet(name, box,
  front=box.right)` makes it open toward the box's right side; top stays up,
  left and right are a cabinetmaker's, standing in front of it; `mirrored=True`
  swaps them. Inside, `cab.back`, `side.inner.front(37)`, `rect(depth=...)`
  and `width`, `depth`, `height` are the module's own, child scopes inherit
  the frame, and the layout file carries world names, so the preview and the
  emitter never see module frames. A cabinet type is written once and placed
  on either wall, rotated or mirrored, which is the usual case when a module
  is designed before it has a project. [decided 2026-10-10]
  `front=` is what makes a module a cabinet [decided 2026-10-12], and the
  constructor says so [decided by Florian 2026-10-12, after the review]:
  `cabinet(name, box, front=...)` with `front=` required, and
  `module(name, box)` for van-level modules such as the floor, the
  ceiling or wall panels, which take the enclosing frame as it is, in the
  van the van's own terms, the driver's left; `module(..., front=)` is an
  error pointing to `cabinet()`, and `cabinet()` refuses a front facing up
  or down. A cabinet says which way it opens,
  also when that is the van's front (`front=box.front`): seen from its
  front, a module in the van's terms that opens toward the windshield has
  its left on the right, since one front cannot serve a left measured
  facing it (the driver's) and one measured looking at it (the
  cabinetmaker's). Hardware is placed by the drawer's or door's own left
  and right, seen from its front, so it comes out the same in either kind
  of module and is never mirrored.
- A face of a part is named by direction. An edge is named by two faces
  (`front.inner`), a corner by three. This is the scheme BOSL2 uses for anchors.
  [proposed]
- Global directions are the primary face names everywhere (`left.right` is the
  inner face of the left side). `inner` and `outer` are sugar that resolves only
  when unambiguous; a shelf at mid height has two inner faces and errors. Each
  board has a `show` face, the visible one, which decides the machine side and
  the chamfer side: what `show()` names, else the outer face, else, for a
  board across its scope's middle, the face toward the scope's top, else its
  back, else its right, named in the scope's own terms [decided by Florian
  2026-10-14; it was the face toward the world axis' positive end, so a
  divider showed its left in a cabinet facing the van's right and its right
  in one facing its front]. `show()` is frozen once the show face is used,
  not when the placement is, so `side.show(side.inner)` works.
- Parts register in the current scope under their name, so `d.face` works
  without assigning it, and paths come for free. [proposed]
- The language's naming is structural, by construction. The geometric resolver
  below is a separate tool for hand-modeled bodies and Copy Path; its heuristics
  do not leak into the language. [proposed]
- Rules for finding named geometry on a body [proposed, tested read-only on
  Planung, see below]:
  - nearest direction wins; a face at 45 degrees is an error, not a guess;
  - the outermost face wins when several point the same way;
  - a side is a plane and may consist of several coplanar faces;
  - an edge is the line where two side planes meet; the real edges are found
    along it (there may be none, because of chamfers, or several);
  - `inner` and `outer` mean toward and away from the module's centre.
- Geometry made by an operation takes the operation's name (`left.toekick.top`).
  A side made by a reference takes the reference's name (`batten3.floor_profile`).
  [proposed]
- Mirroring is a placement option of a module (`mirrored=True`) and nothing
  more: mirrored parts come out of the layout step like any other. [decided
  2026-10-10, replacing the earlier view that mirrored modules never occur]
- Wanted helpers [proposed]: a command that copies the path of the current selection
  to the clipboard; nested copies of parts carry the full path as body name, which
  is also the part label at the machine.

### Primitives

- **Board**: sheet material. Thickness comes from the material. The outline is a 2D
  shape, mostly a rectangle. Other shapes are made by union and difference of 2D
  shapes. [decided]
  The composition happens in 2D before thickness is applied, so a board is flat by
  construction. Grain is required whenever the material has grain, as an axis in
  module space, with a scope-level default; defaulting by longer side is wrong
  for fronts. [proposed]
- **Slat**: solid wood defined by cross-section and length. It has no canonical top
  or bottom. [decided]
  Its faces are named by direction once it is placed. It goes on a cut list by
  length instead of into a nest; typical operations are end cuts and miters; grain
  runs along the length. Board versus slat is a matter of stock form, not species:
  a glued-up solid wood panel is a board. [proposed]
  Spelling [proposed]: `slat(name, material, section=(w, h)).on(face_a,
  face_b).between(start, end)`. The two faces in `on()` pin the two lateral
  axes, the way `on()` pins a board's thickness axis, and `between()` gives the
  length. A slat's own faces are named by direction like a board's. End cuts are
  `.miter(end, angle)`; holes and pockets work as on a board.
- **Operations on a board** [proposed]: `cut` (through, changes the outline),
  `pocket` and `hole` (2D shape plus depth plus face). This list per board is the
  layout. Operations on a narrow face can be written (`side.front.right(50)`
  as an anchor) and are emitted, but no joint or connector uses them: the
  3-axis machine cannot reach a narrow face, so every connector is machined
  from the big faces of both boards. [decided 2026-10-11 by Florian,
  replacing the earlier "Domino, Cabineo, screws into an edge" on narrow
  faces] The box joint's grooves along its fingers are the one exception,
  as the add-in models them (see "Box joints" under Joints and hardware).
- **Cutting with a part or a box** [decided 2026-10-10]: `side.cut(floor)`
  removes the region the floor occupies inside the side, its outline through
  its thickness; a pocket from the face the region enters through, or a
  through cut when it passes the whole thickness. `cut(box)` does the same
  with a box. Room for a fit is stated on the region, not on the operation:
  `side.cut(floor.box().grown(top=0.5, left=0.5))`, so the gap is explicit
  per side and the operation stays a plain cut. A part as a `between()`
  limit means its face toward the board (see "Placement and references");
  `part.into(n)` and `part.gap(n)` move it.
  A drawer floor's grooves are the `groove` joint now [2026-10-12], which
  grows the floor into the boards and cuts what it then occupies in each
  (see "Grooves" under Joints and hardware).
- **Cutouts** [decided and implemented 2026-10-11; `lang/core/cutouts.py`,
  `Board.cutout`]: what the Face Cutout add-in (cutouts_native) does, as an
  operation. `side.cutout()` cuts out a big face inside a `border=` (20),
  keeping `around=` (20) mm of material around everything the board has so
  far: its holes and through cuts, pockets and holes in either big face,
  holes into its narrow faces, V-grooves. `pattern=cross(width)` leaves two
  diagonal bands, `pattern=triangles(columns, rows, spacing)` a lattice of
  triangles with a true gap between them (`aligned=True`: each rounded tip
  reaches the next row's base line; `along=` the extent the columns run
  along, the longer side by default; `start=` the corner, by default the
  bottom, front, left one). `radius=` (8) rounds every corner of the
  openings, `chamfer=` puts a 45 degree chamfer on their rims at the face
  cut from, `depth=` makes it a pocket (`to(side.outer, -3)` leaves 3 mm),
  and a region shape with `at=` limits it to part of the face (the add-in's
  Bounding Box Points). Its defaults and the patterns' sizes are
  `lib/cutout_patterns.py`, which the add-in now reads too. Decided with
  Florian:
  - the default face is the big face that is not the show face, the inner
    face by default: usually the machined one, and the chamfer stays off
    the visible face;
  - Rhombuses, tabs and patterns at an angle to the board's edges are left
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
  The geometry follows the add-in's tool bodies: the outline inset, less
  the material kept, the pattern clipped to that, then every corner
  filleted. Offsets keep sharp corners, as Fusion's sketch Offset does
  (round joins gave rings with radius-20 corners where the add-in has
  sharp ones that its fillets round with 8). Fillets are worked out on the
  lines and arcs the polygons stand for, cusps included, so the arcs are
  exact. Verified in Fusion against the add-in on the same boards (full,
  cross, triangles, aligned triangles, a pocketed cross, each with a hole
  and a pocket kept): zero boolean difference both ways and identical face
  counts; `examples/cutouts.py` compiles with 71 features in 0.6 s.
- **Positioning an operation, `at=`** [decided 2026-10-10]: an operation is
  positioned on a face by an anchor named through that face:
  `side.outer.bottom.front` is the corner, `side.outer.front` the middle of
  the front edge, `side.outer.center` the centre, and the shape's matching
  side or corner is placed on it, so `.cut(rect(depth=60, height=100),
  at=side.outer.bottom.front)` is a toe kick notch. Distances follow the
  edge they are measured from, `side.inner.front(37).bottom(z)`, and a
  position from the reference algebra may stand in for a distance, which is
  how a hole lines up with another part. Patterns come from `spread()` along
  one axis of the face (`pitch=` or `count=`, not both).
- **Depths** [rules fixed 2026-10-12]: `depth=` is a number, `through` or
  `to(face, offset)`. Through and `to()` measure the board from the face
  the operation is on to the opposite face: its thickness from a big face,
  its length or width from a narrow one, so a hole through a board's front
  edge runs out at its back edge (the layout used to write the thickness
  there, and the preview drilled 15 mm where Fusion drilled across). A
  depth past the opposite face, or `to()` with a positive offset, is an
  error; `to()` names a face of the board the operation is on, and a face
  of another part is an error. A V-groove cannot be chamfered.
- **Shapes name their extents** [decided 2026-10-10]: `rect(depth=60,
  height=100)` says which plane it lies in and reads the same on every face;
  placing it on a face in another plane is an error. `circle(d)` has no
  orientation; `polygon(points)` is the raw escape hatch in the face's
  (u, v), its two world axes in x, y, z order.
- **Chamfers** are modeled geometry: along outer contours, along pocket contours,
  and on holes. [decided]
  A chamfer belongs to a contour on a face. Operations from two big faces, of any
  kind, mean the board must be flipped on the machine. [proposed]
  Spelling [decided 2026-10-10]: `.chamfer(what, size)`, where `what` is an
  edge (`side.front.inner`), a face's outline (`side.outer.outline`), or a
  named operation (`side.toekick`). `.cut()`, `.pocket()` and `.hole()`
  accept `chamfer=` as sugar for a chamfer along their own contour.
  The constructor takes no chamfer; a build-wide default such as "1 mm on the
  outline of every show face" is a rule in `rules.py`.
  An edge through the board, where two narrow faces meet
  (`panel.front.left` on a board lying flat), is a corner of the outline,
  so its chamfer cuts the corner off the outline, `size` along both edges,
  as `fillet()` below rounds one [implemented 2026-10-12]. It used to be a
  Fusion chamfer on that edge: the solid came out right, but
  contacts, crossings and `no_interference` saw the square corner, and
  where a cut had taken the corner the preview cut nothing and the emitter
  only reported that it found no edge. `.chamfer()` takes a list too.
  A chamfer is 0 (none) or at least 0.01 mm (`ops.MIN_CHAMFER`), however it
  is made [Florian, 2026-10-13]: Fusion failed on fuzz boards' chamfers of
  6e-5 mm. A list is chamfered whole or not at all. A chamfer must be
  smaller than the depth of what it bevels (a pocket's or a hole's depth,
  the thickness for an edge, an outline or a cut's rim), and smaller than
  the wall it bevels where a pocket, hole or V-groove from the other face
  runs out under its rim and leaves the wall the thickness less its depth
  (one through the board leaves no wall there, and the chamfer stops at
  it). A chamfer along an edge that is gone (corners rounded with half the
  board's width, a cut across all of it) is an error. [found by fuzzing
  and in Fusion, 2026-10-13; see the status at the end]
- **Roundovers** are not modeled. [decided]
  They can be a note on an edge that shows up on labels and work lists. [proposed]
- Corner radii are properties of the 2D shape, so a pocket's inside corner equals
  the cutter radius by construction and no 3D fillet feature exists. Chamfers and
  holes map to Fusion's features. [proposed; "fillets" in the original wording
  meant these corner radii]
  `shape.rounded(r)` [implemented 2026-10-12] rounds every corner with r,
  convex and concave alike (the inside corners of a cut in the shape and of
  a board with it as its outline), with exact arcs, as the cutouts' fillets.
  Half the narrow width rounds the ends fully, so `rect(depth=80,
  width=12).rounded(6)` is a slot; a larger r, or one too large for an
  edge between two corners, is an error, and so is any operation given a
  shape without area (it used to do nothing, silently).
  Anything that does not fit the flat model goes through the escape hatches
  below; that flags the part as no longer plain flat work. [proposed]
- **Fillets** [implemented 2026-10-12; `lang/core/corners.py`,
  `Board.fillet`]: `board.fillet(what, radius)` rounds corners of a board's
  outline, through its thickness, as the router cutting the outline leaves
  them; Florian asked for it the same day ("Not the long edges running
  around the top face of the board, but to change the shape of the
  board."). `what` is a corner named as the edge where two narrow faces
  meet (`panel.front.left` on a board lying flat, `side.front.bottom` on
  one standing), a named through cut (`panel.notch`: every corner it made
  in the outline, the inside one too), a big face's outline
  (`panel.top.outline`: every corner of the outer boundary, not those of
  its holes), or a list of them, which are rounded together. A convex
  corner loses material, a concave one gains it; the arcs are exact and
  tangent to their edges, lines or arcs, worked out as `rounded()` works
  them out. Chosen while implementing:
  - It changes the outline at once, as a cut does: everything after it meets the rounded
    corner, contacts and the joints made on them (a connector keeps to the
    shorter contact), crossings, `no_interference`, cutouts, dog bones (a
    rounded inside corner gets none). Nothing new reaches the layout: the
    preview extrudes the outline, and the emitter recovers its arcs (see
    "Arcs" under Backend), so Fusion gets one cylindrical face per corner
    and no fillet feature.
  - Errors: an edge along a big face (`panel.front.top`, a roundover,
    which stays unmodeled; chamfer it); a corner the outline no longer has
    (a cut, a joint or an earlier fillet took it; the corners a cut made
    are named by the cut); a radius too large for the edges at a corner,
    or for two neighbours together; an arc running into a through cut; and
    an arc taking material where an operation made before it lies, such as
    a joint's holes at that corner. So a corner where a joint goes is
    rounded before the join, which then keeps clear of it.
  `examples/operations.py` rounds a corner of a board lying flat, one of
  a standing board and the corners of a notch, and cuts a corner off. The
  emit plan has them as true arcs, tangent to their edges (tested).
  Verified in Fusion 2026-10-12 on that example: each rounded corner is
  one cylindrical face of its radius about the arc's centre, the cut-off
  corner one face at 45 degrees, the volumes within 0.002 % of the
  preview's. Kept as chosen [decided by Florian 2026-10-12]:
  a chamfer on an edge through the board changes the outline instead of
  making a Fusion chamfer; a fillet or chamfer cutting into an earlier
  operation at its corner is an error; corners are not named by a point
  (`panel.top.front(60).left(40)`) until a build needs it, so the corners
  a joint adds to the outline (tenon shoulders) are reached only through
  the whole outline.
- **Polygons** [proposed]: clip a rectangle's corner; trim by reference planes with
  `between`; walk an outline step by step; a raw point list as escape hatch.
  `shape.clip(top=380, back=120)` [implemented 2026-10-12, replacing
  `clip("top.right", top=..., right=...)`] cuts off the corner where the
  two named edges meet, each value the length of the cut along that edge;
  a rectangle's edges are named as the frame names its plane, a raw shape's
  left, right, bottom and top.

### Placement and references

- A module is a box with six named sides. Boards sit `on` a side or reference and
  are trimmed `between` neighbours, so most parts carry no dimensions of their own.
  `interior.split()` divides space, for example into drawer bays. [proposed]
  `interior` is the box inside the boards lying on its sides that cover the
  side's middle (a carcass side, a bottom between the sides, a back); a
  foot or a cleat in a corner does not count. [2026-10-12]
- Which side the thickness goes: `.on()` a module side puts the thickness
  inward, also a side moved into or out of the box (`on(cab.bottom.into(60))`);
  `.on()` a bare plane requires a side. Limits missing from `.between()`
  default to the enclosing scope's box. When a part is given as a limit, its
  face toward the board is meant: the face toward the other limit on that
  axis, or toward the middle of the enclosing box when it is the only one;
  the board then lies on the far side of that face from the part. A single
  position as a limit leaves the board on the side of it the box's middle is
  on. [proposed; the rule for two limits fixed 2026-10-12: it used to judge
  every part against the box's middle, so a shelf between two partitions
  on one side of the middle ran through the second one] A box as a limit
  gives both ends on each in-plane axis, `between(drawer_box)`. A limit that
  limits neither in-plane axis (a position on the thickness axis, a board
  parallel to this one) is an error rather than being dropped. So are limits
  that leave it open where the board lies, each error naming what is
  ambiguous [decided by Florian 2026-10-14; they put the board inside its
  limits, or on the side the world frame chose]: the same board twice on an
  axis; two boards overlapping each other on it (nothing lies between them);
  a position, or a board's face moved by `gap()`, lying inside a board given
  as another limit, past what its `into()` reaches; a single limit at the
  middle of the box (the board could lie on either side); and a board as the
  only limit whose middle is the box's (not clear which face is meant).
- The constructor is `board(name, material, shape=None)`; the placement
  modifiers are `.on(ref, toward=)`, `.between(*limits)`, `.center(pos)`,
  `.inset(n)`, `.grain(along)`, `.show(face)`, `.manual()`. A board made of
  a shape is placed by its limits [decided by Florian 2026-10-14]: between
  two limits on an axis it fills them less its inset, or it is an error
  naming both widths; with one limit it sits against it, on the side the
  board would lie; with none, at the scope's front, left and bottom side (or
  the origin without a box); and its box is its outline's. (It sat at the
  limits' or the box's lowest corner in world terms with its box the
  limits', so in a cabinet facing elsewhere it lay elsewhere, and its box
  could miss it.) `.inset(n)` shrinks
  the outline by `n` on every side of its box, which is how an inset front
  gets its gap; there are no one-off modifiers such as margin or lift,
  because `.on(box.bottom + slide.recess)` already says lift. [proposed]
- A box exposes its sides as positions (`box.left`, `box.top`) and its lengths
  as `box.width`, `box.depth`, `box.height`, which measure along the
  left-right, front-back and top-bottom axes of the box's frame. Where an
  extent is an argument it is one of those three names, checked by the type
  checker: `bay.split("height", 3)`, `.grain("depth")`. Axis letters do not
  appear in build files. [decided 2026-10-10]
- `split("height", 3)` makes equal bays; `split("height", [230])` cuts a
  230 mm bay off and returns it with the remaining space, which is split
  again: `first, rest = space.split("height", [230]); rest.split("height",
  2)`. Several sizes work the same, the remainder last. No "fill the rest"
  marker: the steps say it. Bays run from bottom to top, left to right,
  front to back in the box's own frame. [decided 2026-10-11]
- Strings in the API are either names checked as literals by the type
  checker (`width`/`depth`/`height`, `"inner"`/`"outer"` in `show()` and
  `to()` for the chained form) or lookups for computed names
  (`box.side(name)`, `part.face(name)`); everything else is an object: box
  sides (`show(cab.front)`, `on(pos, toward=cab.top)`, `grain(cab.top)`),
  faces, edges, anchors, operations. Side keywords (`shrunk(left=5)`,
  `with_sides(front=...)`, `Box.from_sides(...)`) are explicit parameters,
  so a misspelt side is a type error. [decided 2026-10-10]
  Enums instead of these literals were considered and dropped
  [2026-10-12]: Python has no `.height` shorthand, so `Extent.HEIGHT`
  would be noise, catalog names such as "4x20" or "8 M6" cannot be
  identifiers, and pyright already completes a `Literal`'s values once
  the quote is open (checked against its language server: exactly the
  three extents in `split("|")`, the sixteen sizes in `domino("|")`; an
  enum parameter got the whole scope). Since the preview builds without
  the type checker, every such value is also checked at run time
  (`errors.one_of`, reading the allowed values from the `Literal`), so a
  misspelling is a `LangError` naming the call and the choices; tests
  keep the connector literals equal to `lib/connector_data.py`.
- Contour limits: a contour in the part's own plane bounds the outline directly;
  a contour in a perpendicular plane must hold the part over its whole
  thickness: its section across that plane, from one big face to the other,
  keeps clear of the contour [changed 2026-10-14, after fuzzing: it was
  sectioned at both big faces only, the tighter result winning, so a notch
  between them let the part run into it]. Both are polyline math on the snapshot (`lang/core/contours.py`). [implemented
  2026-10-11; the rules below were chosen while implementing and confirmed
  by Florian the same day]
  - In the part's plane, a closed contour is intersected with the outline
    and its bounds stand in for missing limits. An open contour is an edge:
    it limits the axis across its chord (first to last point), the part
    keeps the side its other limit on that axis is on (or the middle of its
    room), and the edge follows the contour; a chord at 45 degrees, or the
    other limit within the contour's reach, is an error.
  - In a perpendicular plane, a closed contour gives a stretch on the axis
    the two planes share; an open contour gives a position there, and must
    cross each face once. The position is the part's end on the contour's
    side: the part lies on the side its other limit on that axis is on,
    without one on the side of an open contour in its own plane on that
    axis, else in the middle of its room; a clearance reaching past the
    other limit is an error, and so are two open contours across a part on
    one side of it. [chosen 2026-10-14 while fixing what fuzzing found,
    confirmed by Florian the same day] Where the contour leaves several stretches (a
    batten along the wall, cut in two by a wheel arch), the part's limits
    on that axis pick one: a single limit the stretch it lies in, two
    limits the one between them, and two limits spanning several stretches
    are an error naming them, since a part is one piece. So the two pieces
    of an interrupted batten are two parts, each given one end:
    `between(..., floor_outline, floor_front)` and `... floor_back)`.
    [decided 2026-10-11]
  - An open contour must run one way: along its chord's axis in the part's
    plane, and through the part's thickness in a perpendicular plane. Run
    from its first point toward its last, no point may lie more than 0.01
    mm behind the furthest the contour has reached along that axis (nothing
    narrower is meant, and the snapshot rounds points to 1e-4 mm); one that
    does runs back along itself, an overhang such as a lip, and is an error
    that says to draw the lip as a closed contour. The whole contour counts,
    whichever part takes it. [decided by Florian, 2026-10-14]
  - `contour.gap(n)` keeps n of clearance, measured in the contour's plane
    with round joins, so it is exact at corners (GEOS offsets the area given
    in one form, without points along its edges, so the same contour gives
    the same part however its points run; the clearance is at least n and
    up to about a hundredth more, which is accepted [decided by Florian,
    2026-10-14]); `contour.into(n)` reaches
    past it. Stretches from closed contours cut every other range down
    (tighter wins). A contour that splits the part in two, leaves nothing,
    lies in a tilted plane or is not planar is an error.
  - The part's box is the bounds of what the contours leave, so a batten
    whose lower edge follows the floor profile has its `bottom` at the
    profile's lowest point.
- Anywhere a length or a position is expected, a reference can be given instead of
  a number. This replaces the extrude options Florian uses a lot in Fusion (start
  from offset or from object plus offset, extent to object plus offset).
  [decided as a need; the spelling below is proposed]

  | Fusion extrude option       | In the language                              |
  |-----------------------------|----------------------------------------------|
  | Start from offset           | `.on()` a reference, moved with `+`/`-`      |
  | Start from object + offset  | the same; the reference is the object        |
  | Extent to object + offset   | `.between()` for parts, `depth=to(...)` for cuts |
  | Extent through all          | `depth=through`                              |

- References can be computed with, for example `(bottom.top + top.bottom) / 2`.
  [decided as a need; the rules are proposed]
  - position +/- length gives a position;
  - position - position gives a length;
  - a weighted mix of positions whose weights add up to 1 gives a position,
    also with positions taken away: `a + b - c` [decided by Florian
    2026-10-14; it was a TypeError]; a length taken from a sum of positions
    whose weights do not add up to 1 is an error saying so;
  - anything else (a bare sum of two positions, mixing axes) is an error.
  This only works for flat, parallel references.
- `+` and `-` move along the world axis (`cab.bottom + 60` is 60 inside only
  where the world's top is its axis's positive end, the van's). Fits that
  hold in any frame use `.into(n)` and `.gap(n)`, which need no sign
  convention and also work on contours, by offsetting the curve; on a box
  side they give a side, its inward direction kept, so a board lies on them
  without `toward=` [decided by Florian 2026-10-14]. [proposed]
- A cut starts at the face of the board it is declared on. One extrude through two
  panels becomes a loop over both. [proposed]

### Master document

- One master per van build, holding planes, base boxes and shapes that the modules
  refer to. Optionally one reference document per module for extra hand-drawn
  geometry. Everything else is generated on top. [decided]
- Four kinds of reference [decided 2026-10-11]: planes, which give a
  position; contours, which give a shape to follow; placeholder boxes, rough
  bodies drawn in the master to divide up the room, which become module
  boxes (`cabinet("kitchen", van.box("Kueche"), front=...)`); and the
  master's user parameters, which are plain numbers (`van.param("Bodenhoehe")`).
  A box's front is stated in Python at placement, never read from the master.
- Naming uses what is visibly named in Fusion: one construction plane per plane
  reference, one sketch per contour (the sketch name is the reference name),
  one component or body per box, one user parameter per number. No hidden
  tags on single curves. The snapshot takes everything in the master; a name
  starting with a double underscore (`__temporarySketch`) is left out.
  Duplicate names are an error. [decided 2026-10-11]
- The master's axes are the world axes. Which world axis is front, left or
  up is a per-project choice made in the build file with `set_frame(Frame(...))`;
  the planning documents use front = -x, left (driver's side) = -y, top = +z.
  [decided 2026-10-11] Every build starts from that default frame
  (`registry.reset()` restores it); `world_frame()` reads the frame in use
  (the language no longer exports a `frame` object, which `set_frame` left
  stale in a build file that imported it).
- `master.py` is an index that binds those names and says where exceptions apply.
  Compile fails early on a missing name, a duplicate name, or a sketch with more
  than one chain of curves. [proposed; the errors are implemented, exceptions
  such as `replace` below are not]
- A module refers only to the master, to its own parts, and to what other modules
  export. The kitchen reads the floor's top from the floor module in Python, not
  from a hand-moved plane in the master; `build.py` orders the compiles. Fusion
  documents stay independent because the dependency exists only at the Python
  level. The master holds vehicle facts, which is what a hand-made document is
  good at; `master.py` may also hold plain measured numbers where nothing needs
  drawing. [proposed]
  Spelling [proposed]: inside a module, `cab.export("worktop", top.top)` publishes a
  reference; a module function returns its module object, and the importer reads
  `kitchen.worktop`. An export cannot take a name that a scope already
  answers to (a direction or alias such as `top`, an extent, an attribute
  such as `interior` or `mount`), since `cab.top` would hide it
  [2026-10-12]. Modules import the build's master index as `van`
  (`from . import master as van`), which is the name the examples use.
- The snapshot is the compile's only view of the master. It holds planes
  (origin and normal), contours as polylines sampled at 0.1 mm with a closed
  flag, boxes (min and max; a body that is not an axis-aligned cuboid is
  exported as its bounding box and flagged), user parameters (value in mm and
  expression), and later the vehicle mesh. Faceting on curved contours is
  accepted for now; arcs can be carried exactly later. The file carries its
  own hash and the source document's name; a layout records the hash of the
  snapshot it used. [decided 2026-10-11, tolerance included]
- Writing it [implemented 2026-10-11]: the compiler add-in's Snapshot Master
  button runs `lang/emit/snapshot.py` on the active document and saves
  `snapshot.json` (shape in `lang/core/snapshot_types.py`; the Fusion-free
  half, `lang/emit/snapshot_format.py`, chains curves, collects names and
  hashes, and is unit tested). Rules chosen while implementing, confirmed
  by Florian 2026-10-11 (naming changed to paths then):
  - items in components are taken in world coordinates, through the
    occurrence they are reached by;
  - items in the root keep their names; items inside components are named
    by the dotted path of component names from the root, then their own
    name (`Bett.oben`, `Moebel.Sitzbank.Sitz`); a component's only body
    takes the component's path (`Moebel.Kueche`), since Florian names the
    components of placeholder bodies and leaves the bodies as Body1; user
    parameters belong to the whole design and have no path;
  - a component whose name starts with `__` is left out with everything in
    it; linked components are left out, since they belong to other
    documents;
  - sketches drawn only to make a body count as contours like any other,
    so they are named `__...` to leave them out (no guessing from hidden
    or consumed sketches);
  - a sketch's construction curves do not count; the rest must form one
    chain without branches; a curve no longer than the join tolerance
    (0.01 mm) is a point its neighbours meet at, and a closed chain of
    fewer than three points (a line drawn twice) is a problem, "the curves
    close around nothing" [found by fuzzing, 2026-10-14]; the places of a
    name made twice are listed in order;
  - surface bodies, duplicate names (per kind: a plane and a sketch may
    share a name) and sketches that are not one chain are listed as
    problems in the file instead of failing the snapshot, and using such a
    name in a build is an error that repeats the problem;
  - the hash covers the content, not the document's name, and the file is
    deterministic (rounded to 0.1 micrometre, sorted, one point per line),
    so an unchanged master gives an unchanged file.
- Reading it [implemented 2026-10-11]: `van = master("snapshot.json")` in
  the build file (a relative path starts at the calling file's directory,
  or at that of the file given as `relative_to=`, for a helper that reads
  the master on its callers' behalf),
  then `van.plane(name)`, `van.box(name)`, `van.param(name)` (mm for
  lengths, degrees for angles), `van.contour(name)` (`lang/master.py`). A
  plane is a `Plane` that acts as a position (`on`, `between`, `spread`,
  arithmetic) when it is axis aligned and is an error when a tilted one is
  used as one. A box that is only a bounding box adds a note to the
  layout's problems. A missing name is an error that suggests close
  matches. The layout carries the snapshots it read (file, source, hash,
  boxes, contours), and the preview draws the boxes as translucent ghosts
  with their names and the contours as lines (`m` toggles them). Checks:
  `inside_box` keeps a module's parts inside its box, `inside(contour,
  gap=)` keeps them inside a closed contour seen along its normal (a part
  in the contour's plane by its outline, any other by its outline's extent
  and its thickness), both by where the material lies, so a tenon or a box
  joint's fingers past the placement box count and an end cut away does
  not [decided by Florian, 2026-10-14]; a part may reach 1e-6 mm out
  (`inside()` also needs more than 1e-6 mm2 outside).
- The sample master is built by `tools/van_master.py` in Fusion (rebuild it
  rather than keep a saved document); its snapshot is
  `examples/van_snapshot.json`, the test fixture, and `examples/van.py` is
  the worked example below.

### Joints and hardware

- The joint and hardware vocabulary is this repo's add-ins: tenons with dog bones,
  box joints, Domino, Clamex, Cabineo, screws, concealed hinges, hatch hinges,
  drawer slides, ball catches, door latches, face and pattern cutouts. [proposed]
- Split each add-in into three layers [proposed]:
  1. settings: what the dialog collects today (also what `lib/group_edit.py`
     already stores per result);
  2. layout: pure Python that turns settings into holes and slots at positions and
     depths on a face (`lib/drawer_slides.py` already is this);
  3. emitter: creates the Fusion features.
  The dialog and the language then share layers 2 and 3.
- The compiler targets the generic emitter, not the add-ins' emitters. Those are
  built around a selected edge, constrained sketches and dialog previews, none of
  which the compiler needs, and the constrained sketches cost writes. Layer 2 is
  extracted from each add-in over time, as `lib/drawer_slides.py` already is.
  Headless add-in calls are at most a stopgap for the first joint. [proposed]
- A joint is a relation between two parts along the rectangle where they touch.
  The concept has a name, **Contact** (`lang/core/contact.py`): a board that
  meets another edge-on, one of its narrow faces on the other's big face.
  It holds both parts, the two faces, the axis along the line where they
  meet and the rectangle: along that axis where the edge-on board's end has
  material and the other board's outline covers it, across it the edge-on
  board's thickness as far as the other board covers it (`across_lo`,
  `across_hi`); a connector stays where the edge-on board's thickness puts
  it and is an error where it would reach past the other board's edge
  [2026-10-12]. Exact for outlines (a toe kick notch in the side
  shortens the bottom's contact); an end interrupted by a notch gives one
  contact per piece. Pockets do not shape it, but a board meeting another
  across a pocket, hole or V-groove made before, in the face it lies on or
  in its own end, is an error, as across a cutout's opening: make it after
  the join [Florian, 2026-10-13]. What joins made does not count (joins go
  across each other's: screws in the tenons' gaps, a drawer's floor in its
  groove past a box joint's reliefs). A contact narrower than 0.01 mm
  either way is none. Joint layouts take a contact plus settings and
  return operations for both parts. [implemented 2026-10-11]
- Besides contacts there are **crossings** (`lang/core/crossing.py`): two
  boards in perpendicular planes whose material passes through each other,
  like battens across and along a floor. They share one axis, the line
  their planes meet along; each board's material at the other's thickness,
  projected onto that axis, gives the height they share. `no_interference`
  uses this too, so lapped boards are not reported. [implemented
  2026-10-11] Boards in one plane overlap only where their material does,
  so a hatch with rounded corners in a rounded opening is not reported
  although its box reaches into the opening's corners. [2026-10-12]
  Hardware is checked too [decided by Florian, implemented 2026-10-12]:
  `no_interference` reports a hardware body whose boxes reach into a
  part's material (`cab.drawer1.runners.left overlaps cab.drawer1.back`)
  and two hardware bodies whose boxes overlap, of one item or of two; a
  body is the union of its boxes, so its own boxes may overlap. An overlap
  counts where it is deeper than 1e-6 mm in every direction, in a board's
  plane as across its thickness, and touching is within 1e-6 mm, as in
  `inside_box` and `inside()` [decided by Florian, 2026-10-14; the material
  was cleaned before, which took out overlaps narrower than 0.01 mm in a
  board's plane while ones as thin across the thickness counted]. A part's
  material is its outline minus its pockets and holes, looked at slab by
  slab between the ends of their ranges along the thickness, so a latch in
  its hole, a runner's coupling in the front board's cut-out, or a pin
  through a pocket from one face and a hole from the other is not
  reported; boards across each other are looked at cell by cell, where the
  stretches each has material along the axis their planes share must
  overlap. A hole is its circle within a quarter of the tolerance (up to
  430 mm across); a pocket's or an outline's arcs are their polygons, so
  something touching such an arc from inside meets the chords' slivers, up
  to 3.8e-5 r deep, and counts. Not looked at yet: material past the
  placement box (tenons, fingers, a floor grown into its grooves) and
  pockets and holes in narrow faces; looking past the boxes would report
  every box joint, whose fingers clear each other only through their
  grooves in narrow faces, so both come together [Florian, 2026-10-14].
  The examples are clean.
- The first joint is the **half lap** (`lang/joints/laps.py`) [decided and
  implemented 2026-10-11]: `long.join(battens, using=half_lap(toward=
  floor.top))` laps the board with each board named, all of which it must
  cross, each reaching through the other's thickness (one ending inside
  the other, short of its far face, would leave the notch cut through the
  other open there: an error [Florian, 2026-10-13]). Its own notches open
  toward `toward`, the other boards' the opposite way;
  the split lies in the middle of the height both share at each crossing
  (`split=` a position instead), and `clearance=` is the play in each
  notch in total, half on each side (default 0), as with tenons and box
  joints [2026-10-12; it was per side, and the split was `at=`]; the
  settings after `toward` are keyword-only. Each notch is a through cut named `lap_<other board>`, so
  the emitter needs nothing new. Its two inside corners at the floor get
  dog bones as part of the notch's cut [implemented 2026-10-12, see "Dog
  bones" below]: `dogbones="corner"` (default, as on tenons [decided by
  Florian 2026-10-12]), `"hidden"`
  (centred on the floor, touching the notch's side, bulging past the
  floor into the half of the crossing that stays this board's, where the
  other board covers it on both faces; the notch must be wider than the
  relief) or None; `tool=6`, `relief=0.1`. `Board.join(*partners, using=joint)`
  hands the board and the boards named to the joint object (the `Joint`
  protocol in `part.py`), as `Scope.mount` does with hardware, so core
  knows no joint types. The join happens when it is called: the boards it
  joins must exist by then.
- Joinery rules are dropped [decided 2026-10-11 by Florian]: which
  connector goes where is hard to formalize, so joints are stated one call
  per board. The earlier proposal (a predicate list, first match wins, as in
  Polyboard's manufacturing methods) is not pursued.
- Joint types are objects with their settings, `tenons(count=3)`,
  `box_joint()`, `domino("5x30", count=4)`, `cabineo(count=2)`,
  `clamex(count=2)`, `screws(count=4)`, `groove(depth=5)`. Connectors are
  joint types, not an option of tenons, which is what the first draft's
  `connector=` implied. [decided]
- **A join names its partners** [decided 2026-10-11 by Florian]:
  `bottom.join(left, right, using=cabineo(count=3))`, partners one by one
  or in lists (`long.join(battens, using=half_lap(...))`), the joint as the
  required keyword `using=`, so the type checker catches a missing joint.
  Nothing is joined that is not named: an earlier version joined every
  board the receiver touched, which Florian rejected in favour of stating
  each connection. Every board named must meet the receiver the way the
  joint needs (a contact for a connector, a crossing for a half lap), else
  the join fails naming it, and a failed join changes no board. A board
  named twice, or the receiver itself, is an error. A connector join may be
  written from either board, since the contact says which one meets the
  other edge-on: `left.join(bottom, top, using=...)` equals the two joins
  from the bottom and the top. A half lap stays relative to its receiver
  (`toward=` is where the receiver's notches open). Where a board crosses
  only some of a list, the build picks them, e.g. the van floor's
  interrupted battens join `[b for b in battens if b.box().overlaps(
  piece.box())]`, the battens on their side of the wheel arch.
- **Connectors** (`lang/joints/connectors.py`) [implemented 2026-10-11]:
  `bottom.join(left, right, using=cabineo(count=3))`,
  `back.join(left, right, bottom, top, using=domino("4x20", count=2))`,
  `top.join(right, using=clamex("P-14", at=[...]))`. Along each contact the connectors sit at `count=` stations, the outer ones `end=`
  from the contact's ends (37 for Dominos, the machine's stop latches; 60
  for the others, the add-in's default), or at the positions `at=` (a
  list, also for one). `end=` given with `at=`, `gaps=` or `count=1`, which
  would ignore it, is an error, as is tenons' `margin=` with `at=` or
  `count=1`. What each connector makes must lie within its contact, along
  it and across it (Clamex guide holes, a Cabineo pocket, every Domino slot
  at its own length) [2026-10-12; Clamex and Cabineo could drill past the
  board's end before]. Every operation is on a big face:
  - `domino(size, ...)`: a slot in the face-on board, centred on the
    edge-on board's thickness or `fence=` from its reference face (the show
    face unless `face=`), half the Domino's length plus 0.5 deep or
    `remaining=` short of the far face; `loose=` lengthens all slots but the
    first (front, left or bottom) per contact. The edge-on board's mortise
    is cut with the Domino machine, which is lined up by a mark: a 90 degree
    V-groove in the edge-on board's reference face, 0.3 deep, running 4 in
    from its end (it starts 1 mm outside the board so it runs out cleanly),
    one per Domino by default; `marks="middle"` leaves out the first and
    last, which the machine's end stops locate, `marks=None` all of them.
    The marks are the layout's `vgroove` operation (`Board.add_vgroove`): a
    straight V-groove from a start to an end point on a big face, a depth,
    ends cut square; the emitter cuts its triangular cross-section along
    the line, the preview subtracts the prism. Auto Setup recognises such a
    groove (two 45 degree flanks, a sharp bottom edge) and traces it with
    the V-bit.
  - `clamex("P-10" | "P-14", ...)`: the access slot or hole in the edge-on
    board, half its thickness deep, two guide holes 101 apart in the other.
  - `cabineo("8" | "12" | "8 M6", ...)`: three overlapping 15 mm holes,
    10.5 deep, in the edge-on board, open toward its end, and the screw hole
    in the other, 5 mm from the access face across the edge-on board's
    thickness; `insert=` for the 8 M6, `surface="flush"` or `"anti-break"`,
    `through=`.
  The access holes go on the edge-on board's big face that is not its show
  face, unless `face=` names one (`face=cab.bottom`, `"inner"`). With the
  default show face (outer) that is the inner face of a carcass bottom or
  top, which is also where the back's Domino slots are, so each board is
  machined from one side; Cabineos from the bottom's underside would mean a
  flip. The dimensions come from `lib/connector_data.py`, plain data shared
  with the connectors_native add-in (and through `lib/domino.py` with
  tenons_native). Operations are named `cabineo_left_1a` (kind, other
  board, station, letter), the stations numbered across all contacts of a
  pair (`domino_divider_1` to `_4` along a notched end); a second join of
  a pair with the same kind of joint is an error naming both boards, and
  every joint error is reported on the board whose `join()` was called,
  naming the other (`cab.back: cabineo with cab.left: ...`) [2026-10-12]. Round access pockets are hole features; the
  slots' round ends come out as true arcs (see "Arcs" under Backend).
  Verified in Fusion 2026-10-11 against connectors_native on the same board
  pair (Cabineo 8 x 3, Domino 4x20 x 3 with marks, Clamex P-10 x 2): the
  boolean difference between the add-in's bodies and the compiled ones is
  zero both ways for all three, and every body has as many faces as the
  add-in's. The drawer cabinet compiles with 160 features in 0.8 s,
  volumes exact.
- **Tenons** (`lang/joints/tenons.py`) [implemented 2026-10-11]: integral
  mortise and tenon as the tenons_native add-in makes it, spelled like the
  connectors: `shelf.join(left, right, using=tenons(count=3, width=50))`,
  from either board. The edge-on board grows full-thickness tenons out of
  its end, as long as the other board is thick (`remaining=` shorter for a
  blind mortise); they widen its outline (`Board.add_to_outline`), its box
  stays the placement box. The other board gets a mortise per tenon,
  `clearance=(0.1, 0.1)` larger along and across the joint: a through cut,
  or a pocket `extra_depth=0.5` deeper than the tenon. Placement:
  `count=` and `width=` with the outer tenons `margin=30` from the
  contact's ends (one is centred), `even=True` for tenons as wide as the
  gaps, or `at=` centres. Dog bones for a `tool=6` cutter, `relief=0.1`
  wider: `"corner"` (default, on the bisector, through the corner) or
  `"hidden"` (into the tenon's root and past the mortise's ends, covered
  by the shoulder) or None [2026-10-12]; a hidden relief is `tool +
  relief` across, which the mortise across the joint and the tenon's
  length must allow; none where a mortise breaks out of its board or a
  tenon is flush with its board's end (the reliefs' geometry is the
  shared one of "Dog bones" below since 2026-10-12, the layout unchanged
  to the bit). With dog bones, the gaps between the tenons must be at
  least the tool, which routes them, and a corner relief bites 0.15 times
  the tool plus half the relief into a tenon's side at its root, so a
  tenon must be wider than its two bites [found by fuzzing, 2026-10-13:
  tenons 1.1 wide and apart with 8 mm dog bones were eaten, leaving
  islands]. Reliefs and mortises are round
  through cuts and pockets, so the tenon joint needs no new operation; a
  through cut that would split a board in pieces is now an error.
  Florian's choices 2026-10-11: corner dog bones by default; screws and
  Clamex/Cabineo in the gaps between tenons are joins of their own that
  take their stations from the tenons, not options of the tenon joint.
  Verified in Fusion against tenons_native on the same board pair (corner
  and hidden dog bones, blind, even, mortises breaking out of the board's
  edge): zero boolean difference both ways, identical face counts.
  `examples/shelf.py` shows all of it.
- **In the gaps between tenons, and screws** [implemented 2026-10-11]: a
  tenon joint records what it made per contact (centres, width, length),
  and a joint given `gaps=t` joins along those contacts, as they were
  before the tenons changed the outline, one per gap between and beside
  the tenons: `cabineo(gaps=t)` (gaps of at least 40), `clamex(gaps=t)`
  (120), `screws(gaps=t)`. `screws` is a joint of its own (`lang/joints/
  screws.py`): `count=`/`at=` on a plain butt joint, or `gaps=t`, through
  the board that is met from its outer face into the other's end, centred
  on its thickness, `countersink=True` for a 90 degree countersink twice
  the screw plus 0.4 wide (a chamfer on the hole's edge), which must lie
  on the face it is sunk into, as hardware's holes do (`hole_fits`) [found
  in the Fusion batch check, 2026-10-13: 4 mm screws into a 4 mm divider
  flush with the side's edge, whose countersinks reached 2.2 past it];
  `offset=12` puts two beside each tenon instead. `screws(tenons=t)` drills through
  the tenons themselves, halfway along each, one in the middle or two
  `offset` in from its edges, square to the tenon board's faces: only
  where the tenon's face lies open because its mortise runs out of the
  other board's edge, as with a top flush with the sides (Florian: the
  screw is driven through the open tenon into the other board), else an
  error; drilled from that open face. Verified in Fusion against
  tenons_native: gap screws centred with countersink and two-sided,
  Clamex P-10 and Cabineo 8 in the gaps, tenon screws centred and
  two-sided: zero difference both ways, identical face counts. The two
  add-ins cut the Cabineo pocket 10.5 and 11 deep; Florian: 10.5 is right,
  so tenons_native now reads all its Lamello and screw dimensions from
  `lib/connector_data.py` too.
- **Box joints** (`lang/joints/box_joints.py`) [implemented 2026-10-12]:
  the corners of a drawer box as the box_joint add-in makes them, spelled
  like the other joints: `front.join(left, right, using=box_joint(7,
  margin=2, clearance=(0.1, 0.1)))`, from either board. The board that
  meets the other edge-on grows fingers through the other board, flush
  with its outer face (`Board.add_to_outline`, its box stays the placement
  box); the other board gets the notches. The corner must be flush: the
  other board's end in the plane of this board's outer face, covering its
  end, which the joint runs along the whole width of, so cut-outs at the
  joint (a slide's coupling cut-out) go after the join; else the join
  fails naming the boards. The add-in's dialog gives the defaults
  [decided by Florian 2026-10-12: they stay the dialog's]:
  `fingers` 5, the odd count of both boards' fingers together, all
  (length - 2 * margin) / fingers wide; `margin` 0, which widens the outer
  two; `tool` 6; `clearance=(along, across)` (0, 0), which widens notches
  and gaps by half the first per side and cuts their bottoms the second
  deeper than the other board is thick. The cutter's radius stays as
  fillets at the bottoms of the notches and gaps, through the board, and
  every finger is rounded over along its mating corners to nest in them,
  by grooves along it from the end: the fingers' from their tips, the
  other board's along the notch walls, opened square on the notch's side
  in a band one radius deep at the inner face, where the root of the
  finger in the notch is not rounded. Dog bones one radius deep sit in
  both inner faces, on the notch walls at the notch bottoms and on the
  fingers' sides at the gaps' bottoms. Nothing shows on the assembled
  joint; `tool=0` makes a square one. The notches and gaps are through
  cuts (`notch_<other>_1`, `gap_<other>_1`...), the dog bones pockets
  (`notch_<other>_reliefs`, `finger_<other>_reliefs`), the grooves
  pockets in narrow faces (`notch_<other>_grooves`,
  `finger_<other>_grooves`). The finger grooves start at the fingers'
  tips, in front of the board's end, so an operation on a narrow face has
  an `offset` now, how far in front of the face it starts (layout field
  `offset`, `Board.add_edge_pocket`), which the plan turns into the plane
  the cut starts from; the emitter needed nothing new. The preview meshes
  pockets and holes in narrow faces now. Two differences from the add-in:
  a margin smaller than half the clearance along the joint works, the
  outer gaps are cut past the board's ends (the add-in's sketch fails
  there); and where the board's end runs through an outer gap's outer
  fillet (with a clearance across), the fillet has a vertex on the end,
  so that the emitter recovers the piece left of it as an arc. The
  drawer cabinet's drawer boxes are box-jointed, as Florian's Dynapro
  boxes (7 fingers, margin 2, tool 6, clearance 0.1), before the slide's
  cut-outs; their floors lie in the sides' lowest finger, in grooves in
  all four boards (see "Grooves" below).
  Machining [decided by Florian 2026-10-12]: no change to the geometry.
  Florian machines box joints with the boards lying flat and mills the
  finger roundovers step by step with a flat cutter, which works well, so
  the grooves along the fingers and the notch walls stay as the add-in
  models them, cuts from the end planes. (The question was that, with a
  board flat on the machine, the finger grooves are roundovers of the
  edges at its inner face, but the square halves of the notch-wall
  grooves cannot be milled from the inner face with a round cutter.) The
  drawer back stays machined from both faces; only the slide's rear hook
  holes may go through it from its inner face instead (`hook_hole=(d,
  through)`, see the slides below). Verified in Fusion 2026-10-12 against
  the add-in on the same board pair in seven settings (the dialog's
  defaults, Florian's 7 / 2 / 6 / 0.1, square with and without
  clearance, 3 and 9 fingers): zero boolean difference both ways and
  equal face counts; with margin 0 and a clearance the add-in fails (its
  known bug) and the language's joint comes out whole. The drawer cabinet
  compiles with its box-jointed drawers in 1.6 s (208 features), every
  body one solid, no side overlapping its front or back.
- **Grooves** (`lang/joints/grooves.py`) [asked for by Florian 2026-10-12,
  spelled as the other joints; implemented 2026-10-12]: a panel set into
  grooves in the boards around it, a drawer floor in its box:
  `floor.join(l, r, f, k, using=groove(5, clearance=(0.5, 0.5)))`. The
  floor is placed between the boards' faces (`between(l, r, f, k)`), so it
  meets each edge-on (a contact); the join moves each edge of it that lies
  on a named board's face `depth` into that board, a corner between two
  such edges with both, and cuts every board a pocket for what the floor
  then occupies in it, from the face the floor meets, `groove_<panel>`.
  The floor goes into the front and back too, not only the sides [Florian].
  Its box stays where it was placed (`Board.add_to_outline`), as with
  tenons and fingers. Chosen while implementing: the join grows the panel,
  rather than the panel being placed `into(n)` the boards and the join
  only cutting, so the depth is stated once, the placement reads as the
  box's inside (as in the drawer cabinet sketched under Examples), and the
  corners are filled the same way for every board; `side.cut(floor.box()
  .grown(...))` stays for grooves by hand. Either board may make the call
  (`left.join(floor, using=groove(5))` grooves the left side alone,
  `side.join(low, high, using=groove(4))` cuts dados for two shelves); the
  boards at a corner of the panel go into one join, so that the corner
  goes into both, and a later join at a corner an earlier one moved is an
  error. Settings:
  - `clearance=(depth, height)`, (0, 0) by default [Florian: 0 unless
    given; he usually gives 0.5, as the drawer cabinet does]: the groove's
    bottom lies `depth` beyond the panel's edge, and its ends as far beyond
    the panel's corners; it is `height` wider than the panel is thick, half
    of it on either side of every panel, a floor lying flat included
    [decided by Florian 2026-10-12, replacing all of it above a lying
    floor]. The floor stays where it was placed, so the slide's cut-outs
    and hook holes, measured from its underside, stay where they were; the
    groove reaches half the clearance below it. In the drawer cabinet
    (0.5) that leaves a 0.25 mm slit under the floor along the boards'
    inner faces, seen only from below the drawer, and a 0.25 mm step at
    the top of each cut-out's sides, on the inner face, where the groove's
    lower wall (0.25 below the floor) meets the cut-out's top (at the
    floor's underside); the floor rests on the runners' drawer members, at
    the height the slide gives, rather than on the grooves' lower walls.
  - `chamfer=3` [decided by Florian 2026-10-12: 3 mm, so the floor goes
    in easily]: the panel's corners between two grooved edges are cut off
    at 45 degrees, 3 along each edge, by the helper `chamfer()` cuts a
    corner of the outline off with (`lang/core/corners.py`), once the
    panel has grown: `floor.chamfer(floor.front.left, 3)` names the corner
    of the placement box, which the grown floor no longer has. At most
    twice the depth, or the chamfer would reach past the boards' faces and
    show; None or 0 for square corners. Corners next to an edge that goes
    into no groove stay square.
  - Dog bones where a groove stops inside its board, as part of its
    pocket: `dogbones="hidden"` [decided by Florian 2026-10-12: the
    default, replacing "corner"] centres them on the groove's end, touching
    its edges and bulging past the end only, and is an error where that
    would break out of the board (they reach `tool / 2 + relief / 2` past
    the end); `"corner"` (as on tenons and half laps) or None; `tool=6`,
    `relief=0.1`, a tool wider than the groove being an error. A corner
    relief bulges 0.93 past the groove's edges as well, which at a corner
    of the panel the end of the board the corner goes into covers. The
    examples build with the default; the drawer cabinet with 9 or 11
    fingers does not, where a floor lies across the lower end of a front
    finger: the front's groove stops inside the finger, and a hidden dog
    bone at its upper corner would reach down past the finger's end into
    the joint's gap (corner dog bones fit there).
    `board.dogbones()` adds nothing more there, since the reliefs are
    arcs, and relieves a groove joined with `dogbones=None` like any
    pocket.
  Nothing shows [Florian: grooves must not show]: a groove is as long as
  the panel needs, so it stops inside its board where the board goes on
  past the panel's corner and runs out of it where the board ends first,
  as into a box joint's gap; at a corner of the panel either way is
  covered by the board the corner goes into. In the drawer cabinet the
  floors lie in the sides' lowest finger: the sides' grooves stop 6.5
  short of their ends, the front's and back's run out into the joints'
  gaps; at a height where the front and back carry the finger, theirs stop
  inside it and the sides' run out into the notch, which the finger fills.
  A groove as deep as its board is thick would show on the far face and
  is an error. An end that runs out of a board where the panel's edge
  beside it goes into no board of the join (a floor running on under a
  back standing on it, a through dado) may show, and the board gets a note
  in the layout's problems naming that end. Since the grooves take
  whatever lies in their way, they also take the fillets a box joint's
  cutter keeps at the fingers' roots, which reach into the floor's corner
  where it lies near the end of a finger: the hand-built Dynapro drawer
  (2026-09-21), whose front and back grooves ended at the sides' faces,
  needed corner chamfers of 2 * (depth - clearance + 1) to clear them;
  here the 3 mm chamfer is only for putting the box together. Checked with
  the preview's meshes (exact booleans): the drawer cabinet's floors
  overlap none of their four boards with 7, 9 and 11 fingers (with 11 the
  floor lies across the end of a finger); grooves kept within each board's
  box would overlap. `no_interference` does not see the floor's corners:
  like tenons and fingers they lie outside the placement box it filters
  on, and looking past the boxes would report every box joint, whose
  fingers clear each other only through their grooves in narrow faces,
  which it does not count yet. Not checked: a panel's edge running past
  the end of its board. A drawer slide's rear hook holes are checked
  against the floor by `slide.machine_box` [decided by Florian
  2026-10-12, see the slides below]: with Blum (a 6 x 10 hole 11 above
  the floor's underside) the floor does not go into the back, so its
  groove join names the sides and the front only,
  `floor.join(l, r, f, using=groove(...))`; Grass's holes (15 and 47
  above) clear a floor up to 14 thick. Verified in Fusion 2026-10-12: the
  drawer cabinet compiles with its grooved floors in 1.8 s (214
  features), every body one solid, each floor overlapping none of its
  four boards and no side its front or back.
- **Dog bones** (`lang/core/dogbones.py`) [decided by Florian 2026-10-12,
  implemented 2026-10-12]: a router leaves its radius in every inside
  corner, so a part with square corners does not go in; a dog bone takes
  the corner out. Two ways, as Florian decided:
  - per board: `side.dogbones(tool=6, relief=0.1)` relieves every inside
    corner of the board, `at=` only some: the corners of named operations
    (`side.toekick`), of a big face (`side.inner`: what that face shows,
    through cuts and its own pockets, as when the add-in is given a face)
    or of the outline's outer boundary (`side.outer.outline`), one or a
    list. `at=` takes objects only [decided by Florian 2026-10-12]: the
    operation itself, never its name as a string, which is an error saying
    to write `side.toekick` instead; so an operation a later join makes is
    named after that join. It acts where it is written, like every
    operation: it relieves the corners the board has at the call, so it
    goes after the cuts and joins whose corners it should relieve, and
    corners made later get none [decided by Florian 2026-10-12, replacing
    the first version, which waited until the board was finished and so
    ignored the order on the page]; a relief that cannot be made (one that
    would split the board) leaves the board as it was. Reliefs go in as
    operations named after the operation the corner belongs to (the last
    whose contour runs through it), `toekick_dogbones`, or `dogbones` for
    the outline's own corners: a through cut where the corner is one of
    the outline (cuts, notches, laps, tenon roots), else a pocket from the
    face the corner is seen from, as deep as what lies beside it (the
    pocket's depth; through for a through pocket); a corner on a pocket's
    floor (a pocket inside a pocket) is cut from the face to the deeper
    one's depth, the shallower's material above it being gone already.
  - per joint: joints that cut inside corners relieve them themselves,
    with `dogbones=`, `tool=` and `relief=`: tenons (corner, hidden or
    None, see above), half laps (corner, hidden or None). Box joints keep the
    cutter's fillets and hide their own reliefs (see above).
  The geometry is dog_bones_native's (read from its code): from the
  corner along the bisector of its two edges, the centre `(tool / 2) /
  sin(angle)` out, `angle` the angle between the edges (not half of it:
  at 90 degrees half a tool, at 60 or 120 degrees 1.155 times that), the
  radius that plus `relief / 2`, so the circle reaches `relief / 2` past
  the corner at any angle; the add-in's Offset is `relief`. The relief
  takes only its own corner's material, as the add-in's in-face profile
  does: where its circle reaches material that is not on the corner's
  level and connected to the corner (a shallower pocket beside a deeper
  one, a web across a narrow opening), that is left out of the shape;
  elsewhere the shape is the whole circle, whose part in the opening cuts
  nothing. The tenons, the half laps and `dogbones()` share the helpers
  (`corner_relief`, `hidden_relief`), so the tenons' layout stayed the
  same to the bit.
  An inside corner [decided while implementing] is a vertex between two
  straight edges of the material, seen from either big face on every
  level (the face, each pocket's floor), where the boundary turns away
  from the material by more than an arc's segment does (`arcs.MAX_STEP`,
  11.5 degrees). Straight means a line as the emitter draws it
  (`arcs.fit`): circles, slots' round ends, rounded corners, kept
  fillets, other reliefs and holes are arcs, and a junction of a line and
  an arc is no corner either, as the add-in only takes corners between
  linear edges. So a corner relieved before (a joint's own dog bones, a
  hole over it) gets none, `dogbones()` on a tenoned, lapped or
  box-jointed board adds nothing at the joint, and a square box joint
  (`tool=0`) gets them in its notches and gaps. A floor's corner next to
  a higher island is not an inside corner (its wall goes up). Holes count
  as round regions; V-grooves, chamfers and operations on narrow faces do
  not count, and neither does a vertex with an edge shorter than 0.01 mm
  (nothing narrower is meant). Reliefs come in the order of the operations
  they belong to, then by face and depth, however the board lies. A corner through the board is relieved once, from the face
  on which it starts deepest. A relief that splits the board is an error
  (`_cut_through`); a relief at a sharp cutout corner (`radius=0`) leaves
  the opening out of its shape, so the cutout's check for operations in
  its openings passes.
  Deviations from the add-in: vertices turning less than 11.5 degrees are
  not corners (the add-in would put a circle of 5 tools and more on a 170
  degree corner); a chamfer on the contour does not stop a relief (the
  add-in finds no corner on a chamfered face, as no edge at the vertex is
  square to it), the relief cuts through the chamfer, and a chamfer along
  a named operation does not follow the relief's arc. `examples/
  dogbones.py`: a panel with every kind of corner (notch, acute V notch,
  a window with obtuse corners, through pocket, dado with one corner under
  a hole, a well in a recess, a pocket from below, round shapes without),
  a shelf relieving only its notch, and a lapped frame with corner and
  hidden dog bones. The van's floor battens get corner dog bones by the
  half lap's default. Verified in Fusion 2026-10-12 against
  dog_bones_native on the example's boards without dog bones (the
  panel's top face, recess floor and bottom face, the shelf's one corner
  edge, a face of each lapped board): zero boolean difference both ways
  and equal face counts on all seven parts.
- Hardware carries its own rules. A drawer slide determines the drawer box width,
  length, position and floor recess, so those numbers never appear in cabinet
  code. [decided; first hardware implemented 2026-10-11]
  `lang/hardware/slides.py`: `DrawerSlide(model, nl)`, the model by name
  (`"Dynapro 40"`, `"Dynapro 50/70"`, `"Movento 760H"`, `"Movento 766H"`,
  every nominal length) or a `lib.drawer_slides` model for one of its own. `slide.drawer_box(bay, front=face.back,
  side_thickness=, height=)` is the drawer box: the sides' inner faces 21 mm
  from the carcass sides (inner width LW - 42 in both catalogs, sides up to
  16 mm), NL - 10 long, with the bottom panel's underside above the bay
  bottom by `slide.bottom_height` (Blum 28.5, "min. 28.5" with the screw
  row at 38; Grass 28, 10 below the screw row as the Grass sheet says,
  kept although Häfele's Dynapro models put the drawer member's top at
  28.5 too [decided 2026-10-12]) and the sides hanging
  below it by `slide.recess` (Grass 10-13, Blum 12-15, default the middle),
  so the sides' lower edge is `slide.side_lift` above the bay bottom; it
  refuses a bay shallower than NL + 3.
  `slide.machine_box(sides=(l, r), front=f, back=k, floor=floor)` machines
  the drawer box: a cut-out at each end of the front board for the
  couplings and one at each end of the back board for the rear hooks,
  from the side's inner face (Grass 69 and 35 mm wide, Blum 75 and 75)
  and from the board's lower edge up to the floor's underside; and the
  holes for each hook into the back board's rear face (`hook_hole`,
  diameter and depth): Grass three pre-drill holes for the hook's screws,
  default 2 x 8, 42 mm from the side's inner face at 15 and 47 above the
  floor's underside and 10 mm from the inner face at 47; Blum one 6 x 10
  hole for the hook's pin, 7 from the inner face at 11 above the floor's
  underside (confirmed by Florian 2026-10-12). The depth may be `through`
  (`hook_hole=(2, through)`) [decided by Florian 2026-10-12, for either
  family]: the holes then go all the way through the back board, drilled
  from its inner face, as a hole is drilled from the face its `at=` names,
  so the back board needs nothing from its rear face (its box joint's
  reliefs are in the inner face too); fixed-depth holes stay in the rear
  face, where the hook sits. A hook hole that would run into the floor,
  where the floor goes into the back board, or into the groove it lies in
  there (its clearance included), is an error naming the back board and
  the hole, and nothing is cut [decided by Florian 2026-10-12]: with Blum
  the floor does not go into the back (its groove join names the sides
  and the front only), as its 6 mm hole 11 above the floor's underside
  meets any floor of 8 mm and more there. Cut-outs are named
  `coupling_left`, `hook_right` and so on, the hook holes `hook_left_a`... Blum's TIP-ON BLUMOTION
  variant (a 125 mm back cut-out) is not covered.
  `drawer.mount(slide, sides=(left, right), front=face.back)` pre-drills the
  carcass sides: a row 38 mm above the bay bottom at the hole positions the
  add-in uses, measured from the runner's front, into each side's face
  toward the bay's middle (a partition between two bays takes a drawer on
  either face), holes `slide_<drawer>_a`...; a drawer runs on one pair, a
  second mount is an error. Hardware mounts through `Scope.mount(hardware,
  ...)`, typed by the hardware's own `mount(self, scope, /, *, ...)`
  (`Mountable`, a ParamSpec), so the type checker checks the keywords and
  core knows nothing about slides. Like the other hardware the slide plans
  every hole and checks them all before it drills one [2026-10-12; it used
  to drill one side before checking the other].
  The runner pair is placed too, as boxes [decided 2026-10-12, replacing
  the STEP and glTF files of one variant]: the layout has a `hardware` list
  per module, each item with bodies made of boxes in world coordinates,
  one body per runner, named by the drawer's own left and right; the
  emitter makes each body as the union of temporary B-rep boxes in a
  component of its own, the preview as the union of box meshes. Five
  boxes per runner (`RunnerShape`): the cabinet rail's flange against the
  carcass side and its base with the carriage, the drawer member whose
  top carries the floor, the coupling under the floor's front end, as
  wide as the front board's cut-out (the space reserved for it), and the
  rear hook behind the drawer box. Each family keeps one cross-section
  across all lengths and load classes, measured from Häfele's CAD box
  (`teccad.hafele.com`, `ccHandler.aspx?CadBox=2&CssClass=topco&Mandant=HDE&ArtikelNr=...`;
  Dynapro 433.19.600-613 and 433.20.615-635, Movento 760H 433.24.010-024,
  766H 433.24.2xx, Movento coupling 433.24.980/981); the lengths follow
  from NL. The real cabinet rail ends 2/3 to 9/10 of the way back,
  irregularly by model and length (Dynapro NL 300/450/600 at 250/285/456,
  Movento 760H NL 250/450/600 at 232/304/404), so the boxes run it the
  whole length. Why boxes: a file per variant would be some 45 files of
  about 1 MB, each needing its frame measured; the language decides
  nothing from the detail, and the hole patterns were verified against
  every model once (`lib/drawer_slides.py`; the 24 pre-drill holes of the
  example coincided with the Dynapro model's screw holes). Checked: with
  the drawer box machined, the runner boxes overlap none of its parts nor
  the carcass, and without the cut-outs the couplings hit the front board
  and the drawer members the back board. Sources: Grass "Dynapro
  Planungshinweise" 113378 12/2021 (the definitive sheet: installation
  dimensions, fastening positions and assembly steps), Blum TD-132/1
  DE/06.22 p.5, the Blum catalogue 2024/2025 p.413 (Movento planning and
  drawer assembly).
- The other hardware [implemented 2026-10-12, by four agents working in
  parallel, each with its add-in as the reference] follows the slide's
  pattern: a hardware object with the add-in's settings, mounted with
  `scope.mount(hardware, ...)`, which refuses what the add-in refuses
  before it drills anything (every hole checked with `Board.hole_fits`: on
  its face and clear of what was made before, and pilots short of the far
  face; `lang/hardware/common.py` holds what the hardware shares), drills
  what the add-in drills, and places
  the bought part as boxes from one table per hardware, separate from the
  drilling data, measured from the makers' CAD models and drawings
  (2026-10-12). The preview shows or hides all hardware with one switch
  (Display, key `w`, `preview.hardware(on)`). Each add-in now
  reads its dimensions from a Fusion-free `lib/` module the language
  reads too; their constants and dialog defaults were compared in Fusion
  against the old literals and are identical. Every placement is
  physical (numbered from the bottom or from the part's own left), so a
  module in the van's terms and a cabinet with `front=` come out alike.
- **Concealed hinges** (`lang/hardware/hinges.py`):
  `ConcealedHinge(model, count=2, end=60, pilot=(3.175, 3))` with
  the models of `lib/concealed_hinges.py` (Blum CLIP top 110 for thin
  doors, +0 and +3). `cab.mount(hinge, door=door, carcass=left)` (`carcass=`
  a board, or the face the plates go on, `wall.left`) hinges a
  door on a carcass board standing square to it (a side, a partition or,
  for a flap, the top or bottom) and drills what concealed_hinge_native
  drills: per hinge two 10 x 5 holes in the door's inner face, 32 apart
  along the edge, in a row 27 mm (+0) or 30 mm (+3) from the carcass
  board's face toward the door's middle, whatever the overlay or gap; and
  two pre-drill holes for the mounting plate's screws in that face, 32
  apart, 38.5 mm behind the door's inner face. The hinges' centres lie
  `end` from the ends of the door's edge (the add-in makes two;
  `count=` spreads more evenly between). Refused as in the add-in:
  `end` under 27 (its dialog's minimum), hinges 42 apart or closer,
  holes that do not fit on their face. The hinge dictates no overlay or door size,
  since the add-in knows none. Each hinge is a body of four boxes, cup,
  arm, clip and mounting plate (`HINGE_SHAPES`), measured on Häfele's CAD
  models of the hinge 342.46.681 and the plates 342.20.800 (0 mm, 8.5
  high) and 342.20.830 (3 mm; the +3 model is the hinge on it), named
  `hinge_1`... under `<door>_hinges`. `examples/hinged_door.py`: a wall cabinet with an
  overlay door.
- **Hatch hinges** (`lang/hardware/hatch_hinges.py`):
  `HatchHinge("Free space 1.11", opening=107, carcass_depth=12, pilot=(2,
  4))` with the specs of `lib/hatch_hinges.py` (or a `lib.hatch_hinges`
  `HingeSpec`, which takes more), placed as `<hatch>_hinges`, holes
  `hinge_<hatch>_a`... and `hinge_<side>_a`.... `cab.mount(hinge, hatch=hatch,
  sides=(left, right), top=top)` drills what hatch_hinge drills, from the
  underside of the carcass top (`top=` the board or the height of its
  underside): into each side panel's inner face three 5 mm holes 37
  behind its front edge, 102, 134 and 166 below that reference; into the
  closed hatch's inner face each mounting plate's pilot holes, 25 in from
  the side panel, 12 and 76 below. It checks what the add-in checks: the
  hatch 16 to 28 thick and closed (0 to 2 mm in front of the carcass),
  flush front edges, the overlap A (how far the hatch top reaches above
  the reference) at most A_max for the thickness (24.5 at 16 down to 21
  at 28; 37 with `opening=90`), checked and never chosen, holes and plate
  on their boards, depths less than the boards, no part containing one of
  the add-in's probe points. `max_overlap(t)`, `highest_hatch_top(top,
  t)` and `lowest(top)` (169 below the reference) give the cabinet what
  the hinge dictates. One body per hinge, named by the hatch's own left
  and right, of four boxes (plate, arm, upper and lower housing) measured
  on Häfele's CAD model of 372.27.300 (glTF, closed, 2026-10-12).
  `examples/hatch.py`: a wall cabinet with a lift-up hatch, its shelf at
  `hinge.lowest(top)`.
- **Ball catches** (`lang/hardware/ball_catches.py`): Ganter GN 450
  catches holding an inspection hatch in its opening, as ball_catch
  drills them. The opening is a named through cut with its rounded
  corners in the shape; `catch.hatch("hatch", panel.opening)` is the
  hatch, the opening shrunk by the slot (`catch.gap`, 3 mm, within 2.5 to
  3.5), offset exactly on its lines and arcs, flush with the panel.
  `scope.mount(catch, opening=panel.opening, edge=panel.opening.left,
  hatch=hatch)` (the hatch's outline is `lang.core.cutouts.inset`; holes
  `catch_<hatch>_<n>` and `catch_<panel>_<n>`) drills per catch a pilot hole for the holder's screw into
  the panel, 8.4 mm outside the opening's contour, and one for the ball's
  screw into the hatch, 9.4 mm inside it, Ø2 x 4 by default, from the
  face that is not the show face unless `face=` names one. `count=` (4)
  catches go on the named edge and the one across from it, the extra one
  of an odd count on the named edge; on each the outer ones sit `end=`
  (40) from the ends of its straight part, the arc tangent points (the
  lines `lang.emit.arcs.fit` finds in the cut's shape). `BallCatch(at=
  [...])` takes points instead. Checked as in the add-in: the hatch under
  every ball, the slot within range, 14 mm to the end of a straight edge
  and 28 between catches, mounting surface for holder and ball part,
  pilots shallower than the boards. One body per catch (holder, its stop
  webs down the opening's edge into the slot, its jaw over the slot, ball
  part; `CATCH_SHAPES`, measured on Ganter's CAD model).
  `examples/inspection_hatch.py`: a floor panel on battens with a rounded
  opening and its hatch.
- **Door latches** (`lang/hardware/latches.py`): `DoorLatch(model,
  count=1, end=100, pilot=(3.175, 3))`, placed as `<door>_latches`, with door_latch_native's
  latches `"Everlock"`, `"Pull Lock 44"` and `"LL-66"` (Sugatsune),
  `cab.mount(latch, door=door, carcass=top)`. The body goes on the door's
  inner face, the strike on the carcass face (the carcass board's big
  face toward the door's middle, or the face given, `carcass=shelf.top`),
  beside the door's edge on that side; holes are measured from the
  carcass face and the door's inner face as the add-in measures from its
  two edges, so inset and overlay doors get the same latch: Everlock a 25
  mm finger hole through the door 30 below and four pilots 26 to either
  side at 26 and 42, strike pair 14 to either side at 25; Pull Lock a
  38.1 hole through 34 below and a 48 counterbore from the inner face
  leaving 10 at the front (none on a door of 10 or less), keeper 9.5 at
  29 behind the door's front face, where the lock sits; LL-66 two pilots
  28 to either side at 10, counter plate 10 at 24.
  One latch in the middle of the edge, more from `end=` from its ends.
  Refused like the add-in: a pilot not below the narrowest pilot
  spacing, an edge no longer than twice `end=`, a carcass board parallel
  to the door, holes that do not fit on their face. Each latch with its strike is one
  body (they interlock when closed) of boxes (`LATCH_SHAPES`): Everlock
  from the maker's installation drawing, without the aluminium inset
  (which needs a 30 mm hole; the 25 mm hole is for the lock without it,
  Florian 2026-10-12), the Pull Lock from its drawing (bezel 44, panels
  1 to 10 thick, which the counterbore leaves), its parts in the door's
  holes as squares inside them and its lock measured from the door's
  front, the keeper too, its screws 29 behind the door's front face as
  the drawing measures them from the bezel, the LL-66 from Sugatsune's CAD
  model; `latch.reach`
  is how far the part behind the door's front reaches from the carcass
  face (Everlock 60, Pull Lock 50.9, LL-66 24.6), which a drawer box
  behind a latched face stays clear of. `examples/door_latch.py`: an inset door with two pull
  locks and two latched drawers.
- **Sliding brackets** (`lang/hardware/sliding_brackets.py`) [decided by
  Florian and implemented 2026-10-12; no add-in yet, the data is in
  `lib/sliding_brackets.py` for one]: Häfele Pacofix, the same parts as
  Keku AS (Häfele: they "click with all Keku plastic fittings"; Keku
  lists its parts under Häfele's numbers), holding a removable panel on
  frame boards standing square to it: `cab.mount(SlidingBracket(),
  panel=cover, frame=[left, right])`, like the hinges. The frame part goes
  on each frame board's inner face (toward the panel's middle, or the face
  named, `frame=[wall.left]`), the panel part (PF) on the panel's back
  face (toward the frame boards), its tongue under the frame part's hook;
  the panel comes off square to itself. Two frame parts, both on the
  frame board's inner face, are the models:
  - `"Pacofix PF-L-R"`, the bent one, the default [Florian uses it,
    2026-10-12]: the hook is bent back over the frame part's own plate,
    which reaches from the panel's back face 33 back. The frame holes lie
    8 behind the panel's back face, the panel holes 19 out from the frame
    board's face, since the tongue lies on the 4 mm plate. The frame
    holes stay 8 behind the panel's back face, at the plate's front end,
    whatever the gap [decided by Florian 2026-10-12]. The panel sits on
    the frame board's edge or up to 3 mm in front of it [decided by
    Florian 2026-10-12; a gap was refused before], the plate then hanging
    over the edge by the gap and the frame holes 8 - gap from it, or the
    frame boards reach past its back face (a panel set in between). The
    frame board must reach 29 behind the panel (the plate's flat
    underside; its last 4 mm are rounded).
  - `"Pacofix PF-L"`, the straight one: the hook points from the plate
    toward the panel, the tongue lies on the frame board. Frame holes 37
    behind the panel's back face (the System 32 line), panel holes 15 out
    from the frame board's face. The gap is read from the model, never
    given: the frame holes depend on the panel's back face only, so a gap
    moves them toward the frame board's edge (37 - gap, up to 29, where
    the plate begins); the frame board must reach 45 behind the panel.
  Each pair of holes is 32 apart along the edge. A panel set in between
  may stop up to 3 mm short of where the panel part's plate begins (3 mm
  short of the frame board's face for the PF-L, 7 for the PF-L-R), the
  plate hanging over its edge [decided by Florian 2026-10-12]. `count=`
  brackets (2) per frame board, the outer ones `end=` (50 [decided by
  Florian 2026-10-12]) from the ends of the stretch panel and board share,
  or `at=` positions along the edge, the same on every frame board;
  numbered from the bottom or from the panel's own left. Holes per part,
  because Euro screws usually go only into the frame board: `frame_hole=`
  and `panel_hole=` each `"pilot"` (Ø2 x 6, the default, for chipboard
  screws), `"euro"` (Ø5 x 11, a 6.3 x 13.5 Euro screw through the 4 mm
  plate, but never deeper than the board less 2 mm, 10 on a 12 mm board
  [decided by Florian 2026-10-12]; a board under 11.5 then takes a
  shorter screw) or (diameter, depth), which stays as given. Refused
  before anything is drilled: a frame board parallel to the panel, a gap
  the frame part does not allow, a frame board ending before the plate
  does, a panel too far short of the plate's start, plates off their
  boards or over pockets (a hole under a plate is fine; the part over a
  gap hangs free), brackets closer than a plate's 48, holes off their
  face or in another hole, holes as deep as the board is thick, `end`
  under 24. The makers' rules are advice for the build, not checks, and
  nothing about them appears in the build's output [decided by Florian
  2026-10-12; they were notes in the layout's problems before]: Keku
  asks for at most 600 between brackets and at least four per panel (two
  frame boards with two each); Häfele rules out hanging loads, such as a
  panel hung overhead, and gives 20 kg per pair vertically, 30 kg lying
  horizontally. Each latched pair is one body of four boxes
  (`BRACKET_SHAPES`: frame plate, hook, panel plate, tongue), `bracket_1`...
  under `<panel>_brackets`, numbered on through the frame boards in the
  order `frame=` names them; holes `bracket_<other>_<n>a/b` with the same
  numbers. Articles, for chipboard / Euro screws: panel
  part PF 262.50.359 / .358, frame part PF-L-R 262.50.390 / .391, PF-L
  262.50.368 / .377; sets 262.50.380 (PF with PF-L-R) and 262.50.313
  (PF with PF-L). Measured on Häfele's CAD models (glTF) of 262.50.359,
  262.50.390 and 262.50.368, fitted together latched. PF-L: the tongue's
  tip against the plate, the hook's tapered sides 0.1 to 0.2 mm clear of
  the tongue's tapered channel, the lip's back flank on the tongue's ramp;
  that confirms the 37 of Häfele's mounting drawing and the 15. PF-L-R:
  the lip's back flank lies on the ramp all along with the panel's back
  face 8.15 to 8.2 in front of the holes (8 taken, the plate's front
  end), the hook's sides 0.2 clear, its roof on the channel's floor, the
  tongue's walls as high as the roof; the tongue's square bottom corner
  meets the hook's rounded closed end there by about 1 mm in the model.
  `examples/removable_panels.py`: a seat base with a cover on its sides'
  edges (PF-L-R) and a rear panel set in between them (PF-L, Euro screws
  on the sides' System 32 line). Left out for now: snapping the frame
  holes to an existing System 32 row, Häfele's 1.5 mm spacer plate under
  the panel part (the PF-L's frame holes then 38.5), the hang-in fittings
  for panels parallel to the frame (SF/EH). Verified in Fusion
  2026-10-12: the example compiles with every bracket body one solid,
  none intersecting a board or another bracket, and all its pilot and
  Euro holes in the sides.
- Open from these [2026-10-12]: the hatch hinge's probe points miss a
  shelf 64 to 82 below the top, which the hardware boxes now catch
  through `no_interference`; the helpers the hardware shares are in
  `lang/hardware/common.py` now (2026-10-12). Decided by Florian: the hinge's
  `end=` is at least 27 (the add-in's dialog), the Everlock hole stays
  25, the Pull Lock keeper's screws go 29 behind the door's front face, as
  the lock's drawing has them (door_latch_native measured them from the
  inner face before; corrected in the add-in too, whose sketch now
  dimensions the pair from the door's projected front edge).
- Not covered by an add-in today, as far as seen: a groove for drawer floors
  (the `groove` joint since 2026-10-12, see "Grooves" above), the drawer-box
  dimensions per slide model (box width, length, recess, the coupling and
  hook cut-outs and the hook holes, in `lang/hardware/slides.py` for both
  families), and the sliding brackets (`lib/sliding_brackets.py` is ready
  for an add-in). [open]

### Runs: tubes, ducts and keep-outs

Water tubes and wiring ducts are planned alongside the furniture so that there is
room for them and they are organised. By hand this is a 3D sketch of the centre
line and a shape swept along it. In the language a run is a primitive. [decided
as a need; the design is proposed]

- A **run** has a name, a cross-section, a clearance and a path. Constructors:
  `tube(name, d, bend_r)` is round and bends with a radius; `duct(name, w, h)`
  is rectangular and turns sharp; `keepout(name, w, h)` reserves room for
  something not modeled yet. `.clearance(n)` and `.path(...)` are modifiers,
  like a board's. Runs appear in the cut list by length, tubes with their bend
  count.
- **Paths are waypoints that change only what they name.** Each waypoint states
  one, two or three coordinates; the others carry over from the previous point.
  One coordinate is an axis-aligned leg, which is nearly every leg of a real
  run; two is a diagonal. Every coordinate is a reference from the position
  algebra, so a waypoint reads like a board limit. Routing is manual: the source
  states the waypoints, the language checks them. Automatic routing is out of
  scope.
- **`along(face, gap)`** is what makes a run follow a component. It pins the
  centre line at the face plus gap plus half the cross-section on that axis for
  the legs that follow, until the next `along` or an explicit coordinate
  overrides it. For ducts it also sets the orientation: the flat side lies
  parallel to the face. Two faces run the duct in a corner. Moving the panel
  moves the run; the gap is checked, not assumed.
- **Crossings produce holes.** Where a run passes through a board, the layout
  step adds the pass-through to that board as an operation: a hole of diameter
  plus clearance for a tube, a rectangular cutout for a duct, at the crossing
  point and angle. `through=` overrides the automatic rule where a grommet or
  bulkhead fitting needs something else.
- **Checks.** Runs are first class for interference and clearance: against
  boards, other runs and the vehicle mesh. Tubes check each bend against the
  room available and against the tube type's minimum bend radius. A duct can
  check that its lid side stays reachable. All of this runs in the layout step.
- **Across modules, through ports.** A module exports named points where a
  service enters or leaves, and the port itself defines the pass-through in that
  module's board. A systems module imports the ports and routes between them.
  Furniture modules know only their own ports, so the compile order stays
  acyclic. Runs inside a module stay in that module.
  Spelling [proposed]: `back.port("cold", face="inner", at=("bottom.left", 60,
  80), d=20)` declares a port on a board face with the pass-through size, by the
  receiver rule; it is exported from the module automatically and read as
  `kitchen.port("cold")`, a point with `.x`, `.y`, `.z`.
- **Emit and preview.** A path is straight legs plus torus sections at tube
  corners. Both the mesher and the emitter build a run from cylinders, boxes and
  tori unioned into one body. In Fusion that can be a temporary B-rep body added
  with one write per run. A sweep along a 3D sketch path, the manual method,
  stays as the fallback if the unioned primitives look wrong at a bend.
- Fittings and connectors on tubes are not designed. [open]

```python
cold = (tube("cold", d=16, bend_r=60)
        .clearance(10)
        .path(
            tank.port("cold"),                     # a point exported by the tank module
            along(kitchen.back.inner, gap=15),     # lateral offset held for the next legs
            via(z=kitchen.top.bottom - 40),        # one coordinate: an axis-aligned leg
            via(x=sink.port("cold").x),
            sink.port("cold"),
        ))
```

A path is a positional sequence whose first and last entries are points.
Waypoints are `via(...)`, not `to(...)`, because `to(face, offset)` is already
the depth of a cut or hole. [proposed]

### Detail levels

Florian models incrementally: rough shapes first, then holes, chamfers and the
choice of connectors. The language does not replicate that as separate stages.
The module is written once, boards first and relations after, and detail is
added below, not by editing the boards. [decided as a workflow; the mechanism is
proposed]

- In Fusion the stages protect work from invalidation: a hole pattern dies when
  its face moves. In the language a hole is a relation to a named face, a joint
  a relation to a contact, a slide pattern follows the bay, so details survive
  shape changes and there is no cost to adding them early or late.
- Details have homes. Joints and hardware go into relation lines after the
  boards. One-offs go inline next to the board they
  concern. A rough module is the boards and their placement; a finished module
  is the same file plus join and mount lines.
- Details that drive the rough shape are chosen early as families with
  defaults: the slide family decides drawer box width and floor recess, the
  connector family and front gap decide the carcass. They are stated once in
  the build and refined to exact models later, in one place.
- A **detail level** is a compile and preview switch: `rough` shows outlines
  and placement only; `full` shows joints, holes, chamfers and hardware. The
  layout step skips the operations below the requested level. A level is a
  filter on operations and never a second code path, so the rough preview
  cannot lie about the shape. Tenons change the outline, so in rough mode a
  board shows its plain outline, which is what one draws by hand at that stage.

### Checks and outputs

- Checks on the layout, before geometry exists: fits on a sheet, machinable from
  one side, no feature narrower than the cutter, interference between parts, gap
  to the vehicle mesh. With contours in the snapshot, parts limited by contours
  are checkable in the layout step too; only parts cut by hand-modeled bodies
  need Fusion first. [proposed]
- Committed next to the source: the layout JSON per module (the semantic diff),
  one SVG per part rendered from it (the visual diff), the cut list, and a lock
  file recording the snapshot hash and the tooling commit a compile used.
  [proposed]
- Units are millimetres everywhere in the language and centimetres only inside
  the emitter. Every compile error carries the part path and the source line.
  [proposed]

### Hand-made geometry and escape hatches

The output is read-only: the next compile replaces it, parametric or direct.
Hand geometry is therefore always input, never a downstream edit. The seam
between generated and hand-made work runs at any granularity, through this
ladder, cheapest first. [proposed]

1. **One-offs in code.** An extra hole or notch is one line with a named face and
   a position.
2. **Hand-drawn 2D shapes as inputs.** The hard part of a one-off is its shape.
   It is drawn as a named sketch in the module's reference document; the code
   says cut, pocket or outline, which face, how deep. This covers most of the
   long tail.
3. **Hand-modeled bodies as inputs.** A bracket or vehicle part is modeled by
   hand and a board is told to clear it. The emitter does the boolean in
   Fusion; the part is flagged as not plain flat work, and the preview shows it
   uncut with the obstacle beside it.
4. **Raw API code inside the module function.** The compiler hands the function
   the real faces and edges behind the names. Reproducible and version
   controlled, unlike a timeline edit.
5. **Takeover by name.** A part declared manual, `board("left",
   ply15).on(cab.left).manual()`, stops being generated. The compiler expects a
   hand-modeled body with that path in the reference document and still includes
   it in checks, nesting and labels. The placement modifiers stay, so the part
   keeps its box for contacts and limits.
6. **Whole hand-modeled components.** Curved trim and upholstered parts,
   referenced for interference checks only.

The one thing to avoid is a hand document that attaches features to faces of a
generated module, since every compile gives those faces new identities. If that
is ever wanted, the compiler emits named construction planes as stable anchors
and hand work attaches to those; whether Fusion re-resolves such links across a
regenerated document is untested. [open]

The Planung check suggests the seam matches what is hand-modeled today: the
furniture modules resolve almost completely, the vehicle-fitted trim does not.
Walking one existing module's timeline and bucketing every feature into the six
rungs above would show which hatches the first version needs. [proposed, not
done]

### Preview backend

A visual, creative process needs a loop of edit, look, edit in well under a
second. Even the best measured compile is 4 s for a kitchen and 13 s for 120
boards, fine for a check, too slow for the loop. [decided as a need; the design
below is proposed]

- The preview is a second consumer of the layout file. A mesher turns parts into
  triangles, a browser page shows them. No kernel, no Fusion, so the time does not
  grow with the module. The mesher reads the layout through the emitter
  plan's own readers (`lang.emit.plan`: `LayoutFrame`, `PartFrame`,
  `named_ops`, `chamfer_target`), so both see the same faces, depths and
  chamfer targets [2026-10-12; they had drifted apart: a through hole into
  a narrow face and chamfers on narrow-face operations came out
  differently]; `tests/test_plan_and_mesh.py` checks every operation kind
  against hand-worked volumes. A mesh boolean that fails leaves the board
  uncut and says so (`preview: ...` in the build's output) instead of
  hiding it.
- Shown: boards as extruded polygons in van coordinates; through cuts exact, since
  they are in the outline; holes and pockets exact through mesh booleans
  (manifold); chamfers too [implemented; all kinds since 2026-10-11]: a
  hole's as a cone, one along a contour (a cut's or pocket's rim, a face's
  outline) as a frustum from the contour at the chamfer's depth to the
  contour moved its size into the material at the face, with mitred
  corners, one along an edge as a triangular prism; hardware as the boxes
  its object gives (a slide's runners); the vehicle and master
  geometry from the snapshot mesh; grain as a subtle stripe per board; colors by
  material; check overlays (interference pairs, parts flagged not flat, sheet
  fit).
- Pieces: world transforms in the layout file (needed by the emitter anyway); a
  mesher writing glTF with shapely, trimesh and manifold, about a day; a static
  three.js page with orbit, part tree, click-to-path, hide and isolate, section
  plane, one to two days; a watcher that reruns the layout on save, rewrites the
  glTF and reloads the scene with the camera kept; the SVG-per-part export from
  the same mesher.
- The watcher rebuilds the preview on every save and compiles into Fusion only on
  request, which keeps the loop fast and avoids provoking the session-wide
  slowdown seen in the benchmark with hundreds of throwaway documents.
- Not shown: results of the raw API escape hatch, hand-body booleans, appearance
  rendering. Those are Fusion's job, as are nesting and CAM.
- Alternatives considered: OpenSCAD as the viewer (almost no code, but no
  picking, paths or overlays, so it would be thrown away); custom graphics
  inside Fusion's viewport (same mesh, in the van you are looking at, worth
  adding later). The browser viewer comes first because it works in tests
  without Fusion, validates the layout format before the emitter exists, and
  Claude can see it through the built-in browser after each edit.
- Click-to-path in the viewer is the Copy Path helper outside Fusion.
- Camera and visibility from code [implemented 2026-10-11]: the page
  exposes `window.preview` (`look`, `view`, `camera`, `fit`, `isolate`,
  `show`, `hide`, `select`, `section`, `labels`, `hardware`, `parts`,
  `ops`, `loaded`, `open`, `designs`, `design`, `version`), so a
  tool driving the browser frames a part, a scope or a named operation
  from a named direction in one call instead of steering the mouse
  (AGENTS.md has the details). The camera is kept in the URL hash, so a
  link or a reload shows the same view. The viewer reads layout version 3
  only and says so in the status line for another (`LAYOUT_VERSION` in
  `lang/preview/viewer/state.js`, kept equal to `layout_types.py`); its
  bookkeeping (`state.js`, `scene-utils.js`) has node tests
  (`lang/preview/viewer/tests/`, run by `tests/test_viewer_js.py`), and a
  rebuild frees the old scene's GPU resources [2026-10-12].
- One preview for a folder [implemented 2026-10-12]: `python -m lang.preview
  examples` serves every build file in the folder, each built into
  `out/<name>/`, and the page switches between them with a dropdown (keys
  `,` and `.`; `preview.open(name)` from code). A build file is a `.py`
  file that imports `lang`; one the others import is a library and not
  listed unless it keeps a build of its own under `if __name__ ==
  "__build__":`. Only the designs that open pages show are built: a save
  of a build file nothing imports marks that design stale, any other
  change (`lang`, `lib`, a shared module or a snapshot in the folder) all
  of them, and a stale design builds when a page shows it. The folder is
  rescanned on every change, so new build files appear without a restart.
  A build goes to a scratch directory and moves in when it went through,
  so a failed one shows its log and leaves the last good scene; a build
  still running after 120 s is stopped and counts as failed, so an endless
  loop in a build file holds up no other design. The log
  holds the error and the lines of the build files it passed through
  (`examples/van.py:39: bottom.join(...)`), not runpy's or the language's
  frames; a Python error raised inside the language also names where
  (`raised in lang/core/shapes.py:243`), and `python -m lang.build
  --traceback` prints the whole stack [2026-10-12]. The hash
  carries the design (`#design=van&eye=…`); without one the page opens
  the folder's first design alphabetically [Florian, 2026-10-12]. Each
  design keeps its own camera, hidden parts, selection and section while
  the page is open, one shown for the first time is fitted. Given a single build file the
  server builds it into `--out` on every save, as before.
- SpaceMouse: the viewer talks to 3DxWare's navigation server
  (`lang/preview/viewer/spacemouse.js`), which works in Chrome and in the
  Claude app's browser pane, not in Safari. It reconnects after a
  connection that was up drops (3 s, doubling up to a minute),
  `spaceMouse.stop()` ends it, and the driver's front view looks from the
  layout's `front`. The page connects in Safari too,
  but the driver does not route the puck to the navigation server while
  Safari is frontmost and zooms the page instead (checked 2026-10-11). A
  workaround through 3DxWare's legacy client framework, taking over the
  puck for Safari in the preview server and navigating the page from the
  raw axes, was considered and not built. [decided 2026-10-11]

## Examples

Written on 2026-10-09 to show the intended feel, before any of it existed;
brought in line with the code on 2026-10-12. The build files in
`examples/` are the reference: the tests build every one of them.

### Board with operations

```python
with board("left", ply15, rect(depth=500, height=720)) as side:
    side.show("outer").grain("height")
    side.cut(rect(depth=60, height=100), at=side.outer.bottom.front, name="toekick")
    side.pocket(rect(depth=200, height=12), at=side.inner.front.bottom(shelf.bottom),
                depth=to(side.outer, -3), chamfer=0.5)    # dado whose bottom is the shelf's
    side.chamfer(side.outer.outline, 1)                   # the show face's outer contour
    side.chamfer(side.front.inner, 1)                     # one edge, named by its two faces
    side.chamfer(side.toekick, 1)                         # the contour a named cut made
    side.fillet(side.back.top, 20)                        # a corner of the outline, rounded through the board
    for z in spread(side.bottom + 100, side.top - 100, pitch=32):
        side.hole(d=5, depth=10, at=side.inner.front(37).bottom(z))   # a shelf-pin column

shape = rect(depth=500, height=720).clip(top=380, back=120)   # the top back corner cut off, 380 x 120
```

Placement modifiers chain freely; an operation that names a point or an
edge of the part needs the part's name, so a part with operations is
written as a block or assigned first:

```python
side = board("left", ply15, rect(depth=500, height=720)).show("outer").grain("height")
side.cut(rect(depth=60, height=100), at=side.outer.bottom.front, name="toekick")
```

### References

```python
mid = (bottom.top + top.bottom) / 2
height = top.bottom - bottom.top         # a length

shelf = (board("shelf", ply15)
         .center(mid)
         .between(left.into(5), right.into(5), back.gap(2)))
```

### Drawer cabinet

As `examples/drawer_cabinet.py` builds it, shortened (the example also
gives the lowest drawer a height of its own and comments every step):

```python
from lang import *
from stock import ply9, ply12, ply15       # examples/stock.py: the birch sheets

GAP = 3  # between fronts


def drawer_cabinet(name, box, n, slide, *, front):
    with cabinet(name, box, front=front) as cab:         # written in its own frame
        left   = board("left", ply15).on(cab.left)
        right  = board("right", ply15).on(cab.right)
        for side in (left, right):
            side.cut(rect(depth=60, height=100), at=side.outer.bottom.front, name="toekick")
        bottom = board("bottom", ply15).on(left.toekick.top, toward=cab.top).between(left, right)
        top    = board("top", ply15).on(cab.top).between(left, right)
        back   = board("back", ply9).on(cab.back).between(left, right, bottom, top)

        bottom.join(left, right, using=cabineo(count=3))
        top.join(left, right, using=cabineo(count=3))
        back.join(left, right, bottom, top, using=domino("4x20", count=2))

        opening = cab.interior.with_sides(bottom=bottom.top)
        fronts = opening.shrunk(left=GAP / 2, right=GAP / 2, top=GAP / 2, bottom=GAP / 2)
        for i, (bay, panel) in enumerate(zip(opening.split("height", n), fronts.split("height", n)), 1):
            d = drawer(f"drawer{i}", bay, panel, slide)
            d.mount(slide, sides=(left, right), front=d.face.back)   # pre-drills the carcass

        cab.export("worktop", top.top)                 # for whatever stands on it
        check(no_interference, fits_sheet)
    return cab


def drawer(name, bay, panel, slide):
    with scope(name, bay) as d:
        face = board("face", ply15).on(bay.front).between(panel).inset(GAP / 2)
        box = slide.drawer_box(bay, front=face.back, side_thickness=ply12.t, height=bay.height - 30)

        l = board("left", ply12).on(box.left).between(box)
        r = board("right", ply12).on(box.right).between(box)
        f = board("front", ply12).on(box.front).between(l, r, box.bottom, box.top)
        k = board("back", ply12).on(box.back).between(l, r, box.bottom, box.top)
        for end in (f, k):
            end.join(l, r, using=box_joint(7, margin=2, clearance=(0.1, 0.1)))
        floor = board("floor", ply9).on(box.bottom + slide.recess).between(l, r, f, k)
        floor.join(l, r, f, k, using=groove(5, clearance=(0.5, 0.5)))
        slide.machine_box(sides=(l, r), front=f, back=k, floor=floor)   # cut-outs and hook holes
    return d


box = Box.from_size(width=500, depth=600, height=720)
drawer_cabinet("drawercab", box, 3, DrawerSlide("Dynapro 40", nl=450), front=box.right)
```

(Joinery rules, which would have made every `join` above disappear, were
dropped on 2026-10-11; joins name their partners.) Things to notice: no
board has a size of its own (the toe kick notch is the one number on a
board), no joint names an edge, and the slide decides the drawer box.

### Master index and floor battens

The battens run across the vehicle. They are shorter between the wheel arches and
longer in front of and behind them. The floor profile is mostly the same along the
vehicle, with one or two exceptions depending on the vehicle.

```python
# master.py -- names are those of construction planes and sketches in the master document
floor_level = plane("Bodenniveau")
floor_front = plane("Boden vorne")
floor_back = plane("Boden hinten")
floor_outline = contour("Bodenumriss")       # usable floor in plan view, incl. wheel arches

floor_profile = contour("Bodenprofil")       # cross-section of the vehicle floor
floor_profile.replace("Bodenprofil Heck",
                      between=(plane("Stufe hinten"), floor_back))
```

```python
# modules/floor.py
from . import master as van

top = van.floor_level - ply12.t

for i, x in enumerate(spread(van.floor_front, van.floor_back, pitch=400)):
    (board(f"batten{i}", ply15)
     .center(x)
     .between(top,
              van.floor_profile.at(x).gap(2),
              van.floor_outline))
```

Each batten is limited by three references and has no numbers of its own.
`.center(x)` is a position on the front-back axis, which is what makes the board
stand on edge across the vehicle. Where the outline runs diagonally or curves, a
batten ends at the tighter of its two faces, so that it fits inside the outline
over its whole thickness. All of that is polyline math in the layout step: the
floor profile is a polyline in the batten's plane, the floor outline is sectioned
at both faces of the batten. The emitter receives a finished outline and extrudes
it; nothing is projected or healed in Fusion. [implemented 2026-10-11 except
`.at(x)` and `replace`; the original draft had the emitter project the master
sketch]

Nothing in `floor.py` is specific to one vehicle. The next van needs a new master
and the same floor code.

As implemented in `examples/van.py`, against the sample master (one floor
profile for the whole length, so no `.at(x)`):

```python
van = master("van_snapshot.json")
floor_level = van.plane("Bodenniveau")
floor_front, floor_back = van.plane("Boden vorne"), van.plane("Boden hinten")
floor_outline = van.contour("Bodenumriss")
floor_profile = van.contour("Bodenprofil")

with module("floor", van.box("Boden")) as f:
    top = floor_level - ply12.t
    above_floor = floor_profile.gap(2)
    inside = floor_outline.gap(3)
    battens = [board(f"batten{i}", ply15).center(x).between(top, above_floor, inside)
               for i, x in enumerate(spread(floor_front, floor_back, pitch=van.param("Lattenabstand")))]
    edge = 3 + ply15.t / 2
    lap = half_lap(toward=f.top)
    for i, y in enumerate(spread(f.left.into(edge), f.right.into(edge), count=6)):
        if i in (0, 5):     # cut in two by the wheel arches: one board from each end
            pieces = [board(f"long{i}_front", ply15).center(y).between(top, above_floor, inside, floor_front),
                      board(f"long{i}_back", ply15).center(y).between(top, above_floor, inside, floor_back)]
            for piece in pieces:     # the battens on its side of the arch
                piece.join([b for b in battens if b.box().overlaps(piece.box())], using=lap)
        else:
            long = board(f"long{i}", ply15).center(y).between(top, above_floor, inside, floor_front, floor_back)
            long.join(battens, using=lap)
    middle = battens[len(battens) // 2]
    joint = (middle.front + middle.back) / 2
    board("panel_front", ply12).on(f.top).between(floor_outline, f.front, joint)
    board("panel_back", ply12).on(f.top).between(floor_outline, joint, f.back)

kitchen_box = van.box("Moebel.Kueche")
kitchen = drawer_cabinet("kitchen", kitchen_box, 3, slide, front=kitchen_box.right)
kitchen.check(inside_box, inside(floor_outline))
```

The battens across beside the wheel arches come out shorter, the one centred
on an arch's rear end ends at its tighter face, every lower edge dips 2 mm
above the floor's valleys and rises into the walls, and the rear panel
carries the arch notches with their rounded corners. The six battens along
stand on the floor 2 mm above its highest point under them, the outer two
in two pieces, and all 48 crossings are half lapped. Compiled in Fusion: 42
parts, 119 features in 1.0 s, every floor part's volume equal to the
layout's.

## Project structure

Tooling goes into this repo. Builds live in a separate repo, one folder per van.
[proposed]

```
fusion-addins/
  lib/            existing shared code
  addins-src/     existing add-ins
    compiler/     new add-in: Snapshot, Compile, Copy Path
  lang/           new package (name is a placeholder)
    core/         references, shapes, parts, contacts, relations -- no Fusion imports
    joints/       settings and layout
    hardware/     slides, hinges, ...
    runs/         tubes, ducts, keep-outs, ports, crossings
    layout/       the layout step: resolve, place, join, check, write layout JSON
    emit/         layout JSON -> Fusion features; the only place that imports adsk
    preview/      mesher, browser viewer, watcher; SVG per part
    export/       cut list
  catalog/        Florian's cabinet functions
  tests/          unit tests for core and layout, runnable outside Fusion
  tools/perf/     compile-speed benchmark
  DESIGN.md       this file
```

```
builds/<van>/
  build.py        which modules to compile
  master.py       index of names in the master document
  materials.py
  modules/
    floor.py
    kitchen.py
    ...
  snapshot.json   the master document, read once
  out/            derived files, committed
    layout/       one JSON per module
    parts/        one SVG per part
    cutlist.csv
    lock.json
```

Fusion documents, not in git:

| Document                    | Made by         | Contains                                 |
|-----------------------------|-----------------|------------------------------------------|
| Vehicle                     | manufacturer    | imported geometry                        |
| Master                      | Florian, by hand | named planes and sketches               |
| Module reference (optional) | Florian, by hand | extra hand-drawn geometry for one module |
| One per module              | compiler        | generated parts, disposable              |
| Assembly                    | compiler        | links to all of the above                |

Three layers change at different speeds: the language rarely, the catalog now and
then, a build constantly. `core` has no Fusion imports so that it can have real
unit tests, which this repo does not have today.

## What the read-only check on "Planung" showed

The naming rules were tested on the existing hand-modeled document (2,279 timeline
items). 451 bodies were classified as boards by a heuristic, which lets a few
brackets and box-shaped electrical parts through. Linked components were skipped.

| Result per board                                               | Boards | Share |
|----------------------------------------------------------------|--------|-------|
| All six sides are one axis-aligned face each                   | 174    | 39%   |
| All six resolve, but some sides are tilted or split into several faces | 219 | 49% |
| At least one side does not resolve                             | 58     | 13%   |

- Furniture modules resolve in 84-100% of boards (Küche 2 84%, Bank FS 93%,
  Bank BFS 96%, Hochschrank 97%, Heckstauraum 98%, Bett 100%).
- Parts fitted to the vehicle do not: Decke 44%, Abdeckungen 0 of 8. Fenster
  reaches 83%, but only 1 of its 66 boards is axis-aligned.
- 443 of 452 board placements sit in unrotated components and none are mirrored,
  so one global direction definition is enough for documents modeled in place.
- "Outermost wins" had to choose on 41% of the cleanly resolved sides.
- 9% of sides are several coplanar faces.
- Where both sides of an edge were single faces, 88% shared exactly one edge and
  11% shared none.

A board made by the compiler knows its sides by construction. This geometric
resolver is only needed for hand-modeled bodies and for the Copy Path helper.

## Measured: compile speed (2026-10-10)

Benchmark: `tools/perf/compile_bench.py`, driven cell by cell through the
MCP server; results and plot in `tools/perf/results/2026-10-10/`. The
workload is a synthetic module of board pairs: a tenon board (28-line
outline, chamfer on every top edge) and a mortise board (six slot mortises,
eight holes and a pocket on the top face, two holes into a narrow face),
about 14 features and 67 sketch entities per pair. 30 pairs are 60 boards,
roughly one kitchen.

| Boards | Parametric | Direct | Direct, deferred sketches + B-rep profiles |
|---|---|---|---|
| 10 | 1.6 s | 0.8 s | |
| 30 | 8.9 s | 2.4 s | |
| 60 | 31.6 s | 6.5 s | 4.1 s (B-rep profiles only) |
| 120 | 135.5 s | 21.4 s | 12.8 s |

Findings:

- Parametric cost per feature grows linearly with the document (0.22 s for the
  first pair, 4.7 s for the 60th), so a module compiles in quadratic time. The
  cost is the compute after every write, not the kernel: in a 60-board
  document a sketch line costs 7 ms parametric and 1 ms direct.
- Direct modeling grows too, but with a seventh of the slope (0.12 s to 0.62 s
  per pair over 60 pairs). Everything the emitter needs worked in a direct
  document: offset planes, sketches on faces, extrude cut by distance and to a
  face, hole features with explicit direction, chamfers, body names, temporary
  B-rep bodies added without a base feature.
- Sketch entities are half the parametric cost. `Sketch.isComputeDeferred`
  while drawing cuts the 60-board parametric compile from 31.6 s to 19.6 s;
  building outlines as temporary B-rep faces and extruding those cuts it to
  22.1 s; both together 15.7 s. In direct mode deferral gives 5.6 s, B-rep
  outlines 5.6 s, and B-rep faces for the mortise slots as well 4.1 s. In
  parametric the slot faces do not pay off, because each needs a Remove
  feature afterwards.
- Batching (one hole feature with eight points, one cut with six profiles)
  halves the parametric time and barely matters in direct mode.
- "To object" extents cost the same as distances. Plain rectangles instead
  of tenon outlines save a quarter in parametric, a third in direct.
- Hand-off gotchas found on the way, all handled in the benchmark: a sketch
  on a face auto-projects the face edges, so its profiles include the whole
  face (pick profiles by area); Fusion stores arcs counter-clockwise, so an
  arc's start and end sketch points cannot be chained from; a face's plane
  normal is not reliably its outward normal in a direct design (pick faces by
  position); body proxies returned inside a base feature's edit session go
  stale after `finishEdit`; a temporary B-rep face's normal follows the wire
  winding, so the extrude direction must be derived from the face normal.
- Repeats after a Fusion restart matched the first runs within 3% (direct
  6.3 s vs 6.5 s, parametric 31.5 s vs 31.6 s at 60 boards).
- Caveat: after about 25 document create/close cycles in a two-day-old
  Fusion session, every modifying API call became 6-7x slower, in new
  documents too, while read-only calls stayed fast. A Fusion restart cleared
  it. Cause unknown; the compiler will create many documents per session, so
  this needs watching.

Decision this supports: compile into direct-modeling documents, draw sketches
with compute deferred, build complex outlines as temporary B-rep faces, and
batch holes and cuts. A parametric document stays available as a debug mode.
Where Multi Arrange and Auto Setup run, which need a timeline today, is still
open (question 2).

What the emitter (2026-10-10) does with this: every outline and pocket shape
is a temporary B-rep face, so no sketch is drawn at all; pockets are batched
per face and depth into one cut; holes are one hole feature each, positioned
by a point on the face (`setPositionByPoint`), since batching barely matters
in direct mode and a sketch per face would auto-project the face; chamfers
are equal-distance chamfers on edges found by position along a contour.
Found on the way: a through hole "to" the opposite face needs the
`directionHint` argument or Fusion reports no target body; a 128-segment
polyline circle chamfers fine; an edge can only be chamfered once, so a
build must not let an outline chamfer and an edge or cut chamfer share an
edge. A feature Fusion refuses does not stop the compile [2026-10-12]: the
part goes on without it, the other holes of a batch are still drilled,
and the report lists it under problems, apart from the build's own checks,
so the document shows everything that worked.

**Arcs** [implemented 2026-10-11]: layout shapes stay polygons, since all
of the layout step's 2D work is shapely, but the emitter plan recovers the
arcs they stand for (`lang/emit/arcs.py`). Circles, slot ends, `rounded()`
corners and round-join offsets all put their vertices exactly on a circle,
a few degrees apart, and booleans keep those vertices. A run of at least 4
segments turning 0.5 to 11.5 degrees each about one centre, every vertex
within 1e-7 mm of the circle, is drawn as a three-point arc (a whole ring
as a circle); everything else stays lines. That leaves coarse polygons
(an octagon) alone, and the master's contours too: sampled every 0.1 mm
and rounded to 0.1 micrometre, they turn too little per step and are too
noisy, so they stay polylines (open question 16). The plan's outlines,
pockets and chamfer contours are loops of lines, arcs and circles; the
emitter builds the temporary faces from `Line3D`, `Arc3D` and `Circle3D`
and finds a chamfer's edges on them by their midpoints. Where a boolean cut
the circle's polygon (a relief added to a rectangle or cut from an
outline, two overlapping circles), the cut point lies on a chord, up to
its sagitta off the circle; it is moved onto the circle, along the line it
continues in or where two circles cross, so arcs meet lines and each
other exactly. The preview keeps meshing the polygons. Verified 2026-10-11: the drawer cabinet (23 parts),
the van (42) and the operations example compile without problems, every
cabinet and van body within 0.005 mm³ of its exact volume, a carcass side
down from 140 faces to 80.

## Open questions

1. ~~Compile speed~~: measured above; a 60-board module in about 4 s direct.
2. How module documents are assembled into the van, and how that performs. A
   short experiment: save a 60-board module, insert it into an assembly ten
   times, time the inserts and the reopen. Also where nesting and CAM run (see
   Backend).
3. ~~Calling the native add-ins headlessly~~: not planned; the compiler targets
   the generic emitter (see Joints).
4. ~~Fully constrained sketches for compiler output~~: no (see Backend).
   Florian to confirm.
5. ~~Where code runs~~: snapshot and emit in Fusion, layout anywhere (see
   Terms and pipeline). Whether the Compile button shells out to a system
   Python for the layout step or the user runs it from a terminal is a detail.
6. ~~Joinery rules~~: dropped 2026-10-11; joints are stated per board (see
   Joints).
7. ~~Connections between modules~~: module exports in Python (see Master
   document).
8. ~~Contour limits~~: drawn sketches as polylines in the snapshot, projected
   or sectioned in the layout step (implemented 2026-10-11, see Placement and
   references). Still open: exceptions looked up by position
   (`floor_profile.at(x)` with `replace(..., between=...)`), and sectioning
   the vehicle body once there is a mesh.
9. ~~Naming for vehicle-fitted parts~~: those are hand-modeled and outside the
   language; only Copy Path cares.
10. ~~Attributes surviving operations~~: irrelevant for compiler output, which
    is never edited; only Copy Path on hand-modeled bodies cares.
11. Drawer construction assumptions in the example above, and the drawer-box
    data per slide model.
12. Package name, and whether path names are German (existing documents use
    German component names) or English. Suggestion: English in code, since the
    API and `lib/` are English and Claude writes most of it, with an optional
    label override for the machine.
13. ~~Direct-modeling documents as a faster backend~~: measured, 5-10x faster,
    API coverage sufficient for the flat-part emitter. Multi Arrange nests
    in them (tested 2026-10-11, see Backend). Open: where CAM runs.
14. The session-wide write slowdown seen in the benchmark: cause, and whether
    many compiles per session provoke it.
15. Terminology: "module" collides with Python's term, and the files live in a
    `modules/` folder; "layout" collides with nesting. Livable, but a conscious
    choice.
16. Whether the snapshot should carry arcs exactly instead of polylines.
    Sampled at 0.1 mm for now, which is up to 0.2 mm off along an axis where
    an arc runs steeply (seen at the sample's wheel-arch corners), and such
    a contour reaches Fusion as a polyline of many tiny faces, since the
    emitter only recovers arcs from exact vertices. The layout's own arcs
    are recovered (see "Arcs" under Backend).
17. Runs: fittings and connectors on tubes; whether a duct needs a lid part of
    its own for the cut list; how a run crossing a board at an angle is cut.
18. Detail levels: two or three, and whether chamfers belong to `full` or to a
    middle level with holes but without joints.

## First slice

The smallest path through all layers [proposed, revised 2026-10-10]:

Status 2026-10-10: steps 1 to 3 are implemented on branch `language`
(`lang/core`, `lang/preview`, `lang/emit`, `addins-src/compiler`, `tests/`,
`examples/`), with pyright strict and 26 tests. The viewer has hide/isolate,
display modes, a capped section and SpaceMouse support; since 2026-10-11 also
the master's ghosts, a floor-grid toggle and a collapsible part tree by path
(hardware bodies included; clicking a group hides or shows all of it); since
2026-10-12 labels with the parts' names and their faces' names as the build
file writes them (a cabinet's own front and left, inner and outer where they
resolve; the layout carries them per part as `faces`). The emitter is a
Fusion-free plan step (`lang/emit/plan.py`: world geometry, batching, chamfer
contours) plus the adsk interpreter (`lang/emit/fusion.py`); it draws the
drawer cabinet (23 parts, 61 features) in 0.4 s and `examples/operations.py`,
which uses every operation kind, in 1.9 s, into a direct document with one
component per scope and bodies named by path. The `compiler` add-in's Compile
Layout button picks a layout file and runs it.

Status 2026-10-11: step 4 is implemented too (71 tests): the Snapshot Master
button and `lang/emit/snapshot.py`, `lang/master.py`, contour limits in
`lang/core/contours.py`, the `inside_box` and `inside()` checks, master
ghosts in the viewer, and `examples/van.py` against the sample master from
`tools/van_master.py` (fixture `examples/van_snapshot.json`), compiled in
Fusion with exact volumes. Not done: `replace`/`.at(x)` for profile
exceptions, the vehicle mesh. The Snapshot Master button was clicked by
Florian on 2026-10-11 and wrote its file.

Status 2026-10-11, later: contacts and the connectors Domino, Clamex and
Cabineo (see "Joints and hardware"), with their dimensions moved into
`lib/connector_data.py`, which connectors_native and `lib/domino.py` now
read too; the drawer cabinet's carcass is joined with them. Joins name
their partners (`join(*partners, using=)`), and the Domino marks are the
new `vgroove` operation through layout, emitter and preview. The emitter
draws the arcs the layout's polygons stand for (see "Arcs" under Backend).
122 tests. Verified in Fusion against connectors_native, now to zero
difference. Integral tenons as the tenons_native add-in makes them, with
screws and connectors in their gaps and screws through open tenons,
verified against it too. Not done: the drawer boxes' joints (box joints,
groove, screws to the face).

Status 2026-10-11, cutouts: `side.cutout()` with full, cross and triangle
patterns (see "Cutouts" under Primitives), verified against cutouts_native
to zero difference with identical face counts. On the way: a pocket may
have several pieces (the layout's rings come polygon by polygon, exteriors
counter-clockwise, holes clockwise; plan and mesher split them); the
emitter chamfers a contour's loops in one feature and, when Fusion fails
it, by halves, leaving a loop it cannot chamfer sharp with a problem
noted; `arcs.fit` starts a ring where no arc runs through it, and leaves a
junction where curves meet at a glancing angle instead of moving it to an
ill-conditioned crossing. The preview shows every kind of chamfer now (see "Preview backend"). 144 tests.

Status 2026-10-12, review: a code and API review of the whole language
(66 findings) was worked through, every fix with tests (445 tests before,
578 pytest and 31 node tests after) and every example's geometry
unchanged. Core: the face a part limit means, limits that limit nothing,
depths past the board and through a narrow face, `to()` on another part,
directions equal across frames, a failed join restoring every board,
problems listed once, layout version 3, `Face`/`Edge`/`Anchor`/`Operation`
in `faces.py`. API: typed `mount` keywords through a ParamSpec, `depth=`
required, `fillet(radius=)`, `clip(top=, back=)`, `between(box)`,
`world_frame()`, hardware exported from `lang` with model names, `pilot=`
and `end=` everywhere, `half_lap(split=)` with total clearance. Joints and
hardware share their machinery (`lang/joints/common.py`,
`lang/hardware/common.py`, `lib/stations.py`, `Board.hole_fits`); the
preview's mesher reads the layout through the plan, the emitter carries
on past refused features, the viewer frees its GPU memory and no longer
hangs `loaded()`. Compiled in Fusion the same day: all eleven examples,
no problems, every body one solid, volumes within 0.03 % of the preview.
Florian's answers on the review's open points (2026-10-12): `dogbones()`
acts where it is written, and cabinets are made with `cabinet(name, box,
front=)` (both done, see "Dog bones" and "Names and paths"); kept as they
are: `Material.t` next to `Board.thickness`, `center` as a placement
modifier, a box query and a face anchor, `material()` without a
sheet-first form, the drawer box recipe in the builds (later the catalog),
clearances as tuples, and the Cabineo's threaded-insert collar reaching
past a 15 mm board's face by 1.35 mm, as in the add-in.

Status 2026-10-12, fuzzing: `tests/fuzz` fuzzes the language with
Hypothesis (how: AGENTS.md "Fuzz Tests"), so far the 2D kernels (arc
recovery, fillets, chamfers, offsets) and cutouts on random boards; joints
and hardware are next. Fixed, each with a regression test: arcs meeting
through one chord or reaching for the first vertex of another arc, and a
vertex moved past the next one (`arcs._snap`); corners sharper than 28
degrees and slivers losing half their area refused by `filleted`; rings
of a collapsed inset or of a hair-thin hole crashing shapely (`grown`,
`chamfered`); the cutouts' rounding as a router would pulling vertices of
new arcs and lines onto large arcs beside them (less than `around=` kept,
corners a cutter cannot reach) and keeping channels narrower than the
cutter; a refused cut changing the outline; a refused cutout leaving its
note; the preview failing on edges shorter than a micrometre. The cutouts
example's openings changed by under 0.5 mm2 each, toward the true tangent
fillets; no other example changed. In Fusion (the same day): its sketch
offset meets the offset circles where an offset extends a corner with an
arc, as `fit` draws it, so `grown` (layout, preview), which mitres the
tangents, is up to a millimetre off there and can also tilt a line by its
snap tolerance: to be fixed. A board whose cut circle touches its edge at
a point builds; a cutout with no border and sharp corners, its openings
touching the outline, does not (Fusion: profile not valid). A batch of 40
fuzz boards compiled with no difference to the preview but these:
operations on material a rounded corner or taper took away are accepted
(Fusion finds no target body or face), a through pocket may split a board
(only through cuts are checked), rim chamfers fail along the short flats
where tangent arcs drawn from polygons meet (up to 0.5 mm, 30 in the
cutouts example, an extra face each), and large rim chamfers (2 mm and
more) leave up to 0.3 % less material in Fusion than in the preview. The
emitter's through pockets cut by distance now (Fusion's through-all
extent failed or stopped short with other components in the document) and
it drops its temporary faces when a step fails; all eleven examples
compile as before, every body one solid within 0.03 % of the preview.
Open, for Florian: geometry that touches itself at a point, has hairline
spikes or sub-micrometre edges: refuse, clean or tolerate.

Round 1b, the same day, as proposed to Florian (openings touching at a
point refused, a cut circle tangent to an edge kept as Fusion builds it;
hairline spikes: cleaned since, see below). Fixed, each with a
regression test: `grown` offsets the lines and arcs exactly as Fusion's
sketch offset does (arcs run on along their circles, corners keep the full
distance), and where that does not hold (a curve vanishes, pieces merge)
mitres with its arcs put back, repairing mitred offsets that cross
themselves and leaving out slivers and specks of holes; `fit` meets curves
that touch where they touch (the cutouts example's 30 flats are gone),
moves a junction only where every arc at it keeps its way (a small circle
touching a large one from inside), and no longer takes a line running into
an arc tangentially for one of its chords (it bent the line up to a
sagitta). The language refuses holes, pockets and V-grooves wholly off the
board, a hole whose centre is off its face or in a hole or pocket made
into that face before, a cut that takes the board away from an operation
made before, through pockets and holes that split the board, a cut that
leaves only what they take, cutout openings that touch the outline or each
other at a point, and openings that touch themselves at a point, through
or not (Fusion: cover failed to make a surface); an operation refused for
its name is no longer kept. The preview meshes rim chamfers that fold
(short edges at an inside corner) in slabs instead of dropping them, which
was the large-chamfer difference, and its tools stop at their depth (they
went 5 um past: a few cm3 on a large pocket). In Fusion: the eleven
examples compile with no problems, every body within 0.03 % of the
preview; 80 fuzz boards differ only by the preview's polygons against true
arcs (up to 0.08 %) and where Fusion fails a rim chamfer. Open: those
chamfers, along the edges of 0.04 to 0.3 mm a cutout's mitred fallback
leaves, or larger than a fillet's radius; where extended curves do not
meet, Fusion bridges them with a line and `grown` drops the shorter curve
(up to 5.6 mm apart at such a corner); a notch whose corner lies
within the polygon's sagitta of a large arc (0.014 mm inside a corner
rounded 496) opens onto the outline as polygons but would be a hole on the
true arcs, and `fit` draws that ring crossing itself. Joints and hardware
are next.

2026-10-13, cleaning [decided with Florian: nothing under 0.01 mm is
meant]: every `Shape` is cleaned when it is made (`geometry.clean`) of
what booleans leave where two edges coincide: points within 1e-6 mm of the
one before, spikes (a ring running out and back along itself within 1e-6
mm), pieces and holes narrower than 0.01 mm on average (twice the area
over the length), and walls of no width (a hole along another ring within
1e-9 mm for more than 0.01 mm), which are opened. Every other vertex stays
exactly where it was: snapping to a grid, even one of 1e-9 mm, moves arc
vertices off their circles and `fit` no longer finds the arcs. Geometry
with nothing to clean comes back unchanged, and every example's plan is
the same. In Fusion an uncleaned spike made the whole body fail
(ASM_WIRE_SELF_INTERSECTS2). A circle cut on a rounded corner's own arc,
refused before as splitting the board, takes the corner now, and a band
cut across a shape exactly as tall parts it in two. A chamfer is 0 or at
least 0.01 mm. The Fusion batch check is in `tests/fuzz` (AGENTS.md). Its
first run: the eleven examples without a difference; of 40 fuzz boards,
the rim chamfers Fusion refused on two (one of them drawn three times):
one along a cutout's fallback edges of 0.06 mm (open, above), and one
where a pocket cutout's triangles, with no border and sharp corners,
reached from edge to edge (below).

The same day, every circle and arc drawn alike [Florian]: `circle()` drew
32 segments a quarter, slot ends 8, the fillets and the cutouts' circles a
vertex every whole degree, so one arc drawn two ways left crescents as
thick as the coarser drawing's sagitta, too thick to clean from a radius
of about 200 mm (a circle cut on a rounded corner's own arc was refused as
splitting the board). Now every circle has its vertices on the whole
degrees about its centre (`cutouts.circle_geometry`), and every arc its
ends plus the whole degrees between them, none nearer an end than 0.6
degrees (`fit` takes a step under half a degree for a sample of a curve,
and one of exactly that fell either side of it); arcs under 5 degrees keep
even steps. Two drawings of one circle coincide but for a sliver at an
arc's end, between whole degrees, up to r (1 - cos 0.5 degrees) thick
(0.019 mm at a radius of 500), harmless while something joins it to the
rest (open). Every example's plan has the same lines, arcs and circles,
and compiles in Fusion without a difference; the preview meshes more
triangles (the van builds in 1.9 s, 1.4 before). The chamfer the batch
check found refused was no missing rim: a pocket cutout's triangles, with
no border and sharp corners, reached from edge to edge, each apex on the
far edge, and the material either side met at that point only; Fusion
chamfers no rim through such a vertex (non-manifold). Pocket cutouts are
checked for openings touching the outline or each other at a point now, as
through ones were. And an inset that dropped a curve where a notch meets a
rounded corner came 0.17 mm nearer the outline than the border, inside the
1 % of the offset `grown`'s self-check allowed: it allows the polygons'
chord errors and 0.02 mm now, and such an inset falls back to the mitred
one. Left open in Fusion: chamfers along a cutout's fallback edges of 0.06
to 0.34 mm.

2026-10-13, fuzzing the joints (`tests/fuzz/joints.py`): random pairs for
every joint, a side and a shelf meeting it edge-on (flat or standing,
anywhere along and across the side, hanging over its edges, between two
sides, the side rounded or pocketed, the shelf's end notched) for Dominos,
Clamex, Cabineos, screws, tenons, joints in the tenons' gaps and dados; a
flush corner for box joints; crossing dividers for half laps; a drawer
box's floor for grooves, into any of its four boards in one join or
several. Each join must keep what the joints promise: a refusal changes no
board, either board's join gives the same, a second join of a pair with
the same kind is refused, no board comes apart, no two share material, no
blind pocket or hole is as deep as its board, connectors and screws sit at
the stations `lib/stations` gives (or `at=`) and within their contact,
tenons stop at the side's outer face (or `remaining=` short of it), and
tenons and mortises, box joints and half laps fill their joint but for the
clearances and dog bones. In tens of thousands of cases, about half of
them joined, the joints keep all of it but for two. A shelf's end notched
to 7 um short of its edge keeps a fin as wide; a dado set the fin 4 deep
into the side, but cleaned the groove for it away as what a boolean
leaves, and the two shared it: a contact narrower than 0.01 mm either way
is now none, the fin stays where it is (`clean` cannot take such fins out
as it takes out pieces as narrow: an opening would also cut the tips where
a circle meets a line tangentially, as the examples' do). And a half lap
where one board ends inside the other, short of its far face, cuts the
other's notch through its whole thickness and leaves it open there;
Florian decided to refuse such a lap. Found on the way, outside the
joints: the exact inset of round 1b could lose a whole region (a slot
through a rounded corner, its walls turned over at the border, took the
inset's corner beside it, so a cross was laid out 17 mm narrower and its
openings ran into the bands); `grown`'s self-check and the offsets fuzz
check now also require an inset to hold the shape shrunk by 1.25 times the
inset with mitred corners (mitred as Fusion's offset: where a tab narrower
than twice the inset turns over, it joins the tab's neighbours straight
across, up to 1.41 times the inset in), and an outward offset to hold the
shape grown round by 0.75 times the offset. And an arc that ends where it
starts (a ring touching itself) kept a circle estimated through two
points. An arc's end moved onto its circle along the line it continues in
could land on the line's other end, where that lies on the circle too, and
leave a line 6e-12 long, or not, as the rounding chose; such a vertex now
stays. And `clean` left a geometry a move had rounded into a crossing (two
crescents nearly touching, in a figure of eight) invalid; it makes it
valid now. The Fusion batch check builds joints too (`fusion_batch.py
joints`): 50 cases, five of every kind of pair, corner, crossing and
frame, 132 parts, every body as the preview's. Fusion found one thing:
screws in the tenons' gaps of a 6 mm side with a pocket where the shelf
meets it go through the 1.5 mm the pocket leaves, and their 1.7 mm
countersink reaches through that, so Fusion cannot cut it (the emitter
reports it, the rest builds). Contacts did not see pockets, so a joint
over one bridged the void; Florian decided to refuse a join across a
pocket, hole or V-groove made before, unless a join made it. The pair fuzz
check pockets the side over the contact and beside it and the shelf out
through its end, and expects a refusal exactly where one lies in a
contact; the lap check expects one exactly where a board ends inside the
other. A second batch, drawn again, found countersinks reaching past the
side's edge (screws as wide as a divider flush with it), now an error, and
the pair check meanwhile tenons the tool could not cut (gaps and tenons
narrower than it), now errors too; the fuzz checks look for both from the
outside.

2026-10-13, fuzzing the hardware (`tests/fuzz/hardware.py`): random
cabinets in the examples' shapes (a carcass and an overlay or inset door,
a removable panel over the edges or set in, a lift-up hatch, a floor or
back panel with an inspection opening, a drawer bay) with concealed
hinges, latches, sliding brackets, hatch hinges, ball catches or slides,
their sizes and settings drawn from their ranges and a little beyond. Each
is built twice, facing two sides of its box (`cabinet(front=)`) at two
places, and what the hardware drills and places, measured from the
cabinet's own front, left and bottom, must come out the same; a refusal
must be one both ways and change nothing; every hole lies on its face,
clear of what was there and of the mount's other holes, a blind one short
of the far face; nothing bought reaches into the boards it is mounted on
(`no_interference`; hardware meeting itself or a third board is the
build's spacing, which the check reports); stations are `lib.stations`'.
Found: three mounts checked each hole against what was there before but
not against their other holes, so latches close together, ball catches
facing each other across a narrow opening and the two hatch hinges in a
narrow cabinet drilled into each other, or were refused by the core
halfway with the first holes drilled; each now refuses before it drills
(latches or catches whose holes meet, hatch hinges whose mounting plates
meet). Then decided by Florian: a Pull Lock 44 on a door thicker than 20.4
mm is refused (its pawl, swinging behind the housing from 20.4 behind the
front, 2.5 mm past the counterbore, would lie in the door;
`LatchShape.max_door`); hinges closer than their mounting plates are long,
56.2 mm, are refused (the add-in's 42 is where their hole pairs meet);
ball catches are numbered along each edge as the other hardware is
(`common.numbering`: from the panel's own left on a level edge of an
upright panel, where they counted from the lower coordinates). And a slide
refused a bay exactly deep enough where its depth rounded 1e-14 short at a
far origin; it is compared within the tolerance now. The Fusion batch
check builds hardware too (`fusion_batch.py hardware`): 36 cabinets, 198
parts and 36 hardware items, every body as the preview's, no problems.

2026-10-13, fuzzing `dogbones()` and `chamfer()` (`tests/fuzz/corners.py`):
the board fuzz's boards (outlines, holes, pockets, cuts, notches,
V-grooves, rounded corners) given dog bones (any tool and relief, `at=`
or not), chamfers on corners through the board, or rim chamfers along
edges, outlines and operations, each built twice, lying two ways at two
places, must come out the same in the board's own frame (differences
narrower than 0.01 mm all over are noise: where three boundaries meet
within that, another frame settles it either way). Dog bones leave no
inside corner they saw unrelieved, each as deep as its wall, each relief
within its disc; a corner chamfer cuts off its triangle and nothing else;
rim chamfers take no more than their size along the rims; a refusal
changes nothing. Found and fixed: a list of chamfers with a refused item
kept the items before it; a corner rounded or chamfered on the outline
redrew all of it and moved the vertices of the arcs elsewhere (they stay
now); dog bones with relief 0 left corners unrelieved (the circle through
the corner, drawn on whole degrees, missed it by its sagitta); vertices
with an edge under 0.01 mm got reliefs, and slivers and spikes the
booleans left in a level made corners; reliefs came in another order when
the board lay otherwise; chamfers as deep as what they bevel or deeper,
and a through pocket that took all of the board, were accepted. The
Fusion batch (`fusion_batch.py corners`) then failed two of 45 boards
(each drawn twice): the same V-groove made twice, the second finding
nothing to cut, and a 13 mm chamfer along a short edge between rounded
corners, whose wall a pocket from the other face had lowered to 4.4 mm
all along. Now refused: a pocket or V-groove wholly in what was cut from
its face before, as deep, or through; and a chamfer deeper than the wall
where something from the other face runs out under its rim. Tried by hand
in Fusion first: it chamfers over a pocket from the other face near the
rim but not under it (allowed), over one that lowers the wall in part
(refused too, the simpler rule), over openings through the board (allowed:
it stops at them), along edges between rounded corners at any size, but
not along a cut's side lowered all along. That also showed a chamfer
along an edge that rounded corners had taken away entirely accepted
(Fusion found no edge, the preview bevelled the round), now an error.
Then two batches of 42 boards each: no problems, every body as the
preview's. The long run found the check's own slip (a cut's chamfer is on
the show face, by default the second big face lying flat and the first on
the back; the check shows the first now) and, checking the hardware, a
top between two sides with no room built at one place, 3.5e-15 mm wide
from rounding, and refused at another: a board narrower than 0.01 mm is
an error now. Again: `clean` left a spike 0.07 mm out and back to a point
1e-12 from where it left (it took only spikes under a nanometre where
the points either side coincide), and the vertex beside it made a 43
degree corner at one place of the board only; such a spike goes now,
however long. And a through relief, kept to its own level, can take the
corner of a shallower pocket beside it down with it: that corner,
relieved as deep as it was, is there again, deeper, a corner the call
made, which a second `dogbones()` relieves (left so: the reliefs are the
corners' at the call).

2026-10-14, five more fuzz harnesses, three of them written by agents in
worktrees of their own and merged (where two fixed one thing, the merge
keeps both findings: `clean` takes a ring's spikes off before judging it
narrow, and opens a narrow piece by 1e-6 instead of dropping it, so
wider parts a hairline joins stay; a piece held on by less than 0.01 mm,
by a hairline or at a point, is apart, `_pieces`, for cuts and for holes
and pockets through the board; `inside()` allows 1e-6 mm, as a distance,
past a contour offset as `between()` offsets it).

The placement (`tests/fuzz/placement.py`): designs written in a module's
own terms, a carcass in the examples' shapes (sides with a toe kick a
bottom stands on and a dado a shelf sits in, its place taken from the
dado's edges and floor; a top, a back grooved into the sides or not, a
shelf and a divider centred between boards, a door over the front or set
in), a bay of the interior in a scope, a module or a cabinet of its own,
with a face and a drawer box in it, and boards placed at random (on a
side, a face or a position, centred on a mix of positions, between sides,
boards, faces, mixes and boxes, inset, some of them rects), then holes,
rows, pockets and notches placed through anchors, `to()` depths, holes
into narrow faces, a board cut by another, edge and corner chamfers,
fillets. Each is built as written, moved (a cabinet facing another side)
and in another world frame (any of the 48 bindings of the names to axes
and signs), written otherwise (other orders; `side + n` for
`side.into(n)`, an anchor from the opposite edge, a depth `to()` the
other face, a row spread from its other end, an edge named from its
other face). Measured from the module's front, left and bottom, every
board, outline, face name, operation, refusal and layout problem must come
out the same, and `on()`, `center()`, `between()`, anchors and depths put
things where they say. Found and fixed: `side.show(side.inner)`, the form
`show()`'s docstring gives, was always refused; a board between a single
board lying across the box's middle ran through it; a board with a face
on its scope's middle had its other face for the inner one, and rounding
put the face across the middle at some places; `spread()` ran from the
lower coordinate whatever end came first, and fitted one position fewer
where rounding left a span of whole pitches a hair short; `0.5 *
cab.bottom + 0.5 * cab.top` was a TypeError; `to(side.outer, -20)` on a
15 mm board made a hole -5 deep (a depth under 0.01 mm is refused now);
an edge's chamfer was on the face named first (`side.front.inner` the
front, `side.inner.front` the inner face), now always on its big face (the
examples' layouts record two chamfers on their big face, no plan
changes); a shaped board's far edge lay 1e-13 off its box at some places,
and a hole into that narrow face was refused there; a clipped notch at a
board's corner cut the corner free but, 4 m out, its edge came 5e-13 off
the board's and held the corner on; a floor reaching 0.0036 mm into a
side was refused as `side.cut(floor)` and made a pocket that deep as
`side.cut(floor.box())` (a region must reach 0.01 mm in); a hole centred
the face tolerance off a board's edge was refused at the origin only; a
notch left a narrow face 6e-14 askew, and a hole into its other end was
then off the board; `clean` dropped a strip 0.2 by 7 mm with a hairline
tail 175 mm long. Left open by the fuzzing (marked `known:` in the
check), decided by Florian the same day and implemented (below): a board
across its scope's middle without `show()` showed the world's positive
face (it shows its top, else back, else right face in the scope's own
frame); a shaped board that does not fill its limits less its inset, or
has fewer than two on an axis, sat at their lowest corner in world terms
(refused when it does not match two limits; with one it sits against it,
with none at the scope's front, left, bottom corner; its box is its
outline's); limits that overlap (two boards overlapping each other, the
same board twice, a position inside a board), a single limit at the
box's middle, and a board as the only limit centred in the box put the
board inside them or on the world's positive or negative side (all three
refused). And `+` and `-` on sides move along the world axis
(`cab.bottom + 60` is 60 in only where the world's top is its axis's
positive end): kept, with `side.into(n)` and `gap(n)` sides that `on()`
takes; `a + b - c` of positions, whose weights add to one, was a
TypeError (allowed).

The master's contours and the snapshot (`tests/fuzz/contours.py`,
`tests/fuzz/snapshots.py`): random masters, contours as the snapshot holds
them (closed rectangles with notches, stars and circles, open edges,
walks, steps and the van floor's ribs, corners rounded by arcs sampled and
rounded as the writer does), in a board's own plane or across it, given
to `between()` with `gap()`, `into()` or bare, with positions, room sides
and an end board. The board must lie in what each contour allows and keep
its gap, as `inside()` agrees, be the board worked out independently, and
come out the same with its axes on other world axes, elsewhere, and each
contour reversed, restarted, resampled, its plane moved and its normal
turned; a refusal changes nothing. `chain()` must give back the chain
however its curves come (shuffled, reversed, split, ends moved under the
tolerance), the writer's snapshot be the same in any order, `dumps` and
`content_hash` deterministic, and `master()` read back what was written.
Found and fixed: a contour across a board was sectioned only at the
board's two faces, so a notch between them let the board run 75 mm into
it (now its section over the whole thickness keeps clear, see "Contour
limits"); an open contour across a board missed a dip between the faces,
its clearance could pass the board's other limit or the room's middle,
fell short of a face the contour only just crossed, and came out refused
or not as the contour ran; GEOS simplifies what it buffers as the points
come, so the same outline reversed with points added moved a panel 0.03
mm for a 26 mm gap (now the area is given to it in one form);
`inside()` reported a face a rounding (1.2e-7 mm) past a contour, which
`between()` takes; a name made twice listed its places in Fusion's order,
so the hash changed with the order of components; a curve under 0.01 mm
at a join was refused as "4 curves meet"; one line drawn twice became a
closed contour of two points, which then failed in shapely. Tried and
dropped: an exact offset of its own, which GEOS unites wrongly, without an
error, where its pieces' edges nearly coincide. Decided by Florian the
same day: an open contour that runs back along itself (an overhang) is
refused (implemented, below); clearances up to about a hundredth more
than asked (never less), so that a mirrored contour can differ by that
much, are accepted; the rules chosen while fixing are confirmed (see
"Contour limits"). Every example's plan is unchanged.

The design checks (`tests/fuzz/checks.py`): scenes of the board fuzz's
boards, each placed against one before it, parallel or across, touching,
apart or overlapping by around 1e-9, 1e-6 and 0.01 mm, or set into one of
its pockets or holes, with hardware boxes standing in holes or against
boards and boxes, in a module whose box is the scene's grown or shrunk a
little and a closed contour around it; each built twice (turned,
mirrored, moved, in another world frame, as a module or a cabinet, in
another order), and `no_interference`, `inside_box`, `fits_sheet` and
`inside(contour)` must name what the truth has (boards in one plane slab
by slab with exact 2D booleans, boards across each other from the
preview's meshes, hardware boxes exactly): an overlap 1e-5 deep and 0.025
wide must be reported, one no deeper than 1e-7 never. Found and fixed:
`no_interference` counted a pocket or hole as missing material only where
it spanned all of the range in question, so a pin through a pocket from
the top and a hole from the bottom, or two parallel boards lapped with a
pocket in each, seemed to overlap, and boards across each other counted
where each had material somewhere in the boxes they share (a divider in a
groove, its end notched clear); it looks slab by slab between the pockets'
and holes' ends now, and across cell by cell. It drew a hole as 64 sides,
1.2e-3 r too much, now a side a degree. `fits_sheet` had no tolerance (a
part from -1219.9 to -976.9 is 243.0000000000001 high), and `inside()`
measured by area; both allow 1e-6 mm as a distance. `clean` dropped a
hardware box's two ends joined by a hairline 6e-14 wide. And a through
hole tangent to the board's edge that cuts a corner off but for the point
where it touches was refused at one place and kept at another, as was the
same circle cut: refused everywhere now, a corner held on at a point being
apart (a circle that only touches the edge is kept, as Fusion builds it).
No example's plan or check results change. Decided by Florian the same
day and implemented (below): an overlap narrower than 0.01 mm in a
board's plane was not reported (`clean` takes such pieces out of the
material), while one as thin across the thickness was, down to 1e-6;
anything deeper than 1e-6 in every direction counts. And material outside
a placement box (a tenon, a tab) was not looked at by `no_interference`,
`inside_box` or `inside()`: `inside_box` and `inside()` take the
outline's extent, `no_interference` too once pockets and holes in narrow
faces count.

The lib modules that compute (`tests/fuzz/test_fuzz_lib.py`):
`lib.stations` on its own and its three callers' refusals, the drawer
slides' choice of holes against every choice, the hatch hinges' overlap
limit in mm and in cm, the cutouts' triangle and rhombus solvers against
their own equations, and (a plain test) every spec's `in_cm()`. Nothing
was found.

Merging the three and running every long fuzz profile again found five
more, each with a regression test: `no_interference` failed ("Shape is
not an area") on a cell lying in a notch of a board's outline, touching
it along the notch's edge only (a material's areas only now); `clean` kept
a spike whose removal left the ring running along itself, invalid (made
valid now, as an invalid input is); `round_offset` left GEOS's invalid
sliver where an area shrinks by half its width (cleaned); a relief took a
piece of material held on to its corner at a point only at some places
of the board (a piece held on at a point is apart); and a level the dog
bones find corners in ran along itself where pockets from either face
meet along an edge, a wall of no width `clean` does not see, which gave
two corners at one place only (the material and levels are opened by
1e-6, `geometry.opened`). And the arcs check, older than this round,
found `fit` taking a dent 0.0014 mm deep into its arc one way round a ring
and keeping it as two short lines the other; where the lists of curves
differ, the drawings must agree within 0.01 mm now. Every pytest run
takes about 30 s (16 without the fuzz tests, whose fast budget is about
14 s); the long profile 16 minutes, its slowest checks (box joints,
placement, cutouts, offsets, dog bones, the design checks) 80 to 100 s
each.

The same day, Florian's decisions on the twelve, implemented by the same
three agents and merged (the rules as they now read are in "Names and
paths", "Placement and references", "Contour limits", "Master document"
and "Joints and hardware"): the default show face, shaped boards placed by
their limits, ambiguous limits refused, `into()` and `gap()` sides and
`a + b - c` (placement); an overlap deeper than 1e-6 mm in every direction
counted by `no_interference`, its material no longer cleaned first, and
`inside_box` and `inside()` taking the outline's extent (checks); an open
contour that runs back along itself refused, and the clearance's
hundredth accepted (contours). Each fuzz harness checks its decided rules
from the outside and marks nothing of them known; no example's plan or
check results changed, and none needed a change. On the way: a floor
reaching exactly 0.01 mm into a side made a pocket as
`side.cut(floor.box())` but was refused as `side.cut(floor)`, its section
cleaned away (taken as it is now); and two circle pockets from either
face of a board, half its thickness each, covered all of it and left
nothing, which neither was refused for alone: pockets and holes from
opposite faces that meet as deep as the board together go through there
now, held to what a pocket through it is. Open, for Florian: an open
contour with a spike, running out and straight back across the way it
runs, keeps its clearance from the rest of the contour, not from the
spike (refuse it, as a line drawn back over itself?); a round pocket's or
an outline's arcs are their polygons in `no_interference`, so a box
touching such an arc from inside meets the chords' slivers (3.8e-5 r)
and is reported, which no example does; and `inside()` also needs more
than 1e-6 mm2 outside, so a corner poking less than about 1e-3 mm out is
not reported.

1. `core`: the position algebra, box, board with `on`, `between` and `center`,
   scopes and paths, and layout JSON output with world transforms. With unit
   tests. [done]
2. `preview`: mesher and browser viewer for that JSON, with the watcher. This
   validates the layout format before the emitter exists and gives the loop.
   [done]
3. `emit`: the interpreter for that JSON in a fresh direct document, bodies
   named by path, with the measured levers (batching, deferred sketches, B-rep
   outlines). [done; see "Measured: compile speed" for what it does differently]
4. Snapshot [done 2026-10-11, decisions in "Master document"], in this order:
   1. The writer in Fusion: `lang/emit/snapshot.py` (loaded like the emitter,
      without the parent package) and a Snapshot button in the compiler
      add-in. With the master active it writes `snapshot.json`: planes,
      sketches as single-chain contours, user parameters, cuboid bodies as
      boxes; double-underscore names skipped, duplicates reported.
   2. Reading: `lang/master.py` with `master(path)`; the layout records the
      snapshot hash and carries boxes and contours; the preview draws ghost
      boxes and contour lines; unit tests against a committed fixture.
   3. A worked example: a sample master built by script through the Fusion
      MCP (planes, a floor outline with wheel arches, a floor profile, user
      parameters, placeholder boxes), its snapshot committed as the fixture,
      and `examples/van.py` with the floor battens and the drawer cabinet
      placed in a placeholder box.
   4. Contour limits: `.between()` takes a contour, `.gap(n)` offsets it;
      own-plane contours bound the outline, perpendicular ones are sectioned
      at both faces; checks for parts inside the module box and the gap to a
      contour. The floor battens are the test case.

Still to do (listed by Florian 2026-10-11, roughly in his order of weight):

- ~~**Cutouts**~~: done 2026-10-11 (full, cross, triangles; see "Cutouts"
  under Primitives). Left out for now: Rhombuses, tabs, patterns at an
  angle to the board's edges.
- ~~**Hardware** beyond the slides~~: done 2026-10-12 (concealed
  hinges, hatch hinges, ball catches, door latches, and sliding brackets
  for removable panels, bent and straight, which have no add-in yet; see
  "Joints and hardware"). Open: whatever else the van needs.
- ~~**Complete the slides**~~: done 2026-10-12 (Blum drawer-box
  machining; runners as boxes for every model and length).
- ~~**Joints**~~: ~~box joints~~ (done 2026-10-12, see "Box joints" under
  Joints and hardware), ~~the drawer floor's groove as a join~~ (done
  2026-10-12, `groove()`, into all four boards, see "Grooves" there),
  ~~dog bones on any inside
  corner~~ (done 2026-10-12, `board.dogbones()` and half laps'
  `dogbones=`, see "Dog bones" under Joints and hardware). Screws through
  a drawer face into the box front were dropped by Florian on 2026-10-12
  as not important.
- Arcs from the snapshot's contours (open question 16). (The preview's
  other chamfers are done, 2026-10-11.)

Added by Florian 2026-10-13:

- **Runs**: water hoses, cable runs, ducts and keep-outs, not looked at
  yet. Proposed so far, not implemented: "Runs: tubes, ducts and
  keep-outs" under Decisions (`tube`, `duct`, `keepout`, waypoint paths,
  `along(face, gap)`, pass-throughs cut where a run crosses a board,
  ports across modules).
- **Cutouts limited to an area by references**: a cutout kept to part of
  a board, its bounds given by other faces, edges and boards (as
  `between()` places a board), not only by a region shape placed with
  `at=` as now (the add-in's Bounding Box Points).
- **External components**: devices installed in the cabinets, such as
  electrical parts and appliances (not connectors, slides or other
  joinery hardware), to plan the room they need: imported from STEP or
  other CAD data, or given as outlines or boxes. Related so far: the
  joinery hardware is drawn as boxes in the layout's `hardware` list and
  checked for overlaps (CAD files were dropped for it on 2026-10-12),
  runs' `keepout`, and hand-modeled bodies as inputs (rung 3 under
  "Hand-made geometry and escape hatches").
- **Colors and appearances**: a color, or a Fusion appearance or physical
  material, given to a part or to a material for all its parts, carried by
  the layout to the preview and to Fusion. Now the preview colors parts by
  material from a fixed palette, in the order the materials come, and the
  compiled bodies get no appearance at all. Related: the grain made
  visible by an appearance (Later, under "Backend"). (The grain itself is
  done: `grain()`, the scope's default and the material's `grain` flag,
  handed to Multi Arrange.)
- **Manufacturing groups**: parts marked in the build as one group, which
  Multi Arrange then nests as a rigid group, keeping their arrangement, as
  its own groups do now (a group name per part, set by hand in its
  dialog). The compiler would write the group into the `lang`/`part`
  attribute next to the grain.
- **Bent boards**: a board bent about one axis, such as one piece running
  from a cabinet's front round a corner (radius 80, say) into its side, a
  front stepping back 100 mm in a smooth S, a panel curved all over, or a
  ceiling panel following the roof. Two halves: drawing it bent (preview,
  Fusion, checks), and its flat pattern for the machine, unrolled, with
  kerfs (slots parallel to the bend axis) where it bends. It narrows the
  non-goal "parts curved in 3D" (see Goal) to parts curved two ways.
  Proposed by Claude on 2026-10-13 and revised with Florian's answers the
  same day; only the points marked [Florian] are his:
  - Legs and bends: the straight stretches are ordinary boards placed as
    now, and a relation makes them one piece, `front.bend(side,
    name="wrap", radius=80)`. The name is required and names the piece on
    labels and in nesting [Florian]; the legs keep theirs for faces and
    joins. The radius is the outer one, on the convex face of the turn
    (no inner radius for now) [Florian]. Joins, holes and limits keep
    working on the legs, so the joint code only ever sees flat boards, and
    nothing joins on the curve. A part limited by both legs follows the
    bend's inside, as a contour limit in its plane does today. A board on
    a curve without legs (the roof's contour, an arc written in code) is
    `.on(curve)`.
  - The step from straight to bent is always smooth [Florian]: every turn
    is eased, its curvature rising from zero where a leg ends and falling
    to zero where the next begins (clothoids, as on roads and railways,
    then an arc of the radius), so `ease=` is above 0, its default a
    project rule. The legs give the shape's frame:
    - Legs meeting at a corner (their outer faces meet in a line) make one
      turn, and each leg is trimmed back as far as the turn needs (radius
      80 at a right angle: 80 mm with ease 0, 113 at 0.5, 150 at 1).
    - Parallel legs ending apart, a front stepping back: the bend fills
      the gap exactly, from where one leg ends to where the other begins,
      as an S of two turns in opposite directions with a straight stretch
      between them. The radius is the shape's control: the largest that
      fits makes a pure S whose turns meet at the inflection (a gap 250
      mm long and 100 mm across, ease 0.5: radius 122), a smaller one
      tighter turns and a straight diagonal between them (radius 80: 157
      mm at 28 degrees). Without `radius=` the S is the largest that
      fits; `radius=(150, 80)` makes an uneven one; a radius too large is
      an error naming the largest. Shapes beyond these take waypoints
      (`via()`, as runs do) or `.on(curve)`.
    - Considered for the S: a spline filling the gap, with three control
      points on each leg's line (so zero curvature at the ends) and the
      handles' length as the weight, drawn exactly in Fusion as a degree-5
      control-point spline. Its best, handle 0.2 (the minimum-jerk
      "smootherstep"), reaches radius 122 in the same gap, as the eased S
      at ease 0.5 does, but its weight means nothing on the board and the
      radius comes out instead of being given.
  - The flat pattern is a plain board: the outline unrolled along the
    neutral layer, the legs' operations moved into it, the kerfs pockets
    from one face, so the emitter's flat side needs nothing new. The neutral layer is the skin for kerfs and the middle for
    bending plywood; on a right angle at outer radius 80 in 12 mm plywood
    the two differ by about 8 mm in length, so it is a stated value,
    calibrated with a test bend.
  - Kerfs are flat-bottomed slots [Florian], all in one face, whichever
    way each turn bends, since the board bends both ways with them there
    [Florian]; the face is the one it is machined from, the inner face by
    default, so an S needs no flipping either. They are closely spaced,
    each closing only part way where a turn bends toward their face
    [Florian]: slots that close fully at the radius are too few, since a
    slot is no narrower than its cutter, and the wide webs between them
    stay straight, so the curve is not smooth. `kerfs=slots(width=3,
    skin=2, pitch=6)` spreads them at the pitch over the stretches that
    curve; on a turn toward their face each closes as far as the curve is
    tight there, on one away from it each opens. The one check is that
    none has to close more than its width at the tightest radius of a turn
    toward their face (12 mm plywood, 2 mm skin, 3 mm slots, outer radius
    80: pitch at most 21.5 mm). Without kerfs the material's minimum
    radius is checked.
  - Fusion gets two bodies: the bent one for the assembly and the checks
    (its section extruded along the bend axis, the legs' operations as
    now, no kerfs), and the flat one, which Multi Arrange and Auto Setup
    take. The preview bends the flat mesh along the neutral layer, which
    closes or opens the kerfs as far as the wood does.
  - Corners of a flat board's outline get the same eased turn,
    `fillet(corner, r, ease=)`, ease 0 being today's arc. Considered: a
    conic, Fusion's sketch Conic Curve (`SketchConicCurves.add(start, end,
    apex, rho)`), whose setback stays while rho sets the shape (0.414 is
    the circle at a right angle); every other rho is tighter than the
    circle somewhere (setback 80: 57 mm in the middle at 0.5, 30 mm at the
    ends at 0.3), and its curvature jumps where it meets a line. Figma's
    corner smoothing gets tighter than its radius (52 mm for radius 80 at
    0.3). The layout's point rings give Fusion no clothoid exactly: it
    would carry the curves, or tangent arcs fitted within 0.01 mm,
    recovered as arcs are now.

(Operations, the half lap, the connectors and the tenons are done; the
assembly experiment from question 2 was dropped as a priority on
2026-10-11, since assembling module documents is easy by hand.)

Before any of it, cheap and useful: write two real modules from the van in the
proposed syntax on paper, a bank and the rear storage, since those resolved
almost completely in the Planung check. That shows what the language lacks
faster than implementing it. And walk one existing module's timeline to bucket
its features into the escape-hatch rungs.

## Where to look in this repo

- `AGENTS.md`: dev cycle (reloading add-ins through MCP), modeling rules, testing
  through MCP.
- `lib/drawer_slides.py`: the model for a Fusion-free layout layer;
  `lib/connector_data.py` the second, for Domino, Clamex and Cabineo.
- `lib/domino.py`, `lib/edge_sketch.py`, `lib/hole_features.py`: sketch and cut
  helpers the native add-ins build with.
- `lib/group_edit.py`: stored settings per result.
- `lib/auto_setup/`: recognition of holes, pockets, contours, rim chamfers and
  V-grooves, and template-based CAM operations.
- `lib/multi_arrange/`: nesting, including the note on document write cost.
- `tools/perf/compile_bench.py` and `tools/perf/results/`: the compile-speed
  benchmark, also a worked example of the emitter's feature calls and their
  gotchas.
- `addins-src/connectors_native/main.py`: a full native add-in (inputs, geometry
  resolution from one edge, execute).

## Prior art worth borrowing from

| Project | Idea |
|---|---|
| BOSL2 (OpenSCAD library) | Directions as vectors defined once; added together to address edges and corners. https://github.com/BelfrySCAD/BOSL2/wiki/Tutorial-Attachment-Basic-Positioning |
| CadQuery / build123d | Selectors such as `>Z` (farthest face in +Z), combinable; named joints on parts. https://cadquery.readthedocs.io/en/latest/selectors.html , https://build123d.readthedocs.io/en/latest/joints.html |
| Onshape FeatureScript | Built-in features are written in the same language as custom ones. https://cad.onshape.com/FsDoc/ |
| Zoo KCL | Naming a sketch line names the face that grows from it. https://zoo.dev/docs/kcl-book/sketch_on_face.html |
| Boxes.py | Edge types per side in matching pairs; joint settings in multiples of thickness. https://boxes-audreyfeldroy.readthedocs.io/en/latest/api_edges.html |
| Carpentry Compiler (2019) | Separate design and fabrication languages with a manufacturability check. https://grail.cs.washington.edu/projects/carpentrycompiler |
| Polyboard | Construction rules as a style sheet with swappable sub-methods. https://wooddesigner.org/help-centre/polyboard-manufacturing-methods/ |
