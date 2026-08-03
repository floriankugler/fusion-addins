"""The per-part settings table of the Multi-Arrange dialog.

One row per selected part with rotation, group, and grain-direction controls,
like the component table in Fusion's own Arrange dialog. Selection inputs
cannot live inside table cells, so the grain direction is assigned through a
single global selection input that applies to the highlighted row (see
main.py); the table shows the assignment state per row.

Rows are prefilled from the settings stored on each body (document
attributes), and the values entered here are written back to those attributes
on execute — so the table doubles as the editor for the persisted settings.
"""

import adsk.core, adsk.fusion
from dataclasses import dataclass

from .. import inputs
from . import model


ROTATION_NAMES = {
    model.ROTATION_FREE: 'Free',
    model.ROTATION_GRAIN: 'Grain',
    model.ROTATION_GRAIN_ONE_WAY: 'Grain one-way',
}

GRAIN_AUTO = 'auto'
GRAIN_SET = 'edge'


@dataclass
class PartRecord:
    token: str
    body: adsk.fusion.BRepBody
    face: adsk.fusion.BRepFace
    direction_token: str | None
    name_cell: adsk.core.StringValueCommandInput
    rotation_cell: adsk.core.DropDownCommandInput
    group_cell: adsk.core.StringValueCommandInput
    grain_cell: adsk.core.StringValueCommandInput


