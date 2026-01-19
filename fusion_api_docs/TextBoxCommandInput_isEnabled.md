# TextBoxCommandInput.isEnabled Property

Parent Object: [TextBoxCommandInput](TextBoxCommandInput.md)  

## Description

Gets or sets if this input is currently enabled or disabled for user interaction.  

Currently, the isEnabled property does not disable SelectionCommandInput objects but instead has the same effect as the SelectionCommandInput.hasFocus property.

## Syntax

"textBoxCommandInput_var" is a variable referencing a TextBoxCommandInput object.  

```python
# Get the value of the property.
propertyValue = textBoxCommandInput_var.isEnabled

# Set the value of the property.
textBoxCommandInput_var.isEnabled = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version June 2015  

