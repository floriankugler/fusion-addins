# Toolbars Object

Derived from: [Base](Base.md) Object  

## Description

Provides access to the toolbars. These are currently the right and left QAT's and the NavBar.

## Methods

| Name | Description |
|----|----|
| [classType](Toolbars_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](Toolbars_item.md) | Returns the specified toolbar using an index into the collection. |
| [itemById](Toolbars_itemById.md) | Returns the Toolbar of the specified ID. |

## Properties

| Name | Description |
| --- | --- |
| [count](Toolbars_count.md) | Gets the number of Toolbar objects in the collection. |
| [isValid](Toolbars_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](Toolbars_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[UserInterface.toolbars](UserInterface_toolbars.md)

## Version

Introduced in version August 2014  

