# CAMExportManager.execute Method

Parent Object: [CAMExportManager](CAMExportManager.md)  

## Description

Executes an export based on the export options.

## Syntax

"cAMExportManager_var" is a variable referencing a [CAMExportManager](CAMExportManager.md) object.

```python
returnValue = cAMExportManager_var.execute(exportOptions)
```

## Return Value

| Type    | Description                                       |
|---------|---------------------------------------------------|
| boolean | Returns true if the export finished successfully. |

## Parameters

| Name | Type | Description |
|----|----|----|
| exportOptions | [CAMExportOptions](CAMExportOptions.md) | The export options defining the export type and necessary meta data. |

## Version

Introduced in version November 2021  

