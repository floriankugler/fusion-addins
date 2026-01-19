# CAMAdditiveBuildExportFilter Object

Derived from: [Base](Base.md) Object  

## Description

Export filter used by CAMAdditiveMachineBuildFileExportOptions.

## Methods

| Name | Description |
|----|----|
| [classType](CAMAdditiveBuildExportFilter_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [extension](CAMAdditiveBuildExportFilter_extension.md) | The extension of the file format, including a leading "." |
| [id](CAMAdditiveBuildExportFilter_id.md) | The id of the file format. |
| [isMultiFileExport](CAMAdditiveBuildExportFilter_isMultiFileExport.md) | True if the export outputs multiple files. If so, fullFilename should point to a directory, not a file. |
| [isValid](CAMAdditiveBuildExportFilter_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [name](CAMAdditiveBuildExportFilter_name.md) | The name of the file format. Might indicate whether a file format is binary or not. |
| [objectType](CAMAdditiveBuildExportFilter_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[CAMAdditiveBuildExportOptions.exportFilters](CAMAdditiveBuildExportOptions_exportFilters.md)

## Version

Introduced in version October 2023  

