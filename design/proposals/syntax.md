# Syntax review

Status: Claude's review of the language's syntax as built and as proposed,
2026-10-15, gone through with Florian item by item the same day. Each item
carries his decision. An item decided for leaves this file when it is built
(the topic file then describes it, or `design/todo.md` lists it); an item
decided against stays here with the reason, so it is not proposed again.

The core reads well: relations instead of numbers, operations reachable as
attributes, typed anchors, `front=` for cabinets. The items are at the
edges: one trap, ceremony that repeats in every build file, and
inconsistencies. The proposals' spellings for bevels, chamfers at angles,
tilted boards and mitres follow what exists (`bevel(what, angle, long=)`
matches `chamfer(what, size)`, `chamfer(corner, front=30, left=80)` matches
`clip(top=, back=)`, `trim(a, b, name=)` names a straight cut that keeps one
side) and are not listed.

## 1. `+` and `-` on sides and faces

`cab.front + 40` moves along the world axis and keeps the side's direction
(`Side.__add__` in `lang/core/refs.py`), so inside a cabinet function it
moves inward or outward depending on `front=`. The examples never trip
because every `+` inside a cabinet is on the vertical axis (`bottom.top +
100`, `unit.bottom + 60`), and the module-level ones (`f.front + x`,
`panel.front + 40`) work only because the default frame has front at -x. A
cabinet placed with `front=box.front`, or a van with another `set_frame()`,
silently flips them, which undoes the point of a cabinet written once and
placed anywhere.

Proposed: a side or face plus a number is an error pointing to `into()` and
`gap()`. Bare positions (master planes, `spread()` results, `center()`) keep
their arithmetic, since they carry no direction to be wrong about.
`spread(bottom.top.gap(100), top.bottom.gap(100), pitch=32)` reads as well
and holds in every frame.

Decision: [decided] Refuse it. A side or face plus a number is an error pointing to `into()` and `gap()`; bare positions keep their arithmetic. The examples change to `gap()` and `into()` on the vertical axis too.

## 2. A carcass block

The five carcass boards, each `.on(cab.x).between(left, right, ...)`, and
their two joins are the same eight lines in seven of the ten examples.
`standard-library.md` lists the drawer box as the first item; a carcass
block would come first, since every cabinet starts with one:
`left, right, bottom, top, back = carcass(cab, ply15, back=ply9,
joins=cabineo(count=3))`.

Decision: [decided] Yes, the first item of the standard library, ahead of the drawer box.

## 3. The drawer slide's three calls

`slide.drawer_box()`, `slide.machine_box()` and `d.mount(slide, ...)` are
three APIs for one slide, and `front=face.back` is given to two of them.
Proposed: the box `drawer_box()` returns remembers its front, so the mount
needs only `sides=`. A standard drawer box would hide most of this anyway.

Decision: [decided] Leave it to the standard library's drawer box, which hides the three calls; the core's slide API stays as it is.

## 4. Checks by default

`check(no_interference, fits_sheet)` closes every module by hand. Proposed:
both run for every module unless turned off explicitly; `check()` adds
`inside_box` and `inside()`.

Decision: [decided] Only `no_interference` runs by default, for every module, with an explicit way to turn it off. `fits_sheet` stays opt-in: the nest refuses oversized parts anyway, and some parts are sawn from bigger stock by hand.

## 5. `shrunk()` and `grown()` for all sides at once

`shrunk(left=GAP / 2, right=GAP / 2, top=GAP / 2, bottom=GAP / 2)` wants a
positional all-sides argument, as `Board.inset(n)` has, with the keywords
overriding it: `shrunk(GAP / 2)`, `grown(0.5, front=0)`.

Decision: [decided] Yes, a positional amount for all sides, with the condition that `shrunk(front=20)` keeps shrinking the front only (the positional amount defaults to 0, so keywords alone work as they do now). Same on `grown()`.

## 6. Centring a shape on a position

`at=` puts a shape's matching side on a position, so a notch centred on a
line is `left(line - 7)` (`design/todo.md`, seen in `runs.md`). The unnamed
axis is centred by default already; proposed: the anchor takes a position
for it, `b.front.top.center(line)`, the shape centred on `line` along the
axis the anchor leaves unnamed.

Decision: [decided] `anchor.center(pos)`: `b.front.top.center(line)` puts the shape's middle on `line` along the axis the anchor has not named. One method on `Anchor` (a position only, never a number); the operations stay as they are. Replaces the todo entry.

## 7. `to(face, -3)`

Only zero or negative offsets are legal, so the sign is ceremony. Proposed:
`to(side.outer, leave=3)`, which says what the number does and cannot be
given the wrong way round.

Decision: [decided] `to(face, leave=3)`; `to(face)` alone reaches the face. The signed offset goes.

## 8. `mid(a, b)`

`(bottom.top + top.bottom) / 2` is the weighted-mix algebra at work; a
`mid(a, b)` helper reads better in a placement line. The algebra stays for
everything else.

Decision: [decided] No. `(a + b) / 2` is plain Python and one name fewer to learn; no `mid()`.

## 9. Factories for hardware

