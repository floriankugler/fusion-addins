# AsBuiltJointInput Object

Derived from: [Base](Base.md) Object  

## Description

Defines all of the information needed to create an as-built joint.

## Methods

| Name | Description |
|----|----|
| [classType](AsBuiltJointInput_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [setAsBallJointMotion](AsBuiltJointInput_setAsBallJointMotion.md) | Defines the relationship between the two joint geometries as a ball joint. |
| [setAsCylindricalJointMotion](AsBuiltJointInput_setAsCylindricalJointMotion.md) | Defines the relationship between the two joint geometries as a cylindrical joint. |
| [setAsPinSlotJointMotion](AsBuiltJointInput_setAsPinSlotJointMotion.md) | Defines the relationship between the two joint geometries as a pin-slot joint. |
| [setAsPlanarJointMotion](AsBuiltJointInput_setAsPlanarJointMotion.md) | Defines the relationship between the two joint geometries as a planar joint. |
| [setAsRevoluteJointMotion](AsBuiltJointInput_setAsRevoluteJointMotion.md) | Defines the relationship between the two joint geometries as a revolute joint. |
| [setAsRigidJointMotion](AsBuiltJointInput_setAsRigidJointMotion.md) | Defines the relationship between the two joint geometries as a rigid joint. |
| [setAsSliderJointMotion](AsBuiltJointInput_setAsSliderJointMotion.md) | Defines the relationship between the two joint geometries as a slider joint. |

## Properties

| Name | Description |
| --- | --- |
| [geometry](AsBuiltJointInput_geometry.md) | Specifies the position of the joint. |
| [isValid](AsBuiltJointInput_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [jointMotion](AsBuiltJointInput_jointMotion.md) | Returns one of the objects derived from JointMotion that defines how the motion between the two joint geometries is defined. Can be null if the motion hasn't yet been defined. |
| [objectType](AsBuiltJointInput_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [occurrenceOne](AsBuiltJointInput_occurrenceOne.md) | Specifies the first of two occurrences the joint is between. |
| [occurrenceTwo](AsBuiltJointInput_occurrenceTwo.md) | Specifies the second of two occurrences the joint is between. |

## Accessed From

[AsBuiltJoints.createInput](AsBuiltJoints_createInput.md)

## Samples

| Name | Description |
|----|----|
| [As-Built Joint Sample](AsBuiltJointSample_Sample.md) | Demonstrates creating a new As-Built Joint. |

## Version

Introduced in version September 2015  

