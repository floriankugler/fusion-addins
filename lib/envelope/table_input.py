"""The rectangles table command input shared by envelope and multi-arrange."""

import adsk.core, adsk.fusion
from dataclasses import dataclass

from .. import inputs
from . import builder


@dataclass
class TableRow:
    width: adsk.core.ValueCommandInput
    height: adsk.core.ValueCommandInput
    count: adsk.core.IntegerSpinnerCommandInput


class RectangleTableInput(inputs.Input):
    """A table of rectangle sizes with add / delete row buttons.

    A table has no counterpart in custom feature parameters, so it only works
    for the one-shot command style the envelope-based add-ins use.
    """

    value: list[builder.RectangleSpec]
    input: adsk.core.TableCommandInput

    def __init__(self, id: str, name: str, tool_tip: str, units: str, update_visibility=lambda: True,
                 initial_rows: list[tuple[str, str, int]] | None = None):
        super().__init__(id, name, tool_tip, update_visibility)
        self.units = units
        self.value = []
        self._rows: list[TableRow] = []
        # Rows to prefill the table with: (width expr, height expr, count).
        self.initial_rows = initial_rows
        # Row inputs need ids that are unique for the lifetime of the dialog,
        # so the counter keeps rising instead of tracking the row index.
        self._next_row_key = 0
        self._add_button: adsk.core.BoolValueCommandInput | None = None
        self._delete_button: adsk.core.BoolValueCommandInput | None = None

    def create_input(self, command_inputs: adsk.core.CommandInputs, params: adsk.fusion.CustomFeatureParameters | None):
        if params is not None:
            raise RuntimeError("The rectangles table cannot be restored from a custom feature.")

        table = command_inputs.addTableCommandInput(self.id, self.name, 3, '2:2:1')
        table.minimumVisibleRows = 2
        table.maximumVisibleRows = 10
        table.hasGrid = False
        table.tablePresentationStyle = adsk.core.TablePresentationStyles.itemBorderTablePresentationStyle  # type: ignore
        self.input = table

        self._add_header_row()
        if self.initial_rows:
            for width_expression, height_expression, count in self.initial_rows:
                self._append_row(width_expression, height_expression, count)
        else:
            self._append_row(builder.DEFAULT_WIDTH_EXPRESSION, builder.DEFAULT_HEIGHT_EXPRESSION, 1)

        children = table.commandInputs
        self._add_button = children.addBoolValueInput(f'{self.id}_add', 'Add', False, '', False)
        self._add_button.tooltip = 'Add another rectangle size'
        self._delete_button = children.addBoolValueInput(f'{self.id}_delete', 'Delete', False, '', False)
        self._delete_button.tooltip = 'Delete the selected rectangle size'
        table.addToolbarCommandInput(self._add_button)
        table.addToolbarCommandInput(self._delete_button)

    def handle_input_changed(self, changed_input: adsk.core.CommandInput) -> bool:
        """Returns True when the change was a table button that was handled."""
        if not changed_input or self.input is None:
            return False

        if self._add_button and changed_input.id == self._add_button.id:
            self._add_button.value = False
            last = self._rows[-1] if self._rows else None
            self._append_row(
                self._expression_of(last.width, builder.DEFAULT_WIDTH_EXPRESSION) if last else builder.DEFAULT_WIDTH_EXPRESSION,
                self._expression_of(last.height, builder.DEFAULT_HEIGHT_EXPRESSION) if last else builder.DEFAULT_HEIGHT_EXPRESSION,
                int(last.count.value) if last else 1,
            )
            return True

        if self._delete_button and changed_input.id == self._delete_button.id:
            self._delete_button.value = False
            self._delete_selected_row()
            return True

        return False

    def set_rows(self, rows: list[tuple[str, str, int]]):
        """Replaces the table contents (used when prefilling from a stored
        arrangement recipe)."""
        while self._rows:
            self.input.deleteRow(len(self._rows))
            self._rows.pop()
        for width_expression, height_expression, count in rows:
            self._append_row(width_expression, height_expression, count)
        self.update_from_input()

    def update_from_input(self):
        specs: list[builder.RectangleSpec] = []
        for row in self._rows:
            specs.append(builder.RectangleSpec(
                width=row.width.value,
                width_expression=self._expression_of(row.width, builder.DEFAULT_WIDTH_EXPRESSION),
                height=row.height.value,
                height_expression=self._expression_of(row.height, builder.DEFAULT_HEIGHT_EXPRESSION),
                count=int(row.count.value),
            ))
        self.value = specs

    def create_in_feature_input(self, feature_input: adsk.fusion.CustomFeatureInput):
        raise RuntimeError("The rectangles table cannot be stored in a custom feature.")

    def update_in_feature(self, feature: adsk.fusion.CustomFeature):
        raise RuntimeError("The rectangles table cannot be stored in a custom feature.")

    def update_from_feature(self, feature: adsk.fusion.CustomFeature):
        raise RuntimeError("The rectangles table cannot be restored from a custom feature.")

    def _add_header_row(self):
        children = self.input.commandInputs
        for column, title in enumerate(('Width', 'Height', 'Count')):
            header = children.addStringValueInput(f'{self.id}_header_{column}', '', title)
            header.isReadOnly = True
            self.input.addCommandInput(header, 0, column, 0, 0)

    def _append_row(self, width_expression: str, height_expression: str, count: int):
        key = self._next_row_key
        self._next_row_key += 1
        children = self.input.commandInputs

        width = children.addValueInput(
            f'{self.id}_width_{key}',
            'Width',
            self.units,
            adsk.core.ValueInput.createByString(width_expression),
        )
        height = children.addValueInput(
            f'{self.id}_height_{key}',
            'Height',
            self.units,
            adsk.core.ValueInput.createByString(height_expression),
        )
        height.minimumValue = builder.MINIMUM_HEIGHT
        height.isMinimumInclusive = False
        count_input = children.addIntegerSpinnerCommandInput(
            f'{self.id}_count_{key}',
            'Count',
            1,
            1000,
            1,
            max(1, count),
        )

        row_index = self.input.rowCount
        self.input.addCommandInput(width, row_index, 0, 0, 0)
        self.input.addCommandInput(height, row_index, 1, 0, 0)
        self.input.addCommandInput(count_input, row_index, 2, 0, 0)
        self._rows.append(TableRow(width, height, count_input))

    def _delete_selected_row(self):
        # The table always keeps one row so the command can never end up with
        # nothing to build.
        if len(self._rows) <= 1:
            return

        # Row 0 holds the header, so the row records are offset by one.
        selected = self.input.selectedRow
        row_index = selected if selected >= 1 else self.input.rowCount - 1
        record_index = row_index - 1
        if not 0 <= record_index < len(self._rows):
            return

        self.input.deleteRow(row_index)
        del self._rows[record_index]
        self.input.selectedRow = -1

    def _expression_of(self, value_input: adsk.core.ValueCommandInput, fallback: str) -> str:
        try:
            expression = value_input.expression
        except Exception:
            expression = None
        return expression if expression else fallback
