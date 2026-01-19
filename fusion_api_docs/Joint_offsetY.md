# Joint.offsetY Property

Parent Object: [Joint](Joint.md)  

## Description

Returns the parameter controlling the offset along the primary axis (y axis) of the joint. To edit this value, get the parameter and use one of its properties to edit the value.  

This property will return null in the case where the jointType property returns InferredJointType.

## Syntax

"joint_var" is a variable referencing a Joint object.  

```python
# Get the value of the property.
propertyValue = joint_var.offsetY
```

## Property Value

This is a read only property whose value is a [ModelParameter](ModelParameter.md).

## Version

Introduced in version September 2022  

