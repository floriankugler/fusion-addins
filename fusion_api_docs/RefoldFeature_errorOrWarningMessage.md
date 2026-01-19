# RefoldFeature.errorOrWarningMessage Property

Parent Object: [RefoldFeature](RefoldFeature.md)  

## Description

Returns the error or warning message in the case where the healthState property returns either WarningFeatureHealthState or ErrorFeatureHealthState. Otherwise this property returns an empty string.

## Syntax

"refoldFeature_var" is a variable referencing a RefoldFeature object.  

```python
# Get the value of the property.
propertyValue = refoldFeature_var.errorOrWarningMessage
```

## Property Value

This is a read only property whose value is a string.

## Version

Introduced in version August 2020  