Parts, joints, materials and the proposed runs are lowercase factories
(`board`, `cabineo`, `sheet_material`, `run`); hardware is CamelCase classes
(`DrawerSlide`, `ConcealedHinge`, `BallCatch`). In a build file both are
settings handed to a relation. Proposed: lowercase factories for hardware
too (`drawer_slide("Dynapro 40", nl=450)`, `hinge(...)`, `hatch_hinge(...)`,
`ball_catch()`, `latch(...)`, `sliding_bracket()`), the classes kept for
typing.

Decision: [decided] Lowercase factories for hardware: `drawer_slide()`, `hinge()`, `hatch_hinge()`, `ball_catch()`, `latch()`, `sliding_bracket()`; the classes stay for typing, as `Board` does behind `board()`.

## 10. Spelling

The API says `center` everywhere, but slots take `centres=`, and the mitre
proposal spells `miter()` in code and `mitres.md` on disk. Proposed: one
spelling; American is already the majority.

Decision: [decided] American throughout: `centers=` on slots, `miter()` and `miters.md` for the proposal.

## 11. Thickness

A material says `ply15.t`, a board says `.thickness`, and `lip()` calls its
second argument `t`. Proposed: one name on both.

Decision: [decided] `thickness` on both: `ply15.thickness` joins `board.thickness` and `.t` goes; `t=` stays the constructor keyword and `lip()`'s argument.

## 12. Lists and tuples

`sides=(left, right)` must be a tuple, while `frame=[left, right]`,
`keep=[shelf]`, `at=[...]` and `chamfer([a, b], 1)` take lists. A reader
cannot know which is which. Proposed: accept any sequence and check the
count at run time.

Decision: [decided] Accept any sequence everywhere, list or tuple; where exactly two are needed (`sides=`), the count is checked when the build runs.

## 13. Shape operators

Shapes compose through `.union()` and `.difference()` only. `rect(...) -
circle(...)` is what shapely and CadQuery users expect and reads better.
The "no operators" rule in `design/api.md` was about placement, where
`left @ cab.left` is cryptic; 2D booleans are conventional.

Decision: [decided] Operators `-` (take away) and `+` (add material) on shapes, as build123d spells them; the methods stay.

## 14. Parts named after directions, reached from the van level

`kitchen["bottom"].cable` is what the runs proposal needs most, since the
boards with holes are bottoms, backs and tops. Proposed: the module exports
its openings (`cab.export("cable", bottom.cable)`), the existing mechanism,
so the van level reads `kitchen.cable`; that gives runs their ports without
a ports feature, and the examples write it that way.

Decision: [decided] The module exports its openings (`cab.export("cable", bottom.cable)`) and the van level reads `kitchen.cable`; the runs proposal's examples are written that way. `cab["bottom"]` stays as the escape.

## 15. Runs: `via()` optional

`.path(start, via(...), ..., end)` reads well, and `passage` is a good
word. Proposed: a bare reference in `path()` is a one-axis stop, an anchor
or opening a three-axis point, and `via()` stays for `bend_r=`.

Decision: [decided] Bare references allowed in `path()`: a bare reference is a one-axis stop, an anchor or opening a three-axis point; `via()` stays for a per-corner `bend_r=` and for two or three references in one stop.

## 16. Defaults without rules

Three proposals lean on "a project rule" that does not exist: the bent
board's `ease=`, "1 mm on the outline of every show face"
(`design/operations.md`, Chamfers), `nest(False)` for a whole kind of part
(`proposals/nesting.md`). Joinery rules were dropped [decided]. Proposed
first: a scope-level defaults object, `cabinet(name, box, front=...,
defaults=Defaults(chamfer=1, tool=6, ease=0.5))`.

Worked through with Florian: the keywords several calls share by name and a
project sets once are few. `tool=` and `relief=` (the same literal in seven
places: `dogbones()`, `tenons()`, `half_lap()`, `groove()`, `box_joint()`),
`dogbones=` on the three joints that take it, `grain` (`scope.default_grain`
exists in the code, but nothing in the API sets it) and the proposed `ease`.
Clearances and pilot holes differ in meaning and shape per joint and per
hardware, so no one key holds them. A `chamfer=1` default would chamfer the
rim of every slot, hole and pocket, which nobody wants; the chamfer rule
meant is an operation added to every board's show-face outline at the end,
after cuts and lips, with an opt-out, and `nest(False)` by kind is a
predicate over parts: both are rules, not keyword defaults. Python already
gives constants at the top of the build file (`GAP = 3`, as the examples
do), `functools.partial(tenons, tool=8, dogbones="hidden")` and the build's
own helpers, at no cost in implicitness.

Decision: [decided] Nothing new. Project-wide values are constants,
`functools.partial` and the build's own helpers; no defaults object and no
rules. `ease` becomes a keyword on `bend()` with a package default
(`bent-boards.md`); show-face chamfers and `nest(False)` stay explicit per
board, or in a helper the build writes. Loose end [open]: `default_grain`
in `lang/core/scope.py` is set by nothing; either drop it or give
`module()` and `cabinet()` a `grain=`.
