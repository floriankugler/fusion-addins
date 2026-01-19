# Ellipse3D.create Method

Parent Object: [Ellipse3D](Ellipse3D.md)  

## Description

Creates a transient 3D ellipse object.

## Syntax

This is a static method.  

```python

returnValue = adsk.core.Ellipse3D.create(center, normal, majorAxis, majorRadius, minorRadius)
```

## Return Value

| Type | Description |
|----|----|
| [Ellipse3D](Ellipse3D.md) | Returns the new Ellipse 3D object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| center | [Point3D](Point3D.md) | The center point of the ellipse. |
| normal | [Vector3D](Vector3D.md) | The normal vector of the ellipse. The plane through the center point and perpendicular to the normal vector defines the plane of the ellipse. |
| majorAxis | [Vector3D](Vector3D.md) | The major axis of the ellipse |
| majorRadius | double | The major radius of the of the ellipse. |
| minorRadius | double | The minor radius of the of the ellipse. |

## Version

Introduced in version August 2014  

