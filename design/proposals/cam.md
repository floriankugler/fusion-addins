# CAM from the language

Status: added by Florian 2026-10-14, worked out by Claude the same day;
reviewed with Florian on 2026-10-15 (the gaps found, holding and tabs), his
decisions written in. Points marked [Florian] are his, [decided] his
decisions, [proposed] Claude's. Builds on the nest (`design/nesting.md`);
the values a plan reads are settings that flow down the build
(`proposals/settings.md`).

Built 2026-10-17 (stage 4 of `proposals/settings.md`'s build order): the
CAM plan, Fusion-free, `lang/cam`, described in `design/cam.md`: a
`cam.json` beside each nest file with a setup per blank, its operations in
order (template, tool, the parameters to set, the features by position),
one side only, Auto Setup's hole rules, the pocket's cutter by the opening
test with rests, slots as pockets, dog bones marked in the layout (version
9) and routed as Auto Setup routes them, the V-bit's chamfers and grooves,
skin and release with the release order, tabs only for what holds too
little, by the position rules below, own blanks, the CAM keys, the command
`python -m lang.cam`, and the check, fuzzed. Built otherwise or beyond what
is written here: the 8 mm adaptive template takes only pockets with room
for twice its cutter across [Florian, 2026-10-17: a pure pocket rougher];
a narrower template that reaches a whole pocket takes it alone where its
cutter is at least ¾ of the widest that gets in, else the widest takes it
and rests go to narrower ones; bores are kept apart by hole diameter (their
feed follows the hole); a blind hole's bottom is its own (`from hole
bottom`), its top the stock's; an inner contour whose cutter is narrower
than its part's outer contour's is taken out whole (its release would come
after the part's), and so are an own blank's openings; "the strongest
neighbour across the kerf" is three classes for now (still held by its
skin, released before, nothing), and a hidden edge is one another part's
box reaches across; `cam.waste_area` defaults to the tabs' 10 cm², measured
as they are. Still to come, kept below: the CAM emitter in the compiler
add-in, the plan in the preview, manufacturing groups, the holding model's
calibration and the lift margin, a slot cut along its line.

Florian's points: since the Fusion geometry is generated again on every
compile, the CAM setups have to be made again too; Auto Setup helps, but it
analyses the geometry to work back to the operations, while the language
knows them; construction, nesting and CAM setup should be one chain; no
G-code, but an output like the layout file that a Fusion add-in compiles into
a CAM setup [Florian]. Generating G-code stays a non-goal.

Today Auto Setup recognises holes, pockets, contours, rim chamfers, V-grooves
and dog bones on selected bodies, chooses templates and tools by rules (each
hole bored with the widest cutter 1 mm smaller, drilled only where no cutter
fits; blind holes over twice the cutter as pockets; through holes over 30 as
contours; checks of pocket corner radii and flute lengths; tabs by contour
length, away from concave corners; operations by widest tool, then by kind;
the V-bit last), and builds the setup from templates Florian exported. Where
Auto Setup runs on compiled documents has not been tried.

Proposed:

- A CAM plan written from the layout and the nest: a setup per blank (the
  nest saws sheets into blanks the bed takes, so a blank is one load on the
  machine; the blank as stock, the work coordinates at its corner) and
  operations in order, each with its template kind and label, its tool and
  the features it machines, named by part path and operation (contours,
  pockets with depths, holes, dog bones, chamfers, V-grooves), plus tab
  positions. No toolpaths.
- There is nothing to recognise: the layout already says what each
  operation is (a dog bone is a dog bone; a hole's diameter, depth, face and
  whether it goes through are exact) and what is hand work (bevels, mitres,
  lipping, slats), which stays out of the plan. Auto Setup's rules and tabs
  (`lib/auto_setup/`) are split into a Fusion-free layer that both use, as
  the joints were split into settings, layout and emitter. The tool data
  (diameters, flute lengths) are read from the templates outside Fusion: an
  `.f3dhsm-template` file is XML with its tool inside, and all 29 of
  Florian's parse [found 2026-10-15].
- A CAM emitter in the compiler add-in builds the setups in the nested
  document from the plan. It binds each operation to geometry the emitter
  made (bodies by path, edges and faces by position, as chamfers are found
  now). Fusion generates the toolpaths and posts them as before. Auto Setup
  stays for hand-modeled parts. The emitter lifts what
  `lib/auto_setup/builder.py` learnt the hard way: the tab sketch before
  the first operation and `checkValidity()` after it, every toolpath
  generated again at the end, `isSetupModelSelected` off on silhouettes, a
  tab position only on the operation whose profile it lies on (Fusion
  projects it onto the nearest contour of its operation otherwise).
- The preview can show the plan: which tool cuts what, the tabs, and how
  well each part holds.
- One side only, for now [decided 2026-10-15]: no flipped setups and
  nothing automatic for machining a part from both faces. Each blank is
  machined from its top, where the nest lays every part with its machining
  face (`machine` in the layout) up, so the side is fixed per part before
  the plan is made. Operations on a part's other big face are left out of
  the plan and reported. In the examples 14 of 137 boards have some: the
  drawer backs (hook holes outside, the floor's groove and the finger
  reliefs inside) and boards machined from their inner face with chamfers on
  the show face. Operations in narrow faces (25 boards, the box joints'
  grooves on drawer parts) are left out without a report; they are taken
  care of [decided 2026-10-15].
- The machining face is the one `machine()` names
  (`side.machine(side.inner)`, built 2026-10-15, see `design/api.md`), else
  the big face more pockets, holes and chamfers are made from, else the show
  face.
- The hand-work list per part (bevels and mitres, lipping and banding,
  roundovers, hardware to fit, slats' operations once they have any) is
  shelved [decided 2026-10-15: not needed for now]. The plan reports what it
  leaves out; the list may come later, from the same step.
- With tool data known, the checks can refuse features narrower than the
  smallest cutter (`design/checks.md`).
- Slots carry their centre line in the layout (`design/operations.md`), so
  a slot as wide as a cutter can be cut in one pass along it (Fusion's 2D
  Slot) instead of as a pocket; then the 0.1 mm a slot is now made wider
  than its cutter no longer applies. 58 of the examples' slots are Domino
  4 mm and no template has a 4 mm cutter, so this is for the 6 and 8 mm
  slots [found 2026-10-15].
- **Parts outside the nest.** A `nest(False)` board may still carry
  operations (the van's four long floor boards, nine each), and the plan
  has nothing for it until it lies on a blank. The way there is nesting a
  selection (`design/nesting.md`, Still open): a material on its own, or a
  part or group of parts, as when parts have to be made again; a
  `nest(False)` board the bed takes is nested alone and gets its blank and
  setup through the same path [decided 2026-10-15]: named in a nest, it is
  its own blank, sawn to size with no margin, and the plan machines its
  operations and no outline [proposed in the nesting review]. One larger
  than the bed is sawn by hand and its operations are hand work [decided
  2026-10-16, nesting review: two setups dropped for now].
- **Manufacturing groups** (`design/nesting.md`, decided 2026-10-16 for
  grain matching): a group's members lie in the nest as designed, with
  gaps the smallest cutter passes, so one contour pass cuts both edges of
  such a gap; the plan has to know a group's internal gaps as shared cuts,
  and the smallest cutter is a setting (`cam.smallest_cutter`) until the
  plan has the tool data [to do].
- **Where the preferences live** [decided 2026-10-16, superseding the
  `[cam]` table of the 15th]: they are settings set in the build, in
  Python, flowing down from the root module to modules, parts, nests and
  setups (`proposals/settings.md`): the templates per kind, dc or udc,
  finishing per kind, the tabs' policy, width, height and least count, the
  breakthrough depth, the finishing stepdown, the holding calibration. The
  machine's values are settings too, and the stock on hand is the inventory
  ledger (`proposals/settings.md`).
- **The plan file** [decided 2026-10-15: names from the nest, a timestamp]:
  `cam.json` beside the nest file, with a version, the hash of the nest it
  was planned from (as the nest records the layout's), so the compiler
  refuses a stale plan, and the time it was written. Setups and NC programs
  are named from the nest's blanks (`<nest> birch 15 1.2`), so the nest
  itself needs a name, from its sources and the time it was written, which
  it has not got yet (`design/nesting.md`, Still open).
- **Z zero is the stock top, always** [decided 2026-10-15]. Through cuts go
  the breakthrough deeper than the stock bottom (0.2 mm today, a
  setting). The layout's thickness is nominal and birch ply
  varies by half a millimetre, so each blank's thickness is a user
  parameter in the nested document, the stock built on it and through
  depths bound to the stock bottom, so one measured value corrects every
  operation [proposed].
- **Grouping** [proposed]: one Fusion operation per tool, kind and template
  across the blank's parts, as Auto Setup does per setup; tabbed contours
  apart from untabbed ones (see the emitter above).
- **Checked** [proposed, Florian: yes]. Fusion-free, as the nest's
  `verify`: every operation of every nested part is in the plan exactly
  once or reported with a reason; every cutter reaches its region (the
  opening test below); each part holds at its moment in the order (Holding,
  below); fuzzed over random boards and nests. In Fusion: every operation
  generates a toolpath that is not empty and none reports contours not
  machined, run as `fusion_batch` does for geometry.

## Holding

Florian's facts [Florian, 2026-10-15]: a vacuum bed with a bleed-through MDF
spoilboard; parts are held by the vacuum, with tabs where that is not
enough, never with clamps or tape [decided]; the dust extraction's suction
lifts a small part whose vacuum is too weak, and the cutter then grabs and
destroys it, so the hold must beat the extraction's pull as well as the
cutting force; what he is unhappy with today is where the tabs are put,
more than how many. Tested 2026-10-17 [Florian]: strips down to 300 by
20 mm and discs down to 60 mm across, milled down to a thin skin and then
cut free by one release pass of 0.4 mm, held, in a board that already had
a big cutout in it and on a spoilboard that had been in use for a while.
Skin and release is the strategy (below).

### The model as it is

`lib/auto_setup/holding.py`, behind Auto Setup's "Automatic (vacuum)" mode,
is Fusion-free, never calibrated, and committed as WIP. It already has
Florian's two objections to area as a measure: a part's hold is its
footprint eroded by a leak margin (12 mm by default), so a part of narrow
runs holds next to nothing whatever its area; and a tab bridges the kerf to
a neighbouring piece whose hold pools with the part's, the skeleton web
being a piece like any other, scored the same way, so a tab into a thin web
buys nothing. It has slide and twist margins (friction times pressure times
the eroded area against the cutting force; the integral of the distance
from the pressure centroid against the cutter at the farthest point).

Run on the examples' nest on 2026-10-15 (twelve build files, 26 blanks, 131
parts, the defaults: pressure 0.5 N/cm², friction 0.5, cutting force 20 N,
safety 1.5, leak margin 12 mm, 50 N a tab): 24 parts fail (the dog-bone
frame's rails, the floor battens, the small cutout panel), 23 of the 26
skeletons fail, 58 of the 91 tabs the planner placed go into the skeleton,
and 12 parts are given up as unholdable. Three faults:

- **It judges the sheet fully cut.** With 10 mm spacing and a 6 mm cutter
  the web is 4 mm and the frame 10 mm; eroded, both are nothing, so the
  only anchor the planner has is worthless and it gives up. But a part is
  pushed only while its own contour is cut, and at that moment every part
  cut after it is still part of the sheet. Cut first into an uncut blank
  with four tabs into it, all 24 failing parts come out at a margin of 3 to
  4 by the same model.
- **Pooled twist uses the skeleton's lever.** Joining a part to the
  skeleton gives the assembly the skeleton's 140 to 180 cm lever, so a tab
  can lower a part's margin: the frame's cross rail went from 0.18 to 0.08
  with two tabs.
- **The constants are guesses.** Force measurements in MDF and
  particleboard put a 6 mm cutter's mean lateral force at 15 to 25 N per
  axis with peaks two to three times that (sources below), so 20 N is the
  right order; the leak margin is the unknown, which the strips calibrate
  (half the narrowest width that holds alone).

### Decided 2026-10-17: skin and release

- **Every contour is roughed to a skin and cut free afterwards.** Inner
  and outer contours alike are milled down to 0.2 mm above the stock
  bottom, and release passes at the end of the setup cut them free
  [decided]. Two operations per cutter [proposed]: a roughing contour with
  0.2 mm of axial stock to leave, in Fusion's own order, and a release
  contour from 0.2 mm above the stock bottom through to the breakthrough,
  0.4 mm of cut,
  one pass, `preserveOrder` on. Not one operation with a finishing
  stepdown: with order by depth Fusion would do the roughing in the
  preserved order too, and travel would suffer.
- **How the two are configured** [proposed, from the 6 mm template's
  parameters]. Both come from the cutter's existing contour template
  (`contour_Kontur 6mm`, the `.dc` and `.udc` variants); the plan sets the
  parameters that differ, as Auto Setup sets a through hole's bottom today,
  so Florian's templates need no change. Roughing: `topHeight_mode` 'from
  stock top' as the template has it, `bottomHeight_mode` 'from stock
  bottom' with `bottomHeight_offset` 0.2 mm (the template says 'from
  contour', −0.2), `doMultipleDepths` as the template (6.4 mm steps),
  `tabsPerContour` 0, Fusion's own order. Release: `topHeight_mode` 'from
  stock bottom' with offset 0.2 mm, `bottomHeight_mode` 'from stock bottom'
  with offset −0.2 mm (the breakthrough setting), `doMultipleDepths` off,
  `preserveOrder` on with the chains handed over in the release order, no
  tabs, the same compensation. Stock bottom rather than the contour's
  edge, so the measured thickness entered per blank moves both heights and
  the skin stays 0.2 mm whatever the ply measures. A release template of
  its own (a tag like `.finish`, say `contour.release_Kontur 6mm`) only if
  the thin pass should run at another feed or with the downcut cutter; the
  template's finishing stepdown stays unused.
- **Inner contours without an island.** An inner contour whose waste the
  cutter mills away entirely, a region narrower than two cutter diameters
  (a slot, a narrow notch), leaves nothing to hold or to release: it is cut
  through in one operation like a pocket, with no release pass and no tabs
  (Auto Setup tabs such slots today, below). Waste that would survive but
  is smaller than worth keeping [threshold open] is pocketed away rather
  than released, so no loose piece flies [proposed].
- **The order of operations**: by tool, widest first, 8 mm, 6 mm, 1/8",
  2 mm and the V-bit, as Auto Setup orders them today, then the release
  passes at the very end: the 6 mm cutter's and, where a contour is cut
  with it, the 1/8" cutter's. One tool change more, which is much better
  than lots of tabs or destroyed parts [decided 2026-10-17]. The V-bit
  stays before the release: no V-cuts on parts that are already free
  [Florian].
- **The release order**: smallest hold first, by eroded area, ties by
  travel [Florian: the size ordering makes sense]; the inner contours of a
  part before its outer. The reason [proposed]: until the release passes
  the skin seals every kerf, so the sheet is one airtight plate and the
  vacuum under it is at its strongest; each released contour opens a slot
  through the sheet onto the bleed-through spoilboard, and the pump's
  capacity is finite, so the vacuum under everything still attached drops
  with every part set free. The parts that need it most go while the sheet
  is still sealed, the large ones last, when their area makes up for the
  loss. Against it stands only the time a released small part lies loose
  under the passing hood, which the experiments survived; the next
  experiment watches it.
- **Tabs: none by default, with a safety net for very small and very
  skinny parts** [Florian, 2026-10-17: there should still be one, to be
  sure]. One measurement covers both: a part's footprint eroded by
  `cam.tab_margin` (6 mm by default) keeps less than `cam.tab_area`
  (10 cm² by default), and the part gets tabs; a part narrower than twice
  the margin keeps nothing and always does. The defaults sit below what
  held: at 6 mm a 300 by 20 strip keeps 23 cm² and a 60 mm disc 18 cm²; a
  300 by 15 strip keeps 8.6 cm² and a 44 mm disc 8 cm², and those get
  tabs. The failing-size experiment tightens both numbers; `cam.tabs
  ("forced")` or `cam.tabs("none")` on a part overrides them [proposed]. A
  tabbed part keeps at least three tabs, by the rules below, and its tab
  positions go on both its roughing and its release operation: the
  roughing stops 0.2 mm above the stock bottom, a tab stands 2 mm tall, so
  a roughing without the tabs would mill them down to the skin [proposed].
  The same threshold decides which surviving waste is pocketed away (above).
  The holding model's job becomes the release order and, once calibrated,
  this exception, with its pressure falling with the kerf area opened
  before a part's release [proposed].
- **Calibration** [found 2026-10-17]: at a leak margin of 12 mm a 20 mm
  strip has no eroded area left, yet it held, so the margin is under 10 mm,
  or the force scaling carries the difference. Open: the failing size.
  The next experiment [proposed]: strips of 15 and 10 mm by 300, discs of
  45 and 30 mm, and the smallest of them released last on a sheet whose
  other parts are already free, the leak budget at its worst.

### Proposed

1. **A lift margin** [proposed]: pressure times the eroded area against the
   extraction's pull on the part's top face plus an upcut cutter's lift,
   next to slide and twist. Narrow parts suffer twice, since the pull acts
   on the whole top and the hold on the eroded bottom.
2. **Where tabs go**, for the parts that still need them, by rules Florian
   called good: into the strongest neighbour across the kerf, by its margin
   at that moment, not the nearest; at least three, spread about the
   centroid, since two are a hinge line; on straight stretches, a tab width
   from convex and three from concave corners as today; preferably on edges
   the layout knows are hidden, against another board, lipped, or in a
   groove or joint; never on a show edge, under a chamfer, or where a pocket
   thins the part. A tabbed part is judged by its own pivot with the tabs
   as a couple (`joint_margin`), not by the assembly's lever, which fixes
   the second fault. The same position rules go into Auto Setup's
   length-based mode (`lib/auto_setup/tabs.py`), which is what Florian uses
   today and is unhappy with.
3. **No wider web.** A wider web around weak parts was dropped in the
   nesting review [decided 2026-10-16, `design/nesting.md`]: 13 to 19 mm of
   web holds nothing either. Skin and release holds a small part by its own
   vacuum; what fails even with tabs is reported.
4. **Loose waste.** The waste inside a through cutout that survives the
   cut is a piece too; the examples have five of 3 to 36 cm², which the
   cutter can throw. Above the threshold it is released like a part, in the
   release order, tabs where it fails, since the plan has the same model for
   it; below it, pocketed away (above) [proposed].

### Prior art

Looked up 2026-10-15. Commercial CAM gives counts and spacing, not reasons:
Vectric places tabs evenly by count or distance and at most avoids corners
and curves ([docs](https://docs.vectric.com/docs/V12.5/VCarvePro/ENU/Help/form/Toolpath%20Tabs/index.html));
Fusion the same, by distance or count ([docs](https://help.autodesk.com/cloudhelp/ENU/Fusion-CAM/files/MFG-REF-2D-CONTOUR-TABS.htm)).
Cabinet nesting software decides by part size: Microvellum tabs or
onion-skins small parts with a count per part and a least distance from the
sheet edge ([docs](https://intercom.help/microvellum-knowledge-base/en/articles/14858821-overview-tutorials-nest-tabbing));
HOMAG's retaining bars join small parts to each other and its macros
pre-mill small parts first ([docs](https://docs.homag.cloud/en/news/article/stay-down-common-line-include-tabs-onion-skinning));
Thermwood puts one tab per part at its start point and lets a neighbour's
cut run through it, with a skin on parts under an area
([forum](https://www.thermwood.com/forums/viewtopic.php?t=8395));
Cabinet Vision onion-skins parts under 4 by 6 inches and cuts them first
([woodweb](https://woodweb.com/cgi-bin/forums/cnc.pl?read=803126)). An
Autodesk patent places tabs by simulated cutting forces, count, position
and size from the force at each spot, mating faces excluded
([US 11,307,559](https://patents.google.com/patent/US11307559B2/en)).
Bystronic's TiltPrevention is the one real physics model, for lasers:
weight, gas pressure and the grate's support decide the lead-outs and a
route that never passes over a cut part, micro-tabs only where still needed
([Bystronic](https://www.bystronic.com/can/en/news/tilt-prevention)); the
laser literature's sequencing rules (inner contours first, skeleton
stiffness, small parts first) are reviewed by [Dewil et al. 2016](https://lirias.kuleuven.be/server/api/core/bitstreams/e6d6dc01-3477-4f4a-9172-2c38cfcebdf4/content).
Shop rules: small parts first while the vacuum is whole, onion skin of 0.5
to 1.3 mm with the last pass at half feed, 13 to 19 mm of web around tiny
parts, climb to a thin layer then conventional, a bigger pump does not help
small parts ([woodweb](https://woodweb.com/knowledge_base/Tabbing_Versus_OnionSkinning_for_Small_Parts.html),
[Laguna](https://info.lagunatools.com/onion-skinning-for-small-parts-on-your-cnc)).
Forces: specific force 32 to 38 N/mm² in particleboard
([Pałubicki 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC8123317/)), mean
15 to 25 N per axis end-milling MDF ([Machines 2026](https://doi.org/10.3390/machines14040359)).
No paper models the pressure loss from a free edge through bleed MDF; a
[blog](https://blog.schallbert.de/en/vacuum-clamping/) reasons it out as a
leak network with about 5 mm of effective leak, and shops quote 500 cm² or
100 by 100 mm as the smallest part that holds alone.

## Where Auto Setup goes wrong

Florian's notes of 2026-10-15 on what Auto Setup does badly and the plan
must do better [Florian]; the causes and the ways out are Claude's
[proposed].

- **The cutter for a pocket by its narrowest passage.** Auto Setup checks a
  pocket template only against the pocket's concave corner arcs, its flute
  length and the floor's area, so a pocket narrower than the cutter between
  straight walls, or a narrow neck between two wider parts, gets a cutter
  that does not reach it. The plan has the pocket's region exactly: a
  cutter of radius r reaches the region opened by r (shrunk by r, grown
  again), so the widest cutter whose opening leaves nothing but the
  material a cutter always leaves in a corner is the one; where none of a
  template's cutters reaches everything, the rest goes to a narrower one
  (as the adaptive templates' 6 mm cleanup does) or is reported.
- **A chamfered hole is drilled from the stock's top.** Fusion measures a
  drill or bore from the hole's top, the top of its cylinder wall, which a
  chamfered rim puts below the face; the V-bit cuts the chamfer last, so
  while the hole is drilled that material is still there, and the drill
  comes down to its feed height inside it. In the plan a hole's heights and
  depth count from the face it is made from, the stock's top there, and its
  chamfer is a V-bit operation of its own afterwards.
- **A slot is not a dog bone.** Auto Setup takes every concave arc narrower
  than the contour or pocket cutter for a dog bone, so the round ends of a
  4 mm slot (a Domino 4) are milled with the dogbone template, and the
  6 mm pocket template passes for the slot, since its ends are left out of
  the fit check as reliefs. The plan does not guess: a slot carries its
  centre line and width (`slot` in the layout) and is cut with a cutter
  narrower than it, as a pocket or along its line. Dog bones should be
  marked as such in the layout too, with the tool `dogbones(tool=)` drew
  them for: today a `dogbones()` relief is a cut or pocket named
  `<operation>_dogbones` and a joint's reliefs are part of its cuts.
- **Tabs on a slot.** With tabs on inner contours, Auto Setup tabs a slot
  or a narrow cutout too, though the cutter mills its waste away entirely
  and nothing is left to hold; the tabs are ridges at the slot's bottom to
  clean off [Florian, 2026-10-17]. The plan tabs or releases an inner
  contour only when its waste survives the cut: the region inside it shrunk
  by the cutter's diameter is not empty (Holding, above).
