# Joint.offset Property

Parent Object: [Joint](Joint.md)  

## Description

Returns the parameter controlling the offset between the two input geometries. This is effectively the offset distance between the two planes defined by the primary and secondary axes of the input geometries or the offset along the tertiary axis (z axis) of the joint.  

This property will return null in the case where the jointType property returns InferredJointType.

## Syntax

"joint_var" is a variable referencing a Joint object.  

```python
# Get the value of the property.
propertyValue = joint_var.offset
```

## Property Value

This is a read only property whose value is a [ModelParameter](ModelParameter.md).

## Version

Introduced in version July 2015  

