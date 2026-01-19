# CustomGraphicsGroup.viewScale Property

Parent Object: [CustomGraphicsGroup](CustomGraphicsGroup.md)  

## Description

Gets and sets the graphics view scale being applied to this graphics entity. A CustomGraphicsViewScale object can be created using the static create method of the class. When assigned to a graphics entity the size of the graphics entity is defined in view space (pixels) instead of model space (centimeters).

## Syntax

"customGraphicsGroup_var" is a variable referencing a CustomGraphicsGroup object.  

```python
# Get the value of the property.
propertyValue = customGraphicsGroup_var.viewScale

# Set the value of the property.
customGraphicsGroup_var.viewScale = propertyValue
```

## Property Value

This is a read/write property whose value is a [CustomGraphicsViewScale](CustomGraphicsViewScale.md).

## Version

Introduced in version September 2017  

