# EllipticalCylinder.create Method

Parent Object: [EllipticalCylinder](EllipticalCylinder.md)  

## Description

Creates a transient 3D elliptical cylinder object.

## Syntax

This is a static method.  

```python

returnValue = adsk.core.EllipticalCylinder.create(origin, axis, majorAxis, majorRadius, minorRadius)
```

## Return Value

| Type | Description |
|----|----|
| [EllipticalCylinder](EllipticalCylinder.md) | Returns the new EllipticalCylinder object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| origin | [Point3D](Point3D.md) | The origin point (center) of the base of the cylinder. |
| axis | [Vector3D](Vector3D.md) | The center axis (along the length) of the cylinder that defines its normal direction. |
| majorAxis | [Vector3D](Vector3D.md) | The direction of the major axis of the ellipse that defines the cylinder. |
| majorRadius | double | The major radius of the ellipse that defines the cylinder. |
| minorRadius | double | The minor radius of the ellipse that defines the cylinder. |

## Version

Introduced in version August 2014  

