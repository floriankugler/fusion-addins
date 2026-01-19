# CustomGraphicsShowThroughColorEffect Object

Derived from: [CustomGraphicsColorEffect](CustomGraphicsColorEffect.md) Object  

## Description

One of the types of color effects that can be applied to a custom graphics entity. With this type of effect, the graphics entity will display using the specified color and will show through other graphics that are in front of it.

## Methods

| Name | Description |
|----|----|
| [classType](CustomGraphicsShowThroughColorEffect_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [create](CustomGraphicsShowThroughColorEffect_create.md) | Creates a new CustomGraphicsShowThroughColorEffect object that can be assigned to a custom graphics entity using its showThrough property. |

## Properties

| Name | Description |
| --- | --- |
| [color](CustomGraphicsShowThroughColorEffect_color.md) | Gets and sets the color associated with this CustomGraphicsShowThroughColorEffect object. The color that will be used to render the portion of the entity that is covered by other objects in the scene. |
| [isValid](CustomGraphicsShowThroughColorEffect_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](CustomGraphicsShowThroughColorEffect_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [opacity](CustomGraphicsShowThroughColorEffect_opacity.md) | Gets and sets the opacity value associated with this CustomGraphicsShowThroughColorEffect object. The opacity is used when rendering the portion of the entity that is covered by other objects in the scene. This can be a value between 0 and 1, where 1 is fully opaque and will completely cover any other entities. |

## Accessed From

[CustomGraphicsShowThroughColorEffect.create](CustomGraphicsShowThroughColorEffect_create.md)

## Version

Introduced in version August 2020  

