# FusionDocument.close Method

Parent Object: [FusionDocument](FusionDocument.md)  

## Description

Closes this document.

## Remarks

Closing a document is not supported within any of the Command related events. When a command is running, a transaction is open, and creating and closing documents cannot be transacted and, as a result, cannot be contained within a command transaction.

## Syntax

"fusionDocument_var" is a variable referencing a [FusionDocument](FusionDocument.md) object.

```python
returnValue = fusionDocument_var.close(saveChanges)
```

## Return Value

| Type    | Description                                          |
|---------|------------------------------------------------------|
| boolean | Returns true if closing the document was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| saveChanges | boolean | This argument defines what the behavior of the close is when the document has been modified. If the document hasn't been modified then this argument is ignored and the document is closed. If the document has been modified and this argument is false then Fusion will close the document and lose any changes. If the document has been modified and this argument is true then it will prompt the user if they want to save the changes or not, just the same as if the user was to interactively close the document. |

## Samples

| Name | Description |
|----|----|
| [Save and Insert File API Sample](SaveAndInsertSample_Sample.md) | Demonstrates creating save a new file and then inserting it into a design. To use this sample, have a design open that has been saved and run the script. It will create a new design that contains a cylinder, save it to the same folder the active design was saved to, and then insert it into the active design. |

## Version

Introduced in version November 2014  

