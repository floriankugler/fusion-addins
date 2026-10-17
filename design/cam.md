# The CAM plan

A nest's blanks planned for the machine: one setup per blank, its
operations in order, each made from one of Florian's CAM templates with
the parameters Fusion is to set on it and the features it machines, bound
by position. Plain Python after the nest, like it; no toolpaths, no
G-code. Part of the modeling language's design; the overview is
`DESIGN.md`. Code: `lang/cam/` (`keys`, `tooling`, `resolve`, `regions`,
`rules`, `holding`, `tabbing`, `plan`, `verify`, `plan_types`, the command
in `__main__`). Built 2026-10-17 as stage 4 of `proposals/settings.md`'s
build order, from `proposals/cam.md`, which keeps what is not built: the
manufacturing groups. The Fusion emitter that makes the setups from the
plan (stage 4b, the same day) is In Fusion below, and the preview shows
the plan on the nest's drawing (stage 4c, In the preview below). Points
marked [decided] are Florian's, [chosen] choices made in building it that
he has not seen.

## Running it

```
python -m lang.cam examples/drawer_cabinet.py                       # every nest nested
python -m lang.cam examples/drawer_cabinet.py drawercab.birch_15     # the nests named
python -m lang.cam examples/drawer_cabinet.py --from-nest            # without running the build
```

- It plans every nest that has a nest file under the build's out folder
  (`out/<build>`, as `python -m lang.nesting` writes them, second nests
  `kitchen.carcass-2` included), or those named, and writes each plan
  beside its nest: `out/<build>/<module>/<nest>/cam.json`.
- The geometry is the nest's: its file and the layout it nested
  (`nest.layout.json`), of this layout version (10) or refused, so the plan
  and the document Compile Layout draws from the nest agree. The CAM
  settings are the build's as it is now: the command runs the build, so a
  CAM setting changed since the nest holds without nesting again
  (`--from-nest` takes the layout nested instead) [chosen]. A part changed
  since the nest (its fingerprint) is planned as nested, and said so.
- It prints per setup its operations with their features and tabs, what it
  leaves out (but what is in a narrow face, which is taken care of
  [decided 2026-10-15]) and its problems, and the plan's own check
  (Checked) adds what it finds to the plan's problems (`check: ...`).

## The plan file

`cam.json`, millimetres, version 1 (`plan_types.py`, `CAM_VERSION`, which
the emitter will repeat and refuse others of):

- **The nest**: its name, when its file was written and its layout's hash
  (`nest`, `nest_written`, `layout_hash`), so the compiler refuses a plan
  whose nest is not the file beside it [decided 2026-10-15]; when the plan
  was written (`written`).
- **The settings** it ran with (`settings`): every CAM key's value for the
  nest (the nest's own, else the value its parts have most, else the
  default) and where it came from, the parts and named operations with
  values of their own, where they were read (`read_from`: the build or the
  layout nested), the templates' folder, and the smallest cutter.
