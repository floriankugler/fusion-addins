# Performance

Status: measured and proposed by Claude on 2026-10-17; nothing built. The
same day Florian made turnover a design goal (`DESIGN.md`, Performance): real
designs are far larger than the examples, and fast turnover is what makes the
language usable, so features are designed to their cost from the start. The
two paths that matter: the preview loop (save to picture) and the compile of
layout and nest files into Fusion.

Measured on `examples/van.py` (42 parts, 233 Fusion features, two modules) and
`examples/drawer_cabinet.py` (23 parts), on this Mac, with Fusion holding 53
open documents. Numbers are one run each and vary by about 10 %.

## The preview loop

One save of the van, from the watcher to the picture, about 3.2 s:

| stage | s | where |
|---|---|---|
| the page's poll (0 to 0.7 s) | 0.35 | `lang/preview/__main__.py`, `index.html` `poll` |
| a fresh interpreter and its imports | 0.53 | trimesh 0.31 (it pulls scipy.spatial), `lang` 0.15 |
| running the build file | 0.61 | `clean` 0.60 cumulative, see below |
| layout and `json.dumps(indent=1)` | 0.13 | 10.7 MB written |
| meshing the scene | 1.07 | `lang/preview/mesh.py` |
| writing the glb | 0.01 | |
| the page: fetch 15 MB, parse, build the scene | 0.45 | fetches end after 0.1 s, the rest is processing |

The drawer cabinet: 1.8 s for the build (1.15 s of it meshing), 0.27 s in the page.

### The mesher

Of the 1.07 s, the manifold booleans take 0.67 s (23 parts have tools), building
the tools with trimesh 0.26 s, and trimesh's validity checks (`is_volume`, run
by `_extruded_polygon` and again by `trimesh.boolean.difference` on every input)
0.24 s. Twelve parts take 0.9 s of it: the drawer boxes, whose dog bone reliefs
are pockets of six circles of 360 points each (every circle the language draws
has its vertices on the whole degrees, `cutouts.circle_geometry`, so that two
drawings of one circle coincide). The van's 134 800 layout points become
306 000 triangles, which the page then has to process too.

Options, each measured on the van:

- **Mesh arcs coarser.** The plan already recovers the arcs (`lang.emit.arcs.fit`)
  so Fusion draws true circles; the mesher can do the same and draw each arc
  again at a step of its own instead of the layout's polygon. At 5 degrees a
  segment (72 per circle) the scene meshes in 0.45 s instead of 1.05 with
  100 000 triangles instead of 306 000; at 10 degrees 0.32 s and 59 000. The
  volume changes by under 1e-6 of the whole (the Fusion batch check's threshold
  is 3e-4 per body; a relief circle of 72 sides holds 0.13 % less than the
  circle, nothing on a board). The language's geometry stays as it is; only
  the triangles change.
- **Use manifold3d directly.** `manifold3d` (already installed, 3.5.4) extrudes
  a `CrossSection` from the rings, makes cylinders, revolves and hulls, and
  does batch booleans, without trimesh's per-tool `Trimesh` construction,
  vertex merging and validity checks. On the heaviest part the boolean itself
  is 0.038 s of the 0.058 s trimesh takes, and building its tools 0.005 s
  instead of 0.022 s; across the scene this is about a third of the mesh time.
  Going all the way (the frustums as `Manifold` from vertices and triangles,
  `manifold3d.triangulate` for the caps, a small glb writer) would also drop
  the trimesh import, 0.31 s of every build. The fuzz tests and `tests/helpers.py`
  use trimesh on their own and can keep it.
- **Mesh only what changed.** Each part's mesh depends on its outline, ops,
  thickness and axes alone (`mesh_part` builds in the part's (u, v, t) frame and
  applies the world transform last). A cache under the design's out directory,
  keyed by a hash of those fields, with the part's vertices and triangles,
  makes the mesh step nearly free on the usual edit, which touches one part or
  one module; the glb is assembled from the cache and the few parts meshed
  anew. The build runs in a subprocess, so the cache lives on disk (`.npz` per
  part, a few MB for the van).

Together the first two take the van's mesh step from 1.07 s to about 0.3 s;
the cache takes the usual edit to about 0.1 s.

### The build step

`clean` runs on every `Shape` (1 568 times for the van) and costs 0.60 s of the
0.61 s the build file takes, of which about 0.4 s is Python copying
coordinates: `_clean_polygon` turns rings into lists of tuples
(`list(poly.exterior.coords)`, and `_without_spikes` returns a list) and hands
them back to `LinearRing` and `Polygon`, which then iterate them point by
point (672 000 coordinate visits, 2 294 ring constructions at 0.11 ms each).
Keeping the rings as numpy arrays (`np.asarray(ring.coords)`, and arrays from
`_without_spikes`) takes shapely's fast path. `_rings` in `part.py` does the
same on its way out (0.07 s); `np.asarray(ring.coords)[:-1].tolist()` is the
array form.

