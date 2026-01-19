# JointLimits.restValue Property

Parent Object: [JointLimits](JointLimits.md)  

## Description

The resting state value. This is in either centimeters or radians depending on if the joint value this is associated with defines a distance or an angle.

## Syntax

"jointLimits_var" is a variable referencing a JointLimits object.  

```python
# Get the value of the property.
propertyValue = jointLimits_var.restValue

# Set the value of the property.
jointLimits_var.restValue = propertyValue
```

## Property Value

This is a read/write property whose value is a double.

## Samples

| Name | Description |
|----|----|
| [BallJointMotion API Sample](BallJointMotionSample_Sample.md) | Demonstrates creating a joint with ball joint motion |
| [CylindricalJointMotion API Sample](CylindricalJointMotionSample_Sample.md) | Demonstrates creating a joint with cylindrical joint motion. |
| [Pin Slot Joint Motion API Sample](PinSlotJointMotionSample_Sample.md) | Demonstrates creating a joint with pin slot joint motion |
| [Planar Joint Motion API Sample](PlanarJointMotionSample_Sample.md) | Demonstrates creating a joint with planar joint motion |
| [SliderJointMotion API Sample](SliderJointMotionSample_Sample.md) | Demonstrates creating a joint with slider joint motion. |

## Version

Introduced in version July 2015  

