# JointInput.isFlipped Property

Parent Object: [JointInput](JointInput.md)  

## Description

Gets and sets if the joint direction is flipped or not. This is effectively specifying if the third axis of the two input geometries is facing (false) or opposed (true).

## Syntax

"jointInput_var" is a variable referencing a JointInput object.  

```python
# Get the value of the property.
propertyValue = jointInput_var.isFlipped

# Set the value of the property.
jointInput_var.isFlipped = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Samples

| Name | Description |
|----|----|
| [Joint API Sample](JointSample_Sample.md) | Demonstrates creating a new joint. |
| [RevoluteJointMotion API Sample](RevoluteJointMotionSample_Sample.md) | Demonstrates creating a joint with revolute joint motion. |

## Version

Introduced in version July 2015  

