# ButtonRowCommandInput.isEnabled Property

Parent Object: [ButtonRowCommandInput](ButtonRowCommandInput.md)  

## Description

Gets or sets if this input is currently enabled or disabled for user interaction.  

Currently, the isEnabled property does not disable SelectionCommandInput objects but instead has the same effect as the SelectionCommandInput.hasFocus property.

## Syntax

"buttonRowCommandInput_var" is a variable referencing a ButtonRowCommandInput object.  

```python
# Get the value of the property.
propertyValue = buttonRowCommandInput_var.isEnabled

# Set the value of the property.
buttonRowCommandInput_var.isEnabled = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version June 2015  

