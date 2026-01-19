# FlangeFeature.errorOrWarningMessage Property

Parent Object: [FlangeFeature](FlangeFeature.md)  

## Description

Returns the error or warning message in the case where the healthState property returns either WarningFeatureHealthState or ErrorFeatureHealthState. Otherwise this property returns an empty string.

## Syntax

"flangeFeature_var" is a variable referencing a FlangeFeature object.  

```python
# Get the value of the property.
propertyValue = flangeFeature_var.errorOrWarningMessage
```

## Property Value

This is a read only property whose value is a string.

## Version

Introduced in version August 2020  

