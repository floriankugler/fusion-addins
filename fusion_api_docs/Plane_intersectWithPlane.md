# Plane.intersectWithPlane Method

Parent Object: [Plane](Plane.md)  

## Description

Creates an infinite line at the intersection of this plane with another plane.

## Syntax

"plane_var" is a variable referencing a [Plane](Plane.md) object.

```python
returnValue = plane_var.intersectWithPlane(plane)
```

## Return Value

| Type | Description |
|----|----|
| [InfiniteLine3D](InfiniteLine3D.md) | Returns an InfiniteLine3D object or null if the planes do not intersect (are parallel). |

## Parameters

| Name  | Type               | Description                  |
|-------|--------------------|------------------------------|
| plane | [Plane](Plane.md) | The plane to intersect with. |

## Version

Introduced in version August 2014  

