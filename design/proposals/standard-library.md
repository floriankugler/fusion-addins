# Standard library

Status: added by Florian 2026-10-14, worked out by Claude the same day;
built 2026-10-15 as `lang/std` with `carcass()` and `drawer_box()`
(`design/std.md`, syntax.md items 2 and 3). This file keeps what is still
open. Only the points marked [Florian] are his.

- The core language kept apart from higher-level building blocks, drawer
  boxes among them [Florian]. `lang/core` holds the primitives, and
  `lang/joints` and `lang/hardware` plug into it through two protocols,
  `Joint` for `join(using=)` and `Mountable` for `mount()`, so the core
  knows no joint or hardware type.
- The rule makes the standard library a test of the core: a building block
  that needs an internal shows something the core lacks. Building the first
  two blocks exported `Joint` from `lang`; nothing else was missing.
- Cabinet types for one build stay in that build's repo
  (`build-repo.md`); `lang/std` holds what is reused across builds.
- Lipping was proposed as the first item, but it is a core operation
  (`design/slats.md`): it reads the board's outline, which the public API
  should not grow for it [decided].
- Runs: the core knows only a section that follows a centre line, and
  `lang/std/runs.py` will hold the catalogue helpers for hoses, conduit,
  cable bundles, trunking and heater ducts [Florian, 2026-10-15]. They
  choose sizes and bend radii and add no geometry (`runs.md`).

Still open:

- **Further blocks**: a drawer cabinet (the carcass, the bays and their
  drawers with faces that share the front), a carcass with a shelf on pins,
  a door on hinges with its gap, once a second build needs them.
- **What `carcass()` does not cover**: a top overhanging the sides, a bottom
  raised without a notch, boards of several materials, a divider; each
  waits for a cabinet that needs it rather than a parameter in advance.
- **Atomic blocks**: a join refused inside `carcass()` raises with the
  boards made so far in the scope, as the same lines by hand would; whether
  a block should take them back is open.
