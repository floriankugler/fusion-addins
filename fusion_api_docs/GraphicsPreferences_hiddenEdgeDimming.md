# GraphicsPreferences.hiddenEdgeDimming Property

Parent Object: [GraphicsPreferences](GraphicsPreferences.md)  

## Description

Gets and sets the dimming percentage to use for hidden edges. the value is a percentage expressed by a value between 0 and 100. Setting this property is only valid when the graphics preset is set to "custom" and will fail if it is set to "quality" or "performance". The graphics preset can be determined by using the graphicsPreset property, as shown below.  

Application.preferences.graphicsPreferences.graphicsPreset

## Syntax

"graphicsPreferences_var" is a variable referencing a GraphicsPreferences object.  

```python
# Get the value of the property.
propertyValue = graphicsPreferences_var.hiddenEdgeDimming

# Set the value of the property.
graphicsPreferences_var.hiddenEdgeDimming = propertyValue
```

## Property Value

This is a read/write property whose value is an integer.

## Version

Introduced in version August 2014  

