# Emitter and Fusion backend

How a layout becomes a Fusion document, why it is done this way, and what
was measured. Part of the modeling language's design; the overview is
`DESIGN.md`. Code: `lang/emit/plan.py`, `loops.py`, `arcs.py`, `nested.py`,
`cam_plan.py` (Fusion-free), `lang/emit/fusion.py` (draws), `cam.py` (the
CAM setups), `addins-src/compiler/`.

## Decisions

- Use Fusion's own features (extrude, hole, chamfer, combine). Do not build
  bodies with our own B-rep code, which would mean reimplementing what
  Fusion already does. [decided]
- The timeline of a generated document is written top to bottom and thrown
  away on the next compile. It is never edited, so no reference ever has to
  be re-resolved: each feature is handed its faces and edges at the moment it
  is created.
- Each module compiles in its own small document, since write cost grows
  with the number of features already in the document (measured below).
- Compile into direct-modeling documents, 5-10x faster than parametric ones
  and enough for everything the emitter does; a parametric document stays a
  debug mode, because its timeline is a readable log of how each part was
  built.
- Compiler output has no sketch constraints and no dimensions. The AGENTS.md
  rule on fully constrained sketches is for the interactive add-ins, whose
  results users edit in the timeline. Generated documents are never edited.
- The emitter is one generic interpreter with a small instruction set: part,
  cut, pocket, hole, chamfer, V-groove, name, hardware box. Every joint and
  hardware pattern reduces to those operations on faces of flat parts, which
  is also what Auto Setup recognises.
- Units are millimetres everywhere in the language and centimetres only
  inside the emitter.
- Where code runs: the snapshot and the emitter run in Fusion, the layout
  step anywhere (plain Python with shapely). Fusion's Python has no shapely,
  so `lang.emit` is loaded inside Fusion without its parent package (see
  AGENTS.md). The compiler add-in's Compile Layout button picks a layout,
  nest or CAM plan file and runs it.

## What the emitter does

- A Fusion-free plan step (`plan.py`) works out world geometry, batching and
  chamfer contours, and is unit tested; the preview's mesher reads the layout
  through the same plan (see `design/preview.md`). `fusion.py` draws it into a
  fresh direct document with one component per scope and bodies named by
  path.
- Every outline and pocket shape is a temporary B-rep face built from
  `Line3D`, `Arc3D` and `Circle3D` (the arcs recovered as in
  `design/geometry.md`), so no sketch is drawn at all; pockets are batched per
  face and depth into one cut, a pocket of several pieces split by the plan;
  holes are one hole feature each, positioned by a point on the face
  (`setPositionByPoint`), since batching barely matters in direct mode and a
  sketch per face would auto-project the face; chamfers are equal-distance
  chamfers on edges found by their midpoints along a contour, a contour's
  loops in one feature and, when Fusion fails it, by halves, leaving a loop
  it cannot chamfer sharp with a problem noted.
- Through pockets cut by distance (Fusion's through-all extent failed or
  stopped short with other components in the document).
- An operation on a narrow face carries an `offset`, how far in front of the
  face it starts, which the plan turns into the plane the cut starts from.
- Hardware bodies are unions of temporary B-rep boxes, each in a component of
  its own.
- A feature Fusion refuses does not stop the compile: the part goes on
  without it, the other holes of a batch are still drilled, and the report
  lists it under problems, apart from the build's own checks, so the document
  shows everything that worked. The emitter drops its temporary faces when a
  step fails.
- The compiled examples come out as the preview's: every body one solid,
  volumes within 0.03 % (the polygons' chord errors).

## Nested documents

A nest file (`design/nesting.md`) is drawn a document per material:
`lang/emit/nested.py` plans it (Fusion-free, unit tested), `NestEmitter`
draws it, and Compile Layout takes a `nest.json` as it takes a layout. Each
piece of stock is a component, each blank one in it at its place holding the
blank as a see-through stock body and its parts' bodies flat, machining face
up, named by path, with their facts moved along. A part is drawn where the
layout has it, with the steps of its module document, and the finished body
is copied into place by the nest's transform; every component sits at the
origin. Drawn inside a component whose occurrence was moved, most parts
failed ("the path is tangent to the profile": Fusion read the profiles in
the other space) and the others came out a thickness too high
[2026-10-14].

## CAM setups

A CAM plan (`design/cam.md`, `cam.json`) is built into the nested
documents: `lang/emit/cam_plan.py` (Fusion-free, unit tested and fuzzed)
checks the plan against the nest beside it, maps every setup's features
from its blank's frame into the document (`nested.sheet_places`, the
blank's corner, the stock's top at the nominal thickness) and says what
each binds by and which parameters each operation gets; `cam.py` builds
them after `NestEmitter` has drawn the document: every sketch first (tab
positions, rest regions), `checkValidity`, then per blank a setup with a
fixed-box stock the blank's size whose height is the measured thickness to
enter, per operation one from its template file, its parameters written,
its geometry bound by position (silhouettes, loops of edges, floors,
cylinders, arc edges, a chamfer's lower edges, a groove's bottom), every
chain turned so the tool runs on its waste, and the toolpaths generated at
the end. The faces and edges are found as the chamfers are: by position,
in the body each part path names on its blank, read once per body.
Details and what was verified: `design/cam.md`, In Fusion.

## Handing parts to Multi Arrange and Auto Setup

- After a compile, Auto Setup derives CAM from the geometry; the language
  nests on its own (above), and Multi Arrange stays a way to nest in
  Fusion. Multi Arrange works in the compiled direct documents as they are:
  it solves in a parametric scratch document and places the nested copies
  without base feature or timeline group. Where Auto Setup runs is open (see
  `design/proposals/cam.md`).
