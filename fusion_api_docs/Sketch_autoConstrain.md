# Sketch.autoConstrain Method

Parent Object: [Sketch](Sketch.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Auto constrains the sketch using the information provided by the input object. This returns a single locally computed solution.

## Syntax

"sketch_var" is a variable referencing a [Sketch](Sketch.md) object.

```python
returnValue = sketch_var.autoConstrain(input)
```

## Return Value

| Type | Description |
|----|----|
| [AutoConstrainResult](AutoConstrainResult.md) | Returns an AutoConstrainResult object where information about how the sketch was constrained can be obtained. Returns null in the case of a failure or if the input is invalid. |

## Parameters

| Name | Type | Description |
|----|----|----|
| input | [AutoConstrainInput](AutoConstrainInput.md) | The AutoConstrainInput object that defines the various settings to use when fully constraining the sketch. The input object must be associated with this sketch (created by this sketch's createAutoConstrainInput method). |

## Samples

| Name | Description |
|----|----|
| [AutoConstrain Sample](AutoConstrainSample_Sample.md) | Demonstrates using the AutoConstrain API to automatically add geometric constraints and dimensions to a sketch. This sample creates a simple sketch with a rectangle and circle, then applies automatic constraints using the origin point as a datum. |

## Version

Introduced in version January 2026  

