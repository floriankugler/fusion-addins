import adsk.core, adsk.fusion
import contextlib
from typing import cast
from abc import abstractmethod
from . import combine, errors, utils
from .addin import Addin
from .utils.fusion import new_event_handler
from .fusionbootstrap.runtime import RuntimeInfo


class CustomComputeFeature(Addin):
    _custom_feature_def: adsk.fusion.CustomFeatureDefinition
    _edited_custom_feature: adsk.fusion.CustomFeature  | None
    _restore_timeline_object: adsk.fusion.TimelineObject
    _compute_disabled: bool

    @property
    def edit_command_id(self) -> str:
        return self.runtime_info.id + '_edit'

    def __init__(self, runtime_info: RuntimeInfo):
        try:
            super().__init__(runtime_info)
            self._compute_disabled = False

            # Create the command definition for the edit command.
            edit_cmd_def = self.ui.commandDefinitions.addButtonDefinition(
                self.edit_command_id,
                'Edit ' + self.plugin_name,
                'Edit ' + self.plugin_name,
                self.resource_dir,
            )

            # Connect to the command created event for the edit command.
            edit_command_created = new_event_handler(self._create_ui, adsk.core.CommandCreatedEventHandler)
            edit_cmd_def.commandCreated.add(edit_command_created)
            self._handlers.append(edit_command_created)

            # Create the custom feature definition.
            self._custom_feature_def = adsk.fusion.CustomFeatureDefinition.create(
                self.runtime_info.id,
                self.plugin_name,
                self.resource_dir,
            )
            self._custom_feature_def.editCommandId = self.edit_command_id

            # Connect to the compute event for the custom feature.
            compute_custom_feature = new_event_handler(self._compute, adsk.fusion.CustomFeatureEventHandler)
            self._custom_feature_def.customFeatureCompute.add(compute_custom_feature)
            self._handlers.append(compute_custom_feature)

        except:
            utils.fusion.handleException()

    def __del__(self):
        try:
            super().__del__()
                
            cmd_def = self.ui.commandDefinitions.itemById(self.edit_command_id)
            if cmd_def:
                cmd_def.deleteMe()
        except:
            utils.fusion.handleException

    def _create_ui(self, args: adsk.core.EventArgs) -> None:
        command = adsk.core.CommandCreatedEventArgs.cast(args).command

        self._edited_custom_feature = cast(adsk.fusion.CustomFeature, self.ui.activeSelections.item(0).entity) if self.ui.activeSelections.count > 0 else None
        if self._edited_custom_feature and self._edited_custom_feature.nativeObject:
            self._edited_custom_feature = self._edited_custom_feature.nativeObject
        editing = self._edited_custom_feature != None
        params = self._edited_custom_feature.parameters if self._edited_custom_feature else None

        self._initialize_inputs(command, params)
        self._attach_common_handlers(command)

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

    def _execute(self, args: adsk.core.CommandEventArgs):
        assert(self.inputs is not None)
        self.update_inputs_from_ui()

        with self.compute_disabled():
            feat_input = self.component.features.customFeatures.createInput(self._custom_feature_def)
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
                features_inside_component, features_outside_component, dependencies = combine.create_features_from_combines(self.component, combines, feature, False)
            except errors.InvalidInputError as e:
                args.executeFailed = True
                args.executeFailedMessage = e.message
            except Exception as e:
                args.executeFailed = True
                args.executeFailedMessage = "An error occurred during execution."
                if self.runtime_info.dev_mode: raise e
            else:
                self._save_defaults_if_requested()
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
                combine.create_features_from_combines(self.component, combines, None, False)
            except errors.InvalidInputError as e:
                self.showError(e.message)
                args.isValidResult = False
            except Exception as e:
                self.showError(f"An error occurred: {e}")
                args.isValidResult = False
                if self.runtime_info.dev_mode: raise e
            else:
                self.showError(None)

    def _edit_execute(self, args: adsk.core.CommandEventArgs):
        assert(self.inputs is not None)
        assert(self._edited_custom_feature is not None)
        self.update_inputs_from_ui()
        features_inside_component: list[adsk.fusion.Feature] = []
        features_outside_component: list[adsk.fusion.Feature] = []

        with self.compute_disabled():
            self._edited_custom_feature.timelineObject.rollTo(True)
            self._edited_custom_feature.dependencies.deleteAll()
            for inp in self.inputs.inputs:
                inp.update_in_feature(self._edited_custom_feature)

            try:
                combines = self.execute()
            except errors.InvalidInputError as e:
                args.executeFailed = True
                args.executeFailedMessage = e.message
            except Exception as e:
                args.executeFailed = True
                args.executeFailedMessage = "An error occurred during execution."
                if self.runtime_info.dev_mode: raise e
            else:
                self._save_defaults_if_requested()
                self._edited_custom_feature.timelineObject.rollTo(True)
                features_inside_component, features_outside_component, dependencies = combine.create_features_from_combines(self._edited_custom_feature.parentComponent, combines, self._edited_custom_feature, False)

                self._edited_custom_feature.timelineObject.rollTo(True)
                for dep in dependencies:
                    self._edited_custom_feature.dependencies.add(dep.revisionId, dep)
                if features_inside_component:
                    self._edited_custom_feature.setStartAndEndFeatures(features_inside_component[0], features_inside_component[-1])
            finally:
                restore_entity = None
                try:
                    restore_entity = self._restore_timeline_object.entity
                except:
                    pass                
                if restore_entity:
                    if restore_entity in features_outside_component:
                        features_outside_component[-1].timelineObject.rollTo(False)    
                    elif restore_entity == self._edited_custom_feature:
                        self._edited_custom_feature.timelineObject.rollTo(False)    
                    else:
                        self._restore_timeline_object.rollTo(False)
                else:
                    if features_outside_component:
                        features_outside_component[-1].timelineObject.rollTo(False)
                    else:
                        self._edited_custom_feature.timelineObject.rollTo(False)

                self._edited_custom_feature = None
                self.inputs = None

    def _activate_edit(self, args: adsk.core.EventArgs):
        assert(self._edited_custom_feature is not None)
        assert(self.inputs is not None)
        command = adsk.core.CommandEventArgs.cast(args).command
        design: adsk.fusion.Design = cast(adsk.fusion.Design, self.app.activeProduct)
        self._restore_timeline_object = design.timeline.item(design.timeline.markerPosition - 1)
        self._edited_custom_feature.timelineObject.rollTo(rollBefore = True)

        command.beginStep()

        with self.compute_disabled():
            for sel in self.inputs.inputs:
                sel.update_from_feature(self._edited_custom_feature)

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
            combine.create_features_from_combines(self.component, combines, feature, True)
        except errors.CustomComputeError as e:
            e.update_status(args.computeStatus)
        except Exception as e:
            args.computeStatus.statusMessages.addError(str(e))
            if self.runtime_info.dev_mode: raise e
        finally:
            self.inputs = None
    
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

    @abstractmethod
    def execute(self) -> list[combine.Combine]:
        pass
