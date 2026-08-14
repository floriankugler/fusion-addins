import os

# All add-ins share the top-level module name 'lib', and whichever add-in loads
# first pins the package path for everyone - possibly to a lib copy that does
# not contain the auto_setup subpackage (older vendored builds, or a stale
# cached path from a deleted add-in). Make sure this add-in's own lib directory
# is searched as well before importing from it.
import lib
_ADDIN_LIB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lib')
if _ADDIN_LIB_DIR not in lib.__path__:
    lib.__path__.append(_ADDIN_LIB_DIR)

from lib import addin, inputs, ui_placement
from lib.auto_setup import recognition, templates, rules, builder
from lib.fusionbootstrap.runtime import RuntimeInfo
import adsk.core, adsk.fusion
from typing import cast

TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')

CUTTERS = ['dc', 'udc']

_addin: addin.Addin | None = None
_export_addin: addin.Addin | None = None


def run(context, runtime_info: RuntimeInfo):
    global _addin, _export_addin
    _addin = AutoSetup(runtime_info)
    _export_addin = AutoSetupExport(runtime_info)
    # Dev support: allow external tooling to restart this add-in by firing the
    # custom event '<id>_reload' (see lib/fusionbootstrap/reloader.py).
    from lib.fusionbootstrap import reloader
    entry = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'auto_setup.py')
    reloader.ensure(runtime_info.id + '_reload', entry)


def stop(context):
    global _addin, _export_addin
    for instance in (_addin, _export_addin):
        if instance:
            instance.shutdown()
    _addin = None
    _export_addin = None


