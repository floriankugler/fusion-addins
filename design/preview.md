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
  appearance rendering. Those are Fusion's job, as are nesting and CAM.

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
  selected part's info gives its grain. Proposed and not built: the grain as
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
