# CAMExportOptions Object

Derived from: [Base](Base.md) Object  

## Description

Parent class for all ExportOptions objects giving access to the setup and file name used for the export.

## Methods

| Name | Description |
|----|----|
| [classType](CAMExportOptions_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [error](CAMExportOptions_error.md) | Gets the last encountered error message. When the CAMExportManager's executeWithExportFuture() method is used, this method only returns errors encoutered when setting up the export. Errors thrown afterwards can be retrieved via the CAMExportFuture object. When the CAMExportManager's execute() method is used, any error can be retrieved using this property. |
| [exportObject](CAMExportOptions_exportObject.md) | The export object we want to export. Depending on the actual export option, this might be geometry, an operation or a setup. |
| [fullFilename](CAMExportOptions_fullFilename.md) | The file we want to export to. Needs to contain a valid path, as no intermediate folders are created. |
| [isThumbnailSupported](CAMExportOptions_isThumbnailSupported.md) | Method to check if the exporter implementation supports thumbnail |
| [isValid](CAMExportOptions_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](CAMExportOptions_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [thumbnailPath](CAMExportOptions_thumbnailPath.md) | Path to the thumbnail for the buildfile |

## Accessed From

[CAMExportFuture.exportOptions](CAMExportFuture_exportOptions.md)

## Derived Classes

[CAM3MFExportOptions](CAM3MFExportOptions.md), [CAMAdditiveBuildExportOptions](CAMAdditiveBuildExportOptions.md)

## Version

Introduced in version November 2021  

