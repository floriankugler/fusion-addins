# BRepLoops.item Method

Parent Object: [BRepLoops](BRepLoops.md)  

## Description

Function that returns the specified loop using an index into the collection.

## Syntax

"bRepLoops_var" is a variable referencing a [BRepLoops](BRepLoops.md) object.

```python
returnValue = bRepLoops_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [BRepLoop](BRepLoop.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Samples

| Name | Description |
|----|----|
| [Patch Feature API Sample](PatchFeatureSample_Sample.md) | Demonstrates creating a new patch feature. |

## Version

Introduced in version August 2014  

