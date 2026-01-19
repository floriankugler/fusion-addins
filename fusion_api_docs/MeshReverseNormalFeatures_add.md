# MeshReverseNormalFeatures.add Method

Parent Object: [MeshReverseNormalFeatures](MeshReverseNormalFeatures.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Creates a mesh reverse normal feature.

## Syntax

"meshReverseNormalFeatures_var" is a variable referencing a [MeshReverseNormalFeatures](MeshReverseNormalFeatures.md) object.

```python
returnValue = meshReverseNormalFeatures_var.add(input)
```

## Return Value

| Type | Description |
|----|----|
| [MeshReverseNormalFeature](MeshReverseNormalFeature.md) | Returns the newly created MeshReverseNormalFeature object or null if the creation failed. Returns nothing in the case where the feature is non-parametric. |

## Parameters

| Name | Type | Description |
|----|----|----|
| input | [MeshReverseNormalFeatureInput](MeshReverseNormalFeatureInput.md) | A MeshReverseNormalFeatureInput object that defines the desired MeshReverseNormal feature. Use the createInput method to create a new MeshReverseNormalFeatureInput object and then use methods on it (the MeshReverseNormalFeatureInput object) to define the normal reversion. |

## Version

Introduced in version July 2025  