- **A setup per blank**, in the nest's order, named `<nest> <material>
  <sheet>.<blank>` (`drawercab.birch_15 birch 15 2.1`) [decided]:
  - `stock`: the material, the sheet and the blank's names, the blank's
    rectangle on its sheet, its nominal thickness, whether it is an own
    blank;
  - `parts`: each part on it, its hold (cm², Holding), its `cam.tabs` and
    how many tabs it got;
  - `operations`, in the order they run, each: a name for Fusion ("6 mm:
    contours, roughing (Kontur 6mm)"), its kind (`drill`, `bore`, `pocket`,
    `contour`, `dogbone`, `chamfer`, `groove`, or `release`, made from the
    contour template), the template (the file's name without its
    extension) and its label, its tool (the template's widest: type,
    diameter, flute, taper, tip), the parameters to set (`params`: `top`
    and `bottom` heights as Fusion's mode and an offset up, `from stock
    top`, `from stock bottom`, `from hole bottom` or `from contour`;
    `multiple_depths` and a V-groove's `stepdowns`, None where the template
    decides; `preserve_order`; a bore's `feed_scale`, the hole in tool
    diameters, which Auto Setup's builder multiplies the template's feed
    by, capped; `tabs`: width, height and positions, or None), and its
    `features`;
  - `release_order`: the contours the release operations cut, in order,
    each its part, outer or inner, ring and cutter;
  - `left_out`: what of each part's operations is not planned, and why:
    `other face`, `narrow face`, `nothing fits` (no template's cutter, a
    note says which), `hand work` (an own blank's outline), `gone`
    (nothing of it is left on the board);
  - `problems`.
- **The frame**: a setup's is its blank's in the nest file, x along the
  blank's length (the sheet's grain), y across, from its corner, so a point
  is where the nest's `transform` puts it; Z zero is the stock's top
  [decided 2026-10-15]. Every feature lies at the stock's top (the parts
  are machining face up) and is given by position for the emitter to bind,
  as it finds a chamfer's edges now; depths are millimetres down from the
  stock's top, None through. Rings run counter-clockwise around what they
  enclose, holes clockwise, as the layout's; points are written as
  computed, unrounded [found by fuzzing: rounded, a ring where a circle
  meets an edge at a glancing angle recovered its arcs otherwise].
- **A feature** names the part and what of its layout operations it
  machines (`ops`: each operation's index in the part's `ops` in the
  nested layout, -1 for the outline, its name and kind, and the aspect:
  `op`, the operation's `chamfer`, its dog bone `relief <k>`, the
  outline's `ring <k>`, 0 the outer one), and its geometry by kind:
  - `outer`, `inner`: a contour, its ring, the part on its left;
  - `pocket`: a region (one piece of a pocket, a round pocket, an inner
    contour's waste taken out whole), its rings, its depth, a slot's line
    (`slot`: its round ends' centres and its width);
  - `rest`: where a pocket's cutter did not reach, for a narrower one: the
    region it is to clear, what was left with the narrower cutter's
    diameter and the clearance of room around it, within the pocket of the
    same operation, so a pocket bounded by it holds the cutter wherever it
    reaches what was left [found in Fusion, 2026-10-17: with a radius of
    room, a rest in a rounded corner held no cutter, and the 2D Pocket
    bounded by it had no passes];
  - `hole`: centre, diameter, depth;
  - `dogbone`: centre, diameter, the tool it was drawn for, depth, and its
    wall as points along the circle where it borders the material;
  - `chamfer`: its size and the edges it runs along at the stock's top,
    before the chamfer, the material on their left, open or closed (a
    hole's rim also by its centre and diameter);
  - `vgroove`: its line's start and end, its depth.

## What the plan takes

There is nothing to recognise: the layout says what each operation is.

- **One side** [decided 2026-10-15]: each blank is machined from its top,
  where the nest lays every part with its machining face up. An operation
  made from the part's other big face is left out and reported (14 of the
  examples' boards have some: the drawer backs, chamfers on show faces); an
  operation in a narrow face (the box joints' grooves) is left out, listed
  in the file and not printed. A through hole or pocket goes through from
  either face, so it is machined from the top whichever face made it.
- **Templates** (`tooling`): the `.f3dhsm-template` files in the folder
  `cam.templates` names (Auto Setup's by default), named
  `<kind>[.<tag>...]_<label>`, read as XML: each operation's tool
  (diameter, flute, taper, tip; inches converted) and parameters, whose
  plain expressions (`6.4mm`, `Math.min(tool_fluteLength * 0.75;
  tool_diameter)`) are evaluated. A label resolves for the cutter variant
  (`cam.cutter`: a template tagged `dc` or `udc`, else an untagged one) and
  the finishing pass (`.finish`), each fallback with a note, as Auto Setup
  resolves it. A template's widest tool is its cutter [decided]; its
  narrowest decides what it reaches, its shortest flute how deep it cuts.
- **Holes** [Florian's rules, `rules.py`]: bored with the widest bore
  cutter at least 1 mm smaller than the hole; in a blind hole the cutter
  must also reach the centre (hole at most twice the cutter: no core left
  standing); where none has the millimetre but one fits at all, it bores 4
  mm deep only, with a note; a hole no bore cutter fits is drilled with a
  drill template of exactly its diameter, at most 4 mm deep, with a note;
  else nothing fits. A through hole over 30 mm is an opening of the
  outline, a blind one over twice the widest bore cutter a round pocket. A
  hole with nothing of the board where it is (in what a through pocket
  takes off the board's edge; the board as a blind pocket's region sees it,
  below) is gone [found by fuzzing, 2026-10-17: bored off the blank].
  Heights from the stock's top, a chamfered hole's too (its chamfer is the
  V-bit's afterwards), the bottom the hole's own (`from hole bottom`), a
  through one's the stock's bottom less the breakthrough, a tight one's 4
  mm below the top. Bores are kept apart by hole diameter, as Auto Setup
  keeps them, since their feed follows the hole [chosen: one operation per
  tool, kind and template otherwise].
- **The opening test** (`regions.unreached`) [`proposals/cam.md`]: a
  cutter of radius r reaches the region opened by r (shrunk by r, grown
  again), so what it leaves is the region less its opening. It must leave
  0.1 mm (Auto Setup's clearance) in the narrowest passage, so the test
  opens by r plus half of that: a slot the language made 0.1 wider than
  its cutter takes that cutter. Of what is left, slivers narrower than 0.01
  mm are noise; the fillet a round cutter leaves in a sharp inside corner
  (a corner between two curves that meet at an angle, as `arcs.fit` reads
  the ring, lines or arcs) is what any cutter leaves, within the tangent
  points of its circle there; then the dog bones, which go by their own
  rule. What else is left (a passage too narrow, a rounded corner tighter
  than the cutter, an area) is unreached, and only that is a rest for a
  narrower cutter, never a corner's sliver [review, 2026-10-17: the
  Cabineos' access holes over the board's edge, a line meeting an arc,
  sent the 2 mm cutter for 176 such slivers in the examples].
  A fillet is told so: between two lines, the piece lies within r/tan(θ/2)
  of the corner of angle θ; else where the cutter comes nearest the corner
  it touches the boundary on each side (an arc puts the contact farther
  out than a line does), and the piece lies within the contact farther
  from the corner, if the boundary from one contact through the corner to
  the other turns only toward the region and in all less than half a turn.
  So a corner cut off and two sharp corners close by are one corner; the
  boundary may turn away along an arc that meets the corner bulging into
  the region and through a dog bone, which its own cutter mills; walls
  that run apart no more than parallel are a passage. Beyond that zone,
  what is narrower than 0.05 mm is the buffers' noise along a wall. The
  region is normalized first, as the buffers and `arcs.fit` answered
  otherwise for a ring written from another start; vertices closer than
  1e-9 mm are one, as `arcs.fit` read a corner into a line between them;
  where the boundary turns back (two dog bones that touch), a point between
  its neighbours tells a needle of the region from a cusp outside it; and
  the shrunk region drops the pieces GEOS leaves nearer the boundary than r
  [all found 2026-10-17, by fuzzing and by probing dog bones].
- **Pockets** (`rules.pocket_cutters`): the configured template
  (`cam.pocket_template`, "Tasche adaptiv 8mm") or a narrower one: the
  widest that gets into the region (its cutter fits at all) takes it; where
  its cutters (an adaptive template's 6 mm clean-up too) leave more than
  the corners' fillets, what is left goes to the next narrower template that
  reaches it, as a rest (what was left grown by that cutter's diameter and
  the clearance, within the pocket: a cutter reaching a point of it lies
  within its diameter of the point, so it reaches in the rest all it does
  in the pocket), else it is reported. A narrower template that
  reaches all of the pocket takes it alone where its cutter is at least ¾ of
  the widest's (the 6 mm cuts a groove the 8 mm would leave rests in) [chosen].
  The 8 mm adaptive template is a pure rougher for larger pockets [Florian,
  2026-10-17]: an adaptive template only for a region of 25 cm² or more
  with room for twice its cutter across (the region shrunk by its cutter's
  diameter is not empty), never a slot, a groove or another narrow pocket.
  A flute must reach the floor (through: the stock's bottom and the
  breakthrough). A pocket's region is its shape on the part's outline
  within its outer loop, openings under it included, as they are material
  yet when the blind pockets run (a counterbore over a through slot is one
  pocket), but an opening another part lies in (one at the board's edge,
  where the nest may put a part). Blind pockets of one depth that overlap
  or touch are one region, as their floor is one face (a Cabineo's three
  access holes). A pocket in several pieces is planned piece by piece; a
  piece nothing gets into is left out as `piece <k>`. A slot is a pocket
  like any other, so it takes a cutter narrower than its width and its
  round ends are no dog bones [decided]. Heights: from the stock's top to
  the pocket's floor (`from contour`), or through.
- **The outline's contours**: the rings of the part's outline less its
  through pockets and its through holes over 30 mm (the outer ring first),
  each with the operations whose material it takes (cuts, through pockets,
  wide holes) and their dog bones. A contour takes the configured template
  (`cam.contour_template`, "Kontur 6mm") or the widest narrower one whose
  cutter reaches all of it on its waste side, with no clearance (a contour
  follows a fillet of its own radius, which a box joint keeps), and whose
  flute cuts through (else the configured one, with a note).
- **Skin and release** [decided 2026-10-17]: an inner contour whose waste
  the contour's cutter mills away (the waste shrunk by the cutter's
  diameter is empty), whose surviving waste holds less than `cam.waste_area`
  (its footprint shrunk by `cam.tab_margin`), whose cutter is narrower than
  its part's outer contour's (its release would come after the part's), or
  which is an own blank's, is taken out whole as a pocket through, with no
  release and no tabs. Every other contour, inner and outer alike, is
  roughed to the skin (top from the stock's top, bottom `cam.skin` above
  the stock's bottom, the template's stepdowns, Fusion's order) and cut free
  by a release pass at the end of the setup (top the skin, bottom the
  breakthrough below the stock's bottom, one depth, `preserveOrder`), both
  from the contour's template, the same tabs on both.
- **The release order** (`holding`) [decided 2026-10-17]: smallest hold
  first, the hold being the part's footprint (its outline less every
  through pocket and hole) shrunk by `cam.tab_margin`, in cm², measured in
  the part's own frame and normalized, so it is the same wherever the nest
  lays it [found by fuzzing: shrunk on the blank, a narrow neck pinched off
  or not as the part lay]; parts that hold alike (within 0.01 cm²) in the
  order that travels least, from the blank's corner; a part's inner
  contours, nearest first, before its outer one. The release passes run
  the widest cutter's first, each in the release order, a tabbed run in an
  operation of its own.
- **Tabs** (`holding`, `tabbing`) [decided 2026-10-17]: none but for a part
  whose hold is under `cam.tab_area` or nothing (narrower than twice the
  margin), or that says `cam.tabs("forced")`; `cam.tabs("none")` gives it
  none; an own blank none. Where they go, by the rules Florian called good:
  - the sites are Auto Setup's (`lib/auto_setup/tabs.py`, lifted onto the
    contour as lines and arcs): straight stretches and wide arcs, a tab
    width from a convex corner and three from a concave one, none on an arc
    under 40 mm radius while the contour has anything else, every 25 mm,
    on the ring's polygon;
  - none under a chamfer (along the outline, an edge of it, a chamfered
    cut), none within 10 mm of a pocket that comes within 1 mm of the
    contour (Auto Setup's full-thickness test), none whose neighbour across
    the kerf is nothing (the blank's edge, a contour cut through before);
  - a site on an edge the layout knows is hidden (another part's box
    reaches across the narrow face over the part's thickness: a board
    against it, a lip, the groove it sits in) weighs 1, a plain one 0.6,
    and one whose neighbour is a part released before (loose) 0.3 times
    that; the neighbour still held by its skin is the strongest [chosen:
    the classes stand for "the strongest neighbour by its margin at that
    moment" until the holding model is calibrated];
  - spread about the part: the first where weight times the distance from
    the centroid is largest, each next where weight times the distance to
    the tabs placed is, at least two tab widths apart;
  - as many as Auto Setup's density gives for the contour's length, at
    least `cam.tab_min_count`; fewer sites than that is a problem in the
    setup; width and height `cam.tab_width` and `cam.tab_height`, else the
    template's (5 by 2).
- **Dog bones**: the layout marks them (`design/operations.md`). One its
  operation's cutter cuts (at most 0.05 mm narrower than it, Auto Setup's
  rule) goes with that operation's feature; another is plunged with a drill
  template of its diameter, else milled along its wall with the widest dog
  bone template 0.05 mm narrower than it, else nothing fits; through, or as
  deep as its pocket, one operation per cutter and depth. A pocket that is
  all dog bones (a box joint's reliefs, a `dogbones()` pocket) has its
  dog bones only.
- **The V-bit** (Auto Setup's `_plan_bevels`): the 90 degree bit that
  reaches deepest, or the labelled one (`cam.chamfer_template`,
  `cam.groove_template`). All chamfers in one 2D Chamfer, the bottom from
  the contour per chain; a chamfer needs its size and the template's tip
  offset of flank (else a note), a hole's rim room for the tip (else it is
  left out). V-grooves in Traces of as many passes as the template's
  stepdown takes for them, one operation per number of passes.
- **The order** [decided 2026-10-17]: by tool, widest first (8 mm, 6 mm,
  1/8", 2 mm), within a tool drills, bores, pockets, contour roughing, dog
  bones, tabbed roughing before untabbed; then the V-bit's, the chamfers
  first; then the release passes. One operation per tool, kind, template
  and parameters across the blank's parts.
- **Own blanks** (a `nest(False)` board a nest names) [decided]: its
  operations, no outline (its cuts and outer ring are hand work, listed),
  no release, no tabs; an opening that is a through pocket or a wide hole
  is taken out whole.

## Keys

`lang/cam/keys.py`, `cam.*`, exported from `lang` (`from lang import
cam`). Nothing reads them during the build, so they are never frozen; the
layout carries them and the plan reads them (`resolve`). A key the plan
needs one value of for a nest (agree) is the nest's own, else its parts',
which must agree (else the plan is refused, naming two parts and where each
value came from), else the default; any other key per part and operation:
the operation's own, the nest's, the part's along its chain, the default
(the proposal's precedence).

| Key | Default | Join | What |
|---|---|---|---|
| `cam.templates` | `addins-src/auto_setup/templates` | agree | the templates' folder, relative to the repository |
| `cam.cutter` | `"dc"` | part | the cutter variant, `dc` or `udc` (Auto Setup's dialog default) |
| `cam.contour_template` | `"Kontur 6mm"` | part | the contour template's label |
| `cam.pocket_template` | `"Tasche adaptiv 8mm"` | part | the pocket template's label |
| `cam.bore_template`, `cam.drill_template`, `cam.dogbone_template` | None | part | the labels a hole or dog bone may take; None every template of the kind |
| `cam.chamfer_template`, `cam.groove_template` | None | part | the V-bit's label; None the 90 degree bit that reaches deepest |
| `cam.finish_outer`, `cam.finish_inner`, `cam.finish_pockets` | False | part | the `.finish` templates (Auto Setup's checkboxes) |
| `cam.breakthrough` | 0.2 | agree | through cuts past the stock's bottom (mm) |
| `cam.skin` | 0.2 | agree | the roughing's skin above the stock's bottom (mm) |
| `cam.tabs` | `"auto"` | part | `auto`, `forced` or `none` |
| `cam.tab_margin` | 6 | part | the rim that holds nothing (mm) |
| `cam.tab_area` | 10 | part | a hold under it gets tabs (cm²) |
| `cam.tab_min_count` | 3 | part | the fewest tabs |
| `cam.tab_width`, `cam.tab_height` | None | part | the tabs' size (mm); None the template's |
| `cam.waste_area` | 10 | part | surviving waste holding less is taken out whole (cm²) [chosen: the tabs' measure and value, so waste that would need tabs as a part does not fly] |
| `cam.smallest_cutter` | None | agree | the smallest cutter groups and checks may count on (mm); None the templates' narrowest |

## Checked

`verify.py` checks every plan the command writes, Fusion-free, and the
tests and fuzz tests require it to find nothing:

- the setups are the nest's blanks, one each, with the blank's parts;
- every operation of every part on a blank is in the plan or left out with
  a reason, not both: each hole, V-groove and chamfer, an operation's
  chamfer and each of its dog bones exactly once, a pocket or a cut (whose
  material the outline's contours take) at least once, every ring of the
  outline exactly once (a release cuts again what a roughing cut, a rest
  what a pocket's cutter left);
- every cutter reaches its region: what a pocket's cutter leaves, one of
  its rests' narrower cutters reaches, kept inside that rest as Fusion's
  pocket bounded by it is (where rests overlap, the one that takes it), or
  a problem says; a contour
  on its waste side; a dog bone's cutter is narrower than it. The check is
  lenient by a hundredth (a cutter 0.01 mm narrower, a fillet's zone that
  much wider, slivers under 0.05 mm noise), so a decision on the edge for
  the plan is no fault [found by fuzzing: two mirror-image corners of one
  pocket, one fillet passed and the other did not as the noise fell];
- every contour roughed is released and every one released roughed; the
  release operations cut the release order; within a cutter's release the
  parts go by their hold; a part's inner contours come before its outer;
- a tabbed part's tabs are on its roughing and its release operation, each
  on its outer contour, and an operation's tabs on its contours;
- the operations are in order; an own blank has no outer contour and no
  release; every feature but a V-groove lies on its blank.

Fuzzed (`tests/fuzz/machining.py`, check `plans`): random parts as the
nest's fuzz test draws them (any side of a module, any of the 48 world
frames, `boards.py`'s holes, pockets, slots, cuts, notches, V-grooves, holes
into narrow faces, rounded corners, an opening, a grain, `machine()`,
`nest(False)` ones named as their own blanks), some with dog bones and a
chamfer along their machining face's outline and `cam.tabs` of their own,
with a random cutter, finishing, tab margin and waste area, nested and
planned: the check finds nothing, and, worked out apart from the plan, an
operation of the other big face is left out as such and one in a narrow
face as that, each part's outer contour is its outline less its openings
where the nest's transform puts it, each hole where the transform puts it,
a part has tabs exactly when its hold says so (unless the plan found no
room for them), and the plan survives JSON. 4000 random nests surveyed
clean on 2026-10-17 after the fixes the survey led to (each a regression
test in `tests/test_cam.py` or a fixed case in
`tests/fuzz/test_fuzz_machining.py`), and again after the fillets between
arcs. Every example that nests is planned
with the check clean.

## On the examples

Planned 2026-10-17 (`python -m lang.nesting` then `python -m lang.cam` on
each): the 8 mm adaptive rougher takes the cutouts example's large pocketed
openings and the dog bones example's 100 by 100 recess only; the drawer
grooves and dados go to the 6 mm, the 58 Domino 4 slots (3.8 wide) to the
1/8"; the 5 mm screw holes are bored with the 1/8", the 2 mm pilots
drilled, the 72 deeper than 4 mm only 4 mm deep with a note (Florian's
rule); the box joints' relief pockets go to the 1/8" dog bone cutter; the
drawer backs' other-face operations are left out; two of the van's floor
battens (430 by 14, a hold of 7 cm²) get 8 tabs each on both their
operations; an 18 mm shelf's through holes are deeper than the 2 mm
cutter's flute (a note). A counterbore over a through slot is one pocket:
blind pockets are clipped by the outline, not by the openings, which are
material yet when they are cut. Each Cabineo's three access holes are one
pocket on the 6 mm, and no example has a rest.

## In Fusion

Compile Layout builds the setups (stage 4b, built 2026-10-17;
`lang/emit/cam_plan.py` Fusion-free and unit tested, `lang/emit/cam.py`
in Fusion, `addins-src/compiler`): pick a `cam.json` and it draws the nest
beside it as a `nest.json` is drawn (`design/emitter.md`, Nested
documents), a document per material, then builds that material's setups
in it. A `nest.json` picked is drawn without setups [chosen: the plan is
what is picked to get them, so a nest is never planned behind the
user's back].

- **Refused**: a plan of another version (`CAM_VERSION`, repeated in
  `cam_plan.py`), of another nest than the `nest.json` beside it (its
  name, `nest_written`, `layout_hash`), one placing a blank where the nest
  has another or none, or machining a part that is not on the blank: plan
  the nest again.
- **The frame** (`cam_plan.plan_cam`): a setup's point is its blank's
  corner in the document plus the point, the sheets one above the other
  as `nested.sheet_places` lays them; a feature's height is the stock's
  top (the nominal thickness) less its depth.
- **The sketches first**: every setup's, before the first operation of
  the document, as they change the design and an operation made before a
  change keeps the model it was made against: per setup a hidden sketch
  `<setup> tabs` holding each tab position once (the roughing and the
  release share them; Fusion takes a tab position only as a model entity)
  and one `<setup> rests` with the rest regions drawn as lines and arcs
  (`arcs.fit`) at their pocket's floor; then `cam.checkValidity()`. They
  are never deleted.
- **The setup**: named as the plan names it; its models the parts' bodies
  on the blank; its stock a fixed box of the blank's rectangle and nominal
  thickness, placed from the model's origin (`job_groundStockModelOrigin`,
  x and y `'model'` at the blank's corner), its bottom offset the parts'
  top less its height (`<top> mm - job_stockFixedZ`), so its top stays at
  the parts' top; the WCS the stock's top corner at the blank's corner
  (box point `top 1`), in the model's orientation, so x runs along the
  blank's length. [chosen: a fixed box rather than the see-through stock
  body as a solid stock: the box's height is a value to edit, the body is
  not in a direct document; the body stays for the eye.] The emitter reads
  the stock back and reports it where it is not the blank.
- **What the operator edits**: the blank's measured thickness, as the
  setup's Stock > Height (Z). The box grows down from the top; every
  height from the stock's bottom (the roughing's skin, the release, the
  through holes and pockets) follows it, what the model gives (a pocket's
  floor, a hole's bottom, a chamfer's edge) keeps its depth from the top,
  and Z zero stays the stock's top. [Direct documents have no user
  parameters, so this is the one value instead of the proposal's user
  parameter.]
- **Each operation** from its template file (the folder the plan read,
  else the one `cam.templates` names in the repository the add-in lies in,
  for a plan made in another checkout) with `createFromCAMTemplate2`, in
  the plan's order, named as the plan names it (a template of several
  operations makes several, `<name> – <the template's operation>`), and
  written as `cam_plan.param_writes` says: the heights as the plan's mode
  (Fusion's values are the plan's names: `'from stock top'`, `'from stock
  bottom'`, `'from hole bottom'`, `'from contour'`) and offset in mm, each
  mode before its offset, none on a Trace (its tip follows the groove's
  bottom; it has no heights); `doMultipleDepths` and a Trace's
  `numberOfStepdowns` only where the plan has them, the stepdowns only
  with several depths; `preserveOrder`; on drills and bores
  `selectSameDiameter` off (Fusion pulls in every hole of the diameter
  otherwise); a Trace's `doChamfer` off; a 2D Chamfer's `chamferWidth` and
  `chamferClearance` 0; a bore's cutting feed the template's times the
  plan's scale, never past 3000 mm/min (Auto Setup's cap) nor below the
  template's; tabs (`group_tabs`, the plan's width and height,
  `tabPositioning` `'tabCount'`, `tabsPerContour` 0, `tabPositions` the
  sketch's points of the operation's positions) where the plan gives them,
  `group_tabs` off elsewhere. A parameter an operation lacks or refuses is
  reported, but the tabs' group, the order and the hole selection where
  the strategy has none.
