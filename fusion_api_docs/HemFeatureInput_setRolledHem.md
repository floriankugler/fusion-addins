# HemFeatureInput.setRolledHem Method

Parent Object: [HemFeatureInput](HemFeatureInput.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Sets the hem input with the values to be used in order to create a rolled hem feature.

## Syntax

"hemFeatureInput_var" is a variable referencing a [HemFeatureInput](HemFeatureInput.md) object.

```python
returnValue = hemFeatureInput_var.setRolledHem(edge, radius, angle, isFlipped, bendPositionType)
```

## Return Value

| Type    | Description                                     |
|---------|-------------------------------------------------|
| boolean | Returns true if defining the hem is successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| edge | [BRepEdge](BRepEdge.md) | The BRepEdge that defines the location of the hem. |
| radius | [ValueInput](ValueInput.md) | The radius of the rolled hem. |
| angle | [ValueInput](ValueInput.md) | The angle of the rolled hem. |
| isFlipped | boolean | Indicates if the hem direction is flipped. |
| bendPositionType | [BendPositionTypes](BendPositionTypes.md) | The bend location type for the hem. |

## Version

Introduced in version September 2025  

