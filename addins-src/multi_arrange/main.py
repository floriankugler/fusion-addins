import os

# All add-ins share the top-level module name 'lib', and whichever add-in loads
# first pins the package path for everyone. Make sure this add-in's own lib
# directory is searched as well before importing from it.
import lib
_ADDIN_LIB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lib')
if _ADDIN_LIB_DIR not in lib.__path__:
    lib.__path__.append(_ADDIN_LIB_DIR)

from lib import addin, inputs, ui_placement, utils
from lib.multi_arrange import model, engine
from lib.multi_arrange.table_input import PartTableInput
from lib.envelope import builder as envelope_builder
from lib.envelope.table_input import RectangleTableInput
from lib.fusionbootstrap.runtime import RuntimeInfo
import adsk.core, adsk.fusion
from typing import cast

_addin: addin.Addin | None = None

RESOURCE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Resources')


def run(context, runtime_info: RuntimeInfo):
    global _addin
    _addin = MultiArrange(runtime_info)
    # Dev support: allow external tooling to restart this add-in by firing the
    # custom event '<id>_reload' (see lib/fusionbootstrap/reloader.py).
    from lib.fusionbootstrap import reloader
    entry = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'multi_arrange.py')
    reloader.ensure(runtime_info.id + '_reload', entry)


def stop(context):
    global _addin
    if _addin:
        _addin.shutdown()
    _addin = None


def _active_design(app: adsk.core.Application) -> adsk.fusion.Design:
    design = adsk.fusion.Design.cast(app.activeProduct)
    if design is None:
        raise RuntimeError('Multi-Arrange only works in the Design workspace.')
    return design


class ButtonInput(inputs.Input):
    """A push button; `value` is True right after a click until reset."""

    value: bool
    input: adsk.core.BoolValueCommandInput

    def __init__(self, id, name, text, tool_tip):
        super().__init__(id, name, tool_tip, lambda: True)
        self.text = text
        self.value = False

    def create_input(self, command_inputs: adsk.core.CommandInputs, params):
        if params is not None:
            raise RuntimeError('A button cannot be restored from a custom feature.')
        self.input = command_inputs.addBoolValueInput(self.id, self.name, False, '', False)
        self.input.text = self.text
        self.input.tooltip = self.tool_tip

    def update_from_input(self):
        self.value = bool(self.input.value)

    def create_in_feature_input(self, feature_input):
        raise RuntimeError('A button cannot be stored in a custom feature.')

    def update_in_feature(self, feature):
        raise RuntimeError('A button cannot be stored in a custom feature.')

    def update_from_feature(self, feature):
        raise RuntimeError('A button cannot be restored from a custom feature.')


