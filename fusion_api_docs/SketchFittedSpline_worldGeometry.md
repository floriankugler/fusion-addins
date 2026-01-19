# SketchFittedSpline.worldGeometry Property

Parent Object: [SketchFittedSpline](SketchFittedSpline.md)  

## Description

Returns an NurbsCurve3D object which provides geometric information in world space. The returned geometry takes into account the assembly context and the position of the sketch in it's parent component, which means the geometry will be returned in the root component space.

## Syntax

"sketchFittedSpline_var" is a variable referencing a SketchFittedSpline object.  

```python
# Get the value of the property.
propertyValue = sketchFittedSpline_var.worldGeometry
```

## Property Value

This is a read only property whose value is a [NurbsCurve3D](NurbsCurve3D.md).

## Version

Introduced in version August 2014  

