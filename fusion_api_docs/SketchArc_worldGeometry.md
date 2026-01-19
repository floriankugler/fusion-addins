# SketchArc.worldGeometry Property

Parent Object: [SketchArc](SketchArc.md)  

## Description

Returns an Arc3D object which provides geometric information in world space. The returned geometry takes into account the assembly context and the position of the sketch in it's parent component, which means the geometry will be returned in the root component space.

## Syntax

"sketchArc_var" is a variable referencing a SketchArc object.  

```python
# Get the value of the property.
propertyValue = sketchArc_var.worldGeometry
```

## Property Value

This is a read only property whose value is an [Arc3D](Arc3D.md).

## Version

Introduced in version August 2014  

