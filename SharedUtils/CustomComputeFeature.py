import adsk.core, adsk.fusion, traceback
from typing import Callable
from abc import ABC, abstractmethod
import Inputs


class CustomComputeFeature(ABC):
    plugin_id = "<<plugin id>>"
    plugin_name = '<<plugin name>>>'
    plugin_desc = '<<plugin description>>'
    plugin_tooltip = '<<plugin tooltip>>'

    app: adsk.core.Application
    ui: adsk.core.UserInterface
    custom_feature_def: adsk.fusion.CustomFeature
    edited_custom_feature: adsk.fusion.CustomFeature 
    restore_timeline_object: adsk.fusion.TimelineObject
    is_rolled_for_edit: bool
    inputs: Inputs.Inputs

    @property
    def create_command_id(self) -> str:
        return self.__class__.plugin_id + 'Create'

    @property
    def edit_command_id(self) -> str:
        return self.__class__.plugin_id + 'Edit'

    def __init__(self):
        try:
            self.app = adsk.core.Application.get()
            self.ui  = self.app.userInterface
            self._handlers = []
            c = self.__class__
            resource_dir = 'Resources/' + c.plugin_name
            self._initial_selection = False

            # Create the command definition for the creation command.
            create_cmd_def = self.ui.commandDefinitions.addButtonDefinition(self.create_command_id, c.plugin_name, c.plugin_tooltip, resource_dir)        

            # Add the create button after the Emboss command in the CREATE panel of the SOLID tab.
            solidWS = self.ui.workspaces.itemById('FusionSolidEnvironment')
            panel = solidWS.toolbarPanels.itemById('SolidCreatePanel')
            panel.controls.addCommand(create_cmd_def, 'EmbossCmd', False)        

            # Create the command definition for the edit command.
            edit_cmd_def = self.ui.commandDefinitions.addButtonDefinition(self.edit_command_id, 
                                                                    'Edit ' + c.plugin_name, 
                                                                    'Edit ' + c.plugin_name, '')        

            # Connect to the command created event for the create command.
            create_command_created = CreateCommandCreatedHandler(self._create_ui)
            create_cmd_def.commandCreated.add(create_command_created)
            self._handlers.append(create_command_created)

            # Connect to the command created event for the edit command.
            edit_command_created = EditCommandCreatedHandler(self._create_ui)
            edit_cmd_def.commandCreated.add(edit_command_created)
            self._handlers.append(edit_command_created)

            # Create the custom feature definition.
            self.custom_feature_def = adsk.fusion.CustomFeatureDefinition.create(c.plugin_id, c.plugin_desc, resource_dir)
            self.custom_feature_def.editCommandId = self.edit_command_id

            # Connect to the compute event for the custom feature.
            compute_custom_feature = ComputeCustomFeature(self.compute)
            self.custom_feature_def.customFeatureCompute.add(compute_custom_feature)
            self._handlers.append(compute_custom_feature)

        except:
            show_message('Run Failed:\n{}'.format(traceback.format_exc()))

    def __del__(self):
        try:
            c = self.__class__
            # Remove all UI elements.
            solid_ws = self.ui.workspaces.itemById('FusionSolidEnvironment')
            panel = solid_ws.toolbarPanels.itemById('SolidCreatePanel')
            cntrl = panel.controls.itemById(self.create_command_id)
            if cntrl:
                cntrl.deleteMe()
                
            cmd_def = self.ui.commandDefinitions.itemById(self.create_command_id)
            if cmd_def:
                cmd_def.deleteMe()

            cmd_def = self.ui.commandDefinitions.itemById(self.edit_command_id)
            if cmd_def:
                cmd_def.deleteMe()
        except:
            show_message('Stop Failed:\n{}'.format(traceback.format_exc()))

    def _create_ui(self, command: adsk.core.Command) -> None:
        self.edited_custom_feature = self.ui.activeSelections.item(0).entity if self.ui.activeSelections.count > 0 else None
        editing = self.edited_custom_feature != None
        params = self.edited_custom_feature.parameters if editing else None

        self.inputs = self.create_inputs()
        for input in self.inputs.selections + self.inputs.values:
            input.create_input(command.commandInputs, params, editing)

        # Connect to the needed command related events.
        on_execute_preview = ExecutePreviewHandler(self._execute_preview)
        command.executePreview.add(on_execute_preview)
        self._handlers.append(on_execute_preview)

        on_pre_select = PreSelectHandler(self._pre_select)
        command.preSelect.add(on_pre_select)
        self._handlers.append(on_pre_select)

        on_validate = ValidateInputsHandler()
        command.validateInputs.add(on_validate)
        self._handlers.append(on_validate)

        if editing:
            onExecute = EditExecuteHandler(self._edit_execute)
            command.execute.add(onExecute)
            self._handlers.append(onExecute)  

            on_activate = EditActivateHandler(self._activate_edit)
            command.activate.add(on_activate)
            self._handlers.append(on_activate)
        else:
            on_execute = CreateExecuteHandler(self._execute)
            command.execute.add(on_execute)
            self._handlers.append(on_execute)  

    def _execute(self):
        self.cache_selection_inputs()
        base_feature = self.component.features.baseFeatures.add()
        end_feature = self.execute(base_feature)

        feat_input = self.component.features.customFeatures.createInput(self.custom_feature_def)
        for sel in self.inputs.selections:
            sel.create_dependencies(feat_input)
        for val in self.inputs.values:
            value_input = val.create_value_input_from_inputs()
            feat_input.addCustomParameter(val.id, val.name, value_input, val.units, True)

        feat_input.setStartAndEndFeatures(base_feature, end_feature)
        feature = self.component.features.customFeatures.add(feat_input)
        for sel in self.inputs.selections:
            sel.create_named_values(feature)

    def _execute_preview(self):
        self.cache_selection_inputs()
        base_feature = self.component.features.baseFeatures.add()
        self.execute(base_feature)

    def _edit_execute(self):
        self.cache_selection_inputs()
        # self.compute(self.edited_custom_feature)

        for sel in self.inputs.selections:
            sel.update_dependencies(self.edited_custom_feature)
        for val in self.inputs.values:
            val.update_param_from_input(self.edited_custom_feature.parameters)

        self.compute(self.edited_custom_feature)

        if self.is_rolled_for_edit:
            self.restore_timeline_object.rollTo(False)
            self.is_rolled_for_edit = False
        self.edited_custom_feature = None

    def _activate_edit(self, command: adsk.core.Command):
        # Save the current position of the timeline.
        des: adsk.fusion.Design = self.app.activeProduct
        timeline = des.timeline
        self.restore_timeline_object = timeline.item(timeline.markerPosition - 1)

        # Roll the timeline to just before the custom feature being edited.
        self.edited_custom_feature.timelineObject.rollTo(rollBefore = True)
        self.is_rolled_for_edit = True

        # Define a transaction marker so the the roll is not aborted with each change.
        command.beginStep()

        # Update selection inputs
        self._initial_selection = True
        for sel in self.inputs.selections:
            if not sel.is_editable:
                sel.input.hasFocus = False
            entities = sel.get_from_dependencies(self.edited_custom_feature)
            for e in entities:
                sel.input.addSelection(e)
        self._initial_selection = False

    def cache_selection_inputs(self):
        for input in self.inputs.values + self.inputs.selections:
            input.update_value_from_input()

    def _pre_select(self, entity):
        if self._initial_selection:
            return True
        else:
            return self.pre_select(entity)

    def pre_select(self, entity):
        return True

    @property
    @abstractmethod
    def component(self) -> adsk.fusion.Component:
        pass

    @abstractmethod
    def create_inputs(self) -> Inputs.Inputs:
        pass

    @abstractmethod
    def compute(self, feature: adsk.fusion.CustomFeature) -> None:
        pass

    @abstractmethod
    def execute(self, base_feature: adsk.fusion.BaseFeature) -> adsk.fusion.Feature:
        pass



class CreateCommandCreatedHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self, create_ui: Callable[[adsk.core.Command], None]):
        super().__init__()
        self.create_ui = create_ui
    def notify(self, args):
        try:
            event_args = adsk.core.CommandCreatedEventArgs.cast(args)
            self.create_ui(event_args.command)
        except:
            show_message('CommandCreated failed: {}\n'.format(traceback.format_exc()))

class EditCommandCreatedHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self, create_ui: Callable[[adsk.core.Command], None]):
        super().__init__()
        self.create_ui = create_ui
    def notify(self, args):
        try:
            event_args = adsk.core.CommandCreatedEventArgs.cast(args)
            self.create_ui(event_args.command)
        except:
            show_message('CommandCreated failed: {}\n'.format(traceback.format_exc()))

class ExecutePreviewHandler(adsk.core.CommandEventHandler):
    def __init__(self, execute: Callable):
        super().__init__()
        self.execute = execute
    def notify(self, args):
        try:
            event_args = adsk.core.CommandEventArgs.cast(args)        
            self.execute()
        except:
            event_args.executeFailed = True
            show_message('ExecutePreview: {}\n'.format(traceback.format_exc()))

class CreateExecuteHandler(adsk.core.CommandEventHandler):
    def __init__(self, execute: Callable):
        super().__init__()
        self.execute = execute
    def notify(self, args):
        try:
            event_args = adsk.core.CommandEventArgs.cast(args)        
            self.execute()
        except:
            event_args.executeFailed = True
            show_message('Execute: {}\n'.format(traceback.format_exc()))

