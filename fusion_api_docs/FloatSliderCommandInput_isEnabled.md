# FloatSliderCommandInput.isEnabled Property

Parent Object: [FloatSliderCommandInput](FloatSliderCommandInput.md)  

## Description

Gets or sets if this input is currently enabled or disabled for user interaction.  

Currently, the isEnabled property does not disable SelectionCommandInput objects but instead has the same effect as the SelectionCommandInput.hasFocus property.

## Syntax

"floatSliderCommandInput_var" is a variable referencing a FloatSliderCommandInput object.  

```python
# Get the value of the property.
propertyValue = floatSliderCommandInput_var.isEnabled

# Set the value of the property.
floatSliderCommandInput_var.isEnabled = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version June 2015  

