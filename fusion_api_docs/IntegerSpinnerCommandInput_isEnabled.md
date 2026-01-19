# IntegerSpinnerCommandInput.isEnabled Property

Parent Object: [IntegerSpinnerCommandInput](IntegerSpinnerCommandInput.md)  

## Description

Gets or sets if this input is currently enabled or disabled for user interaction.  

Currently, the isEnabled property does not disable SelectionCommandInput objects but instead has the same effect as the SelectionCommandInput.hasFocus property.

## Syntax

"integerSpinnerCommandInput_var" is a variable referencing an IntegerSpinnerCommandInput object.  

```python
# Get the value of the property.
propertyValue = integerSpinnerCommandInput_var.isEnabled

# Set the value of the property.
integerSpinnerCommandInput_var.isEnabled = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version July 2015  

