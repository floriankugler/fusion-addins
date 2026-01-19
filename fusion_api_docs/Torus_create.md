# Torus.create Method

Parent Object: [Torus](Torus.md)  

## Description

Creates a transient torus object.

## Syntax

This is a static method.  

```python

returnValue = adsk.core.Torus.create(origin, axis, majorRadius, minorRadius)
```

## Return Value

| Type | Description |
|----|----|
| [Torus](Torus.md) | Returns the new Torus object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| origin | [Point3D](Point3D.md) | The origin point (center) of the torus. |
| axis | [Vector3D](Vector3D.md) | The center axis of the torus. |
| majorRadius | double | The major radius of the torus. |
| minorRadius | double | The minor radius of the torus. |

## Version

Introduced in version August 2014  

