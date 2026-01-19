# ExportManager.createC3MFExportOptions Method

Parent Object: [ExportManager](ExportManager.md)  

## Description

Creates a C3MFExportOptions object that's used to export a design in 3MF format. Creation of the C3MFExportOptions object does not perform the export. You must pass this object to the ExportManager.execute method to perform the export.

## Syntax

"exportManager_var" is a variable referencing an [ExportManager](ExportManager.md) object.

```python
# Uses no optional arguments.
returnValue = exportManager_var.createC3MFExportOptions(geometry)

# Uses optional arguments.
returnValue = exportManager_var.createC3MFExportOptions(geometry, filename)
```

## Return Value

| Type | Description |
|----|----|
| [C3MFExportOptions](C3MFExportOptions.md) | The created createC3MFExportOptions object or null if the creation failed. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| geometry | [Base](Base.md) | The geometry to export. This can be a BRepBody, Occurrence, or Component object. |
| filename | string | The filename of the 3MF file to be created. This is optional and can be left out if the mesh will be opened in a mesh editor. This is an optional argument whose default value is "". |

## Version

Introduced in version September 2021  

