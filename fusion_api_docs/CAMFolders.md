# CAMFolders Object

Derived from: [Base](Base.md) Object  

## Description

Collection that provides access to the folders within an existing setup, folder or pattern.

## Methods

| Name | Description |
|----|----|
| [addFolder](CAMFolders_addFolder.md) | Creates a folder with the specified name and returns it as CAMFolder object. |
| [classType](CAMFolders_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](CAMFolders_item.md) | Function that returns the specified folder using an index into the collection. |
| [itemByName](CAMFolders_itemByName.md) | Returns the folder with the specified name (as appears in the browser). |
| [itemByOperationId](CAMFolders_itemByOperationId.md) | Returns the folder with the specified operation id. |

## Properties

| Name | Description |
| --- | --- |
| [count](CAMFolders_count.md) | The number of items in the collection. |
| [isValid](CAMFolders_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](CAMFolders_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[CAMFolder.folders](CAMFolder_folders.md), [CAMHoleRecognition.folders](CAMHoleRecognition_folders.md), [CAMPattern.folders](CAMPattern_folders.md), [Setup.folders](Setup_folders.md)

## Version

Introduced in version January 2016  

