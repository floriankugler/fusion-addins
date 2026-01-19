# EllipticalCone.setAxes Method

Parent Object: [EllipticalCone](EllipticalCone.md)  

## Description

Sets the center axis of the cone and the major axis direction of the ellipse that defines it.

## Syntax

"ellipticalCone_var" is a variable referencing an [EllipticalCone](EllipticalCone.md) object.

```python
returnValue = ellipticalCone_var.setAxes(axis, majorAxisDirection)
```

## Return Value

| Type    | Description                 |
|---------|-----------------------------|
| boolean | Returns true if successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| axis | [Vector3D](Vector3D.md) | The center axis (along the length) of the cone that defines its normal direction. |
| majorAxisDirection | [Vector3D](Vector3D.md) | The direction of the major axis of the ellipse that defines the cone. |

## Version

Introduced in version August 2014  

