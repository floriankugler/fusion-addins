# ArrangeDefinition2DInput.globalQuantity Property

Parent Object: [ArrangeDefinition2DInput](ArrangeDefinition2DInput.md)  

## Description

Gets and sets the global quantity, which is the default quantity value for components. This defaults to 1.  

This value will become a parameter when the arrangement is created. When created with a real value it must be a whole number. You can also use a string where it is interpreted the same as when entered in the command dialog. The expression must result in a unitless whole number. It's also possible to use an equation like "Total / 4" where "Total" is an existing parameter and be evenly divided by four.

## Syntax

"arrangeDefinition2DInput_var" is a variable referencing an ArrangeDefinition2DInput object.  

```python
# Get the value of the property.
propertyValue = arrangeDefinition2DInput_var.globalQuantity

# Set the value of the property.
arrangeDefinition2DInput_var.globalQuantity = propertyValue
```

## Property Value

This is a read/write property whose value is a [ValueInput](ValueInput.md).

## Version

Introduced in version January 2025  

