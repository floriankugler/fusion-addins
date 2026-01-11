import adsk.core, adsk.fusion
import contextlib
from typing import cast
from abc import ABC, abstractmethod
import Inputs, Combine, Errors
import utils
from utils.fusion import new_event_handler


class CustomComputeFeature(ABC):
    plugin_id = "<<plugin id>>"
    plugin_name = '<<plugin name>>>'
    plugin_desc = '<<plugin description>>'
    plugin_tooltip = '<<plugin tooltip>>'

    app: adsk.core.Application
    ui: adsk.core.UserInterface
    custom_feature_def: adsk.fusion.CustomFeatureDefinition
    edited_custom_feature: adsk.fusion.CustomFeature  | None
    restore_timeline_object: adsk.fusion.TimelineObject
    inputs: Inputs.Inputs | None
    _error_field: adsk.core.TextBoxCommandInput | None
    _compute_disabled: bool

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
            self.inputs = None
            self._compute_disabled = False

            # Create the command definition for the creation command.
            create_cmd_def = self.ui.commandDefinitions.addButtonDefinition(self.create_command_id, c.plugin_name, c.plugin_tooltip, resource_dir)        

            # Add the create button in the Modify panel of the SOLID tab.
            solidWS = self.ui.workspaces.itemById('FusionSolidEnvironment')
            panel = solidWS.toolbarPanels.itemById('SolidModifyPanel')
            separator_id = 'SeparatorBeforeCustomAddins'
            for idx in range(panel.controls.count):
                ctrl = panel.controls.item(idx)
                if ctrl.id == separator_id:
                    panel.controls.addCommand(create_cmd_def, separator_id, True)        
                    break
                if ctrl.id == 'FusionMoveCommand':
                    panel.controls.addCommand(create_cmd_def, 'FusionMoveCommand', True)        
                    panel.controls.addSeparator(separator_id, 'FusionMoveCommand', True)
                    break

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
            self.custom_feature_def = adsk.fusion.CustomFeatureDefinition.create(c.plugin_id, c.plugin_name, resource_dir)
            self.custom_feature_def.editCommandId = self.edit_command_id

            # Connect to the compute event for the custom feature.
            compute_custom_feature = new_event_handler(self._compute, adsk.fusion.CustomFeatureEventHandler)
            self.custom_feature_def.customFeatureCompute.add(compute_custom_feature)
            self._handlers.append(compute_custom_feature)

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

            cmd_def = self.ui.commandDefinitions.itemById(self.edit_command_id)
            if cmd_def:
                cmd_def.deleteMe()
        except:
            utils.fusion.handleException

    def _create_ui(self, args: adsk.core.EventArgs) -> None:
        command = adsk.core.CommandCreatedEventArgs.cast(args).command

        self.edited_custom_feature = cast(adsk.fusion.CustomFeature, self.ui.activeSelections.item(0).entity) if self.ui.activeSelections.count > 0 else None
        if self.edited_custom_feature and self.edited_custom_feature.nativeObject:
            self.edited_custom_feature = self.edited_custom_feature.nativeObject
        editing = self.edited_custom_feature != None
        params = self.edited_custom_feature.parameters if self.edited_custom_feature else None

        self.inputs = self.create_inputs()
        for input in self.inputs.inputs:
            input.create_input(command.commandInputs, params)
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

        with self.compute_disabled():
            feat_input = self.component.features.customFeatures.createInput(self.custom_feature_def)
            for sel in self.inputs.inputs:
                sel.create_in_feature_input(feat_input)

            feature = self.component.features.customFeatures.add(feat_input)

            for sel in self.inputs.inputs:
                sel.create_named_values(feature)

            features_inside_component: list[adsk.fusion.Feature] = []
            features_outside_component: list[adsk.fusion.Feature] = []
            dependencies: list[adsk.fusion.BRepBody] = []
            try:
                combines = self.execute()
                features_inside_component, features_outside_component, dependencies = Combine.create_features_from_combines(self.component, combines, feature, False)
            except Errors.InvalidInputError as e:
                args.executeFailed = True
                args.executeFailedMessage = e.message
            except:
                args.executeFailed = True
                args.executeFailedMessage = "An error occurred during execution."
            finally:
                feature.timelineObject.rollTo(True)
                for dep in dependencies:
                    feature.dependencies.add(dep.revisionId, dep)
                if features_inside_component:
                    feature.setStartAndEndFeatures(features_inside_component[0], features_inside_component[-1])
                if features_outside_component:
                    features_outside_component[-1].timelineObject.rollTo(False)
                else:
                    feature.timelineObject.rollTo(False)

                self.inputs = None

    def _execute_preview(self, args: adsk.core.CommandEventArgs):
        if self._compute_disabled:
            return
        self.update_inputs_from_ui()
        with self.compute_disabled():
            try:
                combines = self.execute()
                Combine.create_features_from_combines(self.component, combines, None, False)
            except Errors.InvalidInputError as e:
                self.showError(e.message)
                args.isValidResult = False
            except Exception as e:
                self.showError(f"An error occurred: {e}")
                args.isValidResult = False
            else:
                self.showError(None)

    def _edit_execute(self, args: adsk.core.CommandEventArgs):
        assert(self.inputs is not None)
        assert(self.edited_custom_feature is not None)
        self.update_inputs_from_ui()
        features_inside_component: list[adsk.fusion.Feature] = []
        features_outside_component: list[adsk.fusion.Feature] = []

        with self.compute_disabled():
            self.edited_custom_feature.timelineObject.rollTo(True)
            self.edited_custom_feature.dependencies.deleteAll()
            for inp in self.inputs.inputs:
                inp.update_in_feature(self.edited_custom_feature)

            try:
                combines = self.execute()
            except Errors.InvalidInputError as e:
                args.executeFailed = True
                args.executeFailedMessage = e.message
            except:
                args.executeFailed = True
                args.executeFailedMessage = "An error occurred during execution."
            else:
                self.edited_custom_feature.timelineObject.rollTo(True)
                features_inside_component, features_outside_component, dependencies = Combine.create_features_from_combines(self.edited_custom_feature.parentComponent, combines, self.edited_custom_feature, False)

                self.edited_custom_feature.timelineObject.rollTo(True)
                for dep in dependencies:
                    self.edited_custom_feature.dependencies.add(dep.revisionId, dep)
                if features_inside_component:
                    self.edited_custom_feature.setStartAndEndFeatures(features_inside_component[0], features_inside_component[-1])
            finally:
                restore_entity = None
                try:
                    restore_entity = self.restore_timeline_object.entity
                except:
                    pass                
                if restore_entity:
                    if restore_entity in [self.edited_custom_feature, *features_outside_component]:
                        features_outside_component[-1].timelineObject.rollTo(False)    
                    else:
                        self.restore_timeline_object.rollTo(False)
                else:
                    if features_outside_component:
                        features_outside_component[-1].timelineObject.rollTo(False)
                    else:
                        self.edited_custom_feature.timelineObject.rollTo(False)

                self.edited_custom_feature = None
                self.inputs = None

    def _activate_edit(self, args: adsk.core.EventArgs):
        assert(self.edited_custom_feature is not None)
        assert(self.inputs is not None)
        command = adsk.core.CommandEventArgs.cast(args).command
        design: adsk.fusion.Design = cast(adsk.fusion.Design, self.app.activeProduct)
        self.restore_timeline_object = design.timeline.item(design.timeline.markerPosition - 1)
        self.edited_custom_feature.timelineObject.rollTo(rollBefore = True)

        command.beginStep()

        with self.compute_disabled():
            for sel in self.inputs.inputs:
                sel.update_from_feature(self.edited_custom_feature)

        # Manually trigger the preview since we've avoided the preview being called while updating the inputs above
        command.doExecutePreview()

    def _compute(self, args: adsk.fusion.CustomFeatureEventArgs):
        if self._compute_disabled:
            return
        try:
            feature: adsk.fusion.CustomFeature = args.customFeature
            self.inputs = self.create_inputs()
            self.update_inputs_from_feature(feature)
            combines = self.execute()
            Combine.create_features_from_combines(self.component, combines, feature, True)
        except Errors.CustomComputeError as e:
            e.update_status(args.computeStatus)
        except Exception as e:
            args.computeStatus.statusMessages.addError(str(e))
        finally:
            self.inputs = None
    
    def _pre_select(self, args: adsk.core.EventArgs):
        event_args = adsk.core.SelectionEventArgs.cast(args)
        event_args.isSelectable = self.pre_select(event_args.activeInput, event_args.selection.entity)

    def update_inputs_from_ui(self):
        assert(self.inputs is not None)
        for input in self.inputs.inputs:
            input.update_from_input()

    def update_inputs_from_feature(self, feature: adsk.fusion.CustomFeature):
        assert(self.inputs is not None)
        for sel in self.inputs.inputs:
            sel.update_from_feature(feature)

    @contextlib.contextmanager
    def compute_disabled(self):
        disabled = self._compute_disabled
        self._compute_disabled = True
        yield
        self._compute_disabled = disabled

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
    def execute(self) -> list[Combine.Combine]:
        pass

    def pre_select(self, input, selection) -> bool:
        return True
    
    def input_changed(self, input):
        pass

