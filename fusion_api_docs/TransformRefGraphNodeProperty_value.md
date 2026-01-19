# TransformRefGraphNodeProperty.value Property

Parent Object: [TransformRefGraphNodeProperty](TransformRefGraphNodeProperty.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Get or set the value of the property. This should be the occurrence of a component.

## Syntax

"transformRefGraphNodeProperty_var" is a variable referencing a TransformRefGraphNodeProperty object.  

```python
# Get the value of the property.
propertyValue = transformRefGraphNodeProperty_var.value

# Set the value of the property.
transformRefGraphNodeProperty_var.value = propertyValue
```

## Property Value

This is a read/write property whose value is an [Occurrence](Occurrence.md).

## Version

Introduced in version May 2025  

