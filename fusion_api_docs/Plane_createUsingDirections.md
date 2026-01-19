# Plane.createUsingDirections Method

Parent Object: [Plane](Plane.md)  

## Description

Creates a transient plane object by specifying an origin along with U and V directions.

## Syntax

This is a static method.  

```python

returnValue = adsk.core.Plane.createUsingDirections(origin, uDirection, vDirection)
```

## Return Value

| Type | Description |
|----|----|
| [Plane](Plane.md) | Returns the new plane object or null if the creation failed. |

## Parameters

| Name       | Type                     | Description                    |
|------------|--------------------------|--------------------------------|
| origin     | [Point3D](Point3D.md)   | The origin point of the plane. |
| uDirection | [Vector3D](Vector3D.md) | The U direction for the plane. |
| vDirection | [Vector3D](Vector3D.md) | The V direction for the plane. |

## Version

Introduced in version August 2014  

