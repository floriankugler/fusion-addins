# BRepShells.item Method

Parent Object: [BRepShells](BRepShells.md)  

## Description

Function that returns the specified shell using an index into the collection.

## Syntax

"bRepShells_var" is a variable referencing a [BRepShells](BRepShells.md) object.

```python
returnValue = bRepShells_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [BRepShell](BRepShell.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version August 2014  

