# BRepCells.item Method

Parent Object: [BRepCells](BRepCells.md)  

## Description

Function that returns the specified BRepCell using an index into the collection.

## Syntax

"bRepCells_var" is a variable referencing a [BRepCells](BRepCells.md) object.

```python
returnValue = bRepCells_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [BRepCell](BRepCell.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Samples

| Name | Description |
|----|----|
| [boundaryFillFeatures.add](boundaryFillFeatures_add_Sample.md) | Demonstrates the boundaryFill.add method. To use this sample you need to have two existing overlapping bodies. You'll be prompted to select the bodies when running the script. |
| [Boundary Fill Feature API Sample](BoundaryFillFeatureSample_Sample.md) | Demonstrates creating a new boundary fill feature. |
| [Trim Feature API Sample](TrimFeatureSample_Sample.md) | Demonstrates creating a new trim feature. |

## Version

Introduced in version June 2015  

