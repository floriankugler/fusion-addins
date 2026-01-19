# MeshBodyList.item Method

Parent Object: [MeshBodyList](MeshBodyList.md)  

## Description

Provides access to a mesh body within the collection.

## Syntax

"meshBodyList_var" is a variable referencing a [MeshBodyList](MeshBodyList.md) object.

```python
returnValue = meshBodyList_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [MeshBody](MeshBody.md) | Returns the specified mesh body or null in the case of a invalid index. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the mesh body to return, where an index of 0 is the first mesh body in the collection. |

## Version

Introduced in version August 2014  

