# PropertyGroup Object

Derived from: [Base](Base.md) Object  

## Description

Represents a group of properties and provides access to the properties.

## Methods

| Name | Description |
|----|----|
| [classType](PropertyGroup_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](PropertyGroup_item.md) | Returns the specified property from the group using an index into the group. |
| [itemById](PropertyGroup_itemById.md) | Returns the specified property from the group using the unique ID of the property. The ID is consistent and can't be modified by the user and isn't affected by localization. |
| [itemByName](PropertyGroup_itemByName.md) | Returns the specified Property using the name of the property. |

## Properties

| Name | Description |
| --- | --- |
| [count](PropertyGroup_count.md) | Returns the number of properties within the group. |
| [id](PropertyGroup_id.md) | Returns the unique ID of this property. |
| [isValid](PropertyGroup_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [name](PropertyGroup_name.md) | Returns the name of this group as seen in the user interface. This name is localized and can change based on the current language |
| [objectType](PropertyGroup_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parent](PropertyGroup_parent.md) | Returns the parent of this group. Typically this will be a Component. |

## Accessed From

[PropertyGroups.item](PropertyGroups_item.md), [PropertyGroups.itemById](PropertyGroups_itemById.md), [PropertyGroups.itemByName](PropertyGroups_itemByName.md)

## Samples

| Name | Description |
| --- | --- |
| [Library Item API Sample](LibraryItemSample_Sample.md) | Demonstrates how to examine library items using the API. To use the sample, create a new Python or C++ script and copy and paste this code, replacing the existing default code. The script will search for and record all components and library items in the current project. They are displayed in a dialog when the script has finished. |

## Version

Introduced in version January 2024  

