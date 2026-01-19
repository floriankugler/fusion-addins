# SketchFittedSpline.activateTangentHandle Method

Parent Object: [SketchFittedSpline](SketchFittedSpline.md)  

## Description

Activates the tangent handle for the specified fit point and returns the sketch line that acts as the handle to control the tangency. You can use the getTangentHandle property to determine if the tangent handle has already been activated. If this method is called for a handle that already exists, nothing changes and the existing sketch line that acts as the tangent handle is returned.  

The getTangentHandle method can be used to determine if the handle has already been activated.  

To deactivate a sketch handle you can delete the sketch line.

## Syntax

"sketchFittedSpline_var" is a variable referencing a [SketchFittedSpline](SketchFittedSpline.md) object.

```python
returnValue = sketchFittedSpline_var.activateTangentHandle(fitPoint)
```

## Return Value

| Type | Description |
|----|----|
| [SketchLine](SketchLine.md) | Returns the sketch line that acts as the tangent handle at the specified fit point. |

## Parameters

| Name | Type | Description |
|----|----|----|
| fitPoint | [SketchPoint](SketchPoint.md) | The fit point on the curve where you want to activate the tangent handle. The fit points can be obtained by using the fitPoints property of the SketchFittedSpline object. |

## Version

Introduced in version April 2019  

