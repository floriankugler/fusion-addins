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
        # A compiled part of a material without grain may turn freely.
        compiled = compiled_part(body)
        if compiled is not None and not compiled.grained:
            return PartSettings(rotation=ROTATION_FREE)
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


# -- parts compiled by the modeling language -------------------------------------

#: The attribute the modeling language's compiler writes on every body it
#: makes (lang/emit/fusion.py): JSON with the part's path, its kind (a
#: board, or a slat, which is not nested), material, thickness, whether the
#: material has a grain, the grain direction (or null) and `up`, the outward
#: normal of the face it is machined from. The vectors are in the body's
#: component space.
COMPILED_GROUP = 'lang'
COMPILED_NAME = 'part'


@dataclass
class CompiledPart:
    body: adsk.fusion.BRepBody          # in the root's context
    path: str
    material: str                       # as the build labels it, e.g. 'birch 15'
    thickness: float                    # mm
    grained: bool
    grain: adsk.core.Vector3D | None    # world; None when the build left it unset
    up: adsk.core.Vector3D              # world


def _world_vector(values, body: adsk.fusion.BRepBody) -> adsk.core.Vector3D | None:
    if not values:
        return None
    vector = adsk.core.Vector3D.create(*(float(v) for v in values))
    if vector.length < 1e-9:
        return None
    context = body.assemblyContext
    if context is not None:
        vector.transformBy(context.transform2)
    vector.normalize()
    return vector


def compiled_part(body: adsk.fusion.BRepBody) -> CompiledPart | None:
    """The compiler's facts about a body, or None for a body it did not make."""
    # The compiler writes on the body itself; a proxy (the body as seen
    # through its occurrence) does not show those attributes.
    native = body.nativeObject or body
    attribute = native.attributes.itemByName(COMPILED_GROUP, COMPILED_NAME)
    if attribute is None or not attribute.value:
        return None
    try:
        data = json.loads(attribute.value)
    except ValueError:
        return None
    if data.get('kind') == 'slat':
        return None                     # solid wood by section and length: on the cut list, not nested
    up = _world_vector(data.get('up'), body)
    if up is None:
        return None
    return CompiledPart(body=body, path=str(data.get('path', body.name)),
                        material=str(data.get('material', '')), thickness=float(data.get('thickness', 0.0)),
                        grained=bool(data.get('grained', True)),
                        grain=_world_vector(data.get('grain'), body), up=up)


def find_compiled_parts(design: adsk.fusion.Design) -> list[CompiledPart]:
    """Every body the compiler made in this design, in the root's context
    (one per occurrence of its component). Found through the attribute
    index, so it stays cheap in a large design."""
    root = design.rootComponent
    found: list[CompiledPart] = []
    for attribute in design.findAttributes(COMPILED_GROUP, COMPILED_NAME):
        body = adsk.fusion.BRepBody.cast(attribute.parent)
        if body is None:
            continue
        if body.parentComponent == root:
            bodies = [body]
        else:
            bodies = [body.createForAssemblyContext(occurrence)
                      for occurrence in root.allOccurrencesByComponent(body.parentComponent)]
        for candidate in bodies:
            part = compiled_part(candidate)
            if part is not None:
                found.append(part)
    return found


def machining_face(part: CompiledPart) -> adsk.fusion.BRepFace | None:
    """The face to put up for a compiled part: the planar face facing `up`
    that lies furthest along it (a pocket's floor faces up too, but lower)."""
    best: tuple[float, float, adsk.fusion.BRepFace] | None = None
    for face in part.body.faces:
        if not isinstance(face.geometry, adsk.core.Plane):
            continue
        point = face.pointOnFace
        ok, normal = face.evaluator.getNormalAtPoint(point)
        if not ok or normal.dotProduct(part.up) < 0.999:
            continue
        key = (round(point.asVector().dotProduct(part.up), 6), face.area)
        if best is None or key > best[:2]:
            best = (key[0], key[1], face)
    return best[2] if best else None


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
