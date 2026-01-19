# CustomGraphicsGroup.viewPlacement Property

Parent Object: [CustomGraphicsGroup](CustomGraphicsGroup.md)  

## Description

Gets and sets the graphics view placement being applied to this graphics entity. A CustomGraphicsViewPlacement object can be created using the static create method of the class. When assigned to a graphics entity the position of the graphics is defined relative to the view in 2D view space (pixels) rather than in 3D model space (centimeters).

## Syntax

"customGraphicsGroup_var" is a variable referencing a CustomGraphicsGroup object.  

```python
# Get the value of the property.
propertyValue = customGraphicsGroup_var.viewPlacement

# Set the value of the property.
customGraphicsGroup_var.viewPlacement = propertyValue
```

## Property Value

This is a read/write property whose value is a [CustomGraphicsViewPlacement](CustomGraphicsViewPlacement.md).

## Version

Introduced in version September 2017  

