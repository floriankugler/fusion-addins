# Nesting experiments

A tryout of nesting solvers for "Nesting" under "Still to do" in DESIGN.md
(branch `claude/modeling-language-features-6de0e5`), before anything goes
into the language. Nothing here is used by `lang/`. Florian's must-haves
[2026-10-14]: sheets of different sizes (offcuts, blanks, full sheets) and
parts nested inside the openings of other parts.

Measured on 2026-10-14 on Florian's Mac (14 cores), on the examples' real
parts and on synthetic cases.

## Verdict

**SVGnest is not a good fit; PackingSolver is.**

- SVGnest (MIT, last commit 2019) nests into one bin shape and opens more
  copies of it. Different sheet sizes need Multi Arrange's trick (sheets
  joined by thin bridges into one bin), which only works with its
  `exploreConcave` option, and that option switches every no-fit polygon
  to its orbiting algorithm: 3 evaluations in 5 minutes for 62 parts, 132
  failed no-fit polygons, and overlapping parts in the result.
  Part-in-part does not work as shipped (a bug, one name wrong); fixed, it
  does. It is slow on the parts the language makes (99 % of the time in
  no-fit polygons) and needed 2 sheets for what fits on 1.
- PackingSolver (MIT, `pip install packingsolver`, released daily, wheel
  for macOS arm64) does variable-sized bin packing natively: sheet types
  with counts and costs, irregular sheets with defects, part-in-part,
  turns per part, separate spacing to parts and to the sheet's edge, true
  circular arcs. It put the van's parts on 1 sheet in 0.01 s and 62 parts
  of the examples on mixed stock in 3 s.

## Numbers

Birch 15, grain along the sheet (turns 0 and 180 only), 10 mm between
parts and to the edge. Every result checked by `check.py` with shapely on
the true outlines: no overlaps, the gaps, the sheet each part is on.

| Case | Solver | Sheets | Cover | Time |
|---|---|---|---|---|
| Van, 20 parts, 2.06 m² (fit on one 2500 x 1250) | SVGnest, as shipped (headless) | 2 | 33 % | 12 evaluations in 29 s; 3 seeds x 10 min (~148 each): still 2 |
| | SVGnest + kept no-fit polygon cache | 2 | | 300 evaluations in 37 s |
| | SVGnest with its own (round) spacing | 2 | | 300 evaluations in 233 s, 2 seeds |
| | SVGnest's own page (browser, web workers) | 1 | | ~1 min, one run; parts 5 mm from the edge |
| | PackingSolver | **1** | 66 % | 0.01 s |
| All examples, 62 parts, 9.26 m²; stock 1250 x 600 x1, 2000 x 1000 x2, 2500 x 1250 as needed | SVGnest, bridged (offcut + 2 blanks + 1 sheet) | 9 (3 copies of the set) | 52 % | 3 evaluations in 325 s; **3 overlapping pairs** |
| | PackingSolver, `variable` (cheapest by area) | **5** (offcut, 1 blank, 3 sheets) | 76 % | best at 3 s |
| | PackingSolver, `binpacking` (fewest sheets) | 6 | 66 % | 0.03 s |
| The same x3, 186 parts | PackingSolver, `variable` | 13 | 80 % | first at 0.3 s, best at 6.5 s |
| Frame 1200 x 800 with a 1000 x 600 opening + 6 parts of 300 x 200, on 1300 x 900 | SVGnest, `useHoles` | 2 | | (the option does nothing) |
| | SVGnest, `useHoles` + `holes` patch | **1** | | all six in the opening |
| | PackingSolver | **1** | | all six in the opening, 4 ms |

## SVGnest's quirks

Run headless by `svgnest/nest.mjs`, which loads its files unchanged into a
node vm with stand-ins for the browser (workers, SVG parsing, the timer)
and a seeded `Math.random`. Fixes are opt-in patches applied in memory
(`--patch holes cache`); `vendor/SVGnest` stays as cloned.

- **One bin shape.** Its placement worker opens another copy of the bin
  while parts remain (fitness +1 per bin), so identical sheets work; there
  is no list of sheets. Rotation is one global count for all parts
  (`rotations: 2` gives 0/180); grain is handled by turning parts first.
- **Bridged sheets** (Multi Arrange's trick): a bin that is not a rectangle
  gets its inner fit polygon from the orbiting algorithm, which without
  `exploreConcave` finds one region only: each copy of a three-sheet bin
  used one of its sheets. With `exploreConcave` all regions are found
  (synthetic squares), but the option also makes every part-part no-fit
  polygon orbital: about 100 s per evaluation for 62 parts, "NFP Error"
  132 times, and overlapping parts. Leftover parts get another copy of the
  whole set of sheets, not more full sheets. SVGnest also skips its inward
  offset of the bin (the margin) when it does not give one polygon, which
  bridges never do.
- **Part-in-part is broken**: svgnest.js builds the part tree with
  `children` but reads holes as `childNodes`, so `useHoles` never runs and
  holes are not shrunk by the spacing. Patch `holes` fixes both; then it
  works.
- **Speed**: Clipper's Minkowski sum in JavaScript, cost about the product
  of the two parts' vertex counts: 1.9 s for two notched battens of 108
  vertices each. It keeps its no-fit polygons for one evaluation only and
  computes most of them again for the next (patch `cache` keeps them: 300
  evaluations in 37 s instead of about 12). Its spacing offset rounds every
  convex corner (a rectangle gets 20 vertices), 6.5 times slower than
  offsetting the parts beforehand with mitred corners (`jobs.py --offset
  own`, the default).
- **Quality** varies a lot by run: of nine runs on the van's parts (eight
  headless, up to 10 minutes and 300 evaluations each, one on its page),
  only the one on its page found one sheet. The genetic algorithm evaluates one
  order at a time, starting from the parts sorted by area, and places each
  part greedily at the no-fit polygon vertex that keeps the bounding box
  narrowest.
