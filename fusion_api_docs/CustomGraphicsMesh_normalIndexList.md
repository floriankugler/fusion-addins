# CustomGraphicsMesh.normalIndexList Property

Parent Object: [CustomGraphicsMesh](CustomGraphicsMesh.md)  

## Description

Gets and sets an array of indices that define which normal is associated with each vertex in the mesh. This is used to look-up the normal in the normalVectors array.

## Syntax

"customGraphicsMesh_var" is a variable referencing a CustomGraphicsMesh object.  

```python
# Get the value of the property.
propertyValue = customGraphicsMesh_var.normalIndexList

# Set the value of the property.
customGraphicsMesh_var.normalIndexList = propertyValue
```

## Property Value

This is a read/write property whose value is an array of type integer.

## Version

Introduced in version September 2017  

