# Component.orientedMinimumBoundingBox Property

Parent Object: [Component](Component.md)  

## Description

Returns an oriented bounding box that is best oriented to tightly fit all B-Rep bodies in the component. All other geometry types are ignored.

## Syntax

"component_var" is a variable referencing a Component object.  

```python
# Get the value of the property.
propertyValue = component_var.orientedMinimumBoundingBox
```

## Property Value

This is a read only property whose value is an [OrientedBoundingBox3D](OrientedBoundingBox3D.md).

## Version

Introduced in version January 2024  

