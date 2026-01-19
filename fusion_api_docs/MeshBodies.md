# MeshBodies Object

Derived from: [Base](Base.md) Object  

## Description

Provides access to the MeshBodies in the parent Component and supports the creation of new mesh bodies.

## Methods

| Name | Description |
| --- | --- |
| [add](MeshBodies_add.md) | Creates a new mesh body by importing an STL, OBJ or 3MF file. Because of a current limitation, if you want to create a mesh body in a parametric model, you must first call the edit method of the base or form feature, use this method to create the mesh body, and then call the finishEdit method of the base or form feature. The base or form feature must be in an "edit" state to be able to add any additional items to it. |
| [addByTriangleMeshData](MeshBodies_addByTriangleMeshData.md) | Creates a new mesh body using the mesh description provided. |
| [classType](MeshBodies_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](MeshBodies_item.md) | Provides access to a mesh body within the collection. |

## Properties

| Name | Description |
| --- | --- |
| [count](MeshBodies_count.md) | Returns the number of mesh bodies in the collection. |
| [isValid](MeshBodies_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](MeshBodies_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Component.meshBodies](Component_meshBodies.md), [FlatPatternComponent.meshBodies](FlatPatternComponent_meshBodies.md)

## Version

Introduced in version August 2014  

