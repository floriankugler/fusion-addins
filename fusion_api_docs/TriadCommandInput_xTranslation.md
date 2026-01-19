# TriadCommandInput.xTranslation Property

Parent Object: [TriadCommandInput](TriadCommandInput.md)  

## Description

Gets and sets the current value of the translation along the X axis of the triad. The value is in centimeters but will be displayed to the user in default units for the design.  

The isValidExpressions property should be checked before using the returned value.

## Syntax

"triadCommandInput_var" is a variable referencing a TriadCommandInput object.  

```python
# Get the value of the property.
propertyValue = triadCommandInput_var.xTranslation

# Set the value of the property.
triadCommandInput_var.xTranslation = propertyValue
```

## Property Value

This is a read/write property whose value is a double.

## Version

Introduced in version May 2022  

