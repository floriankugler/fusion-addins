# EllipticalCylinder.set Method

Parent Object: [EllipticalCylinder](EllipticalCylinder.md)  

## Description

Sets the data defining the elliptical cylinder.

## Syntax

"ellipticalCylinder_var" is a variable referencing an [EllipticalCylinder](EllipticalCylinder.md) object.

```python
returnValue = ellipticalCylinder_var.set(origin, axis, majorAxis, majorRadius, minorRadius)
```

## Return Value

| Type    | Description                 |
|---------|-----------------------------|
| boolean | Returns true if successful. |

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

