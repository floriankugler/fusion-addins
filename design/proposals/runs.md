# Runs: hoses, cables, ducts and keep-outs

Status: proposed, nothing built. Wanted by Florian (water hoses, cable runs,
ducts, keep-outs; 2026-10-13). The design is Claude's: first drafted with
the plan (2026-10-09) and worked out in detail on 2026-10-15. Florian's
points from 2026-10-15 are marked [Florian]:

- a run plans and is checked, and cuts nothing: the boards keep their
  openings as their own operations;
- runs are planned at the van level, as the last step that checks what the
  modules planned (he first preferred the module level, while runs still
  cut their openings);
- a module may also plan its own runs, to be checked on its own; each hose
  is planned in one place;
- van-level runs are checked when the van asks, with `check()` in
  `van.py`, as modules ask for theirs;
- modules are designed on their own and put together later;
- the core knows only a section that follows a centre line, round or
  rectangular, with helpers for hoses, conduit and so on in the standard
  library;
- a keep-out is a material, not an API of its own;
- hoses bend; cable conduits turn at 90 degrees, at their elbows, which the
  standard library's helpers say.
- a run needs 10 mm of room on each side in an opening, unless its material
  says otherwise;
- a run's section and bend radius belong to its material, since it is bought
  by size;
- `Face.gap()` and `Face.into()` keep the face's side, as a box side's do.

Every other point is [proposed] unless marked otherwise. The questions at
the end are his to answer.

The syntax review of 2026-10-15 (`syntax.md`) is written in: bare
references as stops (item 15), modules exporting their openings as the
runs' ports (item 14), `center(line)` in the notch example (item 6),
`into()` for a box side moved (item 1) and `no_interference` running for
every module (item 4).

Hoses, cables and heater ducts are planned alongside the furniture, so that
there is room for them, they are organised, and the boards have the holes
they need. By hand that is a 3D sketch of the centre line, a section
swept along it, and holes cut wherever it passes a board. In the language a
run is a primitive. [decided as a need]

## The core and the standard library

The core knows one thing: a **run** is a section that follows a centre line
[Florian]. It has no kinds. Hoses, conduits, trunking and heater ducts are
catalogue helpers in `lang/std/runs.py` (`standard-library.md`), written on
the public API only.

The core cannot leave everything about the section to the helpers, because
the geometry depends on it: the checks, the preview's mesh and Fusion's
feature. But it depends on five generic facts, all held by the run's
material (the fourth by the run itself), not on any kind:

- **The section's shape.** It is round (`d=`) or rectangular
  (`section=(w, h)`), and nothing else is needed [Florian].
- **How it turns.** Its corners bend at a radius (`bend_r`), or turn square
  and mitred where the radius is 0.
- **Which angles it turns at.** A hose bends at any angle; a cable conduit
  turns only at 90 degrees, at its elbows [Florian]. That is `angles=` on
  the material: none for any angle, `(90,)` for elbows of 90 degrees. Each
  corner of such a material is a fitting.
- **Which way a rectangular section faces.** That is the run's `.flat()`.
- **Whether it is bought.** A run of a keep-out material keeps room free:
  it is drawn translucent and is not on the cut list.

So the helpers choose sizes, radii and angles, and add no geometry of
their own, which is the standard library's rule [Florian]:

```python
# lang/std/runs.py: catalogue helpers, each returning a material
pe_hose(12)              # run_material("PE", d=12, bend_r=60): bends at any angle
conduit(20)              # run_material("conduit", d=20, bend_r=..., angles=(90,)): 90 degree elbows,
                         # bend_r the elbow's radius from the maker's table
cables(10)               # a loose bundle of 12 V cables
trunking(40, 25)         # rectangular, square corners at 90 degrees
heater_duct(75)
```

The numbers in the helpers' tables come from the products Florian uses
(question 1).

## What a run is

- `run(name, material)` is the one constructor [Florian]. A keep-out is a
  run of a keep-out material.
