# SketchCircle.worldGeometry Property

Parent Object: [SketchCircle](SketchCircle.md)  

## Description

Returns a Point3D object which provides the position of the sketch point in world space. The returned coordinate takes into account the assembly context and the position of the sketch in it's parent component, which means the coordinate will be returned in the root component space.

## Syntax

"sketchCircle_var" is a variable referencing a SketchCircle object.  

```python
# Get the value of the property.
propertyValue = sketchCircle_var.worldGeometry
```

## Property Value

This is a read only property whose value is a [Circle3D](Circle3D.md).

## Version

Introduced in version August 2014  