### The layout file

The van's layout is 10.7 MB with `indent=1`, 5.3 MB compact. Compact JSON
costs nothing and halves what the page fetches and parses on every rebuild
(and what the server parses, see below). Rounding coordinates would get it to
4 MB at nine decimals but touches the rule that vertices stay exactly on their
circles; `arcs.fit` allows 1e-7 mm and the mesher 1e-6, so nine decimals
would pass them, but it is a decision, not a cleanup.

### The server and the page

- `status.json` is asked every 0.7 s by every open page, and `nest_state`
  parses the design's whole layout each time (`_nests`: 44 ms for the van's
  10.7 MB) while `_fingerprints` beside it caches by mtime. Caching the nests
  the same way removes a steady 6 % of a core per page and most of the
  handler's latency.
- The page spends 0.35 s on the van after its fetches: parsing 10.5 MB of
  JSON, `toNonIndexed`, `computeVertexNormals`, an `EdgesGeometry` and a
  stencil group per mesh, the part tree and labels. Fewer triangles (above)
  and compact JSON shrink most of it; beyond that the Performance panel would
  say what is left.
- A warm builder process (the heavy imports done once, `lang` and the build's
  modules imported afresh per build) would save the 0.4 s of imports per
  build, at the price of a process that must purge `lang.*` cleanly between
  builds. Worth it only after the above.

## Compiling into Fusion

The van compiles in 2.3 s (plus 0.12 s for the new document and 0.58 s for the
viewport fit the add-in asks for), the drawer cabinet's nest (12 parts, one
material) in 1.24 s. Per step in the van's document:

| step | count | s | each |
|---|---|---|---|
| pocket steps (`_pockets`) | 64 | 1.35 | 21 ms |
| bodies (`_make_body`) | 42 | 0.42 | 10 ms |
| holes (`_holes`) | 116 | 0.42 | 3.6 ms, 1 ms of it `_find_face` |
| V-grooves | 8 | 0.03 | |
| the nest's copy, move and place | 12 | 0.07 | 5.5 ms |

The emitter's cost is document writes, not kernel work: the van's 233 features
take 1 046 writes, because every pocket profile is a temporary face body of
its own, added and deleted again (308 adds, 308 deletes for 64 extrudes), and
every hole is a feature with a face search before it. In a direct document a
write costs 2 to 20 ms and grows with the document (`emitter.md`, Measured),
so the count is what to cut.

What a small experiment in a fresh direct document showed (2026-10-17):

