"""Compile-speed benchmark for the modeling-language compiler (see DESIGN.md).

Builds a synthetic module out of joint-bearing board pairs with Fusion's own
features and times every API call. One "pair" is a tenon board A (outline
with six tenons, chamfer on the top-face edges) and a mating board B (six
slot mortises cut from its top face, eight holes and one pocket on the top
face, two holes into a narrow face). That is roughly fifteen features and
sixty sketch entities per pair, which is close to what the compiler's
generic emitter would produce for real cabinet parts.

Runs inside Fusion's Python. Driven from an MCP script execution, one cell
per execution, for example:

    import importlib.util, json
    spec = importlib.util.spec_from_file_location(
        'compile_bench', '<repo>/tools/perf/compile_bench.py')
    bench = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bench)

    def run(_context):
        print(json.dumps(bench.run_cell({
            'label': 'param_b_t_d_p15', 'design': 'parametric',
            'pairs': 15, 'batched': True, 'outline': 'tenons',
            'extent': 'distance', 'sketch_deferred': False,
            'profile_source': 'sketch', 'out_dir': '<dir>'}), indent=1))

The cell leaves its document open and active; close it afterwards. Results
go to <out_dir>/<label>.json; tools/perf/plot_bench.py plots them.

Do not define a function named `run` in this module: the MCP runner calls
any global `run` at the end of every later execution.
"""
import gc
import json
import math
import os
import time

import adsk.core
import adsk.fusion

# Geometry in cm (the API unit). Boards are 600 x 300 mm, 15 mm thick.
BOARD_W = 60.0
BOARD_H = 30.0
THICKNESS = 1.5
TENON_COUNT = 6
TENON_W = 4.0
SLOT_L = 4.2
SLOT_W = 1.6
HOLE_D = 0.5
HOLE_DEPTH = 1.0
HOLE_COUNT = 8
POCKET_DEPTH = 0.5
CHAMFER = 0.1
PAIR_SPACING_Z = 5.0

DEFAULTS = {
    'label': 'cell',
    'design': 'parametric',     # 'parametric' | 'direct'
    'pairs': 5,
    'batched': True,            # one feature per hole/profile when False
    'outline': 'tenons',        # 'tenons' | 'plain'
    'extent': 'distance',       # mortise cut: 'distance' | 'to_object'
    'sketch_deferred': False,   # Sketch.isComputeDeferred while drawing
    'profile_source': 'sketch', # board A outline: 'sketch' | 'brep'
    'out_dir': None,
}


class Recorder:
    """Times API calls and tags each with the features created so far."""

    def __init__(self):
        self.records = []
        self.features = 0

    def timed(self, kind, fn, is_feature=True, pair=-1):
        t0 = time.perf_counter()
        result = fn()
        dt = time.perf_counter() - t0
        self.records.append({'kind': kind, 'dt': dt, 'n': self.features, 'pair': pair})
        if is_feature:
            self.features += 1
        return result


def _p(x, y, z):
    return adsk.core.Point3D.create(x, y, z)


def _tenon_outline(z):
    """Closed polygon of board A as world points, counter-clockwise.
    Tenons stick out of the top edge (y = BOARD_H) by THICKNESS."""
    pts = [(0.0, 0.0), (BOARD_W, 0.0), (BOARD_W, BOARD_H)]
    pitch = BOARD_W / TENON_COUNT
    for i in reversed(range(TENON_COUNT)):
        x1 = i * pitch + (pitch + TENON_W) / 2.0
        x0 = x1 - TENON_W
        pts += [(x1, BOARD_H), (x1, BOARD_H + THICKNESS),
                (x0, BOARD_H + THICKNESS), (x0, BOARD_H)]
    pts.append((0.0, BOARD_H))
    return [_p(x, y, z) for x, y in pts]


def _plain_outline(z):
    return [_p(0, 0, z), _p(BOARD_W, 0, z), _p(BOARD_W, BOARD_H, z), _p(0, BOARD_H, z)]


