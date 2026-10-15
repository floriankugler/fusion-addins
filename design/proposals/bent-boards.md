# Bent boards

Status: proposed by Claude on 2026-10-13 and revised with Florian's answers
the same day; nothing built. Only the points marked [Florian] are his.

A board bent about one axis, such as one piece running from a cabinet's
front round a corner (radius 80, say) into its side, a front stepping back
100 mm in a smooth S, a panel curved all over, or a ceiling panel following
the roof. Two halves: drawing it bent (preview, Fusion, checks), and its flat
pattern for the machine, unrolled, with kerfs (slots parallel to the bend
axis) where it bends. It narrows the non-goal "parts curved in 3D" to parts
curved two ways.

## Legs and bends

The straight stretches are ordinary boards placed as now, and a relation
makes them one piece, `front.bend(side, name="wrap", radius=80)`. The name is
required and names the piece on labels and in nesting [Florian]; the legs
keep theirs for faces and joins. The radius is the outer one, on the convex
face of the turn (no inner radius for now) [Florian]. Joins, holes and limits
keep working on the legs, so the joint code only ever sees flat boards, and
nothing joins on the curve. A part limited by both legs follows the bend's
inside, as a contour limit in its plane does today. A board on a curve
without legs (the roof's contour, an arc written in code) is `.on(curve)`.

## The shape of a turn

The step from straight to bent is always smooth [Florian]: every turn is
eased, its curvature rising from zero where a leg ends and falling to zero
where the next begins (clothoids, as on roads and railways, then an arc of
the radius), so `ease=` is above 0, a keyword on `bend()` with a package default (no
project rules: `syntax.md` item 16, 2026-10-15). The legs give
the shape's frame:

- Legs meeting at a corner (their outer faces meet in a line) make one turn,
  and each leg is trimmed back as far as the turn needs (radius 80 at a right
  angle: 80 mm with ease 0, 113 at 0.5, 150 at 1).
- Parallel legs ending apart, a front stepping back: the bend fills the gap
  exactly, from where one leg ends to where the other begins, as an S of two
  turns in opposite directions with a straight stretch between them. The
  radius is the shape's control: the largest that fits makes a pure S whose
  turns meet at the inflection (a gap 250 mm long and 100 mm across, ease
  0.5: radius 122), a smaller one tighter turns and a straight diagonal
  between them (radius 80: 157 mm at 28 degrees). Without `radius=` the S is
  the largest that fits; `radius=(150, 80)` makes an uneven one; a radius too
  large is an error naming the largest. Shapes beyond these take waypoints
  (`via()`, as runs do) or `.on(curve)`. [Florian agreed to the S shaped by
  its radius]
- Considered for the S: a spline filling the gap, with three control points
  on each leg's line (so zero curvature at the ends) and the handles' length
  as the weight, drawn exactly in Fusion as a degree-5 control-point spline.
  Its best, handle 0.2 (the minimum-jerk "smootherstep"), reaches radius 122
  in the same gap, as the eased S at ease 0.5 does, but its weight means
  nothing on the board and the radius comes out instead of being given.

## Flat pattern and kerfs

- The flat pattern is a plain board: the outline unrolled along the neutral
  layer, the legs' operations moved into it, the kerfs pockets from one face,
  so the emitter's flat side needs nothing new. The neutral layer is the skin
  for kerfs and the middle for bending plywood; on a right angle at outer
  radius 80 in 12 mm plywood the two differ by about 8 mm in length, so it is
  a stated value, calibrated with a test bend.
- Kerfs are flat-bottomed slots [Florian], all in one face, whichever way
  each turn bends, since the board bends both ways with them there
  [Florian]; the face is the one it is machined from, the inner face by
  default, so an S needs no flipping either. They are closely spaced, each
  closing only part way where a turn bends toward their face [Florian]:
  slots that close fully at the radius are too few, since a slot is no
  narrower than its cutter, and the wide webs between them stay straight, so
  the curve is not smooth. `kerfs=kerfs(width=3, skin=2, pitch=6)` spreads
  them at the pitch over the stretches that curve; on a turn toward their
  face each closes as far as the curve is tight there, on one away from it
  each opens. The one check is that none has to close more than its width at
  the tightest radius of a turn toward their face (12 mm plywood, 2 mm skin,
  3 mm slots, outer radius 80: pitch at most 21.5 mm). Without kerfs the
  material's minimum radius is checked.

## In Fusion and the preview

- Fusion gets two bodies: the bent one for the assembly and the checks (its
  section extruded along the bend axis, the legs' operations as now, no
  kerfs), and the flat one, which Multi Arrange and Auto Setup take. The
  preview bends the flat mesh along the neutral layer, which closes or opens
  the kerfs as far as the wood does.
- Corners of a flat board's outline get the same eased turn,
  `fillet(corner, r, ease=)`, ease 0 being today's arc. Considered: a conic,
  Fusion's sketch Conic Curve (`SketchConicCurves.add(start, end, apex,
  rho)`), whose setback stays while rho sets the shape (0.414 is the circle
  at a right angle); every other rho is tighter than the circle somewhere
  (setback 80: 57 mm in the middle at 0.5, 30 mm at the ends at 0.3), and its
  curvature jumps where it meets a line. Figma's corner smoothing gets
  tighter than its radius (52 mm for radius 80 at 0.3). The layout's point
  rings give Fusion no clothoid exactly: it would carry the curves, or tangent
  arcs fitted within 0.01 mm, recovered as arcs are now.
