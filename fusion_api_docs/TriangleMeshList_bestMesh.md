# TriangleMeshList.bestMesh Property

Parent Object: [TriangleMeshList](TriangleMeshList.md)  

## Description

Returns the mesh with the tightest surface tolerance. This can return null in the case the list is empty, i.e. Count is 0.

## Syntax

"triangleMeshList_var" is a variable referencing a TriangleMeshList object.  

```python
# Get the value of the property.
propertyValue = triangleMeshList_var.bestMesh
```

## Property Value

This is a read only property whose value is a [TriangleMesh](TriangleMesh.md).

## Version

Introduced in version August 2014  

