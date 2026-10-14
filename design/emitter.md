# Emitter and Fusion backend

How a layout becomes a Fusion document, why it is done this way, and what
was measured. Part of the modeling language's design; the overview is
`DESIGN.md`. Code: `lang/emit/plan.py`, `loops.py`, `arcs.py` (Fusion-free),
`lang/emit/fusion.py` (draws), `addins-src/compiler/`.

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
  AGENTS.md). The compiler add-in's Compile Layout button picks a layout file
  and runs it.

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

## Handing parts to Multi Arrange and Auto Setup

- After a compile, Multi Arrange nests and Auto Setup derives CAM from the
  geometry. Multi Arrange works in the compiled direct documents as they are:
  it solves in a parametric scratch document and places the nested copies
  without base feature or timeline group. Where Auto Setup runs is open (see
  `design/proposals/cam.md`).
- The compiler hands each part's facts to those tools as a JSON attribute
  `lang`/`part` on its body: path, material, thickness, whether the material
  has a grain, the grain direction (null when the build left it unset) and
  `up`, the outward normal of the face it is machined from. That face is the
  big face more pockets, holes and chamfers are made from (a cut's chamfer
  counts for the show face), the show face on a tie; the layout carries it as
  `machine`. Multi Arrange uses the build's grain before its own guesses
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
