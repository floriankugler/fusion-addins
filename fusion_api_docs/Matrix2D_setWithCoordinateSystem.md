# Matrix2D.setWithCoordinateSystem Method

Parent Object: [Matrix2D](Matrix2D.md)  

## Description

Reset this matrix to align with a specific coordinate system.

## Syntax

"matrix2D_var" is a variable referencing a [Matrix2D](Matrix2D.md) object.

```python
returnValue = matrix2D_var.setWithCoordinateSystem(origin, xAxis, yAxis)
```

## Return Value

| Type    | Description                 |
|---------|-----------------------------|
| boolean | Returns true if successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| origin | [Point2D](Point2D.md) | The origin point of the coordinate system. |
| xAxis | [Vector2D](Vector2D.md) | The x axis direction of the coordinate system. |
| yAxis | [Vector2D](Vector2D.md) | The y axis direction of the coordinate system. |

## Version

Introduced in version August 2014  

