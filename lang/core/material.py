"""What parts are made of: sheet stock for boards, solid wood for slats.

A sheet material is bought by thickness (`sheet_material("birch", t=15)`),
so a board's thickness comes from it. Solid wood is ripped to whatever a
part needs, so a slat material is only a species (`slat_material("oak")`):
a slat's section is the slat's own, a lip's thickness the lip's.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SheetMaterial:
    name: str
    #: Thickness in mm, as a board's `thickness` (`sheet_material(name, t=)`
    #: sets it) [decided by Florian, 2026-10-15, syntax.md item 11].
    thickness: float
    #: Whether the material has a grain direction that matters.
    grain: bool = True
    #: Sheet size in mm for the sheet-fit check, None if unknown.
    size: tuple[float, float] | None = None

    @property
    def label(self) -> str:
        return f"{self.name} {self.thickness:g}"


@dataclass(frozen=True)
class SlatMaterial:
    #: The species, as the layout labels the slats made of it.
    name: str

    @property
    def grain(self) -> bool:
        """Solid wood always has grain; a slat's runs along its length."""
        return True

    @property
    def label(self) -> str:
        return self.name


Material = SheetMaterial | SlatMaterial


def sheet_material(name: str, t: float, grain: bool = True,
                   size: tuple[float, float] | None = None) -> SheetMaterial:
    return SheetMaterial(name, float(t), grain, size)


def slat_material(name: str) -> SlatMaterial:
    return SlatMaterial(name)
