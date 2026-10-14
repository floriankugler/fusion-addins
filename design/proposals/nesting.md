# Nesting in the language

Status: added by Florian 2026-10-14, worked out by Claude the same day, and
tried the same day in `experiments/nesting/` (two solvers on the examples'
parts, see "Findings" below; its README has every number and how to run
it again). Nothing is built in the language. Points marked [Florian] are
his ideas, [decided] his decisions, [proposed] Claude's, [open] undecided.
Comes before CAM (`cam.md`).

## Florian's points

- Nesting as part of the language, its output either the real parts or a
  nested view; nesting per material; parts marked to be left out of the
  nest; the stock pieces on hand given, and the cuts that waste least found,
  within the size of the machine's bed; SVGnest as a solver to look at
  [Florian].
- Sheets of different sizes are needed: several sheets of one size alone
  are not enough [decided, 2026-10-14].
- Parts are nested inside the openings of other parts: a part with a big
  hole takes the smaller parts that fit in it [decided].
- The grain direction: the turns a part may take are given per part
  [decided].
- The sheets are about 2470 x 1240 and the bed 2000 x 1000, so full sheets
  are sawn into blanks before they go on the machine; offcuts on hand are
  used as they are [decided].
- The bed's size is given together with the sizes of all the sheets on hand
  when nesting is run [decided].
- At most about 5 saw cuts per sheet [decided].
- One big leftover is better than several small ones; how to weigh that is
  open [decided; the ranking open].
- Trying several settings and keeping the best is not worth it when the
  material used comes out this close [decided].
- Two blanks side by side that the bed takes together are not cut apart
  [decided: spotted by Florian in a result].

## Today

Multi Arrange nests compiled parts in Fusion after a compile, with Fusion's
Arrange as a black-box solver (grain, groups, machining face up, several
sheets, reading the `lang`/`part` attribute, see `design/emitter.md`), and
`fits_sheet` checks each part against its material's sheet size.

## Proposed

Nesting is a step after the layout, in plain Python, over the layouts of
all a build's modules [proposed]. The solver is PackingSolver, through its
Python package (see "Findings") [proposed]; Fusion's Arrange through Multi
Arrange stays as the fallback.

- **Running it**: nesting is run with the stock and the machine given: the
  bed's size, every size of sheet on hand per material (a count, or as many
  as needed), the offcuts on hand, the spacing between parts, the margin to
  a blank's edge, the saw's kerf and the most cuts per sheet [decided: bed
  and sheets given when run]. They come from a stock file per workshop
  (or build), and any of them can be given when nesting is run, e.g.
  `python -m lang.nest examples/van.py --bed 2000x1000 --sheet 2470x1240
  --sheet 1525x1525*2 --offcut 1250x600` [proposed; the spelling a working
  title].
- **Input**: the parts' machine outlines (see `bevels.md`), by material, as
  polygons that contain the true outline (arcs sampled, then grown and
  simplified, at most about 0.6 mm outside), with their through holes, so
  smaller parts go into them [decided: part-in-part]. Each part's turns
  [decided]: a part with grain is first turned so its grain runs along the
  sheet's length, then may turn by 0 or 180 degrees; a part whose grain does
  not matter (hidden, or a material without grain) by 90 degree steps or any
  angle. The grain is the layout's `grain`; where none is set (no example
  sets one yet) along the part's longer side [open]. No part is flipped,
  since its machining face goes up. Manufacturing groups (`design/todo.md`)
  are nested rigid [open: not tried]. Left out: slats, which go on the cut
  list by length, and boards marked `.nest(False)` (strips ripped on the saw,
  say), a property modifier like `.manual()`, which go on the cut list by
  size; a rule may set it for a whole kind of part. A part larger than the
  bed is sawn by hand (`.nest(False)`) or machined in two setups, moved
  between them [open]; `fits_sheet` checks against the bed too.
