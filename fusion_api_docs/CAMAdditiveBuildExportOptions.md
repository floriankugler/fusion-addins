# CAMAdditiveBuildExportOptions Object

Derived from: [CAMExportOptions](CAMExportOptions.md) Object  

## Description

Additive buildfile export option. Available with all additive machines except for FFF and DED based machines. Currently picks the first export filter from the print setting's export filter list.

## Methods

| Name | Description |
|----|----|
| [classType](CAMAdditiveBuildExportOptions_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [error](CAMAdditiveBuildExportOptions_error.md) | Gets the last encountered error message. When the CAMExportManager's executeWithExportFuture() method is used, this method only returns errors encoutered when setting up the export. Errors thrown afterwards can be retrieved via the CAMExportFuture object. When the CAMExportManager's execute() method is used, any error can be retrieved using this property. |
| [exportFilters](CAMAdditiveBuildExportOptions_exportFilters.md) | Gets a list of available export filters from the setup's print setting. The export object must be set before using this function. |
| [exportObject](CAMAdditiveBuildExportOptions_exportObject.md) | The export object we want to export. Depending on the actual export option, this might be geometry, an operation or a setup. |
| [fullFilename](CAMAdditiveBuildExportOptions_fullFilename.md) | The file we want to export to. Needs to contain a valid path, as no intermediate folders are created. |
| [isThumbnailSupported](CAMAdditiveBuildExportOptions_isThumbnailSupported.md) | Method to check if the exporter implementation supports thumbnail |
| [isValid](CAMAdditiveBuildExportOptions_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](CAMAdditiveBuildExportOptions_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [selectedExportFilterId](CAMAdditiveBuildExportOptions_selectedExportFilterId.md) | Gets and sets the export filter to be used for the export. By default, this is the first entry in the print setting's filter list. |
| [thumbnailPath](CAMAdditiveBuildExportOptions_thumbnailPath.md) | Path to the thumbnail for the buildfile |

## Accessed From

[CAMExportManager.createCAMAdditiveBuildExportOptions](CAMExportManager_createCAMAdditiveBuildExportOptions.md)

## Version

Introduced in version October 2023  

