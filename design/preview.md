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
  appearance rendering. Those are Fusion's job, as are the CAM's toolpaths;
  the nest is drawn by the nest step and shown as it is, its CAM plan over
  it.

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
  frame, the level, and the mesher's code and libraries; the operations'
  lines (`where`) stay out, so a line inserted above a part in the build
  file meshes nothing again. The next build
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
  bodies included; clicking a group hides or shows all of it) that follows
  the selection [Florian, 2026-10-17]: collapsed at first, a part selected
  in the scene, the list or the nest drawing closes every group and opens
  those above it, so it shows and earlier opens do not pile up; a caret
  click opens or closes a group by hand (with alt the ones below it) until
  the next selection, and a deselection (`esc`) leaves the tree as it is
  (`TreeOpen` in `state.js`, with node tests); click to select, hide and
  isolate, display modes, a capped section plane, a floor
  grid, the master's ghost boxes and contour lines (`m`), hardware on or off
  (`w`), labels with the parts' names (`n`) and their faces' names (`d`) as
  the build file writes them (a cabinet's own front and left, inner and outer
  where they resolve; the layout carries them per part as `faces`). Colors by
  material from a fixed palette. The layout's problems are listed as text; a
  selected part's info gives its grain and its settings, one line each with
  the node that set it (`material birch 15: kitchen`; the layout's
  `settings`, `design/api.md`, Settings). Proposed and not built: the grain as
  a stripe on each board, and check results drawn in the scene (interference
  pairs, sheet fit); both, with what else the preview could do for writing
  build files, in `design/proposals/preview-assist.md`.
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
  `section`, `labels`, `hardware`, `level`, `parts`, `ops`, `openEditor`,
  `changes`, `ghosts`,
  `loaded`, `open`, `designs`, `design`, `version`), so a tool driving the browser frames a
  part, a scope or a named operation from a named direction in one call
  instead of steering the mouse. The camera is kept in the URL hash, so a
  link or a reload shows the same view.
- The viewer reads one layout version (`LAYOUT_VERSION` in
  `lang/preview/viewer/state.js`, kept equal to `layout_types.py`) and says
  so in the status line for another. Its bookkeeping (`state.js`,
  `scene-utils.js`) has node tests (`lang/preview/viewer/tests/`, run by
  `tests/test_viewer_js.py`), and a rebuild frees the old scene's GPU
  resources.
- Lines of the build file (`design/proposals/preview-assist.md`, Lines in
  the layout, built 2026-10-17): the layout names the line that made every
  module, part, hardware item and operation (`where`, `examples/van.py:45`,
  layout version 10), found as the settings' errors find theirs
  (`lang/core/where.py`: the innermost frame outside `lang/` and `lib/`),
  so a board `carcass()` makes points at the build file's `carcass(...)`
  line, the operations a join makes in both boards at the join's line, and
  a loop's boards share one. The selection's info shows the selected
  part's or bought part's line as a link; it and the key `o` ask the server
  to open the editor there (`POST /open`, Serving a folder), and every
  `file.py:line` in the build log in the status box is such a link
  (`logPieces` in `state.js`, with node tests). From code, `preview.parts()`
  and `preview.ops(path)` carry `where`, and `await
  preview.openEditor(at)` opens the editor at a part's, a bought part's or
  an operation's (`'kitchen.left#toekick'`) line or at a line given. The
  lines cost nothing measurable (2026-10-17, on the van: 42 parts, 386
  operations, a frame walk for each): the layout step took 449 ms before
  and 448 ms after (medians of 20 runs in one process), and `python -m
  lang.build examples/van.py` 1.04 s before and after with the scene from
  the mesh cache, 0.71 s without the scene (`--no-scene`; medians of 7
  runs each, the two trees built in turn).
- What a save changed (`design/proposals/preview-assist.md`, built
  2026-10-17): on each new scene the page diffs the new layout against the
  one on screen (`lang/preview/viewer/changes.js`, with node tests), per
  path, parts and bought parts' bodies alike: added, gone or changed. A
  changed part says whether its box changed, whether it moved whole (by
  how much, in the layout's directions), was resized or turned, which of
  its operations differ, were added or removed (named ones matched by
  name, the others by being equal, then by their order among those of
  their kind), which outline segments differ, and what else (material,
  grain, nest, faces, each setting by its value, an operation's own
  settings). A part that moved whole is also compared as moved, and the
  comparison that matches more counts, so the operations that moved with
  it are no change. Provenance is no change: the build file's lines
  (`where`) and a setting's source, nor are numbers within 0.1 µm (float
  noise). The page then tints the parts changed (pink) and added (green)
  for four seconds or until a click (not a drag) or a key; keeps the parts
  gone and the old meshes of parts moved, resized, turned or reshaped as
  grey ghosts until the next build, behind the surfaces they share with
  the new meshes, so a reshaped part's ghost shows only where it was and
  no longer is; and glows, drawn through the parts at a fixed size on
  screen: a halo at each operation that differs (pink), was added (green)
  or removed (red), where `look` aims, a fainter one where a changed one
  was, a line along a chamfer's edge, and a line along each outline
  segment that differs. So a hole moved by half a millimetre is found from
  afar. Key `u` and the checkbox last save under Display show or hide the
  ghosts and glows. The panel under the build log says what changed:
  `3 parts changed: shelf.left (3 ops, outline), shelf.middle (moved
  bottom 20 mm)`, the parts added and gone, each value the scene cannot
  show (`shelf.middle: material birch 18 → oak 18`), the operations it
  could not place and the problems that came and went; a path in it
  selects the part and frames it with its ghost. A build that changed
  nothing says `no part changed` (`only lines of the build file` when
  lines moved); a design shown afresh and a reloaded page have no diff.
  From code, `preview.changes()` gives the last diff (null for none): the
  parts added, gone and changed as above, each outline as the segments
  that differ counted with the world point in their middle, the halos
  with their points (`{at, kind, path, op}`, for `look`), the glowing
  lines counted, what was not placed, the panel's text, and `ms`, what the
  diff and the drawing took; `preview.ghosts(on)` shows or hides the
  ghosts and glows. Cost, on the van (42 parts, 386 operations, a 5.3 MB
  layout; 2026-10-17): in node, the diff of a layout as before 0.9 ms, a
  hole moved 2 ms, the kitchen moved whole (23 parts) 3 ms; in the page,
  the shelf-pin holes of both kitchen sides moved by 2 mm 8.4 ms and
  0.6 ms to draw, the floor's longs spread anew (17 parts, nearly every
  point of the battens' outlines moved with their lap notches) 22 ms and
  6 ms, against 12 ms (node) to 29 ms (page) to parse the layout itself.
  Once, the first diff after the page loaded took 289 ms, with what the
  scene's loading left to collect; the same diff run again in the page
  took 13 to 20 ms.
