# CustomGraphicsBasicMaterialColorEffect Object

Derived from: [CustomGraphicsColorEffect](CustomGraphicsColorEffect.md) Object  

## Description

One of the types of color effects that can be applied to a custom graphics entity. With this type of effect, basic Phong shading and lighting techniques are used so give the entity a 3-dimensional appearance.

## Methods

| Name | Description |
| --- | --- |
| [classType](CustomGraphicsBasicMaterialColorEffect_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [create](CustomGraphicsBasicMaterialColorEffect_create.md) | Statically creates a new basic CustomGraphicsBasicMaterialColorEffect object. This can be used to color custom graphics entities. With this type of effect you define the basic Phong shading properties so that the entity can be rendered with basic shading and lighting effects applied so that it appears 3-dimensional. If only the emissive color is provided, the API will automatically create values for the other colors to render the object as a single color. |

## Properties

| Name | Description |
| --- | --- |
| [ambientColor](CustomGraphicsBasicMaterialColorEffect_ambientColor.md) | Gets and sets the ambientColor associated with this CustomGraphicsBasicMaterialColorEffect object. The ambient color is the color of the light anywhere there's not a specific light source. |
| [diffuseColor](CustomGraphicsBasicMaterialColorEffect_diffuseColor.md) | Gets and sets the diffuseColor associated with this CustomGraphicsBasicMaterialColorEffect object. The diffuse color is the color of reflected light as it scatters off of a rough surface. |
| [emissiveColor](CustomGraphicsBasicMaterialColorEffect_emissiveColor.md) | Gets and sets the emissiveColor associated with this CustomGraphicsBasicMaterialColorEffect object. The emissive color is the primary color of the entity |
| [glossiness](CustomGraphicsBasicMaterialColorEffect_glossiness.md) | Gets and sets the glossiness associated with this CustomGraphicsBasicMaterialColorEffect object. The glossiness determines the size of highlights, and thus the apparent shininess of the material. A value of 0.0 will result in very large highlights like you would see with a rough surface. A maximum value of 128.0 will result in very small highlight as from a smooth surface. |
| [isValid](CustomGraphicsBasicMaterialColorEffect_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](CustomGraphicsBasicMaterialColorEffect_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [opacity](CustomGraphicsBasicMaterialColorEffect_opacity.md) | Gets and sets the opacity associated with this CustomGraphicsBasicMaterialColorEffect object. A value of 1.0 is completely opaque and 0.0 is completely transparent. |
| [specularColor](CustomGraphicsBasicMaterialColorEffect_specularColor.md) | Gets and sets the specularColor associated with this CustomGraphicsBasicMaterialColorEffect object. The specular color is the color of reflected light (highlights) as it is reflected off of a shiny surface. This is commonly white or a lighter shade of the emissive color. |

## Accessed From

[CustomGraphicsBasicMaterialColorEffect.create](CustomGraphicsBasicMaterialColorEffect_create.md)

## Version

Introduced in version September 2017  

