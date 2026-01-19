# SketchControlPointSpline.isVisible Property

Parent Object: [SketchControlPointSpline](SketchControlPointSpline.md)  

## Description

When a sketch is created, geometry is sometimes automatically added to the sketch. For example a sketch point that references the origin point is always included and if a face was selected to create the sketch on, geometry from the face is also included. This automatically created geometry behaves in a special way in that it is invisible but is available for selection and it also participates in profile calculations. It's not possible to make them visible but they can be deleted and they can be used for any other standard sketch operation.

## Syntax

"sketchControlPointSpline_var" is a variable referencing a SketchControlPointSpline object.  

```python
# Get the value of the property.
propertyValue = sketchControlPointSpline_var.isVisible
```

## Property Value

This is a read only property whose value is a boolean.

## Version

Introduced in version July 2022  

