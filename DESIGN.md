# Modeling language: design

A modeling language embedded in Python that compiles flat furniture into
Fusion documents. This file is the overview; the details are in `design/`:

| File | What it holds |
|---|---|
| `design/api.md` | Language and API form, names and paths, frames |
| `design/placement.md` | Boxes, `on`/`between`, the position algebra, contours as limits |
| `design/master.md` | The master document and its snapshot |
| `design/operations.md` | Boards, shapes, cuts, pockets, holes, slots, depths, chamfers, fillets, cutouts, dog bones |
| `design/slats.md` | Sheet and slat materials, slats, lips and edge banding |
| `design/joints.md` | Contacts, crossings, half laps, connectors, tenons, screws, box joints, grooves |
| `design/hardware.md` | Drawer slides, hinges, hatch hinges, ball catches, latches, sliding brackets |
| `design/checks.md` | `no_interference`, `inside_box`, `inside()`, `fits_sheet` |
| `design/geometry.md` | Polygons and arcs, cleaning, tolerances, offsets |
| `design/emitter.md` | The Fusion backend, compile speed, Fusion findings |
| `design/nesting.md` | Nesting: parts on blanks the bed takes, sawn out of the stock on hand; the workshop and nest files |
| `design/preview.md` | The browser preview |
| `design/proposals/` | Features worked out but not built, one file each (listed below) |
| `design/todo.md` | A loose list of things to do |
| `design/bugs.md` | Known bugs and gaps |

Started 2026-10-09 from a design conversation between Florian and Claude;
implemented on branch `language`. How to run, test and fuzz it is in
AGENTS.md.

Markers on a point:

- **[decided]** Florian stated, chose or confirmed it. Ask him before
  changing it.
- **[proposed]** Claude suggested it and it was not rejected. A working
  assumption; check with Florian before building a lot on it.
- **[open]** undecided or unverified.
- **[Florian]** in a proposal: one of his points, as opposed to Claude's.

What is built was reviewed with Florian (2026-10-12) and is the working
design; the topic files describe the code as it is.

## Goal

A modeling language embedded in Python for Florian's van conversion work:
furniture made of plywood boards and solid wood slats, joined with the
connectors and hardware that this repo's add-ins already cover. The Python
source is version controlled and is the parametric model. Fusion documents
are generated from it.

Why: driving Fusion step by step through MCP is slow and hard to review on
large projects. Source text is efficient for Claude to write, readable for
Florian, and can be tailored to exactly his constructions.

Not goals:

- A general-purpose CAD language.
- Replacing Fusion. It stays the kernel, the viewer, and the place for
  toolpaths and post-processing. Nesting is in the language
  (`design/nesting.md`); the choice of CAM operations may follow
  (`design/proposals/cam.md`); generating G-code stays a non-goal.
- Describing parts that are curved in 3D (upholstered parts, parts curved two
  ways). Those stay hand-modeled and are referenced by name. Boards bent about
  one axis may come in (`design/proposals/bent-boards.md`).

## Terms and pipeline

- **Module**: one piece of furniture or assembly (kitchen, bed, floor). It
  compiles on its own into its own Fusion document. A **cabinet** is a module
  with a front, written in its own frame.
- **Master document**: a hand-made Fusion document with named planes,
  sketches, placeholder boxes and parameters for the whole van. The compiler
  reads it and never writes to it.
- **Snapshot**: the master document read once into a JSON file: every plane
  as origin plus normal, every contour as a sampled polyline, every body as a
  box, every user parameter.
- **Layout**: a pure-Python description of each part: its world placement,
  its outline, and a list of operations (2D shape, depth, face), plus the
  hardware as boxes. Written to one JSON file per module. No Fusion involved.
- **Emitter**: an interpreter for the layout file that creates Fusion
  features. The only code that imports `adsk`, with the snapshot writer.
- **Preview**: a second consumer of the layout file that meshes the parts and
  shows them in a browser, without Fusion.
- **Nest**: the parts of a build per material on blanks the machine's bed
  takes, sawn out of the stock on hand (a workshop file), written to a nest
  file the preview shows and the emitter draws, a document per material.

```
Master document --(snapshot, in Fusion, rarely)--> snapshot.json
                                                       |
Python source ---------------------------------------> layout step (plain Python,
                                                       anywhere, < 1 s)
                                                       |
                                  +--------------------+--------------------+
                                  v                    v                    v
                        preview (browser,     nest (plain Python,    emit (in Fusion, seconds,
                        instant)              seconds a material,    one direct document per
                                  ^           workshop file)         module)
                                  |                    |                    ^
                                  +---- nest view -----+---- nest.json -----+
                                                             (a document per material)

afterwards: Auto Setup (CAM); Multi Arrange stays a fallback for nesting in Fusion
```

