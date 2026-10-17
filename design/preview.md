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
- Camera and visibility from code: the page exposes `window.preview`
  (`look`, `view`, `camera`, `fit`, `isolate`, `show`, `hide`, `select`,
  `section`, `labels`, `hardware`, `parts`, `ops`, `loaded`, `open`,
  `designs`, `design`, `version`), so a tool driving the browser frames a
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
- A build goes to a scratch directory and moves in when it went through, so
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
