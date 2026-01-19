# ValueCommandInput.isMaximumLimited Property

Parent Object: [ValueCommandInput](ValueCommandInput.md)  

## Description

Gets and sets whether the maximum value has a limit. The maximum limit is set using the maximumValue property, and the isMaximumInclusive property controls whether the maximum includes the maximum value or must be less than the maximum.  

When a new ValueCommandInput is created this defaults to false so there is no limit.

## Syntax

"valueCommandInput_var" is a variable referencing a ValueCommandInput object.  

```python
# Get the value of the property.
propertyValue = valueCommandInput_var.isMaximumLimited

# Set the value of the property.
valueCommandInput_var.isMaximumLimited = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version November 2022  

