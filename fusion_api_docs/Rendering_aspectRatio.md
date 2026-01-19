# Rendering.aspectRatio Property

Parent Object: [Rendering](Rendering.md)  

## Description

Gets and sets the aspect ratio of the rendered image. This is not the resolution, but only the aspect ratio. To define a custom aspect ratio set this property to CustomAspectRatio and use the resolutionHeight and resolutionWidth properties to define the resolution and aspect ratio. The default value is the aspect ratio defined in the scene settings. The width and height must be between 108 and 4000 pixels.

## Syntax

"rendering_var" is a variable referencing a Rendering object.  

```python
# Get the value of the property.
propertyValue = rendering_var.aspectRatio

# Set the value of the property.
rendering_var.aspectRatio = propertyValue
```

## Property Value

This is a read/write property whose value is a [RenderAspectRatios](RenderAspectRatios.md).

## Version

Introduced in version May 2023  

