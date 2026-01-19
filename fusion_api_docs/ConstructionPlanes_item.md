# ConstructionPlanes.item Method

Parent Object: [ConstructionPlanes](ConstructionPlanes.md)  

## Description

Function that returns the specified construction plane using an index into the collection.

## Syntax

"constructionPlanes_var" is a variable referencing a [ConstructionPlanes](ConstructionPlanes.md) object.

```python
returnValue = constructionPlanes_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [ConstructionPlane](ConstructionPlane.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version August 2014  

