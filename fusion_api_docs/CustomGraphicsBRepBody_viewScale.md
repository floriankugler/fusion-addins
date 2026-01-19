# CustomGraphicsBRepBody.viewScale Property

Parent Object: [CustomGraphicsBRepBody](CustomGraphicsBRepBody.md)  

## Description

Gets and sets the graphics view scale being applied to this graphics entity. A CustomGraphicsViewScale object can be created using the static create method of the class. When assigned to a graphics entity the size of the graphics entity is defined in view space (pixels) instead of model space (centimeters).

## Syntax

"customGraphicsBRepBody_var" is a variable referencing a CustomGraphicsBRepBody object.  

```python
# Get the value of the property.
propertyValue = customGraphicsBRepBody_var.viewScale

# Set the value of the property.
customGraphicsBRepBody_var.viewScale = propertyValue
```

## Property Value

This is a read/write property whose value is a [CustomGraphicsViewScale](CustomGraphicsViewScale.md).

## Version

Introduced in version September 2017  

