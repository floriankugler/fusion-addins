# JointLimits Object

Derived from: [Base](Base.md) Object  

## Description

Used to define limits for the range of motion of a joint.

## Methods

| Name | Description |
|----|----|
| [classType](JointLimits_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [isMaximumValueEnabled](JointLimits_isMaximumValueEnabled.md) | Gets and sets whether the maximum joint limit is enabled or not. |
| [isMinimumValueEnabled](JointLimits_isMinimumValueEnabled.md) | Gets and sets whether the minimum joint limit is enabled or not. |
| [isRestValueEnabled](JointLimits_isRestValueEnabled.md) | Gets and sets whether the resting joint value is enabled or not. |
| [isValid](JointLimits_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [maximumValue](JointLimits_maximumValue.md) | The maximum value of the value. This is in either centimeters or radians depending on if the joint value this is associated with defines a distance or an angle. |
| [minimumValue](JointLimits_minimumValue.md) | The minimum value of the value. This is in either centimeters or radians depending on if the joint value this is associated with defines a distance or an angle. |
| [objectType](JointLimits_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [restValue](JointLimits_restValue.md) | The resting state value. This is in either centimeters or radians depending on if the joint value this is associated with defines a distance or an angle. |

## Accessed From

[BallJointMotion.pitchLimits](BallJointMotion_pitchLimits.md), [BallJointMotion.rollLimits](BallJointMotion_rollLimits.md), [BallJointMotion.yawLimits](BallJointMotion_yawLimits.md), [CylindricalJointMotion.rotationLimits](CylindricalJointMotion_rotationLimits.md), [CylindricalJointMotion.slideLimits](CylindricalJointMotion_slideLimits.md), [PinSlotJointMotion.rotationLimits](PinSlotJointMotion_rotationLimits.md), [PinSlotJointMotion.slideLimits](PinSlotJointMotion_slideLimits.md), [PlanarJointMotion.primarySlideLimits](PlanarJointMotion_primarySlideLimits.md), [PlanarJointMotion.rotationLimits](PlanarJointMotion_rotationLimits.md), [PlanarJointMotion.secondarySlideLimits](PlanarJointMotion_secondarySlideLimits.md), [RevoluteJointMotion.rotationLimits](RevoluteJointMotion_rotationLimits.md), [SliderJointMotion.slideLimits](SliderJointMotion_slideLimits.md)

## Samples

| Name | Description |
|----|----|
| [BallJointMotion API Sample](BallJointMotionSample_Sample.md) | Demonstrates creating a joint with ball joint motion |
| [CylindricalJointMotion API Sample](CylindricalJointMotionSample_Sample.md) | Demonstrates creating a joint with cylindrical joint motion. |
| [Pin Slot Joint Motion API Sample](PinSlotJointMotionSample_Sample.md) | Demonstrates creating a joint with pin slot joint motion |
| [Planar Joint Motion API Sample](PlanarJointMotionSample_Sample.md) | Demonstrates creating a joint with planar joint motion |
| [RevoluteJointMotion API Sample](RevoluteJointMotionSample_Sample.md) | Demonstrates creating a joint with revolute joint motion. |
| [SliderJointMotion API Sample](SliderJointMotionSample_Sample.md) | Demonstrates creating a joint with slider joint motion. |

## Version

Introduced in version July 2015  

