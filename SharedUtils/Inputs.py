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
        self.input = None

    @abstractmethod
    def create_input(self, inputs: adsk.core.CommandInput, params: adsk.fusion.CustomFeatureParameters, editing: bool):
        pass

    @abstractmethod
    def create_in_feature_input(self, feature_input: adsk.fusion.CustomFeatureInput):
        pass

    @abstractmethod
    def update_in_feature(self, feature: adsk.fusion.CustomFeature):
        pass

    @abstractmethod
    def update_from_feature(self, feature: adsk.fusion.CustomFeature):
        pass

    @abstractmethod
    def update_from_input(self):
        pass

    def create_named_values(self, feature: adsk.fusion.CustomFeature):
        pass


class CheckboxInput(Input):
    default_value: bool
    value: bool
    input: adsk.core.BoolValueCommandInput

    def __init__(self, id, name, default_value, tool_tip):
        super().__init__(id, name, tool_tip)
        self.default_value = default_value

    def create_input(self, inputs: adsk.core.CommandInput, params: adsk.fusion.CustomFeatureParameters, editing: bool):
        val = params.itemById(self.id).value if params else self.default_value
        self.input = inputs.addBoolValueInput(self.id, self.name, True, '', bool(val))

    def create_in_feature_input(self, feature_input: adsk.fusion.CustomFeatureInput):
        value_input = adsk.core.ValueInput.createByReal(self.value)
        feature_input.addCustomParameter(self.id, self.name, value_input, '', True)

    def update_in_feature(self, feature: adsk.fusion.CustomFeature):
        feature.parameters.itemById(self.id).value = self.value

    def update_from_feature(self, feature: adsk.fusion.CustomFeature):
        val = feature.parameters.itemById(self.id).value
        if val is not None:
            self.value = bool(val)
            if self.input: self.input.value = self.value

    def update_from_input(self):
        val = self.input.value
        if val is not None:
            self.value = val


class FloatInput(Input):
    default_value: float
    value: float
    expression: str
    input: adsk.core.ValueCommandInput
    units: str
    minimum_value: float = None

    def __init__(self, id, name, default_value, tool_tip, units):
        super().__init__(id, name, tool_tip)
        self.default_value = default_value
        self.units = units

    def create_input(self, inputs: adsk.core.CommandInput, params: adsk.fusion.CustomFeatureParameters, editing: bool):
        param_expr = params.itemById(self.id).expression if params else None 
        value_input = None
        if param_expr is None:
            value_input = adsk.core.ValueInput.createByReal(self.default_value)
        else:
            value_input = adsk.core.ValueInput.createByString(param_expr)
        self.input = inputs.addValueInput(self.id, self.name, self.units, value_input)
        if self.minimum_value is not None:
            self.input.minimumValue = self.minimum_value
            self.input.isMinimumInclusive = True

    def create_in_feature_input(self, feature_input: adsk.fusion.CustomFeatureInput):
        value_input = adsk.core.ValueInput.createByString(self.expression)
        feature_input.addCustomParameter(self.id, self.name, value_input, self.units, True)

    def update_in_feature(self, feature: adsk.fusion.CustomFeature):
        feature.parameters.itemById(self.id).expression = self.expression

    def update_from_feature(self, feature: adsk.fusion.CustomFeature):
        param = feature.parameters.itemById(self.id)
        if param is not None:
            self.value = param.value
            self.expression = param.expression
            if self.input: self.input.expression = param.expression

    def update_from_input(self):
        val = self.input.value
        if val is not None:
            self.value = val
            self.expression = self.input.expression

class DropDownInput(Input):
    default_value: str
    value: int
    options: list[tuple[str, int]]
    input: adsk.core.ButtonRowCommandInput

    def __init__(self, id, name, options, default_value, tool_tip):
        super().__init__(id, name, tool_tip)
        self.options = options
        self.default_value = default_value

    def create_input(self, inputs: adsk.core.CommandInput, params: adsk.fusion.CustomFeatureParameters, editing: bool):
        self.input = inputs.addDropDownCommandInput(self.id, self.name, adsk.core.DropDownStyles.TextListDropDownStyle)
        items = self.input.listItems
        val = params.itemById(self.id).value if params else self.default_value
        for option in self.options:
            selected = val == option[1]
            items.add(option[0], selected)

    def create_in_feature_input(self, feature_input: adsk.fusion.CustomFeatureInput):
        value_input = adsk.core.ValueInput.createByReal(self.value)
        feature_input.addCustomParameter(self.id, self.name, value_input, '', True)

    def update_in_feature(self, feature: adsk.fusion.CustomFeature):
        feature.parameters.itemById(self.id).value = self.value

    def update_from_feature(self, feature: adsk.fusion.CustomFeature):
        param = feature.parameters.itemById(self.id)
        if param is None: 
            return
        self.value = param.value
        name = next(key for key, value in self.options if value == self.value)
        if self.input:
            for item in self.input.listItems:
                item.isSelected = item.name == name

    def update_from_input(self):
        name = self.input.selectedItem.name
        val = next(value for key, value in self.options if key == name)
        self.value = val


class SelectionByEntityTokenInput(Input):
    input: adsk.core.SelectionCommandInput
    value: list[adsk.core.Base]

    def __init__(self, id, name, filter, lower_bound, upper_bound, tool_tip):
        super().__init__(id, name, tool_tip)
        self.filter = filter
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.tokens = []
        self.value = []

    def create_input(self, inputs: adsk.core.CommandInput, params: adsk.fusion.CustomFeatureParameters, editing: bool):
        self.input = inputs.addSelectionInput(self.id, self.name, self.tool_tip)
        self.input.addSelectionFilter(self.filter)
        self.input.setSelectionLimits(self.lower_bound, self.upper_bound)

    def create_in_feature_input(self, feature_input: adsk.fusion.CustomFeatureInput):
        self.tokens = []
        for idx in range(len(self.value)):
            entity = self.value[idx]
            feature_input.addDependency(self.dependency_id(idx), entity)
            self.tokens.append(entity.entityToken)

    def create_named_values(self, feature: adsk.fusion.CustomFeature):
        for idx in range(len(self.value)):
            feature.customNamedValues.addOrSetValue(self.dependency_id(idx), self.value[idx].entityToken)

    def update_in_feature(self, feature: adsk.fusion.CustomFeature):
        for idx in range(len(self.value)):
            id = self.dependency_id(idx)
            feature.dependencies.add(id, self.value[idx])
            feature.customNamedValues.addOrSetValue(id, self.value[idx].entityToken)

    def update_from_feature(self, feature: adsk.fusion.CustomFeature):
        result = []
        if self.input: self.input.clearSelection()
        deps = [d for d in feature.dependencies if d.id.startswith(self.dependency_id_prefix)]
        for idx in range(len(deps)):
            dep = deps[idx]
            token = feature.customNamedValues.value(dep.id) or self.tokens[idx]
            entity = feature.parentComponent.parentDesign.findEntityByToken(token)[0]
            result.append(entity)
            if self.input: self.input.addSelection(entity)
        self.value = result
        
    def update_from_input(self):
        result = []
        for idx in range(self.input.selectionCount):
            result.append(self.input.selection(idx).entity)
        self.value = result

    @property
    def dependency_id_prefix(self):
        return f"{self.id}__"

    def dependency_id(self, idx):
        return f"{self.dependency_id_prefix}{idx}"




class Inputs(ABC):
    inputs: list[Input]

    def __init__(self):
        self.inputs = []
        for _, value in vars(self).items():
            if isinstance(value, Input):
                self.inputs.append(value)
