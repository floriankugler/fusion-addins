# AutoConstrainInput.parentSketch Property

Parent Object: [AutoConstrainInput](AutoConstrainInput.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Returns the Sketch this object is associated with and where the dimension and geometric constraints will be added when the autoConstrain method is called. This property is read-only and is set when the input object is created by the sketch's createAutoConstrainInput method.

## Syntax

"autoConstrainInput_var" is a variable referencing an AutoConstrainInput object.  

```python
# Get the value of the property.
propertyValue = autoConstrainInput_var.parentSketch
```

## Property Value

This is a read only property whose value is a [Sketch](Sketch.md).

## Version

Introduced in version January 2026  

