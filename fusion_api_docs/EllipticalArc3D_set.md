# EllipticalArc3D.set Method

Parent Object: [EllipticalArc3D](EllipticalArc3D.md)  

## Description

Sets all of the data defining the elliptical arc.

## Syntax

"ellipticalArc3D_var" is a variable referencing an [EllipticalArc3D](EllipticalArc3D.md) object.

```python
returnValue = ellipticalArc3D_var.set(center, normal, majorAxis, majorRadius, minorRadius, startAngle, endAngle)
```

## Return Value

| Type    | Description                 |
|---------|-----------------------------|
| boolean | Returns true if successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| center | [Point3D](Point3D.md) | The center point of the elliptical arc. |
| normal | [Vector3D](Vector3D.md) | The normal vector of the elliptical arc. |
| majorAxis | [Vector3D](Vector3D.md) | The major axis of the elliptical arc. |
| majorRadius | double | The major radius of the of the elliptical arc. |
| minorRadius | double | The minor radius of the of the elliptical arc. |
| startAngle | double | The start angle of the elliptical arc in radians, where 0 is along the major axis. |
| endAngle | double | The end angle of the elliptical arc in radians, where 0 is along the major axis. |

## Version

Introduced in version August 2014  

