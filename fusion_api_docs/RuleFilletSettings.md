# RuleFilletSettings Object

Derived from: [Base](Base.md) Object  

## Description

The settings for the rule fillet feature.

## Methods

| Name | Description |
|----|----|
| [classType](RuleFilletSettings_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [setByAllEdges](RuleFilletSettings_setByAllEdges.md) | Method that adds an array of BRepFace and/or Feature objects to have all their edges filleted. Calling this method will set ruleType to RuleFilletRuleTypes.AllEdgesRuleFilletRuleType. |
| [setByBetweenFacesOrFeatures](RuleFilletSettings_setByBetweenFacesOrFeatures.md) | Method that adds two sets of BRepFace and/or Feature objects to have the edges between them filleted. Call this method will set ruleType to RuleFilletRuleTypes.BetweenFacesOrFeaturesRuleFilletRuleType. |
| [setToAsymmetric](RuleFilletSettings_setToAsymmetric.md) | Changes the radius type to be asymmetric. |
| [setToConstantRadius](RuleFilletSettings_setToConstantRadius.md) | Changes the radius type to be constant. |

## Properties

| Name | Description |
| --- | --- |
| [asymmetricOffsetOne](RuleFilletSettings_asymmetricOffsetOne.md) | Gets the parameter controlling the first offset of this asymmetric rule fillet. This property will return null when isConstantRadius is true. To edit the offset, use properties on the parameter to change the value of the parameter. |
| [asymmetricOffsetTwo](RuleFilletSettings_asymmetricOffsetTwo.md) | Gets the parameter controlling the second offset of this asymmetric rule fillet. This property will return null when isConstantRadius is true. To edit the offset, use properties on the parameter to change the value of the parameter. |
| [facesOrFeatures](RuleFilletSettings_facesOrFeatures.md) | Gets an array of BRepFace and/or Feature objects that have all their edges filleted. This returns an empty array if ruleType is not RuleFilletRuleTypes.AllEdgesRuleFilletRuleType. To use this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True). |
| [facesOrFeaturesOne](RuleFilletSettings_facesOrFeaturesOne.md) | Gets the first array of BRepFace and/or Feature objects for between faces/features rule fillet. This returns an empty array if ruleType is not RuleFilletRuleTypes.BetweenFacesOrFeaturesRuleFilletRuleType. To use this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True). |
| [facesOrFeaturesTwo](RuleFilletSettings_facesOrFeaturesTwo.md) | Gets the second array of BRepFace and/or Feature objects for between faces/features rule fillet. This returns an empty array if ruleType is not RuleFilletRuleTypes.BetweenFacesOrFeaturesRuleFilletRuleType. To use this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True). |
| [isConstantRadius](RuleFilletSettings_isConstantRadius.md) | Gets and sets if the rule fillet is a constant or asymmetric radius type. |
| [isValid](RuleFilletSettings_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](RuleFilletSettings_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [radius](RuleFilletSettings_radius.md) | Gets the parameter controlling the radius of a constant radius rule fillet. This property will return null when isConstantRadius is false. To edit the radius, use properties on the parameter to change the value of the parameter. |
| [ruleType](RuleFilletSettings_ruleType.md) | Gets the rule type for the rule fillet. |
| [topologyType](RuleFilletSettings_topologyType.md) | Gets and sets the topology type of the rule fillet. To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True). |

## Accessed From

[FilletFeature.ruleFilletSettings](FilletFeature_ruleFilletSettings.md)

## Version

Introduced in version November 2025  

