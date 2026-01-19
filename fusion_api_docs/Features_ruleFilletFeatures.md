# Features.ruleFilletFeatures Property

Parent Object: [Features](Features.md)  

## Description

This function is retired. See more information in the 'Remarks' section below.  

Returns the collection that provides access to the existing rule fillet features.

## Remarks

This property is obsolete. You should use the Features.FilletFeatures to access all types of fillet features. The FilletFeature.filletFeatureType can be used to determine if a FilletFeature is a rule fillet feature or not.

## Syntax

"features_var" is a variable referencing a Features object.  

```python
# Get the value of the property.
propertyValue = features_var.ruleFilletFeatures
```

## Property Value

This is a read only property whose value is a [RuleFilletFeatures](RuleFilletFeatures.md).

## Version

Introduced in version September 2015  
Retired in version November 2025  

