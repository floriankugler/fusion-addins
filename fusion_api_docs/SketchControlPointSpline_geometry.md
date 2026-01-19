# SketchControlPointSpline.geometry Property

Parent Object: [SketchControlPointSpline](SketchControlPointSpline.md)  

## Description

Returns the transient geometry of the curve which provides geometric information about the curve. The returned geometry is always in sketch space. Use the worldGeometry property to get it in the model's design space.

## Syntax

"sketchControlPointSpline_var" is a variable referencing a SketchControlPointSpline object.  

```python
# Get the value of the property.
propertyValue = sketchControlPointSpline_var.geometry
```

## Property Value

This is a read only property whose value is a [NurbsCurve3D](NurbsCurve3D.md).

## Version

Introduced in version July 2022  

