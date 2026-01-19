# MeshBodies.addByTriangleMeshData Method

Parent Object: [MeshBodies](MeshBodies.md)  

## Description

Creates a new mesh body using the mesh description provided.

## Syntax

"meshBodies_var" is a variable referencing a [MeshBodies](MeshBodies.md) object.

```python
returnValue = meshBodies_var.addByTriangleMeshData(coordinates, coordinateIndexList, normalVectors, normalIndexList)
```

## Return Value

| Type | Description |
|----|----|
| [MeshBody](MeshBody.md) | Returns the newly created MeshBody object or null in the case of a failure. |

## Parameters

| Name | Type | Description |
|----|----|----|
| coordinates | double\[\] | Input array of doubles that defines the X, Y, Z coordinates of each node in the mesh. Each set of three numbers define the coordinates of a node. |
| coordinateIndexList | integer\[\] | An array of integers that represent indices into the coordinates to define the vertices of the triangles. If an empty array is provided, then it's assumed that the first three coordinates defines the first triangle, the next three define the second triangle, and so on. |
| normalVectors | double\[\] | An array of doubles that represent the x, y, z components of the normals at each coordinate. There should be a normal defined for each coordinate. If an empty array is provided for the normal vectors, Fusion will automatically calculate normal vectors that are 90 degrees to the face of the triangle, making it appear flat. |
| normalIndexList | integer\[\] | An array of integers that represent indices into the normal vectors to define the which vector corresponds to which vertex. This should be the same size as the vertex index list. If an empty array is input and normal vectors are provided, it is assumed that the normals match up one-to-one to each coordinate. |

## Version

Introduced in version April 2019  

