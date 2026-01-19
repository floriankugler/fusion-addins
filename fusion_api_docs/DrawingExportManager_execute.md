# DrawingExportManager.execute Method

Parent Object: [DrawingExportManager](DrawingExportManager.md)  

## Description

Executes the export operation to create the file in the format specified by the input ExportOptions object.

## Syntax

"drawingExportManager_var" is a variable referencing a [DrawingExportManager](DrawingExportManager.md) object.

```python
returnValue = drawingExportManager_var.execute(exportOptions)
```

## Return Value

| Type    | Description                                |
|---------|--------------------------------------------|
| boolean | Returns true if the export was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| exportOptions | [DrawingExportOptions](DrawingExportOptions.md) | A DrawingExportOptions object that is created using one of the create methods on the DrawingExportManager object. This defines the type of export and defines the options supported for that file type. |

## Version

Introduced in version December 2020  

