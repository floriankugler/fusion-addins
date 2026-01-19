# Joint.angle Property

Parent Object: [Joint](Joint.md)  

## Description

Returns the parameter controlling the angle between the two input geometries. This is effectively the angle between the two primary axes of the two joint geometries.  

This property will return null in the case where the jointType property returns InferredJointType.

## Syntax

"joint_var" is a variable referencing a Joint object.  

```python
# Get the value of the property.
propertyValue = joint_var.angle
```

## Property Value

This is a read only property whose value is a [ModelParameter](ModelParameter.md).

## Version

Introduced in version July 2015  

