# CAM3MFExportMetadataOptions Object

Derived from: [Base](Base.md) Object  

## Description

Class providing read and write access to meta data of a 3MF file.

## Methods

| Name | Description |
|----|----|
| [classType](CAM3MFExportMetadataOptions_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [copyright](CAM3MFExportMetadataOptions_copyright.md) | Copyright of the 3MF File |
| [creationDate](CAM3MFExportMetadataOptions_creationDate.md) | Creation date of the 3MF File |
| [description](CAM3MFExportMetadataOptions_description.md) | Description of the 3MF File |
| [designer](CAM3MFExportMetadataOptions_designer.md) | Designer of the 3MF File |
| [enabled](CAM3MFExportMetadataOptions_enabled.md) | Enable or disable the integration of Metadata in the 3mf. This is true by default. |
| [isValid](CAM3MFExportMetadataOptions_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [licenseTerms](CAM3MFExportMetadataOptions_licenseTerms.md) | License terms of the 3MF File |
| [modificationDate](CAM3MFExportMetadataOptions_modificationDate.md) | Modification date of the 3MF File |
| [objectType](CAM3MFExportMetadataOptions_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [title](CAM3MFExportMetadataOptions_title.md) | Title of the 3MF File |

## Accessed From

[CAM3MFExportOptions.metadata](CAM3MFExportOptions_metadata.md)

## Version

Introduced in version May 2023  

