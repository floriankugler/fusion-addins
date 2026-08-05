"""Part metadata for multi-arrange.

Per-part settings (rotation mode, grain reference, group membership) are stored
as an attribute on the body so they survive re-runs and design changes. The
arrange command reads them back for whatever bodies the user selects; bodies
without an attribute fall back to free rotation.
"""

import adsk.core, adsk.fusion
import json
from dataclasses import dataclass, field


ATTRIBUTE_GROUP = 'multi_arrange'
ATTRIBUTE_NAME = 'part'

# Rotation modes, in dialog order. The solver's rotation types are richer, but
# only these three make sense for grain handling.
ROTATION_FREE = 0        # any rotation
ROTATION_GRAIN = 1       # 0 or 180 deg: grain along envelope X
ROTATION_GRAIN_ONE_WAY = 2  # 0 deg only: directional grain (e.g. cathedral figure)


@dataclass
class PartSettings:
    """The stored per-body settings. Grain is the default: for sheet goods,
    respecting the grain is the norm and free rotation the exception."""
    rotation: int = ROTATION_GRAIN
    direction_token: str | None = None  # entity token of the grain reference
    group: str | None = None            # rigid group name, None = ungrouped

    def to_json(self) -> str:
        return json.dumps({
            'rotation': self.rotation,
            'direction_token': self.direction_token,
            'group': self.group,
        })

    @staticmethod
    def from_json(raw: str) -> 'PartSettings':
        data = json.loads(raw)
        return PartSettings(
            rotation=int(data.get('rotation', ROTATION_GRAIN)),
            direction_token=data.get('direction_token') or None,
            group=data.get('group') or None,
        )


def save_settings(body: adsk.fusion.BRepBody, settings: PartSettings):
    body.attributes.add(ATTRIBUTE_GROUP, ATTRIBUTE_NAME, settings.to_json())


def load_settings(body: adsk.fusion.BRepBody) -> PartSettings:
    attribute = body.attributes.itemByName(ATTRIBUTE_GROUP, ATTRIBUTE_NAME)
    if attribute is None or not attribute.value:
        return PartSettings()
    try:
        return PartSettings.from_json(attribute.value)
    except (ValueError, KeyError):
        return PartSettings()


def clear_settings(body: adsk.fusion.BRepBody):
    attribute = body.attributes.itemByName(ATTRIBUTE_GROUP, ATTRIBUTE_NAME)
    if attribute:
        attribute.deleteMe()


SHEETS_ATTRIBUTE_NAME = 'sheets'


def save_sheet_specs(design: adsk.fusion.Design, rows: list[dict]):
    """Remembers the sheet table contents (per design) for the next run.

    rows: [{'width': expression, 'height': expression, 'count': int}, ...]
    """
    design.rootComponent.attributes.add(ATTRIBUTE_GROUP, SHEETS_ATTRIBUTE_NAME, json.dumps(rows))


def load_sheet_specs(design: adsk.fusion.Design) -> list[dict] | None:
    attribute = design.rootComponent.attributes.itemByName(ATTRIBUTE_GROUP, SHEETS_ATTRIBUTE_NAME)
    if attribute is None or not attribute.value:
        return None
    try:
        rows = json.loads(attribute.value)
    except ValueError:
        return None
    if not isinstance(rows, list) or not rows:
        return None
    return rows


RECIPE_ATTRIBUTE_NAME = 'recipe'


def save_recipe(component: adsk.fusion.Component, recipe: dict):
    """Stores everything needed to re-create an arrangement on its result
    component: part face tokens, sheet rows, offsets, plane, and options."""
    component.attributes.add(ATTRIBUTE_GROUP, RECIPE_ATTRIBUTE_NAME, json.dumps(recipe))


def load_recipe(component: adsk.fusion.Component) -> dict | None:
    attribute = component.attributes.itemByName(ATTRIBUTE_GROUP, RECIPE_ATTRIBUTE_NAME)
    if attribute is None or not attribute.value:
        return None
    try:
        recipe = json.loads(attribute.value)
    except ValueError:
        return None
    return recipe if isinstance(recipe, dict) else None


def resolve_direction(design: adsk.fusion.Design, token: str) -> adsk.core.Vector3D | None:
    """World-space direction of a stored grain reference, if it still exists."""
    entities = design.findEntityByToken(token)
    if not entities:
        return None
    return direction_of(entities[0])


def texture_grain_direction(body: adsk.fusion.BRepBody) -> adsk.core.Vector3D | None:
    """World-space grain direction from the body's appearance texture mapping.

    Only 3D textures ("3D Cherry", "3D Mahogany", …) are used: their control
    defines the wood grain along the transform's Z axis, and Fusion renders
    that orientation, so what the user sees is what gets nested. For
    image-based projected textures Z is the projection axis (normally the face
    normal, i.e. no grain information at all), and Fusion ignores the mapping
    when rendering — reading those would silently invent a direction.
    """
    try:
        control = body.textureMapControl
    except RuntimeError:
        return None
    if not isinstance(control, adsk.core.TextureMapControl3D):
        return None
    transform = getattr(control, 'transform', None)
    if transform is None:
        return None
    grain = adsk.core.Vector3D.create(
        transform.getCell(0, 2), transform.getCell(1, 2), transform.getCell(2, 2))
    if grain.length < 1e-6:
        return None
    grain.normalize()
    context = body.assemblyContext
    if context is not None:
        # The texture transform is stored in component space.
        grain.transformBy(context.transform2)
        grain.normalize()
    return grain


def direction_of(entity) -> adsk.core.Vector3D | None:
    """World-space direction of a linear reference entity."""
    if isinstance(entity, adsk.fusion.BRepEdge):
        geometry = entity.geometry
        if isinstance(geometry, adsk.core.Line3D):
            vector = geometry.startPoint.vectorTo(geometry.endPoint)
            vector.normalize()
            return vector
        return None
    if isinstance(entity, adsk.fusion.SketchLine):
        line = entity.worldGeometry
        vector = line.startPoint.vectorTo(line.endPoint)
        vector.normalize()
        return vector
    if isinstance(entity, adsk.fusion.ConstructionAxis):
        line = entity.geometry
        vector = line.direction.copy()
        vector.normalize()
        return vector
    return None


@dataclass
class Part:
    """A resolved part: the body, its up-face, and effective settings."""
    body: adsk.fusion.BRepBody
    top_face: adsk.fusion.BRepFace
    settings: PartSettings
    grain: adsk.core.Vector3D | None = None  # resolved world direction, may be None


@dataclass
class Group:
    name: str
    parts: list[Part] = field(default_factory=list)
