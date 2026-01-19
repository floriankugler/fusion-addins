# Matrix2D.getAsCoordinateSystem Method

Parent Object: [Matrix2D](Matrix2D.md)  

## Description

Gets the matrix data as the components that define a coordinate system.

## Syntax

"matrix2D_var" is a variable referencing a [Matrix2D](Matrix2D.md) object.  

```python
(origin, xAxis, yAxis) = matrix2D_var.getAsCoordinateSystem()
```

## Parameters

| Name | Type | Description |
|----|----|----|
| origin | [Point2D](Point2D.md) | The output origin point of the coordinate system. |
| xAxis | [Vector2D](Vector2D.md) | The output x axis direction of the coordinate system. |
| yAxis | [Vector2D](Vector2D.md) | The output y axis direction of the coordinate system. |

## Version

Introduced in version August 2014  