- **Stock and the bed**: nest first, saw after [proposed, measured below]:
  1. The parts are nested on blank sizes that fit the bed (a grid, plus the
     stock's and the bed's own sizes, priced by area plus a little for each
     blank), on the offcuts on hand that fit the bed as they are, and on the
     bed-sized pieces of offcuts that do not (priced next to nothing, so
     they go first).
  2. Each blank is cut down to its parts, so what is left of a sheet stays
     in one piece.
  3. PackingSolver's guillotine solver saws the blanks out of the stock:
     straight cuts right through, the kerf between them, each blank in the
     sheet's grain. The plan is made as simple as it allows: two blanks
     side by side are one when the bed takes them together [decided], a
     blank takes a rest too small to keep along, pieces along a thin waste
     strip take it along. A sheet gets at most `max_cuts` cuts (5)
     [decided]; among the few settings tried the plan kept has: no sheet
     over the limit, the cheapest stock, the largest single leftover, the
     fewest cuts [proposed; the leftover's ranking open, see below].
  4. Refill: the parts of the sheet bought with the fewest are nested into
     the room left on the others (in used blanks, around their parts, then
     in their leftovers, cut down); when all fit, that sheet is not needed.
  One setting of the nest, not several tried [decided].
- **Output**: a nest file committed next to the layouts: per piece of stock
  the saw plan (its cuts, in order), the blanks, each part's blank and
  placement on it, and the leftovers worth keeping, which go back into the
  stock file as offcuts. A changed nest then shows in a diff. The preview
  gets a nest view (the sheets with their saw cuts, blanks and leftovers,
  the parts with grain and labels, the waste per sheet; as drawn by the
  experiments). The emitter writes either the module documents as now or a
  nested document per material, each blank a stock body and each part flat
  on it with its machining face up, named by path. CAM goes there.
- **Cut sheets are pinned.** A van is built over weeks, so a sheet marked as
  cut keeps its nest; later nests take only the parts not cut yet and report
  parts that changed after they were cut [open].
- **Leftovers**, ways to rank them, for Florian to choose [open]:
  1. In order, no weights (what the experiments do): the stock used, then
     the largest single leftover, then the fewest cuts.
  2. A threshold for what counts as stock at all, tied to what the workshop
     reuses (the experiments: 200 mm across and 0.1 m²; say 300 mm and
     0.25 m²); below it a rest is waste, and a blank takes it along instead
     of a cut.
  3. One number when a single score is needed: the sum of the leftovers'
     areas squared (one piece of 1 m² scores 1, two of 0.5 m² score 0.5),
     after the stock used.
  4. Pieces across the whole sheet (full width or length) preferred: they
     store and reuse best.
  Claude's suggestion: 1 with 2, the threshold from Florian.

## Findings (experiments, 2026-10-14)

All in `experiments/nesting/` (branch `claude/svg-nesting-experiments-
4c86b5`): the parts exported per material from the examples' layouts, jobs,
SVGnest run headless, PackingSolver through its Python package, the blank
sawing, and a checker that judges every solver's result the same way with
shapely on the true outlines (overlaps, the gap between parts, the margin to
each blank's edge, defects, the turns and the grain) and draws it. Every
result reported here passed it. Measured on Florian's Mac (14 cores). Parts:
birch 15 of all examples (62 parts, 9.26 m², about 3 sheets), the van's (20
parts, fit on one sheet), an irregular set (45 parts: a ring with discs,
curved rails, wavy shelves, rocker runners, coved brackets, rounded L
brackets, ovals, random concave polygons, chair sides; 4.41 m²) and
synthetic cases. Spacing 10 mm, margin 10 mm, kerf 4 mm.

### Libraries

Checked 2026-10-14 against their repositories and packages.

| | Licence, state | Sheets of different sizes | Turns per part | Part-in-part | From Python |
|---|---|---|---|---|---|
| SVGnest | MIT, last commit 2019 | no: copies of one bin | one count for all | broken (a bug) | no: browser code (ran in node with stand-ins) |
| Deepnest (deepnest-next) | MIT, active | sheet list, used in order | one count for all | yes | no: Electron app, native addon, no CLI |
| **PackingSolver** | MIT, released daily | **sheet types with counts and costs, leftovers, irregular sheets, defects** | **ranges per part** | **yes** | **`pip install packingsolver`, wheel for macOS arm64** |
| jagua-rs + sparrow | MPL / MIT, active | jagua-rs: yes, but its bin packing optimiser is a reference only; sparrow (the best packer in the literature): strips only, its bin packing closed and licensed | yes | no (holes refused) | spyrrow (strips only) |
| Packaide | GPL, 2022 | rectangles | one count | claimed | build with CGAL and Boost.Python |
| libnest2d | LGPL | copies of one bin | one list | no | no macOS wheel |
| ironnest | MPL, young (2026-06) | sheets in order | per part | not stated | wheel |

### SVGnest: not a fit

- Nests into one bin shape and opens copies of it when parts remain; sheets
  of different sizes only through Multi Arrange's trick, one bin made of the
  sheets joined by thin bridges. That needs its `exploreConcave` option
  (else only one sheet of the set is found), and the option makes every
  no-fit polygon orbital: 3 evaluations in 5 minutes for 62 parts, 132
  failed no-fit polygons, overlapping parts in the result, and leftover
  parts got another copy of the whole set of sheets.
- Part-in-part does nothing as shipped: svgnest.js builds the part tree with
  `children` but reads holes as `childNodes`; with that fixed it works.
- 99 % of its time goes into no-fit polygons (Clipper's Minkowski sum in
  JavaScript, cost about the product of the two parts' vertex counts: 1.9 s
  for two notched battens of 108 vertices), and it keeps them for one
  evaluation only (kept, 300 evaluations took 37 s instead of about 12).
- The van's parts, which fit one sheet: 2 sheets in 8 of 9 runs (up to 10
  minutes each); its own page found 1 once, and its export put the parts
  half the spacing from two edges.
