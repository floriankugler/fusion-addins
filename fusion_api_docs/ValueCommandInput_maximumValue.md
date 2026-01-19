# ValueCommandInput.maximumValue Property

Parent Object: [ValueCommandInput](ValueCommandInput.md)  

## Description

Gets and sets the maximum value for the input. Setting this value will automatically set the isMaximumLimited property to true, enabling the use of the maximum value. Use the isMaximumInclusive property to control if the maximum can be equal to this value or must be less than the maximum.

## Syntax

"valueCommandInput_var" is a variable referencing a ValueCommandInput object.  

```python
# Get the value of the property.
propertyValue = valueCommandInput_var.maximumValue

# Set the value of the property.
valueCommandInput_var.maximumValue = propertyValue
```

## Property Value

This is a read/write property whose value is a double.

## Version

Introduced in version November 2022  

