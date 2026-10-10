from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Material:
    name: str
    #: Thickness in mm.
    t: float
    #: Whether the material has a grain direction that matters.
    grain: bool = True
    #: Sheet size in mm for the sheet-fit check, None if unknown.
    sheet: tuple[float, float] | None = None

    @property
    def label(self) -> str:
        return f"{self.name} {self.t:g}"


def material(name: str, t: float, grain: bool = True, sheet=None) -> Material:
    return Material(name, float(t), grain, sheet)
