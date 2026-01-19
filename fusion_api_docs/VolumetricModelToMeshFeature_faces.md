# VolumetricModelToMeshFeature.faces Property

Parent Object: [VolumetricModelToMeshFeature](VolumetricModelToMeshFeature.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Returns the faces that were created by this feature. This works for both parametric and non-parametric features.  

Depending on the modifications made to the body after the feature was created, this may not return all of the faces. For example, when a component is created from a body, the original body and its faces no longer exist, so this won't return any faces. However, you can roll the timeline to immediately after the feature, and all the original faces will be available.

## Syntax

"volumetricModelToMeshFeature_var" is a variable referencing a VolumetricModelToMeshFeature object.  

```python
# Get the value of the property.
propertyValue = volumetricModelToMeshFeature_var.faces
```

## Property Value

This is a read only property whose value is a [BRepFaces](BRepFaces.md).

## Version

Introduced in version May 2025  

