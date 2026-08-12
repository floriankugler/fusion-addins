import adsk.core, adsk.fusion
from typing import Any, Callable
from abc import ABC, abstractmethod
from dataclasses import dataclass
from . import errors
from .utils import misc


class Input(ABC):
    id: str
    name: str
    tool_tip: str
    value: Any
    input: adsk.core.CommandInput | None
    update_visibility: Callable[[], bool]

    def __init__(self, id, name, tool_tip, update_visibility: Callable[[], bool]):
        self.id = id
        self.name = name
        self.tool_tip = tool_tip
        self.input = None
        self.update_visibility = update_visibility

    @abstractmethod
    def create_input(self, inputs: adsk.core.CommandInputs, params: adsk.fusion.CustomFeatureParameters | None):
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

    def _update_visibility(self):
        if self.input:
            self.input.isVisible = self.update_visibility()

    def _required_param(self, params: adsk.fusion.CustomFeatureParameters) -> adsk.fusion.CustomFeatureParameter:
        param = params.itemById(self.id)
        if param is None:
            raise errors.InvalidInputError(
                f"Missing custom feature parameter '{self.id}' for input '{self.name}'."
            )
        return param

    def _required_feature_param(self, feature: adsk.fusion.CustomFeature) -> adsk.fusion.CustomFeatureParameter:
        param = feature.parameters.itemById(self.id)
        if param is None:
            raise errors.InvalidInputError(
                f"Missing custom feature parameter '{self.id}' for input '{self.name}'."
            )
        return param


class CheckboxInput(Input):
    default_value: bool
    value: bool
    input: adsk.core.BoolValueCommandInput

    def __init__(self, id, name, default_value, tool_tip, update_visibility: Callable[[], bool] = lambda: True):
        super().__init__(id, name, tool_tip, update_visibility)
        self.default_value = default_value
        
    def create_input(self, inputs: adsk.core.CommandInputs, params: adsk.fusion.CustomFeatureParameters | None):
        val = self._required_param(params).value if params else self.default_value
        self.input = inputs.addBoolValueInput(self.id, self.name, True, '', bool(val))

    def create_in_feature_input(self, feature_input: adsk.fusion.CustomFeatureInput):
        value_input = adsk.core.ValueInput.createByReal(self.value)
        feature_input.addCustomParameter(self.id, self.name, value_input, '', True)

    def update_in_feature(self, feature: adsk.fusion.CustomFeature):
        self._required_feature_param(feature).value = self.value

    def update_from_feature(self, feature: adsk.fusion.CustomFeature):
        val = self._required_feature_param(feature).value
        if val is not None:
            self.value = bool(val)
            if self.input: self.input.value = self.value

    def update_from_input(self):
        val = self.input.value
        if val is not None:
            self.value = val


class StringInput(Input):
    default_value: str
    value: str
    input: adsk.core.StringValueCommandInput

    def __init__(self, id, name, default_value: str, tool_tip, update_visibility: Callable[[], bool] = lambda: True):
        super().__init__(id, name, tool_tip, update_visibility)
        self.default_value = default_value
        self.value = default_value

    def create_input(self, inputs: adsk.core.CommandInputs, params: adsk.fusion.CustomFeatureParameters | None):
        if params is not None:
            raise errors.InvalidInputError(
                f"String input '{self.name}' cannot be restored from a custom feature."
            )
        self.input = inputs.addStringValueInput(self.id, self.name, self.default_value)
        self.input.tooltip = self.tool_tip

    def create_in_feature_input(self, feature_input: adsk.fusion.CustomFeatureInput):
        raise errors.InvalidInputError(
            f"String input '{self.name}' cannot be stored in a custom feature."
        )

    def update_in_feature(self, feature: adsk.fusion.CustomFeature):
        raise errors.InvalidInputError(
            f"String input '{self.name}' cannot be stored in a custom feature."
        )

    def update_from_feature(self, feature: adsk.fusion.CustomFeature):
        raise errors.InvalidInputError(
            f"String input '{self.name}' cannot be restored from a custom feature."
        )

    def update_from_input(self):
        val = self.input.value
        if val is not None:
            self.value = val


