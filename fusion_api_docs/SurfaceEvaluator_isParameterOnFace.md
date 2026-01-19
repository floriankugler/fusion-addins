# SurfaceEvaluator.isParameterOnFace Method

Parent Object: [SurfaceEvaluator](SurfaceEvaluator.md)  

## Description

Determines if the specified parameter position lies within the surface. When the SurfaceEvaluator is obtained from a BRepFace object, this will respect the boundaries of the face and return true when point is on the visible portion of the surface. When obtained from surface geometry it returns true if the point is within the parametric range of surface.

## Syntax

"surfaceEvaluator_var" is a variable referencing a [SurfaceEvaluator](SurfaceEvaluator.md) object.

```python
returnValue = surfaceEvaluator_var.isParameterOnFace(parameter)
```

## Return Value

| Type    | Description                                                     |
|---------|-----------------------------------------------------------------|
| boolean | Returns true if the parameter position lies within the surface. |

## Parameters

| Name      | Type                   | Description                     |
|-----------|------------------------|---------------------------------|
| parameter | [Point2D](Point2D.md) | The parameter position to test. |

## Version

Introduced in version August 2014  

