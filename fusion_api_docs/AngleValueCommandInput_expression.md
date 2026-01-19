# AngleValueCommandInput.expression Property

Parent Object: [AngleValueCommandInput](AngleValueCommandInput.md)  

## Description

Gets or sets the expression displayed in the input field. This can contain equations and references to parameters but must result in a valid angle expression. If units are not specified as part of the expression, the default user units of degrees are used.

## Syntax

"angleValueCommandInput_var" is a variable referencing an AngleValueCommandInput object.  

```python
# Get the value of the property.
propertyValue = angleValueCommandInput_var.expression

# Set the value of the property.
angleValueCommandInput_var.expression = propertyValue
```

## Property Value

This is a read/write property whose value is a string.

## Version

Introduced in version January 2017  

