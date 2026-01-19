# CopyPasteBodies.item Method

Parent Object: [CopyPasteBodies](CopyPasteBodies.md)  

## Description

Function that returns the specified Copy/Paste Body feature using an index into the collection.

## Syntax

"copyPasteBodies_var" is a variable referencing a [CopyPasteBodies](CopyPasteBodies.md) object.

```python
returnValue = copyPasteBodies_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [CopyPasteBody](CopyPasteBody.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Samples

| Name | Description |
|----|----|
| [Copy Paste Bodies API Sample](CopyPasteBodiesSample_Sample.md) | Demonstrates how to use Copy Paste Bodies related API. |

## Version

Introduced in version June 2017  

