# BRepVertices.item Method

Parent Object: [BRepVertices](BRepVertices.md)  

## Description

Function that returns the specified vertex using an index into the collection.

## Syntax

"bRepVertices_var" is a variable referencing a [BRepVertices](BRepVertices.md) object.

```python
returnValue = bRepVertices_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [BRepVertex](BRepVertex.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version August 2014  

