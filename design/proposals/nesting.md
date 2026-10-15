# Nesting in the language

Status: added by Florian 2026-10-14, worked out by Claude the same day,
tried in `experiments/nesting/`, and built the same evening: what is built,
and the experiments' findings, are in `design/nesting.md`. This file keeps
Florian's points and what is still open. Points marked [Florian] are his
ideas, [decided] his decisions, [proposed] Claude's, [open] undecided.
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
- One big leftover is better than several small ones [decided]; ranked
  by the stock used, then the largest single leftover, then the fewest
  cuts, a rest kept from 300 mm across and 0.25 m² [decided 2026-10-14].
- A part whose grain the build leaves unset turns freely, by quarter turns
  [decided 2026-10-14].
- Trying several settings and keeping the best is not worth it when the
  material used comes out this close [decided].
- Two blanks side by side that the bed takes together are not cut apart
  [decided: spotted by Florian in a result].

## Decided while building, for Florian to review

Claude's decisions of 2026-10-14/15, built and marked [proposed] in
`design/nesting.md`:

- The workshop file is TOML (`examples/workshop.toml`): `bed`, `spacing`,
  `margin`, `kerf`, `max_cuts`, `keep_across`, `keep_area`, `seconds`,
  `[[sheet]]` (size along the grain first, `count` or as many as needed,
  `material` or every material), `[[offcut]]` (material and size). The
  command line's `--sheet` and `--offcut` replace the file's of their kind;
  an offcut on the command line names its material (`"birch 15:1250x600"`).
  No default bed or sheets.
- Several build files can be nested together, their paths after the file's
  name (`van:floor.batten0`).
- Blanks are priced by the area they take of the sheet that suits them,
  a strip beside them too narrow for another blank counted with them
  (by their own area, bed-sized blanks left only waste beside them).
- Two blanks side by side are joined (your rule) only where two margins
  and the kerf make up the spacing.
- The saw plan is in tenths of a millimetre, the kerf rounded up to one; a
  sliver narrower than the kerf is trimmed off where a piece would
  otherwise not fit the bed.
- The nest takes 0.6 s a part, at least 5 s and at most `seconds` (40), the
  solver's time-bound search; the fixed search is an option
  (`--mode deterministic`).
- A sheet over `max_cuts` is reported, not refused.
- Manual parts are never nested; the van's long battens and floor panels
  say `nest(False)`.
- The nest file lists the leftovers but nothing writes them back into the
  workshop file yet (with pinning, below).
- Compile Layout takes a `nest.json` as well as a layout (no new button).

## Still open

- **Cut sheets are pinned.** A van is built over weeks, so a sheet marked as
  cut keeps its nest; later nests take only the parts not cut yet and report
  parts that changed after they were cut [open]. With it, the leftovers of
  the sheets cut go back into the workshop file as offcuts (the nest file
  lists them; nothing writes them back yet).
- **Parts larger than the bed**: today `nest(False)` (sawn by hand), as the
  nest refuses them by name; machined in two setups, moved between them,
  is open.
- **Manufacturing groups** nested rigid (`design/todo.md`) [open: not
  tried].
- **A rule** that sets `nest(False)` for a whole kind of part [proposed],
  once the language has rules.
- **The cut list**: slats by length, `nest(False)` boards by size
  (`build-repo.md`).
- **The saw plan**: reordering its cuts (the simplifying keeps the solver's
  order, a rip first where it cut across first, so a plan may take a cut
  more than it could); trimming factory edges (the guillotine solver takes
  trims); refill on a sheet whose cut budget is spent.
- **Offcuts with an outline** (an L-shaped piece) **and defects**:
  PackingSolver takes both (the experiments), the workshop file has
  rectangles only.
- **Irregular parts**: whether a time budget for knapsack on one sheet
  fewer is worth it, or the first nest is enough.
- **Reproducible nests**: the nest runs for its time and keeps the best it
  found, so a slower or busier machine may find another (a changed nest
  shows in a diff), and too short a time costs sheets (7 instead of 5 for
  the examples' 62 parts in 20 s). `--mode deterministic` runs one fixed
  search instead, which split 124 parts into many small blanks (see
  `design/nesting.md`, Measured); the saw step is time-bound either way.
- **Any angle** for parts whose grain does not matter: not offered, so
  every face stays along an axis in Fusion.
- **`fits_sheet` against the bed**: the bed is given when nesting is run,
  not in the build, so the nest refuses what the bed cannot take instead.