- The compiler hands each part's facts to those tools as a JSON attribute
  `lang`/`part` on its body: path, kind (a board, or a slat, which Multi
  Arrange's compiled parts leave out), material, thickness, whether the material
  has a grain, the grain direction (null when the build left it unset) and
  `up`, the outward normal of the face it is machined from. That face is the
  one `machine()` names, else the big face more pockets, holes and chamfers
  are made from (a cut's chamfer counts for the show face), the show face on
  a tie; the layout carries it as `machine`. Multi Arrange uses the build's grain before its own guesses
  (texture, longest edge), lets parts of a material without grain turn
  freely, and adds all compiled parts of a material at once (Compiled parts +
  Add in its dialog), each by its machining face, so it lands machining side
  up.

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

- Parametric cost per feature grows linearly with the document (0.22 s for
  the first pair, 4.7 s for the 60th), so a module compiles in quadratic
  time. The cost is the compute after every write, not the kernel: in a
  60-board document a sketch line costs 7 ms parametric and 1 ms direct.
- Direct modeling grows too, but with a seventh of the slope (0.12 s to
  0.62 s per pair over 60 pairs).
- Sketch entities are half the parametric cost. `Sketch.isComputeDeferred`
  cuts the 60-board parametric compile from 31.6 s to 19.6 s; outlines as
  temporary B-rep faces to 22.1 s; both 15.7 s. In direct mode deferral gives
  5.6 s, B-rep outlines 5.6 s, and B-rep faces for the mortise slots as well
  4.1 s.
- Batching (one hole feature with eight points, one cut with six profiles)
  halves the parametric time and barely matters in direct mode.
- "To object" extents cost the same as distances.
- Repeats after a Fusion restart matched the first runs within 3%.
- Today's emitter, with no sketches at all, draws the drawer cabinet (23
  parts) in under 2 s and the van example (42 parts, 119 features) in 1.0 s.

## Measured: document writes (2026-10-17)

The van example (42 parts, 233 features, two modules) compiled in 2.3 s, in
a Fusion session holding 53 open documents, plus 0.12 s for the new document
and 0.58 s for the viewport fit the add-in asks for. The drawer cabinet's
nest (12 parts, one material) in 1.24 s. Per step, the emitter's methods
timed from an MCP script:

| step | count | s | each |
|---|---|---|---|
| pocket steps (`_pockets`) | 64 | 1.35 | 21 ms |
| bodies (`_make_body`) | 42 | 0.42 | 10 ms |
| holes (`_holes`) | 116 | 0.42 | 3.6 ms, 1 ms of it `_find_face` |
| V-grooves | 8 | 0.03 | |
| the nest's copy, move and place | 12 | 0.07 | 5.5 ms |

The cost is document writes, not kernel work: the 233 features take 1 046
writes, because every pocket profile is a temporary face body of its own,
added and deleted again (308 adds and 308 deletes for 64 extrudes), and
every hole is a feature with a face search before it. A write in a direct
document costs 2 to 20 ms and grows with the document (above), so the count
of writes per part is the measure to cut; `design/proposals/performance.md`
has the options.

What a fresh direct document showed the same day:

- A body from a temporary face, an extrude and the face's deletion: 4 ms.
- A hole feature: 2.8 ms (3.6 ms in the van's document).
- The same hole as a temporary cylinder (`createCylinderOrCone`) subtracted
  from a temporary copy of the body with `booleanOperation`: 0.1 ms, in
  memory, the volume exact; adding the copy and deleting the old body, once
  per part, 11 to 21 ms. Forty holes: 17 ms instead of 112 ms.
- A pocket step of six circles the emitter's way: 11 ms (adds 2, extrude 7,
  deletes 2; 21 ms in the van's document). As six temporary cylinders: 0.2 ms
  each.

## Fusion findings

- A sketch on a face auto-projects the face edges, so its profiles include
  the whole face (pick profiles by area).
- Fusion stores arcs counter-clockwise, so an arc's start and end sketch
  points cannot be chained from.
- A face's plane normal is not reliably its outward normal in a direct
  design (pick faces by position).
- Body proxies returned inside a base feature's edit session go stale after
  `finishEdit`.
- A temporary B-rep face's normal follows the wire winding, so the extrude
  direction must be derived from the face normal.
- A through hole "to" the opposite face needs the `directionHint` argument or
  Fusion reports no target body.
- An edge can only be chamfered once, so a build must not let an outline
  chamfer and an edge or cut chamfer share an edge.
- Fusion's sketch Offset keeps sharp corners and runs arcs on along their
  circles (see `design/geometry.md`).
- Fusion chamfers over a pocket from the other face near the rim but not
  under it, over openings through the board (stopping at them), along edges
  between rounded corners at any size, but not along a cut's side lowered all
  along; it chamfers no rim through a vertex where material meets at a point
  only (non-manifold). Chamfers of 6e-5 mm fail.
- A session-wide slowdown of every modifying call after many document cycles
  is open (see `design/bugs.md`).
- Two disjoint temporary sheet faces united with `booleanOperation` give one
  sheet body with two faces (two lumps), so one temporary body can carry
  every profile of a pocket step (2026-10-17).
- A prism cannot be built in memory: `createRuledSurface` (it takes the
  `BRepWire`s, `wireBody.wires.item(0)`, not the wire bodies) between an
  outline's wires at two heights, united with two planar caps, stays a sheet
  body (`isSolid` false, volume 0). A stitch feature in the design makes it a
  solid, returning None while doing so, which costs the same writes as the
  extrude (2026-10-17).
- Temporary-B-rep booleans of cylinders and boxes have given exact volumes;
  a torus boolean was wrong once (2026-10-04).
