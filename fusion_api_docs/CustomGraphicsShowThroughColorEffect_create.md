# CustomGraphicsShowThroughColorEffect.create Method

Parent Object: [CustomGraphicsShowThroughColorEffect](CustomGraphicsShowThroughColorEffect.md)  

## Description

Creates a new CustomGraphicsShowThroughColorEffect object that can be assigned to a custom graphics entity using its showThrough property.

## Syntax

This is a static method.  

```python

returnValue = adsk.fusion.CustomGraphicsShowThroughColorEffect.create(color, opacity)
```

## Return Value

| Type | Description |
|----|----|
| [CustomGraphicsShowThroughColorEffect](CustomGraphicsShowThroughColorEffect.md) | Returns the newly created CustomGraphicsShowThroughColorEffect object or null in the case of failure. This can be assigned to a custom graphics entity using its showThrough property. |

## Parameters

| Name | Type | Description |
|----|----|----|
| color | [Color](Color.md) | The color that will be used to render the custom graphics object. |
| opacity | double | The level of opacity that will be applied when rendering the custom graphics object. A value of 0 is fully translucent and will have the effect of the object being completely covered by objects in front of it. A value of 1 is fully opaque which will have the effect of the object completely covering all objects. Values in between will make objects in front of the graphics object appear translucent to varying degrees so you can see the custom graphics object through it. |

## Version

Introduced in version August 2020  

