# Settings: values that flow down the build

Status: proposed, nothing built. Florian's idea, raised in the CAM review of
2026-10-15 (`cam.md`) and worked out with him in conversation on 2026-10-15
and 16; this file replaces the `environment.md` of the 15th. Points marked
[Florian] are his, [decided] his decisions, [proposed] Claude's; the
questions at the end are his to answer.

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
- **Cut-sheet pinning is parked** [Florian]: nothing here depends on it.

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

**Namespaces** [proposed, question 5]: keys live with their readers and are
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
    nest("carcass", material=ply15)                      # this module's nests
    nest("drawers", material=ply12).use(cam.tabs("auto"))
    nest("fronts", [front1, front2, front3]).use(nesting.margin(15))

# build.py
with module("van", van.box("Innenraum")):                # the root module, written in place
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
    nest("remake", [k.left, b.front])                    # across modules
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
  when given a function; `@module.body` is the alternative spelling
  (question 1).
- A module's own keywords and its settings are kept apart [proposed,
  question 2]: a parameter (`drawers=4`) changes what the module is and the
  signature documents it; a setting changes how its parts are made.

## Nests in modules

`nest(name, material=...)` or `nest(name, parts)` inside a body registers a
nest on the module, like `check()`; it selects this module's parts of a
material, or the parts named, and takes `.use()` for nest-level values,
another bed among them for a nest cut on another machine.
What no declared nest names falls into one nest per material, so a module
that declares none behaves as today. A nest at the root may name parts of
several modules (remakes). Nests are named by module and nest
(`kitchen.carcass`), their files written under `out/<module>/<nest>/`
[proposed]. The nest command then takes a build file and, optionally, nest
names; `--set` and `--material` go.

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
- The inventory ledger (`inventory.toml` [proposed]): one kind of entry, a
  piece of stock on hand by material and size with a count, full sheets
  and offcuts alike [Florian: no distinction]; the nest reads it, uses what
  is on hand before it buys, and writes usable rests back. What can be
  bought is the material's `size=`, and the nest reports what it bought.
- Outputs: the layout, the nests, the CAM plan, the drawings. None is an
  input; what pinning would change is parked.
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
today, who reads it. Not all at once: `material`, `chamfer_size`, the
nest's and the CAM's keys first, a joint's or a piece of hardware's when a
build wants to standardize it [proposed, question 3]. The inventory is not
a key; tolerances are fixed [decided] and `check()` already flows per
module.

| Domain | Key | Replaces | Default today | Read by | Join |
|---|---|---|---|---|---|
| core | `material` | `board(name, material)` | required | the board, at resolve | per part |
| core | `grain` | `grain()`; `Scope.default_grain`, set by nothing | unset | layout | per part |
| core | `nest` | `nest(bool)` per board | True | nest | per part |
| ops | `chamfer_size` | `chamfer(what, size)` | required (question 4) | `chamfer()` | per part |
| ops | `fillet_radius` | `fillet(what, radius)` | required (question 4) | `fillet()` | per part |
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
| nesting | `keep_across`, `keep_area`, `seconds`, `refill` | `Workshop`, `Options` | 300, 0.25, 0.6 s a part, on | nest | agree |
| nesting | `turns` | none (grain decides) | by grain | nest | per part |
| cam | `contour_template`, `pocket_template`, `bore_template`, `drill_template`, `dogbone_template`, `chamfer_template`, `groove_template`, `cutter` | Auto Setup's dialog defaults | "Kontur 6mm", "Tasche adaptiv 8mm", ...; dc or udc | plan | agree per operation |
| cam | `finish_outer`, `finish_inner`, `finish_pockets` | the finishing checkboxes | off | plan | per part |
| cam | `tabs`, `tab_width`, `tab_height`, `tab_min_count`, `tab_edges` | tabs dropdown, template (5 x 2 mm), min count 4 | "none", 5, 2, 4, any | plan | per part / agree |
| cam | `breakthrough` | `THROUGH_ALLOWANCE` | 0.2 | plan | agree |
| cam | `finishing_stepdown` | template `finishingStepdown` with 0 stepdowns | off | plan | per part |
| cam | `bore_clearance`, `tight_cut_depth`, `big_hole_limit`, `tool_clearance`, `prefer_drilling` | `rules.py` constants | 1, 4, 30, 0.1, False | plan | agree |
| cam | `hold_pressure`, `hold_friction`, `cutting_force`, `hold_safety`, `leak_margin`, `tab_strength` | `holding.HoldingParams`, `TAB_STRENGTH` | 0.5 N/cm², 0.5, 20 N, 1.5, 12 mm, 50 N | plan | agree |
| cam | `stock_thickness` | none | the material's | plan, emitter | per blank (with pinning) |
| appearance | `appearance` | the preview's palette by material (`design/todo.md`) | by material | preview, emitter | per part |
| appearance | `detail` | `proposals/detail-levels.md` | full | preview | per part |

Not settings: `show()` (a rule per board), `machine()` (a face reference,
meaningless above a part), the checks' tolerances, the inventory.

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

## Questions for Florian

1. `@module` with two roles, or `@module.body` for the decorator.
2. A module's own keywords kept apart from its settings, or `drawers=4` a
   setting too.
3. Which keys first; the table proposes `material`, `chamfer_size`, the
   nest's and the CAM's.
4. Keys that replace a required argument (`chamfer_size`, `fillet_radius`):
   a default (1 mm?) or none, so that a chamfer without a size in a chain
   that sets none stays an error.
5. Namespaces by domain as proposed, or one flat namespace.
6. The inventory ledger's format and name (`inventory.toml`, one kind of
   entry, proposed).
