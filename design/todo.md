# To do

A loose list of things that come to mind for the modeling language. An item
that grows a spec moves into a file of its own in `design/proposals/` (listed
in `DESIGN.md`); known defects are in `design/bugs.md`. Delete items when
done.

- **Snapshot arcs**: carry the master's arcs exactly instead of polylines
  sampled at 0.1 mm, which are up to 0.2 mm off along an axis where an arc
  runs steeply (seen at the sample's wheel-arch corners) and reach Fusion as
  many tiny faces, since the emitter only recovers arcs from exact vertices.
- **Profile exceptions in the master**: a contour looked up by position,
  `floor_profile.at(x)`, with exceptions such as
  `floor_profile.replace("Bodenprofil Heck", between=(plane("Stufe hinten"),
  floor_back))` for vehicles whose floor profile changes along the length.
- **The vehicle body as a mesh** in the snapshot: shown in the preview,
  sectioned as a limit, and checked against for gaps.
- **Cutouts limited to an area by references**: a cutout kept to part of a
  board, its bounds given by other faces, edges and boards (as `between()`
  places a board), not only by a region shape placed with `at=` (the add-in's
  Bounding Box Points). [Florian, 2026-10-13]
- **Cutout patterns left out**: rhombuses, tabs, patterns at an angle to the
  board's edges.
- **External components**: devices installed in the cabinets, such as
  electrical parts and appliances (not connectors, slides or other joinery
  hardware), to plan the room they need: imported from STEP or other CAD
  data, or given as outlines or boxes. Related: the joinery hardware is drawn
  as boxes and checked for overlaps, runs' `keepout`, hand-modeled bodies as
  inputs. [Florian, 2026-10-13]
- **Colors and appearances**: a color, or a Fusion appearance or physical
  material, given to a part or to a material for all its parts, carried by the
  layout to the preview and to Fusion. Now the preview colors parts by
  material from a fixed palette, in the order the materials come, and the
  compiled bodies get no appearance at all. [Florian, 2026-10-13]
- **Grain visible in Fusion**: compiled parts get an appearance whose texture
  runs along the grain (Multi Arrange already reads 3D wood textures'
  direction, see its model.py). Not needed for nesting, which reads the
  attribute. Also a grain stripe in the preview.
- **Manufacturing groups**: decided 2026-10-16 for grain matching, nested
  by the language's nest only; see `design/nesting.md`, Still open.
  [Florian, 2026-10-13]
- **Check results in the preview's scene**: interference pairs highlighted,
  sheet fit, parts flagged as not plain flat work.
- **Slats beyond cosmetic** (see `design/slats.md`): operations and joints
  on slats, all hand work, on the hand-work list (`proposals/cam.md`); the
  rule that every connector is machined from both boards' big faces holds
  for boards only, so a slat's side of a joint may lie in a narrow face or
  an end (a Domino in a rail's end). Joints contacts do not cover yet: frame
  corners in one plane (a rail's end on a stile's narrow face) and a slat
  lying flat on a board (face to face). Angled end cuts are bevels
  (`proposals/bevels.md`), and with them mitred lip corners, which Florian
  needs as well as butted ones. A hinge cup across a lipped door's edge
  needs operations on slats too. [Florian, 2026-10-14]
- **Cut list**: decided 2026-10-16, with bought hardware, written by the
  build as CSV; see `design/nesting.md`, Still open [Florian, 2026-10-14].
- **Banding along curves**: lips go on straight edges only; banding could
  follow a rounded corner or a round outline.
- **More hardware**: whatever else the van needs. The sliding brackets have
  no add-in yet; `lib/sliding_brackets.py` is ready for one.
- **Latched drawer box detail**: a cut-out in the drawer box for the latch
  versus keeping the box clear by `latch.reach` (deferred by Florian,
  2026-10-12).
- **Errors at the layout step name no line**: a board resolves lazily, so a
  missing placement or material, or an inherited grain along its
  thickness, is found when the layout resolves it and `lang.build` prints
  no line of the build file. A board could remember where `board()` made
  it and name that line.
- **The inventory between runs of the nest**: the nests of one run of
  `python -m lang.nesting` share the stock on hand in their order, but a
  nest run alone (the preview's "nest again", or naming one nest) sees the
  whole inventory again, so two nests not yet made may both plan on one
  offcut (found 2026-10-16, stage 2). Marking a nest as made takes the
  pieces it used out of the ledger (pinning, stage 3), so the conflict
  lasts only until the first of them is made; the second, marked later,
  notes that the piece is gone. A nest could be re-run when the ledger lost
  a piece it plans on, or reserve its pieces.
- **Unmarking a nest made**: a mark is undone by editing `made.json` and the
  inventory by hand (`design/nesting.md`, Pinning); a command for it when
  a wrong click calls for one.
- **A nest's values changed since it was made or nested** (another margin,
  another bed) do not count as a change: a nest compares its parts'
  fingerprints only. The preview could say when the values a nest would
  run with differ from those in its file.
- **`nest(False)` boards no nest names** are still only listed as not
  nested; the cut list (`design/nesting.md`, Still open) is where they go.
- **The CAM plan's choices to review** (`design/cam.md`, marked [chosen]):
  a narrower pocket template alone at ¾ of the widest, the 8 mm adaptive's
  room of twice its cutter, the tabs' neighbour classes and weights, a
  hidden edge by another part's box, `cam.waste_area` at 10 cm², the CAM
  settings read from the build as it is now. Keys of the settings table not
  built: `cam.tab_edges`, `cam.finishing_stepdown`, Auto Setup's rule
  constants and the holding calibration.
- **Corners named by a point** (`panel.top.front(60).left(40)`) for
  `fillet()` and `chamfer()`, once a build needs it.
- **Try the language on real modules**: write two modules from the van in
  the language, a bank and the rear storage (they resolved almost completely
  in the Planung check), to see what it lacks; and walk one existing module's
  timeline to bucket its features into the escape-hatch rungs.
- **Open the refactored add-ins' dialogs once in Fusion**:
  concealed_hinge_native, hatch_hinge, ball_catch, door_latch_native,
  connectors_native and tenons_native now read their dimensions and stations
  from `lib/`; they were compared headless only (2026-10-12).
- **Naming**: the package name; German or English path names (suggestion:
  English, with an optional label override for the machine); "module" and
  "layout" collide with Python's and nesting's terms (see `build-repo.md`).
