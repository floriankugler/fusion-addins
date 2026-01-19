# MotionLinkInput Object

Derived from: [Base](Base.md) Object  

## Description

Defines all of the information required to create a new MotionLink. This object provides equivalent functionality to the MotionLink command dialog in that it gathers the required information to create a MotionLink.

## Methods

| Name | Description |
|----|----|
| [classType](MotionLinkInput_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [isReversed](MotionLinkInput_isReversed.md) | Gets and sets whether the direction of the motion is reversed or not. |
| [isValid](MotionLinkInput_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [jointOne](MotionLinkInput_jointOne.md) | Gets and sets the first Joint or AsBuiltJoint for this MotionLink. When you link two motions from the same joint, a valid joint should have its joint motion type of BallJointType, CylindricalJointType, PinSlotJointType or PlanarJointType. A joint whose joint motion is a RigidJointMotion type is never valid as the first joint.. |
| [jointTwo](MotionLinkInput_jointTwo.md) | Gets and sets the second Joint or AsBuiltJoint for this MotionLink. This can be a joint or null, when this is set to null then the two motions are from the same joint specified by jointOne. A joint whose joint motion is a RigidJointMotion type is never valid as the second joint. |
| [motionOne](MotionLinkInput_motionOne.md) | Gets and sets the first motion type. |
| [motionTwo](MotionLinkInput_motionTwo.md) | Gets and sets the second motion type. |
| [objectType](MotionLinkInput_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [valueOne](MotionLinkInput_valueOne.md) | Gets and sets the first motion link value. If the ValueInput uses a real then it is interpreted as centimeters for length and radians for angle. If it is a string then the units can be defined as part of the string (i.e. "2 in" or "60 deg") or if no units are specified it is interpreted using the current default units for length or angle. |
| [valueTwo](MotionLinkInput_valueTwo.md) | Gets and sets the second motion link value. If the ValueInput uses a real then it is interpreted as centimeters for length and radians for angle. If it is a string then the units can be defined as part of the string (i.e. "2 in" or "60 deg") or if no units are specified it is interpreted using the current default units for length or angle. |

## Accessed From

[MotionLinks.createInput](MotionLinks_createInput.md)

## Version

Introduced in version November 2025  

