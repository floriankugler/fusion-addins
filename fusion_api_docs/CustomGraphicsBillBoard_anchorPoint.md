# CustomGraphicsBillBoard.anchorPoint Property

Parent Object: [CustomGraphicsBillBoard](CustomGraphicsBillBoard.md)  

## Description

RETIRED - This property has been retired. It is not needed since the matrix defined for the CustomGraphicsText object defines the position and anchor for the billboarded text. Getting the value of this property will return a point at the origin. Setting this property will be ignored.  Specifies the coordinate in model or view space that the graphics will anchor to. For graphics that represent a label, this will typically be the point where the label attaches to the model. A CustomGraphicsAnchorPoint can be created using the static create method on the CustomGraphicsAnchorPoint object.

## Syntax

"customGraphicsBillBoard_var" is a variable referencing a CustomGraphicsBillBoard object.  

```python
# Get the value of the property.
propertyValue = customGraphicsBillBoard_var.anchorPoint

# Set the value of the property.
customGraphicsBillBoard_var.anchorPoint = propertyValue
```

## Property Value

This is a read/write property whose value is a [Point3D](Point3D.md).

## Version

Introduced in version September 2017  

