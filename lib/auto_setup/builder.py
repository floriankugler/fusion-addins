"""Creates the manufacturing setup and inserts template-based operations."""

import adsk.core, adsk.fusion, adsk.cam
from dataclasses import dataclass, field
from . import recognition, rules, tabs, templates

# Default stock side offset (cm): 'add stock to sides and top-bottom' with 7mm sides.
STOCK_SIDE_OFFSET = 0.7

# Job kinds whose operations machine profiles a tab can sit on.
TABBABLE_KINDS = ('contour', 'dogbone')
# How far from its profile a cut is taken to reach, in tool diameters: one
# diameter is the milled band itself, the rest is safety margin.
TAB_REACH_FACTOR = 2.0
# A tab position this close to a profile sits on it (cm).
ON_CONTOUR_TOL = 0.05


class BuilderError(Exception):
    pass


@dataclass
class BuildSummary:
    setup: adsk.cam.Setup
    operations: list[adsk.cam.Operation] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def create_setup(name: str, bodies: list[adsk.fusion.BRepBody],
                 jobs: list[rules.Job], warnings: list[str],
                 tab_policy: rules.TabPolicy | None = None,
                 x_axis=None,
                 top_face: adsk.fusion.BRepFace | None = None,
                 frame: recognition.Frame | None = None) -> BuildSummary:
    cam = _cam_product()
    tab_policy = tab_policy or rules.TabPolicy()

    setup_input = cam.setups.createInput(adsk.cam.OperationTypes.MillingOperation)
    setup_input.models = list(bodies)
    setup_input.name = name
    setup_input.stockMode = adsk.cam.SetupStockModes.RelativeBoxStock
    parameters = setup_input.parameters
    parameters.itemByName('job_stockOffsetMode').expression = "'simple'"
    parameters.itemByName('job_stockOffsetSides').value.value = STOCK_SIDE_OFFSET
    if x_axis and top_face and frame:
        _apply_wcs_orientation(parameters, x_axis, top_face, frame)
    setup = cam.setups.add(setup_input)

    summary = BuildSummary(setup=setup, warnings=list(warnings))
    tab_points = _TabPoints(name, jobs, tab_policy, summary.warnings)
    for index, job in enumerate(jobs):
        try:
            summary.operations.extend(
                _insert_job(setup, index, job, tab_points, summary.warnings))
        except Exception as error:
            summary.warnings.append(f'Operation "{job.display_name}" failed: {error}')
    # Hide the tabs sketch (if one was created): the operations keep their
    # references; unhide it to drag tab positions around.
    if tab_points.sketch:
        tab_points.sketch.isLightBulbOn = False
    return summary


