# TriangleMesh.textureCoordinatesAsFloat Property

Parent Object: [TriangleMesh](TriangleMesh.md)  

## Description

Returns the texture coordinates used when mapping a texture to this face. The coordinates are returned as an array of floats where they are the u and v components of each coordinate as defined in parametric space. There is a texture coordinate for each vertex in the face mesh.

## Syntax

"triangleMesh_var" is a variable referencing a TriangleMesh object.  

```python
# Get the value of the property.
propertyValue = triangleMesh_var.textureCoordinatesAsFloat
```

## Property Value

This is a read only property whose value is an array of type float.

## Version

Introduced in version August 2014  

