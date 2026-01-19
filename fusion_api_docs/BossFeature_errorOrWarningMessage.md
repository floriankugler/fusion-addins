# BossFeature.errorOrWarningMessage Property

Parent Object: [BossFeature](BossFeature.md)  

## Description

Returns the error or warning message in the case where the healthState property returns either WarningFeatureHealthState or ErrorFeatureHealthState. Otherwise this property returns an empty string.

## Syntax

"bossFeature_var" is a variable referencing a BossFeature object.  

```python
# Get the value of the property.
propertyValue = bossFeature_var.errorOrWarningMessage
```

## Property Value

This is a read only property whose value is a string.

## Version

Introduced in version October 2022  

