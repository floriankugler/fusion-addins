# CustomGraphicsMesh.vertexIndexList Property

Parent Object: [CustomGraphicsMesh](CustomGraphicsMesh.md)  

## Description

Gets and sets an array of indices that define which coordinate in the coordinate list is used for each vertex in the mesh. Each set of three indices defines a triangle. For example: Indices 0, 1, and 2 define the coordinates to use for the first triangle and indices 3, 4, and 5 define the coordinates for the second triangle, and so on.

## Syntax

"customGraphicsMesh_var" is a variable referencing a CustomGraphicsMesh object.  

```python
# Get the value of the property.
propertyValue = customGraphicsMesh_var.vertexIndexList

# Set the value of the property.
customGraphicsMesh_var.vertexIndexList = propertyValue
```

## Property Value

This is a read/write property whose value is an array of type integer.

## Version

Introduced in version September 2017  

