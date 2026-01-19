# CAMExportManager Object

Derived from: [Base](Base.md) Object  

## Description

Export manager used to export the setup's models in one of the formats defined the ExportOptions objects. The export is currently restricted to additive setups only and the availability of the export option and its settings depends on the chosen machine.

## Methods

| Name | Description |
|----|----|
| [classType](CAMExportManager_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [create3MFOptions](CAMExportManager_create3MFOptions.md) | Creates a new 3MF export option. |
| [createCAMAdditiveBuildExportOptions](CAMExportManager_createCAMAdditiveBuildExportOptions.md) | Creates a new export option based on the print setting's export formats. FFF and DED machines are not supported, their export files are generated using posts. |
| [execute](CAMExportManager_execute.md) | Executes an export based on the export options. |
| [executeWithExportFuture](CAMExportManager_executeWithExportFuture.md) | Executes an export based on the export options |

## Properties

| Name | Description |
| --- | --- |
| [isValid](CAMExportManager_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](CAMExportManager_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[CAM.exportManager](CAM_exportManager.md)

## Version

Introduced in version November 2021  