def _face_with_normal(body, nx, ny, nz):
    """The outermost planar face of `body` whose plane is perpendicular to
    the direction. A plane's `normal` is not reliably the outward normal
    (it differed between parametric and direct documents), so the face is
    chosen by position: the one farthest along the direction."""
    best, best_pos = None, -1e9
    for face in body.faces:
        plane = adsk.core.Plane.cast(face.geometry)
        if plane is None:
            continue
        n = plane.normal
        if abs(abs(n.x * nx + n.y * ny + n.z * nz) - 1.0) > 1e-6:
            continue
        c = face.centroid
        pos = c.x * nx + c.y * ny + c.z * nz
        if pos > best_pos:
            best, best_pos = face, pos
    return best


def _profiles_by_area(sketch, target_area, tolerance=0.2):
    """Profiles whose area is within `tolerance` (relative) of `target_area`.
    A sketch on a face auto-projects the face's edges, so its profiles also
    include the whole face; this picks out the drawn shapes."""
    found = []
    for i in range(sketch.profiles.count):
        profile = sketch.profiles.item(i)
        area = profile.areaProperties().area
        if abs(area - target_area) <= tolerance * target_area:
            found.append(profile)
    return found


SLOT_AREA = (SLOT_L - SLOT_W) * SLOT_W + math.pi * (SLOT_W / 2.0) ** 2
POCKET_AREA = 20.0 * 1.2


def _face_normal(face):
    """Outward normal of a planar face at its centroid, as a tuple."""
    ok, normal = face.evaluator.getNormalAtPoint(face.centroid)
    if not ok:
        raise RuntimeError('no normal for face')
    return (normal.x, normal.y, normal.z)


def _direction_toward(profile, into, sketch_normal=None):
    """ExtentDirection that moves a profile along the world vector `into`.
    A sketch profile extrudes along the sketch normal; a B-rep face along
    its own normal, which follows the winding of the wire it was made from."""
    if sketch_normal is not None:
        n = sketch_normal
    else:
        n = _face_normal(profile)
    dot = n[0] * into[0] + n[1] * into[1] + n[2] * into[2]
    return (adsk.fusion.ExtentDirections.PositiveExtentDirection if dot > 0
            else adsk.fusion.ExtentDirections.NegativeExtentDirection)


def _collection(items):
    coll = adsk.core.ObjectCollection.create()
    for item in items:
        coll.add(item)
    return coll