- A body from a temporary face, an extrude and the face's deletion: 4 ms.
- A hole feature: 2.8 ms (3.6 ms in the van's document).
- The same hole as a temporary cylinder (`createCylinderOrCone`) subtracted
  from a temporary copy of the body with `booleanOperation`: 0.1 ms, in
  memory; adding the copy and deleting the old body, once per part: 11 to
  21 ms. Forty holes: 17 ms instead of 112 ms, the volume exact.
- A pocket step of six circles the emitter's way: 11 ms (adds 2, extrude 7,
  deletes 2; 21 ms in the van's document). As six temporary cylinders:
  0.2 ms each.
- Two disjoint temporary faces united with `booleanOperation` give one
  sheet body with two faces, so one body can carry every profile of a step.
- A prism without an extrude does not work in memory: a ruled surface
  between the outline's wires at two heights plus two caps unites into a
  closed sheet body that stays a sheet (`isSolid` false, volume 0); a stitch
  feature in the design makes it a solid (and returns None while doing so),
  which costs the same writes as the extrude. The body stays an extrude.

Options, in the order to try them:

1. **One profile body per pocket step.** Unite the step's faces into one
   temporary body before adding it; the extrude takes `body.faces`. For the
   van: 1 046 writes become about 560. No change to what is drawn.
2. **Primitives as temporary booleans.** Holes (cylinders, flat-bottomed as
   the language means them), countersinks (cones), V-grooves (a box turned
   45 degrees about the groove), and the pockets that are circles, slots
   (the layout carries `slot`) and axis-aligned rectangles (158 of the van's
   308 pocket shapes), subtracted in memory from a temporary copy of the
   body after its extrude cuts, the body then replaced once. The other
   pockets stay extrude cuts (150 shapes with arcs: tenons, mortises,
   notches). All of them are subtractions, so the order among them is free;
   chamfers come last, as now, and find their edges by position. For the
   van about 420 writes, an estimated 1 s instead of 2.3; the gain grows with
   the document. Check with the Fusion batch (`tests/fuzz/fusion_batch.py`),
   which compares every body's volume with the preview's; temporary-B-rep
   booleans have been wrong for tori before, not for cylinders or boxes.
3. **Batch pockets per face and depth, not only consecutive ones**: 64 steps
   become 52 in the van. Small.
4. `_find_face` walks every face of the body for every hole (116 walks); it
   goes away with option 2, else `findBRepUsingPoint` on the component is
   the fast lookup.

The nest documents draw each part with the same steps and then copy it into
place, so they gain the same; the copy itself is cheap.

## Parallelism

Asked by Florian (2026-10-17): what lends itself to more cores? Measured
and reasoned through, piece by piece:

- **The build file**: no. It is a program mutating one registry, and every
  join reads what came before it.
- **The mesher**: the one piece whose work is independent per part, and
  the one that matters most as designs grow (a 300-part design at the van's
  25 ms a part meshes in 7.5 s). Threads give nothing: 1.19 s on one thread,
  1.10 s on four, and four heavy parts in four threads take 370 ms against
  314 ms one after the other, because manifold3d's binding, trimesh and the
  shapely calls hold the interpreter lock (a Python loop in another thread
  gets 12 % of its usual turns while manifold3d booleans run, so the
  boolean itself holds the lock 88 % of the time; calling manifold3d
  directly, without trimesh, scales no better: 188 ms for four booleans
  either way). Processes work, but each new one
  pays the 0.5 s of imports, so only a persistent pool pays: a warm builder
  in the preview server with a few workers that hold the imports, import
  `lang` afresh when it changed, and mesh parts as the build hands them
  over (the build, 0.6 s, and the mesh, 1.07 s, then overlap as well). With
  eight workers the 300-part design meshes in about a second; with the
  per-part cache the usual edit meshes one part either way. The cache
  first, the pool when designs outgrow it.
- **The emitter**: no. Fusion's API runs on its main thread; the kernel
  parallelizes what it will inside a feature, and a nest's documents are
  drawn one after the other. The only lever is fewer, cheaper writes.
- **The page**: three.js builds the geometry on the main thread. A worker
  could parse the glb and compute the edge lines and hand the buffers over,
  but fewer triangles and replacing only the meshes that changed are
  cheaper and come first.
- **The server**: builds of several designs could run in parallel
  subprocesses when several pages show different designs; rare. The nest
  solver already uses the cores (`design/nesting.md`).

## The file format

Asked by Florian (2026-10-17): is JSON a bottleneck? Measured on the van's
layout, 10.7 MB indented, 5.3 MB compact:

| | s |
|---|---|
| `json.dumps` in the build | 0.08 |
| `json.load` in the server (every poll today) | 0.044 |
| fetch in the page, localhost | 0.012 |
| `JSON.parse` in the page | 0.011 (0.007 compact) |
| the glb, 4.4 MB: fetch | 0.009 |

So the format costs about 0.15 s of the 3.2 s loop, spread over the
writer, the server and the page, and compact JSON takes a third of that
away. What the size reflects is the content: 134 800 points, 97 800 of them
in operations, most on circles of 360 points, and the content is what costs
in the mesher and in the page's triangles, not the parsing. Alternatives, in
order of value:

1. **Curves instead of polygons in the layout.** Shapes as runs of lines,
   arcs and circles, which is what `arcs.fit` recovers from the polygons on
   every read anyway (0.09 s per build for the van). A relief circle becomes
   one record instead of 360 points, the van's shape data shrinks about
   tenfold, the emitter draws the arcs without fitting and without the
   snapping that fitting needs, the mesher tessellates at its own step, the
   nest at its 0.25 mm. It changes the layout contract (a version bump,
   every reader) and keeps the rule behind the whole degrees better than
   the polygons do: the circle itself is in the file. This is the
   alternative worth deciding, and its version bump would go with the CAM
   stage's.
2. **A binary encoding** (MessagePack, CBOR, a JSON head with a binary
   buffer for the rings as glTF does, numpy `.npz`): two to three times
   smaller, since a double is 8 bytes and its text about 18, and parsed a
   few times faster than 11 ms. JSON is readable, diffable, and read by the
   viewer, the nest, the fingerprints and the tests, so this is not worth
   its cost at any size the van will reach: ten times the parts is a 50 MB
   JSON parsed in 0.1 s, while those points would long have slowed the
   mesher. The format is not the lever; the content is.
3. **Faster JSON in Python** (orjson for the writer and the server's reads):
   a fraction of the 0.12 s, not measured; small and optional.
4. **Rounding** to nine decimals: 4.0 MB; a decision, as noted above.

## Fidelity levels

Florian's idea (2026-10-17): a control for how exact the preview is, since
an arc drawn as a triangle a degree is rarely what one needs to see.
Measured on the van, the mesher alone:

| level | s | triangles |
|---|---|---|
| full, as today (the layout's polygons, a point a degree on circles) | 1.21 | 306 000 |
| arcs drawn again at 5 degrees a segment | 0.51 | 100 000 |
| arcs at 10 degrees | 0.36 | 59 000 |
| 10 degrees, without holes, chamfers and V-grooves | 0.30 | 48 000 |
| 10 degrees, big-face pockets only | 0.18 | 41 000 |
| outlines only, as the layout has them | 0.14 | 148 000 |

Two axes, and they are different things:

- **How finely curves are drawn.** Changes the triangles, not the shape, so
  it needs no decision about what is shown, and it is where the time is:
  two thirds of the mesh step. The knob is better a chord tolerance than an
  angle: at 0.05 mm a relief circle of radius 3 gets 17 segments and a
  corner of radius 500 still 220, so small holes are cheap and large arcs
  stay smooth where the eye lands. (Between the levels of
  `detail-levels.md` this is the lossless one.)
- **What is shown**, the rough and full levels of `detail-levels.md`:
  leaving out holes, chamfers and V-grooves, then the narrow-face work,
  then pockets. A filter on operations, as decided there, worth a further
  0.2 s on the van; its value is the picture (the rough shape first), not
  the time. Outlines alone must be drawn coarsely too, else their own arcs
  cost more than all the operations (148 000 triangles).
- **The control.** A row under Display in the page (fine, normal, rough),
  per design, sent with `status.json`, so the server builds that design at
  that level (`python -m lang.build --level ...`) and remembers it;
  switching costs one rebuild. The default for the loop is normal; the tests
  and the Fusion batch check pin the fine level by argument
  (`build_scene(layout, level=FINE)`), since they compare volumes. A
  progressive variant, rough first and fine swapped in when it is ready,
  needs no control but costs the CPU twice; only if a switch turns out to
  be in the way.

## What is left after the caches

The daily work is on one module [Florian, 2026-10-17]: a cabinet or a bed of
a few dozen parts, saved and looked at over and over. The whole van is
previewed now and then, between those cycles, and may take seconds. So the
loop to budget is a module's, and a module's build is about the size of the
examples measured here.

With the per-part cache and the quick wins above, the van's save-to-picture
comes down from 3.2 s to about 1.6 s, and the mesher is out of the picture;
what is left is of another kind:

| stage | s | why it stays |
|---|---|---|
| waiting for the page's 0.7 s poll | 0.35 | latency, not work |
| interpreter and imports | 0.53 | a fresh process per build |
| running the build file | 0.3 | sequential by nature (0.61 today; numpy rings take half) |
| layout and JSON | 0.1 | |
| meshing, one part changed | 0.1 | the cache |
| the page | 0.2 | fewer triangles; still rebuilds the whole scene |

Three fixed costs, each with an answer that is not a cache:

- **A warm builder process** in the preview server (the imports done once,
  `lang` and the build's modules imported afresh per build) takes out the
  0.5 s of imports; it is also where a worker pool would live.
- **Push instead of poll**: the server tells the page when a build is done
  (server-sent events or a long poll) instead of the page asking every
  0.7 s; takes out the 0.35 s average wait.
- **Replace only what changed in the page**: the layout carries each part,
  so the page can keep the meshes of the parts whose entry did not change
  (the same hash the mesh cache uses, written into the layout or a side
  file) and rebuild the few that did; takes out most of the 0.2 s and all
  of it grows no further with the design.

With those, a module's loop is around 0.6 s, and what remains is running
the build file itself: about 15 ms a part today, so a module of forty parts
costs 0.3 s and the whole van several seconds. For the module that is fine.
For the van it is the one cost that grows with the design and that neither
the caches nor more cores touch; the answer there, if it is ever needed, is
building one module at a time (modules already run lazily and compile
separately, so a build that runs only the chosen module's body and leaves
the others as they were is in reach, with cross-module joins and references
the part to get right), or reusing a module's layout while its source,
arguments and settings are unchanged. Since the van is previewed now and
then, this waits until the whole-van build actually hurts.

## Suggested order

1. Compact layout JSON, nests cached by mtime in the server, numpy rings in
   `clean` and `_rings`: an afternoon, about 0.5 s off every build.
2. Coarser arcs in the mesher behind a fidelity level, normal by default
   and fine for the tests: a day with the tests; 0.6 to 0.8 s off the van.
3. Profile bodies united per pocket step in the emitter: a day; the compile
   drops by a third and grows slower.
4. The per-part mesh cache: two days; the usual edit then meshes in 0.1 s.
5. Primitives as temporary booleans in the emitter: three days with the
   Fusion batch; the compile halves again.
6. manifold3d directly, dropping trimesh from the build: a week; the last
   0.3 s of mesh time and imports.
7. The three fixed costs, in whatever order the loop then shows them: the
   warm builder, push instead of poll, the page replacing only what changed.
8. Building one module at a time, when the whole-van build hurts.
