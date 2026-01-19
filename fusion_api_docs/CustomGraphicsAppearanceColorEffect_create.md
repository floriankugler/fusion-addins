# CustomGraphicsAppearanceColorEffect.create Method

Parent Object: [CustomGraphicsAppearanceColorEffect](CustomGraphicsAppearanceColorEffect.md)  

## Description

Statically creates a new CustomGraphicsAppearanceColorEffect object. This can be used when setting the color property of the various custom graphics objects. With this coloring effect, an existing appearance is used. The appearance must be available in the design where the graphics will be drawn.

## Syntax

This is a static method.  

```python

returnValue = adsk.fusion.CustomGraphicsAppearanceColorEffect.create(appearance)
```

## Return Value

| Type | Description |
|----|----|
| [CustomGraphicsAppearanceColorEffect](CustomGraphicsAppearanceColorEffect.md) | Returns the created CustomGraphicsAppearanceColorEffect or null in case of a failure. |

## Parameters

| Name | Type | Description |
|----|----|----|
| appearance | [Appearance](Appearance.md) | The appearance to use. The appearance must be available in the design where the graphics will be drawn. |

## Version

Introduced in version September 2017  

