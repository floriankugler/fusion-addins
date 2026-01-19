# DataObjectFuture Object

Derived from: [Future](Future.md) Object  

## Description

Used to check the state of getting data associated with an object where the associated data typically exists on the cloud.

## Methods

| Name | Description |
|----|----|
| [classType](DataObjectFuture_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [dataObject](DataObjectFuture_dataObject.md) | Returns the DataObject when the data has become available, (state returns FinishedFutureState). Returns null if the operation is still running or has failed. |
| [isValid](DataObjectFuture_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](DataObjectFuture_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [state](DataObjectFuture_state.md) | Returns the current state of the process associated with this future. |

## Accessed From

[DataFile.dataObject](DataFile_dataObject.md), [DataFile.thumbnail](DataFile_thumbnail.md)

## Version

Introduced in version September 2024  

