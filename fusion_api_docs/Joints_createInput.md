# Joints.createInput Method

Parent Object: [Joints](Joints.md)  

## Description

Creates a JointInput object, which is the API equivalent to the Joint command dialog. You you use methods and properties on the returned class to set the desired options, similar to providing input and setting options in the Joint command dialog. Once the settings are defined you call the Joints.add method passing in the JointInput object to create the actual joint.

## Syntax

"joints_var" is a variable referencing a [Joints](Joints.md) object.

```python
returnValue = joints_var.createInput(geometryOrOriginOne, geometryOrOriginTwo)
```

## Return Value

| Type | Description |
|----|----|
| [JointInput](JointInput.md) | Returns the JointInput object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| geometryOrOriginOne | [Base](Base.md) | A JointGeometry or JointOrigin object that defines the first set of geometry of the joint. JointGeometry objects are created by using the various static methods on the JointGeometry class and JointOrigin objects are created through the JointOrigins object. |
| geometryOrOriginTwo | [Base](Base.md) | A JointGeometry or JointOrigin object that defines the second set of geometry of the joint. JointGeometry objects are created by using the various static methods on the JointGeometry class and JointOrigin objects are created through the JointOrigins object. |

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

