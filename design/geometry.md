# Geometry and tolerances

How the layout step represents 2D geometry, what it cleans away, and how
arcs survive the trip to Fusion. Part of the modeling language's design; the
overview is `DESIGN.md`. Code: `lang/core/geometry.py`, `shapes.py`,
`cutouts.py`, `lang/emit/arcs.py`.

## Polygons in, arcs out

- Layout shapes are polygons, since all of the layout step's 2D work is
  shapely. Circles, slot ends, `rounded()` corners, fillets and round-join
  offsets put their vertices exactly on a circle, and booleans keep those
  vertices.
- **Every circle and arc is drawn alike** [decided]: every circle has its
  vertices on the whole degrees about its centre
  (`cutouts.circle_geometry`), every arc its ends plus the whole degrees
  between them, none nearer an end than 0.6 degrees; arcs under 5 degrees
  keep even steps. So one arc drawn two ways coincides, and a circle cut on a
  rounded corner's own arc takes the corner instead of leaving crescents.
- **Arc recovery** (`lang/emit/arcs.py`, `fit`): the emitter plan recovers
  the arcs the polygons stand for. A run of at least 4 segments turning 0.5
  to 11.5 degrees each about one centre, every vertex within 1e-7 mm of the
  circle, is drawn as a three-point arc (a whole ring as a circle);
  everything else stays lines. That leaves coarse polygons (an octagon)
  alone, and the master's contours too: sampled every 0.1 mm and rounded to
  0.1 micrometre, they turn too little per step and are too noisy, so they
  stay polylines (see `design/todo.md`, snapshot arcs). The plan's outlines,
  pockets and chamfer contours are loops of lines, arcs and circles.
- Where a boolean cut the circle's polygon (a relief added to a rectangle or
  cut from an outline, two overlapping circles), the cut point lies on a
  chord, up to its sagitta off the circle; it is moved onto the circle,
  along the line it continues in or where two circles cross, so arcs meet
  lines and each other exactly. A junction is moved only where every arc at
  it keeps its way, and left where curves meet at a glancing angle. Curves
  that touch are met where they touch. A line running into an arc
  tangentially is not taken for one of its chords.
- The preview keeps meshing the polygons, so preview and Fusion differ by
  the polygons' chord errors (up to about 0.08 % of a body's volume).

## Cleaning

Nothing under 0.01 mm is meant [decided]. Every `Shape` is cleaned when it
is made (`geometry.clean`) of what booleans leave where two edges coincide:

- points within 1e-6 mm of the one before;
- spikes, a ring running out and back along itself, however long (taken off
  before a ring is judged narrow);
- pieces and holes narrower than 0.01 mm on average (twice the area over the
  length); a narrow piece is opened by 1e-6 rather than dropped, so wider
  parts a hairline joins stay;
- walls of no width (a hole along another ring within 1e-9 mm for more than
  0.01 mm), which are opened.

Every other vertex stays exactly where it was: snapping to a grid, even one
of 1e-9 mm, moves arc vertices off their circles and `fit` no longer finds
the arcs. Geometry with nothing to clean comes back unchanged. An invalid
result (a figure of eight, a ring along itself) is made valid. In Fusion an
uncleaned spike made the whole body fail (ASM_WIRE_SELF_INTERSECTS2).

## Tolerances and pieces

- 0.01 mm: the smallest thing meant. A board, contact, region reaching into
  a board, chamfer, depth or edge shorter than this is none or an error, as
  each rule says.
- 1e-6 mm: the checks' tolerance as a distance (see `design/checks.md`), and
  the opening used for levels and material (`geometry.opened`) so that walls
  of no width where pockets from either face meet do not make corners.
- A piece held on by less than 0.01 mm, by a hairline or at a point, is
  apart (`_pieces`), for cuts and for holes and pockets through the board. A
  through hole tangent to the board's edge that cuts a corner off but for
  the point where it touches is refused as splitting the board; a circle
  that only touches the edge is kept, as Fusion builds it.
- Openings that touch the outline, each other or themselves at a point are
  refused, through or pocketed (Fusion cannot make the profile or the
  chamfer).

## Offsets

`grown` (used by insets, cutouts and the preview) offsets the lines and arcs
exactly as Fusion's sketch Offset does: arcs run on along their circles,
corners keep the full distance and stay sharp (round joins gave rings with
radius-20 corners where Fusion has sharp ones). Where that does not hold (a
curve vanishes, pieces merge or part) it mitres with its arcs put back,
leaving out slivers and specks of holes. GEOS's mitred offset can cross
itself and lose pieces (two sharp corners close together send their
mitres past each other); it is then built again with the mitres bevelled
ever nearer their corners until it is valid, which keeps the distance as a
mitre does, and made valid only when none is. A self-check requires an inset to hold the shape shrunk by 1.25 times
the inset with mitred corners (where a tab narrower than twice the inset
turns over, Fusion joins the tab's neighbours straight across, up to 1.41
times the inset in), and an outward offset to hold the shape grown round by
0.75 times the offset; it allows the polygons' chord errors and 0.02 mm, and
an inset that fails falls back to the mitred one. Contour clearances use
GEOS round offsets instead (see `design/placement.md`).

Known gaps are in `design/bugs.md`.
