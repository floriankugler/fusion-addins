# Language and API form

How a build file reads: the language's form, the shape of its API, and how
objects are named. Part of the modeling language's design; the overview is
`DESIGN.md`.

## Language form

- Embedded in Python, built from a small set of primitives, extended with
  Florian's own functions. A cabinet type is a function. [decided]
- One-way flow from source to Fusion. Generated documents are disposable.
  Hand-drawn input lives only in the master document and in optional
  per-module reference documents. [decided]
- Division of labour inside the source:
  - numbers are variables, each design decision stated once;
  - arrangement is expressed as relations between named parts, not as
    arithmetic on dimensions;
  - repeated constructions are functions;
  - geometry taken from the vehicle comes from the snapshot, as polylines;
    the kernel is only asked for things a polyline cannot give (booleans
    against hand-modeled bodies), and those are the exception.
- Eager position math, deferred emission. A part's position and faces are
  known as soon as its placement is stated, so references like `left.inner`
  work in the next line. Nothing touches Fusion until the whole module is
  declared, because joints change both parts they connect and checks run
  before geometry exists. The examples read as immediate mode; they are not.

## API form

Constructors carry identity, modifiers carry everything else, in the style
of SwiftUI and jQuery. `board("left", ply15)` names a part and its material;
where it sits and what is done to it are method calls that return the part,
so they chain or stand on their own lines. [decided]

- **Placement and property modifiers are order-free and settable once.**
  `on`, `between`, `center`, `inset`, `grain`, `show`, `manual`, `nest`, and a
  slat's `edge_on` (`design/slats.md`). Setting one
  twice is an error. The result never depends on the order they were
  written in.
- **Operation modifiers are ordered.** `cut`, `pocket`, `hole`, `slot`, `chamfer`,
  `fillet`, `cutout`, `dogbones`, `lip`, and the joins. A cut changes the outline
  for everything after it, and so does a fillet (or chamfer) on a corner of
  the outline; a chamfer on a pocket must follow the pocket. The order on
  the page is the order in the layout.
- **Every modifier returns the part itself, and the part is mutable.** A
  later `side.hole(...)` on its own line is the same as the chained form,
  which is what the incremental workflow needs. Operations get a `name=` and
  are reachable as attributes, so `left.toekick.top` names the face a cut
  made: a named operation's edges are positions by direction, a pocket or
  hole also has a `floor`, and `board("bottom").on(left.toekick.top,
  toward=cab.top)` puts the bottom on the toe kick without repeating its
  height. A name the board has itself (`slot`, `hole`, `front`, `outline`)
  is refused, since `side.slot` would reach the method, never the
  operation [decided]; the language's own default names keep clear of
  them (`openings`, `outline_dogbones`).
- **Operations keep a few keywords.** Position and depth interact and belong
  in one call: `pocket(shape, at=, depth=)`. Splitting them into separate
  modifiers would double the length and lose the grouping.
- **Relations are methods on a part.** `bottom.join(left, right, using=...)`,
  `drawer.mount(...)`, `cab.export(...)`. Methods give autocomplete an entry
  point that free functions lack. A relation names every part it involves;
  nothing is related to whatever happens to touch (see `design/joints.md`).
  [decided]
- **Placement resolves lazily with early errors.** `board("left", ply15)`
  has no position until `.on()`. Using `left.inner` before that errors with
  the part path and the missing fact.
- **Faces and edges are attributes, not only strings.** `side.front` is a
  face, `side.front.inner` an edge, so autocomplete shows the six directions
  and a typo fails at parse time. Strings stay allowed where names are
  computed. Direction names and modifier names do not collide. The six
  directions plus `inner` and `outer` are real properties on boxes, scopes,
  boards and faces, not dynamic attributes, so editors and the type checker
  see them; project aliases such as `fs` go through `face()`, `edge()` and
  `side()`.
- **Strict typing.** The package is checked with pyright in strict mode and
  ships a `py.typed` marker, so build files get completion and errors in the
  editor. Positions, sides, faces, anchor and depth specs and the layout
  file are all typed; the layout file's shape lives in `layout_types.py` and
  is the contract the emitter is checked against. A hardware object's
  `mount` names its parts as typed keywords, which `cab.mount(hardware,
  ...)` passes on through a ParamSpec, so `cab.mount(hinge, dor=door)` is a
  type error like a missing `using=`; `pocket()` and `hole()` take `depth=`
  as a required keyword; a misspelt method on a board is an `Operation` to
  the checker, which then reports the call. `tests/typing_checks.py` lists
  what pyright must reject (each line carries a `# type: ignore` that
  pyright reports once it is no longer needed). `cab.<name>` (parts, child
  scopes, exports) stays untyped, since an export can be any value;
  `cab.part(name)` is the typed form.
- **Two layouts on the page, one object.** A chain in parentheses for a few
  calls; a `with board(...) as side:` block when a part has many operations,
  so the receiver is not repeated. Both build the same part. An operation
  that names a point or an edge of the part needs the part's name, so a part
  with operations is written as a block or assigned first.
- **Direction names on a scope are its box sides.** `cab.left` is the side
  of the module's box, also after a part named `left` exists, because
  carcass parts are routinely named after directions and
  `board("left").on(cab.left)` must read naturally. Parts with such names
  are reached as `cab["left"]`; other names resolve to parts, child scopes
  and exports. An export cannot take a part's name.
