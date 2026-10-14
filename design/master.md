# Master document and snapshot

The vehicle's hand-made reference geometry and how the compile reads it.
Part of the modeling language's design; the overview is `DESIGN.md`. Code:
`lang/emit/snapshot.py`, `lang/emit/snapshot_format.py`,
`lang/core/snapshot_types.py`, `lang/master.py`.

## The master

- One master per van build, holding planes, base boxes and shapes that the
  modules refer to. Optionally one reference document per module for extra
  hand-drawn geometry. Everything else is generated on top. [decided]
- Four kinds of reference [decided]: planes, which give a position;
  contours, which give a shape to follow; placeholder boxes, rough bodies
  drawn in the master to divide up the room, which become module boxes
  (`cabinet("kitchen", van.box("Kueche"), front=...)`); and the master's
  user parameters, which are plain numbers (`van.param("Bodenhoehe")`). A
  box's front is stated in Python at placement, never read from the master.
- Naming uses what is visibly named in Fusion: one construction plane per
  plane reference, one sketch per contour (the sketch name is the reference
  name), one component or body per box, one user parameter per number. No
  hidden tags on single curves. The snapshot takes everything in the master;
  a name starting with a double underscore (`__temporarySketch`) is left
  out. Duplicate names are an error. [decided]
- The master's axes are the world axes (see "Frames" in `design/api.md`).
- A module refers only to the master, to its own parts, and to what other
  modules export. The kitchen reads the floor's top from the floor module in
  Python, not from a hand-moved plane in the master. Fusion documents stay
  independent because the dependency exists only at the Python level. The
  master holds vehicle facts, which is what a hand-made document is good at;
  a build may also hold plain measured numbers where nothing needs drawing.
- Exports: inside a module, `cab.export("worktop", top.top)` publishes a
  reference; a module function returns its module object, and the importer
  reads `kitchen.worktop`. An export cannot take a name that a scope already
  answers to (a direction or alias such as `top`, an extent, an attribute
  such as `interior` or `mount`), since `cab.top` would hide it.

## The snapshot

The snapshot is the compile's only view of the master. [decided]

- It holds planes (origin and normal), contours as polylines sampled at
  0.1 mm with a closed flag, boxes (min and max; a body that is not an
  axis-aligned cuboid is exported as its bounding box and flagged), and user
  parameters (value in mm and expression). Faceting on curved contours is
  accepted for now (see `design/todo.md`, snapshot arcs). The file carries
  its own hash and the source document's name; a layout records the hash of
  the snapshot it used.
- Writing it: the compiler add-in's Snapshot Master button runs
  `lang/emit/snapshot.py` on the active document and saves `snapshot.json`.
  The Fusion-free half, `lang/emit/snapshot_format.py`, chains curves,
  collects names and hashes, and is unit tested. Rules [decided]:
  - items in components are taken in world coordinates, through the
    occurrence they are reached by;
  - items in the root keep their names; items inside components are named
    by the dotted path of component names from the root, then their own
    name (`Bett.oben`, `Moebel.Sitzbank.Sitz`); a component's only body
    takes the component's path (`Moebel.Kueche`), since Florian names the
    components of placeholder bodies and leaves the bodies as Body1; user
    parameters belong to the whole design and have no path;
  - a component whose name starts with `__` is left out with everything in
    it; linked components are left out, since they belong to other
    documents;
  - sketches drawn only to make a body count as contours like any other, so
    they are named `__...` to leave them out (no guessing from hidden or
    consumed sketches);
  - a sketch's construction curves do not count; the rest must form one
    chain without branches; a curve no longer than the join tolerance
    (0.01 mm) is a point its neighbours meet at, and a closed chain of fewer
    than three points (a line drawn twice) is a problem, "the curves close
    around nothing"; the places of a name made twice are listed in order;
  - surface bodies, duplicate names (per kind: a plane and a sketch may
    share a name) and sketches that are not one chain are listed as problems
    in the file instead of failing the snapshot, and using such a name in a
    build is an error that repeats the problem;
  - the hash covers the content, not the document's name, and the file is
    deterministic (rounded to 0.1 micrometre, sorted, one point per line),
    so an unchanged master gives an unchanged file.
- Reading it: `van = master("snapshot.json")` in the build file (a relative
  path starts at the calling file's directory, or at that of the file given
  as `relative_to=`, for a helper that reads the master on its callers'
  behalf), then `van.plane(name)`, `van.box(name)`, `van.param(name)` (mm
  for lengths, degrees for angles), `van.contour(name)`. A plane is a
  `Plane` that acts as a position (`on`, `between`, `spread`, arithmetic)
  when it is axis aligned and is an error when a tilted one is used as one.
  A box that is only a bounding box adds a note to the layout's problems. A
  missing name is an error that suggests close matches. The layout carries
  the snapshots it read (file, source, hash, boxes, contours), and the
  preview draws the boxes as translucent ghosts with their names and the
  contours as lines (`m` toggles them).
- The sample master is built by `tools/van_master.py` in Fusion (rebuild it
  rather than keep a saved document); its snapshot is
  `examples/van_snapshot.json`, the test fixture, and `examples/van.py` is
  the worked example.

Not built: profile exceptions looked up by position
(`floor_profile.at(x)`, `replace(..., between=...)`) and the vehicle body as
a mesh; see `design/todo.md`.
