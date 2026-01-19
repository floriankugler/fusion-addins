# TrimFeature.errorOrWarningMessage Property

Parent Object: [TrimFeature](TrimFeature.md)  

## Description

Returns the error or warning message in the case where the healthState property returns either WarningFeatureHealthState or ErrorFeatureHealthState. Otherwise this property returns an empty string.

## Syntax

"trimFeature_var" is a variable referencing a TrimFeature object.  

```python
# Get the value of the property.
propertyValue = trimFeature_var.errorOrWarningMessage
```

## Property Value

This is a read only property whose value is a string.

## Version

Introduced in version July 2016  

