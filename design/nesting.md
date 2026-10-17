# Nesting

How a build's parts get onto the stock on hand and the machine's bed: plain
Python after the layout step, like the preview, and drawn into Fusion by
the emitter. Part of the modeling language's design; the overview is
`DESIGN.md`. Code: the nests declared in the build in `lang/core/nests.py`
(`Scope.nest`, `design/api.md`, Nests), the rest in `lang/nesting/` (`keys`,
`resolve`, `inventory`, `workshop`, `items`, `packing`, `sawing`,
`refilling`, `nest`, `verify`, `draw`, `nest_types`, `fingerprint`,
`pinning`, `ledger`), `lang/emit/nested.py` and `NestEmitter` in
`lang/emit/fusion.py`. Florian added it as a proposal on 2026-10-14 and it
was built the same evening; the nests moved into the build on 2026-10-16
(stage 2 of `proposals/settings.md`), and the parts' fingerprints, nests
marked as made and the inventory written back followed the same day
(stage 3, Pinning); what is still open is under "Still open", the
experiments behind it are at the end and in `experiments/nesting/`.

## Nests in the build

A nest is declared in the module that needs it, `cab.nest("carcass",
material=ply15)` or `cab.nest("fronts", [front1, front2])`, with settings
of its own (`.use(nesting.margin(15))`); what no declared nest of its
module takes makes one nest per material per module, named after the material
(`kitchen.birch_15`), so a build that declares none nests each module's
boards by material [Florian, 2026-10-16; `design/api.md`, Nests]. The
package is `lang.nesting`, the boards' key `nest`, the declaration a method
on the scope, so the three do not share a name [decided by Florian
2026-10-16].

## Running it

```
python -m lang.nesting examples/van.py                        # every nest of the build
python -m lang.nesting examples/van.py kitchen.birch_15 floor.birch_15
python -m lang.nesting out/van/layout.json --inventory stock.toml
python -m lang.nesting examples/van.py --status               # what changed, nesting nothing
python -m lang.nesting examples/van.py --made kitchen.birch_15        # made, every sheet (Pinning)
python -m lang.nesting examples/van.py --made kitchen.birch_15 1 2    # sheets 1 and 2
python -m lang.nesting examples/van.py --fixed kitchen.birch_15 kitchen.left
```

- The command takes one build file (or a layout file) and the nests to
  nest by path, none meaning all; one source per nest [decided
  2026-10-16]: the merging of several build files and their `van:` path
  prefixes are gone, and the measurements over all the examples merge
  their layouts in a test helper.
- The machine is settings (`lang/nesting/keys.py`, `design/api.md`,
  Settings): the bed, the spacing between parts, the margin to a blank's
  edge, the saw's kerf, the most cuts per sheet, the keep threshold, the
  nest's time and refill, used at the build's root (`use(nesting.bed((2000,
  1000)))`; the examples' `stock.py` has them as `workshop`, which each
  build uses), deviating on a module, a part or a nest. The bed has no
  default: a nest with none is refused [decided]. Defaults: spacing and
  margin 10, kerf 4, at most 5 cuts a sheet [decided: about 5], a rest
  kept from 300 mm across and 0.25 m² [decided 2026-10-14]; the nest's
  time per material 0.6 s a part (`rate`), at least 5 s (`least_seconds`)
  and at most 40 (`seconds`) [decided 2026-10-16, measured below]. The
  workshop file and its command-line overrides are gone.
- A nest's values: its own, else its parts' (each along its chain: the
  part, its scopes, the root), else the default. Where the nest needs one
  value (every key but the spacing) its parts must agree, else the nest is
  refused, naming two parts, their values and where each came from;
  between two parts the larger of their spacings holds (each part's
  solver polygon grows by what it asks for above the nest's least, so two
  parts keep at least the larger) [Florian, the settings proposal].
