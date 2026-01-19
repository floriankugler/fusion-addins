# TriangleMesh Object

Derived from: [Base](Base.md) Object  

## Description

The TriangleMesh object represents all of the data defining a triangular mesh.

## Methods

| Name | Description |
|----|----|
| [classType](TriangleMesh_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [isValid](TriangleMesh_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [nodeCoordinates](TriangleMesh_nodeCoordinates.md) | Returns the node coordinates as an array of Point3D objects. |
| [nodeCoordinatesAsDouble](TriangleMesh_nodeCoordinatesAsDouble.md) | Returns the node coordinates as an array of doubles where they are the x, y, z components of each coordinate. |
| [nodeCoordinatesAsFloat](TriangleMesh_nodeCoordinatesAsFloat.md) | Returns the node coordinates as an array of floats where they are the x, y, z components of each coordinate. |
| [nodeCount](TriangleMesh_nodeCount.md) | Returns the total number of nodes in the mesh. |
| [nodeIndices](TriangleMesh_nodeIndices.md) | Returns an array of indices that define which nodes are used for each triangle. This is used to look-up the coordinates in the NodeCoordinates array to get the three coordinates of each triangle. |
| [normalVectors](TriangleMesh_normalVectors.md) | Returns the normal vectors of the mesh where there is a normal vector at each node. The normals are returned as an array of Vector3D objects. |
| [normalVectorsAsDouble](TriangleMesh_normalVectorsAsDouble.md) | Returns the normal vectors of the mesh where there is a normal vector at each node. The normals are returned as an array of doubles where they are the x, y, z components of each vector. |
| [normalVectorsAsFloat](TriangleMesh_normalVectorsAsFloat.md) | Returns the normal vectors of the mesh where there is a normal vector at each node. The normals are returned as an array of floats where they are the x, y, z components of each vector. |
| [objectType](TriangleMesh_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [surfaceTolerance](TriangleMesh_surfaceTolerance.md) | Returns the surface tolerance that was used to generate this mesh. This is most useful when using display meshes that have already been calculated. |
| [textureCoordinates](TriangleMesh_textureCoordinates.md) | Returns the texture coordinates used when mapping a texture to this face. The coordinates are returned as an array of Point2D objects where the x and y properties of the point are u and v coordinates as defined in parametric space. There is a texture coordinate for each vertex in the face mesh. |
| [textureCoordinatesAsDouble](TriangleMesh_textureCoordinatesAsDouble.md) | Returns the texture coordinates used when mapping a texture to this face. The coordinates are returned as an array of doubles where they are the u and v components of each coordinate as defined in parametric space. There is a texture coordinate for each vertex in the face mesh. |
| [textureCoordinatesAsFloat](TriangleMesh_textureCoordinatesAsFloat.md) | Returns the texture coordinates used when mapping a texture to this face. The coordinates are returned as an array of floats where they are the u and v components of each coordinate as defined in parametric space. There is a texture coordinate for each vertex in the face mesh. |
| [triangleCount](TriangleMesh_triangleCount.md) | Returns the number of triangles in the mesh. |

## Accessed From

[MeshBody.displayMesh](MeshBody_displayMesh.md), [TriangleMeshCalculator.calculate](TriangleMeshCalculator_calculate.md), [TriangleMeshList.bestMesh](TriangleMeshList_bestMesh.md), [TriangleMeshList.item](TriangleMeshList_item.md)

## Version

Introduced in version August 2014  

