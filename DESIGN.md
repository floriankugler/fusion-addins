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
  hand-modeled and are referenced by name.

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
  `miter`. A cut changes the outline for everything after it; a chamfer on a
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
- A module is written in its own frame and placed: `module(name, box,
  front=box.right)` makes it open toward the box's right side; top stays up,
  left and right are a cabinetmaker's, standing in front of it; `mirrored=True`
  swaps them. Inside, `cab.back`, `side.inner.front(37)`, `rect(depth=...)`
  and `width`, `depth`, `height` are the module's own, child scopes inherit
  the frame, and the layout file carries world names, so the preview and the
  emitter never see module frames. A cabinet type is written once and placed
  on either wall, rotated or mirrored, which is the usual case when a module
  is designed before it has a project. [decided 2026-10-10]
  `front=` is what makes a module a cabinet [decided 2026-10-12]: without
  it a module takes the enclosing frame as it is, in the van the van's own
  terms, the driver's left, which suits van-level modules such as the
  floor, the ceiling or wall panels. A cabinet says which way it opens,
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
  the chamfer side. [proposed]
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
  faces]
- **Cutting with a part or a box** [decided 2026-10-10]: `side.cut(floor)`
  removes the region the floor occupies inside the side, its outline through
  its thickness; a pocket from the face the region enters through, or a
  through cut when it passes the whole thickness. `cut(box)` does the same
  with a box. Room for a fit is stated on the region, not on the operation:
  `side.cut(floor.box().grown(top=0.5, left=0.5))`, so the gap is explicit
  per side and the operation stays a plain cut. A part as a `between()`
  limit means its nearest face; `part.into(n)` and `part.gap(n)` move it.
  This is the primitive the `groove` joint will reduce to.
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
  one axis of the face.
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
- **Roundovers** are not modeled. [decided]
  They can be a note on an edge that shows up on labels and work lists. [proposed]
- Corner radii are properties of the 2D shape, so a pocket's inside corner equals
  the cutter radius by construction and no 3D fillet feature exists. Chamfers and
  holes map to Fusion's features. [proposed; "fillets" in the original wording
  meant these corner radii]
  Anything that does not fit the flat model goes through the escape hatches
  below; that flags the part as no longer plain flat work. [proposed]
- **Polygons** [proposed]: clip a rectangle's corner; trim by reference planes with
  `between`; walk an outline step by step; a raw point list as escape hatch.

### Placement and references

- A module is a box with six named sides. Boards sit `on` a side or reference and
  are trimmed `between` neighbours, so most parts carry no dimensions of their own.
  `interior.split()` divides space, for example into drawer bays. [proposed]
- Which side the thickness goes: `.on()` a module side puts the thickness
  inward; `.on()` a bare plane requires a side. Limits missing from `.between()`
  default to the enclosing scope's box. When a part is given as a limit, its
  nearest face is meant. [proposed]
