# MeshManager Object

Derived from: [Base](Base.md) Object  

## Description

Provides access to meshes that approximate a B-Rep and T-Spline.

## Methods

| Name | Description |
|----|----|
| [classType](MeshManager_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createMeshCalculator](MeshManager_createMeshCalculator.md) | Creates a new MeshCalculator which is used to calculate new triangular meshes based on various parameters that control the calculation. |

## Properties

| Name | Description |
| --- | --- |
| [displayMeshes](MeshManager_displayMeshes.md) | Returns a collection that provides access to all of the existing display meshes. |
| [isValid](MeshManager_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](MeshManager_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parent](MeshManager_parent.md) | Returns the parent BRepBody, BRepFace, BRepLump, BRepShell, SculptBody, or SculptFace object. |

## Accessed From

[BRepBody.meshManager](BRepBody_meshManager.md), [BRepFace.meshManager](BRepFace_meshManager.md), [BRepLump.meshManager](BRepLump_meshManager.md), [BRepShell.meshManager](BRepShell_meshManager.md), [TriangleMeshCalculator.parentMeshManager](TriangleMeshCalculator_parentMeshManager.md)

## Version

Introduced in version August 2014  

