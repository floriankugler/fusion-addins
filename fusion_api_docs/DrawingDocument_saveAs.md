# DrawingDocument.saveAs Method

Parent Object: [DrawingDocument](DrawingDocument.md)  

## Description

Performs a Save As on this document. This saves the currently open document to the specified location and this document becomes the saved document. If this is a new document that has never been saved you must use the SaveAs method in order to specify the location and name. You can determine if the document has been saved by checking the value of the isSaved property.

## Remarks

Saving a document is not supported within any of the Command related events. When a command is running, a transaction is open, and saving a document cannot be transacted and, as a result, cannot be contained within a command transaction.

## Syntax

"drawingDocument_var" is a variable referencing a [DrawingDocument](DrawingDocument.md) object.

```python
returnValue = drawingDocument_var.saveAs(name, dataFolder, description, tag)
```

## Return Value

| Type    | Description                                 |
|---------|---------------------------------------------|
| boolean | Returns true if the save as was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| name | string | The name to use for this document. If this is an empty string, Fusion will use the default name assigned when the document was created. |
| dataFolder | [DataFolder](DataFolder.md) | The data folder to save this document to. |
| description | string | The description string of the document. This can be an empty string. |
| tag | string | The tag string of the document. This can be an empty string. |

## Version

Introduced in version December 2020  

