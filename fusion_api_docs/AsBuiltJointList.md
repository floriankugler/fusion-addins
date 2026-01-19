# AsBuiltJointList Object

Derived from: [Base](Base.md) Object  

## Description

A list of as-built joints.

## Methods

| Name | Description |
|----|----|
| [classType](AsBuiltJointList_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](AsBuiltJointList_item.md) | Function that returns the specified as-built joint using an index into the list. |
| [itemByName](AsBuiltJointList_itemByName.md) | Function that returns the specified as-built joint using a name. |

## Properties

| Name | Description |
| --- | --- |
| [count](AsBuiltJointList_count.md) | Returns number of as-built joints in the list. |
| [isValid](AsBuiltJointList_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](AsBuiltJointList_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Occurrence.asBuiltJoints](Occurrence_asBuiltJoints.md)

## Version

Introduced in version January 2016  

