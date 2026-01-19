# ExportManager.createIGESExportOptions Method

Parent Object: [ExportManager](ExportManager.md)  

## Description

Creates an IGESExportOptions object that's used to export a design in IGES format. Creation of the IGESExportOptions object does not perform the export. You must pass this object to the ExportManager.execute method to perform the export. The IGESExportOptions supports any available options when exporting to IGES format.

## Syntax

"exportManager_var" is a variable referencing an [ExportManager](ExportManager.md) object.

```python
# Uses no optional arguments.
returnValue = exportManager_var.createIGESExportOptions(filename)

# Uses optional arguments.
returnValue = exportManager_var.createIGESExportOptions(filename, geometry)
```

## Return Value

| Type | Description |
|----|----|
| [IGESExportOptions](IGESExportOptions.md) | The created IGESExportOptions object or null if the creation failed. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| filename | string | The filename of the IGES file to be created. |
| geometry | [Base](Base.md) | The geometry to export. Valid geometry for this is currently a Component object. This argument is optional and if not specified, it results in the root component and it entire contents being exported. This is an optional argument whose default value is null. |

## Samples

| Name | Description |
|----|----|
| [ExportManager API Sample](ExportManager_Sample.md) | Demonstrates how to export f3d to different formats. |
| [Export to other formats API Sample](ExportToOtherFormats_Sample.md) | Demonstrates exporting the active design to IGES, STEP, SAT, SMT, F3D and STL formats. To run this sample, have a design open and run the script. It will write out the translated files to a temp directory, which will it show in a message box. |

## Version

Introduced in version January 2015  

