# GraphicsPreferences.isWoodBumpEnabled Property

Parent Object: [GraphicsPreferences](GraphicsPreferences.md)  

## Description

Gets and sets whether the bump effect is enabled when supported by the Wood (Solid) and the graphics driver. Setting this property is only valid when the graphics preset is set to "custom" and will fail if it is set to "quality" or "performance". The graphics preset can be determined by using the graphicsPreset property, as shown below.  

Application.preferences.graphicsPreferences.graphicsPreset

## Syntax

"graphicsPreferences_var" is a variable referencing a GraphicsPreferences object.  

```python
# Get the value of the property.
propertyValue = graphicsPreferences_var.isWoodBumpEnabled

# Set the value of the property.
graphicsPreferences_var.isWoodBumpEnabled = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version May 2022  

