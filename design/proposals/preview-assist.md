# The preview as a code assistant

Status: proposed by Claude on 2026-10-17 as a brainstorm and gone through
with Florian the same day, item by item; every item below was taken, with
his rules for the clicks, the selection and the glow worked in [Florian,
2026-10-17]. Nothing built. The preview as it is: `design/preview.md`; how
to drive it from code: AGENTS.md.

## Why

Build files are written by hand and by Claude, saved and looked at
(`DESIGN.md`, Performance). The preview reads well: click to path, labels,
settings per part, `look` at a named operation, problems as text. What it
does not do is help the other way: getting the right text into the build
file, and showing what a save changed. The items here do that, and stay
short of a modeling UI: no dragging, no sliders, no editor in the page. The
source stays the model, the one-way flow holds, and each item ends as text
to paste, as a reference Claude reads from the page, or as a clearer
picture. [decided; Florian: "exactly the kind of code-assistant
functionality I was looking for, either for writing the layout code
manually, or to have you write it"]

Every item serves both ways of writing: a click or key for the hand, and a
`preview.*` call for Claude through the built-in browser.

## Lines in the layout

Everything below that links the picture to the text needs the layout to say
where each thing was written.

- Each part, module, hardware item and operation carries `where`: the build
  file's line that made it, `examples/van.py:45`, found as the settings'
  errors find theirs (`lang/core/settings.py`, `build_line`: the innermost
  frame outside the language). So a board the standard library makes points
  at the build file's `carcass(...)` line, the operations a `join` makes in
  both boards share the join's line, and a loop's boards share one line. A
  frame walk per call, a few frames each, which the settings' reads already
  pay; measured on the van before merging, as every feature is. [proposed]
- A layout version: main is at 9 since the CAM plan (PR #16), so this
  takes 10.
- An error found when a board resolves lazily names the board's line (the
  to-do item "Errors at the layout step name no line" moved here):
  `examples/van.py:45: board("batten3", ...): no material along its chain`.
- The selection panel shows the line, and `o` asks the server to open the
  editor there (`POST /open?file=&line=`; the server runs a command given at
  start, `--editor 'code --goto {file}:{line}'` the default). Florian uses
  VS Code [2026-10-17]; where `code` is not on the server's PATH (it is not
  in the app's shell), the default falls back to the binary in the app
  bundle, `/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code`.
  The build log's `file:line:` lines become the same links.
- From code: `preview.parts()` and `preview.ops()` carry the line, and so
  does `preview.selection()` (below).

## The selection panel

What is selected is the panel's subject: one item or several, each with
what it is, what it belongs to and its numbers, and under them the code one
might write about them next, every line copied by a click [Florian,
2026-10-17]. It replaces the box that shows a part's path today.

- **One item.** The panel says what it is (a board, a slat, a bought part,
  a module or scope, a face, an edge, a corner, a point on a face, an
  operation), its full path, its material, and its dimensions: a part's
  three extents in its module's frame, as width, depth and height, so they
  read as the build file writes them; a face's two; an edge's length; an
  operation's size and depth as written. Then what it belongs to, up the
  chain: a face shows its board with path, material and dimensions, an
  operation its board, a board its scope and module with their boxes. The
  path lines are the spellings the build file uses.
- **Several items** (shift-click, below) are listed the same way, each
  with its own lines, and then what relates them: the distance between two
  faces, the gap between two parts, with the code for it (Snippets to
  copy).
- From code: `preview.selection()` gives the same as data, with each
  item's world point and line.

## Click to reference

A click in the scene selects, and copies what the next line of the build
file needs, not only a part's path. [decided by Florian, 2026-10-17, with
these rules]

- A plain click in a face always copies the face: `kitchen.left.inner`. The
  raycast's hit normal against the part's `axes` gives the face's world
  name, which the part's `faces` maps to the build file's names: the
  direction in the scope's frame, and `inner` or `outer` where it resolves.
  The panel shows both, as the face labels do. The part's bare path comes
  from the panel or the parts list, as now. [open: which spelling the
  clipboard gets where both exist]
- A click near an edge, within a tolerance in screen pixels (6 px, say),
  copies the edge: `kitchen.left.inner.front`, the hit face with the face it
  meets. The candidates are the hit face's box edges first; an edge that
  operation geometry makes (`left.toekick.top`) is found the same way along
  the outline's segments that come from a named operation, as a second step
  [open].
- A click where two edges meet, both within the tolerance, copies the corner
  as an anchor on the clicked face: `kitchen.left.inner.front.bottom`.
- Command-click copies an anchor with offsets from the two edges nearest the
  click, on the face the click fell in:
  `kitchen.left.inner.front(37).bottom(120)` [Florian: command-click rather
  than click and hold; the click's proximity to the edges decides which the
  distances are measured from]. The numbers are whole millimetres [open: or
  halves].
