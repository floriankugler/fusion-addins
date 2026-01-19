# PropertyGroups Object

Derived from: [Base](Base.md) Object  

## Description

A collection of PropertyGroup objects.

## Methods

| Name | Description |
|----|----|
| [classType](PropertyGroups_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](PropertyGroups_item.md) | Returns the specified property group from the collection using an index into the collection. |
| [itemById](PropertyGroups_itemById.md) | Returns the specified property group from the collection using the unique ID of the property group. The ID is consistent and can't be modified by the user and isn't affected by localization. |
| [itemByName](PropertyGroups_itemByName.md) | Returns the specified PropertyGroup using the name of the group. |

## Properties

| Name | Description |
| --- | --- |
| [count](PropertyGroups_count.md) | Returns the number of properties within the collection. |
| [isValid](PropertyGroups_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](PropertyGroups_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[BaseComponent.propertyGroups](BaseComponent_propertyGroups.md), [Component.propertyGroups](Component_propertyGroups.md), [FlatPatternComponent.propertyGroups](FlatPatternComponent_propertyGroups.md)

## Samples

| Name | Description |
| --- | --- |
| [Library Item API Sample](LibraryItemSample_Sample.md) | Demonstrates how to examine library items using the API. To use the sample, create a new Python or C++ script and copy and paste this code, replacing the existing default code. The script will search for and record all components and library items in the current project. They are displayed in a dialog when the script has finished. |

## Version

Introduced in version January 2024  

