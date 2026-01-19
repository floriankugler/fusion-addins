# CustomGraphicsLines.indexList Property

Parent Object: [CustomGraphicsLines](CustomGraphicsLines.md)  

## Description

Gets and sets an array of integers that represent indices into the coordinates to define the order the coordinates are used to draw the lines. An empty array indicates that no index list is used and coordinates are used in the order they're provided in the provided CustomGraphicsCoordinates object.

## Syntax

"customGraphicsLines_var" is a variable referencing a CustomGraphicsLines object.  

```python
# Get the value of the property.
propertyValue = customGraphicsLines_var.indexList

# Set the value of the property.
customGraphicsLines_var.indexList = propertyValue
```

## Property Value

This is a read/write property whose value is an array of type integer.

## Version

Introduced in version September 2017  

