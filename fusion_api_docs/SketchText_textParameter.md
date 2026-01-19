# SketchText.textParameter Property

Parent Object: [SketchText](SketchText.md)  

## Description

Returns the model parameter that was created when the sketch text was created that controls the contents of the sketch text. To edit the text, you can use the expression and textValue properties of the returned ModelParameter object.

## Syntax

"sketchText_var" is a variable referencing a SketchText object.  

```python
# Get the value of the property.
propertyValue = sketchText_var.textParameter
```

## Property Value

This is a read only property whose value is a [ModelParameter](ModelParameter.md).

## Version

Introduced in version November 2025  

