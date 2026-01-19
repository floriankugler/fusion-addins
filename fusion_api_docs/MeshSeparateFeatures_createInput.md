# MeshSeparateFeatures.createInput Method

Parent Object: [MeshSeparateFeatures](MeshSeparateFeatures.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Creates a MeshSeparateFeatureInput object. Use properties and methods on this object to define the mesh separate you want to create and then use the add method, passing in the MeshSeparateFeatureInput object.

## Syntax

"meshSeparateFeatures_var" is a variable referencing a [MeshSeparateFeatures](MeshSeparateFeatures.md) object.

```python
returnValue = meshSeparateFeatures_var.createInput(mesh)
```

## Return Value

| Type | Description |
|----|----|
| [MeshSeparateFeatureInput](MeshSeparateFeatureInput.md) | Returns the newly created MeshSeparateFeatureInput object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| mesh | [Base](Base.md) | A mesh body or an object collection with face groups in either a parametric or direct modeling design. |

## Version

Introduced in version July 2025  

