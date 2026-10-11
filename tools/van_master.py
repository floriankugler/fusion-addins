"""Builds the sample master document for examples/van.py in a new Fusion
document. Its snapshot is examples/van_snapshot.json; rebuild the document
with this script instead of keeping a saved copy.

Run it from Scripts and Add-Ins, or through the Fusion MCP server by loading
this file with importlib and calling `build()`. The text stays ASCII because
the MCP transport mangles other characters.

What it holds (world mm; front is -x, the driver's side -y, top +z):

- user parameters Bodenaufbau (floor build-up), Lattenabstand (batten
  pitch), Kuechenhoehe (kitchen height), Neigung (an angle);
- construction planes Bodenniveau (top of the floor), Boden vorne and Boden
  hinten (where the battens start and end), Wand FS (the driver's-side
  wall) and Dach geneigt (tilted, so not a position);
- sketches Bodenumriss (floor outline with both wheel arches, closed),
  Bodenprofil (cross-section of the ribbed vehicle floor, open), Fenster
  (two rectangles: not one chain) and __Hilfsskizze plus the sketches
  behind the bodies (all left out of the snapshot by their names);
- placeholder boxes Boden, Moebel.Kueche (a component inside the empty
  component Moebel), Bett (a moved component with the plane Bett.oben and
  the one-line sketch Bett.Kante of its own), Radkasten FS (filleted, so
  not a cuboid) and the component Sitzbank with the two bodies Sitz and
  Lehne (Sitzbank.Sitz, Sitzbank.Lehne).
"""
import math

import adsk.core
import adsk.fusion

MM = 0.1   # cm per mm

#: The cargo floor: x from the partition to the rear doors, y across.
LENGTH, HALF_WIDTH = 3400.0, 890.0
#: Wheel arches: along x, reaching this far in from the walls.
ARCH_X, ARCH_DEPTH, ARCH_RADIUS = (2000.0, 2900.0), 215.0, 50.0
#: Floor ribs: valley centres across the vehicle, valley depth and widths.
VALLEYS, VALLEY_DEPTH, VALLEY_BOTTOM, VALLEY_TOP = (-600.0, -300.0, 0.0, 300.0, 600.0), 8.0, 60.0, 76.0


def _p(x, y, z=0.0):
    return adsk.core.Point3D.create(x * MM, y * MM, z * MM)


def _v(expression):
    return adsk.core.ValueInput.createByString(expression)


def _fillet_points(corners, radius):
    """A closed polygon with every corner rounded: a list of ('line', a, b)
    and ('arc', a, mid, b) pieces in (x, y)."""
    n = len(corners)
    pieces = []
    tangents = []
    for i, c in enumerate(corners):
        prev, nxt = corners[i - 1], corners[(i + 1) % n]
        a = (c[0] - prev[0], c[1] - prev[1])
        b = (nxt[0] - c[0], nxt[1] - c[1])
        la, lb = math.hypot(*a), math.hypot(*b)
        a, b = (a[0] / la, a[1] / la), (b[0] / lb, b[1] / lb)
        r = radius(c)
        if r == 0:
            tangents.append((c, None, c))
            continue
        t1 = (c[0] - a[0] * r, c[1] - a[1] * r)
        t2 = (c[0] + b[0] * r, c[1] + b[1] * r)
        left = a[0] * b[1] - a[1] * b[0] > 0
        normal = (-a[1], a[0]) if left else (a[1], -a[0])
        o = (t1[0] + normal[0] * r, t1[1] + normal[1] * r)
        d = (c[0] - o[0], c[1] - o[1])
        ld = math.hypot(*d)
        mid = (o[0] + d[0] / ld * r, o[1] + d[1] / ld * r)
        tangents.append((t1, mid, t2))
    for i in range(n):
        t1, mid, t2 = tangents[i]
        if mid is not None:
            pieces.append(("arc", t1, mid, t2))
        pieces.append(("line", t2, tangents[(i + 1) % n][0]))
    return pieces


