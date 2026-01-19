# FlatPatternComponent.boundingBox Property

Parent Object: [FlatPatternComponent](FlatPatternComponent.md)  

## Description

Returns the bounding box of this component. This is always in world space of the component. The boundingBox2 method provides greater control over which types of entities you want included in the bounding box calculation.

## Syntax

"flatPatternComponent_var" is a variable referencing a FlatPatternComponent object.  

```python
# Get the value of the property.
propertyValue = flatPatternComponent_var.boundingBox
```

## Property Value

This is a read only property whose value is a [BoundingBox3D](BoundingBox3D.md).

## Version

Introduced in version October 2022  

