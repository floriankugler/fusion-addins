# ExportManager.createFusionArchiveExportOptions Method

Parent Object: [ExportManager](ExportManager.md)  

## Description

Creates an FusionArchiveExportOptions object that's used to export a design in Fusion archive format. Creation of the FusionArchiveExportOptions object does not perform the export. You must pass this object to the ExportManager.execute method to perform the export. The FusionArchiveExportOptions supports any available options when exporting to Fusion archive format.

## Syntax

"exportManager_var" is a variable referencing an [ExportManager](ExportManager.md) object.

```python
# Uses no optional arguments.
returnValue = exportManager_var.createFusionArchiveExportOptions(filename)

# Uses optional arguments.
returnValue = exportManager_var.createFusionArchiveExportOptions(filename, geometry)
```

## Return Value

| Type | Description |
|----|----|
| [FusionArchiveExportOptions](FusionArchiveExportOptions.md) | The created FusionArchiveExportOptions object or null if the creation failed. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| filename | string | The filename of the Fusion archive file to be created. |
| geometry | [Base](Base.md) | The geometry to export. Valid geometry for this is currently a Component object. This argument is optional and if not specified, it results in the root component and it entire contents being exported. This is an optional argument whose default value is null. |

## Samples

| Name | Description |
|----|----|
| [ExportManager API Sample](ExportManager_Sample.md) | Demonstrates how to export f3d to different formats. |
| [Export to other formats API Sample](ExportToOtherFormats_Sample.md) | Demonstrates exporting the active design to IGES, STEP, SAT, SMT, F3D and STL formats. To run this sample, have a design open and run the script. It will write out the translated files to a temp directory, which will it show in a message box. |

## Version

Introduced in version January 2015  

