# JointInput.offset Property

Parent Object: [JointInput](JointInput.md)  

## Description

Specifies the offset between two input geometries. This is effectively the offset distance between the two planes defined by the primary and secondary axes of the input geometries. When a new JointInput object is created, this value defaults to zero. When the joint is created this will become the value of the parameter that controls the joint offset.  

When using a real value to define the offset, the value is in centimeters. When using a string the expression is evaluated using the document default units for distance.

## Syntax

"jointInput_var" is a variable referencing a JointInput object.  

```python
# Get the value of the property.
propertyValue = jointInput_var.offset

# Set the value of the property.
jointInput_var.offset = propertyValue
```

## Property Value

This is a read/write property whose value is a [ValueInput](ValueInput.md).

## Samples

| Name | Description |
|----|----|
| [Joint API Sample](JointSample_Sample.md) | Demonstrates creating a new joint. |
| [RevoluteJointMotion API Sample](RevoluteJointMotionSample_Sample.md) | Demonstrates creating a joint with revolute joint motion. |

## Version

Introduced in version July 2015  

