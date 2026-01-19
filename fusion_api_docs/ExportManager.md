# ExportManager Object

Derived from: [Base](Base.md) Object  

## Description

Provides support for exporting model data to various formats.

## Methods

| Name | Description |
|----|----|
| [classType](ExportManager_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createC3MFExportOptions](ExportManager_createC3MFExportOptions.md) | Creates a C3MFExportOptions object that's used to export a design in 3MF format. Creation of the C3MFExportOptions object does not perform the export. You must pass this object to the ExportManager.execute method to perform the export. |
| [createDXFFlatPatternExportOptions](ExportManager_createDXFFlatPatternExportOptions.md) | Creates a DXFFlatPatternExport object that's used to export a flat pattern in DXF format. Creation of the DXFFlatPatternExport object does not perform the export. You must call the execute method. You can change any additional settings by setting properties on the returned object before calling the execute method. |
| [createDXFSketchExportOptions](ExportManager_createDXFSketchExportOptions.md) | Creates a DXFSketchExportOptions object that's used to export a sketch in DXF format. Creation of the DXFSketchExportOptions object does not perform the export. You must call the execute method after changing the settings to the desired values. |
| [createFusionArchiveExportOptions](ExportManager_createFusionArchiveExportOptions.md) | Creates an FusionArchiveExportOptions object that's used to export a design in Fusion archive format. Creation of the FusionArchiveExportOptions object does not perform the export. You must pass this object to the ExportManager.execute method to perform the export. The FusionArchiveExportOptions supports any available options when exporting to Fusion archive format. |
| [createIGESExportOptions](ExportManager_createIGESExportOptions.md) | Creates an IGESExportOptions object that's used to export a design in IGES format. Creation of the IGESExportOptions object does not perform the export. You must pass this object to the ExportManager.execute method to perform the export. The IGESExportOptions supports any available options when exporting to IGES format. |
| [createOBJExportOptions](ExportManager_createOBJExportOptions.md) | Creates an OBJExportOptions object that's used to export a design in OBJ format. Creation of the OBJExportOptions object does not perform the export. You must pass this object to the ExportManager.execute method to perform the export. |
| [createSATExportOptions](ExportManager_createSATExportOptions.md) | Creates an SATExportOptions object that's used to export a design in SAT format. Creation of the SATExportOptions object does not perform the export. You must pass this object to the ExportManager.execute method to perform the export. The SATExportOptions supports any available options when exporting to SAT format. |
| [createSMTExportOptions](ExportManager_createSMTExportOptions.md) | Creates an SMTExportOptions object that's used to export a design in SMT format. Creation of the SMTExportOptions object does not perform the export. You must pass this object to the ExportManager.execute method to perform the export. The SMTExportOptions supports any available options when exporting to SMT format. |
| [createSTEPExportOptions](ExportManager_createSTEPExportOptions.md) | Creates an STEPExportOptions object that's used to export a design in STEP format. Creation of the STEPExportOptions object does not perform the export. You must pass this object to the ExportManager.execute method to perform the export. The STEPExportOptions supports any available options when exporting to STEP format. |
| [createSTLExportOptions](ExportManager_createSTLExportOptions.md) | Creates an STLExportOptions object that's used to export a design in STL format. Creation of the STLExportOptions object does not perform the export. You must pass this object to the ExportManager.execute method to perform the export. |
| [createUSDExportOptions](ExportManager_createUSDExportOptions.md) | Creates an USDExportOptions object that's used to export a design in USD format. Creation of the USDExportOptions object does not perform the export. You must pass this object to the ExportManager.execute method to perform the export. The USDExportOptions supports any available options when exporting to USD format. |
| [execute](ExportManager_execute.md) | Executes the export operation to create the file in the format specified by the provided ExportOptions object. |

## Properties

| Name | Description |
| --- | --- |
| [isValid](ExportManager_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](ExportManager_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Design.exportManager](Design_exportManager.md), [FlatPatternProduct.exportManager](FlatPatternProduct_exportManager.md), [WorkingModel.exportManager](WorkingModel_exportManager.md)

## Samples

| Name | Description |
|----|----|
| [ExportManager API Sample](ExportManager_Sample.md) | Demonstrates how to export f3d to different formats. |
| [Export to other formats API Sample](ExportToOtherFormats_Sample.md) | Demonstrates exporting the active design to IGES, STEP, SAT, SMT, F3D and STL formats. To run this sample, have a design open and run the script. It will write out the translated files to a temp directory, which will it show in a message box. |
| [Set parameters from a csv file and export to STEP](SetParametersFromACsvFileAndExportToSTEP_Sample.md) | Reads data from a .csv file and sets user parameters in the model and then exports the model to STEP. When setting parameters be aware that this sample is setting user parameters. It's also possible to set model parameters but that's not demonstrated here. Also when accessing parameters, it is case sensitive so the names you use in your program much exactly match the names in the model. |
| [STLExport API Sample](STLExport_Sample.md) | Demonstrates how to export f3d to STL format. |

## Version

Introduced in version January 2015  