- Shift-click adds to the selection instead of replacing it [Florian:
  multi-select with shift, since a second click only changed the
  selection]. The selection is a list of references, each a part with an
  optional face, edge, corner, point or operation; `h` and `i` act on all of
  them; `esc` clears. Two edges of one face selected make a corner (a
  click at their meeting point does the same at once).
- A click on a hardware body copies its path, as now; a click on a master
  box's ghost copies the master's name with the side,
  `box("Moebel.Kueche").right`, for the build's own variable to replace
  [proposed].
- The clipboard carries the full path, as now; the build file writes the
  tail inside its scope [open: trim to the module shown].
- From code: `preview.name(point)` gives the face, the nearest edge and
  corner and the anchor with offsets for a world point on a part, so a
  measured point or a mark turns into text; `preview.select([refs])` takes
  references too.

## Snippets to copy

Under the items, the code one might write about them next: each a line
copied by a click, with variants where a choice is natural, so the text is
taken and adjusted rather than typed [Florian, 2026-10-17]. The spellings
are the layout's names in the build file's own terms, the position algebra
as `design/placement.md` writes it; the panel offers and never guesses
which is wanted.

- A face: its name, `kitchen.left.inner`; moved in and out, `.into(15)` and
  `.gap(15)`, each with a value to adjust; its centre, `.center`; its
  position, `.position`.
- An edge: its name, `kitchen.left.inner.front`; a point a distance from
  it, `front(37)`; the corners at its ends.
- A corner, or two edges of one face: the anchor,
  `kitchen.left.inner.front.bottom`; with distances from both edges,
  `front(37).bottom(120)` [Florian: the corner, and variants a distance
  from the two edges].
- A point on a face (command-click): the anchor with its offsets from the
  two nearest edges, and the variants measured from the other edges
  (`back(463)` for `front(37)`), and the `center(pos)` form.
- Two parallel faces: the distance, `top.bottom - bottom.top`; the
  midpoint, `(bottom.top + top.bottom) / 2`; a fixed distance from either
  side, `bottom.top.gap(100)` and `top.bottom.gap(100)` [Florian: not just
  the centre, a value from one side or the other]; `between(bottom.top,
  top.bottom)`. Faces that are not parallel are said to be so, with no
  expression.
- Two parts: `between(left, right)`, and the gap between their boxes along
  each axis with the pair of faces that bound it, as above.
- Two anchors or corners: the distances along each axis; a face and an
  anchor: the anchor's distance from the face's plane.
- An operation: its geometry's name, `kitchen.left.toekick`, and its faces
  and edges, `left.toekick.top`.
- From code: `preview.snippets()` lists the snippets offered for the
  selection, so Claude can take one as well.

## Values edited in place

The furthest step, after everything else here [Florian's idea, 2026-10-17;
proposed to build last]:

- A snippet with a value (`into(15)`, `front(37)`, `gap(100)`) shows the
  number as a field: typed, or dragged like a slider, it changes, and the
  scene draws what the snippet then names, live: a dot for an anchor, a
  line across the face for a point a distance from an edge (where the
  anchor may lie), a plane for a side or face moved. A click on the snippet
  copies it with the value as it stands.
- The drawing is the page's own, from the layout's boxes and faces: no
  build runs, and nothing in the model changes until the text is pasted and
  saved. So it stays a copy helper and never a second model, the line drawn
  under Order, keys and cost.
- [open] The drag's scale (a millimetre a pixel, finer with shift) and
  snapping to whole millimetres.

## Operations clicked

- A click on a part picks, among the operations on the hit face, the one the
  hit point lies in: a pocket's or cut's shape contains the point in (u, v),
  a hole's circle does, a V-groove's line or a chamfer's edge is within the
  tolerance; else the part is selected as now. [decided]
- The panel shows the operation: its name, kind, face, the depth as written
  (`depth_spec`), its own settings (`op_settings`) and its line. The
  clipboard gets its geometry's name, `kitchen.left.toekick`, as the build
  file reaches it [proposed]; `preview.look` keeps `path#op`.
- One key (`j`) sections through the selected operation, across its face at
  its point, along whichever of the part's two in-plane axes is nearer the
  view, and isolates the parts it belongs to: with a joint's operation the
  part and its partner. [open: the partner by the join's shared line, which
  a loop blurs, or named on the operation by the layout]
- From code: `preview.ops(path)` gains the line, and
  `preview.select('kitchen.left#toekick')` selects an operation.

## The selection as the pointer, and marks

Florian's words go through the Claude Code app, typed or dictated (macOS
transcription), and may refer to what is selected: "chamfer the selected
edge" [Florian, 2026-10-17]. So the selection is the pointer, and marks
keep a pointer for later.

