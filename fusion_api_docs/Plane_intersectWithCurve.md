# Plane.intersectWithCurve Method

Parent Object: [Plane](Plane.md)  

## Description

Intersect this plane with a curve to get the intersection point(s).

## Syntax

"plane_var" is a variable referencing a [Plane](Plane.md) object.

```python
returnValue = plane_var.intersectWithCurve(curve)
```

## Return Value

| Type | Description |
|----|----|
| [ObjectCollection](ObjectCollection.md) | Returns a collection of the intersection points. |

## Parameters

| Name | Type | Description |
|----|----|----|
| curve | [Curve3D](Curve3D.md) | The intersecting curve. The curve can be a Line3D, InfininteLine3D, Circle3D, Arc3D, EllipticalArc3D, Ellipse3D, or NurbsCurve3D. |

## Version

Introduced in version August 2014  

