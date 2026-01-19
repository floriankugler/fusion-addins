# CanvasEffects.isGroundPlaneEnabled Property

Parent Object: [CanvasEffects](CanvasEffects.md)  

## Description

Gets and sets if the ground plane is enabled. Setting this property is only valid when the graphics preset is set to "custom" and will fail if it is set to "quality" or "performance". The graphics preset can be determined by using the graphicsPreset property, as shown below.  

Application.preferences.graphicsPreferences.graphicsPreset

## Syntax

"canvasEffects_var" is a variable referencing a CanvasEffects object.  

```python
# Get the value of the property.
propertyValue = canvasEffects_var.isGroundPlaneEnabled

# Set the value of the property.
canvasEffects_var.isGroundPlaneEnabled = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version May 2025  

