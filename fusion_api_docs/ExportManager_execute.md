# ExportManager.execute Method

Parent Object: [ExportManager](ExportManager.md)  

## Description

Executes the export operation to create the file in the format specified by the provided ExportOptions object.

## Syntax

"exportManager_var" is a variable referencing an [ExportManager](ExportManager.md) object.

```python
returnValue = exportManager_var.execute(exportOptions)
```

## Return Value

| Type    | Description                                |
|---------|--------------------------------------------|
| boolean | Returns true if the export was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| exportOptions | [ExportOptions](ExportOptions.md) | An ExportOptions object that is created using one of the create methods on the ExportManager object. This defines the type of file and any available options supported for that file type. |

## Samples

| Name | Description |
|----|----|
| [ExportManager API Sample](ExportManager_Sample.md) | Demonstrates how to export f3d to different formats. |
| [Export to other formats API Sample](ExportToOtherFormats_Sample.md) | Demonstrates exporting the active design to IGES, STEP, SAT, SMT, F3D and STL formats. To run this sample, have a design open and run the script. It will write out the translated files to a temp directory, which will it show in a message box. |
| [Set parameters from a csv file and export to STEP](SetParametersFromACsvFileAndExportToSTEP_Sample.md) | Reads data from a .csv file and sets user parameters in the model and then exports the model to STEP. When setting parameters be aware that this sample is setting user parameters. It's also possible to set model parameters but that's not demonstrated here. Also when accessing parameters, it is case sensitive so the names you use in your program much exactly match the names in the model. |
| [STLExport API Sample](STLExport_Sample.md) | Demonstrates how to export f3d to STL format. |

## Version

Introduced in version January 2015  

