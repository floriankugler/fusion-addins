# Plane.create Method

Parent Object: [Plane](Plane.md)  

## Description

Creates a transient plane object by specifying an origin and a normal direction.

## Syntax

This is a static method.  

```python

returnValue = adsk.core.Plane.create(origin, normal)
```

## Return Value

| Type | Description |
|----|----|
| [Plane](Plane.md) | Returns the new plane object or null if the creation failed. |

## Parameters

| Name   | Type                     | Description                        |
|--------|--------------------------|------------------------------------|
| origin | [Point3D](Point3D.md)   | The origin point of the plane.     |
| normal | [Vector3D](Vector3D.md) | The normal direction of the plane. |

## Version

Introduced in version August 2014  