- Repeatable only with a seeded `Math.random` and a fixed number of
  evaluations.

### PackingSolver: how it is used

- `packingsolver.irregular` nests: an `InstanceBuilder` with bin types (a
  shape, copies, cost, defects with their own spacing), item types (a
  `ShapeWithHoles` of points and circular arcs, allowed turns as
  `(start, end, mirror)` ranges, copies), the spacing between items, an
  objective (`BinPacking`: fewest bins; `VariableSizedBinPacking`: cheapest
  bins, the one for mixed stock; `Knapsack`: as much as the bins take;
  `BinPackingWithLeftovers`; `OpenDimensionX`: strips), `optimize` with a
  time limit and a mode. A placement is the part turned about its own
  origin by `angle` (counter-clockwise), then moved by `bl_corner`
  (despite the name, not its bounding box's corner).
- `packingsolver.rectangleguillotine` saws: rectangles (fixed orientation:
  the grain) out of sheets (counts, costs, trims), the cut thickness, two or
  three stages, the first cuts across or along, limits on the cuts per
  stage, `BinPackingWithLeftovers` (fewest sheets, then the largest leftover
  on the last one). Its solution is the cutting tree (each node's depth,
  parent, rectangle, and item, waste or residual).

### PackingSolver: performance

| Case | Result | Time |
|---|---|---|
| The van's 20 parts, one sheet size | 1 sheet (SVGnest: 2) | 0.01 s |
| 62 parts; offcut 1250 x 600, two 2000 x 1000, sheets 2500 x 1250 as needed | 5 (offcut, one 2000 x 1000, three sheets), 76 % covered | best at 3 s |
| The same three times, 186 parts | 13, 80 % | first 0.3 s, best 6.5 s |
| 45 irregular parts, one sheet size | 3, 47 %; the same with polygons or arcs, grain or free turns | 0.03–0.1 s, no better in 120 s |
| The same, knapsack on 2 sheets | 40 of 45 placed, 64 % | still improving at 215 s of 300 |
| A frame's opening, six parts in it | all six in it | 4 ms |

- The first nest comes at once and is good; on rectangular parts it improves
  over seconds, on irregular parts its default search hardly improves it
  (one wider tree search, queue 64, finished in 4 s with the same 3
  sheets); knapsack on one sheet fewer keeps improving for minutes.
- It uses about 6 cores per run, runs until the time limit unless it proves
  the result optimal, and gave the same nest for the same input in every
  repeat tried (its default and its deterministic mode).
- True arcs are exact (areas within 0.015 % of a 0.01 mm sampling) but gave
  the same nests as polygons simplified to 0.25 mm; coarser polygons (1, 2,
  5 mm) did not help its search either.

### PackingSolver: quirks, and what the experiments do about them

- A part that fits a sheet but not within `item_bin_minimum_spacing` is
  placed anyway, centred, the gap shrunk on both sides (a 410 high
  rectangle in a 413 high sheet with spacing 10: 1.5 mm above and below).
  Each sheet is shrunk by the margin instead, and its spacing left at 0.
- Part-in-part fails when the holed part's outline or its hole is a full
  circle, and in some cases where both have arcs (a disc never went into a
  ring given as arcs; the same ring as a polygon took it at once). Holes go
  in as polygons. Probably a bug; not reported upstream.
- A defect may be touched unless its spacing is set (per defect).
- A cost of 0 and a bin type with 0 copies are refused (an offcut on hand
  costs 1, against a sheet's 3 million).
- Bin packing returns nothing when the stock cannot take all the parts;
  knapsack places what fits.
- `BinPackingWithLeftovers` did not push the parts aside, and its strip
  packing found nothing on a sheet's own length and 3090 mm on a longer one
  for parts bin packing fits in 2366.

### Several sheets, offcuts, defects

`VariableSizedBinPacking` takes each size of sheet and each offcut as a bin
type with its count and cost (its area; an offcut on hand next to nothing)
and picks the cheapest set; `BinPacking` counts sheets only, so it fills a
small offcut as gladly as a full sheet (6 sheets where variable sizes gave
5). Offcuts may have any outline (an L-shaped one took 14 of the van's 20
parts, all inside it) and defects, kept clear by their own spacing.

### Grain and part-in-part

- Grain: in a test with the 62 parts, hidden floor strips free, drawer
  faces with the grain across, the rest along the sheet, every part kept
  its grain along the sheet and the free ones used their freedom (two
  turned by 90 degrees); 5 sheets, best at 1.7 s.
- Part-in-part: parts went into a frame's opening (all six), the van's
  `kitchen.right` into a face frame's 1300 x 620 opening, a blob into the
  irregular set's ring. The examples' own openings take no part (the big
  ones are triangles, and the grain rules out the rest).

### The bed: blanks

Sheets 2470 x 1240, bed 2000 x 1000, kerf 4. Material used: the stock sawn
less the pieces left whole as stock (at least 200 mm across and 0.1 m²).

| Parts | Way | Sheets | Cuts per sheet | Left as stock | Material used |
|---|---|---|---|---|---|
| 62 | as if the bed took whole sheets | 4 | – | – | (12.25 m² of sheets) |
| | fixed sawing pattern, up to 3 cuts, the best of 104 | 5 | 3 | 1.49 m² | 13.82 m² |
| | nest first, saw after | 5 | 3, 3, 3, 3, 2 | 3.17 m² in 6 pieces, the largest 1294 x 1240 | 12.14 m² |
| | the same, with offcuts 1250 x 600, 900 x 450, 1600 x 300 | 5 + the 3 | 3, 2, 2, 2, 2 | 4.97 m² | 10.35 m² of sheets |
| | the same, sheets 2470 x 1240 and two 1525 x 1525 | four and one 1525 x 1525 | 3, 3, 3, 3, 2 | 2.38 m² | 12.19 m² |
| | the same, an offcut 2470 x 600 (larger than the bed) | 5 + the offcut | 1 to 3 | 5.10 m², the largest 1270 x 1240 | 11.70 m² |
| | the same, a bed of 2500 x 1250 | 5 | 0, 2, 4, 2, 2 | 3.61 m², the largest 2470 x 645 | 11.70 m² |
| 124 | as if the bed took whole sheets | 8 | – | – | (24.5 m² of sheets) |
| | fixed sawing pattern | 10 | 3 | 3.46 m² | 27.17 m² |
| | nest first, saw after | 11 | 2 on 8 sheets, at most 4 | 9.65 m² in 17 pieces | 24.04 m² |

- Nest first, saw after uses no more material than nesting whole sheets
  would: the bed costs a sheet or two more to buy, and they come back as
  leftovers. Fixed patterns are simpler to saw (every sheet alike) but use
  12 to 15 % more, and most of them cannot take every part at all (no blank
  long or wide enough: 12 of 104 can for the 62 parts).
- Time: the nest 20 s for 62 parts (40 s for 124; 3 s found nothing, 8 s
  gave 6 sheets), the sawing about a second per setting (10 settings), the
  refill 10 s a try.
- The number of sheets depends on the settings (the blank grid, the price
  per blank, cutting blanks down): 5 to 7 for the 62 parts, the material
  within 5 %. Leaving blanks uncut when the freed strip would be narrow made
  it worse (bigger blanks pack worse). Refill took a sheet back now and
  then (11 to 10). Two runs of the same job gave the same result.
- The saw plan as the solver gives it needed up to 5 cuts on a sheet;
  joining blanks the bed takes together and letting pieces take thin waste
  along brought the 62 parts from 5, 3, 5, 5, 2 cuts to 3, 3, 3, 3, 2 and
  made a leftover corner of 441 x 206 into 515 x 246. The simplifying does
  not reorder cuts (a rip first where the solver cut across first), so a
  plan may still take a cut more than it could [open].
- With a bed as large as the sheet (2500 x 1250) the cuts only keep
  leftovers: 0 to 4 per sheet, 3.61 m² kept, the largest 2470 x 645.

### Pushing the parts to one side

- Sliding the parts of a finished nest toward a corner gains nothing on
  PackingSolver's nests: each part already rests on its neighbours.
- A search on the sheet's length (bin packing on ever shorter sheets) works
  where a sheet has room: an irregular last sheet from 1779 to 1348 mm in
  10 s, the examples' emptiest sheet from 2466 to 2122 mm in 21 s; on a full
  sheet it finds nothing shorter.
- With blanks it comes by itself: each blank is cut down to its parts, so
  the last sheet keeps its rest whole (1294 x 1240 for the 62 parts).

### Still open

- How leftovers are ranked, and the threshold for keeping one (above).
- The grain where `grain()` is not set.
- Reordering a saw plan's cuts; trimming factory edges (the guillotine
  solver takes trims); refill on a sheet whose cut budget is spent.
- Parts larger than the bed; manufacturing groups; pinning cut sheets.
- Irregular parts: whether a time budget for knapsack on one sheet fewer is
  worth it in the language, or the first nest is enough.
