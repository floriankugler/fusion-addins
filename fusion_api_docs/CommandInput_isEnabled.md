# CommandInput.isEnabled Property

Parent Object: [CommandInput](CommandInput.md)  

## Description

Gets or sets if this input is currently enabled or disabled for user interaction.  

Currently, the isEnabled property does not disable SelectionCommandInput objects but instead has the same effect as the SelectionCommandInput.hasFocus property.

## Syntax

"commandInput_var" is a variable referencing a CommandInput object.  

```python
# Get the value of the property.
propertyValue = commandInput_var.isEnabled

# Set the value of the property.
commandInput_var.isEnabled = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version August 2014  

