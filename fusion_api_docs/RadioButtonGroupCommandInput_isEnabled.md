# RadioButtonGroupCommandInput.isEnabled Property

Parent Object: [RadioButtonGroupCommandInput](RadioButtonGroupCommandInput.md)  

## Description

Gets or sets if this input is currently enabled or disabled for user interaction.  

Currently, the isEnabled property does not disable SelectionCommandInput objects but instead has the same effect as the SelectionCommandInput.hasFocus property.

## Syntax

"radioButtonGroupCommandInput_var" is a variable referencing a RadioButtonGroupCommandInput object.  

```python
# Get the value of the property.
propertyValue = radioButtonGroupCommandInput_var.isEnabled

# Set the value of the property.
radioButtonGroupCommandInput_var.isEnabled = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version July 2015  

