# FlatPatternComponent.orientedMinimumBoundingBox Property

Parent Object: [FlatPatternComponent](FlatPatternComponent.md)  

## Description

Returns an oriented bounding box that is best oriented to tightly fit all B-Rep bodies in the component. All other geometry types are ignored.

## Syntax

"flatPatternComponent_var" is a variable referencing a FlatPatternComponent object.  

```python
# Get the value of the property.
propertyValue = flatPatternComponent_var.orientedMinimumBoundingBox
```

## Property Value

This is a read only property whose value is an [OrientedBoundingBox3D](OrientedBoundingBox3D.md).

## Version

Introduced in version January 2024  

