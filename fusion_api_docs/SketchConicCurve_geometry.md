# SketchConicCurve.geometry Property

Parent Object: [SketchConicCurve](SketchConicCurve.md)  

## Description

Returns the transient geometry of the curve which provides geometric information about the curve. The returned geometry is always in sketch space.  

Because the fixed spline can be analytically defined, for example it can be the precise intersection of a surface and the sketch plane, returning a NURBS curve that represents the spline may be an approximation of the actual curve. You can use the Evaluator property of the SketchFixedSpline object to perform evaluations on the precise curve.

## Syntax

"sketchConicCurve_var" is a variable referencing a SketchConicCurve object.  

```python
# Get the value of the property.
propertyValue = sketchConicCurve_var.geometry
```

## Property Value

This is a read only property whose value is a [NurbsCurve3D](NurbsCurve3D.md).

## Version

Introduced in version January 2015  

