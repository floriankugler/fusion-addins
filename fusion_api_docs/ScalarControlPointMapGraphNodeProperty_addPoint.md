# ScalarControlPointMapGraphNodeProperty.addPoint Method

Parent Object: [ScalarControlPointMapGraphNodeProperty](ScalarControlPointMapGraphNodeProperty.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Add a point to the map.

## Syntax

"scalarControlPointMapGraphNodeProperty_var" is a variable referencing a [ScalarControlPointMapGraphNodeProperty](ScalarControlPointMapGraphNodeProperty.md) object.

```python
returnValue = scalarControlPointMapGraphNodeProperty_var.addPoint(parameter, value, interpolator)
```

## Return Value

| Type    | Description                 |
|---------|-----------------------------|
| boolean | True if successfully added. |

## Parameters

| Name | Type | Description |
|----|----|----|
| parameter | double | Where in the input domain where the point lies. |
| value | double | The double value of the parameter in the output domain. |
| interpolator | [ControlPointInterpolators](ControlPointInterpolators.md) | The function used to interpolate an output value for a input parameter between this point and the next. |

## Version

Introduced in version May 2025  

