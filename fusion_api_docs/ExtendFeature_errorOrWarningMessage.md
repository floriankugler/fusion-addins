# ExtendFeature.errorOrWarningMessage Property

Parent Object: [ExtendFeature](ExtendFeature.md)  

## Description

Returns the error or warning message in the case where the healthState property returns either WarningFeatureHealthState or ErrorFeatureHealthState. Otherwise this property returns an empty string.

## Syntax

"extendFeature_var" is a variable referencing an ExtendFeature object.  

```python
# Get the value of the property.
propertyValue = extendFeature_var.errorOrWarningMessage
```

## Property Value

This is a read only property whose value is a string.

## Version

Introduced in version July 2016  