- Click-to-path in the viewer is the Copy Path helper outside Fusion
  (faces, edges and anchors proposed in `design/proposals/preview-assist.md`).
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
- The CAM layer (`design/cam.md`; the checkbox CAM plan under Display, key
  `c`, which also shows the nest view): the chosen nest's plan, `cam.json`
  beside its `nest.svg`, drawn over the nest's drawing by the page
  (`lang/preview/viewer/cam.js`, with node tests; the drawing itself is the
  nest step's, unchanged). On each blank, a setup, the parts are shaded by
  their release order, the first cut free palest, and labelled with their
  place in it, their hold (cm², smallest first) and their tabs; a part's
  tooltip and the selection's info say the same; the tabs are black marks on
  the contours. The side panel's CAM plan section says whether the nest has
  a plan and when it was written, and lists per setup its parts in release
  order and its operations in the order they run, each in its tool's colour
  (the widest first, the V-bit last) with its features and tabs counted.
  Clicking an operation draws its features in that colour: pockets as filled
  regions, a rest (what a wider cutter left) dashed, contours as outlines,
  holes and dog bones as circles with a ring around them, a dog bone's wall,
  chamfers' edges and V-grooves as lines, the strokes in screen pixels so
  that a slot shows on a whole sheet; clicking it again draws none, a
  setup's name all of its operations, and the drawing scrolls to the blank.
  What each setup leaves out (but what is in a narrow face) and its
  problems, and the problems of the plan's own check, are listed under the
  drawing, after the nest's. A plan is stale when it was planned for
  another nest file than the one beside it (its `nest_written` and
  `layout_hash` are not the nest's: the nest was written again since) or is
  of another version (`CAM_VERSION`, repeated in `cam.js`; a test checks):
  the panel says so and nothing of it is drawn. Plan again runs `python -m
  lang.cam <build> <nest>` for the nest chosen (a second nest by its own
  name), with the build's CAM settings as they are now, one job at a time
  with the nests (`POST /plan?design=&nest=`; its output in `cam.log`
  beside the plan, shown when it failed), never on a save. From code:
  `await preview.cam(on)` (resolves with whether a plan is drawn),
  `preview.plan()` (the legend: per setup its operations, its parts in
  release order, and the notes; null without a current plan),
  `preview.operation(setup, index)` (a setup by its name, with or without
  the nest's, an operation by its index in it, `'all'` for every one, null
  for none; it throws for one the plan has not), `await
  preview.replan(nest?)` (resolves with the plan's state once it is
  drawn); `preview.nestStates()` gives each nest's `plan` (its state, when
  it and the nest it is of were written, why it is stale).

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
  --traceback` prints the whole stack. An error found when a board
  resolves, which may be at the layout where no line of the build file is
  on the stack (no placement, no material along its chain, a grain along
  its thickness), starts with the board's line
  (`error: examples/van.py:45: floor.batten3 reads material, ...`), and the
  stack below it leaves that line out.
- The editor: `POST /open?file=examples/van.py&line=45` runs the command
  `--editor` gives, VS Code's `code --goto {file}:{line}` by default
  (Florian's editor; `{file}` the file's whole path, `{line}` the line;
  split like a shell's words and run without a shell), for a file in the
  folder served or in the repo; a
  relative file is the repo's, where the builds run. It refuses other
  files, and a request whose `Origin` is not the preview's own page. The
  page's `o`, its line links and `preview.openEditor()` post it. The VS
  Code app does not put `code` on the PATH by itself, so without one there
  the server runs the one in the app bundle (`/Applications/Visual Studio
  Code.app/Contents/Resources/app/bin/code`); only with neither does the
  answer say the editor did not start, and name `--editor`, under the
  selection. Verified 2026-10-17: `o` on `kitchen.left` in the van opened
  `examples/drawer_cabinet.py` in VS Code at line 35, its `carcass(...)`
  call, through the bundle's `code`.
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
