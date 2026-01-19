# MultiLineTextDefinition.parentSketchText Property

Parent Object: [MultiLineTextDefinition](MultiLineTextDefinition.md)  

## Description

Returns the SketchText object this definition is associated with. This property will return null in the case the definition object was obtained from a SketchTextInput object because the SketchText object does not yet exist.

## Syntax

"multiLineTextDefinition_var" is a variable referencing a MultiLineTextDefinition object.  

```python
# Get the value of the property.
propertyValue = multiLineTextDefinition_var.parentSketchText
```

## Property Value

This is a read only property whose value is a [SketchText](SketchText.md).

## Version

Introduced in version July 2022  

