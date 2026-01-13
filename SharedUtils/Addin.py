import adsk.core, adsk.fusion
from typing import cast
from abc import ABC, abstractmethod
import Inputs
import utils
from utils.fusion import new_event_handler


class Addin(ABC):
    plugin_id = "<<plugin id>>"
    plugin_name = '<<plugin name>>>'
    plugin_desc = '<<plugin description>>'
    plugin_tooltip = '<<plugin tooltip>>'

    app: adsk.core.Application
    ui: adsk.core.UserInterface
    inputs: Inputs.Inputs | None
    _error_field: adsk.core.TextBoxCommandInput | None

    @property
    def create_command_id(self) -> str:
        return self.__class__.plugin_id + 'Create'

    def __init__(self):
        try:
            self.app = adsk.core.Application.get()
            self.ui  = self.app.userInterface
            self._handlers = []
            c = self.__class__
            resource_dir = 'Resources/' + c.plugin_name
            self.inputs = None

            # Create the command definition for the creation command.
            create_cmd_def = self.ui.commandDefinitions.addButtonDefinition(self.create_command_id, c.plugin_name, c.plugin_tooltip, resource_dir)        

            # Add the create button in the Modify panel of the SOLID tab.
            panel = self.ui.allToolbarPanels.itemById('SketchModifyPanel')
            for control in panel.controls:
                if control.id == self.create_command_id:
                    control.deleteMe()
                    break
            for ctrl in panel.controls:
                if ctrl.id == 'Offset':
                    panel.controls.addCommand(create_cmd_def, 'Offset', False)        

            # Connect to the command created event for the create command.
            create_command_created = new_event_handler(self._create_ui, adsk.core.CommandCreatedEventHandler)
            create_cmd_def.commandCreated.add(create_command_created)
            self._handlers.append(create_command_created)

        except:
            utils.fusion.handleException()

    def __del__(self):
        try:
            c = self.__class__
            # Remove all UI elements.
            solid_ws = self.ui.workspaces.itemById('FusionSolidEnvironment')
            panel = solid_ws.toolbarPanels.itemById('SolidModifyPanel')
            cntrl = panel.controls.itemById(self.create_command_id)
            if cntrl:
                cntrl.deleteMe()
                
            cmd_def = self.ui.commandDefinitions.itemById(self.create_command_id)
            if cmd_def:
                cmd_def.deleteMe()
        except:
            utils.fusion.handleException()

    def _create_ui(self, args: adsk.core.EventArgs) -> None:
        command = adsk.core.CommandCreatedEventArgs.cast(args).command
        self.inputs = self.create_inputs()
        for input in self.inputs.inputs:
            input.create_input(command.commandInputs, None)
        self._error_field = command.commandInputs.addTextBoxCommandInput('errorMessage', 'Error', '', 3, True)
        self._error_field.isVisible = False
        self.update_inputs_from_ui()
        self.inputs.update_visibilities()
        for input in self.inputs.inputs:
            self.input_changed(input.input)

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

        on_execute = new_event_handler(self._execute, adsk.core.CommandEventHandler)
        command.execute.add(on_execute)
        self._handlers.append(on_execute)  

    def _validate(self, args: adsk.core.ValidateInputsEventArgs):
        pass

    def _input_changed(self, args: adsk.core.InputChangedEventArgs):
        self.update_inputs_from_ui()
        if self.inputs:
            self.inputs.update_visibilities()
        self.input_changed(args.input)

    def _execute(self, args: adsk.core.CommandEventArgs):
        assert(self.inputs is not None)
        self.update_inputs_from_ui()
        self.execute()
        self.inputs = None

    def _execute_preview(self, args: adsk.core.CommandEventArgs):
        pass
    
    def _pre_select(self, args: adsk.core.EventArgs):
        event_args = adsk.core.SelectionEventArgs.cast(args)
        event_args.isSelectable = self.pre_select(event_args.activeInput, event_args.selection.entity)

    def update_inputs_from_ui(self):
        assert(self.inputs is not None)
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
        
    @abstractmethod
    def create_inputs(self) -> Inputs.Inputs:
        pass

    @abstractmethod
    def execute(self):
        pass

    def pre_select(self, input, selection) -> bool:
        return True
    
    def input_changed(self, input):
        pass

