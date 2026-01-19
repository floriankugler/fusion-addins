# ToolbarTabList Object

Derived from: [Base](Base.md) Object  

## Description

A ToolbarTabList is a list of ToolbarTab objects.

## Methods

| Name | Description |
|----|----|
| [classType](ToolbarTabList_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](ToolbarTabList_item.md) | Returns the specified tab using an index into the collection. |
| [itemById](ToolbarTabList_itemById.md) | Returns the ToolbarTab of the specified ID. |

## Properties

| Name | Description |
| --- | --- |
| [count](ToolbarTabList_count.md) | Gets the number of toolbar tabs in the collection. |
| [isValid](ToolbarTabList_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](ToolbarTabList_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[UserInterface.allToolbarTabs](UserInterface_allToolbarTabs.md), [UserInterface.toolbarTabsByProductType](UserInterface_toolbarTabsByProductType.md)

## Version

Introduced in version August 2019  

