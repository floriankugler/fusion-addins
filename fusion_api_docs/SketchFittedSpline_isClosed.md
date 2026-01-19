# SketchFittedSpline.isClosed Property

Parent Object: [SketchFittedSpline](SketchFittedSpline.md)  

## Description

Gets and sets if this spline is closed. A closed spline is also periodic. This property can return false even in the case where the spline is physically closed. It's possible that the start and end points of a spline can be the same point but the curve is still not considered closed. This can happen when the start and end points of an open curve are merged. The curve is physically closed but is not periodic and can have a discontinuity at the joint. Setting it to closed will cause it to be periodic and to always remain closed even as fit points are deleted.

## Syntax

"sketchFittedSpline_var" is a variable referencing a SketchFittedSpline object.  

```python
# Get the value of the property.
propertyValue = sketchFittedSpline_var.isClosed

# Set the value of the property.
sketchFittedSpline_var.isClosed = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version August 2014  

