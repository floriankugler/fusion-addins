# SurfaceEvaluator.parametricRange Method

Parent Object: [SurfaceEvaluator](SurfaceEvaluator.md)  

## Description

Returns the parametric range of the surface. If the surface is periodic in a direction, the range is set to the principle period's range. If the surface is only upper bounded in a direction, the lower bound is set to -double-max. If the surface is only lower bounded in a direction, the upper bound is set to double-max. If the surface is unbounded in a direction, the lower bound and upper bound of the range will both be zero.

## Syntax

"surfaceEvaluator_var" is a variable referencing a [SurfaceEvaluator](SurfaceEvaluator.md) object.

```python
returnValue = surfaceEvaluator_var.parametricRange()
```

## Return Value

| Type | Description |
|----|----|
| [BoundingBox2D](BoundingBox2D.md) | Returns the bounding box with the parameter extents, with the X value being the U range, and the Y value being the V range. |

## Version

Introduced in version August 2014  