- The constructor is `board(name, material, shape=None)`; the placement
  modifiers are `.on(ref, toward=)`, `.between(*limits)`, `.center(pos)`,
  `.inset(n)`, `.grain(along)`, `.show(face)`, `.manual()`. `.inset(n)` shrinks
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
  a contour in a perpendicular plane is sectioned at both big faces of the part
  and the tighter result wins, so the part fits over its whole thickness. Both
  are polyline math on the snapshot (`lang/core/contours.py`). [implemented
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
    cross each face once. Where the contour leaves several stretches (a
    batten along the wall, cut in two by a wheel arch), the part's limits
    on that axis pick one: a single limit the stretch it lies in, two
    limits the one between them, and two limits spanning several stretches
    are an error naming them, since a part is one piece. So the two pieces
    of an interrupted batten are two parts, each given one end:
    `between(..., floor_outline, floor_front)` and `... floor_back)`.
    [decided 2026-10-11]
  - `contour.gap(n)` keeps n of clearance, measured in the contour's plane
    with round joins, so it is exact at corners; `contour.into(n)` reaches
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
  - a weighted mix of positions whose weights add up to 1 gives a position;
  - anything else (a bare sum of two positions, mixing axes) is an error.
  This only works for flat, parallel references.
- `+` and `-` move along the axis. Fits against a part use `.into(n)` and
  `.gap(n)`, which need no sign convention and also work on contours, by
  offsetting the curve. [proposed]
- A cut starts at the face of the board it is declared on. One extrude through two
  panels becomes a loop over both. [proposed]

### Master document

- One master per van build, holding planes, base boxes and shapes that the modules
  refer to. Optionally one reference document per module for extra hand-drawn
  geometry. Everything else is generated on top. [decided]
- Four kinds of reference [decided 2026-10-11]: planes, which give a
  position; contours, which give a shape to follow; placeholder boxes, rough
  bodies drawn in the master to divide up the room, which become module
  boxes (`module("kitchen", van.box("Kueche"), front=...)`); and the
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
  [decided 2026-10-11]
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
  Spelling [proposed]: inside a module, `cab.export("top", top.top)` publishes a
  reference; a module function returns its module object, and the importer reads
  `kitchen.top`. Modules import the build's master index as `van`
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
    chain without branches;
  - surface bodies, duplicate names (per kind: a plane and a sketch may
    share a name) and sketches that are not one chain are listed as
    problems in the file instead of failing the snapshot, and using such a
    name in a build is an error that repeats the problem;
  - the hash covers the content, not the document's name, and the file is
    deterministic (rounded to 0.1 micrometre, sorted, one point per line),
    so an unchanged master gives an unchanged file.
- Reading it [implemented 2026-10-11]: `van = master("snapshot.json")` in
  the build file (a relative path starts at the calling file's directory),
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
  in the contour's plane by its outline, any other by its box).
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
  board's thickness. Exact for outlines (a toe kick notch in the side
  shortens the bottom's contact); pockets do not count; an end interrupted
  by a notch gives one contact per piece. Joint layouts take a contact plus
  settings and return operations for both parts. [implemented 2026-10-11]
- Besides contacts there are **crossings** (`lang/core/crossing.py`): two
  boards in perpendicular planes whose material passes through each other,
  like battens across and along a floor. They share one axis, the line
  their planes meet along; each board's material at the other's thickness,
  projected onto that axis, gives the height they share. `no_interference`
  uses this too, so lapped boards are not reported. [implemented
  2026-10-11]
- The first joint is the **half lap** (`lang/joints/laps.py`) [decided and
  implemented 2026-10-11]: `long.join(battens, using=half_lap(toward=
  floor.top))` laps the board with each board named, all of which it must
  cross. Its own notches open toward `toward`, the other boards' the
  opposite way;
  the split lies in the middle of the height both share at each crossing
  (`at=` a position instead), and `clearance=` widens each notch per side
  (default 0). Each notch is a through cut named `lap_<other board>`, so
  the emitter needs nothing new. `Board.join(*partners, using=joint)`
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
  for the others, the add-in's default), or at the positions `at=`. Every
  operation is on a big face:
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
  board, station, letter). Round access pockets are hole features; the
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
  by the shoulder); none where a mortise breaks out of its board or a
  tenon is flush with its board's end. Reliefs and mortises are round
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
  the screw plus 0.4 wide (a chamfer on the hole's edge); `offset=12`
  puts two beside each tenon instead. `screws(tenons=t)` drills through
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
- Hardware carries its own rules. A drawer slide determines the drawer box width,
  length, position and floor recess, so those numbers never appear in cabinet
  code. [decided; first hardware implemented 2026-10-11]
  `lang/hardware/slides.py`: `DrawerSlide(model, nl)` with the models of
  `lib/drawer_slides.py`. `slide.drawer_box(bay, front=face.back,
  side_thickness=, height=)` is the drawer box: the sides' inner faces 21 mm
  from the carcass sides (inner width LW - 42 in both catalogs, sides up to
  16 mm), NL - 10 long, with the bottom panel's underside 28 mm above the
  bay bottom (10 below the screw row; Grass, Blum assumed) and the sides
  hanging below it by `slide.recess` (Grass 10-13, Blum 12-15, default the
  middle), so the sides' lower edge is `slide.side_lift` above the bay
  bottom; it refuses a bay shallower than NL + 3.
  `slide.machine_box(sides=(l, r), front=f, back=k, floor=floor)` machines
  the drawer box (Grass; no Blum data yet): a cut-out at each end of the
  front board for the couplings, 69 mm wide from the side's inner face,
  and one at each end of the back board for the rear hooks, 35 mm wide,
  both from the board's lower edge up to the floor's underside; and three
  pre-drill holes per hook into the back board's rear face
  (`hook_predrill`, default 2 x 8): 42 mm from the side's inner face at
  15 and 47 above the floor's underside, and 10 mm from the inner face at
  47. Cut-outs are named `coupling_left`, `hook_right` and so on.
  `drawer.mount(slide, sides=(left, right), front=face.back)` pre-drills the
  carcass sides: a row 38 mm above the bay bottom at the hole positions the
  add-in uses, measured from the runner's front. Hardware mounts through
  `Scope.mount(hardware, **options)`, which hands the scope to the hardware
  object, so core knows nothing about slides.
  The runner pair's 3D model is placed too: the layout has a `hardware`
  list per module (a model file relative to the repository, the model's
  axes as world directions, a world origin, and per-body offsets in the
  model's frame plus an envelope box), the emitter imports the STEP into
  the scope's component and moves each body into place, and the preview
  shows the same model from the CAD box's glTF export, whose pieces are
  assigned to bodies by their envelopes because the file names nothing;
  without a mesh file the envelope boxes stand in. Häfele's CAD box delivers the file (`teccad.hafele.com`,
  `ccHandler.aspx?CadBox=2&CssClass=topco&Mandant=HDE&ArtikelNr=...`,
  format STEP, article 433.19.608 for Dynapro 40 kg NL 450) as a left and
  right runner 400 mm apart; in it x = 0 is the mounting face, y = 0 the
  runner front 4 mm behind the carcass edge, and the screw row sits at
  z = 35.9, which the placement aligns with the pre-drilled holes.
  Verified: all 24 pre-drill holes of the example coincide with the
  runners' screw holes. Not yet: Blum's drawer-box machining and models
  for other lengths and for Movento; one slide variant is the prototype
  for now. The model files are committed with the code so that the build is
  one package. Sources: Grass "Dynapro Planungshinweise" 113378 12/2021
  (the definitive sheet: installation dimensions, fastening positions and
  assembly steps), Blum TD-132/1 DE/06.22 p.5.
- Not covered by an add-in today, as far as seen: a groove for drawer floors
  (done with `side.cut(floor.box().grown(...))`), and the drawer-box
  dimensions per slide model (box width, length, recess, the coupling and
  hook cut-outs and the hook pre-drilling are in `lang/hardware/slides.py`
  for Grass; Blum is still to be collected). [open]

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
  grow with the module.
- Shown: boards as extruded polygons in van coordinates; through cuts exact, since
  they are in the outline; holes and pockets exact through mesh booleans
  (manifold); chamfers too [implemented; all kinds since 2026-10-11]: a
  hole's as a cone, one along a contour (a cut's or pocket's rim, a face's
  outline) as a frustum from the contour at the chamfer's depth to the
  contour moved its size into the material at the face, with mitred
  corners, one along an edge as a triangular prism; hardware as catalog
  envelope boxes,
  later the real meshes exported once from Fusion; the vehicle and master
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
  `show`, `hide`, `select`, `section`, `parts`, `ops`, `loaded`), so a
  tool driving the browser frames a part, a scope or a named operation
  from a named direction in one call instead of steering the mouse
  (AGENTS.md has the details). The camera is kept in the URL hash, so a
  link or a reload shows the same view.
