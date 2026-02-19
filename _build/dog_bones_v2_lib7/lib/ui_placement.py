import adsk.core
import json
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


def dump_ui_structure(ui: adsk.core.UserInterface) -> str:
    def control_info(ctrl: adsk.core.ToolbarControl) -> dict:
        info = {
            "id": ctrl.id,
        }
        cmd_ctrl = adsk.core.CommandControl.cast(ctrl)
        if cmd_ctrl:
            try:
                cmd_def = cmd_ctrl.commandDefinition
            except Exception:
                cmd_def = None
            if cmd_def and cmd_def.name:
                info["commandName"] = cmd_def.name
        return info

    workspace = ui.activeWorkspace
    if not workspace:
        return json.dumps({"workspace": None}, indent=2)

    workspace_entry = {
        "id": workspace.id,
        "name": workspace.name,
        "tabs": [],
    }
    for t_idx in range(workspace.toolbarTabs.count):
        tab = workspace.toolbarTabs.item(t_idx)
        if not tab:
            continue
        tab_entry = {
            "id": tab.id,
            "name": tab.name,
            "panels": [],
        }
        for p_idx in range(tab.toolbarPanels.count):
            panel = tab.toolbarPanels.item(p_idx)
            if not panel:
                continue
            panel_entry = {
                "id": panel.id,
                "name": panel.name,
                "controls": [],
            }
            for c_idx in range(panel.controls.count):
                ctrl = panel.controls.item(c_idx)
                if ctrl:
                    panel_entry["controls"].append(control_info(ctrl))
            tab_entry["panels"].append(panel_entry)
        workspace_entry["tabs"].append(tab_entry)

    return json.dumps({"workspace": workspace_entry}, indent=2)


def dump_ui_structure_to_file(ui: adsk.core.UserInterface, path: str) -> str:
    payload = dump_ui_structure(ui)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(payload)
    return path