class ArrangeInputs(inputs.Inputs):
    def __init__(self, units: str, initial_sheet_rows: list[tuple[str, str, int]] | None = None):
        self.update = inputs.SelectionByEntityTokenInput(
            id='update',
            name='Update arrangement',
            filter=['Occurrences'],
            lower_bound=0,
            upper_bound=1,
            tool_tip=(
                'Optional: select an existing Multi-Arrange component to '
                'recreate it. All settings are restored from the stored '
                'arrangement, the old component is hidden while the dialog is '
                'open, and replaced on OK.'
            ),
        )
        self.faces = inputs.SelectionByEntityTokenInput(
            id='faces',
            name='Parts (top faces)',
            filter=['PlanarFaces'],
            lower_bound=1,
            upper_bound=0,
            tool_tip='Select the top face of every part to nest.',
        )
        self.parts_table = PartTableInput(
            id='parts_table',
            name='Part settings',
            tool_tip=(
                'Rotation, grain and grouping per part. Rows are prefilled from '
                'the settings saved on each body and are saved back on OK.'
            ),
        )
        self.direction = inputs.SelectionByEntityTokenInput(
            id='direction',
            name='Grain direction',
            filter=['LinearEdges', 'SketchLines', 'ConstructionLines'],
            lower_bound=0,
            upper_bound=1,
            tool_tip=(
                'Assigns a grain direction to the highlighted table row: select '
                'the row, then pick a linear edge, sketch line or construction '
                'axis. Without a reference the longest edge of the top face is '
                'used.'
            ),
        )
        self.plane = inputs.SelectionByEntityTokenInput(
            id='plane',
            name='Sheet plane',
            filter=['ConstructionPlanes', 'PlanarFaces'],
            lower_bound=0,
            upper_bound=1,
            tool_tip=(
                'Construction plane or planar face to create the envelope sketch '
                'on. Defaults to the X-Y plane when empty.'
            ),
        )
        self.rectangles = RectangleTableInput(
            id='rectangles',
            name='Sheets',
            tool_tip=(
                'Sheet sizes to nest into, laid out left to right. The solver '
                'fills sheets starting from the first one, so put offcuts and '
                'smaller sheets first.'
            ),
            units=units,
            initial_rows=initial_sheet_rows,
        )
        self.offset_x = inputs.FloatInput(
            id='offset_x',
            name='X offset',
            default_value=0,
            tool_tip='Offset of the first sheet corner from the sketch origin, along the sketch X axis',
            units=units,
        )
        self.offset_y = inputs.FloatInput(
            id='offset_y',
            name='Y offset',
            default_value=0,
            tool_tip='Offset of the first sheet corner from the sketch origin, along the sketch Y axis',
            units=units,
        )
        self.spacing = inputs.FloatInput(
            id='spacing',
            name='Object spacing',
            default_value=1.0,
            tool_tip='Minimum distance between nested parts.',
            units=units,
        )
        self.spacing.default_expression = '10 mm'
        self.spacing.minimum_value = 0.0
        self.frame = inputs.FloatInput(
            id='frame',
            name='Frame width',
            default_value=1.0,
            tool_tip='Minimum distance between parts and the envelope border.',
            units=units,
        )
        self.frame.default_expression = '10 mm'
        self.frame.minimum_value = 0.0
        self.part_in_part = inputs.CheckboxInput(
            id='part_in_part',
            name='Nest within parts',
            default_value=True,
            tool_tip='Allow parts to be nested inside cutouts of other parts.',
        )
        self.create_copies = inputs.CheckboxInput(
            id='create_copies',
            name='Create copies',
            default_value=True,
            tool_tip=(
                'Checked: the original parts stay in place and copies are placed '
                'on the envelope in a new "Multi-Arrange" component. Unchecked: '
                'the original bodies are moved onto the envelope.'
            ),
        )
        self.preview = ButtonInput(
            id='preview',
            name='Preview',
            text='Compute preview',
            tool_tip=(
                'Computes the arrangement and shows it in the viewport. The '
                'preview is discarded automatically when any input changes.'
            ),
        )
        super().__init__()


