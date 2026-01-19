# JointLimits.maximumValue Property

Parent Object: [JointLimits](JointLimits.md)  

## Description

The maximum value of the value. This is in either centimeters or radians depending on if the joint value this is associated with defines a distance or an angle.

## Syntax

"jointLimits_var" is a variable referencing a JointLimits object.  

```python
# Get the value of the property.
propertyValue = jointLimits_var.maximumValue

# Set the value of the property.
jointLimits_var.maximumValue = propertyValue
```

## Property Value

This is a read/write property whose value is a double.

## Samples

| Name | Description |
|----|----|
| [RevoluteJointMotion API Sample](RevoluteJointMotionSample_Sample.md) | Demonstrates creating a joint with revolute joint motion. |

## Version

Introduced in version July 2015  

