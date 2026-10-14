# Slats

Status: the primitive is decided, its spelling proposed; nothing built.
Lipping (`lipping.md`) depends on it.

- A **slat** is solid wood defined by cross-section and length. It has no
  canonical top or bottom. [decided]
- Its faces are named by direction once it is placed. It goes on a cut list
  by length instead of into a nest; typical operations are end cuts and
  miters; grain runs along the length. Board versus slat is a matter of stock
  form, not species: a glued-up solid wood panel is a board.
- Spelling: `slat(name, material, section=(w, h)).on(face_a,
  face_b).between(start, end)`. The two faces in `on()` pin the two lateral
  axes, the way `on()` pins a board's thickness axis, and `between()` gives
  the length. A slat's own faces are named by direction like a board's.
  Holes and pockets work as on a board.
- End cuts at an angle are the same operation as a board's bevel and would
  be spelled `bevel()` (see `bevels.md`); the first draft had
  `.miter(end, angle)`.
- Lipping gives the material as a cross-section, `section("oak", 10, 12)`,
  which a slat could share.
