# Ellipse2D.getData Method

Parent Object: [Ellipse2D](Ellipse2D.md)  

## Description

Gets all of the data defining the ellipse.

## Syntax

"ellipse2D_var" is a variable referencing an [Ellipse2D](Ellipse2D.md) object.  

```python
(returnValue, center, majorAxis, majorRadius, minorRadius) = ellipse2D_var.getData()
```

## Return Value

| Type    | Description                 |
|---------|-----------------------------|
| boolean | Returns true if successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| center | [Point2D](Point2D.md) | The output center point of the ellipse. |
| majorAxis | [Vector2D](Vector2D.md) | The output major axis of the ellipse. |
| majorRadius | double | The output major radius of the of the ellipse. |
| minorRadius | double | The output minor radius of the of the ellipse. |

## Version

Introduced in version August 2014  

