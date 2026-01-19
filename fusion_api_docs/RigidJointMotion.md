# RigidJointMotion Object

Derived from: [JointMotion](JointMotion.md) Object  

## Description

Represents the set of information specific to a rigid joint. A rigid joint doesn't support any additional information beyond getting the joint type which it derives from JointMotion.

## Methods

| Name | Description |
|----|----|
| [classType](RigidJointMotion_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [isValid](RigidJointMotion_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [jointType](RigidJointMotion_jointType.md) | Returns an enum value indicating the type of joint this joint represents. |
| [objectType](RigidJointMotion_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Version

Introduced in version July 2015  

