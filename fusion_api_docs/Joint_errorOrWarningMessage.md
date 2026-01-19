# Joint.errorOrWarningMessage Property

Parent Object: [Joint](Joint.md)  

## Description

Returns the error or warning message in the case where the healthState property returns either WarningFeatureHealthState or ErrorFeatureHealthState. Otherwise this property returns an empty string.

## Syntax

"joint_var" is a variable referencing a Joint object.  

```python
# Get the value of the property.
propertyValue = joint_var.errorOrWarningMessage
```

## Property Value

This is a read only property whose value is a string.

## Samples

| Name | Description |
|----|----|
| [Joint API Sample](JointSample_Sample.md) | Demonstrates creating a new joint. |

## Version

Introduced in version July 2016  