- SpaceMouse: the viewer talks to 3DxWare's navigation server
  (`lang/preview/viewer/spacemouse.js`), which works in Chrome and in the
  Claude app's browser pane, not in Safari. The page connects in Safari too,
  but the driver does not route the puck to the navigation server while
  Safari is frontmost and zooms the page instead (checked 2026-10-11). A
  workaround through 3DxWare's legacy client framework, taking over the
  puck for Safari in the preview server and navigating the page from the
  raw axes, was considered and not built. [decided 2026-10-11]

## Examples

These show the intended feel. None of the functions exist.

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
    for z in spread(side.bottom + 100, side.top - 100, pitch=32):
        side.hole(d=5, depth=10, at=side.inner.front(37).bottom(z))   # a shelf-pin column

shape = rect(depth=500, height=720).clip("top.back", top=380, back=120)   # polygon
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

The construction assumed here (inset fronts, box-jointed drawer boxes, grooved
floor) was not confirmed by Florian.

```python
ply15 = material("birch", t=15)
ply12 = material("birch", t=12)
ply9 = material("birch", t=9)
GAP = 3  # between fronts


def drawer_cabinet(name, box, n, slide, front=None):
    with module(name, box, front=front) as cab:          # written in its own frame
        left   = board("left", ply15).on(cab.left)
        right  = board("right", ply15).on(cab.right)
        bottom = board("bottom", ply15).on(cab.bottom).between(left, right)
        top    = board("top", ply15).on(cab.top).between(left, right)
        back   = board("back", ply9).on(cab.back).between(left, right, bottom, top)

        back.join(left, right, bottom, top, using=domino("4x20", count=2))
        bottom.join(left, right, using=tenons(count=3))
        top.join(left, right, using=tenons(count=3))

        for i, bay in enumerate(cab.interior.split("height", n), 1):
            d = drawer(f"drawer{i}", bay, slide)
            d.mount(slide, sides=(left, right))        # Drawer Slides add-in
            d.face.latch(right, "pull_lock_44")        # Door Latch add-in

        cab.export("top", top.top)                     # for whatever stands on it
        cab.check(no_interference, fits_sheet)
    return cab


def drawer(name, bay, slide):
    with scope(name) as d:
        board("face", ply15).on(bay.front).inset(GAP / 2)   # registers as d.face
        box = slide.box_space(bay, behind=d.face, height=bay.height - 30)

        l = board("left", ply12).on(box.left)
        r = board("right", ply12).on(box.right)
        f = board("front", ply12).on(box.front).between(l, r)
        k = board("back", ply12).on(box.back).between(l, r)
        floor = board("floor", ply9).on(box.bottom + slide.recess).between(l, r, f, k)
        f.join(l, r, using=box_joint())
        k.join(l, r, using=box_joint())
        floor.join(l, r, f, k, using=groove(depth=5))
        d.face.join(f, using=screws(count=4))
    return d
```

(Joinery rules, which would have made every `join` above disappear, were
dropped on 2026-10-11; joins name their partners.) Things to notice: no
board has a dimension, no line names an edge, and the slide decides the
drawer box.

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
edge.

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
(hardware bodies included; clicking a group hides or shows all of it). The emitter is a
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
- **Hardware** beyond the slides, as `Mountable` objects like
  `DrawerSlide`, each with its add-in as the reference: concealed hinges
  (concealed_hinge_native), hatch hinges (hatch_hinge), ball catches
  (ball_catch), door latches (door_latch_native), and whatever else the
  van needs.
- **Complete the slides**: Blum (Movento) drawer-box machining, runner
  models for other nominal lengths and for Movento, the other Dynapro
  load classes.
- **Joints**: box joints (box_joint), the drawer floor's groove as a join,
  screws through a drawer face into the box front (two boards face to
  face, which contacts do not cover yet), dog bones on any inside corner
  (dog_bones_native).
- Arcs from the snapshot's contours (open question 16). (The preview's
  other chamfers are done, 2026-10-11.)

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
