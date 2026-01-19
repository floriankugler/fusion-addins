# BRepWireEdgeDefinitions.item Method

Parent Object: [BRepWireEdgeDefinitions](BRepWireEdgeDefinitions.md)  

## Description

Function that returns the specified BRepWireEdgeDefinition object using an index into the collection.

## Syntax

"bRepWireEdgeDefinitions_var" is a variable referencing a [BRepWireEdgeDefinitions](BRepWireEdgeDefinitions.md) object.

```python
returnValue = bRepWireEdgeDefinitions_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [BRepWireEdgeDefinition](BRepWireEdgeDefinition.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version September 2020  

