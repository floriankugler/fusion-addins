# InfiniteLine3D.intersectWithSurface Method

Parent Object: [InfiniteLine3D](InfiniteLine3D.md)  

## Description

Intersect this line with a surface to get the intersection point(s).

## Syntax

"infiniteLine3D_var" is a variable referencing an [InfiniteLine3D](InfiniteLine3D.md) object.

```python
returnValue = infiniteLine3D_var.intersectWithSurface(surface)
```

## Return Value

| Type | Description |
|----|----|
| [ObjectCollection](ObjectCollection.md) | Returns a collection of the intersection points. |

## Parameters

| Name | Type | Description |
|----|----|----|
| surface | [Surface](Surface.md) | The intersecting surface. The surface can be a Plane, Cone, Cylinder, EllipticalCone, EllipticalCylinder, Sphere, Torus, or a NurbsSurface. |

## Version

Introduced in version August 2014  

