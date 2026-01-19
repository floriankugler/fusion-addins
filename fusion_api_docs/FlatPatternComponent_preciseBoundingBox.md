# FlatPatternComponent.preciseBoundingBox Property

Parent Object: [FlatPatternComponent](FlatPatternComponent.md)  

## Description

Returns a bounding box that tightly fits around all B-Rep bodies in the component. All other geometry types are ignored.

## Syntax

"flatPatternComponent_var" is a variable referencing a FlatPatternComponent object.  

```python
# Get the value of the property.
propertyValue = flatPatternComponent_var.preciseBoundingBox
```

## Property Value

This is a read only property whose value is a [BoundingBox3D](BoundingBox3D.md).

## Version

Introduced in version January 2024  

