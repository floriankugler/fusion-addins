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
- **Manufacturing groups**: parts marked in the build as one group, which
  Multi Arrange then nests as a rigid group, keeping their arrangement, as its
  own groups do now (a group name per part, set by hand in its dialog). The
  compiler would write the group into the `lang`/`part` attribute next to the
  grain. If nesting moves into the language, its nester takes the groups too.
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
- **Cut list**: slats and lips by material, section and length (the
  material along the grain), boards by size; with the committed outputs
  (`proposals/build-repo.md`), later [Florian, 2026-10-14]. Perhaps a check
  of slat lengths against the stock's.
- **Banding along curves**: lips go on straight edges only; banding could
  follow a rounded corner or a round outline.
- **More hardware**: whatever else the van needs. The sliding brackets have
  no add-in yet; `lib/sliding_brackets.py` is ready for one.
- **Latched drawer box detail**: a cut-out in the drawer box for the latch
  versus keeping the box clear by `latch.reach` (deferred by Florian,
  2026-10-12).
- **`default_grain`** in `lang/core/scope.py` is set by nothing (placement.md
  promises a scope-level grain default): drop it, or give `module()` and
  `cabinet()` a `grain=`. The loose end of the syntax review's item 16
  (`proposals/syntax.md`, 2026-10-15).
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