class _TabPoints:
    """The tab positions of a setup, handed to the operations that cut through
    them.

    All positions are computed once, and each operation gets exactly those that
    lie on the profiles it machines. That covers its own tabbed contours and a
    profile that a second operation cuts as well - which is the case where tabs
    would otherwise be milled away. The filter has to be geometric rather than
    "everything to everyone", because Fusion does not ignore a position that
    lies off the machined profile: it projects it onto the nearest contour of
    the operation (verified 2026-08-15) and puts a tab there.

    Tab positions must be CAD entities (a bare Point3D has no object path), so
    they are materialized as points in a dedicated design sketch. Bonus: the
    user can drag the points and regenerate to move tabs.

    The positions depend on the tab width, which is owned by the template; the
    first job to ask sets it for all of them, so that two operations over the
    same cut stay consistent. A template with a different width would silently
    shift them, hence the warning.
    """

    def __init__(self, setup_name: str, jobs: list[rules.Job],
                 tab_policy: rules.TabPolicy, warnings: list[str]):
        self._setup_name = setup_name
        self._jobs = jobs
        self._tab_policy = tab_policy
        self._warnings = warnings
        self._positions: list[tuple[adsk.core.Point3D, adsk.fusion.SketchPoint]] | None = None
        self._by_job: dict[int, list[adsk.fusion.SketchPoint]] = {}
        self._width: float | None = None
        self.sketch: adsk.fusion.Sketch | None = None

    def for_job(self, job_index: int, job: rules.Job,
                operation: adsk.cam.Operation) -> list[adsk.fusion.SketchPoint]:
        parameter = operation.parameters.itemByName('tabWidth')
        width = parameter.value.value if parameter else 0.0
        if self._width is None:
            self._width = width
        elif job.tabbed and abs(width - self._width) > 1e-6:
            self._warnings.append(
                f'{operation.name}: the template\'s tab width ({width * 10:.1f}mm) '
                f'differs from the first tabbed operation\'s ({self._width * 10:.1f}mm); '
                f'the setup uses {self._width * 10:.1f}mm to place every tab.')
        if self._positions is None:
            self._positions = self._materialize()
        if job_index not in self._by_job:
            self._by_job[job_index] = self._positions_on_job(job, operation)
        return self._by_job[job_index]

    def _materialize(self) -> list[tuple[adsk.core.Point3D, adsk.fusion.SketchPoint]]:
        result: list[tuple[adsk.core.Point3D, adsk.fusion.SketchPoint]] = []
        for job in self._jobs:
            for edges, label in job.tab_loops:
                for point in tabs.compute_tab_points(
                        edges, self._width, self._tab_policy.min_count,
                        self._warnings, label):
                    sketch = self._tab_sketch()
                    result.append(
                        (point, sketch.sketchPoints.add(sketch.modelToSketchSpace(point))))
        return result

    def _positions_on_job(self, job: rules.Job,
                          operation: adsk.cam.Operation) -> list[adsk.fusion.SketchPoint]:
        """The positions that fall into this operation's milled area.

        A cut sweeps one tool diameter to its waste side; anything within
        TAB_REACH_FACTOR times that of a profile the operation machines - on
        the waste side of it, which is inside an inner cutout and outside an
        outer contour - is close enough to the cut to need a tab here too.
        That is how a tab survives a second operation over the same profile,
        and how a part nested next to a bigger part's opening keeps the tabs
        that opening's cut would otherwise take with it.

        Everything else is left out: Fusion projects a position that lies off
        the machined profile onto the nearest contour, which would put a tab
        where the cut never came near one.
        """
        if not self._positions:
            return []
        parameter = operation.parameters.itemByName('tool_diameter')
        reach = TAB_REACH_FACTOR * (parameter.value.value if parameter else 0.0)
        # [bounds, edges, waste is inside the loop, sampled outline or None]
        loops = [[_loop_bounds(edges), edges, waste_inside, None]
                 for edges, waste_inside in _machined_loops(job)]
        result: list[adsk.fusion.SketchPoint] = []
        for world, sketch_point in self._positions:
            for loop in loops:
                bounds, edges, waste_inside, outline = loop
                if not _within(bounds, world, reach):
                    continue
                if outline is None:
                    outline = loop[3] = tabs.loop_outline(edges)
                distance = outline.distance(world)
                if distance > reach:
                    continue
                # A position on the profile itself belongs to this cut whatever
                # side the outline test claims: that is the same contour
                # machined twice.
                if distance <= ON_CONTOUR_TOL or outline.contains(world) == waste_inside:
                    result.append(sketch_point)
                    break
        return result

    def _tab_sketch(self) -> adsk.fusion.Sketch:
        if self.sketch is None:
            app = adsk.core.Application.get()
            design = adsk.fusion.Design.cast(
                app.activeDocument.products.itemByProductType('DesignProductType'))
            root = design.rootComponent
            self.sketch = root.sketches.add(root.xYConstructionPlane)
            self.sketch.name = f'{self._setup_name} tabs'
        return self.sketch


