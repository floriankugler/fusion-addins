"""The inventory: the stock on hand, a ledger file of one kind of entry,
full sheets and offcuts alike [Florian, 2026-10-16], one per project,
`inventory.toml` beside the build file:

    [[stock]]
    material = "birch 15"       # the material as the layout labels it
    size = [1250, 600]          # mm, along the grain first
    count = 2                   # how many; 1 if not given

The nest uses what is on hand before it buys (`nest`); what it buys is the
material's sheet size (`sheet_material(..., size=)`). The nest only reads
the ledger for now: the rests of a nest made go into it with pinning
(`design/nesting.md`). Florian adds the sheets he buys and deletes by hand
what is used elsewhere.
"""
from __future__ import annotations

import math
import tomllib
from pathlib import Path
from typing import Any

from ..core.errors import LangError
from .workshop import OnHand

#: Its name beside the build file.
NAME = "inventory.toml"
_KEYS = {"material", "size", "count"}


def read_inventory(path: str | Path) -> list[OnHand]:
    """The ledger at `path` (see the module's doc)."""
    try:
        data = tomllib.loads(Path(path).read_text())
    except tomllib.TOMLDecodeError as error:
        raise LangError(f"{path}: {error}") from None
    except OSError as error:
        raise LangError(f"{path}: {error.strerror or error}") from None
    return inventory_from(data, str(path))


def inventory_from(data: dict[str, Any], where: str = "the inventory") -> list[OnHand]:
    unknown = sorted(set(data) - {"stock"})
    if unknown:
        raise LangError(f"{where}: unknown key {', '.join(unknown)}; the inventory lists [[stock]] entries.")
    entries = data.get("stock", [])
    if not isinstance(entries, list) or not all(isinstance(e, dict) for e in entries):  # pyright: ignore[reportUnknownVariableType]
        raise LangError(f"{where}: write each piece of stock as a [[stock]] table.")
    out: list[OnHand] = []
    for k, entry in enumerate(entries, 1):  # pyright: ignore[reportUnknownVariableType, reportUnknownArgumentType]
        what = f"{where}: stock {k}"
        e: dict[str, Any] = entry  # pyright: ignore[reportUnknownVariableType]
        bad = sorted(set(e) - _KEYS)
        if bad:
            raise LangError(f"{what}: unknown key {', '.join(bad)} (the keys: {', '.join(sorted(_KEYS))}).")
        if "material" not in e or "size" not in e:
            raise LangError(f"{what}: give its material and size, as material = \"birch 15\" and size = [1250, 600].")
        material = e["material"]
        if not isinstance(material, str) or not material.strip():
            raise LangError(f"{what}: material is a material's name and thickness, as \"birch 15\".")
        length, width = _size(e["size"], f"{what}: size")
        count = _count(e.get("count", 1), f"{what}: count")
        out.append(OnHand(material.strip(), length, width, count))
    return out


def _size(value: object, what: str) -> tuple[float, float]:
    if not isinstance(value, list) or len(value) != 2:  # pyright: ignore[reportUnknownArgumentType]
        raise LangError(f"{what}: give two numbers in mm, along the grain first, as [1250, 600].")
    out: list[float] = []
    for v in value:  # pyright: ignore[reportUnknownVariableType]
        if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) or v <= 0:
            raise LangError(f"{what}: {v!r} is not a size in mm, more than 0.")
        out.append(float(v))
    return out[0], out[1]


def _count(value: object, what: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise LangError(f"{what}: {value!r} is not a whole number, 1 or more.")
    return value