- **The geometry, by position** (`cam_plan`'s bindings, matched within
  0.02 mm, an arc's middle within its chord's sagitta):

  | Feature | Bound by |
  |---|---|
  | outer contour | the part body's silhouette, outside loop, `isSetupModelSelected` off |
  | inner contour | the loop of the body's edges at the stock's top (else its underside) whose edges all lie on the ring and add up to its length |
  | pocket | its floor: the body's upward faces at its depth holding a point of its region (a floor shared by pockets that overlap, the Cabineo's three holes, is bound once) |
  | pocket through | a loop of edges per ring, as an inner contour |
  | rest | its region in the `rests` sketch, a chain per ring |
  | hole, dog bone drilled | the body's cylinders about its centre of its diameter (`holeFaces`, `circularFaces`) |
  | dog bone milled | its wall's arc edges at its floor (else the top), an open chain |
  | chamfer | the chamfer's lower edges, its edge before the chamfer moved down by its size, a chain per run, open where it is |
  | V-groove | its bottom's straight edges at its depth, an open chain per run |

  The tool's side: through the API Fusion puts the tool on the left of a
  chain's first edge as it runs, whatever the faces beside it say, so
  every chain is turned (`isReverted`) for the tool to run on its waste:
  inside an opening or a pocket's ring, outside a through pocket's island,
  inside a dog bone's circle, on a chamfer's open side [found 2026-10-17:
  left as they came, the drawer cabinet's 108 dog bones and 4 of the
  cutouts example's 24 inner contours were cut on the part's side, their
  toolpaths as long as their circles and rings offset outwards; a pocket's
  ring the wrong way round cleared all the stock around it]. A silhouette
  takes its side from its loop.
