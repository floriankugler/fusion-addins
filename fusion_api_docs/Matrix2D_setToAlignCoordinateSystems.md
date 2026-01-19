# Matrix2D.setToAlignCoordinateSystems Method

Parent Object: [Matrix2D](Matrix2D.md)  

## Description

Sets this matrix to be the matrix that maps from the 'from' coordinate system to the 'to' coordinate system.

## Syntax

"matrix2D_var" is a variable referencing a [Matrix2D](Matrix2D.md) object.

```python
returnValue = matrix2D_var.setToAlignCoordinateSystems(fromOrigin, fromXAxis, fromYAxis, toOrigin, toXAxis, toYAxis)
```

## Return Value

| Type    | Description                 |
|---------|-----------------------------|
| boolean | Returns true if successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| fromOrigin | [Point2D](Point2D.md) | The origin point of the from coordinate system. |
| fromXAxis | [Vector2D](Vector2D.md) | The x axis direction of the from coordinate system. |
| fromYAxis | [Vector2D](Vector2D.md) | The y axis direction of the from coordinate system. |
| toOrigin | [Point2D](Point2D.md) | The origin point of the to coordinate system. |
| toXAxis | [Vector2D](Vector2D.md) | The x axis direction of the to coordinate system. |
| toYAxis | [Vector2D](Vector2D.md) | The y axis direction of the to coordinate system. |

## Version

Introduced in version August 2014  

