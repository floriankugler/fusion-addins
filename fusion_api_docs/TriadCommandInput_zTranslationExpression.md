# TriadCommandInput.zTranslationExpression Property

Parent Object: [TriadCommandInput](TriadCommandInput.md)  

## Description

Gets or sets the expression displayed in the input field for the Z translation. This can contain equations and references to parameters but must result in a valid distance expression. If units are not specified as part of the expression, the default user units of length are used.

## Syntax

"triadCommandInput_var" is a variable referencing a TriadCommandInput object.  

```python
# Get the value of the property.
propertyValue = triadCommandInput_var.zTranslationExpression

# Set the value of the property.
triadCommandInput_var.zTranslationExpression = propertyValue
```

## Property Value

This is a read/write property whose value is a string.

## Version

Introduced in version May 2022  

