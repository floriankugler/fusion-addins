# ExportManager.createDXFFlatPatternExportOptions Method

Parent Object: [ExportManager](ExportManager.md)  

## Description

Creates a DXFFlatPatternExport object that's used to export a flat pattern in DXF format. Creation of the DXFFlatPatternExport object does not perform the export. You must call the execute method. You can change any additional settings by setting properties on the returned object before calling the execute method.

## Syntax

"exportManager_var" is a variable referencing an [ExportManager](ExportManager.md) object.

```python
returnValue = exportManager_var.createDXFFlatPatternExportOptions(filename, flatPattern)
```

## Return Value

| Type | Description |
|----|----|
| [DXFFlatPatternExportOptions](DXFFlatPatternExportOptions.md) | The created DXFFlatPatternExport object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| filename | string | The filename of the DXF file to be created. |
| flatPattern | [FlatPattern](FlatPattern.md) | The FlatPattern object to export. |

## Version

Introduced in version November 2022  

