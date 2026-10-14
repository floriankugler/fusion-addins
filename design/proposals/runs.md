# Runs: tubes, ducts and keep-outs

Status: proposed, nothing built. Wanted by Florian (water hoses, cable runs,
ducts, keep-outs); the design below is Claude's and not yet looked at with
him.

Water tubes and wiring ducts are planned alongside the furniture so that
there is room for them and they are organised. By hand this is a 3D sketch of
the centre line and a shape swept along it. In the language a run is a
primitive. [decided as a need]

- A **run** has a name, a cross-section, a clearance and a path.
  Constructors: `tube(name, d, bend_r)` is round and bends with a radius;
  `duct(name, w, h)` is rectangular and turns sharp; `keepout(name, w, h)`
  reserves room for something not modeled yet. `.clearance(n)` and
  `.path(...)` are modifiers, like a board's. Runs appear in the cut list by
  length, tubes with their bend count.
- **Paths are waypoints that change only what they name.** Each waypoint
  states one, two or three coordinates; the others carry over from the
  previous point. One coordinate is an axis-aligned leg, which is nearly
  every leg of a real run; two is a diagonal. Every coordinate is a reference
  from the position algebra, so a waypoint reads like a board limit. Routing
  is manual: the source states the waypoints, the language checks them.
  Automatic routing is out of scope.
- **`along(face, gap)`** is what makes a run follow a component. It pins the
  centre line at the face plus gap plus half the cross-section on that axis
  for the legs that follow, until the next `along` or an explicit coordinate
  overrides it. For ducts it also sets the orientation: the flat side lies
  parallel to the face. Two faces run the duct in a corner. Moving the panel
  moves the run; the gap is checked, not assumed.
- **Crossings produce holes.** Where a run passes through a board, the layout
  step adds the pass-through to that board as an operation: a hole of
  diameter plus clearance for a tube, a rectangular cutout for a duct, at the
  crossing point and angle. `through=` overrides the automatic rule where a
  grommet or bulkhead fitting needs something else.
- **Checks.** Runs are first class for interference and clearance: against
  boards, other runs and the vehicle mesh. Tubes check each bend against the
  room available and against the tube type's minimum bend radius. A duct can
  check that its lid side stays reachable. All of this runs in the layout
  step.
- **Across modules, through ports.** A module exports named points where a
  service enters or leaves, and the port itself defines the pass-through in
  that module's board. A systems module imports the ports and routes between
  them. Furniture modules know only their own ports, so the compile order
  stays acyclic. Runs inside a module stay in that module. Spelling
  (rewritten from the first draft's string anchor, which the anchor rule
  replaced): `back.port("cold", at=back.inner.left(60).bottom(80), d=20)`
  declares a port on a board face with the pass-through size; it is exported
  from the module automatically and read as `kitchen.port("cold")`, a point
  with `.x`, `.y`, `.z`.
- **Emit and preview.** A path is straight legs plus torus sections at tube
  corners. Both the mesher and the emitter build a run from cylinders, boxes
  and tori unioned into one body. In Fusion that can be a temporary B-rep
  body added with one write per run. A sweep along a 3D sketch path, the
  manual method, stays as the fallback if the unioned primitives look wrong
  at a bend.

```python
cold = (tube("cold", d=16, bend_r=60)
        .clearance(10)
        .path(
            tank.port("cold"),                     # a point exported by the tank module
            along(kitchen.back.inner, gap=15),     # lateral offset held for the next legs
            via(z=kitchen.top.bottom - 40),        # one coordinate: an axis-aligned leg
            via(x=sink.port("cold").x),
            sink.port("cold"),
        ))
```

A path is a positional sequence whose first and last entries are points.
Waypoints are `via(...)`, not `to(...)`, because `to(face, offset)` is
already the depth of a cut or hole.

Open:

- Fittings and connectors on tubes.
- Whether a duct needs a lid part of its own for the cut list.
- How a run crossing a board at an angle is cut.
- `via(z=...)` takes world axis letters, which build files otherwise avoid
  (see `design/placement.md`); it should probably name sides instead [noted
  while restructuring the design docs].
