# BRepWires.item Method

Parent Object: [BRepWires](BRepWires.md)  

## Description

Function that returns the specified wire using an index into the collection.

## Syntax

"bRepWires_var" is a variable referencing a [BRepWires](BRepWires.md) object.

```python
returnValue = bRepWires_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [BRepWire](BRepWire.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Samples

| Name | Description |
|----|----|
| [BrepWire Sample](BrepWireSample_Sample.md) | BrepWires and BrepWire related functions |

## Version

Introduced in version December 2017  

