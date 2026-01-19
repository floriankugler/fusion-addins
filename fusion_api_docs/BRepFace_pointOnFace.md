# BRepFace.pointOnFace Property

Parent Object: [BRepFace](BRepFace.md)  

## Description

Returns a sample point guaranteed to lie on the face's surface, within the face's boundaries, and not on a boundary edge.

## Syntax

"bRepFace_var" is a variable referencing a BRepFace object.  

```python
# Get the value of the property.
propertyValue = bRepFace_var.pointOnFace
```

## Property Value

This is a read only property whose value is a [Point3D](Point3D.md).

## Version

Introduced in version August 2014  

