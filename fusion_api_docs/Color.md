# Color Object

Derived from: [Base](Base.md) Object  

## Description

The Color class wraps all of the information that defines a simple color.

## Methods

| Name | Description |
|----|----|
| [classType](Color_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [create](Color_create.md) | Creates a new color. |
| [getColor](Color_getColor.md) | Gets all of the information defining this color. |
| [setColor](Color_setColor.md) | Sets all of the color information. |

## Properties

| Name | Description |
| --- | --- |
| [blue](Color_blue.md) | Gets and sets the blue component of the color. The value can be 0 to 255. |
| [green](Color_green.md) | Gets and sets the green component of the color. The value can be 0 to 255. |
| [isValid](Color_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](Color_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [opacity](Color_opacity.md) | Gets and sets the opacity of the color. The value can be 0 to 255. A value of 0 is transparent and 255 is opaque. |
| [red](Color_red.md) | Gets and sets the red component of the color. The value can be 0 to 255. |

## Accessed From

[Color.create](Color_create.md), [ColorControlPoint.value](ColorControlPoint_value.md), [ColorGraphNodeProperty.value](ColorGraphNodeProperty_value.md), [ColorProperty.value](ColorProperty_value.md), [ColorProperty.values](ColorProperty_values.md), [Component.componentColor](Component_componentColor.md), [CustomGraphicsBasicMaterialColorEffect.ambientColor](CustomGraphicsBasicMaterialColorEffect_ambientColor.md), [CustomGraphicsBasicMaterialColorEffect.diffuseColor](CustomGraphicsBasicMaterialColorEffect_diffuseColor.md), [CustomGraphicsBasicMaterialColorEffect.emissiveColor](CustomGraphicsBasicMaterialColorEffect_emissiveColor.md), [CustomGraphicsBasicMaterialColorEffect.specularColor](CustomGraphicsBasicMaterialColorEffect_specularColor.md), [CustomGraphicsCoordinates.getColor](CustomGraphicsCoordinates_getColor.md), [CustomGraphicsShowThroughColorEffect.color](CustomGraphicsShowThroughColorEffect_color.md), [CustomGraphicsSolidColorEffect.color](CustomGraphicsSolidColorEffect_color.md), [FlatPatternComponent.componentColor](FlatPatternComponent_componentColor.md), [SceneSettings.backgroundSolidColor](SceneSettings_backgroundSolidColor.md), [SectionAnalysis.sectionColor](SectionAnalysis_sectionColor.md), [SectionAnalysisInput.sectionColor](SectionAnalysisInput_sectionColor.md), [VolumetricColorSample.value](VolumetricColorSample_value.md)

## Version

Introduced in version August 2014  

