# Document.saveAs Method

Parent Object: [Document](Document.md)  

## Description

Performs a Save As on this document. This saves the currently open document to the specified location and this document becomes the saved document. If this is a new document that has never been saved you must use the SaveAs method in order to specify the location and name. You can determine if the document has been saved by checking the value of the isSaved property.

## Remarks

Saving a document is not supported within any of the Command related events. When a command is running, a transaction is open, and saving a document cannot be transacted and, as a result, cannot be contained within a command transaction.

## Syntax

"document_var" is a variable referencing a [Document](Document.md) object.

```python
returnValue = document_var.saveAs(name, dataFolder, description, tag)
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

## Samples

| Name | Description |
|----|----|
| [Save and Insert File API Sample](SaveAndInsertSample_Sample.md) | Demonstrates creating save a new file and then inserting it into a design. To use this sample, have a design open that has been saved and run the script. It will create a new design that contains a cylinder, save it to the same folder the active design was saved to, and then insert it into the active design. |

## Version

Introduced in version March 2015  

