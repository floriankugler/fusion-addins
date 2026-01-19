# TriadCommandInput.isEnabled Property

Parent Object: [TriadCommandInput](TriadCommandInput.md)  

## Description

Gets or sets if this input is currently enabled or disabled for user interaction.  

Currently, the isEnabled property does not disable SelectionCommandInput objects but instead has the same effect as the SelectionCommandInput.hasFocus property.

## Syntax

"triadCommandInput_var" is a variable referencing a TriadCommandInput object.  

```python
# Get the value of the property.
propertyValue = triadCommandInput_var.isEnabled

# Set the value of the property.
triadCommandInput_var.isEnabled = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version May 2022  

