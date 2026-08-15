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

# Opacity applied to the source parts of an arrangement, so it is obvious at a
# glance which parts are already covered. The dim is deliberately strong: while
# the dialog is open these very parts are also selection-highlighted, and a
# milder value is invisible underneath that highlight.
#
# It is applied while the dialog is open AND kept once the arrangement is
# created, so the marker survives into the model; only cancelling the dialog or
# taking a part out of the arrangement restores full opacity.
DIMMED_OPACITY = 0.15
FULL_OPACITY = 1.0


def run(context, runtime_info: RuntimeInfo):
    global _addin
    _addin = MultiArrange(runtime_info)
    _addin.register_restore_event()
    # Dev support: allow external tooling to restart this add-in by firing the
    # custom event '<id>_reload' (see lib/fusionbootstrap/reloader.py).
    from lib.fusionbootstrap import reloader
    entry = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'multi_arrange.py')
    reloader.ensure(runtime_info.id + '_reload', entry)


def stop(context):
    global _addin
    if _addin:
        _addin.unregister_restore_event()
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
    def __init__(self, units: str, initial_sheet_rows: list[tuple] | None = None):
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
            # No lower bound: an empty parts list is how an existing
            # arrangement is deleted (see MultiArrange._input_error). The
            # "at least one part" rule is enforced there instead, so that the
            # delete case can opt out of it.
            lower_bound=0,
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
                'smaller sheets first. The grain column says which way the '
                'wood grain runs on the physical sheet; grain-constrained '
                'parts follow it.'
            ),
            units=units,
            initial_rows=initial_sheet_rows,
            grain_column=True,
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

    def get_ui_placements(self) -> list[ui_placement.UIPlacement]:
        # Everywhere Fusion's own Arrange lives: the Design workspace's solid
        # and assembly Modify panels, plus their same-id twins in the
        # manufacturing model editing environment (product
        # 'MfgWorkingModelToolbar' — panel ids are only unique per product).
        command = ui_placement.PlacementSpec(
            id=self.create_command_id,
            anchor_id='ArrangeCommand',
            insert_before=False,
        )
        placements = [self.get_ui_placement()]
        placements.append(ui_placement.UIPlacement(
            panel_id='AssemblyModifyPanel', command=command))
        for panel_id in ('SolidModifyPanel', 'AssemblyModifyPanel'):
            placements.append(ui_placement.UIPlacement(
                panel_id=panel_id, command=command,
                workspace_id='MfgWorkingModelEnv'))
        return placements

    RESTORE_EVENT_SUFFIX = '_restore_selections'

    def register_restore_event(self):
        """Custom event for restoring selections AFTER Fusion's own event
        processing.

        The preview compute switches documents (scratch-document solve), and
        re-activating this document clears the dialog's selection inputs in
        activation events that run after the button handler — too late for a
        synchronous restore. A custom event is queued behind that processing,
        so its handler sees the cleared inputs and can put the selections
        back."""
        from lib.utils.fusion import new_event_handler
        event_id = self.runtime_info.id + self.RESTORE_EVENT_SUFFIX
        self._restore_event_id = event_id
        try:
            self.app.unregisterCustomEvent(event_id)
        except Exception:
            pass
        event = self.app.registerCustomEvent(event_id)
        handler = new_event_handler(self._on_restore_event, adsk.core.CustomEventHandler)
        event.add(handler)
        # Keep both alive for the add-in's lifetime.
        self._restore_event = event
        self._restore_handler = handler

    def unregister_restore_event(self):
        try:
            self.app.unregisterCustomEvent(self._restore_event_id)
        except Exception:
            pass

    def _on_restore_event(self, args):
        # Heals the dialog after ANY preview compute (also failed ones): the
        # scratch-document round-trip wipes the panel's rendering either way.
        if self.inputs is None:
            return
        utils.fusion.log('[MA] deferred display restore')
        self._rebuilding = True
        try:
            if self._selection_snapshot:
                self._restore_selections(self._selection_snapshot)
            self._refresh_dialog_display()
        finally:
            self._rebuilding = False
        # Re-baseline the fingerprints on the rebuilt inputs: re-created value
        # cells may re-normalize expressions ('2000 mm' -> '2000.00 mm'), and
        # a stale baseline would make the next input event look like a real
        # change, retiring the preview or the notice.
        if self._pending_preview is not None:
            self._preview_fingerprint = self._inputs_fingerprint()
            if self._pending_placements is not None and self._preview_fingerprint is not None:
                self._solved_cache = (self._preview_fingerprint, self._pending_placements)
        if self._notice is not None:
            self._notice_fingerprint = self._inputs_fingerprint()

    def _refresh_dialog_display(self):
        """Re-creates the table rows so the dialog panel renders them again.

        After the scratch-document round-trip the dialog panel discards its
        rendered table rows, even though the underlying command inputs still
        hold every row and value (verified headless: rowCount, cell values
        and selections all remain intact — which is also why OK keeps
        working). Merely toggling visibility does not bring the rows back;
        deleting and re-adding them does. The rebuilds preserve all edited
        values, so the input fingerprint is unchanged and the armed preview
        survives the resulting input events as spurious.
        """
        try:
            self.inputs.rectangles.rebuild()
        except Exception as error:
            self.log_exception_traceback('sheets table rebuild', error)
        try:
            self.inputs.parts_table.rebuild()
        except Exception as error:
            self.log_exception_traceback('parts table rebuild', error)

    def _initialize_inputs(self, command, params):
        self._ui_ready = False
        super()._initialize_inputs(command, params)
        self._ui_ready = True

    def create_inputs(self) -> ArrangeInputs:
        self._preview_graphics: adsk.fusion.CustomGraphicsGroup | None = None
        self._pending_preview = None
        self._preview_fingerprint = None
        self._notice: str | None = None
        self._notice_fingerprint = None
        self._did_execute = False
        self._update_token: str | None = None
        self._update_was_visible = True
        # Opacity each part had when this dialog first saw it, so cancelling can
        # put it back. Written once per part and never dropped: a part that
        # leaves the table and comes back would otherwise have our own dim
        # recorded as its original, and cancel would leave it dimmed.
        self._original_opacity: dict[str, float] = {}
        # Parts currently dimmed by this dialog.
        self._dimmed: set[str] = set()
        # Face tokens of the arrangement being replaced, so execute can un-dim
        # the parts that were dropped from it.
        self._recipe_face_tokens: list[str] = []
        # (fingerprint, sketch-space placements) of the last preview solve;
        # execute reuses the placements when the inputs are still identical,
        # skipping the solve entirely.
        self._solved_cache: tuple | None = None
        self._pending_placements: list[tuple[float, ...]] | None = None
        # Selections as they were when the preview was computed. The scratch
        # document's close re-activates this document, and Fusion clears the
        # dialog's selection inputs in the activation events AFTER the
        # button's input_changed handler (and its synchronous restore) has
        # returned — so the restore is re-applied on every preview cycle
        # while the preview is armed, like the dimming and the update-hide.
        self._selection_snapshot: list | None = None
        # Sheet-plane sketch frames by plane entity token: probing one costs
        # ~2 s in a large design, and a plane's frame cannot change while the
        # dialog is open.
        self._plane_frames: dict[str, adsk.core.Matrix3D] = {}
        self._destroy_hooked = False
        design = self.app.activeDocument.products.itemByProductType('DesignProductType')
        units = design.unitsManager.defaultLengthUnits if design else 'mm'
        initial_rows = None
        fusion_design = adsk.fusion.Design.cast(design) if design else None
        if fusion_design:
            stored = model.load_sheet_specs(fusion_design)
            if stored:
                initial_rows = [
                    (row.get('width', ''), row.get('height', ''), int(row.get('count', 1)),
                     bool(row.get('grain_along_width', False)))
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
        # The deferred display rebuild deletes and re-adds table rows; input
        # events dispatched mid-rebuild see a half-empty table, and the
        # fingerprint mismatch would retire the freshly armed preview and any
        # notice as if the user had changed something.
        if getattr(self, '_rebuilding', False):
            return
        self.inputs.rectangles.handle_input_changed(input)
        if self.inputs.parts_table.handle_input_changed(input):
            self._set_notice(self.inputs.parts_table.message)
            if (self.inputs.faces.input and
                    self.inputs.faces.input.selectionCount != len(self.inputs.parts_table.records)):
                self._rebuild_faces_from_table()
        if self.inputs.faces.input and input.id == self.inputs.faces.input.id:
            snapshot = self._snapshot_selections([self.inputs.plane, self.inputs.update])
            self.inputs.parts_table.sync(
                [cast(adsk.fusion.BRepFace, face) for face in self.inputs.faces.value])
            self._restore_selections(snapshot)
        if getattr(self, '_ui_ready', False):
            self._hook_destroy(input.parentCommand)
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
                if not error and not self.inputs.parts_table.records:
                    # An empty list is valid input (it deletes the selected
                    # arrangement on OK), but there is nothing to preview.
                    error = 'Nothing to preview: the parts list is empty.'
                if error:
                    self._set_notice(error)
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
                    self._selection_snapshot = snapshot
                    try:
                        self._pending_preview = self._compute_preview_data()
                    finally:
                        # Heal the dialog once Fusion's document-activation
                        # aftermath (which wipes the panel's rendering) has
                        # run — a failed compute switches documents all the
                        # same, so this runs unconditionally.
                        self._restore_selections(snapshot)
                        self.app.fireCustomEvent(self._restore_event_id)
                    self._preview_fingerprint = self._inputs_fingerprint()
                    if self._pending_placements is not None and self._preview_fingerprint is not None:
                        self._solved_cache = (self._preview_fingerprint, self._pending_placements)
                    self._set_notice(None)
            except Exception as error:
                # Failures like "not enough room" belong in the dialog, not
                # only in the console.
                self.log_exception_traceback('preview', error)
                self._set_notice(str(error) or error.__class__.__name__)
        elif (self._pending_preview is not None or self._preview_graphics is not None
                or self._notice is not None):
            fingerprint = self._inputs_fingerprint()
            if self._notice is not None and fingerprint != self._notice_fingerprint:
                self._set_notice(None)
            if ((self._pending_preview is not None or self._preview_graphics is not None)
                    and fingerprint != self._preview_fingerprint):
                # A real change: retire the preview like native previews do.
                # The selection snapshot goes with it — restoring selections
                # past this point would fight the user's own edits.
                utils.fusion.log(f'[MA] preview: cleared by real change of {input.id}')
                self._pending_preview = None
                self._selection_snapshot = None
                self._clear_preview_graphics()
            else:
                utils.fusion.log(f'[MA] preview: ignoring spurious change of {input.id}')

    def _set_notice(self, message: str | None):
        """Shows a message until the inputs genuinely change.

        validateInputs runs after every input event and would otherwise
        overwrite the field immediately, and writing the field is itself an
        input event — so the message is pinned to the input fingerprint it was
        raised for.
        """
        self._notice = message
        self._notice_fingerprint = self._inputs_fingerprint()
        self.showError(self._input_error() or message)

    # ------------------------------------------------------- update existing

    def _handle_update_selection(self, input):
        if not self.inputs.update.value:
            # Selection cleared: give the previously selected arrangement its
            # visibility back and stop tracking it.
            self._restore_update_visibility()
            return
        occurrence = cast(adsk.fusion.Occurrence, self.inputs.update.value[0])
        recipe = model.load_recipe(occurrence.component)
        if recipe is None:
            self.showError('The selected component holds no Multi-Arrange arrangement.')
            self.inputs.update.input.clearSelection()
            return
        # Restore a previously selected arrangement first, in case the user
        # switches the update selection mid-dialog.
        self._restore_update_visibility()
        self._apply_recipe(recipe)
        # The arrangement is tracked by its entity token, not by the occurrence
        # reference or a document attribute: references get invalidated by the
        # preview's model churn, and attributes written during input handling
        # are rolled back by the preview cycle before execute ever sees them.
        self._update_token = occurrence.entityToken
        self._update_was_visible = occurrence.isLightBulbOn
        occurrence.isLightBulbOn = False
        self._hook_destroy(input.parentCommand)

    def _resolve_update_occurrence(self) -> adsk.fusion.Occurrence | None:
        """Fresh occurrence for the tracked arrangement, or None."""
        if not self._update_token:
            return None
        design = adsk.fusion.Design.cast(self.app.activeProduct)
        if design is None:
            return None
        try:
            entities = design.findEntityByToken(self._update_token)
        except RuntimeError:
            return None
        for entity in entities or []:
            occurrence = adsk.fusion.Occurrence.cast(entity)
            if occurrence:
                return occurrence
        return None

    def _restore_update_visibility(self):
        occurrence = self._resolve_update_occurrence()
        if occurrence is not None:
            try:
                occurrence.isLightBulbOn = self._update_was_visible
            except RuntimeError:
                pass
        self._update_token = None
        self._update_was_visible = True

    def _reapply_update_hidden(self):
        """Re-hides the arrangement being updated.

        Every preview cycle starts by rolling the document back to the state
        before the dialog's edits, which switches the light bulb back on. The
        hide is therefore re-applied on each cycle, the same self-healing
        approach the preview graphics use.
        """
        occurrence = self._resolve_update_occurrence()
        if occurrence is not None and occurrence.isLightBulbOn:
            try:
                occurrence.isLightBulbOn = False
            except RuntimeError:
                pass

    def _reapply_display_state(self):
        """Restores the dialog's display changes, on every preview cycle.

        The hidden arrangement and the dimmed parts are both document state,
        so each preview cycle's rollback undoes them and both are re-applied
        here.

        This is the ONLY place the open dialog dims from. Doing it from
        `input_changed` as well churned the document while Fusion was handling
        a selection, which silently CLEARED the parts selection input —
        picking a second top face just replaced the first. Writing from the
        preview cycle instead is the same self-healing pattern the light-bulb
        hide has always used safely.
        """
        self._reapply_update_hidden()
        self._sync_dimming()
        # The scratch document's activation churn clears the dialog's
        # selection inputs after the preview compute returns; put them back
        # while the preview is armed.
        if self._pending_preview is not None and self._selection_snapshot:
            self._restore_selections(self._selection_snapshot)

    # ---------------------------------------------------------------- dimming

    def _resolve_body(self, token: str) -> adsk.fusion.BRepBody | None:
        design = adsk.fusion.Design.cast(self.app.activeProduct)
        if design is None:
            return None
        try:
            entities = design.findEntityByToken(token)
        except RuntimeError:
            return None
        for entity in entities or []:
            body = adsk.fusion.BRepBody.cast(entity)
            if body:
                return body
        return None

    def _record_body(self, record) -> adsk.fusion.BRepBody | None:
        """The record's body, re-resolved when its proxy went stale."""
        body = record.body
        try:
            if body is not None and body.isValid:
                return body
        except RuntimeError:
            pass
        return self._resolve_body(record.token)

    def _set_opacity(self, body: adsk.fusion.BRepBody, opacity: float):
        try:
            if abs(body.opacity - opacity) > 1e-6:
                body.opacity = opacity
        except RuntimeError:
            pass

    def _sync_dimming(self):
        """Dims the parts of the arrangement, restores those that left it.

        Only ever called from the preview cycle — see _reapply_display_state.
        """
        if self.inputs is None:
            return
        wanted: dict[str, adsk.fusion.BRepBody] = {}
        for record in self.inputs.parts_table.records:
            body = self._record_body(record)
            if body is not None:
                wanted[record.token] = body

        for token in list(self._dimmed):
            if token not in wanted:
                self._restore_opacity(token, undim=True)

        for token, body in wanted.items():
            try:
                if token not in self._original_opacity:
                    # Every cycle starts rolled back to the pre-dialog state,
                    # so a part's first sighting shows its true opacity.
                    self._original_opacity[token] = body.opacity
            except RuntimeError:
                continue
            self._set_opacity(body, DIMMED_OPACITY)
            self._dimmed.add(token)

    def _restore_opacity(self, token: str, undim: bool = False):
        """Puts a part's opacity back.

        `undim` marks the "taken out of the arrangement" case: a part that was
        already dimmed when the dialog opened belongs to an earlier
        arrangement, and dropping it from this one means it is not arranged at
        all any more, so it goes back to fully visible instead of to the dim it
        arrived with. Cancelling must NOT do that — there the point is to leave
        the model exactly as it was found, dim included.
        """
        self._dimmed.discard(token)
        original = self._original_opacity.get(token)
        if original is None:
            return
        body = self._resolve_body(token)
        if body is None:
            return
        if undim and abs(original - DIMMED_OPACITY) < 1e-6:
            original = FULL_OPACITY
        self._set_opacity(body, original)

    def _restore_all_opacity(self):
        for token in list(self._dimmed):
            self._restore_opacity(token)

    def _persist_dimming(self):
        """Marks the arranged source parts by dimming them, from execute.

        Called from execute so the dim lands in execute's own transaction and
        becomes part of the model; it deliberately outlives the dialog, so the
        parts an arrangement already covers stay recognizable. Parts dropped
        from an arrangement that is being replaced are un-dimmed in the same
        pass, since they are no longer covered by anything.
        """
        if self.inputs is None:
            return
        arranged = set()
        for record in self.inputs.parts_table.records:
            body = self._record_body(record)
            if body is None:
                continue
            arranged.add(body.entityToken)
            self._set_opacity(body, DIMMED_OPACITY)

        for token in self._recipe_face_tokens:
            body = self._resolve_face_body(token)
            if body is None or body.entityToken in arranged:
                continue
            # Was part of the arrangement being replaced, is not part of the
            # new one: nothing covers it any more.
            self._set_opacity(body, FULL_OPACITY)

    def _resolve_face_body(self, face_token: str) -> adsk.fusion.BRepBody | None:
        design = adsk.fusion.Design.cast(self.app.activeProduct)
        if design is None:
            return None
        try:
            entities = design.findEntityByToken(face_token)
        except RuntimeError:
            return None
        for entity in entities or []:
            face = adsk.fusion.BRepFace.cast(entity)
            if face:
                return face.body
        return None

    def _apply_recipe(self, recipe: dict):
        design = _active_design(self.app)
        ins = self.inputs

        ins.faces.input.clearSelection()
        self._recipe_face_tokens = list(recipe.get('faces', []))
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
        for key, target in (('part_in_part', ins.part_in_part),):
            if key in recipe and target.input:
                target.input.value = bool(recipe[key])
                target.update_from_input()

        self._set_notice(
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
        self._selection_snapshot = None
        self._clear_preview_graphics()
        if self._did_execute:
            # The dim stays on as a permanent marker of what is arranged;
            # execute wrote it inside its own transaction.
            return
        # Cancelled: undo both display changes the dialog made.
        self._restore_all_opacity()
        self._restore_update_visibility()

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

        The solve runs in a scratch document (engine.solve_in_scratch); the
        only touch on the user's design is a probe sketch to read the sheet
        plane's frame, deleted immediately and cached per plane. Returns
        (layout, outline_points) where layout is a list of (temporary
        BRepBody, name) at the solved positions.
        """
        design = _active_design(self.app)
        pairs = [(face, settings) for face, settings in self.inputs.parts_table.face_settings()
                 if face.isValid]
        faces = [face for face, _ in pairs]
        settings_list = [settings for _, settings in pairs]
        self._clear_preview_graphics()
        self._pending_placements = None

        plane = self.inputs.plane.value[0] if self.inputs.plane.value else None
        plane_transform = self._plane_transform(design, plane)
        options = engine.Options(
            object_spacing=self.inputs.spacing.value,
            frame_width=self.inputs.frame.value,
            placement_clearance=0.0,
            part_in_part=self.inputs.part_in_part.value,
            create_copies=True,
        )
        layout = engine.compute_layout(design, faces, self._envelope_spec(),
                                       plane_transform, options,
                                       settings_list=settings_list)
        self._pending_placements = layout.placements
        return layout.bodies, layout.outline

    def _envelope_spec(self) -> engine.EnvelopeSpec:
        # Grain is always the envelope's Y axis, so a sheet whose grain runs
        # along its width enters the envelope rotated (width and height
        # swapped). The nested result shows that sheet standing on its side —
        # which is exactly the cut layout relative to the grain.
        rectangles = []
        for spec in self.inputs.rectangles.value:
            if spec.grain_along_width:
                rectangles.append(envelope_builder.RectangleSpec(
                    width=spec.height, width_expression=spec.height_expression,
                    height=spec.width, height_expression=spec.width_expression,
                    count=spec.count))
            else:
                rectangles.append(spec)
        return engine.EnvelopeSpec(
            rectangles=rectangles,
            x_offset=envelope_builder.OffsetSpec(
                value=self.inputs.offset_x.value, expression=self.inputs.offset_x.expression),
            y_offset=envelope_builder.OffsetSpec(
                value=self.inputs.offset_y.value, expression=self.inputs.offset_y.expression),
        )

    def _plane_transform(self, design: adsk.fusion.Design, plane) -> adsk.core.Matrix3D:
        """The sketch frame (sketch space -> world) a sketch on `plane` gets.

        Fusion assigns sketch axes when a sketch is created on a plane or
        face, so the frame is read from a probe sketch (created without edge
        projection) and the probe is deleted again. `plane` None means the
        root X-Y construction plane, whose sketch frame is the identity.
        """
        if plane is None:
            return adsk.core.Matrix3D.create()
        try:
            token = plane.entityToken
        except RuntimeError:
            token = None
        if token and token in self._plane_frames:
            return self._plane_frames[token].copy()
        # The probe lives in a throwaway component: creating a sketch directly
        # on the root of a large design costs several seconds, while the same
        # sketch inside a fresh (identity-placed) component is cheap and gets
        # the identical frame.
        temp_occurrence = design.rootComponent.occurrences.addNewComponent(
            adsk.core.Matrix3D.create())
        try:
            sketch = temp_occurrence.component.sketches.addWithoutEdges(plane)
            transform = sketch.transform
        finally:
            temp_occurrence.deleteMe()
        if token:
            self._plane_frames[token] = transform.copy()
        return transform

    def _execute_preview(self, args: adsk.core.CommandEventArgs):
        # Draw only, and redraw on EVERY cycle while the preview is armed:
        # each preview cycle starts by rolling back the previous one (which
        # eats the previous graphics), and the compute's model churn causes
        # several such cycles right after the button click. Stale previews are
        # retired in input_changed when an input genuinely changes.
        self._reapply_display_state()
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
            # event behind).
            parts = tuple(
                (record.rotation_cell.selectedItem.name if record.rotation_cell.selectedItem else '',
                 record.group_cell.value)
                for record in ins.parts_table.records)
            sheets = tuple(
                (spec.width_expression, spec.height_expression, spec.count,
                 spec.grain_along_width)
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
                sheets,
                parts,
            )
        except Exception:
            return None

    def _validate(self, args: adsk.core.ValidateInputsEventArgs):
        if self.inputs is None:
            return
        if getattr(self, '_rebuilding', False):
            # Mid-rebuild the tables are half-empty; leave the dialog state
            # untouched until the rebuild is done.
            return
        self.update_inputs_from_ui()
        message = self._input_error()
        # Keep a pending notice (preview failure, table hint) visible; only a
        # genuine input problem takes precedence over it.
        self.showError(message or self._notice)
        args.areInputsValid = message is None

    def _input_error(self) -> str | None:
        if self.inputs.parts_table.records:
            return envelope_builder.validate_specs(self.inputs.rectangles.value)
        # An empty parts list together with a selected arrangement means
        # "delete that arrangement": OK is allowed, and the sheet sizes do not
        # matter because nothing is going to be nested.
        if self._resolve_update_occurrence() is not None:
            return None
        return 'Select the top face of at least one part.'

    def execute(self):
        error = self._input_error()
        if error:
            raise RuntimeError(error)
        self._did_execute = True
        self._pending_preview = None
        self._clear_preview_graphics()
        # Delete the arrangement being updated, resolved from its entity token
        # (references and attributes from selection time do not survive the
        # dialog's preview cycles).
        old = self._resolve_update_occurrence()
        self._update_token = None
        if old is not None:
            old.deleteMe()
        # An empty parts list deletes the selected arrangement without building
        # a replacement. _persist_dimming then finds nothing arranged and puts
        # every part of the deleted arrangement back to full opacity.
        if self.inputs.parts_table.records:
            self._run_arrangement()
        self._persist_dimming()

    def _run_arrangement(self):
        design = _active_design(self.app)
        pairs = [(face, settings) for face, settings in self.inputs.parts_table.face_settings()
                 if face.isValid]
        faces = [face for face, _ in pairs]
        settings_list = [settings for _, settings in pairs]
        self._save_settings()
        model.save_sheet_specs(design, [
            {'width': spec.width_expression, 'height': spec.height_expression, 'count': spec.count,
             'grain_along_width': spec.grain_along_width}
            for spec in self.inputs.rectangles.value
        ])

        timeline_start = None
        if design.designType == adsk.fusion.DesignTypes.ParametricDesignType:
            # Marker, not count: features are inserted at the marker, and
            # rolled-back features may be parked at the end of the timeline.
            timeline_start = design.timeline.markerPosition

        root = design.rootComponent
        # The sheet plane's frame must be probed BEFORE the result component
        # exists, so the probe's temporary churn stays out of the timeline
        # group range.
        plane = self.inputs.plane.value[0] if self.inputs.plane.value else None
        plane_transform = self._plane_transform(design, plane)

        result_occurrence = root.occurrences.addNewComponent(adsk.core.Matrix3D.create())
        result_component = result_occurrence.component
        result_component.name = engine.RESULT_COMPONENT_NAME

        options = engine.Options(
            object_spacing=self.inputs.spacing.value,
            frame_width=self.inputs.frame.value,
            placement_clearance=0.0,
            part_in_part=self.inputs.part_in_part.value,
            create_copies=True,
        )
        # Reuse the preview's solved placements when the inputs are still
        # exactly the ones the preview was computed for — the solver is
        # deterministic, so re-solving would produce the same layout.
        cached_placements = None
        fingerprint = self._inputs_fingerprint()
        if (self._solved_cache is not None and fingerprint is not None
                and self._solved_cache[0] == fingerprint):
            cached_placements = self._solved_cache[1]
            utils.fusion.log('[MA] execute: reusing preview placements')
        engine.run(design, faces, self._envelope_spec(), options,
                   plane_transform=plane_transform,
                   timeline_start=timeline_start, settings_list=settings_list,
                   result_occurrence=result_occurrence,
                   cached_placements=cached_placements)

        model.save_recipe(result_component, {
                'faces': [face.entityToken for face in faces],
                'sheets': [
                    {'width': spec.width_expression, 'height': spec.height_expression, 'count': spec.count,
             'grain_along_width': spec.grain_along_width}
                    for spec in self.inputs.rectangles.value
                ],
                'plane': self.inputs.plane.value[0].entityToken if self.inputs.plane.value else None,
                'offset_x': getattr(self.inputs.offset_x, 'expression', ''),
                'offset_y': getattr(self.inputs.offset_y, 'expression', ''),
                'spacing': getattr(self.inputs.spacing, 'expression', ''),
                'frame': getattr(self.inputs.frame, 'expression', ''),
                'part_in_part': self.inputs.part_in_part.value,
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
                part_settings.rotation == model.ROTATION_GRAIN
                and part_settings.direction_token is None
                and part_settings.group is None
            )
            if is_default:
                model.clear_settings(body)
            else:
                model.save_settings(body, part_settings)
