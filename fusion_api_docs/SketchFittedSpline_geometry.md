# SketchFittedSpline.geometry Property

Parent Object: [SketchFittedSpline](SketchFittedSpline.md)  

## Description

Returns the transient geometry of the curve which provides geometric information about the curve. The returned geometry is always in sketch space.

## Syntax

"sketchFittedSpline_var" is a variable referencing a SketchFittedSpline object.  

```python
# Get the value of the property.
propertyValue = sketchFittedSpline_var.geometry
```

## Property Value

This is a read only property whose value is a [NurbsCurve3D](NurbsCurve3D.md).

## Version

Introduced in version August 2014  

