# Settings: values that flow down the build

Status: Florian's idea, raised in the CAM review of 2026-10-15 (`cam.md`)
and worked out with him in conversation on 2026-10-15 and 16; this file
replaces the `environment.md` of the 15th, and its open questions were
settled with him on the 16th (the last section). Points marked [Florian]
are his, [decided] his decisions, [proposed] Claude's.

Built 2026-10-16, stage 1 of the build order below: the mechanism (keys,
bindings, `use()` and `.use()` on scopes, parts and named operations,
`value()`, the chain within the build, set once, freezing as proposed,
provenance in the layout, version 7), the core's keys `material`, `grain`,
`nest` and `chamfer_size`, `@module` with lazy bodies, `module(front=)`
in place of `cabinet()`, and `van.setting()`. They are described in
`design/api.md` (Settings, Modules, Frames) and `design/master.md`; this
file keeps the design and what is still to come. Built otherwise than
written here: the freezing error fires only where the use
would change what was read (a use above the node a read found its value
at is shadowed for that reader and allowed); a key read from its default
is listed in the layout only when the default came from somewhere ("master:
Spalt"); and the root, outside every module, is a node that `use()` there
sets.

Built 2026-10-16, stage 2: nests in the build. `cab.nest(name,
material=...)` and `cab.nest(name, [boards])`, a method on the scope with
`.use()` and `.value()` (the naming decision below), a board in one nest of
its module, a root module's nest naming boards of its modules, and a nest
per material per module for what no declared nest names; the nesting keys
in `lang.nesting` (`bed` without a default, `kerf`, `max_cuts`, `spacing`,
`margin`, `keep_across`, `keep_area`, `seconds`, `rate`, `least_seconds`,
`refill`) read by the nest step from the layout (version 8), the nest's own
value, else its parts', else the default, `agree` or `max` as below; the
inventory, `inventory.toml`, read only; the material's `size=` the sheets
bought; the command taking one build file and nest names, writing
`out/<build>/<module>/<nest>/`; the nest file's name, time, `bought` and
`seconds` (version 2); a `nest(False)` board named in a nest as its own
blank; the preview listing a design's nests. Described in
`design/api.md` (Settings, Nests) and `design/nesting.md`. Built otherwise
or beyond what is written here: a nest by material takes its scope's
boards and its sub-scopes', not a module's inside it (which has nests of
its own); "what no
declared nest names" is any declared nest, so a board a remake names
leaves its module's default nest (with pinning the first nest is frozen
anyway); the nests of one run of the command share the stock on hand in
their order; the `spacing` join grows the solver's polygon of a part that
asks for more than the nest's least by the difference, so between two
parts the larger holds; the `lang.nesting` module `refill` became
`refilling`, so the key keeps its name.

The syntax review's item 16 (`syntax.md`, 2026-10-15) decided against a
defaults object for the modeling calls. Florian reopened it the next day:
the values a build standardizes across its modules (drawer gaps, finger
hole diameters, chamfer sizes), the nest's and the CAM plan's preferences
(spacing, breakthrough, tab width) and the master's parameters are one
kind of thing, set once at the top and overridden where a module, a part or
a nest needs otherwise, as SwiftUI's environment does [Florian]. Item 16's
answer (constants and `functools.partial`) stays right for one-off values;
settings are for what flows.

## Decided in the discussion

