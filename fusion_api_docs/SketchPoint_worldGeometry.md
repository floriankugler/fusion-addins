# SketchPoint.worldGeometry Property

Parent Object: [SketchPoint](SketchPoint.md)  

## Description

Returns a Point3D object which provides the position of the sketch point in world space. The returned coordinate takes into account the assembly context and the position of the sketch in it's parent component, which means the coordinate will be returned in the root component space.

## Syntax

"sketchPoint_var" is a variable referencing a SketchPoint object.  

```python
# Get the value of the property.
propertyValue = sketchPoint_var.worldGeometry
```

## Property Value

This is a read only property whose value is a [Point3D](Point3D.md).

## Version

Introduced in version August 2014  

