# DrawingDocument.close Method

Parent Object: [DrawingDocument](DrawingDocument.md)  

## Description

Closes this document.

## Remarks

Closing a document is not supported within any of the Command related events. When a command is running, a transaction is open, and creating and closing documents cannot be transacted and, as a result, cannot be contained within a command transaction.

## Syntax

"drawingDocument_var" is a variable referencing a [DrawingDocument](DrawingDocument.md) object.

```python
returnValue = drawingDocument_var.close(saveChanges)
```

## Return Value

| Type    | Description                                          |
|---------|------------------------------------------------------|
| boolean | Returns true if closing the document was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| saveChanges | boolean | This argument defines what the behavior of the close is when the document has been modified. If the document hasn't been modified then this argument is ignored and the document is closed. If the document has been modified and this argument is false then Fusion will close the document and lose any changes. If the document has been modified and this argument is true then it will prompt the user if they want to save the changes or not, just the same as if the user was to interactively close the document. |

## Version

Introduced in version December 2020  

