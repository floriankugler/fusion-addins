# Nesting in the language

Status: added by Florian 2026-10-14, worked out by Claude the same day;
nothing built. Only the points marked [Florian] are his. Comes before CAM
(`cam.md`).

Florian's points: nesting as part of the language, its output either the real
parts or a nested view; nesting per material; parts marked to be left out of
the nest; the stock pieces on hand given, and the cuts that waste least
found, within the size of the machine's bed; SVGnest as a solver to look at
[Florian].

Today Multi Arrange nests compiled parts in Fusion after a compile, with
Fusion's Arrange as a black-box solver (grain, groups, machining face up,
several sheets, reading the `lang`/`part` attribute, see
`design/emitter.md`), and `fits_sheet` checks each part against its
material's sheet size.

Proposed: nesting is a step after the layout, in plain Python, over the
layouts of all a build's modules.

- **Input**: the parts' machine outlines (see `bevels.md`), by material. The
  grain allows two turns (0 and 180 degrees), a material without grain any
  turn; no part is flipped, since its machining face goes up. Manufacturing
  groups (`design/todo.md`) are nested rigid. Left out: slats, which go on
  the cut list by length, and boards marked `.nest(False)` (strips ripped on
  the saw, say), a property modifier like `.manual()`, which go on the cut
  list by size; a rule may set it for a whole kind of part.
- **Stock**: a stock file per build or workshop, with full sheets per
  material (a count, or as many as needed), offcuts on hand (rectangles, or
  outlines kept from earlier nests) and the machine's bed (size, spacing
  between parts, margin). The bed is 2000 x 1000 and the sheets are
  2500 x 1250, so every full sheet is first sawn into blanks that fit the
  bed. The nest chooses the blanks together with the parts on them, to waste
  least [Florian]: straight cuts right through, as a panel or track saw makes
  them. `fits_sheet` then checks against the bed too. A part larger than the
  bed is sawn by hand (`.nest(False)`) or machined in two setups, moved
  between them [open].
- **Output**: a nest file committed next to the layouts: the stock piece
  each part comes from, its placement on it, and the leftovers worth keeping
  as offcuts. A changed nest then shows in a diff. The preview gets a nest
  view (sheets with their parts, grain, labels, the waste per sheet). The
  emitter writes either the module documents as now or a nested document per
  material, each sheet a stock body and each part flat on it with its
  machining face up, named by path. CAM goes there.
- **Cut sheets are pinned.** A van is built over weeks, so a sheet marked as
  cut keeps its nest; later nests take only the parts not cut yet and report
  parts that changed after they were cut [open].
- **Solver**, to be measured on the van's real parts (sheets used, time,
  whether the same input gives the same nest) [open]: SVGnest (MIT,
  JavaScript, true-shape nesting with no-fit polygons and a genetic
  algorithm; it runs in the browser or in node, as the viewer's tests do, but
  nests into one bin per run, so several sheets and offcuts need a loop or
  the multi-sheet code of its sibling Deepnest); jagua-rs (Rust, a
  collision-detection engine for irregular cutting and packing that supports
  bin packing; its optimiser sparrow targets strip packing); Fusion's Arrange
  through Multi Arrange stays as the fallback.
