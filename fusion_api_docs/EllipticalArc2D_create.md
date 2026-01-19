# EllipticalArc2D.create Method

Parent Object: [EllipticalArc2D](EllipticalArc2D.md)  

## Description

Creates a transient 2D elliptical arc

## Syntax

This is a static method.  

```python

returnValue = adsk.core.EllipticalArc2D.create(center, majorAxis, majorRadius, minorRadius, startAngle, endAngle)
```

## Return Value

| Type | Description |
|----|----|
| [EllipticalArc2D](EllipticalArc2D.md) | Returns the newly created elliptical arc or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| center | [Point2D](Point2D.md) | A Point2D object that defines the center of the elliptical arc. |
| majorAxis | [Vector2D](Vector2D.md) | The major axis of the elliptical arc |
| majorRadius | double | The major radius of the of the elliptical arc. |
| minorRadius | double | The minor radius of the of the elliptical arc. |
| startAngle | double | The start angle of the elliptical arc in radians, where 0 is along the major axis. |
| endAngle | double | The end angle of the elliptical arc in radians, where 0 is along the major axis. |

## Version

Introduced in version August 2014  

