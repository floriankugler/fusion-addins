"""The per-part settings table of the Multi-Arrange dialog.

One row per selected part with a check box, its rotation mode and its rigid
group, like the component table in Fusion's own Arrange dialog.

Rigid groups are formed by checking rows and pressing the group button rather
than by typing a name into every row: a Fusion table only ever reports a
single highlighted row (`selectedRow`), so the check boxes are what makes a
multi-row command possible at all.

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
}

GROUP_PREFIX = 'Group '


@dataclass
class PartRecord:
    token: str
    body: adsk.fusion.BRepBody
    face: adsk.fusion.BRepFace
    select_cell: adsk.core.BoolValueCommandInput
    name_cell: adsk.core.StringValueCommandInput
    rotation_cell: adsk.core.DropDownCommandInput
    group_cell: adsk.core.StringValueCommandInput


class PartTableInput(inputs.Input):
    """Table of the selected parts and their nesting settings."""

    value: dict[str, model.PartSettings]  # keyed by body entity token
    input: adsk.core.TableCommandInput

    def __init__(self, id: str, name: str, tool_tip: str, update_visibility=lambda: True):
        super().__init__(id, name, tool_tip, update_visibility)
        self.value = {}
        # Message from the last button press, for the dialog to display.
        self.message: str | None = None
        self._records: list[PartRecord] = []
        # Cell inputs need ids that are unique for the lifetime of the dialog.
        self._next_row_key = 0
        self._remove_button: adsk.core.BoolValueCommandInput | None = None
        self._remove_all_button: adsk.core.BoolValueCommandInput | None = None
        self._group_button: adsk.core.BoolValueCommandInput | None = None
        self._ungroup_button: adsk.core.BoolValueCommandInput | None = None

    @property
    def records(self) -> list[PartRecord]:
        return list(self._records)

    def create_input(self, command_inputs: adsk.core.CommandInputs, params: adsk.fusion.CustomFeatureParameters | None):
        if params is not None:
            raise RuntimeError('The parts table cannot be restored from a custom feature.')
        table = command_inputs.addTableCommandInput(self.id, self.name, 4, '1:4:3:3')
        table.minimumVisibleRows = 3
        table.maximumVisibleRows = 12
        table.hasGrid = False
        table.tablePresentationStyle = adsk.core.TablePresentationStyles.itemBorderTablePresentationStyle  # type: ignore
        self.input = table
        self._add_header_row()

        children = table.commandInputs
        self._group_button = children.addBoolValueInput(
            f'{self.id}_group', 'Make group', False, '', False)
        self._group_button.tooltip = (
            'Nests the checked parts as one rigid unit, keeping their current '
            'relative positions.'
        )
        table.addToolbarCommandInput(self._group_button)
        self._ungroup_button = children.addBoolValueInput(
            f'{self.id}_ungroup', 'Clear group', False, '', False)
        self._ungroup_button.tooltip = 'Removes the checked parts from their group.'
        table.addToolbarCommandInput(self._ungroup_button)
        self._remove_button = children.addBoolValueInput(
            f'{self.id}_remove', 'Remove', False, '', False)
        self._remove_button.tooltip = 'Removes the checked parts from the arrangement.'
        table.addToolbarCommandInput(self._remove_button)
        self._remove_all_button = children.addBoolValueInput(
            f'{self.id}_remove_all', 'Remove all', False, '', False)
        self._remove_all_button.tooltip = (
            'Empties the parts list. With an existing arrangement selected '
            'above, clicking OK on an empty list deletes that arrangement and '
            'restores its parts to full opacity.'
        )
        table.addToolbarCommandInput(self._remove_all_button)

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
        self.message = None
        if self._group_button and changed_input.id == self._group_button.id:
            self._group_button.value = False
            self.message = self.group_checked()
            return True
        if self._ungroup_button and changed_input.id == self._ungroup_button.id:
            self._ungroup_button.value = False
            self.message = self.ungroup_checked()
            return True
        if self._remove_button and changed_input.id == self._remove_button.id:
            self._remove_button.value = False
            self.message = self.remove_checked()
            return True
        if self._remove_all_button and changed_input.id == self._remove_all_button.id:
            self._remove_all_button.value = False
            self.message = self.remove_all()
            return True
        return False

    # ------------------------------------------------------------- commands

    def group_checked(self) -> str | None:
        """Puts the checked parts into a new rigid group."""
        targets = self._checked_records()
        if len(targets) < 2:
            return 'Check at least two parts to group them.'
        name = self._next_group_name()
        for record in targets:
            record.group_cell.value = name
            record.select_cell.value = False
        self.update_from_input()
        return None

    def ungroup_checked(self) -> str | None:
        targets = self._checked_records()
        if not targets:
            return 'Check the parts whose group should be cleared.'
        for record in targets:
            record.group_cell.value = ''
            record.select_cell.value = False
        self.update_from_input()
        return None

    def remove_all(self) -> str | None:
        """Empties the table. Like remove_checked, the caller must rebuild the
        faces selection input from `records` afterwards."""
        if not self._records:
            return 'The parts list is already empty.'
        for index in range(len(self._records) - 1, -1, -1):
            self.input.deleteRow(index + 1)
        self._records.clear()
        self.update_from_input()
        return None

    def remove_checked(self) -> str | None:
        """Removes the checked parts. The caller must rebuild the faces
        selection input from `records` afterwards, otherwise the next selection
        sync re-adds them."""
        targets = self._checked_records()
        if not targets:
            return 'Check the parts to remove.'
        for record in targets:
            index = self._records.index(record)
            self.input.deleteRow(index + 1)
            del self._records[index]
        self.update_from_input()
        return None

    def _checked_records(self) -> list[PartRecord]:
        """The checked rows, falling back to the highlighted row."""
        checked = [record for record in self._records if record.select_cell.value]
        if checked:
            return checked
        record = self._selected_record()
        return [record] if record is not None else []

    def _next_group_name(self) -> str:
        existing = {record.group_cell.value.strip() for record in self._records}
        index = 1
        while f'{GROUP_PREFIX}{index}' in existing:
            index += 1
        return f'{GROUP_PREFIX}{index}'

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
                direction_token=None,
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
        for column, title in enumerate(('', 'Part', 'Rotation', 'Group')):
            header = children.addStringValueInput(f'{self.id}_header_{column}', '', title)
            header.isReadOnly = True
            self.input.addCommandInput(header, 0, column, 0, 0)

    def _append_row(self, face: adsk.fusion.BRepFace):
        body = face.body
        stored = model.load_settings(body)
        # Settings saved by older versions may use rotation modes that no
        # longer exist in the dropdown; treat them as Grain.
        stored_rotation = stored.rotation if stored.rotation in ROTATION_NAMES else model.ROTATION_GRAIN
        key = self._next_row_key
        self._next_row_key += 1
        children = self.input.commandInputs

        select_cell = children.addBoolValueInput(f'{self.id}_select_{key}', '', True, '', False)

        name_cell = children.addStringValueInput(f'{self.id}_name_{key}', '', body.name)
        name_cell.isReadOnly = True

        rotation_cell = children.addDropDownCommandInput(
            f'{self.id}_rotation_{key}', '', adsk.core.DropDownStyles.TextListDropDownStyle)  # type: ignore
        for value, name in ROTATION_NAMES.items():
            rotation_cell.listItems.add(name, value == stored_rotation)

        # Group names come from the group buttons, so the cell only reports.
        group_cell = children.addStringValueInput(f'{self.id}_group_{key}', '', stored.group or '')
        group_cell.isReadOnly = True

        row_index = self.input.rowCount
        self.input.addCommandInput(select_cell, row_index, 0, 0, 0)
        self.input.addCommandInput(name_cell, row_index, 1, 0, 0)
        self.input.addCommandInput(rotation_cell, row_index, 2, 0, 0)
        self.input.addCommandInput(group_cell, row_index, 3, 0, 0)
        self._records.append(PartRecord(
            token=body.entityToken,
            body=body,
            face=face,
            select_cell=select_cell,
            name_cell=name_cell,
            rotation_cell=rotation_cell,
            group_cell=group_cell,
        ))
