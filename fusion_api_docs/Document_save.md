# Document.save Method

Parent Object: [Document](Document.md)  

## Description

Saves a version of the current document. You must use the SaveAs method the first time a document is saved. You can determine if a document has been saved by checking the value of the isSaved property.

## Remarks

Saving a document is not supported within any of the Command related events. When a command is running, a transaction is open, and saving a document cannot be transacted and, as a result, cannot be contained within a command transaction.

## Syntax

"document_var" is a variable referencing a [Document](Document.md) object.

```python
returnValue = document_var.save(description)
```

## Return Value

| Type    | Description                                         |
|---------|-----------------------------------------------------|
| boolean | Returns true if saving the document was successful. |

## Parameters

| Name        | Type   | Description                               |
|-------------|--------|-------------------------------------------|
| description | string | The version description for this document |

## Version

Introduced in version November 2014  

