# EllipticalArc2D.set Method

Parent Object: [EllipticalArc2D](EllipticalArc2D.md)  

## Description

Sets all of the data defining the elliptical arc.

## Syntax

"ellipticalArc2D_var" is a variable referencing an [EllipticalArc2D](EllipticalArc2D.md) object.

```python
returnValue = ellipticalArc2D_var.set(center, majorAxis, majorRadius, minorRadius, startAngle, endAngle)
```

## Return Value

| Type    | Description                                                 |
|---------|-------------------------------------------------------------|
| boolean | Returns true if redefining the elliptical arc is successful |

## Parameters

| Name | Type | Description |
|----|----|----|
| center | [Point2D](Point2D.md) | A Point2D object that defines the center of the elliptical arc. |
| majorAxis | [Vector2D](Vector2D.md) | The major axis of the elliptical arc. |
| majorRadius | double | The major radius of the of the elliptical arc. |
| minorRadius | double | The minor radius of the of the elliptical arc. |
| startAngle | double | The start angle of the elliptical arc in radians, where 0 is along the major axis. |
| endAngle | double | The end angle of the elliptical arc in radians, where 0 is along the major axis. |

## Version

Introduced in version August 2014  

