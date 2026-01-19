# CustomGraphicsColorEffect Object

Derived from: [Base](Base.md) Object  

## Description

The base class for all custom graphics color effects.

## Methods

| Name | Description |
|----|----|
| [classType](CustomGraphicsColorEffect_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [isValid](CustomGraphicsColorEffect_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](CustomGraphicsColorEffect_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[CustomGraphicsBRepBody.color](CustomGraphicsBRepBody_color.md), [CustomGraphicsCurve.color](CustomGraphicsCurve_color.md), [CustomGraphicsEntity.color](CustomGraphicsEntity_color.md), [CustomGraphicsGroup.color](CustomGraphicsGroup_color.md), [CustomGraphicsLines.color](CustomGraphicsLines_color.md), [CustomGraphicsMesh.color](CustomGraphicsMesh_color.md), [CustomGraphicsPointSet.color](CustomGraphicsPointSet_color.md), [CustomGraphicsText.color](CustomGraphicsText_color.md)

## Derived Classes

[CustomGraphicsAppearanceColorEffect](CustomGraphicsAppearanceColorEffect.md), [CustomGraphicsBasicMaterialColorEffect](CustomGraphicsBasicMaterialColorEffect.md), [CustomGraphicsShowThroughColorEffect](CustomGraphicsShowThroughColorEffect.md), [CustomGraphicsSolidColorEffect](CustomGraphicsSolidColorEffect.md), [CustomGraphicsVertexColorEffect](CustomGraphicsVertexColorEffect.md)

## Version

Introduced in version September 2017  

