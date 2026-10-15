# CAM from the language

Status: added by Florian 2026-10-14, worked out by Claude the same day;
nothing built. Points marked [Florian] are his, [decided] his decisions,
[proposed] Claude's. Builds on the nest (`design/nesting.md`).

Florian's points: since the Fusion geometry is generated again on every
compile, the CAM setups have to be made again too; Auto Setup helps, but it
analyses the geometry to work back to the operations, while the language
knows them; construction, nesting and CAM setup should be one chain; no
G-code, but an output like the layout file that a Fusion add-in compiles into
a CAM setup [Florian]. Generating G-code stays a non-goal.

Today Auto Setup recognises holes, pockets, contours, rim chamfers, V-grooves
and dog bones on selected bodies, chooses templates and tools by rules (each
hole bored with the widest cutter 1 mm smaller, drilled only where no cutter
fits; blind holes over twice the cutter as pockets; through holes over 30 as
contours; checks of pocket corner radii and flute lengths; tabs by contour
length, away from concave corners; operations by widest tool, then by kind;
the V-bit last), and builds the setup from templates Florian exported. Where
Auto Setup runs on compiled documents has not been tried.

Proposed:

- A CAM plan written from the layout and the nest: a setup per blank (the
  nest saws sheets into blanks the bed takes, so a blank is one load on the
  machine; the blank as stock, the work coordinates at its corner) and
  operations in order, each with its template kind and label, its tool and
  the features it machines, named by part path and operation (contours,
  pockets with depths, holes, dog bones, chamfers, V-grooves), plus tab
  positions. No toolpaths.
- There is nothing to recognise: the layout already says what each
  operation is (a dog bone is a dog bone; a hole's diameter, depth, face and
  whether it goes through are exact) and what is hand work (bevels, mitres,
  lipping, slats), which stays out of the plan. Auto Setup's rules and tabs
  (`lib/auto_setup/`) are split into a Fusion-free layer that both use, as
  the joints were split into settings, layout and emitter. The tool data
  (diameters, flute lengths) are read from the templates outside Fusion, or
  kept in a tool file [open].
- A CAM emitter in the compiler add-in builds the setups in the nested
  document from the plan. It binds each operation to geometry the emitter
  made (bodies by path, edges and faces by position, as chamfers are found
  now). Fusion generates the toolpaths and posts them as before. Auto Setup
  stays for hand-modeled parts.
- The preview can show the plan: which tool cuts what, the tabs.
- One side only, for now [decided 2026-10-15]: no flipped setups and
  nothing automatic for machining a part from both faces. Each blank is
  machined from its top, where the nest lays every part with its machining
  face (`machine` in the layout) up, so the side is fixed per part before
  the plan is made. Operations on a part's other big face are left out of
  the plan, reported, and go on the hand-work list. In the examples 14 of
  137 boards have some: the drawer backs (hook holes outside, the floor's
  groove and the finger reliefs inside) and boards machined from their
  inner face with chamfers on the show face.
- The machining face is the one `machine()` names
  (`side.machine(side.inner)`, built 2026-10-15, see `design/api.md`), else
  the big face more pockets, holes and chamfers are made from, else the show
  face.
- The hand-work list per part comes from the same step: bevels and mitres,
  lipping and banding, roundovers (notes on edges), hardware to fit, and,
  once slats take operations, those (slats are made by hand, `design/slats.md`).
- With tool data known, the checks can refuse features narrower than the
  smallest cutter (`design/checks.md`).
- Slots carry their centre line in the layout (`design/operations.md`), so
  a slot as wide as a cutter can be cut in one pass along it (Fusion's 2D
  Slot) instead of as a pocket; then the 0.1 mm a slot is now made wider
  than its cutter no longer applies.

## Where Auto Setup goes wrong

Florian's notes of 2026-10-15 on what Auto Setup does badly and the plan
must do better [Florian]; the causes and the ways out are Claude's
[proposed].

- **The cutter for a pocket by its narrowest passage.** Auto Setup checks a
  pocket template only against the pocket's concave corner arcs, its flute
  length and the floor's area, so a pocket narrower than the cutter between
  straight walls, or a narrow neck between two wider parts, gets a cutter
  that does not reach it. The plan has the pocket's region exactly: a
  cutter of radius r reaches the region opened by r (shrunk by r, grown
  again), so the widest cutter whose opening leaves nothing but the
  material a cutter always leaves in a corner is the one; where none of a
  template's cutters reaches everything, the rest goes to a narrower one
  (as the adaptive templates' 6 mm cleanup does) or is reported.
- **A chamfered hole is drilled from the stock's top.** Fusion measures a
  drill or bore from the hole's top, the top of its cylinder wall, which a
  chamfered rim puts below the face; the V-bit cuts the chamfer last, so
  while the hole is drilled that material is still there, and the drill
  comes down to its feed height inside it. In the plan a hole's heights and
  depth count from the face it is made from, the stock's top there, and its
  chamfer is a V-bit operation of its own afterwards.
- **A slot is not a dog bone.** Auto Setup takes every concave arc narrower
  than the contour or pocket cutter for a dog bone, so the round ends of a
  4 mm slot (a Domino 4) are milled with the dogbone template, and the
  6 mm pocket template passes for the slot, since its ends are left out of
  the fit check as reliefs. The plan does not guess: a slot carries its
  centre line and width (`slot` in the layout) and is cut with a cutter
  narrower than it, as a pocket or along its line. Dog bones should be
  marked as such in the layout too, with the tool `dogbones(tool=)` drew
  them for: today a `dogbones()` relief is a cut or pocket named
  `<operation>_dogbones` and a joint's reliefs are part of its cuts.
