# NurbsCurve2D.createRational Method

Parent Object: [NurbsCurve2D](NurbsCurve2D.md)  

## Description

Creates a transient 2D NURBS rational b-spline object.

## Syntax

This is a static method.  

```python

returnValue = adsk.core.NurbsCurve2D.createRational(controlPoints, degree, knots, weights, isPeriodic)
```

## Return Value

| Type | Description |
|----|----|
| [NurbsCurve2D](NurbsCurve2D.md) | Returns the new NurbsCurve2D object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| controlPoints | Point2D\[\] | An array of control point that define the path of the spline |
| degree | integer | The degree of curvature of the spline |
| knots | double\[\] | An array of numbers that define the knot vector of the spline. The knots is an array of (>=degree + N + 1) numbers, where N is the number of control points. |
| weights | double\[\] | An array of numbers that define the weights for the spline. |
| isPeriodic | boolean | A bool specifying if the spline is to be Periodic. A periodic curve has a start point and end point that meet (with curvature continuity) forming a closed loop. |

## Version

Introduced in version August 2014  