class MultiArrange(addin.Addin):
    inputs: ArrangeInputs

    @property
    def resource_dir(self) -> str:
        return RESOURCE_DIR

    @property
    def plugin_name(self) -> str:
        return 'Multi-Arrange'

    @property
    def plugin_desc(self) -> str:
        return 'Grain- and group-aware nesting on multi-sheet envelopes'

    @property
    def plugin_tooltip(self) -> str:
        return (
            'Nests the selected parts on a single- or multi-sheet envelope, with '
            'per-part grain direction, rotation constraints and rigid groups. '
            'Works on plain bodies and leaves no Arrange feature behind. Part '
            'settings are saved on the bodies and restored on the next run.'
        )

    def get_ui_placement(self) -> ui_placement.UIPlacement:
        command = ui_placement.PlacementSpec(
            id=self.create_command_id,
            anchor_id='ArrangeCommand',
            insert_before=False,
        )
        return ui_placement.UIPlacement(
            panel_id='SolidModifyPanel',
            command=command,
        )

    def _initialize_inputs(self, command, params):
        self._ui_ready = False
        super()._initialize_inputs(command, params)
        self._ui_ready = True

    def create_inputs(self) -> ArrangeInputs:
        self._preview_graphics: adsk.fusion.CustomGraphicsGroup | None = None
        self._pending_preview = None
        self._preview_fingerprint = None
        self._did_execute = False
        self._hidden_occurrence: adsk.fusion.Occurrence | None = None
        self._destroy_hooked = False
        design = self.app.activeDocument.products.itemByProductType('DesignProductType')
        units = design.unitsManager.defaultLengthUnits if design else 'mm'
        initial_rows = None
        fusion_design = adsk.fusion.Design.cast(design) if design else None
        if fusion_design:
            stored = model.load_sheet_specs(fusion_design)
            if stored:
                initial_rows = [
                    (row.get('width', ''), row.get('height', ''), int(row.get('count', 1)))
                    for row in stored
                    if row.get('width') and row.get('height')
                ] or None
        return ArrangeInputs(units, initial_rows)

    def _snapshot_selections(self, selection_inputs):
        return [(selection, list(selection.value)) for selection in selection_inputs
                if selection.input is not None]

    def _restore_selections(self, snapshot):
        """Re-adds selections that Fusion silently dropped.

        Both changing command inputs mid-dialog (adding table rows) and model
        churn (the preview compute) can clear selection inputs.
        """
        for selection, entities in snapshot:
            if selection.input is None or selection.input.selectionCount >= len(entities):
                continue
            selection.input.clearSelection()
            for entity in entities:
                try:
                    if entity.isValid:
                        selection.input.addSelection(entity)
                except RuntimeError:
                    pass
            selection.update_from_input()

    def _rebuild_faces_from_table(self):
        """Faces selection follows the table after a row was removed."""
        faces = [record.face for record in self.inputs.parts_table.records
                 if record.face.isValid]
        self.inputs.faces.input.clearSelection()
        for face in faces:
            try:
                self.inputs.faces.input.addSelection(face)
            except RuntimeError:
                pass
        self.inputs.faces.update_from_input()

    def input_changed(self, input):
        if self.inputs is None or input is None:
            return
        self.inputs.rectangles.handle_input_changed(input)
        if self.inputs.parts_table.handle_input_changed(input):
            if (self.inputs.faces.input and
                    self.inputs.faces.input.selectionCount != len(self.inputs.parts_table.records)):
                self._rebuild_faces_from_table()
        if self.inputs.faces.input and input.id == self.inputs.faces.input.id:
            snapshot = self._snapshot_selections([self.inputs.plane, self.inputs.update])
            self.inputs.parts_table.sync(
                [cast(adsk.fusion.BRepFace, face) for face in self.inputs.faces.value])
            self._restore_selections(snapshot)
        if (self.inputs.direction.input and input.id == self.inputs.direction.input.id
                and self.inputs.direction.value):
            entity = self.inputs.direction.value[0]
            message = self.inputs.parts_table.assign_direction(entity.entityToken)
            self.showError(message)
            self.inputs.direction.input.clearSelection()
        if self.inputs.update.input and input.id == self.inputs.update.input.id:
            self._handle_update_selection(input)
        if self.inputs.preview.input and input.id == self.inputs.preview.input.id:
            # The framework replays input_changed for every input while the
            # dialog is being built — only react to real clicks after that.
            if not getattr(self, '_ui_ready', False):
                return
            # The button value is deliberately never reset — each click toggles
            # it, which is what makes every click register as an input change.
            self._hook_destroy(input.parentCommand)
            try:
                error = self._input_error()
                if error:
                    self.showError(error)
                else:
                    # Only compute here; drawing happens in _execute_preview.
                    # The compute's model churn (creating and deleting the
                    # solver artifacts) triggers spurious input events
                    # afterwards, each starting another preview rollback cycle
                    # — so the preview data stays armed and is redrawn every
                    # cycle until an input GENUINELY changes (fingerprint).
                    utils.fusion.log('[MA] preview: computing')
                    snapshot = self._snapshot_selections(
                        [self.inputs.faces, self.inputs.plane, self.inputs.update])
                    self._pending_preview = self._compute_preview_data()
                    self._restore_selections(snapshot)
                    self._preview_fingerprint = self._inputs_fingerprint()
                    self.showError(None)
            except Exception as error:
                self.log_exception_traceback('preview', error)
                self.showError(str(error) or error.__class__.__name__)
        elif self._pending_preview is not None or self._preview_graphics is not None:
            fingerprint = self._inputs_fingerprint()
            if fingerprint != self._preview_fingerprint:
                # A real change: retire the preview like native previews do.
                utils.fusion.log(f'[MA] preview: cleared by real change of {input.id}')
                self._pending_preview = None
                self._clear_preview_graphics()
            else:
                utils.fusion.log(f'[MA] preview: ignoring spurious change of {input.id}')

    # ------------------------------------------------------- update existing

    def _handle_update_selection(self, input):
        if not self.inputs.update.value:
            return
        occurrence = cast(adsk.fusion.Occurrence, self.inputs.update.value[0])
        recipe = model.load_recipe(occurrence.component)
        if recipe is None:
            self.showError('The selected component holds no Multi-Arrange arrangement.')
            self.inputs.update.input.clearSelection()
            return
        self._apply_recipe(recipe)
        # Hide the old arrangement so previews and the new result are not
        # obscured by it; restored on cancel, deleted on OK.
        self._hidden_occurrence = occurrence
        occurrence.isLightBulbOn = False
        self._hook_destroy(input.parentCommand)

    def _apply_recipe(self, recipe: dict):
        design = _active_design(self.app)
        ins = self.inputs

        ins.faces.input.clearSelection()
        missing = 0
        for token in recipe.get('faces', []):
            entities = design.findEntityByToken(token)
            if entities:
                ins.faces.input.addSelection(entities[0])
            else:
                missing += 1
        ins.faces.update_from_input()
        ins.parts_table.sync([cast(adsk.fusion.BRepFace, face) for face in ins.faces.value])

        rows = [
            (row.get('width', ''), row.get('height', ''), int(row.get('count', 1)))
            for row in recipe.get('sheets', [])
            if row.get('width') and row.get('height')
        ]
        if rows:
            ins.rectangles.set_rows(rows)

        ins.plane.input.clearSelection()
        plane_token = recipe.get('plane')
        if plane_token:
            entities = design.findEntityByToken(plane_token)
            if entities:
                ins.plane.input.addSelection(entities[0])
        ins.plane.update_from_input()

        for key, target in (('offset_x', ins.offset_x), ('offset_y', ins.offset_y),
                            ('spacing', ins.spacing), ('frame', ins.frame)):
            expression = recipe.get(key)
            if expression and target.input:
                target.input.expression = expression
                target.update_from_input()
        for key, target in (('part_in_part', ins.part_in_part), ('create_copies', ins.create_copies)):
            if key in recipe and target.input:
                target.input.value = bool(recipe[key])
                target.update_from_input()

        self.showError(
            f'{missing} part(s) of the stored arrangement no longer exist and were skipped.'
            if missing else None)

    def _hook_destroy(self, command):
        if self._destroy_hooked or command is None:
            return
        from lib.utils.fusion import new_event_handler
        handler = new_event_handler(self._on_destroy, adsk.core.CommandEventHandler)
        command.destroy.add(handler)
        self._handlers.append(handler)
        self._destroy_hooked = True

    def _on_destroy(self, args):
        self._pending_preview = None
        self._clear_preview_graphics()
        occurrence = self._hidden_occurrence
        self._hidden_occurrence = None
        if occurrence is None or self._did_execute:
            return
        try:
            if occurrence.isValid:
                occurrence.isLightBulbOn = True
        except RuntimeError:
            pass

    # ---------------------------------------------------------------- preview

    def _clear_preview_graphics(self):
        group = self._preview_graphics
        self._preview_graphics = None
        if group is not None:
            try:
                if group.isValid:
                    group.deleteMe()
            except RuntimeError:
                pass

    def _compute_preview_data(self):
        """Solves the arrangement and returns what to draw.

        The solve is transient: every model object it creates is deleted again
        before this returns. Returns (layout, outline_points) where layout is
        a list of (temporary BRepBody, name) at the solved positions.
        """
        design = _active_design(self.app)
        pairs = [(face, settings) for face, settings in self.inputs.parts_table.face_settings()
                 if face.isValid]
        faces = [face for face, _ in pairs]
        settings_list = [settings for _, settings in pairs]
        root = design.rootComponent
        self._clear_preview_graphics()

        outline_points: list[adsk.core.Point3D] = []
        temp_occurrence = root.occurrences.addNewComponent(adsk.core.Matrix3D.create())
        try:
            plane = self.inputs.plane.value[0] if self.inputs.plane.value else root.xYConstructionPlane
            sketch = envelope_builder.build_envelope_sketch_on(
                temp_occurrence.component,
                plane,
                self.inputs.rectangles.value,
                'Envelope',
                x_offset=envelope_builder.OffsetSpec(
                    value=self.inputs.offset_x.value, expression=self.inputs.offset_x.expression),
                y_offset=envelope_builder.OffsetSpec(
                    value=self.inputs.offset_y.value, expression=self.inputs.offset_y.expression),
            )
            if sketch.profiles.count != 1:
                raise RuntimeError('The envelope sketch did not produce a single profile.')
            lines = sketch.sketchCurves.sketchLines
            for index in range(lines.count):
                line = lines.item(index)
                if line.isConstruction or line.isReference:
                    continue
                geometry = line.worldGeometry
                outline_points.append(geometry.startPoint.copy())
                outline_points.append(geometry.endPoint.copy())

            options = engine.Options(
                object_spacing=self.inputs.spacing.value,
                frame_width=self.inputs.frame.value,
                placement_clearance=0.0,
                part_in_part=self.inputs.part_in_part.value,
                create_copies=self.inputs.create_copies.value,
            )
            layout = engine.compute_layout(design, faces, sketch.profiles.item(0), options,
                                           settings_list=settings_list)
        finally:
            if temp_occurrence.isValid:
                temp_occurrence.deleteMe()
        return layout, outline_points

    def _execute_preview(self, args: adsk.core.CommandEventArgs):
        # Draw only, and redraw on EVERY cycle while the preview is armed:
        # each preview cycle starts by rolling back the previous one (which
        # eats the previous graphics), and the compute's model churn causes
        # several such cycles right after the button click. Stale previews are
        # retired in input_changed when an input genuinely changes.
        pending = self._pending_preview
        if pending is None:
            return
        try:
            utils.fusion.log('[MA] preview: drawing graphics')
            self._clear_preview_graphics()
            layout, outline_points = pending
            root = _active_design(self.app).rootComponent
            group = root.customGraphicsGroups.add()
            for body, _name in layout:
                group.addBRepBody(body)
            if outline_points:
                coordinates = []
                for point in outline_points:
                    coordinates.extend((point.x, point.y, point.z))
                graphics_coordinates = adsk.fusion.CustomGraphicsCoordinates.create(coordinates)
                group.addLines(graphics_coordinates, [], False)
            self._preview_graphics = group
        except Exception as error:
            self.log_exception_traceback('preview draw', error)
            self.showError(str(error) or error.__class__.__name__)

    def _inputs_fingerprint(self):
        """Snapshot of all input VALUES; spurious input events caused by the
        preview compute's model churn leave the values unchanged."""
        ins = self.inputs
        try:
            # Read the live records (not the .value snapshot, which may lag one
            # event behind) and include the grain token itself so changing the
            # reference edge also registers as a change.
            parts = tuple(
                (record.rotation_cell.selectedItem.name if record.rotation_cell.selectedItem else '',
                 record.group_cell.value,
                 record.direction_token or '')
                for record in ins.parts_table.records)
            sheets = tuple(
                (spec.width_expression, spec.height_expression, spec.count)
                for spec in ins.rectangles.value)
            return (
                ins.faces.input.selectionCount if ins.faces.input else 0,
                ins.plane.input.selectionCount if ins.plane.input else 0,
                ins.update.input.selectionCount if ins.update.input else 0,
                round(ins.offset_x.value, 6),
                round(ins.offset_y.value, 6),
                round(ins.spacing.value, 6),
                round(ins.frame.value, 6),
                ins.part_in_part.value,
                ins.create_copies.value,
                sheets,
                parts,
            )
        except Exception:
            return None

    def _validate(self, args: adsk.core.ValidateInputsEventArgs):
        if self.inputs is None:
            return
        self.update_inputs_from_ui()
        message = self._input_error()
        self.showError(message)
        args.areInputsValid = message is None

    def _input_error(self) -> str | None:
        return envelope_builder.validate_specs(self.inputs.rectangles.value)

    def execute(self):
        error = self._input_error()
        if error:
            raise RuntimeError(error)
        self._did_execute = True
        self._pending_preview = None
        self._clear_preview_graphics()
        if self.inputs.update.value:
            old = cast(adsk.fusion.Occurrence, self.inputs.update.value[0])
            self._hidden_occurrence = None
            if old.isValid:
                old.deleteMe()
        self._run_arrangement()

    def _run_arrangement(self):
        design = _active_design(self.app)
        pairs = [(face, settings) for face, settings in self.inputs.parts_table.face_settings()
                 if face.isValid]
        faces = [face for face, _ in pairs]
        settings_list = [settings for _, settings in pairs]
        self._save_settings()
        model.save_sheet_specs(design, [
            {'width': spec.width_expression, 'height': spec.height_expression, 'count': spec.count}
            for spec in self.inputs.rectangles.value
        ])

        timeline_start = None
        if design.designType == adsk.fusion.DesignTypes.ParametricDesignType:
            timeline_start = design.timeline.count

        root = design.rootComponent
        result_occurrence = root.occurrences.addNewComponent(adsk.core.Matrix3D.create())
        result_component = result_occurrence.component
        result_component.name = engine.RESULT_COMPONENT_NAME

        plane = self.inputs.plane.value[0] if self.inputs.plane.value else root.xYConstructionPlane
        sketch = envelope_builder.build_envelope_sketch_on(
            result_component,
            plane,
            self.inputs.rectangles.value,
            'Envelope',
            x_offset=envelope_builder.OffsetSpec(
                value=self.inputs.offset_x.value, expression=self.inputs.offset_x.expression),
            y_offset=envelope_builder.OffsetSpec(
                value=self.inputs.offset_y.value, expression=self.inputs.offset_y.expression),
        )
        if sketch.profiles.count != 1:
            raise RuntimeError('The envelope sketch did not produce a single profile.')
        profile = sketch.profiles.item(0)

        options = engine.Options(
            object_spacing=self.inputs.spacing.value,
            frame_width=self.inputs.frame.value,
            placement_clearance=0.0,
            part_in_part=self.inputs.part_in_part.value,
            create_copies=self.inputs.create_copies.value,
        )
        engine.run(design, faces, profile, options,
                   timeline_start=timeline_start, settings_list=settings_list,
                   result_component=result_component)

        model.save_recipe(result_component, {
                'faces': [face.entityToken for face in faces],
                'sheets': [
                    {'width': spec.width_expression, 'height': spec.height_expression, 'count': spec.count}
                    for spec in self.inputs.rectangles.value
                ],
                'plane': self.inputs.plane.value[0].entityToken if self.inputs.plane.value else None,
                'offset_x': getattr(self.inputs.offset_x, 'expression', ''),
                'offset_y': getattr(self.inputs.offset_y, 'expression', ''),
                'spacing': getattr(self.inputs.spacing, 'expression', ''),
                'frame': getattr(self.inputs.frame, 'expression', ''),
                'part_in_part': self.inputs.part_in_part.value,
                'create_copies': self.inputs.create_copies.value,
            })

    def _save_settings(self):
        """Persists the table values as attributes on the bodies.

        Saving goes through the table's row records (body references) instead
        of re-deriving entity tokens: token strings for the same entity are not
        guaranteed to be identical across calls, so a token-keyed lookup can
        silently miss every part.
        """
        for body, part_settings in self.inputs.parts_table.body_settings():
            is_default = (
                part_settings.rotation == model.ROTATION_FREE
                and part_settings.direction_token is None
                and part_settings.group is None
            )
            if is_default:
                model.clear_settings(body)
            else:
                model.save_settings(body, part_settings)
