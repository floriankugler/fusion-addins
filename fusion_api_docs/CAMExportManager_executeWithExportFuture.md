# CAMExportManager.executeWithExportFuture Method

Parent Object: [CAMExportManager](CAMExportManager.md)  

## Description

Executes an export based on the export options

## Syntax

"cAMExportManager_var" is a variable referencing a [CAMExportManager](CAMExportManager.md) object.

```python
returnValue = cAMExportManager_var.executeWithExportFuture(exportOptions)
```

## Return Value

| Type | Description |
|----|----|
| [CAMExportFuture](CAMExportFuture.md) | Returns a CAMExportFuture object if the export has started successfully. |

## Parameters

| Name | Type | Description |
|----|----|----|
| exportOptions | [CAMExportOptions](CAMExportOptions.md) | The export options defining the export type and necessary meta data. |

## Version

Introduced in version September 2024  

