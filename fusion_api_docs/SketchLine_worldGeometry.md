# SketchLine.worldGeometry Property

Parent Object: [SketchLine](SketchLine.md)  

## Description

Returns a Line3D object which provides geometric information in world space. The returned geometry takes into account the assembly context and the position of the sketch in it's parent component, which means the geometry will be returned in the root component space.

## Syntax

"sketchLine_var" is a variable referencing a SketchLine object.  

```python
# Get the value of the property.
propertyValue = sketchLine_var.worldGeometry
```

## Property Value

This is a read only property whose value is a [Line3D](Line3D.md).

## Version

Introduced in version August 2014  

