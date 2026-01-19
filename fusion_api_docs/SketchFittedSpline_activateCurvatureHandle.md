# SketchFittedSpline.activateCurvatureHandle Method

Parent Object: [SketchFittedSpline](SketchFittedSpline.md)  

## Description

Activates the curvature handle for the specified fit point and returns the sketch arc that acts as the handle to control the curvature. You can use the getCurvatureHandle property to determine if the curvature handle has already been activated. If this method is called for a handle that already exists, nothing changes and the existing sketch arc that acts as the curvature handle is returned.  

The getCurvatureHandle method can be used to determine if the handle has already been activated.  

To deactivate a sketch handle you can delete the sketch arc.

## Syntax

"sketchFittedSpline_var" is a variable referencing a [SketchFittedSpline](SketchFittedSpline.md) object.

```python
returnValue = sketchFittedSpline_var.activateCurvatureHandle(fitPoint)
```

## Return Value

| Type | Description |
|----|----|
| [SketchArc](SketchArc.md) | Returns the sketch arc that acts as the curvature handle at the specified fit point. |

## Parameters

| Name | Type | Description |
|----|----|----|
| fitPoint | [SketchPoint](SketchPoint.md) | The fit point on the curve where you want to activate the curvature handle. The fit points can be obtained by using the fitPoints property of the SketchFittedSpline object. |

## Samples

| Name | Description |
|----|----|
| [Sketch spline through points creation and relative functions API Sample](SketchSplineThroughPoints_Sample.md) | Create a sketch spline with points and use some operations for spline tangent handle & curvature handle. |

## Version

Introduced in version April 2019  

