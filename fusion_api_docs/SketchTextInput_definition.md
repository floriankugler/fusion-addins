# SketchTextInput.definition Property

Parent Object: [SketchTextInput](SketchTextInput.md)  

## Description

Returns the SketchTextDefinition object associated with this input. When the SketchTextInput is first created this property will return null. Once one of the "set" methods have been called, this will return the SketchTextDefinition of the appropriate type and can be used to make any additional changes to the text.

## Syntax

"sketchTextInput_var" is a variable referencing a SketchTextInput object.  

```python
# Get the value of the property.
propertyValue = sketchTextInput_var.definition
```

## Property Value

This is a read only property whose value is a [SketchTextDefinition](SketchTextDefinition.md).

## Version

Introduced in version December 2020  

