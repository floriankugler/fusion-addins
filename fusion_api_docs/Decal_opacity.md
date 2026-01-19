# Decal.opacity Property

Parent Object: [Decal](Decal.md)  

## Description

Gets and sets the opacity of the decal where 0 is completely transparent and 1.0 is completely opaque. Setting this property to a value outside the range of 0-1 will result in the value being set to the closest valid value.  

Defaults to 1.0 when the input is created.

## Syntax

"decal_var" is a variable referencing a Decal object.  

```python
# Get the value of the property.
propertyValue = decal_var.opacity

# Set the value of the property.
decal_var.opacity = propertyValue
```

## Property Value

This is a read/write property whose value is a double.

## Version

Introduced in version September 2024  