def _floor_outline(sketch):
    x0, x1 = ARCH_X
    w, a = HALF_WIDTH, HALF_WIDTH - ARCH_DEPTH
    corners = [(0, -w), (x0, -w), (x0, -a), (x1, -a), (x1, -w), (LENGTH, -w),
               (LENGTH, w), (x1, w), (x1, a), (x0, a), (x0, w), (0, w)]
    arch_corners = {(x0, -w), (x0, -a), (x1, -a), (x1, -w), (x1, w), (x1, a), (x0, a), (x0, w)}
    pieces = _fillet_points(corners, lambda c: ARCH_RADIUS if c in arch_corners else 0.0)
    lines = sketch.sketchCurves.sketchLines
    arcs = sketch.sketchCurves.sketchArcs
    for piece in pieces:
        if piece[0] == "line":
            _, p, q = piece
            if math.dist(p, q) > 1e-9:
                lines.addByTwoPoints(_p(*p), _p(*q))
        else:
            _, p, m, q = piece
            arcs.addByThreePoints(_p(*p), _p(*m), _p(*q))


def _floor_profile(sketch):
    """Across the vehicle at x = 0: rising 15 mm into each wall, ribbed in
    between, as (y, z) in model space."""
    w = HALF_WIDTH
    points = [(-w + 30, 0.0)]
    for c in VALLEYS:
        points += [(c - VALLEY_TOP / 2, 0.0), (c - VALLEY_BOTTOM / 2, -VALLEY_DEPTH),
                   (c + VALLEY_BOTTOM / 2, -VALLEY_DEPTH), (c + VALLEY_TOP / 2, 0.0)]
    points.append((w - 30, 0.0))

    def sk(y, z):
        return sketch.modelToSketchSpace(_p(0, y, z))

    lines = sketch.sketchCurves.sketchLines
    arcs = sketch.sketchCurves.sketchArcs
    arcs.addByThreePoints(sk(-w, 15), sk(-w + 12, 3.5), sk(-w + 30, 0))
    for (ya, za), (yb, zb) in zip(points, points[1:]):
        lines.addByTwoPoints(sk(ya, za), sk(yb, zb))
    arcs.addByThreePoints(sk(w - 30, 0), sk(w - 12, 3.5), sk(w, 15))


def _component(parent, name, transform=None):
    occurrence = parent.occurrences.addNewComponent(transform or adsk.core.Matrix3D.create())
    occurrence.component.name = name
    return occurrence.component


