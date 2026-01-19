# NurbsCurve3D.set Method

Parent Object: [NurbsCurve3D](NurbsCurve3D.md)  

## Description

Sets the data that defines a transient 3D NURBS rational b-spline object.

## Syntax

"nurbsCurve3D_var" is a variable referencing a [NurbsCurve3D](NurbsCurve3D.md) object.

```python
returnValue = nurbsCurve3D_var.set(controlPoints, degree, knots, isRational, weights, isPeriodic)
```

## Return Value

| Type    | Description                 |
|---------|-----------------------------|
| boolean | Returns true if successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| controlPoints | Point3D\[\] | The array of control point that define the path of the spline. |
| degree | integer | The degree of curvature of the spline. |
| knots | double\[\] | An array of numbers that define the knot vector of the spline. |
| isRational | boolean | A bool value indicating if the spline is rational. A rational spline must have a weight value for each control point. |
| weights | double\[\] | An array of numbers that define the weights for the spline. |
| isPeriodic | boolean | A bool indicating if the spline is Periodic. A periodic curve has a start point and end point that meet (with curvature continuity) forming a closed loop. |

## Version

Introduced in version August 2014  

