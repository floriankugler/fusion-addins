# CanvasInput.opacity Property

Parent Object: [CanvasInput](CanvasInput.md)  

## Description

Gets and sets the opacity of the canvas where 0 is completely transparent and 100 is completely opaque. Setting this property to a value outside the range of 0-100 will result in the value being set to the closest valid value.  

Defaults to 50 when the input is created.

## Syntax

"canvasInput_var" is a variable referencing a CanvasInput object.  

```python
# Get the value of the property.
propertyValue = canvasInput_var.opacity

# Set the value of the property.
canvasInput_var.opacity = propertyValue
```

## Property Value

This is a read/write property whose value is an integer.

## Version

Introduced in version May 2023  

