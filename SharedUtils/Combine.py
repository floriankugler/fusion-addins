from typing import cast
import adsk.core, adsk.fusion
from dataclasses import dataclass, field
import utils
from enum import Enum

class Operation(Enum):
    CUT = 1
    JOIN = 2

class Combine:        
    target_body: adsk.fusion.BRepBody
    tool_body: adsk.fusion.BRepBody
    type: Operation
    target_snapshot: adsk.fusion.BRepBody

    def __init__(self, target_body: adsk.fusion.BRepBody, tool_body: adsk.fusion.BRepBody, type: Operation):
        self.target_body = target_body
        self.tool_body = tool_body
        self.type = type
        mgr = adsk.fusion.TemporaryBRepManager.get()
        self.target_snapshot = mgr.copy(target_body)

@dataclass
class _TargetCombine:
    target_body: adsk.fusion.BRepBody
    new_body: adsk.fusion.BRepBody

    def merge(self, op: Combine):
        assert(self.target_body == op.target_body)
        mgr = adsk.fusion.TemporaryBRepManager.get()
        bool_type = adsk.fusion.BooleanTypes.UnionBooleanType if op.type == Operation.JOIN else adsk.fusion.BooleanTypes.DifferenceBooleanType
        mgr.booleanOperation(self.new_body, op.tool_body, bool_type) # type: ignore

    @classmethod
    def aggregate_combines(cls, combines: list[Combine], base_component: adsk.fusion.Component) -> tuple[dict[str, '_TargetCombine'], dict[str, '_TargetCombine']]:
        inside_component: dict[str, _TargetCombine] = {}
        outside_component: dict[str, _TargetCombine] = {}
        for c in combines:
            target_dict = inside_component if c.target_body.parentComponent == base_component else outside_component
            target_token = c.target_body.entityToken
            if not target_token in target_dict:
                target_dict[target_token] = _TargetCombine(c.target_body, c.target_snapshot)
            target_dict[target_token].merge(c)
        return inside_component, outside_component


