# C3MFExportOptions Object

Derived from: [ExportOptions](ExportOptions.md) Object  

## Description

Defines that a 3MF export is to be done and specifies the various options.

## Methods

| Name | Description |
|----|----|
| [classType](C3MFExportOptions_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [aspectRatio](C3MFExportOptions_aspectRatio.md) | Gets and sets the minimum aspect ratio for that triangles that are generated for the mesh. Setting this property will automatically set the meshRefinement to MeshRefinementCustom. The default is the value associated with medium mesh refinement. |
| [availablePrintUtilities](C3MFExportOptions_availablePrintUtilities.md) | Returns a list of the known available print utilities. These strings can be used to set the PrintUtility property to specify which print utility to open the 3MF file in. |
| [filename](C3MFExportOptions_filename.md) | Gets and sets the filename that the exported file will be written to. This can be empty in the case of STL export and sending the result to the mesh editor. |
| [geometry](C3MFExportOptions_geometry.md) | Specifies the geometry to export. This can be an Occurrence, or the root Component. For STL, OBJ, and 3MF export, it can be a BRepBody. For DXF export, it can be a sketch of flat pattern. |
| [isOneFilePerBody](C3MFExportOptions_isOneFilePerBody.md) | If the input is an Occurrence or the root Component, this specifies if a single file should be created containing all of the bodies within that occurrence or component or if multiple files should be created; one for each body. If multiple files are created, the body name is appended to the filename. The default is false. |
| [isValid](C3MFExportOptions_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [maximumEdgeLength](C3MFExportOptions_maximumEdgeLength.md) | Gets and sets the maximum length of any mesh edge. This is defined in centimeter. Setting this property will automatically set the meshRefinement to MeshRefinementCustom. The default is the value associated with medium mesh refinement. |
| [meshRefinement](C3MFExportOptions_meshRefinement.md) | Gets and sets the current simple mesh refinement settings. Setting this property will reset the surfaceDeviation, normalDeviation, maximumEdgeLength, and aspectRatio to values that correspond to the specified mesh refinement. The default is MeshRefinementMedium. |
| [normalDeviation](C3MFExportOptions_normalDeviation.md) | Gets and sets the current normal deviation, or the angle the mesh normals at the vertices can deviate from the actual surface normals. This is defined in radians. Setting this property will automatically set the meshRefinement to MeshRefinementCustom. The default is the value associated with medium mesh refinement. |
| [objectType](C3MFExportOptions_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [printUtility](C3MFExportOptions_printUtility.md) | Specifies which print utility to use when opening the 3MF file if the sendToPrintUtility property is true. The value of this property can be one of the strings returned by the availalbePrintUtilities property, which will specify one of the know print utilities. You can also specify a custom print utility by specifying the full path to the print utility executable. The default value of this property is the last setting specified in the user-interface. |
| [sendToPrintUtility](C3MFExportOptions_sendToPrintUtility.md) | Gets and sets whether the created 3MF file will be sent to the print utility specified by the printUtility property. If this is false a filename must be defined. |
| [surfaceDeviation](C3MFExportOptions_surfaceDeviation.md) | Gets and sets the current surface deviation, or the distance the mesh can deviate from the actual surface. This is defined in centimeter. Setting this property will automatically set the meshRefinement to MeshRefinementCustom. The default is the value associated with medium mesh refinement. |

## Accessed From

[ExportManager.createC3MFExportOptions](ExportManager_createC3MFExportOptions.md)

## Version

Introduced in version September 2021  

