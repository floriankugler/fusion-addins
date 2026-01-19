# DataFiles Object

Derived from: [Base](Base.md) Object  

## Description

Returns the items within a folder. This includes everything in a folder except for other folders.

## Methods

| Name | Description |
|----|----|
| [asArray](DataFiles_asArray.md) | Get the current list of all files. |
| [classType](DataFiles_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](DataFiles_item.md) | Returns the specified data file. |
| [itemById](DataFiles_itemById.md) | Returns the file specified using the ID or version ID of the file. |

## Properties

| Name | Description |
| --- | --- |
| [count](DataFiles_count.md) | The number of data items in this collection. |
| [isValid](DataFiles_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](DataFiles_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[DataFile.childReferences](DataFile_childReferences.md), [DataFile.parentReferences](DataFile_parentReferences.md), [DataFile.versions](DataFile_versions.md), [DataFolder.dataFiles](DataFolder_dataFiles.md), [DesignDataFile.childReferences](DesignDataFile_childReferences.htm), [DesignDataFile.parentReferences](DesignDataFile_parentReferences.htm), [DesignDataFile.versions](DesignDataFile_versions.htm)

## Version

Introduced in version January 2015  

