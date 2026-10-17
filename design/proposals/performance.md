# Performance

Status: proposed by Claude on 2026-10-17 after measuring the preview loop
and the Fusion compile on `examples/van.py` (42 parts). The same day Florian
made turnover a design goal (`DESIGN.md`, Performance), and PR #12 built the
preview side: compact layout JSON, the server's cached nests, numpy rings in
`clean`, the mesher's levels and the per-part mesh cache (`design/preview.md`,
The mesher). The van's save-to-picture went from 3.2 s to about 1.5 s, the
build itself from 2.4 s to 1.0 s on a change to one part. What is measured
lives with its topic (`design/preview.md`; `design/emitter.md`, Measured:
document writes); this file holds what is still open, in the order to take
it.

## The loop that matters

The daily work is on one module [Florian, 2026-10-17]: a cabinet or a bed of
a few dozen parts, saved and looked at over and over. The whole van is
previewed now and then, between those cycles, and may take seconds. So the
loop to budget is a module's, and a module's build is about the size of the
examples measured here.

## The compile into Fusion

The van's 233 features take 1 046 document writes, and writes are what a
compile costs (`design/emitter.md`, Measured: document writes, with the
experiment behind the options). In the order to try them:

1. **One profile body per pocket step.** Unite the step's faces into one
   temporary body before adding it (a union of two disjoint sheet faces is
   one body with two faces); the extrude takes `body.faces`. For the van:
   1 046 writes become about 560. No change to what is drawn.
2. **Primitives as temporary booleans.** Holes (cylinders, flat-bottomed as
   the language means them), countersinks (cones), V-grooves (a box turned
   45 degrees about the groove), and the pockets that are circles, slots
   (the layout carries `slot`) and axis-aligned rectangles (158 of the van's
   308 pocket shapes), subtracted in memory from a temporary copy of the
   body after its extrude cuts, the body then replaced once. The other
   pockets stay extrude cuts (150 shapes with arcs: tenons, mortises,
   notches), since a prism cannot be made in memory. All of them are
   subtractions, so the order among them is free; chamfers come last, as
   now, and find their edges by position. For the van about 420 writes, an
   estimated 1 s instead of 2.3; the gain grows with the document. Check
   with the Fusion batch (`tests/fuzz/fusion_batch.py`), which compares
   every body's volume with the preview's.
3. **Batch pockets per face and depth, not only consecutive ones**: 64 steps
   become 52 in the van. Small.
4. `_find_face` walks every face of the body for every hole (116 walks); it
   goes away with option 2, else `findBRepUsingPoint` on the component is
   the fast lookup.

The nest documents draw each part with the same steps and then copy it into
place, so they gain the same; the copy itself is cheap (5.5 ms a part).

## What is left in the preview loop

After PR #12 a module's save-to-picture is three fixed costs and the build
file:

| stage | s | why it stays |
|---|---|---|
| waiting for the page's 0.7 s poll | 0.35 | latency, not work |
| interpreter and imports | 0.5 | a fresh process per build; trimesh 0.3 of it |
| running the build file | 0.3 | sequential by nature |
| layout, JSON and the scene from the cache | 0.2 | |
| the page | 0.2 | rebuilds the whole scene |

Each fixed cost has an answer that is not a cache:

- **A warm builder process** in the preview server: the imports done once,
  `lang` and the build's modules imported afresh per build. It is also
  where a worker pool would live (see Parallelism). Or, instead, drop
  trimesh from the build by using manifold3d directly (it extrudes a
  `CrossSection`, makes cylinders, revolves and hulls, and does batch
  booleans; the frustums as `Manifold` from vertices and triangles, a small
  glb writer): the last third of the mesh time and the 0.3 s import.
- **Push instead of poll**: the server tells the page when a build is done
  (server-sent events or a long poll) instead of the page asking every
  0.7 s.
