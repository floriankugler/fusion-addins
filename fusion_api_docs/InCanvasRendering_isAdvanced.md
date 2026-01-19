# InCanvasRendering.isAdvanced Property

Parent Object: [InCanvasRendering](InCanvasRendering.md)  

## Description

Gets and sets if "Fast" or "Advanced" rendering should be used. If false, "Fast" rendering is used, which uses simplified lighting and materials.  

There are two modes when doing in-canvas rendering; advanced and fast. When using advanced rendering, you can specify the desired quality and the rendering will stop once that quality has been reached. When using fast rendering, the rendering never stops but continues until you stop it.  

When using the API, it's generally best to use advanced rendering so you can easily control the final quality and get notified by the renderComplete event when it has finished. When using fast rendering, the renderComplete event is not fired, and you have to use some other criteria like the number of iterations complete, or the time taken to determine when to stop the rendering process.

## Syntax

"inCanvasRendering_var" is a variable referencing an InCanvasRendering object.  

```python
# Get the value of the property.
propertyValue = inCanvasRendering_var.isAdvanced

# Set the value of the property.
inCanvasRendering_var.isAdvanced = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version September 2023  

