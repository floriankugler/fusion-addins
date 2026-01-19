# SurfaceEvaluator.area Property

Parent Object: [SurfaceEvaluator](SurfaceEvaluator.md)  

## Description

Returns the area of the surface. This is typically used when the SurfaceEvaluator is associated with a BRepFace object where it is always valid. This can fail in the case where the SurfaceEvaluator is associated with one of the geometry classes, (Plane, Cylinder, Cone, EllipticalCone, or EllipticalCylinder object), because these surfaces are unbounded. A BRepFace, even one of these shapes, is bounded by its edges and has a well-defined area.

## Syntax

"surfaceEvaluator_var" is a variable referencing a SurfaceEvaluator object.  

```python
# Get the value of the property.
propertyValue = surfaceEvaluator_var.area
```

## Property Value

This is a read only property whose value is a double.

## Version

Introduced in version June 2015  

