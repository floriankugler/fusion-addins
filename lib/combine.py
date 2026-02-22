from typing import cast
import adsk.core, adsk.fusion
from dataclasses import dataclass
from enum import Enum
from . import utils

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
        if self.target_body != op.target_body:
            raise ValueError("Cannot merge combine operations with different target bodies.")
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


_base_target_attribute_group_name = 'target-body-token'
_base_target_attribute_value_name = 'value'

def create_features_from_combines(component: adsk.fusion.Component, combines: list[Combine], feature: adsk.fusion.CustomFeature | None, is_compute: bool) -> tuple[list[adsk.fusion.Feature], list[adsk.fusion.Feature], list[adsk.fusion.BRepBody]]:
    mgr = adsk.fusion.TemporaryBRepManager.get()
    external_combine_key = lambda idx, op: f"external-combine-{idx}-{op}"

    combines_inside_component, combines_outside_component = _TargetCombine.aggregate_combines(combines, component)
    all_combines = combines_inside_component | combines_outside_component
    dependencies = [c.target_body for c in all_combines.values()]

    existing_inside_features: list[tuple[adsk.fusion.BaseFeature, adsk.fusion.CombineFeature, adsk.fusion.CombineFeature]] = []
    existing_outside_features: list[tuple[adsk.fusion.BaseFeature, adsk.fusion.CombineFeature, adsk.fusion.CombineFeature]] = []
    existing_targets: set[str] = set()
    targets_to_delete: list[tuple[adsk.fusion.BaseFeature, adsk.fusion.CombineFeature, adsk.fusion.CombineFeature]] = []
    
    if feature:
        existing_features = cast(list[adsk.fusion.Feature], list(feature.features))
        internal_idx = 0
        while internal_idx < len(existing_features) and isinstance(existing_features[internal_idx], adsk.fusion.BaseFeature):
            base = cast(adsk.fusion.BaseFeature, existing_features[internal_idx])
            base = base.nativeObject or base
            join = cast(adsk.fusion.CombineFeature, existing_features[internal_idx + 1])
            join = join.nativeObject or join
            intersect = cast(adsk.fusion.CombineFeature, existing_features[internal_idx + 2])
            intersect = intersect.nativeObject or intersect
            existing_inside_features.append((base, join, intersect))
            internal_idx += 3

        external_idx = 0
        while True:
            base_token = feature.customNamedValues.value(external_combine_key(external_idx, 'base'))
            join_token = feature.customNamedValues.value(external_combine_key(external_idx, 'join'))
            intersect_token = feature.customNamedValues.value(external_combine_key(external_idx, 'intersect'))
            if not base_token or not join_token or not intersect_token:
                break
            bases = component.parentDesign.findEntityByToken(base_token)
            joins = component.parentDesign.findEntityByToken(join_token)
            intersects = component.parentDesign.findEntityByToken(intersect_token)
            if bases and joins and intersects:
                base = cast(adsk.fusion.BaseFeature, bases[0])
                join = cast(adsk.fusion.CombineFeature, joins[0])
                intersect = cast(adsk.fusion.CombineFeature, intersects[0])
                existing_outside_features.append((base, join, intersect))
            external_idx += 1
        
        for base, join, intersect in existing_inside_features + existing_outside_features:
            target_token = base.attributes.itemByName(_base_target_attribute_group_name, _base_target_attribute_value_name).value
            targets = component.parentDesign.findEntityByToken(target_token)
            if targets:
                target = cast(adsk.fusion.BRepBody, targets[0])
                token = target.entityToken
                if token in all_combines:
                    existing_targets.add(token)
                    new_body = all_combines[token].new_body
                    base.startEdit()
                    base.updateBody(base.bodies[0], new_body)
                    base.finishEdit()
                    base.attributes.add(_base_target_attribute_group_name, _base_target_attribute_value_name, token)
                else:
                    targets_to_delete.append((base, join, intersect))
            else:
                targets_to_delete.append((base, join, intersect))

    new_combines_inside_component = [ v for k, v in combines_inside_component.items() if not k in existing_targets ]
    new_combines_outside_component = [ v for k, v in combines_outside_component.items() if not k in existing_targets]

    if is_compute:
        assert not new_combines_inside_component
        assert not new_combines_outside_component
        features_inside = cast(list[adsk.fusion.Feature], [f for triplet in existing_inside_features for f in triplet])
        features_outside = cast(list[adsk.fusion.Feature], [f for triplet in existing_outside_features for f in triplet])
        return features_inside, features_outside, dependencies

    if feature:
        feature.timelineObject.rollTo(True)
        feature.setStartAndEndFeatures(None, None) # type: ignore

        for base, join, intersect in targets_to_delete:
            if (base, join, intersect) in existing_inside_features:
                existing_inside_features.remove((base, join, intersect)) 
            elif (base, join, intersect) in existing_outside_features:
                existing_outside_features.remove((base, join, intersect))
            intersect.deleteMe()
            join.deleteMe()
            base.deleteMe()

    if existing_inside_features:
        existing_inside_features[-1][2].timelineObject.rollTo(False)
    elif feature:
        feature.timelineObject.rollTo(False)
    
    new_inside_features: list[tuple[adsk.fusion.BaseFeature, adsk.fusion.CombineFeature, adsk.fusion.CombineFeature]] = []
    for combine in new_combines_inside_component:
        new_inside_features.append(_create_combine_triplet(combine, component))

    new_outside_features: list[tuple[adsk.fusion.BaseFeature, adsk.fusion.CombineFeature, adsk.fusion.CombineFeature]] = []
    for combine in new_combines_outside_component:
        outside_comp = combine.target_body.parentComponent
        new_outside_features.append(_create_combine_triplet(combine, outside_comp))

    if feature:
        _register_external_features(new_outside_features + existing_outside_features, component.parentDesign, feature)

    for idx, (base, join, intersect) in enumerate(existing_outside_features + new_outside_features):
        id = f"custom-feature<{feature.name if feature else "<unknown>"}>-{idx}"
        base.name = f"{id}-base"
        join.name = f"{id}-join"
        intersect.name = f"{id}-intersect"
        if feature:
            feature.customNamedValues.addOrSetValue(external_combine_key(idx, 'base'), base.entityToken)
            feature.customNamedValues.addOrSetValue(external_combine_key(idx, 'join'), join.entityToken)
            feature.customNamedValues.addOrSetValue(external_combine_key(idx, 'intersect'), intersect.entityToken)

    features_inside = cast(list[adsk.fusion.Feature], [f for triplet in existing_inside_features + new_inside_features for f in triplet])
    features_outside = cast(list[adsk.fusion.Feature], [f for triplet in new_outside_features + existing_outside_features for f in triplet])
    return cast(list[adsk.fusion.Feature], features_inside), cast(list[adsk.fusion.Feature], features_outside), dependencies

