# DecalInput.opacity Property

Parent Object: [DecalInput](DecalInput.md)  

## Description

Gets and sets the opacity of the decal where 0 is completely transparent and 1.0 is completely opaque. Setting this property to a value outside the range of 0-1 will result in the value being set to the closest valid value.  

Defaults to 1.0 when the input is created.

## Syntax

"decalInput_var" is a variable referencing a DecalInput object.  

```python
# Get the value of the property.
propertyValue = decalInput_var.opacity

# Set the value of the property.
decalInput_var.opacity = propertyValue
```

## Property Value

This is a read/write property whose value is a double.

## Version

Introduced in version September 2024  

