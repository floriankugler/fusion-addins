# TriadCommandInput.zTranslation Property

Parent Object: [TriadCommandInput](TriadCommandInput.md)  

## Description

Gets and sets the current value of the translation along the Z axis of the triad. The value is in centimeters but will be displayed to the user in default units for the design.  

The isValidExpressions property should be checked before using the value within the command.

## Syntax

"triadCommandInput_var" is a variable referencing a TriadCommandInput object.  

```python
# Get the value of the property.
propertyValue = triadCommandInput_var.zTranslation

# Set the value of the property.
triadCommandInput_var.zTranslation = propertyValue
```

## Property Value

This is a read/write property whose value is a double.

## Version

Introduced in version May 2022  

