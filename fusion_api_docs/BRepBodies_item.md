# BRepBodies.item Method

Parent Object: [BRepBodies](BRepBodies.md)  

## Description

Function that returns the specified body using an index into the collection.

## Syntax

"bRepBodies_var" is a variable referencing a [BRepBodies](BRepBodies.md) object.

```python
returnValue = bRepBodies_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [BRepBody](BRepBody.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Samples

| Name | Description |
|----|----|
| [Get Volume of Active Design API Sample](GetsVolumeOfActiveDesign_Sample.md) | Traverses through the active design and totals the volume of every body within the design. |

## Version

Introduced in version August 2014  

