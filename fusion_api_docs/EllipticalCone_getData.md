# EllipticalCone.getData Method

Parent Object: [EllipticalCone](EllipticalCone.md)  

## Description

Gets the data that defines the Elliptical Cone.

## Syntax

"ellipticalCone_var" is a variable referencing an [EllipticalCone](EllipticalCone.md) object.  

```python
(returnValue, origin, axis, majorAxisDirection, majorRadius, minorRadius, halfAngle) = ellipticalCone_var.getData()
```

## Return Value

| Type    | Description                 |
|---------|-----------------------------|
| boolean | Returns true if successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| origin | [Point3D](Point3D.md) | The output origin point (center) of the base of the cone. |
| axis | [Vector3D](Vector3D.md) | The output center axis (along the length) of the cone that defines its normal direction. |
| majorAxisDirection | [Vector3D](Vector3D.md) | The output direction of the major axis of the ellipse that defines the cone. |
| majorRadius | double | The output major radius of the ellipse that defines the cone. |
| minorRadius | double | The output minor radius of the ellipse that defines the cone. |
| halfAngle | double | The output taper half-angle of the cone. |

## Version

Introduced in version August 2014  

