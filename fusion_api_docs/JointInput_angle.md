# JointInput.angle Property

Parent Object: [JointInput](JointInput.md)  

## Description

Specifies the angle between two input geometries. This is effectively the angle between the two primary axes of the input geometries. When a new JointInput object is created, this value defaults to zero. When the joint is created this will become the value of the parameter that controls the joint angle.  

When using a real value to define the angle, the value is in radians. When using a string the expression is evaluated using the document default units for angles.

## Syntax

"jointInput_var" is a variable referencing a JointInput object.  

```python
# Get the value of the property.
propertyValue = jointInput_var.angle

# Set the value of the property.
jointInput_var.angle = propertyValue
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

