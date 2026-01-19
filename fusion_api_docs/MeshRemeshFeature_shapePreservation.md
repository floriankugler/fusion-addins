# MeshRemeshFeature.shapePreservation Property

Parent Object: [MeshRemeshFeature](MeshRemeshFeature.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Gets and sets how much of the original shape needs to preserved. The value can range between 0 and 1. Only valid if meshRemeshMethodType is AdaptiveType.

## Syntax

"meshRemeshFeature_var" is a variable referencing a MeshRemeshFeature object.  

```python
# Get the value of the property.
propertyValue = meshRemeshFeature_var.shapePreservation
```

## Property Value

This is a read only property whose value is a [ModelParameter](ModelParameter.md).

## Version

Introduced in version March 2024  

