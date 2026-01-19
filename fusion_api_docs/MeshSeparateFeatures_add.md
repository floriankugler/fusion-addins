# MeshSeparateFeatures.add Method

Parent Object: [MeshSeparateFeatures](MeshSeparateFeatures.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Creates a mesh separate feature.

## Syntax

"meshSeparateFeatures_var" is a variable referencing a [MeshSeparateFeatures](MeshSeparateFeatures.md) object.

```python
returnValue = meshSeparateFeatures_var.add(input)
```

## Return Value

| Type | Description |
|----|----|
| [MeshSeparateFeature](MeshSeparateFeature.md) | Returns the newly created MeshSeparateFeature object or null if the creation failed. Returns nothing in the case where the feature is non-parametric. |

## Parameters

| Name | Type | Description |
|----|----|----|
| input | [MeshSeparateFeatureInput](MeshSeparateFeatureInput.md) | A MeshSeparateFeatureInput object that defines the desired MeshSeparate feature. Use the createInput method to create a new MeshSeparateFeatureInput object and then use methods on it (the MeshSeparateFeatureInput object) to define the separation. |

## Version

Introduced in version July 2025  

