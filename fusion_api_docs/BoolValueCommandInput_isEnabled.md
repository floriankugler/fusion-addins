# BoolValueCommandInput.isEnabled Property

Parent Object: [BoolValueCommandInput](BoolValueCommandInput.md)  

## Description

Gets or sets if this input is currently enabled or disabled for user interaction.  

Currently, the isEnabled property does not disable SelectionCommandInput objects but instead has the same effect as the SelectionCommandInput.hasFocus property.

## Syntax

"boolValueCommandInput_var" is a variable referencing a BoolValueCommandInput object.  

```python
# Get the value of the property.
propertyValue = boolValueCommandInput_var.isEnabled

# Set the value of the property.
boolValueCommandInput_var.isEnabled = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version August 2014  

