# TriangleMesh.nodeIndices Property

Parent Object: [TriangleMesh](TriangleMesh.md)  

## Description

Returns an array of indices that define which nodes are used for each triangle. This is used to look-up the coordinates in the NodeCoordinates array to get the three coordinates of each triangle.

## Syntax

"triangleMesh_var" is a variable referencing a TriangleMesh object.  

```python
# Get the value of the property.
propertyValue = triangleMesh_var.nodeIndices
```

## Property Value

This is a read only property whose value is an array of type integer.

## Version

Introduced in version August 2014  

