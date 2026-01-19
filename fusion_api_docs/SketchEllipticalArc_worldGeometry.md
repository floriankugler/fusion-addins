# SketchEllipticalArc.worldGeometry Property

Parent Object: [SketchEllipticalArc](SketchEllipticalArc.md)  

## Description

Returns an EllipticalArc3D object which provides geometric information in world space. The returned geometry takes into account the assembly context and the position of the sketch in it's parent component, which means the geometry will be returned in the root component space.

## Syntax

"sketchEllipticalArc_var" is a variable referencing a SketchEllipticalArc object.  

```python
# Get the value of the property.
propertyValue = sketchEllipticalArc_var.worldGeometry
```

## Property Value

This is a read only property whose value is an [EllipticalArc3D](EllipticalArc3D.md).

## Version

Introduced in version August 2014  

