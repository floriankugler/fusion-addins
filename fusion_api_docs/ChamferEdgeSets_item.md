# ChamferEdgeSets.item Method

Parent Object: [ChamferEdgeSets](ChamferEdgeSets.md)  

## Description

Function that returns the specified chamfer edge set using an index into the collection.

## Syntax

"chamferEdgeSets_var" is a variable referencing a [ChamferEdgeSets](ChamferEdgeSets.md) object.

```python
returnValue = chamferEdgeSets_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [ChamferEdgeSet](ChamferEdgeSet.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version December 2020  

