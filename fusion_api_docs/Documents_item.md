# Documents.item Method

Parent Object: [Documents](Documents.md)  

## Description

Function that returns the specified document using an index into the collection.

## Syntax

"documents_var" is a variable referencing a [Documents](Documents.md) object.

```python
returnValue = documents_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [Document](Document.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version August 2014  

