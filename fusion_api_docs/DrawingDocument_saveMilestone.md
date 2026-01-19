# DrawingDocument.saveMilestone Method

Parent Object: [DrawingDocument](DrawingDocument.md)  

## Description

Saves the document as a new milestone. This method is not applicable when saving a document for the first time. In that case, you must use the SaveAs method. You can determine if a document has been saved by checking the value of the isSaved property.

## Remarks

Saving a document is not supported within any of the Command related events. When a command is running, a transaction is open, and saving a document cannot be transacted and, as a result, cannot be contained within a command transaction.

## Syntax

"drawingDocument_var" is a variable referencing a [DrawingDocument](DrawingDocument.md) object.

```python
returnValue = drawingDocument_var.saveMilestone(milestoneName, versionDescription)
```

## Return Value

| Type | Description |
|----|----|
| boolean | Returns true if saving the document as a milestone was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| milestoneName | string | The name of the milestone as seen in the data panel and Fusion web client. If an empty string is provided a default name will be used. |
| versionDescription | string | The description associated with the version. If an empty string is provided, a default description will be used. |

## Version

Introduced in version March 2024  

