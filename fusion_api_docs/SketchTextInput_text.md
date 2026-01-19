# SketchTextInput.text Property

Parent Object: [SketchTextInput](SketchTextInput.md)  

## Description

Gets and sets the displayed text. This represents the text that results from evaluating the input formatted text. For example, if the formatted text is "'Length: ' + lengthParam", this property will return "Length: 3.0 in".  

Setting this property will overwrite any equation defined by the expression and replace it with simple text. Use the expression property to be able to define a full expression.

## Syntax

"sketchTextInput_var" is a variable referencing a SketchTextInput object.  

```python
# Get the value of the property.
propertyValue = sketchTextInput_var.text

# Set the value of the property.
sketchTextInput_var.text = propertyValue
```

## Property Value

This is a read/write property whose value is a string.

## Version

Introduced in version March 2015  

