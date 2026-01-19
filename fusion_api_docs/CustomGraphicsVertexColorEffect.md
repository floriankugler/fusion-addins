# CustomGraphicsVertexColorEffect Object

Derived from: [CustomGraphicsColorEffect](CustomGraphicsColorEffect.md) Object  

## Description

One of the types of color effects that can be applied to a custom graphics entity. With this type of effect, the graphics entity will display using the colors associated with the vertices of the mesh in the CustomGraphicsCoordinates object.

## Methods

| Name | Description |
|----|----|
| [classType](CustomGraphicsVertexColorEffect_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [create](CustomGraphicsVertexColorEffect_create.md) | Statically creates a new CustomGraphicsVertexColorEffect object. |

## Properties

| Name | Description |
| --- | --- |
| [isValid](CustomGraphicsVertexColorEffect_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](CustomGraphicsVertexColorEffect_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[CustomGraphicsVertexColorEffect.create](CustomGraphicsVertexColorEffect_create.md)

## Version

Introduced in version September 2017  

