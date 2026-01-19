# NurbsCurve2D.getData Method

Parent Object: [NurbsCurve2D](NurbsCurve2D.md)  

## Description

Gets the data that defines a transient 2D NURBS rational b-spline object.

## Syntax

"nurbsCurve2D_var" is a variable referencing a [NurbsCurve2D](NurbsCurve2D.md) object.  

```python
(returnValue, controlPoints, degree, knots, isRational, weights, isPeriodic) = nurbsCurve2D_var.getData()
```

## Return Value

| Type    | Description                 |
|---------|-----------------------------|
| boolean | Returns true if successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| controlPoints | Point2D\[\] | The output array of control point that define the path of the spline. |
| degree | integer | The output degree of curvature of the spline. |
| knots | double\[\] | The output array of numbers that define the knots of the spline. |
| isRational | boolean | The output value indicating if the spline is rational. A rational spline will have a weight value for each control point. |
| weights | double\[\] | The output array of numbers that define the weights for the spline. |
| isPeriodic | boolean | The output value indicating if the spline is Periodic. A periodic curve has a start point and end point that meet (with curvature continuity) forming a closed loop. |

## Version

Introduced in version August 2014  

