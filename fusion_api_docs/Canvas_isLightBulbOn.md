# Canvas.isLightBulbOn Property

Parent Object: [Canvas](Canvas.md)  

## Description

Gets and sets if the light bulb of this canvas as displayed in the browser is on or off.  

A canvas will only be visible if the light bulb is switched on. However, the light bulb can be on and the canvas still invisible if the visibility of a higher level occurrence has its light bulb off or if the light bulb for Canvases folder is off to turn off all canvases in a component.

## Syntax

"canvas_var" is a variable referencing a Canvas object.  

```python
# Get the value of the property.
propertyValue = canvas_var.isLightBulbOn

# Set the value of the property.
canvas_var.isLightBulbOn = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version May 2023  

