# TriadCommandInput.zRotation Property

Parent Object: [TriadCommandInput](TriadCommandInput.md)  

## Description

Gets and sets the current value of the rotation around the Z axis of the triad. The value is in radians but will be displayed to the user in degrees.  

The isValidExpressions property should be checked before using the value within the command.

## Syntax

"triadCommandInput_var" is a variable referencing a TriadCommandInput object.  

```python
# Get the value of the property.
propertyValue = triadCommandInput_var.zRotation

# Set the value of the property.
triadCommandInput_var.zRotation = propertyValue
```

## Property Value

This is a read/write property whose value is a double.

## Version

Introduced in version May 2022  

