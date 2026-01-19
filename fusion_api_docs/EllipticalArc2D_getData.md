# EllipticalArc2D.getData Method

Parent Object: [EllipticalArc2D](EllipticalArc2D.md)  

## Description

Gets all of the data defining the elliptical arc.

## Syntax

"ellipticalArc2D_var" is a variable referencing an [EllipticalArc2D](EllipticalArc2D.md) object.  

```python
(returnValue, center, majorAxis, majorRadius, minorRadius, startAngle, endAngle) = ellipticalArc2D_var.getData()
```

## Return Value

| Type    | Description                |
|---------|----------------------------|
| boolean | Returns true if successful |

## Parameters

| Name | Type | Description |
|----|----|----|
| center | [Point2D](Point2D.md) | The output center point of the elliptical arc. |
| majorAxis | [Vector2D](Vector2D.md) | The output major axis of the elliptical arc. |
| majorRadius | double | The output major radius of the of the elliptical arc. |
| minorRadius | double | The output minor radius of the of the elliptical arc. |
| startAngle | double | The output start angle of the elliptical arc in radians, where 0 is along the major axis. |
| endAngle | double | The output end angle of the elliptical arc in radians, where 0 is along the major axis. |

## Version

Introduced in version August 2014  

