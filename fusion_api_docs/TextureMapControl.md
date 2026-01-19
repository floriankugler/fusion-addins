# TextureMapControl Object

Derived from: [Base](Base.md) Object  

## Description

Provides access to the various settings that control how a texture is applied to a body or mesh. This is the base class for the various texture mapping techniques.

## Methods

| Name | Description |
|----|----|
| [classType](TextureMapControl_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [reset](TextureMapControl_reset.md) | Resets the texture map back to its original default settings. |

## Properties

| Name | Description |
| --- | --- |
| [isValid](TextureMapControl_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](TextureMapControl_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[BRepBody.textureMapControl](BRepBody_textureMapControl.md), [MeshBody.textureMapControl](MeshBody_textureMapControl.md), [TSplineBody.textureMapControl](TSplineBody_textureMapControl.md)

## Derived Classes

[ProjectedTextureMapControl](ProjectedTextureMapControl.md), [TextureMapControl3D](TextureMapControl3D.md)

## Version

Introduced in version March 2022  