def _machined_loops(job: rules.Job) -> list[tuple[list[adsk.fusion.BRepEdge], bool]]:
    """The closed profiles an operation of this job cuts, each with the side
    its waste - and therefore its tool - is on.

    Dog-bone reliefs are left out: they are corner details, and tabs keep
    several tab widths of clearance from corners anyway.
    """
    loops = [(cutout.edges, True) for cutout in job.cutouts]
    loops += [(contour.edges, False) for contour in job.contours if contour.edges]
    return loops


def _loop_bounds(edges: list[adsk.fusion.BRepEdge]) -> adsk.core.BoundingBox3D | None:
    bounds = None
    for edge in edges:
        box = edge.boundingBox
        if bounds is None:
            bounds = box.copy()
        else:
            bounds.combine(box)
    return bounds


def _within(bounds: adsk.core.BoundingBox3D | None, point: adsk.core.Point3D,
            reach: float) -> bool:
    if not bounds:
        return False
    low, high = bounds.minPoint, bounds.maxPoint
    return (low.x - reach <= point.x <= high.x + reach
            and low.y - reach <= point.y <= high.y + reach
            and low.z - reach <= point.z <= high.z + reach)


def _apply_wcs_orientation(parameters, x_axis, top_face: adsk.fusion.BRepFace,
                           frame: recognition.Frame):
    """Orient the setup WCS: Z plane from the top face, X from the axis
    selection (linear edge or construction axis).

    Fusion takes the face normal and the axis' own direction; the flip flags
    align them with the machining frame."""
    parameters.itemByName('wcs_orientation_mode').expression = "'axesZX'"
    parameters.itemByName('wcs_orientation_axisZ').value.value = [top_face]
    parameters.itemByName('wcs_orientation_axisX').value.value = [x_axis]
    flip_z = recognition.face_normal(top_face).dotProduct(frame.z) < 0
    flip_x = recognition.axis_direction(x_axis).dotProduct(frame.x) < 0
    parameters.itemByName('wcs_orientation_flipZ').value.value = flip_z
    parameters.itemByName('wcs_orientation_flipX').value.value = flip_x


def _cam_product() -> adsk.cam.CAM:
    app = adsk.core.Application.get()
    cam = adsk.cam.CAM.cast(app.activeDocument.products.itemByProductType('CAMProductType'))
    if not cam:
        raise BuilderError('No CAM product in the active document.')
    return cam


def _insert_job(setup: adsk.cam.Setup, job_index: int, job: rules.Job,
                tab_points: _TabPoints, warnings: list[str]) -> list[adsk.cam.Operation]:
    template = templates.load(job.variant)
    template_input = adsk.cam.CreateFromCAMTemplateInput.create()
    template_input.camTemplate = template
    created = setup.createFromCAMTemplate2(template_input)

    operations = [op for op in (adsk.cam.Operation.cast(o) for o in created) if op]
    if not operations:
        raise BuilderError(f'Template {job.variant.name} produced no operations.')

    for operation in operations:
        _bind_geometry(operation, job)
        if job.is_through and job.variant.kind in ('drill', 'bore'):
            # Break through the bottom by 0.2mm (for drills instead of the
            # drill tip option), like the contour templates do.
            _try_set(operation, 'bottomHeight_mode', "'from hole bottom'")
            _try_set(operation, 'bottomHeight_offset', '-0.2 mm')
        try:
            _apply_tabs(operation, job_index, job, tab_points, warnings)
        except Exception as error:
            # Losing the whole operation over its tabs helps nobody: keep it,
            # switch the tabs off and say so - loudly, because the part is then
            # cut free.
            group = operation.parameters.itemByName('group_tabs')
            if group:
                group.value.value = False
            warnings.append(
                f'{operation.name}: tabs could not be applied ({error}); the '
                'operation runs WITHOUT tabs and cuts its parts free.')
        if len(operations) == 1:
            operation.name = job.display_name
        else:
            operation.name = f'{job.display_name} – {operation.name}'
    return operations


