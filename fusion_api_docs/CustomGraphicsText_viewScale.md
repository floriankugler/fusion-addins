# CustomGraphicsText.viewScale Property

Parent Object: [CustomGraphicsText](CustomGraphicsText.md)  

## Description

Gets and sets the graphics view scale being applied to this graphics entity. A CustomGraphicsViewScale object can be created using the static create method of the class. When assigned to a graphics entity the size of the graphics entity is defined in view space (pixels) instead of model space (centimeters).

## Syntax

"customGraphicsText_var" is a variable referencing a CustomGraphicsText object.  

```python
# Get the value of the property.
propertyValue = customGraphicsText_var.viewScale

# Set the value of the property.
customGraphicsText_var.viewScale = propertyValue
```

## Property Value

This is a read/write property whose value is a [CustomGraphicsViewScale](CustomGraphicsViewScale.md).

## Version

Introduced in version September 2017  

