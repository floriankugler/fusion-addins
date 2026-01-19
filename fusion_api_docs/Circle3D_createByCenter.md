# Circle3D.createByCenter Method

Parent Object: [Circle3D](Circle3D.md)  

## Description

Creates a transient 3D circle object by specifying a center and radius.

## Syntax

This is a static method.  

```python

returnValue = adsk.core.Circle3D.createByCenter(center, normal, radius)
```

## Return Value

| Type | Description |
|----|----|
| [Circle3D](Circle3D.md) | Returns the new Circle3D object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| center | [Point3D](Point3D.md) | The center point of the circle. |
| normal | [Vector3D](Vector3D.md) | The normal vector of the circle. The plane through the center point and perpendicular to the normal vector defines the plane of the circle. |
| radius | double | The radius of the circle. |

## Version

Introduced in version August 2014  