class AutoSetupInputs(inputs.Inputs):
    def __init__(self, registry: dict[str, list[templates.TemplateVariant]], units: str):
        self.registry = registry
        self.pocket_options = rules.pocket_options(registry)
        self.contour_options = rules.contour_options(registry)

        self.bodies = inputs.SelectionByEntityTokenInput(
            id='bodies',
            name='Bodies',
            filter=['Bodies'],
            lower_bound=1,
            upper_bound=0,
            tool_tip='Select the bodies to include in the setup.',
        )
        self.top_face = inputs.SelectionByEntityTokenInput(
            id='topFace',
            name='Top Face',
            filter=['PlanarFaces'],
            lower_bound=1,
            upper_bound=1,
            tool_tip='Select the top face of one of the bodies. It defines which side of the '
                     'stock faces up.',
        )
        self.x_axis = inputs.SelectionByEntityTokenInput(
            id='xAxis',
            name='X Axis',
            filter=['LinearEdges', 'ConstructionLines'],
            lower_bound=1,
            upper_bound=1,
            tool_tip='Select a linear edge or a construction axis defining the X axis of the '
                     'setup. Y follows from the top face and the X axis.',
        )
        self.setup_name = inputs.StringInput(
            id='setupName',
            name='Setup Name',
            default_value='Auto Setup',
            tool_tip='Name of the created setup.',
        )
        self.cutter = inputs.DropDownInput(
            id='cutter',
            name='Cutter',
            options=[
                inputs.DropDownInput.Item('Down-cut (dc)', 0),
                inputs.DropDownInput.Item('Up/Down-cut (udc)', 1),
            ],
            default_value=0,
            tool_tip='Cutter variant used to pick templates. Templates without a cutter tag '
                     'are valid for either choice.',
        )

        self.pocket_default = self._options_dropdown(
            'pocketDefault', 'Pocket operation', self.pocket_options,
            'Template applied to pockets that are not assigned to a specific bucket below.',
            preferred='Tasche adaptiv 8mm')
        self.pocket_buckets = self._option_buckets(
            'pocket', self.pocket_options, ['PlanarFaces'],
            'Select pocket bottom faces that should use the "{label}" template instead of the default.')
        self._register_buckets('pocket', self.pocket_buckets)

        self.contour_default = self._options_dropdown(
            'contourDefault', 'Contour operation', self.contour_options,
            'Template applied to outer contours and cutouts that are not assigned to a bucket below.',
            preferred='Kontur 6mm')
        self.contour_buckets = self._option_buckets(
            'contour', self.contour_options, ['Edges', 'Faces'],
            'Select contours (edges or side faces) that should use the "{label}" template '
            'instead of the default.')
        self._register_buckets('contour', self.contour_buckets)

        self.finish_outer = inputs.CheckboxInput(
            id='finishOuter',
            name='Finish outer contours',
            default_value=False,
            tool_tip='Use the finishing-pass template variant for all outer contours.',
        )
        self.finish_cutouts = inputs.CheckboxInput(
            id='finishCutouts',
            name='Finish inner contours',
            default_value=False,
            tool_tip='Use the finishing-pass template variant for all interior cutouts.',
        )
        self.finish_pockets = inputs.CheckboxInput(
            id='finishPockets',
            name='Finish pockets',
            default_value=False,
            tool_tip='Use the finishing-pass template variant for all pockets.',
        )
        self.finish_selection = inputs.SelectionByEntityTokenInput(
            id='finishSelection',
            name='Finish contours',
            filter=['Edges', 'Faces'],
            lower_bound=0,
            upper_bound=0,
            tool_tip='Additionally apply a finishing pass to these contours or pockets '
                     '(select edges or side faces), regardless of the checkboxes above.',
        )

        self.tabs_mode = inputs.DropDownInput(
            id='tabsMode',
            name='Tabs',
            options=[
                inputs.DropDownInput.Item('None', rules.TAB_NONE),
                inputs.DropDownInput.Item('Outer contours', rules.TAB_OUTER),
                inputs.DropDownInput.Item('Inner contours', rules.TAB_INNER),
                inputs.DropDownInput.Item('All contours', rules.TAB_ALL),
            ],
            default_value=rules.TAB_NONE,
            tool_tip='Which contours get holding tabs.',
        )
        self.tab_contours = inputs.SelectionByEntityTokenInput(
            id='tabContours',
            name='↳ Tab contours',
            filter=['Edges', 'Faces'],
            lower_bound=0,
            upper_bound=0,
            tool_tip='Additionally place tabs on these contours (select edges or side faces of '
                     'outer contours or cutouts), regardless of the dropdown above.',
        )
        tabs_active = lambda: self.tabs_mode.value != rules.TAB_NONE or len(self.tab_contours.value) > 0
        self.tab_min_count = inputs.IntegerInput(
            id='tabMinCount',
            name='Min tabs per contour',
            default_value=4,
            minimum=1,
            maximum=50,
            tool_tip='Minimum number of tabs on each tabbed contour, so even small parts are '
                     'held safely.',
            update_visibility=tabs_active,
        )
        super().__init__()

    def _options_dropdown(self, id: str, name: str, labels: list[str],
                          tool_tip: str, preferred: str | None = None) -> inputs.DropDownInput:
        options = [inputs.DropDownInput.Item(label, idx) for idx, label in enumerate(labels)]
        if not options:
            options = [inputs.DropDownInput.Item('(no templates found)', -1)]
        default = options[0].value
        if preferred and preferred in labels:
            default = labels.index(preferred)
        return inputs.DropDownInput(
            id=id,
            name=name,
            options=options,
            default_value=default,
            tool_tip=tool_tip,
        )

    def _option_buckets(self, kind: str, labels: list[str], filter: list[str],
                        tool_tip: str) -> list[inputs.SelectionByEntityTokenInput]:
        # Only offer override buckets when there is something to choose between.
        if len(labels) < 2:
            return []
        return [
            inputs.SelectionByEntityTokenInput(
                id=f'{kind}Bucket{idx}',
                name=f'↳ {label}',
                filter=filter,
                lower_bound=0,
                upper_bound=0,
                tool_tip=tool_tip.format(label=label),
            )
            for idx, label in enumerate(labels)
        ]

    def _register_buckets(self, kind: str, buckets: list[inputs.SelectionByEntityTokenInput]):
        # Register bucket inputs as attributes (in dialog order) so the Inputs base class picks them up.
        for idx, bucket in enumerate(buckets):
            setattr(self, f'_{kind}_bucket_{idx}', bucket)

    @property
    def selected_cutter(self) -> str:
        return CUTTERS[self.cutter.value] if 0 <= self.cutter.value < len(CUTTERS) else CUTTERS[0]

    def default_pocket(self) -> str | None:
        idx = self.pocket_default.value
        return self.pocket_options[idx] if 0 <= idx < len(self.pocket_options) else None

    def default_contour(self) -> str | None:
        idx = self.contour_default.value
        return self.contour_options[idx] if 0 <= idx < len(self.contour_options) else None

    def pocket_override_tokens(self) -> dict[str, str]:
        overrides: dict[str, str] = {}
        for idx, bucket in enumerate(self.pocket_buckets):
            for entity in bucket.value:
                overrides[entity.entityToken] = self.pocket_options[idx]
        return overrides

    def contour_override_entities(self) -> list[tuple[object, str]]:
        overrides: list[tuple[object, str]] = []
        for idx, bucket in enumerate(self.contour_buckets):
            for entity in bucket.value:
                overrides.append((entity, self.contour_options[idx]))
        return overrides


