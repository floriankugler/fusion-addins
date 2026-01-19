# CustomGraphicsLines.isLineStrip Property

Parent Object: [CustomGraphicsLines](CustomGraphicsLines.md)  

## Description

Defines if the coordinates are used to define a series of individual lines or a connected set of lines (line strip). If individual lines are drawn (this property is false), each pair of coordinates define a single line. If a line strip is drawn (this property is true), the first pair of coordinates define the first line and the third coordinate defines a line that connects to the second coordinate. The fourth coordinate creates a line connecting to the third coordinate, and so on.

## Syntax

"customGraphicsLines_var" is a variable referencing a CustomGraphicsLines object.  

```python
# Get the value of the property.
propertyValue = customGraphicsLines_var.isLineStrip

# Set the value of the property.
customGraphicsLines_var.isLineStrip = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version September 2017  

