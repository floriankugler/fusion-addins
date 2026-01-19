# CanvasInput.planarEntity Property

Parent Object: [CanvasInput](CanvasInput.md)  

## Description

Gets and sets the plane the canvas is associated with. This can be either a planar Face or a construction plane. In a direct modeling design or the canvas is being created in a base feature, this can be a Plane object.

## Syntax

"canvasInput_var" is a variable referencing a CanvasInput object.  

```python
# Get the value of the property.
propertyValue = canvasInput_var.planarEntity

# Set the value of the property.
canvasInput_var.planarEntity = propertyValue
```

## Property Value

This is a read/write property whose value is a [Base](Base.md).

## Version

Introduced in version May 2023  