def create_features_from_combines(component: adsk.fusion.Component, combines: list[Combine], feature: adsk.fusion.CustomFeature | None, is_compute: bool) -> tuple[list[adsk.fusion.Feature], list[adsk.fusion.Feature], list[adsk.fusion.BRepBody]]:
    mgr = adsk.fusion.TemporaryBRepManager.get()
    token_group_name = 'target-body-token'
    token_value_name = 'value'
    external_combine_key = lambda idx: f"external-combine-{idx}"

    combines_inside_component, combines_outside_component = _TargetCombine.aggregate_combines(combines, component)
    all_combines = combines_inside_component | combines_outside_component
    dependencies = [c.target_body for c in all_combines.values()]

    existing_base_features: list[adsk.fusion.BaseFeature] = []
    existing_inside_combine_features: list[adsk.fusion.CombineFeature] = []
    existing_outside_combine_features: list[adsk.fusion.CombineFeature] = []
    existing_targets: set[str] = set()
    targets_to_delete: list[tuple[adsk.fusion.BaseFeature, adsk.fusion.CombineFeature, adsk.fusion.CombineFeature]] = []
    
    if feature:
        existing_features = cast(list[adsk.fusion.Feature], list(feature.features))

        base_idx = 0
        while base_idx < len(existing_features) and isinstance(existing_features[base_idx], adsk.fusion.BaseFeature):
            base = cast(adsk.fusion.BaseFeature, existing_features[base_idx])
            if base.nativeObject:
                base = base.nativeObject
            existing_base_features.append(base)
            base_idx += 1
        existing_inside_combine_features = cast(list[adsk.fusion.CombineFeature], existing_features[base_idx:])
        
        external_idx = 0
        while token := feature.customNamedValues.value(external_combine_key(external_idx)):
            features = component.parentDesign.findEntityByToken(token)
            if features:
                existing_outside_combine_features.append(cast(adsk.fusion.CombineFeature, features[0]))
            external_idx += 1
        existing_combine_features = existing_inside_combine_features + existing_outside_combine_features
        existing_join_features = existing_combine_features[::2]
        existing_intersect_features = existing_combine_features[1::2]

        for base, join, intersect in zip(existing_base_features, existing_join_features, existing_intersect_features):
            target_token = base.attributes.itemByName(token_group_name, token_value_name).value
            targets = component.parentDesign.findEntityByToken(target_token)
            if targets:
                target = cast(adsk.fusion.BRepBody, targets[0])
                token = target.entityToken
                existing_targets.add(token)
                new_body = all_combines[token].new_body if token in all_combines else mgr.copy(target)
                base.startEdit()
                base.updateBody(base.bodies[0], new_body)
                base.finishEdit()
                base.attributes.add(token_group_name, token_value_name, token)
            else:
                targets_to_delete.append((base, join, intersect))

    new_combines_inside_component = [ v for k, v in combines_inside_component.items() if not k in existing_targets ]
    new_combines_outside_component = [ v for k, v in combines_outside_component.items() if not k in existing_targets]

    if is_compute:
        assert not new_combines_inside_component
        assert not new_combines_outside_component
        features_inside = cast(list[adsk.fusion.Feature], existing_base_features + existing_inside_combine_features)
        features_outside = cast(list[adsk.fusion.Feature], existing_outside_combine_features)
        return features_inside, features_outside, dependencies

    if feature:
        feature.timelineObject.rollTo(True)
        feature.setStartAndEndFeatures(None, None) # type: ignore

        for base, join, intersect in targets_to_delete:
            existing_base_features.remove(base)
            if join in existing_inside_combine_features: 
                existing_inside_combine_features.remove(join)
            else:
                existing_outside_combine_features.remove(join)
            if intersect in existing_inside_combine_features: 
                existing_inside_combine_features.remove(intersect)
            else:   
                existing_outside_combine_features.remove(intersect)
            intersect.deleteMe()
            join.deleteMe()
            base.deleteMe()

    # last_existing_base_feature = existing_base_features[-1] if existing_base_features else feature
    if last_existing_base_feature := last_in_lists(feature, existing_base_features):
        last_existing_base_feature.timelineObject.rollTo(False)
    new_base_features: list[adsk.fusion.BaseFeature] = []
    for combine in new_combines_inside_component + new_combines_outside_component:
        base = component.features.baseFeatures.add()
        base.startEdit()
        component.bRepBodies.add(combine.new_body, base)
        foo = base.attributes.add(token_group_name, token_value_name, combine.target_body.entityToken)
        base.finishEdit()
        new_base_features.append(base)

    # last_existing_inside_combine = existing_inside_combine_features[-1] if existing_inside_combine_features else new_base_features[-1] if new_base_features else last_existing_base_feature
    if last_existing_inside_combine := last_in_lists(last_existing_base_feature, existing_inside_combine_features, new_base_features):
        last_existing_inside_combine.timelineObject.rollTo(False)
    new_inside_combine_features: list[adsk.fusion.Feature] = []
    for combine, base in zip(new_combines_inside_component, new_base_features):
        new_inside_combine_features.extend(create_combine_features(combine, base, component))

    # last_existing_outside_combine = existing_outside_combine_features[-1] if existing_outside_combine_features else new_inside_combine_features[-1] if new_inside_combine_features else last_existing_inside_combine
    if last_existing_outside_combine := last_in_lists(last_existing_inside_combine, existing_outside_combine_features, new_inside_combine_features):
        last_existing_outside_combine.timelineObject.rollTo(False)
    new_outside_combine_features: list[adsk.fusion.Feature] = []
    for combine, base in zip(new_combines_outside_component, new_base_features[len(new_combines_inside_component):]):
        new_outside_combine_features.extend(create_combine_features(combine, base, component))
        
    for idx, f in enumerate(existing_outside_combine_features + new_outside_combine_features):
        id = feature.name if feature else "<unknown>"
        f.name = f"custom-feature<{id}>-{'join' if idx % 2 == 0 else 'intersect'}-{idx}"
        if feature:
            feature.customNamedValues.addOrSetValue(external_combine_key(idx), f.entityToken)

    features_inside = existing_base_features + new_base_features + existing_inside_combine_features + new_inside_combine_features
    features_outside = existing_outside_combine_features + new_outside_combine_features
    return features_inside, features_outside, dependencies

def last_in_lists(fallback, *lists):
    for list in lists:
        if list:
            return list[-1]
    return fallback

def create_combine_features(combine: _TargetCombine, base: adsk.fusion.BaseFeature, component: adsk.fusion.Component) -> list[adsk.fusion.Feature]:
    coll = utils.fusion.as_object_collection(base.bodies)
    join_input = component.features.combineFeatures.createInput(combine.target_body, coll)
    join_input.operation = adsk.fusion.FeatureOperations.JoinFeatureOperation # type: ignore
    join_input.isKeepToolBodies = True
    join_feature = component.features.combineFeatures.add(join_input)
    intersect_input = component.features.combineFeatures.createInput(combine.target_body, coll)
    intersect_input.operation = adsk.fusion.FeatureOperations.IntersectFeatureOperation # type: ignore
    intersect_input.isKeepToolBodies = False
    intersect_feature = component.features.combineFeatures.add(intersect_input)
    return [join_feature, intersect_feature]
