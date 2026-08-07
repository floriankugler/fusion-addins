import adsk.core, adsk.fusion
from typing import cast
from abc import ABC, abstractmethod
import traceback
from . import defaults_store
from . import defaults_ui
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
        if self.has_command_ui:
            self._initialize_inputs(command, None)
            self._attach_common_handlers(command)
        else:
            command.isAutoExecute = True

        on_execute = new_event_handler(self._execute, adsk.core.CommandEventHandler)
        command.execute.add(on_execute)
        self._handlers.append(on_execute)  

    def _validate(self, args: adsk.core.ValidateInputsEventArgs):
        pass

    def _input_changed(self, args: adsk.core.InputChangedEventArgs):
        self.update_inputs_from_ui()
        if self.inputs:
            self.inputs.update_visibilities()
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
            self.execute()
        except Exception as error:
            self.log_exception_traceback("execute", error)
            args.executeFailed = True
            args.executeFailedMessage = str(error) or error.__class__.__name__
        finally:
            self.inputs = None

    def _execute_preview(self, args: adsk.core.CommandEventArgs):
        # Fusion only fires this event after validateInputs approved the
        # inputs, and it rolls the preview's model changes back on its own.
        # args.isValidResult stays False so OK always re-runs execute() from
        # the clean pre-preview state.
        if not self.preview_enabled or self.inputs is None:
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
            self.execute()
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
        event_args.isSelectable = self.pre_select(event_args.activeInput, event_args.selection.entity)

    def _initialize_inputs(self, command: adsk.core.Command, params: adsk.fusion.CustomFeatureParameters | None) -> None:
        self._preview_error = None
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
        self._defaults_ui.create_ui(defaults_inputs, self.inputs)
        self._error_field = values_inputs.addTextBoxCommandInput('errorMessage', 'Error', '', 3, True)
        self._error_field.isVisible = False
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

    def update_inputs_from_ui(self):
        if self.inputs is None:
            raise RuntimeError("Add-in inputs are not initialized.")
        for input in self.inputs.inputs:
            input.update_from_input()

    def _selection_inputs(self) -> list[inp.SelectionByEntityTokenInput]:
        if self.inputs is None:
            return []
        # Duck-typed like Inputs.__init__: after a dev-mode reload isinstance
        # can fail against a stale class object.
        return [
            input for input in self.inputs.inputs
            if isinstance(input, inp.SelectionByEntityTokenInput)
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