def _block(comp, name, lo, hi, distance, start=None):
    """A box body: a rectangle on the component's XY plane, extruded by
    `distance` from `start` (expressions). The sketch is only a means to
    the body, so its name starts with __ and the snapshot leaves it out."""
    sketch = comp.sketches.add(comp.xYConstructionPlane)
    sketch.name = "__" + name
    sketch.sketchCurves.sketchLines.addTwoPointRectangle(_p(lo[0], lo[1]), _p(hi[0], hi[1]))
    extrudes = comp.features.extrudeFeatures
    inp = extrudes.createInput(sketch.profiles.item(0),
                               adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    inp.setDistanceExtent(False, _v(distance))
    if start is not None:
        inp.startExtent = adsk.fusion.OffsetStartDefinition.create(_v(start))
    feature = extrudes.add(inp)
    feature.name = name
    body = feature.bodies.item(0)
    body.name = name
    return body


def build(app=None):
    """Creates the sample master in a new document and returns its design."""
    app = app or adsk.core.Application.get()
    app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
    design = adsk.fusion.Design.cast(app.activeProduct)
    design.designType = adsk.fusion.DesignTypes.ParametricDesignType
    root = design.rootComponent

    params = design.userParameters
    params.add("Bodenaufbau", _v("40 mm"), "mm", "floor build-up: vehicle floor to the top of the floor")
    params.add("Lattenabstand", _v("400 mm"), "mm", "batten pitch")
    params.add("Kuechenhoehe", _v("720 mm"), "mm", "kitchen carcass height")
    params.add("Neigung", _v("10 deg"), "deg", "roof slope")

    planes = root.constructionPlanes

    def offset_plane(base, expression, name):
        inp = planes.createInput()
        inp.setByOffset(base, _v(expression))
        plane = planes.add(inp)
        plane.name = name
        return plane

    offset_plane(root.xYConstructionPlane, "Bodenaufbau", "Bodenniveau")
    offset_plane(root.yZConstructionPlane, "20 mm", "Boden vorne")
    offset_plane(root.yZConstructionPlane, "3380 mm", "Boden hinten")
    offset_plane(root.xZConstructionPlane, "-890 mm", "Wand FS")
    tilted = planes.createInput()
    tilted.setByAngle(root.xConstructionAxis, _v("Neigung"), root.xYConstructionPlane)
    planes.add(tilted).name = "Dach geneigt"

    outline = root.sketches.add(root.xYConstructionPlane)
    outline.name = "Bodenumriss"
    _floor_outline(outline)

    profile = root.sketches.add(root.yZConstructionPlane)
    profile.name = "Bodenprofil"
    _floor_profile(profile)

    windows = root.sketches.add(root.xZConstructionPlane)
    windows.name = "Fenster"
    for x0 in (500.0, 1500.0):
        a = windows.modelToSketchSpace(_p(x0, 0, 900))
        b = windows.modelToSketchSpace(_p(x0 + 700, 0, 1400))
        windows.sketchCurves.sketchLines.addTwoPointRectangle(a, b)

    helper = root.sketches.add(root.xYConstructionPlane)
    helper.name = "__Hilfsskizze"
    helper.sketchCurves.sketchLines.addByTwoPoints(_p(0, 0), _p(100, 100))

    # Placeholder boxes, one component each.
    _block(_component(root, "Boden"), "Boden", (0, -HALF_WIDTH), (LENGTH, HALF_WIDTH), "Bodenaufbau")
    furniture = _component(root, "Moebel")
    _block(_component(furniture, "Kueche"), "Kueche", (300, -HALF_WIDTH), (900, -390), "Kuechenhoehe",
           start="Bodenaufbau")

    move = adsk.core.Matrix3D.create()
    move.translation = adsk.core.Vector3D.create(2300 * MM, -HALF_WIDTH * MM, 900 * MM)
    bed = _component(root, "Bett", move)
    _block(bed, "Bett", (0, 0), (1100, 2 * HALF_WIDTH), "100 mm")
    bed_top = bed.constructionPlanes.createInput()
    bed_top.setByOffset(bed.xYConstructionPlane, _v("100 mm"))
    bed.constructionPlanes.add(bed_top).name = "oben"
    edge = bed.sketches.add(bed.xYConstructionPlane)
    edge.name = "Kante"
    edge.sketchCurves.sketchLines.addByTwoPoints(_p(0, 0), _p(1100, 0))

    arch = _component(root, "Radkasten FS")
    body = _block(arch, "Radkasten FS", (ARCH_X[0], -HALF_WIDTH), (ARCH_X[1], -HALF_WIDTH + ARCH_DEPTH), "250 mm")
    inner_top = [e for e in body.edges
                 if all(abs(v.geometry.y - (-HALF_WIDTH + ARCH_DEPTH) * MM) < 1e-6
                        and abs(v.geometry.z - 250 * MM) < 1e-6 for v in (e.startVertex, e.endVertex))]
    edges = adsk.core.ObjectCollection.create()
    edges.add(inner_top[0])
    fillet = arch.features.filletFeatures.createInput()
    fillet.edgeSetInputs.addConstantRadiusEdgeSet(edges, _v("150 mm"), True)
    arch.features.filletFeatures.add(fillet)

    bench = _component(root, "Sitzbank")
    _block(bench, "Sitz", (1000, 390), (1600, HALF_WIDTH), "400 mm", start="Bodenaufbau")
    _block(bench, "Lehne", (1000, HALF_WIDTH - 100), (1600, HALF_WIDTH), "460 mm", start="Bodenaufbau + 400 mm")

    app.activeViewport.fit()
    return design


def run(context):
    build()
