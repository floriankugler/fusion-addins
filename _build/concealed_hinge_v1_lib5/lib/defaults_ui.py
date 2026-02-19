import adsk.core, adsk.fusion
from dataclasses import dataclass
from typing import Any
from . import defaults_store
from . import inputs as inp


@dataclass
class DefaultRow:
    source_input: inp.Input
    enabled_input: adsk.core.BoolValueCommandInput
    current_value_input: adsk.core.StringValueCommandInput
    new_value_input: adsk.core.StringValueCommandInput


@dataclass
class DefaultsUIControls:
    rows: list[DefaultRow]
    new_value_cache: dict[str, str]
    check_all_button: adsk.core.BoolValueCommandInput | None
    uncheck_all_button: adsk.core.BoolValueCommandInput | None
    use_current_button: adsk.core.BoolValueCommandInput | None
    save_button: adsk.core.BoolValueCommandInput | None
    error_field: adsk.core.TextBoxCommandInput | None


class DefaultValueAdapter:
    def __init__(self, app: adsk.core.Application):
        self.app = app

    def apply_default(self, source: inp.Input, value: Any):
        expr = self._extract_expr(value)
        if expr is not None:
            self._apply_expression_default(source, expr)
            return
        self._apply_literal_default(source, value)

    def display_default(self, source: inp.Input, value: Any) -> str:
        if value is None:
            return ''
        expr = self._extract_expr(value)
        if expr is not None:
            return f"expr: {expr}"
        if isinstance(source, inp.DropDownInput) and isinstance(value, int) and not isinstance(value, bool):
            option = next((item for item in source.options if item.value == value), None)
            if option:
                return f"{value} ({option.name})"
        if isinstance(value, bool):
            return 'true' if value else 'false'
        return str(value)

    def current_value_text(self, source: inp.Input) -> str:
        if isinstance(source, inp.FloatInput):
            expression = getattr(source, 'expression', None)
            if isinstance(expression, str) and expression:
                return expression
            value = getattr(source, 'value', None)
            return '' if value is None else str(value)
        if isinstance(source, inp.IntegerInput):
            return str(source.value)
        if isinstance(source, inp.CheckboxInput):
            return 'true' if source.value else 'false'
        if isinstance(source, inp.DropDownInput):
            return str(source.value)
        return ''

    def parse_new_default(self, source: inp.Input, text: str) -> tuple[Any | None, str | None]:
        if isinstance(source, inp.FloatInput):
            numeric = self._parse_number(text)
            if numeric is not None:
                return numeric, None
            evaluated = self._evaluate_expression(text, source.units)
            if evaluated is None:
                return None, "Invalid expression."
            return {"expr": text}, None

        if isinstance(source, inp.IntegerInput):
            literal = self._parse_int(text)
            if literal is not None:
                if source.minimum_value <= literal <= source.maximum_value:
                    return literal, None
                return None, f"Value out of range [{source.minimum_value}, {source.maximum_value}]."
            evaluated = self._evaluate_expression(text, '')
            if evaluated is None:
                return None, "Invalid expression."
            val = int(round(evaluated))
            if source.minimum_value <= val <= source.maximum_value:
                return {"expr": text}, None
            return None, f"Expression out of range [{source.minimum_value}, {source.maximum_value}]."

        if isinstance(source, inp.CheckboxInput):
            parsed_bool = self._parse_bool(text)
            if parsed_bool is not None:
                return parsed_bool, None
            evaluated = self._evaluate_expression(text, '')
            if evaluated is None:
                return None, "Invalid expression."
            return {"expr": text}, None

        if isinstance(source, inp.DropDownInput):
            literal = self._parse_int(text)
            allowed = {item.value for item in source.options}
            if literal is not None:
                if literal in allowed:
                    return literal, None
                return None, "Value does not match a dropdown option."
            evaluated = self._evaluate_expression(text, '')
            if evaluated is None:
                return None, "Invalid expression."
            val = int(round(evaluated))
            if val in allowed:
                return {"expr": text}, None
            return None, "Expression does not evaluate to a dropdown option."

        return None, "Unsupported input type."

    def _extract_expr(self, value: Any) -> str | None:
        if isinstance(value, dict):
            expr = value.get("expr")
            if isinstance(expr, str):
                return expr
        return None

    def _apply_literal_default(self, source: inp.Input, value: Any):
        if isinstance(source, inp.FloatInput):
            if isinstance(value, (int, float)):
                source.default_value = float(value)
            elif isinstance(value, str):
                source.default_expression = value
            return
        if isinstance(source, inp.IntegerInput):
            if isinstance(value, int) and not isinstance(value, bool):
                if source.minimum_value <= value <= source.maximum_value:
                    source.default_value = value
            return
        if isinstance(source, inp.CheckboxInput):
            if isinstance(value, bool):
                source.default_value = value
            return
        if isinstance(source, inp.DropDownInput):
            if isinstance(value, int) and not isinstance(value, bool):
                allowed = {item.value for item in source.options}
                if value in allowed:
                    source.default_value = value

    def _apply_expression_default(self, source: inp.Input, expression: str):
        if isinstance(source, inp.FloatInput):
            source.default_expression = expression
            return
        if isinstance(source, inp.IntegerInput):
            value = self._evaluate_expression(expression, '')
            if value is None:
                return
            parsed = int(round(value))
            if source.minimum_value <= parsed <= source.maximum_value:
                source.default_value = parsed
            return
        if isinstance(source, inp.CheckboxInput):
            parsed = self._parse_bool(expression)
            if parsed is not None:
                source.default_value = parsed
                return
            value = self._evaluate_expression(expression, '')
            if value is None:
                return
            source.default_value = abs(value) > 1e-9
            return
        if isinstance(source, inp.DropDownInput):
            value = self._evaluate_expression(expression, '')
            if value is None:
                return
            parsed = int(round(value))
            allowed = {item.value for item in source.options}
            if parsed in allowed:
                source.default_value = parsed

    def _parse_number(self, value: str) -> float | None:
        try:
            return float(value)
        except Exception:
            return None

    def _parse_int(self, value: str) -> int | None:
        try:
            return int(value)
        except Exception:
            return None

    def _parse_bool(self, value: str) -> bool | None:
        text = value.strip().lower()
        if text in ['true', 'yes', '1']:
            return True
        if text in ['false', 'no', '0']:
            return False
        return None

    def _evaluate_expression(self, expression: str, units: str) -> float | None:
        design = adsk.fusion.Design.cast(self.app.activeProduct)
        if not design:
            return None
        units_manager = design.unitsManager
        try:
            return units_manager.evaluateExpression(expression, units)
        except Exception:
            return None


