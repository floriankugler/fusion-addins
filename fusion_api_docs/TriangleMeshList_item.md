# TriangleMeshList.item Method

Parent Object: [TriangleMeshList](TriangleMeshList.md)  

## Description

Returns the specified triangle meshes.

## Syntax

"triangleMeshList_var" is a variable referencing a [TriangleMeshList](TriangleMeshList.md) object.

```python
returnValue = triangleMeshList_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [TriangleMesh](TriangleMesh.md) | Returns the specified mesh or null in the case of invalid index. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the mesh to return where the first item has an index of 0. |

## Version

Introduced in version August 2014  