class EditActivateHandler(adsk.core.CommandEventHandler):
    def __init__(self, activate_edit: Callable[[adsk.core.Command], None]):
        super().__init__()
        self.activate_edit = activate_edit
    def notify(self, args):
        try:
            event_args = adsk.core.CommandEventArgs.cast(args)
            self.activate_edit(event_args.command)
        except:
            show_message('Execute: {}\n'.format(traceback.format_exc()))

class EditExecuteHandler(adsk.core.CommandEventHandler):
    def __init__(self, execute: Callable):
        super().__init__()
        self.execute = execute
    def notify(self, args):
        try:
            event_args = adsk.core.CommandEventArgs.cast(args)        
            self.execute()
        except:
            event_args.executeFailed = True
            show_message('Execute: {}\n'.format(traceback.format_exc()))

class ComputeCustomFeature(adsk.fusion.CustomFeatureEventHandler):
    def __init__(self, compute: Callable[[adsk.fusion.CustomFeature], None]):
        super().__init__()
        self.compute = compute
    def notify(self, args):
        try:
            event_args: adsk.fusion.CustomFeatureEventArgs = args
            self.compute(event_args.customFeature)
        except:
            show_message('CustomFeatureCompute: {}\n'.format(traceback.format_exc()))


class PreSelectHandler(adsk.core.SelectionEventHandler):
    def __init__(self, pre_select: Callable[[adsk.core.Base], bool]):
        super().__init__()
        self.pre_select = pre_select
    def notify(self, args):
        try:
            event_args = adsk.core.SelectionEventArgs.cast(args)
            event_args.isSelectable = self.pre_select(event_args.selection.entity)
        except:
            show_message('PreSelectEventHandler: {}\n'.format(traceback.format_exc()))

class ValidateInputsHandler(adsk.core.ValidateInputsEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            event_args = adsk.core.ValidateInputsEventArgs.cast(args)
            return
            # Verify the inputs have valid expressions.
            # if not all( [_lengthInput.isValidExpression, _widthInput.isValidExpression,
            #             _depthInput.isValidExpression, _radiusInput.isValidExpression] ):
            #     eventArgs.areInputsValid = False
            #     return

            # Verify the sizes are valid.
            # diam = _radiusInput.value * 2
            # if diam + 0.01 > _lengthInput.value or diam + 0.01 > _widthInput.value:
            #     eventArgs.areInputsValid = False
            #     return
        except:
            show_message('ValidateInputsHandler: {}\n'.format(traceback.format_exc()))



def show_message(message, error = False):
    ui = adsk.core.Application.get().userInterface
    text_palette: adsk.core.TextCommandPalette = ui.palettes.itemById('TextCommands')
    text_palette.writeText(message)
    if error:
        ui.messageBox(message)