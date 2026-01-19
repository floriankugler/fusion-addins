# SetupInput.isUsingPreviousSetupData Property

Parent Object: [SetupInput](SetupInput.md)  

## Description

Get and set if data from the previous setup should be used when creating another setup. The data applied from the previous setup is machine information and the stock from the preceeding setup. By default this value is false.

## Syntax

"setupInput_var" is a variable referencing a SetupInput object.  

```python
# Get the value of the property.
propertyValue = setupInput_var.isUsingPreviousSetupData

# Set the value of the property.
setupInput_var.isUsingPreviousSetupData = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version January 2025  

