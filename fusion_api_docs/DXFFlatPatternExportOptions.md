# DXFFlatPatternExportOptions Object

Derived from: [ExportOptions](ExportOptions.md) Object  

## Description

Defines that a DXF export of a flat pattern is to be done and specifies the various options.

## Methods

| Name | Description |
|----|----|
| [classType](DXFFlatPatternExportOptions_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [convertToPolylineTolerance](DXFFlatPatternExportOptions_convertToPolylineTolerance.md) | Specifies the tolerance when converting a spline to polylines. This value is only used when the isSplineConvertedToPolyline property is true and otherwise it is ignored. The units for this value are centimeters. Defaults to 0.01 cm. |
| [filename](DXFFlatPatternExportOptions_filename.md) | Gets and sets the filename that the exported file will be written to. This can be empty in the case of STL export and sending the result to the mesh editor. |
| [geometry](DXFFlatPatternExportOptions_geometry.md) | Specifies the geometry to export. This can be an Occurrence, or the root Component. For STL, OBJ, and 3MF export, it can be a BRepBody. For DXF export, it can be a sketch of flat pattern. |
| [isCenterLinesExported](DXFFlatPatternExportOptions_isCenterLinesExported.md) | Specifies if the center lines (bend line) of the flat pattern are exported in the DXF. Defaults to true. |
| [isExtentLinesExported](DXFFlatPatternExportOptions_isExtentLinesExported.md) | Specifies if the bend extent lines of the flat pattern are exported in the DXF. Defaults to true. |
| [isSplineConvertedToPolyline](DXFFlatPatternExportOptions_isSplineConvertedToPolyline.md) | Specifies if splines are converted to polylines. If true, the convertToPolylineTolerance value is used to specify the accuracy of the conversion. Defaults to false. |
| [isValid](DXFFlatPatternExportOptions_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](DXFFlatPatternExportOptions_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [units](DXFFlatPatternExportOptions_units.md) | Gets and sets the units that will be used for the DXF file. This defaults to be the same as the default units of the design. |

## Accessed From

[ExportManager.createDXFFlatPatternExportOptions](ExportManager_createDXFFlatPatternExportOptions.md)

## Version

Introduced in version November 2022  

