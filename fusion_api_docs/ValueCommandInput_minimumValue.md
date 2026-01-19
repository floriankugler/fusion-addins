# ValueCommandInput.minimumValue Property

Parent Object: [ValueCommandInput](ValueCommandInput.md)  

## Description

Gets and sets the minimum value for the input. Setting this value will automatically set the isMinimumLimited property to true, enabling the use of the minimum value. Use the isMinimumInclusive property to control if the minimum can be equal to this value or must be greater than the minimum.

## Syntax

"valueCommandInput_var" is a variable referencing a ValueCommandInput object.  

```python
# Get the value of the property.
propertyValue = valueCommandInput_var.minimumValue

# Set the value of the property.
valueCommandInput_var.minimumValue = propertyValue
```

## Property Value

This is a read/write property whose value is a double.

## Version

Introduced in version November 2022  

