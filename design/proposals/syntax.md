# Syntax review

Status: Claude's review of the language's syntax as built and as proposed,
2026-10-15, gone through with Florian item by item the same day and built
the same day (commits f6e25342 to the merge of the three worker branches
and the standard library). The items decided for are built and have left
this file for the table below, which says where each is described now;
the two decided against stay here in full with the reason, so they are not
proposed again; item 16's loose end is in `design/todo.md`.

The core reads well: relations instead of numbers, operations reachable as
attributes, typed anchors, `front=` for cabinets. The items are at the
edges: one trap, ceremony that repeats in every build file, and
inconsistencies. The proposals' spellings for bevels, chamfers at angles,
tilted boards and mitres follow what exists (`bevel(what, angle, long=)`
matches `chamfer(what, size)`, `chamfer(corner, front=30, left=80)` matches
`clip(top=, back=)`, `trim(a, b, name=)` names a straight cut that keeps one
side) and are not listed.

## Built

| Item | Decision | Described in |
|---|---|---|
| 1 | `+`/`-` on a side or face is refused, pointing to `into()` and `gap()`; bare positions keep their arithmetic | `design/placement.md`, `design/api.md` |
| 2 | A carcass block, the standard library's first item | `design/std.md` |
| 3 | The standard library's drawer box hides the slide's three calls, which stay in the core | `design/std.md` |
| 4 | `no_interference` runs for every module, `uncheck()` turns it off; `fits_sheet` stays opt-in | `design/checks.md` |
| 5 | `shrunk(n)` and `grown(n)` take an amount for all sides, keywords override it | `design/api.md` |
| 6 | `anchor.center(pos)` centres a shape on a position along the unnamed axis | `design/operations.md`, `design/api.md` |
| 7 | `to(face, leave=3)` instead of a signed offset | `design/operations.md` |
| 9 | Lowercase hardware factories, the classes kept for typing | `design/hardware.md`, `design/api.md` |
| 10 | American spelling: `centers=`, `miter()`, `miters.md` | `design/operations.md` |
| 11 | `thickness` on materials as on boards; `t=` stays the constructor keyword | `design/slats.md` |
| 12 | `sides=` takes any sequence of two | `design/hardware.md` |
| 13 | `-` and `+` on shapes, the methods kept | `design/operations.md`, `design/api.md` |
| 14 | Modules export their openings as the runs' ports | `design/proposals/runs.md` |
| 15 | Bare references as stops in `path()`, `via()` for diagonals and `bend_r=` | `design/proposals/runs.md` |

## 8. `mid(a, b)`

`(bottom.top + top.bottom) / 2` is the weighted-mix algebra at work; a
`mid(a, b)` helper reads better in a placement line. The algebra stays for
everything else.

Decision: [decided] No. `(a + b) / 2` is plain Python and one name fewer to learn; no `mid()`.

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