def _apply_tabs(operation: adsk.cam.Operation, job_index: int, job: rules.Job,
                tab_points: _TabPoints, warnings: list[str]):
    """Tabs are fully add-in managed: an operation gets every tab position its
    own cuts run through (see _TabPoints), which covers its own tabbed contours
    as well as the tabs of a part nested into a contour it cuts.

    Fusion tabs a contour at the explicit positions and falls back to the
    template's automatic count for contours that have none, so that count is
    forced to zero: a contour the user did not pick stays untabbed even when it
    shares the operation with tabbed ones.
    """
    group = operation.parameters.itemByName('group_tabs')
    if not group:
        return  # strategy without tab support
    points = (tab_points.for_job(job_index, job, operation)
              if job.variant.kind in TABBABLE_KINDS else [])
    if not points:
        group.value.value = False
        if job.tabbed:
            warnings.append(
                f'{operation.name}: no tab positions could be placed; tabs disabled.')
        return
    group.value.value = True
    _set_if_different(operation, 'tabPositioning', "'tabCount'", warnings)
    _set_if_different(operation, 'tabsPerContour', '0', warnings)
    positions = operation.parameters.itemByName('tabPositions')
    if not positions:
        group.value.value = False
        warnings.append(
            f'{operation.name}: this strategy takes no tab positions; the operation '
            'runs WITHOUT tabs.')
        return
    positions.value.value = points


def _bind_geometry(operation: adsk.cam.Operation, job: rules.Job):
    if job.holes:
        faces = [hole.face for hole in job.holes]
        # The drill strategy selects hole geometry via 'holeFaces', bore via 'circularFaces'.
        parameter = (operation.parameters.itemByName('holeFaces')
                     or operation.parameters.itemByName('circularFaces'))
        if not parameter:
            raise BuilderError(f'{operation.name}: no hole geometry parameter found.')
        parameter.value.value = faces
        return

    parameter = operation.parameters.itemByName('pockets') or operation.parameters.itemByName('contours')
    if not parameter:
        raise BuilderError(f'{operation.name}: no pocket/contour geometry parameter found.')
    contours_param = adsk.cam.CadContours2dParameterValue.cast(parameter.value)
    selections = contours_param.getCurveSelections()
    selections.clear()
    for pocket in job.pockets:
        selection = selections.createNewPocketSelection()
        selection.inputGeometry = [pocket.bottom_face]
    for cutout in job.cutouts:
        chain = selections.createNewChainSelection()
        chain.inputGeometry = [cutout.edges[0]]
    for edge in job.open_chains:
        chain = selections.createNewChainSelection()
        chain.inputGeometry = [edge]
        # A dogbone relief is a single arc: machined as an open chain, not
        # closed up into a tiny circular pocket.
        if chain.isOpenAllowed:
            chain.isOpen = True
    for contour in job.contours:
        silhouette = selections.createNewSilhouetteSelection()
        silhouette.inputGeometry = [contour.body]
        silhouette.loopType = adsk.cam.LoopTypes.OnlyOutsideLoops
        # Without this, the silhouette includes ALL setup bodies, so every
        # contour operation would machine every body's outer contour.
        silhouette.isSetupModelSelected = False
    contours_param.applyCurveSelections(selections)


def _try_set(operation: adsk.cam.Operation, parameter_name: str, expression: str):
    parameter = operation.parameters.itemByName(parameter_name)
    if parameter:
        parameter.expression = expression


def _set_if_different(operation: adsk.cam.Operation, parameter_name: str,
                      expression: str, warnings: list[str]):
    """Write a CAM parameter only when the template does not already carry the
    value, and never fail the operation over it.

    Whether a parameter accepts a write depends on the state of the operation
    (some are only enabled in certain modes), so a template that is already set
    up correctly is left untouched rather than rewritten with the same value.
    """
    parameter = operation.parameters.itemByName(parameter_name)
    if not parameter or parameter.expression == expression:
        return
    try:
        parameter.expression = expression
    except Exception as error:
        warnings.append(
            f'{operation.name}: could not set {parameter_name} to {expression} '
            f'({error}); the template\'s own value is used, so contours without a '
            'tab position may get automatic tabs.')
