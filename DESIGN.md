# Modeling language: design brief

Status: design only, nothing is implemented. Written 2026-10-09 from a design
conversation between Florian and Claude, as the starting point for implementation
work in this repo. Revised 2026-10-10 after a design review and the compile-speed
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
  origin plus normal, every contour as a sampled polyline, and the vehicle body
  as a mesh for the preview. [proposed]
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
  reachable as attributes, so `left.toekick.top` names the face a cut made.
- **Operations keep a few keywords.** Face, position and depth interact and
  belong in one call: `pocket(shape, face=, at=, depth=)`. Splitting them into
  separate modifiers would double the length and lose the grouping.
- **Relations are methods on the moving or edge-on part.** `bottom.join(...)`,
  `drawer.mount(...)`, `face.latch(...)`, `cab.port(...)`, `cab.export(...)`.
  Methods give autocomplete an entry point that free functions lack, and the
  receiver rule removes the asymmetry of binary relations.
- **Placement resolves lazily with early errors.** `board("left", ply15)` has no
  position until `.on()`. Using `left.inner` before that errors with the part
  path and the missing fact. Since emission is deferred anyway, this costs
  nothing.
- **Faces and edges are attributes, not only strings.** `side.front` is a face,
  `side.front.inner` an edge, so autocomplete shows the six directions and a
  typo fails at parse time. Strings stay allowed where names are computed.
  Direction names and modifier names do not collide.
- **Two layouts on the page, one object.** A chain in parentheses for a few
  calls; a `with board(...) as side:` block when a part has many operations, so
  the receiver is not repeated. Both build the same part.
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
  cut, pocket, hole, chamfer, name. Every joint and hardware pattern in this repo
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
  geometry. Multi Arrange wraps its result in a timeline group today, so nesting
  and CAM happen in a separate parametric document that links or copies the
  module documents, or Multi Arrange gets a direct-design mode. [open]

### Names and paths

- Every object has a path, for example `kitchen.drawercab.drawer2.left.front.inner`.
  Code runs inside a scope, so only the tail is written. [decided]
