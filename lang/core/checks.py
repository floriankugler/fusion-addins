"""Checks that run on the layout, before any geometry exists."""
from __future__ import annotations

from .scope import Scope


def no_interference(scope: Scope) -> list[str]:
    """Pairs of parts in the scope (and below) whose boxes overlap."""
    parts = scope.all_parts()
    problems: list[str] = []
    for i, a in enumerate(parts):
        for b in parts[i + 1:]:
            if a.box().overlaps(b.box()):
                problems.append(f"{a.path} overlaps {b.path}")
    return problems


def fits_sheet(scope: Scope) -> list[str]:
    problems: list[str] = []
    for part in scope.all_parts():
        sheet = part.material.sheet
        if sheet is None:
            continue
        w, h = part.outline.width, part.outline.height
        if not ((w <= sheet[0] and h <= sheet[1]) or (w <= sheet[1] and h <= sheet[0])):
            problems.append(f"{part.path} ({w:g} x {h:g}) does not fit a {sheet[0]:g} x {sheet[1]:g} sheet")
    return problems
