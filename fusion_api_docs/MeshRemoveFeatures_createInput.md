# MeshRemoveFeatures.createInput Method

Parent Object: [MeshRemoveFeatures](MeshRemoveFeatures.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Creates a MeshRemoveFeatureInput object. Use properties and methods on this object to define the mesh remove feature you want to create and then use the add method, passing in the MeshRemoveFeatureInput object.

## Syntax

"meshRemoveFeatures_var" is a variable referencing a [MeshRemoveFeatures](MeshRemoveFeatures.md) object.

```python
returnValue = meshRemoveFeatures_var.createInput(inputBodies)
```

## Return Value

| Type | Description |
|----|----|
| [MeshRemoveFeatureInput](MeshRemoveFeatureInput.md) | Returns the newly created MeshRemoveFeatureInput object or null if the creation failed. |

## Parameters

| Name        | Type         | Description                                      |
|-------------|--------------|--------------------------------------------------|
| inputBodies | MeshBody\[\] | A array with mesh bodies in a parametric design. |

## Version

Introduced in version November 2025  

