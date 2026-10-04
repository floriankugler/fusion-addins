"""Re-editing the timeline group a native-feature add-in created.

Native-feature add-ins leave plain sketches and features behind, collected
in one timeline group. To make such a group editable again, the add-in
stores its dialog state as an attribute on one member of the group. Picking
any member later restores the dialog from that state with the timeline
rolled back to just before the group; OK then deletes the old group and
builds the features afresh at that position.

Rebuilding gives every face and edge a new identity, and deleting the old
group silently deletes later features that reference its geometry, so
Addin refuses the edit when that would happen.

Experimental: see Addin.group_edit_enabled.
"""
import json
from dataclasses import dataclass
from typing import Any

import adsk.core, adsk.fusion

from . import inputs as inp

STATE_ATTRIBUTE = 'editState'
STATE_VERSION = 1


@dataclass
class EditTarget:
    group: adsk.fusion.TimelineGroup
    state: dict[str, Any]


def write_state(
    entity: adsk.core.Base,
    attribute_group: str,
    inputs: inp.Inputs,
) -> None:
    values = {}
    for source in inputs.inputs:
        # getattr: after a dev-mode lib reload an input can be an instance
        # of a class that predates save_state.
        save_state = getattr(source, 'save_state', None)
        state = save_state() if save_state else None
        if state is not None:
            values[source.id] = state
    entity.attributes.add(
        attribute_group,
        STATE_ATTRIBUTE,
        json.dumps({'version': STATE_VERSION, 'inputs': values}),
    )


def find_target(
    entity: adsk.core.Base | None,
    attribute_group: str,
) -> EditTarget | None:
    """The group `entity` belongs to, with the state stored in it. None
    when `entity` is not part of a group this add-in created with a
    stored state."""
    group = _timeline_group(entity)
    if group is None:
        return None
    for index in range(group.count):
        member = group.item(index).entity
        attributes = getattr(member, 'attributes', None) if member else None
        attribute = (
            attributes.itemByName(attribute_group, STATE_ATTRIBUTE)
            if attributes
            else None
        )
        if not attribute:
            continue
        try:
            payload = json.loads(attribute.value)
        except ValueError:
            return None
        if payload.get('version') != STATE_VERSION:
            return None
        return EditTarget(group, payload.get('inputs', {}))
    return None


def restore_state(
    inputs: inp.Inputs,
    state: dict[str, Any],
    design: adsk.fusion.Design,
) -> list[str]:
    """Applies `state` to the inputs and their dialog controls. Returns the
    names of the inputs that could not be restored."""
    failed: list[str] = []
    for source in inputs.inputs:
        restore = getattr(source, 'restore_state', None)
        if source.id not in state or not restore:
            continue
        try:
            restored = restore(state[source.id], design)
        except Exception:
            restored = False
        if not restored:
            failed.append(source.name)
    return failed


def _timeline_group(
    entity: adsk.core.Base | None,
) -> adsk.fusion.TimelineGroup | None:
    if entity is None:
        return None
    group = adsk.fusion.TimelineGroup.cast(entity)
    if group:
        return group
    native = getattr(entity, 'nativeObject', None)
    try:
        timeline_object = (native or entity).timelineObject
    except Exception:
        return None
    return timeline_object.parentGroup if timeline_object else None
