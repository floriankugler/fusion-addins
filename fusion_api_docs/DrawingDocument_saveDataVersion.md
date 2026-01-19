# DrawingDocument.saveDataVersion Method

Parent Object: [DrawingDocument](DrawingDocument.md)  

## Description

Creates a version on a dirty document by implictly saving it first. This method is not applicable when saving a document for the first time. In that case, you must use the Document.saveAs method. You can determine if a document has been saved by checking the value of the isSaved property.

## Syntax

"drawingDocument_var" is a variable referencing a [DrawingDocument](DrawingDocument.md) object.

```python
returnValue = drawingDocument_var.saveDataVersion(versionDescription)
```

## Return Value

| Type | Description |
|----|----|
| boolean | Returns true if saving the document with data version was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| versionDescription | string | The description associated with the data version. |

## Version

Introduced in version November 2025  

