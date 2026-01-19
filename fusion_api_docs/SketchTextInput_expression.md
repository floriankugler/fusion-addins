# SketchTextInput.expression Property

Parent Object: [SketchTextInput](SketchTextInput.md)  

## Description

Gets and sets the expression of the parameter that will be created when this SketchText is created. It can be a simple string or it can be an expression that combines text with parameter values. Simple text must be enclosed within single quotes, the same as it is required in the TEXT command dialog.  

An example of a valid expression is: "'Length: ' + lengthParam" and will result in "Length: 3.0 mm". The expression result can be obtained by using the text property on the created SketchTextInput object.

## Syntax

"sketchTextInput_var" is a variable referencing a SketchTextInput object.  

```python
# Get the value of the property.
propertyValue = sketchTextInput_var.expression

# Set the value of the property.
sketchTextInput_var.expression = propertyValue
```

## Property Value

This is a read/write property whose value is a string.

## Version

Introduced in version November 2025  

