"""Template registry for auto_setup.

Operation parameters (tool, feeds, passes, tabs, ...) are owned by user-authored
CAM template files stored in the add-in's templates directory. Files follow the
naming convention

    <kind>[.<tag>[.<tag>...]]_<label>.f3dhsm-template

where kind is one of 'pocket', 'contour', 'drill', 'bore'. Tags encode machine-
readable attributes; the label is purely cosmetic (shown in the UI):

    dc      spiral down-cut cutter variant
    udc     spiral up/down-cut cutter variant
    finish  the template includes a finishing pass

Templates without a cutter tag are valid for any cutter selection.

Templates are authored via the 'Export Auto Setup Templates' command: every
setup in the active document whose name follows the same convention is exported
as one template file (a setup with several operations becomes a multi-operation
template, e.g. rough + finish).
"""

import adsk.core, adsk.cam
import os
from dataclasses import dataclass

KINDS = ('pocket', 'contour', 'drill', 'bore')
CUTTER_TAGS = ('dc', 'udc')
VALID_TAGS = ('dc', 'udc', 'finish')
FILE_EXT = '.f3dhsm-template'


class TemplateError(Exception):
    pass


@dataclass(frozen=True)
class TemplateVariant:
    kind: str
    tags: tuple[str, ...]
    label: str
    path: str

    @property
    def name(self) -> str:
        head = '.'.join((self.kind,) + self.tags)
        return f'{head}_{self.label}'

    @property
    def cutter(self) -> str | None:
        for tag in self.tags:
            if tag in CUTTER_TAGS:
                return tag
        return None

    @property
    def has_finish(self) -> bool:
        return 'finish' in self.tags

    @property
    def display_label(self) -> str:
        return f'{self.label} +finish' if self.has_finish else self.label

    def matches_cutter(self, cutter: str | None) -> bool:
        return self.cutter is None or cutter is None or self.cutter == cutter


def parse_stem(stem: str) -> tuple[str, tuple[str, ...], str] | None:
    """Parse '<kind>[.<tag>...]_<label>' into (kind, tags, label), or None."""
    head, sep, label = stem.partition('_')
    if not sep or not label:
        return None
    parts = head.split('.')
    kind, tags = parts[0], tuple(parts[1:])
    if kind not in KINDS:
        return None
    if any(tag not in VALID_TAGS for tag in tags):
        return None
    return kind, tags, label


def scan(templates_dir: str, issues: list[str] | None = None) -> dict[str, list[TemplateVariant]]:
    """Return available template variants keyed by kind."""
    registry: dict[str, list[TemplateVariant]] = {kind: [] for kind in KINDS}
    if not os.path.isdir(templates_dir):
        return registry
    for file_name in sorted(os.listdir(templates_dir)):
        if not file_name.endswith(FILE_EXT):
            continue
        parsed = parse_stem(file_name[: -len(FILE_EXT)])
        if not parsed:
            if issues is not None:
                issues.append(f'Template file name not understood: {file_name}')
            continue
        kind, tags, label = parsed
        registry[kind].append(TemplateVariant(
            kind=kind, tags=tags, label=label,
            path=os.path.join(templates_dir, file_name)))
    return registry


def load(variant: TemplateVariant) -> adsk.cam.CAMTemplate:
    template = adsk.cam.CAMTemplate.createFromFile(variant.path)
    if not template:
        raise TemplateError(f'Failed to load template {variant.path}')
    return template


def tool_dimensions(variant: TemplateVariant) -> list[tuple[float | None, float | None]]:
    """(diameter, flute length) in cm for every operation in the template.

    The tool of a template operation is serialized into its parameters
    (CAMTemplateOperationInput.tool itself is None for loaded templates).
    The flute length is treated as the tool's maximum milling depth.
    """
    template = load(variant)
    operations = template.operations
    dimensions: list[tuple[float | None, float | None]] = []
    for idx in range(operations.count):
        parameters = operations.get(idx).parameters
        diameter = parameters.itemByName('tool_diameter')
        flute = parameters.itemByName('tool_fluteLength')
        dimensions.append((
            diameter.value.value if diameter else None,
            flute.value.value if flute else None,
        ))
    return dimensions


def primary_tool(variant: TemplateVariant) -> tuple[float | None, float | None]:
    """(diameter, flute length) of the template's first operation."""
    dimensions = tool_dimensions(variant)
    return dimensions[0] if dimensions else (None, None)


def min_tool_dimensions(variant: TemplateVariant) -> tuple[float | None, float | None]:
    """(smallest diameter, shortest flute) across the template's operations."""
    dimensions = tool_dimensions(variant)
    diameters = [d for d, _ in dimensions if d is not None]
    flutes = [f for _, f in dimensions if f is not None]
    return (min(diameters) if diameters else None,
            min(flutes) if flutes else None)


def export_document_setups(templates_dir: str) -> tuple[list[str], list[str]]:
    """Export every convention-named setup of the active document as a template file.

    Returns (exported names, skipped setup names).
    """
    app = adsk.core.Application.get()
    cam = adsk.cam.CAM.cast(app.activeDocument.products.itemByProductType('CAMProductType'))
    if not cam:
        raise TemplateError('The active document has no CAM data.')

    os.makedirs(templates_dir, exist_ok=True)
    exported: list[str] = []
    skipped: list[str] = []
    for setup in cam.setups:
        name = setup.name.strip()
        if not parse_stem(name) or '/' in name:
            skipped.append(name)
            continue
        operations = [op for op in setup.allOperations]
        if not operations:
            skipped.append(name)
            continue
        template = adsk.cam.CAMTemplate.createFromOperations(operations)
        path = os.path.join(templates_dir, f'{name}{FILE_EXT}')
        if not template.save(path):
            raise TemplateError(f'Failed to save template to {path}')
        exported.append(name)
    return exported, skipped
