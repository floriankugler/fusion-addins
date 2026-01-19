# BRepWireEdgeDefinitions.add Method

Parent Object: [BRepWireEdgeDefinitions](BRepWireEdgeDefinitions.md)  

## Description

Creates a new BRepWireEdgeDefinition object associated with the parent BRepWireDefinition object.

## Syntax

"bRepWireEdgeDefinitions_var" is a variable referencing a [BRepWireEdgeDefinitions](BRepWireEdgeDefinitions.md) object.

```python
returnValue = bRepWireEdgeDefinitions_var.add(startVertex, endVertex, modelSpaceCurve)
```

## Return Value

| Type | Description |
|----|----|
| [BRepWireEdgeDefinition](BRepWireEdgeDefinition.md) | Returns the newly created BRepWireEdgeDefinition object or null in the case of failure. |

## Parameters

| Name | Type | Description |
|----|----|----|
| startVertex | [BRepVertexDefinition](BRepVertexDefinition.md) | Vertex definition that defines the start of the edge. For a closed curve, like a circle, you still need to provide a vertex on the curve but should use the same BRepVertexDefinition for both the start and end vertices. |
| endVertex | [BRepVertexDefinition](BRepVertexDefinition.md) | Vertex definition that defines the end of the edge. For a closed curve, like a circle, this should be the same vertex as used for the start vertex. |
| modelSpaceCurve | [Curve3D](Curve3D.md) | A Curve3D object that defines the shape of the edge using 3D geometry in model space. Valid input is an Arc3D, NurbsCurve3D, Circle3D, Ellipse3D, EllipticalArc3D, or Line3D. |

## Samples

| Name | Description |
|----|----|
| [BRep Body definition Sample](BRepBodyDefinition_Sample.md) | Demonstrates creating BRep bodies by BRepBodyDefinition. |

## Version

Introduced in version September 2020  

