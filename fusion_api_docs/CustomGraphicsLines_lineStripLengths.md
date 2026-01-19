# CustomGraphicsLines.lineStripLengths Property

Parent Object: [CustomGraphicsLines](CustomGraphicsLines.md)  

## Description

If isLineStrip is true, this property defines the number of coordinates to use in the line strips. It is an array of integers that defines the number of coordinates for each line strip. An empty array indicates that a single line strip is to be drawn.

## Syntax

"customGraphicsLines_var" is a variable referencing a CustomGraphicsLines object.  

```python
# Get the value of the property.
propertyValue = customGraphicsLines_var.lineStripLengths

# Set the value of the property.
customGraphicsLines_var.lineStripLengths = propertyValue
```

## Property Value

This is a read/write property whose value is an array of type integer.

## Version

Introduced in version September 2017  

