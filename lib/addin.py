import adsk.core, adsk.fusion
from typing import Callable, cast
from abc import ABC, abstractmethod
import re
import traceback
from . import defaults_store
from . import defaults_ui
from . import group_edit
from . import inputs as inp
from . import utils, ui_placement as plc
from .utils.fusion import new_event_handler
from .fusionbootstrap.runtime import RuntimeInfo


class Addin(ABC):
    app: adsk.core.Application
    ui: adsk.core.UserInterface
    inputs: inp.Inputs | None
    _error_field: adsk.core.TextBoxCommandInput | None
    _defaults_ui: defaults_ui.DefaultsUIManager
    _shutdown: bool
    _preview_error: str | None
    _base_timeline_count: int | None
    _last_validation_error: str | None
    #: True while execute() runs for an executePreview event. Lets add-ins
    #: skip work whose result the preview rollback discards anyway (e.g.
    #: cosmetic parameter renames, ~300 ms each in large documents).
    is_previewing: bool = False
    #: The "Preview" checkbox at the bottom of the dialog. Previews are
    #: opt-in per command invocation: in large documents building the
    #: preview costs many seconds per input change.
    _preview_checkbox: adsk.core.BoolValueCommandInput | None = None
    #: Group edit (see group_edit_enabled). The "Edit Existing" selection
    #: input, a target picked before the command started (applied once the
    #: command is active), the group being edited, and where the timeline
    #: marker returns to after the edit.
    _group_edit_input: adsk.core.SelectionCommandInput | None = None
    _group_edit_pending: group_edit.EditTarget | None = None
    _group_edit_target: group_edit.EditTarget | None = None
    _group_edit_restore: adsk.fusion.TimelineObject | None = None
    _group_edit_was_at_end: bool = True

    @property
    def create_command_id(self) -> str:
        return self.runtime_info.id + '_create'
    
    @property
    def resource_dir(self) -> str:
        return 'Resources'

    @abstractmethod
    def get_ui_placement(self) -> plc.UIPlacement:
        pass

    def get_ui_placements(self) -> list[plc.UIPlacement]:
        """All UI placements of the create command; override to place the
        button in more than one panel (e.g. Design and manufacturing model
        environments)."""
        return [self.get_ui_placement()]

    @property
    @abstractmethod
    def plugin_name(self) -> str:
        pass

    @property
    @abstractmethod
    def plugin_desc(self) -> str:
        pass

    @property
    @abstractmethod
    def plugin_tooltip(self) -> str:
        pass

    @property
    def has_command_ui(self) -> bool:
        return True

    @property
    def preview_enabled(self) -> bool:
        """Opt-in for a live preview while the dialog is open.

        When True, every valid input change re-runs execute() inside Fusion's
        executePreview transaction. This only suits add-ins whose execute()
        creates native features: Fusion rolls those back automatically before
        the next preview and before the final execute on OK.
        """
        return False

    @property
    def group_edit_enabled(self) -> bool:
        """Experimental opt-in: lets the dialog edit a timeline group this
        add-in created earlier (see lib/group_edit.py). Picking a member of
        the group - before starting the command or in the dialog's "Edit
        Existing" input - restores the dialog and rolls the timeline back to
        the group; OK rebuilds the group there and deletes the old one.

        Requires execute() to create all its features at the timeline
        marker and to call store_edit_state() on one member of the group it
        creates.
        """
        return False

    def __init__(self, runtime_info: RuntimeInfo):
        try:
            self.runtime_info = runtime_info
            self.app = adsk.core.Application.get()
            self.ui  = self.app.userInterface
            self._handlers = []
            self.inputs = None
            self._shutdown = False
            self._preview_error = None
            self._base_timeline_count = None
            self._last_validation_error = None
            self._defaults_ui = defaults_ui.DefaultsUIManager(
                self.app,
                self.defaults_file,
            )

            existing_cmd_def = self.ui.commandDefinitions.itemById(self.create_command_id)
            if existing_cmd_def:
                existing_cmd_def.deleteMe()

            # Create the command definition for the creation command.
            create_cmd_def = self.ui.commandDefinitions.addButtonDefinition(
                self.create_command_id,
                self.plugin_name,
                self.plugin_tooltip,
                self.resource_dir,
            )        

            # Add the create button to its panel(s).
            for placement in self.get_ui_placements():
                plc.add_command_to_ui(self.ui, placement, create_cmd_def, self.create_command_id)

            # Connect to the command created event for the create command.
            create_command_created = new_event_handler(self._create_ui, adsk.core.CommandCreatedEventHandler)
            create_cmd_def.commandCreated.add(create_command_created)
            self._handlers.append(create_command_created)
            utils.fusion.log(f"[ADDIN] Startup id={self.runtime_info.id}")

        except:
            utils.fusion.handleException()

    def __del__(self):
        self.shutdown()

    def shutdown(self):
        if self._shutdown:
            return
        try:
            utils.fusion.log(f"[ADDIN] Shutdown id={self.runtime_info.id}")
            for placement in self.get_ui_placements():
                plc.remove_command_from_ui(self.ui, placement, self.create_command_id)
            cmd_def = self.ui.commandDefinitions.itemById(self.create_command_id)
            if cmd_def:
                cmd_def.deleteMe()
            self._handlers.clear()
            self.inputs = None
        except:
            utils.fusion.handleException()
            return
        self._shutdown = True

    def _create_ui(self, args: adsk.core.EventArgs) -> None:
        command = adsk.core.CommandCreatedEventArgs.cast(args).command
        self._group_edit_pending = None
        self._group_edit_target = None
        if self.has_command_ui:
            if self.group_edit_enabled:
                # The timeline can only be rolled back once the command is
                # active; _activate picks this up.
                self._group_edit_pending = self._preselected_edit_target()
            self._initialize_inputs(command, None)
            self._attach_common_handlers(command)
        else:
            command.isAutoExecute = True

        on_execute = new_event_handler(self._execute, adsk.core.CommandEventHandler)
        command.execute.add(on_execute)
        self._handlers.append(on_execute)  

    def _validate(self, args: adsk.core.ValidateInputsEventArgs):
        pass

    def _apply_validation(
        self,
        args: adsk.core.ValidateInputsEventArgs,
        compute_error: Callable[[], str | None],
    ) -> None:
        """Standard validateInputs handling for add-ins with a preview.

        `compute_error` returns the add-in's validation message, or None when
        the inputs are valid. It is only called while the model is clean:
        once a preview is applied, the selected entities resolve to the
        geometry the preview modified (a cut shortens the selected edge, a
        join thickens the selected board), so measuring them would judge the
        preview instead of the document. The verdict from the last clean
        state is reused for as long as the preview is up; execute() re-runs
        the full validation against a clean model on every preview cycle and
        again on OK, so nothing invalid slips through.

        This also keeps the error field stable, which matters more than it
        looks: writing the field fires an input event, which makes Fusion
        abort and recompute the preview. Recomputing validation against the
        previewed model flip-flopped the message and drove an endless
        preview loop.
        """
        try:
            self.update_inputs_from_ui()
            if self._model_is_previewed():
                error = self._last_validation_error
            else:
                error = compute_error()
                self._last_validation_error = error
        except Exception as exc:
            error = str(exc)
        args.areInputsValid = error is None
        # A preview failure stays visible until validation itself objects.
        self.showError(error or self._preview_error)

    def _input_changed(self, args: adsk.core.InputChangedEventArgs):
        self.update_inputs_from_ui()
        if self.inputs:
            self.inputs.update_visibilities()
        if self._group_edit_input and args.input.id == self._group_edit_input.id:
            self._group_edit_selected(args.input)
            return
        if self._defaults_ui.handle_input_changed(args.input):
            return
        self.input_changed(args.input)

    def _execute(self, args: adsk.core.CommandEventArgs):
        try:
            if self.inputs is not None:
                self.update_inputs_from_ui()
                if self.preview_enabled:
                    # The preview shown until OK was clicked is rolled back
                    # right before this event; re-resolve selections it had
                    # invalidated.
                    self._refresh_stale_selections()
            edited_group_name = self._delete_edited_group()
            self.execute()
            if edited_group_name is not None:
                self._finish_group_edit(edited_group_name)
        except Exception as error:
            self.log_exception_traceback("execute", error)
            args.executeFailed = True
            args.executeFailedMessage = str(error) or error.__class__.__name__
        finally:
            self.inputs = None
            self._group_edit_target = None

    def store_edit_state(self, entity: adsk.core.Base) -> None:
        """Stores the dialog state on `entity`, a member of the timeline
        group execute() creates, so that group can be edited later. Skipped
        during previews, which Fusion rolls back anyway."""
        if not self.group_edit_enabled or self.is_previewing or self.inputs is None:
            return
        group_edit.write_state(entity, self.runtime_info.id, self.inputs)

    def _preselected_edit_target(self) -> group_edit.EditTarget | None:
        selections = self.ui.activeSelections
        for index in range(selections.count):
            target = group_edit.find_target(
                selections.item(index).entity,
                self.runtime_info.id,
            )
            if target:
                return target
        return None

    def _activate(self, args: adsk.core.CommandEventArgs):
        # Also fires when the command resumes after being suspended; the
        # pending target is consumed on the first activation.
        target = self._group_edit_pending
        self._group_edit_pending = None
        if target is None or self._group_edit_target is not None:
            return
        try:
            self._begin_group_edit(args.command, target)
        except Exception as error:
            self.log_exception_traceback("group edit", error)
            self.showError(f"Could not edit the selected group: {error}")

    def _group_edit_selected(self, selection_input: adsk.core.SelectionCommandInput):
        # Rolling the timeline back can drop the picked member from the
        # input again; edit mode lasts until the command ends either way.
        if self._group_edit_target is not None or selection_input.selectionCount == 0:
            return
        target = group_edit.find_target(
            selection_input.selection(0).entity,
            self.runtime_info.id,
        )
        if target is None:
            return
        try:
            self._begin_group_edit(selection_input.parentCommand, target)
        except Exception as error:
            self.log_exception_traceback("group edit", error)
            self.showError(f"Could not edit the selected group: {error}")

    def _begin_group_edit(self, command: adsk.core.Command, target: group_edit.EditTarget):
        design = adsk.fusion.Design.cast(self.app.activeProduct)
        if design is None or self.inputs is None:
            return
        timeline = design.timeline
        self._group_edit_was_at_end = timeline.markerPosition == timeline.count
        self._group_edit_restore = (
            timeline.item(timeline.markerPosition - 1)
            if timeline.markerPosition > 0
            else None
        )
        # Selections are restored from entity tokens, which must resolve to
        # the entities as they were before the group cut into them.
        target.group.rollTo(True)
        # Inside a command the roll only takes effect behind a step
        # boundary; without one the marker stays put. Cancel still undoes
        # it, as part of the command's transaction.
        command.beginStep()
        self._group_edit_target = target
        failed = group_edit.restore_state(self.inputs, target.state, design)
        self.update_inputs_from_ui()
        self.inputs.update_visibilities()
        if failed:
            utils.fusion.log(
                f"[ADDIN] Group edit id={self.runtime_info.id}: could not restore {', '.join(failed)}"
            )

    def _delete_edited_group(self) -> str | None:
        """Deletes the group being edited before execute() rebuilds it, so
        the new features can take the old names. When execute() fails,
        Fusion aborts the command and the group comes back. Returns the
        group's name, or None when not editing."""
        target = self._group_edit_target
        design = adsk.fusion.Design.cast(self.app.activeProduct)
        if target is None or design is None:
            return None
        timeline = design.timeline
        # Deleting a feature silently deletes every later feature that
        # references its geometry too (e.g. a fillet on a cut's edge).
        later: list[tuple[adsk.fusion.TimelineObject, str]] = []
        for index in range(target.group.index + 1, timeline.count):
            item = timeline.item(index)
            group = adsk.fusion.TimelineGroup.cast(item) if item.isGroup else None
            members = [group.item(i) for i in range(group.count)] if group else [item]
            later.extend((member, member.name) for member in members)
        name = target.group.name
        if not target.group.deleteMe(True):
            raise RuntimeError("Fusion could not delete the edited group.")
        lost = [member_name for member, member_name in later if not member.isValid]
        if lost:
            raise RuntimeError(
                "Rebuilding would delete later features that use geometry "
                f"of '{name}': {', '.join(lost)}. Nothing was changed."
            )
        return name

    def _finish_group_edit(self, name: str):
        """Gives the rebuilt group the edited group's name and moves the
        marker back to where it was."""
        design = adsk.fusion.Design.cast(self.app.activeProduct)
        if design is None:
            return
        timeline = design.timeline
        # The new features were created at the marker, so the marker sits
        # right after their group now.
        if timeline.markerPosition > 0:
            new_group = adsk.fusion.TimelineGroup.cast(
                timeline.item(timeline.markerPosition - 1)
            )
            if new_group:
                new_group.name = name
        restore = self._group_edit_restore
        if self._group_edit_was_at_end:
            timeline.moveToEnd()
        elif restore is not None and restore.isValid:
            restore.rollTo(False)

    def _execute_preview(self, args: adsk.core.CommandEventArgs):
        # Fusion only fires this event after validateInputs approved the
        # inputs, and it rolls the preview's model changes back on its own.
        # args.isValidResult stays False so OK always re-runs execute() from
        # the clean pre-preview state.
        if not self.preview_enabled or self.inputs is None:
            return
        # Previews are opt-in: only build one while the Preview checkbox is
        # ticked. Fusion has already rolled back the previous preview
        # transaction before this event, so returning here leaves the clean
        # model visible.
        if not self._preview_checkbox or not self._preview_checkbox.value:
            return
        try:
            self.update_inputs_from_ui()
            # Fusion aborted the previous preview transaction right before
            # this event, so the model is clean again — but selections the
            # previous preview invalidated (e.g. a cut splitting the selected
            # edge) are only cached as entity tokens now. Re-resolve them
            # before building the new preview. The selection input's UI is
            # deliberately left alone: writing selections from here would
            # fire input events that trigger further preview cycles.
            self._refresh_stale_selections()
            self.is_previewing = True
            try:
                self.execute()
            finally:
                self.is_previewing = False
            self._preview_error = None
            self.showError(None)
        except Exception as error:
            # Preview failures (e.g. geometry that cannot be built yet) belong
            # in the dialog; the command itself stays open. Subclasses that
            # write the error field from _validate must include
            # _preview_error there, or the next validation pass erases the
            # message again.
            self.log_exception_traceback("preview", error)
            self._preview_error = str(error) or error.__class__.__name__
            self.showError(self._preview_error)
    
    def _pre_select(self, args: adsk.core.EventArgs):
        event_args = adsk.core.SelectionEventArgs.cast(args)
        active_input = event_args.activeInput
        if self._group_edit_input and active_input and active_input.id == self._group_edit_input.id:
            event_args.isSelectable = group_edit.find_target(
                event_args.selection.entity,
                self.runtime_info.id,
            ) is not None
            return
        event_args.isSelectable = self.pre_select(active_input, event_args.selection.entity)

    def _initialize_inputs(self, command: adsk.core.Command, params: adsk.fusion.CustomFeatureParameters | None) -> None:
        self._preview_error = None
        self._last_validation_error = None
        # Timeline length of the clean document, taken at dialog open. While
        # an executePreview result is applied the count is higher; it drops
        # back when Fusion aborts the preview transaction. Used by
        # _model_is_previewed.
        self._base_timeline_count = None
        design = adsk.fusion.Design.cast(self.app.activeProduct)
        if design is not None:
            try:
                self._base_timeline_count = design.timeline.count
            except RuntimeError:
                pass
        self.inputs = self.create_inputs()
        if params is None:
            self._defaults_ui.apply_defaults(self.inputs)
        values_tab = command.commandInputs.addTabCommandInput('values_tab', 'Values')
        defaults_tab = command.commandInputs.addTabCommandInput('defaults_tab', 'Defaults')

        values_inputs = values_tab.children
        defaults_inputs = defaults_tab.children

        for input in self.inputs.inputs:
            input.create_input(values_inputs, params)
        self._group_edit_input = None
        if self.group_edit_enabled:
            # Below the add-in's own inputs, so its first selection input
            # keeps the initial focus.
            self._group_edit_input = values_inputs.addSelectionInput(
                'groupEditTarget',
                'Edit Existing',
                'Select a feature or sketch of an earlier result to edit it.',
            )
            self._group_edit_input.addSelectionFilter('Features')
            self._group_edit_input.addSelectionFilter('Sketches')
            self._group_edit_input.setSelectionLimits(0, 1)
        self._defaults_ui.create_ui(defaults_inputs, self.inputs)
        self._error_field = values_inputs.addTextBoxCommandInput('errorMessage', 'Error', '', 3, True)
        self._error_field.isVisible = False
        self._preview_checkbox = None
        if self.preview_enabled:
            self._preview_checkbox = values_inputs.addBoolValueInput(
                'addinPreviewEnabled',
                'Preview',
                True,
                '',
                False,
            )
            self._preview_checkbox.tooltip = (
                'Build a live preview of the result on every input change. '
                'Off by default: in large documents each preview can take '
                'several seconds.'
            )
        self.update_inputs_from_ui()
        self.inputs.update_visibilities()
        for input in self.inputs.inputs:
            self.input_changed(input.input)

    def _attach_common_handlers(self, command: adsk.core.Command) -> None:
        on_input_changed = new_event_handler(self._input_changed, adsk.core.InputChangedEventHandler)
        command.inputChanged.add(on_input_changed)
        self._handlers.append(on_input_changed)

        on_execute_preview = new_event_handler(self._execute_preview, adsk.core.CommandEventHandler)
        command.executePreview.add(on_execute_preview)
        self._handlers.append(on_execute_preview)

        on_pre_select = new_event_handler(self._pre_select, adsk.core.SelectionEventHandler)
        command.preSelect.add(on_pre_select)
        self._handlers.append(on_pre_select)

        on_validate = new_event_handler(self._validate, adsk.core.ValidateInputsEventHandler)
        command.validateInputs.add(on_validate)
        self._handlers.append(on_validate)

        if self.group_edit_enabled:
            on_activate = new_event_handler(self._activate, adsk.core.CommandEventHandler)
            command.activate.add(on_activate)
            self._handlers.append(on_activate)

    def update_inputs_from_ui(self):
        if self.inputs is None:
            raise RuntimeError("Add-in inputs are not initialized.")
        for input in self.inputs.inputs:
            input.update_from_input()

    def _selection_inputs(self) -> list[inp.SelectionByEntityTokenInput]:
        if self.inputs is None:
            return []
        # misc.is_instance like Inputs.__init__: after a dev-mode reload a
        # plain isinstance fails against a stale class object.
        return [
            input for input in self.inputs.inputs
            if utils.misc.is_instance(input, inp.SelectionByEntityTokenInput)
            or hasattr(input, 'refresh_stale_value')
        ]

    def _model_is_previewed(self) -> bool:
        """True while an executePreview result is applied to the model.

        Selected entities can stay valid but resolve to modified geometry in
        that state (e.g. a cut shortens the selected edge), so validation
        code must not do geometry work against the model then — it would
        produce verdicts about the preview instead of the clean document.
        """
        if not self.preview_enabled or self._base_timeline_count is None:
            return False
        design = adsk.fusion.Design.cast(self.app.activeProduct)
        if design is None:
            return False
        try:
            return design.timeline.count != self._base_timeline_count
        except RuntimeError:
            return False

    def _refresh_stale_selections(self):
        design = adsk.fusion.Design.cast(self.app.activeProduct)
        if design is None:
            return
        for input in self._selection_inputs():
            input.refresh_stale_value(design)

    @property
    def component(self) -> adsk.fusion.Component:
        return cast(adsk.fusion.Design, self.app.activeProduct).activeComponent
    
    def _expression_references_parameter(self, expression: str) -> bool:
        """True when the expression names a parameter of this design.

        Add-ins use this to decide whether writing a dimension's expression
        is worth its cost. A dimension is always created on geometry that
        already sits at the intended value, so writing a pure literal only
        swaps the literal Fusion computed for the authored one - whereas an
        expression that NAMES a parameter carries a link that cannot be
        recovered from the geometry and must be written.

        That distinction matters because a parameter write is a document
        update, and those scale with the size of the design: sub-millisecond
        in a small file, ~0.5 s in a 1700-feature assembly.

        Identifiers that are units ('mm') or functions ('sqrt') resolve to
        no parameter and are ignored. Returns True when the design cannot be
        resolved, so the failure mode is a redundant write, never a lost
        link.
        """
        if not expression:
            return False
        design = adsk.fusion.Design.cast(self.app.activeProduct)
        if design is None:
            return True
        for token in set(re.findall(r"[A-Za-z_][A-Za-z_0-9]*", expression)):
            if design.allParameters.itemByName(token):
                return True
        return False

    def _set_parameter_expression(
        self,
        parameter: adsk.fusion.ModelParameter,
        expression: str,
    ) -> None:
        """Write a dimension parameter's expression.

        During preview, the write is skipped when it would not move any
        geometry: each expression write costs ~300 ms in large documents,
        and the preview rollback discards the expression text anyway. On OK
        (and whenever the value would actually change) the write happens.
        """
        if self.is_previewing:
            design = adsk.fusion.Design.cast(self.app.activeProduct)
            if design:
                units = design.unitsManager
                try:
                    target = units.evaluateExpression(
                        expression,
                        units.defaultLengthUnits,
                    )
                except Exception:
                    target = None
                if target is not None and abs(target - parameter.value) < 1e-9:
                    return
        parameter.expression = expression

    def showError(self, message: str | None):
        if not self._error_field:
            return
        # Only write when something actually changes: every write to a command
        # input fires an inputChanged event, and each of those triggers a full
        # preview-rollback cycle in the command.
        if message:
            text = f"<font color=\"red\">{message}</font><br>"
            if not self._error_field.isVisible:
                self._error_field.isVisible = True
            if self._error_field.formattedText != text:
                self._error_field.formattedText = text
        else:
            if self._error_field.isVisible:
                self._error_field.isVisible = False
                self._error_field.formattedText = ''

    def log_exception_traceback(self, context: str, error: Exception):
        utils.fusion.log(
            f"[ADDIN] Error id={self.runtime_info.id} context={context}: {error}\n{traceback.format_exc()}"
        )
        
    def create_inputs(self) -> inp.Inputs:
        return inp.Inputs()

    @abstractmethod
    def execute(self):
        pass

    def pre_select(self, input, selection) -> bool:
        return True
    
    def input_changed(self, input):
        pass

    @property
    def defaults_file(self) -> str:
        return defaults_store.defaults_path(self.__class__.__module__, self.runtime_info.id)
