import adsk.core, adsk.fusion, traceback
from typing import Callable
from abc import ABC, abstractmethod
import Inputs
from utils.fusion import new_event_handler


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
            self.inputs = None

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
            create_command_created = new_event_handler(self._create_ui, adsk.core.CommandCreatedEventHandler)
            create_cmd_def.commandCreated.add(create_command_created)
            self._handlers.append(create_command_created)

            # Connect to the command created event for the edit command.
            edit_command_created = new_event_handler(self._create_ui, adsk.core.CommandCreatedEventHandler)
            edit_cmd_def.commandCreated.add(edit_command_created)
            self._handlers.append(edit_command_created)

            # Create the custom feature definition.
            self.custom_feature_def = adsk.fusion.CustomFeatureDefinition.create(c.plugin_id, c.plugin_desc, resource_dir)
            self.custom_feature_def.editCommandId = self.edit_command_id

            # Connect to the compute event for the custom feature.
            compute_custom_feature = new_event_handler(self._compute, adsk.fusion.CustomFeatureEventHandler)
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

    def _create_ui(self, args: adsk.core.EventArgs) -> None:
        command = adsk.core.CommandCreatedEventArgs.cast(args).command

        self.edited_custom_feature = self.ui.activeSelections.item(0).entity if self.ui.activeSelections.count > 0 else None
        editing = self.edited_custom_feature != None
        params = self.edited_custom_feature.parameters if editing else None

        self.inputs = self.create_inputs()
        for input in self.inputs.selections + self.inputs.values:
            input.create_input(command.commandInputs, params, editing)

        # Connect to the needed command related events.
        on_execute_preview = new_event_handler(self._execute_preview, adsk.core.CommandEventHandler)
        command.executePreview.add(on_execute_preview)
        self._handlers.append(on_execute_preview)

        on_pre_select = new_event_handler(self._pre_select, adsk.core.SelectionEventHandler)
        command.preSelect.add(on_pre_select)
        self._handlers.append(on_pre_select)

        on_validate = new_event_handler(lambda _: _, adsk.core.ValidateInputsEventHandler)
        command.validateInputs.add(on_validate)
        self._handlers.append(on_validate)

        if editing:
            onExecute = new_event_handler(self._edit_execute, adsk.core.CommandEventHandler)
            command.execute.add(onExecute)
            self._handlers.append(onExecute)  

            on_activate = new_event_handler(self._activate_edit, adsk.core.CommandEventHandler)
            command.activate.add(on_activate)
            self._handlers.append(on_activate)
        else:
            on_execute = new_event_handler(self._execute, adsk.core.CommandEventHandler)
            command.execute.add(on_execute)
            self._handlers.append(on_execute)  

    def _execute(self, _):
        self.update_inputs_from_ui()
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

    def _execute_preview(self, _):
        self.update_inputs_from_ui()
        base_feature = self.component.features.baseFeatures.add()
        self.execute(base_feature)

    def _edit_execute(self, _):
        self.update_inputs_from_ui()
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

    def _activate_edit(self, args: adsk.core.EventArgs):
        command = adsk.core.CommandEventArgs.cast(args).command

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

    def _compute(self, args: adsk.core.EventArgs):
        feature = adsk.fusion.CustomFeatureEventArgs.cast(args).customFeature
        if not self.inputs:
            self.inputs = self.create_inputs()
        self.update_inputs_from_feature(feature)
        self.compute(feature)

    def update_inputs_from_ui(self):
        for input in self.inputs.values + self.inputs.selections:
            input.update_value_from_input()

    def update_inputs_from_feature(self, feature: adsk.fusion.CustomFeature):
        for sel in self.inputs.selections:
            sel.value = sel.get_from_dependencies(feature)
        for val in self.inputs.values:
            val.update_value_from_params(feature.parameters)

    def _pre_select(self, args: adsk.core.EventArgs):
        event_args = adsk.core.SelectionEventArgs.cast(args)
        if self._initial_selection:
            event_args.isSelectable = True
        else:
            event_args.isSelectable = self.pre_select(event_args.selection.entity)

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



def show_message(message, error = False):
    ui = adsk.core.Application.get().userInterface
    text_palette: adsk.core.TextCommandPalette = ui.palettes.itemById('TextCommands')
    text_palette.writeText(message)
    if error:
        ui.messageBox(message)