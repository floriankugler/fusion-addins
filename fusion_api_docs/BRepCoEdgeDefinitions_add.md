# BRepCoEdgeDefinitions.add Method

Parent Object: [BRepCoEdgeDefinitions](BRepCoEdgeDefinitions.md)  

## Description

Creates a new BrepCoEdgeDefinition object associated with the parent BrepLoopDefinition object.

## Syntax

"bRepCoEdgeDefinitions_var" is a variable referencing a [BRepCoEdgeDefinitions](BRepCoEdgeDefinitions.md) object.

```python
returnValue = bRepCoEdgeDefinitions_var.add(edgeDefinition, isOpposedToEdge)
```

## Return Value

| Type | Description |
|----|----|
| [BRepCoEdgeDefinition](BRepCoEdgeDefinition.md) | Returns the newly created BrepCoEdgeDefinition object or null in the case of failure. |

## Parameters

| Name | Type | Description |
|----|----|----|
| edgeDefinition | [BRepEdgeDefinition](BRepEdgeDefinition.md) | The BRepEdgeDefinition object this co-edge is related to. |
| isOpposedToEdge | boolean | Boolean that indicates if the orientation of this BRepCoEdgeDefinition is reversed with respect to the associated BRepEdgeDefinition object. |

## Samples

| Name | Description |
|----|----|
| [BRep Body definition Sample](BRepBodyDefinition_Sample.md) | Demonstrates creating BRep bodies by BRepBodyDefinition. |

## Version

Introduced in version September 2020  

