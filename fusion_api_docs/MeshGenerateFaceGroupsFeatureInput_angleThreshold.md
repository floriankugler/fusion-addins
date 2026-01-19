# MeshGenerateFaceGroupsFeatureInput.angleThreshold Property

Parent Object: [MeshGenerateFaceGroupsFeatureInput](MeshGenerateFaceGroupsFeatureInput.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Controls the angle threshold during the face group generation. The values can range between 0 and pi/2. The default value is 0.436. Only valid if meshGenerateFaceGroupsMethodType is FastGenerateFaceGroupsType.

## Syntax

"meshGenerateFaceGroupsFeatureInput_var" is a variable referencing a MeshGenerateFaceGroupsFeatureInput object.  

```python
# Get the value of the property.
propertyValue = meshGenerateFaceGroupsFeatureInput_var.angleThreshold

# Set the value of the property.
meshGenerateFaceGroupsFeatureInput_var.angleThreshold = propertyValue
```

## Property Value

This is a read/write property whose value is a [ValueInput](ValueInput.md).

## Version

Introduced in version January 2025  

