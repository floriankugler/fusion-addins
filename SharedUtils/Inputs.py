import adsk.core, adsk.fusion
from typing import Any
from abc import ABC, abstractmethod
import utils


class Input(ABC):
    id: str
    name: str
    tool_tip: str
    value: Any
    input: adsk.core.CommandInput

    def __init__(self, id, name, tool_tip):
        self.id = id
        self.name = name
        self.tool_tip = tool_tip

    @abstractmethod
    def get_value_from_input(self):
        pass

    @abstractmethod
    def create_input(self, inputs: adsk.core.CommandInput, params: adsk.fusion.CustomFeatureParameters, editing: bool):
        pass

    def update_value_from_input(self):
        val = self.get_value_from_input()
        if val is not None:
            self.value = val

class ValueInput(Input):
    default_value: Any
    units: str

    def __init__(self, id, name, default_value, tool_tip, units = ''):
        super().__init__(id, name, tool_tip)
        self.default_value = default_value
        self.units = units

    @abstractmethod
    def create_value_input(self, value) -> adsk.core.ValueInput:
        pass

    def get_value_from_params(self, params: adsk.fusion.CustomFeatureParameters):
        if not params:
            return self.default_value
        return params.itemById(self.id).value

    def update_param_from_input(self, params: adsk.fusion.CustomFeatureParameters):
        params.itemById(self.id).value = self.get_value_from_input()

    def create_value_input_from_params(self, params: adsk.fusion.CustomFeatureParameters) -> adsk.core.ValueInput:
        return adsk.core.ValueInput.createByReal(self.get_value_from_params(params))

    def create_value_input_from_inputs(self) -> adsk.core.ValueInput:
        return adsk.core.ValueInput.createByReal(self.value)

class CheckboxInput(ValueInput):
    input: adsk.core.BoolValueCommandInput

    def __init__(self, id, name, default_value, tool_tip):
        super().__init__(id, name, default_value, tool_tip, '')

    def get_value_from_params(self, params: adsk.fusion.CustomFeatureParameters):
        val = super().get_value_from_params(params)
        return bool(val)

    def create_input(self, inputs: adsk.core.CommandInput, params: adsk.fusion.CustomFeatureParameters, editing: bool):
        self.input = inputs.addBoolValueInput(self.id, self.name, True, '', self.get_value_from_params(params))

    def get_value_from_input(self):
        return self.input.value

    def create_value_input(self, value) -> adsk.core.ValueInput:
        return adsk.core.ValueInput.createByBoolean(value)

class FloatInput(ValueInput):
    input: adsk.core.ValueCommandInput

    def __init__(self, id, name, default_value, tool_tip, units):
        super().__init__(id, name, default_value, tool_tip, units)

    def create_input(self, inputs: adsk.core.CommandInput, params: adsk.fusion.CustomFeatureParameters, editing: bool):
        value_input = self.create_value_input_from_params(params)
        self.input = inputs.addValueInput(self.id, self.name, self.units, value_input)

    def get_value_from_input(self):
        return self.input.value

    def create_value_input(self, value) -> adsk.core.ValueInput:
        return adsk.core.ValueInput.createByReal(value)

class DropDownInput(ValueInput):
    input: adsk.core.ButtonRowCommandInput

    def __init__(self, id, name, options, default_value, tool_tip):
        super().__init__(id, name, default_value, tool_tip, '')
        self.options = options

    def create_input(self, inputs: adsk.core.CommandInput, params: adsk.fusion.CustomFeatureParameters, editing: bool):
        self.input = inputs.addDropDownCommandInput(self.id, self.name, adsk.core.
        DropDownStyles.TextListDropDownStyle)
        items = self.input.listItems
        for option in self.options:
            selected = self.get_value_from_params(params) == option[1]
            items.add(option[0], selected)

    def get_value_from_input(self):
        name = self.input.selectedItem.name
        for option in self.options:
            if option[0] == name:
                return option[1]

    def create_value_input(self, value) -> adsk.core.ValueInput:
        return adsk.core.ValueInput.createByReal(value)

class SelectionInput(Input):
    input: adsk.core.SelectionCommandInput
    value: list[adsk.core.Base]
    is_editable: bool

    def __init__(self, id, name, filter, lower_bound, upper_bound, is_editable, tool_tip):
        super().__init__(id, name, tool_tip)
        self.filter = filter
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.is_editable = is_editable

    def create_input(self, inputs: adsk.core.CommandInput, params: adsk.fusion.CustomFeatureParameters, editing: bool):
        self.input = inputs.addSelectionInput(self.id, self.name, self.tool_tip)
        self.input.addSelectionFilter(self.filter)
        self.input.setSelectionLimits(self.lower_bound, self.upper_bound)
        # self.input.isVisible = self.is_editable or not editing

    def get_value_from_input(self) -> list[adsk.core.Base]:
        result = []
        for idx in range(0, self.input.selectionCount):
            result.append(self.input.selection(idx).entity)
        return result

    def dependency_id(self, idx):
        return f"{self.id}__{idx}"

    def create_dependencies(self, feature_input: adsk.fusion.CustomFeatureInput):
        for idx in range(0, len(self.value)):
            feature_input.addDependency(self.dependency_id(idx), self.value[idx])

    def create_named_values(self, feature: adsk.fusion.CustomFeature):
        pass

    def get_from_dependencies(self, feature: adsk.fusion.CustomFeature) -> list[adsk.core.Base]:
        result = []
        idx = 0
        while dep := feature.dependencies.itemById(self.dependency_id(idx)):
            result.append(dep.entity)
            idx += 1
        return result

    def update_dependencies(self, feature: adsk.fusion.CustomFeature):
        for idx in range(0, len(self.value)):
            id = self.dependency_id(idx)
            dep = feature.dependencies.itemById(id)
            if dep:
                dep.entity = self.value[idx]
            else:
                feature.dependencies.add(id, self.value[idx])
        idx = len(self.value)
        while dep := feature.dependencies.itemById(self.dependency_id(idx)):
            dep.deleteMe()
            idx += 1

