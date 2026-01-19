# FlatPattern.errorOrWarningMessage Property

Parent Object: [FlatPattern](FlatPattern.md)  

## Description

Returns the error or warning message in the case where the healthState property returns either WarningFeatureHealthState or ErrorFeatureHealthState. Otherwise this property returns an empty string.

## Syntax

"flatPattern_var" is a variable referencing a FlatPattern object.  

```python
# Get the value of the property.
propertyValue = flatPattern_var.errorOrWarningMessage
```

## Property Value

This is a read only property whose value is a string.

## Version

Introduced in version October 2022  

