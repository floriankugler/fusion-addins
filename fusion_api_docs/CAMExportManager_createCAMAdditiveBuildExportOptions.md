# CAMExportManager.createCAMAdditiveBuildExportOptions Method

Parent Object: [CAMExportManager](CAMExportManager.md)  

## Description

Creates a new export option based on the print setting's export formats. FFF and DED machines are not supported, their export files are generated using posts.

## Syntax

"cAMExportManager_var" is a variable referencing a [CAMExportManager](CAMExportManager.md) object.

```python
returnValue = cAMExportManager_var.createCAMAdditiveBuildExportOptions()
```

## Return Value

| Type | Description |
|----|----|
| [CAMAdditiveBuildExportOptions](CAMAdditiveBuildExportOptions.md) | Returns new CAMAdditiveBuildExportOptions. |

## Version

Introduced in version October 2023  

