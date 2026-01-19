# RuleFilletSettings.facesOrFeaturesOne Property

Parent Object: [RuleFilletSettings](RuleFilletSettings.md)  

## Description

Gets the first array of BRepFace and/or Feature objects for between faces/features rule fillet. This returns an empty array if ruleType is not RuleFilletRuleTypes.BetweenFacesOrFeaturesRuleFilletRuleType.  

To use this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True).

## Syntax

"ruleFilletSettings_var" is a variable referencing a RuleFilletSettings object.  

```python
# Get the value of the property.
propertyValue = ruleFilletSettings_var.facesOrFeaturesOne
```

## Property Value

This is a read only property whose value is an array of type [Base](Base.md).

## Version

Introduced in version November 2025  

