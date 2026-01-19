# EllipticalCone.create Method

Parent Object: [EllipticalCone](EllipticalCone.md)  

## Description

Creates a transient elliptical cone object.

## Syntax

This is a static method.  

```python

returnValue = adsk.core.EllipticalCone.create(origin, axis, majorAxisDirection, majorRadius, minorRadius, halfAngle)
```

## Return Value

| Type | Description |
|----|----|
| [EllipticalCone](EllipticalCone.md) | Returns the new EllipticalCone object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| origin | [Point3D](Point3D.md) | The origin point (center) of the base of the cone. |
| axis | [Vector3D](Vector3D.md) | The center axis (along the length) of the cone that defines its normal direction. |
| majorAxisDirection | [Vector3D](Vector3D.md) | The direction of the major axis of the ellipse that defines the cone. |
| majorRadius | double | The major radius of the ellipse that defines the cone. |
| minorRadius | double | The minor radius of the ellipse that defines the cone. |
| halfAngle | double | The taper half-angle of the cone. |

## Version

Introduced in version August 2014  

