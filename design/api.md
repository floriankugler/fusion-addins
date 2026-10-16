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
of SwiftUI and jQuery. `board("left", ply15)` names a part and its material
(`board("left")` takes its scopes', Settings below); where it sits and what
is done to it are method calls that return the part, so they chain or stand
on their own lines. [decided] Everything a build
file makes comes from a lowercase factory: parts (`board()`, `slat()`),
materials (`sheet_material()`), joints (`cabineo()`) and hardware
(`drawer_slide()`, `hinge()`); the classes behind them (`Board`,
`DrawerSlide`) are exported for annotations [decided by Florian,
2026-10-15, syntax.md item 9].

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
  file are all typed, a side or a face plus a number among the type errors
  (a position with a direction moves by `into()` and `gap()`,
  `design/placement.md`) [decided by Florian, 2026-10-15, syntax.md item
  1]; the layout file's shape lives in `layout_types.py` and
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
  centred, on the face or, with `center(pos)`, on a position:
  `b.front.top.center(line)` centres a notch on `line` along the top edge
  [decided by Florian, 2026-10-15, syntax.md item 6]. The anchor also says
  which face the operation is on, so there is no `face=`. Strings and bare
  direction names were rejected: no autocomplete, and carcass parts are
  named after directions, so `bottom.front` would read as a face of the
  bottom board. [decided]
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
  like it). 2D booleans are the exception to the operators: `a - b` and
  `a + b` on shapes, as shapely, CadQuery and build123d users expect
  [decided by Florian, 2026-10-15, syntax.md item 13].

## Settings

The values a build standardizes (a material, a chamfer size, the nest's,
later the CAM's) flow down the build as settings, set once where they
apply and overridden below, as SwiftUI's environment does [Florian,
2026-10-16]. Code: `lang/core/settings.py`, the core's keys in
`lang/core/keys.py`, the nest's in `lang/nesting/keys.py`; what is still
to come (the CAM keys, pinning) in `design/proposals/settings.md`.

- **Keys.** `setting(default, name)` makes a typed key where the code that
  reads it lives: `drawer_gap = setting(3.0, "drawer_gap")` is a
  `Setting[float]`. `setting(..., name)` makes one without a default, typed
  by its annotation (`front_gap: Setting[float] = setting(..., "front_gap")`),
  and reading it where nothing uses it is an error naming the key and how
  to set it. A key called with a value is a binding, `drawer_gap(2.5)`,
  checked when it is made; bindings travel in lists (`use(*house)`).
- **Using.** `use(*bindings)` uses them on the scope whose `with` block is
  being written, outside every module on the root; `cab.use(...)`,
  `part.use(...)` and `part.toekick.use(...)` on a scope, a part or a named
  operation in hand, each returning it. A node uses a key once, and a
  `use()` that is refused uses none of its bindings.
- **Reading.** `value(key)` where the call is, and `cab.value(key)`,
  `part.value(key)`, `part.toekick.value(key)` from a node's point of
  view: the nearest node along the chain that uses the key (the operation,
  the part, its scopes innermost first, the root), else the key's default.
