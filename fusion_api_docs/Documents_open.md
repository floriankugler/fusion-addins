# Documents.open Method

Parent Object: [Documents](Documents.md)  

## Description

Opens an item that has previously been saved.

## Syntax

"documents_var" is a variable referencing a [Documents](Documents.md) object.

```python
# Uses no optional arguments.
returnValue = documents_var.open(dataFile)

# Uses optional arguments.
returnValue = documents_var.open(dataFile, visible)
```

## Return Value

| Type | Description |
|----|----|
| [Document](Document.md) | Returns the open document or null if the open failed. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| dataFile | [DataFile](DataFile.md) | The item to open. |
| visible | boolean | Specifies if the document should be opened visibly or not. This is an optional argument whose default value is True. |

## Version

Introduced in version March 2015  

