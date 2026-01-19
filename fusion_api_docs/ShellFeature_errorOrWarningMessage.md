# ShellFeature.errorOrWarningMessage Property

Parent Object: [ShellFeature](ShellFeature.md)  

## Description

Returns the error or warning message in the case where the healthState property returns either WarningFeatureHealthState or ErrorFeatureHealthState. Otherwise this property returns an empty string.

## Syntax

"shellFeature_var" is a variable referencing a ShellFeature object.  

```python
# Get the value of the property.
propertyValue = shellFeature_var.errorOrWarningMessage
```

## Property Value

This is a read only property whose value is a string.

## Version

Introduced in version July 2016  

