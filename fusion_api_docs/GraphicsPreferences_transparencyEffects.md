# GraphicsPreferences.transparencyEffects Property

Parent Object: [GraphicsPreferences](GraphicsPreferences.md)  

## Description

Gets and sets the style of display for transparency effects. Setting this property is only valid when the graphics preset is set to "custom" and will fail if it is set to "quality" or "performance". The graphics preset can be determined by using the graphicsPreset property, as shown below.  

Application.preferences.graphicsPreferences.graphicsPreset

## Syntax

"graphicsPreferences_var" is a variable referencing a GraphicsPreferences object.  

```python
# Get the value of the property.
propertyValue = graphicsPreferences_var.transparencyEffects

# Set the value of the property.
graphicsPreferences_var.transparencyEffects = propertyValue
```

## Property Value

This is a read/write property whose value is a [TransparencyDisplayEffects](TransparencyDisplayEffects.md).

## Version

Introduced in version August 2014  

