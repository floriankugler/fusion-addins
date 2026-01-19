# FloatSpinnerCommandInput.value Property

Parent Object: [FloatSpinnerCommandInput](FloatSpinnerCommandInput.md)  

## Description

Gets and sets the value associated with this input. The value is always in the database units of the unit type specified. For example, if the unit type is "inch" this value is in centimeters since centimeters are the database length unit. When setting the value it is converted into a string using the unit type and displayed in the input box.  

The isValidExpression property should be checked before using this value within the command because if the expression can't be evaluated there isn't a valid value. Fusion won't allow the execution of a command that contains ValueCommandInput object with invalid expressions so you can dependably use the value in the execute event of the command.

## Syntax

"floatSpinnerCommandInput_var" is a variable referencing a FloatSpinnerCommandInput object.  

```python
# Get the value of the property.
propertyValue = floatSpinnerCommandInput_var.value

# Set the value of the property.
floatSpinnerCommandInput_var.value = propertyValue
```

## Property Value

This is a read/write property whose value is a double.

## Version

Introduced in version July 2015  

