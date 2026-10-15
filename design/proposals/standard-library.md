# Standard library

Status: added by Florian 2026-10-14, worked out by Claude the same day;
nothing built. Only the points marked [Florian] are his.

The core language kept apart from higher-level building blocks, drawer boxes
among them [Florian]. Today `lang/core` holds the primitives, and
`lang/joints` and `lang/hardware` plug into it through two protocols, `Joint`
for `join(using=)` and `Mountable` for `mount()`, so the core knows no joint
or hardware type. The drawer box and the drawer cabinet are functions in
`examples/drawer_cabinet.py` ("later the catalog", from the review of
2026-10-12).

Proposed:

- `lang/std/` holds building blocks written only with the public API
  (`from lang import *`), each with a test and an example: the drawer box
  (box joints, grooved floor, slide machining, moved from
  `examples/drawer_cabinet.py`), the drawer cabinet, a carcass with a choice
  of connectors. It replaces the `catalog/` folder the first draft planned
  for Florian's cabinet functions.
- The rule makes the standard library a test of the core: a building block
  that needs an internal shows something the core lacks. A test can enforce
  the rule by checking the imports.
- Joints and hardware stay in the language. They work out geometry from
  catalogue data that the core cannot express, and they plug in through the
  protocols. The standard library composes and adds no geometry of its own.
- Cabinet types for one build stay in that build's repo
  (`build-repo.md`); `lang/std` holds what is reused across builds.
- Decided with the syntax review (`syntax.md` items 2 and 3, 2026-10-15):
  a carcass block is the first item, ahead of the drawer box (`left, right,
  bottom, top, back = carcass(cab, ply15, back=ply9, joins=cabineo(count=3))`),
  since every cabinet starts with one; and the drawer box hides the slide's
  three calls (`drawer_box()`, `machine_box()`, `mount()`), which stay as
  they are in the core.
- Lipping was proposed as the first item, but it is a core operation
  (`design/slats.md`): it reads the board's outline, which the public API should
  not grow for it [decided]. The drawer box is the first item instead.
- Runs: the core knows only a section that follows a centre line, and
  `lang/std/runs.py` holds the catalogue helpers for hoses, conduit, cable
  bundles, trunking and heater ducts [Florian, 2026-10-15]. They choose
  sizes and bend radii and add no geometry (`runs.md`).
