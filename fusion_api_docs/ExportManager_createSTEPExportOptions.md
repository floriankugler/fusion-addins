# ExportManager.createSTEPExportOptions Method

Parent Object: [ExportManager](ExportManager.md)  

## Description

Creates an STEPExportOptions object that's used to export a design in STEP format. Creation of the STEPExportOptions object does not perform the export. You must pass this object to the ExportManager.execute method to perform the export. The STEPExportOptions supports any available options when exporting to STEP format.

## Syntax

"exportManager_var" is a variable referencing an [ExportManager](ExportManager.md) object.

```python
# Uses no optional arguments.
returnValue = exportManager_var.createSTEPExportOptions(filename)

# Uses optional arguments.
returnValue = exportManager_var.createSTEPExportOptions(filename, geometry)
```

## Return Value

| Type | Description |
|----|----|
| [STEPExportOptions](STEPExportOptions.md) | The created STEPExportOptions object or null if the creation failed. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| filename | string | The filename of the STEP file to be created. |
| geometry | [Base](Base.md) | The geometry to export. Valid geometry for this is currently a Component object. This argument is optional and if not specified, it results in the root component and it entire contents being exported. This is an optional argument whose default value is null. |

## Samples

| Name | Description |
|----|----|
| [ExportManager API Sample](ExportManager_Sample.md) | Demonstrates how to export f3d to different formats. |
| [Export to other formats API Sample](ExportToOtherFormats_Sample.md) | Demonstrates exporting the active design to IGES, STEP, SAT, SMT, F3D and STL formats. To run this sample, have a design open and run the script. It will write out the translated files to a temp directory, which will it show in a message box. |
| [Set parameters from a csv file and export to STEP](SetParametersFromACsvFileAndExportToSTEP_Sample.md) | Reads data from a .csv file and sets user parameters in the model and then exports the model to STEP. When setting parameters be aware that this sample is setting user parameters. It's also possible to set model parameters but that's not demonstrated here. Also when accessing parameters, it is case sensitive so the names you use in your program much exactly match the names in the model. |

## Version

Introduced in version January 2015  

