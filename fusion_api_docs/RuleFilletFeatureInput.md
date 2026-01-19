# RuleFilletFeatureInput Object

Derived from: [Base](Base.md) Object  

## Description

This class defines the methods and properties that pertain to the definition of a rule fillet feature.

## Methods

| Name | Description |
|----|----|
| [classType](RuleFilletFeatureInput_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [setAsymmetricOffsets](RuleFilletFeatureInput_setAsymmetricOffsets.md) | Sets the fillet to be an asymmetric fillet and defines the two offsets. |
| [setByAllEdges](RuleFilletFeatureInput_setByAllEdges.md) | Method that adds an array of BRepFace and/or Feature objects to have all their edges to be filleted. Calling this method will set ruleType to RuleFilletRuleTypes.AllEdgesRuleFilletRuleType. |
| [setByBetweenFacesOrFeatures](RuleFilletFeatureInput_setByBetweenFacesOrFeatures.md) | Method that adds two sets of BRepFace and/or Feature objects to have the edges between them filleted. Call this method will set ruleType to RuleFilletRuleTypes.BetweenFacesOrFeaturesRuleFilletRuleType. |

## Properties

| Name | Description |
| --- | --- |
| [asymmetricOffsetOne](RuleFilletFeatureInput_asymmetricOffsetOne.md) | Returns the current first offset for an asymmetric fillet. Use setAsymmetricOffsets to set the offsets. Returns null in the case where the fillet is a constant radius fillet. |
| [asymmetricOffsetTwo](RuleFilletFeatureInput_asymmetricOffsetTwo.md) | Returns the current second offset for an asymmetric fillet. Use setAsymmetricOffsets to set the offsets. Returns null in the case where the fillet is a constant radius fillet. |
| [facesOrFeatures](RuleFilletFeatureInput_facesOrFeatures.md) | Gets an array of BRepFace and/or Feature objects that are to have all their edges filleted. This is applicable only when ruleType is RuleFilletRuleTypes.AllEdgesRuleFilletRuleType. This is set by the setByAllEdges method. |
| [facesOrFeaturesOne](RuleFilletFeatureInput_facesOrFeaturesOne.md) | Gets the first array of BRepFace and/or Feature objects for between faces/features rule fillet. This is applicable only when ruleType is RuleFilletRuleTypes.BetweenFacesOrFeaturesRuleFilletRuleType. This is set by the setByBetweenFacesOrFeatures method. |
| [facesOrFeaturesTwo](RuleFilletFeatureInput_facesOrFeaturesTwo.md) | Gets the second array of BRepFace and/or Feature objects for between faces/features rule fillet. This is applicable only when ruleType is RuleFilletRuleTypes.BetweenFacesOrFeaturesRuleFilletRuleType. This is set by the setByBetweenFacesOrFeatures method. |
| [isRollingBallCorner](RuleFilletFeatureInput_isRollingBallCorner.md) | Gets and sets if a rolling ball or setback solution is to be used in any corners. A value of true will create a rolling ball fillet. |
| [isValid](RuleFilletFeatureInput_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](RuleFilletFeatureInput_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [radius](RuleFilletFeatureInput_radius.md) | Gets and sets the radius of the fillet. Setting this will set the fillet to a constant radius fillet and any asymmetric information will be lost. Returns null in the case the fillet is asymmetric. |
| [ruleType](RuleFilletFeatureInput_ruleType.md) | Gets the rule type for the rule fillet. |
| [targetBaseFeature](RuleFilletFeatureInput_targetBaseFeature.md) | When creating a feature that is owned by a base feature, set this property to the base feature you want to associate the new feature with. By default, this is null, meaning it will not be associated with a base feature. Because of a current limitation, if you want to create a feature associated with a base feature, you must set this property AND call the startEdit method of the base feature, create the feature, and then call the finishEdit method of the base feature. The base feature must be in an "edit" state to be able to add any additional items to it. |
| [topologyType](RuleFilletFeatureInput_topologyType.md) | Gets and sets the topology type of the rule fillet. |

## Accessed From

[FilletFeatures.createRuleFilletInput](FilletFeatures_createRuleFilletInput.md)

## Version

Introduced in version November 2025  

