# Cone.create Method

Parent Object: [Cone](Cone.md)  

## Description

Creates a transient cone object.

## Syntax

This is a static method.  

```python

returnValue = adsk.core.Cone.create(origin, axis, radius, halfAngle)
```

## Return Value

| Type | Description |
|----|----|
| [Cone](Cone.md) | Returns the new Cone object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| origin | [Point3D](Point3D.md) | The origin point (center) of the base of the cone. |
| axis | [Vector3D](Vector3D.md) | The center axis (along the length) of the cone that defines its normal direction. |
| radius | double | The radius of the cone. |
| halfAngle | double | The taper half-angle of the cone. |

## Version

Introduced in version August 2014  