class SelectionByEntityTokenInput(Input):
    input: adsk.core.SelectionCommandInput
    value: list[adsk.core.Base]
    is_editable: bool

    def __init__(self, id, name, filter, lower_bound, upper_bound, is_editable, tool_tip):
        super().__init__(id, name, tool_tip)
        self.filter = filter
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.is_editable = is_editable

    def create_input(self, inputs: adsk.core.CommandInput, params: adsk.fusion.CustomFeatureParameters, editing: bool):
        self.input = inputs.addSelectionInput(self.id, self.name, self.tool_tip)
        self.input.addSelectionFilter(self.filter)
        self.input.setSelectionLimits(self.lower_bound, self.upper_bound)
        # self.input.isVisible = self.is_editable or not editing

    def get_value_from_input(self) -> list[adsk.core.Base]:
        result = []
        for idx in range(0, self.input.selectionCount):
            result.append(self.input.selection(idx).entity)
        return result

    def dependency_id(self, idx):
        return f"{self.id}__{idx}"

    def create_dependencies(self, feature_input: adsk.fusion.CustomFeatureInput):
        self.tokens = []
        for idx in range(0, len(self.value)):
            entity = self.value[idx]
            feature_input.addDependency(self.dependency_id(idx), entity)
            self.tokens.append(entity.entityToken)

    def create_named_values(self, feature: adsk.fusion.CustomFeature):
        for idx in range(0, len(self.value)):
            feature.customNamedValues.addOrSetValue(self.dependency_id(idx), self.value[idx].entityToken)

    def get_from_dependencies(self, feature: adsk.fusion.CustomFeature) -> list[adsk.core.Base]:
        result = []
        idx = 0
        while feature.dependencies.itemById(self.dependency_id(idx)):
            token = feature.customNamedValues.value(self.dependency_id(idx)) or self.tokens[idx]
            entity = feature.parentComponent.parentDesign.findEntityByToken(token)[0]
            result.append(entity)
            idx += 1
        return result

    def update_dependencies(self, feature: adsk.fusion.CustomFeature):
        for idx in range(0, len(self.value)):
            id = self.dependency_id(idx)
            dep = feature.dependencies.itemById(id)
            if dep:
                dep.entity = self.value[idx]
            else:
                feature.dependencies.add(id, self.value[idx])
            feature.customNamedValues.addOrSetValue(id, self.value[idx].entityToken)
        idx = len(self.value)
        while dep := feature.dependencies.itemById(self.dependency_id(idx)):
            dep.deleteMe()
            feature.customNamedValues.remove(self.dependency_id(idx))
            idx += 1

class FaceSelectionByEdgesInput(SelectionInput):
    def __init__(self, id, name, lower_bound, upper_bound, is_editable, tool_tip):
        super().__init__(id, name, 'PlanarFaces', lower_bound, upper_bound, is_editable, tool_tip)

    def dependency_id(self, idx, suffix = ''):
        if not suffix:
            return f"{self.id}__{idx}"    
        else:
            return f"{self.id}__{idx}__{suffix}"

    def create_dependencies(self, feature_input: adsk.fusion.CustomFeatureInput):
        for idx in range(0, len(self.value)):
            face: adsk.fusion.BRepFace = self.value[idx]
            edges = utils.brep.outer_edges_of_face(face)
            for idx2 in range(len(edges)):
                feature_input.addDependency(self.dependency_id(idx, idx2), edges[idx2])

    def get_from_dependencies(self, feature: adsk.fusion.CustomFeature) -> list[adsk.core.Base]:
        result = []
        idx = 0
        while dep := feature.dependencies.itemById(self.dependency_id(idx, 0)):
            edges = [dep.entity]
            idx2 = 1
            while dep := feature.dependencies.itemById(self.dependency_id(idx, idx2)):
                edges.append(dep.entity)
                idx2 += 1
            face = utils.brep.common_face_of_edges(edges)
            result.append(face)
            idx += 1
        return result

    def update_dependencies(self, feature: adsk.fusion.CustomFeature):
        for idx in range(0, len(self.value)):
            face: adsk.fusion.BRepFace = self.value[idx]
            edges = utils.brep.outer_edges_of_face(face)
            for idx2 in range(len(edges)):
                dep = feature.dependencies.itemById(self.dependency_id(idx, idx2))
                if dep:
                    dep.entity = edges[idx2]
                else:
                    feature.dependencies.add(self.dependency_id(idx, idx2), edges[idx2])
            idx2 = len(edges)
            while dep := feature.dependencies.itemById(self.dependency_id(idx, idx2)):
                dep.deleteMe()
                idx2 += 1
        
        idx = len(self.value)
        while dep := feature.dependencies.itemById(self.dependency_id(idx, 0)):
            dep.deleteMe()
            while dep := feature.dependencies.itemById(self.dependency_id(idx, idx2)):
                dep.deleteMe()
                idx2 += 1
            idx += 1


class Inputs(ABC):
    selections: list[SelectionInput]
    values: list[ValueInput]

