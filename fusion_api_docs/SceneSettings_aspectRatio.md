# SceneSettings.aspectRatio Property

Parent Object: [SceneSettings](SceneSettings.md)  

## Description

Gets and sets the aspect ratio of the rendered image. This is not the resolution, but only the aspect ratio. To define a custom aspect ratio set this property to CustomRenderAspectRatio and use the aspectRatioHeight and aspectRatioWidth properties to define any aspect ratio.  

This is used for in-canvas render to allow you to use a different aspect ratio than what is implicitly defined by the size of the active viewport.  

If this is set to CustomRenderAspectRatio, use the aspectRatioHeight and aspectRatioWidth to define the aspect ratio.

## Syntax

"sceneSettings_var" is a variable referencing a SceneSettings object.  

```python
# Get the value of the property.
propertyValue = sceneSettings_var.aspectRatio

# Set the value of the property.
sceneSettings_var.aspectRatio = propertyValue
```

## Property Value

This is a read/write property whose value is a [RenderAspectRatios](RenderAspectRatios.md).

## Version

Introduced in version May 2023  

