# BRepBodyDefinition.createVertexDefinition Method

Parent Object: [BRepBodyDefinition](BRepBodyDefinition.md)  

## Description

Creates a new BRepVertexDefinition object that's associated with the body.

## Syntax

"bRepBodyDefinition_var" is a variable referencing a [BRepBodyDefinition](BRepBodyDefinition.md) object.

```python
returnValue = bRepBodyDefinition_var.createVertexDefinition(position)
```

## Return Value

| Type | Description |
|----|----|
| [BRepVertexDefinition](BRepVertexDefinition.md) | Returns the created BRepVertexDefinition object or null in the case of failure. |

## Parameters

| Name | Type | Description |
|----|----|----|
| position | [Point3D](Point3D.md) | Specifies the position of the vertex in model space. |

## Samples

| Name | Description |
|----|----|
| [BRep Body definition Sample](BRepBodyDefinition_Sample.md) | Demonstrates creating BRep bodies by BRepBodyDefinition. |

## Version

Introduced in version September 2020  