class DefaultsUIManager:
    def __init__(self, app: adsk.core.Application, defaults_file: str):
        self.app = app
        self.defaults_file = defaults_file
        self._values: dict[str, Any] = {}
        self._adapter = DefaultValueAdapter(app)
        self._controls = DefaultsUIControls([], {}, None, None, None, None, None)

    def apply_defaults(self, inputs: inp.Inputs):
        self._values = defaults_store.load(self.defaults_file)
        for source in inputs.inputs:
            if source.id not in self._values:
                continue
            value = self._values.get(source.id)
            try:
                self._adapter.apply_default(source, value)
            except Exception:
                continue

    def create_ui(self, command_inputs: adsk.core.CommandInputs, inputs: inp.Inputs):
        self._controls = DefaultsUIControls([], {}, None, None, None, None, None)
        self._render_defaults_table(command_inputs, inputs)
        self._render_actions_row(command_inputs)
        self._render_error_label(command_inputs)
        self._render_footer(command_inputs)

    def handle_input_changed(self, changed_input: adsk.core.CommandInput) -> bool:
        if not changed_input:
            return False

        controls = self._controls
        if controls.check_all_button and changed_input.id == controls.check_all_button.id:
            for row in controls.rows:
                row.enabled_input.value = True
            controls.check_all_button.value = False
            return True

        if controls.uncheck_all_button and changed_input.id == controls.uncheck_all_button.id:
            for row in controls.rows:
                row.enabled_input.value = False
            controls.uncheck_all_button.value = False
            return True

        if controls.use_current_button and changed_input.id == controls.use_current_button.id:
            self._fill_new_defaults_from_current_values()
            controls.use_current_button.value = False
            return True

        if controls.save_button and changed_input.id == controls.save_button.id:
            self._save_selected_defaults()
            controls.save_button.value = False
            return True

        row = next((r for r in controls.rows if r.new_value_input.id == changed_input.id), None)
        if row is not None:
            new_text = row.new_value_input.value
            old_text = controls.new_value_cache.get(row.new_value_input.id, '')
            if new_text != old_text:
                controls.new_value_cache[row.new_value_input.id] = new_text
                row.enabled_input.value = new_text.strip() != ''
            return False

        return False

    def _render_defaults_table(self, children: adsk.core.CommandInputs, inputs: inp.Inputs):
        table = children.addTableCommandInput('defaults_table', '', 4, '1:2:2:3')
        table.minimumVisibleRows = 3
        table.maximumVisibleRows = 12

        header_use = children.addStringValueInput('defaults_header_use', '', 'Use')
        header_use.isReadOnly = True
        header_name = children.addStringValueInput('defaults_header_input', '', 'Input')
        header_name.isReadOnly = True
        header_current = children.addStringValueInput('defaults_header_current', '', 'Current default')
        header_current.isReadOnly = True
        header_new = children.addStringValueInput('defaults_header_new', '', 'New default')
        header_new.isReadOnly = True
        table.addCommandInput(header_use, 0, 0, 0, 0)
        table.addCommandInput(header_name, 0, 1, 0, 0)
        table.addCommandInput(header_current, 0, 2, 0, 0)
        table.addCommandInput(header_new, 0, 3, 0, 0)

        row_idx = 1
        for source in inputs.inputs:
            if not self._is_savable_input(source):
                continue

            enabled = children.addBoolValueInput(f'defaults_enabled__{source.id}', '', True, '', False)
            enabled.value = False
            name = children.addStringValueInput(f'defaults_name__{source.id}', '', source.name)
            name.isReadOnly = True
            current_value = children.addStringValueInput(
                f'defaults_current__{source.id}',
                '',
                self._adapter.display_default(source, self._values.get(source.id)),
            )
            current_value.isReadOnly = True
            new_value = children.addStringValueInput(f'defaults_new__{source.id}', '', '')
            self._set_new_default_tooltip(source, new_value)

            table.addCommandInput(enabled, row_idx, 0, 0, 0)
            table.addCommandInput(name, row_idx, 1, 0, 0)
            table.addCommandInput(current_value, row_idx, 2, 0, 0)
            table.addCommandInput(new_value, row_idx, 3, 0, 0)

            row = DefaultRow(source, enabled, current_value, new_value)
            self._controls.rows.append(row)
            self._controls.new_value_cache[new_value.id] = new_value.value
            row_idx += 1

    def _render_actions_row(self, children: adsk.core.CommandInputs):
        actions_table = children.addTableCommandInput('defaults_actions', '', 3, '1:1:1')
        actions_table.minimumVisibleRows = 1
        actions_table.maximumVisibleRows = 1

        self._controls.check_all_button = children.addBoolValueInput('defaults_check_all', 'Check all', False, '', False)
        self._controls.uncheck_all_button = children.addBoolValueInput('defaults_uncheck_all', 'Uncheck all', False, '', False)
        self._controls.use_current_button = children.addBoolValueInput('defaults_use_current', 'Use current values', False, '', False)
        actions_table.addCommandInput(self._controls.check_all_button, 0, 0, 0, 0)
        actions_table.addCommandInput(self._controls.uncheck_all_button, 0, 1, 0, 0)
        actions_table.addCommandInput(self._controls.use_current_button, 0, 2, 0, 0)

    def _render_error_label(self, children: adsk.core.CommandInputs):
        self._controls.error_field = children.addTextBoxCommandInput('defaults_errorLabel', 'Errors', '', 3, True)
        self._controls.error_field.isFullWidth = True
        self._controls.error_field.isVisible = False

    def _render_footer(self, children: adsk.core.CommandInputs):
        path_input = children.addStringValueInput('defaults_path', 'Path of defaults file', self.defaults_file)
        path_input.isReadOnly = True
        path_input.tooltip = self.defaults_file
        path_input.tooltipDescription = self.defaults_file

        self._controls.save_button = children.addBoolValueInput('defaults_save', 'Save selected defaults', False, '', False)
        self._controls.save_button.isFullWidth = True

    def _set_new_default_tooltip(self, source: inp.Input, input: adsk.core.StringValueCommandInput):
        input.tooltip = 'Enter a literal value or an expression.'
        if isinstance(source, inp.DropDownInput):
            options = [f"{item.value} = {item.name}" for item in source.options]
            input.tooltipDescription = f"Dropdown ids: {', '.join(options)}"

    def _fill_new_defaults_from_current_values(self):
        for row in self._controls.rows:
            row.new_value_input.value = self._adapter.current_value_text(row.source_input)
            self._controls.new_value_cache[row.new_value_input.id] = row.new_value_input.value
            row.new_value_input.isValueError = False

    def _save_selected_defaults(self):
        values = defaults_store.load(self.defaults_file)
        errors: list[str] = []
        for row in self._controls.rows:
            row.new_value_input.isValueError = False
            if not row.enabled_input.value:
                continue

            raw_text = row.new_value_input.value.strip()
            if raw_text == '':
                values.pop(row.source_input.id, None)
                continue

            parsed, error = self._adapter.parse_new_default(row.source_input, raw_text)
            if error:
                row.new_value_input.isValueError = True
                errors.append(f"{row.source_input.name}: {error}")
                continue
            values[row.source_input.id] = parsed

        if errors:
            self._show_error('<br>'.join(errors))
            return

        comment: dict[str, Any] = {}
        for source in (row.source_input for row in self._controls.rows):
            if isinstance(source, inp.DropDownInput):
                comment[source.id] = {
                    "type": "dropdown",
                    "options": [{"name": option.name, "value": option.value} for option in source.options],
                }

        defaults_store.save(self.defaults_file, values, comment)
        self._values = values
        for row in self._controls.rows:
            row.current_value_input.value = self._adapter.display_default(row.source_input, values.get(row.source_input.id))
            row.enabled_input.value = False
        self._show_error(None)

    def _is_savable_input(self, source: inp.Input) -> bool:
        return (
            isinstance(source, inp.FloatInput)
            or isinstance(source, inp.IntegerInput)
            or isinstance(source, inp.CheckboxInput)
            or isinstance(source, inp.DropDownInput)
        )

    def _show_error(self, message: str | None):
        error_field = self._controls.error_field
        if not error_field:
            return
        if message:
            error_field.isVisible = True
            error_field.formattedText = f"<font color=\"red\">{message}</font><br>"
        else:
            error_field.isVisible = False
            error_field.formattedText = ''
