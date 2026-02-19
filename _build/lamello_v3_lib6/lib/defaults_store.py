import json
import os
import sys
from typing import Any


def defaults_path(addin_module_name: str, addin_id: str) -> str:
    module = sys.modules.get(addin_module_name)
    module_file = getattr(module, "__file__", None) if module else None
    if not module_file:
        return f"{addin_id}.json"

    addin_folder = os.path.dirname(os.path.abspath(module_file))
    parent_folder = os.path.dirname(addin_folder)
    return os.path.join(parent_folder, f"{addin_id}.json")


def load(path: str) -> dict[str, Any]:
    try:
        with open(path, "r", encoding="utf-8") as handle:
            payload = json.load(handle)
    except FileNotFoundError:
        return {}
    except Exception:
        return {}

    if not isinstance(payload, dict):
        return {}

    values = payload.get("values")
    if isinstance(values, dict):
        return values

    return {}


def save(path: str, values: dict[str, Any], comment: dict[str, Any]) -> None:
    payload: dict[str, Any] = {"values": values}
    if comment:
        payload["_comment"] = comment

    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)
        handle.write("\n")
