# Sketch.createAutoConstrainInput Method

Parent Object: [Sketch](Sketch.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Creates a new AutoConstrainInput object associated with this sketch. The input object is used to define the various options when adding dimension and geometric constraints to help constrain a sketch. The returned object has all options defined with default values and additional constraints can be applied by passing this into the autoConstrain method.

## Syntax

"sketch_var" is a variable referencing a [Sketch](Sketch.md) object.

```python
returnValue = sketch_var.createAutoConstrainInput()
```

## Return Value

| Type | Description |
|----|----|
| [AutoConstrainInput](AutoConstrainInput.md) | Returns the newly created AutoConstrainInput object. Validation of sketch suitability (entity count, entitlements, fully constrained status, 3D vs 2D, etc.) is performed when the autoConstrain method is called, not during input creation. |

## Samples

| Name | Description |
|----|----|
| [AutoConstrain Sample](AutoConstrainSample_Sample.md) | Demonstrates using the AutoConstrain API to automatically add geometric constraints and dimensions to a sketch. This sample creates a simple sketch with a rectangle and circle, then applies automatic constraints using the origin point as a datum. |

## Version

Introduced in version January 2026  

