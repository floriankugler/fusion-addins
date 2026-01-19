# DirectionCommandInput.isEnabled Property

Parent Object: [DirectionCommandInput](DirectionCommandInput.md)  

## Description

Gets or sets if this input is currently enabled or disabled for user interaction.  

Currently, the isEnabled property does not disable SelectionCommandInput objects but instead has the same effect as the SelectionCommandInput.hasFocus property.

## Syntax

"directionCommandInput_var" is a variable referencing a DirectionCommandInput object.  

```python
# Get the value of the property.
propertyValue = directionCommandInput_var.isEnabled

# Set the value of the property.
directionCommandInput_var.isEnabled = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version January 2016  

