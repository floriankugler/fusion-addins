# Plane.intersectWithSurface Method

Parent Object: [Plane](Plane.md)  

## Description

Intersect this plane with a surface to get the intersection point(s).

## Syntax

"plane_var" is a variable referencing a [Plane](Plane.md) object.

```python
returnValue = plane_var.intersectWithSurface(surface)
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

