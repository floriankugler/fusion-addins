# CustomGraphicsViewPlacement.viewPoint Property

Parent Object: [CustomGraphicsViewPlacement](CustomGraphicsViewPlacement.md)  

## Description

A 2D point in the view that defines the position of the graphics. This is relative to the corner and is in pixels. The x and y directions vary for each of the corners. These directions are only used to position the 2D point and do not affect the standard coordinate system the graphics were drawn in.  

upperLeftViewCorner - The x direction is to the right and y is down.  

upperRightViewCorner - The x direction is to the left and y is down.  

lowerLeftViewCorner - The x direction is to the right and y is up.  

lowerRightViewCorner - The x direction is to the left and y is up.

## Syntax

"customGraphicsViewPlacement_var" is a variable referencing a CustomGraphicsViewPlacement object.  

```python
# Get the value of the property.
propertyValue = customGraphicsViewPlacement_var.viewPoint

# Set the value of the property.
customGraphicsViewPlacement_var.viewPoint = propertyValue
```

## Property Value

This is a read/write property whose value is a [Point2D](Point2D.md).

## Version

Introduced in version September 2017  

