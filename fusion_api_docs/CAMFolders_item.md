# CAMFolders.item Method

Parent Object: [CAMFolders](CAMFolders.md)  

## Description

Function that returns the specified folder using an index into the collection.

## Syntax

"cAMFolders_var" is a variable referencing a [CAMFolders](CAMFolders.md) object.

```python
returnValue = cAMFolders_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [CAMFolder](CAMFolder.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version January 2016  

