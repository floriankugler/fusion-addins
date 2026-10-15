# Checks

Design checks that run on the layout, before any geometry exists in Fusion.
Part of the modeling language's design; the overview is `DESIGN.md`. Code:
`lang/core/checks.py`.

- A module asks for checks with `check(...)` inside it or `module.check(...)`
  after: `check(no_interference, fits_sheet)`,
  `kitchen.check(inside_box, inside(floor_outline))`. Results go into the
  layout's problems and the build's output.
- Every check allows 1e-6 mm, as a distance: a part may reach that far out of
  a box or contour, and an overlap counts only where it is deeper than that
  in every direction. Touching never counts. [decided]

## no_interference

Reports parts whose material overlaps, and hardware that reaches into parts
or into other hardware.

- Boards in one plane overlap only where their material does, so a hatch
  with rounded corners in a rounded opening is not reported although its box
  reaches into the opening's corners. A part's material is its outline minus
  its pockets and holes, looked at slab by slab between the ends of their
  ranges along the thickness, so a latch in its hole, a runner's coupling in
  the front board's cut-out, or a pin through a pocket from one face and a
  hole from the other is not reported.
- Boards across each other are looked at cell by cell, where the stretches
  each has material along the axis their planes share must overlap (the
  crossings of `design/joints.md`), so lapped boards are not reported.
- Hardware [decided]: a hardware body whose boxes reach into a part's
  material is reported (`cab.drawer1.runners.left overlaps cab.drawer1.back`),
  and so are two hardware bodies whose boxes overlap, of one item or of two;
  a body is the union of its boxes, so its own boxes may overlap.
- An overlap counts where it is deeper than 1e-6 mm in every direction, in a
  board's plane as across its thickness [decided]; the material is not
  cleaned first. A hole is its circle within a quarter of the tolerance (up
  to 430 mm across); a pocket's or an outline's arcs are their polygons (see
  `design/bugs.md`).
- Not looked at yet: material past the placement box (tenons, fingers, a
  floor grown into its grooves) and pockets and holes in narrow faces.
  Looking past the boxes would report every box joint, whose fingers clear
  each other only through their grooves in narrow faces, so both come
  together [decided].

## inside_box and inside()

- `inside_box` keeps a module's parts inside its box.
- `inside(contour, gap=)` keeps them inside a closed contour seen along its
  normal: a part in the contour's plane by its outline, any other by its
  outline's extent and its thickness.
- Both look at where the material lies, so a tenon or a box joint's fingers
  past the placement box count and an end cut away does not [decided].
  Anything further out than 1e-6 mm counts, however little its area.
- `inside()` measures a part as `between()` places it, so the two agree: the
  clearance offset by the same call in the part's own axes, and a part across
  the contour from 1e-6 mm inside its faces, as `between()` holds it.

## fits_sheet

Checks each part against its material's sheet size (`size=`), within 1e-6
mm; a slat is on no sheet and passes. Nesting
against the machine's bed is proposed in `design/proposals/nesting.md`.

## Not built

Proposed early on, not built: machinable from one side, no feature narrower
than the cutter (needs tool data, see `design/proposals/cam.md`), the gap to
the vehicle mesh. With contours in the snapshot, parts limited by contours
are checkable in the layout step; only parts cut by hand-modeled bodies would
need Fusion first.
