# ValueCommandInput.isMinimumLimited Property

Parent Object: [ValueCommandInput](ValueCommandInput.md)  

## Description

Gets and sets whether the minimum value has a limit. The minimum limit is set using the minimumValue property, and the isMinimumInclusive property controls whether the minimum includes the minimum value or must be greater than the minimum.  

When a new ValueCommandInput is created this defaults to false so there is no limit.

## Syntax

"valueCommandInput_var" is a variable referencing a ValueCommandInput object.  

```python
# Get the value of the property.
propertyValue = valueCommandInput_var.isMinimumLimited

# Set the value of the property.
valueCommandInput_var.isMinimumLimited = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version November 2022  

