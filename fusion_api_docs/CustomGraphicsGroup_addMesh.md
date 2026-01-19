# CustomGraphicsGroup.addMesh Method

Parent Object: [CustomGraphicsGroup](CustomGraphicsGroup.md)  

## Description

Adds a new CustomGraphicsMesh entity to this group.

## Syntax

"customGraphicsGroup_var" is a variable referencing a [CustomGraphicsGroup](CustomGraphicsGroup.md) object.

```python
returnValue = customGraphicsGroup_var.addMesh(coordinates, coordinateIndexList, normalVectors, normalIndexList)
```

## Return Value

| Type | Description |
|----|----|
| [CustomGraphicsMesh](CustomGraphicsMesh.md) | Returns the new CustomGraphicsMesh object or null in the case of a failure. |

## Parameters

| Name | Type | Description |
|----|----|----|
| coordinates | [CustomGraphicsCoordinates](CustomGraphicsCoordinates.md) | The CustomGraphicsCoordinates object that defines the coordinates of the vertices of the mesh. A CustomGrahpicsCoordinates object can be created using the static create method of the CustomGraphicsCoordinates class. |
| coordinateIndexList | integer\[\] | An array of integers that represent indices into the coordinates to define the vertices of the triangles. If an empty array is provided, then it's assumed that the first three coordinates defines the first triangle, the next three define the second triangle, and so on. |
| normalVectors | double\[\] | An array of doubles that represent the x, y, z components of the normals at each coordinate. There should be a normal defined for each coordinate. If an empty array is provided for the normal vectors, Fusion will automatically calculate normal vectors that are 90 degrees to the face of the triangle, making it appear flat. |
| normalIndexList | integer\[\] | An array of integers that represent indices into the normal vectors to define the which vector corresponds to which vertex. This should be the same size as the vertex index list. If an empty array is input and normal vectors are provided, it is assumed that the normals match up one-to-one to each coordinate. |

## Samples

| Name | Description |
| --- | --- |
| [Custom Graphics Sample](CustomGraphicsSample_Sample.md) | A sample demonstrating how to create custom graphics entities. To use the sample, create a new Python or C++ script and copy and paste this code, replacing the default code. You also need to unpack this zip file which contains a [resource folder](../ExtraFiles/GraphicsSampleResources.zip) into the same folder where the source code file (.py or .cpp) is. |

## Version

Introduced in version September 2017  