Three steps with files between them. The layout step can use shapely and
numpy because nothing heavy runs inside Fusion's Python, and `core` is tested
against real van data without Fusion.

## Principles

The rules behind every topic file; details in `design/api.md`.

- Embedded in Python, built from a small set of primitives, extended with
  Florian's own functions. A cabinet type is a function. [decided]
- One-way flow from source to Fusion. Generated documents are disposable and
  never edited; hand-drawn input lives only in the master and in optional
  per-module reference documents. [decided]
- Constructors carry identity, modifiers carry everything else:
  `board("left", ply15)` names a part and its material; where it sits and
  what is done to it are method calls that return the part. Placement
  modifiers are order-free and set once; operations are ordered, as they are
  on the machine. [decided]
- Arrangement is stated as relations between named parts, not as arithmetic
  on dimensions: boards sit `on` a side and are trimmed `between` neighbours,
  so most parts carry no numbers of their own. Anywhere a length or position
  is expected, a reference can be given.
- Relations name every part they involve: `bottom.join(left, right,
  using=cabineo(count=3))`. Nothing is joined to whatever happens to touch.
  [decided]
- Hardware carries its own rules: the drawer slide sizes the drawer box and
  drills the carcass, so those numbers never appear in cabinet code.
  [decided]
- Faces, edges and anchors are typed attributes (`side.inner.front(37)`), and
  the package is checked with pyright in strict mode, so build files get
  completion and errors in the editor.
- Use Fusion's own features; no B-rep code of our own. Compile into direct
  documents, one per module. [decided]
- The layout step refuses what it cannot build rather than guessing, and a
  refusal changes nothing. Nothing under 0.01 mm is meant.

## Example

The carcass of `examples/drawer_cabinet.py`:

```python
from lang import *
from stock import ply9, ply15


def carcass(name, box, *, front):
    with cabinet(name, box, front=front) as cab:          # written in its own frame
        left = board("left", ply15).on(cab.left)
        right = board("right", ply15).on(cab.right)
        for side in (left, right):                         # a toe kick notch, named
            side.cut(rect(depth=60, height=100), at=side.outer.bottom.front, name="toekick")
        bottom = board("bottom", ply15).on(left.toekick.top, toward=cab.top).between(left, right)
        top = board("top", ply15).on(cab.top).between(left, right)
        back = board("back", ply9).on(cab.back).between(left, right, bottom, top)

        bottom.join(left, right, using=cabineo(count=3))
        top.join(left, right, using=cabineo(count=3))
        back.join(left, right, bottom, top, using=domino("4x20", count=2))

        for side in (left, right):                         # shelf-pin columns, lined up
            for z in spread(bottom.top + 100, top.bottom - 100, pitch=32):
                side.hole(d=5, depth=10, at=side.inner.front(37).bottom(z))

        cab.export("worktop", top.top)                     # for whatever stands on it
        check(no_interference, fits_sheet)
    return cab


box = Box.from_size(width=500, depth=600, height=720)
carcass("carcass", box, front=box.right)
```

No board has a size of its own (the toe kick notch is the one number on a
board), no joint names an edge, and the cabinet is placed by naming which way
it opens. The build files in `examples/` are the reference for everything
else, and the tests build every one of them: the drawer cabinet with its
slides, box-jointed drawers and grooved floors (`drawer_cabinet.py`), the van
floor against the sample master (`van.py`), and one file each for operations,
cutouts, dog bones, tenons (`shelf.py`), hinges, latches, the lift-up hatch,
the inspection hatch and removable panels.

## Code

```
lang/
  core/        no Fusion: refs, box, directions, faces, shapes, geometry, part,
               scope, ops, corners, cutouts, dogbones, contact, crossing,
               contours, checks, material, layout and layout_types, errors
  joints/      half laps, connectors, tenons, screws, box joints, grooves
  hardware/    slides, hinges, hatch hinges, ball catches, latches, sliding brackets
  emit/        plan, loops, arcs, nested (Fusion-free); fusion (draws); the snapshot writer
  nest/        nesting: workshop file, parts, PackingSolver, saw plans, refill, verify, drawing
  preview/     mesher, server, three.js viewer
  master.py    reading the snapshot
  build.py     `python -m lang.build`; `python -m lang.nest` nests
addins-src/compiler/   Snapshot Master and Compile Layout (layouts and nests) buttons
lib/           data shared with the add-ins (connector_data, stations, drawer_slides, ...)
examples/      build files; van_snapshot.json is the sample master's snapshot
tests/         pytest suite; tests/fuzz the Hypothesis fuzzing (AGENTS.md)
tools/         van_master.py builds the sample master; perf/ the compile benchmark
```

