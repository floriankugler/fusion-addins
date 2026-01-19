# DeriveFeature.errorOrWarningMessage Property

Parent Object: [DeriveFeature](DeriveFeature.md)  

## Description

Returns the error or warning message in the case where the healthState property returns either WarningFeatureHealthState or ErrorFeatureHealthState. Otherwise this property returns an empty string.

## Syntax

"deriveFeature_var" is a variable referencing a DeriveFeature object.  

```python
# Get the value of the property.
propertyValue = deriveFeature_var.errorOrWarningMessage
```

## Property Value

This is a read only property whose value is a string.

## Version

Introduced in version January 2026  

