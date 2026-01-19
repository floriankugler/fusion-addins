# AngleValueCommandInput.value Property

Parent Object: [AngleValueCommandInput](AngleValueCommandInput.md)  

## Description

Gets and sets the current value of the command input. The value is in radians but will be displayed to the user in degrees. Setting this value can fail if the input value is not within the minimum and maximum value range.  

The isValidExpression property should be checked before using the value within the command because if the expression can't be evaluated there isn't a valid value. Fusion won't allow the execution of a command that contains ValueCommandInput object with invalid expressions so you can dependably use the value in the execute event of the command.

## Syntax

"angleValueCommandInput_var" is a variable referencing an AngleValueCommandInput object.  

```python
# Get the value of the property.
propertyValue = angleValueCommandInput_var.value

# Set the value of the property.
angleValueCommandInput_var.value = propertyValue
```

## Property Value

This is a read/write property whose value is a double.

## Version

Introduced in version January 2017  

