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
- Its weak point, seen on irregular parts (curves, concave shapes): the
  first nest comes at once and is good, then its default search hardly
  improves it (3 sheets at 47 % for 45 irregular parts, whatever the time
  limit). Knapsack on one sheet fewer keeps improving: 40 of 45 parts on 2
  sheets after 5 minutes. So a nest in the language would take the first
  bin packing, then try one sheet fewer with knapsack for a time budget.

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
| Van + a face frame 1400 x 720 with a 1300 x 620 opening, 21 parts | PackingSolver | 2 | | `kitchen.right` in the opening; 1 sheet looks possible |
| Irregular, 45 parts, 4.41 m² (`irregular.py`: ring and discs, curved rails, wavy shelves, rockers, coved brackets, L brackets, ovals, random concave polygons, chair sides) | SVGnest + cache + holes | 3 | 47 % | 13 evaluations in 600 s (the first 252 s) |
| | PackingSolver, `binpacking`, polygons or arcs, grain or 4 turns or any angle | 3 | 47 % | 0.03–0.1 s, no better in 60–120 s |
| | PackingSolver, tree search queue 64 (deterministic) | 3 | 47 % | 4 s |
| | PackingSolver, `knapsack` on 2 sheets | 2, 40 of 45 placed | 64 % | 300 s, still improving at 215 s |
| All examples, mixed stock, grain per part (hidden floor strips free, drawer faces across) | PackingSolver, `variable` | 5 | 76 % | best at 1.7 s; two strips turned 90 |

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
- Grain per part: each part type takes its own list of turns (ranges
  `(start, end, mirror)`; equal ends give one angle). `jobs.py` turns each
  part so its grain runs along the sheet (the layout's `grain` when set,
  else its longer side, `--across` its shorter one) and gives it 0 and 180;
  parts named by `--free-parts` (hidden ones, say) get 90 degree steps or
  any angle. In the mixed test it kept every grain along the sheet and used
  the freedom where it had it. No example sets `grain()` yet, so the
  fallback decided everywhere.
- Part-in-part: works with polygons (the frame case, the face frame with
  the van, a blob inside the ring). It fails when the part with the hole,
  or the hole, is a full circle (`build_circle`), and in some cases where
  both the outline and the hole have arcs: a disc never went into a ring
  given as arcs, while the same ring as a polygon took it at once [tested
  in isolation, 2026-10-14; probably a PackingSolver bug, not reported]. So
  holes go in as polygons.
- True arcs: accepted and exact (areas within 0.015 % of a 0.01 mm
  sampling), but they gave the same nests as polygons simplified to
  0.25 mm, so polygons are enough, and safer for holes (above). Coarser
  polygons (1, 2, 5 mm) did not help the search either.
- Irregular parts: the first nest interlocks shapes (wavy shelves face to
  face, chair sides nested, rails in pairs), but the default search (tree
  search plus "sequential single knapsack" for bin packing, per its
  source) stops improving after its first pass on these parts; a tree
  search with queue 64 finished in 4 s with the same 3 sheets. Knapsack
  on a fixed number of sheets runs column generation and improves for
  minutes (107 improvements in 300 s).
- Offcuts with any outline and defects (a knot, a used corner): an
  L-shaped offcut took 14 of the van's 20 parts (knapsack), all inside its
  outline; a defect is kept clear by `item_defect_minimum_spacing`, set per
  defect (the spacing; by default parts may touch it). A sheet type with 0
  copies is refused, so `ps_nest.py` leaves those out.
- Packing toward one side (an offcut strip across the sheet): **open**.
  The `leftovers` objective did not push the parts aside in any of its
  modes; its strip packing (`OpenDimensionX`) found nothing on the sheet's
  own length and 3090 mm on a longer one for parts that bin packing fits
  in 2366; a binary search on the sheet's length with bin packing
  (`--compact`) works, but on the sheets tried it found no shorter length
  within 3 s per step (the van's sheet is nearly full lengthwise anyway: by
  hand the parts need about 2440 mm).
- Not tried yet: quality rules, and sawing full sheets into blanks for the
  2000 x 1000 bed (its rectangle guillotine solver could saw the blanks the
  nest chooses).

## Files

- `export_parts.py`: layout files to one parts file per material (machine
  outline = outline less through cuts, simplified so that it never cuts
  into the part) and an SVG for SVGnest's page.
- `cases.py`: synthetic parts (squares, a frame with an opening, mixed
  shapes, a face frame).
- `irregular.py`: irregular parts, each with true arcs, a fine sampling for
  the checks and a containing polygon for the solvers.
- `jobs.py`: a parts file to a job: sheets (`2500x1250`, `2000x1000*2`, or
  several bridged for SVGnest), offcuts (`--offcut "x,y ..."`) and defects,
  grain and turns per part, spacing and margin, SVGnest's options and
  patches.
- `svgnest/nest.mjs`: SVGnest headless.
- `ps_nest.py`: PackingSolver (objectives, modes, `--arcs`, `--compact`,
  `--set` for its parameters).
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
