# FilletFeature.ruleFilletSettings Property

Parent Object: [FilletFeature](FilletFeature.md)  

## Description

Gets the RuleFilletSettings object for the rule fillet.  

This is valid only when the filletFeatureType is FilletFeatureTypes.RuleFilletFeatureType, otherwise this returns null.

## Syntax

"filletFeature_var" is a variable referencing a FilletFeature object.  

```python
# Get the value of the property.
propertyValue = filletFeature_var.ruleFilletSettings
```

## Property Value

This is a read only property whose value is a [RuleFilletSettings](RuleFilletSettings.md).

## Version

Introduced in version November 2025  

