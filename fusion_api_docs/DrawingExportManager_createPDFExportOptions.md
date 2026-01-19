# DrawingExportManager.createPDFExportOptions Method

Parent Object: [DrawingExportManager](DrawingExportManager.md)  

## Description

Defines the various settings for a STEP export.

## Syntax

"drawingExportManager_var" is a variable referencing a [DrawingExportManager](DrawingExportManager.md) object.

```python
returnValue = drawingExportManager_var.createPDFExportOptions(filename)
```

## Return Value

| Type | Description |
|----|----|
| [PDFExportOptions](PDFExportOptions.md) | Returns a PDFExportOptions object if successful and null if it should fail. |

## Parameters

| Name | Type | Description |
|----|----|----|
| filename | string | The name of the file to export to. Use settings on the returned PDFExportOptions object to change other settings. |

## Version

Introduced in version December 2020  

