# CAM3MFExportOptions Object

Derived from: [CAMExportOptions](CAMExportOptions.md) Object  

## Description

3MF export option. Available with all additive machines except Formlabs. Expects a setup as its export object.

## Methods

| Name | Description |
|----|----|
| [classType](CAM3MFExportOptions_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [areSimulationSurrogatesSplit](CAM3MFExportOptions_areSimulationSurrogatesSplit.md) | Flag toggling if surrogate supports used in the simulation should be split. This option might not be available for all machine types. The default value is false. |
| [areSimulationThickeningStructuresKept](CAM3MFExportOptions_areSimulationThickeningStructuresKept.md) | Flag toggling if thickening structures used for simulation should be kept. This option might not be available for all machine types. The default value is false. |
| [areSupportsIncluded](CAM3MFExportOptions_areSupportsIncluded.md) | **RETIRED** Flag toggling if support information should be included in the exported file. Includes both support structures marked as open or closed support as well as meta data used in Netfabb. This option might not be available for all machine types. The default value is false. |
| [error](CAM3MFExportOptions_error.md) | Gets the last encountered error message. When the CAMExportManager's executeWithExportFuture() method is used, this method only returns errors encoutered when setting up the export. Errors thrown afterwards can be retrieved via the CAMExportFuture object. When the CAMExportManager's execute() method is used, any error can be retrieved using this property. |
| [exportObject](CAM3MFExportOptions_exportObject.md) | The export object we want to export. Depending on the actual export option, this might be geometry, an operation or a setup. |
| [fullFilename](CAM3MFExportOptions_fullFilename.md) | The file we want to export to. Needs to contain a valid path, as no intermediate folders are created. |
| [isMachineInformationIncluded](CAM3MFExportOptions_isMachineInformationIncluded.md) | Flag toggling if machine information should be included in the exported file. The machine information is only compatible with Netfabb. This option might not be available for all machine types. The default value is false. |
| [isProcessSimulationDataIncluded](CAM3MFExportOptions_isProcessSimulationDataIncluded.md) | Flag toggling if simulation information should be included in the exported file. This option might not be available for all machine types. The default value is false. |
| [isSimulationPostProcessingIncluded](CAM3MFExportOptions_isSimulationPostProcessingIncluded.md) | Flag toggling if post processing of the simulation should be included. This option might not be available for all machine types. The default value is false. |
| [isSliceDataIncluded](CAM3MFExportOptions_isSliceDataIncluded.md) | Flag toggling if slice data which has been generated beforehand by generating the entire setup or the additive toolpath object should be included in the exported file. The default value is false. |
| [isThumbnailSupported](CAM3MFExportOptions_isThumbnailSupported.md) | Method to check if the exporter implementation supports thumbnail |
| [isValid](CAM3MFExportOptions_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [isVolumetricDataIncluded](CAM3MFExportOptions_isVolumetricDataIncluded.md) | Flag toggling if volumetric data should be included in the exported file. The flag is only evaluated if the user has bought the product design extension. The default value is false. |
| [metadata](CAM3MFExportOptions_metadata.md) | Class for setting the meta data options with in the 3mf export |
| [objectType](CAM3MFExportOptions_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [supportInclusion](CAM3MFExportOptions_supportInclusion.md) | Flag setting if support information should be included in the exported file. Includes both support structures marked as open or closed support as well as meta data used in Netfabb. This option might not be available for all machine types. The default value is NotIncluded. |
| [thumbnailPath](CAM3MFExportOptions_thumbnailPath.md) | Path to the thumbnail for the buildfile |
| [volumetricDataResolution](CAM3MFExportOptions_volumetricDataResolution.md) | Integer value representing the resolution of the volumetric data. The value is only evaluated if the user has bought the product design extension. The default value is 128. |

## Accessed From

[CAMExportManager.create3MFOptions](CAMExportManager_create3MFOptions.md)

## Version

Introduced in version November 2021  

