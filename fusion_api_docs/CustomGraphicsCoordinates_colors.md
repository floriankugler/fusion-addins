# CustomGraphicsCoordinates.colors Property

Parent Object: [CustomGraphicsCoordinates](CustomGraphicsCoordinates.md)  

## Description

Gets and sets the colors associated with the coordinate data. This is used when a mesh is displayed using per-vertex coloring. The color at each vertex is represented by four values where they are the red, green, blue, and alpha values. This should contain the same number of colors as vertices.

## Syntax

"customGraphicsCoordinates_var" is a variable referencing a CustomGraphicsCoordinates object.  

```python
# Get the value of the property.
propertyValue = customGraphicsCoordinates_var.colors

# Set the value of the property.
customGraphicsCoordinates_var.colors = propertyValue
```

## Property Value

This is a read/write property whose value is an array of type short.

## Version

Introduced in version September 2017  

