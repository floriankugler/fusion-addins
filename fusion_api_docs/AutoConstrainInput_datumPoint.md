# AutoConstrainInput.datumPoint Property

Parent Object: [AutoConstrainInput](AutoConstrainInput.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Gets and sets an optional datum point that the dimensions will be based on. This defaults to null, which indicates there is no datum point specified. When no datum point is provided, AutoConstrain will automatically select an appropriate datum based on the sketch content and geometry.

## Syntax

"autoConstrainInput_var" is a variable referencing an AutoConstrainInput object.  

```python
# Get the value of the property.
propertyValue = autoConstrainInput_var.datumPoint

# Set the value of the property.
autoConstrainInput_var.datumPoint = propertyValue
```

## Property Value

This is a read/write property whose value is a [SketchPoint](SketchPoint.md).

## Samples

| Name | Description |
|----|----|
| [AutoConstrain Sample](AutoConstrainSample_Sample.md) | Demonstrates using the AutoConstrain API to automatically add geometric constraints and dimensions to a sketch. This sample creates a simple sketch with a rectangle and circle, then applies automatic constraints using the origin point as a datum. |

## Version

Introduced in version January 2026  

