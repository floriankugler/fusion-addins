# SceneSettings.aspectRatioHeight Property

Parent Object: [SceneSettings](SceneSettings.md)  

## Description

Gets and sets the height of the aspect ratio of the rendered image. This is not the resolution, but only the aspect ratio. For example specifying the width and height of 4:3 is equivalent to setting 20:15. It's only the ratio of the numbers that matters.  

The resolution is determined by the screen resolution when rendering in-canvas or is specified when rendering locally or using the cloud. When setting this property the aspectRatio property is automatically set to CustomRenderAspectRatio.

## Syntax

"sceneSettings_var" is a variable referencing a SceneSettings object.  

```python
# Get the value of the property.
propertyValue = sceneSettings_var.aspectRatioHeight

# Set the value of the property.
sceneSettings_var.aspectRatioHeight = propertyValue
```

## Property Value

This is a read/write property whose value is an integer.

## Version

Introduced in version May 2023  

