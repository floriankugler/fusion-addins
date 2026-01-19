# AppearanceTexture Object

Derived from: [Base](Base.md) Object  

## Description

Provides access to a list of properties that define a texture.

## Methods

| Name | Description |
|----|----|
| [changeTextureImage](AppearanceTexture_changeTextureImage.md) | Changes the image of this texture. |
| [classType](AppearanceTexture_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [isValid](AppearanceTexture_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](AppearanceTexture_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [properties](AppearanceTexture_properties.md) | Returns a collection of the properties associated with this texture. |
| [textureType](AppearanceTexture_textureType.md) | Gets the type of texture this appearance currently is. |

## Accessed From

[AppearanceTextureProperty.value](AppearanceTextureProperty_value.md), [ColorProperty.connectedTexture](ColorProperty_connectedTexture.md), [FloatProperty.connectedTexture](FloatProperty_connectedTexture.md)

## Version

Introduced in version August 2014  