class Builder:
    def __init__(self, cfg, rec):
        self.cfg = cfg
        self.rec = rec
        self.app = adsk.core.Application.get()
        self.design = None
        self.root = None
        self.tmp = adsk.fusion.TemporaryBRepManager.get()

    # -- document --------------------------------------------------------

    def create_document(self):
        doc = self.rec.timed('doc_create', lambda: self.app.documents.add(
            adsk.core.DocumentTypes.FusionDesignDocumentType), is_feature=False)
        self.design = adsk.fusion.Design.cast(self.app.activeProduct)
        wanted = (adsk.fusion.DesignTypes.DirectDesignType
                  if self.cfg['design'] == 'direct'
                  else adsk.fusion.DesignTypes.ParametricDesignType)
        if self.design.designType != wanted:
            def set_type():
                self.design.designType = wanted
            self.rec.timed('design_type', set_type, is_feature=False)
        self.root = self.design.rootComponent
        return doc

    # -- sketch helpers --------------------------------------------------

    def _begin_sketch(self, kind, target, pair):
        sketch = self.rec.timed(kind, lambda: self.root.sketches.add(target), pair=pair)
        if self.cfg['sketch_deferred']:
            sketch.isComputeDeferred = True
        return sketch

    def _end_sketch(self, sketch):
        if self.cfg['sketch_deferred']:
            sketch.isComputeDeferred = False

    def _polyline(self, sketch, world_points, pair):
        lines = sketch.sketchCurves.sketchLines
        local = [sketch.modelToSketchSpace(p) for p in world_points]
        first = self.rec.timed('sketch_line', lambda: lines.addByTwoPoints(local[0], local[1]),
                               is_feature=False, pair=pair)
        prev = first
        for i in range(2, len(local)):
            nxt = self.rec.timed('sketch_line',
                                 lambda: lines.addByTwoPoints(prev.endSketchPoint, local[i]),
                                 is_feature=False, pair=pair)
            prev = nxt
        self.rec.timed('sketch_line',
                       lambda: lines.addByTwoPoints(prev.endSketchPoint, first.startSketchPoint),
                       is_feature=False, pair=pair)

    def _slot(self, sketch, cx, cy, z, pair):
        """Rounded-end slot along x: two lines, two arcs."""
        lines = sketch.sketchCurves.sketchLines
        arcs = sketch.sketchCurves.sketchArcs
        r = SLOT_W / 2.0
        hx = SLOT_L / 2.0 - r
        s = sketch.modelToSketchSpace
        # Fusion normalises arcs to counter-clockwise, so start/end sketch
        # points of an arc cannot be chained from; coincident points suffice
        # for the profile.
        top = self.rec.timed('sketch_line', lambda: lines.addByTwoPoints(
            s(_p(cx - hx, cy + r, z)), s(_p(cx + hx, cy + r, z))), is_feature=False, pair=pair)
        self.rec.timed('sketch_arc', lambda: arcs.addByThreePoints(
            top.endSketchPoint, s(_p(cx + hx + r, cy, z)), s(_p(cx + hx, cy - r, z))),
            is_feature=False, pair=pair)
        bottom = self.rec.timed('sketch_line', lambda: lines.addByTwoPoints(
            s(_p(cx + hx, cy - r, z)), s(_p(cx - hx, cy - r, z))), is_feature=False, pair=pair)
        self.rec.timed('sketch_arc', lambda: arcs.addByThreePoints(
            bottom.endSketchPoint, s(_p(cx - hx - r, cy, z)), top.startSketchPoint),
            is_feature=False, pair=pair)

    def _slot_face(self, cx, cy, z):
        """A rounded-end slot as a temporary planar face body."""
        r = SLOT_W / 2.0
        hx = SLOT_L / 2.0 - r
        curves = [
            adsk.core.Line3D.create(_p(cx - hx, cy + r, z), _p(cx + hx, cy + r, z)),
            adsk.core.Arc3D.createByThreePoints(
                _p(cx + hx, cy + r, z), _p(cx + hx + r, cy, z), _p(cx + hx, cy - r, z)),
            adsk.core.Line3D.create(_p(cx + hx, cy - r, z), _p(cx - hx, cy - r, z)),
            adsk.core.Arc3D.createByThreePoints(
                _p(cx - hx, cy - r, z), _p(cx - hx - r, cy, z), _p(cx - hx, cy + r, z)),
        ]
        wire, _ = self.tmp.createWireFromCurves(curves)
        return self.tmp.createFaceFromPlanarWires([wire])

    def _add_face_bodies(self, face_bodies, pair):
        """Adds temporary face bodies to the component. Parametric designs
        need a base feature (one for all of them); direct designs do not."""
        parametric = self.design.designType == adsk.fusion.DesignTypes.ParametricDesignType
        if parametric:
            def add_base():
                base = self.root.features.baseFeatures.add()
                base.startEdit()
                for fb in face_bodies:
                    self.root.bRepBodies.add(fb, base)
                base.finishEdit()
                # Proxies returned inside the edit session go stale once the
                # edit ends (RemoveFeatures then reports the body lost).
                return [base.bodies.item(i) for i in range(base.bodies.count)]
            return self.rec.timed('base_feature', add_base, pair=pair)
        return [self.rec.timed('brep_add', lambda: self.root.bRepBodies.add(fb),
                               is_feature=False, pair=pair) for fb in face_bodies]

    def _drop_face_bodies(self, bodies, pair):
        """Removes the surface bodies again. In a parametric design a
        RemoveFeature after the consuming extrude is one feature per body;
        in a direct design deleteMe is a plain write."""
        parametric = self.design.designType == adsk.fusion.DesignTypes.ParametricDesignType
        for b in bodies:
            if parametric:
                self.rec.timed('remove_feature',
                               lambda: self.root.features.removeFeatures.add(b), pair=pair)
            else:
                self.rec.timed('body_delete', lambda: b.deleteMe(), is_feature=False, pair=pair)

    # -- features --------------------------------------------------------

    def _offset_plane(self, z, pair):
        planes = self.root.constructionPlanes
        def make():
            inp = planes.createInput()
            inp.setByOffset(self.root.xYConstructionPlane, adsk.core.ValueInput.createByReal(z))
            return planes.add(inp)
        return self.rec.timed('plane', make, pair=pair)

    def _extrude_new(self, profile, distance, pair, kind='extrude_new', direction=None):
        """New body along +z. `direction` is needed for B-rep face profiles,
        whose normal may point either way."""
        extrudes = self.root.features.extrudeFeatures
        def make():
            inp = extrudes.createInput(
                profile, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
            extent = adsk.fusion.DistanceExtentDefinition.create(
                adsk.core.ValueInput.createByReal(distance))
            inp.setOneSideExtent(
                extent, direction or adsk.fusion.ExtentDirections.PositiveExtentDirection)
            return extrudes.add(inp)
        return self.rec.timed(kind, make, pair=pair)

    def _extrude_cut(self, profiles, body, pair, kind, depth=None, to_face=None,
                     direction=adsk.fusion.ExtentDirections.NegativeExtentDirection):
        """Cut into `body`. Sketch profiles on a face extrude along the
        outward sketch normal, so the default direction is negative."""
        extrudes = self.root.features.extrudeFeatures
        def make():
            inp = extrudes.createInput(profiles, adsk.fusion.FeatureOperations.CutFeatureOperation)
            if to_face is not None:
                extent = adsk.fusion.ToEntityExtentDefinition.create(to_face, False)
            else:
                extent = adsk.fusion.DistanceExtentDefinition.create(
                    adsk.core.ValueInput.createByReal(depth))
            inp.setOneSideExtent(extent, direction)
            inp.participantBodies = [body]
            return extrudes.add(inp)
        return self.rec.timed(kind, make, pair=pair)

    def _holes(self, points, body, pair, kind, sketch, into):
        """`into` is the world direction from the sketch face into the body.
        The hole's natural direction is opposite the sketch normal; the
        direction is made explicit as lib/hole_features.py does."""
        holes = self.root.features.holeFeatures
        normal = sketch.xDirection.crossProduct(sketch.yDirection)
        natural = adsk.core.Vector3D.create(-normal.x, -normal.y, -normal.z)
        default_direction = natural.dotProduct(adsk.core.Vector3D.create(*into)) > 0
        def make():
            inp = holes.createSimpleInput(adsk.core.ValueInput.createByReal(HOLE_D))
            inp.setPositionBySketchPoints(_collection(points))
            inp.isDefaultDirection = default_direction
            inp.setDistanceExtent(adsk.core.ValueInput.createByReal(HOLE_DEPTH))
            inp.tipAngle = adsk.core.ValueInput.createByString('180 deg')
            inp.participantBodies = [body]
            return holes.add(inp)
        return self.rec.timed(kind, make, pair=pair)

    def _chamfer(self, face, pair):
        chamfers = self.root.features.chamferFeatures
        def make():
            inp = chamfers.createInput2()
            inp.chamferEdgeSets.addEqualDistanceChamferEdgeSet(
                _collection(list(face.edges)), adsk.core.ValueInput.createByReal(CHAMFER), False)
            return chamfers.add(inp)
        return self.rec.timed('chamfer', make, pair=pair)

    def _name_body(self, body, name, pair):
        def rename():
            body.name = name
        self.rec.timed('body_name', rename, is_feature=False, pair=pair)

    # -- board A: outline + chamfer -------------------------------------

    def _board_a(self, pair, z):
        outline = (_tenon_outline(z) if self.cfg['outline'] == 'tenons' else _plain_outline(z))
        if self.cfg['profile_source'] == 'brep':
            body = self._board_a_brep(outline, pair, z)
        else:
            plane = self._offset_plane(z, pair)
            sketch = self._begin_sketch('sketch_outline', plane, pair)
            self._polyline(sketch, outline, pair)
            self._end_sketch(sketch)
            profile = self.rec.timed('profile_lookup', lambda: sketch.profiles.item(0),
                                     is_feature=False, pair=pair)
            extrude = self._extrude_new(profile, THICKNESS, pair)
            body = extrude.bodies.item(0)
        self._name_body(body, 'pair%d.a' % pair, pair)
        top = _face_with_normal(body, 0, 0, 1)
        self._chamfer(top, pair)
        return body

    def _board_a_brep(self, outline, pair, z):
        """Outline as a temporary B-rep planar face, extruded as the profile."""
        def make_face():
            lines = []
            for i in range(len(outline)):
                a = outline[i]
                b = outline[(i + 1) % len(outline)]
                lines.append(adsk.core.Line3D.create(a, b))
            wire, _ = self.tmp.createWireFromCurves(lines)
            return self.tmp.createFaceFromPlanarWires([wire])
        face_body = self.rec.timed('brep_face', make_face, is_feature=False, pair=pair)
        added = self._add_face_bodies([face_body], pair)
        face = added[0].faces.item(0)
        extrude = self._extrude_new(face, THICKNESS, pair, kind='extrude_new_brep',
                                    direction=_direction_toward(face, (0, 0, 1)))
        body = extrude.bodies.item(0)
        self._drop_face_bodies(added, pair)
        return body

    # -- board B: mortises, holes, pocket, edge holes -------------------

    def _board_b(self, pair, z):
        plane = self._offset_plane(z, pair)
        sketch = self._begin_sketch('sketch_outline', plane, pair)
        self._polyline(sketch, _plain_outline(z), pair)
        self._end_sketch(sketch)
        profile = self.rec.timed('profile_lookup', lambda: sketch.profiles.item(0),
                                 is_feature=False, pair=pair)
        body = self._extrude_new(profile, THICKNESS, pair).bodies.item(0)
        self._name_body(body, 'pair%d.b' % pair, pair)
        top = _face_with_normal(body, 0, 0, 1)
        bottom = _face_with_normal(body, 0, 0, -1)
        side = _face_with_normal(body, -1, 0, 0)
        zt = z + THICKNESS
        batched = self.cfg['batched']

        # Mortises: six slots, either drawn in one sketch on the top face or
        # made as temporary planar faces and extruded as such.
        pitch = BOARD_W / TENON_COUNT
        to_face = bottom if self.cfg['extent'] == 'to_object' else None
        depth = None if to_face is not None else THICKNESS
        slot_bodies = []
        cut_direction = adsk.fusion.ExtentDirections.NegativeExtentDirection
        if self.cfg['profile_source'] == 'brep':
            faces = self.rec.timed('brep_face', lambda: [
                self._slot_face(i * pitch + pitch / 2.0, BOARD_H - 3.0, zt)
                for i in range(TENON_COUNT)], is_feature=False, pair=pair)
            slot_bodies = self._add_face_bodies(faces, pair)
            profiles = [b.faces.item(0) for b in slot_bodies]
            cut_direction = _direction_toward(profiles[0], (0, 0, -1))
        else:
            sk = self._begin_sketch('sketch_mortise', top, pair)
            for i in range(TENON_COUNT):
                self._slot(sk, i * pitch + pitch / 2.0, BOARD_H - 3.0, zt, pair)
            self._end_sketch(sk)
            profiles = self.rec.timed('profile_lookup', lambda: _profiles_by_area(sk, SLOT_AREA),
                                      is_feature=False, pair=pair)
            if len(profiles) != TENON_COUNT:
                raise RuntimeError('expected %d slot profiles, found %d' % (TENON_COUNT, len(profiles)))
        if batched:
            self._extrude_cut(_collection(profiles), body, pair, 'extrude_cut_mortise',
                              depth=depth, to_face=to_face, direction=cut_direction)
        else:
            for pr in profiles:
                self._extrude_cut(pr, body, pair, 'extrude_cut_mortise', depth=depth,
                                  to_face=to_face, direction=cut_direction)
        self._drop_face_bodies(slot_bodies, pair)

        # Holes and pocket on the top face, one sketch. Faces are re-resolved
        # because every modifying feature gives the body new face identities.
        top = _face_with_normal(body, 0, 0, 1)
        sk = self._begin_sketch('sketch_holes', top, pair)
        s = sk.modelToSketchSpace
        points = []
        for k in range(HOLE_COUNT):
            x = 5.0 + k * (BOARD_W - 10.0) / (HOLE_COUNT - 1)
            points.append(self.rec.timed('sketch_point',
                                         lambda: sk.sketchPoints.add(s(_p(x, 5.0, zt))),
                                         is_feature=False, pair=pair))
        rect = sk.sketchCurves.sketchLines
        self.rec.timed('sketch_rect', lambda: rect.addTwoPointRectangle(
            s(_p(20.0, 15.0, zt)), s(_p(40.0, 16.2, zt))), is_feature=False, pair=pair)
        self._end_sketch(sk)
        pocket_profiles = self.rec.timed('profile_lookup', lambda: _profiles_by_area(sk, POCKET_AREA),
                                         is_feature=False, pair=pair)
        if len(pocket_profiles) != 1:
            raise RuntimeError('expected 1 pocket profile, found %d' % len(pocket_profiles))
        pocket_profile = pocket_profiles[0]
        if batched:
            self._holes(points, body, pair, 'hole_face', sk, (0, 0, -1))
        else:
            for pt in points:
                self._holes([pt], body, pair, 'hole_face', sk, (0, 0, -1))
        self._extrude_cut(pocket_profile, body, pair, 'extrude_cut_pocket', depth=POCKET_DEPTH)

        # Two holes into the narrow face at x = 0.
        side = _face_with_normal(body, -1, 0, 0)
        sk = self._begin_sketch('sketch_edge', side, pair)
        s = sk.modelToSketchSpace
        edge_points = [self.rec.timed('sketch_point',
                                      lambda: sk.sketchPoints.add(s(_p(0.0, y, z + THICKNESS / 2.0))),
                                      is_feature=False, pair=pair) for y in (10.0, 20.0)]
        self._end_sketch(sk)
        if batched:
            self._holes(edge_points, body, pair, 'hole_edge', sk, (1, 0, 0))
        else:
            for pt in edge_points:
                self._holes([pt], body, pair, 'hole_edge', sk, (1, 0, 0))
        return body

    def build(self):
        for pair in range(self.cfg['pairs']):
            z = pair * PAIR_SPACING_Z
            self._board_a(pair, z)
            self._board_b(pair, z + PAIR_SPACING_Z / 2.0)


def summarize(cfg, rec, total, design):
    by_kind = {}
    for r in rec.records:
        k = by_kind.setdefault(r['kind'], {'count': 0, 'total': 0.0, 'max': 0.0})
        k['count'] += 1
        k['total'] += r['dt']
        k['max'] = max(k['max'], r['dt'])
    feature_records = [r for r in rec.records if r['kind'] not in (
        'sketch_line', 'sketch_arc', 'sketch_point', 'sketch_rect', 'profile_lookup',
        'body_name', 'doc_create', 'design_type', 'brep_face', 'brep_add', 'body_delete')]
    n = len(feature_records)
    head = feature_records[:max(1, n // 10)]
    tail = feature_records[-max(1, n // 10):]
    per_pair = {}
    for r in rec.records:
        if r['pair'] >= 0:
            per_pair[r['pair']] = per_pair.get(r['pair'], 0.0) + r['dt']
    pairs_sorted = [per_pair[k] for k in sorted(per_pair)]
    parametric = design.designType == adsk.fusion.DesignTypes.ParametricDesignType
    return {
        'label': cfg['label'],
        'total_s': total,
        'features': rec.features,
        'timeline_count': design.timeline.count if parametric else None,
        'bodies': design.rootComponent.bRepBodies.count,
        'api_calls': len(rec.records),
        'sketch_entities': sum(1 for r in rec.records if r['kind'].startswith('sketch_')
                               and r['kind'] not in ('sketch_outline', 'sketch_mortise',
                                                     'sketch_holes', 'sketch_edge')),
        'feature_write_avg_first_tenth_ms': 1000.0 * sum(r['dt'] for r in head) / len(head),
        'feature_write_avg_last_tenth_ms': 1000.0 * sum(r['dt'] for r in tail) / len(tail),
        'first_pair_s': pairs_sorted[0] if pairs_sorted else None,
        'last_pair_s': pairs_sorted[-1] if pairs_sorted else None,
        'by_kind': by_kind,
    }


def run_cell(overrides):
    cfg = dict(DEFAULTS)
    cfg.update(overrides)
    rec = Recorder()
    gc.disable()
    try:
        t0 = time.perf_counter()
        builder = Builder(cfg, rec)
        doc = builder.create_document()
        builder.build()
        total = time.perf_counter() - t0
    finally:
        gc.enable()
    summary = summarize(cfg, rec, total, builder.design)
    summary['document'] = doc.name
    if cfg['out_dir']:
        os.makedirs(cfg['out_dir'], exist_ok=True)
        path = os.path.join(cfg['out_dir'], cfg['label'] + '.json')
        with open(path, 'w') as fh:
            json.dump({'config': cfg, 'summary': summary, 'records': rec.records}, fh)
        summary['path'] = path
    return summary
