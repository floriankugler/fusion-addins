# ImportManager Object

Derived from: [Base](Base.md) Object  

## Description

Provides access to functionality to support importing various modeling formats into Fusion.

## Methods

| Name | Description |
| --- | --- |
| [classType](ImportManager_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createDXF2DImportOptions](ImportManager_createDXF2DImportOptions.md) | Creates a DXF2DImportOptions object that is used to import 2D data to create sketches. Creation of the createDXF2DImportOptions object does not perform the import. You must pass this object to the ImportManager.importToTarget method to perform the import. The sketches created as a result of the import are available through the 'results' property of the DXF2DImportOptions. |
| [createFusionArchiveImportOptions](ImportManager_createFusionArchiveImportOptions.md) | Creates a FusionArchiveImportOptions object that imports a design from a Fusion archive format. The creation of the FusionArchiveImportOptions object does not perform the import. You must pass this object to one of the ImportManager import methods to perform the import. The FusionArchiveImportOptions object supports the available options when importing from a Fusion archive format. This method only supports f3d files. For f3z files, you should use the DataFolder.uploadFile method. |
| [createIGESImportOptions](ImportManager_createIGESImportOptions.md) | Creates an IGESImportOptions object that is used to import a design from IGES format. Creation of the IGESImportOptions object does not perform the import. You must pass this object to one of the ImportManager import methods to perform the import. The IGESImportOptions supports any available options when importing from IGES format. |
| [createSATImportOptions](ImportManager_createSATImportOptions.md) | Creates an SATImportOptions object that's used to import a design from SAT format. Creation of the SATImportOptions object does not perform the import. You must pass this object to one of the ImportManager import methods to perform the import. The SATImportOptions supports any available options when importing from SAT format. |
| [createSMTImportOptions](ImportManager_createSMTImportOptions.md) | Creates an SMTImportOptions object that's used to import a design from SMT format. Creation of the SMTImportOptions object does not perform the import. You must pass this object to one of the ImportManager import methods to perform the import. The SMTImportOptions supports any available options when importing from SMT format. |
| [createSTEPImportOptions](ImportManager_createSTEPImportOptions.md) | Creates an STEPImportOptions object that's used to import a design from STEP format. Creation of the STEPImportOptions object does not perform the import. You must pass this object to one of the ImportManager import methods to perform the import. The STEPImportOptions supports any available options when importing from STEP format. |
| [createSVGImportOptions](ImportManager_createSVGImportOptions.md) | Creates a SVGImportOptions object that is used to import SVG data into a sketch. Creation of the SVGImportOptions object does not perform the import. You must pass this object to the importToTarget or importToTarget2 methods to perform the import and provide the sketch you want to import to as the target. |
| [importToNewDocument](ImportManager_importToNewDocument.md) | Executes the import operation to import a file (of the format specified by the input ImportOptions object) to a new document. This method does not support the DXF2DImportOptions or SVGImportOptions objects. Use ImportToTarget or ImportToTarget2 for those types. |
| [importToTarget](ImportManager_importToTarget.md) | Executes the import operation to import a file (of the format specified by the input ImportOptions object) into an existing component in an existing design. |
| [importToTarget2](ImportManager_importToTarget2.md) | Executes the import operation to import a file (of the format specified by the input ImportOptions object) into an existing component in an existing design and returns the imported objects. |

## Properties

| Name | Description |
| --- | --- |
| [isValid](ImportManager_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](ImportManager_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Application.importManager](Application_importManager.md)

## Samples

| Name | Description |
|----|----|
| [Import Manager API Sample](ImportManager_Sample.md) | Demonstrates how to import different formats to Fusion document |

## Version

Introduced in version September 2015  

