# RipFeature.errorOrWarningMessage Property

Parent Object: [RipFeature](RipFeature.md)  

## Description

Returns the error or warning message in the case where the healthState property returns either WarningFeatureHealthState or ErrorFeatureHealthState. Otherwise this property returns an empty string.

## Syntax

"ripFeature_var" is a variable referencing a RipFeature object.  

```python
# Get the value of the property.
propertyValue = ripFeature_var.errorOrWarningMessage
```

## Property Value

This is a read only property whose value is a string.

## Version

Introduced in version September 2023  

