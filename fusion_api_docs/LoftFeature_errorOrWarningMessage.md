# LoftFeature.errorOrWarningMessage Property

Parent Object: [LoftFeature](LoftFeature.md)  

## Description

Returns the error or warning message in the case where the healthState property returns either WarningFeatureHealthState or ErrorFeatureHealthState. Otherwise this property returns an empty string.

## Syntax

"loftFeature_var" is a variable referencing a LoftFeature object.  

```python
# Get the value of the property.
propertyValue = loftFeature_var.errorOrWarningMessage
```

## Property Value

This is a read only property whose value is a string.

## Version

Introduced in version July 2016  

