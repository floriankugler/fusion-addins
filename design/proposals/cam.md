# CAM from the language

Status: added by Florian 2026-10-14, worked out by Claude the same day;
nothing built. Only the points marked [Florian] are his. Builds on the
nest (`design/nesting.md`).

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

- A CAM plan per nested sheet, written from the layout and the nest: setups
  (the stock, the work coordinates at its corner, top or flipped side) and
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
- The preview can show the plan: which tool cuts what, the tabs, the flips.
- Parts machined from both faces need a flipped setup of their sheet and a
  way to register it. Florian has no standard procedure for this yet, so it
  is worked out with nesting and CAM [Florian].
- The hand-work list per part comes from the same step: bevels and mitres,
  lipping and banding, roundovers (notes on edges), hardware to fit, and,
  once slats take operations, those (slats are made by hand, `design/slats.md`).
- With tool data known, the checks can refuse features narrower than the
  smallest cutter (`design/checks.md`).
- Slots carry their centre line in the layout (`design/operations.md`), so
  a slot as wide as a cutter can be cut in one pass along it (Fusion's 2D
  Slot) instead of as a pocket; then the 0.1 mm a slot is now made wider
  than its cutter no longer applies.
