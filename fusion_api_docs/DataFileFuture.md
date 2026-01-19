# DataFileFuture Object

Derived from: [Base](Base.md) Object  

## Description

Used to check the state and get back the results of a file upload.

## Methods

| Name | Description |
|----|----|
| [classType](DataFileFuture_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [dataFile](DataFileFuture_dataFile.md) | Returns the DataFile when the upload is complete (uplodeState returns UploadFinished). Returns null if the upload is still running or has failed. |
| [isValid](DataFileFuture_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](DataFileFuture_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [uploadState](DataFileFuture_uploadState.md) | Returns the current state of the upload. |

## Accessed From

[Component.saveCopyAs](Component_saveCopyAs.md), [DataFile.copyWithInput](DataFile_copyWithInput.md), [DataFolder.uploadAssembly](DataFolder_uploadAssembly.md), [DataFolder.uploadFile](DataFolder_uploadFile.md), [FlatPatternComponent.saveCopyAs](FlatPatternComponent_saveCopyAs.md)

## Version

Introduced in version March 2015  

