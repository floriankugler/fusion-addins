# CurveEvaluator3D.getParametersAtPoints Method

Parent Object: [CurveEvaluator3D](CurveEvaluator3D.md)  

## Description

Get the parameter positions that correspond to a set of points on the curve. For reliable results, the points should lie on the curve within model tolerance. If the points do not lie on the curve, the parameter of the nearest point on the curve will generally be returned.

## Syntax

"curveEvaluator3D_var" is a variable referencing a [CurveEvaluator3D](CurveEvaluator3D.md) object.  

```python
(returnValue, parameters) = curveEvaluator3D_var.getParametersAtPoints(points)
```

## Return Value

| Type    | Description                                                |
|---------|------------------------------------------------------------|
| boolean | Returns true if the parameters were successfully returned. |

## Parameters

| Name | Type | Description |
|----|----|----|
| points | Point3D\[\] | An array of points to get the curve parameter values at. |
| parameters | double\[\] | The output array of parameter positions corresponding to the set of points. The length of this array will be equal to the length of the points array specified. |

## Version

Introduced in version August 2014  

