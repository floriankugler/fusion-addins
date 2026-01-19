# Rendering.resolutionHeight Property

Parent Object: [Rendering](Rendering.md)  

## Description

Gets and sets the height of the image in pixels. If anything but CustomRenderAspectRatio is defined as the aspect ratio, the resolution width will be modified to maintain the specified aspect ratio. The height must be between 108 and 4000 pixels.

## Syntax

"rendering_var" is a variable referencing a Rendering object.  

```python
# Get the value of the property.
propertyValue = rendering_var.resolutionHeight

# Set the value of the property.
rendering_var.resolutionHeight = propertyValue
```

## Property Value

This is a read/write property whose value is an integer.

## Version

Introduced in version May 2023  

