# Canvas.transform Property

Parent Object: [Canvas](Canvas.md)  

## Description

Gets and sets the transform of the canvas. This allows you to control the position, rotation, scaling, and flipping. The X and Y axes defined by the matrix and must be perpendicular to one another.  

This is a 3x3 matrix where the third column controls the position of the canvas and defines the position using 2D coordinates in the model space.

## Syntax

"canvas_var" is a variable referencing a Canvas object.  

```python
# Get the value of the property.
propertyValue = canvas_var.transform

# Set the value of the property.
canvas_var.transform = propertyValue
```

## Property Value

This is a read/write property whose value is a [Matrix2D](Matrix2D.md).

## Version

Introduced in version May 2023  

