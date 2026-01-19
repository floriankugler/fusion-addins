# AngleValueCommandInput.isEnabled Property

Parent Object: [AngleValueCommandInput](AngleValueCommandInput.md)  

## Description

Gets or sets if this input is currently enabled or disabled for user interaction.  

Currently, the isEnabled property does not disable SelectionCommandInput objects but instead has the same effect as the SelectionCommandInput.hasFocus property.

## Syntax

"angleValueCommandInput_var" is a variable referencing an AngleValueCommandInput object.  

```python
# Get the value of the property.
propertyValue = angleValueCommandInput_var.isEnabled

# Set the value of the property.
angleValueCommandInput_var.isEnabled = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version January 2017  

