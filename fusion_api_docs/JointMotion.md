# JointMotion Object

Derived from: [Base](Base.md) Object  

## Description

The base class for the classes that represent all of the various joint types.

## Methods

| Name | Description |
|----|----|
| [classType](JointMotion_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [isValid](JointMotion_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [jointType](JointMotion_jointType.md) | Returns an enum value indicating the type of joint this joint represents. |
| [objectType](JointMotion_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[AsBuiltJoint.jointMotion](AsBuiltJoint_jointMotion.md), [AsBuiltJointInput.jointMotion](AsBuiltJointInput_jointMotion.md), [Joint.jointMotion](Joint_jointMotion.md), [JointInput.jointMotion](JointInput_jointMotion.md)

## Derived Classes

[BallJointMotion](BallJointMotion.md), [CylindricalJointMotion](CylindricalJointMotion.md), [PinSlotJointMotion](PinSlotJointMotion.md), [PlanarJointMotion](PlanarJointMotion.md), [RevoluteJointMotion](RevoluteJointMotion.md), [RigidJointMotion](RigidJointMotion.md), [SliderJointMotion](SliderJointMotion.md)

## Version

Introduced in version July 2015  

