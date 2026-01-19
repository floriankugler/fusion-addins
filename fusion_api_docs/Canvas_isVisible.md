# Canvas.isVisible Property

Parent Object: [Canvas](Canvas.md)  

## Description

Returns if the canvas is currently visible in the graphics window. The isLightBulbOn property of the canvas controls if the canvas should be displayed or not, but even when true, the canvas may not be visible because the occurrence that references the component may not be visible. It's also possible to turn off the visibility of all canvases for a component. This property takes all of that into account when reporting if the canvas is visible or not.

## Syntax

"canvas_var" is a variable referencing a Canvas object.  

```python
# Get the value of the property.
propertyValue = canvas_var.isVisible
```

## Property Value

This is a read only property whose value is a boolean.

## Version

Introduced in version May 2023  

