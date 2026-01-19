# GraphicsPreferences.minimumFramesPerSecond Property

Parent Object: [GraphicsPreferences](GraphicsPreferences.md)  

## Description

Gets and sets the minimum frames per second. The isDynamic property must be true for this to be considered. Setting this property is only valid when the graphics preset is set to "custom" and will fail if it is set to "quality" or "performance". The graphics preset can be determined by using the graphicsPreset property, as shown below.  

Application.preferences.graphicsPreferences.graphicsPreset

## Syntax

"graphicsPreferences_var" is a variable referencing a GraphicsPreferences object.  

```python
# Get the value of the property.
propertyValue = graphicsPreferences_var.minimumFramesPerSecond

# Set the value of the property.
graphicsPreferences_var.minimumFramesPerSecond = propertyValue
```

## Property Value

This is a read/write property whose value is a double.

## Version

Introduced in version August 2014  

