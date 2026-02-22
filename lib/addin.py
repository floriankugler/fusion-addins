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

    @property
    def create_command_id(self) -> str:
        return self.runtime_info.id + '_create'
    
    @property
    def resource_dir(self) -> str:
        return 'Resources'

    @abstractmethod
    def get_ui_placement(self) -> plc.UIPlacement:
        pass

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

    def __init__(self, runtime_info: RuntimeInfo):
        try:
            self.runtime_info = runtime_info
            self.app = adsk.core.Application.get()
            self.ui  = self.app.userInterface
            self._handlers = []
            self.inputs = None
            self._shutdown = False
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

            # Add the create button in the Modify panel of the SOLID tab.
            placement = self.get_ui_placement()
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
            placement = self.get_ui_placement()
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
        if self.inputs is not None:
            self.update_inputs_from_ui()
        self.execute()
        self.inputs = None

    def _execute_preview(self, args: adsk.core.CommandEventArgs):
        pass
    
    def _pre_select(self, args: adsk.core.EventArgs):
        event_args = adsk.core.SelectionEventArgs.cast(args)
        event_args.isSelectable = self.pre_select(event_args.activeInput, event_args.selection.entity)

    def _initialize_inputs(self, command: adsk.core.Command, params: adsk.fusion.CustomFeatureParameters | None) -> None:
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

    @property
    def component(self) -> adsk.fusion.Component:
        return cast(adsk.fusion.Design, self.app.activeProduct).activeComponent
    
    def showError(self, message: str | None):
        if not self._error_field:
            return
        if message:
            self._error_field.isVisible = True
            self._error_field.formattedText = f"<font color=\"red\">{message}</font><br>"
        else:
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
