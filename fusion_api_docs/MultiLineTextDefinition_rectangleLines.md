# MultiLineTextDefinition.rectangleLines Property

Parent Object: [MultiLineTextDefinition](MultiLineTextDefinition.md)  

## Description

Returns the four sketch lines that define the boundary of the sketch text. By adding constraints to these lines you can associatively control the size, position and angle of the sketch text. If the MultiLineTextDefinition object is obtained from a SketchTextInput object, this property will return null because the text and it's associated lines have not been created yet.

## Syntax

"multiLineTextDefinition_var" is a variable referencing a MultiLineTextDefinition object.  

```python
# Get the value of the property.
propertyValue = multiLineTextDefinition_var.rectangleLines
```

## Property Value

This is a read only property whose value is an array of type [SketchLine](SketchLine.md).

## Version

Introduced in version December 2020  

