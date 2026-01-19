# CustomGraphicsLines.isScreenSpaceLineStyle Property

Parent Object: [CustomGraphicsLines](CustomGraphicsLines.md)  

## Description

Specifies if the line style is computed based on the screen or model space. The default is based on the screen which means the style is drawn the same regardless of how you zoom in or out of the view. That is the length of lines and spaces are based on pixels. If it is drawn relative to model space then the lines and spaces are defined in centimeters and will zooming in and out will change the apparent spacing.

## Syntax

"customGraphicsLines_var" is a variable referencing a CustomGraphicsLines object.  

```python
# Get the value of the property.
propertyValue = customGraphicsLines_var.isScreenSpaceLineStyle

# Set the value of the property.
customGraphicsLines_var.isScreenSpaceLineStyle = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version September 2017  