## Status

Built, in Fusion and the preview, each verified against its add-in where
there is one: placement and references, the master snapshot and contour
limits, every operation (cuts, pockets, holes, slots, chamfers, fillets, cutouts,
dog bones), half laps, Dominos, Clamex, Cabineos, tenons, screws, box joints,
grooves, drawer slides, concealed hinges, hatch hinges, ball catches, door
latches, sliding brackets, slats and lips (cosmetic slats for now), the checks,
the folder preview, and nesting (sheets and offcuts sawn into blanks for the
bed, the preview's nest view, nested documents in Fusion). Everything is
fuzzed (AGENTS.md, "Fuzz Tests").

Proposed, in `design/proposals/`. Where they depend on each other Florian
wants them done in this order: bevels before miters and
before fitted ends on tilted boards; tilted boards before miters at angles
other than 90 degrees; nesting before CAM. The spellings in the 2026-10-14
proposals are working titles, settled in a detailed plan for each before it
is implemented. [Florian]

| Proposal | |
|---|---|
| `bent-boards.md` | Boards bent about one axis, eased turns, kerfs |
| `chamfers-at-angles.md` | Corner and rim chamfers given by two lengths |
| `bevels.md` | Narrow faces cut at an angle, as hand work |
| `tilted-boards.md` | Boards turned about one axis of their scope |
| `miters.md` | Mitered corners as a joint |
| `standard-library.md` | `lang/std`: building blocks on the public API only |
| `nesting.md` | What is left of nesting (built: `design/nesting.md`): pinning cut sheets, parts larger than the bed, groups, the cut list |
| `cam.md` | A CAM plan from the layout, built by an add-in |
| `runs.md` | Hoses, cables, ducts and keep-outs: one run primitive that plans and is checked, routed through the boards' own openings, at the van level or in a module |
| `detail-levels.md` | Rough and full previews |
| `hand-made-geometry.md` | Escape hatches for what the language cannot say |
| `copy-path.md` | Copy Path, named faces on hand-modeled bodies, the Planung check |
| `build-repo.md` | A repo per van, committed outputs (cut list, SVGs, lock file) |
| `syntax.md` | Claude's syntax review of 2026-10-15, gone through with Florian: 16 items, each with his decision |

Smaller items are in `design/todo.md`, known defects in `design/bugs.md`.

## Where to look in this repo

- `AGENTS.md`: the dev cycle (reloading add-ins through MCP), modeling rules,
  running the language, the preview's `window.preview`, the fuzz tests.
- `lib/drawer_slides.py`, `lib/connector_data.py`, `lib/stations.py`: the
  models for Fusion-free data and layout shared by add-ins and the language.
- `lib/domino.py`, `lib/edge_sketch.py`, `lib/hole_features.py`: sketch and
  cut helpers the native add-ins build with.
- `lib/group_edit.py`: stored settings per add-in result.
- `lib/auto_setup/`: recognition of holes, pockets, contours, rim chamfers
  and V-grooves, and template-based CAM operations.
- `lib/multi_arrange/`: nesting in Fusion with its Arrange, including the note
  on document write cost; the language nests on its own now.
- `tools/perf/compile_bench.py` and `tools/perf/results/`: the compile-speed
  benchmark, also a worked example of the emitter's feature calls.
- `addins-src/connectors_native/main.py`: a full native add-in (inputs,
  geometry resolution from one edge, execute).

## Prior art worth borrowing from

| Project | Idea |
|---|---|
| BOSL2 (OpenSCAD library) | Directions as vectors defined once; added together to address edges and corners. https://github.com/BelfrySCAD/BOSL2/wiki/Tutorial-Attachment-Basic-Positioning |
| CadQuery / build123d | Selectors such as `>Z` (farthest face in +Z), combinable; named joints on parts. https://cadquery.readthedocs.io/en/latest/selectors.html , https://build123d.readthedocs.io/en/latest/joints.html |
| Onshape FeatureScript | Built-in features are written in the same language as custom ones. https://cad.onshape.com/FsDoc/ |
| Zoo KCL | Naming a sketch line names the face that grows from it. https://zoo.dev/docs/kcl-book/sketch_on_face.html |
| Boxes.py | Edge types per side in matching pairs; joint settings in multiples of thickness. https://boxes-audreyfeldroy.readthedocs.io/en/latest/api_edges.html |
| Carpentry Compiler (2019) | Separate design and fabrication languages with a manufacturability check. https://grail.cs.washington.edu/projects/carpentrycompiler |
| Polyboard | Construction rules as a style sheet with swappable sub-methods (not pursued: joins are stated per board). https://wooddesigner.org/help-centre/polyboard-manufacturing-methods/ |
