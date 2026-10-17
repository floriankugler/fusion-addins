# Preview

The browser preview: the fast loop of edit, look, edit. Part of the modeling
language's design; the overview is `DESIGN.md`. Code: `lang/preview/`. How to
drive it from code is in AGENTS.md.

## Why

A visual, creative process needs a loop of edit, look, edit in well under a
second. A compile into Fusion takes seconds and grows with the module, fine
for a check, too slow for the loop. [decided as a need]

- The preview is a second consumer of the layout file. A mesher turns parts
  into triangles, a browser page shows them. No kernel, no Fusion, so the
  time does not grow with the module.
- The browser viewer comes first because it works in tests without Fusion,
  validated the layout format before the emitter existed, and Claude can see
  it through the built-in browser after each edit. Considered: OpenSCAD as
  the viewer (almost no code, but no picking, paths or overlays); custom
  graphics inside Fusion's viewport (same mesh, in the van you are looking
  at, worth adding later).
- Not shown: results of the raw API escape hatch, hand-body booleans,
  appearance rendering. Those are Fusion's job, as is CAM; the nest is
  drawn by the nest step and shown as it is.

## The mesher

- The mesher (shapely, trimesh, manifold) reads the layout through the
  emitter plan's own readers (`lang.emit.plan`: `LayoutFrame`, `PartFrame`,
  `named_ops`, `chamfer_target`), so both see the same faces, depths and
  chamfer targets; `tests/test_plan_and_mesh.py` checks every operation kind
  against hand-worked volumes.
