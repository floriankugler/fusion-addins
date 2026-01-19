# Canvas.imageFilename Property

Parent Object: [Canvas](Canvas.md)  

## Description

Gets and sets the filename of the image used for the canvas. When getting this property, the filename returned is the file that was used when the canvas was initially created. it's possible the file may no longer exist.  

When setting this property, it is the full filename to the image to use for the canvas. PNG, JPEG, and TIFF files are supported.

## Syntax

"canvas_var" is a variable referencing a Canvas object.  

```python
# Get the value of the property.
propertyValue = canvas_var.imageFilename

# Set the value of the property.
canvas_var.imageFilename = propertyValue
```

## Property Value

This is a read/write property whose value is a string.

## Version

Introduced in version May 2023  

