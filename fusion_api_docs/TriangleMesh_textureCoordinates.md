# TriangleMesh.textureCoordinates Property

Parent Object: [TriangleMesh](TriangleMesh.md)  

## Description

Returns the texture coordinates used when mapping a texture to this face. The coordinates are returned as an array of Point2D objects where the x and y properties of the point are u and v coordinates as defined in parametric space. There is a texture coordinate for each vertex in the face mesh.

## Syntax

"triangleMesh_var" is a variable referencing a TriangleMesh object.  

```python
# Get the value of the property.
propertyValue = triangleMesh_var.textureCoordinates
```

## Property Value

This is a read only property whose value is an array of type [Point2D](Point2D.md).

## Version

Introduced in version August 2014  

