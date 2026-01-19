# CustomGraphicsCurve.id Property

Parent Object: [CustomGraphicsCurve](CustomGraphicsCurve.md)  

## Description

An id you can specify for the entity. By default, all new graphics entities do not have an id and this property will return an empty string. But in cases where entities will be selected, assigning an id can make understanding what was selected much easier.

## Syntax

"customGraphicsCurve_var" is a variable referencing a CustomGraphicsCurve object.  

```python
# Get the value of the property.
propertyValue = customGraphicsCurve_var.id

# Set the value of the property.
customGraphicsCurve_var.id = propertyValue
```

## Property Value

This is a read/write property whose value is a string.

## Version

Introduced in version September 2017  

