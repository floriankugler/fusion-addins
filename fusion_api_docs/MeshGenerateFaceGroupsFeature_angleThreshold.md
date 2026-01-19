# MeshGenerateFaceGroupsFeature.angleThreshold Property

Parent Object: [MeshGenerateFaceGroupsFeature](MeshGenerateFaceGroupsFeature.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Controls the angle threshold during the face group generation. The values can range between 0 and pi/2. Only valid if meshGenerateFaceGroupsMethodType is FastGenerateFaceGroupsType.

## Syntax

"meshGenerateFaceGroupsFeature_var" is a variable referencing a MeshGenerateFaceGroupsFeature object.  

```python
# Get the value of the property.
propertyValue = meshGenerateFaceGroupsFeature_var.angleThreshold
```

## Property Value

This is a read only property whose value is a [ModelParameter](ModelParameter.md).

## Version

Introduced in version January 2025  