- **`at=` is an anchor named through its face.**
  `side.inner.front(37).bottom(z)` is 37 mm behind the front edge of the
  inner face at the position `z`; `side.outer.bottom.front` is a corner;
  `side.front.right(50)` is a point on a narrow face, centred in the
  thickness because the thickness axis is not named. A number measures from
  the edge it follows, a position is taken as it is, an unnamed axis stays
  centred. The anchor also says which face the operation is on, so there is
  no `face=`. Strings and bare direction names were rejected: no
  autocomplete, and carcass parts are named after directions, so
  `bottom.front` would read as a face of the bottom board. [decided]
- **Strings are names or lookups.** Strings in the API are either names
  checked as literals by the type checker (`width`/`depth`/`height`,
  `"inner"`/`"outer"` in `show()` and `to()`, catalogue names such as
  `"4x20"`) or lookups for computed names (`box.side(name)`,
  `part.face(name)`); everything else is an object: box sides
  (`show(cab.front)`, `on(pos, toward=cab.top)`, `grain(cab.top)`), faces,
  edges, anchors, operations. Side keywords (`shrunk(left=5)`,
  `with_sides(front=...)`, `Box.from_sides(...)`) are explicit parameters,
  so a misspelt side is a type error. `shrunk()` and `grown()` also take a
  leading amount for all six sides, which a side's keyword overrides:
  `shrunk(GAP / 2)`, `grown(0.5, front=0)`; keywords alone move their
  sides only [decided by Florian, 2026-10-15, syntax.md item 5]. Enums instead of literals were
  considered and dropped: Python has no `.height` shorthand, catalogue names
  such as "4x20" or "8 M6" cannot be identifiers, and pyright completes a
  `Literal`'s values once the quote is open (an enum parameter got the whole
  scope). Since the preview builds without the type checker, every such
  value is also checked at run time (`errors.one_of`, reading the allowed
  values from the `Literal`), so a misspelling is a `LangError` naming the
  call and the choices; tests keep the connector literals equal to
  `lib/connector_data.py`.
- What this is not: free functions for everything (no autocomplete entry
  point), operators such as `left @ cab.left` (cryptic), or dataclass specs
  (that is what the layout JSON is for, and the language should not look
  like it).

## Names and paths

- Every object has a path, for example
  `kitchen.drawercab.drawer2.left.front.inner`. Code runs inside a scope, so
  only the tail is written. Parts register in the current scope under their
  name, so `d.face` works without assigning it. [decided]
- Mapping to Fusion [decided]:
  - scopes (module, sub-assembly) are nested components;
  - a board is a body inside its module's component, not a component of its
    own (Florian does not rely on Fusion's parts list or on drawings per
    part); bodies are named by path, which is also the part label at the
    machine;
  - bought parts are bodies in components of their own, drawn as boxes (see
    `design/hardware.md`).
- A face of a part is named by direction. An edge is named by two faces
  (`front.inner`), a corner by three. This is the scheme BOSL2 uses for
  anchors.
- Global directions are the primary face names everywhere (`left.right` is
  the inner face of the left side). `inner` and `outer` are sugar that
  resolves only when unambiguous; a shelf at mid height has two inner faces
  and errors.
- Each board has a `show` face, the visible one, which decides the machine
  side and the chamfer side: what `show()` names, else the outer face, else,
  for a board across its scope's middle, the face toward the scope's top,
  else its back, else its right, named in the scope's own terms [decided].
  `show()` is frozen once the show face is used, not when the placement is,
  so `side.show(side.inner)` works.
- Geometry made by an operation takes the operation's name
  (`left.toekick.top`).
- The language's naming is structural, by construction. Finding named faces
  on hand-modeled bodies is a separate tool (see
  `design/proposals/copy-path.md`), whose heuristics do not leak into the
  language.

## Frames

- The world frame is defined once per project: front is -x (toward the
  vehicle's front), left is -y (the driver's side), top is +z, as in the
  Planung document. Aliases are possible (`fs`, `bfs` for driver and
  passenger side). [decided] Which world axis is front, left or up is chosen
  in the build file with `set_frame(Frame(...))`; every build starts from
  the default frame (`registry.reset()` restores it) and `world_frame()`
  reads the frame in use.
- A cabinet is written in its own frame and placed: `cabinet(name, box,
  front=box.right)` makes it open toward the box's right side; top stays up,
  left and right are a cabinetmaker's, standing in front of it;
  `mirrored=True` swaps them. Inside, `cab.back`, `side.inner.front(37)`,
  `rect(depth=...)` and `width`, `depth`, `height` are the module's own,
  child scopes inherit the frame, and the layout file carries world names,
  so the preview and the emitter never see module frames. A cabinet type is
  written once and placed on either wall, rotated or mirrored. [decided]
- `front=` is what makes a module a cabinet, and the constructor says so
  [decided]: `cabinet(name, box, front=...)` with `front=` required, and
  `module(name, box)` for van-level modules such as the floor, the ceiling
  or wall panels, which take the enclosing frame as it is, in the van's own
  terms, the driver's left. `module(..., front=)` is an error pointing to
  `cabinet()`, and `cabinet()` refuses a front facing up or down. A cabinet
  says which way it opens, also when that is the van's front
  (`front=box.front`): seen from its front, a module in the van's terms that
  opens toward the windshield has its left on the right, since one front
  cannot serve a left measured facing it (the driver's) and one measured
  looking at it (the cabinetmaker's).
- Hardware is placed by the drawer's or door's own left and right, seen from
  its front, so it comes out the same in either kind of module and is never
  mirrored.
- Mirroring is a placement option of a module (`mirrored=True`) and nothing
  more: mirrored parts come out of the layout step like any other. [decided]
