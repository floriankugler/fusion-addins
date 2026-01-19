# Ellipse2D.set Method

Parent Object: [Ellipse2D](Ellipse2D.md)  

## Description

Sets all of the data defining the ellipse.

## Syntax

"ellipse2D_var" is a variable referencing an [Ellipse2D](Ellipse2D.md) object.

```python
returnValue = ellipse2D_var.set(center, majorAxis, majorRadius, minorRadius)
```

## Return Value

| Type    | Description                                           |
|---------|-------------------------------------------------------|
| boolean | Returns true if redefining the ellipse is successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| center | [Point2D](Point2D.md) | A Point2D object that defines the center of the ellipse. |
| majorAxis | [Vector2D](Vector2D.md) | The major axis of the ellipse. |
| majorRadius | double | The major radius of the of the ellipse. |
| minorRadius | double | The minor radius of the of the ellipse. |

## Version

Introduced in version August 2014  