class FloatInput(Input):
    default_value: float
    default_expression: str | None
    value: float
    expression: str
    input: adsk.core.ValueCommandInput
    units: str
    minimum_value: float | None = None
    minimum_inclusive: bool = True

    def __init__(self, id: str, name: str, default_value: float, tool_tip: str, units: str, update_visibility: Callable[[], bool] = lambda: True):
        super().__init__(id, name, tool_tip, update_visibility)
        self.default_value = default_value
        self.default_expression = None
        self.value = default_value
        # Reading the expression from the UI input can fail (e.g. before the
        # dialog is fully built), in which case update_from_input keeps the
        # previous value — so there must always be one.
        self.expression = ''
        self.units = units

    def create_input(self, inputs: adsk.core.CommandInputs, params: adsk.fusion.CustomFeatureParameters | None):
        param_expr = self._required_param(params).expression if params else None
        value_input = None
        if param_expr is None:
            if self.default_expression is not None:
                value_input = adsk.core.ValueInput.createByString(self.default_expression)
            else:
                value_input = adsk.core.ValueInput.createByReal(self.default_value)
        else:
            value_input = adsk.core.ValueInput.createByString(param_expr)
        self.input = inputs.addValueInput(self.id, self.name, self.units, value_input)
        if self.minimum_value is not None:
            self.input.minimumValue = self.minimum_value
            self.input.isMinimumInclusive = self.minimum_inclusive

    def create_in_feature_input(self, feature_input: adsk.fusion.CustomFeatureInput):
        value_input = adsk.core.ValueInput.createByString(self.expression)
        feature_input.addCustomParameter(self.id, self.name, value_input, self.units, True)

    def update_in_feature(self, feature: adsk.fusion.CustomFeature):
        self._required_feature_param(feature).expression = self.expression

    def update_from_feature(self, feature: adsk.fusion.CustomFeature):
        param = self._required_feature_param(feature)
        self.value = param.value
        self.expression = param.expression
        if self.input: self.input.expression = param.expression

    def update_from_input(self):
        val = self.input.value
        if val is not None:
            self.value = val
            try:
                self.expression = self.input.expression
            except:
                pass

class IntegerInput(Input):
    default_value: int
    value: int
    input: adsk.core.IntegerSpinnerCommandInput
    minimum_value: int
    maximum_value: int

    def __init__(self, id, name, default_value: int, minimum: int, maximum: int, tool_tip, update_visibility: Callable[[], bool] = lambda: True):
        super().__init__(id, name, tool_tip, update_visibility)
        self.default_value = default_value
        self.minimum_value = minimum
        self.maximum_value = maximum

    def create_input(self, inputs: adsk.core.CommandInputs, params: adsk.fusion.CustomFeatureParameters | None):
        val = int(self._required_param(params).value if params else self.default_value)
        self.input = inputs.addIntegerSpinnerCommandInput(self.id, self.name, self.minimum_value, self.maximum_value, 1, val)

    def create_in_feature_input(self, feature_input: adsk.fusion.CustomFeatureInput):
        value_input = adsk.core.ValueInput.createByReal(self.value)
        feature_input.addCustomParameter(self.id, self.name, value_input, '', True)

    def update_in_feature(self, feature: adsk.fusion.CustomFeature):
        self._required_feature_param(feature).value = self.value

    def update_from_feature(self, feature: adsk.fusion.CustomFeature):
        param = self._required_feature_param(feature)
        self.value = int(param.value)
        if self.input: self.input.value = self.value

    def update_from_input(self):
        val = self.input.value
        if val is not None:
            self.value = val

class DropDownInput(Input):
    @dataclass
    class Item:
        name: str
        value: int

    default_value: int
    value: int
    options: list[Item]
    input: adsk.core.DropDownCommandInput

    def __init__(self, id, name, options: list[Item], default_value: int, tool_tip, update_visibility: Callable[[], bool] = lambda: True):
        super().__init__(id, name, tool_tip, update_visibility)
        self.options = options
        self.default_value = default_value

    def create_input(self, inputs: adsk.core.CommandInputs, params: adsk.fusion.CustomFeatureParameters | None):
        self.input = inputs.addDropDownCommandInput(self.id, self.name, adsk.core.DropDownStyles.TextListDropDownStyle) # type: ignore
        items = self.input.listItems
        val = self._required_param(params).value if params else self.default_value
        for option in self.options:
            selected = val == option.value
            items.add(option.name, selected)

    def create_in_feature_input(self, feature_input: adsk.fusion.CustomFeatureInput):
        value_input = adsk.core.ValueInput.createByReal(self.value)
        feature_input.addCustomParameter(self.id, self.name, value_input, '', True)

    def update_in_feature(self, feature: adsk.fusion.CustomFeature):
        self._required_feature_param(feature).value = self.value

    def update_from_feature(self, feature: adsk.fusion.CustomFeature):
        param = self._required_feature_param(feature)
        self.value = int(param.value)
        name = self._option_name_for_value(self.value)
        if self.input:
            for item in self.input.listItems:
                item.isSelected = item.name == name

    def update_from_input(self):
        selected = self.input.selectedItem
        if not selected:
            raise errors.InvalidInputError(f"Dropdown '{self.name}' has no selected item.")
        val = self._option_value_for_name(selected.name)
        self.value = val

    def _option_name_for_value(self, value: int) -> str:
        for item in self.options:
            if item.value == value:
                return item.name
        raise errors.InvalidInputError(
            f"Dropdown '{self.name}' has no option for value '{value}'."
        )

    def _option_value_for_name(self, name: str) -> int:
        for item in self.options:
            if item.name == name:
                return item.value
        raise errors.InvalidInputError(
            f"Dropdown '{self.name}' has no option named '{name}'."
        )


