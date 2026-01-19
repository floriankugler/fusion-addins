# TableCommandInput.isEnabled Property

Parent Object: [TableCommandInput](TableCommandInput.md)  

## Description

Gets or sets if this input is currently enabled or disabled for user interaction.  

Currently, the isEnabled property does not disable SelectionCommandInput objects but instead has the same effect as the SelectionCommandInput.hasFocus property.

## Syntax

"tableCommandInput_var" is a variable referencing a TableCommandInput object.  

```python
# Get the value of the property.
propertyValue = tableCommandInput_var.isEnabled

# Set the value of the property.
tableCommandInput_var.isEnabled = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version September 2016  

