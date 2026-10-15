# Environment: values that flow down the tree

Status: proposed 2026-10-15, nothing built. Florian's idea, raised in the
CAM review of that day (`cam.md`): CAM preferences live in the workshop
file, but a particular setup may need other values, so defaults should flow
down the tree from the top and be overridable at any level, module, nest,
blank, part or setup, as SwiftUI's environment does; and he asked what else
such a mechanism could carry, not only CAM values [Florian]. The design
below is Claude's [proposed]; the questions at the end are his to answer.

The syntax review's item 16 (`syntax.md`) decided against keyword defaults
for the modeling calls (`tool=`, `relief=`, `dogbones=`, `ease=`):
constants, `functools.partial` and the build's helpers do that. The
environment is for another kind of value: not what a part is, but how it is
made and shown, which the workshop knows better than the build file and
which the build file should not have to repeat on every board. Whether item
16's keywords may ride along is question 3.

## The idea

Two trees meet at a part. The source tree: the build, its modules and
cabinets, their scopes, the parts, their operations. The manufacturing
tree: the workshop, a nest, its materials, sheets and blanks, the parts on
them, the setups and operations the plan makes. A value set at a node holds
for everything below it until a node nearer the part sets it again. A
reader (the layout step, the nest, the CAM plan, the emitter, the preview)
asks for a key and gets the nearest value.

Resolution, nearest first [proposed]: an override given for one blank or
setup after nesting; the part; its scope, module, build file; the nest
run's command line; the material in the workshop file; the workshop file;
the package's own defaults. The manufacturing tree's lower levels beat the
source tree because they are deliberate interventions for one run; the
source tree beats the workshop's general values because the build knows its
parts.

## Writing it

In the build, like `check()`: `environment(...)` inside a scope applies to
it, `kitchen.environment(...)` after, `board(...).environment(...)` on a
part as a property modifier: order-free, once per key per node, the same
key twice at one node an error, as placement modifiers are set once. Keys
are keyword arguments of one typed `Environment` (a dataclass), so pyright
and the layout step refuse a key that does not exist, and each key
documents its unit and meaning in one place.

```python
with module("floor", box) as f:
    environment(nest=False)                # ripped on the saw, every board of it
    ...
with cabinet("kitchen", box, front=box.right) as cab:
    environment(appearance="birch", tabs="auto")
    ...
    drawer_box(...)                        # a std helper may set its own: environment(spacing=20)
small.environment(spacing=20, finishing_stepdown=1.0)   # a weak part: a wider web, a thin last pass
```

In the workshop file: a `[cam]` table for the machine's defaults and a
`[cam.material."birch 9"]` table for one material. On the command line,
`--env finishing_stepdown=0.5` for one nest run. For one blank or setup, a
small file beside the nest file keyed by the blank's name, which is brittle
while every nest renumbers its blanks (pinned cut sheets, `nesting.md`)
[open, question 4].

In the layout, each part carries the keys that were set for it anywhere in
the source tree, resolved (a handful, usually none), so the nest and the
plan read a flat dict per part and lay the workshop's values beneath it and
the blank's over it. A tree per module would be smaller; flat is simpler for
every reader [proposed].

## What would flow

- **CAM** (`cam.md`): the template per kind (contour, pocket, bore, drill,
  dogbone, chamfer, groove) and the cutter type (dc or udc), finishing per
  kind, the tab policy (none, auto, all) and the tabs' width, height and
  least count, which edges may take tabs, the breakthrough depth, the
  finishing stepdown, the holding calibration, the tools loaded.
- **Nest** (`nesting.md`): `spacing` and `margin` per part (the wider web
  around weak parts), `nest` for a whole subtree (the floor module, ripped
  on the saw; today `nest(False)` on each of its boards), the turns allowed,
  the grain default (`default_grain` in `scope.py`, the loose end of item
  16: `environment(grain="length")` on a module), the machining face
  (`machine="inner"`).
- **Appearance** (`todo.md`): a color or Fusion appearance per module or
  scope, carried to the preview and the compiled bodies; the grain texture.
- **Checks**: nothing. Tolerances are fixed [decided], and `check()` already
  flows: a module's checks take in its parts.
- **Modeling keywords**: item 16's `tool=`, `relief=`, `dogbones=`, `ease=`
  could be keys read as a keyword's default when it is not given. That was
  decided against as a defaults object, and the environment is the same
  thing by another door, so [open], question 3.
- **Reading it back**: `environment().spacing` in a build or helper, for the
  rare case that geometry depends on it, a helper leaving room for tabs.

## What it buys

- The van floor says once that nothing in it is nested.
- The drawer box helper gives its small parts wider webs and tabs without
  the build knowing.
- 9 mm panels get a thinner last pass through their material's table in the
  workshop file; 18 mm another contour template.
- One blank cut from an odd offcut gets its own breakthrough or template
  without touching the build.
- Preview colors per module come for free.

## Questions for Florian

1. The resolution order, in particular a blank's or setup's override beating
   the part's own setting.
2. The spelling: `environment(...)` as `check()` is written, a keyword on
   `module()` and `cabinet()`, or a `with environment(...):` block, which
   would also scope a value to a few boards without a scope of their own.
3. Whether item 16's modeling keywords ride along, or stay constants and
   partials.
4. Where blank- and setup-level overrides are written, given that every
   nest renumbers its blanks until cut sheets are pinned.
