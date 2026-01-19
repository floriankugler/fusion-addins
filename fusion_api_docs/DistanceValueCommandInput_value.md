# DistanceValueCommandInput.value Property

Parent Object: [DistanceValueCommandInput](DistanceValueCommandInput.md)  

## Description

Gets and sets the current value of the command input. The value is in centimeters but will be displayed to the user in the current default document units. Setting this value can fail if the input value is not within the minimum and maximum value range.  

The isValidExpression property should be checked before using this value within the command because if the expression can't be evaluated there isn't a valid value. Fusion won't allow the execution of a command that contains ValueCommandInput object with invalid expressions so you can dependably use the value in the execute event of the command.

## Syntax

"distanceValueCommandInput_var" is a variable referencing a DistanceValueCommandInput object.  

```python
# Get the value of the property.
propertyValue = distanceValueCommandInput_var.value

# Set the value of the property.
distanceValueCommandInput_var.value = propertyValue
```

## Property Value

This is a read/write property whose value is a double.

## Version

Introduced in version January 2016  

