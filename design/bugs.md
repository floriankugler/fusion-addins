# Known bugs and gaps

Defects and gaps in the modeling language that are known and not fixed.
Where a fuzz check skips one, it is marked there too (`KNOWN` in
`tests/fuzz/boards.py`, `fuzzing.degenerate`; see AGENTS.md). Remove an entry
when it is fixed or decided.

## Geometry

- **Offsets where extended curves do not meet.** Fusion's sketch Offset
  bridges them with a line; `grown` drops the shorter curve instead, up to
  5.6 mm apart at such a corner. (`design/geometry.md`, Offsets)
- **A notch corner within a large arc's sagitta.** A notch whose corner lies
  within the polygon's sagitta of a large arc (0.014 mm inside a corner
  rounded 496) opens onto the outline as polygons but would be a hole on the
  true arcs, and `fit` draws that ring crossing itself.
- **Rim chamfers Fusion refuses**: along the short edges (0.06 to 0.34 mm) a
  cutout's mitred fallback inset leaves, rim chamfers larger than a
  fillet's radius, and a rim that a shallower pocket from the same face,
  made before, cuts into pieces at its corner (a 3 mm slot chamfered 1 mm,
  its end 2 mm out of a 1.3 mm pocket's corner; found with a Fusion batch
  of slots, 2026-10-14; the same slot fully inside the pocket, or crossing
  its edge elsewhere, is chamfered). The emitter leaves the loop sharp and
  reports it.
- **Slivers at arc ends.** Two drawings of one circle coincide but for a
  sliver at an arc's end, between whole degrees, up to r (1 - cos 0.5
  degrees) thick (0.019 mm at a radius of 500). Harmless while something
  joins it to the rest.
- **Outline rings touching at a point**: the preview's mesh of such a part may
  not be watertight (marked `KNOWN` in the board fuzz).

## Checks

- **`no_interference` sees arcs as polygons.** A pocket's or an outline's
  arcs are their polygons, so something touching such an arc from inside
  meets the chords' slivers, up to 3.8e-5 r deep, and is reported. No example
  or mount does it; drawing the arcs finer in the check, or round pockets as
  holes, would cure it. Left so for now [Florian, 2026-10-14].
- **`no_interference` stops at the placement box** and does not count
  pockets and holes in narrow faces, so tenons, box joint fingers and grown
  floors are not checked against other parts. Both come together [Florian,
  2026-10-14] (marked `KNOWN` in the checks fuzz).
- **Grooves**: a panel's edge running past the end of its board is not
  checked.
- **Hatch hinges**: the add-in's probe points miss a shelf 64 to 82 below the
  top. The hardware boxes catch it through `no_interference`.

## Fusion

- **Session-wide slowdown.** After about 25 document create/close cycles in a
  two-day-old Fusion session, every modifying API call became 6-7x slower, in
  new documents too, while read-only calls stayed fast. A Fusion restart
  cleared it. Cause unknown; whether many compiles per session provoke it is
  open. The preview loop avoids compiling on every save partly for this.
