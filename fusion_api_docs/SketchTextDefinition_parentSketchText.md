# SketchTextDefinition.parentSketchText Property

Parent Object: [SketchTextDefinition](SketchTextDefinition.md)  

## Description

Returns the SketchText object this definition is associated with. This property will return null in the case the definition object was obtained from a SketchTextInput object because the SketchText object does not yet exist.

## Syntax

"sketchTextDefinition_var" is a variable referencing a SketchTextDefinition object.  

```python
# Get the value of the property.
propertyValue = sketchTextDefinition_var.parentSketchText
```

## Property Value

This is a read only property whose value is a [SketchText](SketchText.md).

## Version

Introduced in version July 2022  