- The stock: what can be bought is the material's sheet size,
  `sheet_material(..., size=(2500, 1250))`, along the grain first, as many
  as needed (one size per material [decided 2026-10-16]); what is on hand
  is the inventory, a ledger of one kind of entry for full sheets and
  offcuts alike [Florian], `inventory.toml` beside the build file unless
  `--inventory` names another:

  ```toml
  [[stock]]
  material = "birch 15"        # as the layout labels it
  size = [1250, 600]           # mm, along the grain first
  count = 2                    # 1 if not given
  ```

  The nest uses what is on hand before it buys; a material with no size and
  nothing on hand is refused by name. The nests of one run share the
  stock on hand, in their order (a piece one uses is not there for the
  next). A run only reads the file; marking a nest as made writes it back:
  the rests of the sheets made go in, the pieces on hand they used come out
  (Pinning).
- `--no-refill` leaves refill out whatever the nest's `refill`, `--mode
  deterministic` runs the solver's one fixed search instead of the best it
  finds in its time (see Measured).
- It writes each nest into `--out` (by default `out/<build>`, beside the
  preview's build) under its module and name, `out/van/kitchen/birch_15/`:
  `nest.json` (`nest_types.py`, version 3), `nest.layout.json` (the
  layout, for the emitter) and `nest.svg`. Problems are printed and kept in
  the nest file; a nest whose part fits no blank at all, or whose parts
  give two values of a key it needs one of, is an error, and the others
  are nested still. The parts no nest takes are listed at the end.
- Before it nests one, it says which of the nest's parts changed since its
  file was written, which are new to it and which are gone, by the parts'
  fingerprints (The nest file): a nest stays good when only another module
  changed. `--status` says so for each nest, and for a nest marked as made
  what is made of it and what a run would nest, and writes nothing.
- A nest marked as made (`--made`, Pinning) is never nested again: a run
  of it nests what is not made of it into a second nest beside it
  (`kitchen.birch_15-2`) and reports the parts made that the build no
  longer has. `--made` and `--fixed` change the marks only; `--made` runs
  no build.

## What is nested

- A nest's parts: those a nest by material takes (its material's boards in
  its scope that are nested), those a nest names, or a module's nested
  boards of a material that no declared nest of the module takes. A board
  is in one nest of its module at most; a nest around it may name it again
  (a remake), which leaves it in its module's nest.
- Nested are boards but those marked `nest(False)` (strips ripped on the
  saw, panels larger than the bed; they go on the cut list by size) and
  manual parts [decided]; never a slat or a lip, which go on the cut list
  by length (`design/slats.md`), while a lipped board is nested cut back.
  `nest()` is a property modifier, given once, at any time, since it
  changes no shape, and `use(nest(False))` says it for every board of a
  scope. The van's long battens and floor panels say `nest(False)`.
- A `nest(False)` board a nest names is its own blank [decided
  2026-10-16]: sawn to its size out of its material's stock like a blank,
  with no margin, counted in the stock used, the rests beside it kept; it
  may be larger than the bed, so the bed check and the joining of pieces
  leave it out, and nothing else is nested onto it. Its outline is cut by
  hand: the blank is the rectangle around it, from its machining face, in
  its grain where it has one, else its longer side along the sheet. The
  nest file marks it (`own_blank`); the CAM plan will machine its
  operations and no outline. It comes out of the material's sheets or a
  piece on hand.
- A part no blank can take, larger than the bed with its margins either
  way round or than all the stock of its material (along its grain where it
  has one), is refused by name, with `nest(False)` as the way out [decided:
  refused; machining in two setups dropped for now, 2026-10-16].
- Per material, as the layout labels it (`birch 15`), within the nest.
- A part lies on its blank with its machining face up (`machine` in the
  layout: what `machine()` names, else the face with more operations, see
  `design/api.md`), so the nest sees its outline from that face: as it is
  where u × v points out of that face, else mirrored. Never flipped
  [decided].
- Its machine outline is the outline less its through pockets and through
  holes. An opening stays open for other parts where the smallest part of
  the material could go in (its inside, the spacing in from its edge, has
  at least that part's area), and is filled where it could not, sparing the
  solver its vertices [decided: part-in-part].
- The solver gets a polygon containing the outline: grown by 0.375 mm
  (mitred up to 1.5 times that, so square corners stay square and a needle
  of material is cut off), simplified by 0.25 mm, at most 0.81 mm outside
  the outline (0.53 at a square corner). Openings go in as polygons:
  PackingSolver puts nothing into a circular hole. A hole the growth makes
  (a notch whose narrow mouth closes) is held to the same rule as an
  opening.
- Turns: a part whose grain is set keeps it along the sheet's length, 0 or
  180 degrees when its grain runs along its u, 90 or 270 along its v; a part
  whose grain the build left unset, or of a material without grain, turns
  by quarter turns [decided 2026-10-14: free, 90 degree steps]. Never by
  other angles, so its faces stay along the axes in Fusion and in CAM
  [decided 2026-10-16: small hidden parts might nest closer at any angle,
  which is not worth it].

## Nest first, saw after

Per material (`nest.py`):

1. The parts are nested with PackingSolver's variable sized bin packing on
   blank sizes the bed takes: a grid (400 to 2000 by 200 along the grain,
   250 to 1000 across, plus the stock's and the bed's own sizes) of those
   some sheet can give, each priced by the area it takes of the sheet that
   suits it best, counting with it a strip beside it too narrow for the
   smallest blank, plus 0.05 m² for the sawing [decided 2026-10-16; priced
   by their own area, bed-sized blanks won, one a sheet with only waste
   beside it; measured below]; on the pieces on hand the bed takes as they
   are, and on the bed-sized pieces of those it does not take (both priced
   next to nothing, so they go first). With nothing to buy, the grid's
   blanks are those the pieces on hand larger than the bed can give. One setting, not several tried [decided]. A
   nest that found nothing in its time is given twice as long, four times
   at most.
2. Each blank is cut down to its parts and margin, so what is left of a
   sheet stays in one piece. A `nest(False)` board the nest names is a
   blank of its own size, with no margin, nested with nothing else.
3. The blanks are sawn out of the stock (`sawing.py`): the pieces on hand
   first (larger than the bed, or ones the bed takes that the nest left),
   then the material's sheets, bought: PackingSolver's guillotine solver, straight cuts right
   through, the kerf between, each blank in the sheet's grain, in tenths of
   a millimetre (the kerf rounded up to one) [decided 2026-10-16]. Ten settings side by side (two
   or three stages, rips or cross cuts first, limits on the cuts per stage;
   rips first is to be the rule, Still open),
   a second each; the plan is made as simple as it allows, then kept by,
   in this order: every blank sawn, no sheet over `max_cuts`, the cheapest
   stock, the largest single piece kept, the fewest cuts [decided: the
   leftover ranking, 2026-10-14]. Simplifying: two rests side by side are
   one; pieces holding blanks and rests too small to keep, side by side,
   are one piece when the bed takes them together [decided], two holding
   blanks only where two margins and the kerf make up the spacing (their
   parts are that far apart) [decided 2026-10-16]; a rest too small to keep goes along with the
   pieces beside it; a piece the solver left larger than the bed is cut
   down to its blank, also where what comes off is narrower than the kerf
   (the blade takes it whole: a trim) [decided 2026-10-16]. A piece
   holding an own blank is never joined or grown, and is cut down to its
   blank whatever the bed [decided 2026-10-16].
4. Where the stock runs short (a material with nothing to buy), the parts
   of the blanks it could not take are nested again on what is left, twice
   more at most; what still finds no stock is reported as left over.
5. Refill (`refilling.py`): the bought sheet with the least on it is emptied
   into the room on the others, in the pieces holding blanks (around their
   parts) and in each sheet's largest rest while it has two cuts to spare,
   cut down to what it takes; again while it works, unless the nest's
   `refill` is False. A piece on hand is never emptied, nor a sheet
   holding an own blank, and nothing goes onto an own blank.

A rest of a sheet is stock, kept, from `keep_across` and `keep_area`
(300 mm, 0.25 m²); smaller ones are waste. A sheet over the cut limit is
reported, not refused: a sheet larger than the bed both ways needs two cuts
whatever the limit [decided 2026-10-16: five cuts is a target].

## The nest file

`nest.json`, millimetres, version 3 (`nest_types.py`): the nest's name
(`kitchen.carcass`) and when it was written, for a second nest (Pinning)
the nest it follows and why each part is in it (`changed`, `not made`,
`new`), then per material: each piece
of stock used (`sheet`, the material's size, or `offcut`; `bought` or on
hand; its size, x along its length and grain), its saw cuts in the
order they are made (a cut's middle line, edge to edge of the piece it
splits; a piece's cuts, then each of its pieces' in turn), its blanks
(named `<sheet>.<blank>`, their place on it, `own_blank` for a
`nest(False)` board's) with their parts, and its rests, marked kept or
waste. A part on a blank: its path, its fingerprint (below), its machining
face, its turn and where its frame's origin lies, and `transform`, world
millimetres to the blank's frame with the part flat and its machining face
up at z = its thickness. Per material too: the sheets bought by size
(those bought only, not the stock on hand), the pieces on hand used, the
areas (parts, stock, kept, used = stock less kept), the parts left over,
notes (the time the material had, the saw setting kept, the solver's
times). Then the boards of its kind it leaves out and why, the problems,
the settings it ran with (each value, the parts that asked for a larger
spacing, where each value came from, the sheet size to buy per material,
the stock on hand given; `seconds` is the limit), and the hash of the
layout nested (`lang.core.layout.layout_hash`), which says only that
something in the build changed since; whether the nest still holds is told
by its parts' fingerprints. Versions 2 and 3 kept what the emitter reads as
it was.

A part's **fingerprint** (`fingerprint.py`) is a hash of itself as
machined, not of where it sits in the build [decided 2026-10-16]: its
material and thickness, its grain where it is set, its outline and every
operation (pockets, holes, V-grooves, chamfers, a cut with a chamfer, a
narrow face's operations) with its sizes and its face, all as its nest
frame sees them: from its machining face, which is `top` (the opposite face
`bottom`, the narrow faces `+X`, `-X`, `+Y`, `-Y`), from the outline's
lower corner. So machined from its other face a part is another part, and
so is its mirror image. Left out: its place and the way it faces in the
build, its name and its operations' names (a chamfer along a named
operation takes that operation's geometry), the order of its operations,
how a depth was written, a cut without a chamfer (the outline has it),
and its settings. The description is taken in the four quarter turns of
its plane and the least hash kept, so a part turned in its plane is the
same part as long as its grain turns with it; coordinates and sizes are
rounded to 1/1024 mm, a binary step on which no value written with up to
four decimals of a millimetre lies halfway, so the noise of another
position cannot tip it [found by fuzzing, 2026-10-16: a length of 410.4875
rounded to micrometres came out two ways]; rings start at their least
point and run the way that comes first; SHA-256, 16 hex digits. The fuzz
tests build random designs moved, facing another side and in another world
frame (where a frame of the other hand makes the mirror image), and random
boards an operation at a time, and require the fingerprints to hold, and
to change with each operation kept.

## Checked

`verify.py` checks every nest before it is written, apart from the solvers
(the tests and fuzz tests use it too): per piece of stock, its pieces lie
on it apart from each other and with the cuts cover it whole, each cut runs
straight through its piece and through no other, at most `max_cuts`, each
blank but an own blank fits the bed, a rest is marked kept exactly when the
nest keeps it; per blank, each part's true outline as placed lies the
margin inside it (an own blank: its board alone, within it), the larger of
the two parts' spacings from every other part, turned by one of its own
turns; per material, every part placed once or listed as left over, the
sheets bought of the material's size, no more pieces on hand used than
there are. What it finds is a problem in
the nest file. The saw step also refuses a plan whose blank lies outside
its piece.

## The preview and Fusion

- The preview lists a design's nests in its nest view (`design/preview.md`),
  each nest marked as made followed by its second nests, shows the one
  chosen (its `nest.svg`) with the sheets made and the parts changed since
  marked on it, says what changed and what is made, nests that one again
  on request, and marks nests, sheets and parts there (Pinning).
- The compiler's Compile Layout takes a `nest.json` too and draws a
  document per material (no button of its own [decided 2026-10-16]; its
  dialog not yet clicked through with a nest file, `design/todo.md`, nor
  with versions 2 and 3, which changed nothing it reads (3 is not run in
  Fusion yet either);
  `lang/emit/nested.py` plans it, Fusion-free): per
  piece of stock a component, the pieces one above the other along y, per
  blank a component at its place holding the blank as a see-through stock
  body and its parts' bodies, flat, machining face up, named by path, their
  facts (`lang`/`part`) moved along. CAM goes there. Each part is drawn
  where the layout has it, as in its module document, and its finished body
  moved into place: drawn inside a component whose occurrence is moved,
  Fusion read the profiles in the other space ("the path is tangent to the
  profile") [found 2026-10-14]. Verified on the van's nest: 36 parts, each
  one solid within 0.01 mm of its place, machining face up.

## Pinning

A van is built over weeks; Florian machines a module's sheets in one go,
and now and then a change in between means making parts again [decided
2026-10-16: pinning, after the nest definitions]. Built 2026-10-16
(`pinning.py`, `ledger.py`, stage 3 of `proposals/settings.md`).

- **Marks.** A nest is marked as made, whole or by sheets, with `python -m
  lang.nesting build.py --made kitchen.carcass [SHEET ...]` (a sheet by its
  number, `2`, or `birch 15:2` where two materials of the nest have a sheet
  2) or a click in the preview's nest view, never in the build file. A
  mark reads the nest file, not the build, so it works while the build is
  broken. A sheet marked twice is marked once; marking a nest whole after
  some of its sheets marks the others.
- **The state file**, `made.json` in the build's out folder
  (`out/<build>/`), data the tools write:

  ```json
  {"version": 1,
   "nests": {"kitchen.carcass": {"follows": "", "written": "2026-10-16T09:30:00+02:00",
                                 "sheets": {"birch 15": ["1", "2"]}}},
   "made": {"kitchen.carcass": {"kitchen.left": {"fingerprint": "3f2a9c...",
                                                 "by": "kitchen.carcass birch 15 sheet 1",
                                                 "when": "2026-10-16T17:02:11+02:00"}}}}
  ```

  `nests`: each nest marked, by path: the nest of the build it follows (a
  second nest's, below; "" for the build's own), when its file was written
  (the marks belong to that file, and a file written after its mark is
  refused), and its sheets marked made per material, in the order marked.
  `made`: per nest of the build, each part made, as its fingerprint was,
  what made it (a sheet of the nest or of a second nest, or `fixed`) and
  when. The latest mark or fix of a part wins. To undo a mark, edit this
  file (and the inventory) by hand.
- **Frozen.** A nest with a sheet marked is never nested again and its file
  never written again. Running it (the command, or the preview's button)
  compares its parts' fingerprints with what is made: parts made and
  unchanged are left out; parts changed since they were made, parts of it
  on a sheet not made (or left over), and parts new to it are nested anew
  into its **second nest**, `kitchen.carcass-2`, in the folder
  `kitchen/carcass-2/` beside the first, whose file names the nest it
  follows and why each part is in it. Once that one is marked too, the next
  run writes `kitchen.carcass-3`, and so on: the nest and its second nests
  are its chain, and being made is per chain, so a remake
  (`van.nest("remake", [k["left"]])`) makes a part made in its module's nest
  again. Parts made that the build's nest no longer has are reported as
  gone. A second nest not marked is nested again on every run like any
  nest, and removed when nothing is left for it. A nest of the build
  declared with a second nest's name (`carcass-2` beside `carcass` marked)
  is an error. A nest marked by sheets whose next nest is marked too
  (what it left went there) takes no more marks.
- **Fixed.** A part made and changed since can be marked as fixed by hand
  (a hole added on the bench): `--fixed kitchen.carcass kitchen.left`, or
  the preview's button with the part selected. It counts as made as the
  build has it now, until it changes again. A part not made, gone or
  unchanged is refused.
- **The inventory written back** [Florian, decided in the nesting review]:
  marking sheets as made, and only that (never a plain run), takes the
  pieces on hand they were sawn from out of the ledger and puts their kept
  rests in. A piece comes out of the first entry of its material and size:
  its `count` lowered, or the entry removed with the comment lines right
  above its `[[stock]]` and one blank line around it; a piece the ledger no
  longer has (used elsewhere) is noted, not an error. A rest goes in at
  the end as a `[[stock]]` entry (several of one size on one sheet as one
  with a count) under a comment saying which nest and sheet kept it and
  when. The ledger goes through tomlkit (`ledger.py`, 0.15.2 tried), so
  everything else stays as Florian wrote it: his comments, blank lines and
  spellings (quoted keys, a count in hex, a header's own comment) and the
  order of his entries; only a header spelt `[[ stock ]]` comes back as
  `[[stock]]`. The stock written as an inline array (`stock =
  [{material = ..., size = ...}]`) is edited in place, a rest appended to
  the array with its comment beside it where the array spans lines. A
  ledger that is not TOML or not the ledger's keys is refused and left as
  it was, and the text written is read back and must give exactly the
  stock meant. Where there is none and a rest is kept, it is made beside
  the build file. A sheet marked again changes nothing.
- Not taken as a change: the nest's own values (another margin, another
  bed) and the stock; a nest compares its parts. A part moved to another
  nest of the build is gone from one and new to the other. Two nests not
  yet made may still plan on one offcut (`design/todo.md`): the ledger
  loses a piece only when a nest using it is marked.
- The fuzz tests run random builds edited at random (parts changed, moved,
  added, removed) through random runs, marks and fixes against a plain
  model of what a second nest takes, what is made and what the ledger
  holds, its comments included (`tests/fuzz/pinning.py`).

## Still open

Gone through with Florian on 2026-10-16. Built since, with the nests in
the build (stage 2 of `proposals/settings.md`, 2026-10-16): one source per
nest, the nest file's `bought` (the sheets bought only) and
`settings.seconds` (the limit), a `nest(False)` board named in a nest as
its own blank (but for rips first), the nest's name and time, and the
values a nest reads as settings with the stock on hand in the inventory
(Running it, What is nested); and in stage 3 the parts' fingerprints (The
nest file) and pinning with the inventory written back (Pinning). The
build order of what remains is in that proposal.

### Decided, to build

- **A cut through a through pocket.** The layout step refuses a cut that
  splits a board together with the through pockets and holes made before
  it, as it refuses such a pocket after a cut [decided 2026-10-16]; the
  message names the cut and the pocket. Then the nest fuzz's `KNOWN` and
  the entry in `design/bugs.md` go.
- **Rips first.** Florian rips a sheet along its length first, then cross
  cuts [decided 2026-10-16]: the saw step tries only settings whose first
  cuts are rips (with three stages: rip, cross cut, rip within a piece),
  once measured on the examples what that costs in sheets, rests and cuts.
  Reordering cuts is then needed within that order only, perhaps not at
  all: the simplifying joins pieces within one strip, so a plan may still
  take a cut more than it could.
- **Refill past the cut limit.** Refill may take a sheet a cut or two over
  `max_cuts` when that empties a bought sheet, reported as over like any
  [decided 2026-10-16]. A rest the bed takes as it is needs no cut and is
  offered whatever the sheet's cuts; today a rest is offered only while its
  sheet has two cuts to spare.
- **`nest(False)` boards in the saw plan**: built as own blanks when a
  nest names them (What is nested); rips first comes with the item above.
  A `nest(False)` board no nest names is still only listed as not nested
  (the cut list, below).
- **The cut list**, written by the build as CSV beside `layout.json`, by
  module [decided 2026-10-16]: slats and lips by species, section and
  length, a plain list (not fitted onto stock lengths); `nest(False)` boards
  by material, thickness and length × width (the grain along the length),
  with their operations as a note; manual parts by name; bought hardware,
  counted by what it is. The layout names a mount only by its place
  (`kitchen.drawer1.runners`), so it has to say what each is (product,
  size, article number): a layout version.
- **Manufacturing groups**, for grain matching, their only use [decided
  2026-10-16]: fronts in one face nested as they sit in it, so the grain
  runs on across them. Said in the build, one call over the boards
  [proposed]. The members share material, thickness, the direction of their
  plane, the machining face and the grain, else the group is refused by
  name. A group is one item of several shapes (PackingSolver takes that, no
  bridges), turned only as its grain allows. Its gaps stay as designed: the
  designer makes them wide enough for the smallest bit, and the nest refuses
  a group with a narrower one (the smallest bit a setting until the
  CAM plan's tool data); within a group the checks allow gaps under the
  spacing, and the CAM plan has to know that one pass cuts both edges of
  such a gap. No group attribute for Multi Arrange [decided]. A layout
  version, one bump with the hardware's.
- **Reproducible nests**: the nest runs for its time and keeps the best it
  found, so another run may find another nest, and too short a time costs
  sheets (7 instead of 5 for the examples' 62 parts in 20 s). The nest file
  is the record [decided 2026-10-16]: a nest is made on request only, its
  fingerprints tell whether it still holds, and pinning keeps what was cut.
  `--mode deterministic` stays an option; it split 124 parts into many
  small blanks (Measured, below), so measure it on a module's nest before
  anything else.
- **Compile Layout with a nest file**, clicked through once in Fusion
  (`design/todo.md`).

### With the nests defined in the build

The settings proposal (`proposals/settings.md`, from the CAM review of
2026-10-15) moved nests into the build, built 2026-10-16 (Nests in the
build, Running it): a nest is named where it is defined and the nest file
records the name and when it was written, so its blanks' names
(`<sheet>.<blank>`) hold for good, which the CAM plan names its setups by;
nesting a selection (a material, parts, a module, as when parts are made
again) is declaring such a nest; `use(nest(False))` marks a whole module's
boards as sawn by hand (in the saw plan and on the cut list), not "not in
this nest"; a `nest(False)` board named in a nest is its own blank, which
the CAM plan will machine without its outline; and pinning, built
2026-10-16 as decided (Pinning, above), with the inventory one ledger per
project, as there is one project at a time.

### Dropped [decided 2026-10-16]

- **Offcuts with an outline** (an L-shaped piece) **and defects**: the saw
  plan's rests are rectangles and a blank's waste is a thin frame; a damaged
  offcut goes in as its largest clean rectangle. Both solvers would take
  them (the experiments).
- **Factory-edge trims**: the margin on the bed takes them.
- **Parts larger than the bed**, machined in two setups: for now
  `nest(False)`, sawn by hand, their operations hand work.
- **Irregular parts**, knapsack on one sheet fewer: the parts are mostly
  rectangular.
- **A wider web around weak parts**: 13 to 19 mm holds nothing either; a
  small part is anchored to larger ones by tabs, the CAM plan's work.
- **A rule** that sets `nest(False)` for a whole kind of part
  (`proposals/syntax.md`, item 16).
- **Any angle** (What is nested, Turns).

## Measured

On Florian's Mac (14 cores), sheets 2470 x 1240, bed 2000 x 1000, kerf 4,
spacing and margin 10.

- Blank prices, the examples' 62 parts of birch 15 (9.25 m²), 20 s: by
  their own area 7 sheets before refill, 5 after, 14.8 m² used; by the area
  they take of a sheet 5 sheets without refill, 13.0 m² (2026-10-14, the
  same in two runs). With every part's grain along the sheet, as in the
  experiments: 6 sheets either way, 14.3 against 11.9 m² used.
- Time (2026-10-15, after the fixes the fuzzing brought, which changed the
  solver's polygons slightly): the same 62 parts on 7 sheets in 20 s (12.3
  m² used, 9.2 kept; three runs alike), on 5 in 40 s and with the default
  (37 s): 12.14 m² used, 3.17 kept, the experiments' best. 124 parts (each
  twice), 40 s: 9 sheets, 24.1 m² used.
- `--mode deterministic`: 5 sheets for the 62 parts (12.7 to 13.0 m² used:
  the saw step still varies), 9 for 124 but in 87 blanks and 27.2 m² used;
  about 40 s for both, under a second for a few parts. So the default stays
  the time-bound search.
- The van's 36 parts in three materials, 5 s a material: one sheet of each
  and the offcut, about 16 s with the saw and refill.
- The saw's ten settings run side by side (the solver lets go of the GIL):
  a second for all of them instead of ten.

## The experiments (2026-10-14)

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

