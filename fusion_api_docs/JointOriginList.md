# JointOriginList Object

Derived from: [Base](Base.md) Object  

## Description

A list of joint origins.

## Methods

| Name | Description |
|----|----|
| [classType](JointOriginList_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](JointOriginList_item.md) | Function that returns the specified joint origin using an index into the list. |
| [itemByName](JointOriginList_itemByName.md) | Function that returns the specified joint origin using a name. |

## Properties

| Name | Description |
| --- | --- |
| [count](JointOriginList_count.md) | Returns number of joint origins in the list. |
| [isValid](JointOriginList_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](JointOriginList_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Version

Introduced in version January 2016  

