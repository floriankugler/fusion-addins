# GraphicsPreferences.graphicsPreset Property

Parent Object: [GraphicsPreferences](GraphicsPreferences.md)  

## Description

Gets and sets if the different graphics settings are using predefined settings to get the best performance, quality, or are custom to allow any settings. Setting this to performance or quality will result in other graphics settings changing to match the defined preset.

## Syntax

"graphicsPreferences_var" is a variable referencing a GraphicsPreferences object.  

```python
# Get the value of the property.
propertyValue = graphicsPreferences_var.graphicsPreset

# Set the value of the property.
graphicsPreferences_var.graphicsPreset = propertyValue
```

## Property Value

This is a read/write property whose value is a [GraphicsPresets](GraphicsPresets.md).

## Version

Introduced in version May 2025  