- A run is not a board: it has no outline, faces or operations, and takes
  no joins or hardware. It changes no board either ("Boards keep their
  openings").
- A run registers under its name where it is written: at the van level,
  outside every module, or in a module ("Where runs are written"). A name
  that a part or scope already has there is an error.
- Its modifiers are `.path(...)` and, for a rectangular section,
  `.flat(...)`, each given once (both below).

## Materials

As with sheets and slats, the stock is a material, defined once next to the
others in `stock.py`, through the helpers or in the core's own spelling:

```python
pe12 = pe_hose(12)
cable10 = run_material("cables", d=10, bend_r=15, gap=2)  # clipped into a channel, so 2 will do
trunk = trunking(40, 25)
channel = keepout_material("channel", section=(60, 40))  # room for cables to come
```

- `run_material(name, d= | section=(w, h), bend_r=0, angles=None,
  gap=10)`.
  - `bend_r` is the smallest radius of the centre line in a bend; 0 turns
    square.
  - `angles` are the only angles its corners may turn at, its fittings',
    or None for any.
  - `gap` is the room it needs on each side in the openings it passes,
    which the checks hold it to: 10 mm unless the material says otherwise
    [Florian].
  - `material.passage` is its section grown by `gap` all round, the size of
    a hole for it.
- **It is `gap`, not `clearance`,** because half laps and tenons take their
  `clearance=` in total, half on each side. A run's room is given per side
  [Florian], as `gap()` moves a face away from a part.
- `keepout_material(name, d= | section=(w, h), bend_r=0, gap=10)` is
  the same, for room kept free rather than something bought [Florian]. It
  is the same type, with the difference recorded, so a run, its path and
  its checks are the same code either way.
- A rectangular section's two sizes come in either order. The larger is the
  width of its wide faces, as with a slat.
- Labels: `PE Ø12`, `trunking 40x25`, `channel 60x40 (kept free)`.
- The section and the bend radius belong to the material, unlike a slat's
  section, whose material is a species only [decided for slats]: a hose or
  a trunking is bought by its size, and its bend radius goes with that size
  [Florian].

## The path

`.path(start, *stops)` takes a start, then stops. The centre line runs
straight from each one to the next, and its corners are bends or square
(see "Corners"). Routing is by hand: the build file says where the run goes,
and the language checks it. Automatic routing is out of scope [from the
first draft].

### Points

A point fixes the centre line on all three axes:

- `point(a, b, c)` takes three positions on three different axes, in any
  order: `point(floor_front + 100, ground.center("width"), floor_level +
  20)`. Each position knows its axis, so no axis is named.
- A point on a face is the anchor that `at=` takes:
  `back.outer.bottom(150).right(60)`.
- An opening means its centre: a named hole such as `top.tap`, or a named
  pocket through, also one a module exports (`kitchen.cable`). As the start
  or the end of a path, it lies on the face the opening was made from; in
  the middle, the run passes through it.
- Later, a connection on an external component, such as a pump's outlet
  (see `design/todo.md`).

Points on faces and openings are passed square: the leg at such a point
runs along the board's thickness axis, which is how a hose goes through a
hole.

- **Arriving.** The run turns onto that line where it already is. The
  corner before the point takes the point's two other coordinates and keeps
  its own coordinate along the axis. So a hose ends at the tap hole from
  below just by naming `top.tap`.
- **Leaving.** When such a point is the start, or an opening the run
  passes in the middle, the next stop must name that axis, because it says
  how far the leg goes.

Any other point is reached by a straight leg from the stop before, which is
a diagonal if more than one coordinate changes.

### Stops

A stop is a reference, bare, or `via(...)` with one, two or three
references, each on a different axis [decided by Florian, 2026-10-15,
syntax.md item 15: `via()` had wrapped every stop]. Each reference says
where the centre line goes on its axis, and the other coordinates carry over
from the stop before [from the first draft]. A bare reference makes a leg
along one axis, which is nearly every leg of a real run, so a path is mostly
references and points; `via()` is for two or three references in one stop,
a diagonal, and for a corner's own `bend_r=` (see "Corners"). The axis comes
from the reference, just as `center()` takes its axis from the position it
is given. That settles the first draft's open point: `via(z=...)` named
world axes, which build files avoid.

What a reference positions follows how `on()` and `center()` place a board:

- **A box side** (`cab.bottom`, `cab.back.into(30)`): the run lies on it,
  inside the box.
- **A part's face** (`panel.bottom`, `back.inner.gap(15)`): the run lies on
  it, outside the part.
- **A part**, or a part moved by `gap()` or `into()` (`left.gap(30)`): its
  face toward where the run comes from, just as a part given as a
  `between()` limit means its face toward the board.
- **`center(pos)`**: the centre line lies on the position.
- **A bare position** (a plane of the master, or a sum of positions) is an
  error. It does not say which side the run lies on; `center()` puts the
  centre line on it.

"Lies on" means the run's surface touches the reference: its centre line is
half the section away from it, on that side. A run lying on a face that then
moves along the face keeps lying on it, because the coordinate carries over.
So following a panel needs no word of its own, and the first draft's
`along(face, gap)` goes.

This needs one small change to the core: `Face.gap(n)` and `Face.into(n)`
keep the face's side, as a box side's `gap()` and `into()` do since
2026-10-14 [Florian, 2026-10-15]. Then `back.inner.gap(15)` is a plane 15
in front of the back that a run lies on, and so can a board's `on()`,
without `toward=`. Today they return bare positions. The change stands on
its own and can be made before runs.

Errors:

- two references on one axis;
- a stop that does not move the run;
- a leg that runs back along the leg before it (a turn of 180 degrees);
- a part as a reference when the run's centre line lies within the part's
  extent on that axis, since it is not clear which face is meant.

### Corners

- Where the material has a `bend_r`, the corners are bends of the centre
  line at that radius. `via(..., bend_r=120)` gives one corner a wider
  bend; a bend tighter than the material's is an error.
- A bend takes up `bend_r × tan(angle / 2)` of the legs on either side. A
  leg too short for its bends is an error that names the leg and the room
  it lacks: "kitchen.cold: the leg up to 40 under the top is 46 long; its
  bend needs 60".
- A start or an end has no bend, so the first and last legs need room for
  one bend only.
- Where `bend_r` is 0 the corners are square: the section runs on to the
  outer corner, mitred.
- Where the material has `angles`, every corner must turn at one of them,
  within 0.1 degrees, or it is an error naming the corner and its angle:
  "cable_rear: the corner under the kitchen's bottom turns 84.3 degrees;
  conduit 20 turns only at 90". Each such corner is a fitting, bent at the
  material's `bend_r`, and `via(..., bend_r=)` cannot change it.

### Rectangular sections lie flat

`.flat(ref)` says which way a rectangular section's wide faces face: along
the axis of `ref`, which is a box side, a part's face or a direction. So
trunking screwed to the wall behind a cabinet is
`run("cables", trunk).flat(cab.back)`.

- Every leg must lie square to that axis, since a leg along it would twist
  the section; such a leg is an error.
- A rectangular section without `flat()` is an error, unless it is square.
- `flat()` on a round section is an error.

## Boards keep their openings

A run changes no board. It plans where a hose or a cable goes, and it is
checked against everything else; the openings it needs are the boards' own
operations [Florian]. That keeps each board's operations in the
order they are written. A cutout pattern made after the hole for a hose
keeps material around it, as around any hole, and `dogbones()` relieves a
notch for trunking like any other. Runs that cut their own openings could
not do that (see "Considered and set aside").

- **The opening leads and the run follows.** A hole, or a named pocket
  through, is a point a run passes (see "Points"). So the run goes where
  the opening is, and the opening's place is written once:

  ```python
  back.hole(d=pe12.passage, at=back.outer.bottom(150).right(60), depth=through, name="cold")
  run("cold", pe12).path(back.cold, ...)
  ```

- **`passage`** is the size an opening needs: the material's section grown
  by its gap on each side. For a 12 mm hose with the default 10 mm, it is
  32.
- **The checks tie them together.** A run that passes a board where the
  board has no opening overlaps its material, and `no_interference` reports
  that, saying where: "kitchen.cold passes kitchen.back at 60 from its
  right and 150 above its bottom, on its outer face, where it has no
  opening; a hole of 32 there would clear it". A run that passes an opening
  with less room than its gap on any side is reported too.
- **Openings along a run**, such as the notches in a floor's battens, are a
  loop over the boards, along a line the module chooses (see the second
  example).
- **What this gives up** is openings shaped by the run, such as an oblong
  where a run bends inside a board. Those are written as pockets by hand,
  or as a larger hole, and the check says whether they clear the run.

## Where runs are written

Runs are planned at the van level, where the modules are put together. That
is the last step: it checks that what was planned in the modules fits
[Florian]. The modules plan the openings, and the runs check them.

- **A van-level run** is written after the modules, outside every
  `with module()`.
  - It reads what a module exports, its openings first of all
    (`cab.export("cable", bottom.cable)` in the module, `kitchen.cable` at
    the van level), and may reach a module's parts (`ground.panel_front`);
    a part named after a direction is `kitchen["bottom"]`, which the exports
    make unnecessary [decided by Florian, 2026-10-15, syntax.md item 14].
  - When `van.py` asks with `check(no_interference)`, it is checked against
    the parts, hardware and runs of every module (see "Checks").
  - Its path is just its name, `cable_rear`.
  - One hose is one run, however many modules it passes.
- **It writes into no module.** So it keeps to the rule that a module
  refers only to the master, its own parts and other modules' exports
  [decided]. It is not a module, and it changes nothing in one.
- **The order needs nothing new.** Modules, with their openings, come
  first, and runs after them, so a run is resolved when it is written, like
  everything else.
- **A run may also be written inside a module,** to plan that module on its
  own [Florian]. It belongs to the module, is checked with it, and its path
  is `kitchen.cold`. When the van later routes the same hose, the two runs
  overlap, and `no_interference` reports it. So each hose is planned in one
  place [Florian]:
  - the van routes all of it and the module's own run goes;
  - or the module keeps its piece, and the van routes the rest as a second
    run.
- **Modules designed on their own fit together through the openings they
  export.** The kitchen plans its hole behind the drawers, and the floor
  plans its channel and the holes in its panels. Where those do not line up, the
  van-level run says so, and the module that gives way is changed: its
  hole moves, or its module function takes the place as an argument.
- **In a van nearly every place a run goes belongs to a module:** under the
  floor to the floor, behind the wall panels to the walls. The run only
  checks the space; whoever owns a board plans its openings.

### Considered and set aside

- **Runs that cut their own openings** (`.through(*boards)` in the drafts
  before). Resolved last, their openings would come after a board's own
  operations, so a cutout pattern made earlier would not keep material
  around them [Florian]. Resolved when written, a run at the van level
  would write into modules. Their one gain was openings shaped by the run.
- **Runs per module, joined at ports** (the drafts before):
  - one module placed a port in its own terms, and the van's build file
    said which port followed which;
  - runs were resolved at the end of the build;
  - the module with an opening at a port led.

  All of that was needed only while a run belonged to the module whose
  boards it cut. A run that only checks reads the modules' openings
  directly from the van level.
- **Ports placed in the van's build file**, from the master's boxes, and
  passed into the module functions. Set aside because that file was not
  meant to route [Florian]; with runs at the van level, there are no ports.
  What is left of them is the exports: a module names the openings a run
  may use (`cab.export("cable", bottom.cable)`), nothing more.

## Checks

- **When a run is written**, these are errors:
  - bends that do not fit their legs, or a bend tighter than the material's;
  - a leg that would twist a rectangular section;
  - a stop that does not move the run;
  - an opening in its path that is narrower than the section.
- **A run is checked for overlaps**, as `no_interference`
  (`design/checks.md`) checks parts. A module's runs are checked with the
  module's `no_interference`, which runs for every module unless the module
  turns it off (syntax.md item 4). Van-level runs are checked only when the
  van asks [Florian]: `check(no_interference)` written in `van.py`, outside
  every module, which is an error today and becomes allowed; the van level
  has no module to carry a default. There it checks the van-level runs against the parts, hardware
  and runs of every module. It could also check the modules' parts against
  each other, which nothing does today [open]. A run is reported where it
  overlaps:
  - a part's material, judged by the run's shadow on that part's plane:
    the part of the plane that the run's material covers between the part's
    two big faces, which is where a missing opening shows up;
  - a hardware body, judged by its boxes;
  - another run, judged by the distance between their centre lines.

  As for parts, touching does not count, so a run lying on a board is not
  reported. Where a run passes through a board's opening, it must also keep
  its gap from the board's material all round. A keep-out keeps
  everything out, runs included: once the cables it kept room for are
  routed, they take its place.
- `inside_box` and `inside(contour)` take the module's runs.
- **Not yet:**
  - the gap to the vehicle body (with the mesh, `design/todo.md`);
  - a run's distance from heat, such as the heater's exhaust;
  - whether a trunking's lid can still be reached.

## Layout

The layout goes to version 6. Each module gets a `runs` list next to
`hardware`. Van-level runs go into the module with path `""` that holds the
loose parts.

```python
class RunSegmentLayout(TypedDict):
    kind: Literal["line", "arc"]
    start: list[float]
    end: list[float]
    #: An arc's centre; the arc is the shorter way round from start to end.
    center: NotRequired[list[float]]


class RunLayout(TypedDict):
    path: str
    #: The material's label.
    material: str
    #: Room kept free (a keep-out material) rather than something bought.
    keepout: bool
    #: [d] when round; [w, h] when rectangular, the wide faces' width first.
    section: list[float]
    #: The world name of the way the wide faces face (`flat()`); None when
    #: the section is round or square.
    flat: str | None
    #: The centre line, legs and bends in order, tangent at every bend (mm).
    segments: list[RunSegmentLayout]
    #: The centre line's length (mm).
    length: float
```

A run changes no board, so the boards' layout is the same with or without
runs, and neither nesting nor the CAM plan sees them.

## Preview

- A run is its section swept along its centre line, with the arcs sampled,
  using `trimesh.creation.sweep_polygon`. Tried on a 12 mm hose with a
  60 mm bend between two 100 mm legs: the mesh is watertight, and its volume
  is within 0.2 % of the true one with a 16-sided section. [tried
  2026-10-15]
- Runs appear in the part tree under their scope and carry their names on
  labels. One switch shows or hides all of them, as for hardware (in
  Display, on a key, and as `preview.runs(on)`).
- Runs are coloured by material. Keep-outs are translucent, like the
  master's ghost boxes.

## Fusion

- **One body per run**, in a component of its own under its scope, as with
  hardware, and named by its path. It has no `lang`/`part` attribute, so
  Multi Arrange and Auto Setup leave it out.
- **A round run with bends is a pipe feature** along a sketch of its centre
  line, with the lines and arcs drawn in 3D through shared sketch points and
  taken as one path. Tried in Fusion on two legs and two bends in different
  planes: one solid, 7 faces, the exact volume, 16 ms. That was in a
  parametric document; a direct one is untested. [tried 2026-10-15]
- **A rectangular run with bends** is a sweep of the rectangle along the
  same path (untested).
- **The first draft's way does not work.** It built round runs from
  cylinders and tori as temporary B-rep, but Fusion's booleans on a
  temporary torus return wrong volumes: an intersection with a box came out
  empty or partial, however the torus was turned. [tried 2026-10-15]
- **A run with square corners is boxes**: temporary B-rep boxes along its
  legs, each run on by half the width at a corner, and unioned, as for
  hardware. Tried on two legs at a right angle: one solid, the exact
  volume. A mitre at any other angle needs one more cut. A round section
  with square corners is cylinders and spheres at the corners, which still
  needs a probe.

## Cut list

Runs are listed by material and length, the centre line's, rounded up; a
hose routed at the van level is one run, so one length. Runs that bend are
listed with their number of bends, and runs whose corners are fittings with
their fittings by angle (`conduit 20: 3 elbows 90`). Keep-outs are not
listed. This comes later, with the
committed outputs (`build-repo.md`), as for slats.

## Examples

These have not been run; they show the spelling.

### A hose to the tap

This hose stays inside the drawer cabinet. It comes from the wall through a
hole in the back and goes to a tap hole in the top. The holes are the
boards' own, written before anything that must keep clear of them, and the
hose is routed through them:

```python
# in drawer_cabinet(), after the drawers
back.hole(d=pe12.passage, at=back.outer.bottom(150).right(60), depth=through, name="cold")
top.hole(d=35, at=top.top.back(200).right(60), depth=through, name="tap")
run("cold", pe12).path(back.cold,              # in from the wall, through its hole in the back
                       back.inner.gap(60),     # 60 in front of the back, for the bend
                       top.bottom.gap(100),    # up behind the drawers, to 100 under the top
                       top.tap)                # forward under the tap hole, and up into it
```

The tap hole and the hole in the back are both 60 from the right side, so
the corner before the tap only moves the hose forward. In the 600 mm deep
cabinet of `drawer_cabinet.py`'s own build, the hose stays clear of the
drawers, which end 136 in front of the back. The legs between two bends are
at least 120 long, room for two 60 mm bends; the first and the last need
room for one.

### A cable through two modules

This cable comes from behind the kitchen's drawers, goes under the floor
and comes up at the back of the van. The kitchen and the floor each plan
their own openings; the cable is one run at the van level, which checks
that they fit:

```python
# in floor(), after the panels: a cable channel along the van, notched into
# the battens across, and a hole in each panel where a cable comes through
line = f.left.into(300)                                   # the channel's middle
for b in battens:                                         # the whole length, for later cables too
    b.cut(rect(width=14, height=12), at=b.front.top.center(line), name="cable")
panel_front.hole(d=24, at=panel_front.top.front(kitchen_box.back.into(135)).left(line),
                 depth=through, name="cable")             # under the kitchen
panel_back.hole(d=24, at=panel_back.top.front(floor_back - 100).left(line),
                depth=through, name="cable")              # at the back, for a bed
f.export("cable_front", panel_front.cable)                # the openings, for the van's runs
f.export("cable_back", panel_back.cable)
f.export("underside", panel_front.bottom)                 # the channel's ceiling

# in drawer_cabinet(): a hole behind the drawers, on the cabinet's cable line
x = cab.left.into(135)
bottom.hole(d=cable10.passage, at=bottom.top.left(x).back(back.inner.gap(15)),
            depth=through, name="cable")
cab.export("cable", bottom.cable)                         # the opening, for the van's run
cab.export("underside", bottom.bottom)                    # the toe kick's ceiling

# van.py, after the modules
ground = floor("floor", van.box("Boden"))
kitchen = drawer_cabinet(kitchen_box, front=kitchen_box.right, name="kitchen", n=3, slide=slide, bottom_drawer=230)
run("cable_rear", cable10).path(
    kitchen.cable,            # down through the hole behind the drawers
    kitchen.underside,        # just under the bottom, in the toe kick
    ground.cable_front,       # forward to the floor's hole, and down through it
    ground.underside,         # under the panels, in the channel
    ground.cable_back)        # to the hole at the back, and up through it
check(no_interference)        # the van-level runs against every module
```

- **Each opening places the run once.** At each hole, the corner before it
  takes the hole's position across, so the cable lines up with it without
  repeating its place. The kitchen's hole and the floor's front hole both
  lie 135 from the end of the kitchen box toward the van's back, which is
  the cabinet's own left. So under the kitchen's bottom the cable runs only
  forward, and in the channel only along the van.
- **Where the modules don't match,** the run says so. If the floor's hole
  lay outside the kitchen's toe kick, the leg to it would pass through the
  kitchen's side, which has no opening there. `no_interference` reports
  that, and one module moves its opening. A small offset only turns the leg
  in the toe kick into a diagonal.
- **The notches.** Under the panels, the cable's top touches their
  undersides, which is where the battens' tops are. The notches are 14 wide
  and 12 deep, so the cable has its gap of 2 below and on either side.
- **The panel holes are 24, not 14,** because the cable bends right under
  each panel, partly inside the hole. A smaller hole would be reported.
- **`center(line)` centres each notch** on the channel's middle along the
  batten, and `kitchen_box.back.into(135)` is 135 into the kitchen box from
  its back side in any frame (syntax.md items 6 and 1).
- **The cable's `bend_r` of 15** fits the 17 mm between the panel's top and
  the cable's centre line under it. A conduit with a bend radius of 80
  would be refused there.

### Room kept free

A keep-out keeps a channel free along the wall behind the kitchen, for
cables to come:

```python
run("wall_channel", channel).flat(cab.back).path(...)
```

## Later

- **Fittings** beyond elbows:
  - tees and branches, a run that starts on another run;
  - couplings.

  Rigid drain pipe (HT) needs nothing new: elbows of 15, 30, 45 and 87
  degrees are `angles=(15, 30, 45, 87)`.
- **Falls**: drains that fall along their whole length.
- **Clips**: how far apart they are along a run, which also says where the
  run is held.
- **Grommets**: the hole a grommet needs, in place of the run's shadow.
- **Centre lines drawn in the master**: a 3D sketch in the master as a
  run's path, for routes that are easier drawn than written.
- **External components' connections** as points.

## Questions for Florian

1. **The van's runs.** Which does it have, and which matter first? That
   means the water hoses (which product and size), the drain (rigid pipe
   with elbows, or a flexible hose), the cables (loose bundles, conduit or
   trunking), the heater ducts, and gas. This gives the standard library's
   tables, and decides whether falls belong in the first version.
