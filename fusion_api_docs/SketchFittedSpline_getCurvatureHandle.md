# SketchFittedSpline.getCurvatureHandle Method

Parent Object: [SketchFittedSpline](SketchFittedSpline.md)  

## Description

Returns the sketch arc that acts as the handle to control the curvature at the specified fit point. Returns null in the case where the curvature handle has not been activated at that sketch point. Deleting the returned arc will deactivate the curvature handle. Use the activateCurvatureHandle method to activate the curvature handle.

## Syntax

"sketchFittedSpline_var" is a variable referencing a [SketchFittedSpline](SketchFittedSpline.md) object.

```python
returnValue = sketchFittedSpline_var.getCurvatureHandle(fitPoint)
```

## Return Value

| Type | Description |
|----|----|
| [SketchArc](SketchArc.md) | Returns the sketch arc that acts as the handle to control the curvature at the specified point or returns null in the case where the curvature handle has not been activated at the specified sketch point. |

## Parameters

| Name | Type | Description |
|----|----|----|
| fitPoint | [SketchPoint](SketchPoint.md) | The fit point on the curve where you want to get the curvature handle. The fit points can be obtained by using the fitPoints property of the SketchFittedSpline object. |

## Samples

| Name | Description |
|----|----|
| [Sketch spline through points creation and relative functions API Sample](SketchSplineThroughPoints_Sample.md) | Create a sketch spline with points and use some operations for spline tangent handle & curvature handle. |

## Version

Introduced in version April 2019  