def _entity_is_valid(entity) -> bool:
    try:
        return bool(entity.isValid)
    except Exception:
        return False


def _entity_token(entity) -> str | None:
    try:
        return entity.entityToken
    except Exception:
        return None


class SelectionByEntityTokenInput(Input):
    input: adsk.core.SelectionCommandInput
    value: list[
        adsk.fusion.BRepEdge
        | adsk.fusion.BRepFace
        | adsk.fusion.BRepVertex
        | adsk.fusion.ConstructionAxis
        | adsk.fusion.ConstructionPoint
        | adsk.fusion.SketchLine
        | adsk.fusion.SketchPoint
    ]
    #: Entity tokens parallel to `value`, captured while the entities were
    #: valid, so stale references can be re-resolved after a preview rollback.
    tokens: list[str | None]

    def __init__(self, id, name, filter: list[str], lower_bound: int, upper_bound: int, tool_tip: str, update_visibility: Callable[[], bool] = lambda: True):
        super().__init__(id, name, tool_tip, update_visibility)
        self.filter = filter
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.tokens = []
        self.value = []

    def create_input(self, inputs: adsk.core.CommandInputs, params: adsk.fusion.CustomFeatureParameters | None):
        self.input = inputs.addSelectionInput(self.id, self.name, self.tool_tip)
        for filter in self.filter:
            self.input.addSelectionFilter(filter)
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
        result_tokens = []
        if self.input: self.input.clearSelection()
        deps = [d for d in feature.dependencies if d.id.startswith(self.dependency_id_prefix)]
        for idx in range(len(deps)):
            dep = deps[idx]
            token = feature.customNamedValues.value(dep.id) or self.tokens[idx]
            entities = feature.parentComponent.parentDesign.findEntityByToken(token)
            if not entities:
                raise errors.ReferenceLostError()
            entity = entities[0]
            result.append(entity)
            result_tokens.append(token)
            if self.input: self.input.addSelection(entity)
        self.value = result
        self.tokens = result_tokens
        
    def update_from_input(self):
        ui_entities = []
        read_failed = False
        for idx in range(self.input.selectionCount):
            try:
                ui_entities.append(self.input.selection(idx).entity)
            except RuntimeError:
                # A selection that references a consumed entity can throw on
                # access; treat it like model churn below.
                read_failed = True

        if not self.has_stale_value() and not read_failed:
            # Clean model: the selection input is authoritative.
            self.value = ui_entities
            self.tokens = [_entity_token(entity) for entity in ui_entities]
            return

        # Some cached entities are currently invalid: the model is in a
        # previewed state whose changes consumed the selected entities (e.g.
        # a cut that splits the selected edge), and Fusion silently dropped
        # them from the selection input. Keep the cached selections — they
        # resolve again once the preview is rolled back — and merge in
        # anything newly selected on top of the preview.
        known = set(token for token in self.tokens if token)
        for entity in ui_entities:
            token = _entity_token(entity)
            if token in known:
                continue
            self.value.append(entity)
            self.tokens.append(token)

    def has_stale_value(self) -> bool:
        """True while a cached selection references an invalid entity —
        i.e. an applied preview has modified the selected bodies."""
        return any(not _entity_is_valid(entity) for entity in self.value)

    def refresh_stale_value(self, design: adsk.fusion.Design):
        """Re-resolves stale cached selections via their entity tokens.

        Meant for the moment right after a preview rollback: the original
        entities exist again, but references cached before the preview can
        stay invalid. Entities whose token no longer resolves are dropped.
        """
        if not self.has_stale_value():
            return
        fresh = []
        fresh_tokens = []
        for entity, token in zip(self.value, self.tokens):
            if _entity_is_valid(entity):
                fresh.append(entity)
                fresh_tokens.append(token)
                continue
            if not token:
                continue
            try:
                entities = design.findEntityByToken(token)
            except RuntimeError:
                continue
            if entities:
                fresh.append(entities[0])
                fresh_tokens.append(token)
        self.value = fresh
        self.tokens = fresh_tokens

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
            # misc.is_instance, not isinstance: after a dev-mode module reload
            # an Input subclass can still inherit from the pre-reload Input
            # class, which fails a plain isinstance even though the object is
            # perfectly usable. Dropping it here would silently remove the
            # input from the dialog.
            if misc.is_instance(value, Input) or (
                hasattr(value, 'create_input')
                and hasattr(value, 'update_from_input')
                and hasattr(value, 'id')
            ):
                self.inputs.append(value)

    def update_visibilities(self):
        for input in self.inputs:
            input._update_visibility()
