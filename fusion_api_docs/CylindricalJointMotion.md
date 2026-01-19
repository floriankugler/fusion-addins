# CylindricalJointMotion Object

Derived from: [JointMotion](JointMotion.md) Object  

## Description

Represents the set of information specific to a cylindrical joint.

## Methods

| Name | Description |
|----|----|
| [classType](CylindricalJointMotion_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [customRotationAxisEntity](CylindricalJointMotion_customRotationAxisEntity.md) | This property can be set using various types of entities that can infer an axis. For example, a linear edge, sketch line, planar face, and cylindrical face. This property is only valid in the case where the rotationAxis property returns CustomJointDirection. Setting this property will automatically set the rotationAxis property to CustomJointDirection. To set this property, you need to position the timeline marker to immediately before this joint. This can be accomplished using the following code: thisJoint.timelineObject.rollTo(True) |
| [isValid](CylindricalJointMotion_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [jointType](CylindricalJointMotion_jointType.md) | Returns an enum value indicating the type of joint this joint represents. |
| [objectType](CylindricalJointMotion_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [rotationAxis](CylindricalJointMotion_rotationAxis.md) | Gets and sets the direction of the axis of rotation. This can be set to XAxisJointDirection, YAxisJointDirection, or ZAxisJointDirection. It can return those three directions and CustomJointDirection. If this returns CustomJointDirection then the customRotationAxisEntity will return an entity that defines the axis. If there is a custom rotation axis defined and this property is set to one of the three standard axes, the custom rotation will be removed and customRotationAxisEntity will return null. |
| [rotationAxisVector](CylindricalJointMotion_rotationAxisVector.md) | Returns the direction of the rotation axis. This property will return null in the case where the CylindricalJointMotion object was obtained from a JointInput object. |
| [rotationLimits](CylindricalJointMotion_rotationLimits.md) | Returns a JointLimits object that defines the rotation limits for this joint. Use the functionality of the returned JointLimits object to get, set, and modify the joint limits. |
| [rotationValue](CylindricalJointMotion_rotationValue.md) | Gets and sets the rotation value. This is in radians. Setting this value is the equivalent of using the Drive Joints command. |
| [slideLimits](CylindricalJointMotion_slideLimits.md) | Returns a JointLimits object that defines the slide limits for this joint. Use the functionality of the returned JointLimits object to get, set, and modify the joint limits. |
| [slideValue](CylindricalJointMotion_slideValue.md) | Gets and sets the slide value. This is in centimeters. Setting this value is the equivalent of using the Drive Joints command. |

## Samples

| Name | Description |
|----|----|
| [CylindricalJointMotion API Sample](CylindricalJointMotionSample_Sample.md) | Demonstrates creating a joint with cylindrical joint motion. |

## Version

Introduced in version July 2015  

