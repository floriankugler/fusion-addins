# BallJointMotion Object

Derived from: [JointMotion](JointMotion.md) Object  

## Description

Represents the set of information specific to a ball joint.

## Methods

| Name | Description |
|----|----|
| [classType](BallJointMotion_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [customPitchDirectionEntity](BallJointMotion_customPitchDirectionEntity.md) | This property defines a custom pitch direction and can be set using various types of entities that can infer a direction. For example, a linear edge, sketch line, planar face, and cylindrical face.This property is only valid in the case where the pitchDirection property returns CustomJointDirection. Setting this property will automatically set the pitchDirection property to CustomJointDirection. To set this property, you need to position the timeline marker to immediately before this joint. This can be accomplished using the following code: thisJoint.timelineObject.rollTo(True) |
| [customYawDirectionEntity](BallJointMotion_customYawDirectionEntity.md) | This property defines a custom yaw direction and can be set using various types of entities that can infer a direction. For example, a linear edge, sketch line, planar face, and cylindrical face.This property is only valid in the case where the yawDirection property returns CustomJointDirection. Setting this property will automatically set the yawDirection property to CustomJointDirection. To set this property, you need to position the timeline marker to immediately before this joint. This can be accomplished using the following code: thisJoint.timelineObject.rollTo(True) |
| [isValid](BallJointMotion_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [jointType](BallJointMotion_jointType.md) | Returns an enum value indicating the type of joint this joint represents. |
| [objectType](BallJointMotion_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [pitchDirection](BallJointMotion_pitchDirection.md) | Gets and sets the direction that the pitch is measured from. This can only be set to ZAxisJointDirection and can return ZAxisJointDirection or CustomJointDirection. If this returns CustomJointDirection then the customNormalDirectionEntity will return an entity that defines the direction. If there is a custom direction defined and this property is set to ZAxisJointDirection, the custom direction will be removed and customNormalDirectionEntity will return null. |
| [pitchDirectionVector](BallJointMotion_pitchDirectionVector.md) | Returns the direction that the pitch angle is measured from. This property will return null in the case where the BallJointMotion object was obtained from a JointInput object. |
| [pitchLimits](BallJointMotion_pitchLimits.md) | Returns a JointLimits object that defines the limits of rotation for the pitch. Use the functionality of the returned JointLimits object to get, set, and modify the joint limits. |
| [pitchValue](BallJointMotion_pitchValue.md) | Gets and sets the pitch value. This is in radians. Setting this value is the equivalent of using the Drive Joints command. |
| [rollDirectionVector](BallJointMotion_rollDirectionVector.md) | Returns the direction that the roll angle is measured from. This property will return null in the case where the BallJointMotion object was obtained from a JointInput object. |
| [rollLimits](BallJointMotion_rollLimits.md) | Returns a JointLimits object that defines the limits of rotation for the roll. Use the functionality of the returned JointLimits object to get, set, and modify the joint limits. |
| [rollValue](BallJointMotion_rollValue.md) | Gets and sets the roll value. This is in radians. Setting this value is the equivalent of using the Drive Joints command. |
| [yawDirection](BallJointMotion_yawDirection.md) | Gets and sets the direction that the pitch is measured from. This can only be set to XAxisJointDirection and can return XAxisJointDirection or CustomJointDirection. If this returns CustomJointDirection then the customYawDirectionEntity will return an entity that defines the direction. If there is a custom direction defined and this property is set to XAxisJointDirection, the custom direction will be removed and customYawDirectionEntity will return null. |
| [yawDirectionVector](BallJointMotion_yawDirectionVector.md) | Returns the direction that the yaw angle is measured from. This property will return null in the case where the BallJointMotion object was obtained from a JointInput object. |
| [yawLimits](BallJointMotion_yawLimits.md) | Returns a JointLimits object that defines the limits of rotation for the yaw. Use the functionality of the returned JointLimits object to get, set, and modify the joint limits. |
| [yawValue](BallJointMotion_yawValue.md) | Gets and sets the yaw value. This is in radians. Setting this value is the equivalent of using the Drive Joints command. |

## Samples

| Name | Description |
|----|----|
| [BallJointMotion API Sample](BallJointMotionSample_Sample.md) | Demonstrates creating a joint with ball joint motion |

## Version

Introduced in version July 2015  

