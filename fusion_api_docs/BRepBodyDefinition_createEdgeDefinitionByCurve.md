# BRepBodyDefinition.createEdgeDefinitionByCurve Method

Parent Object: [BRepBodyDefinition](BRepBodyDefinition.md)  

## Description

Using a curve in model space it creates a new BRepEdgeDefinition object that's associated with the body.

## Syntax

"bRepBodyDefinition_var" is a variable referencing a [BRepBodyDefinition](BRepBodyDefinition.md) object.

```python
returnValue = bRepBodyDefinition_var.createEdgeDefinitionByCurve(startVertex, endVertex, modelSpaceCurve)
```

## Return Value

| Type | Description |
|----|----|
| [BRepEdgeDefinition](BRepEdgeDefinition.md) | Returns the created BRepEdgeDefinition object or null in the case of failure. |

## Parameters

| Name | Type | Description |
|----|----|----|
| startVertex | [BRepVertexDefinition](BRepVertexDefinition.md) | Vertex definition that defines the start of the edge. For a closed curve, like a circle, you still need to provide a vertex on the curve but you should use the same BRepVertexDefinition for both the start and end vertices. |
| endVertex | [BRepVertexDefinition](BRepVertexDefinition.md) | Vertex definition that defines the end of the edge. For a closed curve, like a circle, this should be the same vertex as used for the start vertex. |
| modelSpaceCurve | [Curve3D](Curve3D.md) | A Curve3D object that defines the shape of the edge using 3D geometry in model space. Valid input is an Arc3D, NurbsCurve3D, Circle3D, Ellipse3D, EllipticalArc3D, or Line3D. |

## Samples

| Name | Description |
|----|----|
| [BRep Body definition Sample](BRepBodyDefinition_Sample.md) | Demonstrates creating BRep bodies by BRepBodyDefinition. |

## Version

Introduced in version September 2020  

