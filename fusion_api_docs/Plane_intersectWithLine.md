# Plane.intersectWithLine Method

Parent Object: [Plane](Plane.md)  

## Description

Creates a 3D point at the intersection of this plane and a line.

## Syntax

"plane_var" is a variable referencing a [Plane](Plane.md) object.

```python
returnValue = plane_var.intersectWithLine(line)
```

## Return Value

| Type | Description |
|----|----|
| [Point3D](Point3D.md) | Returns a Point3D object or null if the plane and line do not intersect (are parallel). |

## Parameters

| Name | Type                                 | Description                 |
|------|--------------------------------------|-----------------------------|
| line | [InfiniteLine3D](InfiniteLine3D.md) | The line to intersect with. |

## Version

Introduced in version August 2014  

