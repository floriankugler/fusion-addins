# ExportManager.createSTLExportOptions Method

Parent Object: [ExportManager](ExportManager.md)  

## Description

Creates an STLExportOptions object that's used to export a design in STL format. Creation of the STLExportOptions object does not perform the export. You must pass this object to the ExportManager.execute method to perform the export.

## Syntax

"exportManager_var" is a variable referencing an [ExportManager](ExportManager.md) object.

```python
# Uses no optional arguments.
returnValue = exportManager_var.createSTLExportOptions(geometry)

# Uses optional arguments.
returnValue = exportManager_var.createSTLExportOptions(geometry, filename)
```

## Return Value

| Type | Description |
|----|----|
| [STLExportOptions](STLExportOptions.md) | The created createSTLExportOptions object or null if the creation failed. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| geometry | [Base](Base.md) | The geometry to export. This can be a BRepBody, Occurrence, or Component object. |
| filename | string | The filename of the STL file to be created. This is optional and can be left out if the mesh will be opened in a mesh editor. This is an optional argument whose default value is "". |

## Samples

| Name | Description |
|----|----|
| [Export to other formats API Sample](ExportToOtherFormats_Sample.md) | Demonstrates exporting the active design to IGES, STEP, SAT, SMT, F3D and STL formats. To run this sample, have a design open and run the script. It will write out the translated files to a temp directory, which will it show in a message box. |
| [STLExport API Sample](STLExport_Sample.md) | Demonstrates how to export f3d to STL format. |

## Version

Introduced in version January 2015  

