# VolumetricModelToMeshFeatures.add Method

Parent Object: [VolumetricModelToMeshFeatures](VolumetricModelToMeshFeatures.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Add a new volumetric model to mesh feature. To create a new volumetric model to mesh feature use the createInput function to create a new input object and use the methods and proprties on that object to define the required input for an volumetric model to mesh feature. Once the information is defined on the input object you can pass it to the Add method to create the Volumetric Model to Mesh.

## Syntax

"volumetricModelToMeshFeatures_var" is a variable referencing a [VolumetricModelToMeshFeatures](VolumetricModelToMeshFeatures.md) object.

```python
returnValue = volumetricModelToMeshFeatures_var.add(input)
```

## Return Value

| Type | Description |
|----|----|
| [VolumetricModelToMeshFeature](VolumetricModelToMeshFeature.md) | The newly added volumetric model to mesh feature. |

## Parameters

| Name | Type | Description |
|----|----|----|
| input | [VolumetricModelToMeshFeatureInput](VolumetricModelToMeshFeatureInput.md) | The input object for creating a volumetric model to mesh feature. |

## Version

Introduced in version May 2025  

