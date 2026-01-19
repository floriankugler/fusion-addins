# VolumetricModelToMeshFeatureInput.volumetricModel Property

Parent Object: [VolumetricModelToMeshFeatureInput](VolumetricModelToMeshFeatureInput.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Gets and sets the volumetric model to be converted to a mesh. The volumetric model must have the same parent component as the VolumetricModelToMeshFeature.This property is typed as core.Base because the adsk.fusion library does not reference the volume library where the VolumetricModel object is defined. At runtime, this property will return a VolumetricModel object.

## Syntax

"volumetricModelToMeshFeatureInput_var" is a variable referencing a VolumetricModelToMeshFeatureInput object.  

```python
# Get the value of the property.
propertyValue = volumetricModelToMeshFeatureInput_var.volumetricModel

# Set the value of the property.
volumetricModelToMeshFeatureInput_var.volumetricModel = propertyValue
```

## Property Value

This is a read/write property whose value is a [Base](Base.md).

## Version

Introduced in version May 2025  

