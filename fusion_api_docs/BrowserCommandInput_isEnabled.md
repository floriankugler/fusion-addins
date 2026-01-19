# BrowserCommandInput.isEnabled Property

Parent Object: [BrowserCommandInput](BrowserCommandInput.md)  

## Description

Gets or sets if this input is currently enabled or disabled for user interaction.  

Currently, the isEnabled property does not disable SelectionCommandInput objects but instead has the same effect as the SelectionCommandInput.hasFocus property.

## Syntax

"browserCommandInput_var" is a variable referencing a BrowserCommandInput object.  

```python
# Get the value of the property.
propertyValue = browserCommandInput_var.isEnabled

# Set the value of the property.
browserCommandInput_var.isEnabled = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version July 2021  

