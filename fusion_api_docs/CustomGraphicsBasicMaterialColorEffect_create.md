# CustomGraphicsBasicMaterialColorEffect.create Method

Parent Object: [CustomGraphicsBasicMaterialColorEffect](CustomGraphicsBasicMaterialColorEffect.md)  

## Description

Statically creates a new basic CustomGraphicsBasicMaterialColorEffect object. This can be used to color custom graphics entities. With this type of effect you define the basic Phong shading properties so that the entity can be rendered with basic shading and lighting effects applied so that it appears 3-dimensional.  

If only the emissive color is provided, the API will automatically create values for the other colors to render the object as a single color.

## Syntax

This is a static method.  

```python

# Uses no optional arguments.
returnValue = adsk.fusion.CustomGraphicsBasicMaterialColorEffect.create(diffuseColor)

# Uses optional arguments.
returnValue = adsk.fusion.CustomGraphicsBasicMaterialColorEffect.create(diffuseColor, ambientColor, specularColor, emissiveColor, glossiness, opacity)
```

## Return Value

| Type | Description |
|----|----|
| [CustomGraphicsBasicMaterialColorEffect](CustomGraphicsBasicMaterialColorEffect.md) | Returns the created CustomGraphicsBasicMaterialColorEffect or null in case of a failure. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| diffuseColor | [Color](Color.md) | The diffuse color is the color of reflected light as it scatters off of a rough surface and is the primary color of the entity. This color is always required. |
| ambientColor | [Color](Color.md) | The ambient color is the color of the light anywhere there's not a specific light source. If not specified the same color as the diffuse color is used. This is an optional argument whose default value is null. |
| specularColor | [Color](Color.md) | The specular color is the color of reflected light (highlights) as it is reflected off of a shiny surface. This is commonly white or a lighter shade of the diffuse color. If not specified, white is used. This is an optional argument whose default value is null. |
| emissiveColor | [Color](Color.md) | The emissive color is the color of light that entity emits, such as in a light bulb. If not specified, black for no emissive light is used. This is an optional argument whose default value is null. |
| glossiness | double | This specifies how glossy the entity is. The glossiness determines the size of highlights, and thus the apparent shininess of the material. A value of 0.0 will result in very large highlights like you would see with a rough surface. A maximum value of 128.0 will result in very small highlight as from a smooth surface. This is an optional argument whose default value is 5.0. |
| opacity | double | Specifies the opacity of the entity where a value of 1.0 is completely opaque and 0.0 is completely transparent. This is an optional argument whose default value is 1.0. |

## Version

Introduced in version September 2017  

