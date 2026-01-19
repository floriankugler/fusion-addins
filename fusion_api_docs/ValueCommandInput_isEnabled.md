# ValueCommandInput.isEnabled Property

Parent Object: [ValueCommandInput](ValueCommandInput.md)  

## Description

Gets or sets if this input is currently enabled or disabled for user interaction.  

Currently, the isEnabled property does not disable SelectionCommandInput objects but instead has the same effect as the SelectionCommandInput.hasFocus property.

## Syntax

"valueCommandInput_var" is a variable referencing a ValueCommandInput object.  

```python
# Get the value of the property.
propertyValue = valueCommandInput_var.isEnabled

# Set the value of the property.
valueCommandInput_var.isEnabled = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version August 2014  