- **The toolpaths** are generated per setup at the end
  (`cam.generateToolpath`), as Fusion may generate an operation the moment
  it is made, against the bare template. An operation that fails is
  reported and the next one goes on; the summary lists per setup each
  operation with how many of its features were bound, and every problem.
  `cam.toolpath_report` checks the generated toolpaths (AGENTS.md,
  Testing the CAM Emitter Through MCP).

Verified in Fusion 2026-10-17 (build 2705.1.30, through the MCP server,
the add-in's `compile_file` loaded from the worktree) on the drawer
cabinet nested and planned with the plan's fixes of that day: every
operation has a toolpath, valid, not empty, with no warning (no "contours
were not machined"), none failed to bind:

| Setup | Operations (features) | Built in |
|---|---|---|
| birch 15 1.1 | 6 mm roughing (3), 1/8" bores ⌀5 (19), 1/8" pockets (2), 2 mm drills (12), 6 mm release (3) | 3.8 s |
| birch 15 2.1 | 6 mm pockets (12), 6 mm roughing (4), 1/8" bores ⌀5 (19), 1/8" pockets (6), 2 mm drills (12), 6 mm release (4) | 6.2 s |
| birch 12 1.1 | 6 mm pockets (9), 6 mm roughing (12), 1/8" dog bones 3 deep (108), 2 mm drills 4 deep (18), 6 mm release (12) | 18.9 s (3.5 s in a fresh session) |
| birch 9 1.1 | 6 mm roughing (4), V-grooves (8), 6 mm release (4) | 0.3 s |

The nest's document took 2.3, 8.2 and 0.1 s more, the toolpaths 16, 14
and 3 s to generate (Fusion's session slowdown after many documents,
`design/bugs.md`, makes the first numbers vary sixfold). The stock's
height set from 15 to 15.6 mm on birch 15 2.1 put the stock's bottom at
-0.6 with its top and the WCS where they were, and left the pockets',
bores' and drills' toolpaths as they were while the roughing went deeper;
on the van's floor battens the release's top and bottom followed the
height (-15.3 and -15.7 at 15.5 mm). Also built clean: the cutouts example
(inner contours, each of its 24 a release 37.7 mm longer turned the other
way round, chamfers, V-grooves, the 8 mm adaptive), the dog bones
panels (through pockets, milled dog bones), the operations example
(chamfers along edges, rims and the outline, through pockets) and the
van's floor (16 tab positions on both operations of two battens: the
release's cut 64 mm longer with them, a tab's ramps). Screenshots on that
Mac, under the worktree's `out/fusion-cam/`, not kept in the repository.

Not exercised in Fusion yet: rests (no example's plan has one now; an
earlier plan's, with a cutter's radius of room, gave an empty 2D Pocket,
and a rest now has the narrower cutter's diameter, The plan file), a dog
bone plunged with a drill, an own blank, a template with a finishing
pass.

## In the preview

The nest view's CAM layer (`design/preview.md`; key `c`) draws the chosen
nest's plan over its drawing, a setup on its blank: the parts shaded and
numbered by their release order with their holds and tabs, the tabs as
marks, and the operation chosen from the setup's legend (its operations in
order, each in its tool's colour) as its features: pockets filled, rests
dashed, contours outlined, holes and dog bones as circles, chamfers and
V-grooves as lines. What a setup leaves out and the problems are listed
under the drawing. A plan planned for another nest file than the one beside
it (by `nest_written` and `layout_hash`) is stale and not drawn, and Plan
again runs the command for that nest from the page. Fuzzed
(`tests/fuzz/plan_views.py`, check `plan_views`): `machining.py`'s random
plans, drawn as the nest step draws them and read by the view's own code,
land where the setup's frame puts them on the blank, every feature drawn
as its kind says, each part's outer contour on the part drawn but for what
the plan bores or pockets [found by fuzzing: a through hole across the
part's edge is a notch in the drawing's outline and a hole beside a
straight contour in the plan, both right].

## Still open

- Posting each setup's NC program (with the post Florian uses, `masso.cps`)
  beside the plan, with a record of what was posted, for a Fusion-free
  check of the material the programs remove against the plan and the
  layout (`proposals/gcode.md` on the branch
  `claude/fusion-cam-dependency-2e0017`, step 1): after the toolpaths are
  generated, once Fusion's future says they are done; not built in stage
  4b, whose brief left posting out.
- A rest in Fusion (In Fusion, above); manufacturing groups and their
  shared gaps (`cam.smallest_cutter` is there for them), the holding model
  calibrated (the release order and the tabs' neighbour weights would
  follow it), a slot as wide as its cutter cut along its line (Fusion's 2D
  Slot).
- Keys of the proposal's table not built: `cam.tab_edges`,
  `cam.finishing_stepdown`, Auto Setup's rule constants as keys
  (`bore_clearance`, `tight_cut_depth`, ...), the holding calibration.
