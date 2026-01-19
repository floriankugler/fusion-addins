# MeshBodyDisplayOverrides Object

Derived from: [Base](Base.md) Object  

## Description

Container for overrides that control how the mesh is displayed in the interactive 3D view.

## Methods

| Name | Description |
|----|----|
| [classType](MeshBodyDisplayOverrides_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [isSuppressFaceGroupColors](MeshBodyDisplayOverrides_isSuppressFaceGroupColors.md) | Controls whether the mesh body face group colors are shown. If set to true, the face groups will be shown with the assigned appearance, ignoring the current display settings. |
| [isSuppressTriangleEdges](MeshBodyDisplayOverrides_isSuppressTriangleEdges.md) | Controls whether the edges of the triangles of the mesh body are shown. If set to true, individual triangles will not be visible, edges of face groups (if any) will be shown instead. |
| [isValid](MeshBodyDisplayOverrides_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](MeshBodyDisplayOverrides_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[MeshBody.displayOverrides](MeshBody_displayOverrides.md)

## Version

Introduced in version May 2025  

