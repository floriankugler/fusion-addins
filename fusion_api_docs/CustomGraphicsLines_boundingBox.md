# CustomGraphicsLines.boundingBox Property

Parent Object: [CustomGraphicsLines](CustomGraphicsLines.md)  

## Description

Returns a box oriented parallel to the world x-y-x axes that contains the graphics entity. Depending on whether the graphics are drawn in model space or screen space this will return the bounding box in either centimeters (model) or pixels (screen). In the case where it returns the bounding box in pixel space, the Z coordinates of the box will be 0 and can be ignored.

## Syntax

"customGraphicsLines_var" is a variable referencing a CustomGraphicsLines object.  

```python
# Get the value of the property.
propertyValue = customGraphicsLines_var.boundingBox
```

## Property Value

This is a read only property whose value is a [BoundingBox3D](BoundingBox3D.md).

## Version

Introduced in version September 2017  

