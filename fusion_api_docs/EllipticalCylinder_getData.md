# EllipticalCylinder.getData Method

Parent Object: [EllipticalCylinder](EllipticalCylinder.md)  

## Description

Gets the data defining the elliptical cylinder.

## Syntax

"ellipticalCylinder_var" is a variable referencing an [EllipticalCylinder](EllipticalCylinder.md) object.  

```python
(returnValue, origin, axis, majorAxis, majorRadius, minorRadius) = ellipticalCylinder_var.getData()
```

## Return Value

| Type    | Description                 |
|---------|-----------------------------|
| boolean | Returns true if successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| origin | [Point3D](Point3D.md) | The output origin point (center) of the base of the cylinder. |
| axis | [Vector3D](Vector3D.md) | The output center axis (along the length) of the cylinder that defines its normal direction. |
| majorAxis | [Vector3D](Vector3D.md) | The output direction of the major axis of the ellipse that defines the cylinder. |
| majorRadius | double | The output major radius of the ellipse that defines the cylinder. |
| minorRadius | double | The output minor radius of the ellipse that defines the cylinder. |

## Version

Introduced in version August 2014  

