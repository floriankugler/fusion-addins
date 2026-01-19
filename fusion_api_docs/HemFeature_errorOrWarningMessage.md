# HemFeature.errorOrWarningMessage Property

Parent Object: [HemFeature](HemFeature.md)  

## Description

Returns the error or warning message in the case where the healthState property returns either WarningFeatureHealthState or ErrorFeatureHealthState. Otherwise this property returns an empty string.

## Syntax

"hemFeature_var" is a variable referencing a HemFeature object.  

```python
# Get the value of the property.
propertyValue = hemFeature_var.errorOrWarningMessage
```

## Property Value

This is a read only property whose value is a string.

## Version

Introduced in version September 2025  

