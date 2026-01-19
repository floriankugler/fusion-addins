# JointGeometry.createByTwoEdgeIntersection Method

Parent Object: [JointGeometry](JointGeometry.md)  

## Description

Creates a new transient JointGeometry object that is positioned at the intersection of the two input linear BRepEdge objects.

## Syntax

This is a static method.  

```python

returnValue = adsk.fusion.JointGeometry.createByTwoEdgeIntersection(edgeOne, edgeTwo)
```

## Return Value

| Type | Description |
|----|----|
| [JointGeometry](JointGeometry.md) | Returns the transient JointGeometry object that can be used to create a joint or joint origin or null in case of a failure. |

## Parameters

| Name | Type | Description |
|----|----|----|
| edgeOne | [BRepEdge](BRepEdge.md) | The first linear BRepEdge object. |
| edgeTwo | [BRepEdge](BRepEdge.md) | The second linear BRepEdge object. This edge must exist either on the same body as edgeOne or on a body in the same component as edgeOne. edgeOne and edgeTwo must also both lie on the same plane and must intersect, they cannot be parallel. |

## Version

Introduced in version September 2022  