class PartTableInput(inputs.Input):
    """Table of the selected parts and their nesting settings."""

    value: dict[str, model.PartSettings]  # keyed by body entity token
    input: adsk.core.TableCommandInput

    def __init__(self, id: str, name: str, tool_tip: str, update_visibility=lambda: True):
        super().__init__(id, name, tool_tip, update_visibility)
        self.value = {}
        self._records: list[PartRecord] = []
        # Cell inputs need ids that are unique for the lifetime of the dialog.
        self._next_row_key = 0
        self._clear_grain_button: adsk.core.BoolValueCommandInput | None = None
        self._remove_button: adsk.core.BoolValueCommandInput | None = None

    @property
    def records(self) -> list[PartRecord]:
        return list(self._records)

    def create_input(self, command_inputs: adsk.core.CommandInputs, params: adsk.fusion.CustomFeatureParameters | None):
        if params is not None:
            raise RuntimeError('The parts table cannot be restored from a custom feature.')
        table = command_inputs.addTableCommandInput(self.id, self.name, 4, '3:3:2:1')
        table.minimumVisibleRows = 3
        table.maximumVisibleRows = 12
        table.hasGrid = False
        table.tablePresentationStyle = adsk.core.TablePresentationStyles.itemBorderTablePresentationStyle  # type: ignore
        self.input = table
        self._add_header_row()

        children = table.commandInputs
        self._remove_button = children.addBoolValueInput(
            f'{self.id}_remove', 'Remove', False, '', False)
        self._remove_button.tooltip = 'Removes the selected part from the arrangement.'
        table.addToolbarCommandInput(self._remove_button)
        self._clear_grain_button = children.addBoolValueInput(
            f'{self.id}_clear_grain', 'Clear grain direction', False, '', False)
        self._clear_grain_button.tooltip = (
            'Removes the grain direction reference of the selected row, falling '
            'back to the longest edge of its top face.'
        )
        table.addToolbarCommandInput(self._clear_grain_button)

    # ------------------------------------------------------------------- sync

    def sync(self, faces: list[adsk.fusion.BRepFace]):
        """Aligns the table rows with the current faces selection.

        Existing rows keep their edited values; new parts are prefilled from
        the settings stored on the body.
        """
        wanted: dict[str, adsk.fusion.BRepFace] = {}
        for face in faces:
            token = face.body.entityToken
            if token not in wanted:
                wanted[token] = face

        for index in reversed(range(len(self._records))):
            if self._records[index].token not in wanted:
                self.input.deleteRow(index + 1)
                del self._records[index]

        present = {record.token for record in self._records}
        for token, face in wanted.items():
            if token not in present:
                self._append_row(face)

    def handle_input_changed(self, changed_input: adsk.core.CommandInput) -> bool:
        if not changed_input or self.input is None:
            return False
        if self._clear_grain_button and changed_input.id == self._clear_grain_button.id:
            self._clear_grain_button.value = False
            record = self._selected_record()
            if record:
                record.direction_token = None
                record.grain_cell.value = GRAIN_AUTO
            return True
        if self._remove_button and changed_input.id == self._remove_button.id:
            self._remove_button.value = False
            self.remove_selected()
            return True
        return False

    def remove_selected(self) -> bool:
        """Removes the highlighted row (or the only row). The caller must
        rebuild the faces selection input from `records` afterwards, otherwise
        the next selection sync re-adds the part."""
        record = self._selected_record()
        if record is None:
            return False
        index = self._records.index(record)
        self.input.deleteRow(index + 1)
        del self._records[index]
        self.update_from_input()
        return True

    def assign_direction(self, direction_token: str) -> str | None:
        """Assigns a picked direction reference to the highlighted row.

        Returns an error message when no row can be determined.
        """
        record = self._selected_record()
        if record is None:
            return 'Select the part row the grain direction belongs to, then pick the direction.'
        record.direction_token = direction_token
        record.grain_cell.value = GRAIN_SET
        return None

    def _selected_record(self) -> PartRecord | None:
        if len(self._records) == 1:
            return self._records[0]
        row = self.input.selectedRow
        index = row - 1  # row 0 is the header
        if 0 <= index < len(self._records):
            return self._records[index]
        return None

    def face_settings(self) -> list[tuple[adsk.fusion.BRepFace, model.PartSettings]]:
        """(face, settings) pairs straight from the row records, in row order.

        The canonical source for what to arrange: positional pairing avoids
        entity-token joins entirely (token strings only match when derived
        from the same proxy object)."""
        self.update_from_input()
        return [(record.face, self.value[record.token]) for record in self._records]

    def body_settings(self) -> list[tuple[adsk.fusion.BRepBody, model.PartSettings]]:
        """The per-body settings straight from the row records.

        Used for saving: entity tokens are not comparable as strings, so a
        token-keyed dict cannot be safely re-joined against freshly computed
        tokens — the body references kept in the records avoid that entirely.
        """
        self.update_from_input()
        result = []
        for record in self._records:
            result.append((record.body, self.value[record.token]))
        return result

    # ------------------------------------------------------------- framework

    def update_from_input(self):
        result: dict[str, model.PartSettings] = {}
        for record in self._records:
            selected = record.rotation_cell.selectedItem
            rotation = model.ROTATION_FREE
            if selected:
                for value, name in ROTATION_NAMES.items():
                    if name == selected.name:
                        rotation = value
            result[record.token] = model.PartSettings(
                rotation=rotation,
                direction_token=record.direction_token,
                group=record.group_cell.value.strip() or None,
            )
        self.value = result

    def create_in_feature_input(self, feature_input: adsk.fusion.CustomFeatureInput):
        raise RuntimeError('The parts table cannot be stored in a custom feature.')

    def update_in_feature(self, feature: adsk.fusion.CustomFeature):
        raise RuntimeError('The parts table cannot be stored in a custom feature.')

    def update_from_feature(self, feature: adsk.fusion.CustomFeature):
        raise RuntimeError('The parts table cannot be restored from a custom feature.')

    # ----------------------------------------------------------------- rows

    def _add_header_row(self):
        children = self.input.commandInputs
        for column, title in enumerate(('Part', 'Rotation', 'Group', 'Grain')):
            header = children.addStringValueInput(f'{self.id}_header_{column}', '', title)
            header.isReadOnly = True
            self.input.addCommandInput(header, 0, column, 0, 0)

    def _append_row(self, face: adsk.fusion.BRepFace):
        body = face.body
        stored = model.load_settings(body)
        key = self._next_row_key
        self._next_row_key += 1
        children = self.input.commandInputs

        name_cell = children.addStringValueInput(f'{self.id}_name_{key}', '', body.name)
        name_cell.isReadOnly = True

        rotation_cell = children.addDropDownCommandInput(
            f'{self.id}_rotation_{key}', '', adsk.core.DropDownStyles.TextListDropDownStyle)  # type: ignore
        for value, name in ROTATION_NAMES.items():
            rotation_cell.listItems.add(name, value == stored.rotation)

        group_cell = children.addStringValueInput(f'{self.id}_group_{key}', '', stored.group or '')

        grain_cell = children.addStringValueInput(
            f'{self.id}_grain_{key}', '', GRAIN_SET if stored.direction_token else GRAIN_AUTO)
        grain_cell.isReadOnly = True

        row_index = self.input.rowCount
        self.input.addCommandInput(name_cell, row_index, 0, 0, 0)
        self.input.addCommandInput(rotation_cell, row_index, 1, 0, 0)
        self.input.addCommandInput(group_cell, row_index, 2, 0, 0)
        self.input.addCommandInput(grain_cell, row_index, 3, 0, 0)
        self._records.append(PartRecord(
            token=body.entityToken,
            body=body,
            face=face,
            direction_token=stored.direction_token,
            name_cell=name_cell,
            rotation_cell=rotation_cell,
            group_cell=group_cell,
            grain_cell=grain_cell,
        ))
