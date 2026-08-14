"""Creates the manufacturing setup and inserts template-based operations."""

import adsk.core, adsk.fusion, adsk.cam
from dataclasses import dataclass, field
from . import recognition, rules, tabs, templates

# Default stock side offset (cm): 'add stock to sides and top-bottom' with 7mm sides.
STOCK_SIDE_OFFSET = 0.7


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
    get_tab_sketch = _tab_sketch_factory(name)
    for job in jobs:
        try:
            summary.operations.extend(
                _insert_job(setup, job, tab_policy, summary.warnings, get_tab_sketch))
        except Exception as error:
            summary.warnings.append(f'Operation "{job.display_name}" failed: {error}')
    # Hide the tabs sketch (if one was created): the operations keep their
    # references; unhide it to drag tab positions around.
    sketch = get_tab_sketch(create=False)
    if sketch:
        sketch.isLightBulbOn = False
    return summary


def _tab_sketch_factory(setup_name: str):
    """Lazily creates the sketch holding tab position points.

    Tab positions must be CAD entities (bare Point3D has no object path), so
    they are materialized as points in a dedicated design sketch. Bonus: the
    user can drag the points and regenerate to move tabs.
    """
    state: dict[str, adsk.fusion.Sketch] = {}

    def get(create: bool = True) -> adsk.fusion.Sketch | None:
        if 'sketch' not in state:
            if not create:
                return None
            app = adsk.core.Application.get()
            design = adsk.fusion.Design.cast(
                app.activeDocument.products.itemByProductType('DesignProductType'))
            root = design.rootComponent
            sketch = root.sketches.add(root.xYConstructionPlane)
            sketch.name = f'{setup_name} tabs'
            state['sketch'] = sketch
        return state['sketch']

    return get


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


def _insert_job(setup: adsk.cam.Setup, job: rules.Job, tab_policy: rules.TabPolicy,
                warnings: list[str], get_tab_sketch) -> list[adsk.cam.Operation]:
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
        _apply_tabs(operation, job, tab_policy, warnings, get_tab_sketch)
        if len(operations) == 1:
            operation.name = job.display_name
        else:
            operation.name = f'{job.display_name} – {operation.name}'
    return operations


def _apply_tabs(operation: adsk.cam.Operation, job: rules.Job, tab_policy: rules.TabPolicy,
                warnings: list[str], get_tab_sketch):
    """Tabs are opt-in and fully add-in managed: explicitly off unless the job
    is tabbed, in which case manual positions are computed and applied."""
    group = operation.parameters.itemByName('group_tabs')
    if not group:
        return  # strategy without tab support
    if not job.tabbed:
        group.value.value = False
        return

    tab_width = operation.parameters.itemByName('tabWidth').value.value
    points: list[adsk.core.Point3D] = []
    for edges, label in job.tab_loops:
        points.extend(tabs.compute_tab_points(
            edges, tab_width, tab_policy.min_count, warnings, label))
    if not points:
        group.value.value = False
        warnings.append(f'{operation.name}: no tab positions could be placed; tabs disabled.')
        return
    sketch = get_tab_sketch()
    sketch_points = [
        sketch.sketchPoints.add(sketch.modelToSketchSpace(point)) for point in points]
    group.value.value = True
    operation.parameters.itemByName('tabPositions').value.value = sketch_points


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
