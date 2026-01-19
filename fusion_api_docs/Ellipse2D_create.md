# Ellipse2D.create Method

Parent Object: [Ellipse2D](Ellipse2D.md)  

## Description

Creates a transient 2D ellipse by specifying a center position, major and minor axes, and major and minor radii.

## Syntax

This is a static method.  

```python

returnValue = adsk.core.Ellipse2D.create(center, majorAxis, majorRadius, minorRadius)
```

## Return Value

| Type | Description |
|----|----|
| [Ellipse2D](Ellipse2D.md) | Returns the new Ellipse 2D object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| center | [Point2D](Point2D.md) | A Point2D object that defines the center of the ellipse. |
| majorAxis | [Vector2D](Vector2D.md) | The major axis of the ellipse |
| majorRadius | double | The major radius of the of the ellipse. |
| minorRadius | double | The minor radius of the of the ellipse. |

## Version

Introduced in version August 2014  