- **The name is settings** [decided]: a key is a *setting*, a node *uses* a
  value, code reads a *value*. Not "environment" (framework jargon) and not
  "parameter" (Fusion's user parameters).
- **One mechanism for everything that flows** [Florian]: design standards,
  nesting values and CAM values go down the same chain, from the same
  spelling, in Python. No TOML for manufacturing values.
- **Inputs are Python, outputs are data** [Florian]: the build, its
  standards and the machine are code; the layout, nests, plans and
  drawings are files the tools write. The machine's values (the bed, the
  saw's kerf, the cuts per sheet) are settings like any other, used at the
  root, so there is no workshop file [Florian, 2026-10-16]. One exception:
  the **inventory** of stock on hand is a ledger file, since the nest
  writes usable rests back into it.
- **Nests are declared in the module** that needs them [Florian], with
  settings of their own.
- **`cabinet()` folds into `module(name, box, front=None)`** [decided]: a
  module that opens toward a side is written in its own frame; the word
  "module" stays. (Reverses the two-constructor decision of 2026-10-12;
  `design/api.md` and `scope.py` follow when this is built.)
- **Materials stay plain data** [decided]: a name, a thickness, a sheet
  size. A material is a value, not a node of the chain.
- **The master's parameters become settings** [Florian: "could be very
  useful"], bound in the build's index of the master's names.
- **A module body takes its scope** [Florian: good], and a module is called
  like a constructor and configured with `.use()` on what it returns
  (below).
- **`lang.nesting`, `nest`, and `cab.nest()`** [decided by Florian
  2026-10-16]: the nesting package is `lang.nesting` (`python -m
  lang.nesting`, the keys' namespace, `nesting.margin(15)`), the boards'
  key stays `nest`, and a nest is declared by a method on the scope,
  `cab.nest(name, material=ply15)` or `cab.nest(name, [part, ...])`, so
  there is no top-level `nest()` function to collide with the key.
- **Cut-sheet pinning comes after the nests defined in the build**
  [decided in the nesting review the same day, `design/nesting.md`, Still
  open]: nothing here depends on it; the parts' fingerprints in the nest
  file are its first step.

## The chain

Build (the root module), module, part, nest, sheet, blank, setup, operation
[Florian]. It is not a tree: many parts come together in one nest, so at
the nest it is a directed acyclic graph, and a key the nest needs one value
of (the margin to the blank's edge) is an error when its parts disagree
[Florian]; a key a part sets for itself (a forced tab, a finishing pass)
passes through the nest to that part's own setups and operations.

Resolution is by a fixed precedence of levels, nearest the reader first
[proposed]: operation, setup, blank, sheet, nest, part, module (innermost
scope first), root, then the key's default. For a reader at an operation,
"part" is the part it machines, so one part's values never reach a
neighbour's operations through the shared nest. Each key declares how the
join at the nest is taken: `agree` (one value or an error: `margin`), `max`
(`spacing` between two parts takes the larger), or none, the per-part
pass-through. A node uses a key once; the same key twice at one node is an
error, as placement modifiers are set once.

## Keys

A key is a typed object with a default, defined where the code that reads
it lives, so pyright knows it and the default is the code's own:

```python
# lang/core/ops.py, next to chamfer()
chamfer_size = setting(1.0, "chamfer_size")            # Setting[float], mm

# the build's standards.py
drawer_gap = setting(3.0, "drawer_gap")
finger_hole = setting(30.0, "finger_hole")

# the build's master.py, the index of the master's names
van = master("snapshot.json")
spalt = van.setting("Spalt")       # Setting[float] in mm; its default is the master's value
```

- Keys are objects, not keyword arguments, because a build's own keys
  cannot be typed as keywords of a function the package defines; one
  spelling serves library, build and master keys alike [proposed].
- A key may have **no default**: `material` is one, so a board without a
  material in a chain that sets none is an error, as it is today; only
  inside a scope that uses a material does omission mean "this one"
  [proposed, the guard against a forgotten `ply9` silently becoming 15 mm].
- A key called with a value is a **binding**: `chamfer_size(0.5)`,
  `material(ply15)`, `tabs("auto")`. Bindings are what `use()` takes, any
  number at a time, and what travels in lists.
- A key read after the build (by the nest, the plan, the emitter, the
  preview) holds JSON data, since it travels in the layout; a key read
  during the build (`chamfer_size`, a joint for `carcass()`) may hold any
  object.
- A key may validate its value (`spacing` positive) and names its unit in
  its docstring; everything is mm unless it says otherwise.
- **A keyword is a binding on the node the call makes** [decided
  2026-10-16, Florian's answer to the defaults question]. The core reads a
  key through the chain, and a call's keyword for it uses the key on the
  node it makes first: `board("back", ply9)` is `material(ply9)` on the
  board, `chamfer(what, size=0.5)` is `chamfer_size(0.5)` on the
  operation, `nest(False)` and `grain()` on a board are `nest` and `grain`
  there, `dogbones(tool=8)` is `dogbone_tool(8)` on the operation. So a
  key that replaces a required argument has **no default**: `chamfer(what)`
  in a chain that uses no `chamfer_size` is an error naming the key, as a
  missing `size=` is today, and a build opts into a standard with a line
  that says so. SwiftUI's `.font()` is the same shape, a modifier that sets
  what the view reads.
- **One spelling per key per node** [decided 2026-10-16]: a keyword or
  modifier where a call makes the node, `use()` in a scope, `.use()` on a
  scope, nest, part or operation only for keys that no call there has a
  keyword for (the CAM's, appearance). `left.use(nest(False))` is not
  offered next to `left.nest(False)`.

**Namespaces** [decided 2026-10-16]: keys live with their readers and are
named by domain, so `margin` of the nest and `margin` of a box joint do not
collide and a binding shows its domain where it is written. The language's
own design keys are exported from `lang` (`material`, `grain`, `nest`,
`chamfer_size`); the others come from their packages: `nesting.margin`,
`cam.tabs`, `joints.groove_clearance`, `hardware.hinge_model`,
`std.drawer_floor`. In the layout and in provenance a key's full name is
written (`cam.tab_width`).

## Writing and reading

Like `check()` and `module.check()`: the function acts on the scope whose
`with` block is being written, the method on a node held in hand.

```python
use(material(ply15), chamfer_size(1.0), nesting.spacing(10))   # the current scope, any number
use(*house)                                                     # a list of bindings, unpacked
kitchen.use(chamfer_size(0.5))                                  # a module, from outside
front.use(cam.finishing_stepdown(1.0))                          # a part
left.toekick.use(cam.tabs("none"))                              # a named operation
carcass_nest.use(nesting.margin(15))                            # a nest
gap = value(drawer_gap)                                         # read along the current chain
left.value(cam.tabs)                                            # read from a part's point of view
```

There is no "current part" or "current nest", so for those the method is
the only form; the function keeps a module body free of references to its
own scope object.

**Freezing** [proposed]. Operations compute their geometry on the line
where they are written (`design/api.md`: operations are ordered), so a key
read there is read then. If an ancestor could use another value afterwards,
the chamfers already made would keep the old size while the settings say
otherwise, and nothing would tell. So a key freezes for a subtree once
something in it has read it: a later `use()` above is an error naming the
operation and line that read it. In the normal flow, settings at the top
of a scope, it never fires. Keys nothing reads during the build (`nest`,
`grain`, every nesting and CAM key, appearance) are never frozen, so a part
or module takes them at any time.

## Modules

A module body is a function that takes its scope; the `@module` decorator
makes it callable like a constructor [proposed]:

```python
# modules/kitchen.py
@module
def kitchen(cab: Scope, *, drawers: int = 3) -> None:
    left = board("left").on(cab.left)                    # material from the chain
    back = board("back", ply9).on(cab.back)...           # its own
    left.chamfer(left.outer.front)                       # size = value(chamfer_size), read here
    with scope("drawers"):
        use(material(ply12))
        for i in range(drawers):
            drawer_box(f"drawer{i}", ..., gap=value(drawer_gap))
    cab.nest("carcass", material=ply15)                  # this module's nests
    cab.nest("drawers", material=ply12).use(cam.tabs("auto"))
    cab.nest("fronts", [front1, front2, front3]).use(nesting.margin(15))

# build.py
with module("van", van.box("Innenraum")) as root:        # the root module, written in place
    use(
        material(ply15),
        chamfer_size(1.0),
        drawer_gap(2.5),
        nesting.bed((2000, 1000)),                       # the machine is settings too
        nesting.kerf(4),
        nesting.spacing(10),
        nesting.margin(10),
        cam.breakthrough(0.2),
        cam.tab_width(8),
    )
    k = kitchen(van.box("Küche"), front=kitchen_front, drawers=4).use(chamfer_size(0.5))
    b = bed(van.box("Bett"), front=bed_front).use(material(ply18), spalt(2.0))
    root.nest("remake", [k["left"], b["front"]])         # across modules
    check(fits_sheet)
```

- **Modules resolve lazily, as boards do** [proposed, for Florian's
  `.use()` on the result]. `kitchen(box, front=, drawers=4)` makes a
  module whose body has not run; `.use()` is an order-free modifier, set
  once per key; the body runs on first use: an attribute (`k.left`), an
  export, a nest or check that needs its parts, or the layout step. The
  parent is the scope current at the call, so the chain is fixed then;
  values the parent uses after the call but before the body runs still
  apply. A `.use()` of a key the body has already read is the freezing
  error above. This is the board's own pattern (placement resolved the
  first time a face, the box or the layout asks) applied one level up.
- The decorated body is named after the function (`name=` for a second
  instance), keeps its own keywords (`drawers=4`), and returns the scope,
  so `k.left` and the exports work as before. `with module(...)` stays for
  bodies written in place, such as the root's.
- `module` has two roles, a scope when given a name and a box, a decorator
  when given a function [decided 2026-10-16: one word for one thing; not
  `@module.body`].
- A module's own keywords and its settings are kept apart [decided
  2026-10-16]: a parameter (`drawers=4`) changes what the module is and
  the signature documents it; a setting changes how its parts are made,
  and nobody needs to override `drawers` from the root. The same question
  SwiftUI's environment poses, what goes in and what stays a parameter,
  answered the same way [Florian].

## Nests in modules

`cab.nest(name, material=...)` or `cab.nest(name, parts)` registers a nest
on the module or scope, like `cab.check()`; it selects this module's
boards of a material, or the boards named, and takes `.use()` for
nest-level values, another bed among them for a nest cut on another
machine. What no declared nest names falls into one nest per material per
module, so a module that declares none behaves as before, by module. A
root module's nest may name parts of several modules (remakes). Nests are
named by module and nest (`kitchen.carcass`), their files written under
`out/<build>/<module>/<nest>/`. The nest command takes a build file and,
optionally, nest names; `--material` and the workshop's options went.
Built so (stage 2, above).

## The master's parameters

The snapshot carries every user parameter with its value and unit, read
today as `van.param("Spalt")`, a bare float. `van.setting("Spalt")` in the
build's `master.py` binds it as a setting whose default is the master's
value, in its unit (mm, deg, unitless), so nothing changes until a module
says `use(spalt(2.0))`, and provenance reports "master: Spalt". Change
Parameters in Fusion thus edits the build's standards, and a module can
still deviate without touching the master. Binding is explicit in the
index rather than automatic for every parameter, since pyright cannot type
names invented from a file; a dump of all parameters may exist for
provenance [proposed].

## Inputs, outputs, inventory

- Python: the build, its modules and standards, `master.py`. The machine
  is settings (`nesting.bed`, `nesting.kerf`, `nesting.max_cuts`), used at
  the root and by a nest that goes elsewhere [Florian].
- The inventory ledger (`inventory.toml` [decided; built 2026-10-16, read
  only]): one kind of entry, a piece of stock on hand by material and size
  with a count, full sheets and offcuts alike [Florian: no distinction],
  one per project. The nest
  reads it and uses what is on hand before it buys; the kept rests of a
  nest marked as made go into it and the pieces it used come out (pinning,
  `design/nesting.md`); Florian adds the sheets he buys and deletes by hand
  what is used elsewhere, so the nest rewrites it keeping what he wrote.
  What can be bought is the material's `size=`: a material's sheets are
  always bought in one size, and everything else on hand is an offcut in
  the ledger [decided 2026-10-16]; the nest reports what it bought.
- Outputs: the layout, the nests, the CAM plan, the drawings, the cut list.
  None is an input until a nest is marked as made.
- The layout carries, per part, the keys set along its source chain,
  resolved, each with the node that set it, and the nests declared with
  their values; the nest and the plan lay the nest, sheet, blank and setup
  levels on top. Keys read only during the build need not be written.
- **Provenance** everywhere: the plan's report and the preview, on
  selection, list a part's effective values with where each came from
  ("chamfer_size 0.5: kitchen"), so the implicitness this adds stays
  visible.

## What would flow

Surveyed 2026-10-16 from the code: what a key would replace, its default
today, who reads it. Not all at once [decided 2026-10-16]: first
`material`, `nest` and `grain`, which replace the per-board modifiers and
settle the `default_grain` loose end, and `chamfer_size` as the example of
a key an operation reads; the nest's and the CAM's keys when nesting and
CAM are developed further; a joint's or a piece of hardware's when a build
wants to standardize it. Every key is API surface. The inventory is not a
key; tolerances are fixed [decided] and `check()` already flows per
module.

| Domain | Key | Replaces | Default today | Read by | Join |
|---|---|---|---|---|---|
| core | `material` | `board(name, material)` | required | the board, at resolve | per part |
| core | `grain` | `grain()`; `Scope.default_grain`, set by nothing | unset | layout | per part |
| core | `nest` | `nest(bool)` per board | True | nest | per part |
| ops | `chamfer_size` | `chamfer(what, size)` | none: required unless used above | `chamfer()` | per part |
| ops | `fillet_radius` | `fillet(what, radius)` | none: required unless used above | `fillet()` | per part |
| ops | `dogbone_tool`, `dogbone_relief` | `tool=6, relief=0.1` on `dogbones()`, `tenons()`, `groove()`, `box_joint()` | 6, 0.1 | the operation | per part |
| ops | `cutout_border`, `cutout_around`, `cutout_radius` | `cutout()` keywords from `lib/cutout_patterns` | 20, 20, 8 | `cutout()` | per part |
| ops | `lip_thickness`, `lip_material` | `lip(what, t, material)` | required | `lip()` | per part |
| joints | `groove_clearance`, `groove_chamfer`, `groove_dogbones` | `groove()` keywords | (0, 0), 3, "hidden" | the joint | per part |
| joints | `tenon_clearance`, `tenon_extra_depth`, `tenon_dogbones` | `tenons()` keywords | (0.1, 0.1), 0.5, "corner" | the joint | per part |
| joints | `box_joint_fingers`, `box_joint_clearance` | `box_joint()` keywords | 5, (0, 0) | the joint | per part |
| joints | `half_lap_clearance` | `half_lap(clearance=)` | 0 | the joint | per part |
| joints | `clamex_model`, `cabineo_model`, `screw_diameter`, `station_end` | factory defaults, `lib/stations` | "P-10", "8", `SCREW_DIAMETER`, per joint | the joint | per part |
| hardware | per factory: `hinge_model`, `hinge_count`, `hinge_end`, `hinge_pilot`; likewise latch, ball catch, hatch hinge, sliding bracket, slides | the factories' keywords | "Blum CLIP top 110 Thin +0", 2, ...; "GN 450"; "Pacofix PF-L-R"; opening 107 | the hardware | per part |
| std | `drawer_gap`, `drawer_floor`, `carcass_back`, `carcass_toekick`, `carcass_joins` | `carcass()`, `drawer_box()` keywords | ply9, (60, 100), ... | the helper | per part |
| nesting | `bed`, `kerf`, `max_cuts` | `Workshop.bed`, `.kerf`, `.max_cuts` | required, 4, 5 | nest | agree |
| nesting | `spacing` | `Workshop.spacing` | 10 | nest | max |
| nesting | `margin` | `Workshop.margin` | 10 | nest | agree |
| nesting | `keep_across`, `keep_area`, `seconds`, `rate`, `least_seconds`, `refill` | `Workshop`, `Options`, `nest_seconds` | 300, 0.25, 40, 0.6 s a part, 5, on | nest | agree |
| nesting | `turns` | none (grain decides) | by grain | nest | per part |
| cam | `contour_template`, `pocket_template`, `bore_template`, `drill_template`, `dogbone_template`, `chamfer_template`, `groove_template`, `cutter` | Auto Setup's dialog defaults | "Kontur 6mm", "Tasche adaptiv 8mm", ...; dc or udc | plan | agree per operation |
| cam | `finish_outer`, `finish_inner`, `finish_pockets` | the finishing checkboxes | off | plan | per part |
| cam | `tabs`, `tab_width`, `tab_height`, `tab_min_count`, `tab_edges` | tabs dropdown, template (5 x 2 mm), min count 4 | "none", 5, 2, 4, any | plan | per part / agree |
| cam | `breakthrough` | `THROUGH_ALLOWANCE` | 0.2 | plan | agree |
| cam | `finishing_stepdown` | template `finishingStepdown` with 0 stepdowns | off | plan | per part |
| cam | `bore_clearance`, `tight_cut_depth`, `big_hole_limit`, `tool_clearance`, `prefer_drilling` | `rules.py` constants | 1, 4, 30, 0.1, False | plan | agree |
| cam | `hold_pressure`, `hold_friction`, `cutting_force`, `hold_safety`, `leak_margin`, `tab_strength` | `holding.HoldingParams`, `TAB_STRENGTH` | 0.5 N/cm², 0.5, 20 N, 1.5, 12 mm, 50 N | plan | agree |
| cam | `stock_thickness` | none | the material's | plan, emitter | per blank (with pinning) |
| cam | `smallest_cutter` | none ("a workshop value until the CAM plan's tool data", `design/nesting.md`, groups) | the templates' narrowest | nest (a group's gaps), checks | agree |
| appearance | `appearance` | the preview's palette by material (`design/todo.md`) | by material | preview, emitter | per part |
| appearance | `detail` | `proposals/detail-levels.md` | full | preview | per part |

Not settings: `show()` (a rule per board), `machine()` (a face reference,
meaningless above a part), the checks' tolerances, the inventory, and a
manufacturing group (`design/nesting.md`), which is a relation between
boards, said as one call over them.

## What it buys

- A carcass stops repeating `ply15`; the root can switch a build to 18 mm
  for a what-if.
- The van floor says once that nothing in it is nested.
- The drawer boxes' nest says once that its small parts may be tabbed.
- 9 mm panels get a thinner last pass through their module; a show front a
  finishing pass of its own.
- A standard chamfer, drawer gap or finger hole is written once and read
  by every helper, and one module deviates in one line.
- The master's Change Parameters dialog edits the build's standards.
- Every effective value says where it came from.

## Settled 2026-10-16

The questions the first draft left open, and Florian's answers [decided]:

1. The decorator is `@module`, the same word as the scope.
2. A module's own keywords (`drawers=4`) stay keywords, apart from settings.
3. First keys: `material`, `nest`, `grain`, and `chamfer_size` as the
   example of a key an operation reads; nesting and CAM keys once those are
   further along; joints and hardware when a build asks.
4. No defaults for keys that replace a required argument; a call's keyword
   is a binding on the node it makes, and the core reads the key (Keys,
   above).
5. Namespaces by domain.
6. `inventory.toml`, one kind of entry.
7. One spelling per key per node: `nest()`, `grain()` and the material
   argument stay the part-level spelling; `.use()` on a part is for keys
   without a keyword.

7. From the merge with the nesting review (`design/nesting.md`): the
   workshop file allowed several `[[sheet]]` sizes per material, as many as
   needed. Florian buys a material's sheets in one size, the material's
   `size=`; the rest is offcuts, which the ledger holds [decided
   2026-10-16].

## Build order

Coordinated with the nesting review's "Still open" (`design/nesting.md`,
2026-10-16), whose implementation Florian paused until the settings are
built [Florian]. Each stage is a session of its own [proposed].

1. **Settings, the mechanism**: `setting`, bindings, `use`, `.use`,
   `value`, the chain within the build, freezing, provenance in the layout
   (a layout version); `material`, `nest`, `grain` and `chamfer_size`;
   `@module` with lazy modules and `.use()`, `module(front=)` taking over
   from `cabinet()`; `van.setting()` in the master index.
2. **Nests in the build** [built 2026-10-16]: `cab.nest()` in a module
   with `.use()`; the nesting keys (bed, kerf, cuts per sheet, spacing,
   margin, keep, time) replacing the workshop file; the inventory ledger
   replacing its stock; one source per nest (the merge of build files and
   the `van:` prefixes go); the nest's name and time in the nest file; a
   `nest(False)` board named in a nest as its own blank; the command taking
   a build file and nest names.
3. **Fingerprints and pinning**: the parts' hashes in the nest file (its
   version 3), the state file marking nests as made, re-nesting changed
   parts beside a frozen nest, rests into the ledger.
4. **The CAM plan** (`cam.md`) with its keys, including `smallest_cutter`
   and a group's shared gaps.

Independent of the settings, from the nesting review, in their own
sessions whenever Florian wants them: the layout refusing a cut through a
through pocket; rips first in the saw plan; refill past the cut limit;
the cut list as CSV with the hardware's product data (a layout version,
best taken together with stage 1's); manufacturing groups (with that same
version); Compile Layout clicked through with a nest file.
