# Occurrence.orientedMinimumBoundingBox Property

Parent Object: [Occurrence](Occurrence.md)  

## Description

Returns an oriented bounding box that is best oriented to tightly fit all B-Rep bodies in the occurrence. All other geometry types are ignored.

## Syntax

"occurrence_var" is a variable referencing an Occurrence object.  

```python
# Get the value of the property.
propertyValue = occurrence_var.orientedMinimumBoundingBox
```

## Property Value

This is a read only property whose value is an [OrientedBoundingBox3D](OrientedBoundingBox3D.md).

## Version

Introduced in version January 2024  

