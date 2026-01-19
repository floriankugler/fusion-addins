# InfiniteLine3D.intersectWithCurve Method

Parent Object: [InfiniteLine3D](InfiniteLine3D.md)  

## Description

Intersect this line with a curve to get the intersection point(s).

## Syntax

"infiniteLine3D_var" is a variable referencing an [InfiniteLine3D](InfiniteLine3D.md) object.

```python
returnValue = infiniteLine3D_var.intersectWithCurve(curve)
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

