# Hand-made geometry and escape hatches

Status: proposed. Built so far: one-offs in code (rung 1) and `.manual()` as
a placement modifier, without the reference document it expects.

The output is read-only: the next compile replaces it. Hand geometry is
therefore always input, never a downstream edit. The seam between generated
and hand-made work runs at any granularity, through this ladder, cheapest
first. Anything that does not fit the flat model goes through these hatches,
which flags the part as no longer plain flat work.

1. **One-offs in code.** An extra hole or notch is one line with a named face
   and a position.
2. **Hand-drawn 2D shapes as inputs.** The hard part of a one-off is its
   shape. It is drawn as a named sketch in the module's reference document;
   the code says cut, pocket or outline, which face, how deep. This covers
   most of the long tail.
3. **Hand-modeled bodies as inputs.** A bracket or vehicle part is modeled by
   hand and a board is told to clear it. The emitter does the boolean in
   Fusion; the part is flagged as not plain flat work, and the preview shows
   it uncut with the obstacle beside it.
4. **Raw API code inside the module function.** The compiler hands the
   function the real faces and edges behind the names. Reproducible and
   version controlled, unlike a timeline edit.
5. **Takeover by name.** A part declared manual, `board("left",
   ply15).on(cab.left).manual()`, stops being generated. The compiler expects
   a hand-modeled body with that path in the reference document and still
   includes it in checks, nesting and labels. The placement modifiers stay,
   so the part keeps its box for contacts and limits.
6. **Whole hand-modeled components.** Curved trim and upholstered parts,
   referenced for interference checks only.

The one thing to avoid is a hand document that attaches features to faces of
a generated module, since every compile gives those faces new identities. If
that is ever wanted, the compiler emits named construction planes as stable
anchors and hand work attaches to those; whether Fusion re-resolves such
links across a regenerated document is untested. [open]

The read-only check on Planung (see `copy-path.md`) suggests the seam matches
what is hand-modeled today: the furniture modules resolve almost completely,
the vehicle-fitted trim does not. Walking one existing module's timeline and
bucketing every feature into the six rungs above would show which hatches the
first version needs (see `design/todo.md`).

Related: external components (electrical parts, appliances) to plan room
for, in `design/todo.md`; runs' `keepout` in `runs.md`.
