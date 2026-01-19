# CutPasteBodies.item Method

Parent Object: [CutPasteBodies](CutPasteBodies.md)  

## Description

Function that returns the specified Cut/Paste Body feature using an index into the collection.

## Syntax

"cutPasteBodies_var" is a variable referencing a [CutPasteBodies](CutPasteBodies.md) object.

```python
returnValue = cutPasteBodies_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [CutPasteBody](CutPasteBody.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Samples

| Name | Description |
|----|----|
| [Cut Paste Bodies API Sample](CutPasteBodiesSample_Sample.md) | Demonstrates how to use Cut Paste Bodies related API. |

## Version

Introduced in version June 2017  