- Boards are extruded polygons in van coordinates; through cuts exact, since
  they are in the outline; holes and pockets, also in narrow faces, through
  mesh booleans. Chamfers of every kind: a hole's as a cone, one along a
  contour (a cut's or pocket's rim, a face's outline) as a frustum from the
  contour at the chamfer's depth to the contour moved its size into the
  material at the face, with mitred corners (rims that fold at short edges
  of an inside corner are meshed in slabs), one along an edge as a
  triangular prism; countersinks as revolved cones. Hardware as the boxes
  its object gives.
- A mesh boolean that fails leaves the board uncut and says so (`preview:
  ...` in the build's output) instead of hiding it.
- Levels (`lang/preview/levels.py`): the mesher meshes at a level, which
  changes the triangles and never the layout. `fine` meshes the layout's
  polygons as they are, a vertex a degree on the language's circles.
  `normal`, the preview's default, recovers the arcs and circles of
  outlines, pocket shapes and chamfered regions as the plan does for Fusion
  (`lang.emit.arcs.fit`) and draws each again with its chords at most
  0.05 mm inside it, a step at most 30 degrees, and never with more
  segments than the layout has for it: a relief circle of radius 3 gets 18
  sides instead of 360, a corner of radius 500 about 220 a full turn. Lines
  and whatever is not an arc stay as they are, and a shape drawn again that
  comes out invalid, or holds more or less than its chords allow, is
  meshed from the layout's polygon. On the van this takes the mesh step
  from 1.2 s to 0.44 s and the scene from 306 000 triangles to 38 000, the
  volume within 1e-5. `python -m lang.build --level fine|normal` (default
  normal) and `build_scene(layout, level=FINE)`; the build writes the level
  into `level.txt` beside the scene. The tests and the Fusion batch check
  mesh at `fine`, as they compare volumes; `tests/fuzz/boards.py`
  (`run_levels`, check `levels`) meshes random boards at both and requires
  the same closed meshes, the volumes within each shape's length times the
  tolerance over its height. A level that leaves operations out (rough,
  `design/proposals/detail-levels.md`) is not built.

  ![The van at normal and at fine, whole and close up on a drawer's finger
  joint with its relief pockets](../img/preview-levels.jpg)
- The mesh cache (`MeshCache` in `lang/preview/mesh.py`): a part is meshed
  in its own (u, v, t) frame and placed last, so its mesh before the
  placement depends on its entry alone. The build keeps each part's mesh
  in `out/<design>/.mesh/<hash>.npz` (`--mesh-cache DIR`, or
  `--no-mesh-cache`), the hash (`part_key`) of exactly what the mesh comes
  from: the outline, ops, thickness, axes, box and show face, the layout's
  frame, the level, and the mesher's code and libraries. The next build
  takes the unchanged parts from there and meshes the rest, and the
  folder keeps only what the last build used. A part whose meshing
  reported a problem is not kept, so it says so on every build. A scene
  from the cache is the scene meshed anew to the bit (tested on every
  example at both levels, and fuzzed: `run_cache`, check `mesh_cache`). A
  part moved (its box, or its outline in its plane) is meshed anew; a part
  renamed is not. On the van, a build after one part changed takes 1.0 s
  (the scene 0.1 s of it, the rest the imports and the build file), a
  cold one 1.5 s.

## The viewer

- A static three.js page: orbit, a collapsible part tree by path (hardware
  bodies included; clicking a group hides or shows all of it), click to
  select, hide and isolate, display modes, a capped section plane, a floor
  grid, the master's ghost boxes and contour lines (`m`), hardware on or off
  (`w`), labels with the parts' names (`n`) and their faces' names (`d`) as
  the build file writes them (a cabinet's own front and left, inner and outer
  where they resolve; the layout carries them per part as `faces`). Colors by
  material from a fixed palette. The layout's problems are listed as text; a
  selected part's info gives its grain and its settings, one line each with
  the node that set it (`material birch 15: kitchen`; the layout's
  `settings`, `design/api.md`, Settings). Proposed and not built: the grain as
  a stripe on each board, and check results drawn in the scene (interference
  pairs, sheet fit).
- The level row under Display (fine, normal) picks the level the shown
  design is meshed at. The page sends it with its next status requests
  (`status.json?design=van&level=fine`) until the server reports it; the
  server keeps it per design, for every page, marks the design stale on a
  change, and builds it at that level from then on (`--level`). The status
  says the level asked (`level`) and the one the scene on disk was meshed
  at (`built`, from `level.txt`). From code, `preview.level()` is the level
  of the scene on screen and `await preview.level('fine')` asks for one and
  resolves once its scene is on screen.
- Camera and visibility from code: the page exposes `window.preview`
  (`look`, `view`, `camera`, `fit`, `isolate`, `show`, `hide`, `select`,
  `section`, `labels`, `hardware`, `level`, `parts`, `ops`, `loaded`,
  `open`, `designs`, `design`, `version`), so a tool driving the browser frames a
  part, a scope or a named operation from a named direction in one call
  instead of steering the mouse. The camera is kept in the URL hash, so a
  link or a reload shows the same view.
- The viewer reads one layout version (`LAYOUT_VERSION` in
  `lang/preview/viewer/state.js`, kept equal to `layout_types.py`) and says
  so in the status line for another. Its bookkeeping (`state.js`,
  `scene-utils.js`) has node tests (`lang/preview/viewer/tests/`, run by
  `tests/test_viewer_js.py`), and a rebuild frees the old scene's GPU
  resources.
- Click-to-path in the viewer is the Copy Path helper outside Fusion.
- The nest view (button or key `k`, `preview.nest(on)` from code) shows a
  nest of the design as the nest step drew it (`nest.svg` in the nest's
  folder beside the build, `<module>/<nest>/`, see `design/nesting.md`):
  its name and time, the sheets with their numbered saw cuts, blanks (an
  own blank hatched), kept rests and waste, the parts labelled with their
  grain; a part clicked there is selected in the model. The side panel
  lists the design's nests as its layout gives them (`module.nest`,
  declared or one per material per module; `preview.nests()` from code)
  and shows the one chosen (`await preview.showNest('kitchen.carcass')`);
  it says whether the nest's parts are as nested, by their fingerprints
  (so a change to another module leaves it good), which changed, which are
  new and which are gone, or that it is not nested yet (also where its
  file is of an older version, without fingerprints), and Nest again
  runs `python -m lang.nesting <build> <nest>` for it, with the inventory
  beside the build file, one nest at a time and never on a save (a nest
  takes seconds to minutes); a failed nest shows its log.
- Pinning (`design/nesting.md`, Pinning) in the nest view: a nest marked
  as made says so (every sheet, or which, and frozen), what of it changed
  since it was made, what is not made and new (what its second nest takes)
  and what made is gone; its second nests follow it in the list, indented,
  and Nest again on either nests what is not made. On the drawing the
  sheets made are tinted and outlined, the parts changed since red, the
  parts gone grey. Mark made marks the nest whole, a sheet's button that
  sheet, and with a part selected (in the drawing or the model) that is
  made and changed since, Fixed by hand marks it; each asks first, posts
  to the server (`POST /made?design=&nest=[&sheet=birch 15:2]`, `POST
  /fixed?design=&nest=&part=`, which run `python -m lang.nesting --made` or
  `--fixed` and answer with what it printed, shown under the buttons) and
  writes the inventory back as the command does. From code:
  `preview.nestStates()` (the nests as the server gives them),
  `await preview.markMade(nest, [[material, sheet]])` and
  `await preview.markFixed(nest, part)` (they ask too; `window.confirm` can
  be replaced to script them).

## Serving a folder

- `python -m lang.preview examples` serves every build file in the folder,
  each built into `out/<name>/`, and the page switches between them with a
  dropdown (keys `,` and `.`; `preview.open(name)` from code). A build file
  is a `.py` file that imports `lang`; one the others import is a library and
  not listed unless it keeps a build of its own under `if __name__ ==
  "__build__":`.
- Only the designs that open pages show are built: a save of a build file
  nothing imports marks that design stale, any other change (`lang`, `lib`, a
  shared module or a snapshot in the folder) all of them, and a stale design
  builds when a page shows it. The folder is rescanned on every change, so
  new build files appear without a restart.
- A build goes to a scratch directory (its part meshes kept in the
  design's `.mesh` beside it) and moves in when it went through, so
  a failed one shows its log and leaves the last good scene; a build still
  running after 120 s is stopped and counts as failed. The log holds the
  error and the lines of the build files it passed through
  (`examples/van.py:39: bottom.join(...)`), not runpy's or the language's
  frames; a Python error raised inside the language also names where
  (`raised in lang/core/shapes.py:243`), and `python -m lang.build
  --traceback` prints the whole stack.
- The hash carries the design (`#design=van&eye=…`); without one the page
  opens the folder's first design alphabetically [decided]. Each design keeps
  its own camera, hidden parts, selection and section while the page is
  open; one shown for the first time is fitted. Given a single build file
  the server builds it into `--out` on every save.
- The watcher rebuilds the preview on every save and compiles into Fusion
  only on request, which keeps the loop fast.

## SpaceMouse

The viewer talks to 3DxWare's navigation server
(`lang/preview/viewer/spacemouse.js`), which works in Chrome and in the
Claude app's browser pane, not in Safari. It reconnects after a connection
that was up drops (3 s, doubling up to a minute), `spaceMouse.stop()` ends
it, and the driver's front view looks from the layout's `front`. The page
connects in Safari too, but the driver does not route the puck to the
navigation server while Safari is frontmost and zooms the page instead. A
workaround through 3DxWare's legacy client framework was considered and not
built. [decided]
