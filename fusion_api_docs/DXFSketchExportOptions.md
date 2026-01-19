# DXFSketchExportOptions Object

Derived from: [ExportOptions](ExportOptions.md) Object  

## Description

Defines the various settings associated with exporting a sketch in DXF format.

## Methods

| Name | Description |
|----|----|
| [classType](DXFSketchExportOptions_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [filename](DXFSketchExportOptions_filename.md) | Gets and sets the filename that the exported file will be written to. This can be empty in the case of STL export and sending the result to the mesh editor. |
| [geometry](DXFSketchExportOptions_geometry.md) | Specifies the geometry to export. This can be an Occurrence, or the root Component. For STL, OBJ, and 3MF export, it can be a BRepBody. For DXF export, it can be a sketch of flat pattern. |
| [isConstructionExported](DXFSketchExportOptions_isConstructionExported.md) | Indicates if construction geometry should be exported. Defaults to true, which will export all construction geometry. If false it will be ignored and not included in the DXF file. |
| [isPointsExported](DXFSketchExportOptions_isPointsExported.md) | Indicates if the sketch points should be exported. Defaults to true, which will export all points. If false it will be ignored and not included in the DXF file. |
| [isProjectedGeometryExported](DXFSketchExportOptions_isProjectedGeometryExported.md) | Indicates if any projected geometry should be exported. Defaults to true, which will export all projected geometry. If false it will be ignored and not included in the DXF file. |
| [isValid](DXFSketchExportOptions_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](DXFSketchExportOptions_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [units](DXFSketchExportOptions_units.md) | Gets and sets the units that will be used for the DXF file. This defaults to be the same as the default units of the design. |

## Accessed From

[ExportManager.createDXFSketchExportOptions](ExportManager_createDXFSketchExportOptions.md)

## Version

Introduced in version January 2025  

