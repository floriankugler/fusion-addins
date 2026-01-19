# FloatSliderCommandInput.valueTwo Property

Parent Object: [FloatSliderCommandInput](FloatSliderCommandInput.md)  

## Description

Gets or sets the second value associated with this input. The value is always in the database units of the unit type specified. For example, if the unit type is "inch" this value is in centimeters since centimeters are the database length unit. When setting the value it is converted into a string using the unit type and displayed in the input box.  

This property is only available when the hasTwoSliders property returns true.

## Syntax

"floatSliderCommandInput_var" is a variable referencing a FloatSliderCommandInput object.  

```python
# Get the value of the property.
propertyValue = floatSliderCommandInput_var.valueTwo

# Set the value of the property.
floatSliderCommandInput_var.valueTwo = propertyValue
```

## Property Value

This is a read/write property whose value is a double.

## Version

Introduced in version June 2015  

