# DropDownCommandInput.isEnabled Property

Parent Object: [DropDownCommandInput](DropDownCommandInput.md)  

## Description

Gets or sets if this input is currently enabled or disabled for user interaction.  

Currently, the isEnabled property does not disable SelectionCommandInput objects but instead has the same effect as the SelectionCommandInput.hasFocus property.

## Syntax

"dropDownCommandInput_var" is a variable referencing a DropDownCommandInput object.  

```python
# Get the value of the property.
propertyValue = dropDownCommandInput_var.isEnabled

# Set the value of the property.
dropDownCommandInput_var.isEnabled = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version January 2015  

