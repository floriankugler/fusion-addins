# ProfileLoops Object

Derived from: [Base](Base.md) Object  

## Description

A collection of loops within a Profile.

## Methods

| Name | Description |
|----|----|
| [classType](ProfileLoops_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](ProfileLoops_item.md) | Function that returns the specified profile loop using an index into the collection. |

## Properties

| Name | Description |
| --- | --- |
| [count](ProfileLoops_count.md) | Returns the number of loops within this profile. |
| [isValid](ProfileLoops_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](ProfileLoops_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Profile.profileLoops](Profile_profileLoops.md)

## Version

Introduced in version August 2014  

