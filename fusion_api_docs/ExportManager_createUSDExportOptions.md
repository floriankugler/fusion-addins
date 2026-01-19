# ExportManager.createUSDExportOptions Method

Parent Object: [ExportManager](ExportManager.md)  

## Description

Creates an USDExportOptions object that's used to export a design in USD format. Creation of the USDExportOptions object does not perform the export. You must pass this object to the ExportManager.execute method to perform the export. The USDExportOptions supports any available options when exporting to USD format.

## Syntax

"exportManager_var" is a variable referencing an [ExportManager](ExportManager.md) object.

```python
# Uses no optional arguments.
returnValue = exportManager_var.createUSDExportOptions(filename)

# Uses optional arguments.
returnValue = exportManager_var.createUSDExportOptions(filename, geometry)
```

## Return Value

| Type | Description |
|----|----|
| [USDExportOptions](USDExportOptions.md) | The created USDExportOptions object or null if the creation failed. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| filename | string | The filename of the USD file to be created. |
| geometry | [Base](Base.md) | The geometry to export. Valid geometry for this is currently a Component object. This argument is optional and if not specified, it results in the root component and it entire contents being exported. This is an optional argument whose default value is null. |

## Version

Introduced in version March 2022  

