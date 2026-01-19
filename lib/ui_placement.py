import adsk.core
from dataclasses import dataclass


@dataclass(frozen=True)
class PlacementSpec:
    id: str
    anchor_id: str
    insert_before: bool = False


@dataclass(frozen=True)
class UIPlacement:
    panel_id: str
    command: PlacementSpec
    section: PlacementSpec | None = None


def add_command_to_ui(
    ui: adsk.core.UserInterface,
    placement: UIPlacement,
    command_def: adsk.core.CommandDefinition,
    command_id: str,
) -> None:
    if placement.command.id != command_id:
        raise RuntimeError(
            f"UI placement command id mismatch: {placement.command.id} != {command_id}"
        )

    panel = ui.allToolbarPanels.itemById(placement.panel_id)
    if not panel:
        raise RuntimeError(f"UI panel not found: {placement.panel_id}")

    existing_ctrl = panel.controls.itemById(command_id)
    if existing_ctrl:
        existing_ctrl.deleteMe()

    section = placement.section
    if section and not panel.controls.itemById(section.id):
        panel.controls.addSeparator(section.id, section.anchor_id, section.insert_before)

    panel.controls.addCommand(
        command_def,
        placement.command.anchor_id,
        placement.command.insert_before,
    )


def remove_command_from_ui(
    ui: adsk.core.UserInterface,
    placement: UIPlacement,
    command_id: str,
) -> None:
    panel = ui.allToolbarPanels.itemById(placement.panel_id)
    if panel:
        panel_ctrl = panel.controls.itemById(command_id)
        if panel_ctrl:
            panel_ctrl.deleteMe()

