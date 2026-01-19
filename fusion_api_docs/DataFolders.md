# DataFolders Object

Derived from: [Base](Base.md) Object  

## Description

Collection object the provides a list of data folders.

## Methods

| Name | Description |
|----|----|
| [add](DataFolders_add.md) | Creates a new folder within the parent folder. |
| [asArray](DataFolders_asArray.md) | Get the current list of all folders. |
| [classType](DataFolders_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](DataFolders_item.md) | Returns the specified folder. |
| [itemById](DataFolders_itemById.md) | Returns the folder specified using the ID of the folder. |
| [itemByName](DataFolders_itemByName.md) | Returns the folder specified using the name of the folder. |

## Properties

| Name | Description |
| --- | --- |
| [count](DataFolders_count.md) | The number of folders in this collection. |
| [isValid](DataFolders_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](DataFolders_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[DataFolder.dataFolders](DataFolder_dataFolders.md)

## Version

Introduced in version January 2015  

