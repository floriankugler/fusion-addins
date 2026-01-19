# AutoConstrainResult.addedConstraints Property

Parent Object: [AutoConstrainResult](AutoConstrainResult.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Returns an array of the GeometricConstraint objects that were added to constrain the sketch. If no geometric constraints were added during the auto constrain operation, this property returns an empty array.

## Syntax

"autoConstrainResult_var" is a variable referencing an AutoConstrainResult object.  

```python
# Get the value of the property.
propertyValue = autoConstrainResult_var.addedConstraints
```

## Property Value

This is a read only property whose value is an array of type [GeometricConstraint](GeometricConstraint.md).

## Samples

| Name | Description |
|----|----|
| [AutoConstrain Sample](AutoConstrainSample_Sample.md) | Demonstrates using the AutoConstrain API to automatically add geometric constraints and dimensions to a sketch. This sample creates a simple sketch with a rectangle and circle, then applies automatic constraints using the origin point as a datum. |

## Version

Introduced in version January 2026  

