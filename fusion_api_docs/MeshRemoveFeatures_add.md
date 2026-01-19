# MeshRemoveFeatures.add Method

Parent Object: [MeshRemoveFeatures](MeshRemoveFeatures.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Creates a mesh remove feature. Works only in parametric mode.

## Syntax

"meshRemoveFeatures_var" is a variable referencing a [MeshRemoveFeatures](MeshRemoveFeatures.md) object.

```python
returnValue = meshRemoveFeatures_var.add(input)
```

## Return Value

| Type | Description |
|----|----|
| [MeshRemoveFeature](MeshRemoveFeature.md)\[\] | When successfull, a MeshRemoveFeature is created for each MeshBody that was input. An array of the created MeshRemoveFeature objects is returned. |

## Parameters

| Name | Type | Description |
|----|----|----|
| input | [MeshRemoveFeatureInput](MeshRemoveFeatureInput.md) | A MeshRemoveFeatureInput object that defines the desired mesh remove feature. Use the createInput method to create a new MeshRemoveFeatureInput object and then use methods on it (the MeshRemoveFeatureInput object) to define the removal. |

## Version

Introduced in version November 2025  

