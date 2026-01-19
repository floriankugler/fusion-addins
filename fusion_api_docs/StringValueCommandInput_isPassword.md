# StringValueCommandInput.isPassword Property

Parent Object: [StringValueCommandInput](StringValueCommandInput.md)  

## Description

Gets or sets if this string input behaves as a password field. This defaults to false for a newly created StringValueCommandInput. If true, dots are displayed instead of the actual characters but the value property will get and set the actual string.

## Syntax

"stringValueCommandInput_var" is a variable referencing a StringValueCommandInput object.  

```python
# Get the value of the property.
propertyValue = stringValueCommandInput_var.isPassword

# Set the value of the property.
stringValueCommandInput_var.isPassword = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version June 2015  