- Mapping to Fusion [decided]:
  - scopes (module, sub-assembly) are nested components;
  - a board is a body inside its module's component, not a component of its own
    (Florian does not rely on Fusion's parts list or on drawings per part);
  - bought parts (slides, hinges) are linked components, as in existing documents.
- Directions are defined once per project, for example `left = -x`. Aliases are
  possible (`fs`, `bfs` for driver and passenger side). [decided]
  In the existing "Planung" document x appears to run along the vehicle and z is up.
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
- Mirrored modules practically never occur, so they get no special handling. [decided]
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
  layout. Operations on the narrow faces (Domino, Cabineo, screws into an edge)
  are allowed; the one-side check counts them as secondary operations, not as a
  flip.
- **Positioning an operation, `at=`** [proposed]: an operation is positioned in
  the 2D frame of the face it is on. `at=` names an anchor of that face by
  directions, `"bottom.front"` for a corner, `"front"` for the middle of an
  edge, `"center"`, and the shape's matching anchor is placed on it, so
  `.cut(rect(60, 100), at="bottom.front")` is a toe kick notch. Offsets move
  inward from the anchor: `at=("bottom.front", 20, 30)`. Positions from the
  reference algebra may replace either offset, `at=("front", shelf.top + 10)`,
  which is how a hole lines up with another part. Patterns come from `spread()`
  along one axis of the face.
- **Chamfers** are modeled geometry: along outer contours, along pocket contours,
  and on holes. [decided]
  A chamfer belongs to a contour on a face. Operations from two big faces, of any
  kind, mean the board must be flipped on the machine. [proposed]
  One spelling [proposed]: `.chamfer(what, size, face=)`, where `what` is an
  edge (`side.front.inner` or `"front.inner"`), `"outline"`, or the name of a
  pocket or hole, and `face=` defaults to the show face. `.pocket()` and
  `.hole()` accept `chamfer=` as sugar for a chamfer along their own contour.
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
  modifiers are `.on(ref)`, `.between(*limits)`, `.center(pos)`, `.inset(n)`,
  `.grain(axis)`, `.show(face)`, `.manual()`. `.inset(n)` shrinks the outline
  by `n` on every side of its box, which is how an inset front gets its gap;
  there are no one-off modifiers such as margin or lift, because
  `.on(box.bottom + slide.recess)` already says lift. [proposed]
- A box exposes its sides as positions (`box.left`, `box.top`) and its lengths
  as `box.extent(direction)`. `width`, `depth` and `height` are per-project
  aliases bound to axes where the directions are defined, so `bay.height` is
  `bay.extent("z")` in a project where z is up. [proposed]
- Contour limits: a contour in the part's own plane bounds the outline directly;
  a contour in a perpendicular plane is sectioned at both big faces of the part
  and the tighter result wins, so the part fits over its whole thickness. Both
  are polyline math on the snapshot. [proposed]
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
- Two kinds of reference: planes, which give a position, and contours, which give a
  shape to follow. [proposed]
- Naming uses what is visibly named in Fusion: one construction plane per plane
  reference, one sketch per contour (the sketch name is the reference name). No
  hidden tags on single curves. [proposed]
- `master.py` is an index that binds those names and says where exceptions apply.
  Compile fails early on a missing name, a duplicate name, or a sketch with more
  than one chain of curves. [proposed]
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
- The snapshot is the compile's only view of the master. It holds planes, contour
  polylines sampled at a stated tolerance, and the vehicle mesh. Faceting on
  curved contours is accepted for now; arcs can be carried exactly later. The
  lock file records the snapshot's hash. [proposed]

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
  The layout layer finds those rectangles from the parts' boxes. The concept has a
  name, **Contact**: the shared plane, the rectangle, the two parts, which one
  meets edge-on. Joint layouts take a contact plus settings and return operations
  for both parts. [proposed]
- Joinery rules are a list of predicate plus joint, first match wins, and an
  explicit call always beats a rule. Predicates see the contact: materials,
  roles (end panel, mid panel), visibility. [proposed]
- One vocabulary for explicit calls and rules [proposed]: joint types are
  objects with their settings, `tenons(count=3)`, `box_joint()`, `domino(size=8,
  count=4)`, `cabineo(count=2)`, `clamex(count=2)`, `screws(count=4)`,
  `groove(depth=5)`. An explicit call is `part.join(joint)` on the edge-on
  part, which joins at every contact its placement created; `into=(a, b)`
  narrows it. A rule is the same joint object behind a predicate. Connectors
  are joint types, not an option of tenons, which is what the first draft's
  `connector=` implied. Hardware follows the same receiver rule:
  `drawer.mount(slide, sides=(left, right))`, `face.latch(right, model)`.
- Hardware carries its own rules. A drawer slide determines the drawer box width,
  length, position and floor recess, so those numbers never appear in cabinet
  code. The slide data today appears to cover only the carcass hole patterns. [proposed]
- Joinery as rules instead of one call per joint, as in Polyboard's manufacturing
  methods: state once which joint applies where, write only the exceptions.
  [proposed; mechanism above]
- Not covered by an add-in today, as far as seen: a groove for drawer floors, and
  the drawer-box dimensions per slide model (box width, length, recess, rear hook
  notches). That is data to collect before the drawer example can compile. [open]

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
- Details have homes. Joints and hardware go into the rules file and into
  relation lines after the boards. One-offs go inline next to the board they
  concern. A rough module is the boards and their placement; a finished module
  is the same file plus rules and a few mount and exception lines.
- Details that drive the rough shape are chosen early as families with
  defaults: the slide family decides drawer box width and floor recess, the
  connector family and front gap decide the carcass. They live in the rules file
  and are refined to exact models later, in one place.
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
  (manifold); chamfers as lines or omitted; hardware as catalog envelope boxes,
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

## Examples

These show the intended feel. None of the functions exist.

### Board with operations

```python
side = (board("left", ply15, rect(500, 720))
        .show("outer").grain("z")
        .cut(rect(60, 100), at="bottom.front", name="toekick")
        .pocket(rect(200, 12), face="inner", at=("front", shelf.bottom),
                depth=to("outer", -3), chamfer=0.5)       # dado lined up with the shelf
        .chamfer("outline", 1)                            # the show face's outer contour
        .chamfer("front.inner", 1))                       # one edge, named by its two faces

side.chamfer(side.back.inner, 1)        # the same edge kind, as an attribute
for z in spread(side.bottom + 100, side.top - 100, pitch=32):
    side.hole(d=5, depth=10, face="inner", at=("front", 37, z))   # a shelf-pin column

shape = rect(500, 720).clip("top.back", top=380, back=120)   # polygon
```

The same part as a block, for when the list of operations is long:

```python
with board("left", ply15, rect(500, 720)) as side:
    side.show("outer").grain("z")
    side.cut(rect(60, 100), at="bottom.front", name="toekick")
    side.chamfer("outline", 1)
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


def drawer_cabinet(name, box, n, slide):
    with module(name, box) as cab:
        left   = board("left", ply15).on(cab.left)
        right  = board("right", ply15).on(cab.right)
        bottom = board("bottom", ply15).on(cab.bottom).between(left, right)
        top    = board("top", ply15).on(cab.top).between(left, right)
        back   = (board("back", ply9)
                  .on(cab.back)
                  .between(left, right, bottom, top)
                  .join(cabineo(count=4)))

        bottom.join(tenons(count=3))          # at every contact it has: left and right
        top.join(tenons(count=3))

        for i, bay in enumerate(cab.interior.split("z", n), 1):
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
        f = board("front", ply12).on(box.front).between(l, r).join(box_joint())
        k = board("back", ply12).on(box.back).between(l, r).join(box_joint())
        (board("floor", ply9)
         .on(box.bottom + slide.recess)
         .between(l, r, f, k)
         .join(groove(depth=5)))
        d.face.join(screws(count=4), into=f)
    return d
```

With a rules file saying carcass joints are tenons, drawer boxes are box
jointed and floors are grooved, every `join` above disappears and only
exceptions remain. Things to notice: no board has a dimension, no line names an
edge, and the slide decides the drawer box.

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
it; nothing is projected or healed in Fusion. [proposed; the original draft had
the emitter project the master sketch]

Nothing in `floor.py` is specific to one vehicle. The next van needs a new master
and the same floor code.

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
  catalog/        Florian's cabinet functions and joinery rules
  tests/          unit tests for core and layout, runnable outside Fusion
  tools/perf/     compile-speed benchmark
  DESIGN.md       this file
```

```
builds/<van>/
  build.py        which modules to compile
  master.py       index of names in the master document
  materials.py
  rules.py        joinery rules for this build
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
6. ~~Joinery rules~~: predicate list, first match wins, explicit call wins (see
   Joints). Predicate vocabulary still to be written.
7. ~~Connections between modules~~: module exports in Python (see Master
   document).
8. Contour limits: project one drawn master sketch into the part's plane, or
   section the vehicle body at that plane? Current answer: a drawn profile with
   exceptions looked up by position, as polylines in the snapshot.
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
    API coverage sufficient for the flat-part emitter. Open: where nesting
    and CAM run, since Multi Arrange wraps its result in a timeline group.
14. The session-wide write slowdown seen in the benchmark: cause, and whether
    many compiles per session provoke it.
15. Terminology: "module" collides with Python's term, and the files live in a
    `modules/` folder; "layout" collides with nesting. Livable, but a conscious
    choice.
16. Whether the snapshot should carry arcs exactly instead of polylines, and at
    what tolerance to sample.
17. Runs: fittings and connectors on tubes; whether a duct needs a lid part of
    its own for the cut list; how a run crossing a board at an angle is cut.
18. Detail levels: two or three, and whether chamfers belong to `full` or to a
    middle level with holes but without joints.

## First slice

The smallest path through all layers [proposed, revised 2026-10-10]:

1. `core`: the position algebra, box, board with `on`, `between` and `center`,
   scopes and paths, and layout JSON output with world transforms. With unit
   tests.
2. `preview`: mesher and browser viewer for that JSON, with the watcher. This
   validates the layout format before the emitter exists and gives the loop.
3. `emit`: the interpreter for that JSON in a fresh direct document, bodies
   named by path, with the measured levers (batching, deferred sketches, B-rep
   outlines).
4. Snapshot: one plane and one contour read from a master document into JSON,
   used as limits.

Then, in this order: operations (cut, pocket, hole, chamfer); one contact and one
holes-only joint; contour limits with the floor battens as the test case; the
assembly experiment from question 2.

Before any of it, cheap and useful: write two real modules from the van in the
proposed syntax on paper, a bank and the rear storage, since those resolved
almost completely in the Planung check. That shows what the language lacks
faster than implementing it. And walk one existing module's timeline to bucket
its features into the escape-hatch rungs.

## Where to look in this repo

- `AGENTS.md`: dev cycle (reloading add-ins through MCP), modeling rules, testing
  through MCP.
- `lib/drawer_slides.py`: the model for a Fusion-free layout layer.
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