- **Its page's export** places the parts relative to the sheet's own
  corner while the solver placed them in the sheet shrunk by half the
  spacing: parts end up half the spacing from the left and top edges
  (5 mm for a 10 mm spacing).
- **Repeatable** only with a seeded `Math.random` and a fixed number of
  evaluations (not a time limit); the page's runs are not.

## PackingSolver's notes

Run by `ps_nest.py` (its own venv: `.venv`, `pip install packingsolver`).

- A placement is the part turned about its own origin by `angle`
  (counter-clockwise), then moved by `bl_corner` (despite the name, not its
  bounding box's corner).
- Objectives: `variable` (cheapest set of sheets, cost = area by default)
  is the one for mixed stock; `binpacking` only counts sheets, so it fills
  the small ones as gladly as full ones; `knapsack` when the stock on hand
  may not take everything: bin packing then returns nothing at all, while
  knapsack placed 55 of 62 parts.
- The default mode (`anytime`) improves until the time limit unless it
  proves the result optimal; the van stopped at once, mixed stock ran to
  the limit with the best at 3 s. Two runs of each case gave the same nest
  (anytime and deterministic modes, 20 s limit); a run limited by time may
  still differ on a slower machine. `sequential` mode placed nothing in
  20 s.
- Part-in-part: works (frame case). On the examples' real parts no
  opening can take a part (the large ones are triangles, and the grain
  rules out the rest), so a real case needs a part with a large rectangular
  opening.
- **Open**: `leftovers` (fewest sheets, then the largest leftover) did not
  push the parts to one side in any of its modes within 20 s: the van's
  parts still reach 2366 of 2500 mm, where they fit in about 1900. Whether
  a longer run, another mode or the `variable` objective with costs does
  better is to be tried.
- Not tried yet: true arcs (the layout's outlines are sampled; the
  emitter's arc recovery could give PackingSolver the arcs), defects (used
  parts of an offcut), quality rules, and its rectangle guillotine solver
  for sawing full sheets into blanks for the 2000 x 1000 bed.

## Files

- `export_parts.py`: layout files to one parts file per material (machine
  outline = outline less through cuts, simplified so that it never cuts
  into the part) and an SVG for SVGnest's page.
- `cases.py`: synthetic parts (squares, a frame with an opening, mixed
  shapes).
- `jobs.py`: a parts file to a job: sheets (`2500x1250`, `2000x1000*2`, or
  several bridged for SVGnest), grain, spacing and margin, SVGnest's
  options and patches.
- `svgnest/nest.mjs`: SVGnest headless.
- `ps_nest.py`: PackingSolver.
- `check.py`: checks any result against its job and draws it.

```bash
# once: the examples' layouts, their parts, PackingSolver's venv, SVGnest
for f in examples/*.py; do n=$(basename $f .py); [ $n = stock ] || .venv/bin/python -m lang.build $f --out experiments/nesting/out/layouts/$n; done
.venv/bin/python experiments/nesting/export_parts.py experiments/nesting/out/layouts/*/layout.json --out experiments/nesting/out/parts/all
python3 -m venv experiments/nesting/.venv && experiments/nesting/.venv/bin/pip install packingsolver shapely
git clone https://github.com/Jack000/SVGnest.git experiments/nesting/vendor/SVGnest

# a job, then either solver, then the check
.venv/bin/python experiments/nesting/jobs.py experiments/nesting/out/parts/all/birch_15.json --sheets "1250x600*1" "2000x1000*2" 2500x1250 --out experiments/nesting/out/jobs/mixed.json
experiments/nesting/.venv/bin/python experiments/nesting/ps_nest.py experiments/nesting/out/jobs/mixed.json experiments/nesting/out/results/mixed.json --objective variable --time-limit 30
node experiments/nesting/svgnest/nest.mjs experiments/nesting/out/jobs/mixed.json experiments/nesting/out/results/mixed_svgnest.json
.venv/bin/python experiments/nesting/check.py experiments/nesting/out/jobs/mixed.json experiments/nesting/out/results/mixed.json --svg mixed.svg
```

SVGnest's own page: launch configuration `svgnest` (port 8766), then
`http://localhost:8766/vendor/SVGnest/index.html`, upload an SVG from
`out/parts/<set>/<material>.svg` and click the sheet (the rectangle at the
top left) to make it the bin.
