# EllipticalCone.getAxes Method

Parent Object: [EllipticalCone](EllipticalCone.md)  

## Description

Gets the center axis of the cone that defines its normal direction and the major axis direction of the ellipse that defines it.

## Syntax

"ellipticalCone_var" is a variable referencing an [EllipticalCone](EllipticalCone.md) object.  

```python
(axis, majorAxisDirection) = ellipticalCone_var.getAxes()
```

## Parameters

| Name | Type | Description |
|----|----|----|
| axis | [Vector3D](Vector3D.md) | The output center axis (along the length) of the cone that defines its normal direction. |
| majorAxisDirection | [Vector3D](Vector3D.md) | The output direction of the major axis of the ellipse that defines the cone. |

## Version

Introduced in version August 2014  

