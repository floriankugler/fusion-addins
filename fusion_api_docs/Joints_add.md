# Joints.add Method

Parent Object: [Joints](Joints.md)  

## Description

Creates a new joint.

## Syntax

"joints_var" is a variable referencing a [Joints](Joints.md) object.

```python
returnValue = joints_var.add(input)
```

## Return Value

| Type | Description |
|----|----|
| [Joint](Joint.md) | Returns the newly created Joint or null in the case of failure. |

## Parameters

| Name | Type | Description |
|----|----|----|
| input | [JointInput](JointInput.md) | The JointInput object that defines the geometry and various inputs that fully define a joint. A JointInput object is created using the Joints.createInput method. |

## Samples

| Name | Description |
|----|----|
| [BallJointMotion API Sample](BallJointMotionSample_Sample.md) | Demonstrates creating a joint with ball joint motion |
| [CylindricalJointMotion API Sample](CylindricalJointMotionSample_Sample.md) | Demonstrates creating a joint with cylindrical joint motion. |
| [Joint API Sample](JointSample_Sample.md) | Demonstrates creating a new joint. |
| [Pin Slot Joint Motion API Sample](PinSlotJointMotionSample_Sample.md) | Demonstrates creating a joint with pin slot joint motion |
| [Planar Joint Motion API Sample](PlanarJointMotionSample_Sample.md) | Demonstrates creating a joint with planar joint motion |
| [RevoluteJointMotion API Sample](RevoluteJointMotionSample_Sample.md) | Demonstrates creating a joint with revolute joint motion. |
| [SliderJointMotion API Sample](SliderJointMotionSample_Sample.md) | Demonstrates creating a joint with slider joint motion. |

## Version

Introduced in version July 2015  