- `preview.selection()` gives the selection as references with their
  spellings, world points and lines, so a sentence about "this edge" reads
  as `kitchen.left.inner.front`.
- `p` pins the selection as a mark: the reference with an optional note
  typed in the panel, listed there, drawn as a pin at its point with the
  face or edge highlighted. Marks are kept per design in the page (local
  storage) and cleared by hand or when their part's entry changes in a
  build. `preview.marks()` lists them, `preview.mark(ref, note)` adds one
  from code, so Claude can point at something when explaining, and
  `preview.unmark(ref)` removes one.
- No text channel in the page beyond the note. [decided]

## What a save changed

The question the loop exists for: did the edit do what I meant. [decided]

- On a rebuild the page diffs the new layout against the one on screen, per
  path: parts added, gone and changed (their entry differs). Within a
  changed part it compares the operations (by name, else by index and
  kind), the outline, the box, and the rest (material, settings, grain,
  nest). Linear in the parts and operations, in the page, so no server
  change; a reload loses only the last diff. [proposed]
- Changed parts are tinted for a few seconds, or until a click or key; parts
  gone are kept as grey ghosts, and a moved or reshaped part's old mesh as a
  ghost, until the next build (`u` toggles the ghosts).
- A glow for small changes [Florian]: a change the tint cannot show, a hole
  moved by 2 mm or a chamfer's size, gets a glowing halo at each operation
  that differs, was added or removed (placed as `look` places it), and an
  outline change a glow along the segments that differ. A change the diff
  cannot place (a material, a setting) is said in the panel. The glow is
  what finds a 0.5 mm change.
- The panel lists the changes (`3 parts changed: kitchen.left (2 ops), ...`)
  and `preview.changes()` gives them, so Claude sees what a save did
  without a screenshot.

## The source pane

- `l` opens a read-only pane with the build file's text, lines numbered; the
  server serves the folder's files (`/source?design=&file=`). The pane shows
  the file of the selected reference's line and scrolls there, the lines
  that made the selection highlighted; clicking a line selects everything
  it made (a loop's line all its boards, a `carcass()` line the whole
  carcass, a `join` line the operations in both boards). Hovering a part
  highlights its lines, hovering a line its parts. [decided]
- Editing stays in the editor: the pane is for reading in both directions
  without an editor plugin.
- Where it sits [open]: a strip under the scene or a third column; hidden by
  default.

## Problems anchored

- First, without a layout change: the paths and operation names in a
  problem's text become links (the longest known path that matches), and a
  click selects and frames what they name. [decided]
- Then, a layout version: a problem carries what it is about (`{text, path,
  op?, face?}`), so a refusal that names a face looks at that face, and
  `no_interference`'s pair carries the overlap box, drawn red where the
  parts meet (the to-do item "Check results in the preview's scene" moved
  here: interference pairs, sheet fit, parts flagged as not plain flat
  work). [proposed]
- Drawing a refused operation where it would have been needs the refusal to
  carry its shape and face; later. [open]

## Color by

- A dropdown under Display, `c` cycles it: material (as now), module, nest,
  grain (the stripe, `design/preview.md`), machining face (the face up on the
  machine tinted, a second material on the triangles whose normal is its
  direction), show face, changed since the last build. A part without the
  value is grey, and a legend lists the values. `preview.colorBy(name)`.
  [decided]

## The cut list as a tab

- The cut list is decided as a CSV the build writes (`design/nesting.md`,
  The cut list). Once it exists, the page shows it as the nest view is
  shown (`t`): by module and material, slats by length, hardware counted,
  with a search box; clicking a row selects and frames the part, and the
  selected part's row is marked. `preview.cutlist()`. [decided]

## Order, keys and cost

- Order [proposed]: the lines first, since marks, problem links, the source
  pane and the editor hop stand on them and the plumbing is small; then
  click to reference with shift-select, and the selection panel with its
  snippets, the daily friction; then what a save changed, nearly free and
  sharpening every later save; then the selection pointer and marks,
  operations clicked, problems, color by and the source pane; the cut list
  when its CSV exists; values edited in place last.
- Keys, working titles [open]: `o` open in the editor, `l` source pane, `j`
  section through the operation, `p` pin, `u` ghosts of the last build, `c`
  color by, `t` cut list; shift-click selects more, command-click copies an
  anchor with offsets. AGENTS.md's list of `window.preview` grows with each
  call above when it is built.
- Cost: each item is a layout field or a page feature; the server gains two
  small endpoints (open, source). The page's work per build is linear in
  parts and operations, measured on the van as the budget asks
  (`DESIGN.md`, Performance). No new process.
- Not in: dragging parts, sliders on parameters, an editor in the page. The
  most in that direction would be a what-if override of a master parameter
  in the URL, read by the build and never saved; it waits. [decided]
