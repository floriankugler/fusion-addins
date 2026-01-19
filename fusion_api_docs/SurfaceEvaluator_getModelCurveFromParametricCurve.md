# SurfaceEvaluator.getModelCurveFromParametricCurve Method

Parent Object: [SurfaceEvaluator](SurfaceEvaluator.md)  

## Description

Creates the 3D equivalent curve in model space, of a 2D curve defined in the parametric space of the surface.

## Syntax

"surfaceEvaluator_var" is a variable referencing a [SurfaceEvaluator](SurfaceEvaluator.md) object.

```python
returnValue = surfaceEvaluator_var.getModelCurveFromParametricCurve(parametricCurve)
```

## Return Value

| Type | Description |
|----|----|
| [ObjectCollection](ObjectCollection.md) | Returns an ObjectCollection containing one or more curves. When the SufaceEvaluatior is obtained from a face, and the curve cuts across internal boundaries of the face, multiple curves are returned. The returned curves are trimmed to the boundaries of the face. If the SurfaceEvaluator is obtained from a geometry object, a single curve returned because there are no boundaries with which to trim the curve. The type of curve(s) returned depends on the shape of the input curve and surface. |

## Parameters

| Name | Type | Description |
|----|----|----|
| parametricCurve | [Curve2D](Curve2D.md) | The parameter space curve to map into this surface's parameter space. |

## Version

Introduced in version August 2014  

