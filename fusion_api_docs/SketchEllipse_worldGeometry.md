# SketchEllipse.worldGeometry Property

Parent Object: [SketchEllipse](SketchEllipse.md)  

## Description

Returns an Ellipse3D object which provides geometric information in world space. The returned geometry takes into account the assembly context and the position of the sketch in it's parent component, which means the geometry will be returned in the root component space.

## Syntax

"sketchEllipse_var" is a variable referencing a SketchEllipse object.  

```python
# Get the value of the property.
propertyValue = sketchEllipse_var.worldGeometry
```

## Property Value

This is a read only property whose value is an [Ellipse3D](Ellipse3D.md).

## Version

Introduced in version August 2014  