def _create_combine_triplet(combine: _TargetCombine, component: adsk.fusion.Component) -> tuple[adsk.fusion.BaseFeature, adsk.fusion.CombineFeature, adsk.fusion.CombineFeature]:
    base = component.features.baseFeatures.add()
    base.startEdit()
    new_body = combine.new_body
    ac = combine.target_body.assemblyContext
    if ac and not ac.transform2.isEqualTo(adsk.core.Matrix3D.create()):
        new_body = utils.brep.transformed(new_body, utils.matrix.inverted_matrix(ac.transform2))
    component.bRepBodies.add(new_body, base)
    base.attributes.add(_base_target_attribute_group_name, _base_target_attribute_value_name, combine.target_body.entityToken)
    base.finishEdit()

    coll = utils.fusion.as_object_collection(base.bodies)
    join_input = component.features.combineFeatures.createInput(combine.target_body, coll)
    join_input.operation = adsk.fusion.FeatureOperations.JoinFeatureOperation # type: ignore
    join_input.isKeepToolBodies = True
    join = component.features.combineFeatures.add(join_input)
    intersect_input = component.features.combineFeatures.createInput(combine.target_body, coll)
    intersect_input.operation = adsk.fusion.FeatureOperations.IntersectFeatureOperation # type: ignore
    intersect_input.isKeepToolBodies = False
    intersect = component.features.combineFeatures.add(intersect_input)
    return (base, join, intersect)

def _register_external_features(external_features: list[tuple[adsk.fusion.BaseFeature, adsk.fusion.CombineFeature, adsk.fusion.CombineFeature]], design: adsk.fusion.Design, feature: adsk.fusion.CustomFeature):
    garbage_collect_features(design)
    for base, join, intersect in external_features:
        design.attributes.add('external-base-features', base.entityToken, feature.entityToken)
        design.attributes.add('external-join-features', join.entityToken, feature.entityToken)
        design.attributes.add('external-intersect-features', intersect.entityToken, feature.entityToken)

def garbage_collect_features(design: adsk.fusion.Design):
    _garbage_collect_attributes(design, design.attributes.itemsByGroup('external-intersect-features'))
    _garbage_collect_attributes(design, design.attributes.itemsByGroup('external-join-features'))
    _garbage_collect_attributes(design, design.attributes.itemsByGroup('external-base-features'))

def _garbage_collect_attributes(design: adsk.fusion.Design, attributes: list[adsk.core.Attribute]):
    for att in attributes:
        external_feature_token = att.name
        parent_feature_token = att.value
        external_feature = design.findEntityByToken(external_feature_token)
        parent_feature = design.findEntityByToken(parent_feature_token)
        if not external_feature or not parent_feature:
            if external_feature:
                cast(adsk.fusion.Feature, external_feature[0]).deleteMe()
            att.deleteMe()

