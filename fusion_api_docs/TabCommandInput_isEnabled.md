# TabCommandInput.isEnabled Property

Parent Object: [TabCommandInput](TabCommandInput.md)  

## Description

Gets or sets if this input is currently enabled or disabled for user interaction.  

Currently, the isEnabled property does not disable SelectionCommandInput objects but instead has the same effect as the SelectionCommandInput.hasFocus property.

## Syntax

"tabCommandInput_var" is a variable referencing a TabCommandInput object.  

```python
# Get the value of the property.
propertyValue = tabCommandInput_var.isEnabled

# Set the value of the property.
tabCommandInput_var.isEnabled = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version July 2015  