class AutoSetup(addin.Addin):
    inputs: AutoSetupInputs

    @property
    def resource_dir(self) -> str:
        # Absolute path so the command can also be (re)registered from outside
        # Fusion's add-in launcher (e.g. a scripted restart during development).
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Resources')

    @property
    def plugin_name(self) -> str:
        return 'Auto Setup'

    @property
    def plugin_desc(self) -> str:
        return 'Automatic manufacturing setup creation'

    @property
    def plugin_tooltip(self) -> str:
        return ('Creates a manufacturing setup with drilling, boring, pocket and contour '
                'operations derived from the geometry of the selected bodies. '
                'Operation parameters come from the templates in the add-in\'s templates folder.')

    def get_ui_placement(self) -> ui_placement.UIPlacement:
        command = ui_placement.PlacementSpec(
            id=self.create_command_id,
            anchor_id='CreateSetupCmd',
            insert_before=False,
        )
        return ui_placement.UIPlacement(
            panel_id='CAMJobPanel',
            command=command,
        )

    def create_inputs(self) -> AutoSetupInputs:
        design = self.app.activeDocument.products.itemByProductType('DesignProductType')
        units = design.unitsManager.defaultLengthUnits if design else 'mm'
        return AutoSetupInputs(templates.scan(TEMPLATES_DIR), units)

    def execute(self):
        bodies = cast(list[adsk.fusion.BRepBody], self.inputs.bodies.value)
        top_face = cast(adsk.fusion.BRepFace, self.inputs.top_face.value[0])
        x_axis = self.inputs.x_axis.value[0]

        frame = recognition.Frame.from_x_axis(
            x_axis, recognition.face_normal(top_face))
        result = recognition.recognize(bodies, frame)
        assignments = rules.Assignments(
            cutter=self.inputs.selected_cutter,
            pocket_default=self.inputs.default_pocket(),
            contour_default=self.inputs.default_contour(),
            finish_outer_all=self.inputs.finish_outer.value,
            finish_cutouts_all=self.inputs.finish_cutouts.value,
            finish_pockets_all=self.inputs.finish_pockets.value,
            finish_selection=list(self.inputs.finish_selection.value),
            pocket_overrides=self.inputs.pocket_override_tokens(),
            contour_overrides=self.inputs.contour_override_entities(),
        )
        tab_policy = rules.TabPolicy(
            mode=self.inputs.tabs_mode.value,
            selection=list(self.inputs.tab_contours.value),
            min_count=self.inputs.tab_min_count.value,
        )
        jobs, warnings = rules.plan(result, self.inputs.registry, assignments, tab_policy)
        summary = builder.create_setup(
            self.inputs.setup_name.value, bodies, jobs, warnings, tab_policy,
            x_axis=x_axis, top_face=top_face, frame=frame)

        if summary.warnings:
            self.ui.messageBox(
                'Setup created with warnings:\n\n' + '\n'.join(f'• {w}' for w in summary.warnings),
                'Auto Setup',
            )


class AutoSetupExport(addin.Addin):
    @property
    def resource_dir(self) -> str:
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Resources')

    @property
    def create_command_id(self) -> str:
        return self.runtime_info.id + '_export'

    @property
    def has_command_ui(self) -> bool:
        return False

    @property
    def plugin_name(self) -> str:
        return 'Export Auto Setup Templates'

    @property
    def plugin_desc(self) -> str:
        return 'Export setups as Auto Setup templates'

    @property
    def plugin_tooltip(self) -> str:
        return ('Exports every setup of the active document whose name follows the '
                '"<kind>[.<tag>...]_<label>" convention (kind: pocket, contour, drill, bore, '
                'dogbone; tags: dc, udc, finish) as a template file used by the Auto Setup '
                'command.')

    def get_ui_placement(self) -> ui_placement.UIPlacement:
        command = ui_placement.PlacementSpec(
            id=self.create_command_id,
            anchor_id=self.runtime_info.id + '_create',
            insert_before=False,
        )
        return ui_placement.UIPlacement(
            panel_id='CAMJobPanel',
            command=command,
        )

    def execute(self):
        exported, skipped = templates.export_document_setups(TEMPLATES_DIR)
        lines = [f'Exported {len(exported)} template(s) to {TEMPLATES_DIR}:']
        lines += [f'• {name}' for name in exported]
        if skipped:
            lines.append('')
            lines.append('Skipped setups (name does not match "<kind>[.<tag>...]_<label>"):')
            lines += [f'• {name}' for name in skipped]
        self.ui.messageBox('\n'.join(lines), 'Export Auto Setup Templates')