- **Replace only what changed in the page**: the layout carries each part,
  so the page can keep the meshes of the parts whose entry did not change
  (the mesh cache's hash, written into the layout or a side file) and
  rebuild the few that did; this grows no further with the design.

What remains then is running the build file: about 7 ms a part after the
numpy rings, so a module of forty parts costs 0.3 s and the whole van
several seconds. For the module that is fine. For the van it is the one cost
that grows with the design and that neither caches nor cores touch; the
answer there, if it is ever needed, is **building one module at a time**
(modules already run lazily and compile separately, so a build that runs
only the chosen module's body and leaves the others as they were is in
reach, with cross-module joins and references the part to get right), or
reusing a module's layout while its source, arguments and settings are
unchanged. Since the van is previewed now and then, this waits until the
whole-van build actually hurts.

## Curves instead of polygons in the layout

Asked by Florian (2026-10-17): is JSON a bottleneck? No. The van's layout
(10.7 MB indented, 5.3 MB compact) was written in 0.08 s, parsed in 0.044 s
in Python and in 11 ms in the page (7 ms compact), fetched in 12 ms on
localhost, and the 4.4 MB glb in 9 ms: about 0.15 s of the loop, and compact
JSON took a third of that away. What the size reflects is the content:
134 800 points, 97 800 of them in operations, most on circles of 360 points
(every circle the language draws has a vertex per degree,
`cutouts.circle_geometry`, so two drawings of one circle coincide), and the
content is what costs in the mesher and in the page, not the parsing.

The alternative worth deciding is **curves, not polygons, in the layout**:
shapes as runs of lines, arcs and circles, which is what `arcs.fit` recovers
from the polygons on every read anyway (0.09 s per build for the van). A
relief circle becomes one record instead of 360 points, the van's shape data
shrinks about tenfold, the emitter draws the arcs without fitting and without
the snapping that fitting needs, the mesher tessellates at its level, the
nest at its 0.25 mm. It changes the layout contract (a version bump, every
reader: plan, mesher, viewer, nest, fingerprints) and keeps the rule behind
the whole degrees better than the polygons do: the circle itself is in the
file. Its version bump would go with another one, as the CAM stage's.

Considered and set aside: a binary encoding (MessagePack, CBOR, a JSON head
with a binary buffer for the rings as glTF does, numpy `.npz`) is two to
three times smaller and parsed a few times faster than 11 ms, but JSON is
readable, diffable and read by five tools, and ten times the parts would be
a 50 MB JSON parsed in 0.1 s while those points would long have slowed the
mesher: the format is not the lever. Faster JSON libraries (orjson) for the
writer and the server's reads: a fraction of 0.12 s, not measured.
Rounding coordinates to nine decimals (4.0 MB) passes the arc tolerance
(1e-7) and the mesher's (1e-6), but touches the rule that vertices stay
exactly on their circles; a decision, not a cleanup.

## Parallelism, considered

Asked by Florian (2026-10-17): what lends itself to more cores? Measured and
reasoned through, piece by piece:

- **The build file**: no. It is a program mutating one registry, and every
  join reads what came before it.
- **The mesher**: the one piece whose work is independent per part. Threads
  give nothing: 1.19 s on one thread, 1.10 s on four, and four heavy parts
  in four threads take 370 ms against 314 ms one after the other, because
  manifold3d's binding, trimesh and the shapely calls hold the interpreter
  lock (a Python loop in another thread gets 12 % of its usual turns while
  manifold3d booleans run; calling manifold3d directly scales no better).
  Processes work, but each new one pays the 0.5 s of imports, so only a
  persistent pool pays: a few workers in the warm builder that hold the
  imports and mesh parts as the build hands them over. With the per-part
  cache the usual edit meshes one part either way, so the cache came first;
  the pool when designs outgrow it.
- **The emitter**: no. Fusion's API runs on its main thread; the kernel
  parallelizes what it will inside a feature, and a nest's documents are
  drawn one after the other. The only lever is fewer, cheaper writes.
- **The page**: three.js builds the geometry on the main thread. A worker
  could parse the glb and compute the edge lines and hand the buffers over,
  but replacing only the meshes that changed is cheaper and comes first.
- **The server**: builds of several designs could run in parallel
  subprocesses when several pages show different designs; rare. The nest
  solver already uses the cores (`design/nesting.md`).

## Fidelity

How finely the preview draws arcs is built (`design/preview.md`, Levels:
fine and normal, two thirds of the mesh time). The level that leaves
operations out, the rough one, is `design/proposals/detail-levels.md`, with
what it buys measured there.

## Suggested order

1. The emitter: united profile bodies (a day; the compile drops by a third
   and grows slower), then primitives as temporary booleans (three days with
   the Fusion batch; the compile halves again).
2. The three fixed costs of the loop, in whatever order the loop then shows
   them: the warm builder (or manifold3d directly), push instead of poll,
   the page replacing only what changed.
3. Curves instead of polygons in the layout, when a version bump is due
   anyway.
4. Building one module at a time, when the whole-van build hurts.
