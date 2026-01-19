# CanvasInput.transform Property

Parent Object: [CanvasInput](CanvasInput.md)  

## Description

Gets and sets the transform of the canvas. This allows you to control the position, rotation, scaling, and flipping. The X and Y axes defined by the matrix, must be perpendicular to one another. The directions of the X and Y axes defines the orientation of the image.  

This is a 3x3 matrix where the third column controls the position of the canvas and is relative to the parameter space of the plane defined by the specified planar face or construction plane.

## Syntax

"canvasInput_var" is a variable referencing a CanvasInput object.  

```python
# Get the value of the property.
propertyValue = canvasInput_var.transform

# Set the value of the property.
canvasInput_var.transform = propertyValue
```

## Property Value

This is a read/write property whose value is a [Matrix2D](Matrix2D.md).

## Version

Introduced in version May 2023  