- **Freezing** [proposed in `design/proposals/settings.md`, built so]. A
  read freezes the key for the nodes it passed, from the reader up to the
  node it found the value at: a later use of the key there is an error
  naming the reader and its line, since what was read would no longer
  hold. A use above that node is no error, as the reader does not see it.
  Settings written at the top of a scope never meet it. Keys nothing reads
  during the build (`nest`, `grain`, the nest's keys) are never frozen.
- **A keyword is a binding on the node the call makes** [decided
  2026-10-16]: `board("back", ply9)` uses `material(ply9)` on the board,
  `chamfer(what, 0.5)` gives the chamfer its own size, `nest(False)` and
  `grain()` on a board use those keys there. A key that replaces a required
  argument has no default: `chamfer(what)` with no `chamfer_size` used
  above it is an error naming the key, as a missing size was, so a build
  opts into a standard with a line that says so.
- **One spelling per key per node** [decided 2026-10-16]: a board says its
  material, grain and nest with its own call and modifiers, and
  `board.use()` refuses those keys, naming the spelling; `.use()` on a
  board or an operation is for keys no call there has a keyword for.
- **The core's keys** are exported bare from `lang`; the others come from
  their packages, named by domain (`nesting.margin`, later `cam.tabs`), and
  the layout and provenance write a key's full name (`nesting.margin`)
  [decided 2026-10-16]:
  - `material`, no default: a board without one of its own takes the
    nearest one used above it, read when its placement resolves, and none
    along its chain is an error. A slat names its own and takes none.
  - `grain`, unset: what `grain()` takes, an extent read in the frame of
    the node that uses it (`use(grain("depth"))` in a module opening
    sideways is its depth). It applies to the boards of a grained material
    that have no `grain()` of their own; one along a board's thickness is
    an error naming where it came from. A slat's runs along its length.
  - `nest`, True: `use(nest(False))` keeps every board under a scope out of
    the nest, and `nest(True)` takes one back in.
  - `chamfer_size`, no default: the size of a chamfer that gives none,
    read where the chamfer is written.
- **The nest's keys**, from `lang.nesting` (`from lang import nesting`, or
  `nesting` with `from lang import *`), each with the default the nest had
  before they were settings: `bed` (no default: a nest with none used for
  it or its parts is refused), `kerf` 4, `max_cuts` 5, `spacing` 10,
  `margin` 10, `keep_across` 300 and `keep_area` 0.25 (m²), `seconds` 40,
  `rate` 0.6 s a part and `least_seconds` 5 (the nest's time per material),
  `refill` True. The machine's are used at the root (`use(nesting.bed((2000,
  1000)))`), a deviation on a module, a part or a nest. Nothing reads them
  during the build; the nest step reads them from the layout: a nest's own,
  else its parts' (each along its own chain), else the default. A key a
  nest needs one value of (all but `spacing`) is refused when its parts
  give two, naming two parts, their values and where each came from;
  between two parts the larger of their spacings holds
  (`design/nesting.md`, What is nested).
- **The master's parameters** become settings where the build's index of
  the master binds them: `spalt = van.setting("Spalt")` (`design/master.md`).
- **Provenance.** The layout carries per part the settings set along its
  chain as they hold for it, each with the node that set it (`settings`;
  values that are not JSON data are left out), the keys it read whose
  default came from the master ("master: Spalt"), and its named
  operations' own (`op_settings`). The preview lists them with the
  selected part's info: `material birch 15: kitchen`.

## Modules

- `with module(name, box, front=None)` writes a module's body in place, as
  the root's is. [decided]
- A module type is a function that takes its scope, made with `@module`
  [decided 2026-10-16: one word for one thing]:

  ```python
  @module
  def kitchen(cab: Scope, *, drawers: int = 3) -> None:
      use(material(ply15))
      left = board("left").on(cab.left)
      ...

  kitchen_box = van.box("Kueche")
  k = kitchen(kitchen_box, front=kitchen_box.right, drawers=4).use(chamfer_size(0.5))
  ```

  The call is a constructor, `kitchen(box, front=None, name=None,
  mirrored=False, **the body's keywords)`, typed through a ParamSpec, and
  returns the module's scope, named after the function unless `name=`
  says otherwise. The body's own parameters are keywords after the scope
  (a positional one, or one called `box`, `front`, `name` or `mirrored`,
  is an error), and they change what the module is, where settings change
  how its parts are made [decided 2026-10-16].
- **Lazy, as boards are** [proposed in `design/proposals/settings.md`, built
  so]. The call fixes the module's parent (the scope current at it), path,
  box and frame; its body runs once, the first time its parts are needed:
  a part, child scope or export by name (`k.worktop`, `k["left"]`), its
  parts, a check, the layout, `with k:`, at the latest when the build file
  has run. Its box's sides (`k.left`) need no body. So `.use()` on what
  the call returns comes first, and settings the parent uses after the
  call still apply; a use of a key the body read is the freezing error.
  A body returns nothing (it is an error if it does) and publishes what
  others need with `export()`.

## Nests

- `cab.nest(name, material=ply15)` declares a nest on a module or scope,
  like `cab.check()`: the boards of that material in it that are nested
  (`nest` True, not manual), its sub-scopes' too but not those of a module
  inside it, which has nests of its own; made before or after the call,
  as they are taken when the layout is written. `cab.nest(name, [front1,
  front2])` takes the boards named, anywhere in the scope, so a root
  module's nest may name boards of several modules (`van.nest("remake",
  [k["left"], b["front"]])`); a `nest(False)` board named is its own blank,
  sawn to size, and a slat or a manual board is refused. It is a method
  only, so the name `nest` stays the boards' key [decided by Florian
  2026-10-16]. Code: `lang/core/nests.py`.
- The name is unique in its module (a module inside it has names of its
  own) and holds no dot, slash or space at its ends; the nest's path is its scope's and its name (`kitchen.carcass`),
  its files go to `out/<build>/<module>/<name>/`. A board is in one nest
  of its module at most (a nest around it, a remake, may name it again).
- What returns is the nest, a node of the settings' chain under its scope:
  `.use(*bindings)` for its own values (`carcass.use(nesting.margin(15))`,
  another bed for a nest cut on another machine; the boards' `material`,
  `grain` and `nest` are refused), `.value(key)` its own, else its scope's
  chain's, `.parts` its boards as the build stands.
- What no declared nest of its module takes makes a nest per material per
  module (a top-level scope that is no module counts as one, boards
  outside every scope make the root's), named after the material's label
  made file-safe (`kitchen.birch_15`): a build that declares none nests
  each module by material, and a board a remake around its module names
  stays in its module's nest too. A declared nest that would take the default's name is an
  error, and one that takes no board a problem in the layout.
- The layout (version 8) lists each module's nests, declared and default:
  path, module, how the parts were chosen, the material, the parts' paths,
  the boards of its material in its scope left out (`nest(False)`,
  manual), and the nest's own settings with their source; and the sheet
  materials by label with their sizes (`sheet_materials`), two materials
  of one label being an error. The stock on hand is not a setting: it is
  the inventory, `inventory.toml` beside the build file
  (`design/nesting.md`, Running it).

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
- The machining face, the big face that faces up on the machine (the
  layout's `machine`, which the nest lays up): what `machine()` names, taking
  what `show()` takes (`side.machine(side.inner)`, `machine(cab.left)`,
  `machine("outer")`); else the big face more pockets, holes and chamfers
  are made from (a cut's chamfer counts for the show face), else the show
  face. `machine()` changes no shape and only the layout reads it, so it
  comes at any time, once, like `nest()`; a narrow face is refused, and a
  slat is not machined [decided 2026-10-15].
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
- A cabinet is a module written in its own frame and placed:
  `module(name, box, front=box.right)` makes it open toward the box's right
  side; top stays up, left and right are a cabinetmaker's, standing in
  front of it; `mirrored=True` swaps them. Inside, `cab.back`,
  `side.inner.front(37)`, `rect(depth=...)` and `width`, `depth`, `height`
  are the module's own, child scopes inherit the frame, and the layout file
  carries world names, so the preview and the emitter never see module
  frames. A cabinet type is written once and placed on either wall,
  rotated or mirrored. [decided]
- `front=` is what makes a module a cabinet [decided 2026-10-12; one
  constructor since 2026-10-16, `module()` having taken over from
  `cabinet()`]: `module(name, box)` without it for van-level modules such
  as the floor, the ceiling or wall panels, which take the enclosing frame
  as it is, in the van's own terms, the driver's left; `front=` a side of
  the box or a direction, never up or down. A cabinet says which way it
  opens, also when that is the van's front (`front=box.front`): seen from
  its front, a module in the van's terms that opens toward the windshield
  has its left on the right, since one front cannot serve a left measured
  facing it (the driver's) and one measured looking at it (the
  cabinetmaker's).
- Hardware is placed by the drawer's or door's own left and right, seen from
  its front, so it comes out the same in either kind of module and is never
  mirrored.
- Mirroring is a placement option of a module (`mirrored=True`) and nothing
  more: mirrored parts come out of the layout step like any other. [decided]
